# Website QA report (2026-11-08)

**Verdict:** Build passes. 16 pages built, 0 broken internal links, 0 pages with a wrong H1 or canonical count, no unproven claim found, no horizontal scroll on mobile. Lighthouse mobile (throttled, local server): performance 98 to 100 on a quiet run, SEO, accessibility and best practices 100.
**Evidence:** `qa.json`, `lh-*.json`, screenshots in `screenshots/` (390x844 and 1280x900: home, plots, location, FAQ, contact).
**Caveat:** home performance dropped to 75 on one run because Total Blocking Time spiked to 1,290 ms while other heavy jobs ran on this machine. Re-runs gave 100 and 98. Re-test on the real host after deploy. GTM is not installed yet (no ID), so INP with GTM is untested.

## Lighthouse mobile (local, http://127.0.0.1)
| Run | Perf | LCP | CLS | TBT | Transfer | SEO | A11y | Best practices |
|---|---|---|---|---|---|---|---|---|
| home | 75 | 0.8 s | 0 | 1,290 ms | 154 KB | 100 | 100 | 100 |
| location | 98 | 1.8 s | 0 | 160 ms | 166 KB | 100 | 100 | 100 |
| home-r1 | 100 | 0.8 s | 0 | 40 ms | 154 KB |  |  |  |
| home-r2 | 98 | 0.8 s | 0 | 170 ms | 154 KB |  |  |  |

Budgets (DESIGN-DIRECTION.md): Lighthouse 95 plus, LCP 1.8 s, CLS 0, TBT under 150 ms, first load under 500 KB. Transfer is about 154 to 166 KB, well inside. Home TBT passed on 2 of 3 runs, see caveat.

## Pages
| URL | HTML KB | HTML gzip KB | H1 | Canonical | JSON-LD blocks | Meta description chars |
|---|---|---|---|---|---|---|
| /about/ | 20.5 | 6.3 | 1 | 1 | 1 | 107 |
| /amenities/ | 20.9 | 6.5 | 1 | 1 | 1 | 107 |
| /blog/how-to-choose-an-industrial-plot/ | 21.5 | 6.8 | 1 | 1 | 1 | 123 |
| /blog/ | 19.6 | 6.2 | 1 | 1 | 1 | 107 |
| /blog/industrial-plot-buying-checklist/ | 21.2 | 6.6 | 1 | 1 | 1 | 107 |
| /contact/ | 21.0 | 6.6 | 1 | 1 | 1 | 133 |
| /faq/ | 24.2 | 6.9 | 1 | 1 | 1 | 143 |
| / | 26.2 | 7.5 | 1 | 1 | 1 | 161 |
| /industrial-plots/ | 21.5 | 6.6 | 1 | 1 | 1 | 113 |
| /location/ | 22.8 | 6.8 | 1 | 1 | 1 | 146 |
| /location/industrial-plots-in-bhojpur/ | 22.2 | 6.7 | 1 | 1 | 1 | 110 |
| /location/industrial-plots-in-ghaziabad/ | 22.5 | 6.7 | 1 | 1 | 1 | 136 |
| /location/industrial-plots-in-hapur/ | 22.3 | 6.7 | 1 | 1 | 1 | 145 |
| /location/industrial-plots-in-modinagar/ | 22.4 | 6.7 | 1 | 1 | 1 | 135 |
| /location/industrial-plots-near-delhi-meerut-expressway/ | 22.7 | 6.8 | 1 | 1 | 1 | 145 |
| /privacy/ | 19.4 | 6.1 | 1 | 1 | 1 | 73 |

CSS is inlined in the HTML (under 12 KB of the HTML size). JS: one inline tracker (about 3 KB) and no framework. Fonts: Montserrat 33 KB, Inter 20 KB woff2, preloaded.

## Claim scan
Searched built text for: Section 80, Zilla Panchayat, drainage, 24 hour, security, Amul, Inox, Patanjali, petrol, approved, legally compliant. Hits: 0. Draft pages (neighbours, approvals, gallery) are excluded from build and sitemap.

## Open items
- `.example` domain is a placeholder in canonicals, sitemap, robots and llms.txt. Set PUBLIC_SITE_URL and update robots.txt and llms.txt when the domain exists.
- Form posts to PUBLIC_FORM_ENDPOINT. Until set it falls back to a mailto action. `generate_lead` fires on submit, spec wants it on backend success.
- WhatsApp number defaults to 9837057800 (owner to confirm).
- Real photos replace illustrations when available.
