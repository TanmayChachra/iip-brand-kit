"""IIP signage, redesigned from scratch (round 5). No photos: white, charcoal, sunburst crop, tri-colour stripe, polished icons.
Writes live/ and outlined/ 04_Templates/sign-*.svg.  Run: python Brand-Kit/_build/build_signage.py   (parent then runs export.py)
Taglines are adaptive: variant A = 'A Modern Industrial Address.', variant B = 'The Groundwork for Growth.'  (tokens/content.json).
Units: pole 50 u/in, hoarding 100 u/ft.  Every design is drawn by art(e): e = bleed extension in user units (0 = trim size)."""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import kitlib as K
from kitlib import C, text, width, lockup_vertical, lockup_horizontal, sunburst, stripe, icon, svg

CT = json.loads((K.KIT / "tokens/content.json").read_text())
LINES = CT["taglines"]["alt_lines"]; TAG_A, TAG_B = list(LINES)[0], list(LINES)[1]
PH = [f"{p[:5]} {p[5:]}" for p in CT["phones"]]
INK, MIST, RING, GRAY = C["charcoal"], C["mist"], "#D5DAE1", C["gray"]
XB, SB, IM, IS = "Montserrat-ExtraBold", "Montserrat-SemiBold", "Inter-Medium", "Inter-SemiBold"


# ---------- small helpers ----------
def fit(lines, font, maxw, tracking=0.0):
    """Font size so the widest line is exactly maxw."""
    return maxw / max(width(l, font, 1.0, tracking) for l in lines)


def tagline(lines, x, y, size, anchor="start", lh=1.06, ink=INK):
    s = "".join(text(l, x, y + i * size * lh, size, XB, ink, 0.0, anchor) for i, l in enumerate(lines))
    return s, y + (len(lines) - 1) * size * lh


def phones(x, y, size, anchor="start", gap=1.14, ink=INK):
    return "".join(text(p, x, y + i * size * gap, size, XB, ink, 0.01, anchor) for i, p in enumerate(PH)), y + size * gap


def rule(x, y, w, h): return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{C["red"]}"/>'


def v_extent(w):
    """Half width of lockup_vertical for badge width w (mirror of its geometry)."""
    fs = w * 0.48; sub = fs * 0.27
    sw = width("INDUSTRIAL PARK", SB, sub, 0.30); lw = max(fs * 0.55, (width("ISAPUR", XB, fs, 0.035) - sw) / 2 - sub * 0.9)
    return max(w / 2, sw / 2 + sub * 0.7 + lw)


def v_lockup_left(x, y, w, uid):
    """Vertical lockup whose left edge sits on x."""
    s, h = lockup_vertical(x + v_extent(w), y, w, uid=uid); return s, h, 2 * v_extent(w)


def facts(x, y, w, size, items, ink=INK):
    """One line fact strip: icon + label, evenly spaced by measured width, hairline dividers. items = [(icon, label)]."""
    ws = [size * 2.4 + width(lab, IS, size, 0.05) for _, lab in items]
    gap = (w - sum(ws)) / (len(items) - 1); cx = x; s = ""
    for i, ((ic, lab), iw) in enumerate(zip(items, ws)):
        s += icon(ic, cx, y - size * 1.25, size * 1.9, ink, 2.6) + text(lab, cx + size * 2.4, y + size * 0.3, size, IS, ink, 0.05)
        if i: s += f'<rect x="{cx - gap / 2:.1f}" y="{y - size * 1.5:.1f}" width="{max(2, size * 0.08):.1f}" height="{size * 3.2:.1f}" fill="#D1D5DB"/>'
        cx += iw + gap
    return s


FACTS = [("wide-roads", "50 FT RCC ROADS"), ("expressway", "DELHI-MEERUT EXPRESSWAY"), ("street-light", "STREET LIGHTING")]


def burst(cx, cy, r, ring=1.12):
    return sunburst(cx, cy, r, MIST) + sunburst(cx, cy, r * ring, "none", RING, max(3, r * 0.006))


def frame(W, H, e, body):
    return (f'<defs><clipPath id="cp"><rect x="{-e}" y="{-e}" width="{W + 2 * e}" height="{H + 2 * e}"/></clipPath></defs>'
            f'<g clip-path="url(#cp)"><rect x="{-e}" y="{-e}" width="{W + 2 * e}" height="{H + 2 * e}" fill="#FFFFFF"/>{body}</g>')


# ---------- designs ----------
def pole(variant):
    W, H = 1000, 1600
    def art(e):
        b = burst(W - 20, 150, 600) if variant == "A" else burst(40, 1230, 560)
        s, h = lockup_vertical(500, 110, 250, uid="pl" + variant); b += s
        lines = LINES[TAG_A if variant == "A" else TAG_B]
        size = min(fit(lines, XB, 860), 152 if variant == "A" else 130)
        y0 = 820 if variant == "A" else 890
        t, yb = tagline(lines, 500, y0, size, "middle"); b += t
        ry = yb + size * 0.40
        b += rule(500 - 75, ry, 150, 14)
        ps = 98 if variant == "A" else 118
        b += text("CALL", 500, ry + 80, 32, IS, GRAY, 0.3, "middle")
        p, yb2 = phones(500, ry + 80 + ps * 1.05, ps, "middle"); b += p
        b += stripe(-e - 76, H - 84, W + 2 * e + 2 * 76, 84 + e, 76)
        return frame(W, H, e, b)
    return art, W, H, "20in", "32in", 50


def street():
    W, H = 1200, 1800
    def art(e):
        b = burst(W - 10, 250, 700)
        s, wd = lockup_horizontal(90, 110, 100, uid="st"); k = 1020 / wd
        s, wd = lockup_horizontal(90, 110, 100 * k, uid="st"); b += s
        lines = LINES[TAG_A]
        t, yb = tagline(lines, 90, 640, 156); b += t
        b += rule(90, yb + 50, 170, 16)
        y = yb + 160
        for ic, lab in FACTS:                                                      # facts as three rows, big icons
            b += icon(ic, 90, y - 52, 76, INK, 2.6) + text(lab, 195, y + 12, 44, IS, INK, 0.04); y += 118
        p, yb2 = phones(90, y + 40, 100); b += p
        b += stripe(-e - 80, H - 90, W + 2 * e + 2 * 80, 90 + e, 80)
        return frame(W, H, e, b)
    return art, W, H, "24in", "36in", 50


def hoarding_a():
    W, H = 4000, 2000
    def art(e):
        b = burst(3350, 900, 1480)
        s, h, wd = v_lockup_left(240, 250, 640, "ha"); b += s
        lines = LINES[TAG_A]; size = min(fit(lines, XB, 1700), 290)
        t, yb = tagline(lines, 2050, 560, size); b += t
        b += rule(2050, yb + 80, 360, 34)
        p, _ = phones(2050, yb + 340, 140); b += p
        b += stripe(-e - 130, H - 150, W + 2 * e + 2 * 130, 150 + e, 130)
        return frame(W, H, e, b)
    return art, W, H, "40ft", "20ft", 100 / 12


def hoarding_b():
    W, H = 4000, 2000
    def art(e):
        b = burst(3600, 1250, 1350)
        s, wd = lockup_horizontal(260, 200, 100, uid="hb"); k = 1900 / wd
        s, wd = lockup_horizontal(260, 200, 100 * k, uid="hb"); b += s
        p, _ = phones(3740, 330, 150, "end"); b += p
        lines = LINES[TAG_B]; size = 372
        t, yb = tagline(lines, 260, 1200, size); b += t
        b += rule(260, yb + 100, 360, 34)
        b += text(CT["address"], 3740, yb + 125, 58, IM, GRAY, 0.0, "end")
        b += stripe(-e - 130, H - 150, W + 2 * e + 2 * 130, 150 + e, 130)
        return frame(W, H, e, b)
    return art, W, H, "40ft", "20ft", 100 / 12


def hoarding_wide():
    W, H = 4000, 1500
    def art(e):
        b = burst(3500, 650, 1150)
        s, wd = lockup_horizontal(240, 190, 100, uid="hw"); k = 2150 / wd
        s, wd = lockup_horizontal(240, 190, 100 * k, uid="hw"); b += s
        lines = LINES[TAG_B]; size = fit(lines, XB, 1250)
        t, yb = tagline(lines, 3760, 520, size, "end"); b += t
        p, _ = phones(3760, 920, 118, "end"); b += p
        b += facts(240, 1190, 3520, 54, FACTS)
        b += stripe(-e - 100, H - 110, W + 2 * e + 2 * 100, 110 + e, 100)
        return frame(W, H, e, b)
    return art, W, H, "40ft", "15ft", 100 / 12


def gate():
    W, H = 4000, 1000
    def art(e):
        b = burst(3700, 520, 760)
        s, wd = lockup_horizontal(260, 140, 100, uid="gt"); k = 600 / 100
        s, wd = lockup_horizontal(260, 120, 100 * k, uid="gt"); b += s
        lines = LINES[TAG_B]; size = fit(lines, XB, 1280)
        t, yb = tagline(lines, 3760, 400, size, "end"); b += t
        b += rule(3760 - 300, yb + 70, 300, 22)
        b += stripe(-e - 62, H - 70, W + 2 * e + 2 * 62, 70 + e, 62)
        return frame(W, H, e, b)
    return art, W, H, "20ft", "5ft", 100 / 12


DESIGNS = {"sign-pole-20x32in-A": pole("A"), "sign-pole-20x32in-B": pole("B"), "sign-street-pole-24x36in": street(),
           "sign-hoarding-40x20ft-A": hoarding_a(), "sign-hoarding-40x20ft-B": hoarding_b(), "sign-hoarding-40x15ft": hoarding_wide(), "sign-gate-fascia-4to1": gate()}
PRINT = {"sign-pole-20x32in-A": (1.0, 0.8), "sign-hoarding-40x20ft-A": (3.0, 12.0)}     # bleed in, slug in


def crop_marks(W, H, o, bleed, slug):
    """o = offset of trim origin inside the print canvas. Marks sit outside the bleed, never on the art."""
    s = ""; g = bleed + slug * 0.08; L = slug * 0.8; sw = max(1.2, W / 700)
    for (x, y, dx, dy) in ((0, 0, -1, -1), (W, 0, 1, -1), (0, H, -1, 1), (W, H, 1, 1)):
        X, Y = o + x, o + y
        s += f'<path d="M{X + dx * g:.1f} {Y:.1f}h{dx * L:.1f}M{X:.1f} {Y + dy * g:.1f}v{dy * L:.1f}" stroke="#000" stroke-width="{sw:.2f}"/>'
    return s


def guide(W, H, safe, label):
    """Transparent overlay, same viewBox as the art: trim, safe margin, centre lines."""
    fs = W / 70
    b = (f'<rect x="0" y="0" width="{W}" height="{H}" fill="none" stroke="#111827" stroke-width="{fs * 0.12:.1f}"/>'
         f'<rect x="{safe}" y="{safe}" width="{W - 2 * safe}" height="{H - 2 * safe}" fill="none" stroke="#0F4D3A" stroke-width="{fs * 0.12:.1f}" stroke-dasharray="{fs * 0.8:.1f} {fs * 0.5:.1f}"/>'
         f'<path d="M{W / 2} 0V{H}M0 {H / 2}H{W}" stroke="#E53935" stroke-width="{fs * 0.06:.1f}" stroke-dasharray="{fs * 0.4:.1f} {fs * 0.4:.1f}"/>')
    b += text(label, safe + fs * 0.6, safe + fs * 1.8, fs * 1.1, IS, "#0F4D3A", 0.04)
    return b


OUT = {}
for outline in (False, True):
    K.MODE["outline"] = outline; OUT.clear()
    for name, (art, W, H, pw, ph, upi) in DESIGNS.items():
        OUT["04_Templates/" + name] = svg(W, H, art(0), pw, ph, name)
        if name in PRINT:
            bi, si = PRINT[name]; bl, sl = bi * upi, si * upi; o = bl + sl
            body = (f'<g transform="translate({o:.1f} {o:.1f})">{art(bl)}</g>' + crop_marks(W, H, o, bl, sl) +
                    text(f"TRIM {pw.replace('in', ' in').replace('ft', ' ft')} x {ph.replace('in', ' in').replace('ft', ' ft')}   BLEED {bi:g} in   CROP MARKS OUTSIDE BLEED", o, W * 0 + o * 0.45, max(10, W / 110), IS, "#111827", 0.04))
            CW, CH = W + 2 * o, H + 2 * o
            OUT["04_Templates/" + name + "-print"] = svg(CW, CH, body, f"{CW / upi / (12 if pw.endswith('ft') else 1):g}{'ft' if pw.endswith('ft') else 'in'}",
                                                           f"{CH / upi / (12 if ph.endswith('ft') else 1):g}{'ft' if ph.endswith('ft') else 'in'}", name + " print, bleed and crop marks", "#FFFFFF")
    OUT["04_Templates/sign-pole-20x32in-guide"] = svg(1000, 1600, guide(1000, 1600, 75, "SAFE MARGIN 1.5 in"), "20in", "32in", "Pole board guide overlay")
    OUT["04_Templates/sign-hoarding-40x20ft-guide"] = svg(4000, 2000, guide(4000, 2000, 50, "SAFE MARGIN 6 in"), "40ft", "20ft", "Hoarding guide overlay")
    sub = "outlined" if outline else "live"
    for rel, s in OUT.items():
        p = K.KIT / sub / (rel + ".svg"); p.parent.mkdir(parents=True, exist_ok=True); p.write_text(s, encoding="utf-8")
print("signage", len(OUT))
