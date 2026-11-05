#!/usr/bin/env bash
set -u
root="$(cd "$(dirname "$0")/../.." && pwd)"; run="${1:-.}"; f="$run/decision-summary.pdf"; fail=0
[ -f "$f" ] || { echo "FAIL: $f missing"; exit 1; }
python3 "$root/skills/pdf/scripts/check_pdf.py" "$f" --min-pages 1 --max-pages 1 --require-text "Summary,Scope,Risks,Decision needed" || fail=1
python3 -c "import sys; from pypdf import PdfReader; m=PdfReader(sys.argv[1]).metadata; assert m and m.title, 'no title metadata'; print('title:', m.title)" "$f" || fail=1
[ $fail -eq 0 ] && echo "PASS pdf" || echo "FAIL pdf"; exit $fail
