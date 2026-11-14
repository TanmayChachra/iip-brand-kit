# Plot maps (Phase 1, Phase 2, Phase 3, Phase 1 extension)

Reusable brand asset for future projects, in particular an SVG plot selector add-on. Not tied to the website: the website may use them later.

## Inputs (from the owner, see TODOS.md)
- Plotting maps of Phase 1, Phase 2, Phase 3 and Phase 1 extension (images or PDFs) into `source/`. Their colour coding does not matter, only the boundaries.
- The Google Earth project (link, or exported KML or KMZ) with the phase boundaries. A KML gives exact boundary coordinates, so each phase outline can be drawn geo-accurately straight from it.
- Satellite images: I do not scrape Google Earth or Google Maps imagery (licence). Screenshots or exports from the owner's own Google Earth project are fine, or the KML alone.

## Output
- `svg/phase-1.svg`, `phase-2.svg`, `phase-3.svg`, `phase-1-extension.svg` and `svg/all-phases.svg` (all together, geo placed).
- One group per phase (`<g id="phase-1">`), one `<path>` per plot with a stable id (`p1-001`, `p2-014`, `p1x-007`), `data-plot`, `data-phase`, `<title>` for accessibility. Only outlines and a plot number, brand colours, no inherited map colours. Every plot is its own unit so a selector can colour, hover and click it.
- `data/plots.json`: id, phase, plot number, area in sq yards (blank until the owner supplies it), status (blank), centroid, bounding box. `data/phases.geojson` from the KML.
- Tracing: phase outlines from KML; plot lines traced from the supplied plotting maps (vector trace plus manual cleanup), snapped to the phase outline. I check each SVG against the source image by overlay and report mismatches.

## Not now
The plot selector UI itself is a separate future project that will read these files.

## Built from the owner's layout PDFs (2026-11-12)
Produced by `build_plots.py` (`python build_plots.py`, needs pymupdf and shapely; reads the three layout PDFs from the owner's Drive folder, read only, nothing copied here). It writes `svg/phase1.svg`, `svg/phase2.svg`, `svg/phase3.svg` and `data/plots.json` (id, phase, plot number, `area_sqyd`, `area_method` sheet or computed, `area_review`, status blank, centroid, bbox, in SVG units). The Phase 1 PDF already contains the Phase 1 extension (the E plots at the top) as part of the one Phase 1 map. It is not sold separately, so nothing is tagged or split, and `all-phases.svg`, `phases.geojson` and the geo placement are still open (they need the KML). 

Each SVG has one `<path class="plot" id="p1-001" data-plot data-phase>` per plot with a `<title>`, a plot number text, grey road shapes (Phase 1 and 3), road labels with widths, and a north arrow rotated to the true north shown on the source sheet (the sheets are not north-up). Brand tokens only, flat light ground, no imagery. No owner names, khasra numbers or contact data are carried over. Method: plot lines from the vector PDF, tiny gaps closed, one face per label.

| Phase | Plots | Areas in plots.json |
|---|---|---|
| 1 | 218 | all computed |
| 2 | 147 (D15 & D16 is one shape, A48 has 1st and 2nd) | 4 from the sheet (D17 to D20), 143 computed |
| 3 | 23 | all 23 from the sheet table (total 14320.49 sq yd matches) |

Areas: drawing scale measured from dimension text (feet-inches) matched to plot edges: 0.4480, 0.5768 and 0.9218 PDF units per foot for Phases 1, 2, 3 (spread under 0.5 percent over 709, 431 and 84 matches; 50'-0" roads agree). Computed area = polygon area / scale^2 / 9. Validation against sheet areas: Phase 3 mean absolute error 0.08 percent (max 0.3), Phase 2 four plots 0.5 percent (max 1.5). `area_review` is true outside 250 to 3000 sq yd: 37 in Phase 1 (mostly the small S and B corner plots, plus E28 to E31), 20 in Phase 2 (S1 to S14 strips, A22 to A24, C10, A48(2nd), and D15 & D16 at 8553, a merged shape with an approximate outline), 1 in Phase 3 (plot 18, 229.9 per the sheet). Hover title on each plot shows the area; computed ones say approx.

Known gaps:
- Phase 1: B-3(1) and B-3(2) now built (about 273 sq yd each). Still left out: 30 (outline open, face leaks into the road) and S-4(II), S-1(II) (their labels sit on top of S-4(I) and S-1(I), same shape, so likely duplicate text, not separate plots; check with the architect). Some blank plot shapes with no readable label (for example beside 29 and 31) are not exported. The small S and B-25 plots at the central junction are tiny and need a check against the sheet.
- Phase 1 plot 30 is now built (boxed between 31 and 29, its outline is open in the PDF); the old gap note for 30 no longer applies.
- Phase 2: D15 & D16 and D38 sit behind a dotted boundary with gaps, so their outlines are approximate (rounded to the nearest closed boundary).
- Roads: see the restyle section below (Phase 2 roads are computed, not drawn on the sheet).
- Phase 3 areas are read from the rendered table (it is drawn as outlines, not text); each row checks out (sq ft / 9 = sq yd).
- Outlines are checked by eye against the PDF render, not by overlay.

## Restyle to website quality (2026-11-12)
`python build_plots.py` now writes the restyled maps. Look: light ground, plots filled by block in tints of the brand green, yellow and red plus neutrals (thin white gutters from a small inset, soft stroke), plot number in ink, roads as filled grey bands with white labels, legend at the foot, north arrow (true north of the source sheet), no title block or borders. Hover title keeps plot number and area. Fonts are named Inter and Montserrat with fallbacks (not embedded).
- Labels: every plot has its number, sized to fit (horizontal, or along the long axis). Plots too small to hold it (S strips, junction corner plots) get a small leader label outside.
- Roads: Phases 1 and 3 use the sheet's grey fills, Phase 2 roads are computed (morphological closing of the gaps between plots plus the 50 ft Main Road strip), every label is as the PDF says (widths, MAIN ROAD, EXISTING COLONY ROAD, CHAKH ROAD). Public roads are drawn darker from the PDF edge lines: Phase 2 MODINAGAR - HAPUR ROAD with TO HAPUR and TO MODINAGAR arrows, Phase 3 ROAD with TO BHADOLA and TO HAPUR ROAD. The Phase 1 sheet shows no public road or gate, so none is drawn; Phase 3 shows no gate either.
- Phase 1 letter-spaced road labels are placed from a table (`FRAG1`) read by eye (50'-0" everywhere, 40'-0" on the two diagonals).
- Shops (owner fact): plots under 250 sq yd are `plot_type` "shop" in `plots.json` and the SVG (`data-type`, distinct fill, legend "Commercial shops"). `area_review` is now only 250 to 300 sq yd (borderline) or over 3000. Nothing is hidden.
- `snapshots.py` writes `img/phase1-snapshot.webp`, `phase2-snapshot.webp`, `phase3-snapshot.webp`: clean crops of the PDF pages (no title block, quality 80, long side 2000 px). These are the faithful fallback.
- Weak spots: the Phase 2 D15 & D16 and D38 outlines are approximate; Phase 1 S-1(II) and S-4(II) are not drawn (likely duplicate labels); Phase 2 road ends are cut at plot edges; unlabelled land and "OTHER'S PROPERTY" are left blank; tiny junction plots in Phase 1 are cramped.

Context (owner, 2026-11-12, never shown): the whole E sector of Phase 1 is the Phase 1 extension. It is drawn as ordinary Phase 1 plots, no separate label or flag.

## Owner corrections to Phase 1 (2026-11-13)
All are explicit overrides in the `OVERRIDES` section of `build_plots.py` (geometry read from the vector PDF line and arc end points), applied after the automatic trace, so they survive regeneration. The E sector is not flagged as the extension. Plot ids are renumbered by sort order (3 plots added), so p1-ids after B-27(I) moved by up to 3; match on `plot`, not on id. `phase1-snapshot.webp` is a crop of the PDF page, so it is unchanged. New named road paths sit in `<g id="roads">`: `chakh-road-1`, `chakh-road-2` (same fill as other roads, `data-road="CHAKH ROAD"`, hover title), labels in `road-labels`.

| # | Item | Status | Detail |
|---|---|---|---|
| 1 | CHAKH ROAD behind D4, D5, D6, D8 up to C12 | done | Thin strip (about 4 units, 9 ft) between the sheet boundary (orange line) and the plot edges: left of D5 and D4, behind D5 to D14, on along the top of the C block to the C-12 corner. The sheet labels it "CHAK ROAD" (tiny text). Drawn as `chakh-road-1`, small labels |
| 2 | E36 quadrilateral | done | Red mark is a tower, not drawn. Area 418.9 to 480.6 sq yd |
| 3 | S-1(I) | done | Right arc replaced by the straight diagonal (453.1,702.1) to (460.4,691.4); plot_type shop (forced, 135.4 sq yd) |
| 4 | C 8 A, C 8 B, plot below C9 | done | Both were never drawn (labels "C- 8A", "C- 8B" have a space, not matched) and stay out; their area stays blank. Thin plot below C-9 was missing: added as C-9(I) (63.2 sq yd, shop by size). Upper plot stays "C-9" |
| 5 | S-4(I) | done | Left arc replaced by the diagonal (481.4,736.1) to (488.9,725.1); shop (forced, 146.6 sq yd) |
| 6 | B-27(II), B-27(III) | done | Added left of B-27(I), 251.7 and 460.0 sq yd (II is borderline, `area_review`) |
| 7 | Second CHAKH ROAD | done | `chakh-road-2`: cut from the existing road fill, below B-46 to B-32 (starts at B-46, x 296), up the right side of B-32 and B-31 (3 to 5 units wide), then right along the top of B-51 to B-54. Label added |
| 8 | B-34 | done | The label underline left a hole in the traced face and the drawn plot stopped halfway (y 839 to 867). Now the full quad to the red line, 408.5 sq yd |

Not done and why: S-1(II) and S-4(II) stay out (labels sit on S-1(I) and S-4(I), likely duplicates, no owner answer yet).

## Owner corrections to Phase 2, Phase 3 and Phase 1 shops (2026-11-13)
All are explicit entries in `OVERRIDES` (keys 1, 2, 3) of `build_plots.py`, applied after the automatic trace. Plot ids are renumbered by sort order (A48 renamed), so match on `plot`, not on id. `phase2-snapshot.webp` is unchanged (PDF crop).

| # | Item | Status | Detail |
|---|---|---|---|
| 1 | Staircase between S7 and S8 | done | Not a plot, left as blank ground (no number). Road in front rebuilt (see 2 and 3) |
| 2 | Road jagged in front of S14 | done | Main Road below A55 is now one straight polygon (`main_road`): sheet boundary line on the left, A56 to A59 and the S strips on the right |
| 3 | Road between A56 and A55 | done | Same polygon, joined to the road above |
| 4 | CHAKH ROAD behind A1 to A9 and behind A59 to A44 | done | `chakh-road-1` (between the two dotted lines left of A9 to A1), `chakh-road-2` (right of A59 to A47 over the A55/A56 gap, then along the foot of A47 to A44). QUESTION: the PDF letters on the A9 to A1 strip read NALI, not CHAKH; drawn as chakh as the owner said |
| 5 | A48 labels | done | A48 (I) and A48 (II) |
| 6 | C10 colour | done | Plotted fill like the C block |
| 7 | D15 & D16 | done | Left edge on the line right of D3, D6, D9 (near vertical), top, right and bottom edges as the PDF red lines. Area now 8428.6 sq yd (old 8553.3), computed |
| 8 | Nali (drains) | done | `<g id="nali">`, 5 thin blue-grey lines labelled NALI: along the top of D15 & D16, between D15 & D16 and D38, right of D17, left of A47 (was unmarked), right of A44. Legend "Nali (drain)". The dotted strip right of A56 to A59 also carries NALI letters in the PDF (drawn as chakh) |
| 9 | D37, D38 | done | Exact PDF outlines (D38 flat bottom on y 252, D37 below it) |
| 10 | CHAKH ROAD behind A47 | done | In `chakh-road-2` |
| 11 | Not commercial | done | C10, A48 (II), A22, A23, A24 forced `plot` (`plotted`). Phase 2 shops are now only S1 to S14 (very small, owner confirmed). Phase 3 plot 18 forced `plot` |
| 12 | Chakh visibility | done | Shared style: earthy fill (`CHAKHC`), darker edge, bold letter-spaced label, legend entry "Chakh road" in Phase 1 and 2 (Phase 3 has no chakh road). No geometry change in Phase 1 or 3 for this |

Phase 3: sheet table re-checked, all 23 `area_sqyd` equal the owner's table exactly (plot 12 was 841.538, now 841.536). Hover title shows the area rounded to whole sq yd.

Phase 1 shop rule (owner): only S block plots are shops, every other plot is `plot` whatever its size. Changed to plot: 11A, 11B, 12, B-6, B-7, B-8, B-10, B-11( I ), B-22A, C-15, B-49, B-50, B-21(I), B-25(II), C-16, B-24, B-25(III), E28 to E31, C-9(I). Shared edges now meet exactly: S-5 on B-24, S-6 and S-7 on each other and on B-24, S-4(I) on B-21(II) (S-5 area 86.7 to 115.6, S-7 13.5 to 17.3 after reading the true lines). QUESTION: the owner wrote S-4 and S-7; S-7 sits next to S-6 and S-5, S-4(I) is across the road, so S-6 and S-7 were joined.

RESOLVED (2026-11-13): the Phase 1 triangular end beside the red E. LINE road. B-23 and B-22A are labelled plots in the PDF and stay as they are. The three unlabelled triangles bounded by the thick black lines (right of B-22A, 44' and 56'-6"; below B-22A, 32'-6" and 51'-6"; below B-23, 37'-3" and 59'-3") are commercial shops, drawn as `Shop 1`, `Shop 2`, `Shop 3` (plot_type shop, shop fill, legend "Commercial shops", no number text, hover title says Shop; 86.5, 69.9 and 95.5 sq yd computed). Shared edges meet B-22A and B-23 exactly.

## Chakh road, one shared style (2026-11-13)
The Phase 1 look is now the single chakh style, defined once in `build_plots.py` (`CHAKHC` fill, `CHAKHS` edge .3 wide, `CHAKHFS` 3.0, class `ck`): earthy fill, darker edge, no dash, label "CHAKH ROAD" bold, letter-spaced, ink with white halo, 3.0 px, centred across its band (snapped to the band's cross section). Phase 2 labels were white on the band or off-centre, and Phase 1 mixed 2.8, 3.0 and 4.6 px; all now identical. Phase 3 has no chakh road. Phase 2 `chakh-road-2` gained the strip in the gap between A55 and A56 (Main Road edge to the band, from the PDF where the dotted lines cross the gap), joined to the band; Main Road untouched. No other geometry, plot types, labels or nali changed.

## Close-out, Phase 1 maps v1.0 (2026-11-13)
All three maps are DONE (v1.0, 2026-11-13). The `OVERRIDES` section of `build_plots.py` is frozen: no further geometry edits unless the owner reopens a map.

| Map | Status | Version | Date |
|---|---|---|---|
| Phase 1 (includes the extension) | done | v1.0 | 2026-11-13 |
| Phase 2 | done | v1.0 | 2026-11-13 |
| Phase 3 | done | v1.0 | 2026-11-13 |

Final counts (from `data/plots.json` and the SVGs):

| Phase | Plots (all drawn shapes) | Shops | Nali | Chakh roads |
|---|---|---|---|---|
| 1 | 225 (222 numbered, 3 unnumbered shops) | 19 | 0 | 2 |
| 2 | 147 | 14 | 5 | 2 |
| 3 | 23 | 0 | 0 | 0 |

Changelog: 2026-11-13, v1.0. Phase 1 triangular end drawn as 3 unnumbered commercial shops (`Shop 1` to `Shop 3`), README TODO resolved, status written to `data/MAPS-STATUS.json`. `plot` values `Shop 1` to `Shop 3` carry no number on the map; match plots on `plot`, not on id.

S-1 (II) and S-4 (II) removed, duplicate labels in the architect PDF, owner decision 2026-11-13. Verified absent from svg/phase1.svg and data/plots.json.

## Owner corrections round 4 (2026-11-13)
All in `OVERRIDES` of `build_plots.py`. Plot ids after C-8A shift by 2 in Phase 1 (match on `plot`).
- Phase 1 C-8A (100.6 sq yd) and C-8B (745.8 sq yd) added left of C-9 and the thin plot below it (lines from the PDF), plot_type plot. C-9 stays one plot, no suffix. QUESTION: the thin plot below C-9 is still named C-9(I) (owner's wording read as: upper plot is C-9, already true); say if it needs another name.
- Chakh roads, one style in Phase 1 and 2: same fill and stroke, label white on the band, 2.6 px, letter-spaced, centred, spaced about 75 to 130 units. New bands (before they were plain road grey with a label): strip below D4 to D20 over the 50 ft crossing, left strip beside 45 to 36 (joins the top-left band), strip below 36 to 33, strip B at x 266 to 296 (joined to the bottom band). Geometry of the strips beside D5, D4 and behind D4 to D8 unchanged.
- Phase 1 legend: Block E entry removed. E plots use the standard plot fill (legend "Industrial plots", was "Plots 1 to 48"); `data-block="E"` kept as data only.
- Road between C and E: checked against the PDF. It is 50 ft (22.4 units) and flares to 60 ft (label "60'") beside E1 and E52 at the junction, same road fill and styling as the other 50 ft roads. Geometry left as the PDF shows it.
- Phase 2: the strip left of A1 to A9 has two dotted lines. NALI added behind A8 to A14 (`nali-6`, inner side, y 273 to 410). CHAKH behind A1 to A9, full width below A8, outer half beside the nali. PDF letters: CHAKH ROAD from A1 to about A7, NALI around A9 and A8, which agrees. There was no nali along A1 to A7 to remove. The other 5 nali are untouched.
