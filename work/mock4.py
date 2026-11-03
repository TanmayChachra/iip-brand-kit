"""Round 3 mockups. Boards at true 10 in width on the real pole photo, with straps and shadow; plus street row, hoarding, gate."""
import pathlib, shutil
from PIL import Image, ImageDraw, ImageFilter
import mock as K
import warp as W
import mock2 as M

ROOT = M.ROOT
B3 = ROOT / "b3"
OUT = ROOT / "mock4"; OUT.mkdir(exist_ok=True)


def straps(im, x, y, w, h):
    d = ImageDraw.Draw(im)
    for yy in (y + 4, y + h - 9):
        d.rectangle([x - 4, yy, x + w + 4, yy + 4], fill=(48, 50, 52))
        d.rectangle([x - 4, yy, x + w + 4, yy + 1], fill=(92, 94, 96))
    return im


def on_pole(photo, art, cx, y, w, h):
    im = K.place(photo, art, (cx - w // 2, y, w, h), shadow=(3, 5, 5, 0.5))
    return straps(im, cx - w // 2, y, w, h)


def main():
    pole1 = Image.open(ROOT / "src/real-pole-1.jpg")
    stack = Image.open(ROOT / "src/real-pole-stack.jpg")
    for k in ("quiet", "ink"):
        for tag in ("clean", "proof"):
            art = Image.open(B3 / f"{k}-{tag}-20x32.png")
            # same width, shape and mounting as the Shri Balaji board directly above (190 x 307 px in the photo)
            on_pole(pole1, art, 650, 846, 190, 304).save(OUT / f"{k}-{tag}-pole.jpg", quality=92)
            on_pole(stack, art, 652, 1338, 172, 275).save(OUT / f"{k}-{tag}-stack.jpg", quality=92)
            W.composite(ROOT / "gen/scene-hoarding-a.png", B3 / f"{k}-{tag}-hoarding.png", OUT / f"{k}-{tag}-hoarding.jpg", quad=M.HOARD)
            cur = ROOT / "gen/scene-poles-a.png"
            for i, q in enumerate(M.ROW):
                tmp = OUT / f"_{k}{tag}-row.jpg"
                W.composite(cur, B3 / f"{k}-{tag}-20x36.png", tmp, quad=q, inset=0.0)
                cur = OUT / f"_{k}{tag}-row{i}.jpg"; shutil.copy(tmp, cur)
            shutil.copy(cur, OUT / f"{k}-{tag}-row.jpg")
        W.composite(ROOT / "gen/scene-gate-a.png", B3 / f"{k}-gate.png", OUT / f"{k}-gate.jpg", quad=M.GATE)
    for f in OUT.glob("_*"): f.unlink()


if __name__ == "__main__":
    main()

