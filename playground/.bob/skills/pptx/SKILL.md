---
name: pptx
description: Use whenever a .pptx deck, slides, or a presentation is requested, created, edited, or reviewed, including "put together a deck", "slides for my director", "pitch", "summarise this as a presentation", or any file ending in .pptx.
---

# Building PowerPoint decks that survive a real audience

A deck is a visual argument, not a text dump. Sonnet's default output (title + bullets,
default blue, a colour bar across the top) reads as machine-made within one slide.
This skill fixes that with code, not willpower: `scripts/deckkit.py` encodes the layout
rules, `scripts/check_pptx.py` proves the file is clean, `scripts/render.sh` shows you
what the audience will see.

## Workflow (do all six, in order)

1. **Outline before code.** Write the slide list as `N. <title that states the point> — <layout> — <one line of content>`.
   Titles are sentences that make the claim ("Churn fell 2 points after pricing change"),
   not labels ("Churn"). One idea per slide. 8-12 slides for a 10-minute talk.
2. **Pick a palette and a title font** from `deckkit.PALETTES` (or the user's brand colours).
   One dominant dark colour, one accent, white content slides. Never default to blue.
3. **Build with deckkit.** `from deckkit import Deck, PALETTES` then one call per slide.
   Vary layouts: never two consecutive `bullets_with_visual` slides. Every content slide
   carries a visual: a chart, a table, cards, stats, a timeline, or an image.
   Facts and numbers go in via `notes=` as speaker notes with their source URL.
4. **Check the file.** `python scripts/check_pptx.py deck.pptx --min-slides N --max-slides N`.
   Fix every ERROR in the generator and rebuild. Do not hand-edit.
5. **Render and look.** `bash scripts/render.sh deck.pptx out/` writes one PNG per slide.
   If you can view images, open every one and look for: text cut off, two things touching,
   a title wrapping into the body, an empty-looking slide, grey-on-grey text.
   If you cannot view images, say so in the report and point the user at the PNGs.
6. **Report with evidence.** The final message contains: file path, slide count, the
   check_pptx summary line verbatim, which slides you visually inspected, and what you
   did NOT verify (for example "feature claims on slide 4 are from memory").

## Layout menu (deckkit)

| Call | Use for |
|---|---|
| `title_slide(title, subtitle, byline)` | opening, dark background |
| `section_slide(title, kicker)` | divider between parts |
| `bullets_with_visual(title, bullets, image= or caption=)` | 3-5 bullets plus a picture or callout panel |
| `two_column(title, left_head, left_items, right_head, right_items)` | before/after, pros/cons, A vs B |
| `cards(title, [(head, body), ...])` | 2-4 options, use cases, pillars |
| `stats(title, [(big_number, label), ...])` | 2-4 headline numbers |
| `table(title, header, rows, col_widths=)` | comparisons with 3+ attributes |
| `bar_chart(title, categories, {series: values}, kind="bar"/"line"/"pie", takeaway=)` | any quantitative claim; native, editable |
| `timeline(title, [(label, desc), ...])` | plans, phases, roadmaps |
| `closing_slide(title, ask)` | the decision you want, dark background |
| `sources_slide([lines])` | every URL you relied on |

Need a layout deckkit lacks? Add a method to `deckkit.py` following the same pattern
(use `_title`, `_text`, `_rect`, `_bullets`), then run the checker. Do not drop to raw
python-pptx inside your build script; the helpers carry the fit logic and the rules.

## Rules the code enforces (so you know why output looks the way it does)

- 16:9, 0.6" margins, titles 38pt that shrink to fit on one line, body 16-18pt, nothing under 11pt.
- Text shrinks to fit its box using real font metrics; if `check_pptx` still reports
  `overflow`, you have too much text for the slide. Cut words or split the slide.
- Bullets are real bullet formatting, never a typed "•".
- No horizontal colour bars, no accent stripes under titles, no left-edge card stripes.
  These are the fingerprints of generated slides. Cards get a tint and a numbered circle.
- Charts are native PowerPoint charts with data labels and a one-line takeaway under them.
- Speaker notes hold the detail and the sources; slides hold the point.

## Content rules the code cannot enforce

- Every number on a slide has a source in the notes or the sources slide. If you did not
  fetch the source during this task, say "unverified" in the notes and in the report.
- Write the title slide byline from what the user told you. Never ship `[Name]`-style
  brackets; `check_pptx` flags them, but write the real value in the first place.
- The last content slide states a decision or an action with an owner and a date.
- If the user gave a template (.pptx/.potx), open it with python-pptx, reuse its layouts,
  and skip deckkit's `Deck()`; the checker and renderer still apply.

## Editing an existing deck

1. `python scripts/inspect_pptx.py deck.pptx` lists every slide, shape name, position and text.
   Work from that inventory; never guess shape names.
2. Edit with python-pptx and save under a new name:
   - change text: `run.text = "..."` on the existing runs (keeps formatting); `shape.text_frame.text = ...` wipes it
   - delete slide N: `xml_slides = prs.slides._sldIdLst; sl = list(xml_slides)[N-1]; prs.part.drop_rel(sl.rId); xml_slides.remove(sl)`
   - reorder: move the `<p:sldId>` element inside `prs.slides._sldIdLst`
   - add a slide in the deck's own style: `prs.slides.add_slide(prs.slide_layouts[i])` and fill its placeholders
   - replace a picture: delete the old shape (`sh._element.getparent().remove(sh._element)`) and `add_picture` at the same box
   - duplicating a slide is not supported by python-pptx; rebuild it with the same layout instead
3. Run `check_pptx.py` and `render.sh` on the new file, then the Gate 4 report. Mention which slides changed.

## Dependencies

`pip install python-pptx pillow` for building and checking. `render.sh` needs LibreOffice
(`soffice`) and Poppler (`pdftoppm`); on macOS `brew install --cask libreoffice && brew install poppler`,
on Debian/Ubuntu `apt install libreoffice-impress poppler-utils`. If `soffice` is missing,
skip step 5, say so, and rely on the checker.

## Red flags in your own behaviour

| Thought | Reality |
|---|---|
| "The user is in a hurry, skip the checker" | The checker takes two seconds. Shipping overflow costs the meeting. |
| "I rendered one slide and it looked fine" | Defects cluster on the dense slides you did not open. Open all of them. |
| "I know this library's features" | Memory is where the wrong feature claims come from. Fetch the docs or mark unverified. |
| "Title + bullets is cleaner" | It is the default everyone recognises as generated. Use a visual layout. |
| "Nearly ready to present" | Either the checker passed and you looked at every slide, or it is not ready. Say which. |
