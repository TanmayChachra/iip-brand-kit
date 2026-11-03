"""Composite exact board artwork onto the user's real roadside photos. Exact artwork, real light: no AI re-drawing."""
import numpy as np, pathlib, sys
from PIL import Image, ImageFilter, ImageDraw

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT / "mock"; OUT.mkdir(exist_ok=True)
rng = np.random.default_rng(7)


def place(photo, art, box, tilt=0.0, shadow=(3, 4, 5, 0.45), gain=0.97, sat=0.93, blur=0.8, noise=2.6):
    """box = (x, y, w, h) of the board's top-left and size in photo pixels."""
    x, y, w, h = box
    a = art.convert("RGB").resize((w, h), Image.LANCZOS)
    # colour-match to a hazy phone photo: slightly flatter, slightly soft, with grain
    arr = np.asarray(a).astype(np.float32)
    g = arr.mean(2, keepdims=True)
    arr = g + (arr - g) * sat
    arr = arr * gain
    arr = 128 + (arr - 128) * 0.97
    # gentle top-to-bottom daylight falloff
    arr *= np.linspace(1.03, 0.96, h)[:, None, None]
    arr += rng.normal(0, noise, arr.shape)
    a = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(blur))
    # thin dark board edge
    ImageDraw.Draw(a).rectangle([0, 0, w - 1, h - 1], outline=(40, 40, 40), width=max(1, round(w / 90)))
    base = photo.convert("RGBA")
    dx, dy, rad, op = shadow
    sh = Image.new("L", base.size, 0)
    ImageDraw.Draw(sh).rectangle([x + dx, y + dy, x + w + dx, y + h + dy], fill=int(255 * op))
    sh = sh.filter(ImageFilter.GaussianBlur(rad))
    black = Image.new("RGBA", base.size, (0, 0, 0, 255)); black.putalpha(sh)
    base = Image.alpha_composite(base, black)
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    tile = a.convert("RGBA")
    if tilt:
        tile = tile.rotate(tilt, expand=True, resample=Image.BICUBIC)
    layer.paste(tile, (x - (tile.width - w) // 2, y - (tile.height - h) // 2), tile)
    return Image.alpha_composite(base, layer).convert("RGB")


def main():
    pole1 = Image.open(ROOT / "src/real-pole-1.jpg")
    stack = Image.open(ROOT / "src/real-pole-stack.jpg")
    for kit in ["jamun", "gulaal", "kora"]:
        for s in ["10x10", "10x12", "10x14"]:
            art = Image.open(ROOT / f"boards/{kit}-{s}.png")
            w_in, h_in = map(int, s.split("x"))
            ppi = 92 / 10.0   # pole face is about 10 in wide in the photo
            w, h = round(w_in * ppi), round(h_in * ppi)
            # flush on the pole face, just under the competitor board
            im = place(pole1, art, (629 - w // 2, 852, w, h))
            im.save(OUT / f"{kit}-{s}-pole.jpg", quality=92)
            # bottom of the three-board stack: same pole, same scale (pole ~ 66 px wide there)
            ppi2 = 66 / 10.0
            w2, h2 = round(w_in * ppi2), round(h_in * ppi2)
            im2 = place(stack, art, (648 - w2 // 2, 1350, w2, h2))
            im2.save(OUT / f"{kit}-{s}-stack.jpg", quality=92)
        # optional competitor-class size (18 in wide, same 10x14 proportions)
        art = Image.open(ROOT / f"boards/{kit}-10x14.png")
        w = 189; h = round(189 * 1.4)
        place(pole1, art, (553, 852, w, h)).save(OUT / f"{kit}-18x25-pole.jpg", quality=92)


if __name__ == "__main__":
    main()
