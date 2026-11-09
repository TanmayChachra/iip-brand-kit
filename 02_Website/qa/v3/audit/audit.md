# IIP site v2 design audit (2026-11-08, read only)

**Verdict:** v2 is clean, fast and accessible, but it does not yet read as premium or as an Indian industrial park. It looks like a quiet minimal template: off-white page, light-weight type, no yellow, no flag, almost no brand character, and none of the 14 stand-in photos shows India or the park's kind of land. It will not beat the owner's "template" and "not premium" complaints in this state. Top fixes are photographs, brand colour and type weight, then layout hygiene.
**Evidence:** built `dist` served on 127.0.0.1:4399, 18 full-page screenshots (1440, 1024, 390 x 6 pages), Playwright CLI checks, source read of `site-v2/src`, Vercel guidelines text fetched today, Airbnb and Figma DESIGN.md fetched today.
**Caveats:** the builder was still editing (inner pages not done per `PROGRESS.md`; `dist` rebuilt 20:25, I audited after that). Impeccable's engine binary was NOT run (policy: no downloaded binaries), so its detector step was done by hand from `craft-floor.md` and `critique.md`. As a fork I cannot spawn sub-agents, so the critique ran inline (the skill calls this degraded: single-context). The OSM map is not on any page yet.

## Scorecard (my judgment, 0 to 10)
| Area | Score | Why |
|---|---|---|
| Craft and accessibility | 8 | no overflow at 390, 1 H1 per page, all text contrast 8.9 to 15, focus ring 2px solid, reduced motion clean, 0 broken images, alt on every image, no em dashes |
| Performance | 8 | home 7.6 KB HTML gzip, CSS 27.8 KB gzip (near the 30 KB cap), JS 12 KB gzip |
| Brand fit | 3 | no yellow anywhere, no tri-colour flag, Work Sans at weight 400 instead of kit Montserrat 800 |
| Photography | 3 | wrong geography, one CGI-looking shed, sky-heavy hero |
| Premium feel | 3 | big empty areas, tiny type in data rows, weak hierarchy, no authored moment visible |
| Copy | 7 | plain and factual, claims inside the allowed list, but a few markdown leaks and thin pages |

## The 15 highest-impact fixes (ranked)
1. **Replace the hero photograph** (`src/pages/index.astro` hero, file `public/img/photo/hero-*.webp`). It is an Eastern-European looking aerial (red-white chimney, apartment blocks, storm sky) where 60 percent of the frame is sky and the subject is a thin strip. Use an Indian expressway, industrial belt or flat NCR plain scene, subject filling the frame. Best honest source: Wikimedia Commons photographs of the Delhi-Meerut Expressway (CC licences with attribution) or Unsplash India industrial and truck images; log photographer names, not just photo ids, in `public/img/photo/credits.json`.
2. **Remove or replace the shed picture** (`shed-*.webp`, used on the home visit panel and as the plots hero). It reads as a 3D render, which is the artificial look the owner rejected. If the source is AI or CGI, drop it. Also repeats across pages.
3. **Fix the geography of the whole photo set.** Forklift interior (Western), US style loading docks, European poplar avenue, interchange aerials, street lights at sunset: none is India. Pick 12 to 14 frames that read as an Indian highway belt (dust haze, trucks, concrete road, neem and gulmohar trees, low sheds) or reduce the count to 6 strong ones. Say in the footer credit line that all are stand-ins (already there).
4. **Bring the brand colour in.** `src/styles/place.css:4-7` has green and off-white only, zero yellow (checked: 0 elements use #FFD600). Add `--p-accent-2: #FFD600` for the one accent: primary button hover, key numerals, a 4 px underline under the H1, the plots strip. Use the thin tri-colour flag (kit `02_Pattern`, 1 percent of width) as the nav bottom line and the close section top edge. Owner asked for colourful, not black and white.
5. **Use the kit typeface.** `place.css:2,8-10` loads Work Sans at weight 400 for display. Brand kit says Montserrat 800 display and Inter text (`01_Brand/Brand-Kit/tokens/brand.tokens.json`). Switch `--font-display` to the kit's Montserrat subset (already in v1 `public/fonts`), weight 700 to 800, tracking -0.02em. Weight 400 headlines are the main reason it feels light and template-like.
6. **Fix the heading hierarchy.** The type moment (`place.css:15`, up to 66 px) is larger than the home H1 (48 px, `h1` computed 48px/400). Make the H1 the biggest thing on the page (Figma 86 px, Airbnb 64 px) and keep the address at 40 to 48 px.
7. **Fold composition on desktop.** At 1440 the first screen is a sky-dominated band plus a small headline and 40 percent empty cream below (`section` 900 px with 589 px top padding for the hero). Make the picture the full hero (min-height 100dvh minus nav) with the headline overlaid bottom-left on a flat scrim, or crop tighter so the subject fills it.
8. **Put the real OSM map on the site.** `public/img/map/map-park.*` exists but no page uses it (`mapImg: false` on all 5 pages checked). Use it on the home visit section and `/location/` in place of the "Find us on the map" text link, and add the OSM credit to the footer credits line.
9. **Orphaned headings in two-column prose** (`place.css:56-57`, `.cols2`): "How buying works" on `/industrial-plots/` and "Straight-line distances" on `/location/` sit at the bottom of column 1 with their text in column 2. Add `.cols2 h2 { break-after: avoid; }` or drop columns below 1280 px.
10. **Home visit panel is cramped.** Opening hours render as three squeezed columns ("Monday, Wednesday to Sunday" wrapping inside a 480 px panel) and the home booking form puts four inputs in one narrow row with wrapping labels (`src/pages/index.astro:96-101`, `place.css:41`). Stack the hours as two rows and make the form two columns of two.
11. **Markdown leaks into plain text.** `/contact/` lead shows literal `**98370 57800** or **98377 64222**`; `/faq/` answers show `](/location/)` and `](/blog/industrial-plot-buying-checklist/)` as raw text. Fix in the content files: `src/content/pages/contact.md` lead (remove the asterisks) and the FAQ `faq:` answers (frontmatter strings are not rendered as Markdown: strip the link syntax or render with a small inline-link filter). Also a red dashed outline appears around those FAQ answers on mobile (debug style or invalid markup, find the rule).
12. **Form posts to a dead address.** `src/components/BookForm.astro:5` action is `mailto:visits@isapurindustrialpark.example` unless `PUBLIC_FORM_ENDPOINT` is set. A real visitor's lead would be lost. Wire a real endpoint (Cloudflare Pages Function, Formspree, or a Google Form) before launch; until then show the call and WhatsApp buttons first. Also `Day you can visit` and `Plot size` are free text (`BookForm.astro:11-12`): use `type="date"` (or a select) and a select with the plot size bands.
13. **Footer closing CTA is a full-width white bar** (`Base.astro:68`, `btn--xl btn--wide`) that reads as an input field, not a button. Use a yellow pill button, auto width, with the arrow, left aligned under the headline.
14. **Logo sits on a white tile** on the off-white nav (`Base.astro:48`, `logo-horizontal.svg` has a white background rect). Use the transparent kit lockup (`01_Brand/Brand-Kit/live/01_Logo/logo-horizontal.svg` without background) or match nav background to white. Never alter the logo; remove only the surrounding tile if the file has an optional background.
15. **Thin content and long titles for SEO.** Home has 257 words, plots 349, contact 170. Titles are over 60 characters on home (64) and neighbours (66): shorten in `src/content/pages/*.md` frontmatter. Add one real paragraph per section (who it suits, what to bring to a visit) and the 5 landing pages' unique facts.

## Where the owner's complaints land
- **Template?** Yes, still. Layout families are fine but visual identity is absent: no yellow, no flag, no sunburst, light type, small data text (rows at 16 px in 1440 wide rows). Fixes 4 to 7, 13.
- **AI made?** The photo set no longer is, but one CGI shed and the generic stock cliches (steel lattice, sunset street lights, forklift) read as stock. Fixes 1 to 3.
- **Premium and international?** Not yet. International sites in this category (Airbnb, Figma refs below) use 64 to 86 px display, 96 px section padding, one confident photograph per screen. We use 48 px at weight 400 with 900 px screens that are half empty.
- **Colour?** Green is visible, yellow is not, no black and white problem but a beige and sage problem (page is 85 percent off-white). One full green band exists only in the footer. Add one mid page green band and yellow accents.
- **Claims:** all inside the allowed list. "Street lighting: Installed" and "Greenery: Planted" are owner-stated, keep wording as is. Neighbours page correctly uses straight-line and states no partnership. No Section 80, no approvals, no phases. No em dashes.

## Skill 1: impeccable (hand run, binary not executed)
Used `critique.md` Assessment A and the `craft-floor.md` Verify and Refuse lists.
- Specificity: fails the "could another product use this unchanged" test (it could be any logistics broker).
- Refuse list hits: kicker/eyebrow above headings on the home visit section ("Address and hours", `visit` section) and small uppercase group labels in the plots rows (`.grp h3` 13 px, `place.css:23`); hero-metric style plots rows (big number, small label); same-size 4-up photo strip as filler (`.pl-strip`, `place.css:26`) that carries no information; photographs as decoration, not evidence.
- Pass: no gradient text, no glass, no side-border cards, no section numbers, no emoji, contrast, focus visible.
- Type floor: display max 6rem OK, tracking OK, body measure 62ch OK (`.prose`), but body rows at 16 px in dense 3-column grid at 1440 feel small.
- Provocative questions: what is the one picture the owner would be proud to show a buyer? Where is the money moment (a plot, a road, a gate)? Why does a park that sells land show no land?
- Not done: the detector overlay and `impeccable detect` (needs the downloaded engine).

## Skill 2: web-design-guidelines (Vercel rules, fetched today), file:line
- `src/components/BookForm.astro:11` plot size is `type="text"`: use select. Same file :12 day is `type="text"`: use `type="date"` or select.
- `BookForm.astro:5` mailto action with `.example` domain, no real submit path.
- `BookForm.astro:7-12` inputs have labels, autocomplete, aria-describedby: pass. Missing `spellcheck="false"` on name and phone, and `autocomplete="tel"` is present, ok.
- `BookForm.astro:15` live region `role="status"` present: pass.
- `src/layouts/Base.astro:21` viewport allows zoom: pass. `Base.astro:24` theme-color matches page: pass. No `color-scheme` meta or CSS (light only, acceptable).
- `Base.astro:26` display font preloaded with `font-display: swap` (`place.css:2`): pass. No `preconnect` needed (self-hosted).
- `place.css` has no `transition: all`, no `outline: none` (0 hits), tabular nums on `.dist` (`:58`), `text-wrap: balance` on h1 and h2 (`:76`): pass. `place.css` lacks `touch-action: manipulation` on buttons and links.
- Brand name not wrapped with `translate="no"` (`Base.astro:48`, footer): add.
- Long titles: home 64, neighbours 66 chars (`src/content/pages`).
- Images: all `<img>` have width and height (0 missing), hero `fetchpriority="high"`, below fold lazy: pass.
- Animation: 0 running animations under `prefers-reduced-motion: reduce`, 0 hidden elements: pass.
- Tab walk at 1440: skip link, logo, nav links, header CTA, hero CTA, address link, directions, phones, picture links: order logical, every stop shows a 2px solid outline, none hidden under the sticky header. The photo links carry no visible text but have alt names (0 unnamed links on 5 pages).
- Mobile tap targets: 0 failing at 390 on all 6 pages (only the visually hidden skip link is under 44 px, that is fine). At 1024 and 1440 nav links and footer links are 36 px tall (`Visit 48x36`): raise to 44 px or accept for pointer devices.

## Skill 3: awesome-design-md (Airbnb, Figma) vs our CSS
| Metric | Airbnb | Figma | Ours (site-v2) |
|---|---|---|---|
| Hero display | 64 px, -1 px tracking | 86 px, -1.72 px (-0.02em) | 48 px, -1.2 px, weight 400 |
| Section heading | 28 px | 64 px | 32 px, weight 400 |
| Body | 16 px | 16 to 20 px | 20 px paragraphs, 16 px rows, 14 px labels |
| Section padding | 64 px | 96 px | 120 px top, 72 px bottom (900 px screens, mostly empty) |
| Button | 48 px high, padding 14x24, radius 8 or pill | padding 10x20, pill 50 px | 44 px, padding 0x24, radius 2 px |
| Radius scale | 4 / 8 / 14 / 20 / 32 / pill | 6 / 8 / 24 / 32 / pill | sharp, one scale (consistent) |
| Colour | white canvas plus one hot accent (#ff385c) | black and white plus big pastel blocks | off-white plus one dark green, accent missing |
Takeaways: hero at least 64 px and heavier; one decisive accent used on every CTA; large colour blocks are what stops a plain page looking bland (Figma). Our sharp radius is a valid choice but pairs best with bold type.

## Skill 4: playwright-cli (Playwright CLI 0.1.23)
- 18 screenshots in `screenshots/` (WEBP, 1200 px wide cap): home, plots, location, neighbours, faq, contact at 1440, 1024, 390.
- Horizontal overflow: none on any of the 18. H1 count: 1 on all. Broken images: 0. Console errors: none (only navigation-aborted image requests while moving between pages, benign).
- Upscaled images: `shed-hero-1600.webp` 1367 px source shown at 1440, `junction-hero-1600.webp` 1279 px shown at 1440 (slightly soft on large screens).
- Full-page heights at 1440: home 5400, inner pages exactly 2700 (3 fixed screens): content is laid in fixed 900 px screens, so inner pages with short text leave large empty bands.
- Contrast (computed): nav 14.96, body 14.96, buttons 8.92, footer links 8.92, labels 13.58: all pass AA.
- Reduced motion: no running animations, nothing left hidden.

## Photo audit (14 photographs)
| Photo (id) | Used | Sharp | India | Verdict |
|---|---|---|---|---|
| hero (1592385456792) | home hero | yes | no | replace (fix 1) |
| shed (1766793110924) | home visit, plots hero | yes | no, CGI look | replace (fix 2) |
| steel (1509024368907) | strip | yes | n/a abstract lattice | cut, decoration |
| forklift (1770827730773) | strip | yes | no, indoor | cut |
| lights (1705564707876) | strip | yes | generic sunset | keep only if India |
| treeroad / roadtrees | strip, wall | yes | European avenue | replace |
| aerial-a, b, c | wall, neighbours hero | yes | no (Eastern Europe) | replace |
| junction, expressway | wall, location hero | yes, slightly upscaled | no | replace (use real Delhi-Meerut Expressway) |
| docks (1780367261654) | home booking | yes | US style | cut |
| dusk / lane | wall | yes | generic | review |
Rule: pick photographs that a Ghaziabad factory owner would recognise as home. If none can be found, show fewer photographs and more type, map and numerals rather than foreign ones.

## Copy audit
- No AI tells found in visible copy ("Industrial plots on Hapur-Modinagar Road", "Fuel next door"). Fixed facts only; no fake precision.
- Issues: markdown leaks (fix 11); `Closed, opens tomorrow at 8:00` is computed in the browser by the kit's `system.js` from the hours table, so it stays correct (verified in `public/assets/system.js:234`).
- Two H2s in the plots rows ("Plots, roads and distances") plus group labels in 13 px are small; consider bigger numerals for 50 ft, 4.7 km, 300 sq yd as the one authored moment.

## Files
`audit.md`, `result.json`, `screenshots/*.webp`, `shoot.js`, `checks.js`, `checks2.js` (the Playwright CLI scripts), `shoot-parsed.json`, `checks-parsed.json`, `checks2-parsed.json` (raw results).
