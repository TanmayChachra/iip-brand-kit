"""Context mockups of the NEW signage: exact artwork warped into blank panels of real-looking roadside scenes (perspective warp,
panel shading kept, neutral light). Output: Brand-Kit/reference/mockups/ctx-*.webp (2400 px wide, q88).
Reuses Archive/work-v1/warp.py and mock4.py.  python Brand-Kit/_build/build_ctx_mockups.py"""
import pathlib, sys, shutil
import cv2, numpy as np
from PIL import Image, ImageFilter

KIT = pathlib.Path(__file__).resolve().parents[1]
OLD = KIT.parent / "Archive/work-v1"
sys.path.insert(0, str(OLD))
import warp as W            # composite()
import mock4 as M4          # on_pole()
PNG = KIT / "export/png"
OUT = KIT / "reference/mockups"; OUT.mkdir(parents=True, exist_ok=True)
TMP = pathlib.Path(__file__).resolve().parent / "_ctx_tmp"; TMP.mkdir(exist_ok=True)
UP = 2.0


def pad(art_path, aspect):
    """white margin so the art keeps its shape inside a panel of a different aspect (like a real printed flex on a bigger frame)."""
    a = Image.open(art_path).convert("RGB"); w, h = a.size
    if w / h < aspect: nw, nh = round(h * aspect), h
    else: nw, nh = w, round(w / aspect)
    c = Image.new("RGB", (nw, nh), (250, 250, 250)); c.paste(a, ((nw - w) // 2, (nh - h) // 2))
    p = TMP / (pathlib.Path(art_path).stem + f"-{aspect:.2f}.png"); c.save(p); return p


def scaled(scene, quads):
    im = cv2.imread(str(scene)); im = cv2.resize(im, None, fx=UP, fy=UP, interpolation=cv2.INTER_CUBIC)
    p = TMP / (pathlib.Path(scene).stem + "-up.png"); cv2.imwrite(str(p), im)
    return p, [(np.array(q, np.float32) * UP).tolist() for q in quads]


def quad_aspect(q):
    q = np.array(q); return float((np.linalg.norm(q[1] - q[0]) + np.linalg.norm(q[2] - q[3])) / (np.linalg.norm(q[3] - q[0]) + np.linalg.norm(q[2] - q[1])))


def chain(scene, jobs, out, inset=0.012):
    """jobs = [(art_png, quad)], quads in the ORIGINAL scene pixels."""
    sp, qs = scaled(scene, [q for _, q in jobs]); cur = sp
    for i, ((art, _), q) in enumerate(zip(jobs, qs)):
        a = pad(art, quad_aspect(q)); nxt = TMP / f"_step{i}.jpg"
        W.composite(cur, a, nxt, quad=q, inset=inset); cur = nxt
    return cur


def save(src, name, width=2400):
    im = Image.open(src).convert("RGB"); k = width / im.width
    im = im.resize((width, round(im.height * k)), Image.LANCZOS).filter(ImageFilter.UnsharpMask(1.2, 60, 2))
    im.save(OUT / f"{name}.webp", quality=88, method=6); print(name, im.size)


# ---- 1. hoarding and pole beside competitors (scene-versus: competitor Balaji flat on top, IIP pole below, hoarding right)
top = [[391, 184], [533, 205], [528, 428], [378, 418]]
bot = [[381, 432], [528, 436], [527, 672], [368, 676]]
hoa = [[801, 433], [1127, 452], [1126, 574], [798, 569]]
r = chain(OLD / "gen/scene-versus.png", [(OLD / "gen/competitor-balaji-flat.png", top), (PNG / "sign-pole-20x32in-A.png", bot), (PNG / "sign-hoarding-40x15ft.png", hoa)], "x", 0.01)
save(r, "ctx-hoarding-beside-competitors")

# ---- 2. big roadside hoarding 40 x 20 ft, both tagline variants
HOARD = [[440, 51], [1381, 110], [1387, 437], [440, 447]]
save(chain(OLD / "gen/scene-hoarding-a.png", [(PNG / "sign-hoarding-40x20ft-A.png", HOARD)], "x", 0.014), "ctx-hoarding-roadside-A")
save(chain(OLD / "gen/scene-hoarding-a.png", [(PNG / "sign-hoarding-40x20ft-B.png", HOARD)], "x", 0.014), "ctx-hoarding-roadside-B")

# ---- 3. row of street pole boards
ROW = [[[1160, 292], [1293, 292], [1293, 536], [1160, 538]], [[659, 464], [737, 464], [736, 601], [659, 603]], [[464, 531], [517, 531], [517, 625], [464, 626]],
       [[357, 568], [396, 568], [396, 640], [357, 640]], [[294, 590], [326, 590], [326, 649], [294, 649]], [[249, 604], [277, 604], [277, 655], [249, 655]]]
save(chain(OLD / "gen/scene-poles-a.png", [(PNG / "sign-street-pole-24x36in.png", q) for q in ROW], "x", 0.0), "ctx-street-pole-row")

# ---- 4. gate fascia
GATE = [[160, 236], [619, 386], [619, 478], [165, 388]]
save(chain(OLD / "gen/scene-gate-a.png", [(PNG / "sign-gate-fascia-4to1.png", GATE)], "x", 0.0), "ctx-gate-fascia")

# ---- 5. pole boards on the real poles (A under Shri Balaji, B on the stack), side by side so the page has no empty space
p1 = Image.open(OLD / "src/real-pole-1.jpg"); stack = Image.open(OLD / "src/real-pole-stack.jpg")
a = M4.on_pole(p1, Image.open(PNG / "sign-pole-20x32in-A.png"), 650, 846, 190, 304)
b = M4.on_pole(stack, Image.open(PNG / "sign-pole-20x32in-B.png"), 652, 1338, 172, 275)
H = 1600; a = a.resize((round(a.width * H / a.height), H), Image.LANCZOS); b = b.resize((round(b.width * H / b.height), H), Image.LANCZOS)
d = Image.new("RGB", (a.width + b.width, H)); d.paste(a, (0, 0)); d.paste(b, (a.width, 0)); d.save(TMP / "poles.png")
save(TMP / "poles.png", "ctx-pole-boards-on-real-poles")
shutil.rmtree(TMP, ignore_errors=True)
