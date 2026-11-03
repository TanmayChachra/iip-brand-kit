"""Round 2 mockups: exact artwork placed into real / neutral-light photographs."""
import pathlib, shutil
from PIL import Image
import mock as K
import warp as W

ROOT = pathlib.Path(__file__).resolve().parent
B2 = ROOT / "b2"
OUT = ROOT / "mock2"; OUT.mkdir(exist_ok=True)
KITS = ["quiet", "portal", "ink"]

HOARD = [[440, 51], [1381, 110], [1387, 437], [440, 447]]
GATE = [[160, 236], [619, 386], [619, 478], [165, 388]]
ROW = [  # nearest to farthest, inner corners tl, tr, br, bl
    [[1160, 292], [1293, 292], [1293, 536], [1160, 538]],
    [[659, 464], [737, 464], [736, 601], [659, 603]],
    [[464, 531], [517, 531], [517, 625], [464, 626]],
    [[357, 568], [396, 568], [396, 640], [357, 640]],
    [[294, 590], [326, 590], [326, 649], [294, 649]],
    [[249, 604], [277, 604], [277, 655], [249, 655]],
]


def main():
    pole1 = Image.open(ROOT / "src/real-pole-1.jpg")
    stack = Image.open(ROOT / "src/real-pole-stack.jpg")
    for k in KITS:
        for s in ["10x10", "10x12", "10x14"]:
            art = Image.open(B2 / f"{k}-{s}.png")
            w_in, h_in = map(int, s.split("x"))
            w, h = round(w_in * 9.2), round(h_in * 9.2)
            K.place(pole1, art, (629 - w // 2, 852, w, h)).save(OUT / f"{k}-{s}-pole.jpg", quality=92)
            w2, h2 = round(w_in * 6.6), round(h_in * 6.6)
            K.place(stack, art, (648 - w2 // 2, 1350, w2, h2)).save(OUT / f"{k}-{s}-stack.jpg", quality=92)
        art = Image.open(B2 / f"{k}-10x14.png")
        K.place(pole1, art, (553, 852, 189, round(189 * 1.4))).save(OUT / f"{k}-18x25-pole.jpg", quality=92)
        W.composite(ROOT / "gen/scene-hoarding-a.png", B2 / f"{k}-hoarding.png", OUT / f"{k}-hoarding.jpg", quad=HOARD)
        W.composite(ROOT / "gen/scene-gate-a.png", B2 / f"{k}-gate.png", OUT / f"{k}-gate.jpg", quad=GATE)
        # street-pole row: same board on every pole
        cur = ROOT / "gen/scene-poles-a.png"
        for i, q in enumerate(ROW):
            tmp = OUT / f"_{k}-row.jpg"
            W.composite(cur, B2 / f"{k}-10x18.png", tmp, quad=q, inset=0.0)
            cur = OUT / f"_{k}-row{i}.jpg"; shutil.copy(tmp, cur)
        shutil.copy(cur, OUT / f"{k}-row.jpg")
    # Portal pole serial: step 1, step 2, step 3, door
    arts = [B2 / f"portal-step-{i}.png" for i in (1, 2, 3)] + [B2 / "portal-10x14.png"]
    tiles = []
    for a in arts:
        im = K.place(pole1, Image.open(a), (629 - 46, 852, 92, 129))
        tiles.append(im.crop((440, 700, 820, 1060)))
    sheet = Image.new("RGB", (380 * 4 + 30, 360), (255, 255, 255))
    for i, t in enumerate(tiles): sheet.paste(t, (i * 390, 0))
    sheet.save(OUT / "portal-serial.jpg", quality=92)


if __name__ == "__main__":
    main()
