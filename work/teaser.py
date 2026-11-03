"""Gulaal pole serial (Burma-Shave style): 3 teaser poles then the reveal."""
from playwright.sync_api import sync_playwright
from PIL import Image
import boards as B, mock as K

LINES = [("कारखाना<br>कहाँ<br>लगाओगे?", "#E4007C", "#FFF4DC"),
         ("सोच<br>रहे<br>हो?", "#FEF102", "#1A0B2E"),
         ("सोचना<br>बंद।<br>चलो।", "#1A0B2E", "#FEF102")]


def teaser(txt, bg, fg):
    return f"""<div class=b style="background:{bg};font-family:'Yatra One',serif;color:{fg};display:flex;align-items:center;justify-content:center;text-align:center">
 <div style="position:absolute;inset:3.2cqw;border:1.3cqw solid {fg};border-radius:3cqw;opacity:.9"></div>
 <div style="font-size:21cqw;line-height:1.08;text-shadow:.8cqw .8cqw 0 rgba(0,0,0,.35)">{txt}</div></div>"""


with sync_playwright() as p:
    br = p.chromium.launch()
    for i, (t, bg, fg) in enumerate(LINES, 1):
        pg = br.new_page(viewport={"width": 1000, "height": 1400}, device_scale_factor=3)
        pg.set_content(B.page(teaser(t, bg, fg), 10, 14)); pg.wait_for_load_state("networkidle"); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(400)
        pg.screenshot(path=str(B.OUT / f"gulaal-teaser-{i}.png")); pg.close()
    br.close()

pole = Image.open(B.ROOT / "src/real-pole-1.jpg")
arts = [B.OUT / f"gulaal-teaser-{i}.png" for i in (1, 2, 3)] + [B.OUT / "gulaal-10x14.png"]
tiles = []
for a in arts:
    im = K.place(pole, Image.open(a), (629 - 46, 852, 92, 129))
    tiles.append(im.crop((440, 700, 820, 1060)))
sheet = Image.new("RGB", (380 * 4 + 30, 360), (255, 255, 255))
for i, t in enumerate(tiles): sheet.paste(t, (i * 390, 0))
sheet.save(K.OUT / "gulaal-serial.jpg", quality=92)

