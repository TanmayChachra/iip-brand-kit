"""Builds the home 'Where' section map data (OpenStreetMap only, ODbL). Run: python scripts/build_where.py (needs shapely).
Inputs: 02_Website/assets/map/cache (fetch_regional.py: reg2_motor, reg2_river, osrm2_*; older region_major2, roads, region_land),
        01_Brand/Plot-Maps/data/phase-boundaries.geojson (owner's Google Earth outlines, approximate; geometry only, no imagery).
Outputs: public/data/where-region.json (lazy loaded: region svg + park svg) and src/assets/where-pins.json (pin positions in percent).
Map data from OpenStreetMap contributors."""
import json, math, pathlib
from shapely.geometry import LineString, Point, Polygon, box, shape
from shapely.ops import linemerge, unary_union, nearest_points

HERE = pathlib.Path(__file__).resolve().parent
SITE = HERE.parent
ROOT = SITE.parents[1]
CACHE = ROOT / "02_Website/assets/map/cache"
J = lambda f: json.load(open(CACHE / f, encoding="utf-8"))["elements"]
G = lambda e: [(c["lat"], c["lon"]) for c in e["geometry"]]
T = lambda e: e["tags"]

W, H = 1000, 1130
# region frame
LON_W, LON_E, LAT_N = 77.262, 77.80, 29.03
KM_W = (LON_E - LON_W) * 97.5
SC = W / KM_W
PR = lambda lat, lon: ((lon - LON_W) * 97.5 * SC, (LAT_N - lat) * 111.2 * SC)

gj = json.load(open(ROOT / "01_Brand/Plot-Maps/data/phase-boundaries.geojson", encoding="utf-8"))
PH = [shape(f["geometry"]) for f in gj["features"]]
CEN = unary_union(PH).centroid
PARK = (CEN.y, CEN.x)  # about 28.7826 N, 77.6560 E
# park frame, 1.5 km wide
PKM = 1.5
PSC = W / PKM
PP = lambda lat, lon: ((lon - PARK[1]) * 97.5 * PSC + W / 2, (PARK[0] - lat) * 111.2 * PSC + H / 2)

PLACES = {  # key: (lat, lon, name, ladder km or None, label side)
    "ramp": (28.8013952, 77.6204507),
    "mod": (28.8320713, 77.5770873),
    "hap": (28.7299677, 77.775499),
    "meerut": (28.9845, 77.7064),
    "dadri": (28.5312, 77.5401),
    "delhi": (28.6469, 77.3155),
}
CTX = {"ghz": (28.6692, 77.4538), "noida": (28.5708, 77.3261)}


def simp(g, tol=1.0, dp=1, clip=None):
    out = []
    for geom in g:
        if len(geom) < 2: continue
        ls = LineString(geom)
        if clip is not None: ls = ls.intersection(clip)
        if ls.is_empty: continue
        for part in (ls.geoms if hasattr(ls, "geoms") else [ls]):
            if part.geom_type != "LineString": continue
            c = list(part.simplify(tol).coords)
            if len(c) >= 2: out.append("M" + "L".join(f"{x:.{dp}f} {y:.{dp}f}" for x, y in c))
    return " ".join(out)


def build():
    clip = box(-20, -20, W + 20, H + 20)
    mot = J("reg2_motor.json")
    xy = lambda e, P=PR: [P(*c) for c in G(e)]
    ne3 = [e for e in mot if T(e).get("highway") == "motorway" and T(e).get("ref") == "NE3"]
    epe = [e for e in mot if T(e).get("highway") == "motorway" and T(e).get("ref") == "NE-2"]
    other_mw = [e for e in mot if T(e).get("highway") == "motorway" and T(e).get("ref") not in ("NE3", "NE-2", "NEX")]
    trunk = [e for e in mot if T(e).get("highway") == "trunk"]
    ramp_pt = Point(PR(*PLACES["ramp"]))
    links = [e for e in mot if T(e).get("highway") == "motorway_link" and LineString(xy(e)).distance(ramp_pt) < 25]
    # NE3 only where it is the Delhi-Meerut line (drop short spurs)
    d = J("region_major2.json"); near = J("roads.json")
    sec = [G(e) for e in d if T(e).get("highway") in ("secondary", "primary") and T(e).get("ref") != "MDR148W"]
    mdr_ways = list({e["id"]: e for e in d + near if T(e).get("ref") == "MDR148W" and T(e).get("name") != "niwari road"}.values())
    ends = {(round(c["lat"], 4), round(c["lon"], 4)) for e in mdr_ways for c in (e["geometry"][0], e["geometry"][-1])}
    for e in d:
        if T(e).get("highway") == "secondary" and not T(e).get("ref") and e not in mdr_ways and T(e).get("bridge") and {(round(c["lat"], 4), round(c["lon"], 4)) for c in (e["geometry"][0], e["geometry"][-1])} & ends:
            mdr_ways.append(e)
    try:
        riv = [G(e) for e in J("reg2_river.json") if T(e).get("name") in ("Yamuna", "Hindon", "Hindon River", "Yamuna River", "Ganga", "Krishni") or "Yamuna" in T(e).get("name", "") or "Hindon" in T(e).get("name", "")]
    except FileNotFoundError:
        riv = []

    # EPE junction = where NE3 meets NE-2
    a = unary_union([LineString(xy(e)) for e in ne3]); b = unary_union([LineString(xy(e)) for e in epe])
    ix = a.intersection(b)
    pts = [ix] if ix.geom_type == "Point" else [g for g in getattr(ix, "geoms", []) if g.geom_type == "Point"]
    parkxy = Point(PR(*PARK))
    # the junction nearest the park along the expressway on the Delhi side (about 14 km from the ramp)
    jn = min(pts, key=lambda p: abs(p.distance(parkxy) / SC - 15))
    jlat = LAT_N - jn.y / SC / 111.2; jlon = LON_W + jn.x / SC / 97.5
    print("EPE junction", round(jlat, 4), round(jlon, 4), "straight km from park", round(jn.distance(parkxy) / SC, 1))

    # routes from the park (OSRM geometry, cached)
    def route(k):
        r = json.load(open(CACHE / f"osrm2_{k}.json"))["routes"][0]
        return [(lat, lon) for lon, lat in r["geometry"]["coordinates"]], r["distance"] / 1000
    R = {}
    for k in ("ramp", "mod", "hap", "meerut", "dadri", "delhi"):
        R[k] = route(k)
        print(k, round(R[k][1], 1), "km")
    # EPE junction route = prefix of the Delhi route up to the junction
    dl = LineString([PR(*c) for c in R["delhi"][0]])
    cut = dl.project(jn)
    pre = []
    acc = 0
    for c in R["delhi"][0]:
        p = Point(PR(*c))
        if dl.project(p) > cut: break
        pre.append(c)
    pre.append((jlat, jlon))
    R["epe"] = (pre, None)

    order = ["ramp", "mod", "hap", "epe", "meerut", "delhi", "dadri"]  # draw order = ladder order (dadri last: it is 46.3, delhi 46.0)
    rts = {k: simp([R[k][0]], 0.5, 1, None) for k in order}
    # paths, all in pixel space; routes are converted lat/lon to px
    def route_px(k):
        return "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in LineString([PR(*c) for c in R[k][0]]).simplify(0.6).coords)
    rts = {k: route_px(k) for k in order}

    mw = simp([xy(e) for e in ne3], 1.0)
    ep = simp([xy(e) for e in epe], 1.0)
    om = simp([xy(e) for e in other_mw], 1.2)
    tr = simp([xy(e) for e in trunk], 1.2)
    lk = simp([xy(e) for e in links], 0.8)
    sc_ = simp([[PR(*c) for c in g] for g in sec], 1.0)
    md = simp([xy(e) for e in mdr_ways], 0.6)
    rv = simp([[PR(*c) for c in g] for g in riv], 1.5)

    svg = (f'<svg class="wr__svg" viewBox="0 0 {W} {H}" aria-hidden="true" xmlns="http://www.w3.org/2000/svg">'
           f'<rect width="{W}" height="{H}" fill="#EBF0E6"/>'
           f'<path d="{rv}" fill="none" stroke="#C8DBE3" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>'
           f'<defs><path id="w-t" d="{tr}"/><path id="w-o" d="{om}"/><path id="w-s" d="{sc_}"/><path id="w-e" d="{ep}"/><path id="w-m" d="{md}"/><path id="w-x" d="{mw}"/><path id="w-l" d="{lk}"/></defs>'
           '<g fill="none" stroke-linecap="round" stroke-linejoin="round">'
           '<use href="#w-s" stroke="#C3C9C2" stroke-width="3.6"/><use href="#w-s" stroke="#fff" stroke-width="2"/>'
           '<use href="#w-t" stroke="#B2BAB3" stroke-width="5"/><use href="#w-t" stroke="#fff" stroke-width="3.2"/>'
           '<use href="#w-o" stroke="#B2BAB3" stroke-width="5"/><use href="#w-o" stroke="#fff" stroke-width="3.2"/>'
           '<use href="#w-e" stroke="#374151" stroke-width="8"/><use href="#w-e" stroke="#fff" stroke-width="5.4"/><use href="#w-e" stroke="#374151" stroke-width="1" stroke-dasharray="5 5"/>'
           '<use href="#w-m" stroke="#fff" stroke-width="9"/><use href="#w-m" stroke="#0F4D3A" stroke-width="5"/>'
           '<use href="#w-x" stroke="#111827" stroke-width="14"/><use href="#w-l" stroke="#111827" stroke-width="10"/><use href="#w-x" stroke="#FFD600" stroke-width="9.4"/><use href="#w-l" stroke="#FFD600" stroke-width="6"/>'
           '<g class="wr__rts">'
           + "".join(f'<path class="wr__rt" data-k="{k}" style="--i:{i}" d="{rts[k]}" pathLength="1"/>' for i, k in enumerate(order)) +
           '</g></g></svg>')

    # ---- park from above (OSM only) ----
    pclip = box(-30, -30, W + 30, H + 30)
    roads = [e for e in near if T(e).get("highway") in ("unclassified", "tertiary", "secondary", "residential") and not (T(e).get("ref") == "MDR148W")]
    mdr_p = simp([[PP(*c) for c in G(e)] for e in mdr_ways], 0.5, 1, pclip)
    rd_p = simp([[PP(*c) for c in G(e)] for e in roads], 0.6, 1, pclip)
    land = J("region_land.json")
    wat = []
    for e in land:
        g = e.get("geometry") or []
        if T(e).get("natural") == "water" and len(g) > 3:
            pg = Polygon([PP(c["lat"], c["lon"]) for c in g]).buffer(0).intersection(pclip)
            if not pg.is_empty and pg.geom_type == "Polygon": wat.append("M" + "L".join(f"{x:.0f} {y:.0f}" for x, y in pg.exterior.coords) + "Z")
    ph_fill = ["#FFD600", "#0F4D3A", "#E53935"]
    ph_op = [".85", ".78", ".82"]
    phs = "".join(f'<path d="M' + "L".join(f"{x:.1f} {y:.1f}" for x, y in (PP(lat, lon) for lon, lat in p.exterior.coords)) + f'Z" fill="{ph_fill[i]}" fill-opacity="{ph_op[i]}" stroke="#111827" stroke-width="1.6" stroke-linejoin="round"/>' for i, p in enumerate(PH))
    psvg = (f'<svg class="wr__svg" viewBox="0 0 {W} {H}" aria-hidden="true" xmlns="http://www.w3.org/2000/svg">'
            f'<rect width="{W}" height="{H}" fill="#E8EFE2"/>'
            f'<path d="{" ".join(wat)}" fill="#D6E5EB"/>'
            f'<g fill="none" stroke-linecap="round" stroke-linejoin="round"><path d="{rd_p}" stroke="#C3C9C2" stroke-width="7"/><path d="{rd_p}" stroke="#fff" stroke-width="5"/>'
            f'<path d="{mdr_p}" stroke="#fff" stroke-width="22"/><path d="{mdr_p}" stroke="#0F4D3A" stroke-width="13"/><path d="{mdr_p}" stroke="#fff" stroke-width="1.3" stroke-dasharray="9 9"/></g>'
            f'<g>{phs}</g></svg>')

    pct = lambda x, y: [round(x / W * 100, 2), round(y / H * 100, 2)]
    pins = {k: pct(*PR(*PLACES[k])) for k in PLACES}
    pins["epe"] = pct(jn.x, jn.y)
    pins["park"] = pct(*PR(*PARK))
    ctx = {k: pct(*PR(*v)) for k, v in CTX.items()}
    # expressway label: on the NE3 line between the junction and the Delhi side, tangent angle
    nl = linemerge(unary_union([LineString(xy(e)) for e in ne3]))
    parts = list(nl.geoms) if hasattr(nl, "geoms") else [nl]
    main = max(parts, key=lambda g: g.length)
    s_r = main.project(ramp_pt); s_j = main.project(jn)
    # plate lies beside the line (west side), parallel to it, midway between the ramp and the EPE junction
    tgt = s_r + (s_j - s_r) * 0.58
    p0, p1, c0 = main.interpolate(tgt - 60), main.interpolate(tgt + 60), main.interpolate(tgt)
    ang = math.degrees(math.atan2(p1.y - p0.y, p1.x - p0.x))
    nx, ny = (p1.y - p0.y), -(p1.x - p0.x)  # normal
    nl_ = math.hypot(nx, ny); nx, ny = nx / nl_, ny / nl_
    if nx > 0: nx, ny = -nx, -ny  # west side
    c0 = Point(c0.x + nx * 36, c0.y + ny * 36)
    if ang > 90: ang -= 180
    if ang < -90: ang += 180
    xl = pct(c0.x, c0.y) + [round(ang, 1)]
    # park view
    phc = [pct(*PP(p.representative_point().y, p.representative_point().x)) for p in PH]
    mp = unary_union([LineString([PP(*c) for c in G(e)]) for e in mdr_ways])
    q = nearest_points(mp, Point(W / 2, H / 2))[0]
    l0 = mp.project(q)
    # label sits on the road to the south-east of the park centre, where it is straight
    a0, a1 = mp.interpolate(l0 + 235 - 40), mp.interpolate(l0 + 235 + 40) if l0 + 275 < mp.length else (mp.interpolate(l0 - 235 - 40), mp.interpolate(l0 - 235 + 40))
    ang2 = math.degrees(math.atan2(a1.y - a0.y, a1.x - a0.x))
    if ang2 > 90: ang2 -= 180
    if ang2 < -90: ang2 += 180
    mid = mp.interpolate(l0 + 235) if l0 + 275 < mp.length else mp.interpolate(l0 - 235)
    # direction to the expressway ramp from the park (screen angle, degrees clockwise from east)
    rx, ry = PR(*PLACES["ramp"]); px, py = PR(*PARK)
    ramp_ang = math.degrees(math.atan2(ry - py, rx - px))
    pk = {"ph": phc, "road": pct(mid.x, mid.y) + [round(ang2, 1)], "ramp": round(ramp_ang, 1), "park": [50, 50]}
    out = {"region": svg, "park": psvg}
    d = SITE / "public/data"; d.mkdir(parents=True, exist_ok=True)
    (d / "where-region.json").write_text(json.dumps(out, separators=(",", ":")), encoding="utf-8")
    (SITE / "src/assets/where-pins.json").write_text(json.dumps({"pins": pins, "ctx": ctx, "xl": xl, "pk": pk, "park": PARK}, separators=(",", ":")), encoding="utf-8")
    print("sizes", len(svg), len(psvg), "pins", pins, "xl", xl, "pk", pk)


if __name__ == "__main__":
    build()
