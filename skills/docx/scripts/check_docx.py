#!/usr/bin/env python3
"""Programmatic QA for a .docx report. Exit 1 on any ERROR.

Usage: python check_docx.py report.docx [--min-words N] [--max-words N] [--require-headings "Summary,Findings"] [--json]

Checks:
  open              python-docx opens it
  word-count        body words within bounds
  headings          uses real Heading styles (not bold normal text) and required headings exist
  leftover-text     lorem/TODO/[insert]/bracket placeholders
  empty-table-cell  tables with blank cells
  literal-bullets   paragraphs starting with a typed "•" or "- " instead of a list style
  fake-heading      short bold paragraph in Normal style that looks like a heading (WARN)
  long-paragraph    paragraph over 180 words (WARN)
  newline-in-run    "\\n" inside a run (should be separate paragraphs)
"""
import argparse
import json
import re
import sys

try:
    from docx import Document
except ImportError:
    print("pip install python-docx", file=sys.stderr)
    sys.exit(2)

LEFTOVER = re.compile(
    r"(\blorem\b|\bipsum\b|\bTODO\b|\bTBD\b|\bFIXME\b|placeholder text|\[insert[^\]]*\]|"
    r"\[(?:your|author|date|name|team|company|client)[^\]]*\]|\bx{4,}\b)", re.I)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("doc")
    ap.add_argument("--min-words", type=int, default=50)
    ap.add_argument("--max-words", type=int, default=100000)
    ap.add_argument("--require-headings", default="")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    findings = []

    def add(level, check, msg):
        findings.append({"level": level, "check": check, "msg": msg})

    try:
        d = Document(a.doc)
    except Exception as e:  # noqa: BLE001
        add("ERROR", "open", str(e))
        return report(findings, a.json)

    words = 0
    headings = []
    for p in d.paragraphs:
        t = p.text.strip()
        if not t:
            continue
        words += len(t.split())
        style = (p.style.name or "") if p.style is not None else ""
        if style.lower().startswith("heading") or style.lower() == "title":
            headings.append(t)
        if LEFTOVER.search(t):
            add("ERROR", "leftover-text", f"{LEFTOVER.search(t).group(0)!r} in: {t[:70]}")
        if re.match(r"^[•\-\*]\s", t) and "list" not in style.lower():
            add("ERROR", "literal-bullets", f"typed bullet instead of list style: {t[:60]}")
        if len(t.split()) > 180:
            add("WARN", "long-paragraph", f"{len(t.split())} words: {t[:50]}...")
        if (not style.lower().startswith("heading")) and len(t.split()) <= 8 and p.runs and all(r.bold for r in p.runs if r.text.strip()):
            add("WARN", "fake-heading", f"bold Normal paragraph looks like a heading: {t[:60]}")
        for r in p.runs:
            if "\n" in r.text:
                add("ERROR", "newline-in-run", f"literal newline in run: {r.text[:40]!r}")

    for ti, tbl in enumerate(d.tables, 1):
        for ri, row in enumerate(tbl.rows):
            for ci, cell in enumerate(row.cells):
                if not cell.text.strip():
                    add("ERROR", "empty-table-cell", f"table {ti} row {ri + 1} col {ci + 1} is blank")
                else:
                    words += len(cell.text.split())

    if words < a.min_words or words > a.max_words:
        add("ERROR", "word-count", f"{words} words, expected {a.min_words}-{a.max_words}")
    if not headings:
        add("ERROR", "headings", "no Heading-styled paragraphs; a report needs real headings for navigation/TOC")
    for req in [h.strip() for h in a.require_headings.split(",") if h.strip()]:
        if not any(req.lower() in h.lower() for h in headings):
            add("ERROR", "headings", f"required heading missing: {req!r}")

    return report(findings, a.json, words, headings)


def report(findings, as_json, words=None, headings=None):
    errors = [f for f in findings if f["level"] == "ERROR"]
    if as_json:
        print(json.dumps({"words": words, "headings": headings, "errors": len(errors), "findings": findings}, indent=2))
    else:
        for f in findings:
            print(f"{f['level']:5} {f['check']:16} {f['msg']}")
        print(f"\n{words} words, {len(headings or [])} headings, {len(errors)} errors")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
