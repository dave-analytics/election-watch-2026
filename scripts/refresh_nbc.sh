#!/usr/bin/env bash
# Refresh every race (all House, Senate and governor) and Tennessee counties from NBC News pages.
# Run from the repo root. Plain requests only; pages are parsed for their embedded JSON and deleted.
set -u
T=$(mktemp -d)
base=https://www.nbcnews.com/politics/2026-elections
curl -sS -m 30 -o "$T/gov.html" "$base/tennessee-governor-results" && curl -sS -m 30 -o "$T/sen.html" "$base/tennessee-senate-results" && \
  python3 -I scripts/tn_counties.py "$T/gov.html" "$T/sen.html" counties-tn.json data.json
./scripts/fetch_all.sh "$T/sums" && python3 -I scripts/merge_summaries.py "$T/sums" data.json
python3 -I -c "
import json; d=json.load(open('data.json')); h=[r for r in d['races'] if r['chamber']=='house']
d['meta']['house'].update(wonD=sum(r.get('winner')=='D' for r in h), wonR=sum(r.get('winner')=='R' for r in h))
json.dump(d, open('data.json','w'), indent=1, ensure_ascii=False)"
rm -rf "$T"
python3 -I -m json.tool data.json >/dev/null && echo "data.json valid"
