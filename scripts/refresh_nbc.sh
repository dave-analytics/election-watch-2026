#!/usr/bin/env bash
# Refresh races that have NBC News pages. Run from the repo root.
# Downloads pages into a temp dir (plain requests, no browser spoofing) and parses only their embedded JSON.
set -u
T=$(mktemp -d)
base=https://www.nbcnews.com/politics/2026-elections
get(){ curl -sS -m 30 -o "$T/$1.html" "$base/$2" && echo "$1"; }
get gov tennessee-governor-results >/dev/null && get sen tennessee-senate-results >/dev/null && \
  python3 -I scripts/tn_counties.py "$T/gov.html" "$T/sen.html" counties-tn.json data.json
get txgov texas-governor-results >/dev/null && python3 -I scripts/nbc_race.py G-TX "$T/txgov.html" data.json
get tngov tennessee-governor-results >/dev/null && python3 -I scripts/nbc_race.py G-TN "$T/tngov.html" data.json
# Every uncalled Senate and House race, from its NBC page (Senate specials live under 2026-special-elections)
python3 -I -c "
import json
N={'AL':'alabama','AK':'alaska','AZ':'arizona','AR':'arkansas','CA':'california','CO':'colorado','CT':'connecticut','DE':'delaware','FL':'florida','GA':'georgia','HI':'hawaii','ID':'idaho','IL':'illinois','IN':'indiana','IA':'iowa','KS':'kansas','KY':'kentucky','LA':'louisiana','ME':'maine','MD':'maryland','MA':'massachusetts','MI':'michigan','MN':'minnesota','MS':'mississippi','MO':'missouri','MT':'montana','NE':'nebraska','NV':'nevada','NH':'new-hampshire','NJ':'new-jersey','NM':'new-mexico','NY':'new-york','NC':'north-carolina','ND':'north-dakota','OH':'ohio','OK':'oklahoma','OR':'oregon','PA':'pennsylvania','RI':'rhode-island','SC':'south-carolina','SD':'south-dakota','TN':'tennessee','TX':'texas','UT':'utah','VT':'vermont','VA':'virginia','WA':'washington','WV':'west-virginia','WI':'wisconsin','WY':'wyoming'}
for r in json.load(open('data.json'))['races']:
    if r['state'] not in N or (r.get('winner') and all(c.get('pct') is not None for c in r.get('cands',[]))): continue
    if r['chamber']=='senate':
        print(r['id'], ('2026-special-elections/' if r.get('special') else '2026-elections/')+N[r['state']]+'-senate-results')
    elif r['chamber']=='house':
        print(r['id'], '2026-elections/'+N[r['state']]+'-us-house-district-'+(str(r['district']) if r['district'] else 'at-large')+'-results')
" | while read id path; do
  curl -sS -m 30 -o "$T/$id.html" "https://www.nbcnews.com/politics/$path" && grep -q __NEXT_DATA__ "$T/$id.html" && python3 -I scripts/nbc_race.py "$id" "$T/$id.html" data.json || echo "$id: no NBC page"
done
rm -rf "$T"
python3 -I -m json.tool data.json >/dev/null && echo "data.json valid"
