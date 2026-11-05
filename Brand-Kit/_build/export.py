"""Exports outlined SVGs to PNG (+ transparent where useful) and print-ready vector PDF (fonts already outlined)."""
import pathlib, re, sys
from playwright.sync_api import sync_playwright

KIT = pathlib.Path(__file__).resolve().parents[1]
SRC = KIT / "outlined"
PNG = KIT / "export" / "png"; PDF = KIT / "export" / "pdf"
PNG.mkdir(parents=True, exist_ok=True); PDF.mkdir(parents=True, exist_ok=True)


def dims(svg):
    m = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg); return float(m[1]), float(m[2])


def size_css(svg):
    w = re.search(r'<svg[^>]* width="([^"]+)"', svg)[1]; h = re.search(r'<svg[^>]* height="([^"]+)"', svg)[1]
    return w, h


def to_px(v):
    n = float(re.match(r"[\d.]+", v)[0])
    return n * {"px": 1, "in": 96, "mm": 96 / 25.4, "ft": 96 * 12}.get(re.search(r"[a-z]+", v)[0], 1)


with sync_playwright() as p:
    br = p.chromium.launch()
    for f in sorted(SRC.rglob("*.svg")):
        s = f.read_text(encoding="utf-8")
        vw, vh = dims(s)
        wcss, hcss = size_css(s)
        long_px = 2400 if "hoarding" not in f.name else 4000
        k = long_px / max(vw, vh)
        W, H = round(vw * k), round(vh * k)
        pg = br.new_page(viewport={"width": W, "height": H})
        html = f'<html><body style="margin:0;background:transparent"><div style="width:{W}px;height:{H}px">{re.sub(r"<svg", f"<svg style=\"width:{W}px;height:{H}px\"", s, 1)}</div></body></html>'
        pg.set_content(html.replace('<?xml version="1.0" encoding="UTF-8"?>', ""))
        pg.wait_for_timeout(150)
        out = PNG / (f.stem + ".png")
        pg.screenshot(path=str(out), omit_background=("logo-badge" in f.name or "logo-" in f.name and "reversed" not in f.name))
        # vector PDF at true physical size
        wi, hi = to_px(wcss) / 96, to_px(hcss) / 96
        if max(wi, hi) > 200:  # hoarding: cap PDF page at 40in wide, scale down (print at 100%+ from vector)
            sc = 40 / max(wi, hi); wi, hi = wi * sc, hi * sc
        pg.pdf(path=str(PDF / (f.stem + ".pdf")), width=f"{wi:.3f}in", height=f"{hi:.3f}in", print_background=True, page_ranges="1")
        pg.close()
    br.close()
print(len(list(PNG.glob("*.png"))), "png,", len(list(PDF.glob("*.pdf"))), "pdf")
