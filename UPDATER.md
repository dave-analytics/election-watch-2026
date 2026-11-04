# Chamber Watch — results updater

Instructions for the scheduled agent that refreshes `data.json` every 15 minutes.
The site (`index.html`) re-reads `data.json` every 60 seconds; nothing else needs changing.

## Each run

1. `git pull` the default branch.
2. Search for current 2026 midterm results (WebSearch, `standard` mode; `extended` only if results are thin):
   - Senate: which of the 35 races in `data.json` have been **called**, by whom, and current vote % / % reporting for uncalled close races.
   - House: total seats called for each party (AP / NBC / Decision Desk HQ counts), and calls for the House districts listed in `data.json`.
3. Edit `data.json` only where a source shows a change:
   - Race called: set `"winner": "D"|"R"|"I"`, `"status": "Called"`, `"flip": true` if winner's party ≠ `incParty`. Fill `pct` on candidates if known.
   - Uncalled with returns: `"status": "Counting"`, `"reporting": <number>`, candidate `pct`.
   - House totals: `meta.house.wonD`, `meta.house.wonR`, `meta.house.netD` (net D seats vs. before).
   - Always set `meta.updatedAt` to the current UTC ISO time, and keep `meta.note` naming the sources used this run.
4. Rules:
   - **Only record a call that at least one major desk (AP, NBC, CNN, Fox, ABC, CBS, DDHQ) has made.** Never infer a winner from partial returns.
   - If sources conflict, leave the race uncalled and note it in `meta.note`.
   - Never remove races or rewrite fields you have no new information for.
   - Validate: `python3 -m json.tool data.json` must pass before committing.
5. If anything changed: commit `Update results <UTC time>` and push. If nothing changed, update nothing and do not commit.

## When to stop

Once every Senate race is called and the House totals reach 435 (or the user says stop), report that and disable the scheduled task.

## Watched races

Races with `"featured": true` (currently CA-27, Whitesides vs. Gibbs) are the user's priority: check each one every run — vote share, % reporting and any call — using NBC's district page or the California Secretary of State results (https://electionresults.sos.ca.gov).
