# Audit of pre-existing local skills

**Date:** 2026-11-04. **Finding:** the repository branch had no commits and no files when this work
started, so the local skills mentioned in the brief were never available to audit. Nothing was deleted
because nothing was present.

## Rubric to apply when they are pushed

Score each existing `SKILL.md` 0-2 on each line; keep a skill only if it scores 7 or more of 10, and
record the score here.

| Criterion | 0 | 1 | 2 |
|---|---|---|---|
| Trigger | description says what it does, not when | "use when" with one trigger | "use when" with file types, phrases and symptoms |
| Mechanism | prose advice only | names a library or tool | ships a script that does the deterministic part |
| Verification | none | "check your work" | a command whose output decides pass/fail |
| Report contract | none | "summarise" | fixed shape incl. what was not verified |
| Evidence it works | none | one anecdote | with/without comparison on a fixed task saved in the repo |

Rationalisations to refuse while scoring: "it worked for me once" (not evidence), "it is short so it is
fine" (short and untested is the common case), "Bob already knows this" (then the skill is empty).

## Procedure

1. `cp -r <old-skill> evals/_audit/<name>/` and write one realistic task prompt for it.
2. `bash tools/run_eval.sh` style run with and without it; keep both transcripts.
3. Score with the rubric before opening the outputs. Record the row below.

| Skill | Trigger | Mechanism | Verification | Report | Evidence | Total | Decision |
|---|---|---|---|---|---|---|---|
| (none present) | | | | | | | |
