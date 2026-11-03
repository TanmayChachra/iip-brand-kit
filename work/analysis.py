"""Colour distinctness (CIEDE2000) of each direction vs the road environment and competitor boards, plus WCAG contrast."""
import json, numpy as np, pathlib
from PIL import Image
from scipy.cluster.vq import kmeans2
from skimage.color import rgb2lab, deltaE_ciede2000

ROOT = pathlib.Path(__file__).resolve().parent
def lab(rgb): return rgb2lab(np.array([[rgb]], np.float64) / 255)[0, 0]
def hex2rgb(h): h = h.lstrip('#'); return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
def de(a, b): return float(deltaE_ciede2000(lab(a)[None, None], lab(b)[None, None])[0, 0])

def dominant(img, box, k=4):
    im = Image.open(img).convert("RGB").crop(box).resize((100, 100))
    px = np.asarray(im).reshape(-1, 3)
    np.random.seed(1)
    cen, lbl = kmeans2(px.astype(float), k, minit='++', seed=1)
    cnt = np.bincount(lbl, minlength=k)
    order = np.argsort(-cnt)
    return [tuple(int(v) for v in cen[i]) for i in order if cnt[i] > 0]

src = ROOT / "src"
env = {
    "Roadside foliage": dominant(src / "real-pole-1.jpg", (0, 0, 520, 1200), 5)[:3],
    "Concrete and dust": dominant(src / "real-pole-1.jpg", (0, 1300, 1200, 1600), 3)[:2],
    "Hazy sky": dominant(src / "real-pole-1.jpg", (800, 0, 1200, 300), 2)[:1],
}
comp = {
    "Shri Balaji (blue board)": dominant(src / "real-pole-1.jpg", (565, 545, 735, 790), 4)[:3],
    "Shri Balaji (red board)": dominant(src / "real-pole-stack.jpg", (570, 640, 760, 960), 3)[:2],
    "Shri Haridas (SHD)": dominant(src / "real-pole-stack.jpg", (590, 160, 800, 600), 4)[:3],
    "Shivansh": dominant(src / "real-pole-stack.jpg", (565, 1000, 740, 1330), 3)[:3],
}
brands = {
    "jamun": {"Jamun violet": "#4B1DA6", "Sun yellow": "#FEF102", "White": "#FFFFFF"},
    "gulaal": {"Gulaal pink": "#E4007C", "Sun yellow": "#FEF102", "Cream": "#FFF4DC"},
    "kora": {"Kora ivory": "#FBF6E9", "Ink": "#14110F", "Sun yellow": "#FEF102"},
}
def lum(rgb):
    f = lambda c: (c/255/12.92) if c/255 <= .03928 else ((c/255 + .055)/1.055) ** 2.4
    r, g, b = rgb; return .2126*f(r) + .7152*f(g) + .0722*f(b)
def cr(a, b):
    la, lb = lum(a), lum(b); hi, lo = max(la, lb), min(la, lb); return (hi + .05) / (lo + .05)

out = {"env": {k: ['#%02X%02X%02X' % c for c in v] for k, v in env.items()},
       "comp": {k: ['#%02X%02X%02X' % c for c in v] for k, v in comp.items()}, "brands": {}}
for kit, cols in brands.items():
    main_name, main_hex = list(cols.items())[0]
    m = hex2rgb(main_hex)
    groups = {}
    for gname, g in {**env, **comp}.items():
        groups[gname] = round(min(de(m, c) for c in g), 1)
    nearest = min(groups, key=groups.get)
    out["brands"][kit] = {"main": main_name, "hex": main_hex, "deltaE": groups, "nearest": nearest, "nearest_de": groups[nearest]}
out["contrast"] = {
    "jamun": {"white on violet": round(cr((255,255,255), hex2rgb("#4B1DA6")), 1), "yellow on violet": round(cr(hex2rgb("#FEF102"), hex2rgb("#4B1DA6")), 1)},
    "gulaal": {"cream on pink": round(cr(hex2rgb("#FFF4DC"), hex2rgb("#E4007C")), 1), "ink on yellow": round(cr(hex2rgb("#1A0B2E"), hex2rgb("#FEF102")), 1)},
    "kora": {"ink on ivory": round(cr(hex2rgb("#14110F"), hex2rgb("#FBF6E9")), 1), "ink on yellow": round(cr(hex2rgb("#14110F"), hex2rgb("#FEF102")), 1)},
}
json.dump(out, open(ROOT / "analysis.json", "w"), indent=1)
print(json.dumps(out["brands"], indent=1)); print(out["contrast"])
