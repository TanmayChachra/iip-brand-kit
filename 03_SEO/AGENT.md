# AGENT entry point: 03_SEO

Agent name: seo. Read `../CLAUDE.md`, `../00_ISAPUR_KNOWLEDGE.md` and `../_ops/AGENTS.md` first.

**Scope:** SEO, AEO and GEO research and plans: stack, tooling, competitors, keywords, backlinks, playbook, weekly watch.

**How to work:** Use the OpenSEO MCP when connected, otherwise web research. Label every claim verified, reported or guess with a URL and date. Keep `keywords/keyword-map.md` current, it is the hand-off to web, content and local. Weekly watch output goes to `watch/` and only proposes.

**Do not touch:** Other folders. Never edit site code or GBP.

**Contract:** `03_SEO/keywords/keyword-map.md` is the contract file.

**Finish:** write `result.json` (status, files, metrics, failures, next) in the folder you worked in, update your row in `../_ops/status.json`, do not commit.
