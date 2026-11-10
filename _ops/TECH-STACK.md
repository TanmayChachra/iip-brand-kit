# Tech stack and operations (maintain end to end)

Single technical record for IIP marketing and visibility: accounts by role, infrastructure, every MCP and skill, how to reconnect, what is verified. Update this file in the same commit as any change (CLAUDE.md sync rule). No passwords, tokens or API keys here, ever. Account email addresses live only in `_ops/private/TECH-STACK-private.md` (git ignored) and in Claude memory.

Last verified: 2026-11-09.

## 1. Accounts by role
| Role | Account | Owns | Status |
|---|---|---|---|
| Owner personal Google and Cloudflare account | the owner's personal Gmail (see private file) | The personal server network tanmay-hq.in, the self-hosted OpenSEO Worker, DataForSEO account, Cloudflare account used by the MCPs, Google Business Profile Phase 1 today | Active |
| Business Google account | to be created (decision 2026-11-09: recommended, owner creates) | Future owner of Business Profiles, GA4, GTM, Search Console, YouTube, registrar, IIP Cloudflare account | Pending |
| Registrar | Porkbun (planned) | isapurindustrialpark.in and .com | Pending purchase |
| Hosting | Cloudflare Pages (planned) | The Astro site | Pending domain |
| Email | Zoho Mail free or Cloudflare Email Routing (planned) | info@ on the IIP domain | Pending domain |

## 2. Infrastructure
- **OpenSEO** (self-hosted, Cloudflare Worker): https://openseo.tanmay-hq.in , MCP at /mcp. Protected by Cloudflare Access (team domain tanmaypersonaln8n.cloudflareaccess.com). Managed OAuth is ON, allowed redirect URIs: loopback for Claude Code, https://claude.ai/api/mcp/auth_callback and https://claude.com/api/mcp/auth_callback for Claude Desktop and web. Projects: Default (crownmont.ca, not IIP, do not touch) and **Isapur Industrial Park** (id 46ae0e81-28ff-4b06-ae7f-aa188879b44c, domain isapurindustrialpark.in planned, market India, language en, created 2026-11-09). Do all IIP paid searches inside the IIP project.
- **DataForSEO**: API account connected 2026-11-09, funds added by the owner on 2026-11-09 (51 USD deposited), OpenSEO to DataForSEO verified with one keyword call (earlier 403 was the trial limit). Budget idea: about 5K a month (currency to confirm). Spend cap in the account is still to set. Paid calls only after the owner's yes and a cost estimate.
- **GitHub**: repo TanmayChachra/iip-brand-kit (public). Pages from /docs: kit (/), board (/board/), poster lab (/experiments/poster-lab/). Source of the board: `_ops/board/build_board.py` from `_ops/status.json`.
- **Local site builds**: `02_Website/site` (v1, rejected), `02_Website/site-v2` (Astro, taste-skill 2.5.1, work in progress). Preview ports 4321 (v1) and 4323 (v2) via `.claude/launch.json`. Node 24, Astro 7.x pinned in package.json.
- **Scheduled task**: `iip-seo-weekly-watch` (Mondays about 9:13, runs while the Claude app is open, writes proposals to `03_SEO/watch/`).

## 3. MCP inventory (this project)
Never delete or re-add these without the owner. The owner authorized the Cloudflare, OpenSEO and DataForSEO connections with full access from the owner's personal account (2026-11-09).
| MCP | Endpoint | How it is connected | Purpose | Verified |
|---|---|---|---|---|
| cloudflare-api | https://mcp.cloudflare.com/mcp | Claude Desktop connector (authorized, whoami ok). Also a user-scope CLI entry that still needs its own `/mcp` sign-in in a terminal | DNS, Pages, Workers, Email Routing, Access (2,500+ API endpoints in Code Mode: search, execute, docs) | 2026-11-09 |
| openseo | https://openseo.tanmay-hq.in/mcp | Claude Desktop connector (connected, whoami and list_projects ok). The CLI entry shows Needs authentication until signed in via `/mcp` | Keyword research, rank tracking, audits, backlinks, AI visibility, Local SEO (uses DataForSEO credits) | 2026-11-09 |
| dataforseo | DataForSEO MCP (api_request, docs_search, docs_list_sections, docs_index) | Added by the owner as a Claude Desktop connector | Raw DataForSEO API. Free calls such as /v3/appendix/user_data work now (balance read: 1 USD). Paid calls need funds and approval | 2026-11-09 |
| astro-docs | https://mcp.docs.astro.build/mcp | User-scope CLI entry, no auth | Astro documentation search | 2026-11-09 |
| context7 | https://mcp.context7.com/mcp | User-scope CLI entry | Library docs | 2026-11-09 |
| runpod, runpod-docs | npx @runpod/mcp-server, https://docs.runpod.io/mcp | User-scope CLI entries | Not used by IIP (other projects) | 2026-11-09 |
Also planned (not connected): Google Analytics MCP, Search Console MCP, Tag Manager MCP, Google Workspace MCP, Porkbun MCP (after the accounts exist). Details: `03_SEO/research/tooling/mcp-servers.md`.

Reconnect runbook: Claude Desktop, Settings, Connectors, pick the connector, Reconnect. CLI: in a terminal run `claude`, `/mcp`, choose the server, Authenticate. OpenSEO needs Managed OAuth on in Cloudflare Zero Trust, Access controls, Applications, OpenSEO.

## 4. Skills installed (user level, ~/.claude/skills)
marketingskills (12: seo-audit, schema, site-architecture, ai-seo, programmatic-seo, directory-submissions, link-building, conversion-tracking, ab-testing, cro, copywriting, copy-editing), claude-seo core (seo-technical, seo-schema, seo-sitemap, seo-local, seo-geo), jdevalk (astro-seo, static-seo, metadata-check), OpenSEO skills (12), design stack (taste-skill 2.5.1, impeccable 4.8.1 skill folder only, web-design-guidelines, awesome-design-md), playwright-cli 0.1.23 (npm global). The Impeccable engine binary is deliberately NOT run (downloaded executable). Log: `03_SEO/research/tooling/installed.md`, `02_Website/research/design-skills-installed.md`.

## 5. Maintenance rules
1. Any new account, MCP, skill, host or scheduled task is added here the same day, with endpoint, scope, purpose and verified date.
2. Monthly: re-verify each MCP (a free read), check DataForSEO balance and spend, check OpenSEO and Astro versions, review `03_SEO/watch/`.
3. Secrets stay in environment variables or the services' own settings. Never in git, docs or chat.
4. Domain, DNS and Access changes go through the Cloudflare MCP and need the owner's confirmation first.

## 6. Change log
- 2026-11-09: Cloudflare, OpenSEO and DataForSEO MCPs connected and verified through Claude Desktop connectors. Astro docs MCP added. DataForSEO balance read: 1 USD.

## 7. Secrets and addresses policy (how nothing gets lost)
- Account email addresses and where every secret lives are in the local-only map `_ops/private/ACCOUNTS-AND-SECRETS-MAP.md` (git ignored). A backup copy outside the project (`~/IIP-private-backup`) can be made with `python _ops/private/backup.py` once the owner approves. Claude memory holds a pointer.
- Secret values never go in this repo, docs, chat or screenshots. They live in the owner's password manager or in each service's own settings (for example the Claude Desktop connector settings for DataForSEO).
- Proposed, not installed: a local git pre-commit hook that runs `_ops/private/scan_secrets.py` to block commits containing key-like strings, private files or blocklisted addresses. It needs the owner's explicit yes because it changes `.git/hooks`.
- If a secret was exposed, rotate it the same day using the recovery column in the private map.
- 2026-11-09: owner added DataForSEO funds (51 USD). OpenSEO test call succeeded, 92 keywords checked (about 50.97528 USD left). OpenCLI extension is enabled but Reddit needs the owner logged in to reddit.com in Chrome.
- 2026-11-09: OpenSEO project Isapur Industrial Park created. Paid research run (about 0.42 USD): 92 keywords, 5 seed ideas, competitor overviews, backlinks, local SERP, 5x5 rank grid. Results: 03_SEO/keywords/openseo-research-2026-11-09.md. DataForSEO balance about 50.56 USD.
- 2026-11-10: Domain isapurindustrialpark.com bought at Porkbun (business Gmail account created). Cloudflare zone created in the IsapurIndustrialPark account (id db3c919b72534e491e8e33c393480b5d), pending until nameservers at Porkbun are set to celeste.ns.cloudflare.com and decker.ns.cloudflare.com. .in not registered per registry check, owner to confirm. Porkbun MCP (https://porkbun.com/mcp) added at user scope, needs owner sign-in via /mcp.
