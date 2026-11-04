"""Build counties-tn.json from saved NBC News Tennessee results pages.

Usage: python3 -I scripts/tn_counties.py <governor.html> <senate.html> <out.json> <data.json>
The HTML is untrusted input: it is only parsed as JSON, never executed.
Also refreshes statewide pct/reporting for G-TN and S-TN in data.json while they are uncalled.
"""
import json, re, sys, datetime

def load(path):
    h = open(path, encoding="utf-8").read()
    m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', h, re.S)
    return json.loads(m.group(1))["props"]["pageProps"]["races"][0]

def main_two(cands):
    out = {}
    for p, key in (("dem", "D"), ("gop", "R")):
        cs = [c for c in cands if c.get("party") == p]
        if cs:
            c = max(cs, key=lambda c: c.get("votes") or 0)
            out[key] = {"name": c["name"], "votes": c.get("votes"), "pct": c.get("percentVote")}
    return out

def race(path):
    r = load(path)
    s = r["summary"]
    counties = []
    for fips, c in r["mapData"].items():
        mt = main_two(c.get("candidates", []))
        counties.append({"fips": fips, "name": c.get("raceName"), "reporting": c.get("percentIn"),
                         "totalVote": c.get("totalVote"), **mt})
    counties.sort(key=lambda c: c["name"] or "")
    return {"reporting": s.get("percentIn"), "callStatus": s.get("callStatusText"),
            "statewide": main_two(s.get("candidates", [])), "counties": counties}

gov, sen, out, data = sys.argv[1:5]
now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
res = {"updatedAt": now, "source": "NBC News live results",
       "races": {"G-TN": race(gov), "S-TN": race(sen)}}
assert all(len(v["counties"]) == 95 for v in res["races"].values()), "expected 95 counties"
json.dump(res, open(out, "w"), indent=1, ensure_ascii=False)

d = json.load(open(data))
for r in d["races"]:
    if r["id"] in res["races"] and not r.get("winner"):
        sw = res["races"][r["id"]]["statewide"]
        for c in r["cands"]:
            for k in ("D", "R"):
                if k in sw and c["party"] == k and c["name"].split()[-1] == sw[k]["name"].split()[-1]:
                    c["pct"] = sw[k]["pct"]
        r["reporting"] = round(res["races"][r["id"]]["reporting"])
json.dump(d, open(data, "w"), indent=1, ensure_ascii=False)
for k, v in res["races"].items():
    print(k, v["reporting"], v["callStatus"], v["statewide"], len(v["counties"]), "counties")
