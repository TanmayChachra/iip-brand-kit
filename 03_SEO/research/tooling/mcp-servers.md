# MCP servers for the IIP SEO, website and analytics workflow

Checked 2026-11-08. Stars and last push dates were read from the GitHub API on that day (labelled "verified"). Pricing and endpoints from vendor blogs are labelled "reported" and must be re-checked on the vendor page before paying.

## Verdict (3 lines)
1. OpenSEO (self hosted) is the hub: one server gives keyword research, rank tracking, backlinks, site audits, AI visibility, a local map rank grid, and it can plug into Google Search Console and GA4 itself. Install it first.
2. Add only three more now: the official Astro docs MCP (free, remote), the official Google Analytics MCP (read only, once the site has traffic) and later a Tag Manager MCP with owner approval for every write.
3. Skip the paid big suite MCPs (Ahrefs, Semrush), Brave, Perplexity, and every Google Business Profile community MCP for now. They cost money or are tiny, unproven projects.

## Already on this machine (do not duplicate)
- MCP servers in `~/.claude.json`: context7 (library docs), runpod, runpod-docs.
- Plugins: ponytail, telegram.
- Built in to this app: Claude in Chrome, built in browser, computer use, scheduled tasks, terminal, GitHub through the `gh` CLI, Google Workspace skill.
- Skills: about 75 local skills (gstack set, graphify, orchestrator, ai-delegation, agent-reach, design skills). Agent-Reach already covers web search through Exa.

## Table

Priority key: NOW = install when the site work starts, LATER = after the site is live, SKIP = not worth it today.

| Server | What it does for IIP | Cost | Auth (owner does it, never paste keys in chat) | Maturity (verified 2026-11-08) | Risk | Priority |
|---|---|---|---|---|---|---|
| **OpenSEO** `every-app/open-seo` | Keywords, rank tracking, competitor insight, backlinks, site audits, AI visibility, Local SEO map grid, GSC and GA4 connectors. One MCP endpoint for Claude. | Software is MIT and free. Data costs pay-as-you-go through your own DataForSEO key (reported, README says "bring your own key"). Local SEO map needs a Google Maps key with billing enabled (docs/GOOGLE_MAPS_SETUP.md). | DataForSEO key in the OpenSEO env file; MCP signs in with your OpenSEO account or an API key from Settings. | 26,806 stars, MIT, last push 2026-11-07. Docker or Cloudflare self host. | Public site needs a strong admin password and set up the admin account before exposing it (README says registration closes after the first admin). Set a DataForSEO spend cap. | **NOW** |
| **DataForSEO MCP** `dataforseo/mcp-server-typescript` | Raw SEO data API for Claude. | Pay as you go (reported). | API login and password. | 261 stars, Apache-2.0, pushed 2026-11-02. | Duplicates OpenSEO. Same key already powers OpenSEO. | SKIP (key still needed for OpenSEO) |
| **Google Analytics MCP** `googleanalytics/google-analytics-mcp` (official, Google) | Ask Claude about GA4 reports and property settings. Read only. | Free. | Google Application Default Credentials with read only analytics scope. | 3,685 stars, Apache-2.0, pushed 2026-11-05. Described as experimental by Google (reported). | Low, read only. | **LATER** (needs live GA4 data first). Note OpenSEO also has a GA connector, try that first. |
| **Search Console MCP** `AminForou/mcp-gsc` | Queries, clicks, URL inspection, sitemaps. | Free. | OAuth or service account. | 2,142 stars, MIT, pushed 2026-11-06. (Other options: surendranb 40 stars, saurabhsharma2u 321 stars covers GSC plus Bing plus GA4.) | Community project. Read the scopes before approving. | **LATER**, or skip if OpenSEO's GSC connector is enough (docs/SELF_HOSTING_GOOGLE_SEARCH_CONSOLE.md). |
| **Tag Manager MCP** `stape-io/google-tag-manager-mcp-server` or `paolobietolini/gtm-mcp-server` | Create and edit GTM tags, triggers, variables from chat. | Free (Stape also sells hosting, optional). | Google OAuth to your GTM account. | Stape: 245 stars, Apache-2.0, pushed 2026-11-03. Paolo: 186 stars, BSD-3, pushed 2026-11-04, says it makes a version before publishing (reported from README snippet). | Can change live tracking. Keep Claude to draft and preview, owner clicks Publish. | **LATER** (once GTM container exists) |
| **Astro Docs MCP** `https://mcp.docs.astro.build/mcp` | Current Astro documentation search for the website build. | Free. | None. | Official: the URL appears on docs.astro.build/en/guides/build-with-ai (verified 2026-11-08). | None. Overlaps partly with context7. | **NOW** (one command) |
| **Playwright MCP** `microsoft/playwright-mcp` | Drive a browser to test the site, forms, tracking events. | Free. | None. | 39,318 stars, Apache-2.0, pushed 2026-11-06. | Heavy on RAM (15 GB machine). Built in browser and Chrome extension already cover most needs. | LATER (only for scripted test runs) |
| **Lighthouse MCP** `priyankark/lighthouse-mcp` | Run Lighthouse performance audits from chat, no API key. | Free. | None. | 217 stars, MIT, pushed 2026-11-03. | Small project. The plain `lighthouse` CLI or PageSpeed web page does the same. | LATER (or just use the CLI in the build) |
| **PageSpeed Insights MCP** `PhialsBasement/Pagespeed-MCP-Server` | PSI API wrapper. | Free API key. | Google API key. | 13 stars, last push 2025-09-13. | Stale and tiny. | SKIP |
| **Firecrawl MCP** `firecrawl/firecrawl-mcp-server` | Crawl and scrape competitor sites into clean text. | Free credits (reported: 1,000 per month; check current page), paid after. | Firecrawl API key. | 7,777 stars, MIT, pushed 2026-11-08. | Credits burn on big crawls. | LATER (competitor crawl, we can start with Agent-Reach Jina Reader which is free) |
| **Exa MCP** `exa-labs/exa-mcp-server` | Neural web search. | Free tier reported (1,000 requests per month, check). | Exa key. | 5,216 stars, MIT, pushed 2026-11-05. | Already reachable through Agent-Reach. | SKIP (duplicate) |
| **Brave Search MCP** `brave/brave-search-mcp-server` | Web search. | Reported: free tier removed in February 2026, replaced by monthly credit with a card required. Sources conflict. | Brave key. | 1,565 stars, MIT, pushed 2026-11-06. | Needs a card. | SKIP |
| **Perplexity MCP** `perplexityai/modelcontextprotocol` | Cited search answers, also useful as an AI visibility check. | Paid API (reported about $5 per 1,000 searches). | Perplexity key. | 2,612 stars, MIT, pushed 2026-10-21. | Spend. | SKIP now. For AEO checks, ask Perplexity in the browser by hand. |
| **Cloudflare MCP** `cloudflare/mcp-server-cloudflare` | Manage Pages, DNS, Workers from chat. | Free with a Cloudflare account. | OAuth. | 4,453 stars, Apache-2.0, pushed 2026-10-22. | Can change DNS. Approval needed per change. | LATER (only if hosting on Cloudflare Pages) |
| **GitHub MCP** `github/github-mcp-server` | Repos, issues, PRs. | Free. | Token. | 34,319 stars, MIT, pushed 2026-11-06. | Token handling. | SKIP, the `gh` CLI already works here. |
| **Google Workspace MCP** `taylorwilsdon/google_workspace_mcp` | Sheets, Docs, Drive, Gmail, Calendar from chat. Good for keyword sheets and weekly reports. | Free. | Google OAuth. | 3,483 stars, MIT, pushed 2026-11-05. | Wide scopes. Pick narrow ones (Sheets and Drive only). Compare with the Google Workspace skill already present. | LATER |
| **Bing Webmaster MCP** `isiahw1/mcp-server-bing-webmaster` | Bing index and query data. | Free. | Bing API key. | 31 stars, MIT, pushed 2026-02-10. | Small. Bing Webmaster Tools can import from Search Console in the web UI. | SKIP (use the web UI) |
| **Ahrefs MCP** (official remote, `https://api.ahrefs.com/mcp/mcp`) | Backlinks and keywords from Ahrefs data. | Paid Ahrefs plan (reported). The old local repo `ahrefs/ahrefs-mcp-server` is archived (verified). | MCP scoped key from Ahrefs (reported). | Remote endpoint reported by a third party, not read on an Ahrefs page. | Spend. | SKIP for now |
| **Semrush MCP** (official remote, `https://mcp.semrush.com/v2/mcp`) | Semrush data in Claude. | Uses API units of a paid plan (reported). | OAuth. | Endpoint verified on developer.semrush.com on 2026-11-08 (shows v2; one blog said v1, so always copy from the vendor page). | Spend. | SKIP for now |
| **Google Business Profile MCPs** (`marcusbtc/gbp-mcp` and others) | Posts, reviews, insights from chat. | Free API, but Google must approve API access (guess, check). | OAuth plus Google Cloud project. | `marcusbtc/gbp-mcp`: 0 stars, last push 2026-08-18. No official Google server (reported). | Unproven. Could post or reply publicly. | SKIP. Manage GBP by hand and use OpenSEO Local SEO grid to measure. |
| **Screaming Frog MCP** (inside SEO Spider v24, reported) or `mshahiddigital/screamingfrog-audit-mcp` | Full site crawl audit. | App has a free tier limited to 500 URLs (known product limit, reported). Our site will be small. | None. | Not verified from a repo. | Needs the desktop app installed (RAM). | LATER (optional) |

## Install snippets (no secrets)

Copy as is. Owner adds keys in the env file or the login window, never in chat.

```bash
# Astro docs (official remote, no key)
claude mcp add --transport http "Astro docs" https://mcp.docs.astro.build/mcp

# OpenSEO after it runs locally in Docker (port 3001, from the OpenSEO docs)
claude mcp add --transport http --scope user openseo http://localhost:3001/mcp

# Google Analytics official MCP (after owner sets Application Default Credentials)
claude mcp add analytics-mcp -- pipx run analytics-mcp
```

The OpenSEO and Astro lines come from vendor docs (OpenSEO line reported by the project wiki via a search snippet; Astro line verified on the Astro page). The Analytics line is the usual pattern from Google's docs (reported, confirm on https://developers.google.com/analytics/devguides/MCP before running).

## Suggested order
1. Self host OpenSEO (Docker on your machine first, Cloudflare later). Connect GSC and GA4 inside it once the site exists.
2. Add the Astro docs MCP the day website work begins.
3. After launch: GA4 MCP, then GTM MCP (draft only), then Workspace MCP for Sheets.
4. Revisit paid suites only if OpenSEO data is not enough.

## Sources
- OpenSEO: https://github.com/every-app/open-seo (README, docs/SELF_HOSTING_DOCKER.md, docs/GOOGLE_MAPS_SETUP.md, docs/SELF_HOSTING_GOOGLE_SEARCH_CONSOLE.md)
- Astro: https://docs.astro.build/en/guides/build-with-ai/
- Semrush: https://developer.semrush.com/api/basics/semrush-mcp/
- Ahrefs archived repo: https://github.com/ahrefs/ahrefs-mcp-server
- Google Analytics MCP: https://github.com/googleanalytics/google-analytics-mcp
- All star counts and push dates: GitHub API, 2026-11-08.
