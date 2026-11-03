import math, pathlib
from PIL import Image, ImageDraw, ImageFont
import maps as M

ROOT = M.ROOT
im = Image.open(ROOT / "gen/map-raw.png").convert("RGB")
d = ImageDraw.Draw(im, "RGBA")
def font(sz, bold=True):
    for f in ["C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"]:
        try: return ImageFont.truetype(f, sz)
        except Exception: pass
    return ImageFont.load_default()

def hav(a, b):
    R = 6371000; p1, p2 = math.radians(a[0]), math.radians(b[0]); dl = math.radians(b[1] - a[1]); dp = p2 - p1
    h = math.sin(dp/2)**2 + math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
    return 2*R*math.asin(math.sqrt(h))

P = M.PINS
dist = {k: hav(P["IIP Phase 1"], v) for k, v in P.items() if k != "IIP Phase 1"}
print({k: round(v) for k, v in dist.items()})

def pin(name, xy, col, r, label, side=1):
    x, y = xy
    d.ellipse([x-r-4, y-r-4, x+r+4, y+r+4], fill=(255, 255, 255, 235))
    d.ellipse([x-r, y-r, x+r, y+r], fill=col)
    f = font(26 if name == "IIP Phase 1" else 22)
    w = d.textlength(label, font=f)
    bx = x + r + 12 if side > 0 else x - r - 12 - w - 20
    by = y - 17
    d.rounded_rectangle([bx, by, bx + w + 20, by + 36], 8, fill=(20, 17, 15, 225))
    d.text((bx + 10, by + 4), label, font=f, fill=(255, 255, 255, 255))

# road line (approximate, along the pins)
pts = [M.px(*P["IIP Phase 1"]), M.px(*P["SHD"]), M.px(*P["CKS"]), M.px(*P["Atom"])]
pin("SHD", M.px(*P["SHD"]), (30, 30, 120, 255), 11, f"SHD Industrial Park  ~{dist['SHD']/1000:.1f} km", 1)
pin("CKS", M.px(*P["CKS"]), (30, 30, 120, 255), 11, f"CKS Industrial Park  ~{dist['CKS']/1000:.1f} km", 1)
pin("Atom", M.px(*P["Atom"]), (30, 30, 120, 255), 11, f"Atom Industrial Park  ~{dist['Atom']/1000:.1f} km", -1)
pin("IIP Phase 1", M.px(*P["IIP Phase 1"]), (254, 241, 2, 255), 17, "ISAPUR INDUSTRIAL PARK  Phase 1", -1)
# scale bar 500 m
mpp = 156543.03 * math.cos(math.radians(28.78)) / 2 ** M.Z
L = 500 / mpp
x, y = 40, im.height - 50
d.rectangle([x - 12, y - 34, x + L + 16, y + 22], fill=(0, 0, 0, 150))
d.rectangle([x, y, x + L, y + 8], fill=(255, 255, 255, 255))
d.text((x, y - 28), "500 m", font=font(20), fill=(255, 255, 255, 255))
# north arrow
d.polygon([(im.width - 60, 40), (im.width - 76, 84), (im.width - 44, 84)], fill=(255, 255, 255, 235))
d.text((im.width - 68, 88), "N", font=font(22), fill=(255, 255, 255, 255))
# attribution
t = "Imagery: Esri, Maxar, Earthstar Geographics. Pin positions approximate."
f = font(16, False); w = d.textlength(t, font=f)
d.rectangle([im.width - w - 24, im.height - 30, im.width, im.height], fill=(0, 0, 0, 150))
d.text((im.width - w - 12, im.height - 26), t, font=f, fill=(255, 255, 255, 255))
im.save(ROOT / "gen/map-annotated.png")
import json; json.dump({k: round(v) for k, v in dist.items()}, open(ROOT / "gen/dist.json", "w"))
