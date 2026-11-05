# Survey of widely adopted Claude Agent Skills (SKILL.md) and recommendations for an IBM Bob port

Prepared 2026-11-04 from primary sources fetched during this session. Raw material (shallow clones of
`anthropics/skills`, `obra/superpowers`, `mattpocock/skills`, `anthropics/claude-plugins-official`; fetched docs;
skills.sh pages; awesome-list READMEs) is saved under
`/tmp/claude-0/-home-user-Bob-Skills/b342c007-b76f-5ffe-9fc5-ab63ba919308/scratchpad/skills-survey/` and should be
treated as untrusted data.

Target user: research and documentation work (reports, PowerPoint, Word, PDF, web research, technical docs), porting
to IBM Bob (Sonnet-based coding agent).

## 0. Evidence sources and how adoption was measured

| Source | What it gives | Caveat |
| --- | --- | --- |
| skills.sh (Vercel registry) leaderboard and per-repo pages, fetched 2026-11-04 | Per-skill install counts (`npx skills add`) | Vercel's own report: counts are "aggregate registry counters" and "do not represent unique people"; the registry only launched Jan 2026 and skews toward CLI/coding-agent users |
| GitHub star counts via shields.io (`img.shields.io/github/stars/<repo>.json`), 2026-11-04 | Repo-level popularity | Star counts are per repo, not per skill; the GitHub API itself was blocked by the session proxy so shields.io was used as the resolver |
| Four curated "awesome" lists (travisvn 16k stars, ComposioHQ 79k, karanb192 584, hesreallyhim/awesome-claude-code 57k) | How often a skill is independently curated | Lists are opinionated; Composio's list is partly marketing for its own plugin |
| Anthropic docs (platform.claude.com, code.claude.com, support.claude.com) and the agentskills.io spec | What is built in, what is portable, what makes a skill effective | Authoritative for Claude products only |
| IBM Bob docs (bob.ibm.com/docs) | What Bob can and cannot do with skills | Bob docs are JS-rendered; text was extracted from the fetched HTML |

Repo star counts collected (shields.io, 2026-11-04): anthropics/skills 187k; obra/superpowers 312k; mattpocock/skills
313k; anthropics/claude-plugins-official 46k; hesreallyhim/awesome-claude-code 57k; ComposioHQ/awesome-claude-skills
79k; sickn33/antigravity-awesome-skills 49k; vercel-labs/skills 38k; vercel-labs/agent-skills 34k;
alirezarezvani/claude-skills 29k; travisvn/awesome-claude-skills 16k; huggingface/skills 11k; BehiSecc/awesome-claude-skills
10k; PleasePrompto/notebooklm-skill 7.8k; anthropics/claude-plugins-community 4.8k; karanb192/awesome-claude-skills 584;
michalparkola/tapestry-skills-for-claude-code 573; sanjay3290/ai-skills 450; Anjos2/recursive-research 52.

Registry scale (Vercel, "State of agent skills", https://vercel.com/blog/state-of-agent-skills): one million skills and
~280M installs seven months after launch; the top 375 skills (0.04%) carry 62% of installs; no single skill exceeds 1%
of installs; "writing and documents" and "business operations" skills draw the most installs per listing, while
"research" skills are oversupplied (55% fewer installs per listing than average). The skills.sh home page on
2026-11-04 showed 1,251,951 all-time listings.

## 1. Full inventory of `github.com/anthropics/skills` (187k stars)

Top-level: `README.md`, `THIRD_PARTY_NOTICES.md`, `skills/` (19 skills), `spec/` (now just a pointer to
https://agentskills.io/specification), `template/SKILL.md`. The README states the repo registers as a Claude Code
plugin marketplace (`/plugin marketplace add anthropics/skills`) with two bundles, `document-skills` and
`example-skills`, and that "these example skills are all already available to paid plans in Claude.ai".

Per-skill install counts are from https://skills.sh/anthropics/skills (3.7M total installs, 21 listings incl.
`template-skill` 73.7K and a stray `claude-academy-guide` 194). Descriptions are the frontmatter `description`
field from the raw SKILL.md (condensed where very long; full text in
`skills-survey/anthropics-skills-frontmatter.txt`).

| Skill | License | skills.sh installs | SKILL.md lines / files | Frontmatter description (condensed) |
| --- | --- | --- | --- | --- |
| frontend-design | Apache-2.0 | 1.1M | 71 / 2 | Guidance for distinctive, intentional visual design when building new UI or reshaping an existing one; aesthetic direction, typography, avoiding templated defaults. |
| skill-creator | Apache-2.0 | 424.1K | 485 / 18 | Create new skills, modify and improve existing skills, and measure skill performance; run evals, benchmark with variance analysis, optimize a description for triggering accuracy. |
| pptx | Proprietary (source-available) | 248.8K | 238 / 56 | Use any time a .pptx or .potx file is involved as input or output: creating decks, reading/extracting text, editing, combining/splitting, templates, layouts, speaker notes. |
| pdf | Proprietary (source-available) | 223.0K | 314 / 12 | Anything with PDF files: extract text/tables, merge/split, rotate, watermark, create new PDFs, fill forms, encrypt/decrypt, extract images, OCR scanned PDFs. |
| docx | Proprietary (source-available) | 212.9K | 91 / 61 | Create, read, edit or manipulate Word documents (.docx/.dotx): TOC, headings, page numbers, letterheads, images, find-and-replace, tracked changes, comments; reports/memos/letters as .docx. |
| webapp-testing | Apache-2.0 | 197.6K | 95 / 6 | Toolkit for interacting with and testing local web applications using Playwright: verify frontend functionality, screenshots, browser logs. |
| xlsx | Proprietary (source-available) | 193.3K | 99 / 53 | Any task where a spreadsheet file (.xlsx/.xlsm/.xltx/.csv/.tsv) is the primary input or output; formulas, formatting, charts, cleaning messy tabular data. |
| mcp-builder | Apache-2.0 | 137.1K | 252 / 11 | Guide for creating high-quality MCP servers in Python (FastMCP) or Node/TypeScript (MCP SDK). |
| canvas-design | Apache-2.0 | 127.2K | 129 / 83 | Create visual art in .png and .pdf documents using design philosophy; posters, designs, static pieces; never copy existing artists. |
| web-artifacts-builder | Apache-2.0 | 116.1K | 73 / 5 | Suite of tools for elaborate multi-component claude.ai HTML artifacts (React, Tailwind, shadcn/ui); not for simple single-file artifacts. |
| brand-guidelines | Apache-2.0 | 115.7K | 73 / 2 | Applies Anthropic's official brand colors and typography to any artifact. |
| theme-factory | Apache-2.0 | 98.9K | 59 / 13 | Toolkit for styling artifacts (slides, docs, reports, HTML landing pages) with 10 pre-set colour/font themes or a generated theme. |
| doc-coauthoring | (no license field; repo says Apache for non-document skills) | 97.9K | 375 / 1 | Structured workflow for co-authoring documentation, proposals, technical specs, decision docs: transfer context, refine through iteration, verify the doc works for readers. |
| algorithmic-art | Apache-2.0 | 92.5K | 404 / 4 | Generative/algorithmic art with p5.js, seeded randomness, flow fields, particle systems. |
| internal-comms | Apache-2.0 | 83.5K | 32 / 6 | Resources for writing internal communications in company formats: status reports, leadership updates, 3P updates, newsletters, FAQs, incident reports, project updates. |
| slack-gif-creator | Apache-2.0 | 78.2K | 254 / 7 | Create animated GIFs optimized for Slack; constraints, validation tools, animation concepts. |
| claude-api | Apache-2.0 | 77.5K | 616 / 96 | Reference for the Claude API / Anthropic SDK (model ids, pricing, params, streaming, tool use, MCP, caching); triggers whenever Claude/Anthropic is named. |
| discernment-nudge | n/a | 14.9K | 209 / 2 | After a substantive answer the user may act on, append 2-3 follow-up questions that help the user check facts, probe reasoning, notice missing context; once per conversation. |
| academy-guide | n/a | 14.5K | 147 / 2 | Recommend matching Claude Academy (academy.claude.com) courses when the user asks how to use Claude products. |

License note (load-bearing for porting): `skills/docx/LICENSE.txt` (and the identical files for pptx, pdf, xlsx)
says "users may not: extract these materials from the Services or retain copies outside the Services; reproduce or
copy; create derivative works; distribute, sublicense, or transfer". The README calls them "source-available, not
open source ... shared as a reference". The other skills carry Apache-2.0 LICENSE.txt files.

Dependencies declared inside the four document skills (from their `## Dependencies` sections and scripts/):
- docx: `docx` npm package (docx-js) for creation, `pandoc`, LibreOffice (`soffice`), `pdftoppm` (Poppler); scripts
  `accept_changes.py`, `comment.py`, `merge_runs.py`, OOXML `office/` unpack/pack/validate helpers.
- pptx: `pptxgenjs` (npm) for creation, `markitdown[pptx]`, `Pillow`, `defusedxml`, `lxml`, LibreOffice, `pdftoppm`;
  scripts `add_slide.py`, `clean.py`, `thumbnail.py`; a required visual QA step renders slides to images.
- pdf: `pypdf`, `pdfplumber`, `reportlab`, `pdf2image`, `qpdf`, `pdftotext`/poppler; 8 form-handling scripts.
- xlsx: `openpyxl`, `pandas`, `markitdown`, LibreOffice via `scripts/recalc.py` (mandatory formula recalculation).

## 2. `github.com/obra/superpowers` (312k stars, MIT) — 15 skills, 3.8M installs on skills.sh

| Skill | Installs | Description |
| --- | --- | --- |
| brainstorming | 417.6K | You MUST use this before any creative work - creating features, building components, adding functionality, modifying behavior, or planning anything new, in software or out of it (a talk, a business, a renovation). |
| systematic-debugging | 320.3K | Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes. |
| writing-plans | 293.7K | Use when you have a spec or requirements for a multi-step task, before touching code. |
| using-superpowers | 279.4K | Use when starting any conversation - establishes how to find and use skills, requiring skill invocation before ANY response. |
| requesting-code-review | 271.9K | Use when completing tasks, implementing major features, or before merging. |
| test-driven-development | 270.0K | Use when implementing any feature or bugfix, before writing implementation code. |
| verification-before-completion | 264.5K | Use when about to claim work is complete, fixed, or passing; requires running verification commands and confirming output; evidence before assertions. |
| executing-plans | 253.1K | Use when executing an implementation plan in the current session as the implementer yourself. |
| subagent-driven-development | 247.6K | Use when executing implementation plans with independent tasks in the current session. |
| receiving-code-review | 230.7K | Use when receiving code review feedback, before implementing suggestions; technical rigor, not performative agreement. |
| dispatching-parallel-agents | 227.2K | Use when facing 2+ independent tasks without shared state. |
| writing-skills | 227.1K | Use when creating new skills, editing existing skills, or verifying skills work before deployment. |
| using-git-worktrees | 226.0K | Use when starting feature work that needs isolation from the current workspace. |
| finishing-a-development-branch | 223.4K | Use when implementation is complete, all tests pass, and you need to decide how to integrate. |
| diagnosing-superpowers | 27.4K | Use when a superpowers session went wrong and the user wants to know why. |

Superpowers is the only collection that appears in all four awesome lists surveyed. It is a software-development
lifecycle bundle; only `brainstorming`, `writing-skills` and `verification-before-completion` are domain-neutral.

## 3. Other high-adoption collections and the cross-collection view

- skills.sh all-time leaderboard (2026-11-04, top of the list): find-skills (vercel-labs/skills) 4.2M; grill-me
  (mattpocock/skills) 1.5M; hyperframes-cli / hyperframes / media-use / hyperframes-registry / hyperframes-animation
  (heygen-com/hyperframes, video) 1.0-1.4M each; agent-browser (vercel-labs/agent-browser) 1.4M; grill-with-docs
  1.3M; reddit-automation (flowkit-labs) 1.2M; design-mobile-apps (designed-by-ai) 1.2M;
  improve-codebase-architecture, tdd, setup-matt-pocock-skills, handoff, grilling, prototype, triage (all
  mattpocock) 1.0-1.2M; frontend-design (anthropics/skills) 1.1M; ui-taste (uizze.sh) 981K; ai-video-generation
  (101-skills/superpowers, a namesquat of the real superpowers) 957K; domain-modeling 936K; teach 914K;
  codebase-design 912K; diagnosing-bugs 891K; vercel-react-best-practices 871K; lark-doc and 20 more Feishu skills
  (open.feishu.cn, 17.9M total); code-review (mattpocock) 851K.
- mattpocock/skills (313k stars, MIT): ~40 skills in engineering/, productivity/, misc/, in-progress/. Beyond the
  coding ones, the relevant entries are `research` ("Investigate a question against high-trust primary sources and
  capture the findings as a Markdown file in the repo ... Use when the user wants a topic researched, docs or API facts
  gathered"), `grill-me`/`grilling` (relentless interview to sharpen a plan), `handoff` (compact a conversation into a
  handoff document), `teach`, `to-questionnaire`, `writing-for-agents`, and the in-progress `writing-fragments` /
  `writing-shape` / `writing-beats` prose-writing trio.
- anthropics/claude-plugins-official (46k stars): 40 Anthropic plugins + 14 external. Skills shipped inside them that
  matter here: `skill-creator` (same as the repo skill), `frontend-design`, `plugin-dev/skill-development`,
  `session-report`, `claude-md-management/claude-md-improver`. The rest are LSPs, code review, security, MCP dev.
- Claude Code itself bundles skills (code.claude.com/docs/en/commands): `/deep-research` is a bundled *workflow*
  ("Fan out web searches on a question, fetch and cross-check sources, and synthesize a cited report"), plus
  `/slides`, `/design`, `/dataviz`, `/code-review`, `/simplify`, `/claude-api` etc. These are not published as
  open SKILL.md files.
- Community research-oriented skills found in the lists have weak adoption: sanjay3290/ai-skills `deep-research`
  (450 stars), Anjos2/recursive-research (52), tapestry `article-extractor` (573), PleasePrompto/notebooklm-skill
  (7.8k, drives Google NotebookLM through a browser). karanb192's list adds `grounded` (literature reviews with
  live source discovery), `llm-wiki`, `docs-to-book` (crawl docs into a Typst PDF), `feynman-pdf`, `tldr`, and a
  large family of "humanize/unslop" prose editors.

Cross-listing count (presence in travisvn, ComposioHQ, karanb192, awesome-claude-code):
docx, pdf, pptx, xlsx, skill-creator, canvas-design, brand-guidelines, internal-comms, mcp-builder, webapp-testing,
web-artifacts-builder, slack-gif-creator and brainstorming each appear in 3 of 4; superpowers (as a bundle) and
Playwright skills in 4 of 4; theme-factory, deep-research in 1; doc-coauthoring, find-skills, grill-me in 0 (they
are newer than most lists).

### (a) Top ~25 skills ranked by evidence of adoption

Ranking blends skills.sh installs (primary, numeric), host-repo stars, and cross-listing. Installs are skills.sh
all-time counters on 2026-11-04.

| # | Skill | Source repo (stars) | Installs | One-line purpose | URL |
| --- | --- | --- | --- | --- | --- |
| 1 | find-skills | vercel-labs/skills (38k) | 4.2M | Router that finds/installs other skills from skills.sh | https://skills.sh/vercel-labs/skills |
| 2 | grill-me / grilling / grill-with-docs | mattpocock/skills (313k) | 1.5M / 1.1M / 1.3M | Relentless interview to sharpen a plan, decision or design (with-docs variant also writes ADRs/glossary) | https://github.com/mattpocock/skills |
| 3 | hyperframes family (5 skills) | heygen-com/hyperframes | 1.0-1.4M each | AI video composition CLI and registry | https://skills.sh/heygen-com/hyperframes |
| 4 | agent-browser | vercel-labs/agent-browser | 1.4M | Browser automation CLI for agents | https://skills.sh/vercel-labs/agent-browser |
| 5 | media-use | heygen-com/hyperframes | 1.3M | Media (image/video/audio) handling for agents | https://skills.sh/heygen-com/hyperframes |
| 6 | reddit-automation | flowkit-labs/skills | 1.2M | Reddit posting/monitoring automation | https://skills.sh/flowkit-labs/skills |
| 7 | design-mobile-apps | designed-by-ai/skills | 1.2M | Mobile UI design guidance | https://skills.sh/designed-by-ai/skills |
| 8 | tdd / improve-codebase-architecture / domain-modeling / codebase-design / diagnosing-bugs / code-review | mattpocock/skills (313k) | 0.85-1.2M each | Software-engineering workflow skills | https://github.com/mattpocock/skills |
| 9 | handoff | mattpocock/skills | 1.1M | Compact the current conversation into a handoff document for another agent | https://github.com/mattpocock/skills/tree/main/skills/productivity/handoff |
| 10 | frontend-design | anthropics/skills (187k) | 1.1M | Distinctive visual design guidance for UI; avoids generic "AI" aesthetics | https://github.com/anthropics/skills/tree/main/skills/frontend-design |
| 11 | prototype / triage / teach / setup-matt-pocock-skills | mattpocock/skills | 0.9-1.1M | Prototyping, issue triage, teaching, repo setup | https://github.com/mattpocock/skills |
| 12 | ui-taste | uizze.sh | 981K | UI taste/aesthetics guidance | https://skills.sh/uizze.sh |
| 13 | vercel-react-best-practices | vercel-labs/agent-skills (34k) | 871K | React/Next.js best practices | https://github.com/vercel-labs/agent-skills |
| 14 | lark-doc (+20 Feishu skills) | open.feishu.cn | 856K (17.9M total) | Feishu/Lark docs, OKR, video-conf integrations | https://skills.sh/open.feishu.cn |
| 15 | skill-creator | anthropics/skills (187k); also in claude-plugins-official (46k) | 424K | Create, evaluate, benchmark and description-optimize skills | https://github.com/anthropics/skills/tree/main/skills/skill-creator |
| 16 | brainstorming | obra/superpowers (312k) | 418K | Mandatory design-before-build interview for any creative work, software or not | https://github.com/obra/superpowers/tree/main/skills/brainstorming |
| 17 | systematic-debugging | obra/superpowers | 320K | Root-cause-first debugging discipline | https://github.com/obra/superpowers/tree/main/skills/systematic-debugging |
| 18 | writing-plans / executing-plans | obra/superpowers | 294K / 253K | Write and execute multi-step implementation plans | https://github.com/obra/superpowers |
| 19 | using-superpowers | obra/superpowers | 279K | Bootstrap: how to find and invoke skills every conversation | https://github.com/obra/superpowers |
| 20 | requesting/receiving-code-review, TDD, verification-before-completion, subagent-driven-development, dispatching-parallel-agents, writing-skills, using-git-worktrees, finishing-a-development-branch | obra/superpowers | 223-272K each | Remaining SDLC skills | https://github.com/obra/superpowers |
| 21 | pptx | anthropics/skills (proprietary) | 249K | Create/edit/read PowerPoint decks (pptxgenjs, python-pptx, LibreOffice QA) | https://github.com/anthropics/skills/tree/main/skills/pptx |
| 22 | pdf | anthropics/skills (proprietary) | 223K | Read, create, merge, split, fill, OCR PDFs (pypdf, pdfplumber, reportlab) | https://github.com/anthropics/skills/tree/main/skills/pdf |
| 23 | docx | anthropics/skills (proprietary) | 213K | Create/edit Word docs incl. tracked changes and comments (docx-js, OOXML scripts) | https://github.com/anthropics/skills/tree/main/skills/docx |
| 24 | webapp-testing | anthropics/skills | 198K | Playwright-based local web app testing | https://github.com/anthropics/skills/tree/main/skills/webapp-testing |
| 25 | xlsx | anthropics/skills (proprietary) | 193K | Create/edit spreadsheets with formulas, mandatory LibreOffice recalculation | https://github.com/anthropics/skills/tree/main/skills/xlsx |
| 26 | mcp-builder | anthropics/skills | 137K | Build MCP servers (FastMCP / TS SDK) | https://github.com/anthropics/skills/tree/main/skills/mcp-builder |
| 27 | canvas-design | anthropics/skills | 127K | PNG/PDF posters and static visual design | https://github.com/anthropics/skills/tree/main/skills/canvas-design |
| 28 | web-artifacts-builder / brand-guidelines / theme-factory / doc-coauthoring / internal-comms | anthropics/skills | 116K / 116K / 99K / 98K / 84K | Artifact tooling, Anthropic brand, 10 themes, doc co-authoring workflow, internal comms templates | https://github.com/anthropics/skills/tree/main/skills |

Observations: (1) the raw leaderboard is dominated by coding-agent and media skills; (2) among skills relevant to
documents, the Anthropic document quartet (pptx/pdf/docx/xlsx) plus skill-creator, brainstorming, doc-coauthoring and
internal-comms are the ones with both measurable installs and independent curation; (3) nothing research-specific
has broken through on install counts, which matches Vercel's finding that research skills are oversupplied and
under-installed, so the research workflow is a place to write a custom skill rather than adopt one.

## 4. What Anthropic says is built in, and where

- claude.ai Help Center, "Use skills in Claude" (https://support.claude.com/en/articles/12512180-using-skills-in-claude):
  "Anthropic provides several built-in skills that are available to all users, including: Enhanced Excel spreadsheet
  creation and manipulation; Professional Word document creation; PowerPoint presentation generation; PDF creation and
  processing." They activate automatically with code execution on. Enabled skills also apply inside the Claude for
  Excel/PowerPoint/Word/Outlook add-ins, and skills enabled on claude.ai sync into Claude Code (v2.1.273+) when signed
  in with the same account, but not when using an API key or Bedrock.
- Platform docs overview (https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview): pre-built
  skills are `pptx`, `xlsx`, `docx`, `pdf`, available on claude.ai, the Claude API (as `skill_id` in the `container`
  parameter with the code-execution tool), AWS, and Microsoft Foundry. "The pre-built document Skills (PowerPoint,
  Excel, Word, PDF) are not available in Claude Code, though the open-source Claude API skill comes bundled with it."
  The claude.ai runtime allows "no runtime package installation ... only pre-installed packages". Custom skills do not
  sync between claude.ai, the API and Claude Code.
- The anthropics/skills README: skill-creator, mcp-builder, webapp-testing, frontend-design, canvas-design,
  web-artifacts-builder, brand-guidelines, internal-comms, theme-factory, doc-coauthoring, algorithmic-art,
  slack-gif-creator, claude-api are "example skills ... already available to paid plans in Claude.ai" and installable
  into Claude Code as the `example-skills` plugin; docx/pdf/pptx/xlsx are the `document-skills` plugin and "power
  Claude's document capabilities under the hood".
- Claude Code additionally bundles its own slash-command skills and workflows (`/deep-research`, `/slides`,
  `/design`, `/dataviz`, `/code-review`, `/simplify`, `/claude-api`, `/skill-doctor`, ...) per
  https://code.claude.com/docs/en/commands.

## 5. What makes a skill effective (primary sources)

- Anthropic, "Skill authoring best practices"
  (https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices): concise is key ("Default
  assumption: Claude is already very smart"); set appropriate degrees of freedom (high = prose guidance, medium =
  parameterised scripts, low = "run exactly this script" for narrow-bridge tasks); test with every model you plan
  to use; gerund-form names (`processing-pdfs`); descriptions written in third person that say both what the skill
  does and when to use it, with concrete trigger terms, because Claude picks from "potentially 100+ available
  Skills" using only the description; keep SKILL.md under 500 lines and split into reference files; keep references
  one level deep (nested references get partially read with `head -100`); add a table of contents to reference
  files over 100 lines; use step-by-step workflows with checklists; build feedback loops (run validator, fix,
  repeat); avoid time-sensitive content; consistent terminology. The page's worked examples are a "Research
  synthesis workflow" (read sources, identify themes, cross-reference claims, structured summary, verify every
  citation) and a PDF form-filling workflow.
- Anthropic engineering post (https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills):
  progressive disclosure (metadata at startup, body on activation, resources on demand) is "the core design
  principle"; bundle deterministic scripts for things code does better than tokens; "start with evaluation", "structure
  for scale", "think from Claude's perspective" (watch real trajectories; name and description drive triggering),
  "iterate with Claude" (have the agent capture its successful approaches into the skill); audit skills from
  untrusted sources, especially bundled code and network access.
- agentskills.io specification (https://agentskills.io/specification): required `name` (1-64 chars, lowercase
  alphanumerics and single hyphens, must match the directory name) and `description` (1-1024 chars, what + when, with
  keywords); optional `license`, `compatibility` (1-500 chars, environment requirements), `metadata` map,
  `allowed-tools` (experimental); conventional `scripts/`, `references/`, `assets/`; metadata ~100 tokens,
  instructions < 5000 tokens recommended, SKILL.md under 500 lines; one-level-deep file references; validate with
  `skills-ref validate ./my-skill`.
- Claude Code's own frontmatter extensions (https://code.claude.com/docs/en/skills) are not in the spec and will not
  carry over: `when_to_use`, `argument-hint`, `disable-model-invocation`, `user-invocable`, `disallowed-tools`,
  `model`, `effort`, `context: fork`, `agent`, `hooks`; description + when_to_use are truncated at 1,536 chars.
- Vercel's report adds the demand-side view: portable, cross-industry, workflow-improving skills get installed;
  "the measure of a skill will shift from popularity to effectiveness ... skills will get tests and benchmarks".

## 6. What IBM Bob offers a ported skill (from bob.ibm.com/docs, fetched 2026-11-04)

- Format: `.bob/skills/<name>/SKILL.md` (project) or `~/.bob/skills/` (global); YAML front matter with `name` (must
  match the folder; lowercase kebab-case, max 64 chars, invalid names are skipped) and `description` (IDE docs:
  "skills without descriptions are ignored"; Shell docs: falls back to the first instruction line). Supporting files
  and subfolders (checklists, templates, scripts) are readable once activated. Project skill overrides a global one
  of the same name. Skills "load once per conversation". Bob asks permission before activating a skill unless
  `"approval": {"allowed_permissions": ["skill"]}` is set (Shell) or Auto-Approve is configured (IDE).
- Tools (https://bob.ibm.com/docs/ide/core-concepts/tools): read (`read_file`, `glob`, `grep`, `list_files`, symbol
  tools), write (`write_file`, `apply_diff`, `insert_content`, `search_and_replace`), `execute_command`,
  `spawn_subagent` (types `explore` on a lighter model and `general` with full tools; `fork_context` option),
  `start_subtask`, MCP tools, `switch_mode` (Agent/Plan/Ask/...), `use_skill`, `start_workflow`,
  `update_todo_list`, `ask_followup_question`. No web search or web fetch tool is listed. bob.ibm.com/llms.txt says
  "Advanced mode: access extended capabilities including MCP and browser tools" and lists "Browser Control". Context
  window is documented as 270,000 tokens.
- Practical consequences: anything a skill does via Python/Node scripts works through `execute_command` if the
  packages and binaries (LibreOffice, Poppler, pandoc, Node) are installed on the user's machine; web research needs
  an MCP server (search/fetch) or `curl` via `execute_command`, or Advanced-mode browser control; viewing rendered
  slide/page thumbnails depends on whether Bob can ingest images, which the tools page does not promise; Claude
  Code-only frontmatter and features (`context: fork`, hooks, `/slash` arguments, artifacts, `present_files`) must be
  stripped.

## 7. (b) Shortlist recommended for research + documentation work on Bob

Ordered by expected value for this user. "Port" means copy and adapt; "re-implement" means write a new skill in
the same shape because the original cannot be copied.

1. **docx (Anthropic) — re-implement, do not copy.** The most-curated document skill (3 of 4 lists, 213K installs)
   and the one that produces the user's primary deliverable. Its design is worth imitating exactly: create new
   documents with docx-js (or python-docx) from a script, edit existing ones by unpacking OOXML and editing
   `word/document.xml` in place with tracked-change and comment helpers, then validate and render to PDF/PNG via
   LibreOffice + pdftoppm to check the result. The proprietary LICENSE.txt forbids copying or derivative works, so the
   Bob skill must be an original SKILL.md plus original scripts (python-docx / docx-js are open source). Bob
   dependencies: Node or Python, LibreOffice, Poppler, pandoc installed locally; image review of rendered pages is
   optional but needs Bob image input or a human check.
2. **pptx (Anthropic) — re-implement.** 249K installs, 3 of 4 lists; PowerPoint is a named deliverable. Imitate the
   workflow: outline, then pptxgenjs or python-pptx generation, mandatory file QA (`python-pptx` reload, XML
   validation) and visual QA (render to thumbnails via LibreOffice and inspect), with the design-rules section
   (palette, typography, spacing, "avoid" list) rewritten in your own words. Same license constraint and the same
   local tool dependencies; the visual QA loop is the part most likely to degrade on Bob if it cannot read images.
3. **pdf (Anthropic) — re-implement, lighter lift.** 223K installs. Most of the skill is generic library guidance
   (pypdf, pdfplumber, reportlab, pdftotext, qpdf, OCR with ocrmypdf) that any author can restate; the valuable
   parts are the quick-start table of "which tool for which job" and the form-filling scripts. Depends only on
   pip packages plus poppler/qpdf; no browser or image viewing needed except for scanned-PDF OCR.
4. **doc-coauthoring (Anthropic, Apache) — port with edits.** 98K installs; a pure-prose three-stage workflow
   (context gathering, refinement/structure, reader testing) that matches technical-doc and proposal writing. It
   has conditional branches for "if artifacts are available" and "if no access to sub-agents"; on Bob take the
   file-based branch and the sub-agent branch (Bob has `spawn_subagent`, which fits the "test the doc with a fresh
   reader" step). No tooling dependency.
5. **skill-creator (Anthropic, Apache) — port the authoring half only.** 424K installs, 3 of 4 lists, also shipped in
   claude-plugins-official. The "Capture intent / Interview / Write the SKILL.md / Skill writing guide" sections are
   what the user needs to author further Bob skills. The eval half (spawn with-skill and baseline subagents in the
   same turn, grader subagent, HTML viewer opened in a browser, description-optimization loop) depends on parallel
   subagents, a local web viewer and Claude-side scripts; drop it or keep `quick_validate.py` only. Replace the
   Claude.ai- and Cowork-specific sections with Bob's `.bob/skills` conventions.
6. **brainstorming (superpowers, MIT) — port.** 418K installs, in 3 of 4 lists, explicitly "in software or out of
   it". It forces a requirements interview before drafting, which is the single biggest quality lever for reports and
   decks. Strip the superpowers-specific bits (`using-superpowers` bootstrap, visual-companion HTML, references to
   writing-plans) and keep the question-first protocol and the "one question at a time" rule.
7. **A research skill modelled on mattpocock `research` plus Anthropic's "research synthesis workflow" example — write
   new.** No research skill has measurable adoption (Vercel: research is the most oversupplied category), so adopt
   the two best-evidenced patterns instead: mattpocock's rule "investigate against primary sources (official docs,
   source code, specs, first-party APIs), not a secondary write-up ... follow every claim back to the source that owns
   it" and save findings as a Markdown file in the repo; Anthropic's five-step synthesis checklist (read all sources,
   identify themes, cross-reference claims, structured summary, verify citations). Dependency: Bob has no built-in
   web search/fetch, so the skill must name the mechanism (an MCP search/fetch server, `curl` via `execute_command`,
   or Advanced-mode browser) and should delegate reading to `spawn_subagent` (type `explore`) to protect the 270K
   context.
8. **internal-comms (Anthropic, Apache) — port the pattern, replace the examples.** 84K installs, 3 of 4 lists. It is
   a 32-line SKILL.md that routes to example files (3P updates, newsletter, FAQ answers, general comms). Swap in the
   user's own status-report, research-summary and technical-memo formats; this is the cheapest way to make Bob
   produce documents in house style. No dependencies.
9. **theme-factory (Anthropic, Apache) — port.** 99K installs. Ten named colour/font themes that can be applied to
   decks, docs and HTML reports, which gives consistent styling across pptx/docx/HTML output. Depends on fonts being
   installed; otherwise pure data.
10. **brand-guidelines (Anthropic, Apache) — port the structure, replace the content.** 116K installs, 3 of 4 lists.
    The skill is Anthropic's palette and typography, so the content is useless as-is, but the shape (a short SKILL.md
    with the exact colour hex values, fonts and usage rules, plus a python-pptx snippet) is the right template for an
    IBM/user brand skill that the pptx and docx skills can reference.
11. **handoff (mattpocock, MIT) — port, optional.** 1.1M installs. Compacts a long working session into a handoff
    document; useful for multi-session research projects and for writing up what was done. No dependencies.
12. **grill-me / grilling (mattpocock, MIT) — port, optional.** 1.5M / 1.1M installs. A stress-test interview for a
    plan or decision; valuable before committing to a report outline or an architecture doc. Overlaps with
    brainstorming, so pick one as the default and keep the other for explicit invocation.

Optional/secondary: xlsx (re-implement if reports carry data tables; the mandatory LibreOffice recalculation step is
the key idea), canvas-design (PNG/PDF one-pagers; needs Pillow/reportlab and fonts), mcp-builder (only if the user
ends up building a web-search MCP server for Bob), verification-before-completion (superpowers; the "evidence before
assertions" rule transfers directly to fact-checking a report).

## 8. (c) Not recommended for this user / this port, and why

- **docx / pptx / pdf / xlsx copied verbatim** — license forbids extraction, copying, derivative works and
  redistribution outside Anthropic services. Use them as reading material only.
- **find-skills (4.2M)** — a wrapper around the `npx skills` CLI and skills.sh search; Bob has its own skill
  loader and no skills.sh integration.
- **hyperframes family, media-use, ai-video-generation, ai-image-generation** — video/image generation products;
  off-task and SaaS-dependent.
- **agent-browser, webapp-testing, Playwright skills, NotebookLM skill** — require a driven browser (Playwright or
  Chrome); Bob's browser control exists only in Advanced mode and these skills assume Claude Code tool names.
- **web-artifacts-builder, frontend-design, ui-taste, design-mobile-apps, vercel-react-best-practices** — UI/React
  and claude.ai-artifact tooling; frontend-design's 1.1M installs are real but it is a UI aesthetics skill, not a
  document skill.
- **superpowers SDLC skills other than brainstorming/writing-skills/verification (tdd, systematic-debugging,
  writing-plans, executing-plans, subagent-driven-development, using-git-worktrees, code-review pair,
  finishing-a-development-branch, using-superpowers, diagnosing-superpowers)** — coding-lifecycle workflows, several
  hard-wired to Claude Code subagent/worktree semantics and to the superpowers bootstrap hook.
- **mattpocock engineering skills (tdd, triage, to-tickets, wayfinder, implement, codebase-design, etc.)** — coding
  and issue-tracker workflows; `setup-matt-pocock-skills` configures a tracker the user does not need.
- **claude-api, academy-guide, discernment-nudge, slack-gif-creator, algorithmic-art** — Anthropic-product,
  consumer-UX or novelty skills with no bearing on research/document output.
- **lark-* (Feishu), reddit-automation, Composio app-automation skills** — platform integrations the user did not
  ask for; the Composio entries exist to sell its plugin.
- **Community "deep-research"/"recursive-research" skills** — 450 and 52 stars, no install evidence, and they assume
  Claude Code's WebSearch/WebFetch tools; writing a Bob-native research skill (item 7 above) is less work than
  adapting them.

## 9. Porting checklist distilled from the primary sources

1. Keep only `name` and `description` in frontmatter (plus optional `license`, `compatibility`, `metadata` per the
   spec); delete Claude Code-only keys. `name` must equal the folder name and be kebab-case <= 64 chars (both the spec
   and Bob require this).
2. Write descriptions in third person, with what + when + trigger vocabulary (file extensions, deliverable names).
   Bob chooses skills from descriptions alone and loads a skill once per conversation, so the description carries
   the whole triggering burden.
3. Keep SKILL.md under 500 lines; move templates, examples and reference tables into sibling files referenced one
   level deep; put a table of contents at the top of any reference file over 100 lines.
4. Convert "use the X tool" instructions to Bob's names (`execute_command`, `spawn_subagent`, `read_file`,
   `ask_followup_question`) and remove artifact/`present_files`/Claude.ai branches.
5. Bundle deterministic scripts (render, validate, recalc, extract) and tell Bob to run them rather than reason
   through the task; declare system dependencies in `compatibility`.
6. Add a validator feedback loop to every document skill (reload the file, validate XML, render, compare).
7. Test each ported skill with and without the skill on 2-3 realistic prompts in Bob (the skill-creator and the
   engineering post both insist on this), then iterate on the description if it fails to trigger.
