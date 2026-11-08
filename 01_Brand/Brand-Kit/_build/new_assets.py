"""Round 5 assets: (1) trace the supplied dark green rosette emblem to a one colour SVG,
(2) store the three finalised reference boards and crop the application mockups from them (WEBP, for the site and book).
Inputs: ../IIP Assets/Dark Green IIP Rosette Emblem.png and the three boards pasted by the owner (path in BOARDS)."""
import pathlib, re, sys
import numpy as np, vtracer
from PIL import Image, ImageFilter

KIT = pathlib.Path(__file__).resolve().parents[1]
ROOT = KIT.parent
SRC = ROOT / "IIP Assets/Dark Green IIP Rosette Emblem.png"
BOARDS = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else None
GREEN = "#0F4D3A"

# ---- 1. emblem trace ----
im = Image.open(SRC).convert("L")
K = 3
big = im.resize((im.width * K, im.height * K), Image.BICUBIC).filter(ImageFilter.GaussianBlur(2.2))
mask = (np.asarray(big) < 128)
tmp = KIT / "_build/_emblem_bin.png"
Image.fromarray(np.where(mask, 0, 255).astype("uint8")).save(tmp)
out = KIT / "_build/_emblem_trace.svg"
vtracer.convert_image_to_svg_py(str(tmp), str(out), colormode="binary", hierarchical="stacked", mode="spline",
                                filter_speckle=40, corner_threshold=60, length_threshold=4.0, splice_threshold=45, path_precision=2)
raw = out.read_text()
paths = re.findall(r'<path d="([^"]+)"(?:[^>]*?transform="translate\(([-\d.]+),([-\d.]+)\)")?', raw)
body = "".join(f'<path d="{d}"' + (f' transform="translate({x},{y})"' if x else "") + "/>" for d, x, y in paths)
W, H = im.size
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}px" height="{H}px">'
       f'<title>IIP rosette emblem, one colour (dark green)</title>'
       f'<g id="emblem" transform="scale({1/K:.6f})" fill="{GREEN}" fill-rule="evenodd">{body}</g></svg>')
for sub in ("live", "outlined"):
    (KIT / sub / "01_Logo/logo-badge-mono-green.svg").write_text(svg, encoding="utf-8")
tmp.unlink(); out.unlink()
print("emblem svg", len(svg))

# ---- 2. reference boards + crops ----
if BOARDS:
    ref = KIT / "reference"; (ref / "mockups").mkdir(parents=True, exist_ok=True)
    names = {1: "board-1-brand-kit-extended", 2: "board-2-sunburst-asset-type", 3: "board-3-brand-kit-final"}
    for n, nm in names.items():
        Image.open(BOARDS / f"{n}.webp").convert("RGB").save(ref / f"{nm}.webp", quality=90, method=6)
    crops = {  # board, name, (x0, y0, x1, y1) in the board's own pixels
        (1, "stationery-letterhead-envelope"): (438, 697, 654, 842), (1, "business-card"): (662, 697, 868, 842),
        (1, "id-card"): (878, 697, 1085, 842), (1, "safety-helmet"): (1094, 697, 1300, 842), (1, "safety-vest"): (1309, 697, 1514, 842),
        (2, "sunburst-image-mask"): (428, 112, 712, 392), (2, "sunburst-feature-badge"): (806, 112, 1092, 392),
        (2, "sunburst-cta-badge"): (1190, 112, 1480, 392), (2, "sunburst-variations"): (990, 535, 1515, 698),
        (2, "wall-sign"): (383, 823, 725, 1000), (2, "envelope-sunburst"): (1242, 823, 1510, 1000),
        (3, "pole-board-street"): (532, 24, 1051, 806), (3, "hoarding-billboard"): (1062, 77, 1461, 366),
        (3, "gate-fascia"): (1062, 374, 1461, 571), (3, "boundary-wall"): (1062, 579, 1461, 808),
    }
    for (b, nm), box in crops.items():
        Image.open(BOARDS / f"{b}.webp").convert("RGB").crop(box).save(ref / "mockups" / f"{nm}.webp", quality=88, method=6)
    print("crops", len(crops))
