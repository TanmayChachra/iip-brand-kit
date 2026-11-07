"""Regenerates every editable asset. Run:  python Brand-Kit/_build/build_kit.py
Reads tokens/brand.tokens.json + tokens/content.json.  Writes:
  live/      SVG with editable text (install Montserrat + Inter from /fonts)
  outlined/  SVG with text converted to shapes (no fonts needed, send to the print shop)
"""
import base64, json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import kitlib as K
from kitlib import C, text, badge, lockup_vertical, lockup_horizontal, stripe, sunburst, icon, svg, width

KIT = K.KIT
CT = json.loads((KIT / "tokens/content.json").read_text())
HERO = "data:image/jpeg;base64," + base64.b64encode((KIT / "assets/hero-warehouse.jpg").read_bytes()).decode()
PH = "   |   ".join(CT["phones"])
OUTS = {}


def put(rel, s): OUTS[rel] = s


def hero(x, y, w, h, fade_top=0.0):
    """Photo slot, cover-fit. id=hero-photo so it can be swapped."""
    ar = 1024 / 542
    iw, ih = (w, w / ar) if w / h > ar else (h * ar, h)
    ix, iy = x + (w - iw) / 2, y + (h - ih) / 2
    clip = f'<clipPath id="hc{int(x)}{int(y)}"><rect x="{x}" y="{y}" width="{w}" height="{h}"/></clipPath>'
    g = f'<g clip-path="url(#hc{int(x)}{int(y)})"><image id="hero-photo" href="{HERO}" x="{ix:.1f}" y="{iy:.1f}" width="{iw:.1f}" height="{ih:.1f}" preserveAspectRatio="xMidYMid slice"/>'
    if fade_top:
        g += (f'<defs><linearGradient id="ft{int(y)}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient></defs>'
              f'<rect x="{x}" y="{y}" width="{w}" height="{fade_top}" fill="url(#ft{int(y)})"/>')
    return clip + g + "</g>"


def phones(cx, y, size, ink=None, anchor="middle"):
    ink = ink or C["charcoal"]
    return text(PH, cx, y, size, "Montserrat-ExtraBold", ink, 0.02, anchor)


def proof(cx, y, size, ink=None):
    if not CT["show_proof"]: return ""
    ink = ink or C["charcoal"]
    return text("  |  ".join(CT["proof_lines"]), cx, y, size, "Inter-SemiBold", ink, 0.02, "middle")


def tag3(x, y, size, anchor="start", ink=None):
    ink = ink or C["charcoal"]
    return "".join(text(l, x, y + i * size * 1.14, size, "Montserrat-SemiBold", ink, 0.0, anchor) for i, l in enumerate(CT["tagline"]))


# ---------------- logos ----------------
def logos():
    s, h = lockup_vertical(500, 90, 300, uid="p"); put("01_Logo/logo-primary-vertical", svg(1000, 90 + h + 90, s, "1000px", f"{90 + h + 90}px", "ISAPUR Industrial Park primary logo", C["white"]))
    s, wd = lockup_horizontal(80, 80, 260, uid="h"); put("01_Logo/logo-horizontal", svg(int(wd + 160), 420, s, f"{int(wd + 160)}px", "420px", "Horizontal logo", C["white"]))
    put("01_Logo/logo-badge-only", svg(500, 500, badge(50, 50, 400, uid="bo"), "500px", "500px", "Badge only (icon, favicon, social avatar, helmet)"))
    s, h = lockup_vertical(500, 90, 300, ink="#000000", mono=("#000000", "#FFFFFF"), line="#000000", uid="m"); put("01_Logo/logo-mono-black", svg(1000, 90 + h + 90, s, "1000px", f"{90 + h + 90}px", "Single colour black logo", C["white"]))
    s, h = lockup_vertical(500, 90, 300, ink="#FFFFFF", mono=("#FFFFFF", C["charcoal"]), line="#FFFFFF", uid="r"); put("01_Logo/logo-reversed-on-charcoal", svg(1000, 90 + h + 90, s, "1000px", f"{90 + h + 90}px", "Reversed logo for dark backgrounds", C["charcoal"]))


# ---------------- patterns ----------------
def patterns():
    put("02_Pattern/tri-colour-stripe", svg(1200, 160, stripe(40, 40, 1120, 80), "1200px", "160px", "Tri-colour stripe (highlight, tag, CTA)", C["white"]))
    put("02_Pattern/sunburst-outline", svg(800, 800, sunburst(400, 400, 340, "none", C["gray"], 4), "800px", "800px", "Sunburst outline", C["white"]))
    put("02_Pattern/sunburst-solid-yellow", svg(800, 800, sunburst(400, 400, 340, C["yellow"]), "800px", "800px", "Sunburst solid", C["white"]))
    ring = "".join(f'<polygon points="0,-26 26,0 0,26 -26,0" fill="{C["red"]}" stroke="{C["yellow"]}" stroke-width="6" transform="translate({400 + 330 * __import__("math").cos(__import__("math").pi * 2 * i / 24):.1f} {400 + 330 * __import__("math").sin(__import__("math").pi * 2 * i / 24):.1f}) rotate({360 * i / 24 + 0})"/>' for i in range(24))
    put("02_Pattern/sunburst-ring-border", svg(800, 800, ring, "800px", "800px", "Sunburst ring (border or frame)", C["white"]))
    cells = "".join(sunburst(100 + 170 * c + (85 if r % 2 else 0), 100 + 150 * r, 80, "none", "#D1D5DB", 2) for r in range(6) for c in range(6))
    put("02_Pattern/sunburst-repeat-pattern", svg(1100, 1000, cells, "1100px", "1000px", "Sunburst repeating pattern (subtle background)", C["white"]))
    pan = (f'<polygon points="260,0 1200,0 940,520 0,520" fill="{C["mist"]}"/><polygon points="0,0 360,0 100,520 0,520" fill="{C["line"]}" opacity=".7"/>')
    put("02_Pattern/diagonal-panels", svg(1200, 520, pan, "1200px", "520px", "Diagonal panels (section divider)", C["white"]))
    badges = [("PLOTS", "AVAILABLE", "NOW", C["white"], C["charcoal"], C["yellow"], C["red"]), ("GROWTH", "READY", "", C["yellow"], C["charcoal"], None, None),
              ("STRATEGIC", "LOCATION", "", C["red"], "#FFFFFF", None, None), ("SUSTAINABLE", "DEVELOPMENT", "", C["green"], "#FFFFFF", None, None)]
    s = ""
    for i, (a, b, c3, fill, ink, st, st2) in enumerate(badges):
        cx = 260 + i * 480
        if st: s += sunburst(cx, 260, 220, fill, st2, 12) + sunburst(cx, 260, 214, "none", st, 6)
        else: s += sunburst(cx, 260, 220, fill)
        lines = [l for l in (a, b, c3) if l]
        fs = 46 if len(max(lines, key=len)) <= 9 else 30
        for j, l in enumerate(lines): s += text(l, cx, 260 - (len(lines) - 1) * fs * 0.6 + j * fs * 1.25 + fs * 0.35, fs, "Montserrat-ExtraBold", ink, 0.02, "middle")
    put("02_Pattern/cta-badges", svg(2000, 520, s, "2000px", "520px", "Sunburst CTA and feature badges", C["white"]))


def icons():
    for n in K.ICONS: put(f"03_Icons/icon-{n}", svg(48, 48, icon(n, 0, 0, 48, C["charcoal"], 2.4), "256px", "256px", n))


# ---------------- templates ----------------
def pole_board(with_photo=True):
    W, H = 1000, 1600
    b = ""
    s, h = lockup_vertical(500, 80, 250, uid="pb"); b += s
    y0 = 80 + h + 70
    if with_photo:
        b += hero(0, 660, W, 740, 150)
        b += tag3(930, y0 + 90, 88, "end")
        b += proof(500, 1446, 28)
        b += phones(500, 1500, 58)
        b += stripe(0, 1556, W, 44, 40)
    else:
        b += tag3(500, y0 + 240, 120, "middle")
        b += f'<rect x="460" y="{y0 + 640}" width="80" height="8" fill="{C["red"]}"/>'
        b += proof(500, 1432, 28)
        b += phones(500, 1500, 58)
        b += stripe(0, 1556, W, 44, 40)
    return svg(W, H, b, "20in", "32in", "Pole board 20 x 32 in", C["white"])


def street_pole():
    W, H = 1000, 1500
    b = ""
    s, h = lockup_vertical(500, 70, 240, uid="sp"); b += s
    b += text(CT["tagline_one_line"].upper(), 500, 70 + h + 52, 30, "Montserrat-Medium", C["gray"], 0.22, "middle")
    b += hero(0, 520, W, 560, 120)
    feats = CT["features"]; n = len(feats); cw = W / n
    for i, (ic, l1, l2) in enumerate(feats):
        cx = cw * i + cw / 2
        b += icon(ic, cx - 28, 1110, 56, C["charcoal"], 2.4)
        b += text(l1, cx, 1210, 22, "Montserrat-SemiBold", C["charcoal"], 0.06, "middle")
        if l2: b += text(l2, cx, 1238, 22, "Montserrat-SemiBold", C["charcoal"], 0.06, "middle")
    cta = f'<polygon points="170,1340 220,1290 780,1290 830,1340 780,1390 220,1390" fill="#FFFFFF" stroke="{C["yellow"]}" stroke-width="5"/>'
    b += cta + text(CT["cta"][0], 500, 1332, 40, "Montserrat-ExtraBold", C["charcoal"], 0.06, "middle") + text(CT["cta"][1], 500, 1375, 40, "Montserrat-ExtraBold", C["charcoal"], 0.06, "middle")
    b += phones(500, 1450, 40) + stripe(0, 1480, W, 20, 18)
    return svg(W, H, b, "24in", "36in", "Street pole board 24 x 36 in (2:3)", C["white"])


def hoarding():
    W, H = 2000, 1000
    b = sunburst(1760, 520, 560, C["mist"]) + sunburst(1760, 520, 560, "none", C["line"], 4)
    s, wd = lockup_horizontal(90, 330, 330, uid="ho"); b += s
    b += f'<rect x="{1070 - 4}" y="270" width="6" height="440" fill="{C["charcoal"]}" fill-opacity=".25"/>'
    b += tag3(1150, 400, 124, "start")
    b += proof(1000, 760, 40)
    b += phones(1000, 880, 92)
    b += stripe(0, 940, W, 60, 54)
    return svg(W, H, b, "40ft", "20ft", "Hoarding 40 x 20 ft (2:1)", C["white"])


def hoarding_wide():
    """40 x 15 ft (8:3), the wide hoarding format."""
    W, H = 2000, 750
    b = sunburst(1780, 400, 430, C["mist"]) + sunburst(1780, 400, 430, "none", C["line"], 4)
    s, wd = lockup_horizontal(90, 215, 260, uid="hw"); b += s
    b += f'<rect x="{1010 - 3}" y="190" width="6" height="330" fill="{C["charcoal"]}" fill-opacity=".25"/>'
    b += tag3(1080, 245, 96, "start")
    b += proof(1000, 585, 32)
    b += phones(1000, 664, 70)
    b += stripe(0, 705, W, 45, 40)
    return svg(W, H, b, "40ft", "15ft", "Hoarding 40 x 15 ft (8:3)", C["white"])


def business_cards():
    W, H = 1050, 600
    s, wd = lockup_horizontal(70, 130, 340, uid="bc")
    front = s + stripe(0, 560, W, 40, 36)
    back = (text("Name Surname", 70, 190, 60, "Montserrat-ExtraBold", C["charcoal"]) + text("Director", 70, 245, 30, "Inter-Medium", C["gray"], 0.04)
            + f'<rect x="70" y="285" width="70" height="6" fill="{C["red"]}"/>'
            + text(CT["phones"][0], 70, 360, 36, "Montserrat-SemiBold", C["charcoal"], 0.03) + text(CT["phones"][1], 70, 410, 36, "Montserrat-SemiBold", C["charcoal"], 0.03)
            + text("sales@yourdomain.in", 70, 460, 30, "Inter-Medium", C["charcoal"]) + text(CT["address"], 70, 505, 22, "Inter-Regular", C["gray"])
            + badge(790, 70, 190, uid="bcb") + stripe(0, 560, W, 40, 36))
    put("04_Templates/business-card-front", svg(W, H, front, "3.5in", "2in", "Business card front 3.5 x 2 in", C["white"]))
    put("04_Templates/business-card-back", svg(W, H, back, "3.5in", "2in", "Business card back 3.5 x 2 in", C["white"]))


def letterhead():
    W, H = 2100, 2970
    s, wd = lockup_horizontal(160, 150, 300, uid="lh")
    b = s + stripe(0, 0, W, 38, 34)
    b += f'<rect x="160" y="520" width="1780" height="2" fill="{C["line"]}"/>'
    b += stripe(0, 2860, W, 38, 34) + text(CT["address"], 160, 2815, 34, "Inter-Regular", C["gray"]) + text("  |  ".join(CT["phones"]), 1940, 2815, 34, "Inter-SemiBold", C["charcoal"], 0, "end")
    put("04_Templates/letterhead-A4", svg(W, H, b, "210mm", "297mm", "Letterhead A4", C["white"]))


def id_card():
    W, H = 540, 860
    b = stripe(0, 0, W, 34, 30)
    s, h = lockup_vertical(270, 80, 120, uid="id"); b += s
    b += f'<rect x="170" y="330" width="200" height="240" rx="14" fill="{C["mist"]}" stroke="{C["line"]}" stroke-width="2"/>' + text("PHOTO", 270, 460, 24, "Inter-Medium", C["gray"], 0.1, "middle")
    b += text("Employee Name", 270, 640, 42, "Montserrat-ExtraBold", C["charcoal"], 0, "middle") + text("Designation  |  ID 0001", 270, 685, 24, "Inter-Medium", C["gray"], 0.04, "middle")
    b += stripe(0, 800, W, 60, 54)
    put("04_Templates/id-card-54x86mm", svg(W, H, b, "54mm", "86mm", "ID card 54 x 86 mm", C["white"]))


def social():
    W, H = 1080, 1920
    b = sunburst(900, 1500, 520, C["mist"])
    s, h = lockup_vertical(540, 190, 300, uid="wa"); b += s
    b += tag3(540, 930, 110, "middle")
    b += f'<rect x="480" y="1300" width="120" height="9" fill="{C["red"]}"/>'
    b += f'<rect x="140" y="1480" width="800" height="150" rx="75" fill="{C["charcoal"]}"/>' + text("Call for a site visit", 540, 1535, 36, "Inter-Medium", "#FFFFFF", 0.03, "middle") + text(CT["phones"][0], 540, 1595, 54, "Montserrat-ExtraBold", C["yellow"], 0.03, "middle")
    b += stripe(0, 1850, W, 70, 64)
    put("04_Templates/whatsapp-status-1080x1920", svg(W, H, b, "1080px", "1920px", "WhatsApp status 9:16", C["white"]))
    W, H = 1080, 1080
    b = sunburst(900, 180, 420, C["mist"])
    s, wd = lockup_horizontal(80, 90, 230, uid="so"); b += s
    b += tag3(80, 560, 120, "start") + stripe(0, 1000, W, 80, 72) + phones(540, 930, 52, anchor="middle")
    put("04_Templates/social-post-1080x1080", svg(W, H, b, "1080px", "1080px", "Social post 1:1", C["white"]))


def build_all():
    for outline in (False, True):
        K.MODE["outline"] = outline
        OUTS.clear()
        logos(); patterns(); icons()      # round 5: signage, stationery and social now live in build_signage.py, build_stationery.py, build_social.py
        sub = "outlined" if outline else "live"
        for rel, s in OUTS.items():
            p = KIT / sub / (rel + ".svg"); p.parent.mkdir(parents=True, exist_ok=True); p.write_text(s, encoding="utf-8")
    print("built", len(OUTS), "assets x 2 modes")


if __name__ == "__main__":
    build_all()
