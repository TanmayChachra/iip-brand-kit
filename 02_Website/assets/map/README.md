# Map artwork (OpenStreetMap, no AI)

Verdict: real, accurate map of the area around Isapur Industrial Park in brand colours, SVG with outlined text plus WEBPs. Built 2026-11-08.
Evidence: roads, rail, water, landuse and place nodes from the Overpass API (cache in `cache/`), route geometry from the OSRM public demo router, labels only from OSM tags. Contact sheet checked, SVG parsed, no live text, no em dashes.
Caveat: OSM only carries the ref MDR148W for the road at the park, the name "Hapur-Modinagar Road" comes from the project knowledge file and Google Maps. The OSRM route is about 4.5 km and 5 min; the plate says 4.7 km by road (about 8 min), the figure measured on Google Maps on 2026-11-06 (`01_Brand/Brand-Kit/research/driving-distances.json`). Modinagar 11.4 km and Hapur 13.4 km are driving distances to the bus stands from the same file. Direction arrows use the OSM town nodes.

Credit for the website footer: **Map data from OpenStreetMap contributors, ODbL (https://www.openstreetmap.org/copyright)**.

Files (in `02_Website/site-v2/public/img/map/`): map-park.svg (1800x1200, editable), map-park.webp (1800 wide), map-park-tall.webp (1200x1500, mobile), map-park-sm.webp (800 wide).
Rebuild: `python 02_Website/assets/map/build_map.py` (uses `cache/`, no network). Refresh data: delete a cache file and run `ovp.py` helpers (polite, few requests).
Style: sage ground, white roads with hairlines, built-up tint cream-yellow, expressway yellow with green casing, route green, badge from the kit unaltered at the Phase 1 pin (28.7809, 77.6559), on-ramp at OSM way 935414874 (28.8014, 77.6205).
