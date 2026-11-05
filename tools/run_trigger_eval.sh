#!/usr/bin/env bash
# Does Bob pick the skill from its description alone? Runs the task WITHOUT the $skill prefix
# and reports whether use_skill <skill> appears in the transcript.
#   bash tools/run_trigger_eval.sh <skill>
set -uo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"; skill="${1:?}"
task="$root/evals/$skill/task.md"; run="$root/evals/$skill/runs/trigger-$(date +%Y%m%d-%H%M%S)"; mkdir -p "$run"
( cd "$run" && cat "$task" | bob run --format stream-json --workspace "$run" --max-turns "${MAX_TURNS:-40}" > transcript.jsonl 2> stderr.log )
if grep -q "use_skill" "$run/transcript.jsonl" && grep -q "\"$skill\"" "$run/transcript.jsonl"; then echo "TRIGGERED $skill"; else echo "NOT TRIGGERED $skill (description needs more trigger words)"; fi
echo "transcript: $run/transcript.jsonl"
