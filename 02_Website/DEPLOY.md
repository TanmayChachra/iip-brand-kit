# Deploy: Cloudflare Pages (owner account)

Not executed yet. Each step needs the owner's yes. Site: `02_Website/site-v2` (Astro, static).

## 0. Before
- Everything to deploy is committed and pushed to GitHub `main` first.
- Local check: `cd 02_Website/site-v2 && npm ci && npm run build` gives `dist/` with 19 pages.

## 1. Create the project
Cloudflare dashboard, Workers & Pages, Create, Pages, Connect to Git.
1. Pick repo `TanmayChachra/iip-brand-kit` (branch `main`). Authorise only that repo.
2. Project name: `iip-site` (gives `iip-site.pages.dev`).
3. Framework preset: Astro (or None, same settings).
4. Root directory: `02_Website/site-v2`
5. Build command: `npm run build`
6. Build output directory: `dist`
7. Environment variable `NODE_VERSION` = `22.23.4` (package.json engines needs 22.23.4 or newer, `24` also works).
   Alternative: file `.node-version` in `site-v2`.

## 2. Environment variables (Production and Preview)
None is a secret.

| Name | Value |
|---|---|
| `PUBLIC_SITE_URL` | `https://isapurindustrialpark.com` |
| `PUBLIC_GTM_ID` | `GTM-KMBRGVSD` |
| `PUBLIC_WHATSAPP` | `919837764222` (digits, country code, no plus) |

Optional: `PUBLIC_FORM_ENDPOINT` (form backend URL). Unset means the form hands the request to WhatsApp.
These are read at build time, so changing one needs a new deployment.

## 3. First build and check
Save and Deploy. Open `https://iip-site.pages.dev`. Check: home loads, `/sitemap-index.xml` and `/robots.txt` show `isapurindustrialpark.com`, canonical in page source is the .com, GTM loads (Tag Assistant), `_headers` applied (`curl -I` shows `X-Content-Type-Options: nosniff`).
While on `pages.dev` the canonical points at the .com, which is correct for launch.

## 4. Custom domain isapurindustrialpark.com
Zone `isapurindustrialpark.com` is already in the owner's Cloudflare account.
1. Pages project `iip-site`, Custom domains, Set up a custom domain, enter `isapurindustrialpark.com`.
2. Cloudflare adds the apex record itself because the zone is on the same account: `CNAME  @  iip-site.pages.dev`, proxied (orange cloud, CNAME flattening). Confirm in DNS, Records. If it is missing, add exactly that.
3. Wait for status Active and the certificate to issue (a few minutes).
4. Add `www.isapurindustrialpark.com` the same way (record `CNAME www iip-site.pages.dev`, proxied), then a Redirect Rule: www to apex, 301, so one host is canonical.
5. Do not touch the existing MX and TXT records (Email Routing, verification).
6. The `.in` domain (if used) gets a 301 Redirect Rule to the .com apex, path preserved.

## 5. After live
- Search Console: add the domain property, submit `https://isapurindustrialpark.com/sitemap-index.xml`. Bing Webmaster the same.
- GA4 and GTM: Preview mode on the live URL, confirm `page_view` and the CTA events from `04_Analytics/event-spec.md`.
- Update `00_ISAPUR_KNOWLEDGE.md` change log, `TODOS.md`, `CHANGELOG.md`, `_ops/TECH-STACK.md` (hosting row Active), `_ops/status.json`.

## Rollback
Pages project, Deployments, pick the previous good one, Rollback to this deployment. Removing the custom domain does not delete the zone.

## Private previews (done 2026-11-13)
Pages projects `iipreview-nav`, `iipreview-v3`, `iipreview-v1`, `iipreview-kit` (direct upload, no git), all noindex. Links in `02_Website/previews/LINKS.md`, start at https://iipreview-nav.pages.dev/.
- Redeploy everything: `npx wrangler login` once (browser), then `powershell -File 02_Website/previews/deploy.ps1`. It builds v3 and v1, runs `previews/package.mjs` (adds noindex `_headers` and `Disallow: /` robots, skips `public/assets` and the 59 MB brand book PDF), uploads, checks HTTP and headers, and rewrites LINKS.md.
- Never put a token in a file. For automation the owner sets `CLOUDFLARE_API_TOKEN` in the environment.
- The preview robots and headers exist only under `previews/dist`. The production build is unchanged.

## Go live (needs the owner's yes, not done)
1. Make sure `public/assets` (design toolkit, 36 MB) is not in the production build.
2. Create the production project (section 1) or, for direct upload: `npx wrangler pages deploy 02_Website/site-v2/dist --project-name iip-site --branch main` after building with `PUBLIC_SITE_URL=https://isapurindustrialpark.com` and `PUBLIC_GTM_ID=GTM-KMBRGVSD` set in the shell.
3. Attach the domain (section 4): Custom domains, `isapurindustrialpark.com`, then `www` with a 301 Redirect Rule to the apex, and the `.in` domain 301 to the .com.
4. Check with curl: 200, no `X-Robots-Tag: noindex`, canonical is the .com, `/robots.txt` allows crawling, sitemap loads.
5. Search Console and Bing: submit `/sitemap-index.xml`.
6. Rollback: Pages project, Deployments, previous good one, Rollback. Removing the custom domain does not touch the zone.

## Compliance and security headers (added 2026-11-14)
- Research and verdicts: `02_Website/research/legal-privacy-security.md`.
- Consent: `src/components/Gtm.astro` (head) sets Google Consent Mode v2 defaults to denied and requests GTM only after the visitor accepts (choice in localStorage `iip-consent`, 6 month expiry). `src/components/Consent.astro` is the banner, included once in `layouts/Home.astro` (Inner uses it). Footer has Terms and Cookie settings. Pages `/privacy/` and `/terms/` live in `src/content/pages/`.
- Tested in the browser: no GTM request before a choice or after Reject, GTM loads after Accept.
- `public/_headers` is the production file: CSP (script and style allow `'unsafe-inline'` because Astro inlines CSS and the pages carry inline scripts; per-page hashes are not practical in one static file), HSTS, nosniff, X-Frame-Options, Referrer-Policy, Permissions-Policy, long cache on `/fonts`, `/img`, `/brand`, `/_astro`. No Cache-Control on `/*` on purpose (Pages merges matching rules and would duplicate it). The CSP allows GTM, GA4, Cloudflare Web Analytics and Clarity hosts. If `PUBLIC_FORM_ENDPOINT` is set, add its origin to `form-action` and `connect-src`.
- Previews keep their own noindex headers from `previews/package.mjs`; they do not use this file.
- After go-live: `curl -I https://isapurindustrialpark.com/` shows `content-security-policy` and `strict-transport-security`; grade it on securityheaders.com and the MDN HTTP Observatory; open home, one inner page and `/plot-maps/` with the console open, expect no CSP errors after Accept.
- Owner steps: enable Web Analytics in the Pages project (cookieless counts, no banner needed). Add Clarity in GTM only later, per `04_Analytics/gtm-plan.md`.
- Lawyer items: RERA applicability, DPDP reading, jurisdiction line in `/terms/`.
