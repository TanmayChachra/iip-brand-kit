# AGENT entry point: 01_Brand

Agent name: brand. Read `../CLAUDE.md`, `../00_ISAPUR_KNOWLEDGE.md` and `../_ops/AGENTS.md` first.

**Scope:** Brand kit, poster, logo files, references, poster lab. The kit is LOCKED (final). Change it only on an explicit owner request.

**How to work:** Rebuild with `python 01_Brand/Brand-Kit/_build/build_all.py` then `publish.py`. Logo never changes. New brand textures from the poster lab can be promoted into `Brand-Kit/` only after the owner picks them.

**Do not touch:** Everything outside `01_Brand/`.

**Contract:** `01_Brand/Brand-Kit/tokens/` (colours, content) is read by the web agent.

**Finish:** write `result.json` (status, files, metrics, failures, next) in the folder you worked in, update your row in `../_ops/status.json`, do not commit.
