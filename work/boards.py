"""Render IIP pole boards (10x10, 10x12, 10x14 in, width x height) for the 3 brand directions.
Logo is the untouched supplied artwork (transparent master). 100 css px = 1 inch, rendered at 3x = 300 dpi."""
import sys, base64, pathlib
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT / "boards"; OUT.mkdir(exist_ok=True)
LOGO = "data:image/png;base64," + base64.b64encode((ROOT / "logo/iip-master-1x.png").read_bytes()).decode()
PHONE = "98XXX XXXXX"

FONTS = ("https://fonts.googleapis.com/css2?family=Teko:wght@500;600;700&family=Hind:wght@500;600;700"
         "&family=Yatra+One&family=Rozha+One&family=Baloo+2:wght@600;700;800&family=Archivo:wdth,wght@62..125,500..900"
         "&family=Mukta:wght@500;700;800&display=swap")

def _svg(bg, fg):
    svg = (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 12 12'><rect width='12' height='12' fill='{bg}'/>"
           f"<polygon points='6,1.2 10.8,6 6,10.8 1.2,6' fill='{fg}'/></svg>")
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()


DIAMOND = _svg("#FEF102", "#EE1D23")
DIAMOND_INK = _svg("#FFF4DC", "#E4007C")

LOGO_W = {10: 52, 12: 62, 14: 74}   # logo width as % of board width, keyed by board height (in)


def jamun(h):
    lw = {10: 46, 12: 56, 14: 70}[h]
    return f"""
<div class=b style="background:#4B1DA6;font-family:Teko,Hind,sans-serif;display:flex;flex-direction:column;align-items:center">
 <div style="position:absolute;inset:0;background:repeating-conic-gradient(from 0deg at 50% {34 if h==14 else 38}%,rgba(255,255,255,.07) 0 6deg,rgba(255,255,255,0) 6deg 12deg)"></div>
 <img src="{LOGO}" style="position:relative;width:{lw}cqw;margin-top:{6 if h==14 else 5}cqw;display:block">
 <div style="position:relative;text-align:center;color:#fff;margin-top:{3 if h==14 else 1.5}cqw;line-height:.9">
  <div style="font-size:{ {10:12,12:15,14:17}[h] }cqw;font-weight:700;letter-spacing:.02em">ISAPUR</div>
  <div style="font-size:{ {10:8.5,12:10.5,14:12}[h] }cqw;font-weight:600;letter-spacing:.04em">INDUSTRIAL PARK</div>
  <div style="font-size:{ {10:8,12:9,14:10}[h] }cqw;font-weight:600;color:#FEF102;margin-top:1.2cqw;font-family:Hind;line-height:1.15">बड़े काम की जगह</div>
 </div>
 <div style="position:absolute;left:0;right:0;bottom:0;height:{12 if h==14 else 11}cqw;background:#FEF102 url('{DIAMOND}') repeat-x;background-size:{12 if h==14 else 11}cqw auto;"></div>
</div>"""


def gulaal(h):
    lw = {10: 46, 12: 54, 14: 66}[h]
    return f"""
<div class=b style="background:#E4007C;font-family:'Yatra One','Rozha One',serif;display:flex;flex-direction:column;align-items:center">
 <div style="position:absolute;inset:3.2cqw;border:1.3cqw solid #FFF4DC;border-radius:3cqw"></div>
 <div style="position:absolute;inset:5.6cqw;border:.5cqw dashed #FEF102;border-radius:1.6cqw"></div>
 <img src="{LOGO}" style="position:relative;width:{lw}cqw;margin-top:{10 if h==14 else 8.5}cqw;display:block">
 <div style="position:relative;text-align:center;color:#FFF4DC;margin-top:{3 if h>10 else 1.5}cqw;line-height:1.02;text-shadow:.8cqw .8cqw 0 #1A0B2E;padding:0 9cqw">
  <div style="font-size:{15.5 if h>10 else 13.5}cqw">कारखाना<br>यहीं लगाओ!</div>
 </div>
 <div style="position:absolute;left:8cqw;right:8cqw;bottom:8cqw;height:9cqw;background:#FEF102;border-radius:1.2cqw;display:flex;align-items:center;justify-content:center;font:800 {5.2 if h>10 else 4.6}cqw 'Baloo 2';color:#1A0B2E;letter-spacing:.04em">ISAPUR INDUSTRIAL PARK</div>
</div>"""


def kora(h):
    lw = {10: 46, 12: 56, 14: 67}[h]
    return f"""
<div class=b style="background:#FBF6E9;font-family:Archivo,Hind,sans-serif;display:flex;flex-direction:column;align-items:center;color:#14110F">
 <div style="position:absolute;inset:0;border:2.4cqw solid #14110F"></div>
 <div style="position:relative;margin-top:{7 if h>10 else 6}cqw;font-weight:800;font-stretch:112%;letter-spacing:.2em;font-size:{3.5 if h>10 else 3.2}cqw">ISAPUR INDUSTRIAL PARK</div>
 <img src="{LOGO}" style="position:relative;width:{lw}cqw;margin-top:{4 if h>10 else 3}cqw;display:block">
 <div style="position:relative;width:{lw}cqw;height:{1.6}cqw;background:#14110F;margin-top:{3.5 if h>10 else 2.5}cqw"></div>
 <div style="position:relative;margin-top:{3 if h>10 else 2}cqw;font-weight:900;font-stretch:80%;font-size:{ {10:7.5,12:8.5,14:9.5}[h] }cqw;line-height:1.08;text-align:center;text-transform:uppercase">Where industry<br>begins.</div>
 <div style="position:absolute;left:2.4cqw;right:2.4cqw;bottom:2.4cqw;height:{10 if h>10 else 9}cqw;background:#FEF102;display:flex;align-items:center;justify-content:center;font:900 {5.4 if h>10 else 5}cqw Archivo;letter-spacing:.14em">{PHONE}</div>
</div>"""


KITS = {"jamun": jamun, "gulaal": gulaal, "kora": kora}
SIZES = [(10, 10), (10, 12), (10, 14)]


def page(inner, w, h):
    return f"""<!doctype html><meta charset=utf-8><link rel=stylesheet href="{FONTS}">
<style>*{{box-sizing:border-box;margin:0}}body{{background:#888}}
.b{{container-type:size;width:{w*100}px;height:{h*100}px;position:relative;overflow:hidden}}</style>{inner}"""


def main(only=None):
    with sync_playwright() as p:
        br = p.chromium.launch()
        for kit, fn in KITS.items():
            if only and kit not in only: continue
            for w, h in SIZES:
                pg = br.new_page(viewport={"width": w * 100, "height": h * 100}, device_scale_factor=3)
                pg.set_content(page(fn(h), w, h)); pg.wait_for_load_state("networkidle")
                pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(400)
                pg.screenshot(path=str(OUT / f"{kit}-{w}x{h}.png"))
                pg.close()
        br.close()


if __name__ == "__main__":
    main(sys.argv[1:] or None)

