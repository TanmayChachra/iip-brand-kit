# ISAPUR Industrial Park (IIP): project instructions for every chat in this repo

Read this first, then `00_ISAPUR_KNOWLEDGE.md` (single source of truth, never delete or move, append to its change log). Open work is in `TODOS.md`, history in `CHANGELOG.md`.

## What this project is
Brand system for Isapur Industrial Park (the name is exactly "Isapur Industrial Park", short form IIP; the developer is NOT revealed anywhere). Audience: local factory owners on the Hapur-Modinagar Road. Live site: https://tanmaychachra.github.io/iip-brand-kit/ (built from `docs/`, source `Brand-Kit/site/`).

## Hard rules
- The logo is never changed. English only. Phones 9837057800 and 9219549800.
- Taglines are ADAPTIVE, never fixed: "A Modern Industrial Address." and "The Groundwork for Growth." Use one per creative, never both.
- No claim on a board or post unless its proof is on file (knowledge file section 3). Distances: say straight-line or driving.
- Online images are WEBP. No em dashes anywhere. No Co-Authored-By lines or Claude mentions in git. Never type or store secrets (API keys live in env vars the owner sets).
- The owner has NO photos yet. Do not use AI warehouse images as if they were the park.

## Phases
1. Brand kit, brand book, brief (done, being refined page by page).
2. Social media and online presence (next). Content pillars decided later with ChatGPT help. Hashtags to be researched with an Apify actor (owner supplies the key, open todo).
3. **AI-driven assets** (later, after refinement). Everything AI generated goes in `AI-Assets/`. Until phase 3, the kit must keep a distinctive, human-crafted character that generic AI tools cannot easily copy: do not steer the kit toward looks that AI design tools replicate easily.

## How documentation stays synced (adapted from gstack document-release)
After every change that ships, update the affected docs in the same commit:
1. `00_ISAPUR_KNOWLEDGE.md`: facts, decisions, one change log line (append only).
2. `TODOS.md`: tick done items, add new ones, remove stale ones.
3. `CHANGELOG.md`: one dated entry written for the owner (what they can now do), newest first.
4. `README.md` folder map and this file if structure, rules or phases changed.
5. Rebuild with `python Brand-Kit/_build/publish.py` so `docs/` matches the kit.
Check coverage by type: reference (kit page), how-to (README rebuild steps, print guide), explanation (knowledge file, brand story), tutorial (brief). Flag gaps in TODOS.md.

## Tools
Use `/orchestrator` for multi-part work (forks for independent jobs). Heavy design tools (ArtCraft family: VectorCraft, ArtCraft) only for refined detailed work or on request, one job at a time. SVG assets open with VectorCraft, Inkscape, Figma, Illustrator or any browser.
