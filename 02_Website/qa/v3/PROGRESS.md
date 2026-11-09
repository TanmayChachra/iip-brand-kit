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
