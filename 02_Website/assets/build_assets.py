"""Fresh website assets for IIP, generated in code from the brand kit (colours, kitlib badge, Montserrat/Inter outlined).
Run: python 02_Website/assets/build_assets.py
Writes SVG sources to 02_Website/assets/svg/ and web outputs to 02_Website/site/public/img/ (+ favicons in public/).
Nothing here is a photo of the park. Illustrations are labelled illustrative where they could be mistaken for the site."""
import math, pathlib, shutil, sys, random, io
ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "01_Brand/Brand-Kit/_build"))
import kitlib as K
from kitlib import text, width, svg, badge, stripe, sunburst, icon, lockup_horizontal

K.MODE["outline"] = True
A = ROOT / "02_Website/assets"; SV = A / "svg"; PUB = ROOT / "02_Website/site/public"; IMG = PUB / "img"
for d in (SV, IMG, IMG / "og", IMG / "textures", IMG / "spot", IMG / "cards", IMG / "slots"): d.mkdir(parents=True, exist_ok=True)

YEL, RED, GRN, INK = "#FFD600", "#E53935", "#0F4D3A", "#111827"
BONE, SAGE, CREAM, MIST, GRAY, LINE = "#F4F0E8", "#EEF2EE", "#FFF6CC", "#F2F4F6", "#6B7280", "#E5E7EB"
SUN = "#FFE27A"; ROAD, CURB = "#CDD2D9", "#AEB6C1"; GRASS, HEDGE, LEAF = "#58A56B", "#2F7D4A", "#3F9A5A"
XB, SB, IM, IS = "Montserrat-ExtraBold", "Montserrat-SemiBold", "Inter-Medium", "Inter-SemiBold"
OUT = {}      # name -> svg string (also copied to public/img when WEB True)


def put(name, s, web=None):
    (SV / f"{name}.svg").write_text(s, encoding="utf-8")
    if web: (IMG / web / f"{name}.svg" if web is not True else IMG / f"{name}.svg").write_text(s, encoding="utf-8")


def shade(hexc, f):
    h = hexc.lstrip("#"); r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return "#%02x%02x%02x" % tuple(max(0, min(255, int(c * f))) for c in (r, g, b))


# ------------------------------------------------------------------ 1. hero illustration (flat side elevation)
def tree(x, base, s=1.0, c1=LEAF, c2=HEDGE):
    return (f'<rect x="{x - 5 * s:.1f}" y="{base - 78 * s:.1f}" width="{10 * s:.1f}" height="{78 * s:.1f}" rx="3" fill="#7A5A3C"/>'
            f'<circle cx="{x:.1f}" cy="{base - 96 * s:.1f}" r="{44 * s:.1f}" fill="{c2}"/><circle cx="{x - 30 * s:.1f}" cy="{base - 76 * s:.1f}" r="{30 * s:.1f}" fill="{c1}"/>'
            f'<circle cx="{x + 32 * s:.1f}" cy="{base - 80 * s:.1f}" r="{32 * s:.1f}" fill="{c1}"/><circle cx="{x + 4 * s:.1f}" cy="{base - 124 * s:.1f}" r="{28 * s:.1f}" fill="{c1}"/>')


def street_light(x, base, h=230, arm=-60):
    top = base - h
    return (f'<rect x="{x - 3}" y="{top}" width="6" height="{h}" fill="{INK}" opacity=".85"/>'
            f'<path d="M{x} {top + 6}Q{x + arm / 2} {top - 14} {x + arm} {top + 6}" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round" opacity=".85"/>'
            f'<ellipse cx="{x + arm}" cy="{top + 12}" rx="17" ry="7" fill="{YEL}"/><ellipse cx="{x + arm}" cy="{top + 12}" rx="38" ry="22" fill="{YEL}" opacity=".25"/>'
            f'<rect x="{x - 14}" y="{base - 12}" width="28" height="12" rx="3" fill="{INK}" opacity=".85"/>')


def shed(x, w, h, accent, base=470):
    y = base - h
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#D6DEE7"/>'
    for i in range(int(w // 24)): s += f'<rect x="{x + 12 + i * 24}" y="{y}" width="3" height="{h}" fill="#C2CDD9"/>'
    s += f'<rect x="{x - 8}" y="{y - 22}" width="{w + 16}" height="22" rx="4" fill="#7A8BA0"/>'
    s += f'<rect x="{x - 8}" y="{y - 6}" width="{w + 16}" height="10" fill="{accent}"/>'
    sw = w * 0.42; sx = x + (w - sw) / 2
    s += f'<rect x="{sx - 8}" y="{y + h * 0.28}" width="{sw + 16}" height="{h * 0.72}" fill="#9AA8B8"/><rect x="{sx}" y="{y + h * 0.32}" width="{sw}" height="{h * 0.68}" fill="#F1F4F8"/>'
    for i in range(int(h * 0.68 // 15)): s += f'<rect x="{sx}" y="{y + h * 0.32 + 12 + i * 15}" width="{sw}" height="2.4" fill="#C9D2DC"/>'
    s += f'<rect x="{x + 22}" y="{y + 28}" width="{w - 44}" height="26" rx="3" fill="#BFE0F0"/>'
    for i in range(1, int((w - 44) // 60)): s += f'<rect x="{x + 22 + i * 60}" y="{y + 28}" width="3" height="26" fill="#D6DEE7"/>'
    s += f'<rect x="{x + w - 58}" y="{y + h - 92}" width="34" height="92" fill="#8795A6"/><rect x="{x + w - 54}" y="{y + h - 88}" width="26" height="88" fill="#E8EDF2"/>'
    return s


def truck(x, y):
    s = f'<rect x="{x}" y="{y - 70}" width="176" height="68" rx="5" fill="{GRN}"/><rect x="{x}" y="{y - 30}" width="176" height="8" fill="{YEL}"/><rect x="{x}" y="{y - 22}" width="176" height="6" fill="{RED}"/>'
    s += f'<path d="M{x + 180} {y - 50}h38l24 22v24h-62z" fill="{YEL}"/><path d="M{x + 192} {y - 44}h24l14 16h-38z" fill="#BFE0F0"/>'
    for wx in (x + 28, x + 70, x + 206):
        s += f'<circle cx="{wx}" cy="{y}" r="15" fill="{INK}"/><circle cx="{wx}" cy="{y}" r="6" fill="#9AA3AF"/>'
    return s


def hero_body():
    b = f'<rect width="1600" height="700" fill="#FFF3C4"/>'
    b += sunburst(1180, 330, 600, SUN, opacity=0.5, n=22) + sunburst(1180, 330, 380, "#FFD966", opacity=0.35, n=22)
    for cx, cy, sc in ((250, 110, 1.0), (760, 70, 0.8), (1420, 120, 1.1)):
        b += f'<g fill="#FFFFFF" opacity=".85"><circle cx="{cx}" cy="{cy}" r="{26 * sc}"/><circle cx="{cx + 30 * sc}" cy="{cy + 6 * sc}" r="{32 * sc}"/><circle cx="{cx + 66 * sc}" cy="{cy + 10 * sc}" r="{22 * sc}"/><rect x="{cx - 26 * sc}" y="{cy + 8 * sc}" width="{110 * sc}" height="{24 * sc}" rx="{12 * sc}"/></g>'
    b += f'<path d="M0 470V420Q120 380 260 410T520 400T800 415T1080 395T1360 410T1600 395V470Z" fill="#BFDCC8"/>'
    xs = [(50, 330, 196, GRN), (410, 360, 214, YEL), (820, 350, 190, RED), (1220, 330, 206, GRN)]
    for x, w, h, ac in xs: b += shed(x, w, h, ac)
    b += f'<rect x="0" y="470" width="1600" height="72" fill="{GRASS}"/><rect x="0" y="470" width="1600" height="8" fill="#6DB87E"/>'
    for i in range(0, 1600, 54): b += f'<rect x="{i + 4}" y="{486 + (i // 54 % 2) * 4}" width="48" height="26" rx="13" fill="{HEDGE}"/>'
    b += f'<rect x="0" y="542" width="1600" height="12" fill="{CURB}"/><rect x="0" y="554" width="1600" height="146" fill="{ROAD}"/>'
    b += f'<rect x="0" y="566" width="1600" height="3" fill="#FFFFFF" opacity=".8"/><rect x="0" y="684" width="1600" height="3" fill="#FFFFFF" opacity=".8"/>'
    for i in range(-1, 18): b += f'<rect x="{i * 100 + 20}" y="622" width="58" height="7" rx="2" fill="{YEL}"/>'
    for x in (140, 520, 930, 1330, 1540): b += tree(x, 542, 1.0 if x % 2 else 0.88)
    for x in (320, 720, 1120, 1480): b += street_light(x, 542)
    b += truck(1000, 614)
    b += f'<rect x="0" y="688" width="1600" height="12" fill="{GRN}"/><rect x="0" y="688" width="533" height="12" fill="{YEL}"/><rect x="533" y="688" width="533" height="12" fill="{RED}"/>'
    return b


def hero():
    full = svg(1600, 700, hero_body(), "1600px", "700px", "Illustration: industrial park street with sheds, 50 ft road, trees and street lights (not a photo of the park)")
    put("hero-illustration", full, True)
    body = hero_body()
    m = (f'<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="430 0 780 700" width="780" height="700">'
         f'<title>Illustration: industrial park street (mobile crop, not a photo of the park)</title>{body}</svg>\n')
    put("hero-illustration-mobile", m, True)
    return body


# ------------------------------------------------------------------ 2. plot layout schematic (isometric)
def iso_layout():
    S = 0.68; ox, oy = 470, 120
    P = lambda x, y, z=0: (ox + (x - y) * 0.866 * S, oy + (x + y) * 0.5 * S - z * S)
    poly = lambda pts, fill, extra="": '<polygon points="' + " ".join(f"{P(*p)[0]:.1f},{P(*p)[1]:.1f}" for p in pts) + f'" fill="{fill}" {extra}/>'
    widths, depths, gap = [190, 230, 190, 210], [120, 120, 120], 40
    W = sum(widths) + gap * (len(widths) + 1); D = sum(depths) + gap * (len(depths) + 1)
    b = f'<rect width="1200" height="800" fill="{CREAM}"/>' + sunburst(930, 120, 360, SUN, opacity=0.35, n=22)
    b += poly([(-70, -70, 0), (W + 70, -70, 0), (W + 70, D + 150, 0), (-70, D + 150, 0)], "#BFE3C8")
    b += poly([(-6, -6, 0), (W + 6, -6, 0), (W + 6, D + 6, 0), (-6, D + 6, 0)], CURB)
    b += poly([(0, 0, 0), (W, 0, 0), (W, D, 0), (0, D, 0)], ROAD)
    b += poly([(-70, D + 30, 0), (W + 70, D + 30, 0), (W + 70, D + 120, 0), (-70, D + 120, 0)], "#BFC6CF")      # main road along the front
    b += poly([(-70, D + 74, 0), (W + 70, D + 74, 0), (W + 70, D + 79, 0), (-70, D + 79, 0)], YEL)
    gx = W / 2
    # dashed centre lines in the road gaps
    xs, x0 = [], gap
    for w in widths: xs.append(x0); x0 += w + gap
    ys, y0 = [], gap
    for d in depths: ys.append(y0); y0 += d + gap
    lines = []
    for i in range(len(widths) + 1): lines.append(((xs[i] - gap / 2 if i < len(widths) else W - gap / 2), None))
    for i in range(len(widths) + 1):
        cx = gap / 2 if i == 0 else xs[i - 1] + widths[i - 1] + gap / 2
        t = 0
        while t < D:
            b += poly([(cx - 1.6, t, 0), (cx + 1.6, t, 0), (cx + 1.6, min(t + 18, D), 0), (cx - 1.6, min(t + 18, D), 0)], YEL); t += 32
    for j in range(len(depths) + 1):
        cy = gap / 2 if j == 0 else ys[j - 1] + depths[j - 1] + gap / 2
        t = 0
        while t < W:
            b += poly([(t, cy - 1.6, 0), (min(t + 18, W), cy - 1.6, 0), (min(t + 18, W), cy + 1.6, 0), (t, cy + 1.6, 0)], YEL); t += 32
    # entry road from the front road into the park
    b += poly([(gx - 20, D, 0), (gx + 20, D, 0), (gx + 20, D + 30, 0), (gx - 20, D + 30, 0)], ROAD)
    tops = [("#CFE7D6", 1), ("#FFF1B8", 1), ("#E2EBE3", 1), ("#FFFFFF", 1), (YEL, 1), ("#D6E6F2", 1)]
    rng = random.Random(7); boxes = []
    for j, (yy, d) in enumerate(zip(ys, depths)):
        for i, (xx, w) in enumerate(zip(xs, widths)):
            boxes.append((xx + yy, xx, yy, w, d, rng.choice(tops)[0], rng.random() < 0.55, i, j))
    for _, xx, yy, w, d, c, hasshed, i, j in sorted(boxes):
        h = 14
        b += poly([(xx, yy + d, 0), (xx + w, yy + d, 0), (xx + w, yy + d, h), (xx, yy + d, h)], shade(c, 0.86))
        b += poly([(xx + w, yy, 0), (xx + w, yy + d, 0), (xx + w, yy + d, h), (xx + w, yy, h)], shade(c, 0.72))
        b += poly([(xx, yy, h), (xx + w, yy, h), (xx + w, yy + d, h), (xx, yy + d, h)], c)
        b += poly([(xx + 8, yy + 8, h + 0.1), (xx + w - 8, yy + 8, h + 0.1), (xx + w - 8, yy + d - 8, h + 0.1), (xx + 8, yy + d - 8, h + 0.1)], "none", f'stroke="{shade(c, 0.7)}" stroke-width="1.4" stroke-dasharray="5 4"')
        if hasshed:
            sx, sy, sw, sd, sh = xx + w * 0.22, yy + d * 0.25, w * 0.56, d * 0.5, 30
            b += poly([(sx, sy + sd, h), (sx + sw, sy + sd, h), (sx + sw, sy + sd, h + sh), (sx, sy + sd, h + sh)], "#C3CEDA")
            b += poly([(sx + sw, sy, h), (sx + sw, sy + sd, h), (sx + sw, sy + sd, h + sh), (sx + sw, sy, h + sh)], "#9AA8B8")
            b += poly([(sx, sy, h + sh), (sx + sw, sy, h + sh), (sx + sw, sy + sd, h + sh), (sx, sy + sd, h + sh)], "#7A8BA0")
            b += poly([(sx + sw * 0.3, sy + sd, h), (sx + sw * 0.7, sy + sd, h), (sx + sw * 0.7, sy + sd, h + sh * 0.7), (sx + sw * 0.3, sy + sd, h + sh * 0.7)], "#F1F4F8")
    # trees along the outer edges and the front verge
    def itree(x, y):
        px, py = P(x, y)
        return f'<rect x="{px - 2.5:.1f}" y="{py - 18:.1f}" width="5" height="18" fill="#7A5A3C"/><circle cx="{px:.1f}" cy="{py - 28:.1f}" r="15" fill="{HEDGE}"/><circle cx="{px - 8:.1f}" cy="{py - 22:.1f}" r="10" fill="{LEAF}"/><circle cx="{px + 9:.1f}" cy="{py - 23:.1f}" r="10" fill="{LEAF}"/>'
    for t in range(0, int(W), 90): b += itree(t + 20, -38)
    for t in range(0, int(D), 80): b += itree(-38, t + 20)
    for t in range(0, int(W) + 70, 90):
        if abs(t - gx) > 40: b += itree(t, D + 125)
    for t in range(0, int(D), 80): b += itree(W + 38, t + 30)
    # gate marker with the badge
    gxp, gyp = P(gx, D + 30)
    b += f'<rect x="{gxp - 2:.1f}" y="{gyp - 118:.1f}" width="4" height="118" fill="{INK}" opacity=".85"/>'
    b += badge(gxp - 44, gyp - 205, 88, uid="iso")
    # caption and legend
    b += text("Illustrative layout, not to scale", 60, 748, 22, IS, INK)
    b += text("Plot sizes, positions and buildings are indicative only", 60, 776, 17, IM, GRAY)
    for i, (lab, col, kind) in enumerate((("50 ft roads", ROAD, "road"), ("Plots", "#CFE7D6", "plot"), ("Planted greenery", HEDGE, "tree"))):
        y = 52 + i * 34
        b += f'<rect x="48" y="{y}" width="28" height="20" rx="4" fill="{col}"/>'
        if kind == "road": b += f'<rect x="52" y="{y + 9}" width="20" height="2.4" fill="{YEL}"/>'
        b += text(lab, 88, y + 16, 17, IS, INK)
    put("plot-layout-schematic", svg(1200, 800, b, "1200px", "800px", "Illustrative isometric plot layout, not to scale"), True)


# ------------------------------------------------------------------ 3. location diagram
def location():
    b = f'<rect width="1200" height="700" fill="{SAGE}"/>' + sunburst(600, 440, 330, "#E1ECDF", n=22)
    b += f'<path d="M-20 140L1220 100" stroke="{GRN}" stroke-width="62" fill="none"/><path d="M-20 140L1220 100" stroke="#FFFFFF" stroke-width="3" fill="none" stroke-dasharray="26 18"/>'
    b += text("Delhi-Meerut Expressway", 330, 126, 24, XB, "#FFFFFF", 0.02, "middle", None, 'transform="rotate(-1.8 330 126)"')
    b += f'<path d="M-20 452L1220 440" stroke="{ROAD}" stroke-width="40" fill="none"/><path d="M-20 452L1220 440" stroke="{YEL}" stroke-width="3.5" fill="none" stroke-dasharray="22 16"/>'
    b += text("Hapur-Modinagar Road", 330, 502, 19, IS, GRAY, 0.04, "middle")
    dots = lambda d, c: f'<path d="{d}" stroke="{c}" stroke-width="9" fill="none" stroke-linecap="round" stroke-dasharray="2 16"/>'
    b += dots("M600 440Q780 380 900 112", YEL) + dots("M600 446L150 452", RED) + dots("M600 440L1050 440", GRN)
    for x, y, col in ((900, 112, YEL), (150, 452, RED), (1050, 440, GRN)): b += f'<circle cx="{x}" cy="{y}" r="15" fill="{col}" stroke="#FFFFFF" stroke-width="5"/>'
    b += text("Expressway on-ramp", 880, 178, 25, XB, INK) + text("4.7 km driving, about 8 min", 880, 206, 19, IM, INK)
    b += text("3.9 km straight-line to", 880, 232, 16, IM, GRAY) + text("the nearest expressway point", 880, 252, 16, IM, GRAY)
    b += text("Modinagar bus stand", 60, 392, 25, XB, INK) + text("11.4 km driving, about 28 min", 60, 420, 19, IM, GRAY)
    b += text("Hapur bus stand", 1140, 380, 25, XB, INK, 0.0, "end") + text("13.4 km driving, about 31 min", 1140, 408, 19, IM, GRAY, 0.0, "end")
    b += f'<circle cx="600" cy="440" r="70" fill="#FFFFFF" stroke="{YEL}" stroke-width="6"/>' + badge(560, 400, 80, uid="loc")
    b += text("Isapur Industrial Park", 600, 580, 27, XB, INK, 0.0, "middle") + text("Hapur-Modinagar Road, Yusufpur Isapur", 600, 608, 18, IM, GRAY, 0.0, "middle")
    b += text("Schematic route diagram, not to scale. Driving times from Google Maps, 2026-11-06.", 40, 672, 17, IM, GRAY)
    put("location-diagram", svg(1200, 700, b, "1200px", "700px", "Schematic location diagram with driving distances, not to scale"), True)


# ------------------------------------------------------------------ 4. spot illustrations (480x360, stroke 2.4)
def spot_wrap(tint, body, name, title):
    b = f'<rect width="480" height="360" fill="none"/>' + sunburst(240, 180, 168, tint, n=22) + f'<g fill="none" stroke="{INK}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">{body}</g>'
    put(name, svg(480, 360, b, "480px", "360px", title), "spot")


def spots():
    # roads
    body = (f'<path d="M150 300L205 80M330 300L275 80" fill="#E6E9EE"/><path d="M150 300L205 80H275L330 300Z" fill="#CDD2D9"/>'
            f'<path d="M240 300v-30M240 250v-30M240 205v-24M240 160v-18M240 124v-12" stroke="{YEL}" stroke-width="6"/>'
            f'<path d="M130 300L195 80M350 300L285 80" stroke="{INK}"/><path d="M96 296q40-20 84-8M384 296q-40-20-84-8" stroke="{GRN}" stroke-width="6"/>'
            f'<g transform="translate(310 112)"><rect width="76" height="44" rx="8" fill="{GRN}"/><path d="M12 22h52M44 10l12 12-12 12" stroke="#FFFFFF"/></g><path d="M348 156v62" stroke="{INK}"/>')
    spot_wrap("#FFE9A0", body, "spot-roads", "Spot illustration: wide road")
    # street lighting
    body = (f'<path d="M110 300h260"/><path d="M215 300V110q0-34 40-34h50" stroke-width="3"/><path d="M215 300V110" />'
            f'<path d="M290 80h60l-10 20h-40z" fill="{YEL}"/><path d="M296 100L250 300h130L336 100z" fill="{YEL}" opacity=".22" stroke="none"/>'
            f'<rect x="200" y="290" width="30" height="12" rx="3" fill="#CDD2D9"/><path d="M110 300q30-30 60 0M400 300q-30-30-60 0" stroke="{GRN}" stroke-width="5"/>'
            f'<path d="M300 66l-10-16M326 62l0-18M352 66l10-16" stroke="{YEL}" stroke-width="5"/>')
    spot_wrap("#FFF1B8", body, "spot-street-lighting", "Spot illustration: street light")
    # planted greenery
    body = (f'<path d="M100 300h280"/><rect x="176" y="190" width="14" height="110" rx="4" fill="#7A5A3C"/><circle cx="183" cy="150" r="58" fill="{HEDGE}"/><circle cx="148" cy="176" r="38" fill="{LEAF}"/><circle cx="222" cy="170" r="40" fill="{LEAF}"/>'
            f'<rect x="300" y="220" width="12" height="80" rx="4" fill="#7A5A3C"/><circle cx="306" cy="190" r="40" fill="{LEAF}"/><circle cx="284" cy="206" r="26" fill="{HEDGE}"/>'
            f'<rect x="110" y="276" width="44" height="24" rx="12" fill="{HEDGE}"/><rect x="236" y="276" width="44" height="24" rx="12" fill="{LEAF}"/><rect x="330" y="276" width="44" height="24" rx="12" fill="{HEDGE}"/>')
    spot_wrap("#D6EBDB", body, "spot-planted-greenery", "Spot illustration: planted greenery")
    # plots
    body = (f'<path d="M110 120h260v170H110z" fill="#FFFFFF"/><path d="M110 205h260M240 120v170" />'
            f'<rect x="124" y="134" width="102" height="57" fill="#CFE7D6"/><rect x="254" y="134" width="102" height="57" fill="{YEL}"/><rect x="124" y="219" width="102" height="57" fill="#FFF1B8"/><rect x="254" y="219" width="102" height="57" fill="#D6E6F2"/>'
            f'<path d="M110 96h260M110 88v16M370 88v16" stroke="{RED}"/><path d="M92 120v170M84 120h16M84 290h16" stroke="{RED}"/>')
    spot_wrap("#DDECE0", body, "spot-plots", "Spot illustration: plots on a plan")
    # site visit
    body = (f'<path d="M110 300h260"/><path d="M130 300l50-90 50 90M220 300l60-110 60 110" fill="#E6E9EE"/>'
            f'<path d="M240 70c-30 0-52 22-52 50 0 38 52 90 52 90s52-52 52-90c0-28-22-50-52-50z" fill="{RED}"/><circle cx="240" cy="120" r="16" fill="#FFFFFF"/>'
            f'<path d="M232 120l6 6 12-14" stroke="{GRN}" stroke-width="3"/><path d="M290 250l40-14 22 36-34 10z" fill="{YEL}"/><path d="M330 236l6-18" stroke-width="3"/>')
    spot_wrap("#FFD9D6", body, "spot-site-visit", "Spot illustration: site visit")
    # documents
    body = (f'<rect x="150" y="70" width="180" height="230" rx="14" fill="#FFFFFF"/><rect x="204" y="56" width="72" height="34" rx="8" fill="{YEL}"/>'
            f'<path d="M180 130l10 10 20-22M180 180l10 10 20-22M180 230l10 10 20-22" stroke="{GRN}" stroke-width="3.4"/>'
            f'<path d="M230 126h70M230 176h70M230 226h54" stroke="{GRAY}"/><circle cx="318" cy="268" r="30" fill="{GRN}"/><path d="M304 268l10 10 18-20" stroke="#FFFFFF" stroke-width="3.4"/>')
    spot_wrap("#DCE8F2", body, "spot-documents", "Spot illustration: documents checklist")


# ------------------------------------------------------------------ 5. plot card graphics (neutral, no prices, no invented sizes)
def cards():
    def card(name, tint, art, big, small, title):
        b = f'<rect width="480" height="320" rx="24" fill="#FFFFFF" stroke="{LINE}" stroke-width="2"/><path d="M0 24Q0 0 24 0H456Q480 0 480 24V8H0Z" fill="{GRN}"/>'
        b += sunburst(380, 98, 120, tint, n=22) + f'<g fill="none" stroke="{INK}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><g transform="translate(0 -30)">{art}</g></g>'
        b += text(big, 32, 228, 34, XB, INK) + text(small, 32, 266, 21, IM, GRAY)
        b += stripe(0, 300, 480, 20, cap=False, skew=10) if False else f'<rect x="32" y="284" width="64" height="5" fill="{RED}"/>'
        put(name, svg(480, 320, b, "480px", "320px", title), "cards")
    card("card-plot-from-300", "#FFE9A0", f'<path d="M300 130h120v90H300z" fill="#CFE7D6"/><path d="M300 106h120M300 98v16M420 98v16" stroke="{RED}"/><path d="M278 130v90M270 130h16M270 220h16" stroke="{RED}"/>', "From 300 sq yards", "Industrial plots", "Card: plots from 300 sq yards")
    card("card-site-visit", "#FFD9D6", f'<path d="M360 70c-24 0-42 18-42 40 0 30 42 70 42 70s42-40 42-70c0-22-18-40-42-40z" fill="{RED}"/><circle cx="360" cy="110" r="12" fill="#FFFFFF"/>', "See it on site", "Book a site visit", "Card: site visit")
    card("card-layout-map", "#D6EBDB", f'<rect x="300" y="84" width="130" height="96" rx="6" fill="#FFFFFF"/><path d="M300 132h130M365 84v96"/><rect x="310" y="94" width="45" height="28" fill="#CFE7D6"/><rect x="375" y="142" width="45" height="28" fill="{YEL}"/>', "Layout map", "Ask for plot details", "Card: layout map and plot details")


# ------------------------------------------------------------------ 6. dividers, textures, seal
def tiles():
    # dividers
    put("divider-flag", svg(1200, 12, stripe(-12, 0, 1224, 12, cap=False, skew=12), "1200px", "12px", "Tri-colour flag divider").replace("<svg ", '<svg preserveAspectRatio="none" ', 1), True)
    d = "".join(f'<path d="M{x} 0l7 7-7 7-7-7z" fill="{YEL if i % 5 == 2 else RED}" fill-opacity=".85"/>' for i, x in enumerate(range(14, 1200, 36)))
    put("divider-diamonds", svg(1200, 14, d, "1200px", "14px", "Diamond row divider"), True)
    # tiles (CSS repeat). Colours are low opacity so text stays readable on top.
    def star(cx, cy, r, fill): return f'<polygon points="{K.sunburst_points(cx, cy, r, 22, 0.14)}" fill="{fill}"/>'
    for nm, col, op in (("sunburst-tile", GRN, 0.05), ("sunburst-tile-light", "#FFF6CC", 0.09)):
        g = "".join(star(x, y, 40, col) for x, y in ((0, 0), (170, 0), (0, 170), (170, 170), (85, 85)))
        put(nm, svg(170, 170, f'<g fill-opacity="{op}" opacity="1">{g}</g>', "170px", "170px", "Sunburst tile"), "textures")
    road = (f'<rect x="130" y="0" width="40" height="300" fill="{GRN}" fill-opacity=".07"/><rect x="0" y="130" width="300" height="40" fill="{GRN}" fill-opacity=".06"/>'
            f'<path d="M150 0v300M0 150h300" stroke="{YEL}" stroke-opacity=".6" stroke-width="3" stroke-dasharray="22 18"/>')
    put("road-lanes-tile", svg(300, 300, road, "300px", "300px", "Road lanes tile"), "textures")
    plot = f'<rect x="12" y="12" width="150" height="100" rx="3" fill="none" stroke="{GRN}" stroke-opacity=".16" stroke-width="2"/>'
    put("plot-plan-tile", svg(180, 130, plot, "180px", "130px", "Plot plan tile"), "textures")
    rings = "".join(f'<circle cx="1180" cy="120" r="{r}" fill="none" stroke="{YEL if i % 3 == 0 else GRN}" stroke-opacity="{0.28 if i % 3 == 0 else 0.10}" stroke-width="{4 if i % 3 == 0 else 2}"/>' for i, r in enumerate(range(100, 2000, 78)))
    put("halo-rings", svg(1600, 900, rings, "1600px", "900px", "Halo rings texture"), "textures")
    seal = sunburst(300, 300, 290, SUN, n=22, opacity=0.9) + sunburst(300, 300, 262, "none", "#FFFFFF", 5, n=22, opacity=0.9) + f'<circle cx="300" cy="300" r="200" fill="#FFFFFF"/>' + badge(130, 130, 340, uid="seal")
    put("seal-badge-on-sunburst", svg(600, 600, seal, "600px", "600px", "Badge on sunburst seal"), True)


# ------------------------------------------------------------------ 9. photo slots
def slots():
    for nm, w, h, lab in (("slot-16x9", 1600, 900, "16:9"), ("slot-4x3", 1200, 900, "4:3"), ("slot-1x1", 800, 800, "1:1")):
        cx, cy = w / 2, h / 2
        b = (f'<rect width="{w}" height="{h}" fill="{MIST}"/><rect x="12" y="12" width="{w - 24}" height="{h - 24}" rx="18" fill="none" stroke="{GRAY}" stroke-width="3" stroke-dasharray="14 12"/>'
             f'<g fill="none" stroke="{GRAY}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" transform="translate({cx - 40} {cy - 70})"><rect x="0" y="16" width="80" height="54" rx="8"/><circle cx="40" cy="43" r="14"/><path d="M26 16l6-10h16l6 10"/></g>')
        b += text("Real site photo goes here", cx, cy + 60, 30, IS, GRAY, 0.0, "middle") + text(lab + " placeholder, not a photo of the park", cx, cy + 96, 20, IM, GRAY, 0.0, "middle")
        put(nm, svg(w, h, b, f"{w}px", f"{h}px", f"Photo placeholder {lab}"), "slots")


# ------------------------------------------------------------------ 7. OG images
def og(name, lines, sub):
    b = f'<rect width="1200" height="630" fill="{BONE}"/>' + sunburst(1010, 250, 420, SUN, opacity=0.55, n=22) + sunburst(1010, 250, 270, "#FFD966", opacity=0.4, n=22)
    inner = hero_body()
    b += (f'<clipPath id="oc"><rect x="650" y="70" width="490" height="400" rx="26"/></clipPath><g clip-path="url(#oc)"><svg x="650" y="70" width="490" height="400" viewBox="560 120 730 600" preserveAspectRatio="xMidYMid slice">{inner}</svg></g>'
          f'<rect x="650" y="70" width="490" height="400" rx="26" fill="none" stroke="#FFFFFF" stroke-width="6"/>')
    s, wd = lockup_horizontal(56, 46, 96, uid="og"); b += s
    size = min(62, min(560 / width(l, XB, 1.0, 0.0) for l in lines)); y = 292
    for l in lines: b += text(l, 56, y, size, XB, INK); y += size * 1.18
    b += f'<rect x="56" y="{y - size * 0.6:.0f}" width="86" height="7" fill="{RED}"/>'
    ssz = min(27, 560 / width(sub, IM, 1.0, 0.0)); b += text(sub, 56, y + 44, ssz, IM, GRAY)
    b += f'<rect x="0" y="540" width="1200" height="90" fill="{GRN}"/>' + stripe(-12, 528, 1224, 12, cap=False, skew=12)
    b += text("98370 57800   |   92195 49800", 56, 598, 28, XB, "#FFFFFF", 0.02) + text("Hapur-Modinagar Road, Ghaziabad", 1144, 598, 24, IM, "#FFF6CC", 0.0, "end")
    s = svg(1200, 630, b, "1200px", "630px", "OG image: " + name)
    (A / "svg" / f"og-{name}.svg").write_text(s, encoding="utf-8")
    return s


def build():
    hero(); iso_layout(); location(); spots(); cards(); tiles(); slots()
    ogs = {"home": (["Industrial plots on", "Hapur-Modinagar Road"], "50 ft RCC roads, street lighting, planted greenery"),
           "plots": (["Industrial plots", "from 300 sq yards"], "Isapur Industrial Park, Ghaziabad"),
           "location": (["4.7 km driving to the", "Delhi-Meerut Expressway"], "Distance from Isapur Industrial Park to the on-ramp"),
           "blog": (["Industrial plot guides", "for factory owners"], "Plain advice before you buy")}
    for k, (l, s) in ogs.items(): og(k, l, s)
    print("svg built")


if __name__ == "__main__":
    build()
