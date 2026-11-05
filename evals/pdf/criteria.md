# pdf eval: pass criteria
- decision-summary.pdf exists, exactly 1 page, check_pdf.py 0 errors
- required text present: "Summary", "Scope", "Risks", "Decision needed"
- Title metadata set

## Sandbox result (2026-11-05, Sonnet subagent as proxy for Bob)

With skill: reportlab route, Title metadata set, 1 page, 0 checker errors at the time, render viewed.
But it shipped `[Owner TBC]` in the table and the checker's placeholder list did not include it.
Checker fixed (any `[Letter...]` bracket that is not a citation tag, plus TBC); the saved run now FAILS
on `leftover-text`, which is the correct verdict. Re-run under Bob to confirm the skill text
("never leave brackets") plus the checker close it.
