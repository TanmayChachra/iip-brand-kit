# Installed skills (2026-11-08)

**Verdict:** 32 skills installed into `~/.claude/skills/` (top-level skill folders went from 77 to 109). Nothing skipped, nothing overwritten. No installer was run, no script from a clone was executed.
**Evidence:** shallow clones in the session scratchpad, every file read or grepped before copy. Security grep (curl, wget, bash -c, eval, base64, Invoke-WebRequest, subprocess, requests, fetch(, os.system, pipe to sh, iex, npx, npm i, pip install, git clone) plus a hidden unicode scan.
**Caveat:** grep plus reading the hit lines, not a full code audit. New skills load in the next Claude session.

## Security gate result
- All hits were documentation text (words like "evaluate", prose that mentions curl or fetch as a tip, `npm install @jdevalk/astro-seo-graph` and `npm install -g linkinator` as instructions the agent would propose, not run at install). No pipe-to-shell, no remote code fetch, no eval, no base64, no hidden unicode.
- `conversion-tracking` ships `assets/gtm-recipes/*.json` (GTM custom HTML tags), `assets/snippets/*.js`, and `scripts/build_recipe.py` and `scripts/check_recipes.py`. Scanned: no network calls or beacons, only DOM listeners and dataLayer pushes. They run only if someone imports a recipe into GTM. Kept, since GTM is in our plan. Read each recipe before importing.
- claude-seo: only the five core skill folders were copied. Its `install.sh`, `install.ps1`, extensions, hooks and agents were NOT copied (the curl | bash installers). `LICENSE.txt` and the `evals` folders were left out of every copy.
- jdevalk `static-seo` and `astro-seo` AGENTS.md contain install and curl examples for the agent to propose to the user. The owner should approve any `npm install -g` line.
- OpenSEO skills: copied the 12 public skills from `.agents/skills/` (the ones documented at https://openseo.so/docs/skills/). The repo's internal developer skills (deslop, merge-ready, papercuts and similar) were not copied. They need the OpenSEO MCP connected to do real work.

## Names and one rename
- OpenSEO `seo-audit` clashes with marketingskills `seo-audit`. The OpenSEO copy was installed as `openseo-seo-audit` and its frontmatter `name:` was changed to match (the only edit made to any copied file).

## Installed list
| Skill folder | Source | Files | KB | Note |
|---|---|---|---|---|
| seo-audit | marketingskills | 8 | 65 |  |
| schema | marketingskills | 2 | 17 |  |
| site-architecture | marketingskills | 5 | 49 |  |
| ai-seo | marketingskills | 16 | 164 |  |
| programmatic-seo | marketingskills | 3 | 22 |  |
| directory-submissions | marketingskills | 4 | 89 |  |
| link-building | marketingskills | 4 | 30 |  |
| conversion-tracking | marketingskills | 74 | 623 |  |
| ab-testing | marketingskills | 3 | 29 |  |
| cro | marketingskills | 3 | 26 |  |
| copywriting | marketingskills | 4 | 56 |  |
| copy-editing | marketingskills | 4 | 36 |  |
| seo-technical | claude-seo core | 2 | 24 |  |
| seo-schema | claude-seo core | 2 | 13 |  |
| seo-sitemap | claude-seo core | 1 | 6 |  |
| seo-local | claude-seo core | 1 | 18 |  |
| seo-geo | claude-seo core | 3 | 33 |  |
| astro-seo | jdevalk/skills | 3 | 44 |  |
| static-seo | jdevalk/skills | 3 | 42 |  |
| metadata-check | jdevalk/skills | 2 | 6 |  |
| ai-prompt-research | open-seo | 1 | 10 |  |
| ai-visibility-audit | open-seo | 1 | 13 |  |
| competitive-landscape | open-seo | 1 | 6 |  |
| competitor-analysis | open-seo | 1 | 6 |  |
| keyword-clustering | open-seo | 1 | 6 |  |
| keyword-research | open-seo | 1 | 7 |  |
| link-prospecting | open-seo | 1 | 7 |  |
| local-seo | open-seo | 1 | 13 |  |
| openseo-seo-audit | open-seo | 1 | 15 | renamed from seo-audit to avoid clash with marketingskills seo-audit |
| seo-coach | open-seo | 1 | 10 |  |
| seo-project-setup | open-seo | 1 | 9 |  |
| seo-report | open-seo | 1 | 22 |  |

## Token cost
- 32 more skills appear in the skills list in every session. The marketingskills descriptions are long (about 100 tokens each), OpenSEO and claude-seo ones 30 to 60. Estimated 2,000 to 3,000 tokens added to the listing per session (guess). Bodies and references load only when a skill is used.
- To uninstall, delete the folder from `~/.claude/skills/`. Least needed first: seo-project-setup, seo-report, seo-coach (need the OpenSEO MCP), competitive-landscape, keyword-clustering.

## Needs the OpenSEO MCP
ai-prompt-research, ai-visibility-audit, competitive-landscape, competitor-analysis, keyword-clustering, keyword-research, link-prospecting, local-seo, openseo-seo-audit, seo-coach, seo-project-setup, seo-report.
