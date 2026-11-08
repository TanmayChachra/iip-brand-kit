"""Trace the supplied badge (raster only, no vector source exists) into a small clean SVG using flat colour masks.
It is a TRACE of the supplied artwork, not a redraw. Replace with the original vector if one is found.
Output: badge-paths.json (viewBox 0 0 W H, layers: base yellow, red, green)."""
import json, pathlib, numpy as np, cv2
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parents[2]
SRC = ROOT / "work/logo/iip-master-3x.png"
OUT = pathlib.Path(__file__).resolve().parent / "badge-paths.json"

im = np.array(Image.open(SRC).convert("RGBA")).astype(np.int32)
rgb, a = im[..., :3], im[..., 3]
pal = {"yellow": (254, 241, 2), "red": (238, 29, 35), "green": (0, 165, 79)}
dist = np.stack([((rgb - np.array(v)) ** 2).sum(2) for v in pal.values()], 0)
idx = dist.argmin(0)
H, W = a.shape
solid = a > 128


def contours_to_path(mask, eps):
    m = (mask.astype(np.uint8)) * 255
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    m = cv2.GaussianBlur(m, (0, 0), 1.2)
    m = (m > 127).astype(np.uint8) * 255
    cs, hier = cv2.findContours(m, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
    d = []
    for c in cs:
        if cv2.contourArea(c) < 40: continue
        ap = cv2.approxPolyDP(c, eps, True).reshape(-1, 2)
        if len(ap) < 3: continue
        d.append("M" + " L".join(f"{x:.0f} {y:.0f}" for x, y in ap) + "Z")
    return " ".join(d)


layers = {
    "base": contours_to_path(solid, 1.2),
    "red": contours_to_path(solid & (idx == 1), 1.0),
    "green": contours_to_path(solid & (idx == 2), 1.0),
}
data = {"w": W, "h": H, "colors": {"base": "#FEF102", "red": "#EE1D23", "green": "#00A54F"}, "paths": layers}
OUT.write_text(json.dumps(data))
print(W, H, {k: len(v) for k, v in layers.items()}, OUT.stat().st_size, "bytes")
