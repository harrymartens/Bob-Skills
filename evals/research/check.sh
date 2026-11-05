#!/usr/bin/env bash
set -u
root="$(cd "$(dirname "$0")/../.." && pwd)"; run="${1:-.}"; f="$run/research.md"; fail=0
[ -f "$f" ] || { echo "FAIL: $f missing"; exit 1; }
for h in "## Answer" "## Counter-evidence" "## Confidence" "## Sources"; do grep -q "^$h" "$f" || { echo "FAIL: missing $h"; fail=1; }; done
grep -qiE "is wrong if|wrong if" "$f" || { echo "FAIL: no red-team line"; fail=1; }
n=$(grep -cE '^\[S[0-9]+\] https?://' "$f"); echo "sources: $n"; [ "$n" -ge 4 ] || fail=1
python3 "$root/skills/research/scripts/check_citations.py" "$f" --cache "$run/sources" || fail=1
[ $fail -eq 0 ] && echo "PASS research" || echo "FAIL research"; exit $fail
