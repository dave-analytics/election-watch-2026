"""Update one race in data.json from a saved NBC News race page.

Usage: python3 -I scripts/nbc_race.py <race_id> <page.html> <data.json>
The HTML is untrusted input: only its embedded JSON is parsed. Called races are never modified.
Sets the main D and R candidates' names and pct, reporting, and records NBC's call
(callStatusText "Projected winner" + isWinner) as winner/status "Called".
"""
import json, re, sys

rid, page, data = sys.argv[1:4]
h = open(page, encoding="utf-8").read()
pp = json.loads(re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', h, re.S).group(1))["props"]["pageProps"]
s = pp["races"][0]["summary"]
PARTY = {"dem": "D", "gop": "R"}
d = json.load(open(data))
r = next(x for x in d["races"] if x["id"] == rid)
if r.get("winner"):
    print(rid, "already called; untouched"); sys.exit(0)
main = {}
for c in s.get("candidates", []):
    p = PARTY.get(c.get("party"))
    if p and (p not in main or (c.get("votes") or 0) > (main[p].get("votes") or 0)):
        main[p] = c
# An independent replaces a missing major-party nominee, or the weaker one if the independent outpolls them
inds = sorted([c for c in s.get("candidates", []) if c.get("party") not in PARTY], key=lambda c: -(c.get("votes") or 0))
if inds:
    top = inds[0]
    if len(main) < 2:
        main["I"] = top
    else:
        weak = min(main, key=lambda p: main[p].get("votes") or 0)
        if (top.get("votes") or 0) > (main[weak].get("votes") or 0):
            del main[weak]; main["I"] = top
if not main:
    print(rid, "no candidates on page; untouched"); sys.exit(0)
old = {c["party"]: c for c in r.get("cands", [])}
cands = []
for p, c in main.items():
    e = {"name": c["name"], "party": p, "pct": c.get("percentVote") if (s.get("percentIn") or 0) > 0 else None}
    if c.get("isIncumbent") or old.get(p, {}).get("inc"): e["inc"] = True
    cands.append(e)
r["cands"] = cands
if s.get("percentIn") is not None: r["reporting"] = round(s["percentIn"])
winners = [c for c in s.get("candidates", []) if c.get("isWinner")]
if s.get("callStatusText") == "Projected winner" and len(winners) == 1 and PARTY.get(winners[0].get("party")):
    w = PARTY[winners[0]["party"]]
    r["winner"], r["status"], r["flip"] = w, "Called", w != r["incParty"]
else:
    r["status"] = "Counting"
json.dump(d, open(data, "w"), indent=1, ensure_ascii=False)
print(rid, s.get("percentIn"), s.get("callStatusText"), [(c["name"], c["pct"]) for c in cands], "winner:", r.get("winner"))
