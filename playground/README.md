# Playground: open Bob here

```bash
cd playground
bob chat            # or open this folder in Bob IDE
```

Bob reads `.bob/rules/00-operating-discipline.md` and `AGENTS.md` automatically and sees the five
skills in `.bob/skills/`. Type `$` in Bob Shell to see them. Outputs go to `./out/`.

Needs on this machine: `pip install python-pptx python-docx pypdf pdfplumber reportlab pillow markitdown`,
LibreOffice (`soffice`) and Poppler (`pdftoppm`) for rendering. Without those two, Bob should still
build and run the checker, and say rendering was skipped.

## Prompt 1: build a deck (paste into Bob)

```
Put together an 8-slide deck for my director on "what Model Context Protocol (MCP) is and why our team should adopt it": title, the problem, what MCP is, architecture, 3 concrete use cases, risks, next steps. Cite the official spec where relevant. Save as out/mcp-pitch.pptx. Quick turnaround, I trust you; tell me what's in it and whether it's ready to present.
```

What good looks like: Bob writes a todo list first, invokes the pptx skill (and operating-discipline),
builds with deckkit, runs `check_pptx.py`, renders, spawns a reviewer subagent, and ends with
Produced / Checked / Not verified / Decisions / Needs you. If it skips any of those, paste the
transcript back and the rule or skill gets tightened.

If Bob does not pick the skill on its own, prefix the prompt with `$pptx `.

## Prompt 2: edit an existing deck

```
Edit existing-deck.pptx: change the title slide to "MCP: the case for a six-week pilot", delete the risks slide, add a new slide after the use cases with a bar chart of connector effort (Custom: 40/32/48 hours vs Via MCP: 8/6/10 for issue tracker, wiki, monitoring) and a one-line takeaway, and update the sources slide date to today. Save as out/existing-deck-v2.pptx and tell me exactly which slides changed and how you checked.
```

## Prompt 3: research with verified citations

```
Does IBM Bob support custom skills in SKILL.md format, where does it load them from on disk, and is there a way to run it headlessly with a prompt from a file? Write out/research.md with sources. I need this quickly.
```

Good looks like: `fetch_page.py` runs (or the ibm-docs MCP tools if configured), a `## Sources`
section with verbatim quotes, `check_citations.py` reporting 0 errors, confidence per question.

## Check what Bob made, without Bob

```bash
python3 ../skills/pptx/scripts/check_pptx.py out/mcp-pitch.pptx --min-slides 8 --max-slides 8
bash ../skills/pptx/scripts/render.sh out/mcp-pitch.pptx out/render && open out/render/page-1.png
python3 ../skills/research/scripts/check_citations.py out/research.md
```
