"""Merge NBC race summaries (from fetch_all.sh) into data.json.

Usage: python3 -I scripts/merge_summaries.py <summary_dir> data.json
Rules: called races are final (only missing vote shares are filled once); the main D and R are shown,
an independent replaces a missing or weaker major-party candidate; calls come only from NBC projections.
"""
import json, glob, os, sys, subprocess

sdir, data = sys.argv[1:3]
d = json.load(open(data))
byid = {r["id"]: r for r in d["races"]}
P = {"dem": "D", "gop": "R"}
pty = lambda c: P.get(c.get("party"), "I")
man = {l.split()[0]: l.split() for l in subprocess.run(["python3", "-I", "scripts/manifest.py"], capture_output=True, text=True, check=True).stdout.splitlines()}

def pick(cands):
    by = lambda c: -(c.get("votes") or 0)
    main = {}
    for c in sorted(cands, key=by):
        p = pty(c)
        if p in ("D", "R") and p not in main: main[p] = c
    rest = [c for c in sorted(cands, key=by) if c not in main.values()]
    out = list(main.values())
    if rest:
        top = rest[0]
        if len(out) < 2: out.append(top)
        elif (top.get("votes") or 0) > min(c.get("votes") or 0 for c in out):
            out.remove(min(out, key=lambda c: c.get("votes") or 0)); out.append(top)
    return out

stats = {"created": 0, "updated": 0, "called": 0, "filled": 0, "frozen": 0}
for f in sorted(glob.glob(os.path.join(sdir, "*.json"))):
    rid = os.path.basename(f)[:-5]
    s = json.load(open(f))
    _, chamber, st, dist, _ = man[rid]
    counted = (s.get("percentIn") or 0) > 0
    chosen = pick(s.get("candidates", []))
    incs = [c for c in s["candidates"] if c.get("isIncumbent")]
    winners = [c for c in s["candidates"] if c.get("isWinner")]
    called = s.get("callStatus") == "Projected winner" and len(winners) == 1
    r = byid.get(rid)
    if r is None:
        inc_party = pty(incs[0]) if incs else ("R" if s.get("partyGain") == "dem" else (pty(winners[0]) if called and not s.get("partyGain") else None))
        r = {"id": rid, "chamber": chamber, "state": st, "incParty": inc_party,
             "incumbent": incs[0]["name"] if incs else "Open seat", "open": not incs, "cands": [], "status": "Counting", "addedReason": "all races"}
        if chamber == "house": r["district"] = int(dist)
        d["races"].append(r); byid[rid] = r; stats["created"] += 1
    if r.get("winner"):
        if all(c.get("pct") is not None for c in r.get("cands", [])) or not counted:
            stats["frozen"] += 1; continue
        fill_only = True
    else:
        fill_only = False
    old_inc = {c["name"] for c in r.get("cands", []) if c.get("inc")}
    r["cands"] = [dict({"name": c["name"], "party": pty(c), "pct": c.get("percentVote") if counted else None},
                       **({"inc": True} if c.get("isIncumbent") or c["name"] in old_inc else {})) for c in chosen]
    if s.get("percentIn") is not None: r["reporting"] = round(s["percentIn"])
    if fill_only:
        stats["filled"] += 1; continue
    stats["updated"] += 1
    if called:
        w = pty(winners[0])
        r["winner"], r["status"] = w, "Called"
        r["flip"] = bool(s.get("partyGain")) or (r.get("incParty") not in (None, w))
        stats["called"] += 1
    else:
        r["status"] = "Too close to call" if s.get("callStatus") == "Too close to call" else "Counting"
json.dump(d, open(data, "w"), indent=1, ensure_ascii=False)
print(stats, "total races:", len(d["races"]))
