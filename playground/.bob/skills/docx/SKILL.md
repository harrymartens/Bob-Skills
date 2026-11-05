---
name: docx
description: Use whenever a Word document is requested or touched: .docx, "Word doc", report, memo, one-pager, proposal, letter, or "write it up as a document" with headings, tables, or a table of contents.
---

# Word documents that read as written, not generated

Generate with `python-docx`, then prove the file with `scripts/check_docx.py` and look at
it with `scripts/render.sh`. The common defects are structural: bold text pretending to be
headings (so no navigation pane, no TOC), typed "•" bullets, `\n` inside runs, empty
table cells, placeholder brackets left in.

## Workflow

1. **Outline first.** Headings as a numbered list with one line of intent each. A memo is
   Summary / Context / Findings / Recommendation / Next steps. A report adds Method and
   Appendix. Put the outline in your todo tool.
2. **Build with python-docx using real styles.** `doc.add_heading(text, level)` for every
   heading; `doc.add_paragraph(text, style="List Bullet")` for bullets; one `add_paragraph`
   per paragraph, never `\n`. Tables: `doc.add_table(rows, cols, style="Light Grid Accent 1")`
   with a header row, every cell filled. Set `doc.core_properties.title` and `.author`.
3. **Check.** `python scripts/check_docx.py out.docx --min-words N --require-headings "Summary,Recommendation"`.
   Fix every ERROR in the generator.
4. **Render and look.** `bash scripts/render.sh out.docx out/` gives one PNG per page.
   Look for: a heading orphaned at the bottom of a page, a table split awkwardly, a wall
   of text with no headings for a full page, inconsistent fonts.
5. **Report with evidence.** Path, page count, word count, the checker summary line,
   and what was not verified.

## Rules

- One typeface for body (Calibri or Arial, 11pt), headings from the built-in Heading styles.
- Paragraphs under 120 words. If a paragraph makes three points, it is three paragraphs or a list.
- Every number has a source: footnote-style `[1]` and a Sources section at the end, or
  the research skill's `[S1]` convention if the content came from research.
- Tables for comparisons with three or more attributes; lists for everything shorter.
- Page breaks (`doc.add_page_break()`) before top-level sections in reports longer than three pages.
- Never leave `[Name]`, `[Date]`, `TBD` or `lorem` in the file. The checker flags them, but write the real value.

## Editing an existing .docx

Open it with `Document(path)`, change text through `run.text` (not `paragraph.text`, which
discards formatting), save under a new name, then run the checker and renderer on the
result. Tracked changes and comments are beyond python-docx; say so instead of faking them.

## Dependencies

`pip install python-docx`. Rendering needs LibreOffice and Poppler (see the pptx skill).
