#!/usr/bin/env python3
"""Verify that every claim in a research document is backed by a live source that
actually contains the quoted evidence. Exit 1 on any failure.

Document contract (see ../SKILL.md):
  * A claim line carries one or more tags like [S3].
  * A "## Sources" section lists each tag once:
        [S3] https://example.com/page — "exact words copied from the page"
    The quote must be at least 6 words and appear verbatim (whitespace-normalised,
    case-insensitive) in the fetched page text, or in a cached copy saved by the run.

Usage:
    python check_citations.py research.md [--cache DIR] [--offline] [--json]

--cache DIR   directory where the run saved each fetched page as <tag>.html/.txt
--offline     only use the cache; do not hit the network
"""
import argparse
import html
import json
import re
import subprocess
import sys
from pathlib import Path

TAG = re.compile(r"\[S(\d+)\]")
SOURCE_LINE = re.compile(r"^\s*\[S(\d+)\]\s+(\S+)\s+[—–-]+\s+[\"“](.+?)[\"”]\s*$")


def norm(s: str) -> str:
    s = html.unescape(re.sub(r"<[^>]+>", " ", s))
    return re.sub(r"\s+", " ", s).strip().lower()


def fetch(url: str, timeout=30) -> tuple[int, str]:
    try:
        r = subprocess.run(
            ["curl", "-sS", "-L", "--max-time", str(timeout), "-A", "Mozilla/5.0 (research-check)",
             "-w", "\n%{http_code}", url],
            capture_output=True, text=True, errors="replace",
        )
    except FileNotFoundError:
        return 0, ""
    body, _, code = r.stdout.rpartition("\n")
    try:
        return int(code), body
    except ValueError:
        return 0, ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("doc")
    ap.add_argument("--cache")
    ap.add_argument("--offline", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--min-words", type=int, default=6)
    a = ap.parse_args()

    text = Path(a.doc).read_text(encoding="utf-8", errors="replace")
    head, _, sources_part = text.partition("## Sources")
    findings = []

    def add(level, tag, msg):
        findings.append({"level": level, "tag": tag, "msg": msg})

    sources = {}
    for line in sources_part.splitlines():
        m = SOURCE_LINE.match(line)
        if m:
            sources[m.group(1)] = (m.group(2), m.group(3))
        elif line.strip().startswith("[S"):
            add("ERROR", line.strip()[:6], f"malformed source line (need: [Sn] URL — \"quote\"): {line.strip()[:80]}")

    used = set(TAG.findall(head))
    if not used:
        add("ERROR", "-", "no [Sn] citation tags found in the body")
    for t in sorted(used, key=int):
        if t not in sources:
            add("ERROR", f"S{t}", "cited in body but missing from ## Sources")
    for t in sources:
        if t not in used:
            add("WARN", f"S{t}", "listed in ## Sources but never cited")

    # claims without a tag: any bullet/numbered line or sentence with a number/percentage/date and no tag
    for ln in head.splitlines():
        s = ln.strip()
        if not s or s.startswith("#") or s.startswith(">") or s.startswith("|"):
            continue
        if re.match(r"^(?:[-*•]|\d+[.)])\s+", s) and not TAG.search(s) and len(s.split()) >= 6:
            add("WARN", "-", f"untagged claim: {s[:90]}")

    for t, (url, quote) in sources.items():
        if len(quote.split()) < a.min_words:
            add("ERROR", f"S{t}", f"quote too short ({len(quote.split())} words); copy a full sentence")
            continue
        page = None
        if a.cache:
            for ext in (".html", ".txt", ".md"):
                cp = Path(a.cache) / f"S{t}{ext}"
                if cp.exists():
                    page = cp.read_text(encoding="utf-8", errors="replace")
                    break
        if page is None and not a.offline:
            code, page = fetch(url)
            if code == 0 or code >= 400:
                add("ERROR", f"S{t}", f"HTTP {code} for {url}")
                continue
        if page is None:
            add("ERROR", f"S{t}", f"no cached copy and --offline set: {url}")
            continue
        if norm(quote) in norm(page):
            add("OK", f"S{t}", f"quote found at {url}")
        else:
            add("ERROR", f"S{t}", f"quote NOT found on page: \"{quote[:60]}...\" ({url})")

    errors = [f for f in findings if f["level"] == "ERROR"]
    if a.json:
        print(json.dumps({"errors": len(errors), "sources": len(sources), "findings": findings}, indent=2))
    else:
        for f in findings:
            print(f"{f['level']:5} {f['tag']:5} {f['msg']}")
        print(f"\n{len(sources)} sources, {len(used)} cited, {len(errors)} errors")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
