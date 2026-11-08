# Claude skills and plugins for building the IIP website (researched 2026-11-08)

**Verdict:** Add very little. We already have strong design and QA skills installed. The real gaps are Astro SEO checks, Core Web Vitals and accessibility audits, and one design reviewer that catches "AI slop" and a washed-out black and white look. Add 4 things now, 3 later, skip the rest.
**Evidence:** stars, last push and licence read from the GitHub API on 2026-11-08 (verified). SKILL.md heads and scripts read through the API for the skills below. Local overlap read from `~/.claude/skills` (names only).
**Caveat:** security notes are a manual read of the entry file and script names plus targeted greps, not a full code audit. Star counts on mega packs (impeccable, taste-skill, ui-ux-pro-max) are very high and partly hype: judge by what the skill does for us.

Labels: V = verified at the source on 2026-11-08, R = reported by a third party, G = guess.

## Already installed locally (do not add again)
web-design-guidelines (Vercel), taste-skill, taste-skill-v1, minimalist-skill, brutalist-skill, soft-skill, gpt-tasteskill, redesign-skill, image-to-code-skill, imagegen-frontend-web, imagegen-frontend-mobile, stitch-skill, awesome-design-md, design-consultation, design-html, design-review, plan-design-review, qa, qa-only, browse, benchmark, health, ship, land-and-deploy, setup-deploy, canary, cso, devex-review, ponytail, orchestrator, artifact-design, plus the shared-library and docs skills. (V, directory listing.)

## Candidates

| Repo | Stars | Last push | Licence | What it does | Install | Security note | Overlap | Verdict |
|---|---|---|---|---|---|---|---|---|
| https://github.com/anthropics/skills (`frontend-design`) | 189,037 (whole repo) | 2026-11-06 | per skill `LICENSE.txt` (API shows none for the repo) | Design lead prompt: pick a distinct aesthetic, typography and colour decisions, avoid templated defaults | Copy `skills/frontend-design/` into `~/.claude/skills/` or add the Anthropic plugin marketplace | Prompt only, no scripts in this skill (V, SKILL.md read) | Partly overlaps taste-skill and design-consultation | **Add now** (one small file, official) |
| same repo (`webapp-testing`) | same | same | per skill | Playwright Python helper `scripts/with_server.py` to start the dev server and drive pages | Copy folder | Runs local scripts only (G: not fully read) | Overlaps `qa`, `browse` and the Playwright we already use | Skip |
| https://github.com/addyosmani/web-quality-skills | 3,054 | 2026-08-24 | MIT | Five skills: accessibility, core-web-vitals, performance, seo, web-quality-audit. Checklists plus one `analyze.sh` | `npx skills add addyosmani/web-quality-skills` or its plugin | `analyze.sh` only greps files for `http://` strings, no curl or wget (V, grep) | Fills a real gap (CWV and a11y checklists) | **Add now** |
| https://github.com/jdevalk/skills (`astro-seo`, `static-seo`, `metadata-check`, `astro-github-actions`) | 111 | 2026-07-05 | MIT | Audits Astro SEO: head, JSON-LD, sitemap, IndexNow, OG images. Routes code through the npm package `@jdevalk/astro-seo-graph` | `npx skills add jdevalk/skills --skill astro-seo` | The skill itself is prompt text. It recommends an npm dependency: check the package before using it. The repo also holds WordPress scripts we do not need (V, tree) | Gap: nothing installed targets Astro | **Add now** as an audit tool. We still write our own `SEO.astro` and `Schema.astro` |
| https://github.com/pbakaus/impeccable | 105,792 | 2026-11-08 | Apache-2.0 | 24 design commands: critique (scored UX review), audit (a11y, performance, theming, responsive), polish, colorize, bolder, quieter, typeset, adapt, optimize, plus a 62 rule slop detector with no LLM | `npx impeccable install` from the project root, then `/impeccable init` | The installer is an npm package (remote code, run it only inside `02_Website/site/`). Browser helper scripts talk to `localhost` only (V, grep of `live-browser.js`). It writes `PRODUCT.md` and `DESIGN.md` into the project | Overlaps design-review, taste-skill | **Add later** after the first build: `critique`, `audit`, and `colorize` directly serve "not too much black and white" |
| https://github.com/nextlevelbuilder/ui-ux-pro-max-skill | 146,667 | 2026-11-07 | MIT | Searchable style, palette (192) and font pairing (74) library, with Python helper scripts and a CLI | `/plugin install ui-ux-pro-max@ui-ux-pro-max-skill` or `npm i -g ui-ux-pro-max-cli` | 845 files, Python scripts, a global npm CLI: larger surface (V, tree) | Our brand is locked, so palette and font search is not needed | Skip |
| https://github.com/Leonxlnx/taste-skill | 111,790 | 2026-11-07 | MIT | Anti-slop frontend rules | already installed | n/a | installed | Keep, load one taste skill only (taste-skill) |
| https://github.com/vercel-labs/agent-skills (`web-design-guidelines`, react-best-practices) | 33,701 | 2026-10-28 | none stated | Web interface guideline review; React and Next performance rules | web-design-guidelines already installed | React rules do not apply to Astro | installed | Keep `web-design-guidelines` as a review gate. Skip the React pack |
| https://github.com/shadcn-ui/ui (skills folder) | 127,601 | 2026-11-08 | MIT | shadcn component skills (one found: migrate-radix-to-base) | n/a | n/a | React only | Skip |
| https://github.com/addyosmani/agent-skills | 113,972 | 2026-11-01 | not read | Engineering lifecycle skills including frontend-ui-engineering, performance-optimization, ci-cd | plugin | not scanned | Overlaps ship, health, qa | Skip (maybe look later) |
| https://github.com/obra/superpowers | 314,300 | 2026-11-03 | MIT | Planning, TDD, verification workflow skills | plugin | not scanned | Overlaps orchestrator, ponytail, gstack | Skip |
| https://github.com/ChromeDevTools/chrome-devtools-mcp | 54,948 | 2026-11-08 | Apache-2.0 | Chrome DevTools for agents (traces, console, network). Its eval folder shows Lighthouse audit support | `npx` MCP server | Controls a real browser: heavy on RAM (15 GB machine) | Overlaps browse and Playwright | Later, only if `@lhci/cli` is not enough |
| https://github.com/microsoft/playwright-mcp | 39,318 | 2026-11-06 | Apache-2.0 | Browser automation MCP | MCP | Heavy RAM | We script Playwright directly | Skip |
| https://github.com/Community-Access/accessibility-agents | 438 | 2026-11-07 | MIT | Accessibility audit agents | plugin | not scanned | Axe in Playwright does the same, deterministic | Skip |
| https://github.com/coreyhaines31/marketingskills and https://github.com/AgriciDaniel/claude-seo | 59,121 and 27,346 | 2026-11-06 and 2026-11-01 | MIT | SEO and CRO skills | see `03_SEO/research/tooling/claude-skills.md` | see that file | Covered by the SEO tooling research | Follow that file |
| Astro Docs MCP `https://mcp.docs.astro.build/mcp` | n/a | n/a | n/a | Official Astro docs search | add as an MCP URL | Read only docs (R: URL verified by the SEO tooling fork on docs.astro.build) | none | **Add now** |
| https://github.com/ComposioHQ/awesome-claude-skills , https://github.com/VoltAgent/awesome-agent-skills , https://github.com/travisvn/awesome-claude-skills | 79,016 , 36,966 , 15,741 | 2026-09-18 , 2026-11-05 , 2026-04-28 | none, MIT, none | Lists of skills | browse only | Lists point at third party code: read before installing anything | n/a | Browse, do not install |

## Not skills, but the QA tools the cycle needs (npm, versions V from `npm view` on 2026-11-08)
`astro` 7.4.7, `@astrojs/check` 0.9.12, `@playwright/test` 1.65.0, `@axe-core/playwright` 4.14.0, `@lhci/cli` 0.16.0 (Lighthouse CI), `linkinator` 8.1.0 (link check), `html-validate` 11.19.0, `pa11y` 10.0.0 (optional).

## Top 8, in install order
1. **web-design-guidelines** (installed): run as the review gate on every page. No install.
2. **Astro Docs MCP**: official docs while building. Add as an MCP URL.
3. **anthropics/skills frontend-design**: one file, steers away from templated looks. Copy the folder.
4. **addyosmani/web-quality-skills**: CWV, performance, accessibility, SEO checklists. `npx skills add addyosmani/web-quality-skills`.
5. **jdevalk/skills astro-seo and metadata-check**: audit head tags, schema, sitemap on the finished pages. `npx skills add jdevalk/skills --skill astro-seo`.
6. **impeccable** (after the first build): `critique`, `audit`, `colorize`, `polish`. Install only inside `02_Website/site/`.
7. **chrome-devtools-mcp** (only if needed): deeper traces than Lighthouse CI.
8. **taste-skill** (installed): one pre-flight check before the visual pass. Do not load the other taste skills in the same run.
Owner or lead runs the install commands. Nothing was installed by this research.

## Token cost note (G)
Each installed skill adds its name and description to every session's skill list (roughly 50 to 150 tokens each). This machine already lists about 90 skills. Packs that install dozens (impeccable has 24 commands behind one entry, ui-ux-pro-max ships several sub-skills) cost little until invoked but add up when many are loaded at once. Install by name, not whole packs. Keep one design reviewer loaded per task (web-design-guidelines for review, impeccable for polish) and never run two taste skills together.
