# Go-live state (updated 2026-11-14, resume from here if a session dies)

Owner order: finish the website and go live today. Mobile first. Do not exhaust limits: every helper checkpoints its own notes.

## Helpers started 2026-11-14 (check their notes, not the chat)
- Home (stage 6 layout, mobile-first, speed, remove public/assets): notes in 02_Website/V3-HOME.md, build folder dist-home.
- Inner pages (mobile-first audit and fixes): notes in 02_Website/V3-SITE.md, build folder dist-inner.
- Compliance and security (privacy page, consent, analytics choice, headers, security tool review): notes in 02_Website/research/legal-privacy-security.md, build folder dist-legal.

## After the three finish (do in order)
1. Merge check: one clean `npm run build` of site-v2 (dist), run link checker, grep for 92195 49800, 98370 57800, resale; Lighthouse mobile on home and two inner pages.
2. Run 02_Website/previews/deploy.ps1 (preview refresh), look at the previews on a phone-size viewport.
3. Create the production Pages project iip-site, deploy dist (production headers, no noindex), attach isapurindustrialpark.com and www via the Cloudflare MCP, set DNS (apex and www CNAME to the Pages project), keep the .in redirect rule and www redirect, set PUBLIC_SITE_URL and PUBLIC_GTM_ID in the Pages project.
4. Verify live: 200, https, headers, sitemap, robots (no Disallow), canonical, GTM after consent, no console errors; submit sitemap in Search Console; Bing and IndexNow if time.
5. Update board, TODOS, CHANGELOG, knowledge file, TECH-STACK; commit and push with the owner's own authorship (no co-author lines).

## Still open
CTA redo for print (kit publish blocked), kit additions (ink drawing style, yellow bullet), Blender film (on hold), Business Profile reads and edits, gate position, owner facts.

## Integrator log
- Step 1 merge check: one actionbar per page (home in index.astro, inner in Inner.astro), Consent included once in Home.astro (Inner wraps Home), Gtm in Home head, Foot shared with Privacy, Terms, Cookie settings, public/_headers is production, robots.txt.ts has no Disallow. Base.astro is dead code. dist-q is TRACKED in git (1818 files): not deleted.
- Step 2 clean build OK (26 pages, 7.8M, no dist/assets). dist-home, dist-inner, dist-legal removed (untracked). dist-q kept (tracked).
- Step 3 partial: static checks PASS (links, h1, titles, desc, canonical, jsonld, banned strings, phones, robots, sitemap 25). Lighthouse mobile: home 87-89 perf (a11y/bp/seo 100), location 98, plot-maps 96, contact 98, CLS 0. Home below 90 on this machine (banner and GTM not the cause; style/layout 1.4s under 4x CPU).
- Step 3 done, report at 02_Website/qa/v3/TEST-REPORT.md. Consent banner fixed (stack above bar, body margin), road label halo added.
- Step 4 preview v3 refreshed (iipreview-v3, noindex, 200). previews/dist is partly locked by a process (package.mjs rm fails EPERM; nav, v1, kit local dist gone, regenerate with package.mjs after reboot or unlock). Step 5: Pages project iip-site created.
- Step 5 DONE: https://iip-site.pages.dev/ deployed (deployment be717896), 200, CSP and HSTS present, no X-Robots-Tag, robots Allow, home h1 1, built with GTM-KMBRGVSD and https://isapurindustrialpark.com. Custom domain and DNS NOT touched (lead does).

## Integrator report (2026-11-14)
PASS: merge check, clean build, static tests, banner and sticky bar, GTM consent gate, no console or CSP errors, preview, production package.
FAIL on target: Lighthouse mobile home 87 to 89 (target 90); location 98, plot-maps 96, contact 98; a11y, BP, SEO 100 everywhere; CLS 0.
Gaps: Vale not run, form submit not browser-tested, road label tilt on plot maps, dist-q (tracked) kept, previews/dist locked (rerun package.mjs for nav, v1, kit before next full preview deploy), Base.astro dead code.
Changes this pass: Consent.astro (banner pad after load, body margin so footer stays reachable), plotmaps.css road label halo. Uncommitted.
Blocks go-live: nothing hard. Lead attaches domain and DNS.

## LIVE 2026-11-14
Production project iip-site, domain isapurindustrialpark.com attached, DNS CNAME @ added. www and .in redirect to the .com. Verified 200, HSTS, CSP, robots Allow, canonical, sitemap 200. Source committed (0f940619). Remaining: Search Console sitemap submit (owner), Cloudflare Web Analytics toggle, Business Profile website links, Bing import, print CTA redo, kit publish.
