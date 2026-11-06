"""Brand kit SVG toolkit. One source (tokens + content.json) -> live-text SVG and outlined SVG for every asset.
Colours and fonts come ONLY from tokens, so a change in one place updates every file."""
import json, pathlib, functools
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

KIT = pathlib.Path(__file__).resolve().parents[1]
FONTS = KIT / "fonts"
TOK = json.loads((KIT / "tokens/brand.tokens.json").read_text())
C = {k: v["value"] for k, v in TOK["color"].items()}
BADGE = json.loads((pathlib.Path(__file__).resolve().parent / "badge-paths.json").read_text())

FONTFILE = {"Montserrat-ExtraBold": "Montserrat-ExtraBold.ttf", "Montserrat-SemiBold": "Montserrat-SemiBold.ttf",
            "Montserrat-Medium": "Montserrat-Medium.ttf", "Inter-Medium": "Inter-Medium.ttf",
            "Inter-SemiBold": "Inter-SemiBold.ttf", "Inter-Regular": "Inter-Regular.ttf"}
FAMILY = {"Montserrat-ExtraBold": ("Montserrat", 800), "Montserrat-SemiBold": ("Montserrat", 600), "Montserrat-Medium": ("Montserrat", 500),
          "Inter-Medium": ("Inter", 500), "Inter-SemiBold": ("Inter", 600), "Inter-Regular": ("Inter", 400)}
MODE = {"outline": False}


@functools.lru_cache(None)
def _font(name):
    p = FONTS / FONTFILE[name]
    blob = hb.Blob.from_file_path(str(p))
    face = hb.Face(blob)
    return hb.Font(face), TTFont(p), face.upem


def shape(text, font, size, tracking):
    hf, tt, upem = _font(font)
    buf = hb.Buffer(); buf.add_str(text); buf.guess_segment_properties()
    hb.shape(hf, buf, {"kern": True, "liga": False})
    s = size / upem
    items, x = [], 0.0
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        items.append((info.codepoint, x + pos.x_offset * s)); x += pos.x_advance * s + tracking * size
    return items, x - tracking * size


def width(text, font, size, tracking=0.0):
    return shape(text, font, size, tracking)[1]


def text(t, x, y, size, font="Montserrat-ExtraBold", fill="#111827", tracking=0.0, anchor="start", opacity=None, extra=""):
    """x,y = baseline. Live <text> by default, outlined <path> when MODE['outline']."""
    items, w = shape(t, font, size, tracking)
    x0 = x - (w / 2 if anchor == "middle" else w if anchor == "end" else 0)
    op = f' fill-opacity="{opacity}"' if opacity is not None else ""
    if MODE["outline"]:
        hf, tt, upem = _font(font); gs = tt.getGlyphSet(); order = tt.getGlyphOrder(); s = size / upem
        d = []
        for gid, gx in items:
            pen = SVGPathPen(gs); gs[order[gid]].draw(TransformPen(pen, (s, 0, 0, -s, x0 + gx, y))); d.append(pen.getCommands())
        return f'<path d="{" ".join(d)}" fill="{fill}"{op} {extra}><title>{esc(t)}</title></path>'
    fam, wt = FAMILY[font]
    ls = f' letter-spacing="{tracking * size:.2f}"' if tracking else ""
    return (f'<text x="{x0:.2f}" y="{y:.2f}" font-family="{fam}, sans-serif" font-weight="{wt}" font-size="{size:.2f}"{ls} '
            f'fill="{fill}"{op} {extra}>{esc(t)}</text>')


def esc(s): return s.replace("&", "&amp;").replace("<", "&lt;")


def badge(x, y, size, mono=None, uid="b"):
    """Traced badge placed with top-left (x,y), width=size. mono=None for full colour, or (base, detail) colours.
    The three badge paths are defined once per file (see svg()) and reused, so files stay small."""
    k = size / BADGE["w"]
    base, red, green = (BADGE["colors"][n] for n in ("base", "red", "green"))
    if mono: base, red, green = mono[0], mono[1], mono[1]
    u = lambda n, f: f'<use href="#iip-b-{n}" xlink:href="#iip-b-{n}" fill="{f}" fill-rule="evenodd"/>'
    return (f'<g id="badge-{uid}" transform="translate({x:.2f} {y:.2f}) scale({k:.5f})">{u("base", base)}{u("red", red)}{u("green", green)}</g>')


def badge_defs():
    P = BADGE["paths"]
    return '<defs>' + "".join(f'<path id="iip-b-{n}" d="{P[n]}"/>' for n in ("base", "red", "green")) + '</defs>'


def lockup_vertical(cx, y, w, ink=None, mono=None, uid="v", line=None):
    """Primary lockup. w = badge width. Returns (svg, height)."""
    ink = ink or C["charcoal"]; line = line or C["red"]
    bx = cx - w / 2
    s = badge(bx, y, w, mono, uid)
    fs = w * 0.48                                   # ISAPUR cap-height driver
    ty = y + w * 1.0 + fs * 0.86 + w * 0.10
    s += text("ISAPUR", cx, ty, fs, "Montserrat-ExtraBold", ink, 0.035, "middle")
    sub = fs * 0.27; sy = ty + sub * 1.9
    sw = width("INDUSTRIAL PARK", "Montserrat-SemiBold", sub, 0.30)
    s += text("INDUSTRIAL PARK", cx, sy, sub, "Montserrat-SemiBold", ink, 0.30, "middle")
    lw = max(fs * 0.55, (width("ISAPUR", "Montserrat-ExtraBold", fs, 0.035) - sw) / 2 - sub * 0.9)
    ly = sy - sub * 0.36
    for sgn in (-1, 1):
        x1 = cx + sgn * (sw / 2 + sub * 0.7); x2 = x1 + sgn * lw
        s += f'<rect x="{min(x1, x2):.2f}" y="{ly - sub * 0.07:.2f}" width="{lw:.2f}" height="{sub * 0.14:.2f}" fill="{line}"/>'
    return s, sy + sub * 0.5 - y


def lockup_horizontal(x, y, h, ink=None, mono=None, uid="h", line=None, divider=True):
    """Horizontal lockup (owner approved layout, round 5): badge | thick rule | ISAPUR over INDUSTRIAL PARK.
    INDUSTRIAL PARK is tracked so both lines have exactly the same width. No red line unless line is given."""
    ink = ink or C["charcoal"]
    s = badge(x, y, h, mono, uid)
    rx = x + h + h * 0.22
    s += f'<rect x="{rx:.2f}" y="{y + h * 0.13:.2f}" width="{h * 0.022:.2f}" height="{h * 0.74:.2f}" fill="{ink}"/>'
    tx = rx + h * 0.26
    fs = h * 0.40
    wI = width("ISAPUR", "Montserrat-ExtraBold", fs, 0.02)
    sub = fs * 0.30
    base = width("INDUSTRIAL PARK", "Montserrat-SemiBold", sub, 0.0)
    tr = (wI - base) / (14 * sub)                      # tracking that makes the second line as wide as the first
    cap1, cap2 = fs * 0.70, sub * 0.70; gap = h * 0.075
    top = y + h / 2 - (cap1 + gap + cap2) / 2
    by1 = top + cap1; by2 = by1 + gap + cap2
    s += text("ISAPUR", tx, by1, fs, "Montserrat-ExtraBold", ink, 0.02)
    s += text("INDUSTRIAL PARK", tx, by2, sub, "Montserrat-SemiBold", ink, tr)
    if line:
        s += f'<rect x="{tx:.2f}" y="{by2 + sub * 0.7:.2f}" width="{wI:.2f}" height="{sub * 0.13:.2f}" fill="{line}"/>'
    return s, tx + wI - x


def stripe(x, y, w, h, skew=None):
    """Tri-colour stripe (yellow, red, green) of parallelograms. h = height."""
    sk = skew if skew is not None else h * 0.9
    unit = (w - sk) / 3.0
    cols = [C["yellow"], C["red"], C["green"]]
    s = ""
    for i, c in enumerate(cols):
        x0 = x + i * unit
        s += f'<polygon points="{x0 + sk:.1f},{y:.1f} {x0 + sk + unit * 1.05:.1f},{y:.1f} {x0 + unit * 1.05:.1f},{y + h:.1f} {x0:.1f},{y + h:.1f}" fill="{c}"/>'
    return s


def sunburst_points(cx, cy, r, n=24, depth=0.12):
    import math
    pts = []
    for i in range(n * 2):
        a = math.pi * i / n - math.pi / 2
        rr = r if i % 2 == 0 else r * (1 - depth)
        pts.append(f"{cx + rr * math.cos(a):.2f},{cy + rr * math.sin(a):.2f}")
    return " ".join(pts)


def sunburst(cx, cy, r, fill="none", stroke=None, sw=2, n=24, depth=0.12, opacity=None):
    st = f' stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"' if stroke else ""
    op = f' opacity="{opacity}"' if opacity is not None else ""
    return f'<polygon points="{sunburst_points(cx, cy, r, n, depth)}" fill="{fill}"{st}{op}/>'


ICONS = {
    "industrial-plots": '<path d="M6 40V24l10-6v6l10-6v6l10-6v22z"/><path d="M12 40v-6h4v6M24 40v-6h4v6"/><path d="M38 40V14"/>',
    "wide-roads": '<path d="M14 42L20 6M34 42L28 6"/><path d="M24 8v6M24 20v8M24 34v8"/>',
    "power-supply": '<path d="M28 4L12 28h12l-4 16 16-24H24z"/>',
    "water-supply": '<path d="M24 5C16 16 11 23 11 30a13 13 0 0026 0C37 23 32 16 24 5z"/>',
    "connectivity": '<path d="M5 20a27 27 0 0138 0M11 27a18 18 0 0126 0M17 34a9 9 0 0114 0"/><circle cx="24" cy="40" r="2.2"/>',
    "sustainable": '<path d="M24 42V24M24 24c0-9-6-14-15-14 0 9 6 14 15 14zM24 30c0-7 5-11 13-11 0 7-5 11-13 11z"/>',
    "secure": '<path d="M24 5l15 6v11c0 10-7 17-15 21C16 39 9 32 9 22V11z"/><path d="M17 24l5 5 9-10"/>',
    "business-support": '<path d="M4 26l9-8 7 3 6-3 8 6M4 26l9 10 5-1 3 3 4-1 3 3 8-8-5-8"/>',
    "plug-and-play": '<circle cx="24" cy="24" r="6"/><path d="M24 4v6M24 38v6M4 24h6M38 24h6M10 10l4 4M34 34l4 4M38 10l-4 4M14 34l-4 4"/>',
    "growth": '<path d="M6 42h36"/><path d="M10 42V30h6v12M20 42V22h6v20M30 42V14h6v28"/><path d="M8 20l10-8 8 4 12-10"/>',
}


def icon(name, x, y, size, stroke="#111827", sw=2.6):
    k = size / 48
    return (f'<g transform="translate({x:.2f} {y:.2f}) scale({k:.4f})" fill="none" stroke="{stroke}" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round"><title>{name}</title>{ICONS[name]}</g>')


def svg(w, h, body, width_attr, height_attr, title, bg=None, defs=""):
    r = f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else ""
    if '#iip-b-' in body and 'id="iip-b-base"' not in defs: defs = defs + badge_defs()
    return (f'<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'viewBox="0 0 {w} {h}" width="{width_attr}" height="{height_attr}">\n<title>{esc(title)}</title>{defs}\n{r}\n{body}\n</svg>\n')

# round 5: polished icon set (owner approved style)
from icons_v2 import ICONS_V2
ICONS.update(ICONS_V2)

# owner pick: the original wide-roads icon (from the hoarding design) and its 2.4 stroke for every icon
ICONS["wide-roads"] = '<path d="M14 42L20 6M34 42L28 6"/><path d="M24 8v6M24 20v8M24 34v8"/>'
