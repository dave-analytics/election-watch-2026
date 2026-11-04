#!/usr/bin/env bash
# Fetch every race's NBC page (plain requests), keep only a compact summary per race in $1.
set -u
OUT=${1:?summary dir}; mkdir -p "$OUT"
python3 -I scripts/manifest.py | xargs -P 6 -L 1 bash -c '
  id=$0; path=$4; f=$(mktemp)
  if curl -sS -m 40 --retry 2 -o "$f" -w "%{http_code}" "https://www.nbcnews.com/politics/$path" | grep -q 200; then
    python3 -I scripts/nbc_summary.py "$f" > "'"$OUT"'/$id.json" 2>/dev/null || { rm -f "'"$OUT"'/$id.json"; echo "$id parse-failed"; }
  else echo "$id fetch-failed $path"; fi
  rm -f "$f"'
echo "summaries: $(ls "$OUT" | wc -l)"
