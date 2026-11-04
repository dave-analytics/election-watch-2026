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

## Governor races

Races with `"chamber": "governor"` (ids `G-<ST>`, currently Tennessee and Texas) are updated and called exactly like Senate races, but never count toward the Senate or House totals. Do not add other governor races unless the user asks.

## Candidates and percentages

For every uncalled race, record `pct` (current vote share) for the main Democrat and main Republican, plus `reporting` (% of expected vote in). The site shows only the main D and R candidates, so don't add minor-party or write-in candidates. Keep an independent only when one major party has no nominee (e.g. Nebraska's Dan Osborn).

## Rolling close-race list

Keep the site stocked with live close races:

- A **close race** is one rated `tossup`, `leanD` or `leanR`, or any race (Senate or House) where a desk's current returns show a margin under 5 points with counting still under way.
- **Called races are final.** Any race that has a `winner` (status `"Called"`) is closed: never edit, re-check or remove it in later runs. Only races without a `winner` get updated.
- **When a tracked race is called:** record the call once (`winner`, `status: "Called"`, `flip`) **together with the main D and R `pct` at the time of the call** — a called card must never be left without percentages.
- **When any race not on the list is called** (Senate or House, close or not): add it once with its result (candidates, `incParty`, `rating` if known, `winner`, `status: "Called"`, `"addedReason": "called"`). It is then final like any other called race.
- **Then, for each close race called this run, add one replacement:** the uncalled race with the smallest current margin (from NBC, CNN, AP or DDHQ live results) that is not already in `data.json`. Give it `status: "Counting"`, candidates with current `pct`, `reporting`, and `"addedReason": "next closest uncalled race"`. Never add a race whose candidates or margin you could not confirm from a source; skip to the next one instead.
- Never remove races, and never add duplicates (check the `id` first: `S-<ST>` for Senate, `H-<ST>-<NN>` for House).
- Note each addition in `meta.note`.

## When to stop

Once every Senate race is called and the House totals reach 435 (or the user says stop), report that and disable the scheduled task.

## Watched races

Races with `"featured": true` (currently CA-27, Whitesides vs. Gibbs) are the user's priority: check each one every run — vote share, % reporting and any call — using NBC's district page or the California Secretary of State results (https://electionresults.sos.ca.gov).
