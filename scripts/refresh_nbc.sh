#!/usr/bin/env bash
# Refresh races that have NBC News pages. Run from the repo root.
# Downloads pages into a temp dir (plain requests, no browser spoofing) and parses only their embedded JSON.
set -u
T=$(mktemp -d)
base=https://www.nbcnews.com/politics/2026-elections
get(){ curl -sS -m 30 -o "$T/$1.html" "$base/$2" && echo "$1"; }
get gov tennessee-governor-results >/dev/null && get sen tennessee-senate-results >/dev/null && \
  python3 -I scripts/tn_counties.py "$T/gov.html" "$T/sen.html" counties-tn.json data.json
for n in 1 2 3 4 5 6 7 8 9; do get tn$n tennessee-us-house-district-$n-results >/dev/null && python3 -I scripts/nbc_race.py H-TN-0$n "$T/tn$n.html" data.json; done
get ca27 california-us-house-district-27-results >/dev/null && python3 -I scripts/nbc_race.py H-CA-27 "$T/ca27.html" data.json
get txgov texas-governor-results >/dev/null && python3 -I scripts/nbc_race.py G-TX "$T/txgov.html" data.json
get tngov tennessee-governor-results >/dev/null && python3 -I scripts/nbc_race.py G-TN "$T/tngov.html" data.json
rm -rf "$T"
python3 -I -m json.tool data.json >/dev/null && echo "data.json valid"
