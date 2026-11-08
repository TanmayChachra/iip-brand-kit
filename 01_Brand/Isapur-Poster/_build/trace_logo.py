# Vectorizes the IIP logo JPEG into a layered flat-colour SVG.
# 1) remove page artefacts  2) snap every pixel to the brand palette (kills JPEG noise)
# 3) per colour: upscale 4x, blur, threshold (smooth, straight edges)  4) trace each layer with vtracer, stack in order.
import sys, re, numpy as np, vtracer
from PIL import Image, ImageDraw, ImageFilter
src, out = sys.argv[1], sys.argv[2]
K = 4
im = Image.open(src).convert("RGB"); w, h = im.size
d = ImageDraw.Draw(im)
d.rectangle((0, 1085, w, h), fill="white"); d.rectangle((930, 1030, w, 1090), fill="white")
im = im.crop((0, 0, w, 1085)); w, h = im.size
PAL = {"white": (255,255,255), "yellow": (254,241,2), "red": (238,29,35), "green": (0,165,79), "outline": (60,60,60), "diecut": (215,215,215)}
keys = list(PAL); cols = np.array([PAL[k] for k in keys])
a = np.asarray(im).astype(int)
idx = ((a[:, :, None, :] - cols[None, None]) ** 2).sum(-1).argmin(-1)
# the die-cut hairline and page white are background: only keep what is inside the star
white = (idx == keys.index("white")) | (idx == keys.index("diecut"))
from scipy import ndimage as ndi
lab, n = ndi.label(white); bg = lab == lab[0, 0]            # outer white = connected to the corner
inside = ~bg                                                 # everything in the badge (holes included)
masks = {
  "yellow":  inside,                                         # base disc + ring, drawn first
  "red":     idx == keys.index("red"),
  "green":   idx == keys.index("green"),
  "outline": idx == keys.index("outline"),
}
def smooth(m, blur):
    big = Image.fromarray((m * 255).astype("uint8")).resize((w * K, h * K), Image.BICUBIC).filter(ImageFilter.GaussianBlur(blur))
    return Image.fromarray(((np.asarray(big) > 127) * 0).astype("uint8") + np.where(np.asarray(big) > 127, 0, 255).astype("uint8"))  # black shape on white
FILL = {"yellow": "#FEF102", "red": "#EE1D23", "green": "#00A54F", "outline": "#3C3C3C"}
BLUR = {"yellow": 6, "red": 3.0, "green": 1.6, "outline": 1.2}
parts = []
for name in ["yellow", "red", "green", "outline"]:
    smooth(masks[name], BLUR[name]).save(f"_layer_{name}.png")
    vtracer.convert_image_to_svg_py(f"_layer_{name}.png", f"_layer_{name}.svg", colormode="binary", hierarchical="stacked",
        mode="spline", filter_speckle=24 if name != "outline" else 16, corner_threshold=70, length_threshold=6.0,
        splice_threshold=45, path_precision=1)
    s = open(f"_layer_{name}.svg").read()
    paths = re.findall(r"<path[^>]*/>", s)
    body = "".join(re.sub(r'fill="[^"]*"', "", p) for p in paths)
    parts.append(f'<g id="{name}" fill="{FILL[name]}" fill-rule="evenodd" transform="scale({1/K})">{body}</g>')
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
       f'<title>IIP logo (vector trace of supplied JPEG)</title>' + "".join(parts) + "</svg>")
open(out, "w", encoding="utf-8").write(svg); print(len(svg))
