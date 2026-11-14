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
