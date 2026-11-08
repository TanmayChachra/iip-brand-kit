# Claude skills for the IIP SEO, GEO, CRO and analytics workflow

Checked 2026-11-08. Stars and dates read from the GitHub API that day (verified). Security notes come from a quick regex scan of each repo's script files for network calls, shell pipes and installers. It is NOT a full code audit, so read a skill before installing it.

## Verdict (3 lines)
1. Start with `coreyhaines31/marketingskills` (59k stars) but install only the 10 to 13 skills we use, and add `AgriciDaniel/claude-seo` core skills for technical, local and GEO audits.
2. For AEO and GEO add `onvoyage-ai/gtm-engineer-skills`; for the Astro build add `jdevalk/skills` (astro-seo, static-seo, metadata-check).
3. Every skill adds a line to every session and big plugins add subagents, so install by name, not "all". The extension installers in claude-seo use `curl | bash`: skip those.

## Already installed locally (do not add again)
gstack set (qa, review, design-review, browse, ship, cso, etc.), web-design-guidelines, graphify, orchestrator, ai-delegation, agent-reach, document-generate, diagram, taste and design skills. These already cover QA, design review, web browsing and diagrams. No local skill covers SEO audit, schema, GEO, CRO copy or analytics tracking. That is the gap.

## Candidates

| Repo | Stars | Last push | Licence | What it does | Install | Security note | Priority |
|---|---|---|---|---|---|---|---|
| https://github.com/coreyhaines31/marketingskills | 59,118 | 2026-11-06 | MIT | 53 marketing skills. Relevant: seo-audit, ai-seo, schema, site-architecture, programmatic-seo, directory-submissions, link-building, competitor-profiling, competitors, content-strategy, copywriting, copy-editing, cro, ab-testing, conversion-tracking, analytics, customer-research, lead-magnets. | `npx skills add coreyhaines31/marketingskills --skill seo-audit ai-seo schema site-architecture` (CLI documented in its README) | Mostly markdown. Scripts found: dev scripts using child_process and subprocess, plus JS snippets in conversion-tracking/assets. Nothing remote fetched at install in the scan. | **NOW, selective** |
| https://github.com/AgriciDaniel/claude-seo | 27,342 | 2026-11-01 | MIT | Plugin with 26 skills and 19 subagents: seo-audit, seo-technical, seo-local, seo-maps, seo-geo, seo-schema, seo-sitemap, seo-cluster, seo-content-brief, seo-backlinks, seo-dataforseo, seo-competitor-pages. | `/plugin marketplace add AgriciDaniel/claude-seo` then `/plugin install claude-seo@agricidaniel-claude-seo` (README) | Optional extensions (ahrefs, banana) have install scripts with `curl` piped to `bash` and `rm -rf` in uninstall. Do not run extension installers. Core skills only. | **NOW, core only** (use seo-local, seo-geo, seo-technical, seo-schema) |
| https://github.com/onvoyage-ai/gtm-engineer-skills | 1,358 | 2026-10-11 | MIT | 12 skills for AEO and GEO: audit-website-aeo, improve-aeo-geo, geo-content-planning, geo-content-research, build-backlinks, build-resource-pages, reddit-opportunity-research, research-keywords, write-seo-geo-content. | `git clone https://github.com/onvoyage-ai/gtm-engineer-skills.git` then copy wanted folders into `~/.claude/skills` | `audit-website-aeo/scripts/aeo-audit.mjs` fetches pages and mentions `npm install`. Read before running. | **LATER** (when site is live) |
| https://github.com/jdevalk/skills | 111 | 2026-07-05 | MIT | Skills by an SEO developer (author name from README, reported): astro-seo, static-seo, content-seo, metadata-check, readability-check, astro-github-actions. | `npx skills add jdevalk/skills --skill astro-seo` (README) | Only 5 code files; wp-static-clone scripts use wget and urllib but we will not install that one. | **NOW** (astro-seo, static-seo, metadata-check) |
| https://github.com/Auriti-Labs/geo-optimizer-skill | 1,296 | 2026-11-04 | MIT | Audit whether ChatGPT, Perplexity and other AI engines can find and cite a site. Large repo (1,098 files, 158 code files). | See repo README. | Many scripts with fetch and shell calls, and an included frontend app. Heavier than we need. | LATER, only if claude-seo seo-geo is not enough |
| https://github.com/leopard627/fire-your-seo-agency | 997 | 2026-11-03 | MIT | One skill that audits SEO, AEO, GEO. | See repo README. | `tools/validate.py` uses subprocess, urllib and a pipe to sh. Read first. | SKIP (overlaps the two above) |
| https://github.com/JeffLi1993/seo-audit-skill | 783 | 2026-06-17 | MIT | Beginner SEO audit and reports. | See README. | Not scanned. | SKIP (overlap) |
| https://github.com/ethanplusai/astro-conversion-kit | 125 | 2026-10-31 | MIT | Converts an existing WordPress site into Astro. | See README. | Not scanned. | SKIP (we have no old site) |
| https://github.com/anthropics/skills | 189,030 | 2026-11-06 | none stated | Anthropic example skills (docx, pdf, pptx, webapp-testing, frontend-design, mcp-builder, skill-creator). | Plugin marketplace. | Official. | SKIP (gstack qa and design skills already cover most) |
| https://github.com/ComposioHQ/awesome-claude-skills and https://github.com/VoltAgent/awesome-agent-skills | 79,015 and 36,965 | 2026-09-18 and 2026-11-05 | none / MIT | Lists of skills to browse. | Browse only. | Lists include untrusted skills. | Browse, never bulk install |
| OpenSEO agent skills (https://openseo.so/docs/skills/setup) | part of OpenSEO | n/a | MIT | Pre built SEO workflows that call the OpenSEO MCP. | Per OpenSEO setup page (README link, not read in full). | Runs only against our own OpenSEO. | **NOW**, once OpenSEO runs |

## Top 8 recommendation, in install order
1. OpenSEO agent skills (pairs with the MCP, our real data).
2. marketingskills: seo-audit, schema, site-architecture, ai-seo (week one).
3. claude-seo core: seo-technical, seo-schema, seo-sitemap, seo-local (week one).
4. jdevalk astro-seo, static-seo, metadata-check (while building the Astro site).
5. marketingskills: conversion-tracking, analytics, ab-testing (for GTM and GA4 work).
6. marketingskills: directory-submissions, link-building (backlink and listing sprint).
7. onvoyage gtm-engineer-skills: audit-website-aeo, improve-aeo-geo (after launch).
8. marketingskills: cro, copywriting, copy-editing (landing page tests).

Skipped on purpose: duplicates (fire-your-seo-agency, seo-audit-skill), irrelevant (astro-conversion-kit), generic collections.

## Token cost note
- Each installed skill puts its name and a one line description in every session. Our 75 local skills already cost that. Adding the whole marketingskills pack (53) plus the whole claude-seo plugin (26 skills plus 19 agents) would add roughly 100 more listed items (estimate, guess). Installing about 20 by name keeps it small.
- A skill body is only loaded when it is used, but SEO skills can be long and call tools many times, so run them in a background fork and read only the short report.
- Keep audits file based: skills write findings to `03_SEO/research/`, the lead reads the summary and result.json.

## Install safety checklist (owner)
1. Prefer `npx skills add <repo> --skill <name>` with names.
2. Open the SKILL.md and any scripts folder first.
3. Never run install scripts that pipe `curl` into `bash`.
4. Keep API keys in env variables, never in skill files.
