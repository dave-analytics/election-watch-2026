# election-watch-2026

Chamber Watch: live Senate and House seat counts for the 2026 midterms, with races searchable by state.

- `index.html` — the site (static, no build step). Re-reads `data.json` every 60 seconds.
- `data.json` — seat baselines, ratings, candidates and race calls.
- `UPDATER.md` — instructions for the scheduled agent that refreshes `data.json` every 15 minutes.

Host it anywhere that serves static files (GitHub Pages from `main` / root, or Vercel with no build command).
