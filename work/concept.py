"""Concept route: conceptual adverts. AI makes the empty photographic plate only; logo and all words are set exactly."""
import base64, io, sys, pathlib
from PIL import Image
from playwright.sync_api import sync_playwright
import boards2 as B

ROOT = B.ROOT
OUT = ROOT / "concept"; OUT.mkdir(exist_ok=True)
FONTS = B.FONTS + "&family=Caveat:wght@500;600&family=Montserrat:ital,wght@1,300;1,500"
FONTS = FONTS.replace("family=Montserrat:wght@400;500;600;700;800", "family=Montserrat:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,300;1,400")


def plate(name, w=1000):
    im = Image.open(ROOT / f"gen/{name}.png").convert("RGB")
    im = im.resize((w * 2, round(im.height * w * 2 / im.width)), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf, "JPEG", quality=90)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def wrap(inner, w, h):
    return (f'<!doctype html><meta charset=utf-8><link rel=stylesheet href="{FONTS}"><style>*{{box-sizing:border-box;margin:0}}'
            f'.p{{width:{w}px;height:{h}px;position:relative;overflow:hidden;font-family:Montserrat,Hind,sans-serif}}'
            f'.bg{{position:absolute;inset:0;background-size:cover;background-position:center}}</style>{inner}')


def steps_poster(w=1000, h=1250):
    return f"""<div class=p><div class=bg style="background-image:url({plate('plate-steps')})"></div>
 <img src="{B.LOGO}" style="position:absolute;left:70px;top:64px;width:120px">
 <div style="position:absolute;left:70px;top:250px;width:640px;color:#15171A">
  <div style="font-weight:300;font-size:74px;line-height:1.08;letter-spacing:-.01em">Every factory<br>begins with<br><b style="font-weight:700">one step.</b></div>
  <div style="margin-top:34px;width:84px;height:7px;background:{B.RED}"></div>
  <div style="margin-top:30px;font-weight:600;font-size:18px;letter-spacing:.36em">ISAPUR INDUSTRIAL PARK</div></div>
 <div style="position:absolute;right:60px;bottom:48px;font:600 16px Inter;letter-spacing:.24em;color:#fff">9837057800  |  9219549800</div></div>"""


def build_poster(w=1000, h=1250):
    return f"""<div class=p><div class=bg style="background-image:url({plate('plate-build')})"></div>
 <img src="{B.LOGO}" style="position:absolute;left:64px;top:56px;width:100px">
 <div style="position:absolute;left:0;right:0;top:170px;text-align:center;color:#1d1f22">
  <div style="font-weight:300;font-size:92px;letter-spacing:.06em">BUILDING</div>
  <div style="font-weight:300;font-style:italic;font-size:58px;letter-spacing:.03em;margin-top:-4px">INDIA'S NEXT FACTORIES</div>
  <div style="margin-top:34px;font-weight:600;font-size:17px;letter-spacing:.34em">ISAPUR INDUSTRIAL PARK</div>
  <div style="margin-top:12px;font-weight:500;font-size:15px;letter-spacing:.3em;color:#55575c">ROOM TO BUILD. ROOM TO GROW.</div></div>
 <div style="position:absolute;left:96px;top:640px;font:600 38px Caveat;color:#25272b;transform:rotate(-4deg);line-height:1.1">Plug in.<br>Build up.</div>
 <svg style="position:absolute;left:150px;top:735px" width="130" height="120" viewBox="0 0 130 120" fill="none" stroke="#25272b" stroke-width="3" stroke-linecap="round"><path d="M10 6 C 20 70, 60 100, 118 104"/><path d="M96 90 L 118 104 L 94 114"/></svg>
 <div style="position:absolute;right:70px;top:610px;font:600 38px Caveat;color:#25272b;text-align:right;transform:rotate(3deg);line-height:1.1">Together we<br>make it real.</div></div>"""


def door_poster(w=1000, h=1250):
    return f"""<div class=p><div class=bg style="background-image:url({plate('plate-door')})"></div>
 <img src="{B.LOGO}" style="position:absolute;left:70px;top:64px;width:120px">
 <div style="position:absolute;left:0;right:0;top:230px;text-align:center;color:#fff">
  <div style="font-weight:300;font-size:150px;letter-spacing:-.01em;line-height:1">Step in.</div>
  <div style="margin-top:34px;font-weight:600;font-size:18px;letter-spacing:.36em">ISAPUR INDUSTRIAL PARK</div></div>
 <div style="position:absolute;right:60px;bottom:48px;font:600 16px Inter;letter-spacing:.24em;color:#fff">9837057800  |  9219549800</div></div>"""


def steps_wide():
    return f"""<div class=p style="width:1200px;height:500px"><div class=bg style="background-image:url({plate('plate-steps', 1200)});background-position:0 52%"></div>
 <img src="{B.LOGO}" style="position:absolute;left:56px;top:44px;width:92px">
 <div style="position:absolute;left:56px;top:170px;color:#15171A">
  <div style="font-weight:300;font-size:50px;line-height:1.1">Every factory begins<br>with <b style="font-weight:700">one step.</b></div>
  <div style="margin-top:20px;width:64px;height:5px;background:{B.RED}"></div>
  <div style="margin-top:18px;font-weight:600;font-size:14px;letter-spacing:.34em">ISAPUR INDUSTRIAL PARK</div></div></div>"""


def steps_tall():
    return f"""<div class=p style="width:1000px;height:1800px"><div class=bg style="background-image:url({plate('plate-steps', 1800)});background-position:20% 100%"></div>
 <img src="{B.LOGO}" style="position:absolute;left:70px;top:70px;width:130px">
 <div style="position:absolute;left:70px;top:300px;color:#15171A">
  <div style="font-weight:300;font-size:92px;line-height:1.08">Every<br>factory<br>begins with<br><b style="font-weight:700">one step.</b></div>
  <div style="margin-top:36px;width:90px;height:8px;background:{B.RED}"></div>
  <div style="margin-top:30px;font-weight:600;font-size:21px;letter-spacing:.34em">ISAPUR INDUSTRIAL PARK</div></div></div>"""


POSTERS = {"steps": steps_poster, "build": build_poster, "door": door_poster}
EXTRA = {"steps-hoarding": (steps_wide, 1200, 500, 2), "steps-tall": (steps_tall, 1000, 1800, 2)}


def main(names):
    with sync_playwright() as p:
        br = p.chromium.launch()
        for n in names:
            if not (ROOT / f"gen/plate-{n}.png").exists() or (ROOT / f"gen/plate-{n}.png").stat().st_size < 1000:
                print("skip", n); continue
            pg = br.new_page(viewport={"width": 1000, "height": 1250}, device_scale_factor=2)
            pg.set_content(wrap(POSTERS[n](), 1000, 1250)); pg.wait_for_load_state("networkidle"); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(500)
            pg.screenshot(path=str(OUT / f"{n}.png")); pg.close(); print("ok", n)
        for n, (fn, w, h, d) in EXTRA.items():
            pg = br.new_page(viewport={"width": w, "height": h}, device_scale_factor=d)
            pg.set_content(wrap(fn(), w, h)); pg.wait_for_load_state("networkidle"); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(500)
            pg.screenshot(path=str(OUT / f"{n}.png")); pg.close(); print("ok", n)
        br.close()


if __name__ == "__main__":
    main(sys.argv[1:] or list(POSTERS))

