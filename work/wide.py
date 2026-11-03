"""Landscape artwork for hoardings (2.4:1) and gate fascia (4:1), same 3 directions."""
import sys, pathlib
from playwright.sync_api import sync_playwright
import boards as B

OUT = B.ROOT / "wide"; OUT.mkdir(exist_ok=True)
L = B.LOGO


def jamun(r):
    return f"""<div class=b style="background:#4B1DA6;font-family:Teko,Hind,sans-serif;color:#fff;display:flex;align-items:center">
 <div style="position:absolute;inset:0;background:repeating-conic-gradient(from 0deg at {5+40*0.5/r*2}% 46%,rgba(255,255,255,.07) 0 6deg,rgba(255,255,255,0) 6deg 12deg)"></div>
 <img src="{L}" style="position:relative;height:80cqh;margin-left:7cqh;margin-top:-5cqh">
 <div style="position:relative;margin-left:8cqh;margin-top:-5cqh;line-height:.88">
  <div style="font-size:{30 if r<3 else 42}cqh;font-weight:700;letter-spacing:.02em;white-space:nowrap">ISAPUR</div>
  <div style="font-size:{17 if r<3 else 25}cqh;font-weight:600;letter-spacing:.05em;white-space:nowrap">INDUSTRIAL PARK</div>
  <div style="font-size:{15 if r<3 else 20}cqh;white-space:nowrap;font-weight:600;color:#FEF102;margin-top:3cqh;font-family:Hind;line-height:1.15">बड़े काम की जगह</div>
 </div>
 <div style="position:absolute;left:0;right:0;bottom:0;height:12cqh;background:#FEF102 url("{B.DIAMOND}") repeat-x;background-size:12cqh auto"></div></div>"""


def gulaal(r):
    return f"""<div class=b style="background:#E4007C;font-family:'Yatra One','Rozha One',serif;color:#FFF4DC;display:flex;align-items:center">
 <div style="position:absolute;inset:3.4cqh;border:1.6cqh solid #FFF4DC;border-radius:4cqh"></div>
 <div style="position:absolute;inset:7cqh;border:.6cqh dashed #FEF102;border-radius:2cqh"></div>
 <img src="{L}" style="position:relative;height:70cqh;margin-left:11cqh;margin-top:-3cqh">
 <div style="position:relative;margin-left:9cqh;margin-top:-6cqh;line-height:1.05;text-shadow:1cqh 1cqh 0 #1A0B2E;font-size:{25 if r<3 else 31}cqh;white-space:nowrap">कारखाना<br>यहीं लगाओ!</div>
 <div style="position:absolute;right:11cqh;bottom:11cqh;height:12cqh;padding:0 5cqh;background:#FEF102;border-radius:2cqh;display:flex;align-items:center;font:800 6.2cqh 'Baloo 2';color:#1A0B2E;letter-spacing:.05em">ISAPUR INDUSTRIAL PARK</div></div>"""


def kora(r):
    return f"""<div class=b style="background:#FBF6E9;font-family:Archivo,Hind,sans-serif;color:#14110F;display:flex;align-items:center">
 <div style="position:absolute;inset:0;border:4.5cqh solid #14110F"></div>
 <img src="{L}" style="position:relative;height:66cqh;margin-left:11cqh;margin-top:-5cqh">
 <div style="position:relative;margin-left:10cqh;margin-top:-5cqh">
  <div style="font-weight:800;font-stretch:112%;letter-spacing:.2em;font-size:5.4cqh">ISAPUR INDUSTRIAL PARK</div>
  <div style="width:100%;height:1.8cqh;background:#14110F;margin:3cqh 0 4cqh"></div>
  <div style="font-weight:900;font-stretch:80%;font-size:{17 if r<3 else 22}cqh;white-space:nowrap;line-height:1.02;text-transform:uppercase">Where industry<br>begins.</div></div>
 <div style="position:absolute;left:4.5cqh;right:4.5cqh;bottom:4.5cqh;height:12cqh;background:#FEF102;display:flex;align-items:center;justify-content:center;font:900 6.6cqh Archivo;letter-spacing:.14em">{B.PHONE}</div></div>"""


KITS = {"jamun": jamun, "gulaal": gulaal, "kora": kora}
RATIOS = {"hoarding": 2.4, "gate": 4.0}


def main():
    with sync_playwright() as p:
        br = p.chromium.launch()
        for name, r in RATIOS.items():
            H = 500; W = int(H * r)
            for kit, fn in KITS.items():
                pg = br.new_page(viewport={"width": W, "height": H}, device_scale_factor=2)
                html = B.page(fn(r), W / 100, H / 100)
                pg.set_content(html); pg.wait_for_load_state("networkidle"); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(400)
                pg.screenshot(path=str(OUT / f"{kit}-{name}.png")); pg.close()
        br.close()


if __name__ == "__main__":
    main()

