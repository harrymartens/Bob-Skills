#!/usr/bin/env python3
"""Programmatic QA for a .pptx deck. Exit 1 when any ERROR is found.

Usage:
    python check_pptx.py deck.pptx [--min-slides N] [--max-slides N] [--json]

Checks (no human eyes required):
  open            file opens with python-pptx
  slide-count     within --min-slides/--max-slides
  empty-shape     placeholder or text box that contains no text and no picture
  leftover-text   lorem/TODO/[insert]/XXX style template residue
  off-slide       shape extends past the slide boundary
  overflow        estimated wrapped text height exceeds its box (font metrics)
  overlap         two text-bearing shapes whose boxes intersect
  tiny-font       any run below 10pt (body) in a non-footer shape
  no-title        slide has no title-like text (WARN only)
  text-wall       more than 120 words on one slide (WARN only)
"""
import argparse
import json
import re
import sys
from pathlib import Path

try:
    from pptx import Presentation
    from pptx.util import Emu, Pt
    from PIL import ImageFont
except ImportError as e:  # pragma: no cover
    print(f"missing dependency: {e}. pip install python-pptx pillow", file=sys.stderr)
    sys.exit(2)

# Bracketed placeholders start with a letter ([Owner TBC], [Name]); citation tags ([S1], [12]) are digits.
LEFTOVER = re.compile(
    r"(\blorem\b|\bipsum\b|\bTODO\b|\bTBD\b|\bTBC\b|\bFIXME\b|placeholder text|click to add|"
    r"\[(?!S?\d+\])[A-Za-z][^\]\n]{1,40}\]|\bx{4,}\b)",
    re.I,
)
EMU_PER_PT = 12700
DEFAULT_PT = 18.0
LINE_SPACING = 1.2
INSET_EMU = Emu(91440)  # python-pptx default text frame inset (0.1")

# Metric-compatible stand-ins. Serif and bold variants are wider, so a wrong guess
# under-estimates and lets overflow through; when unsure we pick the wider family.
FONT_CANDIDATES = {
    "sans": [
        "/usr/share/fonts/truetype/crosextra/Carlito-Regular.ttf",          # Calibri clone
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",  # Arial clone
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "C:/Windows/Fonts/calibri.ttf", "C:/Windows/Fonts/arial.ttf",
        "/Library/Fonts/Arial.ttf", "/System/Library/Fonts/Supplemental/Arial.ttf",
    ],
    "sans-bold": [
        "/usr/share/fonts/truetype/crosextra/Carlito-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "C:/Windows/Fonts/calibrib.ttf", "C:/Windows/Fonts/arialbd.ttf",
        "/Library/Fonts/Arial Bold.ttf", "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    ],
    "serif": [
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
        "C:/Windows/Fonts/georgia.ttf", "C:/Windows/Fonts/times.ttf",
        "/Library/Fonts/Georgia.ttf", "/System/Library/Fonts/Supplemental/Georgia.ttf",
    ],
    "serif-bold": [
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
        "C:/Windows/Fonts/georgiab.ttf", "C:/Windows/Fonts/timesbd.ttf",
        "/Library/Fonts/Georgia Bold.ttf", "/System/Library/Fonts/Supplemental/Georgia Bold.ttf",
    ],
}
SERIF_HINTS = ("georgia", "cambria", "times", "garamond", "palatino", "book", "serif", "century", "constantia")
_font_cache = {}


def font_key(family: str | None, bold: bool) -> str:
    fam = (family or "").lower()
    serif = any(h in fam for h in SERIF_HINTS)
    return ("serif" if serif else "sans") + ("-bold" if bold else "")


def load_font(size_pt: float, family=None, bold=False):
    key = (font_key(family, bold), int(round(size_pt * 4)))
    if key in _font_cache:
        return _font_cache[key]
    f = None
    for p in FONT_CANDIDATES[key[0]] + FONT_CANDIDATES["sans"]:
        if Path(p).exists():
            try:
                f = ImageFont.truetype(p, key[1])  # 4x for precision
                break
            except OSError:
                continue
    _font_cache[key] = f
    return f


def text_width_pt(text: str, size_pt: float, family=None, bold=False) -> float:
    f = load_font(size_pt, family, bold)
    if f is None:
        return len(text) * size_pt * (0.55 if bold else 0.5)  # crude fallback
    return f.getlength(text) / 4.0


def wrapped_lines(text: str, size_pt: float, width_pt: float, family=None, bold=False) -> int:
    if width_pt <= 0:
        return max(1, len(text.split()))
    lines = 0
    for para in text.split("\n"):
        words = para.split()
        if not words:
            lines += 1
            continue
        cur = ""
        n = 1
        for w in words:
            trial = (cur + " " + w).strip()
            if text_width_pt(trial, size_pt, family, bold) > width_pt and cur:
                n += 1
                cur = w
            else:
                cur = trial
        lines += n
    return lines


def run_size_pt(run, para, default=DEFAULT_PT) -> float:
    if run.font.size:
        return run.font.size.pt
    if para.font.size:
        return para.font.size.pt
    return default


def shape_bbox(shape):
    if shape.left is None or shape.top is None or shape.width is None or shape.height is None:
        return None
    return (int(shape.left), int(shape.top), int(shape.left + shape.width), int(shape.top + shape.height))


def intersects(a, b):
    return not (a[2] <= b[0] or b[2] <= a[0] or a[3] <= b[1] or b[3] <= a[1])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("deck")
    ap.add_argument("--min-slides", type=int, default=1)
    ap.add_argument("--max-slides", type=int, default=200)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    findings = []

    def add(level, check, slide, msg):
        findings.append({"level": level, "check": check, "slide": slide, "msg": msg})

    try:
        prs = Presentation(args.deck)
    except Exception as e:  # noqa: BLE001
        add("ERROR", "open", 0, f"cannot open: {e}")
        return report(findings, args.json)

    n = len(prs.slides)
    if n < args.min_slides or n > args.max_slides:
        add("ERROR", "slide-count", 0, f"{n} slides, expected {args.min_slides}-{args.max_slides}")

    sw, sh = int(prs.slide_width), int(prs.slide_height)

    for idx, slide in enumerate(prs.slides, start=1):
        text_boxes = []
        slide_words = 0
        has_title = False
        for shape in slide.shapes:
            bbox = shape_bbox(shape)
            if bbox and (bbox[0] < -1000 or bbox[1] < -1000 or bbox[2] > sw + 1000 or bbox[3] > sh + 1000):
                add("ERROR", "off-slide", idx, f"shape '{shape.name}' extends past slide edge")

            if shape.shape_type == 13:  # picture
                continue
            if not shape.has_text_frame:
                if shape.is_placeholder and not getattr(shape, "image", None):
                    # non-text placeholder (picture/chart/table) that was never filled
                    if shape.shape_type is None or shape.shape_type == 14:
                        add("ERROR", "empty-shape", idx, f"unfilled placeholder '{shape.name}'")
                continue

            tf = shape.text_frame
            text = tf.text.strip()
            if not text:
                if shape.is_placeholder:
                    add("ERROR", "empty-shape", idx, f"empty placeholder '{shape.name}'")
                continue

            slide_words += len(text.split())
            if LEFTOVER.search(text):
                add("ERROR", "leftover-text", idx, f"template residue in '{shape.name}': {LEFTOVER.search(text).group(0)!r}")

            if shape.is_placeholder and shape.placeholder_format.type is not None and "TITLE" in str(shape.placeholder_format.type):
                has_title = True
            elif bbox and bbox[1] < sh * 0.35 and any(
                (r.font.size and r.font.size.pt >= 24) for p in tf.paragraphs for r in p.runs
            ):
                has_title = True

            # overflow estimate
            if bbox and shape.width and shape.height:
                width_pt = (shape.width - 2 * INSET_EMU) / EMU_PER_PT
                height_pt = (shape.height - 2 * INSET_EMU) / EMU_PER_PT
                total_h = 0.0
                for para in tf.paragraphs:
                    ptxt = "".join(r.text for r in para.runs) or para.text
                    sizes = [run_size_pt(r, para) for r in para.runs] or [para.font.size.pt if para.font.size else DEFAULT_PT]
                    size = max(sizes)
                    fam = next((r.font.name for r in para.runs if r.font.name), None)
                    bold = any(r.font.bold for r in para.runs)
                    indent = (para.level or 0) * size * 1.5
                    lines = wrapped_lines(ptxt, size, width_pt - indent, fam, bold) if ptxt.strip() else 1
                    total_h += lines * size * LINE_SPACING
                    if para.space_after:
                        total_h += para.space_after.pt
                    for r in para.runs:
                        s = run_size_pt(r, para)
                        if s < 10 and bbox[1] < sh * 0.9:
                            add("ERROR", "tiny-font", idx, f"{s:.0f}pt text in '{shape.name}': {r.text[:40]!r}")
                autofit = tf.auto_size  # None/NONE means fixed box
                if total_h > height_pt * 1.08 and str(autofit) in ("None", "MSO_AUTO_SIZE.NONE (0)", "NONE"):
                    add("ERROR", "overflow", idx,
                        f"'{shape.name}' needs ~{total_h:.0f}pt but box is {height_pt:.0f}pt high "
                        f"(~{total_h / max(height_pt, 1):.1f}x). Reduce text, font, or enlarge box.")
            if bbox:
                text_boxes.append((shape.name, bbox))

        for i in range(len(text_boxes)):
            for j in range(i + 1, len(text_boxes)):
                a, b = text_boxes[i], text_boxes[j]
                if intersects(a[1], b[1]):
                    # tolerate tiny touches (< 2% of slide area)
                    ox = min(a[1][2], b[1][2]) - max(a[1][0], b[1][0])
                    oy = min(a[1][3], b[1][3]) - max(a[1][1], b[1][1])
                    if ox * oy > 0.02 * sw * sh:
                        add("ERROR", "overlap", idx, f"'{a[0]}' overlaps '{b[0]}'")

        if not has_title:
            add("WARN", "no-title", idx, "no title-sized text near top of slide")
        if slide_words > 120:
            add("WARN", "text-wall", idx, f"{slide_words} words on one slide; split it")

    return report(findings, args.json, n)


def report(findings, as_json, n_slides=None):
    errors = [f for f in findings if f["level"] == "ERROR"]
    if as_json:
        print(json.dumps({"slides": n_slides, "errors": len(errors), "findings": findings}, indent=2))
    else:
        for f in findings:
            print(f"{f['level']:5} slide {f['slide']:>3} {f['check']:13} {f['msg']}")
        print(f"\n{n_slides} slides, {len(errors)} errors, {len(findings) - len(errors)} warnings")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
