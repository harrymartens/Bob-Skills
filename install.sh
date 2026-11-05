#!/usr/bin/env bash
# Install the skills, the always-on rule and the example configs into a Bob config directory.
#   bash install.sh            -> ~/.bob (global: every project)
#   bash install.sh /path/to/project/.bob   (project-local)
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"; target="${1:-$HOME/.bob}"
mkdir -p "$target/skills" "$target/rules"
for s in "$here"/skills/*/; do n="$(basename "$s")"; rm -rf "$target/skills/$n"; cp -r "$s" "$target/skills/$n"; echo "skill  $n -> $target/skills/$n"; done
cp "$here/bob/rules/00-operating-discipline.md" "$target/rules/00-operating-discipline.md"; echo "rule   00-operating-discipline.md -> $target/rules/"
if [ ! -f "$target/AGENTS.md" ]; then cp "$here/bob/AGENTS.md" "$target/AGENTS.md"; echo "agents AGENTS.md -> $target/AGENTS.md"; else echo "agents AGENTS.md exists, not overwritten (merge $here/bob/AGENTS.md by hand)"; fi
echo
echo "Optional: MCP server for IBM docs -> see mcp/ibm-docs/README.md (bob mcp add ...)"
echo "Optional: custom modes            -> cp $here/bob/custom_modes.yaml $target/settings/custom_modes.yaml (global) or <project>/.bob/custom_modes.yaml"
echo "Restart Bob (new task) so it rescans skills."
