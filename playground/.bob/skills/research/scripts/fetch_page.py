#!/usr/bin/env python3
"""Fetch a URL, cache the raw page for the citation checker, print readable text.

Usage: python fetch_page.py URL --tag S3 [--cache ./sources] [--grep "phrase"]

Writes <cache>/S3.html (raw) and <cache>/S3.txt (text), prints the text (truncated to
--max-chars, default 12000) so you can copy an exact quote. --grep prints only the
lines containing the phrase, with 1 line of context, which is the fastest way to find
the sentence to quote.
"""
import argparse
import html
import re
import subprocess
import sys
from pathlib import Path


def to_text(raw: str) -> str:
    raw = re.sub(r"(?is)<(script|style|noscript|svg|nav|footer|header)[^>]*>.*?</\1>", " ", raw)
    raw = re.sub(r"(?i)<br\s*/?>|</p>|</div>|</li>|</h[1-6]>|</tr>", "\n", raw)
    txt = html.unescape(re.sub(r"<[^>]+>", " ", raw))
    lines = [re.sub(r"[ \t]+", " ", ln).strip() for ln in txt.splitlines()]
    return "\n".join(ln for ln in lines if ln)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("--tag", required=True)
    ap.add_argument("--cache", default="sources")
    ap.add_argument("--grep")
    ap.add_argument("--max-chars", type=int, default=12000)
    a = ap.parse_args()
    r = subprocess.run(["curl", "-sS", "-L", "--max-time", "40", "-A", "Mozilla/5.0 (research-fetch)",
                        "-w", "\n%{http_code} %{url_effective}", a.url], capture_output=True, text=True, errors="replace")
    body, _, status = r.stdout.rpartition("\n")
    code = status.split(" ")[0] if status else "0"
    if not code.isdigit() or int(code) >= 400 or int(code) == 0:
        print(f"FETCH FAILED: HTTP {code} {a.url}\n{r.stderr.strip()[:300]}", file=sys.stderr)
        sys.exit(1)
    Path(a.cache).mkdir(parents=True, exist_ok=True)
    (Path(a.cache) / f"{a.tag}.html").write_text(body, encoding="utf-8")
    text = to_text(body)
    (Path(a.cache) / f"{a.tag}.txt").write_text(text, encoding="utf-8")
    print(f"# {a.tag}: HTTP {status.strip()} | {len(text)} chars | cached {a.cache}/{a.tag}.html")
    if a.grep:
        lines = text.splitlines()
        hits = [i for i, ln in enumerate(lines) if a.grep.lower() in ln.lower()]
        if not hits:
            print(f"(no line contains {a.grep!r}; try a shorter phrase)")
        for i in hits[:20]:
            print("\n".join(lines[max(0, i - 1): i + 2]))
            print("---")
    else:
        print(text[: a.max_chars])
        if len(text) > a.max_chars:
            print(f"\n[... truncated; {len(text) - a.max_chars} more chars in {a.cache}/{a.tag}.txt]")


if __name__ == "__main__":
    main()
