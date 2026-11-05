#!/usr/bin/env python3
"""Inventory an existing deck so you can edit it by slide index and shape name.

Usage: python inspect_pptx.py deck.pptx [--slide N]
Prints, per slide: index, layout name, each shape's name, type, position (inches) and text.
"""
import sys
from pptx import Presentation
from pptx.util import Emu

path = sys.argv[1]
only = int(sys.argv[sys.argv.index("--slide") + 1]) if "--slide" in sys.argv else None
prs = Presentation(path)
print(f"{path}: {len(prs.slides)} slides, {Emu(prs.slide_width).inches:.2f}x{Emu(prs.slide_height).inches:.2f} in")
for i, s in enumerate(prs.slides, 1):
    if only and i != only:
        continue
    print(f"\n== slide {i}  layout='{s.slide_layout.name}'")
    for sh in s.shapes:
        kind = "table" if sh.has_table else "chart" if sh.has_chart else "picture" if sh.shape_type == 13 else "text" if sh.has_text_frame else str(sh.shape_type)
        pos = f"({Emu(sh.left).inches:.1f},{Emu(sh.top).inches:.1f}) {Emu(sh.width).inches:.1f}x{Emu(sh.height).inches:.1f}" if sh.left is not None else ""
        txt = sh.text_frame.text.replace("\n", " / ")[:90] if sh.has_text_frame else ""
        print(f"  [{sh.shape_id}] {sh.name!r:28} {kind:8} {pos:22} {txt}")
    if s.has_notes_slide and s.notes_slide.notes_text_frame.text.strip():
        print(f"  notes: {s.notes_slide.notes_text_frame.text[:120]!r}")
