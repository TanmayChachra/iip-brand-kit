"""Rebuild the three Isapur Industrial Park plot maps (phase1..3.svg + plots.json).

Usage: python build_plots.py [--src DIR]
Source PDFs are read only and never copied. Needs pymupdf and shapely.
Method: take plot linework (strokes + outlines of big filled shapes) from the vector PDF,
buffer it a little to close hairline gaps, cut the page into faces, keep faces that
contain a plot label (text), grow them back. Faces without a label are not plots.
"""
import json, math, re, sys, pathlib
from html import escape as esc
import pymupdf
from shapely.geometry import Polygon, LineString, MultiPoint, box, Point
from shapely.algorithms.polylabel import polylabel
from shapely.affinity import rotate as shp_rotate
from shapely.ops import unary_union
from shapely.affinity import affine_transform
from shapely.prepared import prep

HERE = pathlib.Path(__file__).parent
SRC = pathlib.Path(r"G:\My Drive\SilverleafBuildcon\Isapur Industrial Park\01_Layouts")
for i, a in enumerate(sys.argv):
    if a == "--src":
        SRC = pathlib.Path(sys.argv[i + 1])
TOK = json.loads((HERE.parent / "Brand-Kit/tokens/brand.tokens.json").read_text(encoding="utf-8"))["color"]
C = {k: v["value"] for k, v in TOK.items()}


def rgb(c):
    return tuple(round(v, 2) for v in c) if c else None


HATCH = {(0.72, 0.36, 0.36), (0.75, 1.0, 0.0), (0.65, 0.87, 0.0), (0.54, 0.72, 0.0), (0.34, 0.45, 0.0),
         (0.44, 0.58, 0.0), (0.72, 0.54, 0.0), (0.36, 0.72, 0.54), (0.0, 0.58, 0.29), (1.0, 1.0, 1.0),
         (0.0, 0.25, 1.0), (0.86, 0.86, 0.86)}


def is_gray(f):
    return f and abs(f[0] - f[1]) < .02 and abs(f[1] - f[2]) < .02 and .5 < f[0] < .8


LBL = {
    1: (re.compile(r"^(D\d{1,2}|\d{1,2}[AB]?|E\d{1,2}|[BCS]-?\d{1,2}[A-Z]?(\(.*\))?|S-?\d\s?\(.*\))$"), {0x954a, 0xff00ff, 0x0}),
    2: (re.compile(r"^([ABCD]\d{1,2}|D15 & D16|S\d{1,2}|A48( \(1st\))?)$"), {0xff0000, 0xff00ff, 0xff, 0x1c7200, 0x0}),
    3: (re.compile(r"^\d\d$"), {0x954a}),
}
SUFFIX = re.compile(r"^\(\s*[IVX]+\s*\)$|^\(\d(st|nd)\)$")
ROAD = re.compile(r"(\d+'-\d+\"\s*WIDE ROAD|MAIN ROAD|EXISTING COLONY ROAD|CHAKH ROAD)")


P3_AREAS = dict(zip(['%02d' % i for i in range(1, 24)], [
    708.873, 750.605, 683.938, 608.566, 1081.763, 1253.873, 517.317, 528.672, 501.926, 876.657, 841.536, 841.536,
    841.566, 563.806, 563.806, 556.795, 314.401, 229.893, 371.068, 256.558, 406.253, 355.184, 665.891]))
# Phase 3 area table (sq yd) is drawn as outlines in the PDF, not text, so it is transcribed from the rendered sheet
# and cross-checked (each row's sq ft / 9 equals its sq yd).


# Drawing scale in PDF units per foot, measured from dimension text (feet-inches) matched to plot edges
# (median of 709, 431 and 84 matches, spread under 0.5 percent), so sq yd = units^2 / scale^2 / 9.
SCALE = {1: 0.4480, 2: 0.5768, 3: 0.9218}


def natkey(s):
    return [int(t) if t.isdigit() else t for t in re.split(r"(\d+)", s)]


def seg_lines(items):
    out = []
    for it in items:
        if it[0] == "l":
            out.append(LineString([(it[1].x, it[1].y), (it[2].x, it[2].y)]))
        elif it[0] == "re":
            r = it[1]
            out.append(LineString([(r.x0, r.y0), (r.x1, r.y0), (r.x1, r.y1), (r.x0, r.y1), (r.x0, r.y0)]))
        elif it[0] == "qu":
            q = it[1]
            out.append(LineString([(p.x, p.y) for p in (q.ul, q.ur, q.lr, q.ll, q.ul)]))
    return out


def poly_of(items):
    pts = []
    for it in items:
        if it[0] == "l":
            pts += [(it[1].x, it[1].y), (it[2].x, it[2].y)]
        elif it[0] == "re":
            r = it[1]
            pts += [(r.x0, r.y0), (r.x1, r.y0), (r.x1, r.y1), (r.x0, r.y1)]
        elif it[0] == "qu":
            q = it[1]
            pts += [(p.x, p.y) for p in (q.ul, q.ur, q.lr, q.ll)]
        elif it[0] == "c":
            pts += [(it[1].x, it[1].y), (it[4].x, it[4].y)]
    if len(pts) < 3:
        return None
    return MultiPoint(pts).convex_hull  # fills are triangulated convex pieces


def stroke_ok(ph, col, w):
    if col is None or col in HATCH:
        return False
    if col == (0.0, 0.0, 0.0):
        return ph != 2 and w >= 0.3
    return True


def build(ph):
    doc = pymupdf.open(SRC / f"IIP-Phase{ph}.pdf")
    pg = doc[0]
    M = pg.rotation_matrix
    lines, roads = [], []
    for x in pg.get_drawings():
        col, fill = rgb(x["color"]), rgb(x["fill"])
        if fill and is_gray(fill) and all(i[0] == "l" for i in x["items"]) and len(x["items"]) % 3 == 0:
            for k in range(0, len(x["items"]), 3):  # fills are lists of triangles
                t = poly_of(x["items"][k:k + 3])
                if t is not None and t.area > 0:
                    roads.append(t)
        elif col and not fill and stroke_ok(ph, col, x["width"] or 0):
            lines += seg_lines(x["items"])
    ru = unary_union(roads).buffer(0.3).buffer(-0.3) if roads else None
    roads = [g for g in (ru.geoms if ru is not None and hasattr(ru, 'geoms') else [ru] if ru is not None else []) if g.area > 300]
    spans = []
    for b in pg.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            for s in l["spans"]:
                t = s["text"].strip()
                if t:
                    bb = s["bbox"]
                    spans.append(dict(t=t, c=s["color"], x=(bb[0] + bb[2]) / 2, y=(bb[1] + bb[3]) / 2,
                                      d=l["dir"], f=s["font"]))
    dgs = [x for x in spans if x["t"] in ("1", "2") and x["c"] == 0xff00ff]
    for b3 in [x for x in spans if x["t"] == "B-3" and x["c"] == 0xff00ff]:  # "B-3" and its 1 or 2 are separate strings
        dg = min(dgs, key=lambda q: (q["x"] - b3["x"]) ** 2 + (q["y"] - b3["y"]) ** 2)
        if (dg["x"] - b3["x"]) ** 2 + (dg["y"] - b3["y"]) ** 2 < 12 ** 2:
            b3["t"] = f"B-3({dg['t']})"
            dg["t"] = ""
            dgs.remove(dg)
    spans = [x for x in spans if x["t"]]
    unrel = []
    rx, cols = LBL[ph]
    labs = [s for s in spans if rx.match(s["t"]) and s["c"] in cols and "Black" not in s["f"]
            or (ph == 1 and rx.match(s["t"]) and s["c"] == 0xff00ff)]
    if ph == 1:
        labs = [s for s in labs if s["c"] != 0 or re.fullmatch(r"D\d{1,2}", s["t"])]
    if ph == 3:
        labs = [s for s in labs if pymupdf.Point(s["x"], s["y"]).transform(M).x < 590]
    for s in spans:
        if SUFFIX.match(s["t"]) and labs:
            near = min(labs, key=lambda a: (a["x"] - s["x"]) ** 2 + (a["y"] - s["y"]) ** 2)
            if (near["x"] - s["x"]) ** 2 + (near["y"] - s["y"]) ** 2 < 40 ** 2 and not near.get("sfx"):
                near["t"] += s["t"].replace(" ", "")
                near["sfx"] = 1
    base = unary_union(lines)
    pb = base.bounds
    maxa = {1: 0.02, 2: 0.04, 3: 0.04}[ph] * (pb[2] - pb[0]) * (pb[3] - pb[1])
    cache = {}

    def faces_for(eps):
        if eps not in cache:
            net = base.buffer(eps)
            ar = box(pb[0] - 5, pb[1] - 5, pb[2] + 5, pb[3] + 5).difference(net)
            fl = [f for f in (ar.geoms if hasattr(ar, "geoms") else [ar]) if f.area > 8]
            cache[eps] = [(prep(f), f) for f in fl]
        return cache[eps]

    plots = {}
    for s in labs:
        pt = Point(s["x"], s["y"])
        for eps in (0.5, 1.5, 3.0, 6.0, 10.0, 16.0):
            fl = faces_for(eps)
            hit = [f for pf, f in fl if pf.contains(pt)]
            if not hit:
                near = min((f for _, f in fl), key=lambda f: f.distance(pt))
                hit = [near] if near.distance(pt) < 4 else []
            if hit and hit[0].area < maxa:
                plots.setdefault((eps, id(hit[0])), (hit[0], [], eps))[1].append(s["t"])
                break
        else:
            unrel.append(s["t"])
    res = []
    for f, ts, eps in plots.values():
        if len(ts) > 1 and not any("&" in t for t in ts):
            unrel.append(" + ".join(ts))  # several labels in one face: divider lines missing, do not guess
            continue
        g = f.buffer(eps, join_style=2, mitre_limit=4).simplify(0.15)
        if g.geom_type != "Polygon":
            g = max(g.geoms, key=lambda q: q.area)
        bb = g.bounds
        ba = (bb[2] - bb[0]) * (bb[3] - bb[1])
        if ba > 40000 or (ba > 4000 and g.area < 0.35 * ba):  # leaked into roads or open land: do not guess
            unrel.append(" + ".join(ts))
            continue
        res.append(dict(poly=g, labels=ts, area=None))
    if ph == 3:
        for r in res:
            r["area"] = P3_AREAS.get(r["labels"][0])
    if ph == 2:
        for s in spans:
            m = re.match(r"= ([\d.]+) SQ\. YDS\.", s["t"])
            if m:
                pt = Point(s["x"], s["y"])
                for r in res:
                    if r["poly"].contains(pt):
                        r["area"] = float(m.group(1))
    roadlabels = []
    n_ = [s for s in spans if s["t"] == "N" and s["c"] == 0xff0000]
    s_ = [s for s in spans if s["t"] == "S" and s["c"] == 0xff0000]
    if not n_:
        cand = [s for s in spans if s["t"] in ("N", "S") and s["c"] == 0 and s["f"] == "ArialMT"]
        n_ = [c for c in cand if c["t"] == "N"][-1:]
        s_ = [c for c in cand if c["t"] == "S"][-1:]
    north = None
    if n_ and s_:
        north = dict(ang=math.degrees(math.atan2(n_[0]["y"] - s_[0]["y"], n_[0]["x"] - s_[0]["x"])))
    T = [M.a, M.c, M.b, M.d, M.e, M.f]
    for r in res:
        r["poly"] = affine_transform(r["poly"], T)
    if ph == 1:
        res += plot30(res)
    res = apply_overrides(ph, res)
    for r in res:
        r["area_c"] = r["poly"].area / SCALE[ph] ** 2 / 9
    roads = [affine_transform(r, T) for r in roads]
    if north:
        dx, dy = math.cos(math.radians(north["ang"])), math.sin(math.radians(north["ang"]))
        north["ang"] = math.degrees(math.atan2(dx * M.b + dy * M.d, dx * M.a + dy * M.c))
    roadlabels = road_labels(ph, pg, M)
    pub = extras(ph, res, roads)
    named = named_roads(ph, res, roads)
    roads = pub.pop("roads")
    nali = OVERRIDES.get(ph, {}).get("nali", [])
    return dict(pub=pub.get("pub"), nali=nali, plots=res, roads=roads, named=named, roadlabels=roadlabels, north=north, nlabels=len(labs), unrel=unrel)


# ---------------------------------------------------------------- OVERRIDES (owner corrections, 2026-11-13)
# Explicit geometry and settings applied after the automatic trace, so they survive every regeneration.
# Coordinates are page units after rotation (same as the SVG), read from the vector PDF (exact line and arc end points).
# Plot labels are the keys; "replace" swaps the outline, "add" creates a plot the trace missed, "remove" drops a face.
OVERRIDES = {1: dict(
    replace={
        # E36: the red mark beside it is a high-tension tower, not a plot feature. Plain quadrilateral between E35 and E37.
        "E36": [(468.6, 111.1), (504.0, 110.8), (503.6, 135.6), (468.7, 135.7)],
        # S-1(I) and S-4(I): the architect straightened the corner arcs into diagonals (arc end points from the PDF).
        "S-1(I)": [(433.1, 691.8), (460.4, 691.4), (453.1, 702.1), (432.9, 701.7)],
        "S-4(I)": [(488.9, 725.1), (509.0, 725.3), (508.8, 736.5), (481.4, 736.0)],
        # B-34: the label underline cut a hole in the traced face, so the drawn outline stopped halfway. Full quad top to bottom.
        "B-34": [(569.7, 892.9), (583.2, 893.2), (583.9, 838.5), (570.4, 838.3)],
        # shared edges must meet exactly (owner): S-5 sits on B-24's top edge (436.0,753.1)-(458.5,753.4), S-6 and S-7 share the
        # divider x 424.7 (y 761.4 to 768.8), S-6 and B-24 share x 436.0, S-4(I) sits on B-21(II)'s top edge. Lines from the PDF.
        "S-5": [(436.0, 753.1), (454.4, 737.4), (458.7, 739.8), (458.5, 753.4)],
        "B-24": [(436.0, 753.1), (458.5, 753.4), (458.2, 769.3), (436.0, 769.0)],
        "S-6": [(424.7, 761.4), (436.0, 752.3), (436.0, 769.0), (424.7, 768.8)],
        "S-7": [(417.9, 766.9), (424.7, 761.4), (424.7, 768.8), (417.9, 768.7)],
    },
    add={
        # the thin plot below C-9 (36'-7" top edge, 20' and 21' sides), no text label of its own in the PDF
        "C-9(I)": [(528.3, 611.5), (544.6, 611.7), (537.6, 620.6), (528.4, 620.4)],
        # C-8B and C-8A (owner 2026-11-13, plot_type plot): the two plots left of C-9 and of the thin plot below it. Labels in the PDF
        # have a space ("C- 8B") so the tracer skipped them; lines read from the PDF (black lines).
        "C-8B": [(483.7, 585.8), (528.6, 586.4), (528.3, 616.4), (483.4, 615.8)],
        "C-8A": [(483.4, 615.8), (528.3, 616.4), (528.2, 620.5), (483.4, 619.8)],
        # B-27 (II) and (III): labels have a space ("B-27 (II)") so the tracer skipped them; lines read from the PDF
        "B-27(II)": [(481.4, 769.8), (510.6, 770.1), (510.3, 785.8), (481.4, 785.4)],
        "B-27(III)": [(481.4, 785.4), (510.3, 785.8), (509.8, 814.9), (481.5, 814.4)],
        # Triangular end B-23 / B-22A beside the red E. LINE road (owner: commercial shops, no plot number). Three unlabelled
        # triangles bounded by the thick black lines: right of B-22A, below B-22A, below B-23. Shared edges meet exactly:
        # x 426.1 (B-22A right edge), y 739.7 to 740.0 (B-22A foot), x 408.2 (B-22A and B-23 edge), y 754.1 (B-23 foot).
        # The hypotenuse is the diagonal (446.0,724.3)-(387.1,770.6). Labels "Shop n" are never drawn as text.
        "Shop 1": [(426.1, 724.3), (446.0, 724.3), (426.1, 740.0)],
        "Shop 2": [(408.2, 740.0), (426.1, 740.0), (408.2, 754.1)],
        "Shop 3": [(387.3, 754.1), (408.2, 754.1), (387.1, 770.6)],
    },
    remove=[],
    commercial=["S-1(I)", "S-4(I)", "Shop 1", "Shop 2", "Shop 3"],  # plot_type "shop", legend "Commercial shops", whatever the area
    # CHAKH ROAD bands (named roads drawn with the normal road fill and labelled like other roads).
    # 1: the strip between the sheet boundary (orange line) and the plot edges, left of D5 and D4, behind D5 to D14 and
    #    on along the top of the C block to the C-12 corner. Outer edge then inner edge, from the PDF lines.
    chakh=[
        dict(id="chakh-road-1", poly=[(136.9, 646.5), (137.7, 591.9), (138.1, 569.5), (138.6, 509.1), (225.8, 512.8),
                                     (248.2, 513.4), (392.7, 515.1), (462.1, 514.0), (484.4, 514.3), (629.1, 516.4),
                                     (629.1, 520.2), (484.3, 518.0), (462.1, 517.8), (389.0, 518.8), (248.1, 517.0),
                                     (225.7, 516.6), (142.3, 513.0), (141.7, 569.6), (141.4, 591.9), (140.6, 646.6)]),
        # 2: below B-46 to B-32, up the right side of B-32 and B-31, then right along the top of B-51 to B-54.
        #    Cut out of the existing road fill, so it follows the sheet exactly.
        dict(id="chakh-road-2", cut=[
            [(266, 883.0), (296.5, 884.8), (296.5, 892), (266, 892)],  # strip B, same band (was plain road fill with a label)
            [(296, 883.0), (619.2, 892.6), (619.2, 904), (296, 904)],
            [(619.0, 892.0), (624.0, 892.0), (624.0, 771.0), (619.0, 771.0)],
            [(619.0, 770.5), (711.5, 770.5), (711.5, 778.5), (619.0, 778.5)]]),
        # 3 (owner 2026-11-13, styling only): the PDF labels these strips CHAKH ROAD but the sheet fill is plain road grey, so they
        #    were drawn as road. Now bands like the others: the strip below D4 to D20 (D bottoms to plot tops, over the 50 ft
        #    road crossing), the left strip beside 45 to 36 (boundary line to the plot edges, x_r(y) = 140.5 + .0057 (y - 647))
        #    and strip A below 36 to 33. Each is cut from the road fill, minus the plots, thin slivers opened away.
        dict(id="chakh-road-3", open=.6, cut=[
            [(136.5, 646.3), (140.6, 646.6), (159.2, 647.2), (177.1, 647.8), (224.1, 649.3), (246.4, 650.4), (301.8, 651.9),
             (303.5, 651.9), (303.6, 655.5), (248.5, 654.1), (222.8, 652.9), (180.7, 651.4), (160.5, 650.9), (140.4, 650.2), (136.5, 650.0)],
            [(125, 646.5), (140.5, 646.5), (141.8, 878.0), (125, 878.0)],
            [(125, 876.0), (226.5, 876.0), (226.5, 888.0), (125, 888.0)]]),
    ],
    # labels of the new bands: (x, y, rotation, font size or None for the road default)
    # one shared size and spacing (about 75 to 130 units apart along each strip); the PDF's own CHAKH ROAD labels add more
    chakh_labels=[(190, 512.9, 1.3, 3.0), (300, 515.0, 0.7, 3.0), (410, 516.0, 0.7, 3.0), (556, 517.4, 0.8, 3.0), (140.2, 545, -90, 3.0),
                  (139.2, 620, -90, 3.0), (139, 850, -90, 3.0), (165, 649.1, 1.9, 3.0), (360, 888.0, 1.1, 3.0), (450, 895.0, 1.1, 3.0),
                  (540, 890.0, 1.1, 3.0), (621.3, 800, -90, 3.0), (621.3, 870, -90, 3.0), (665, 774.3, 0.0, 3.0)],
),
2: dict(
    # Phase 2 owner corrections (2026-11-13). Coordinates read from the vector PDF (line end points, dotted line fits).
    rename={"A48 (1st)": "A48 (I)", "A48(2nd)": "A48 (II)"},
    # C10, A48 (II) and A22 to A24 are ordinary plotted plots, never the shop fill (owner)
    plotted=["C10", "A48 (II)", "A22", "A23", "A24"],
    replace={
        # D15 & D16: left edge is the line right of D3, D6 and D9 (near vertical), top and right edges and the bottom edge
        # along the tops of D13 and D14 straight from the PDF (red lines), no bulge into the roads
        "D15 & D16": [(644.6, 98.0), (758.2, 119.2), (788.0, 123.8), (793.4, 136.8), (787.5, 285.1), (637.2, 274.2)],
        # D37 and D38 exactly as the PDF (magenta): D38 apex at the top, flat bottom on y 252 above D37
        "D37": [(806.2, 252.0), (857.6, 252.0), (861.6, 306.8), (862.6, 349.0), (802.3, 349.1)],
        "D38": [(791.2, 252.0), (794.8, 162.8), (803.6, 146.4), (832.3, 199.2), (857.6, 252.0)],
    },
    # Main Road below A55: one straight band. Left edge is the sheet boundary line, right edge A56 to A59 then the S strips,
    # bottom is the road end line. (The staircase between S7 and S8 is not a plot: it stays blank ground, no number.)
    main_road=[(368.4, 596.0), (368.2, 617.0), (387.0, 826.0), (412.0, 821.4), (404.6, 726.4), (397.5, 616.3), (398.6, 596.0)],
    # nali slivers must not turn into road: between D15 and D38
    noroad=[[(780, 90), (812, 90), (812, 252.0), (780, 252.0)]],
    chakh=[
        # 1: strip between the two dotted lines left of A9 to A1 (x = 303.08 - 0.06 y and 307.11 - 0.06 y)
        # (dotted lines refit from the PDF: x = 302.51 - .05895 y and 306.58 - .0590 y, ends y 273 and 631.4). Behind A8 to A14 (y 273 to
        # 410) the strip is the NALI (drawn as nali-6, inner side); the chakh road runs behind A1 to A9 (y 275 to 631.4), full width
        # below A8 and on the outer half where it overlaps the nali
        dict(id="chakh-road-1", polys=[[(278.3, 410), (282.4, 410), (269.3, 631.4), (265.3, 631.4)], [(286.3, 275), (288.4, 275), (280.4, 410), (278.3, 410)]]),
        # 2: between the dotted lines right of A59 up to A47, over the A55 to A56 gap, then along the foot of A47 to A44
        dict(id="chakh-road-2", polys=[
            [(485.2, 493.0), (485.0, 500.0), (472.5, 600.0), (471.2, 620.0), (463.3, 727.0), (468.2, 727.0), (476.2, 620.0),
             (477.6, 600.0), (488.8, 500.0), (489.0, 498.8)],
            [(485.0, 491.6), (619.0, 482.4), (619.0, 489.4), (487.5, 498.8)],
            # the gap between A55 and A56 (PDF: dotted lines run across it): from the Main Road edge to the band
            [(397.5, 609.0), (476.8, 607.0), (476.3, 616.5), (398.3, 617.8)]]),
    ],
    chakh_labels=[(276, 455, -86.6, 3.0), (272.5, 535, -86.6, 3.0), (269, 610, -86.6, 3.0), (470.5, 665, -85.6, 3.0), (480.5, 545, -83, 3.0),
                  (555, 492.4, -4.1, 3.0)],
    # nali (small drains), polylines read from the PDF: (id, points). Labelled NALI in the sheet.
    nali=[("nali-1", [(650.0, 96.7), (783.4, 120.6), (790.6, 123.7)]),  # along the top of D15 & D16 (dotted line)
          ("nali-2", [(790.8, 150.0), (790.4, 252.0)]),  # between D15 & D16 and D38
          ("nali-3", [(781.6, 381.0), (781.3, 486.0)]),  # right of D17
          ("nali-4", [(482.2, 392.0), (483.0, 440.0), (484.1, 490.0)]),  # left of A47 (not marked on the first version)
          ("nali-5", [(612.9, 383.0), (618.3, 450.0), (620.5, 489.0)]),
          # behind A8 to A14: the strip's inner side from its top end to the foot of A8 (the only nali along the A1 to A14 side)
          ("nali-6", [(289.5, 273.0), (281.4, 410.0)])],  # right of A44
),
3: dict(plotted=["18"]),  # owner: plot 18 is an ordinary plotted plot (229.9 sq yd from the sheet), not a shop
}


def apply_overrides(ph, res):
    ov = OVERRIDES.get(ph)
    if not ov:
        return res
    res = [r for r in res if r["labels"][0] not in ov.get("remove", [])]
    for r in res:  # relabel (Phase 2: A48 1st and 2nd become (I) and (II))
        r["labels"] = [ov.get("rename", {}).get(t, t) for t in r["labels"]]
    by = {r["labels"][0]: r for r in res}
    for k, pts in ov.get("replace", {}).items():
        by[k]["poly"] = Polygon(pts)  # no holes, no notches
    for k, pts in ov.get("add", {}).items():
        if k in by:
            raise SystemExit(f"override add: {k} already traced, check")
        res.append(dict(poly=Polygon(pts), labels=[k], area=None))
    for r in res:
        if r["labels"][0] in ov.get("commercial", []):
            r["force_type"] = "shop"
        if r["labels"][0] in ov.get("plotted", []):
            r["force_type"] = "plot"  # owner: ordinary plotted plot, never the shop fill, whatever its area
    return res


def named_roads(ph, res, roads):
    """CHAKH ROAD bands from OVERRIDES: returns [(id, name, polygon)] (a polygon may be a multipolygon)."""
    ov = OVERRIDES.get(ph)
    out = []
    if not ov:
        return out
    plots = unary_union([r["poly"] for r in res]).buffer(0.25)
    ru = unary_union(roads)
    for c in ov.get("chakh", []):
        if "polys" in c:
            g = unary_union([Polygon(q).buffer(0) for q in c["polys"]])
        elif "poly" in c:
            g = Polygon(c["poly"]).buffer(0)
        else:
            g = unary_union([Polygon(p) for p in c["cut"]]).intersection(ru)
        g = g.difference(plots).buffer(0.2).buffer(-0.2)
        if c.get("open"):
            g = g.buffer(-c["open"]).buffer(c["open"])  # drop slivers between plots
        out.append((c["id"], "CHAKH ROAD", g))
    return out


# ---------------------------------------------------------------- roads, extras
CANON = {"MAINROAD": "MAIN ROAD", "EXISTINGCOLONYROAD": "EXISTING COLONY ROAD", "CHAKHROAD": "CHAKH ROAD",
         "MODINAGAR-HAPURROAD": "MODINAGAR - HAPUR ROAD"}
W50 = "50'-0\" WIDE ROAD"
W40 = "40'-0\" WIDE ROAD"
# Phase 1 labels that the PDF letter-spaces or splits across text lines (x, y, angle, text), page units after rotation.
# Read off the sheet by eye: every road there is 50'-0" wide except the two diagonals (40'-0").
FRAG1 = [(473, 646, -90, W50), (472, 768, -90, W50), (438, 825, 0, W50), (580, 827, 0, W50), (425, 713, 0, W50),
         (561, 715, 0, W50), (356, 469, 0, W50), (464, 399, -90, W50), (547, 635, -52, W40), (355, 810, -38, W40)]


def road_labels(ph, pg, M):
    out = []
    for b in pg.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            ts = "".join(s["text"] for s in l["spans"]).replace(" ", "")
            m = re.fullmatch(r"(\d+)'-(\d+)\"WIDEROAD", ts)
            t = f"{m[1]}'-{m[2]}\" WIDE ROAD" if m else CANON.get(ts)
            if not t or t == "MODINAGAR - HAPUR ROAD":
                continue
            bb = l["bbox"]
            q = pymupdf.Point((bb[0] + bb[2]) / 2, (bb[1] + bb[3]) / 2).transform(M)
            dx, dy = l["dir"][0] * M.a + l["dir"][1] * M.c, l["dir"][0] * M.b + l["dir"][1] * M.d
            out.append(dict(text=t, x=q.x, y=q.y, rot=math.degrees(math.atan2(dy, dx))))
    if ph == 1:
        out += [dict(text=t, x=x, y=y, rot=a) for x, y, a, t in FRAG1]
    out += [dict(text="CHAKH ROAD", x=x, y=y, rot=a, fs=f) for x, y, a, f in OVERRIDES.get(ph, {}).get("chakh_labels", [])]
    return out


def plot30(res):
    """Plot 30 has purple sides in the PDF but its outline is open on the page, so it is boxed between its
    neighbours 31 and 29 (same row), and the row's top and bottom edges."""
    g = {r["labels"][0]: r["poly"] for r in res}
    x0, x1 = g["31"].bounds[2], g["29"].bounds[0]
    return [dict(poly=box(x0, g["29"].bounds[1], x1, g["29"].bounds[3]), labels=["30"], area=None)]


# public roads: edge polylines read from the PDF (page units after rotation); upper edge first, then lower edge
PUB = {
    2: dict(name="MODINAGAR - HAPUR ROAD", name_at=(632, 763),
            U=[(391, 833), (930, 638.5)], L=[(503, 833), (930, 678)],
            arrows=[("TO HAPUR", (867, 671), 1), ("TO MODINAGAR", (765, 729), -1), ("TO HAPUR", (507, 802), 1)]),
    3: dict(name="ROAD", name_at=(303, 920),
            U=[(23, 683), (40, 690), (57, 698), (163, 756), (196, 793), (235, 841), (275, 880), (315, 906),
               (362, 936), (377, 947), (431, 977), (523, 1019)],
            L=[(23, 723), (39, 730), (145, 789), (207, 866), (252, 909), (295, 937), (341, 967), (357, 978),
               (414, 1010), (492, 1045)],
            arrows=[("TO BHADOLA", (59, 721), -1), ("TO HAPUR ROAD", (460, 1013), 1)]),
}


def extras(ph, res, roads):
    out = dict(roads=roads)
    if ph == 2:
        U = unary_union([r["poly"] for r in res])
        R = 21  # closing: fills every gap narrower than 42 units between plots (roads are 11 to 29 units wide)
        G = U.buffer(R, join_style=2).buffer(-R, join_style=2).difference(U).buffer(-3, join_style=2).buffer(3, join_style=2)
        W = unary_union([r["poly"] for r in res if r["labels"][0][0] == "S" or r["labels"][0] in ("A56", "A57", "A58", "A59")])
        # Main Road below A55 has no plot on its left, so it is the 50 ft strip left of A56 to A59 and the S strips
        s14, a59 = [r["poly"] for r in res if r["labels"][0] in ("S14", "A59")]
        W = unary_union([W, box(min(s14.bounds[0], a59.bounds[0]), a59.bounds[3] - 1, max(s14.bounds[2], a59.bounds[2]), s14.bounds[1] + 1)])
        main = unary_union([affine_transform(W, [1, 0, 0, 1, dx, 0]) for dx in range(-29, 1)]).difference(W).buffer(-1, join_style=2).buffer(1, join_style=2)
        ov = OVERRIDES[2]
        for q in ov["noroad"]:  # slivers between plots that are nali or boundary, not road (the closing would fill them)
            G = G.difference(Polygon(q))
        # Main Road below A55 as ONE straight band (left edge: sheet boundary line, right edge: A56 to A59 and the S strips),
        # replaces the computed strip that was jagged in front of S1 to S14 and broken between A55 and A56
        main = Polygon(ov["main_road"]).difference(U.buffer(0.05))
        G = unary_union([G, main])
        out["roads"] = [g for g in (G.geoms if hasattr(G, "geoms") else [G]) if g.area > 150]
    p = PUB.get(ph)
    if p:
        up, lo = LineString(p["U"]), LineString(p["L"])
        poly = Polygon(p["U"] + p["L"][::-1])
        pts = []
        for i in range(41):
            a, b = up.interpolate(i / 40, True), lo.interpolate(i / 40, True)
            pts.append(((a.x + b.x) / 2, (a.y + b.y) / 2))
        out["pub"] = dict(poly=poly, center=LineString(pts), name=p["name"], name_at=p["name_at"], arrows=p["arrows"])
    return out


# ---------------------------------------------------------------- drawing
ROADC, PUBC = "#7B8390", "#4B5563"
CHAKHFS = 2.6  # ONE shared chakh style (Phase 1 look): earthy fill CHAKHC, edge CHAKHS .3 wide, label white on the band, bold, letter-spaced, 2.6 px, centred on the band
CHAKHC, CHAKHS, NALIC = "#9C6B2F", "#6E4817", "#7A92A8"  # chakh road (earthy, clearly apart from the grey roads), nali (restrained blue-grey)
PAL = {  # fill, soft stroke: tints of the brand green, yellow and red plus neutrals
    "sage": ("#CDE4D8", "#86B8A0"), "deep": ("#A9D2BD", "#5E9E82"), "sun": ("#FBEDA6", "#DFC654"),
    "rose": ("#F4D6D2", "#DB9F99"), "shop": ("#F3C58F", "#C98A3C"), "mist": ("#DDE2E8", "#A3AEBC")}


def block_of(ph, num):
    if ph == 1:
        return num[0] if num[0] in "EDC" else "B" if num[0] in "BS" else "N"
    if ph == 2:
        return num[0]
    k = int(num)
    return "W" if k <= 9 else "E" if k <= 16 else "S"


BLOCKS = {
    1: [("N", "mist", "Industrial plots"), ("D", "sun", "Block D"), ("C", "rose", "Block C"),
        ("B", "deep", "Blocks B and S")],
    2: [("A", "sage", "Block A"), ("B", "sun", "Block B"), ("C", "rose", "Block C"), ("D", "mist", "Block D"),
        ("S", "deep", "Strip plots S")],
    3: [("W", "sage", "Plots 1 to 9"), ("E", "sun", "Plots 10 to 16"), ("S", "rose", "Plots 17 to 23")],
}
CAP = {1: 6.5, 2: 7.2, 3: 11}
INSET = {1: .7, 2: .8, 3: 1.5}
RFS = {1: 4.6, 2: 5.2, 3: 8.5}
EXT = {1: 3.3, 2: 3.6}  # font size of leader labels for plots too small to hold their number


def fit_label(poly, text, cap):
    """Largest font size at which the text box sits inside the plot, horizontal, along the plot's long axis,
    or vertical. Horizontal wins unless another angle fits a much bigger size. Returns (x, y, size, angle)."""
    inner = poly.buffer(-0.4)
    if inner.is_empty or inner.geom_type != "Polygon":
        inner = poly
    pole = polylabel(inner, 0.2)
    cs = list(poly.minimum_rotated_rectangle.exterior.coords)
    e = max(((cs[i + 1][0] - cs[i][0], cs[i + 1][1] - cs[i][1]) for i in range(2)), key=lambda v: math.hypot(*v))
    ang = (math.degrees(math.atan2(e[1], e[0])) + 90) % 180 - 90  # readable: -90..90
    tries = [0.0]
    if abs(ang) > 12:
        tries.append(ang)
    if abs(abs(ang) - 90) > 12:
        tries.append(-90.0)
    cands = [inner.centroid, pole] if inner.contains(inner.centroid) else [pole]
    best = {}
    for a in tries:
        fs = cap
        while fs >= 1.5:
            w, h = .64 * fs * len(text) + .5, .78 * fs + .3
            for c in cands:
                bx = shp_rotate(box(c.x - w / 2, c.y - h / 2, c.x + w / 2, c.y + h / 2), a, origin=(c.x, c.y))
                if inner.contains(bx):
                    best[a] = (c.x, c.y, fs, a)
                    break
            if a in best:
                break
            fs -= .25
    if not best:
        return (pole.x, pole.y, 1.5, 0.0)
    top = max(best.values(), key=lambda v: v[2])
    h0 = best.get(0.0)
    return h0 if h0 and h0[2] >= .8 * top[2] else top


def fmt(v):
    return f"{v:.1f}".rstrip("0").rstrip(".")


def pth(g):
    return "M" + "L".join(f"{fmt(x)} {fmt(y)}" for x, y in list(g.exterior.coords)[:-1]) + "Z"


def svg(ph, d):
    P = d["plots"]
    pub = d.get("pub")
    x0, y0, x1, y1 = unary_union([p["poly"] for p in P] + d["roads"] + [g for _, _, g in d.get("named", [])] + ([pub["poly"]] if pub else [])).bounds
    m = 24
    fl = max(5, (x1 - x0) / 80)  # legend font
    top, bot = 55, fl * 5.5
    x0 -= m; y0 -= m + top; x1 += m; y1 += m + bot
    W, H = x1 - x0, y1 - y0
    fs0 = RFS[ph]
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{fmt(x0)} {fmt(y0)} {fmt(W)} {fmt(H)}" role="img" '
         f'aria-label="Isapur Industrial Park Phase {ph} plot map">',
         "<style>svg{font-family:Inter,'Helvetica Neue',Arial,sans-serif}"
         ".plot{stroke-width:.45;cursor:pointer}"
         f".plot:hover{{filter:brightness(.9);stroke:{C['green']};stroke-width:.9}}"
         f".pn{{font-weight:600;fill:{C['charcoal']};text-anchor:middle;dominant-baseline:central;pointer-events:none}}"
         ".rl{font-weight:600;fill:#fff;text-anchor:middle;dominant-baseline:central;letter-spacing:.02em}"
         ".rx{fill:" + C["charcoal"] + ";paint-order:stroke;stroke:#fff;stroke-width:1.1}"
         ".ck{font-weight:700;letter-spacing:.1em;fill:#fff;stroke:none}"
         f".nl{{fill:{NALIC};font-size:3px;font-weight:700;letter-spacing:.18em;text-anchor:middle;dominant-baseline:central;paint-order:stroke;stroke:#fff;stroke-width:.7;pointer-events:none}}"
         ".ht{font-family:Montserrat,Inter,Arial,sans-serif;font-weight:700;fill:" + C["charcoal"] + "}"
         ".lg{font-weight:500;fill:" + C["charcoal"] + "}"]
    for k, (fill, st) in PAL.items():
        o.append(f".c-{k}{{fill:{fill};stroke:{st}}}")
    o.append("</style>")
    o.append(f'<rect x="{fmt(x0)}" y="{fmt(y0)}" width="{fmt(W)}" height="{fmt(H)}" fill="#FBFBF9"/>')
    o.append('<g id="roads">')
    for r in d["roads"]:
        o.append(f'<path d="{pth(r)}" fill="{ROADC}"/>')
    for rid, rname, g in d.get("named", []):  # named road bands (CHAKH ROAD), same fill as the other roads
        for k, q in enumerate(g.geoms if hasattr(g, "geoms") else [g]):
            if q.geom_type == "Polygon" and q.area > 1:
                o.append(f'<path id="{rid}{"" if k == 0 else "-" + str(k + 1)}" class="road-named" data-road="{rname}" d="{pth(q)}" fill="{CHAKHC}" stroke="{CHAKHS}" stroke-width=".3"><title>{rname}</title></path>')
    if pub:
        o.append(f'<path id="public-road" d="{pth(pub["poly"])}" fill="{PUBC}"/>')
    o.append("</g>")
    colors = {b: k for b, k, _ in BLOCKS[ph]}
    if ph == 1:
        colors["E"] = colors["N"]  # owner: E plots take the standard plot colour, no legend entry of their own
    order = sorted(P, key=lambda p: natkey(p["labels"][0]))
    o.append(f'<g id="phase-{ph}">')
    for i, p in enumerate(order, 1):
        p["id"] = f"p{ph}-{i:03d}"
        p["num"] = " & ".join(p["labels"])
        p["block"] = block_of(ph, p["labels"][0])
        a = p["area"] or p["area_c"]
        # owner: Phase 1 shops are only the S block plots (whatever their size); Phase 2 and 3 very small plots are shops
        p["type"] = p.get("force_type") or (("shop" if p["labels"][0].startswith("S") else "plot") if ph == 1 else "shop" if a < 250 else "plot")
        nolab = p["num"].startswith("Shop ")  # unlabelled commercial shops: hover says Shop, no number text
        t = f"{'Shop' if nolab else 'Plot ' + esc(p['num'])}, {a:.0f} sq yd" + ("" if p["area"] else " (approx.)")
        g = p["poly"].buffer(-INSET[ph], join_style=2, mitre_limit=3)
        if g.is_empty:
            g = p["poly"]
        if g.geom_type != "Polygon":
            g = max(g.geoms, key=lambda q: q.area)
        hu = g.convex_hull
        if hu.area < 1.12 * g.area:  # drop small notches (survey marks) so the plot reads as the simple shape it is
            g = hu
        p["draw"] = g
        o.append(f'<path id="{p["id"]}" class="plot c-{"shop" if p["type"] == "shop" else colors[p["block"]]}" data-type="{p["type"]}" data-plot="{esc(p["num"])}" data-phase="{ph}" '
                 f'data-block="{p["block"]}" d="{pth(g)}"><title>{t}</title></path>')
    o.append('</g>')
    nali_o = []
    if d.get("nali"):  # small drains: thin blue-grey lines labelled NALI
        nali_o = ['<g id="nali">']
        for nid, pts in d["nali"]:
            ls = LineString(pts)
            nali_o.append(f'<path id="{nid}" class="nali" data-road="NALI" d="M' + "L".join(f"{fmt(x)} {fmt(y)}" for x, y in pts) +
                     f'" fill="none" stroke="{NALIC}" stroke-width="1.1" stroke-linecap="round" stroke-linejoin="round"><title>Nali (drain)</title></path>')
            for f in ((.5,) if ls.length < 150 else (.28, .72)):
                q, q2, q1 = ls.interpolate(f, True), ls.interpolate(min(1, f + .04), True), ls.interpolate(max(0, f - .04), True)
                a = math.degrees(math.atan2(q2.y - q1.y, q2.x - q1.x))
                a = a - 180 if a > 90 else a + 180 if a < -90 else a
                nali_o.append(f'<text class="nl" transform="translate({fmt(q.x)} {fmt(q.y)}) rotate({fmt(a)})">NALI</text>')
        nali_o.append("</g>")
    o += nali_o
    o.append('<g id="labels">')
    placed = []
    allp = unary_union([p["draw"] for p in order])
    for p in order:
        if p["num"].startswith("Shop "):
            continue
        x, y, fs, ang = fit_label(p["draw"], p["num"], CAP[ph])
        if ph in EXT and fs < EXT[ph] - .4:
            e = EXT[ph]
            others = allp.difference(p["draw"].buffer(.2))
            c = p["draw"].centroid
            bb = p["draw"].bounds
            r0 = max(bb[2] - bb[0], bb[3] - bb[1]) / 2 + 1
            w, h = .64 * e * len(p["num"]) + 1, .78 * e + .6
            spot = None
            for k in range(10):
                for a in range(0, 360, 30):
                    tx, ty = c.x + (r0 + k * 2.2 + w / 2) * math.cos(math.radians(a)), c.y + (r0 + k * 2.2 + h / 2) * math.sin(math.radians(a))
                    bx = box(tx - w / 2, ty - h / 2, tx + w / 2, ty + h / 2)
                    if not bx.intersects(others) and not any(bx.intersects(q) for q in placed):
                        spot = (tx, ty, bx)
                        break
                if spot:
                    break
            if spot:
                placed.append(spot[2])
                bxn = spot[2]
                o.append(f'<path d="M{fmt(c.x)} {fmt(c.y)}L{fmt(spot[0])} {fmt(spot[1])}" stroke="{C["charcoal"]}" stroke-width=".3" opacity=".6" fill="none"/>')
                o.append(f'<text class="pn" font-size="{fmt(e)}" x="{fmt(spot[0])}" y="{fmt(spot[1])}" style="paint-order:stroke;stroke:#fff;stroke-width:.5">{esc(p["num"])}</text>')
                continue
        rot = f' transform="rotate({fmt(ang)} {fmt(x)} {fmt(y)})"' if ang else ""
        o.append(f'<text class="pn" font-size="{fmt(fs)}" x="{fmt(x)}" y="{fmt(y)}"{rot}>{esc(p["num"])}</text>')
    o.append('</g><g id="road-labels">')
    allr = unary_union(d["roads"] + [g for _, _, g in d.get("named", [])] + ([pub["poly"]] if pub else []))
    for r in d["roadlabels"]:
        rot = r["rot"]
        rot = rot - 180 if rot > 90 else rot + 180 if rot < -90 else rot
        on = allr.buffer(-2).contains(Point(r["x"], r["y"]))  # label sits on a drawn road band, else ink with a halo
        cls = "rl" if on else "rl rx"
        fsz, lx_, ly_ = r.get("fs") or fs0, r["x"], r["y"]
        if r["text"] == "CHAKH ROAD":  # shared chakh label: same size and ink+halo everywhere, centred across its band
            cls, fsz = "rl ck", CHAKHFS
            cut = LineString([(lx_ - 12 * math.sin(math.radians(rot)), ly_ + 12 * math.cos(math.radians(rot))),
                              (lx_ + 12 * math.sin(math.radians(rot)), ly_ - 12 * math.cos(math.radians(rot)))]).intersection(
                unary_union([g for _, _, g in d.get("named", [])]))
            if not cut.is_empty:
                lx_, ly_ = cut.centroid.x, cut.centroid.y
        o.append(f'<text class="{cls}" font-size="{fmt(fsz)}" transform="translate({fmt(lx_)} {fmt(ly_)}) rotate({fmt(rot)})">{esc(r["text"])}</text>')
    if pub:
        cl = pub["center"]

        def at(pt, pad=0):
            s = min(max(cl.project(Point(pt)), pad), cl.length - pad)
            q = cl.interpolate(s)
            q2, q1 = cl.interpolate(min(cl.length, s + 6)), cl.interpolate(max(0, s - 6))
            return q.x, q.y, math.degrees(math.atan2(q2.y - q1.y, q2.x - q1.x))
        k = fs0
        for text, pt, sg in pub["arrows"]:
            L = k * 9
            x, y, a = at(pt, L / 2 + 4)
            hx, tx = (L / 2, -L / 2) if sg > 0 else (-L / 2, L / 2)
            hd = k * .9
            hh = -hd if sg > 0 else hd
            yy = k * 1.1
            o.append(f'<g transform="translate({fmt(x)} {fmt(y)}) rotate({fmt(a)})">'
                     f'<path d="M{fmt(tx)} {fmt(yy)}L{fmt(hx)} {fmt(yy)}" stroke="#fff" stroke-width="{fmt(k * .22)}" fill="none"/>'
                     f'<path d="M{fmt(hx)} {fmt(yy)}L{fmt(hx + hh)} {fmt(yy - hd * .7)}L{fmt(hx + hh)} {fmt(yy + hd * .7)}Z" fill="#fff"/>'
                     f'<text class="rl" font-size="{fmt(k * .95)}" y="{fmt(-k * .9)}" style="font-weight:500">{esc(text)}</text></g>')
        x, y, a = at(pub["name_at"])
        o.append(f'<text class="rl" font-size="{fmt(fs0 * 1.45)}" style="font-weight:700;letter-spacing:.12em" '
                 f'transform="translate({fmt(x)} {fmt(y)}) rotate({fmt(a)})">{esc(pub["name"])}</text>')
    o.append("</g>")
    n = d["north"]  # true north of the source sheet
    if n:
        ax, ay = x1 - 38, y0 + 40
        c, s_ = math.cos(math.radians(n["ang"])), math.sin(math.radians(n["ang"]))
        o.append(f'<g id="north"><g transform="translate({fmt(ax)} {fmt(ay)}) rotate({fmt(n["ang"] + 90)})">'
                 f'<path d="M0 -16L6 9L0 4L-6 9Z" fill="{C["charcoal"]}"/></g>'
                 f'<text class="ht" font-size="9" text-anchor="middle" dominant-baseline="central" '
                 f'x="{fmt(ax + 25 * c)}" y="{fmt(ay + 25 * s_)}">N</text></g>')
    lx, ly = x0 + m, y1 - bot + fl * .4
    o.append(f'<g id="legend"><text class="ht" font-size="{fmt(fl * 1.1)}" x="{fmt(lx)}" y="{fmt(ly + fl * .5)}">Legend</text>')
    items = [(colors[b], PAL[colors[b]][1], t) for b, _, t in BLOCKS[ph]]
    if any(p["type"] == "shop" for p in P):
        items.append(("shop", PAL["shop"][1], "Commercial shops"))
    items.append((None, ROADC, "Road"))
    if d.get("named"):
        items.append((None, CHAKHC, "Chakh road"))
    if d.get("nali"):
        items.append((None, NALIC, "Nali (drain)"))
    if pub:
        items.append((None, PUBC, "Public road"))
    cx, cy = lx, ly + fl * 2.2
    for key, col, t in items:
        w = fl * (.62 * len(t) + 2.6)
        if cx + w > x1 - m:
            cx, cy = lx, cy + fl * 1.9
        fill = PAL[key][0] if key else col
        o.append(f'<rect x="{fmt(cx)}" y="{fmt(cy - fl * .6)}" width="{fmt(fl * 1.2)}" height="{fmt(fl * 1.2)}" rx="{fmt(fl * .2)}" '
                 f'fill="{fill}" stroke="{col}" stroke-width=".5"/>'
                 f'<text class="lg" font-size="{fmt(fl)}" x="{fmt(cx + fl * 1.7)}" y="{fmt(cy)}" dominant-baseline="central">{t}</text>')
        cx += w
    o.append("</g></svg>")
    return "\n".join(o)


def main():
    out = []
    for ph in (1, 2, 3):
        d = build(ph)
        (HERE / "svg" / f"phase{ph}.svg").write_text(svg(ph, d), encoding="utf-8")
        for p in d["plots"]:
            c = p["poly"].centroid
            sheet = p["area"] is not None
            a = p["area"] if sheet else round(p["area_c"], 1)
            out.append(dict(id=p["id"], phase=ph, plot=p["num"], block=p["block"], plot_type=p["type"], area_sqyd=a, area_method="sheet" if sheet else "computed",
                            area_review=250 <= a < 300 or a > 3000, status=None,
                            centroid=[round(c.x, 1), round(c.y, 1)], bbox=[round(v, 1) for v in p["poly"].bounds]))
        print(ph, "labels", d["nlabels"], "plots", len(d["plots"]), "unreliable", d["unrel"], "merged", [p["labels"] for p in d["plots"] if len(p["labels"]) > 1], "north", d["north"])
    (HERE / "data" / "plots.json").write_text(json.dumps(out, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
