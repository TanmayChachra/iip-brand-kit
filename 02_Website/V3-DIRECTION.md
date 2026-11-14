# Website v3 direction: research and three concepts (2026-11-12)

Status: research only, no site code. Written after the owner rejected v1 and disliked the v2 home. Labels: verified (read or measured by me on the date shown), reported (third party, not checked at the source), guess (my judgement). Hard rules from CLAUDE.md apply: logo never changed, no AI imagery as the park, no unproven claim, English only, no em dashes, phones only from `phones.mjs`.

## 0. Owner feedback, restated as requirements
1. Navbar logo too small. Use the badge alone on mobile, a larger lockup on desktop.
2. Hero does not convert, is not pretty, H1 too big and clashes with the logo type.
3. Address and hours block has weak layout, unclear attention.
4. "Plots, roads and distances" table fights for attention and is badly designed.
5. Map must zoom out to show Modinagar and Hapur, and be more visible.

## 1. What the four reference sites actually do (opened 2026-11-12, desktop width, built-in browser)

### vipcutlery.com (verified)
- Signature idea: a full-bleed hero video of hand-etched copper ware, with one big italic serif line ("Crafted to Perfection") centred over it. Product is the hero, text is tiny by comparison.
- Build: Shopify theme. 8 video elements on the page (hero is 1080p MP4 loop, background video component), GSAP and ScrollTrigger loaded, Geist for UI text. No canvas. Page is about 9,500 px tall.
- Crafted feel: a founder story block ("In 1970, a 26-year-old spent a month packing spoons...") with a true origin, a proof strip of four numbers (500+ clients, 20+ years, 50+ years, "2x around the earth" spoons), six short story videos near the footer. Real numbers with a human fact next to them.
- Weak points to avoid: newsletter popup plus cookie box cover the hero on first load; heavy video payload.

### rajasthansweets.in (verified)
- Signature idea: the hero is ONE illustrated SVG (`Main_page.svg`): hanging ornate frames (like palace windows on threads) holding product photos, on a patterned cream ground, with a heritage motif as a scalloped divider between sections (`section-svg-up`). The brand's own culture becomes the layout.
- Build: Shopify Dawn base, Swiper only, Fraunces serif headings, almost no JS animation. The craft is in the artwork, not in code. Page about 4,200 px, very light.
- Crafted feel: motif repeats (frame shape, scallop edge, pattern) so every section feels from the same hand.

### reliablevacation.com (verified)
- Signature idea: the logo sits at the sun position of a mountain photo. On scroll the logo travels up and shrinks into the sticky nav, and the real sun, a person on the ridge and a fog layer come into view. Logo as the sun, scroll as the sunrise.
- Build: Framer (generator meta says Framer). Layers named in the DOM: Sky, Mountain, Foreground, Cloud, Progressive Blur, inside a "Desktop Scroll" sticky container. 2 canvas elements, 194 images, Instrument Serif plus Inter. Services are a numbered list of rows with slightly tilted photos that slide as you scroll, section edges use a "Dome" curve.
- Footer: dark brown ground, small link columns, then a gigantic serif "Reliable" wordmark with a flat white circle (sun) rising behind it as you reach the bottom. The one memorable end to the page.
- Weak points: 15,600 px page, 194 images, heavy for a B2B audience on mid phones.

### healixhealthcare.ae (verified)
- Signature idea: a calm centred serif headline ("Care Delivered Anytime, Anywhere.") with ONE button, then a wide photo of two hands clasping that bleeds off the right edge, the brand mark appears on the white coat cuff. Handshake equals the promise.
- Palette (measured computed styles): warm cream #F6F4EF ground, warm ink #26211F, one orange #E36B2B/#F27200 for every action, cool pale #F0F5F5 as a second ground. One accent used only for actions plus an orange marquee strip of five trust words.
- Build: Framer, Hedvig Letters Serif for headings, Switzer/Manrope/Inter for text, 1 canvas, 13 SVG. Floating pill navbar with a single orange CTA.
- Weak points: many sections were still blank during my scroll test (reveal-on-scroll not fired), a reminder that hidden-until-animated content hurts SEO and users.

### Pattern across all four (verified, 2026-11-12)
1. All four use a serif display heading. Sizes are modest next to the imagery. None uses a heavy uppercase sans in the headline.
2. One signature object per site (video of ware, hanging frames, rising logo/sun, joined hands). The hero is the object, not a paragraph and a table.
3. One accent colour for actions. 4. A distinctive footer or divider shape repeated through the page.

## A. What to borrow from each, translated to an industrial plots park (original concepts only)
| Source | Principle to borrow (not the asset or exact idea) | IIP translation |
|---|---|---|
| VIP Cutlery | A founder-grade human fact beside real numbers. One calm line over the hero. | A 4-number proof strip using ONLY documented facts (see section F). Hero line short and set in a serif at modest size. No video (no own footage, and speed). |
| Rajasthan Sweets | Local culture as ornament; repeated shape; one hand-drawn SVG hero. | A surveyor's plan-sheet motif: plot grid, dimension ticks, north arrow, boundary dashes, as one inline SVG hero and as the repeated divider (a notched "plot corner" edge). Brand sunburst as a faint line motif. |
| Reliable Vacation | The logo is the sun. Scroll equals time of day. Giant wordmark footer with a rising disc. | The IIP badge rises at a horizon line drawn over the plots. Footer carries a giant "ISAPUR" wordmark with a flat yellow sun disc half risen behind it. Navbar swap: big badge in hero travels to a compact nav lockup. |
| Healix | One accent, one button, a unique palette, calm centred headline, a human-contact image. | Palette: brand green #0F4D3A on cream, yellow #FFD600 only for actions, ink #111827. Call and WhatsApp as the only buttons. For "hands joining": a handshake between factory owner and site team needs a real photo, so defer until the owner has one; until then use a drawn plot-corner "join" (two boundary lines meeting at a pin). |

## B. Three concepts for the v3 home

Shared rules for all three (these keep the site fast and SEO safe):
- h1 is real HTML text, first in the DOM, in the hero. All other copy, phones, address, hours are HTML text. The SVG art has `aria-hidden="true"` and `role="presentation"`, and carries no information that is not also in text.
- No video, no canvas, no WebGL. Art is inline SVG (target under 12 KB gzip) plus CSS transforms. Optional scroll-linked motion uses CSS `animation-timeline: scroll()/view()` inside `@supports`, with a plain static layout as the default. JS budget stays under 60 KB (hard budget from DESIGN-DIRECTION.md).
- LCP element is the h1 or the lead paragraph (text, system fallback metrics matched with `size-adjust`), target LCP under 1.8 s on mobile (budget guess; Google's "good" threshold is 2.5 s, reported at web.dev/articles/lcp). CLS 0: every art box has fixed aspect ratio.
- `prefers-reduced-motion: reduce`: no transforms run, art renders in its final state, nothing is hidden before it animates. Same for no-JS and for crawlers.
- Never use opacity 0 on content waiting for a reveal (Healix lesson). Motion only moves decorative layers.
- Fonts: 2 families, 3 files max, `font-display: swap`, preload only the heading file used by the h1.

### Concept 1: "First Light" (recommended)
Idea: the IIP badge rises like a sun at the horizon of a drawn plot field. The page is a day starting on the park.
- Hero (desktop): cream ground. Left 7 columns: eyebrow "Hapur-Modinagar Road", h1 (section C size), one lead line, button row (Call, WhatsApp, text link "See the location"). Right 5 columns and bottom band: one inline SVG, a flat green horizon band with perspective plot-grid lines in line-weight strokes, and the badge as a half-risen sun on the horizon. Mobile: art goes below the buttons, shorter.
- Motion: on load, badge translates up 24 px and a yellow disc scales 0.9 to 1 (600 ms, once). On scroll, the badge moves into the nav slot (scroll-linked, CSS only), so the logo is large in the hero and compact (but never below 40 px) in the sticky nav. Reduced motion: badge already in nav position, hero art static.
- Scroll story: "Morning" (hero), "Roads" (plan-sheet line drawing, stroke-dashoffset draws once into view), "Neighbours" (map band, section E), "Plots" (3 numbers), "Visit" (address and hours), then footer.
- Footer: dark green ground, giant "ISAPUR" wordmark (Montserrat ExtraBold, the logo face, so it IS the logo, set as real text in one span with `aria-label`), yellow sun disc half risen behind it, rising 40 px when the footer enters view. Link columns small above it. Phones and address as real text.
- Why it is fast: art is one SVG, motion is transform only, no images in the hero.

### Concept 2: "Ground to Growth"
Idea: the tagline "The Groundwork for Growth." told as a vertical scroll story from bare plot to working factory. Use the tagline once on the page and it must be the story title, not repeated in the hero.
- Hero: calm centred serif h1, one button pair, and under it a wide SVG strip of one bare plot outline (dashed boundary, pin, 2 dimension ticks) bleeding off both edges.
- Scroll story (4 beats, sticky container, CSS scroll-driven): beat 1 bare plot outline; beat 2 approved roads drawn as thick lines (label "15.24 m wide main roads, as on the approved layout"); beat 3 plot block fills with a flat shed silhouette; beat 4 yellow sun disc and "Book a site visit". Each beat has its own real h2 and paragraph in HTML in normal flow. On mobile and reduced motion the beats stack as 4 normal sections with the SVG state fixed per beat.
- Footer: "plot corner" notch edge, three columns, a bar with the badge and the two phone buttons. No giant wordmark (keeps it quieter).
- Risk: scroll-pinned stories can annoy factory owners on phones. Mitigation: pin only at width 1024 and up, no pin on touch.

### Concept 3: "The Site Board"
Idea: the whole page reads as the sanctioned layout sheet pinned on a site-office wall (the living-room wall scroll idea, translated to a site hoarding): framed panel, title block in the corner (park name, phone, hours), plot grid, stamp-like labels. Precise, trustworthy, very "industrial drawing".
- Hero: a large framed rectangle, thin ink border, drawn plot grid as background, a title block bottom-right with "Isapur Industrial Park", road name, hours and the two phone buttons; h1 sits top-left, small. Hanging cord detail (two lines from the top corners to a nail) echoes Rajasthan Sweets' hanging frames without copying them.
- Motion: on load the frame drops 12 px and settles (once). On scroll the title block stays sticky as a slim bar (name, Call, WhatsApp). Sections are further "sheets" with a drawing number (A1, A2...) as the heading eyebrow.
- Footer: a "revision table" style footer (rev, date, what changed is NOT shown; instead address, hours, phones, map link). Giant wordmark optional.
- Risk: can look cold. Counter: cream ground, one warm yellow, big human sentence in the hero lead.

Recommendation: Concept 1 for the home. It answers "logo too small" (the logo is the hero), "H1 too large" (the h1 shrinks because the art carries the weight), and gives the owner the "logo rises like a sun" idea in an original industrial form. Reuse the plan-sheet drawing language of Concept 3 for inner pages.

## C. Font fix

### What the wordmark font is
- Brand tokens and the knowledge file say display is Montserrat (500, 600, 800), "ExtraBold for ISAPUR". Knowledge file line 158 says Montserrat is an approximation of the original wordmark face (UNVERIFIED). The kit SVGs use `font-family="Montserrat"` (58 uses) and Inter (20) (verified by grep 2026-11-12). The supplied logo artwork's true face is unknown. Do not claim "same font".
- The clash cause (guess): v2 set the h1 in Montserrat at heavy weight and large size, so two wide geometric heavy faces compete with the nav wordmark.

### Recommendation
Keep Montserrat ONLY for the logo and the footer wordmark. Change page headings to a serif so the logo stays the only heavy geometric voice. All four reference sites do this (section 1).
- Logo-safe scale if the owner prefers to keep Montserrat for headings: weight 600 max (never 800), never uppercase, h1 at most 44 px desktop and 32 px mobile, letter-spacing -0.01em, line length 22 ch to 26 ch, and the h1 cap height must stay under 60 percent of the wordmark cap height wherever the two appear within one screen.
- Nav logo: desktop lockup 176 px wide minimum (kit minimum is 120 px, verified in tokens), badge only 44 px high on mobile.

### Three Fontshare candidates (licence read 2026-11-12)
Licence (verified): https://www.fontshare.com/licenses/itf-ffl, ITF Free Font License v2.0 dated 17 Aug 2026. States free for personal and commercial use, websites included, self-hosting via @font-face is permitted and recommended, no derivative works, no extraction of font files from documents. The General Sans page (https://www.fontshare.com/fonts/general-sans) shows "Closed Source / ITF Free Font License", designer Frode Helland for Indian Type Foundry. Satoshi, Erode and Cabinet Grotesk pages also showed the same licence line when read by script (reported, because the page text loaded via script; re-check on the page when downloading). Record the licence page URL and the download date in the project docs.

| Font | Role | Why for IIP | Pairing | Sizes (desktop / mobile) |
|---|---|---|---|---|
| Erode (https://www.fontshare.com/fonts/erode) | h1, h2, large numerals | Soft serif, warm, contrast with heavy logo, matches the serif pattern of all four references | Inter 400/500 body (already in the kit) | h1 clamp(2rem, 3.4vw + 0.5rem, 3.25rem) weight 500; h2 clamp(1.5rem, 2vw + 0.5rem, 2.25rem); numerals 56 to 72 px |
| General Sans (https://www.fontshare.com/fonts/general-sans) | all-sans option | Orderly rationalist sans, quieter than Montserrat, one family for headings and body | Self-pair, headings 600, body 400 | h1 clamp(2rem, 3vw + 0.5rem, 3rem); body 17 px / 1.6 |
| Satoshi (https://www.fontshare.com/fonts/satoshi) | all-sans option | Neutral modern sans, wide weight range, good numerals | Self-pair or with Erode for numerals | h1 clamp(2rem, 3vw + 0.5rem, 3rem) weight 600 |

Recommended: Erode headings plus Inter body, Montserrat limited to the logo. Cabinet Grotesk was also checked (same licence) but is too characterful next to the badge, so not shortlisted. Self-host WOFF2 subsets (Latin), headings file under 30 KB.

## D. Hero conversion research (B2B, land and plots)

Evidence is thin and mostly vendor blogs. I found no controlled study on phone placement in B2B land heroes. Treat as direction, then test.
1. One primary action, secondary as a plain text link: https://pathtoflowhq.com/articles/hero-section-design (read 2026-11-12, reported). It also says specific headline, keep the hero light, avoid autoplay video and rotating carousels, proof logos right under the hero.
2. Static hero beats rotating hero, content should peek so people scroll: NN/g carousel guidance, https://www.nngroup.com/articles/designing-effective-carousels/ (reported via search summary 2026-11-12, not read in full).
3. Single high-contrast CTA above the fold, and track phone taps to judge the fold: https://www.madebyfactory.com/7-above-the-fold-elements-every-b2b-homepage-needs/ (reported via search summary, the page itself returned 404 when fetched on 2026-11-12, so treat as unverified).
4. B2B landing conversion benchmarks (5 to 15 percent vs 2 to 3 percent) and "66 percent of clicks happen without scrolling": https://saleshive.com/blog/optimizing-a-landing-page-for-lead-generation and https://www.albacross.com/newsroom/b2b-lead-generation-strategies (reported, vendor figures with no primary source: do not quote on the site).
5. Local factory-owner behaviour (guess, from the audience in CLAUDE.md): they decide by phone and by visiting, they use WhatsApp for documents and maps, and they read on mid-range Android phones. So the conversion is a call, a WhatsApp message or a booked visit, not a form.

### Recommended hero (applies to Concept 1, adaptable to others)
- Eyebrow: "Hapur-Modinagar Road, Ghaziabad district"
- h1 (about 8 words): "Industrial plots on Hapur-Modinagar Road" (keeps the SEO phrase; size per section C).
- Lead (one line, only documented facts): "Layouts sanctioned by Zila Panchayat Ghaziabad, subject to conditions. Site visits 8 am to 8 pm, closed Tuesday."
- Button 1 (primary, yellow on green or ink): "Call 92195 49800" (tel link from `phones.mjs`, `data-cta-id="hero-call"`).
- Button 2 (secondary, outline): "WhatsApp 98377 64222" (wa.me link from `phones.mjs`, prefilled text "Hello, I want to visit Isapur Industrial Park. Please share plot sizes and prices.", `data-cta-id="hero-wa"`).
- Text link: "Book a site visit" (anchor to the form).
- Note: the owner decision is 9219549800 as the sales call number and 9837764222 as WhatsApp; the current `content.json` order and `phones.mjs` must be checked so the swap point matches before build. Both numbers stay behind the single swap point.
- Trust line under buttons (small): "Open now / Closed today" computed in HTML with a static fallback "8 am to 8 pm, closed Tuesday".
- Mobile: buttons are full width, stacked, 48 px high, sticky bottom bar repeats only Call and WhatsApp (already in the phone bar rule).
- Test plan: after launch measure `hero-call`, `hero-wa`, form submit per 100 sessions via the event spec in `04_Analytics/event-spec.md`. Test swap of button order after 4 weeks of data (guess).

## E. Layout rules

### Address and hours block ("Visit" section)
1. One focal point: the address is the headline of the block (serif 28 to 32 px), nothing else is larger.
2. Left column: address, then a "Get directions" button (secondary). Right column: hours as a compact 7-row list, today's row highlighted with the yellow marker, Tuesday row shows "Closed" in grey. Phones sit under hours as the two buttons.
3. Status chip ("Open now until 8 pm") sits above the address, not buried under it. Rendered in HTML with a static fallback.
4. No card within a card. One flat panel on the sage ground, 24 px padding, hairline divider between columns, gap equal on all sides.
5. Remove the neighbouring-pump row from this block (it is a proof item, not a visit item) and the photo beside it. The map takes that space (see map spec).
6. Mobile: address, chip, buttons, then hours, single column, buttons full width.

### Replacing the "plots, roads and distances" table
- Delete the three three-row lists. Replace with ONE row of three big numbers plus ONE icon row.
- Big numbers (serif numerals 56 to 72 px, caption 15 px grey), only documented facts: "15.24 m" "wide main roads on the approved layout" (Phase 2 plan, 50 ft equals 15.24 m); "3" "layouts sanctioned by Zila Panchayat Ghaziabad" (Phase 1 extension, 2, 3; add "subject to conditions" in the caption); "8 am to 8 pm" "site visits, closed Tuesday". Plot-size number held until owner confirms (see F).
- Icon row (one line, 4 items, line icons 28 px, 14 px labels): "Hapur-Modinagar Road", "4.7 km by road to the Delhi-Meerut Expressway", "11.4 km by road to Modinagar bus stand", "13.4 km by road to Hapur bus stand". Distance facts stay labelled "by road" or "straight-line" and need their source row in the knowledge file before shipping.
- Full table of all distances lives on `/location/` only. The home links to it with one text link.
- Rules: max 3 numbers, no borders around cells, numerals aligned on a baseline grid, one ground colour behind the whole strip, nothing else in the section competes (no photo strip).
- Remove the photo strip of stand-in photos (street light, factory yard, palms, road) from this section: it illustrates claims the park cannot prove (see F).

### Zoomed-out map spec
- Source: OpenStreetMap data (open licence ODbL, attribution "Map data from OpenStreetMap contributors" in the footer credit line, reported, confirm at openstreetmap.org/copyright at build). Render once to a static WEBP (the existing `site-v2/public/img/map/` pipeline), do not hot-link tiles and do not bulk-scrape the public tile servers (OSM tile usage policy, reported).
- Extent (guess, tune on render): west 77.52, east 77.88, south 28.70, north 28.90 (shows Modinagar near the west, Hapur near the east, the Delhi-Meerut Expressway and the Hapur-Modinagar Road). Approx zoom 11 to 12.
- Marked: park pin (large badge, the only yellow), Modinagar and Hapur as labelled dots (town name text), the expressway on-ramp, the Hapur-Modinagar Road as a thick green line, light grey for other roads, no clutter labels.
- Size: full-bleed band, 1440 x 560 on desktop (aspect 2.6), 390 x 360 on mobile (crop to Modinagar, park, Hapur horizontally via two renders). It sits directly under the hero stats, with the section h2 "Where the park is" and a one-line caption. Image is 1800 px wide WEBP under 120 KB with width and height set.
- Real text next to it (not in the image): "Modinagar about X km by road, Hapur about Y km by road" using the verified distances. The alt text names Modinagar, Hapur and the road.
- Link: the whole map links to `/location/`, plus a "Open in Maps" text link to the `mapSearch` URL.

## F. Claim check on the current home (`02_Website/site-v2/src/pages/index.astro`)
Source of truth: `06_Content/approvals-facts.md` (documents read visually 2026-11-12). It supports sanctioned layouts, wide roads and drainage lanes shown on drawings, and an applicant statement of completed development. It does NOT support RCC, power, lighting installed, planted greenery, drainage built.

Remove or soften until proof exists:
| Where on the home | Current text | Action | Safe replacement |
|---|---|---|---|
| `<title>` and meta description | "50 ft RCC roads, street lighting, planted greenery" | Remove | "Industrial plots on Hapur-Modinagar Road, Ghaziabad district. Layouts sanctioned by Zila Panchayat Ghaziabad, subject to conditions. Book a site visit." |
| Plots section, "Roads and facilities" | Roads "50 ft RCC" | Remove "RCC". Keep the width only as a drawing fact | "15.24 m (50 ft) wide main roads on the approved Phase 2 layout" |
| Same | Street lighting "Installed" | Remove | None. Phase 2 letter lists electric poles and lights inside "internal development" but that is an applicant statement, no photo. Say nothing until site photos exist. |
| Same | Greenery "Planted" | Remove | "The approved layout includes a green divider strip" (Phase 2 and 3 plans) |
| Same | "Petrol pump, IndianOil, next door" | Soften | "IndianOil pump about 190 m away (straight-line, from Maps)" or move to `/location/` |
| Visit section | "Fuel next door, IndianOil pump, about 190 m" | Soften | same wording as above, or drop from the visit block |
| Map section, fact | "50 ft RCC roads inside the park" | Remove | Use the 15.24 m line above |
| Plots, "Plot size, from 300 sq yards" and the map fact "300 sq yards, the smallest plot" | Plot size claim | Hold: owner must confirm. Documents show plots from roughly 195 sq m (about 233 sq yd, Phase 3, partial read) and about 390 to 900 sq m on Phase 2 | Show no plot size on the home until the owner supplies a chart or confirms the smallest plot |
| Plots, "Price on request" | OK (no claim) | Keep | "Price on request" |
| Photo strip: "street-light", "factory-yard", "verge-palms", "road-green" with links to /amenities/ and /neighbours/ | Images implying lighting, greenery, factories | Remove from the home | They are stand-ins and imply park features. If used elsewhere, label as stand-in photographs in the footer credit line only. |
| Hero image alt: "Delhi-Meerut Expressway ... six lanes and street lights" | Stand-in photo of a real expressway | Remove with the hero photo (v3 hero is drawn) | |
| Plots, distances (Expressway 4.7 km, Modinagar bus stand 11.4 km, Hapur bus stand 13.4 km, Bhojpur exit 4.3 km straight) | Distance claims | Keep only with "by road" or "straight-line" labels, and only if each has a source row (Maps lookup date) in `00_ISAPUR_KNOWLEDGE.md` section 3. Bhojpur exit has no road/drive label beyond straight-line: keep labelled | |
| Hero lead "Open 8 am to 8 pm, every day except Tuesday" | Owner-supplied hours | Keep (owner fact) | |
| Not on the home today, but do not add | "approved", "RERA", "ready", "power", "water", "sewerage", "drainage built", "security" | Never add without proof. Safe sanctioned wording: "Layout map sanctioned by Zila Panchayat Ghaziabad, subject to conditions." Phase 2 only: "approval letter dated 16 March 2026". Printed notes say water, sewerage (septic tank) and building approval are per plot owner. | |

Also check before ship: `llms.txt.ts`, JSON-LD and the `/amenities/` and `/neighbours/` pages for the same three claims (schema must not carry a claim without proof, CLAUDE.md).

## G. Next steps for the build (owner decisions needed first)
1. Pick a concept (recommended: First Light).
2. Confirm: smallest plot size, which phone is call and which is WhatsApp (the `phones.mjs` swap point), and permission to use the sanctioned-layout line on the hero.
3. Approve the font change (Erode plus Inter, Montserrat logo only) and download Erode from Fontshare, save the licence URL and date in the docs.
4. Then build, run `perf.mjs`, `consistency.mjs`, `check.mjs`, `gate.mjs`, and update knowledge file, TODOS, CHANGELOG and `_ops/TECH-STACK.md`.
