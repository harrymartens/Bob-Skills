# Capability matrix: what Claude's best workflows do, how other vendors do it, and how far Bob is

Built 2026-11-04 from the raw skill files (cloned `anthropics/skills` and `obra/superpowers`), vendor
docs, and the Bob facts in `bob-platform-facts.md`. Every cell names its source. "Distance" is how far
Bob's default behaviour was from the capability in the sandbox baseline runs (`evals/*/runs/*baseline`).

License note: Anthropic's `pptx`, `docx`, `pdf`, `xlsx` skills are source-available with a licence that
forbids copying and derivative works (`skills/pptx/LICENSE.txt` in that repo). They were read as
reference only; every script and sentence in this repo's skills is original. `superpowers` is MIT and
`skill-creator`/`mcp-builder` are Apache-2.0, so their patterns were ported freely.

| # | Capability | Anthropic (Claude.ai / skills repo) | superpowers (obra) | OpenAI Codex | Cursor / Windsurf | Bob today | Distance | Built here |
|---|---|---|---|---|---|---|---|---|
| 1 | Always-on operating rules that force planning and verification | `using-superpowers` loaded by a SessionStart hook; Claude Code `CLAUDE.md` | `skills/using-superpowers/SKILL.md`: "invoke relevant skills BEFORE any response", red-flag table | `AGENTS.md`, layered root→cwd, `AGENTS.override.md` (developers.openai.com/codex/guides/agents-md) | `.cursor/rules/*.mdc` with `alwaysApply: true`; Windsurf `.windsurf/rules/*.md` | `AGENTS.md` + `.bob/rules/*.md` always loaded (bob-platform-facts §3); nothing shipped by default | High: 0/3 baseline runs planned or verified | `bob/rules/00-operating-discipline.md` + `skills/operating-discipline` |
| 2 | Plan as a todo list before acting | Claude Code `TaskCreate`; superpowers `writing-plans` | `writing-plans`: bite-sized tasks with the exact test per task | AGENTS.md conventions only | n/a | `update_todo_list` tool exists (§5) but unused unless asked | High | Gate 1 of operating-discipline; TODO.md fallback |
| 3 | Delegate to fresh-context subagents | Claude Code `Agent` tool; `subagent-driven-development` | `dispatching-parallel-agents`: one agent per independent domain, prompt structure | Codex cloud tasks (no in-session subagents documented) | Cursor background agents | `spawn_subagent` (explore/general), `start_subtask` (§5) | High: 0/3 baseline runs delegated | Gate 2; mandatory reviewer subagent per deliverable |
| 4 | Evidence before completion claims | `verification-before-completion`: "NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE" | same (MIT, ported) | n/a | n/a | none | High: baseline said "nearly ready" over a 404 citation and `[Director name]` | Gate 3 + per-skill checkers (`check_*.py`) |
| 5 | Fixed report shape incl. what was not verified | Claude Code system prompt "Report outcomes faithfully" | `verification-before-completion` patterns | n/a | n/a | none | Medium | Gate 4: Produced / Checked / Not verified / Decisions / Needs you |
| 6 | Deck generation with design rules encoded | `pptx` skill: pptxgenjs + `validate.py` + render via LibreOffice + visual QA; design rules (palette, 36pt titles, no accent bars) | n/a | n/a | n/a | python-pptx from memory: default blue, colour bars, placeholders | High | `skills/pptx`: `deckkit.py` encodes the rules as layouts; `check_pptx.py`; `render.sh` |
| 7 | Programmatic file QA (overflow, placeholders, structure) | `pptx/scripts/office/validate.py` (XSD + chart checks); `markitdown` grep for placeholder text | n/a | n/a | n/a | none | High | `check_pptx.py` (font-metric overflow, overlap, off-slide, placeholder regex), `check_docx.py`, `check_pdf.py` |
| 8 | Visual QA by rendering to images | `soffice --convert-to pdf` + `pdftoppm`, "inspect every one" | n/a | n/a | n/a | LibreOffice available if installed; image ingestion by Bob not documented (§5) | Medium | `render.sh`; skills say what to do if images cannot be viewed |
| 9 | Word documents with real styles | `docx` skill: docx-js, OOXML editing, tracked changes, render check | n/a | n/a | n/a | python-docx from memory | Medium | `skills/docx` + `check_docx.py` (fake headings, literal bullets, blank cells) |
| 10 | PDF create/read/merge | `pdf` skill: pypdf, pdfplumber, reportlab, OCR notes | n/a | n/a | n/a | ad hoc | Low | `skills/pdf` + `check_pdf.py` |
| 11 | Research with verified citations | Claude Code `/deep-research` (fan out, fetch, cross-check, cite); best-practices "verify every citation" | n/a | OpenAI deep research product (not a skill) | n/a | no web tool by default; `experiments.webFetch` off (§5) | High: baseline cited unread URLs and reasoned from "docs don't mention it" | `skills/research`: `[Sn]` contract, `fetch_page.py` cache, `check_citations.py` verbatim-quote check, red-team section |
| 12 | Adversarial pass on own conclusions | `discernment-nudge` (follow-up questions); `deep-research` cross-check | `requesting-code-review` (reviewer subagent) | n/a | n/a | none | High | research skill step 5 ("This is wrong if...") + reviewer subagent in Gate 2 |
| 13 | Access to vendor documentation as a tool | Claude connectors / MCP | n/a | Codex MCP config | Cursor MCP | `.bob/mcp.json` stdio + streamable HTTP (§4) | Medium | `mcp/ibm-docs` server (6 tools, live self-test) |
| 14 | Skill discovery by description | agentskills.io spec: description is the trigger; Anthropic best practices: "pushy" descriptions | `description: Use when...` convention | n/a | `.mdc` `description` for agent-requested rules | SKILL.md description auto-activates; skill loads once per conversation (§1) | n/a | all five SKILL.md descriptions list file types, phrases and symptoms; `tools/run_trigger_eval.sh` tests it |
| 15 | Eval loop with/without skill | `skill-creator`: spawn with-skill and baseline runs in the same turn, assertions, viewer | `writing-skills`: RED (baseline) → GREEN → REFACTOR with pressure scenarios | n/a | n/a | none | High | `evals/<skill>/{task.md,criteria.md,check.sh,runs/}`, `tools/run_eval.sh`, `make eval`, `make baseline-<skill>` |
| 16 | Spreadsheets with recalculated formulas | `xlsx` skill: openpyxl + mandatory LibreOffice recalc | n/a | n/a | n/a | none | not built | deferred (not in scope; pattern = same as pptx/docx) |

## Where each column's facts come from

- Anthropic: `anthropics/skills` clone (SKILL.md of pptx, docx, pdf, skill-creator), https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices, https://code.claude.com/docs/en/commands (`/deep-research`).
- superpowers: `obra/superpowers` clone, `skills/*/SKILL.md`.
- Codex: https://developers.openai.com/codex/guides/agents-md.
- Cursor: `.cursor/rules/*.mdc` frontmatter (`description`, `globs`, `alwaysApply`) per https://stevekinney.com/courses/ai-development/cursor-rules and vendor docs; Windsurf rules directory per the same comparison (secondary source; not verified against windsurf.com).
- Bob: `docs/bob-platform-facts.md` (sections cited as §n), fetched from bob.ibm.com/docs and the `@ibm/bob` npm bundle on 2026-11-04.
- Distance: `evals/*/runs/2026-11-04-sonnet-sandbox-baseline/transcript.txt`.
