"""Satellite mosaic of the Hapur-Modinagar road around Isapur from Esri World Imagery tiles (attribution required)."""
import math, io, requests, pathlib
from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parent
Z = 16
CENTER = (28.7755, 77.6695)
NX, NY = 9, 5

def tile_xy(lat, lon, z):
    n = 2 ** z
    x = (lon + 180) / 360 * n
    y = (1 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2 * n
    return x, y

cx, cy = tile_xy(*CENTER, Z)
x0, y0 = int(cx - NX / 2), int(cy - NY / 2)
mos = Image.new("RGB", (NX * 256, NY * 256))
for i in range(NX):
    for j in range(NY):
        u = f"https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{Z}/{y0+j}/{x0+i}"
        r = requests.get(u, timeout=30, headers={"User-Agent": "iip-brand-kit/1.0"}); r.raise_for_status()
        mos.paste(Image.open(io.BytesIO(r.content)).convert("RGB"), (i * 256, j * 256))
mos.save(ROOT / "gen/map-raw.png")

def px(lat, lon):
    x, y = tile_xy(lat, lon, Z)
    return (x - x0) * 256, (y - y0) * 256

PINS = {   # approximate, read from Google Maps; verify against imagery
    "IIP Phase 1": (28.7812, 77.6559),
    "SHD": (28.7784, 77.6604),
    "CKS": (28.7770, 77.6611),
    "Atom": (28.7686, 77.6843),
}
print({k: px(*v) for k, v in PINS.items()}, mos.size)
