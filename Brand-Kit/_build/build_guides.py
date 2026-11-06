"""Accurate logo guides (additive): clear space and minimum size, drawn from the real lockup geometry.
Writes live/ and outlined/ 01_Logo/logo-clear-space-vertical, -horizontal and logo-minimum-size.  Run: python Brand-Kit/_build/build_guides.py"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import kitlib as K
from kitlib import C, text, width, badge, lockup_vertical, lockup_horizontal, svg

G = "#0F4D3A"; R = "#E53935"; GR = "#6B7280"


def vertical_extent(cx, y, w):
    """Mirror of lockup_vertical geometry -> (left, top, right, bottom)."""
    fs = w * 0.48; ty = y + w * 1.0 + fs * 0.86 + w * 0.10; sub = fs * 0.27; sy = ty + sub * 1.9
    sw = width("INDUSTRIAL PARK", "Montserrat-SemiBold", sub, 0.30)
    lw = max(fs * 0.55, (width("ISAPUR", "Montserrat-ExtraBold", fs, 0.035) - sw) / 2 - sub * 0.9)
    half = max(w / 2, sw / 2 + sub * 0.7 + lw)
    return cx - half, y, cx + half, sy + sub * 0.04


def dim(x1, y1, x2, y2, label, ox=0, oy=0):
    s = f'<path d="M{x1} {y1}L{x2} {y2}" stroke="{G}" stroke-width="2"/>'
    for (x, y) in ((x1, y1), (x2, y2)):
        vert = abs(x1 - x2) < 1
        s += (f'<path d="M{x - 7} {y}H{x + 7}" stroke="{G}" stroke-width="2"/>' if vert else f'<path d="M{x} {y - 7}V{y + 7}" stroke="{G}" stroke-width="2"/>')
    return s + text(label, (x1 + x2) / 2 + ox, (y1 + y2) / 2 + oy, 22, "Montserrat-ExtraBold", G, 0.0, "middle")


def clear_space(kind):
    W, H = 1200, 1000
    if kind == "vertical":
        bw = 215; cx, y0 = W / 2, 190
        s, h = lockup_vertical(cx, y0, bw, uid="cs"); l, t, r, b = vertical_extent(cx, y0, bw)
    else:
        bh = 215; x0, y0 = 300, 330
        s, wd = lockup_horizontal(x0, y0, bh, uid="cs"); l, t, r, b = x0, y0, x0 + wd, y0 + bh
        sh = (W - (r - l)) / 2 - l; s = f'<g transform="translate({sh:.1f} 0)">{s}</g>'; l += sh; r += sh
        bw = bh
    X = bw * 0.25
    body = s
    body += f'<rect x="{l - X:.1f}" y="{t - X:.1f}" width="{r - l + 2 * X:.1f}" height="{b - t + 2 * X:.1f}" fill="{G}" fill-opacity="0.07" stroke="{G}" stroke-width="2.5" stroke-dasharray="14 9"/>'
    body += f'<rect x="{l:.1f}" y="{t:.1f}" width="{r - l:.1f}" height="{b - t:.1f}" fill="none" stroke="{R}" stroke-width="1.6"/>'
    for (px, py) in ((l - X, t - X), (r, t - X), (l - X, b), (r, b)):          # X squares at the four corners
        body += f'<rect x="{px:.1f}" y="{py:.1f}" width="{X:.1f}" height="{X:.1f}" fill="{G}" fill-opacity="0.22" stroke="{G}" stroke-width="1.5"/>'
        body += text("X", px + X / 2, py + X / 2 + 10, 30, "Montserrat-ExtraBold", G, 0.0, "middle")
    body += dim(l - X, (t + b) / 2, l, (t + b) / 2, "X", 0, -14)
    body += dim((l + r) / 2, t - X, (l + r) / 2, t, "X", 24, 8)
    body += text("X = one quarter of the badge width", W / 2, H - 150, 30, "Montserrat-SemiBold", C["charcoal"], 0.0, "middle")
    body += text("Keep this zone free of text, edges, photos and other logos.", W / 2, H - 105, 24, "Inter-Medium", GR, 0.0, "middle")
    body += text("Red line: edge of the logo.  Green dashed line: edge of the clear space.", W / 2, H - 68, 22, "Inter-Medium", GR, 0.0, "middle")
    body += text("CLEAR SPACE, " + kind.upper() + " LOCKUP", 60, 80, 26, "Montserrat-SemiBold", C["charcoal"], 0.14)
    return svg(W, H, body, "1200px", "1000px", f"Clear space, {kind} lockup", C["white"])


def minimum_size():
    W, H = 1200, 700
    # Drawn at a true 96 dpi reference: 30 mm = 113 px, 120 px, 16 px.
    b = text("MINIMUM SIZE", 60, 80, 26, "Montserrat-SemiBold", C["charcoal"], 0.14)
    s, h = lockup_vertical(210, 170, 113, uid="m1"); b += s
    b += f'<path d="M153.5 {170 + h + 30}H266.5" stroke="{G}" stroke-width="2"/>' + text("30 mm wide (print)", 210, 170 + h + 66, 22, "Inter-Medium", C["charcoal"], 0.0, "middle")
    s, h2 = lockup_vertical(600, 170, 120, uid="m2"); b += s
    b += f'<path d="M540 {170 + h2 + 30}H660" stroke="{G}" stroke-width="2"/>' + text("120 px wide (screen)", 600, 170 + h2 + 66, 22, "Inter-Medium", C["charcoal"], 0.0, "middle")
    b += badge(940, 170, 16, uid="m3") + badge(990, 170, 32, uid="m4") + badge(1060, 170, 64, uid="m5")
    b += text("Badge alone: 16 px, 32 px, 64 px", 1020, 170 + 64 + 66, 22, "Inter-Medium", C["charcoal"], 0.0, "middle")
    s, wd = lockup_horizontal(80, 470, 70, uid="m6"); b += s
    b += text("Horizontal lockup: 25 mm tall in print, 60 px tall on screen. Never smaller.", 80 + wd + 60, 520, 24, "Inter-Medium", GR, 0.0, "start")
    b += text("Below these sizes use the badge alone.", 600, 640, 26, "Montserrat-SemiBold", C["charcoal"], 0.0, "middle")
    return svg(W, H, b, "1200px", "700px", "Minimum size", C["white"])


def monotone():
    W, H = 1200, 560
    b = text("MONOTONE USE", 60, 80, 26, "Montserrat-SemiBold", C["charcoal"], 0.14)
    cells = [("Black on white", "#FFFFFF", C["charcoal"], (C["charcoal"], "#FFFFFF")), ("Deep green on white", "#FFFFFF", G, (G, "#FFFFFF")),
             ("White on charcoal", C["charcoal"], "#FFFFFF", ("#FFFFFF", C["charcoal"])), ("White on deep green", G, "#FFFFFF", ("#FFFFFF", G))]
    for i, (lab, bg, ink, mono) in enumerate(cells):
        x = 60 + i * 280
        b += f'<rect x="{x}" y="130" width="260" height="300" rx="14" fill="{bg}" stroke="#E5E7EB"/>'
        s, h = lockup_vertical(x + 130, 175, 96, ink=ink, mono=mono, uid=f"mn{i}", line=ink); b += s
        b += text(lab, x + 130, 470, 20, "Inter-Medium", C["charcoal"], 0.0, "middle")
    b += text("Use when a job is one colour: newspaper, stamp, embossing, engraving, fax, a single colour print.", 60, 530, 22, "Inter-Medium", GR, 0.0, "start")
    return svg(W, H, b, "1200px", "560px", "Monotone use", C["white"])


def misuse():
    W, H = 1200, 700
    b = text("LOGO MISUSE", 60, 80, 26, "Montserrat-SemiBold", C["charcoal"], 0.14)
    tiles = ["Do not stretch or squash", "Do not rotate", "Do not change the colours", "Do not add shadows or glow", "Do not place on busy backgrounds", "Do not rebuild the wordmark"]
    for i, lab in enumerate(tiles):
        col, row = i % 3, i // 3; x, y = 60 + col * 375, 120 + row * 290
        cx, cy = x + 170, y + 120
        b += f'<rect x="{x}" y="{y}" width="340" height="250" rx="12" fill="#FFFFFF" stroke="#E5E7EB"/>'
        if i == 4: b += "".join(f'<rect x="{x + k * 28}" y="{y}" width="14" height="250" fill="{C["yellow"]}" opacity=".85"/>' for k in range(12))
        mono = ("#2563EB", "#F59E0B") if i == 2 else None
        s, h = lockup_vertical(0, 0, 66, mono=mono, uid=f"mu{i}")
        tf = {0: "scale(1.5 0.8)", 1: "rotate(-14)", 3: "", 5: ""}.get(i, "")
        fx = ' style="filter:drop-shadow(8px 10px 6px rgba(0,0,0,.55))"' if i == 3 else ""
        b += f'<g transform="translate({cx} {y + 34}) {tf}"{fx}>{s}</g>'
        if i == 5: b += f'<rect x="{x + 40}" y="{y + 96}" width="260" height="62" fill="#FFFFFF"/>' + text("ISAPUR", cx, y + 134, 34, "Inter-SemiBold", C["charcoal"], 0.0, "middle")
        b += f'<circle cx="{x + 310}" cy="{y + 30}" r="16" fill="#E53935"/><path d="M{x + 303} {y + 23}l14 14M{x + 317} {y + 23}l-14 14" stroke="#fff" stroke-width="3.5" stroke-linecap="round"/>'
        b += text(lab, x + 170, y + 232, 19, "Inter-Medium", C["charcoal"], 0.0, "middle")
    return svg(W, H, b, "1200px", "700px", "Logo misuse", C["white"])


OUT = {}
for outline in (False, True):
    K.MODE["outline"] = outline; OUT.clear()
    OUT["01_Logo/logo-clear-space-vertical"] = clear_space("vertical")
    OUT["01_Logo/logo-clear-space-horizontal"] = clear_space("horizontal")
    OUT["01_Logo/logo-minimum-size"] = minimum_size()
    OUT["01_Logo/logo-monotone-use"] = monotone()
    OUT["01_Logo/logo-misuse-sheet"] = misuse()
    sub = "outlined" if outline else "live"
    for rel, s in OUT.items():
        p = K.KIT / sub / (rel + ".svg"); p.write_text(s, encoding="utf-8")
print("guides", len(OUT))
