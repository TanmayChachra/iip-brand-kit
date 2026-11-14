"""Builds the two inline SVG assets of the v3 home page. Run: python scripts/build_home_assets.py (needs shapely).
1. src/assets/layout.svg.html (phase 2 only, unused by the page) from 01_Brand/Plot-Maps/svg/phase2.svg and data/plots.json
   (the architect layout drawing; plots get data-b = size band, data-a = area, no <title>, no style block, legend cut).
2. src/assets/region-map.json: inline SVG of the zoomed-out OpenStreetMap region (cache from 02_Website/assets/map/cache,
   fetched with ovp.py), plus pin positions in percent for HTML labels.
Map data from OpenStreetMap contributors (ODbL)."""
import json, math, pathlib, re
from shapely.geometry import LineString, box

HERE = pathlib.Path(__file__).resolve().parent
SITE = HERE.parent
ROOT = SITE.parents[1]
OUT = SITE / "src/assets"; OUT.mkdir(parents=True, exist_ok=True)
PM = ROOT / "01_Brand/Plot-Maps"

# ---------- 1. layout ----------
BANDS = [("b1", "300 to 500 sq yards", 285, 500), ("b2", "500 to 1000 sq yards", 500, 1000), ("b3", "1000 to 2500 sq yards", 1000, 2501)]


def band(p):
    if p["plot_type"] == "shop": return "shop"
    a = p["area_sqyd"]
    for k, _, lo, hi in BANDS:
        if lo <= a < hi: return k
    return ""  # under 285 (computed outlines, not claimed) and the merged D15 and D16 shape (8553, approximate outline)


def layout():
    plots = {p["id"]: p for p in json.load(open(PM / "data/plots.json", encoding="utf-8")) if p["phase"] == 2}
    s = open(PM / "svg/phase2.svg", encoding="utf-8").read()
    s = re.sub(r"<style>.*?</style>\n?", "", s, flags=re.S)
    s = s.replace('<g id="legend">', "<g id=\"legend\" display=\"none\">")
    s = re.sub(r'<g id="legend".*?</g>\s*(?=</svg>)', "", s, flags=re.S)
    s = re.sub(r'<rect x="113.4"[^>]*/>\n?', "", s, count=1)
    s = re.sub(r'<svg [^>]*>', '<svg class="lay" xmlns="http://www.w3.org/2000/svg" viewBox="113.4 -56.2 840.6 895" role="img" aria-labelledby="lay-t lay-d" preserveAspectRatio="xMidYMid meet"><title id="lay-t">Layout drawing of the park</title><desc id="lay-d">Architect layout drawing. Plots in blocks A to D with 50 ft wide main roads between them, small commercial shops, and the Modinagar-Hapur Road along the south edge. The size buttons next to it light up the plots in each size range.</desc>', s, count=1)
    cnt = {k: 0 for k, *_ in BANDS}; cnt["shop"] = 0
    seq = {}

    def fix(m):
        t = m.group(0)
        pid = re.search(r'id="(p2-\d+)"', t).group(1)
        p = plots[pid]; b = band(p)
        if b: cnt[b] += 1
        blk = p["block"]; n = seq.get(blk, 0); seq[blk] = n + 1
        t = re.sub(r'<title>.*?</title>', '', t)
        t = re.sub(r' data-phase="2"', '', t)
        t = re.sub(r' data-block="[^"]*"', f' data-k="{blk}" style="--n:{n}"', t)
        t = t.replace(' class="plot', f' data-b="{b}" data-a="{round(p["area_sqyd"])}" class="plot') if True else t
        return t
    s = re.sub(r'<path id="p2-\d+".*?</path>', fix, s, flags=re.S)
    # roads: stroke-draw classes. Dash length = longest subpath so the draw is smooth.
    def roadfix(m):
        i = m.group(0)
        return i
    # mark the road paths
    s = s.replace('<g id="roads">', '<g id="roads" class="rd">')
    s = s.replace('<path id="public-road"', '<path class="pub" id="public-road"')
    s = s.replace('<g id="labels">', '<g id="labels" class="lb">').replace('<g id="road-labels">', '<g id="road-labels" class="lb2">')
    s = s.replace('<g id="north">', '<g id="north" class="lb2">')
    s = re.sub(r' fill="#111827"', "", s)
    # road width labels are too small to read at page size: hide them (class rw); the public road label gets class pubL
    s = re.sub(r'<text class="rl( rx)?"( font-size="5.2")', lambda m: '<text class="rl rw' + (m.group(1) or '') + '"' + m.group(2), s)
    s = s.replace('<text class="rl" font-size="7.5"', '<text class="rl pubL" font-size="7.5"')
    # big block letters (readable at small size), placed at the median plot centre of each block
    import statistics
    blk = ""
    for k in "ABCD":
        c = [pp["centroid"] for pp in plots.values() if pp["block"] == k and pp["plot_type"] == "plot" and pp["area_sqyd"] < 3000]
        if c: blk += f'<text x="{statistics.median(x for x, y in c):.0f}" y="{statistics.median(y for x, y in c):.0f}">{k}</text>'
    s = s.replace("</svg>", f'<g class="blk" aria-hidden="true">{blk}</g></svg>')
    (OUT / "layout.svg.html").write_text(s, encoding="utf-8")
    # layout-bands.json (all three phases) is written by build_master.py; this phase 2 only file must not overwrite it
    print("layout (phase 2 only, not used by the page)", len(s), "bytes", cnt)
    # longest road subpath for the dash
    mx = 0
    for d in re.findall(r'<path[^>]* d="([^"]+)" fill="#7B8390"', s):
        for sub in d.split("M")[1:]:
            pts = [tuple(map(float, q.split())) for q in re.split(r"[LZ]", sub) if q.strip()]
            mx = max(mx, sum(math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)))
    print("longest road subpath", round(mx))


# ---------- 2. region map (v3 round 4: premium cartography) ----------
# Geometry only in the SVG (ground, built-up, water, road hierarchy, on-ramp route as a masked dashed path). Labels, chips, the
# expressway label and the badge are HTML on top (crisp at any width), placed by percent from the numbers computed here.
# Cache: region_major, roads, region_land (landuse, water), region_minor (tertiary, unclassified), fetched with ovp.py.
from shapely.geometry import Point, Polygon
from shapely.ops import nearest_points, unary_union, linemerge
W, H = 1000, 860
LAT0, LON0, KM = 28.7845, 77.676, 24.0
SC = W / KM
P = lambda lat, lon: ((lon - LON0) * 97.5 * SC + W / 2, (LAT0 - lat) * 111.2 * SC + H / 2)
PARK = (28.7809, 77.6559); RAMP = (28.8013952, 77.6204507)
MOD = (28.8320713, 77.5770873); HAP = (28.7299677, 77.775499)
CACHE = ROOT / "02_Website/assets/map/cache"
clip = box(-30, -30, W + 30, H + 30)
J = lambda f: json.load(open(CACHE / f, encoding="utf-8"))["elements"]
G = lambda e: [(c["lat"], c["lon"]) for c in e["geometry"]]
T = lambda e: e["tags"]
XOFF = 165  # label distance along the expressway from the on-ramp, in map units


def path(geoms, tol=0.9, dp=1):
    out = []
    for g in geoms:
        if len(g) < 2: continue
        ls = LineString([P(*c) for c in g]).intersection(clip)
        if ls.is_empty: continue
        for part in (ls.geoms if hasattr(ls, "geoms") else [ls]):
            if part.geom_type != "LineString": continue
            c = list(part.simplify(tol).coords)
            out.append("M" + "L".join(f"{x:.{dp}f} {y:.{dp}f}" for x, y in c))
    return " ".join(out)


def polys(els, tol=2.6):
    out = []
    for e in els:
        g = e.get("geometry") or []
        if len(g) < 4: continue
        pg = Polygon([P(c["lat"], c["lon"]) for c in g])
        if not pg.is_valid: pg = pg.buffer(0)
        pg = pg.intersection(clip)
        if pg.is_empty: continue
        for part in (pg.geoms if hasattr(pg, "geoms") else [pg]):
            if part.geom_type != "Polygon" or part.area < 40: continue
            c = list(part.simplify(tol).exterior.coords)
            out.append("M" + "L".join(f"{x:.0f} {y:.0f}" for x, y in c) + "Z")
    return " ".join(out)


def region():
    d = J("region_major2.json"); near = J("roads.json"); land = J("region_land.json"); minor = J("region_minor.json")
    sel = lambda f, src=d: [G(e) for e in src if f(T(e))]
    res = polys([e for e in land if T(e).get("landuse") == "residential"])
    ind = polys([e for e in land if T(e).get("landuse") in ("industrial", "commercial", "construction")])
    farm = polys([e for e in land if T(e).get("landuse") in ("farmland", "orchard", "meadow", "forest") or T(e).get("leisure") == "park" or T(e).get("natural") in ("wood", "scrub")])
    wat = polys([e for e in land if T(e).get("natural") == "water" or T(e).get("landuse") == "basin"])
    wl = path([G(e) for e in land if T(e).get("waterway") in ("river", "canal")], 2, 0)
    mnr = path([G(e) for e in minor if T(e).get("highway") in ("tertiary", "tertiary_link") or (T(e).get("highway") == "unclassified" and len(e["geometry"]) > 30)], 3.2, 0)  # fewer hairlines: calm, no clutter
    sec = path(sel(lambda t: t.get("highway") in ("secondary", "primary") and t.get("ref") != "MDR148W"))
    trunk = path(sel(lambda t: t.get("highway") in ("trunk", "trunk_link")))
    mdr_ways = list({e["id"]: e for e in d + near if T(e).get("ref") == "MDR148W" and T(e).get("name") != "niwari road"}.values())
    ends = {(round(c["lat"], 4), round(c["lon"], 4)) for e in mdr_ways for c in (e["geometry"][0], e["geometry"][-1])}
    for e in d:  # ref-less bridges joined to the road belong to it
        if T(e).get("highway") == "secondary" and not T(e).get("ref") and e not in mdr_ways and T(e).get("bridge") and {(round(c["lat"], 4), round(c["lon"], 4)) for c in (e["geometry"][0], e["geometry"][-1])} & ends:
            mdr_ways.append(e)
    mdr = path([G(e) for e in mdr_ways], 0.6)
    rp0 = Point(P(*RAMP))  # junction loops far from the on-ramp read as stray blobs: keep motorway links only within 1.5 km of it
    exw = [e for e in d if T(e).get("ref") != "NEX" and "Ganga" not in T(e).get("name", "") and (T(e).get("highway") == "motorway" or (T(e).get("highway") == "motorway_link" and LineString([P(*c) for c in G(e)]).distance(rp0) < 60))]
    mw = path([G(e) for e in exw])
    rt = json.load(open(CACHE / "osrm_28.8013952.json", encoding="utf-8"))["routes"][0]["geometry"]["coordinates"]
    route = path([[(lat, lon) for lon, lat in rt]], 0.5)
    # expressway label sits on a straight stretch of the longest merged NE3 carriageway, south west of the on-ramp
    ne = [LineString([P(*c) for c in G(e)]) for e in exw if T(e).get("ref") == "NE3" and T(e).get("highway") == "motorway"]
    mg = linemerge(unary_union(ne)); parts = list(mg.geoms) if hasattr(mg, "geoms") else [mg]
    main = max(parts, key=lambda g: g.length)
    s0 = main.project(Point(P(*RAMP)))
    ds = max((-1, 1), key=lambda k: main.interpolate(min(max(s0 + k * 200, 0), main.length)).y)  # larger y = further south
    tgt = s0 + ds * XOFF
    a = main.interpolate(tgt - 40); b = main.interpolate(tgt + 40); c0 = main.interpolate(tgt)
    ang = math.degrees(math.atan2(b.y - a.y, b.x - a.x))
    if ang > 90: ang -= 180
    if ang < -90: ang += 180
    # the mapped road stops short of both town nodes: a short grey dashed link joins each end to its town
    road = unary_union([LineString([P(*c) for c in G(e)]) for e in mdr_ways])
    links = []
    for t in (MOD, HAP):
        pt = Point(P(*t)); q = nearest_points(road, pt)[0]
        if q.distance(pt) > 6: links.append(f"M{q.x:.1f} {q.y:.1f}L{pt.x:.1f} {pt.y:.1f}")
    pct = lambda lat, lon: [round(P(lat, lon)[0] / W * 100, 2), round(P(lat, lon)[1] / H * 100, 2)]
    pins = {"mod": pct(*MOD), "hap": pct(*HAP), "park": pct(*PARK), "ramp": pct(*RAMP),
            "xl": [round(c0.x / W * 100, 2), round(c0.y / H * 100, 2), round(ang, 1)]}
    svg = (f'<svg class="reg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="reg-t reg-d" xmlns="http://www.w3.org/2000/svg">'
           '<title id="reg-t">Map of the area around the park</title>'
           '<desc id="reg-d">Map from OpenStreetMap data. The Hapur-Modinagar Road runs from Modinagar in the north west, past Isapur Industrial Park, to Hapur in the south east. The Delhi-Meerut Expressway runs from the north east to the south west and crosses that road near Bhojpur. The expressway on-ramp is 4.7 km from the park by road, Modinagar is 11.4 km and Hapur 13.4 km by road.</desc>'
           f'<rect width="{W}" height="{H}" fill="#EBF0E6"/>'
           f'<path d="{farm}" fill="#E0E9DA"/><path d="{res}" fill="#F8F5EE" stroke="#EAE5D8" stroke-width="1"/><path d="{ind}" fill="#F0ECE1" stroke="#E4DECF" stroke-width="1"/>'
           f'<path d="{wat}" fill="#D6E5EB"/><path d="{wl}" fill="none" stroke="#C8DBE3" stroke-width="2.2" stroke-linecap="round"/>'
           f'<defs><path id="r-s" d="{sec}"/><path id="r-t" d="{trunk}"/><path id="r-m" d="{mdr}"/><path id="r-x" d="{mw}"/></defs>'
           '<g fill="none" stroke-linecap="round" stroke-linejoin="round">'
           f'<path d="{mnr}" stroke="#CFD4CC" stroke-width="1.5"/>'
           '<use href="#r-s" stroke="#C3C9C2" stroke-width="5"/><use href="#r-s" stroke="#fff" stroke-width="3.2"/>'
           '<use href="#r-t" stroke="#B2BAB3" stroke-width="6.6"/><use href="#r-t" stroke="#fff" stroke-width="4.6"/>'
           f'<path d="{" ".join(links)}" stroke="#8A948C" stroke-width="2" stroke-dasharray="2 6"/>'
           '<use href="#r-m" stroke="#fff" stroke-width="12.5"/><use href="#r-m" stroke="#0F4D3A" stroke-width="7.4"/>'
           '<use href="#r-x" stroke="#111827" stroke-width="17"/><use href="#r-x" stroke="#FFD600" stroke-width="11.4"/><use href="#r-x" stroke="#111827" stroke-opacity=".5" stroke-width="1" stroke-dasharray="7 7"/>'
           f'<mask id="reg-m" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}"><path class="rt-m" d="{route}" pathLength="1" stroke="#fff" stroke-width="12"/></mask>'
           f'<path class="rt" d="{route}" stroke="#E53935" stroke-width="3.6" stroke-dasharray="7 6" mask="url(#reg-m)"/>'
           '</g></svg>')
    (OUT / "region-map.json").write_text(json.dumps({"svg": svg, "pins": pins}), encoding="utf-8")
    print("region svg", len(svg), pins)


if __name__ == "__main__":
    import subprocess, sys
    layout(); region()
    subprocess.run([sys.executable, str(HERE / "build_master.py")], check=True)  # master map + layout-bands.json, always last
