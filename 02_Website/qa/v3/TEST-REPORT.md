# Test report v3 go-live (2026-11-14, integrator)
Build: site-v2 `npm run build` with PUBLIC_SITE_URL=https://isapurindustrialpark.com and PUBLIC_GTM_ID=GTM-KMBRGVSD. 26 pages, 7.8 MB, no dist/assets. Served locally with the production `_headers` applied (gzip server). Old report: TEST-REPORT-prev.md.

| Check | Result |
|---|---|
| Link checker, anchors, one h1 per page (26 pages) | PASS |
| Titles under 60, descriptions under 155 | PASS |
| Canonical and sitemap on https://isapurindustrialpark.com, 25 urls, all new pages in sitemap and footer | PASS |
| robots.txt has no Disallow, llms.txt present | PASS |
| JSON-LD parses on every page | PASS |
| No 92195 49800, 98370 57800, 9219549800, 9837057800, resale, 4.7 / 4.3 / 11.4 / 13.4 km, no em dash | PASS |
| Phones in tel: and wa.me only 98377 64222 / 919837764222 | PASS |
| Images WEBP (share.jpg only for social card) | PASS |
| One sticky Call/WhatsApp bar per page (home in index.astro, inner in Inner.astro) | PASS |
| Consent banner stacks directly above the sticky bar on phones (banner bottom = bar top), buttons 44 px high | PASS (fixed: pad recomputed on load) |
| Footer legal links reachable while banner is open (body margin = banner height) | PASS (fixed) |
| GTM request absent before choice, present after Accept (360 and 1440, home, plot-maps, contact, privacy) | PASS |
| Console errors and CSP violations at 360x800 and 1440 (home, plot-maps, contact, privacy) | PASS (none) |
| Horizontal scroll at 360 | PASS |
| CLS | PASS (0 on all four) |
| Lighthouse mobile, home | FAIL on target: performance 87 to 89 (a11y 100, best practices 100, SEO 100), TBT about 440 ms, LCP 1.5 to 1.8 s. Same score without GTM and banner, so not caused by them. Style and layout 1.4 s under 4x CPU. Helper measured 93 to 100 earlier on a quieter machine; rerun on the live URL. |
| Lighthouse mobile, location page | PASS 98 / 100 / 100 / 100 |
| Lighthouse mobile, plot-maps | PASS 96 / 100 / 100 / 100 |
| Lighthouse mobile, contact | PASS 98 / 100 / 100 / 100 |
| Road labels on plot maps: contrast | FIXED (dark halo on white text, plotmaps.css `.rl`) |
| Road label tilt (rotate -52, -90) | KNOWN GAP, readable, left as drawn |
| Form WhatsApp hand-off | Not browser-submitted by integrator (wa.me link and form-action allowlist verified in markup and CSP) |
| Vale | NOT RUN (vale not installed here). Helper ran it on privacy and terms. |
