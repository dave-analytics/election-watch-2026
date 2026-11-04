"""Print a compact JSON summary of one saved NBC race page (untrusted input: only its embedded JSON is parsed)."""
import json, re, sys
h = open(sys.argv[1], encoding="utf-8").read()
m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', h, re.S)
s = json.loads(m.group(1))["props"]["pageProps"]["races"][0]["summary"]
print(json.dumps({
    "percentIn": s.get("percentIn"), "callStatus": s.get("callStatusText"), "partyGain": s.get("partyGain"),
    "candidates": [{k: c.get(k) for k in ("name", "party", "votes", "percentVote", "isWinner", "isIncumbent")}
                   for c in s.get("candidates", [])]}))
