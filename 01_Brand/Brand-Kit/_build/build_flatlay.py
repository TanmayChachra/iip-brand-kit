"""Flat-lay stationery mockup from the exact outlined artwork (no AI). Output: Brand-Kit/reference/mockups/flatlay-stationery.webp (3000 px wide).
Run after build_stationery.py:  python 01_Brand/Brand-Kit/_build/build_flatlay.py"""
import pathlib, re
from playwright.sync_api import sync_playwright
from PIL import Image

KIT = pathlib.Path(__file__).resolve().parents[1]
SRC = KIT / "outlined/06_Stationery"
K = 5.5   # px per mm


def art(name, wmm, hmm):
    s = (SRC / f"{name}.svg").read_text(encoding="utf-8").replace('<?xml version="1.0" encoding="UTF-8"?>', "")
    s = re.sub(r"(<svg[^>]*?) width=\"[^\"]+\" height=\"[^\"]+\"", rf'\1 width="{wmm * K:.0f}" height="{hmm * K:.0f}"', s, 1)
    return re.sub(r'id="([^"]+)"', lambda m: f'id="{name}-{m.group(1)}"', s) if False else s


def item(name, wmm, hmm, x, y, rot, z=1):
    return (f'<div class="p" style="left:{x}px;top:{y}px;width:{wmm * K:.0f}px;height:{hmm * K:.0f}px;transform:rotate({rot}deg);z-index:{z}">'
            f'{art(name, wmm, hmm)}</div>')


NOISE = ("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='300' height='300'><filter id='n'><feTurbulence type='fractalNoise' "
         "baseFrequency='.85' numOctaves='2' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .55 0'/></filter>"
         "<rect width='300' height='300' filter='url(%23n)'/></svg>")
html = f"""<html><head><style>
body{{margin:0;width:3000px;height:2000px;position:relative;overflow:hidden;background:radial-gradient(ellipse at 40% 30%,#f1f2f4,#dfe2e6 75%)}}
body:after{{content:"";position:absolute;inset:0;background:url("{NOISE}");opacity:.07;pointer-events:none}}
.p{{position:absolute;background:#fff;outline:1px solid rgba(0,0,0,.06);
 filter:drop-shadow(0 1px 1.5px rgba(0,0,0,.22)) drop-shadow(0 14px 18px rgba(0,0,0,.13)) drop-shadow(0 46px 56px rgba(0,0,0,.09))}}
.p svg{{display:block}}
.strap{{position:absolute;left:2432px;top:-140px;width:92px;height:1190px;background:#0F4D3A;transform-origin:50% 100%;transform:rotate(4deg);z-index:0;
 filter:drop-shadow(0 10px 14px rgba(0,0,0,.18))}}
.strap:after{{content:"ISAPUR  ISAPUR  ISAPUR  ISAPUR  ISAPUR  ISAPUR";position:absolute;inset:0;writing-mode:vertical-rl;color:#fff;font:800 26px Montserrat,Arial;letter-spacing:6px;
 display:flex;align-items:center;justify-content:center;opacity:.85;white-space:nowrap}}
</style></head><body>
{item("letterhead-A4", 210, 297, 150, 150, -3.5, 2)}
{item("envelope-DL", 220, 110, 1330, 130, 3, 2)}
{item("card-back", 88.9, 50.8, 1280, 880, -7, 3)}
{item("card-front-A", 88.9, 50.8, 1780, 900, 4, 4)}
{item("card-front-B", 88.9, 50.8, 1480, 1260, -3, 5)}
{item("visiting-card", 88.9, 50.8, 1960, 1330, 3, 3)}
{item("id-card-front", 54, 86, 2380, 980, 4, 4)}
{item("id-card-back", 54, 86, 2650, 1120, -5, 3)}
</body></html>"""
tmp = KIT / "_build/_flatlay.html"; tmp.write_text(html, encoding="utf-8")
out = KIT / "reference/mockups"; out.mkdir(parents=True, exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 3000, "height": 2000}); pg.goto(tmp.as_uri()); pg.wait_for_timeout(800)
    pg.screenshot(path=str(out / "_flat.png")); b.close()
Image.open(out / "_flat.png").convert("RGB").save(out / "flatlay-stationery.webp", quality=90, method=6)
(out / "_flat.png").unlink(); tmp.unlink()
print("flatlay ok", (out / "flatlay-stationery.webp").stat().st_size // 1024, "KB")
