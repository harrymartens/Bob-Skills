#!/usr/bin/env bash
# Usage: bash evals/pptx/check.sh <run-dir>   (run-dir contains mcp-pitch.pptx)
set -u
root="$(cd "$(dirname "$0")/../.." && pwd)"; run="${1:-.}"; f="$run/mcp-pitch.pptx"; fail=0
[ -f "$f" ] || { echo "FAIL: $f missing"; exit 1; }
python3 "$root/skills/pptx/scripts/check_pptx.py" "$f" --min-slides 8 --max-slides 8 || fail=1
layouts=$(python3 - "$f" <<'PY'
import sys; from pptx import Presentation
kinds=set()
for s in Presentation(sys.argv[1]).slides:
    types=sorted({str(sh.shape_type) for sh in s.shapes}); has_tbl=any(sh.has_table for sh in s.shapes); has_chart=any(sh.has_chart for sh in s.shapes)
    kinds.add(("table" if has_tbl else "chart" if has_chart else "shapes%d" % min(len(s.shapes)//3,3)))
print(len(kinds))
PY
)
echo "distinct layouts: $layouts"; [ "$layouts" -ge 3 ] || { echo "FAIL: fewer than 3 layout types"; fail=1; }
for u in $(markitdown "$f" 2>/dev/null | grep -oE 'https?://[^ )>"]+' | sort -u); do
  code=$(curl -sS -o /dev/null -w '%{http_code}' -L --max-time 30 "$u"); echo "$code $u"; [ "$code" -lt 400 ] || fail=1; done
[ $fail -eq 0 ] && echo "PASS pptx" || echo "FAIL pptx"; exit $fail
