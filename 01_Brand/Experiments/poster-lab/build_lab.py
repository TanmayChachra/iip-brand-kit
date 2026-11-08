"""Poster lab: same layout and text as the FINAL poster, only font, background texture and colour change.
Source (never edited): Isapur-Poster/03_Design/01_LATEST_isapur-industrial-park.svg
Output: Experiments/poster-lab/svg/*.svg, png/*.png, thumbs/*.webp, index.html.   Run: python 01_Brand/Experiments/poster-lab/build_lab.py
Rules kept: badge untouched, text and layout identical, no new claims. Fonts load from Google Fonts at render time (open licence)."""
import json, math, pathlib, re, sys
import xml.etree.ElementTree as ET
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SRC = ROOT / "Isapur-Poster/03_Design/01_LATEST_isapur-industrial-park.svg"
SVGNS = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVGNS); ET.register_namespace("xlink", "http://www.w3.org/1999/xlink")
W, H = 1827, 2290
LIGHT_INK = {"#111111", "#151515", "#000000", "#111827"}


def rect(x, y, w, h, **a): return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" ' + " ".join(f'{k.replace("_", "-")}="{v}"' for k, v in a.items()) + "/>"


# ---------- textures: each returns SVG markup drawn over the background colour, under everything else ----------
def grain(opacity=0.35, freq=0.8, tint="0.35 0.30 0.22", fid="g1", seed=3):
    r, g, b = tint.split()
    return (f'<filter id="{fid}" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="{freq}" numOctaves="2" seed="{seed}" stitchTiles="stitch"/>'
            f'<feColorMatrix type="matrix" values="0 0 0 0 {r}  0 0 0 0 {g}  0 0 0 0 {b}  0 0 0 0.9 -0.28"/></filter>'
            f'<rect width="{W}" height="{H}" filter="url(#{fid})" opacity="{opacity}"/>')


def grid(color="#1f4a3c", minor=60, major=300, a1=0.07, a2=0.13):
    return (f'<defs><pattern id="gm" width="{minor}" height="{minor}" patternUnits="userSpaceOnUse"><path d="M{minor} 0H0V{minor}" fill="none" stroke="{color}" stroke-opacity="{a1}" stroke-width="1.2"/></pattern>'
            f'<pattern id="gM" width="{major}" height="{major}" patternUnits="userSpaceOnUse"><path d="M{major} 0H0V{major}" fill="none" stroke="{color}" stroke-opacity="{a2}" stroke-width="2"/></pattern></defs>'
            f'<rect width="{W}" height="{H}" fill="url(#gm)"/><rect width="{W}" height="{H}" fill="url(#gM)"/>')


def rays(cx=913.5, cy=235, n=40, color="#F2C94C", op=0.16, r=3200):
    s = ""
    for i in range(n):
        a0 = 2 * math.pi * i / n; a1 = a0 + math.pi / n
        s += f'<path d="M{cx} {cy}L{cx + r * math.cos(a0):.0f} {cy + r * math.sin(a0):.0f}L{cx + r * math.cos(a1):.0f} {cy + r * math.sin(a1):.0f}Z"/>'
    return f'<g fill="{color}" fill-opacity="{op}">{s}</g>'


def contours(color="#2f5d4a", op=0.16, step=0.22, seed=7):
    """Topographic lines (plot-and-land feel): level sets of a smooth field."""
    from skimage import measure
    rng = np.random.default_rng(seed); gx, gy = np.meshgrid(np.linspace(0, W, 228), np.linspace(0, H, 286))
    f = np.zeros_like(gx)
    for _ in range(9):
        kx, ky = rng.uniform(0.0006, 0.0022, 2) * rng.choice([-1, 1], 2); f += rng.uniform(0.5, 1) * np.sin(kx * gx * 2 * math.pi + ky * gy * 2 * math.pi + rng.uniform(0, 6.28))
    d = ""
    for lv in np.arange(f.min(), f.max(), step):
        for c in measure.find_contours(f, lv):
            if len(c) < 12: continue
            d += "M" + "L".join(f"{p[1] * W / 227:.0f} {p[0] * H / 285:.0f}" for p in c[::2])
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-opacity="{op}" stroke-width="2"/>'


def halftone(color="#C98A1B", op=0.20, pitch=34, corner=(W, 0), reach=2500):
    s = ""
    for gy in range(0, H + pitch, pitch):
        for gx in range(0, W + pitch, pitch):
            d = math.hypot(gx - corner[0], gy - corner[1]) / reach
            r = max(0, (1 - d)) ** 1.6 * pitch * 0.46
            if r > 0.8: s += f'<circle cx="{gx + (pitch / 2 if (gy // pitch) % 2 else 0)}" cy="{gy}" r="{r:.1f}"/>'
    return f'<g fill="{color}" fill-opacity="{op}">{s}</g>'


def gradient(c1, c2, fid="gr"):
    return (f'<defs><linearGradient id="{fid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient></defs>'
            f'<rect width="{W}" height="{H}" fill="url(#{fid})"/>')


def diagonal(color="#1f4a3c", op=0.07, gap=46):
    return (f'<defs><pattern id="dg" width="{gap}" height="{gap}" patternUnits="userSpaceOnUse" patternTransform="rotate(52)"><path d="M0 0V{gap}" stroke="{color}" stroke-opacity="{op}" stroke-width="3"/></pattern></defs>'
            f'<rect width="{W}" height="{H}" fill="url(#dg)"/>')


# ---------- variants ----------
V = [
    dict(id="01-bone-paper", name="Bone paper", font=("Archivo", "Archivo"), wts=(800, 500), bg="#F4F0E8", leaf="#E7E1D4", note="Warm bone base with fine paper grain. The calmest step away from pure white.",
         tex=lambda: grain(0.42, 0.85, "0.40 0.32 0.20")),
    dict(id="02-blueprint-grid", name="Blueprint hairline grid", font=("Barlow Semi Condensed", "Barlow"), wts=(800, 500), bg="#EEF2EE", leaf="#DFE7E0", note="Pale sage with an engineer's hairline grid (60 px minor, 300 px major). Says plots, survey, plan.",
         tex=lambda: grid(a1=0.11, a2=0.2)),
    dict(id="03-sunburst-echo", name="Sunburst echo", font=("Poppins", "Poppins"), wts=(800, 500), bg="#F8F2E2", leaf="#EEE5CD", note="The badge's sunburst repeated as faint rays across the whole poster. Ties everything to the logo.",
         tex=lambda: rays(op=0.22) + grain(0.22, 0.9, "0.5 0.4 0.2", "g3", 5)),
    dict(id="04-contour-land", name="Contour land", font=("Bricolage Grotesque", "Instrument Sans"), wts=(800, 500), bg="#EEF0E4", leaf="#E1E5D2", note="Topographic contour lines: land, plots, terrain. Hand-drawn feel that templates rarely have.",
         tex=lambda: contours(op=0.24) + grain(0.20, 0.9, "0.3 0.35 0.2", "g4", 9)),
    dict(id="05-concrete", name="Concrete", font=("Space Grotesk", "Space Grotesk"), wts=(700, 500), bg="#E7E6E2", leaf="#D9D8D3", note="Cool concrete grey with coarse mottling plus fine grain. Industrial, honest, a little brutalist.",
         tex=lambda: grain(0.22, 0.006, "0.25 0.25 0.24", "g5a", 2) + grain(0.5, 0.75, "0.2 0.2 0.2", "g5b", 11)),
    dict(id="06-halftone-warm", name="Warm halftone", font=("Outfit", "DM Sans"), wts=(800, 500), bg="#F7F0E3", leaf="#EDE3CF", note="Print-style halftone dots fading from the top right corner in warm amber. Poster-shop energy.",
         tex=lambda: halftone() + grain(0.18, 0.9, "0.4 0.3 0.15", "g6", 4)),
    dict(id="07-deep-green", name="Deep green night", font=("Plus Jakarta Sans", "Plus Jakarta Sans"), wts=(800, 500), bg="#0F4D3A", leaf="#13604A", dark=True, note="Brand green as the whole canvas, cream text. Boldest option; the photo sits as a clean window.",
         tex=lambda: diagonal("#FFFFFF", 0.05) + grain(0.25, 0.9, "1 1 1", "g7", 6)),
    dict(id="08-sand-gradient", name="Sand gradient", font=("Red Hat Display", "Red Hat Text"), wts=(800, 500), bg="#F8F2E4", leaf="#EDE2CB", note="Soft cream to sand gradient with a touch of grain. Quiet and premium.",
         tex=lambda: gradient("#FBF7EC", "#EAD9B8") + grain(0.25, 0.85, "0.45 0.35 0.2", "g8", 8)),
    dict(id="09-control-montserrat", name="Control: bone only", font=("Montserrat", "Inter"), wts=(800, 500), bg="#F4F0E8", leaf="#E7E1D4", note="Same Montserrat and Inter as the final, only the bone colour. Shows what the background alone changes.",
         tex=lambda: ""),
]
DARK = {"#111111": "#F6F1E4", "#151515": "#F6F1E4", "#000000": "#F6F1E4", "#111827": "#F6F1E4", "#666666": "#C9D8CF", "#101d1a": "#F6F1E4",
        "#d6d6d6": "#3F7563", "#dcdcdc": "#3F7563", "#CFCFCF": "#3F7563", "#fdfdfd": "#0F4D3A", "#ffffff": "#0F4D3A", "#FFFFFF": "#0F4D3A"}


def tag(e): return e.tag.split("}")[-1]


def make(v, hero=None):
    tree = ET.parse(SRC); root = tree.getroot()
    layer = [e for e in root.iter() if e.get("id") == "Layer_1"][0]
    logo = [e for e in root.iter() if e.get("id") == "logo"][0]
    in_logo = {id(x) for x in logo.iter()}
    hero_img = [e for e in root.iter() if tag(e) == "image"][0]
    hero_g = [e for e in root.iter() if e.get("id") == "shift-hero-photo"][0]
    hb = {id(x) for x in hero_g.iter()}
    cta_g = [e for e in root.iter() if e.get("id") == "cta-industrial-plot-available"][0]
    hb |= {id(x) for x in cta_g.iter()}
    for e in root.iter():
        if id(e) in in_logo: continue
        if tag(e) == "text":
            fam = v["font"][0] if "Montserrat" in e.get("font-family", "") else v["font"][1]
            wt = e.get("font-weight")
            e.set("font-family", f"'{fam}', sans-serif")
            if "Montserrat" in str(e.get("font-family")) or fam == v["font"][0]:
                pass
            if wt in ("800", "bold"): e.set("font-weight", str(v["wts"][0]))
            elif wt == "500": e.set("font-weight", str(v["wts"][1]))
        for k in ("fill", "stroke"):
            val = e.get(k)
            if not val: continue
            if k == "fill" and val.lower() == "#ebebeb": e.set(k, v["leaf"]); continue
            if v.get("dark"):
                if val in DARK and id(e) not in hb: e.set(k, DARK[val])
            elif k == "fill" and val.lower() in ("#fdfdfd", "#ffffff"): e.set(k, v["bg"])
    if hero:
        import base64, io
        im = Image.open(hero).convert("RGB").resize((1812, 530), Image.LANCZOS)
        if v.get("invert"):
            from PIL import ImageOps; im = ImageOps.invert(im)
        buf = io.BytesIO(); im.save(buf, "WEBP", quality=88)
        hero_img.set("{http://www.w3.org/1999/xlink}href", "data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode())
        hero_img.set("preserveAspectRatio", "xMidYMid slice")
    bgrect = [e for e in layer if e.get("id") == "background"][0]; bgrect.set("fill", v["bg"])
    if v.get("blend"):
        hero_g.set("style", f"mix-blend-mode:{v['blend']}")
    elif v.get("dark"):  # keep the photo as a clean rounded window
        cp = ET.fromstring(f'<clipPath xmlns="{SVGNS}" id="hero-window"><rect x="40" y="1122" width="1747" height="500" rx="30"/></clipPath>')
        layer.insert(0, cp); hero_g.set("clip-path", "url(#hero-window)")
    else:
        hero_g.set("style", "mix-blend-mode:multiply")
    if v.get("layout"): LAYOUTS[v["layout"]](root, layer)
    tex = ET.fromstring(f'<g xmlns="{SVGNS}" id="lab-texture">{v["tex"]()}</g>') if v["tex"]() else None
    if tex is not None: layer.insert(list(layer).index(bgrect) + 1, tex)
    fams = {v["font"][0], v["font"][1]}
    fonts = "".join(f"@import url('https://fonts.googleapis.com/css2?family={f.replace(' ', '+')}:wght@400;500;600;700;800');" for f in fams)
    style = ET.Element(f"{{{SVGNS}}}style"); style.text = fonts
    root.insert(0, style)
    return ET.tostring(root, encoding="unicode")


IMG_NOTES = {
    "hero-original": ("Original render", "The supplied render, on bone paper. Baseline for the image tests."),
    "hero-duotone-green": ("Duotone green", "Same render turned into brand green and white. Looks printed, ties to the badge green."),
    "hero-warm-grade": ("Warm grade", "Same render graded warm, like late afternoon light."),
    "hero-line-sketch": ("Line sketch", "Same render as fine charcoal linework. Plan and drawing feel, very distinctive."),
    "hero-mono": ("Charcoal mono", "Same render in greyscale. Lets the yellow badge and CTA carry the colour."),
    "hero-ai-golden-hour": ("AI golden hour", "AI generated concept: warm golden hour version of the scene."),
    "hero-ai-flat-illustration": ("AI flat illustration", "AI generated concept: flat vector style in brand colours."),
    "hero-ai-aerial-layout": ("AI aerial layout", "AI generated concept: isometric plot layout."),
    "hero-ai-blueprint-line": ("AI blueprint line", "AI generated concept: architectural line drawing."),
}
IMG_BASE = dict(font=("Montserrat", "Inter"), wts=(800, 500), bg="#F4F0E8", leaf="#E7E1D4", tex=lambda: grain(0.42, 0.85, "0.40 0.32 0.20"))


def image_variants():
    out = []
    for folder in ("hero", "hero-ai"):
        for f in sorted((HERE / folder).glob("*.png")):
            if f.stem not in IMG_NOTES: continue
            n, note = IMG_NOTES[f.stem]
            out.append(dict(IMG_BASE, id="img-" + f.stem.replace("hero-", ""), name=n, note=note, hero=str(f)))
    return out



# ---------- layouts (same elements, different arrangement) ----------
def _ctx(root):
    par = {c: p for p in root.iter() for c in p}
    by = {e.get("id"): e for e in root.iter() if e.get("id")}
    sub_g = par[by["subtitle"]]
    feats = [by["shift-feature-dividers"], by["shift-feature-icons"], by["shift-features-text"]]
    return par, by, sub_g, feats


def _wrap(par, el, transform):
    g = ET.Element(f"{{{SVGNS}}}g", {"transform": transform}); parent = par[el]; i = list(parent).index(el)
    parent.remove(el); g.append(el); parent.insert(i, g); par[g] = parent; par[el] = g; return g


def _photo(by, y, h):
    hg = by["shift-hero-photo"]; hg.set("transform", "translate(0 0)")
    im = [e for e in hg.iter() if tag(e) == "image"][0]
    for k in ("transform",): im.attrib.pop(k, None)
    im.set("x", "0"); im.set("y", str(y)); im.set("width", "1827"); im.set("height", str(h)); im.set("preserveAspectRatio", "xMidYMid slice")


def lay_photo_first(root, layer):
    par, by, sub, feats = _ctx(root); _photo(by, 0, 760)
    _wrap(par, by["logo"], "translate(0 515)")
    _wrap(par, by["title"], "translate(0 519)"); _wrap(par, sub, "translate(0 519)")
    _wrap(par, by["stats"], "translate(0 468)")
    for f in feats: _wrap(par, f, "translate(0 -96)")


def lay_sandwich(root, layer):
    par, by, sub, feats = _ctx(root); _photo(by, 790, 530)
    _wrap(par, by["stats"], "translate(0 534)")
    for f in feats: _wrap(par, f, "translate(0 -34)")


def lay_left(root, layer):
    par, by, sub, feats = _ctx(root)
    _wrap(par, by["logo"], "translate(-589 0)")
    t = by["title"]; t.set("transform", "matrix(1 0 0 1 140 618)"); t.set("text-anchor", "start")
    _wrap(par, sub, "translate(-296 0)")


def lay_compact(root, layer):
    par, by, sub, feats = _ctx(root); _photo(by, 420, 760)
    _wrap(par, by["logo"], f"translate({225 - 729 * 0.78:.1f} {110 - 75 * 0.78:.1f}) scale(0.78)")
    t = by["title"]; t.set("transform", "matrix(1.15 0 0 1.15 520 270)"); t.set("text-anchor", "start")
    _wrap(par, sub, f"translate({520 - 436 * 1.15:.1f} {294 - 656 * 1.15:.1f}) scale(1.15)")
    _wrap(par, by["stats"], "translate(0 424)")
    for f in feats: _wrap(par, f, "translate(0 -124)")


FEAT_DARK = {"#101d1a": "#F4EFE3", "#111111": "#F4EFE3", "#151515": "#F4EFE3", "#666666": "#C9CFD8", "#000000": "#F4EFE3", "#d6d6d6": "#4a5568", "#dcdcdc": "#4a5568", "#CFCFCF": "#4a5568"}


def lay_band(root, layer):
    par, by, sub, feats = _ctx(root)
    band = ET.fromstring(f'<rect xmlns="{SVGNS}" x="0" y="1915" width="1827" height="375" fill="#111827"/>')
    parent = par[feats[0]]; parent.insert(list(parent).index(feats[0]), band)
    for f in feats:
        for e in f.iter():
            for k in ("fill", "stroke"):
                if e.get(k) in FEAT_DARK: e.set(k, FEAT_DARK[e.get(k)])


LAYOUTS = {"photo-first": lay_photo_first, "sandwich": lay_sandwich, "left": lay_left, "compact": lay_compact, "band": lay_band}


def layouts():
    A = "hero-ai/"; H1 = "hero/"
    def mk(i, name, base, hero, lay, note, **kw):
        d = dict(byid(base)); d.update(id="lay-" + i, name=name, note=note, hero=str(HERE / hero), layout=lay, **kw); return d
    return [
        mk("photo-first", "Photo first", "08-sand-gradient", A + "hero-ai-golden-hour.png", "photo-first", "Hero image leads at the top, the badge sits on its lower edge, then name, proof, facilities, CTA. Emotion before facts."),
        mk("sandwich", "Sandwich", "01-bone-paper", H1 + "hero-original.png", "sandwich", "Name, then the photo, then the proof grid. Photo moves up so the eye lands on the place before the numbers."),
        mk("left-editorial", "Left editorial", "02-blueprint-grid", H1 + "hero-line-sketch.png", "left", "Badge and name aligned to one left edge, the rest stays on the full width grid. Strong single alignment axis."),
        mk("compact-header", "Compact header", "03-sunburst-echo", A + "hero-ai-aerial-layout.png", "compact", "Badge beside the name saves height, so the image gets 760 px and the stats stay unchanged."),
        mk("footer-band", "Footer band", "06-halftone-warm", H1 + "hero-original.png", "band", "Charcoal band behind facilities and CTA: the yellow CTA gets maximum contrast and the page gets a clear base."),
    ]



# ---------- NEW BRAND TEXTURES (built from the brand's own parts: sunburst, diamonds, flag, roads, plots, circuit, halo) ----------
import random
YEL, RED, GRN = "#FFD600", "#E53935", "#0F4D3A"


def _star(cx, cy, r, n=22, depth=0.86):
    pts = []
    for i in range(2 * n):
        a = math.pi * i / n - math.pi / 2; rr = r if i % 2 == 0 else r * depth
        pts.append(f"{cx + rr * math.cos(a):.1f},{cy + rr * math.sin(a):.1f}")
    return "M" + "L".join(pts) + "Z"


def t_sunburst_tiles(W, H, color=GRN, op=0.045, pitch=170, r=40):
    d = ""
    for j, y in enumerate(range(0, H + pitch, pitch // 2)):
        for x in range(-pitch, W + pitch, pitch):
            d += _star(x + (pitch // 2 if j % 2 else 0), y, r)
    return f'<path d="{d}" fill="{color}" fill-opacity="{op}"/>'


def t_diamond_chain(W, H, op=0.24, pitch=46, size=8):
    s = ""
    for j, y in enumerate(range(0, H + pitch, pitch)):
        col = YEL if j % 6 == 3 else RED
        for x in range(0, W + pitch, pitch):
            cx = x + (pitch / 2 if j % 2 else 0)
            s += f'<path d="M{cx} {y - size}L{cx + size} {y}L{cx} {y + size}L{cx - size} {y}Z" fill="{col}"/>'
    return f'<g fill-opacity="{op}">{s}</g>'


def t_flag_hatch(W, H, op=0.20, pitch=96, wd=7):
    return (f'<defs><pattern id="fh" width="{pitch}" height="{pitch}" patternUnits="userSpaceOnUse" patternTransform="rotate(52)">'
            f'<rect x="0" width="{wd}" height="{pitch}" fill="{YEL}"/><rect x="{wd * 1.8}" width="{wd}" height="{pitch}" fill="{RED}"/><rect x="{wd * 3.6}" width="{wd}" height="{pitch}" fill="{GRN}"/></pattern></defs>'
            f'<rect width="{W}" height="{H}" fill="url(#fh)" opacity="{op}"/>')


def t_roads(W, H, op=0.08):
    s = ""
    for x in range(120, W, 330):
        s += f'<rect x="{x - 20}" y="0" width="40" height="{H}" fill="{GRN}" fill-opacity="{op}"/><path d="M{x} 0V{H}" stroke="{YEL}" stroke-opacity="0.55" stroke-width="3" stroke-dasharray="26 22"/>'
    for y in range(200, H, 420):
        s += f'<rect x="0" y="{y - 14}" width="{W}" height="28" fill="{GRN}" fill-opacity="{op * 0.8}"/><path d="M0 {y}H{W}" stroke="{YEL}" stroke-opacity="0.45" stroke-width="2.5" stroke-dasharray="22 20"/>'
    return s


def t_plot_plan(W, H, seed=4):
    rng = random.Random(seed); s = ""
    bw, bh, gap = 150, 100, 30
    for y in range(0, H + bh, bh + gap):
        for x in range(0, W + bw, bw + gap):
            r = rng.random(); fill = f' fill="{YEL}" fill-opacity="0.12"' if r < 0.10 else (f' fill="{GRN}" fill-opacity="0.07"' if r < 0.17 else ' fill="none"')
            s += f'<rect x="{x}" y="{y}" width="{bw}" height="{bh}" rx="3"{fill} stroke="{GRN}" stroke-opacity="0.13" stroke-width="2"/>'
    return s


def t_circuit(W, H, color=GRN, op=0.17, seed=21, n=70):
    rng = random.Random(seed); g = 44; d = ""; nodes = ""
    dirs = [(1, 0), (0, 1), (1, 1), (-1, 1), (-1, 0), (0, -1)]
    for _ in range(n):
        x, y = rng.randrange(0, W // g) * g, rng.randrange(0, H // g) * g; d += f"M{x} {y}"
        for _ in range(rng.randint(2, 6)):
            dx, dy = rng.choice(dirs); k = rng.randint(1, 3); x += dx * g * k; y += dy * g * k; d += f"L{x} {y}"
        nodes += f'<circle cx="{x}" cy="{y}" r="7" fill="none" stroke="{color}" stroke-width="3"/>'
    return f'<g stroke="{color}" stroke-opacity="{op}" fill="none" stroke-width="3" stroke-linejoin="round"><path d="{d}"/><g stroke-opacity="{op + 0.1}">{nodes}</g></g>'


def t_halo_rings(W, H, cx=913.5, cy=235, op=0.12):
    s = ""
    for i, r in enumerate(range(130, 3400, 78)):
        col, w, o = (YEL, 4, op * 2.4) if i % 3 == 0 else (GRN, 2, op)
        s += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{col}" stroke-width="{w}" stroke-opacity="{o:.2f}"/>'
    return s


def t_starfield(W, H, seed=9, n=70):
    rng = random.Random(seed); s = ""
    for _ in range(n):
        r = rng.choice([14, 22, 34, 50]); col = rng.choice([YEL, YEL, RED, GRN])
        s += f'<path d="{_star(rng.uniform(0, W), rng.uniform(0, H), r)}" fill="{col}" fill-opacity="{0.22 if col == YEL else 0.14}"/>'
    return s


TEXTURES = {
    "sunburst-tiles": ("Sunburst tiles", "The badge's 22 point sunburst repeated as a quiet half-drop tile.", t_sunburst_tiles),
    "diamond-chain": ("Diamond chain", "The badge's red diamonds as rows, with a yellow row every sixth line.", t_diamond_chain),
    "flag-hatch": ("Flag hatch", "Yellow, red and green slanted hairlines, the tri-colour flag turned into a texture.", t_flag_hatch),
    "road-lanes": ("Road lanes", "Wide RCC roads with yellow dashed centre lines. The park's main promise, as a pattern.", t_roads),
    "plot-plan": ("Plot plan", "A site plan of plots and lanes, a few plots filled yellow and green.", t_plot_plan),
    "circuit-trace": ("Circuit trace", "Orthogonal and 45 degree traces with ring nodes, from the circuit-style LiP lettering.", t_circuit),
    "halo-rings": ("Halo rings", "Concentric ripples radiating from the badge, every third ring yellow.", t_halo_rings),
    "starfield": ("Mini suns", "Scattered small sunbursts in brand colours at four sizes.", t_starfield),
}


def brand_variants():
    def mk(i, name, base, hero, tid, note, **kw):
        d = dict(byid(base)); fn = TEXTURES[tid][2]
        d.update(id="brand-" + i, name=name, note=note, hero=str(HERE / hero), tex=(lambda fn=fn: fn(W, H) + grain(0.16, 0.9, "0.4 0.3 0.2", "gb" + i, 3))); d.update(kw); return d
    O = "hero/hero-original.png"; A = "hero-ai/"
    return [
        mk("sun-tiles", "Sun tiles on bone", "01-bone-paper", O, "sunburst-tiles", "Bone, tiny sunbursts repeated across the sheet, Archivo."),
        mk("plot-plan", "Plot plan sage", "02-blueprint-grid", A + "hero-ai-aerial-layout.png", "plot-plan", "Sage with a site plan behind the content, Barlow, the isometric layout image."),
        mk("circuit-night", "Circuit night", "07-deep-green", O, "circuit-trace", "Deep green with fine cream circuit traces, Plus Jakarta Sans.", tex=lambda: t_circuit(W, H, color="#FFFFFF", op=0.2) + grain(0.16, 0.9, "1 1 1", "gbc", 3)),
        mk("flag-hatch", "Flag hatch on sand", "08-sand-gradient", "hero/hero-warm-grade.png", "flag-hatch", "Sand gradient with the flag colours as faint slanted hairlines, Red Hat Display."),
        mk("diamonds", "Diamond chain cream", "03-sunburst-echo", O, "diamond-chain", "Cream with rows of the badge diamonds, Poppins.", bg="#F8F2E2"),
        mk("rings", "Halo rings", "06-halftone-warm", O, "halo-rings", "Ripples from the badge across a warm base, Outfit and DM Sans."),
        mk("road-lanes", "Road lanes concrete", "05-concrete", "hero/hero-mono.png", "road-lanes", "Concrete grey with road lanes and yellow dashes, Space Grotesk."),
        mk("mini-suns", "Mini suns on yellow", "03-sunburst-echo", O, "starfield", "Pale brand yellow with small sunbursts, Poppins.", bg="#FFEFA8", leaf="#F7DF86"),
    ]


def texture_swatches():
    out = []; (HERE / "textures").mkdir(exist_ok=True)
    for tid, (name, note, fn) in TEXTURES.items():
        w, h = 1200, 800
        body = f'<rect width="{w}" height="{h}" fill="#F4F0E8"/>' + fn(w, h)
        svg = f'<svg xmlns="{SVGNS}" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><title>texture {tid}</title><defs><clipPath id="cl"><rect width="{w}" height="{h}"/></clipPath></defs><g clip-path="url(#cl)">{body}</g></svg>'
        (HERE / f"textures/texture-{tid}.svg").write_text('<?xml version="1.0" encoding="UTF-8"?>\n' + svg, encoding="utf-8")
        out.append(dict(id=tid, name=name, note=note))
    return out


def split_tex(top="#DDE8D8", y=1110, fid="sp"):
    return (f'<path d="M0 0H{W}V{y - 90}L0 {y + 90}Z" fill="{top}"/>' + grain(0.30, 0.85, "0.35 0.3 0.2", fid, 12))


def byid(i): return [v for v in V if v["id"] == i][0]


def mixes():
    H1, A = "hero/", "hero-ai/"
    def mk(i, name, base, hero, note, **kw):
        d = dict(byid(base)); d.update(id="mix-" + i, name=name, note=note, hero=str(HERE / hero), **kw); return d
    return [
        mk("blueprint-room", "Blueprint room", "02-blueprint-grid", A + "hero-ai-blueprint-line.png", "Hairline grid, Barlow Semi Condensed and the AI line drawing. A survey sheet that happens to sell plots."),
        mk("blueprint-night", "Blueprint night", "07-deep-green", A + "hero-ai-blueprint-line.png", "Deep green canvas, the line drawing inverted to cream and screen blended in. Feels like a lit drawing board.", invert=True, blend="screen",
           tex=lambda: grid(color="#FFFFFF", a1=0.06, a2=0.12) + grain(0.22, 0.9, "1 1 1", "gmn", 6)),
        mk("sun-aerial", "Sun and aerial", "03-sunburst-echo", A + "hero-ai-aerial-layout.png", "Sunburst rays, Poppins and the isometric plot layout. Bright and energetic, the layout is the star."),
        mk("land-aerial", "Land and layout", "04-contour-land", A + "hero-ai-aerial-layout.png", "Contour lines under the isometric layout, Bricolage Grotesque. The land theme made literal."),
        mk("concrete-mono", "Brutalist", "05-concrete", H1 + "hero-mono.png", "Concrete grey, Space Grotesk and the charcoal photo. Colour comes only from the badge, CTA and flag."),
        mk("halftone-golden", "Golden print", "06-halftone-warm", A + "hero-ai-golden-hour.png", "Warm halftone dots, Outfit and the golden hour render. Looks like a screen printed poster."),
        mk("sand-warm", "Quiet premium", "08-sand-gradient", H1 + "hero-warm-grade.png", "Sand gradient, Red Hat Display and the warm graded photo. The most calm and expensive feeling."),
        mk("grid-sketch", "Technical sketch", "02-blueprint-grid", H1 + "hero-line-sketch.png", "Grid, Barlow and the local line sketch of the real render. Technical without any AI image."),
        mk("sunshine", "Sunshine yellow", "03-sunburst-echo", H1 + "hero-original.png", "A pale brand yellow canvas with darker rays, Poppins, original render. The badge colour carried across the whole sheet.",
           bg="#FFEFA8", leaf="#F7DF86", tex=lambda: rays(color="#F2B705", op=0.20) + grain(0.22, 0.9, "0.5 0.4 0.1", "gsun", 5)),
        mk("split-sage", "Split sage", "01-bone-paper", H1 + "hero-duotone-green.png", "Sage block over bone with a slanted join (echoing the flag), Archivo and the green duotone photo. Two zones, one calm palette.",
           tex=lambda: split_tex()),
    ]


def main():
    for d in ("svg", "png", "thumbs"): (HERE / d).mkdir(exist_ok=True)
    with sync_playwright() as p:
        br = p.chromium.launch(); pg = br.new_page(viewport={"width": W, "height": H})
        for v in V + image_variants() + mixes() + layouts() + brand_variants():
            s = make(v, v.get("hero")); (HERE / f"svg/{v['id']}.svg").write_text('<?xml version="1.0" encoding="UTF-8"?>\n' + s, encoding="utf-8")
            pg.goto((HERE / f"svg/{v['id']}.svg").as_uri()); pg.wait_for_timeout(1800); pg.evaluate("document.fonts.ready")
            pg.wait_for_timeout(600)
            pg.screenshot(path=str(HERE / f"png/{v['id']}.png"), clip={"x": 0, "y": 0, "width": W, "height": H})
            im = Image.open(HERE / f"png/{v['id']}.png").convert("RGB")
            im.save(HERE / f"thumbs/{v['id']}.webp", quality=80, method=6)
            im.resize((W // 3, H // 3)).save(HERE / f"thumbs/{v['id']}-s.webp", quality=78, method=6)
            print("ok", v["id"])
        sw = texture_swatches(); pg2 = br.new_page(viewport={"width": 1200, "height": 800})
        for t in sw:
            pg2.goto((HERE / f"textures/texture-{t['id']}.svg").as_uri()); pg2.wait_for_timeout(300)
            pg2.screenshot(path=str(HERE / f"thumbs/tex-{t['id']}.png"))
            im = Image.open(HERE / f"thumbs/tex-{t['id']}.png").convert("RGB"); im.save(HERE / f"thumbs/tex-{t['id']}.webp", quality=82, method=6); (HERE / f"thumbs/tex-{t['id']}.png").unlink()
        json.dump(sw, open(HERE / "textures.json", "w"), indent=1)
        br.close()
    json.dump([{k: v[k] for k in ("id", "name", "font", "bg", "note")} for v in V + image_variants() + mixes() + layouts() + brand_variants()], open(HERE / "variants.json", "w"), indent=1)


if __name__ == "__main__":
    main()
