"""Crops the Unsplash stand-ins to the exact boxes the site shows (the skill's photo-upscale check wants the source in the box's ratio).
Sources: .taste-skill/cand/<id>.jpg (Unsplash, 1800 px wide). Outputs: public/img/photo/<name>-<kind>.webp
kinds: hero (3:2, 1600 and 960), m (4:5 phone crop 960x1200), 43 (4:3, as wide as the source allows), sq (1:1 960)."""
import pathlib, json
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / ".taste-skill/cand"; OUT = ROOT / "public/img/photo"
U = lambda i: SRC.parent / "cand2" / f"{i}.jpg"
W = lambda i: SRC.parent / "wm" / f"photo-{i}.webp"
FILES = {"expressway-a": W("f122935210"), "expressway-b": W("f122935199"), "road-india": U("1598105397032"), "road-green": U("1596829568009"), "verge-palms": U("1705821365889"),
         "sheds-blue": U("1787063757757"), "sheds-aerial": U("1787058105751"), "street-light": U("1578326516120"), "factory-yard": U("1636867900334"), "jcb-lowbed": U("1709735133497"),
         "shed-dusk": U("1655575900119"), "truck-white": U("1627019866926")}
# focus: where the crop is centred, as fractions (x, y) of the source
FOCUS = {"expressway-a": (0.5, 0.62), "street-light": (0.5, 0.45), "sheds-blue": (0.5, 0.62), "factory-yard": (0.35, 0.6), "shed-dusk": (0.45, 0.5), "sheds-aerial": (0.5, 0.55), "jcb-lowbed": (0.55, 0.55)}


def crop(im, ratio, name):
    w, h = im.size; fx, fy = FOCUS.get(name, (0.5, 0.5))
    cw, ch = (w, int(w / ratio)) if w / h < ratio else (int(h * ratio), h)
    x = min(max(int(fx * w - cw / 2), 0), w - cw); y = min(max(int(fy * h - ch / 2), 0), h - ch)
    return im.crop((x, y, x + cw, y + ch))


def save(im, path, q=72):
    im.save(path, "WEBP", quality=q, method=6)


def main():
    for p in OUT.glob("*.webp"): p.unlink()
    info = {}
    for name, f in FILES.items():
        im = Image.open(f).convert("RGB")
        r = crop(im, 3.6, name)
        for w in (1600, 960):                       # hero desktop band, 3.6:1 (the 1600 file is as wide as the source allows)
            ww = min(w, r.width); save(r.resize((ww, int(ww / 3.6))), OUT / f"{name}-hero-{w}.webp")
        m = crop(im, 4 / 5, name)
        for w in (780, 360):                        # 4:5 phone crops: hero (780) and wall tiles (360)
            save(m.resize((w, int(w * 1.25))), OUT / f"{name}-m-{w}.webp", 70)
        f = crop(im, 4 / 3, name)
        for w in (1350, 800, 600):                  # 4:3 frames: visit and booking photographs, wall tiles
            ww = min(w, f.width); save(f.resize((ww, int(ww * 0.75))), OUT / f"{name}-43-{w}.webp")
        q = crop(im, 1, name)
        for w in (600, 320):                        # 1:1 detail strip
            ww = min(w, q.width); save(q.resize((ww, ww)), OUT / f"{name}-sq-{w}.webp")
    wm = {x["id"]: x for x in json.load(open(SRC.parent / "wm" / "credits.json"))["photos"]}
    cred = {"note": "Stand-ins until the park's own shoot. Unsplash License (free, no credit needed) and Wikimedia Commons (credit and licence below).", "unsplash": {k: f"https://unsplash.com/photos/{f.stem}" for k, f in FILES.items() if "cand2" in str(f)},
            "wikimedia": {k: {"by": wm[f.stem[6:]]["by"], "licence": wm[f.stem[6:]]["licence"], "page": wm[f.stem[6:]]["page"]} for k, f in FILES.items() if "/wm/" in str(f).replace(chr(92), "/")}}
    (OUT / "credits.json").write_text(json.dumps(cred, indent=1))
    print(sum(p.stat().st_size for p in OUT.glob("*.webp")) // 1024, "KB total,", len(list(OUT.glob("*.webp"))), "files")


main()
