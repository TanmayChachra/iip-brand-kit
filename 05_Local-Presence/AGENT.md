# AGENT entry point: 05_Local-Presence

Agent name: local. Read `../CLAUDE.md`, `../00_ISAPUR_KNOWLEDGE.md` and `../_ops/AGENTS.md` first.

**Scope:** Google Business Profile, listings, citations, reviews.

**How to work:** One canonical NAP in `citations/nap.md`, copied exactly everywhere. Record every listing in `citations/citations-targets.csv` (status column). Never create accounts or post for the owner without a yes in chat. GBP edits are done by the owner or with explicit permission.

**Do not touch:** Other folders.

**Contract:** `05_Local-Presence/citations/nap.md` is the contract file.

**Finish:** write `result.json` (status, files, metrics, failures, next) in the folder you worked in, update your row in `../_ops/status.json`, do not commit.
