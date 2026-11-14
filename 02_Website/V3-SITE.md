# V3 inner pages (2026-11-13): the locked home design language rolled out to every inner page

Not committed, not deployed. Home is the reference. Design language untouched (`DESIGN-LANGUAGE.md`).

## What changed
- **Layout**: `src/layouts/Inner.astro` wraps `Home.astro` (extended with optional props: pageType, crumbs, faq, article, noindex, place, css, nav aria-current). Same header with the large logo mark, flag stripe bar, Erode and Inter, buttons, footer. `Base.astro`, `place.css` and the old system assets are no longer used by any page (left on disk, not deleted).
- **Shared parts**: `components/Foot.astro` (footer, used by home too, adds Plot maps and Approvals links, plus on inner pages a closing strip with Call 98377 64222 and WhatsApp), `components/WhereMap.astro` (the road map, extracted from home, hero of location pages), `components/Sheet.astro` (ink drawing: truck on the 50 ft RCC road, street light, tree, for pages with no drawing of their own). Heroes reuse `Vig` (gate, papers) and the home map.
- **Hero drawing per page**: location and 5 town pages: road map. Amenities, around us: gate and fuel pump. Plots, approvals: layout sheet with the stamp. FAQ, contact, about, guides, 404, privacy: truck sheet. Plot maps: none (the map is the page).
- **Sections**: every `##` is one section, heading in columns 1 to 5, text in 6 to 12 (stacked under 1024). `src/lib/inner.mjs` turns ordered lists into the home sunburst steps. Styles in `src/styles/inner.css` (about 4 KB raw). FAQ uses the home accordion. Motion: only what home.mjs and CSS already do (flag bar fills with scroll, map route draw, press and hover feedback). Nothing new animates, so reduced motion is respected.
- **New /approvals/**: only the safe wording of `06_Content/approvals-facts.md`, plain explainer per phase, no images, no personal data, links to contact and plot maps. Judgement call for the owner: "Phase 1 (extension)" is written "Phase 1" (the extension is never shown separately); the 14 conditions and the drainage lanes are not mentioned.
- **New /plot-maps/**: the three finished maps (`01_Brand/Plot-Maps/svg/phase1-3.svg`, status done) inline, optimised by `scripts/build_plotmaps.py` (style block moved to CSS, hover titles to `data-a`, repeated points dropped, drain shapes and legend entry removed, legend rebuilt as HTML, viewBox cropped above the legend, group ids prefixed). 25 KB gz for all three, page 41 KB gz. Phase 1, 2, 3 switch (without script all three show stacked), hover or tap for "Plot N, about X sq yd" (sizes only for plots of 285 sq yd or more, shops show "Shop N"), legend, "Plots run from 300 sq yards upward", no extension label. On phones the map scrolls sideways at a readable size. Linked from the nav (Plot maps), the footer and the home hero (new "See every plot on the plot maps" link). Home papers link now goes to /approvals/ (was /contact/). Sizes are drawing figures: confirm with the owner before print use.
- `llms.txt` no longer says "contact for price" and lists the two new pages. Sitemap and canonicals use https://isapurindustrialpark.com (checked in dist), both new pages are in the sitemap.

## Copy lines changed (before, now)
- Everywhere: removed all "Contact for price" and rates lines (plots page, FAQ, 5 town pages, llms.txt) and "Call us for the current plot list and rates".
- Everywhere: removed straight-line figures (3.9, 4.3, 9.3, 13.0 km), "How we measured ... Plan on a test drive", "Times change with traffic. Tolls apply". One caption stays under distance tables: "By road, measured on Google Maps, 6 November 2026."
- Removed: "What this page does not claim about plots" (amenities); "This is a general guide, not legal advice" (guide); the water, drainage, permitted use and documents FAQ answers; "We do not publish these details here".
- Location lead: now "The park is on the Hapur-Modinagar Road at Yusufpur Isapur... on-ramp at Bhojpur is 4.7 km by road, about 8 minutes."
- Contact: "Before you come" now starts "Bring the truck you run. We show you the turn into your plot." Form note adds the privacy link.
- About: "We say what is on site today, and mark the rest as coming only when we have confirmed it" now "We tell you what is for sale today and we give distances by road." Buyers: warehouse and godown owners, investors.
- Amenities: lead adds power 24/7; new sections Power 24/7, A petrol pump at the gate, Shops inside the park.
- Plots: lead now "Call us and we find a plot that suits your needs." Sizes table is 3 rows (300, 500 to 1000, 2000 to 2500 sq yards). Buying steps are the home five steps.
- Around us (was INOX Air, Namaste India, straight-line distances): now the four running units, the IndianOil pump at the entry and exit, shops. Description rewritten (brand names out). Lead now "Factories already run close to the park, and an IndianOil petrol pump sits at its entry and exit."
- FAQ: rewritten to 21 answers (sizes, available today, who for, shops, how to buy, papers, payment, WhatsApp list, roads, trucks, lights, greenery, power, pump, where, expressway, Modinagar and Hapur, Meerut and Delhi, visit, what to look at, contact). Description lost "price" and "documents to check". Payment: "Payments run for about three months on average."
- Town pages: leads trimmed to one fact each, "short answer" stubs dropped, "Inside the park" and "Plots" blocks include power 24/7, pump and a plot maps link. Bhojpur description: "4.3 km straight-line to the Bhojpur expressway exit" now "4.7 km by road to the Delhi-Meerut Expressway on-ramp at Bhojpur" (4 km rule). Ghaziabad lead lost the 34.7 km sentence (still in the table and description).
- Guides: rewritten without water, drainage, permitted use or disclaimers, with a lead line each and links to approvals and plot maps. Industrial-areas guide lost "land price" and the Google Maps aside.
- 404: "Page not found, see the industrial plots" now "That page is not here, but the plots are".
- Approvals and plot maps: new.
- Not touched: home copy (except two links) and SEO titles.

## QA
- Build: 21 pages. Playwright at 1440 and 390 for location, town, FAQ, contact, approvals, plot maps, blog index, post, plots, amenities, around us, about, privacy, 404 (`scripts/shots_inner.py`, `qa/v3/screens/v3inner-*.png`): CLS 0 on all 28 runs, no horizontal overflow, no console errors. Looked at location, plots, contact, plot maps, 404. Fixed full width sections, the phone map size and the truck sheet spill.
- Grep of dist html: no 92195 49800, no 98370 57800, no "resale", no INOX or Namaste, no Section 80, one h1 per page. Home still has "rain water harvesting" and one "4.3 km" line (home was not changed this round, decide with the owner). "Water tanks" stays as a product name on Around us (same as home).
- Taste gate (`scripts/qall.sh`, output `qa/v3/qall-inner.txt`, about 2 min a page): FAQ at 1440 gave 37 FAIL, all in the families the home waivers already cover plus the new layout: section-height, one-section, one-heading, split-pair, container-edges (skip link, nav bar, footer strip), hero-screen, text-only and hero-fill (no photographs by the owner rule, drawings instead), same-action and button-styles (Call and WhatsApp repeat in header, hero and closing strip), phone-number, effect-kind, cta, section-tile, section-air. Proposed waivers: those families per page, no content waivers. The run was not finished for every page when this was written, so per page counts are open.

## Open
Owner: confirm the "help you sell your land" and "payments through us" step lines, the "Phase 1" wording and the drawing figures on the plot maps. Optional cleanup: delete `Base.astro`, `place.css`, `src/scripts/home.js`.

# Mobile first pass on the inner pages (2026-11-14)
Not committed, not deployed. Built to `site-v2/dist-inner` (own folder), served on 4331 to 4340.

## What changed
- `src/styles/inner.css` rewritten true mobile first: base is 360 px, then `min-width:768` and `min-width:1024` (hero and sections go to the 12 column grid only at 1024). `src/assets/plotmaps/viewer.css` rewritten the same way.
- Breadcrumbs: 44 px tap rows, 15 px. Eyebrow 13 px. Footer legal links 44 px wide. Form labels 16 px, inputs 56 px high at 18 px (no iOS zoom), note text darkened to pass 7:1. Prose links get vertical padding for the thumb.
- Distance tables and the plot size table: stacked rows on phones (place on its own line, km and minutes under it, header kept for screen readers), real table from 768.
- Contact form: fields stack, full width button, `type=tel inputmode=tel`, date input native. Bar hides while a field has focus.
- Sticky Call and WhatsApp bar: markup in `Inner.astro` (class `actionbar`), CSS, 640 px breakpoint and the `--bar` body space come from `home.css` (home helper). Consent.astro already measures `.actionbar`. WATCH: if the home helper adds the same bar to `Home.astro`, delete the one in `Inner.astro`, or inner pages show two.
- Plot maps: page order on phones is phase chips (one row, scrolls sideways, 48 px), map, zoom minus and plus (48 px, 1x to 3x, drag to move, pinch and double tap still work, `touch-action: pan-x pan-y pinch-zoom`), legend as a collapsible (closed on phones, open on desktop), ask button. Tap a plot for its number and size. Without script all three maps still show stacked. Desktop: map left, controls right.
- Map hero tabs on location pages 44 px, visible focus ring on the map pins (`.ih .wr__p:focus-visible`).
- New pages found in the build and covered by the same CSS: terms.

## Checks (all on dist-inner)
- `scripts/audit_inner.py`: 26 pages x 360, 390, 412, 768, 1440. Horizontal scroll: none. Images without width and height: none. Remaining items: text 15 px or 13 px in breadcrumb, footer legal links and eyebrow (labels, waived), consent banner buttons (Consent.astro, compliance helper: min-height 44 is in its CSS, the audit measured 21 px, recheck on the live build with PUBLIC_GTM_ID).
- `scripts/check_inner.mjs`: 26 pages, 0 failures (one h1 each, internal links and anchors resolve, no 92195 49800, no 98370 57800, no resale, every img sized and not png or jpg).
- `scripts/shots_inner_final.py`: `qa/v3/screens/v3final-inner-<page>-360.png` and `-1440.png` for every page, CLS 0 on all 50 runs, no overflow. Looked at location, contact, faq, plot maps (360), plus `v3final-inner-plotmaps-zoom-360.png` and the faq hero at 390. Zoom, phase switch and legend tested by script, no page errors.
- Lighthouse mobile (default simulated 4G, `qa/v3/lh/inner-*.json`): location perf 100 / a11y 100 / best practices 100 / SEO 100 (LCP 1.2 s, CLS 0.025); faq 100/100/100/100 (LCP 1.2 s, CLS 0); plot maps 98/100/100/100 (LCP 1.6 s, CLS 0.004, TBT 140 ms). Before: only old runs exist (`qa/v3/lh-plots.json` 100/100/100/SEO 69, home 72/100/100/69, SEO low then because of local noindex and robots); the new build has no inner page under 98.
- Taste gate: `scripts/qall_inner.sh` (q.sh on dist-inner), output `qa/v3/qall-inner-final.txt`, one page per type: location, faq, contact, plot maps, guide, 404, plots, privacy, guides index, amenities.

## Taste gate waivers (inner pages)
Same families as the home waivers, plus layout facts of compact inner pages. No content waivers.
- Desktop rhythm: section-height, one-section, one-heading, split-pair, hero-screen, section-air, section-tile, container-edges, off-grid (skip link, nav, footer strip). Inner pages are reference pages of 2 to 5 short sections, not one screen each.
- Drawings not photos (owner rule until the photo direction): hero-fill, text-only, no-visual, visual-caption (the OpenStreetMap credit must stay).
- Call and WhatsApp repeat in header, hero, sticky bar and closing strip on purpose: same-action, button-styles, phone-number, cta.
- effect-kind: scroll linked flag bar from the home layout.
- spill: the sunburst `burst` is a clipped corner decoration inside the panel, the drawing itself fits (checked in `v3final-inner-faq-hero-390.png`).
- Not mine, passed to the owners: consent banner (`collide`, `nav-covers`, `focus-hidden`: covers the last footer links until the visitor chooses, dismissable, Consent.astro), road map labels (`tilt`, `contrast`, `cut-text`, `overlap-text`: WhereRegion and home.css, home helper).
- Fixed in this pass: focus ring on map pins, note text contrast on the contact panel, 44 px taps.
