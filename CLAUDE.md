# ISAPUR Industrial Park (IIP): project instructions for every chat in this repo

Read this first, then `00_ISAPUR_KNOWLEDGE.md` (single source of truth, never delete or move, append to its change log), then `_ops/AGENTS.md` (who owns which folder) and `_ops/TECH-STACK.md` (accounts, hosting, MCPs and skills for this project: maintain it end to end, never delete the MCPs listed there). Open work is in `TODOS.md`, history in `CHANGELOG.md`.

## What this project is
Marketing, brand and visibility for Isapur Industrial Park (the name is exactly "Isapur Industrial Park", short form IIP; the developer is NOT revealed anywhere). Audience: local factory owners on the Hapur-Modinagar Road. Live boards: https://tanmaychachra.github.io/iip-brand-kit/ (brand kit), `/board/` (phase 2), `/experiments/poster-lab/`.

## Hard rules
- The logo is never changed. English only. Phone and WhatsApp: 98377 64222 ONLY (owner decision 2026-11-12). 92195 49800 is used ONLY for rent and lease contact (call number on the rent section, the rent page and rent FAQ, owner decision 2026-11-14); WhatsApp stays 98377 64222 everywhere; it stays off every other page, schema, print and listing. 98370 57800 is retired everywhere. Keep every use behind one swap point: `01_Brand/Brand-Kit/tokens/content.json` and `02_Website/site-v2/src/lib/phones.mjs`. Primary domain is isapurindustrialpark.com (the .in redirects to it). Display font is Erode, text Inter, Montserrat only inside the logo.
- Taglines are ADAPTIVE, never fixed: "A Modern Industrial Address." and "The Groundwork for Growth." Use one per creative, never both.
- No claim on a board, post or web page unless its proof is on file (knowledge file section 3). Distances: say straight-line or driving. Partner brands (Amul, Inox Air, Patanjali and similar) are named only after the owner confirms and the brand's presence is verified. Never put schema markup for a claim that has no proof.
- Online images are WEBP. No em dashes anywhere. No Co-Authored-By lines or Claude mentions in git. Never type or store secrets (API keys live in env vars the owner sets).
- The owner has NO photos yet. Do not use AI warehouse images as if they were the park. This rule lasts only until the photographic direction for the brand is finalised (open task `photodirection` in TODOS.md and on the board); the owner will then allow AI-assisted imagery inside that direction. Until then only real photos, licensed stand-ins, drawings and stylised 3D.
- **Release rule (2026-11-14):** all work, lead and helpers, happens on git branch `staging`. `main` always equals production. Nobody runs wrangler against Pages project `iip-site` or edits production DNS, except `02_Website/release/promote.ps1` (or `rollback.ps1`) after the owner types GO LIVE. Helpers deploy only with `02_Website/release/deploy-staging.ps1`. A production hotfix goes staging, then promote. Process: `02_Website/release/RELEASE-PROCESS.md`.
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
5. `_ops/TECH-STACK.md` for any account, MCP, skill, host or scheduled task change, then `_ops/status.json` (feeds the board), then rebuild the board and the kit as needed (commands in `README.md`).
Coverage by type: reference (kit page, competitor tables), how-to (README, playbook), explanation (knowledge file, research findings), tutorial (brief). Flag gaps in TODOS.md.

## Research truth labels
Every research claim carries a source URL and a label: verified (read at the source, give date), reported (third party), guess. Scheduled research writes dated files into `03_SEO/watch/` and never changes plans on its own.

## Tools
Use `/orchestrator` for multi-part work (forks for independent jobs, caps on helper reports). Heavy design tools (ArtCraft family) only for refined work or on request. SEO data comes from the self-hosted OpenSEO MCP once the owner connects it; until then research is web based and labelled.
