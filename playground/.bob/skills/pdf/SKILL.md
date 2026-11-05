---
name: pdf
description: Use whenever a PDF is the requested output or the input: "export as PDF", "send me a PDF", reading or extracting text/tables from a .pdf, merging or splitting PDFs, or checking that a generated PDF is correct.
---

# PDFs: generate from a source you control, then verify

## Producing a PDF

Pick the route by what the content is:

| Content | Route |
|---|---|
| A report or memo with headings, tables, images | Build the .docx with the docx skill, then `bash scripts/render.sh out.docx out/` (LibreOffice writes `out/out.pdf` and page PNGs) |
| Slides | Build with the pptx skill; `render.sh` writes the PDF |
| A form, invoice, certificate, or fixed-layout page | `reportlab` directly (`SimpleDocTemplate` with `Paragraph`, `Table`, `Spacer`); set `title=` and `author=` on the document |
| Markdown/HTML you already have | `pandoc in.md -o out.pdf` if pandoc is installed, else convert to .docx first |

Then always:

```bash
python scripts/check_pdf.py out.pdf --min-pages N --max-pages M --require-text "Summary,Recommendation"
bash scripts/render.sh out.pdf out/   # PNG per page; look at every page if you can view images
```

Fix ERRORs at the source (the .docx, the reportlab script), regenerate, re-check.
A PDF is never hand-edited.

## Reading a PDF

- Text: `python -c "import pdfplumber; ..."` or `pdftotext -layout in.pdf -`. Prefer `pdfplumber`
  when you need tables (`page.extract_tables()`); use `pypdf` for metadata, page counts, merge/split.
- Scanned PDFs have no text layer. If `pdftotext` returns almost nothing, say so and ask
  whether OCR (`ocrmypdf`) is acceptable rather than guessing content.
- When quoting from a PDF in research, cite page numbers and keep the extracted text file
  as the cached source for the citation checker.

## Merge / split / rotate

`pypdf.PdfWriter` with `append(reader)` to merge, `add_page(reader.pages[i])` to select, and
`page.rotate(90)` to rotate. Write to a new file, then run `check_pdf.py` on it.

## Report with evidence

Path, page count, the checker summary line, which pages you looked at, and anything unverified.

## Dependencies

`pip install pypdf pdfplumber reportlab`. Rendering needs LibreOffice and Poppler.
