"""Clean cropped WEBP snapshots of the layout PDFs (no sheet title block, no borders): img/phaseN-snapshot.webp.
Usage: python snapshots.py [--src DIR]. Needs pymupdf and pillow. Crop boxes are in page units after rotation."""
import io, pathlib, sys
import pymupdf
from PIL import Image, ImageDraw

HERE = pathlib.Path(__file__).parent
SRC = pathlib.Path(r"G:\My Drive\SilverleafBuildcon\Isapur Industrial Park\01_Layouts")
if "--src" in sys.argv:
    SRC = pathlib.Path(sys.argv[sys.argv.index("--src") + 1])
# phase: (crop x0, y0, x1, y1, [white-out rectangles]); Phase 1 sheet has no title block
CROP = {1: None, 2: (122, 16, 930, 833, []), 3: (26, 180, 590, 1052, [(0, 993, 395, 1100)])}
Z = 4
for ph, box in CROP.items():
    pg = pymupdf.open(SRC / f"IIP-Phase{ph}.pdf")[0]
    if box is None:
        r = pymupdf.Rect()
        for x in pg.get_drawings():
            r |= x["rect"]
        r = (r * pg.rotation_matrix) if False else r
        pts = [pymupdf.Point(r.x0, r.y0).transform(pg.rotation_matrix), pymupdf.Point(r.x1, r.y1).transform(pg.rotation_matrix)]
        box = (min(p.x for p in pts) - 8, min(p.y for p in pts) - 8, max(p.x for p in pts) + 8, max(p.y for p in pts) + 8, [])
    x0, y0, x1, y1, wh = box
    pm = pg.get_pixmap(matrix=pymupdf.Matrix(Z, Z), clip=pymupdf.Rect(x0, y0, x1, y1))
    im = Image.open(io.BytesIO(pm.tobytes("png"))).convert("RGB")
    d = ImageDraw.Draw(im)
    for a, b, c, e in wh:
        d.rectangle([(a - x0) * Z, (b - y0) * Z, (c - x0) * Z, (e - y0) * Z], fill="white")
    k = 2000 / max(im.size)
    if k < 1:
        im = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
    out = HERE / "img" / f"phase{ph}-snapshot.webp"
    out.parent.mkdir(exist_ok=True)
    im.save(out, "WEBP", quality=80)
    print(out.name, im.size, out.stat().st_size // 1024, "KB")
