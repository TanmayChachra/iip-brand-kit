# v3 test report (2026-11-13)

Build: `npm run build` in `02_Website/site-v2`, 25 pages. Link/SEO checker: `02_Website/qa/v3/check.mjs` (output `check-out.json`). Lighthouse JSON: `lh-home.json`, `lh-plots.json`.

| Check | Result |
|---|---|
| Build, no errors | PASS |
| New pages wired (footer, llms.txt, in-body links, sitemap) | PASS (fixed: footer, llms.txt, plots, amenities, approvals links added) |
| All internal links resolve (25 pages) | PASS |
| One h1 per page | PASS |
| Titles unique and under 60 | PASS (fixed: home title was 63) |
| Descriptions unique and under 155 | PASS (fixed: layout-approvals was 159) |
| Canonical and sitemap use https://isapurindustrialpark.com | PASS |
| robots.txt, llms.txt present | PASS |
| JSON-LD parses; types LocalBusiness, WebSite, WebPage, Place, BreadcrumbList, Article, FAQPage; no rating, offer, review or award | PASS |
| Images WEBP | PASS (only PNG icons, favicon and share.jpg for social cards remain) |
| 404 page (404.html, one h1, served as 404 on Cloudflare) | PASS |
| Phones only 98377 64222; no 92195 49800, 98370 57800, 9219549800, 9837057800, "resale" | PASS |
| Old distance figures (3.9, 9.3, 13.0 km) absent | PASS |
| GTM id once per page | PASS |
| Console errors home, faq, shops, roads-and-freight | PASS (none) |
| CLS | PASS (0 home and plots) |
| Lighthouse mobile, plots: perf 100, a11y 100, best practices 100 | PASS |
| Lighthouse mobile, home: perf 72, a11y 100, best practices 100, LCP 1.4 s, CLS 0 | FAIL (TBT 2.1 s: 3.7 s main-thread style and layout in the home document under 4x CPU throttle, from the large inline SVG story. Design level, not fixed) |
| Lighthouse SEO 69 on previews | EXPECTED (is-crawlable fails by design: noindex header and Disallow on previews only) |
| Vale on how-buying-works, roads-and-freight, shops, layout-approvals, faq | PASS (0 errors, warnings, suggestions) |

Findings for the owner:
- `site-v2/public/assets` (36 MB, taste toolkit demos with 124 HTML pages) is copied into every production build. Packaging skips it. Before go-live, move it out of `public/` or exclude it, otherwise it ships to the public site.
- Home TBT, see above.

## Deployment checks (previews)
All four URLs return HTTP 200 with `X-Robots-Tag: noindex, nofollow, noarchive`, each home has one h1. See `02_Website/previews/LINKS.md`.
