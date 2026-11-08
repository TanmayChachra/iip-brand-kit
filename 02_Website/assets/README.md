# Website assets (fresh, generated in code from the brand kit)

Source of truth: `assets/build_assets.py` (SVG) and `assets/render_assets.py` (WEBP, PNG, favicons, contact sheet). Rebuild: `python 02_Website/assets/build_assets.py` then `python 02_Website/assets/render_assets.py`. SVG sources are in `assets/svg/`, web outputs in `site/public/img/` (favicons in `site/public/`). Preview of everything: `assets/_contact-sheet.png`.

Brand rules followed: kit colours and fonts (Montserrat, Inter outlined), badge from the kit unchanged, thin tri-colour flag, 22 point sunburst, stroke 2.4 on spot art. Nothing is a photo of the park. All scenes are illustrations and carry "Illustrative, not to scale" or "Schematic" where they could be mistaken for the site. Distances come only from `00_ISAPUR_KNOWLEDGE.md` (4.7 km driving to the expressway on-ramp, 3.9 km straight-line, Modinagar bus stand 11.4 km driving, Hapur bus stand 13.4 km driving). No prices, no invented plot sizes (only "From 300 sq yards").

| File (public/img/) | What | Size | Use |
|---|---|---|---|
| `hero-illustration.svg` / `.webp` | Flat scene: sheds, 50 ft road with yellow dashed line, trees, street lights, truck, sunburst sky | 18 KB / 19 KB | Home hero (desktop) |
| `hero-illustration-mobile.svg` / `.webp` | 780 x 700 crop of the same | 18 KB / 10 KB | Home hero (390 px wide) |
| `plot-layout-schematic.webp` | Isometric layout, labelled illustrative | 44 KB | Industrial plots page |
| `location-diagram.webp` | Route diagram with the verified distances | 36 KB | Location page and landing pages |
| `spot/spot-*.svg` (6) | roads, street lighting, planted greenery, plots, site visit, documents | 1 KB each | Section illustrations, amenities |
| `cards/card-*.svg` (3) | plot from 300 sq yards, site visit, layout map | about 27 KB each | Plots page cards |
| `divider-flag.svg`, `divider-diamonds.svg` | Thin tri-colour flag, diamond row | 1 to 2 KB | Section dividers (stretch to width) |
| `textures/sunburst-tile(.svg, -light)`, `road-lanes-tile.svg`, `plot-plan-tile.svg`, `halo-rings.svg/.webp` | Low opacity tileable textures (light variant for green bands) | under 3 KB, halo webp 13 KB | CSS `background-image` repeat |
| `seal-badge-on-sunburst.svg` | Badge on a sunburst seal | 23 KB | Stat seals, about page |
| `og/og-home|plots|location|blog.png` | 1200 x 630 social cards (PNG on purpose, some crawlers reject WEBP) | about 82 KB each | `og:image` |
| `../favicon.svg`, `favicon-32.png`, `apple-touch-icon.png`, `icon-192.png`, `icon-512.png` | Badge on a canvas, badge itself unchanged | 1 to 23 KB | Head tags and manifest |
| `slots/` (SVG sources in `assets/svg/slot-*.svg`) | Photo placeholders 16:9, 4:3, 1:1 | n/a | Use CSS boxes on the site, swap for real photos later |

Heavy outlined-text SVGs (location diagram 352 KB, layout 172 KB, slots) stay in `assets/svg/` only. The site ships their WEBP versions.

Not done: the optional ChatGPT concept art (code generated SVG was cheaper and more on brand). Real photos replace the illustrations in the hero once the shoot happens.
