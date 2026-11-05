# IBM Bob skills and CLI, python-pptx rendering, MCP tool limits

## Answer
1. Yes. Bob Shell supports custom skills as a folder containing a SKILL.md with YAML front matter (name, description) followed by instructions. [S1]
   - Project skills load from `.bob/skills/<skill-name>/SKILL.md` in the project root. Global skills load from `~/.bob/skills/`. [S1]
   - Folder names must be lowercase kebab-case, up to 64 characters; Bob skips invalid ones. [S1]
   - A search-result summary said project skills override same-named global skills and that skills run only in certain modes. I did not verify either on the page I fetched, so I left them out of the claims.
2. Bob Shell's non-interactive command is `bob run [options] [prompt...]`, and it requires the `BOB_API_KEY` environment variable. [S2]
   - There is no documented flag that reads a prompt from a file. The documented way is to pipe the file on stdin: `cat prompt.txt | bob run`. [S2]
   - Inferred: `bob run "..." < prompt.txt` should behave the same way, but I did not test it.
   - Non-interactive runs use only non-destructive tools by default. The `--yolo` write flag came from a search summary and is not on the fetched page, so verify it before relying on it.
   - A search summary claimed `bob -p`. The current docs page does not show `-p`, so I am not using it.
3. No. python-pptx creates, reads and updates .pptx files and does not need PowerPoint installed. [S3]
   - Inferred: it has no slide-to-image function, because nothing in the docs mentions one. This rests on absence of evidence.
   - The usual workaround is LibreOffice headless conversion to PDF, then rasterising the pages (for example with pdftoppm). I got this from search results only and did not verify it.
4. The MCP spec sets no maximum number of tools. `tools/list` supports pagination, which lets a server return its tools across several pages. [S4]
   - Inferred: any practical cap comes from a client or model context limit, not from the spec.

## Counter-evidence
- Q1 is wrong if skills are gated to a particular mode or version. Searched the Bob docs and a search summary, which conflicted on modes. I did not resolve it.
- Q2 is wrong if a newer Bob version added a prompt-file flag or `-p`. Searched the live docs page and found no such flag.
- Q3 is wrong if python-pptx added native rendering. Searched the docs front page and found nothing, but I did not check the changelog.
- Q4 is wrong if a newer spec revision adds a limit. I read only the 2025-06-18 revision and found no limit.

## Confidence
| Question | Level | Why |
|---|---|---|
| 1 | High | Official Bob docs, quoted. |
| 2 | Medium | Official docs support `bob run` and stdin piping. The "no file flag" part is absence of evidence. |
| 3 | Medium | Docs describe no rendering. The conclusion is inferred. |
| 4 | Medium | Spec revision 2025-06-18 shows pagination and no cap. I did not read the latest revision. |

## Sources
[S1] https://bob.ibm.com/docs/shell/features/skills — "Create a folder inside .bob/skills/ in your project root, or use ~/.bob/skills/ for global skills."
[S2] https://bob.ibm.com/docs/shell/getting-started/start-bobshell-non-interactive — "Use the bob run subcommand to run Bob Shell non-interactively from the command line."
[S3] https://python-pptx.readthedocs.io/en/latest/ — "python-pptx is a Python library for creating, reading, and updating PowerPoint (.pptx) files."
[S4] https://modelcontextprotocol.io/specification/2025-06-18/server/tools — "To discover available tools, clients send a tools/list request."
