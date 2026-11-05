# research eval: pass criteria

Programmatic (check.sh exits 0):
- research.md exists with ## Answer, ## Counter-evidence, ## Confidence, ## Sources sections
- check_citations.py reports 0 errors: every [Sn] tag has a source line, every quote is found verbatim on the live page
- at least 4 sources

Transcript:
- fetch_page.py (or curl) was run before Sources were written
- a "This is wrong if" line exists per conclusion
- confidence is given per question

Baseline (no skill, 2026-11-04, Sonnet): answers mostly right, but no quotes, one answer ("bob run"
vs "-p") unresolved, and the MCP "no limit" claim admitted as inference from one page.
