"""Brand-coloured map of the Isapur Industrial Park area from cached OpenStreetMap data (see ovp.py, cache/).
Outputs (outlined text, no font dependency): site-v2/public/img/map/map-park.svg, map-park.webp, map-park-tall.webp, map-park-sm.webp
Run: python 02_Website/assets/map/build_map.py
Data: Overpass (roads, rail, water, landuse, places), route geometry from the OSRM public demo router (cache/osrm_*.json).
Credit for the page footer: Map data from OpenStreetMap contributors (ODbL)."""
import json, math, pathlib, sys, io
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "01_Brand/Brand-Kit/_build"))
import kitlib as K
K.MODE["outline"] = True
OUT = ROOT / "02_Website/site-v2/public/img/map"; OUT.mkdir(parents=True, exist_ok=True)
C = lambda n: json.loads((HERE / f"cache/{n}.json").read_text(encoding="utf-8"))

SAGE, WHITE, HAIR = "#EEF2EE", "#FFFFFF", "#CBD6CF"
YEL, GRN, INK = "#FFD600", "#0F4D3A", "#111827"
BUILT, IND, FARM, WATER = "#F5EDC8", "#F1E3A2", "#E8EFE6", "#CFDCD4"
LBL = "#46605A"
PARK = (28.7809, 77.6559)          # Phase 1 pin (knowledge file)
RAMP = (28.8013952, 77.6204507)    # motorway_link start near Bhojpur (OSM way 935414874), the on-ramp
TOWNS = {"Modinagar": (28.8320713, 77.5770873, "11.4 km by road"), "Hapur": (28.7299677, 77.775499, "13.4 km by road")}   # OSM place nodes, distances to bus stands from driving-distances.json
SW = K.width


def view(cx_lat, cx_lon, W, H, km_w):
    kx = 97.5; ky = 111.2                              # km per degree at 28.8 N
    sc = W / km_w                                       # px per km
    def p(lat, lon): return ((lon - cx_lon) * kx * sc + W / 2, (cx_lat - lat) * ky * sc + H / 2)
    return p, sc


def poly(coords, p):
    return "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in (p(c["lat"], c["lon"]) for c in coords))


def plate(x, y, t, size, fg=INK, bg=WHITE, pad=10, anchor="middle"):
    w = SW(t, "Montserrat-SemiBold", size, 0.01) + pad * 2; h = size + pad * 1.2
    x0 = x - (w / 2 if anchor == "middle" else w if anchor == "end" else 0)
    return (f'<rect x="{x0:.1f}" y="{y - size - pad * 0.1:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{bg}" stroke="{HAIR}" stroke-width="1.2"/>'
            + K.text(t, x0 + pad, y + pad * 0.1 + 1, size, "Montserrat-SemiBold", fg, 0.01)), w, h


def halo(t, x, y, size, fill=LBL, font="Montserrat-SemiBold", anchor="start", rot=None, tracking=0.02):
    g = K.text(t, x, y, size, font, fill, tracking, anchor, extra=f'stroke="{SAGE}" stroke-width="{size * 0.32:.1f}" stroke-linejoin="round" paint-order="stroke"')
    return f'<g transform="rotate({rot:.1f} {x:.1f} {y:.1f})">{g}</g>' if rot is not None else g


def build(W, H, cen, km_w, name, sizes):
    p, sc = view(cen[0], cen[1], W, H, km_w)
    roads, rail, water, land, places = C("roads")["elements"], C("rail")["elements"], C("water")["elements"], C("landuse")["elements"], C("places")["elements"]
    rt = C("osrm_28.8013952")["routes"][0]["geometry"]["coordinates"]
    L = []
    L.append(f'<rect width="{W}" height="{H}" fill="{SAGE}"/>')
    # landuse
    for e in land:
        col = IND if e["tags"].get("landuse") == "industrial" else BUILT if e["tags"].get("landuse") in ("residential", "commercial", "retail") else FARM if e["tags"].get("landuse") in ("farmland", "meadow", "orchard") else None
        if not col: continue
        rings = [e["geometry"]] if "geometry" in e else [m["geometry"] for m in e.get("members", []) if m.get("geometry") and m["role"] == "outer"]
        for g in rings:
            if len(g) > 3 and g[0] == g[-1]: L.append(f'<path d="{poly(g, p)}Z" fill="{col}"/>')
    # water
    for e in water:
        rings = [e["geometry"]] if "geometry" in e else [m["geometry"] for m in e.get("members", []) if m.get("geometry")]
        for g in rings:
            if e["tags"].get("natural") == "water" and len(g) > 3 and g[0] == g[-1]: L.append(f'<path d="{poly(g, p)}Z" fill="{WATER}"/>')
            elif e["tags"].get("waterway"): L.append(f'<path d="{poly(g, p)}" fill="none" stroke="{WATER}" stroke-width="{max(2, sc * 0.05):.1f}" stroke-linecap="round"/>')
    # rail
    for e in rail:
        L.append(f'<path d="{poly(e["geometry"], p)}" fill="none" stroke="#B8C7BF" stroke-width="{sc * 0.05:.1f}" stroke-dasharray="{sc * 0.12:.1f} {sc * 0.07:.1f}"/>')
    # roads by class
    W_ = {"residential": 0.035, "unclassified": 0.045, "tertiary": 0.07, "secondary": 0.11}
    order = ["residential", "unclassified", "tertiary", "secondary"]
    for cls in order:
        ds = " ".join(poly(e["geometry"], p) for e in roads if e["tags"].get("highway") == cls)
        w = W_[cls] * sc
        L.append(f'<path d="{ds}" fill="none" stroke="{HAIR}" stroke-width="{w + 2.2:.1f}" stroke-linecap="round" stroke-linejoin="round"/>')
        L.append(f'<path d="{ds}" fill="none" stroke="{WHITE}" stroke-width="{w:.1f}" stroke-linecap="round" stroke-linejoin="round"/>')
    mw = [e for e in roads if e["tags"].get("highway") in ("motorway", "motorway_link")]
    ds = " ".join(poly(e["geometry"], p) for e in mw)
    L.append(f'<path d="{ds}" fill="none" stroke="{GRN}" stroke-width="{0.13 * sc:.1f}" stroke-linecap="round" stroke-linejoin="round"/>')
    L.append(f'<path d="{ds}" fill="none" stroke="{YEL}" stroke-width="{0.08 * sc:.1f}" stroke-linecap="round" stroke-linejoin="round"/>')
    # route
    rd = "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in (p(lat, lon) for lon, lat in rt))
    L.append(f'<path d="{rd}" fill="none" stroke="{WHITE}" stroke-width="{0.085 * sc:.1f}" stroke-linecap="round" stroke-linejoin="round"/>')
    L.append(f'<path d="{rd}" fill="none" stroke="{GRN}" stroke-width="{0.05 * sc:.1f}" stroke-linecap="round" stroke-linejoin="round"/>')
    rpts = [p(lat, lon) for lon, lat in rt]
    # labels: villages
    sz = sizes["place"]; placed = []
    px, py = p(*PARK); rx, ry = p(*RAMP)
    names = {"Yusufpur Isapur": "Yusufpur Isapur", "Bhadola": "Bhadola", "Jahangirpur": "Jahangirpur", "Patti": "Patti", "Aurangabad Fajalgarh": "Aurangabad Fajalgarh", "Nahali": "Nahali",
             "Kilhauda": "Kilhauda", "Khanjarpur": "Khanjarpur", "Yusufpur Nanglabair": "Yusufpur Nanglabair", "Raghunathpur Khera": "Raghunathpur Khera"}
    seen = set()
    for e in places:
        n = e["tags"].get("name")
        if n not in names or n in seen: continue
        x, y = p(e["lat"], e["lon"])
        if not (50 < x < W - 50 and 50 < y < H - 50): continue
        if math.hypot(x - px, y - py) < sizes["clear"] or math.hypot(x - rx, y - ry) < sizes["clear"] * 0.8: continue
        if min(math.hypot(x - a_, y - b_) for a_, b_ in rpts[::3]) < sizes['clear'] * 0.5: continue
        w = SW(names[n], "Montserrat-SemiBold", sz, 0.02)
        box = (x - w / 2, y - sz, x + w / 2, y + 4)
        if any(not (box[2] < b[0] or box[0] > b[2] or box[3] < b[1] or box[1] > b[3]) for b in placed): continue
        placed.append(box); seen.add(n)
        L.append(f'<circle cx="{x:.1f}" cy="{y + sz * 0.9 + 0:.1f}" r="0" fill="none"/>' + halo(names[n], x, y, sz, anchor="middle"))
    # road labels
    exw = [e for e in mw if e["tags"].get("highway") == "motorway"]
    def seg_angle(e):
        g = e["geometry"]; a = p(g[0]["lat"], g[0]["lon"]); b = p(g[-1]["lat"], g[-1]["lon"]); return math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))
    best = None
    for e in exw:
        g = e["geometry"]; xs = [p(c["lat"], c["lon"]) for c in g]
        mid = xs[len(xs) // 2]
        if 100 < mid[0] < W - 100 and 100 < mid[1] < H - 100:
            ln = math.hypot(xs[-1][0] - xs[0][0], xs[-1][1] - xs[0][1])
            if best is None or ln > best[0]: best = (ln, mid, seg_angle(e))
    if best:
        ang = best[2]; ang = ang - 180 if ang > 90 else ang + 180 if ang < -90 else ang
        nx, ny = -math.sin(math.radians(ang)), math.cos(math.radians(ang))
        off = 0.22 * sc
        L.append(halo("Delhi-Meerut Expressway", best[1][0] + nx * off * -1.0, best[1][1] + ny * off * -1.0 + sizes["road"] * 0.35, sizes["road"], GRN, "Montserrat-ExtraBold", "middle", ang, 0.05))
    sec = [e for e in roads if e["tags"].get("ref") == "MDR148W"]
    bests = None
    for e in sec:
        xs = [p(c["lat"], c["lon"]) for c in e["geometry"]]
        for i in range(len(xs) - 1):
            mx, my = (xs[i][0] + xs[i + 1][0]) / 2, (xs[i][1] + xs[i + 1][1]) / 2
            ln = math.hypot(xs[i + 1][0] - xs[i][0], xs[i + 1][1] - xs[i][1])
            if 90 < mx < W - 90 and 90 < my < H - 90 and math.hypot(mx - px, my - py) > sizes["clear"] * 1.2 and ln > 20 and mx < px - sizes["clear"]:
                sc_ = math.hypot(mx - (px + (rx - px) * 0.42), my - (py + (ry - py) * 0.42))
                if bests is None or sc_ < bests[0]: bests = (sc_, mx, my, math.degrees(math.atan2(xs[i + 1][1] - xs[i][1], xs[i + 1][0] - xs[i][0])))
    if bests:
        ang = bests[3]; ang = ang - 180 if ang > 90 else ang + 180 if ang < -90 else ang
        nx, ny = -math.sin(math.radians(ang)), math.cos(math.radians(ang))
        L.append(halo("Hapur-Modinagar Road", bests[1] + nx * sizes["road"] * 0.9, bests[2] + ny * sizes["road"] * 0.9 + sizes["road"] * 0.35, sizes["road"] * 0.95, LBL, "Montserrat-SemiBold", "middle", ang, 0.03))
    # route plate and ramp marker
    mid = [p(lat, lon) for lon, lat in rt][len(rt) // 2]
    pl, w, h = plate(mid[0], mid[1] - sizes["plate"] * 1.1, "4.7 km by road", sizes["plate"], GRN)
    L.append(pl)
    L.append(f'<circle cx="{rx:.1f}" cy="{ry:.1f}" r="{sizes["dot"]:.1f}" fill="{YEL}" stroke="{GRN}" stroke-width="{sizes["dot"] * 0.35:.1f}"/>')
    pl, w, h = plate(rx + sizes["dot"] * 2.0, ry - sizes["dot"] * 1.4, "Expressway on-ramp", sizes["plate"], INK, anchor="start")
    L.append(pl)
    # park marker
    r = sizes["ring"]
    L.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{r:.1f}" fill="{GRN}" fill-opacity="0.12" stroke="{GRN}" stroke-opacity="0.45" stroke-width="2"/>')
    L.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{r * 0.62:.1f}" fill="{WHITE}" stroke="{WHITE}" stroke-width="6"/>')
    L.append(K.badge(px - sizes["badge"] / 2, py - sizes["badge"] / 2, sizes["badge"], uid="map"))
    t = "Isapur Industrial Park"
    if sizes.get("name_below"): L.append(halo(t, W - 36, py + r + sizes["name"] * 1.5, sizes["name"], INK, "Montserrat-ExtraBold", "end", None, 0.01))
    else: L.append(halo(t, px - r - 12, py + sizes["name"] * 0.35, sizes["name"], INK, "Montserrat-ExtraBold", "end", None, 0.01))
    # towns, direction arrows
    for n, (lat, lon, d) in (TOWNS.items() if sizes.get('arrows', True) else []):
        x, y = p(lat, lon); cx_, cy_ = W / 2, H / 2; dx, dy = x - cx_, y - cy_
        m = sizes["edge"]
        tx = ((W / 2 - m) / abs(dx)) if dx else 1e9; ty = ((H / 2 - m) / abs(dy)) if dy else 1e9; t_ = min(tx, ty)
        ex, ey = cx_ + dx * t_, cy_ + dy * t_
        if 0 <= x <= W and 0 <= y <= H: continue
        ang = math.degrees(math.atan2(dy, dx)); a = sizes["arrow"]
        tri = f'<path d="M{a} 0L{-a * 0.7} {a * 0.75}L{-a * 0.7} {-a * 0.75}Z" fill="{GRN}" transform="translate({ex:.1f} {ey:.1f}) rotate({ang:.1f})"/>'
        L.append(tri)
        sx = -1 if dx > 0 else 1
        tx_ = ex - sx * -1 * 0  # text inward of the arrow
        anchor = "end" if dx > 0 else "start"; tx0 = ex - (a * 1.6 if dx > 0 else -a * 1.6)
        L.append(halo(n, tx0, ey + (sizes["place"] * 0.2) - (0 if abs(dy) < 1 else (14 if dy < 0 else -sizes["place"] * 1.5)), sizes["name"] * 0.9, INK, "Montserrat-ExtraBold", anchor))
        L.append(halo(d, tx0, ey + sizes["place"] * 1.35 - (0 if abs(dy) < 1 else (14 if dy < 0 else -sizes["place"] * 1.5)), sizes["place"], LBL, "Montserrat-SemiBold", anchor))
    body = f'<defs><clipPath id="cl"><rect width="{W}" height="{H}"/></clipPath></defs><g clip-path="url(#cl)">{"".join(L)}</g>'
    return K.svg(W, H, body, f"{W}px", f"{H}px", "Map of the area around Isapur Industrial Park (OpenStreetMap data)", SAGE)


def webp(svg_path, out, w, maxkb):
    from playwright.sync_api import sync_playwright
    from PIL import Image
    with sync_playwright() as pw:
        b = pw.chromium.launch(); pg = b.new_page(viewport={"width": 2400, "height": 2400})
        s = svg_path.read_text(encoding="utf-8"); pg.set_content(f"<body style='margin:0'>{s.split('?>', 1)[-1]}</body>")
        el = pg.query_selector("svg"); el.screenshot(path=str(out.with_suffix(".png"))); b.close()
    im = Image.open(out.with_suffix(".png")).convert("RGB")
    im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    for qv in (84, 78, 72, 66, 60, 54, 48):
        buf = io.BytesIO(); im.save(buf, "WEBP", quality=qv, method=6)
        if len(buf.getvalue()) <= maxkb * 1024: break
    out.write_bytes(buf.getvalue()); out.with_suffix(".png").unlink()
    return qv, len(buf.getvalue()) // 1024


if __name__ == "__main__":
    wide = dict(place=17, road=15, plate=17, dot=9, ring=58, badge=78, name=24, edge=70, arrow=14, clear=70)
    (OUT / "map-park.svg").write_text(build(1800, 1200, (28.7895, 77.6395), 6.6, "wide", wide), encoding="utf-8")
    tall = dict(place=24, road=21, plate=24, dot=12, ring=78, badge=104, name=32, edge=90, arrow=18, clear=95, name_below=True, arrows=False)
    tp = OUT / "_tall.svg"; tp.write_text(build(1200, 1500, (28.7915, 77.6382), 5.4, "tall", tall), encoding="utf-8")
    print("wide", webp(OUT / "map-park.svg", OUT / "map-park.webp", 1800, 120))
    print("sm", webp(OUT / "map-park.svg", OUT / "map-park-sm.webp", 800, 60))
    print("tall", webp(tp, OUT / "map-park-tall.webp", 1200, 100)); tp.unlink()
    import os
    for f in sorted(OUT.iterdir()): print(f.name, os.path.getsize(f) // 1024, "KB")
