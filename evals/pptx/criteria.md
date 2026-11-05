# pptx eval: pass criteria

Programmatic (check.sh exits 0):
- mcp-pitch.pptx exists and opens
- exactly 8 slides
- check_pptx.py reports 0 errors (no overflow, no overlap, no bracket placeholders, no tiny fonts)
- at least 3 distinct layout types (detected by shape mix)
- every cited URL in the deck resolves (HTTP < 400)

Transcript (judged by reading runs/<date>/transcript.txt):
- the agent fetched at least one spec page before writing citations
- the agent ran check_pptx.py and render.sh
- the final message names what was not verified

Baseline (no skill, 2026-11-04, Sonnet): shipped `[Director name]` placeholder, cited a 404 URL,
viewed 0 rendered slides, said "nearly ready". With skill: 0 checker errors, 5/5 URLs resolve,
all slides rendered, unverified items listed.
