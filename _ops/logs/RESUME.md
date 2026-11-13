# Resume point (saved 2026-11-10)

Read this first after a restart, then CLAUDE.md, _ops/TECH-STACK.md, TODOS.md.

## State
- Website v2 (`02_Website/site-v2`, Astro, taste-skill 2.5.1): home passes the gate, inner pages open. A background builder fork was running when the session ended and is probably dead. Its progress is in `02_Website/qa/v3/PROGRESS.md` (read it, it is written after each step). Next: relaunch a builder with the same brief (see DESIGN-DIRECTION.md v3 plus the audit at `02_Website/qa/v3/audit/audit.md`): all pages to GATE PASS, home polish, /industrial-areas-in-ghaziabad/ guide page, site URL from one env var.
- v1 site (`02_Website/site`) is rejected, reference only. AI renders archived in `Archive/website-v1b-ai-renders/`.
- OpenSEO project "Isapur Industrial Park" id 46ae0e81-28ff-4b06-ae7f-aa188879b44c is set up, research done (about 0.45 USD spent, balance about 50.5 USD): `03_SEO/keywords/openseo-research-2026-11-09.md` (Maps position strong, organic demand small, Hindi check done).
- MCPs live this session: cloudflare-api, openseo, dataforseo (Desktop connectors), astro-docs. Never delete them. Free reads first, paid runs need cost estimate.
- Secrets and emails: local only, `_ops/private/ACCOUNTS-AND-SECRETS-MAP.md`. Commit guard hook and external backup are written but NOT installed or run (owner must say yes).

## Owner is doing now (2026-11-10)
1. Buying the domain (isapurindustrialpark.in plus .com at Porkbun).
2. Creating the business Gmail and moving the Google assets to it.
3. Compiling the approval documents to send.
4. Connecting the Google Business Profiles.
Also pending from the owner: plot maps and Google Earth KML, on-ground photos, sales questions, WhatsApp number, 360 tour later, A/B testing after launch.

## Next for Claude when the owner returns
1. Relaunch the v2 builder (see above) and show screenshots in the Browser pane (launch.json entry iip-site-v2, port 4323).
2. When the domain is named: update site config, schema, NAP, tech record; create DNS and Pages through the Cloudflare MCP (confirm first); create the rank tracker in OpenSEO (free until run).
3. When approval docs arrive: Approvals page and markup.
4. When GBP is under the new account: read profiles via OpenSEO, apply the ready edits in `05_Local-Presence/gmb/audit.md` only with the owner's approval.
5. Keep board, TODOS, knowledge file and TECH-STACK in sync, then push.

## Overnight rule (owner, 2026-11-11)
Run builder batches back to back. Before each batch check get_usage: stop launching when the 5-hour window is at 95 percent or more (keep 5 percent free). When idle (no batch left or limit reached), run `shutdown /h` to hibernate the laptop. Next morning: say resume.

## 2026-11-11 night status
Site v2: all 19 pages pass the gate (only waived phone numbers), CSS 27.5 KiB, perf 0 FAIL. Not deployed. Next: owner approves deploy (02_Website/DEPLOY.md), then GTM tags, sitemap, OpenSEO audit. Note: site-v2 CSS files were minified in place; keep originals out of repo, edit with care.
