# v3 build progress (site-v2, taste-skill 2.5.1)

Plan line 1: kind = place (page type place, site-kind other). Main action: Book a site visit.
Plan line 2 (the deal): nav plain words (nav-cards dealt, no panel photographs since stand-ins would be a second photo layer), footer-columns, colour-band close (.ground-brand = brand green #0F4D3A), buttons arrow, offer composition strip (3 groups + 4 detail photographs), place composition wall (re-dealt, strip equalled the offer), type moment address, moment picture-develops on the visit photograph, rooms layout not used. Palette: client's own colours via start.mjs brand (bg #f3f5ef, ink #10231b, accent brand green #0f4d3a, surface #e3ece2). Type: Work Sans (skill's trade pairing, self-hosted subset). The skill bans Montserrat for pages and the owner rejected the v1 Montserrat 800 look; the logo SVG keeps the kit wordmark.
Voice card: plain business, short facts, no figures of speech. Fact sheet: only claims allowed in DESIGN-DIRECTION.md.

Screens: hero, visit (type moment + panel + shed photo), plots (3 groups + strip), around (wall of 6), book (form), footer.closing.

## Steps done
- [x] 0 stack: site-v2 from v1 plumbing, kit copied to public/assets, Work Sans self hosted, npm install ok.
- [x] 1 gate armed on dist/index.html.
- [x] 2-5 copy and build: Base layout, home (6 screens), inner template, blog, 404, form component.
- [ ] 6 checks and fixes
- [ ] map (other fork), Impeccable critique, web-design-guidelines audit, screenshots, report

## Update (home gate)
- Home page: GATE: PASS (round 2 of 3), 3 waivers (2 phone-number for the client's real numbers, 1 one-section for the address type moment), 15 WARN.
- Fixes done: photos pre-cropped to display ratios (scripts/process_photos.py), picture hero with 4:5 phone crop, group headings with nouns, type moment resized, phone grid gaps, booking head, address link.
- Next: full consistency, check.mjs 5 sizes, perf.mjs, inner pages, map, Impeccable and guidelines audits, screenshots, report.

## Update 2 (audit fixes, coordinator override)
- Kit type back: Montserrat 800 display (tight tracking) and Inter body, self-hosted (the skill bans both; owner and brand kit win, hero-lines waived).
- Yellow: flag under the header and on top of the closing band (public/brand/flag.svg), h1 yellow bar, yellow button on the green band, yellow primary on hover, yellow selection colour.
- Photos replaced: 12 Unsplash stand-ins that read as India (trucks, roads, factory belt, palm verges) plus 2 Wikimedia Commons Delhi-Meerut Expressway photographs (Pinakpani, CC BY-SA 4.0). Credits in credits.json and the one footer line. No AI imagery.
- OSM map on the home around section (tile), location page and the 5 landing pages (tall crop on tablet and phone).
- Form: no mailto. Hands the request to WhatsApp (wa.me from phones.mjs, typed details), PUBLIC_FORM_ENDPOINT used when set; plot size select, day date field.
- Raw markdown on contact and FAQ fixed, orphan headings fixed (break-after avoid), visit panel stacked, closing button no longer a bar, logo background tile removed (no change to the artwork), titles under 60, address type moment smaller than the h1.
- Gate home: PASS (4 waivers: phone-number x2, one-section, hero-lines).
- Open: full consistency at tablet and phone, inner pages, guidelines re-audit, screenshots, report.
Update 3: gate PASS on home; stale photo keys fixed on inner pages, blog, 404; screenshots regenerated; report.md written.

## Update 4 (coordinator round 3: every page to GATE)
- Inner pages rebuilt on one template: `src/lib/sections.mjs` splits each page's Markdown at its h2s and groups them into 1 to 5 sections (one h2 each, text left, stand-in photo or the OSM map right, never flipped). FAQ: 20 short plain answers, 5 sections of 4. Phone numbers removed from prose (footer, action bar and contact page carry them).
- Headings reworded to name plots, place or section (copy-headings). Folded headings are bold run-in lines, not h3.
- Heading scale: h1 80px, h2 52px, numerals 52px at 1440 (42 / 28 / 28 at 390). Set through `--t-h1` on the hero and `--t-h2` on :root.
- Photo set cut to one cohesive daylight tone: expressway-a, expressway-b, road-green, sheds-blue, factory-yard, verge-palms, jcb-lowbed, street-light (amenities only). Removed: cyan aerial, amber dusk, teal road-india, goods truck.
- Checks run per page with `scripts/q.sh` and `scripts/qall.sh` on a copy of dist (`dist-q`), one at a time.
- 2026-11-10 resumed: neighbours phase mentions removed; robots.txt and llms.txt now generated from PUBLIC_SITE_URL and phones.mjs; guide page /industrial-areas-in-ghaziabad/ added; home and plots titles retargeted.
- 2026-11-10 round: quick consistency on all inner pages; remaining FAILs were section-height by 1 to 30 px (threshold for two-screen sections now 170 words), tap size of lone prose links (44 px), phone-number waivers for the contact page text (98370 57800, 98377 64222) in scripts/waivers.default.json; mobile photos kept (hiding them failed no-visual), shorter ratio 2.4 instead.

## Update 5 (2026-11-11, batch 1)
- Domain: astro.config.mjs read process.env only, so .env was ignored and canonicals, sitemap, robots and llms.txt said isapurindustrialpark.example. Now uses vite loadEnv for PUBLIC_*. Build OK (19 pages); canonical x19, sitemap, robots Sitemap line, llms.txt all https://isapurindustrialpark.com. GTM id present in built pages. Only dist/assets/starter.html (template asset, not a page) holds a placeholder domain.
- Gate (scripts/q.sh via qall.sh on dist-q, one page at a time, 1440 and 390): all 18 inner pages PASS: faq, contact, neighbours, blog, blog/how-to-choose-an-industrial-plot, blog/industrial-plot-buying-checklist, 404, location, 5 location landings, industrial-plots, amenities, about, privacy, industrial-areas-in-ghaziabad. Only remaining FAILs are the 2 phone-number waivers (98370 57800, 98377 64222, client's real numbers).
- Fixes: section heights now from content weight (was forced to 2 screens on pages with a distance table, 50 to 69% empty); distance table on phone is 2 lines per row (hole fixed); last-section weight counts the table, Bhojpur split into 2 sections; Ghaziabad duplicate distance table merged into the one table; how-to blog grouped in 2 sections and trimmed; lone "Plot sizes" link merged into its sentence on 3 landings (sat under the phone action bar); footer links no colour fade (checker read hover fade as scroll reveal); dead IntersectionObserver in track.js replaced by a scroll check (no data-view nodes exist yet).
- Still FAIL: none beyond the waivers. WARNs remain (nav toggle size, photo-set, photo-credit, section-height on phone).
- Not run: home gate, check.mjs 5 sizes, perf.mjs.
- Next batch: deploy to Cloudflare Pages, Impeccable audit, screenshots, home regate, verify GTM/GA4 fire, event-spec data-view if needed.

## Update 6 (2026-11-11, batch 2)
- Home gate (q.sh): PASS except the 2 phone-number waivers. Fixed: map h2 vs numerals scale (numerals now 0.55 x h2, which also cleared one-heading), map split off the page's pair lines (removed the 5/7 override, now 6/6), 390 hero ends at 844 (photo 380px), plots section within 2 screens on phone (row height 48px, group gap).
- check.mjs 5 sizes (reports in qa/v3/screens): 1440, 820, 768 no findings. 1024: neighbour (hero edge shows 48px of #visit, WARN level). 390: only hero-lines (stress h1 of 46 chars takes 4 lines; real h1 is waived in waivers.json).
- perf.mjs: 0 FAIL, 4 WARN. 485 KiB at 390 (budget 500). CLS 0, LCP 180 ms CPU-relative. JS 170 KiB gz counted is mostly GTM/GA (loaded live); own JS is system 12.3 + motion 8.4 + layout 5.4 + backgrounds 3.8 = about 30 KiB gz, under 60. CSS 64 KiB on the wire is over the 30 KiB budget (6 files, mostly skill system.css and motion/layout css): OPEN, needs a purge pass. WARN: logo-horizontal.svg below-fold not lazy (it is the footer logo copy).
- Placeholder domain: only public/assets/starter.html (untracked-by-source skill template copy, example mailto). Removed from public (deleted tracked file, not staged or committed). Nothing in src carries a placeholder domain.
- Accessibility review (web-design-guidelines by hand on home, inner page, contact form): form now has aria-label, labels, autocomplete, inputmode, role=status line, skip link, aria-current, lang, 44px nav toggle already OK. No other blocking issue found. Not checked: screen reader run, colour contrast tool.
- Impeccable critique, 5 biggest problems (screens/home-d.webp, home-m.webp): 1) big empty bands between sections at 1440 (sections held to a screen by the gate rule). 2) hero photo is a thin strip, h1 sits under it, weak first impression. 3) plots h2 sits tight on the group labels (fix tried: gap +16px, section-height FAIL at 1440, reverted). 4) route map is pale, labels tiny. 5) "Book a site visit" appears in header, book section and closing band. Fixed this batch: top 3 only partly (see gate fixes: numerals, map split and ratio 0.8); problems 1 to 3 remain a design choice conflicting with the gate, needs owner call.
- Next batch (deploy prep only, deploy needs owner approval): CSS purge to 30 KiB; drop unused skill demo files from public/assets (demo.html, check.mjs, hero-*.html, _hover-test.html); confirm PUBLIC_* env in Cloudflare Pages build; verify _headers and _redirects; GTM and GA4 live check after deploy; regate all pages with qall.sh.

## Update 7 (2026-11-11, batch 3)
- CSS cut: all 7 stylesheets (system, cards, motion, backgrounds, layout, moment, place) comments stripped, minified and shorthand-merged with lightningcss in place, then PurgeCSS pass (pages plus loaded JS as content). Raw 258 KB to 137 KB, gzip on the wire about 66 KiB to 29.4 KiB (budget 30). PurgeCSS alone removed little (JS lists most class names); the gain is comments and minify. Look unchanged by design (same rules). Further purge without JS tokens would save about 1.5 KiB gz but risks dynamic classes: not done.
- Home gate (q.sh /): same result as before, only the 2 phone-number waivers at 1440, 390 clean. qall.sh over 18 inner pages: output in qa/v3/qall-batch3.txt (only waived phone-number FAILs expected, see final tally below).
- 02_Website/DEPLOY.md written: Cloudflare Pages project iip-site, root 02_Website/site-v2, npm run build, dist, Node 22.23.4, env vars, custom domain .com apex. Nothing executed.
- Note: the minified CSS in public/assets and src/styles is now the source of truth, originals (with skill comments) are in the skill folder if needed.
- Final tally: qall.sh 17 pages, each only the 2 waived phone-number FAILs (390 clean), no new FAIL. perf.mjs home: 0 FAIL, 4 WARN, CSS 27.5 KiB gz (PASS, 6 files), total 466 KiB. Not done: DEPLOY.md steps not executed.
