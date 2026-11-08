# AGENT entry point: 04_Analytics

Agent name: analytics. Read `../CLAUDE.md`, `../00_ISAPUR_KNOWLEDGE.md` and `../_ops/AGENTS.md` first.

**Scope:** GTM and GA4 plan, event spec, dashboards and the A/B test log.

**How to work:** Keep `event-spec.md` versioned (version line at top). Conversions: click_call, click_whatsapp, generate_lead, click_directions. Never store IDs that are secrets (GTM and GA4 IDs are public, API keys are not). Monthly review rules are in `gtm-plan.md`.

**Do not touch:** Other folders. The web agent adds data attributes, you do not edit site code.

**Contract:** `04_Analytics/event-spec.md` is the contract file.

**Finish:** write `result.json` (status, files, metrics, failures, next) in the folder you worked in, update your row in `../_ops/status.json`, do not commit.
