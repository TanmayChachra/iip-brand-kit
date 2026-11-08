# Traces the grey decorative leaves from the reference as filled shapes (flat #ebebeb measured) -> SVG paths in poster px.
import re, numpy as np, vtracer
from PIL import Image
from scipy import ndimage as ndi
im = Image.open("../01_Source/poster-reference.webp").convert("L"); a = np.asarray(im).astype(int); K = 3
m = (a < 247) & (a > 215)
reg = np.zeros_like(m); reg[30:420, 1380:] = True; reg[1790:, :240] = True   # leaf areas only (excludes stripes, text, photo)
m &= reg; m = ndi.binary_opening(m, iterations=1); m = ndi.binary_fill_holes(m)
out = Image.fromarray(np.where(m, 0, 255).astype("uint8")).resize((a.shape[1] * K, a.shape[0] * K), Image.BICUBIC)
out.save("_leaf.png")
vtracer.convert_image_to_svg_py("_leaf.png", "_leaf.svg", colormode="binary", mode="spline", filter_speckle=400, corner_threshold=60, length_threshold=6.0, path_precision=1)
s = open("_leaf.svg").read(); ps = re.findall(r"<path[^>]*/>", s)
print(f'<g id="decor-leaves" fill="#EBEBEB" transform="scale({1/K})">' + "".join(re.sub(r'fill="[^"]*"', "", p) for p in ps) + "</g>", end="")
