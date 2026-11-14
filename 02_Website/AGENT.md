# AGENT entry point: 02_Website

Agent name: web. Read `../CLAUDE.md`, `../00_ISAPUR_KNOWLEDGE.md` and `../_ops/AGENTS.md` first.

**Scope:** The IIP website: information architecture, page specs and the Astro project (`site/`). Performance and SEO first, design second.

**How to work:** Stack and budgets: `03_SEO/research/stack/findings.md`. Keep `pages.md` current (slug, purpose, primary keyword). Components: SEO, Schema, Breadcrumbs, CTA, Gtm. Every page needs one canonical, one H1, schema that matches visible text, `tel:` and WhatsApp CTAs, data attributes from `04_Analytics/event-spec.md`. No claim without proof (knowledge file section 3). Developer name never shown.

**Do not touch:** Other folders. Do not write keywords yourself, read `03_SEO/keywords/keyword-map.md`.

**Contract:** `02_Website/pages.md` (page list) is read by seo and analytics.

**Finish:** write `result.json` (status, files, metrics, failures, next) in the folder you worked in, update your row in `../_ops/status.json`, do not commit.

**Release guard:** work only on branch `staging`. Deploy only with `release/deploy-staging.ps1` (Pages project iip-staging). Never run wrangler against `iip-site`, never touch production DNS or merge to `main`: only `release/promote.ps1`, run by the lead after the owner types GO LIVE. See `release/RELEASE-PROCESS.md`.
