#!/usr/bin/env python3
"""Programmatic QA for a generated PDF. Exit 1 on any ERROR.

Usage: python check_pdf.py out.pdf [--min-pages N] [--max-pages N] [--require-text "a,b"] [--json]

Checks:
  open          pypdf opens it and it is not encrypted
  page-count    within bounds
  empty-page    a page with fewer than 5 words of extractable text (WARN if it has images)
  leftover-text lorem/TODO/[insert]/bracket placeholders
  require-text  each required phrase appears somewhere
  metadata      Title metadata present (WARN)
  fonts         every font referenced is embedded (WARN; unembedded fonts render differently elsewhere)
"""
import argparse
import json
import re
import sys

try:
    from pypdf import PdfReader
except ImportError:
    print("pip install pypdf", file=sys.stderr)
    sys.exit(2)

LEFTOVER = re.compile(r"(\blorem\b|\bipsum\b|\bTODO\b|\bTBD\b|\bTBC\b|\bFIXME\b|\[(?!S?\d+\])[A-Za-z][^\]\n]{1,40}\]|\bx{4,}\b)", re.I)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("--min-pages", type=int, default=1)
    ap.add_argument("--max-pages", type=int, default=10000)
    ap.add_argument("--require-text", default="")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    findings = []

    def add(level, check, msg):
        findings.append({"level": level, "check": check, "msg": msg})

    try:
        r = PdfReader(a.pdf)
        if r.is_encrypted:
            add("ERROR", "open", "PDF is encrypted")
            return report(findings, a.json)
    except Exception as e:  # noqa: BLE001
        add("ERROR", "open", str(e))
        return report(findings, a.json)

    n = len(r.pages)
    if n < a.min_pages or n > a.max_pages:
        add("ERROR", "page-count", f"{n} pages, expected {a.min_pages}-{a.max_pages}")

    all_text = []
    unembedded = set()
    for i, page in enumerate(r.pages, 1):
        t = page.extract_text() or ""
        all_text.append(t)
        has_images = bool(getattr(page, "images", None) and len(page.images) > 0)
        if len(t.split()) < 5:
            add("WARN" if has_images else "ERROR", "empty-page", f"page {i} has {len(t.split())} words")
        m = LEFTOVER.search(t)
        if m:
            add("ERROR", "leftover-text", f"page {i}: {m.group(0)!r}")
        try:
            res = page.get("/Resources") or {}
            fonts = res.get("/Font") or {}
            for k in fonts:
                f = fonts[k].get_object()
                desc = f.get("/FontDescriptor")
                if desc is None and f.get("/Subtype") != "/Type0":
                    unembedded.add(str(f.get("/BaseFont")))
                elif desc is not None:
                    d = desc.get_object()
                    if not any(key in d for key in ("/FontFile", "/FontFile2", "/FontFile3")):
                        unembedded.add(str(f.get("/BaseFont")))
        except Exception:  # noqa: BLE001
            pass

    joined = "\n".join(all_text)
    for req in [s.strip() for s in a.require_text.split(",") if s.strip()]:
        if req.lower() not in joined.lower():
            add("ERROR", "require-text", f"missing phrase: {req!r}")
    if not (r.metadata and r.metadata.title):
        add("WARN", "metadata", "no Title metadata")
    for f in sorted(unembedded):
        add("WARN", "fonts", f"font not embedded: {f}")

    return report(findings, a.json, n, len(joined.split()))


def report(findings, as_json, pages=None, words=None):
    errors = [f for f in findings if f["level"] == "ERROR"]
    if as_json:
        print(json.dumps({"pages": pages, "words": words, "errors": len(errors), "findings": findings}, indent=2))
    else:
        for f in findings:
            print(f"{f['level']:5} {f['check']:14} {f['msg']}")
        print(f"\n{pages} pages, {words} words, {len(errors)} errors")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
