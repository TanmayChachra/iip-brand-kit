"""Round 2: minimal, whitespace-first directions. Quiet (paper), Portal (ivory + vermilion door), Ink (charcoal + trace line).
Logo is the untouched transparent master."""
import sys, base64, pathlib
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT / "b2"; OUT.mkdir(exist_ok=True)
LOGO = "data:image/png;base64," + base64.b64encode((ROOT / "logo/iip-master-1x.png").read_bytes()).decode()
PHONE = "98XXX XXXXX"
FONTS = ("https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800&family=Inter:wght@400;500;600"
         "&family=Sora:wght@300;400;600;700&family=Manrope:wght@400;500;700;800&family=Hind:wght@400;500;600&display=swap")

PAPER, INK, RED = "#F7F4EC", "#15171A", "#EE1D23"
IVORY, VERM = "#F4F0E6", "#D6311F"
CHAR, IV2, YEL = "#121316", "#F4EFE3", "#FEF102"


def page(inner, w, h):
    return (f'<!doctype html><meta charset=utf-8><link rel=stylesheet href="{FONTS}"><style>*{{box-sizing:border-box;margin:0}}'
            f'body{{background:#888}}.b{{container-type:size;width:{w}px;height:{h}px;position:relative;overflow:hidden}}</style>{inner}')


# ---------------- pole boards (width 10 in, heights 10/12/14) ----------------
def quiet(h):
    hh = 14 if h > 14 else h
    lw = {10: 33, 12: 46, 14: 52}[hh]
    return f"""<div class=b style="background:{PAPER};color:{INK};font-family:Montserrat,Hind,sans-serif;display:flex;flex-direction:column;align-items:center">
 <div style="position:absolute;inset:0;border:.7cqw solid {INK}"></div>
 <img src="{LOGO}" style="position:relative;width:{lw}cqw;margin-top:{9 if h>10 else 6}cqw;display:block">
 <div style="position:relative;margin-top:{7 if h>10 else 4}cqw;font-weight:800;font-size:{13 if h>10 else 11}cqw;letter-spacing:.015em;line-height:1">ISAPUR</div>
 <div style="position:relative;margin-top:2cqw;font-weight:500;font-size:{4.3 if h>10 else 3.9}cqw;letter-spacing:.4em;padding-left:.4em">INDUSTRIAL PARK</div>
 <div style="position:relative;margin-top:{5 if h>10 else 3.5}cqw;width:12cqw;height:.9cqw;background:{RED}"></div>
 <div style="position:relative;margin-top:{5 if h>10 else 3.5}cqw;font-weight:500;font-size:{6.4 if h>10 else 5.6}cqw;line-height:1.2">Room to build.</div>
 <div style="position:relative;margin-top:1.4cqw;font:500 {4.6 if h>10 else 4.2}cqw Hind;color:#6b6a66">बनाने की जगह</div>
 <div style="position:absolute;left:0;right:0;bottom:{7 if h>10 else 5}cqw;text-align:center;font:600 {4 if h>10 else 3.6}cqw Inter;letter-spacing:.22em">{PHONE}</div></div>"""


def portal(h):
    hh = 14 if h > 14 else h
    dw = {10: 38, 12: 44, 14: 44}[hh]; dh = {10: 42, 12: 54, 14: 66}[hh]
    lw = dw * (0.62 if h == 10 else 0.74)
    gap = {10: 3, 12: 5, 14: 7}[hh]
    return f"""<div class=b style="background:{IVORY};color:{INK};font-family:Sora,Hind,sans-serif;display:flex;flex-direction:column;align-items:center">
 <div style="position:absolute;inset:0;border:.7cqw solid {INK}"></div>
 <div style="position:relative;margin-top:{8 if h>10 else 6}cqw;width:{dw}cqw;height:{dh}cqw;background:{VERM};border-radius:{dw/2}cqw {dw/2}cqw 0 0;display:flex;justify-content:center;padding-top:{dw*0.16}cqw">
  <img src="{LOGO}" style="width:{lw}cqw;height:{lw}cqw;display:block"></div>
 <div style="position:relative;width:{dw+14}cqw;height:.8cqw;background:{INK}"></div>
 <div style="position:relative;margin-top:{5 if h>10 else 3.5}cqw;font-weight:700;font-size:{6.6 if h>10 else 5.8}cqw;letter-spacing:.34em;padding-left:.34em">ISAPUR</div>
 <div style="position:relative;margin-top:1.6cqw;font-weight:400;font-size:{3.7 if h>10 else 3.3}cqw;letter-spacing:.4em;padding-left:.4em">INDUSTRIAL PARK</div>
 <div style="position:relative;margin-top:{gap}cqw;font-weight:300;font-size:{7.4 if h>10 else 6.4}cqw">Step in.</div>
 <div style="position:absolute;left:0;right:0;bottom:{6 if h>10 else 4}cqw;text-align:center;font:600 {3.8 if h>10 else 3.4}cqw Inter;letter-spacing:.22em">{PHONE}</div></div>"""


def ink(h):
    hh = 14 if h > 14 else h
    lw = {10: 42, 12: 48, 14: 54}[hh]
    return f"""<div class=b style="background:{CHAR};color:{IV2};font-family:Manrope,Hind,sans-serif;display:flex;flex-direction:column;align-items:center">
 <div style="position:absolute;inset:2.4cqw;border:.5cqw solid {IV2};opacity:.85"></div>
 <img src="{LOGO}" style="position:relative;width:{lw}cqw;margin-top:{10 if h>10 else 7.5}cqw;display:block">
 <div style="position:relative;margin-top:{6 if h>10 else 4}cqw;font-weight:800;font-size:{12.5 if h>10 else 11}cqw;letter-spacing:.02em;line-height:1">ISAPUR</div>
 <div style="position:relative;margin-top:2cqw;font-weight:400;font-size:{4.2 if h>10 else 3.8}cqw;letter-spacing:.42em;padding-left:.42em">INDUSTRIAL PARK</div>
 <div style="position:relative;margin-top:{5 if h>10 else 3.5}cqw;font-weight:500;font-size:{6.2 if h>10 else 5.4}cqw">Plug in. Build up.</div>
 <div style="position:absolute;left:50%;bottom:{14 if h>10 else 11}cqw;width:.45cqw;height:{ {10:0,12:5,14:15}[hh] }cqw;margin-left:-.22cqw;background:{YEL}"></div>
 <div style="position:absolute;left:50%;bottom:{11.6 if h>10 else 8.6}cqw;width:2.4cqw;height:2.4cqw;margin-left:-1.2cqw;border-radius:50%;background:{YEL}"></div>
 <div style="position:absolute;left:0;right:0;bottom:{5.6 if h>10 else 4.4}cqw;text-align:center;font:600 {3.8 if h>10 else 3.4}cqw Inter;letter-spacing:.22em">{PHONE}</div></div>"""


# ---------------- steps teaser serial for Portal ----------------
def steps(n):
    blocks = "".join(f'<div style="position:absolute;left:{18+(i)*0}cqw;width:{64-i*0}cqw;height:0"></div>' for i in range(0))
    bars = ""
    for i in range(n):
        wdt = 36 + 8 * i
        bars += f'<div style="position:absolute;left:{50-wdt/2}cqw;bottom:{26+ i*11}cqw;width:{wdt}cqw;height:9.2cqw;background:{VERM}"></div>'
    return f"""<div class=b style="background:{IVORY};color:{INK};font-family:Sora,sans-serif">
 <div style="position:absolute;inset:0;border:.7cqw solid {INK}"></div>{bars}
 <div style="position:absolute;left:0;right:0;top:9cqw;text-align:center;font-weight:300;font-size:7.4cqw;letter-spacing:.02em">{ ["Step 1.", "Step 2.", "Step 3."][n-1] }</div>
 <div style="position:absolute;left:0;right:0;bottom:7cqw;text-align:center;font:600 3.4cqw Inter;letter-spacing:.22em;opacity:.55">ISAPUR INDUSTRIAL PARK</div></div>"""


# ---------------- landscape: hoarding (2.4:1) and gate (4:1) ----------------
def w_quiet(r):
    return f"""<div class=b style="background:{PAPER};color:{INK};font-family:Montserrat,Hind,sans-serif;display:flex;align-items:center">
 <div style="position:absolute;inset:0;border:1.6cqh solid {INK}"></div>
 <img src="{LOGO}" style="position:relative;height:62cqh;margin-left:{16 if r<3 else 12}cqh;display:block">
 <div style="position:relative;margin-left:{11 if r<3 else 9}cqh">
  <div style="font-weight:800;font-size:{27 if r<3 else 32}cqh;line-height:1;letter-spacing:.01em;white-space:nowrap">ISAPUR</div>
  <div style="margin-top:3cqh;font-weight:500;font-size:{6.2 if r<3 else 7.4}cqh;letter-spacing:.4em;white-space:nowrap">INDUSTRIAL PARK</div>
  <div style="margin-top:5cqh;width:{18 if r<3 else 16}cqh;height:1.6cqh;background:{RED}"></div>
  <div style="margin-top:5cqh;font-weight:500;font-size:{10 if r<3 else 11}cqh;white-space:nowrap">Room to build.</div></div></div>"""


def w_portal(r):
    dw = 52 if r < 3 else 62
    return f"""<div class=b style="background:{IVORY};color:{INK};font-family:Sora,Hind,sans-serif;display:flex;align-items:flex-end">
 <div style="position:absolute;inset:0;border:1.6cqh solid {INK}"></div>
 <div style="position:relative;margin-left:{16 if r<3 else 12}cqh;margin-bottom:9cqh;width:{dw*0.78}cqh;height:{72 if r<3 else 78}cqh;background:{VERM};border-radius:{dw*0.39}cqh {dw*0.39}cqh 0 0;display:flex;justify-content:center;padding-top:{dw*0.12}cqh">
  <img src="{LOGO}" style="width:{dw*0.58}cqh;height:{dw*0.58}cqh"></div>
 <div style="position:absolute;left:{10 if r<3 else 8}cqh;bottom:9cqh;width:{dw*0.78+12}cqh;height:1cqh;background:{INK}"></div>
 <div style="position:relative;margin-left:{12 if r<3 else 10}cqh;margin-bottom:{30 if r<3 else 28}cqh">
  <div style="font-weight:700;font-size:{13 if r<3 else 15}cqh;letter-spacing:.34em;white-space:nowrap">ISAPUR</div>
  <div style="margin-top:3cqh;font-weight:400;font-size:{5.6 if r<3 else 7}cqh;letter-spacing:.4em;white-space:nowrap">INDUSTRIAL PARK</div>
  <div style="margin-top:8cqh;font-weight:300;font-size:{12 if r<3 else 13}cqh;white-space:nowrap">Step in.</div></div></div>"""


def w_ink(r):
    return f"""<div class=b style="background:{CHAR};color:{IV2};font-family:Manrope,Hind,sans-serif;display:flex;align-items:center">
 <div style="position:absolute;inset:3.4cqh;border:.6cqh solid {IV2};opacity:.85"></div>
 <img src="{LOGO}" style="position:relative;height:62cqh;margin-left:{16 if r<3 else 12}cqh;display:block">
 <div style="position:relative;margin-left:{11 if r<3 else 9}cqh">
  <div style="font-weight:800;font-size:{27 if r<3 else 32}cqh;line-height:1;white-space:nowrap">ISAPUR</div>
  <div style="margin-top:3cqh;font-weight:400;font-size:{6.2 if r<3 else 7.4}cqh;letter-spacing:.4em;white-space:nowrap">INDUSTRIAL PARK</div>
  <div style="margin-top:6cqh;font-weight:500;font-size:{10 if r<3 else 11}cqh;white-space:nowrap">Plug in. Build up.</div></div>
 <div style="position:absolute;left:12cqh;right:12cqh;bottom:11cqh;height:.8cqh;background:{YEL}"></div>
 <div style="position:absolute;right:11cqh;bottom:9.8cqh;width:3.2cqh;height:3.2cqh;border-radius:50%;background:{YEL}"></div></div>"""


KITS = {"quiet": (quiet, w_quiet), "portal": (portal, w_portal), "ink": (ink, w_ink)}
SIZES = [(10, 10), (10, 12), (10, 14), (10, 18)]
RATIOS = {"hoarding": 2.4, "gate": 4.0}


def shot(br, html, w, h, path, dpr):
    pg = br.new_page(viewport={"width": w, "height": h}, device_scale_factor=dpr)
    pg.set_content(page(html, w, h)); pg.wait_for_load_state("networkidle"); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(450)
    pg.screenshot(path=str(path)); pg.close()


def main(only=None):
    with sync_playwright() as p:
        br = p.chromium.launch()
        for kit, (pole, wide) in KITS.items():
            if only and kit not in only: continue
            for w, h in SIZES:
                shot(br, pole(h), w * 100, h * 100, OUT / f"{kit}-{w}x{h}.png", 3)
            for name, r in RATIOS.items():
                shot(br, wide(r), int(500 * r), 500, OUT / f"{kit}-{name}.png", 2)
        if not only or "portal" in only:
            for n in (1, 2, 3):
                shot(br, steps(n), 1000, 1400, OUT / f"portal-step-{n}.png", 3)
        br.close()


if __name__ == "__main__":
    main(sys.argv[1:] or None)
