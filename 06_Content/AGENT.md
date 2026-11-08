# AGENT entry point: 06_Content

Agent name: content. Read `../CLAUDE.md`, `../00_ISAPUR_KNOWLEDGE.md` and `../_ops/AGENTS.md` first.

**Scope:** Content pillars, blog and social calendar, copy drafts (starts after the site skeleton and keyword map).

**How to work:** Pillars are decided with the owner (ChatGPT help). Taglines adaptive, one per creative. Claims need proof. Hashtags come from the Apify research (owner supplies the key as an env var).

**Do not touch:** Other folders.

**Contract:** Reads `03_SEO/keywords/keyword-map.md` and brand tokens.

**Finish:** write `result.json` (status, files, metrics, failures, next) in the folder you worked in, update your row in `../_ops/status.json`, do not commit.
