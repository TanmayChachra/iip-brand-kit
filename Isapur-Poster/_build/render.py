"""Render master SVG to PNG and PDF with the bundled fonts (no system install needed).  usage: python render.py [crop]"""
import pathlib, re, sys
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parents[1]
SVG = ROOT / "03_Design/01_LATEST_isapur-industrial-park.svg"
FONTS = ROOT / "fonts"
faces = "".join(f"@font-face{{font-family:'{fam}';font-weight:{w};src:url('file:///{(FONTS / f).as_posix()}')}}" for fam, w, f in [
    ("Montserrat", 400, "Montserrat-Regular.ttf"), ("Montserrat", 500, "Montserrat-Medium.ttf"), ("Montserrat", 600, "Montserrat-SemiBold.ttf"),
    ("Montserrat", 700, "Montserrat-Bold.ttf"), ("Montserrat", 800, "Montserrat-ExtraBold.ttf"),
    ("Inter", 400, "Inter-Regular.ttf"), ("Inter", 500, "Inter-Medium.ttf"), ("Inter", 600, "Inter-SemiBold.ttf")])
s = SVG.read_text(encoding="utf-8")
html = f"<html><head><style>{faces}body{{margin:0}}</style></head><body>{re.sub(r'<\\?xml[^>]*\\?>', '', s)}</body></html>"
tmp = ROOT / "03_Design/_render.html"; tmp.write_text(html, encoding="utf-8")
with sync_playwright() as p:
    br = p.chromium.launch(); pg = br.new_page(viewport={"width": 1827, "height": 2290}, device_scale_factor=1)
    pg.goto(tmp.as_uri()); pg.wait_for_timeout(600); pg.evaluate("document.fonts.ready")
    pg.screenshot(path=str(ROOT / "03_Design/02_LATEST_preview.png"), clip={"x": 0, "y": 0, "width": 1827, "height": 2290})
    if "pdf" in sys.argv:
        pg.pdf(path=str(ROOT / "03_Design/00_LATEST_isapur-industrial-park.pdf"), width="1827px", height="2290px", print_background=True, page_ranges="1")
    br.close()
tmp.unlink()
print("ok")
