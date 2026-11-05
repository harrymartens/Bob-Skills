#!/usr/bin/env python3
"""IBM documentation MCP server (stdio).

Tools
  search_ibm_docs(query, product_key="", limit=10, start=0)  -> ranked topics from www.ibm.com/docs
  fetch_ibm_doc(href_or_url, max_chars=20000)                 -> one topic as clean text, with its canonical URL
  list_ibm_products(query)                                    -> product keys for scoping searches
  get_ibm_toc(product_key, section="", depth=2)               -> table of contents subtree for a product version
  search_bob_docs(query, limit=10)                            -> pages from bob.ibm.com/docs (sitemap keyword index)
  fetch_bob_doc(url, max_chars=20000)                         -> one bob.ibm.com/docs page as clean text

Evidence for the endpoints is in ../../docs/ibm-docs-mcp-feasibility.md. The API is undocumented;
responses are cached on disk for an hour (the server's own cache-control) and the client identifies
itself honestly. Works with mcp>=1.2 (FastMCP) and mcp 2.x (MCPServer); stdlib HTTP only.

Run:  python3 server.py            (stdio, what Bob's mcp.json uses)
Test: python3 selftest.py          (spawns this server over stdio and calls each tool)
"""
from __future__ import annotations

import gzip
import hashlib
import html
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

try:  # mcp 2.x
    from mcp.server.mcpserver import MCPServer as _Server
except ImportError:  # mcp 1.x
    from mcp.server.fastmcp import FastMCP as _Server  # type: ignore

API = "https://www.ibm.com/docs/api/v1"
UA = "Mozilla/5.0 (compatible; bob-skills-ibm-docs/0.1; +https://github.com/harrymartens/Bob-Skills)"
CACHE_DIR = Path(os.environ.get("IBM_DOCS_CACHE", Path.home() / ".cache" / "ibm-docs-mcp"))
CACHE_TTL = int(os.environ.get("IBM_DOCS_CACHE_TTL", "3600"))
TIMEOUT = 40

mcp = _Server("ibm-docs", instructions="Search and read IBM product documentation (www.ibm.com/docs) and IBM Bob docs (bob.ibm.com/docs). Search first, then fetch the href the search returned. Quote the fetched text; do not answer from memory.")


# ---------------------------------------------------------------- HTTP + cache
def _get(url: str, accept: str = "*/*") -> bytes:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    key = CACHE_DIR / (hashlib.sha256(url.encode()).hexdigest() + ".bin")
    if key.exists() and time.time() - key.stat().st_mtime < CACHE_TTL:
        return key.read_bytes()
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": accept, "Accept-Encoding": "gzip"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        data = r.read()
        if r.headers.get("Content-Encoding") == "gzip":
            data = gzip.decompress(data)
    key.write_bytes(data)
    return data


def _get_json(url: str):
    return json.loads(_get(url, "application/json").decode("utf-8", "replace"))


def _strip_tags(s: str) -> str:
    return html.unescape(re.sub(r"<[^>]+>", "", s or "")).strip()


# ---------------------------------------------------------------- HTML -> text
class _Text(HTMLParser):
    """Keeps <article>/<main> prose, drops nav/script/style, renders headings, lists, code, tables."""
    BLOCK = {"p", "div", "li", "tr", "h1", "h2", "h3", "h4", "h5", "h6", "pre", "section", "article", "dt", "dd", "br", "table"}
    SKIP = {"script", "style", "noscript", "nav", "header", "footer", "svg", "button"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out: list[str] = []
        self.skip = 0
        self.in_article = 0
        self.has_article = False
        self.cell = False
        self.title = ""
        self._in_title = False
        self.canonical = ""

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "title":
            self._in_title = True
        if tag == "link" and a.get("rel") == "canonical":
            self.canonical = a.get("href", "")
        if tag in ("article", "main"):
            self.in_article += 1
            self.has_article = True
        if tag in self.SKIP or (tag == "aside"):
            self.skip += 1
            return
        if self.skip:
            return
        if tag in ("h1", "h2", "h3", "h4"):
            self.out.append("\n\n" + "#" * int(tag[1]) + " ")
        elif tag == "li":
            self.out.append("\n- ")
        elif tag == "pre":
            self.out.append("\n```\n")
        elif tag in ("td", "th"):
            self.out.append(" | ")
            self.cell = True
        elif tag in self.BLOCK:
            self.out.append("\n")

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        if tag in self.SKIP or tag == "aside":
            self.skip = max(0, self.skip - 1)
            return
        if tag in ("article", "main"):
            self.in_article = max(0, self.in_article - 1)
        if self.skip:
            return
        if tag == "pre":
            self.out.append("\n```\n")
        elif tag in ("td", "th"):
            self.cell = False
        elif tag in self.BLOCK:
            self.out.append("\n")

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        if self.skip or (self.has_article and not self.in_article):
            return
        self.out.append(data if self.cell or "```" in "".join(self.out[-3:]) else re.sub(r"\s+", " ", data))

    def text(self) -> str:
        t = "".join(self.out)
        t = re.sub(r"[ \t]+\n", "\n", t)
        t = re.sub(r"\n{3,}", "\n\n", t)
        return t.strip()


def html_to_text(raw: str) -> tuple[str, str, str]:
    p = _Text()
    p.feed(raw)
    return p.text(), p.title.strip(), p.canonical


def _clip(s: str, n: int) -> str:
    return s if len(s) <= n else s[:n] + f"\n\n[... truncated, {len(s) - n} more chars; call again with a higher max_chars]"


# ---------------------------------------------------------------- IBM docs tools
@mcp.tool()
def search_ibm_docs(query: str, product_key: str = "", limit: int = 10, start: int = 0) -> str:
    """Search www.ibm.com/docs. product_key scopes to one product version, e.g. SSEPGG_12.1.0 (Db2 12.1),
    SSRD57H_3.0.0 (IBM Bob Premium Package for Z); find keys with list_ibm_products. Returns JSON with
    hits, next, and topics [{title, snippet, href, url, product, date}]. Pass a topic's href to fetch_ibm_doc."""
    q = urllib.parse.urlencode({"query": query, "lang": "en", "start": start, "limit": max(1, min(limit, 25)), "fallback": "true"})
    if product_key:
        q += "&products=" + urllib.parse.quote(product_key)
    try:
        data = _get_json(f"{API}/search?{q}")
    except urllib.error.HTTPError as e:
        return json.dumps({"error": f"HTTP {e.code}", "url": f"{API}/search?{q}"})
    topics = [{
        "title": _strip_tags(t.get("title")),
        "snippet": _strip_tags(t.get("snippet")),
        "href": t.get("href"),
        "url": t.get("fullurl"),
        "product": (t.get("product") or {}).get("label"),
        "product_key": (t.get("product") or {}).get("key"),
        "date": t.get("date"),
    } for t in data.get("topics", [])]
    return json.dumps({"hits": data.get("hits"), "start": data.get("start"), "next": data.get("next"), "topics": topics}, indent=1)


@mcp.tool()
def fetch_ibm_doc(href_or_url: str, max_chars: int = 20000) -> str:
    """Fetch one IBM docs topic as clean text. Accepts the href from search_ibm_docs
    (e.g. SSEPGG_12.1.0/com.ibm.db2.luw.messages.db2.doc/doc/rdb2msg.html) or a full
    https://www.ibm.com/docs/en/...?topic=... URL. Returns title, canonical URL and the article text."""
    s = href_or_url.strip()
    if s.startswith("http"):
        url = s
    else:
        url = f"{API}/content/{s.lstrip('/')}"
    try:
        raw = _get(url, "text/html").decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return json.dumps({"error": f"HTTP {e.code}", "url": url, "hint": "unknown href; use the exact href from search_ibm_docs"})
    text, title, canonical = html_to_text(raw)
    if "Bot Index" in title or len(raw) > 1_500_000:
        return json.dumps({"error": "topic not found (landing page returned)", "url": url,
                           "hint": "use the href from search_ibm_docs or get_ibm_toc; product landing pages have no article text"})
    if not canonical and not s.startswith("http"):
        canonical = url
    return json.dumps({"title": title, "url": canonical or url, "chars": len(text), "text": _clip(text, max_chars)}, indent=1)


@mcp.tool()
def list_ibm_products(query: str, limit: int = 20) -> str:
    """Find IBM product keys by name substring (e.g. 'Db2', 'Bob', 'watsonx Code Assistant').
    Returns [{name, key, url_key}]. Search results carry the versioned key (KEY_version) to use in search_ibm_docs."""
    try:
        data = _get_json(f"{API}/products")
    except urllib.error.HTTPError as e:
        return json.dumps({"error": f"HTTP {e.code}"})
    ql = query.lower()
    rows = [{"name": p.get("name"), "key": p.get("key"), "url_key": p.get("productUrlKey")}
            for p in data if ql in (p.get("name") or "").lower() or ql in (p.get("productUrlKey") or "").lower()]
    return json.dumps(rows[:limit], indent=1)


def _walk(node, depth, max_depth, section, out, prefix=""):
    label = node.get("label") or ""
    href = node.get("href") or ""
    if section and section.lower() not in label.lower() and prefix == "":
        pass
    out.append({"title": prefix + label, "href": href})
    if depth < max_depth:
        for ch in node.get("topics") or []:
            _walk(ch, depth + 1, max_depth, section, out, prefix + "  ")


@mcp.tool()
def get_ibm_toc(product_key: str, section: str = "", depth: int = 2, max_entries: int = 200) -> str:
    """Table of contents for a product version key (e.g. SSRD57H_3.0.0). section narrows to the first
    subtree whose label contains that text. Returns [{title (indented by level), href}] usable with fetch_ibm_doc."""
    try:
        data = _get_json(f"{API}/toc/{urllib.parse.quote(product_key)}")
    except urllib.error.HTTPError as e:
        return json.dumps({"error": f"HTTP {e.code}", "hint": "use a versioned key such as SSEPGG_12.1.0"})
    root = data.get("toc") or data
    if section:
        stack = [root]
        found = None
        while stack and not found:
            n = stack.pop(0)
            if section.lower() in (n.get("label") or "").lower():
                found = n
            stack.extend(n.get("topics") or [])
        if not found:
            return json.dumps({"error": f"no TOC section containing {section!r}"})
        root = found
    out: list = []
    _walk(root, 0, depth, section, out)
    return json.dumps({"entries": len(out), "toc": out[:max_entries]}, indent=1)


# ---------------------------------------------------------------- Bob docs tools
BOB_SITEMAP = "https://bob.ibm.com/sitemap.xml"


def _bob_pages() -> list[dict]:
    raw = _get(BOB_SITEMAP, "application/xml").decode("utf-8", "replace")
    locs = re.findall(r"<loc>(https://bob\.ibm\.com/docs/[^<]+)</loc>", raw)
    pages = sorted({u for u in locs if not re.search(r"/docs/(?:[a-z]{2}(?:-[a-z]{2})?)/", u) or "/docs/ide/" in u or "/docs/shell/" in u})
    return [{"url": u, "words": re.sub(r"[-/_]", " ", u.split("/docs/")[-1]).lower()} for u in pages]


@mcp.tool()
def search_bob_docs(query: str, limit: int = 10) -> str:
    """Search IBM Bob documentation (bob.ibm.com/docs: Bob IDE and Bob Shell) by keywords against page paths
    from the site's sitemap; there is no server-side search. Returns [{url, path}]. Then fetch_bob_doc(url)."""
    terms = [t for t in re.findall(r"[a-z0-9]+", query.lower()) if len(t) > 1]
    scored = []
    for p in _bob_pages():
        score = sum(2 if t in p["words"].split() else 1 if t in p["words"] else 0 for t in terms)
        if score:
            scored.append((score, p["url"]))
    scored.sort(key=lambda x: (-x[0], x[1]))
    return json.dumps([{"url": u, "path": u.split("bob.ibm.com", 1)[1], "score": s} for s, u in scored[:limit]], indent=1)


@mcp.tool()
def fetch_bob_doc(url: str, max_chars: int = 20000) -> str:
    """Fetch one bob.ibm.com/docs page (server-rendered) as clean text: title, url, text."""
    if not url.startswith("https://bob.ibm.com/"):
        return json.dumps({"error": "only https://bob.ibm.com/ URLs"})
    try:
        raw = _get(url, "text/html").decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return json.dumps({"error": f"HTTP {e.code}", "url": url})
    text, title, _ = html_to_text(raw)
    return json.dumps({"title": title, "url": url, "chars": len(text), "text": _clip(text, max_chars)}, indent=1)


if __name__ == "__main__":
    mcp.run("stdio")
