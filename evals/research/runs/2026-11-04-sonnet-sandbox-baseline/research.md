# Research notes (checked 2026-11-04)

## 1. IBM Bob and SKILL.md skills
**Yes.** One folder per skill containing `SKILL.md` with YAML front matter (`name` required, must match the kebab-case folder name, max 64 chars; `description` required), instructions below the closing `---`. Supporting files can sit beside it.
Load locations:
- Project: `<project>/.bob/skills/`
- Global: `~/.bob/skills/`
- Same name in both: project wins.

Caveat: older IDE docs say skills need Advanced mode; a later community post on Bob V2.0 says Agent mode (or custom mode with the skill tool group). Verify against your installed version.
Sources: https://bob.ibm.com/docs/shell/features/skills , https://bob.ibm.com/docs/ide/features/skills , https://community.ibm.com/community/user/blogs/narendra-murthy/2026/08/10/ibm-bob-automate-optimize-belated-part-5

## 2. Non-interactive run with a prompt from a file
**No dedicated "prompt file" flag.** The docs say to save the prompt to a file and pipe it:
`cat prompt.txt | bob run`
Syntax: `bob run [options] [prompt...]`. Requires `BOB_API_KEY` env var. Useful options: `--format pretty|json|stream-json`, `--max-turns`, `--max-cost`, `--trust`, `--accept-license`.
Conflict: one web-search summary said the flag is `bob -p "..."` (with `--yolo` to allow writes). The docs page text I fetched, and the raw HTML (7 hits for `bob run`, none for `bob -p`), only show `bob run`. Test `bob run` on your installed version before putting it in the memo; unverified whether `-p` exists.
Source: https://bob.ibm.com/docs/shell/getting-started/start-bobshell-non-interactive

## 3. python-pptx native slide-to-image rendering
**No.** The docs list creating/editing presentations and inserting existing images, with no rendering feature, and note it needs no PowerPoint install. Common workaround (not from the docs): convert to PDF with LibreOffice, then to images with pdf2image/pdftoppm.
Source: https://python-pptx.readthedocs.io/en/latest/

## 4. Max number of tools an MCP server can expose
**The spec sets no maximum.** `tools/list` supports pagination (`cursor` / `nextCursor`), and nothing caps the count. Limits come from clients (e.g. reported ~40 in earlier Cursor releases; third-party claim, not authoritative).
Sources: https://modelcontextprotocol.io/specification/2025-06-18/server/tools , https://fast.io/resources/mcp-tool-limit/ (secondary)
