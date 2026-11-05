#!/usr/bin/env bash
# Run one skill eval through Bob Shell headlessly and check the result.
#
#   bash tools/run_eval.sh <skill> [--no-skill]
#
# Requires: bob (Bob Shell) on PATH, BOB_API_KEY exported, skills installed via install.sh.
# Writes evals/<skill>/runs/<timestamp>[-baseline]/{transcript.jsonl,transcript.txt,result.json,...artifacts}
# then runs evals/<skill>/check.sh on that directory and records PASS/FAIL in evals/<skill>/runs/LATEST.
set -uo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
skill="${1:?usage: run_eval.sh <skill> [--no-skill]}"; shift || true
baseline=0; [ "${1:-}" = "--no-skill" ] && baseline=1
task="$root/evals/$skill/task.md"; [ -f "$task" ] || { echo "no task at $task"; exit 2; }
command -v bob >/dev/null || { echo "bob not on PATH"; exit 2; }
[ -n "${BOB_API_KEY:-}" ] || { echo "BOB_API_KEY not set (bob run needs an Inference-scope key)"; exit 2; }

stamp="$(date +%Y%m%d-%H%M%S)"; [ $baseline -eq 1 ] && stamp="$stamp-baseline"
run="$root/evals/$skill/runs/$stamp"; mkdir -p "$run"
prompt="$(cat "$task")"
if [ $baseline -eq 0 ]; then
  # operating-discipline is a rule (always on); other skills are invoked explicitly so the eval
  # tests the skill body, not description triggering. Triggering is tested by run_trigger_eval.sh.
  [ "$skill" != "operating-discipline" ] && prompt="\$$skill $prompt"
  extra=""
else
  # baseline: hide this repo's skills/rules by running from a scratch workspace with no .bob dir
  extra="--disable-tool-groups skill"
fi
echo "run dir: $run"
( cd "$run" && printf '%s' "$prompt" | bob run --format stream-json --workspace "$run" --max-turns "${MAX_TURNS:-60}" $extra \
    > transcript.jsonl 2> stderr.log )
grep '"type":"result"' "$run/transcript.jsonl" | tail -1 > "$run/result.json"
# human-readable transcript: tool calls and messages in order
python3 - "$run/transcript.jsonl" > "$run/transcript.txt" <<'PY'
import json, sys
for line in open(sys.argv[1], encoding="utf-8", errors="replace"):
    try: ev = json.loads(line)
    except Exception: continue
    t = ev.get("type")
    if t == "tool_use": print(f"[tool_use] {ev.get('name') or ev.get('tool')}: {json.dumps(ev.get('input') or ev.get('args') or {})[:400]}")
    elif t == "tool_result": print(f"[tool_result] {str(ev.get('content') or ev.get('output') or '')[:400]}")
    elif t == "message": print(f"[message] {str(ev.get('content') or ev.get('text') or '')[:2000]}")
    elif t == "result": print(f"[result] status={ev.get('status')} last_message={str(ev.get('last_message'))[:4000]}")
    elif t == "error": print(f"[error] {ev}")
PY
if bash "$root/evals/$skill/check.sh" "$run" > "$run/check.log" 2>&1; then verdict=PASS; else verdict=FAIL; fi
tail -3 "$run/check.log"
echo "$verdict $stamp" | tee "$root/evals/$skill/runs/LATEST"
echo "transcript: $run/transcript.txt"
