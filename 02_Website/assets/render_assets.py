"""Raster outputs for the website assets: hero WEBP, OG PNG, favicons, contact sheet. Run after build_assets.py.
python 02_Website/assets/render_assets.py"""
import io, pathlib, shutil
from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parents[2]
A = ROOT / "02_Website/assets"; SV = A / "svg"; PUB = ROOT / "02_Website/site/public"; IMG = PUB / "img"
BADGE = ROOT / "01_Brand/Brand-Kit/live/01_Logo/logo-badge-only.svg"
BONE = "#F4F0E8"
report = {}


def shot(pg, svg_path, w, h, transparent=False, bg=None):
    s = pathlib.Path(svg_path).read_text(encoding="utf-8")
    s = s.split("?>", 1)[-1]
    pg.set_viewport_size({"width": w, "height": h})
    pg.set_content(f"<body style='margin:0;background:{bg or 'transparent'}'>{s}</body>")
    pg.evaluate(f"(()=>{{const e=document.querySelector('svg');e.setAttribute('width','{w}');e.setAttribute('height','{h}');e.style.display='block'}})()")
    return Image.open(io.BytesIO(pg.screenshot(omit_background=transparent, clip={'x': 0, 'y': 0, 'width': w, 'height': h}))).convert("RGBA" if transparent else "RGB")


def save_webp(im, path, q=78):
    im.save(path, "WEBP", quality=q, method=6)
    kb = pathlib.Path(path).stat().st_size / 1024
    while kb > 100 and q > 50:
        q -= 6; im.save(path, "WEBP", quality=q, method=6); kb = pathlib.Path(path).stat().st_size / 1024
    return round(kb, 1), q


with sync_playwright() as p:
    br = p.chromium.launch(); pg = br.new_page()
    im = shot(pg, SV / "hero-illustration.svg", 1600, 700); report["hero.webp"] = save_webp(im, IMG / "hero-illustration.webp")
    im = shot(pg, SV / "hero-illustration-mobile.svg", 780, 700); report["hero-mobile.webp"] = save_webp(im, IMG / "hero-illustration-mobile.webp")
    im = shot(pg, SV / "plot-layout-schematic.svg", 1200, 800); report["layout.webp"] = save_webp(im, IMG / "plot-layout-schematic.webp")
    im = shot(pg, SV / "location-diagram.svg", 1200, 700); report["location.webp"] = save_webp(im, IMG / "location-diagram.webp")
    im = shot(pg, SV / "halo-rings.svg", 1600, 900, bg=BONE); save_webp(im, IMG / "textures/halo-rings.webp", 70)
    # OG as PNG (some social crawlers reject WEBP), quantised to stay under 120 KB
    for n in ("home", "plots", "location", "blog"):
        im = shot(pg, SV / f"og-{n}.svg", 1200, 630)
        out = IMG / f"og/og-{n}.png"; im.save(out, optimize=True)
        if out.stat().st_size > 115 * 1024:
            im.quantize(colors=96, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).save(out, optimize=True)
        report[f"og-{n}.png"] = round(out.stat().st_size / 1024, 1)
    # favicons: badge unchanged, only placed on a canvas
    shutil.copy(BADGE, PUB / "favicon.svg")
    for sz, name, pad, bg in ((32, "favicon-32.png", 0.04, None), (180, "apple-touch-icon.png", 0.12, BONE), (192, "icon-192.png", 0.12, BONE), (512, "icon-512.png", 0.12, BONE)):
        inner = int(sz * (1 - 2 * pad)); b = shot(pg, BADGE, inner, inner, transparent=True)
        canvas = Image.new("RGBA", (sz, sz), (0, 0, 0, 0) if bg is None else bg); canvas.alpha_composite(b, ((sz - inner) // 2, (sz - inner) // 2))
        (canvas if bg is None else canvas.convert("RGB")).save(PUB / name, optimize=True)
    # contact sheet
    names = ["hero-illustration", "plot-layout-schematic", "location-diagram", "seal-badge-on-sunburst", "spot-roads", "spot-street-lighting", "spot-planted-greenery", "spot-plots", "spot-site-visit", "spot-documents",
             "card-plot-from-300", "card-site-visit", "card-layout-map", "slot-16x9", "divider-flag", "og-home", "og-plots", "og-location", "og-blog"]
    tiles = []
    for n in names:
        s = SV / f"{n}.svg"
        w, h = (900, 394) if n == "hero-illustration" else (560, 340) if not n.startswith(("divider", "og")) else ((900, 12) if n.startswith("divider") else (560, 294))
        if n.startswith("divider"):
            continue
        tiles.append(shot(pg, s, w, h, bg="#cccccc") if True else None)
    W = 3; cw = 560; sheet_h = 0; rows = []
    for i in range(0, len(tiles), W):
        r = tiles[i:i + W]; rh = max(t.height * cw // t.width for t in r); rows.append((r, rh)); sheet_h += rh + 8
    sheet = Image.new("RGB", (W * (cw + 8), sheet_h), "#888888"); y = 0
    for r, rh in rows:
        for j, t in enumerate(r): sheet.paste(t.resize((cw, t.height * cw // t.width)), (j * (cw + 8), y))
        y += rh + 8
    sheet.save(A / "_contact-sheet.png")
    br.close()
for k, v in report.items(): print(k, v)

# keep public/ light: heavy outlined-text SVGs stay in assets/svg, the site ships the WEBP versions
for rel in ("location-diagram.svg", "plot-layout-schematic.svg"): (IMG / rel).unlink(missing_ok=True)
for f in (IMG / "slots").glob("*.svg"): f.unlink()
