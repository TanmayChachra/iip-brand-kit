# Website design direction v3 (2026-11-08, replaces v1 and v2)

History: v1 looked like a template (owner: "I hate that website design"). v2 (dark forest theme with AI generated renders) was stopped: the owner does not like the artificial imagery direction. v3 is rebuilt as `02_Website/site-v2/` with the updated taste-skill (tasteskill 2.5.1, its run, deal and gate) and Impeccable. The v1 Astro site stays in `02_Website/site/` for reference only.

## Design read
Reading this as: a PLACE (people come to visit the park and book a site visit) for local factory owners, with a plain, confident, photograph-led company language at the figma.com and x.ai level of finish, built as Astro static pages. Kind = place, page type = place, site-kind = other. Main action: Book a site visit (one label everywhere, the call and WhatsApp buttons are separate intents in the phone bar).

## Imagery (hard rule, owner decision)
NO AI generated imagery and no flat cartoon illustration. Allowed:
1. Real licensed stand-in photographs found with the skill's `scripts/photos.mjs` (live search, licence recorded): industrial buildings, concrete roads, steel, trucks and loading, trees and verges, Indian industrial belt, dusk and daylight. 12 to 20 on the full page. Credits in ONE footer line only (no captions under images, skill house rule 1). Never shown as the park's own pictures and never with another maker's name; the footer line says photographs are stand-ins until the park's own shoot.
2. A real map of the area drawn from OpenStreetMap data (accurate roads, expressway, villages) in the brand colours (`site-v2/public/img/map/`), attribution in the footer credit line.
3. Typography, real numerals, flat brand colour grounds, the thin tri-colour flag, the brand sunburst as a large cropped line motif, the brand badge from the kit.
The park's own photographs and the owner's supplied poster render are not used on the site yet. Real photos drop in later under the same file names.

## Look
Place rules from the skill: flat grounds, square photographs, one button style, the phone bar, dealt moments, no shader effect, no grain, no gradient scene, light page (dark pages and dark heroes are for tech only). Colour is the client's own, through `start.mjs brand`: brand green #0F4D3A, brand yellow #FFD600 as the accent, red #E53935 only inside the thin flag, ink #111827, off-white ground (not pure white), light sage and cream-yellow tints as flat section grounds, one full brand-green band for contrast. Not black and white: green and yellow are visible on every screen. Type: the kit's Montserrat (display) and Inter (text), self-hosted subsets, unless the skill's own check fails them, then say why. No em dashes anywhere.

## Structure, copy, claims
Same pages and URLs as `02_Website/pages.md`. Same words as `06_Content/website-copy/` and the imported site copy, edited to the skill's copy rules (plain, concrete, fact on the first screen, headings name things, buttons verb plus object). Claims unchanged: only 50 ft RCC roads, street lighting, planted greenery, plots from 300 sq yards, contact for price, hours 8 am to 8 pm except Tuesday, distances with road or straight-line labels, neighbours from Maps (INOX Air plant about 0.6 km, Namaste India plant about 0.7 km, IndianOil pump about 190 m from Phase 1, straight-line, text only). No approvals, no drainage, power or security claims. No phases or resale. Phones only from `phones.mjs` (the skill's rule 9 about phone formats is for invented demo sites: these are the client's real numbers, waive with the brief as the reason).

## Budgets and tracking
Hard: HTML under 30 KB gzip, CSS under 30 KB, JS under 60 KB (GTM separate and deferred), first load under 500 KB on mobile, Lighthouse mobile 95 plus, CLS 0, WEBP images with width and height. The skill's `perf.mjs`, `consistency.mjs`, `check.mjs` and `gate.mjs` must pass (waivers only with reasons in `.taste-skill/waivers.json`). Keep the v1 plumbing: SEO and Schema components, sitemap, robots, llms.txt, tracking script and event spec (`04_Analytics/event-spec.md`), data-cta-id attributes, content collections.
