#!/usr/bin/env bash
# Usage: bash evals/operating-discipline/check.sh <run-dir>  (expects transcript.txt and the final message in it)
set -u
run="${1:-.}"; t="$run/transcript.txt"; fail=0
[ -f "$t" ] || { echo "FAIL: $t missing"; exit 1; }
for k in "Produced:" "Checked:" "Not verified:" "Decisions I made"; do grep -q "$k" "$t" || { echo "FAIL: final report lacks '$k'"; fail=1; }; done
todo_line=$(grep -n -iE "update_todo_list|TaskCreate|todo" "$t" | head -1 | cut -d: -f1)
write_line=$(grep -n -E "\] (write_file|write_to_file|apply_diff|insert_content|execute_command|Bash|Write|Edit)\b" "$t" | head -1 | cut -d: -f1)
echo "first todo at line ${todo_line:-none}, first write/command at line ${write_line:-none}"
[ -n "$todo_line" ] && [ -n "$write_line" ] && [ "$todo_line" -lt "$write_line" ] || { echo "FAIL: no todo before first action"; fail=1; }
grep -qiE "spawn_subagent|Agent\(|subagent" "$t" || { echo "FAIL: no delegation"; fail=1; }
grep -qiE "check_pptx|check_docx|check_pdf|check_citations" "$t" || { echo "FAIL: no checker run"; fail=1; }
[ $fail -eq 0 ] && echo "PASS operating-discipline" || echo "FAIL operating-discipline"; exit $fail
