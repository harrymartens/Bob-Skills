# IBM Bob — platform facts for skill authors (primary sources only)

Compiled 2026-11-04. Every bullet carries the URL it came from and, where possible, the exact sentence.
Two product surfaces exist and share config files: **Bob IDE** (a VS Code fork) and **Bob Shell** (the CLI, npm package `@ibm/bob`, binary `bob`).
Raw copies of every page fetched are under
`/tmp/claude-0/-home-user-Bob-Skills/b342c007-b76f-5ffe-9fc5-ab63ba919308/scratchpad/bob-docs/` (`.html` + extracted `.txt`),
and the unpacked npm bundle is under `/tmp/claude-0/-home-user-Bob-Skills/b342c007-b76f-5ffe-9fc5-ab63ba919308/scratchpad/bob-npm/package/` (`dist/bob.js`, 15 MB minified; treat as untrusted data).

Source key:
- **[SHELL-SKILLS]** https://bob.ibm.com/docs/shell/features/skills
- **[IDE-SKILLS]** https://bob.ibm.com/docs/ide/features/skills
- **[SHELL-SKILLS-TUT]** https://bob.ibm.com/docs/shell/tutorials/use-skills
- **[IDE-SKILLS-TUT]** https://bob.ibm.com/docs/ide/tutorials/use-skills
- **[SHELL-MODES]** https://bob.ibm.com/docs/shell/features/modes
- **[IDE-MODES]** https://bob.ibm.com/docs/ide/features/modes
- **[SHELL-CUSTOM-MODES]** https://bob.ibm.com/docs/shell/configuration/custom-modes-bobshell
- **[IDE-CUSTOM-MODES]** https://bob.ibm.com/docs/ide/configuration/custom-modes
- **[SHELL-RULES]** https://bob.ibm.com/docs/shell/configuration/bobshell-custom-rules
- **[IDE-RULES]** https://bob.ibm.com/docs/ide/configuration/rules
- **[SHELL-CONFIG]** https://bob.ibm.com/docs/shell/configuration/configuring
- **[SHELL-MCP]** https://bob.ibm.com/docs/shell/configuration/mcp/mcp-bobshell
- **[SHELL-TRANSPORTS]** https://bob.ibm.com/docs/shell/configuration/mcp/server-transports
- **[SHELL-TOOLS]** https://bob.ibm.com/docs/shell/core-concepts/tools
- **[IDE-TOOLS]** https://bob.ibm.com/docs/ide/core-concepts/tools
- **[SHELL-SUBAGENTS]** https://bob.ibm.com/docs/shell/features/subagents
- **[SHELL-NONINT]** https://bob.ibm.com/docs/shell/getting-started/start-bobshell-non-interactive
- **[SHELL-INT]** https://bob.ibm.com/docs/shell/getting-started/start-bobshell-interactive
- **[SHELL-INSTALL]** https://bob.ibm.com/docs/shell/getting-started/install-and-setup
- **[SHELL-SLASH]** https://bob.ibm.com/docs/shell/features/slash-commands
- **[SHELL-CTX]** https://bob.ibm.com/docs/shell/core-concepts/context-window-management
- **[SHELL-APPROVAL]** https://bob.ibm.com/docs/shell/configuration/approval-settings
- **[SHELL-HOOKS]** https://bob.ibm.com/docs/shell/configuration/lifecycle-hooks
- **[SHELL-ACP]** https://bob.ibm.com/docs/shell/features/acp
- **[SHELL-CHANGELOG]** https://bob.ibm.com/docs/shell/changelog
- **[IDE-CHANGELOG]** https://bob.ibm.com/docs/ide/changelog
- **[SHELL-INIT-TUT]** https://bob.ibm.com/docs/shell/tutorials/start-a-project
- **[IDE-STD-TUT]** https://bob.ibm.com/docs/ide/tutorials/standardize-bobs-behavior
- **[ONPREM-MODELS]** https://bob.ibm.com/docs/ide/enterprise/on-premises/model-gateway/supported-models
- **[NEWS-2026]** https://newsroom.ibm.com/2026-04-28-introducing-ibm-bob-ai-development-partner-that-takes-enterprises-from-ai-assisted-coding-to-production-ready-software
- **[NEWS-2025]** https://newsroom.ibm.com/2025-10-07-ibm-unveils-new-software-product-and-intelligent-infrastructure-capabilities-to-help-enterprises-operationalize-ai
- **[NPM]** https://registry.npmjs.org/@ibm/bob (metadata) and https://registry.npmjs.org/@ibm/bob/-/bob-2.0.9.tgz (bundle, v2.0.9, released 2026-10-23)
- **[AGENTSKILLS]** https://agentskills.io/specification.md

---

## 1. Skills (SKILL.md)

**Yes — Bob supports SKILL.md skills with YAML front matter, in `.bob/skills/<name>/SKILL.md` (project) and `~/.bob/skills/<name>/SKILL.md` (global).** The format is agentskills.io-compatible for `name`/`description`; Bob adds its own optional `metadata.*` keys and ignores agentskills `license`/`compatibility`/`allowed-tools`.

- Location: "Create a folder inside .bob/skills/ in your project root, or use ~/.bob/skills/ for global skills. Add a SKILL.md file inside that folder." — [SHELL-SKILLS], identical in [IDE-SKILLS].
- Precedence: "Priority: If both locations contain a skill with the same name, the project-level skill takes precedence." — [SHELL-SKILLS].
- Bundle confirms three-level first-wins: "**First-wins deduplication by name:** workspace > global > builtin. A workspace skill silently overrides a global one with the same name." — built-in `create-skill` skill text inside [NPM] `dist/bob.js` (saved as `bob-docs/builtin-create-skill.txt`).
- Format: "The SKILL.md file uses YAML front matter followed by the skill instructions" with example `---\nname: code-review\ndescription: Review code for bugs, security issues, and best practices\n---` — [SHELL-SKILLS].
- Required fields (Shell doc): "name: The skill's name. Match it to the skill's folder name—Bob uses the folder name to identify and reference the skill. Folder names must be lowercase kebab-case (letters, numbers, and single hyphens), up to 64 characters; Bob skips folders with invalid names." and "description: A clear summary that helps Bob decide when to activate this skill. If you omit it, Bob uses the first line of the instructions instead." — [SHELL-SKILLS].
- IDE doc wording differs slightly: "description: A clear summary that helps Bob decide when to activate this skill—skills without descriptions are ignored" — [IDE-SKILLS]. (The Shell doc and the bundle both say the first body line is the fallback; the IDE page says ignored. Treat "always write a description" as the safe rule.)
- Name regex (bundle): `sds=/^[a-z0-9]+(-[a-z0-9]+)*$/; function iAt(e){return e.length<=64&&sds.test(e)}` and the error `Invalid skill name "${e}". Must be kebab-case, max 64 characters, letters and numbers only`; reserved names: `["builtin","global","workspace"]` — [NPM] `dist/bob.js`.
- Name comes from the directory (bundle parser `$hi`): when the file is `SKILL.md`, name = basename of its parent dir (`u=o?r:...`); `description` falls back to the first non-empty body line, then to the name — [NPM] `dist/bob.js`.
- Silent skip: "**Validation is silent.** An invalid name (uppercase, underscores, spaces, leading/trailing or doubled dashes) causes the skill to be **skipped with no error**." — built-in `create-skill` text, [NPM].
- Instructions: "Everything below the --- delimiter becomes the instructions Bob receives when the skill is activated." — [SHELL-SKILLS].
- Supporting files: "You can include additional files and subfolders alongside SKILL.md to provide reference materials, templates, checklists, scripts, or other resources. Bob can read these files automatically once the skill is activated." — [SHELL-SKILLS]. Bundle: "**Supporting files:** any file placed alongside `SKILL.md` is available to the skill at activation time — scripts, static reference data, templates, etc." — [NPM].
- Loading semantics: "Skills load once per conversation to avoid duplicate prompts. Bob automatically determines when to activate a skill based on your request and the skill's description." — [SHELL-SKILLS]. The `use_skill` tool description in the bundle: "Activate a skill by name to load its full instructions into context. Only call this once per skill per current context window. If context was compacted and you need the instructions again, you may re-activate the skill." — [NPM].
- Approval: "By default, Bob asks for your permission before activating a skill." To skip: add `"skill"` to `approval.allowed_permissions` in `~/.bob/settings/settings.json` — [SHELL-SKILLS]. In `bob run` everything is pre-approved (see §7).
- Explicit invocation: Shell: "Type $ followed by a skill name to open the skill picker and insert a skill reference into your prompt." — [SHELL-INT]; tutorial uses `$changelog-entry Add a changelog entry for this change.` — [SHELL-SKILLS-TUT]. IDE: "The Skill Name is what you type to invoke the skill directly, for example /changelog-entry." — [IDE-SKILLS-TUT].
- New skill needs a new task: "Tell the user the skill will be available in the **next task** — start a new conversation to use it." — built-in `create-skill`, [NPM]; tutorial: "Restart Bob Shell after you add a skill." — [SHELL-SKILLS-TUT].
- Trust gating: skills in untrusted folders are suspended: "Untrusted folders run in safe mode: workspace-sourced configuration, skills, agents, rules, and MCP servers are suspended until you explicitly grant trust." — [IDE-CHANGELOG] (2.0.x "Workspace trust"). Tutorial: "the folder is trusted" is a troubleshooting check — [SHELL-SKILLS-TUT].

### Frontmatter fields Bob honours (from the bundle parser + built-in create-skill skill)

| Field | Source | Behaviour |
|---|---|---|
| `name` | docs + bundle | Display/reference name; directory name is canonical. |
| `description` | docs + bundle | Auto-activation trigger; fallback = first body line. |
| `metadata.user-invocable` (also accepted at top level `user-invocable`) | bundle | default `true`; "`false` ⇒ agent-only (no `/` command), but Bob can still auto-invoke it. Rarely wanted for user skills; this is how built-ins like `create-plan` work." |
| `metadata.disable-model-invocation` (also top level) | bundle | default `false`; "`true` ⇒ Bob will **not** auto-invoke it; it runs only when the user types `/<skill-name>`. This is the "Allow Bob to use this skill" toggle in settings." |
| `metadata.argument-hint` (also top level) | bundle | "Autocomplete hint shown after `/skill-name`, e.g. `"[issue-number]"`." |
| `metadata.groups` / `groups` | bundle | Parsed as an array of strings (tool-group names) if present: `I=Array.isArray(m.groups??a.data.groups)&&(...).every(k=>typeof k=="string")?...:void 0`. Not documented; effect unverified (likely restricts tool groups while skill active — verify locally). |

Parser excerpt ([NPM] `dist/bob.js`): `m=a.data.metadata||{},p=m["user-invocable"]??a.data["user-invocable"],A=p===!0||p===!1?p:!0,d=Xgt(m["argument-hint"]??a.data["argument-hint"]),S=(m["disable-model-invocation"]??a.data["disable-model-invocation"])===!0`.

The IDE tutorial itself shows a top-level `user-invocable: true` in a SKILL.md example — [IDE-SKILLS-TUT].

- Slash commands were migrated to skills: translation string "Bob has migrated {{count}} slash commands to skills. The old commands folders can be safely deleted." — [NPM] `dist/translations/en.json`. Migrated skills are written with `metadata: {"user-invocable": true, "disable-model-invocation": true}` — bundle `_writeSkills`.

### Other skill roots Bob scans (undocumented, from bundle)

- Global roots: `~/.bob`, `~/.agents`, `~/.claude` (each `<root>/skills/*` and `<root>/plugins/*/skills/*`). Workspace roots: `.bob/skills`, `.bob/plugins/*/skills`, `.agents/skills`, `.claude/skills`. Bundle: `Cmr=[join(homedir(),".bob"),join(homedir(),".agents"),join(homedir(),".claude")], xds=[".bob/skills",".bob/plugins/*/skills",".agents/skills",".claude/skills"]` — [NPM] `dist/bob.js`.
- Built-in guidance: "**Always default to the `.bob` folder.** ... Only use `.agents` or `.claude` instead if the user's workspace clearly shows they are already working in that ecosystem ... If the user does use an alternative root, the precedence order is .bob > .agents > .claude" — built-in `create-skill`, [NPM].
- Plugins: "You can now place skills, modes, rules, and MCP server definitions in a plugins/ subdirectory alongside your project" and "You can now place mcp.json configuration files inside ~/.bob/plugins/<plugin-name>/ to automatically load global MCP servers alongside your plugin skills, custom modes, and rules." — [IDE-CHANGELOG]. Bundle reads an optional `plugin.json` manifest (`{name, id}`) per plugin dir — [NPM].

### Built-in skills (bundle registry, `scope:"builtin"`)

`create-plan`, `create-skill`, `create-mode`, `configure-mcp`, `configure-hooks`, `build-mcp-server`, `create-chart`, `office-insights` — [NPM] `dist/bob.js`. Plan mode's customInstructions: "Must always start of every planning session, call use_skill with skill_name: "create-plan" to load the full planning workflow before responding." — [SHELL-MODES].

### Size limits

- No explicit byte/line limit for SKILL.md was found in docs or bundle (grep for maxSkill/MAX_RULES/etc. returned nothing). Only name length (64) is enforced.
- Guidance: "Keep the main SKILL.md file focused on the core workflow. Move detailed reference material, examples, and checklists to supporting files." — [SHELL-SKILLS]. "A skill that balloons into hundreds of lines of branching instructions is a sign the scope is wrong." — built-in `create-skill`, [NPM].
- Context budget matters: skills count against the 270k window; baseline example shows "Skills (454)" tokens — [SHELL-CTX].
- Comparison to agentskills.io: spec says `name` "Max 64 characters. Lowercase letters, numbers, and hyphens only", `description` "Max 1024 characters", plus optional `license`, `compatibility`, `metadata`, `allowed-tools` — [AGENTSKILLS]. Bob matches the name rule; Bob does not enforce the 1024-char description cap and does not read `allowed-tools`/`license`/`compatibility` (not present in bundle parser). Bob's `metadata` map is read for its own keys, which is compatible with the spec's "Arbitrary key-value mapping".

---

## 2. Modes

- Built-ins (current, v2): "By default, the following three modes are available with Bob:" Agent, Plan, Ask — [SHELL-MODES], [IDE-MODES].
  - Agent: role "You are Bob, a highly skilled software engineer..."; tools "Read, Edit, Execute, Browser*, MCP, Skill, Todo, Subagent, Mode" (IDE adds "Subtask"); allowed subagents "All".
  - Plan: tools "Read, Edit (Markdown and text files only), Browser*, MCP, Skill, Subagent, Mode"; allowed subagents "Explore".
  - Ask: tools "Read, Browser*, MCP, Skill, Subagent"; allowed subagents "Explore".
  - "* Browser tools are available only when you turn on the experimental Enable Web Fetch setting (experiments.webFetch). The setting is off by default." — [SHELL-MODES].
- History: v1 had "Code, Ask, Plan, Advanced, Orchestrator" — [IDE-CHANGELOG] 1.0.1: "Code mode writes, modifies, and refactors code. Ask mode provides answers... Plan mode... Advanced mode provides extended capabilities including MCP and browser tools. Orchestrator mode coordinates multi-step projects across specialties." Consolidated in 2.0: "Bob now ships with three focused default modes: Plan, Agent, and Ask. ... with Advanced and Orchestrator capabilities folded into the defaults." — [IDE-CHANGELOG]; "Agent mode replaces Code and Advanced modes" — [SHELL-CHANGELOG] 2.0.0.
- Custom modes: **yes**. Files: "Global modes: Edit ~/.bob/settings/custom_modes.yaml" and "Project modes: Edit .bob/custom_modes.yaml in your project" — [IDE-CUSTOM-MODES]; Shell: "Create or edit ~/.bob/settings/custom_modes.yaml for modes available across all projects" / "Create or edit .bob/custom_modes.yaml in your project root" — [SHELL-CUSTOM-MODES]. "Bob Shell uses the same configuration format as Bob IDE, supporting both YAML (preferred) and JSON formats."
- Schema (top-level key `customModes:` list) with properties `slug`, `name`, `description`, `roleDefinition`, `whenToUse`, `customInstructions`, `groups`, `allowedSubagents` — [SHELL-CUSTOM-MODES] table, [IDE-CUSTOM-MODES] "Mode components".
- Example — [IDE-CUSTOM-MODES]:
  ```yaml
  customModes:
    - slug: docs-writer
      name: 📝 Documentation Writer
      description: Writes and revises Markdown documentation.
      roleDefinition: You are a technical writer specializing in clear documentation.
      whenToUse: Use this mode for writing and editing documentation.
      customInstructions: Focus on clarity and completeness in documentation.
      groups:
        - read
        - - edit
          - fileRegex: ".*\\.(md|mdx)$"
            description: Markdown files only
        - skill
  ```
- Tool groups (Shell): "read ... edit: Modify files (can be restricted with fileRegex) ... execute: Execute terminal commands (command is accepted as a legacy alias) ... browser: Fetch public web pages (experimental; requires experiments.webFetch) ... mcp ... skill: Activate skills ... todo ... subagent ... mode" — [SHELL-CUSTOM-MODES]. IDE adds `workflow` and `subtask` groups — [IDE-CUSTOM-MODES].
- Validation: "slug must use only letters, numbers, and hyphens." "If you omit groups, the mode does not get any grouped tools." "If you set allowedSubagents, only the listed subagent presets are available in that mode." — [IDE-CUSTOM-MODES].
- Overriding built-ins: "You can override default Bob modes (such as Agent, Ask, or Plan) by creating a custom mode with the same slug in your project configuration." "Project-specific overrides take precedence over global overrides, which take precedence over defaults." — [IDE-CUSTOM-MODES]. Note Shell page states the opposite order for duplicate slugs: "If two modes share a slug, Bob Shell uses the first one it finds, in this order: Built-in modes (agent, plan, ask), User-level modes (~/.bob/settings/custom_modes.yaml), Project-level modes (.bob/custom_modes.yaml)" — [SHELL-CUSTOM-MODES]. **Conflict between IDE and Shell docs — verify locally.**
- Mode-specific instruction files: "Create mode-specific instruction files in .bob/rules-{mode-slug}/" ... "Files in the directory are loaded alphabetically and combined with the customInstructions property from your mode configuration." — [SHELL-CUSTOM-MODES], [IDE-CUSTOM-MODES].
- CLI selection: "bob --mode my-mode" (slug) — [SHELL-CUSTOM-MODES]; `--mode <mode>` "Starting mode (for example, agent, plan, ask)" on both `bob chat` and `bob run` — [SHELL-INT], [SHELL-NONINT]. Default via `session.defaultMode` in settings.json — [SHELL-CONFIG].
- Interactive: "/mode does not take an argument, and modes do not appear as separate slash commands. Custom workflow commands cannot change the active mode." — [SHELL-SLASH] (contradicts [SHELL-MODES] "type /mode <name> directly (for example, /mode ask)" — verify).
- Built-in `create-mode` skill exists: "Guide for creating a new custom Bob mode (custom_modes.yaml) — covers the schema, permission groups, roleDefinition, and file location." — [NPM].

---

## 3. Rules / instruction files

- **AGENTS.md** is the primary context file. Shell: "The simplest approach is an AGENTS.md file in your workspace root. Bob Shell loads it as workspace rules for every mode" — [SHELL-RULES]. Hierarchy: "Global context: ~/.bob/AGENTS.md (applies to all projects); Project context: AGENTS.md in project root and parent directories; Local context: AGENTS.md in subdirectories (for component-specific instructions)" — [SHELL-CONFIG].
- `/init` generates them: "Bob generates the main AGENTS.md file in the Galaxium Travels root directory. It also generates mode-specific context files in .bob/rules-agent/AGENTS.md, .bob/rules-ask/AGENTS.md, and .bob/rules-plan/AGENTS.md." — [SHELL-INIT-TUT]. The bundle's init prompt tells Bob to fold in other assistants' files: "If there are Claude Code rules (in CLAUDE.md), Cursor rules (in .cursor/rules/ or .cursorrules), or Copilot rules (in .github/copilot-instructions.md), make sure to include them" — [NPM] `dist/bob.js`. **CLAUDE.md / .cursorrules / .roorules are NOT loaded directly as rules; they are only read by /init to seed AGENTS.md.** (Bundle rule loader constants: `Dfi=".bob", npi="rules", Ofi="rules-", kds="AGENTS.md"` — no other filenames.)
- Rules directories: `.bob/rules/` (workspace, all modes), `.bob/rules-<mode-slug>/` (mode-specific), `~/.bob/rules/` (global), `~/.bob/rules-<mode-slug>/` — [SHELL-RULES], [IDE-RULES]. Windows global: `%USERPROFILE%\.bob\rules\`.
- Priority: "Bob Shell combines rules from multiple sources in this order: Global rules (~/.bob/rules/); Workspace rules (.bob/rules/). Within each level, mode-specific rules load before general rules. Workspace rules can override global rules." — [SHELL-RULES]. AGENTS.md: "Loaded after mode-specific rules but before general workspace rules" and "Disable with "bob-shell.useAgentRules": false in settings" (IDE: `"bob-code.useAgentRules": false`) — [SHELL-RULES], [IDE-RULES]. Bundle assembly order: `workspace_rules_<mode>`, `workspace_rules`, `agents_md`, `global_rules_<mode>`, `global_rules` — [NPM] function `Z3n`.
- File behaviour: "Recursive reading: Bob Shell reads all files in rules directories, including subdirectories; Alphabetical order...; Automatic filtering: Excludes cache files (.DS_Store, *.bak, *.cache, *.log, *.tmp, Thumbs.db); Symbolic links: Supported with maximum depth of 5; Empty files: Silently skipped" — [SHELL-RULES].
- Any file type: tutorial uses `.bob/rules/basic_rules.md`; examples show `.md` and `.txt` — [IDE-STD-TUT], [IDE-CUSTOM-MODES].
- Rules count against context: "Rules: Custom instructions from project and mode rule files (for example, AGENTS.md or .bob/rules-*)" — [SHELL-CTX]. Advice: "Keep custom rules and AGENTS.md short — put only setup, test, and style commands there" — [SHELL-CTX].
- No `.bobrules` file exists (not in docs or bundle). `.bobignore` controls file access — [SHELL-RULES] sidebar, [IDE-CHANGELOG].
- Hooks (related): `hooks` key in `~/.bob/settings/settings.json` (global) or `.bob/settings.json` (workspace); events SessionStart, UserPromptSubmit, PreToolUse, PostToolUse, PreCompact, PostCompact, Stop; "Workspace hooks only run in trusted folders." — [SHELL-HOOKS].

---

## 4. MCP

- Files: "Global configuration: Settings in ~/.bob/settings/mcp.json apply to all workspaces; Project-level configuration: Settings in .bob/mcp.json apply only to the current project. When a server name exists in both global and project configurations, the project-level configuration takes precedence." — [SHELL-MCP]. Bundle also loads `.bob/plugins/<name>/mcp.json` and `~/.bob/plugins/<name>/mcp.json` — [NPM], [IDE-CHANGELOG].
- JSON shape — [SHELL-MCP]:
  ```json
  {
    "mcpServers": {
      "server1": {
        "command": "python",
        "args": ["/path/to/server.py"],
        "env": { "API_KEY": "your_api_key" },
        "alwaysAllow": ["tool1", "tool2"],
        "disabled": false
      }
    }
  }
  ```
  Remote: `{"mcpServers": {"remote-server": {"url": "https://your-server-url.com/mcp"}}}`.
- Properties: "command: Path to the executable for Stdio transport; url: HTTP endpoint URL for Streamable HTTP transport ... args ... headers ... env ... cwd ... timeout: Request timeout in milliseconds (default: 600,000 ms / 10 minutes); alwaysAllow: Tool names to approve automatically ...; disabled" — [SHELL-MCP].
- Transports: "Bob supports STDIO and Streamable HTTP; SSE is no longer supported" — [SHELL-TRANSPORTS]. "Servers configured with "type": "sse" fail to connect with a "Legacy HTTP+SSE is unsupported" error." — [SHELL-MCP]. Protocol versions supported: 2025-11-25, 2025-06-18, 2025-03-26, 2024-11-05, 2024-10-07 — [SHELL-MCP].
- Secrets: "Secrets are stored encrypted in ~/.bob/settings/ and can be referenced in MCP server configurations using ${KEY} syntax." (`/manage-secrets set KEY VALUE`) — [SHELL-SLASH].
- CLI management: "Manage Model Context Protocol servers directly from the CLI with bob mcp add, bob mcp add-json, bob mcp remove, and bob mcp list. Supports both global and workspace scopes" — [SHELL-CHANGELOG] 2.0.0. Bundle command definitions — [NPM] `dist/bob.js`: `bob mcp add <name> <commandOrUrl> [args...]` with `-s, --scope <scope>` "Configuration scope: workspace or global" (default workspace), `-t, --transport <transport>` "Transport type: stdio or http", `-e, --env <KEY=VALUE>` (repeatable), `-H, --header <K: V>` (repeatable), `--timeout <ms>`, `--include-tools <tools>` "Comma-separated list of tools to always allow", `--exclude-tools <tools>` "Comma-separated list of tools to disable"; `bob mcp add-json <name> <json>` "Add or overwrite an MCP server entry from a raw JSON config string"; `bob mcp remove <name> [-s scope]`; `bob mcp list`. Example: `bob mcp add -s global -t http my-remote https://host/mcp -H "Authorization: Bearer ${TOKEN}"` (unverified composite; see §10).
- Tool naming: "mcp__<server>__<tool> — Each tool from a connected MCP server is exposed under its own name" — [SHELL-TOOLS]. MCP resources via `@server:resource-name`; MCP prompts appear as slash commands — [SHELL-INT], [SHELL-SLASH].
- Disable: `bob run --disable-mcp`, or `session.mcp: false` — [SHELL-NONINT], [SHELL-CONFIG].

---

## 5. Built-in tools

Shell tool list — [SHELL-TOOLS]: `read_file`, `grep`, `glob`, `list_files` (read); `write_file`, `apply_diff`, `insert_content`, `search_and_replace` (write); `execute_command` (command); `mcp__<server>__<tool>`; `switch_mode`; `ask_followup_question`. IDE adds `GetSymbolsOverview`, `FindSymbol`, `FindReferencingSymbols`, `spawn_subagent`, `start_subtask`, `use_skill`, `start_workflow`, `update_todo_list` — [IDE-TOOLS]. Bundle additionally registers `office_read`, `office_edit`, `create_html_artifact`, `web_fetch`, `web_search` — [NPM].

- **Web fetch: yes, experimental, off by default.** "browser: Web fetch tool (experimental, off by default; enable experiments.webFetch)" — [SHELL-TOOLS]. Settings description: "experiments.webFetch ... When enabled, new tasks can fetch and read content from public HTTP and HTTPS URLs" — [NPM]. Bundle tool id `web_fetch`, groups `["browser"]`: "Use this tool only when completing the user's request requires reading the contents of a specific public HTTP or HTTPS page, the exact URL is already available..." — [NPM].
- **Web search: exists in IDE as experimental; present in Shell bundle but not documented for Shell.** "Web search (experimental) — You can now let Bob search the web to answer questions that require up-to-date information. Turn on the experimental web_search tool in **Bob Settings → Chat** to try it" — [IDE-CHANGELOG]. Bundle `web_search` tool: "Search the public web for current information. Returns result titles, URLs, and snippets." and system-prompt part "Use `web_search` to discover relevant public pages. When `web_fetch` is available, use it to read the full contents..." — [NPM]. No Shell doc page mentions web_search; how to enable it in Shell is unknown (see §10).
- **Todo list: yes.** "update_todo_list — Create or update a markdown checklist of task steps" — [IDE-TOOLS]; Shell group "todo: To-do list management tools" (default in Agent only) — [SHELL-TOOLS]. Agent mode instructions: "If you're following a set to do list as part of your task, use 'update_todo_list' as you progress" — [SHELL-MODES].
- **Subagents: yes.** "A subagent is an independent agent that Bob can spawn to handle a focused, self-contained task. It runs in its own isolated context window" — [SHELL-SUBAGENTS]. Types: "explore — Read-only codebase exploration, runs on a lighter model" and "general — Full tool access, runs on the default model". "You are prompted to approve the spawn before it starts." `fork_context: true` passes conversation history. Bundle: explore preset `groups:["read"], modelTier:"explorer", denyTools:["update_todo_list","use_skill"]` — [NPM]. Disable with `--disable-subagents` or `session.subagents: false`.
- **Subtasks (IDE only): yes.** "start_subtask — Create a new task with a title, instructions, and optional todo list" — [IDE-TOOLS]. Shell says subtasks appear in the UI; the `subtask` group exists in Shell approval settings — [SHELL-APPROVAL].
- **No Roo-style `new_task`, `attempt_completion`, `browser_action`, `use_mcp_tool`, `access_mcp_resource`, `list_code_definition_names`** — none of these strings exist in the bundle — [NPM].
- Workflows (IDE): "start_workflow — Launch a named workflow with its own structured steps" e.g. `/create-pull-request`, `/review` — [IDE-TOOLS].
- Tool groups and defaults per mode table (read/edit/execute/browser/mcp/skill/todo/subagent/mode) — [SHELL-TOOLS]. Disable per run: `bob run --disable-tool-groups execute,mcp "Review @src/"` — [SHELL-TOOLS].
- Ask-user: `ask_followup_question` — [SHELL-TOOLS]; the built-in `create-skill` skill says "Always ask questions using the `ask_followup_question` tool." — [NPM].

---

## 6. Model and thinking

- Public positioning: "Bob dynamically routes tasks to a suitable model based on accuracy, performance, and cost, drawing on a mix of frontier models including Anthropic Claude, Mistral open source models, and IBM Granite, alongside specialized fine-tuned models for code reasoning, security, and next-edit prediction." — [NEWS-2026]. Earlier: "IBM will integrate Anthropic's large language models (LLMs) directly into select IBM software products, starting with Project Bob, its new AI-first IDE." — [NEWS-2025].
- Self-hosted supported frontier models: "Claude Sonnet 5", "Claude Opus 4.8" (Anthropic / AWS Bedrock), "Google Gemini 3.7 Flash", "OpenAI GPT5.6 Sol"; air-gapped: Mistral Medium 3.5 (Z package only), Nvidia Nemotron 3 Ultra / 3.5 Super, Poolside Laguna S 2.1; guardrail `openai/gpt-oss-20b`. "Tip: For optimal results on complex IBM Z tasks ... frontier models such as Claude Sonnet deliver the highest level of reasoning" — [ONPREM-MODELS]. Example gateway config uses `max_input_tokens: 270000`, `max_output_tokens: 20000`.
- **User model selection in SaaS Bob Shell is NOT exposed by default.** Bundle: `-m, --model <model>`, `--provider <provider>` ("harness or openrouter"), `--reasoning-effort <effort>`, `-o, --output <path>`, the `session.model` setting and the `/model` picker are all registered only when `Dm()` is true, where `function Dm(){return Lls&&process.env.BOB_DEV_KEY===Uls}` (an internal dev-key gate) — [NPM] `dist/bob.js`. ACP.md: "Model selection (`session/set_model`) is not supported; use modes instead." — [NPM] `ACP.md`.
- Model tiers (internal abstraction): `her=["fast","premium","ultra","explorer"]`, default `RM="premium"`; subagent explore preset uses tier `explorer`; env var `BOB_USE_MODEL_E...` exists — [NPM]. Modes/subagents, not users, pick tiers.
- **Reasoning effort**: values `["none","minimal","low","medium","high","xhigh","max"]` passed as `providerOptions.bob.reasoningEffort`; CLI flag `--reasoning-effort` is dev-gated (see above). No public settings key for thinking/extended thinking was found in docs. — [NPM].
- FAQ has questions "Can I choose which model Bob uses?" and "Can our organization choose or restrict which models Bob routes to?" but answer bodies are rendered client-side and were not retrievable — https://bob.ibm.com/docs/shell/faq (verify in browser).

---

## 7. CLI (Bob Shell)

- Package/binary: npm `@ibm/bob`, `"bin": {"bob": "dist/bob.js"}`, latest 2.0.9 (2026-10-23), `"engines": {"node": ">=22"}` — [NPM] package.json. Docs say "Node.js Version 24 or later" — [SHELL-INSTALL]. Install: `curl -fsSL https://bob.ibm.com/download/bobshell.sh | bash` or `npm install -g @ibm/bob` — [SHELL-INSTALL].
- Top-level usage (from package README in [NPM]):
  ```
  bob [options] [command]
  Options:
    -v, --version              Show current version number
    -p, --prompt <prompt>      Prompt to send to the agent
    -r, --resume [task-id]     Open the resume picker, or resume a specific task id
    --list-tasks [limit]       List available tasks (optional: number or 'all', default 20)
    --show-license             Show full paths to license files for review
    --accept-license           Accept the IBM license agreement and continue
    -h, --help                 Display help for command
  Commands:
    chat [options]             Launch the interactive terminal UI client
    run [options] [prompt...]  Execute a single task in headless mode
    mcp [options]              Manage MCP server configurations
    acp [options]              Start Bob Shell as an Agent Client Protocol server
  ```
- **Headless**: `bob run [options] [prompt...]` — "Use the bob run subcommand to run Bob Shell non-interactively from the command line." — [SHELL-NONINT]. Requires `BOB_API_KEY`: "bob run requires a valid API key set as the BOB_API_KEY environment variable. Interactive SSO or IBMid tokens from bob chat are not reused for non-interactive sessions." — [SHELL-NONINT]. "When running non-interactively with bob run, all tools are pre-approved. You are not prompted to approve tool calls during execution." — [SHELL-NONINT].
- Prompt from file / stdin: "echo "Explain this project" | bob run", "cat prompt.txt | bob run", "cat buildError.txt | bob run "Explain this build error"" — [SHELL-NONINT]. (Bundle: stdin is read when not a TTY and combined with the argument prompt.)
- Output formats: `--format <format>` "Output format: pretty (default), json, or stream-json". json = "a single JSON object after the session completes" with fields `type:"result"`, `timestamp`, `status` ("success"/"error"), `stats{task_id,total_tokens,input_tokens,output_tokens,cache_read_tokens,cache_write_tokens,cache_ratio,duration_ms,session_costs,tool_calls}`, `last_message`. stream-json = NDJSON events `message`, `tool_use`, `tool_result`, `error`, `result`. Example: `bob run --format stream-json "Audit @src/" | grep '"type":"result"' | jq '.last_message'` — [SHELL-NONINT].
- `bob run` options — [SHELL-NONINT]: `--format`, `--mode <mode>`, `--max-cost <bobcoins>`, `--max-turns <n>`, `--disable-mcp`, `--disable-subagents`, `--disable-tool-groups <groups>`, `--workspace <path>`, `--log-level <level>`, `--resume <task-id>|latest`, `--team-id <id>`, `--trust`, `--accept-license`. "Bob Shell now accepts --max-cost 0 and --max-turns 0 to remove the cost and turn limits" — [SHELL-CHANGELOG] 2.0.6. Prompt may follow boolean flags: `bob run --disable-mcp "fix the tests"` — [SHELL-CHANGELOG].
- Selecting a mode from CLI: `bob run --mode test-runner "Run the test suite and report failures"`; `bob run --mode test-runner --format json "Run tests" > results.json` — [SHELL-CUSTOM-MODES].
- Selecting a skill from CLI: **no dedicated flag.** Skills are referenced inside the prompt text with `$<skill-name>` (Shell picker inserts `$changelog-entry ...`) or activated automatically by description — [SHELL-SKILLS-TUT], [SHELL-INT]. For evals, put `$<skill-name>` in the `bob run` prompt or rely on auto-activation (unverified that `$name` is honoured in `bob run` prompts — see §10).
- File references: `@path` in prompts; "Files are inlined up to 100 KB per file. Total inlined content across all @ mentions is capped at 500 KB. Directories show up to 50 entries." — [SHELL-INT].
- Interactive: `bob chat [options]` with `--mode`, `--auto-approve`, `--trust`, `--resume`, `--instance-id`, `--team-id`, `--log-level` — [SHELL-INT]. `--yolo` is deprecated alias for `--auto-approve` — [NPM].
- Task listing: `bob --list-tasks all` emits NDJSON when piped: `{"id","title","status","workspace","updatedAt"}` — [SHELL-NONINT].
- Settings: `~/.bob/settings/settings.json` (user), `<workspace>/.bob/` (project); keys `session.maxTurns` (100), `session.defaultMode` ("agent"), `session.mcp`, `session.subagents`, `logging.logLevel`, `tasks.retentionDays`, `telemetry.enabled`; "CLI flags always override file values for the current session." — [SHELL-CONFIG]. Logs: `~/.bob/logs/shell/`; `BOB_LOG_LEVEL=debug`.
- ACP: `bob acp` exposes Bob to Zed/IntelliJ/Neovim/Xcode; mode per session via `_meta["bob/mode"]` — [SHELL-ACP], [NPM] ACP.md.
- Export: `/export <json|markdown> [file-name]` — [SHELL-SLASH].

---

## 8. Context window and limits

- "Each session in Bob Shell has a context window — the token budget for that conversation. The limit is 270,000 tokens. Everything Bob loads counts against it." "Reserved for model response: Tokens held back for Bob's next reply (typically 20,000)." "Compaction typically begins around 190,000 tokens of total usage." — [SHELL-CTX]. "The context window has increased from 200,000 to 270,000 tokens" — [IDE-CHANGELOG] 2.0.
- What fills it: System prompt, Tool definitions, MCP Tools, Rules, Skills, Messages. Baseline example "about 8,500 tokens. Most of that is Tool definitions (5,100), System prompt (1,500), Rules (830), and Skills (454)." "Bob re-sends the full overhead stack on every prompt." — [SHELL-CTX].
- No hard byte limit on skill or rule files found (see §1, §3). Only limits: skill name ≤ 64 chars; `@`-mention inlining 100 KB/file, 500 KB total — [SHELL-INT].
- Compaction hooks `PreCompact`/`PostCompact`; `/compact` command — [SHELL-HOOKS], [SHELL-SLASH].

---

## 9. Lineage — fork of Roo Code / Cline / Kilo?

**Evidence says: not a code fork, but clearly modelled on the Roo Code family's configuration conventions.**

- No `roo`, `roocode`, `.roomodes`, `kilocode`, `boomerang`, `attempt_completion`, `new_task`, `browser_action`, `use_mcp_tool`, `access_mcp_resource`, or `list_code_definition_names` strings exist in the 15 MB Shell bundle. The only `cline` hits are the word "decline"; the only `.roorules` hit is in the `/init` prompt listing other assistants' files — [NPM] `dist/bob.js` (grep performed 2026-11-04).
- Package has no dependencies on Roo/Cline packages: `dependencies` is empty; optional deps are `@lydell/node-pty`, `@officecli/officecli`, `@vscode/ripgrep` — [NPM] package.json. The engine is IBM's own "harness" (`--provider` values "harness or openrouter"; bundle namespace `com.ibm.bob`).
- Bob IDE is a VS Code fork (not an extension): IBM community statement that Bob "will not be an extension in VS Code, but Bob's interface will be forked from VS Code" — https://community.ibm.com/community/user/discussion/project-bob-ibmi-competitors (search snippet; secondary). IBM calls it "an AI-first IDE" — [NEWS-2025].
- Roo-Code-shaped conventions nevertheless match closely: `customModes:` YAML with `slug/name/roleDefinition/whenToUse/customInstructions/groups` and `- [edit, {fileRegex}]` tuples; `rules-{mode-slug}/` directories; `.bobignore` (cf. `.rooignore`); tools `apply_diff`, `insert_content`, `search_and_replace`, `ask_followup_question`, `switch_mode`, `update_todo_list`; v1 modes "Code/Ask/Architect-like Plan/Orchestrator"; "alwaysAllow" in mcp.json — [SHELL-CUSTOM-MODES], [SHELL-TOOLS], [SHELL-MCP], [IDE-CHANGELOG]. Roo Code's docs (docs.roocode.com, custom modes / custom instructions pages) therefore describe a near-identical config surface, but Roo's agent loop (`new_task`, `attempt_completion`) is not what Bob runs; Bob v2 replaced those with `spawn_subagent`, `start_subtask`, `use_skill`.
- Skills follow the Claude Code / agentskills.io convention (SKILL.md, `user-invocable`, `disable-model-invocation`, `argument-hint`, scanning `.claude/skills` and `.agents/skills`) — [NPM] parser, [IDE-SKILLS-TUT].
- Conclusion for skill authoring: use agentskills.io-style SKILL.md (name = dir, description = trigger), plus Bob's optional `metadata` keys; do not rely on Roo docs for skills, but Roo docs are a reasonable mental model for modes/rules.

---

## 10. Unknown / needs local verification

Run on the machine where Bob Shell is installed and paste outputs:

```bash
bob --version
bob --help
bob chat --help
bob run --help
bob mcp --help && bob mcp add --help
bob acp --help
# Does -m/--model, --reasoning-effort, --provider appear? (expected: hidden unless BOB_DEV_KEY)
bob run --help | grep -i -E 'model|reasoning|provider|output'
# Config and skill directories actually present
ls -la ~/.bob ~/.bob/settings ~/.bob/skills ~/.bob/rules ~/.bob/plugins 2>/dev/null
cat ~/.bob/settings/settings.json
cat ~/.bob/settings/mcp.json 2>/dev/null; cat .bob/mcp.json 2>/dev/null
ls -la .bob .bob/skills .bob/rules .bob/rules-* .bob/custom_modes.yaml 2>/dev/null
# Does Bob pick up skills from .claude/skills or .agents/skills in this workspace? (bundle says yes)
mkdir -p .claude/skills/probe-claude .agents/skills/probe-agents .bob/skills/probe-bob
for d in .claude/skills/probe-claude .agents/skills/probe-agents .bob/skills/probe-bob; do printf -- '---\nname: %s\ndescription: Probe skill; reply with the word PROBE-%s\n---\nReply with PROBE-%s.\n' "$(basename $d)" "$(basename $d)" "$(basename $d)" > "$d/SKILL.md"; done
# Interactive: run `bob chat`, type `$` and see which probe skills the picker lists; or /skills
# Headless: does $skill-name in the prompt force activation under bob run?
export BOB_API_KEY=...   # Inference-scope key from bob.ibm.com
bob run --format json --max-turns 3 '$probe-bob Do it' | jq .
bob run --format stream-json --max-turns 3 'Use the probe-bob skill' | grep -E '"tool_use"|use_skill'
# Is web_search available in Shell, and how is experiments.webFetch set?
grep -n -i 'webFetch\|web_search\|experiments' ~/.bob/settings/settings.json
bob run --format stream-json --max-turns 2 'Fetch https://example.com and quote its title' | grep -i 'web_fetch\|web_search'
# Which tool groups / skill metadata.groups actually restrict tools (undocumented):
# create a skill with `metadata: {groups: [read]}` and observe whether edit tools are refused.
# Mode precedence conflict (IDE doc: project > global > builtin; Shell doc: builtin > user > project):
# define slug `ask` in both ~/.bob/settings/custom_modes.yaml and .bob/custom_modes.yaml with different names, run `bob chat --mode ask`, check footer mode name.
# Does `/mode ask` (with argument) work in bob chat? (docs conflict)
# FAQ answers on model choice (client-rendered): open https://bob.ibm.com/docs/shell/faq in a browser,
#   sections "Can I choose which model Bob uses?" and "Can our organization choose or restrict which models Bob routes to?"
# Skill file size: create a 200 KB SKILL.md and check `bob run --format json` stats / any truncation warning in ~/.bob/logs/shell/
```

Open questions these settle: (a) whether `$skill` references work in `bob run`; (b) whether `.claude/skills` discovery is live in the installed version; (c) real `bob run --help` flag set (incl. any model/effort flags); (d) how to enable web_search in Shell; (e) mode-slug precedence; (f) any skill/rule size truncation.
