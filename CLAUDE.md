# ISAPUR Industrial Park (IIP): project instructions for every chat in this repo

Read this first, then `00_ISAPUR_KNOWLEDGE.md` (single source of truth, never delete or move, append to its change log), then `_ops/AGENTS.md` (who owns which folder). Open work is in `TODOS.md`, history in `CHANGELOG.md`.

## What this project is
Marketing, brand and visibility for Isapur Industrial Park (the name is exactly "Isapur Industrial Park", short form IIP; the developer is NOT revealed anywhere). Audience: local factory owners on the Hapur-Modinagar Road. Live boards: https://tanmaychachra.github.io/iip-brand-kit/ (brand kit), `/board/` (phase 2), `/experiments/poster-lab/`.

## Hard rules
- The logo is never changed. English only. Phones 9837057800 and 9219549800.
- Taglines are ADAPTIVE, never fixed: "A Modern Industrial Address." and "The Groundwork for Growth." Use one per creative, never both.
- No claim on a board, post or web page unless its proof is on file (knowledge file section 3). Distances: say straight-line or driving. Partner brands (Amul, Inox Air, Patanjali and similar) are named only after the owner confirms and the brand's presence is verified. Never put schema markup for a claim that has no proof.
- Online images are WEBP. No em dashes anywhere. No Co-Authored-By lines or Claude mentions in git. Never type or store secrets (API keys live in env vars the owner sets).
- The owner has NO photos yet. Do not use AI warehouse images as if they were the park.
- Never edit another agent's folder (see `_ops/AGENTS.md`). Cross-agent hand-offs happen only through the contract files listed there.

## Phases
1. Brand kit, brand book, brief. DONE and final (the locked kit is `01_Brand/Brand-Kit/`, poster is final).
2. **Visibility (now):** website (Astro, performance and SEO first, design second), SEO, local presence (GBP, listings), AEO and GEO, analytics (GTM, GA4), then social and content. Lowest hanging fruit first, broader categories later.
3. AI-driven assets (later). Everything AI generated goes in `01_Brand/AI-Assets/`. The kit keeps a distinctive, human-crafted character that generic AI tools cannot easily copy.

## How documentation stays synced (adapted from gstack document-release)
After every change that ships, update the affected docs in the same commit:
1. `00_ISAPUR_KNOWLEDGE.md`: facts, decisions, one change log line (append only).
2. `TODOS.md`: tick done items, add new ones, remove stale ones.
3. `CHANGELOG.md`: one dated entry written for the owner (what they can now do), newest first.
4. `README.md` folder map and this file if structure, rules or phases changed.
5. `_ops/status.json` (feeds the board), then rebuild the board and the kit as needed (commands in `README.md`).
Coverage by type: reference (kit page, competitor tables), how-to (README, playbook), explanation (knowledge file, research findings), tutorial (brief). Flag gaps in TODOS.md.

## Research truth labels
Every research claim carries a source URL and a label: verified (read at the source, give date), reported (third party), guess. Scheduled research writes dated files into `03_SEO/watch/` and never changes plans on its own.

## Tools
Use `/orchestrator` for multi-part work (forks for independent jobs, caps on helper reports). Heavy design tools (ArtCraft family) only for refined work or on request. SEO data comes from the self-hosted OpenSEO MCP once the owner connects it; until then research is web based and labelled.
