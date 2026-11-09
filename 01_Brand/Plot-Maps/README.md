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
