# IIP design language (locked by the owner on 2026-11-13, extracted from the built home page)

Source of truth for every page. The values below are read from `02_Website/site-v2/src/styles/home.css` (tokens at the top of that file). Do not change colours, fonts, spacing or section order without the owner. Brand tokens live in `01_Brand/Brand-Kit/tokens/brand.tokens.json`.

## Palette
| Token | Hex | Use |
|---|---|---|
| `--y` yellow | #FFD600 | accents: stripe, shutter, active chip, badges, link underline |
| `--r` red | #E53935 | the short heading underline, stripe middle, one detail only per drawing |
| `--g` green | #0F4D3A | primary button, links, roof sheeting, stripe end, footer ink |
| `--g2` bright green | #00A54F | roof rib hairlines, small highlights |
| `--mist` | #F2F4F6 | panel ground, drawing sheet, diagonal section ground |
| `--line` | #E5E7EB | hairlines, borders, empty progress bars |
| `--ink` | #111827 | text, drawing lines, footer ground |
| `--mut` | #4B5563 | secondary text, annotations |
| white | #FFFFFF | page ground |
Tints used inside drawings only: #374151 (secondary line), #9CA3AF (lightest line), #DCEFE4 (tree canopy), #FFD60066 (footprint). Yellow, red and green are accents, never full slabs. No gradients, no shadows (one exception: the nav menu panel has a soft drop shadow, the status dot is a flat ring).

## Type
- Display: **Erode** (variable 300 to 700, used at 600), tracking -0.012em, `text-wrap:balance`. Body and UI: **Inter** (variable). Montserrat only inside the logo.
- h1 `clamp(34px, 4.2vw, 60px)` / 1.06, max 15em. h2 `clamp(28px, 2.9vw + 8px, 44px)` / 1.1. h3 21 to 22 px (feature, buying), stage titles `clamp(26px, 2.2vw + 8px, 38px)`, FAQ summary 19 px, all Erode 600.
- Body 17 / 1.6 Inter 400. Lead `clamp(17px, 1.3vw, 19px)`, sub 18 px in `--mut`. Caption 13 px. Fine print 15 px.
- Eyebrow: Inter 700, 12 px, uppercase, tracking 0.16em, `--mut`. Tag line (hero): Inter 600 15 px in green with a small yellow parallelogram.
- Every h1 and section h2 carries the short red underline: 56 x 4 px, 16 px under the heading.
- Drawing annotations: Inter 600, 8 to 11 drawing units, uppercase, tracking 0.09em, `--mut`.

## Layout and spacing
- Container `min(100% - 2 x gutter, 1240px)`, gutter `clamp(20px, 4.5vw, 64px)`. 12 column grid, 24 px column gap. Nav height 72 px, content starts below it.
- Desktop (1024 and up): hero text columns 1 to 5, sticky map columns 6 to 12. Story: sticky stage columns 1 to 5, flow columns 7 to 12. Phones and tablets stack, mobile first (2026-11-14): hero text first, then the map in the flow (not sticky, one finger scrolls the page over it until it is zoomed); the build stage is sticky under the nav (drawing at most 26svh) only beside the six build steps and is released after stage 6.
- Sections are one screen tall on desktop (`min-height:100svh`, content centred), 56 px top and 24 px bottom padding when stacked. Panel padding 20 px (12 px stacked). Heading to body 18 px, body to object 24 to 30 px.
- Panels: `--mist` ground with the sunburst outline cropped in the top right corner, no radius, no border. Cards and chips: 2 px `--line` border, 6 px radius.

## Brand devices
- Flag stripe, always in this order: yellow, red, green. Used as the progress bar under the nav (fills with the scroll), the lid of the map sheet, the fascia band of the shed, canopy and roof edges in drawings, and the footer top edge. File `/brand/flag.svg`.
- Sunburst (24 tooth, `src/lib/burst.mjs`): outline mist in panel corners, filled badges for distances, steps and the approval stamp.
- Logo badge sits on the shed sign board, the gate beam and the map pin. The logo is never changed.

## Buttons and links
- Primary `.b--g`: green fill, white text. Secondary `.b--o`: 2 px green outline, green text, fills green on hover. Ask `.b--y`: yellow fill, ink text.
- 52 px tall (44 px in the nav, 40 px inside the shutter block), 24 px side padding, 6 px radius, Inter 600 16 px, icon 20 px with 10 px gap. Press feedback `scale(.97)` 160 ms. Hover colour change 160 ms.
- Text link `.more`: green, 600, 2 px yellow underline, arrow nudges 4 px on hover.
- Focus ring 3 px green with 3 px offset (yellow on the dark footer). Touch targets at least 44 px.

## Copy rules for the page
Short, plain, confident lines. No hedging or legal-sounding disclaimers on the page ("it is not a promise that", "subject to", "illustrative"). Only claims on the owner's allowed list (knowledge file). Nothing about water, security, permitted uses or price. No brand names. Taglines adaptive, one per creative.

## Motion rules
- Scroll drives the story. Position equals progress: no time easing between stages, fully reversible. Primary engine is CSS scroll-driven animation (`animation-timeline` on a named view timeline, `animation-range` in `svh`); a small fallback scrubs the same keyframes through motion's `scroll()` where unsupported. `prefers-reduced-motion` shows the finished drawing, the open shutter, a static map.
- Only `transform`, `opacity`, `clip-path` and `stroke-dashoffset` animate. No bounce, no spring, no blur, no glow, no floating, no uniform fade-up.
- Strokes draw (`pathLength=1`, dash offset 1 to 0), cladding wipes in with clip-path from the side it is fitted, the shutter lifts with a translate inside a clip. Each part has its own start and end inside its stage, so parts overlap and settle.
- Text steps sit beside the drawing: each step brightens as its stage completes (the step centre meets the viewport centre on desktop), then dims to make way for the next.
- One-shot interface motion (finder text swap, ask button) uses `motion/mini`, 280 ms, ease `cubic-bezier(.23,1,.32,1)`. Map zoom lerps with a 70 ms time constant (170 ms for phase fly-to). Easings: out `cubic-bezier(.23,1,.32,1)`, move `cubic-bezier(.77,0,.175,1)`.
- Map controls: wheel gain 0.0045 per pixel of delta (about 1.6x per mouse notch), pinch exponent 1.6, zoom 0.9x to 10x, plus, minus, reset, double click or double tap to zoom 2.6x on the pointer, pan clamped to the content.

## Drawing style: the architect's ink drawing (every illustration)
Illustrations are drawn as sheets by a good architect, calm and premium, never cartoons.
1. **Line**: hairline monoline, about 1.25 px on screen at any size (`--sw` is set from the rendered size by `home.mjs`; default 1.6 units). Ink `--ink` for outlines, #374151 for secondary members, #9CA3AF for ribs, hatching and leaders. The ground line is 1.5 x. Nothing thicker than 2 px. Round joins, butt caps. Never `vector-effect:non-scaling-stroke` with dash drawing (it breaks `pathLength`).
2. **Views**: orthographic elevations and plans (the shed in gable end elevation, the truck in side elevation, the plot in plan, the layout sheet in plan). Light isometric allowed, not used yet.
3. **Accuracy**: a real steel PEB shed (tapered columns, rafters with depth, purlins, girts, sheeting rhythm of vertical ribs, roller shutter with guide rails, slats, hood and bottom bar, personnel door, sign board). Trucks are believable side elevations: chassis rails, box body with stanchions, cab-over cab with window and door, wheel arches, tandem rear axle, tyre, tread and rim rings. No faces, no oversized wheels.
4. **Drafting devices**: ground line with hatch ticks, concrete hatch in footings, dimension and leader lines, level marks (GL 0.00, plinth, eave, ridge), small uppercase annotations (50 FT RCC ROAD, RCC FOOTING, STEEL PORTAL FRAME, WALL SHEETING), pegs with yellow caps, a datum triangle.
5. **Colour**: sparse spot fills only. Green roof sheeting, yellow roller shutter and one yellow peg cap, the flag stripe as a fascia band (the one place red appears besides the stripe), white sign boards, a pale green tint for tree canopies. Walls are open line work, not filled.
6. **Files**: `src/components/Shed.astro` (stage, ghost plan, finale), `Truck.astro`, `Vig.astro` (gate and fuel pump, shop row, layout sheet). Classes `.o .o2 .o3` (lines), `.fy .fr .fg .fw .fk .fk2 .fk3 .fg2 .fy2` (spot fills), `.tx` (annotation), `.lb` (labels hidden in the finale and on phones), `.k` plus `.kd .kfade .kwipe .kwipeL .kwipeR .kwipeD .kout .klift .ktruck` (scrubbed parts).
7. **Wording**: levels and labels are drafting conventions, not claims about the park. Only "50 FT RCC ROAD" is a park claim and it is on the owner's list.

## How a scrubbed part is declared
`<path class="o k kd" style="--i:2;--s:.1;--e:.45">`: `--i` is the stage (0 to 5, spacing `--hs` svh), `--s` and `--e` are the start and end inside the stage window (`--dw` svh wide, starting `--d0` svh after the stage start). Desktop `--d0:50 --dw:35 --hs:70`, stacked layouts `--d0:32.5 --dw:27 --hs:55`. For the visit shutter set `--tl:--fin;--r0:95;--rw:100;--rh:0` inline. Section drawings use `.vk` with `--s` and `--e` on their own view timeline `--v`.
