# Builds the white die-cut halo (24-point star outline) of the IIP logo from the supplied JPEG.
# Prints one SVG <g id="halo"> in logo source coordinates (1080x1085 space).
import sys, re, numpy as np, vtracer
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage as ndi
src = sys.argv[1]; K = 4
im = Image.open(src).convert("RGB"); w, h = im.size
d = ImageDraw.Draw(im); d.rectangle((0, 1085, w, h), fill="white"); d.rectangle((930, 1030, w, 1090), fill="white")
im = im.crop((0, 0, w, 1085)); w, h = im.size
a = np.asarray(im).astype(int)
white = (a.min(-1) > 245)                       # pure page white only; hairline (light grey) is NOT white
lab, n = ndi.label(white); outer = lab == (1 + np.bincount(lab[lab > 0]).argmax() - 1 if False else np.bincount(lab.ravel())[1:].argmax() + 1)   # largest white region = page
inside = ~outer                                  # badge + hairline
inside = ndi.binary_fill_holes(inside)
big = Image.fromarray((inside * 255).astype("uint8")).resize((w * K, h * K), Image.BICUBIC).filter(ImageFilter.GaussianBlur(5))
m = np.asarray(big) > 127
Image.fromarray(np.where(m, 0, 255).astype("uint8")).save("_halo.png")
vtracer.convert_image_to_svg_py("_halo.png", "_halo.svg", colormode="binary", hierarchical="stacked", mode="polygon",
    filter_speckle=200, corner_threshold=60, length_threshold=8.0, path_precision=1)
s = open("_halo.svg").read(); paths = re.findall(r"<path[^>]*/>", s)
body = "".join(re.sub(r'fill="[^"]*"', "", p) for p in paths)
print(f'<g id="halo" fill="#FFFFFF" stroke="#D2D2D2" stroke-width="5" stroke-linejoin="miter" transform="scale({1/K})">{body}</g>')
