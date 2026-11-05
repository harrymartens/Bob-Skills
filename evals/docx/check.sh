#!/usr/bin/env bash
set -u
root="$(cd "$(dirname "$0")/../.." && pwd)"; run="${1:-.}"; f="$run/recommendation.docx"; fail=0
[ -f "$f" ] || { echo "FAIL: $f missing"; exit 1; }
python3 "$root/skills/docx/scripts/check_docx.py" "$f" --min-words 400 --max-words 1200 --require-headings "Summary,Risks,Next steps" || fail=1
python3 -c "import sys; from docx import Document; d=Document(sys.argv[1]); assert len(d.tables)>=1, 'no table'; print('tables:',len(d.tables))" "$f" || fail=1
if command -v soffice >/dev/null; then bash "$root/skills/docx/scripts/render.sh" "$f" "$run/render" 50 >/dev/null && pages=$(ls "$run"/render/page-*.png | wc -l) && echo "pages: $pages" && { [ "$pages" -ge 1 ] && [ "$pages" -le 3 ] || fail=1; }; fi
[ $fail -eq 0 ] && echo "PASS docx" || echo "FAIL docx"; exit $fail
