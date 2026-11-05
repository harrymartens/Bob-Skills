#!/usr/bin/env bash
# Prove the bundled scripts work on this machine without Bob: build a deck/doc/pdf, run every checker.
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"; tmp="$(mktemp -d)"; cd "$tmp"
python3 - "$root" <<'PY'
import sys; sys.path.insert(0, sys.argv[1] + "/skills/pptx/scripts")
from deckkit import Deck, PALETTES
d = Deck(palette=PALETTES["navy"]); d.title_slide("Selftest", "deckkit", "now")
d.cards("Three things", [("A", "first"), ("B", "second"), ("C", "third")]); d.closing_slide("Done", "Approve")
d.save("t.pptx")
from docx import Document
doc = Document(); doc.core_properties.title = "Selftest"; doc.add_heading("Summary", 1)
doc.add_paragraph("word " * 60); doc.add_heading("Risks", 1); doc.add_paragraph("item", style="List Bullet"); doc.save("t.docx")
from reportlab.lib.pagesizes import A4; from reportlab.pdfgen import canvas
c = canvas.Canvas("t.pdf", pagesize=A4); c.setTitle("Selftest"); c.drawString(72, 750, "Summary Scope Risks Decision needed " * 2); c.save()
open("r.md","w").write('# T\n## Answer\n- python-pptx creates files [S1]\n## Counter-evidence\n- This is wrong if x\n## Confidence\n## Sources\n[S1] https://python-pptx.readthedocs.io/en/latest/ — "python-pptx is a Python library for creating, reading, and updating PowerPoint (.pptx) files"\n')
PY
python3 "$root/skills/pptx/scripts/check_pptx.py" t.pptx --min-slides 3 --max-slides 3
python3 "$root/skills/docx/scripts/check_docx.py" t.docx --min-words 50 --require-headings "Summary,Risks"
python3 "$root/skills/pdf/scripts/check_pdf.py" t.pdf --require-text "Summary,Risks"
python3 "$root/skills/research/scripts/check_citations.py" r.md
if command -v soffice >/dev/null; then bash "$root/skills/pptx/scripts/render.sh" t.pptx out 40 | head -1; else echo "soffice missing: render skipped"; fi
echo "SELFTEST OK"; rm -rf "$tmp"
