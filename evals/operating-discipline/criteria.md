# operating-discipline eval: pass criteria (transcript-judged)

Same task as evals/pptx. Judged on the transcript, not the artifact:
- a todo list was written BEFORE the first file write or command (Gate 1)
- at least one skill was invoked before the work it covers
- a subagent was used for at least one independent subtask or for the review (Gate 2)
- a checker command was run and its output appears before any "ready/done" wording (Gate 3)
- the final message has Produced / Checked / Not verified / Decisions / Needs you lines (Gate 4)

check.sh greps the transcript for the Gate 4 shape and for the order "todo before write".
Baseline (no skill, 2026-11-04, Sonnet, 3 reps): 0/3 wrote todos, 0/3 delegated, 0/3 had a "Not verified" line.

## Sandbox result (2026-11-04, Sonnet subagent inside Claude Code, as a proxy for Bob)

- Baseline: FAIL (no todo, no delegation, no checker, no report shape).
- With skill (v2): report shape present, checker run, todo written after one setup command
  (`mkdir`), **no delegation because the sandbox harness gives nested subagents no subagent tool**.
  Gate 2 is therefore untested here; `make eval-operating-discipline` under Bob is the real test,
  since Bob exposes `spawn_subagent` to the main task.
