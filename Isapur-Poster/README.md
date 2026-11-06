# Isapur Industrial Park poster (editable)

Recreated from the supplied poster image (`01_Source/poster-reference.webp`, supplied by the owner, 2026-11-06). Original implementation: all shapes and text are rebuilt, only the warehouse render is the supplied pixels.

## Folders
| Folder | What |
|---|---|
| `01_Source/` | Supplied poster image and supplied logo JPEG. Never edited. |
| `02_Logo/` | `iip-logo.svg` (vector trace of the JPEG, 4 layers: yellow, red, green, outline) and `iip-logo.pdf` |
| `03_Design/` | `00_LATEST_...pdf` (print), `01_LATEST_...svg` (master, live text), `02_LATEST_preview.png`. Older versions are numbered `_archive/v01..` (higher number = newer backup). |
| `fonts/` | Montserrat and Inter, static cuts plus variable masters (SIL OFL) |
| `_build/` | Scripts that generate the logo trace, the static fonts and the poster |

## Fonts (no fallbacks in the file)
| Role | Font | Weight |
|---|---|---|
| ISAPUR | Montserrat | ExtraBold 800 |
| INDUSTRIAL PARK, stat values, phone | Montserrat | Bold 700 (phone 800) |
| Stat labels | Inter | Medium 500 |
| Feature labels | Inter | Regular 400 |

Install the files in `fonts/` before opening the SVG. The SVG names only `Montserrat` and `Inter`.

## Open it
VectorCraft (installed from github.com/storytold/vectorcraft v0.21.1, SHA256 verified): File, Open, `03_Design/isapur-industrial-park.svg`. Layer ids: `logo`, `title`, `subtitle`, `stats`, `hero-photo`, `feature-icons`, `features-text`, `cta`, `corner-stripes`.

## Change log
- 2026-11-06: halo and dark outline merged into ONE continuous stroke (a 22-point die-cut star, id `halo`, fitted to the supplied logo). Feature 3 is now Highway Connectivity (truck icon) and feature 4 Drainage (channel and drop icon); labels corrected. Originals kept as `*.before-*.svg`. `03_Design/isapur-industrial-park.svg` is hand-edited and is now the master; `_build/build_poster.py` only reproduces the first version. Re-apply with `_build/fix_halo_icons.py`, re-render with `_build/render.py pdf`.

- 2026-11-06 (later): feature 3 is now "Delhi-Meerut Expressway, 4 km away" (straight-line from the map pin, drive distance still to be odometer-checked). Feature 4 is now "Waste Water Drainage" (owner states there is a naala behind the park for disposal). No public source found for this naala or for effluent rules at this site; file the owner's own evidence (site photo of the naala, plot plan, any UPPCB or UPSIDA consent) before printing. Previous version kept as `isapur-industrial-park.before-industrial-drainage.svg`.

- 2026-11-06 (later still): top row now has 5 stats; "4 km away / Delhi-Meerut Expressway" added in the same style as "50 ft. Wide / RCC Roads" (gantry-sign icon, `icon-expressway`). Bottom feature 3 is now "Highway / Connectivity". Backup `isapur-industrial-park.before-expressway-stat.svg`; script `_build/add_expressway_stat.py`. The 4 km is straight-line, confirm by odometer.

- 2026-11-06 (round 3): fixed SVG that would not open in strict editors (duplicate attributes, `_build/fix_round3.py`). Bottom row now: Manufacturing, Power, Highway Connectivity, Waste Water Drainage, Street Lighting (new lamp icon), Planted Greenery. Straight-line note removed from the expressway stat. Files renumbered, PDF first.

## Honest limits
- The logo is a trace of a JPEG, not the designer's original vector. Edges are clean, the thin die-cut outline of the star is not included. Use the original vector for very large print if it exists.
- The warehouse image is raster (embedded WEBP crop). It cannot be vectorized meaningfully.
- Montserrat and Inter are the chosen fonts, not the poster's original (a rounder geometric face); text widths differ slightly from the reference.

## Log
| What | Tool | Output |
|---|---|---|
| Logo vectorization | vtracer 3.x plus palette snapping and smoothing (`_build/trace_logo.py`) | `02_Logo/iip-logo.svg` |
| Poster | Python generator (`_build/build_poster.py`) | `03_Design/isapur-industrial-park.svg` |
| PDF and preview | vectorcraft-cli | `03_Design/*.pdf`, `preview-vectorcraft.png` |
| Static fonts | fontTools instancer (`_build/make_*_static.py`) | `fonts/*.ttf` |
