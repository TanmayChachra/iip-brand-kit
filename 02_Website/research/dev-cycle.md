# Web development cycle for the IIP Astro site (v1, 2026-11-08)

**Verdict:** Run a short loop of brief, build, gate, preview, launch. Every step ends in a file or a number so any agent can pick up where another stopped. Total agent time for the first launch-ready site is about 4 to 5 hours (G), most of it content and QA, not code.
**Evidence:** tool versions are from `npm view` on 2026-11-08 (verified): astro 7.4.7, @astrojs/check 0.9.12, @playwright/test 1.65.0, @axe-core/playwright 4.14.0, @lhci/cli 0.16.0, linkinator 8.1.0, html-validate 11.19.0. Cloudflare Pages preview deployments per branch are reported from Cloudflare docs (confirm on deploy day).
**Caveat:** time estimates are guesses. Google's Rich Results Test has no official API, so schema checks are a script plus one manual run at launch.

Labels: V = verified, R = reported, G = guess.

## The loop (one pass per page type, then per page)

| # | Step | Output | Time (G) | Owner agent |
|---|---|---|---|---|
| 1 | **Brief**: goal, audience, primary CTA, allowed claims. Read `CLAUDE.md`, knowledge file section 3, `DESIGN-DIRECTION.md`, `pages.md` | `02_Website/BRIEF.md` (one page) | 10 min | web |
| 2 | **Tokens**: colours, fonts, spacing, radius from `Brand-Kit/tokens/brand.tokens.json` into CSS variables. Self-host Montserrat and Inter (Latin subset) | `src/styles/tokens.css` | 20 min | web |
| 3 | **Wireframe**: sections per page in plain Markdown (order, one job, CTA). No visuals yet | `02_Website/wireframes.md` | 30 min | web |
| 4 | **Shell**: `Base.astro` layout, header with thin flag, sticky mobile bar (call, WhatsApp), footer, `SEO.astro`, `Schema.astro`, `Gtm.astro` (loads after first interaction), skip link | layout and 5 components | 45 min | web |
| 5 | **Components**: Hero, ProofChips, PlotCards, DistanceTable, AmenityGrid, FaqList, CtaBand, ImageSlot (photo placeholder with swap path), SectionBand (green, yellow, sage backgrounds) | `src/components/` | 45 min | web |
| 6 | **Assets in**: illustrations, icons, OG images, favicons into `public/img/` as WEBP and SVG | `02_Website/assets/INDEX.md` lists every file with alt text | parallel | assets |
| 7 | **Content in**: copy from `06_Content/website-copy/`, titles, metas and H1 from `03_SEO/keywords/keyword-map.md` into content collections | `src/content/` | 60 min | web with content and seo outputs |
| 8 | **QA gates** (below), fix, repeat until all pass | `02_Website/qa/YYYY-MM-DD/` reports | 30 to 60 min | web plus qa skill |
| 9 | **Preview deploy**: push a branch, Cloudflare Pages builds a preview URL per branch (R). Check on a real phone | preview URL in `CHECKLIST.md` | 15 min | lead |
| 10 | **Launch checklist** (below) | all boxes ticked | 30 min | lead with owner |
| 11 | **Post launch**: Search Console, GTM tests, first review at 14 days | `04_Analytics/reviews/` | 30 min | analytics |

## QA gates (all must pass before a preview is shared, and again before launch)

| Gate | Tool | Pass rule | Command sketch |
|---|---|---|---|
| Type and build | `@astrojs/check` | 0 errors | `npx astro check && npx astro build` |
| Performance | `@lhci/cli` on the built `dist/` (mobile preset, 3 runs) | Perf 95 plus, LCP 1.8 s or less, CLS 0, TBT under 150 ms. Budgets: HTML 30 KB gzip, CSS 30 KB, JS 60 KB, hero image 100 KB, first load 500 KB | `npx lhci autorun` with `lighthouserc.json` budgets |
| Accessibility | `@axe-core/playwright` on every page, 390 px and 1280 px | 0 serious or critical violations. Also: contrast AA, focus rings, alt text, skip link, 44 px tap targets | Playwright test file `qa/a11y.spec.ts` |
| Screenshots | `@playwright/test` | Mobile 390 and desktop 1280 per page saved to `qa/YYYY-MM-DD/shots/`. Lead looks at one contact sheet. No horizontal scroll | `qa/shots.spec.ts` |
| Links | `linkinator` on the served `dist/` | 0 broken internal links, outbound links reviewed | `npx linkinator http://localhost:4321 --recurse` |
| HTML validity | `html-validate` | 0 errors | `npx html-validate dist/**/*.html` |
| Schema | Script parses every JSON-LD block, checks required fields for Organization, LocalBusiness, Place, FAQPage, BreadcrumbList, Article. Then manual run of Google's Rich Results Test (https://search.google.com/test/rich-results) and https://validator.schema.org/ once at launch | 0 errors, markup matches visible text, no schema for unproven claims | `qa/schema-check.mjs` |
| Robots and sitemap | Script | `robots.txt` has the sitemap line, `sitemap-index.xml` lists only built pages, drafts absent, one canonical per page, one H1 per page | `qa/seo-check.mjs` |
| **Claim check** | Script against the knowledge file | Fail the build if any unproven term appears in `dist/`: Section 80, Zilla Panchayat, Amul, Inox, Patanjali, petrol, drainage, "24 hour", security, UPSIDA, any price. List lives in `qa/forbidden-terms.json` and is edited only by the lead when proof lands | `qa/claim-check.mjs` |
| Design review | `web-design-guidelines`, later impeccable `critique` and `audit` | No P0 findings. Colour check: at least 40 percent of scroll height is non black and white | skill run, report saved |

Rule: a gate that fails twice for the same reason gets a fix in the shared component, not a patch on one page.

## Launch checklist (copy into `02_Website/CHECKLIST.md`)
- [ ] Domain bought, DNS on Cloudflare, HTTPS forced, www redirect decided
- [ ] `site` in `astro.config.mjs` is the final domain, canonicals correct
- [ ] Owner proof received for each published claim, forbidden list updated, proof pages un-drafted
- [ ] Real photos placed in the ImageSlots (or slots hidden)
- [ ] NAP matches `05_Local-Presence/citations/nap.md` everywhere
- [ ] GTM container ID and GA4 set, all events in `04_Analytics/event-spec.md` fire on a real phone
- [ ] Form endpoint works, success fires `generate_lead` once
- [ ] Search Console domain verified, sitemap submitted. Bing Webmaster imported, IndexNow key set
- [ ] robots.txt allows search bots, sitemap line present
- [ ] 404 page, privacy page live
- [ ] Lighthouse mobile 95 plus on home, plots, location, contact
- [ ] GBP website link set with UTM (`?utm_source=google&utm_medium=organic&utm_campaign=gbp`)
- [ ] Rollback: previous Cloudflare deployment can be promoted in one click (R)

## Post launch
Day 0: submit sitemap, request indexing for home and 3 money pages. Day 3: check coverage and GTM events. Day 14: first review with `04_Analytics/gtm-plan.md` rules. Day 30: first keyword and conversion review, decide what to double down on and what to drop.

## How parallel agents split the work without conflicts
All agents work from this one chat as forks and write disjoint paths. The lead integrates and commits once per batch.
| Agent | Writes only | Reads |
|---|---|---|
| web | `02_Website/site/` except `public/img/`, `02_Website/*.md` | assets index, content, keyword map, event spec, tokens |
| assets | `02_Website/assets/`, `02_Website/site/public/img/` | design direction, brand kit |
| content | `06_Content/website-copy/` | keyword map (when ready), knowledge file |
| seo | `03_SEO/keywords/` | competitor findings |
| analytics | `04_Analytics/` | `pages.md` |
| qa (lead or a fork) | `02_Website/qa/` | built `dist/` |
Hand-offs happen through files only: `pages.md` (slugs), `keyword-map.md` (titles, H1, metas), `assets/INDEX.md` (file names and alt text), `event-spec.md` (data attributes), `qa/forbidden-terms.json` (claims). If a contract changes, the owner of the file bumps its version line and the lead re-runs the gates.

## Checklist file format (`02_Website/CHECKLIST.md`)
One line per item: `- [ ] ID | gate | agent | evidence path | note`. Example: `- [x] G3 | lighthouse home | web | qa/2026-11-09/lhci-home.json | perf 97`. The lead keeps it; each agent updates its own lines only. `_ops/status.json` row for 02_Website points at this file.
