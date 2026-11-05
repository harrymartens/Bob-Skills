# Bob-Skills

Skills, an always-on rule, an eval harness and an MCP server that make IBM Bob (Sonnet-backed)
plan, delegate, verify and produce decks, documents and research the way Claude does.

Bob already has a todo list, subagents, skills, modes and MCP. Left alone it uses none of them:
in the baseline runs saved under `evals/*/runs/*baseline/` it shipped `[Director name]` on a title
slide, cited a URL that returns 404, viewed zero rendered slides and said "nearly ready". The
skills here fix that with code (checkers Bob must run) and with a rule file Bob always loads.

## What is in the repo

| Path | What | Bob surface |
|---|---|---|
| `bob/rules/00-operating-discipline.md` | the six standing orders: plan, use skill, delegate, verify, report shape, no brackets | `.bob/rules/` (always loaded) |
| `skills/operating-discipline` | the four gates in full, rationalisation table, red flags | skill (`use_skill`) |
| `skills/pptx` | `deckkit.py` layout library with design rules baked in, `check_pptx.py`, `render.sh` | skill |
| `skills/docx` | python-docx workflow, `check_docx.py`, `render.sh` | skill |
| `skills/pdf` | routes for generating PDFs, `check_pdf.py` | skill |
| `skills/research` | `[Sn]` citation contract, `fetch_page.py` cache, `check_citations.py` (verbatim quote check), red-team section | skill |
| `mcp/ibm-docs` | MCP server: search/fetch www.ibm.com/docs and bob.ibm.com/docs, live self-test | `.bob/mcp.json` |
| `bob/custom_modes.yaml` | optional `researcher` and `deck-builder` modes | `custom_modes.yaml` |
| `bob/AGENTS.md` | template for your standing context | `AGENTS.md` |
| `evals/<skill>/` | `task.md`, `criteria.md`, `check.sh`, `runs/` with saved evidence | - |
| `tools/run_eval.sh`, `Makefile` | drives `bob run` headlessly, saves transcript + artifacts, runs the check | - |
| `docs/` | Bob platform facts (with URLs), capability matrix, popular-skills survey, IBM docs feasibility, audit rubric | - |

## Install

```bash
git clone https://github.com/harrymartens/Bob-Skills && cd Bob-Skills
pip install python-pptx python-docx pypdf pdfplumber reportlab pillow markitdown "mcp>=1.2"
# LibreOffice + Poppler for rendering: brew install --cask libreoffice && brew install poppler
#                                     apt install libreoffice-impress libreoffice-writer poppler-utils
make check-tools         # which binaries are present
make test                # builds a deck/doc/pdf and runs every checker, no Bob needed
bash install.sh          # copies skills + rule into ~/.bob (or: bash install.sh /path/project/.bob)
bob mcp add ibm-docs -- python3 "$PWD/mcp/ibm-docs/server.py"   # optional
```

Restart Bob (new task) so it rescans `~/.bob/skills`. In `bob chat`, `$pptx`, `$research` etc. invoke a
skill explicitly; otherwise the description triggers it.

## Eval status

"Sandbox" = the same task run by a Sonnet subagent inside this repo's build environment, with and
without the skill, as a proxy for Bob. "Bob" = `make eval-<skill>` on your machine; not run yet.

| Skill | Sandbox baseline | Sandbox with skill | Bob | Last run |
|---|---|---|---|---|
| pptx | FAIL: placeholder text, 404 citation, 3 layouts | PASS: 0 checker errors, 5 layouts, 5/5 URLs resolve | not run | 2026-11-04 |
| docx | not run with this task | PASS: 539 words, 7 real headings, 2 tables, 2 pages | not run | 2026-11-04 |
| pdf | not run | checker verified on generated files (`make test`) | not run | 2026-11-05 |
| research | FAIL: no quotes, no counter-evidence section | PASS: 4/4 quotes found verbatim on live pages | not run | 2026-11-04 |
| operating-discipline | FAIL: no todo, no delegation, no report shape | partial: report shape + checker + todo; delegation untestable in sandbox (nested subagents have no subagent tool) | not run | 2026-11-04 |
| ibm-docs MCP | - | `python3 mcp/ibm-docs/selftest.py` OK, 6 tools live | not run | 2026-11-05 |

Rendered slides from the with-skill runs are reproducible: `bash skills/pptx/scripts/render.sh evals/pptx/runs/2026-11-04-sonnet-sandbox-with-skill/mcp-pitch.pptx out/`.

## What to run on your machine (Bob is installed there, not here)

```bash
export BOB_API_KEY=...          # Inference-scope key; bob run does not reuse the chat login
make eval                      # all five skills through bob run; results in evals/*/runs/<stamp>/
make baseline-pptx             # same task with skills disabled, for the before/after
make trigger-pptx              # does Bob pick the skill from its description alone?
```

Then paste back `evals/*/runs/LATEST` and any FAIL `check.log`. Open questions only a local run can
settle are listed with exact commands in `docs/bob-platform-facts.md` section 10 (whether `$skill`
works under `bob run`, whether `.claude/skills` is scanned, web_search enablement, mode precedence).

## How the skills were built

Raw material: cloned `anthropics/skills` and `obra/superpowers`, Bob docs fetched from bob.ibm.com,
the `@ibm/bob` npm bundle, live probes of www.ibm.com/docs. Method: for each skill, run the task
without the skill (RED), read the transcript for the exact rationalisations, write the skill against
those, run again (GREEN), close the loopholes the second run exposed (REFACTOR). Evidence for each
step is in `evals/<skill>/runs/` and `evals/<skill>/criteria.md`.

Anthropic's document skills are source-available with a no-copying licence; they were read for their
approach only. All scripts and text here are original. The superpowers patterns (MIT) were ported.

## Adding a skill

1. Write `evals/<name>/task.md` and `criteria.md` first, then `check.sh` that exits non-zero on the failure you expect.
2. `make baseline-<name>` and read the transcript. Quote the rationalisations in `criteria.md`.
3. Write `skills/<name>/SKILL.md` (name = folder, kebab-case; description starts with "Use when" and lists file types and phrases) and any script the deterministic part needs.
4. `make eval-<name>` until it passes; record the run in the table above.
