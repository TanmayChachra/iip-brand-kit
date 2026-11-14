"""Builds the master map of the park: the three architect layouts (Phase 1, 2, 3) on one canvas at one common scale.
Run: python scripts/build_master.py  ->  src/assets/master.svg.html + layout-bands.json (counts across all three layouts)
Placement: each sheet is drawn at the same scale (drawing scales measured in 01_Brand/Plot-Maps/README.md: 0.4480, 0.5768, 0.9218 PDF units per foot).
The sheets are NOT placed at their true positions on the ground: that needs the owner's KML or Google Earth export (see the empty #satellite-slot)."""
import json, math, pathlib, re, statistics

HERE = pathlib.Path(__file__).resolve().parent
SITE = HERE.parent
ROOT = SITE.parents[1]
OUT = SITE / "src/assets"
PM = ROOT / "01_Brand/Plot-Maps"
PPU = {1: 0.4480, 2: 0.5768, 3: 0.9218}                      # PDF units per foot, measured
VB = {1: (110.7, -5.6, 632.9, 1175.0), 2: (113.4, -56.2, 840.6, 895.0), 3: (-1.0, 129.6, 604.8, 945.0)}  # minx, miny, w, h (legend cropped)
BANDS = [("b1", "300 to 500 sq yards", 285, 500), ("b2", "500 to 1000 sq yards", 500, 1000), ("b3", "1000 to 2500 sq yards", 1000, 2501)]
plots = {p["id"]: p for p in json.load(open(PM / "data/plots.json", encoding="utf-8"))}


def band(p):
    if p["plot_type"] == "shop": return "shop"
    for k, _, lo, hi in BANDS:
        if lo <= p["area_sqyd"] < hi: return k
    return ""


def clean(ph, cnt):
    s = open(PM / f"svg/phase{ph}.svg", encoding="utf-8").read()
    s = re.sub(r"<style>.*?</style>\n?", "", s, flags=re.S)
    s = re.sub(r'<g id="legend".*?</g>\s*(?=</svg>)', "", s, flags=re.S)
    s = re.sub(r'<rect x="[^"]*" y="[^"]*" width="[^"]*" height="[^"]*" fill="#FBFBF9"/>\n?', "", s, count=1)
    body = s[s.index(">", s.index("<svg")) + 1: s.rindex("</svg>")]
    n = [0]

    def fix(m):
        t = m.group(0)
        pid = re.search(r'id="(p\d-\d+)"', t).group(1)
        p = plots[pid]; b = band(p)
        if b: cnt[b] = cnt.get(b, 0) + 1
        t = re.sub(r'<title>.*?</title>', '', t)
        t = re.sub(r' data-(phase|block|type)="[^"]*"', '', t)
        t = t.replace(' class="plot', f' data-b="{b}" data-a="{round(p["area_sqyd"])}" style="--n:{n[0]}" class="plot')
        n[0] += 1
        return t
    body = re.sub(r'<path id="p\d-\d+".*?</path>', fix, body, flags=re.S)
    body = re.sub(r'<text class="rl( rx)?"[^>]*>[^<]*(WIDE ROAD|COLONY ROAD|CHAKH ROAD|MAIN ROAD)</text>\n?', '', body)
    body = body.replace('<g id="roads">', '<g class="rd">').replace('<g id="labels">', '<g class="lb">').replace('<g id="road-labels">', '<g class="lb2">').replace('<g id="north">', '<g class="lb2 nth">')
    body = body.replace('<path id="public-road"', '<path class="pub"')
    body = re.sub(r'<g id="phase-\d">', '<g class="plots">', body)
    body = body.replace(' fill="#111827"', '')
    body = re.sub(r'<text class="rl"( font-size="7.5" style="font-weight:700;letter-spacing:.12em")', r'<text class="rl pubL"\1', body)
    return body, n[0]


def main():
    cnt, parts, info = {}, [], {}
    sc = {p: 1 / PPU[p] for p in PPU}                        # feet per PDF unit
    wh = {p: (VB[p][2] * sc[p], VB[p][3] * sc[p]) for p in VB}
    gap = 100
    pos = {1: (0, 0), 2: (wh[1][0] + gap, 0)}
    pos[3] = (pos[2][0] + (wh[2][0] - wh[3][0]) / 2, wh[2][1] + gap + 60)
    for ph in (1, 2, 3):
        body, count = clean(ph, cnt)
        x, y = pos[ph]; mx, my, w, h = VB[ph]
        parts.append(f'<g class="ph" data-ph="{ph}" transform="translate({x:.0f} {y:.0f}) scale({sc[ph]:.4f}) translate({-mx} {-my})"><rect class="sheetbg" x="{mx}" y="{my}" width="{w}" height="{h}"/><svg x="{mx}" y="{my}" width="{w}" height="{h}" viewBox="{mx} {my} {w} {h}" overflow="hidden">{body}</svg></g>'
                     f'<text class="pl" x="{x:.0f}" y="{y - 36:.0f}">Phase {ph}</text>')
        info[ph] = [round(x), round(y) - 140, round(wh[ph][0]), round(wh[ph][1]) + 140]
    W = pos[2][0] + wh[2][0]; H = max(wh[1][1], pos[3][1] + wh[3][1])
    vb = f"-40 -180 {W + 80:.0f} {H + 220:.0f}"
    svg = (f'<svg class="mm__svg lay" viewBox="{vb}" role="img" aria-labelledby="mm-t mm-d" xmlns="http://www.w3.org/2000/svg" data-boxes=\'{json.dumps(info)}\' data-vb="{vb}">'
           '<title id="mm-t">Master map of the park: the three layouts side by side</title>'
           '<desc id="mm-d">The architect layout drawings of Phase 1, Phase 2 and Phase 3 on one canvas at one common scale. They are shown side by side, not at their true positions on the ground. You can drag to move, zoom, switch between the phases and touch a plot to see its number and size.</desc>'
           '<g class="cam"><g id="satellite-slot" data-owner-todo="Place the owner own satellite or Google Earth export here (an image element or the KML geometry). Never scrape Google imagery."></g>'
           + "".join(parts) + '</g></svg>')
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "master.svg.html").write_text(svg, encoding="utf-8")
    bands = [{"id": k, "label": lab, "n": cnt.get(k, 0)} for k, lab, *_ in BANDS] + [{"id": "shop", "label": "Shops", "n": cnt.get("shop", 0)}]
    (OUT / "layout-bands.json").write_text(json.dumps(bands), encoding="utf-8")
    print("master", len(svg), "bytes", vb, info, bands)
    # longest road subpath (own units) for the stroke draw
    mx_ = 0
    for d in re.findall(r' d="([^"]+)" fill="#7B8390"', svg):
        for sub in d.split("M")[1:]:
            pts = [tuple(map(float, q.split())) for q in re.split(r"[LZ]", sub) if q.strip()]
            mx_ = max(mx_, sum(math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)))
    print("longest road subpath", round(mx_))


if __name__ == "__main__":
    main()
