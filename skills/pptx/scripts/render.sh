#!/usr/bin/env bash
# Render every slide/page of an Office file or PDF to PNG for visual QA.
# Usage: bash render.sh deck.pptx [outdir] [dpi]
# Works for .pptx, .docx, .pdf. Prints the PNG paths it produced.
set -euo pipefail
in="$1"; out="${2:-$(dirname "$in")/render}"; dpi="${3:-80}"
mkdir -p "$out"; rm -f "$out"/page-*.png
case "$in" in
  *.pdf) pdf="$in" ;;
  *)
    profile="$(mktemp -d)"
    SAL_USE_VCLPLUGIN=svp soffice -env:UserInstallation="file://$profile" --headless \
      --convert-to pdf --outdir "$out" "$in" >/dev/null 2>&1 || { echo "soffice failed" >&2; exit 1; }
    rm -rf "$profile"
    pdf="$out/$(basename "${in%.*}").pdf" ;;
esac
pdftoppm -png -r "$dpi" "$pdf" "$out/page"
ls -1 "$out"/page-*.png
