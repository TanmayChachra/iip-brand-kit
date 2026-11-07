"""Social media starter templates (additive, does not touch build_kit.py). Writes live/ and outlined/ 05_Social/*.svg.
Run:  python Brand-Kit/_build/build_social.py   then   python Brand-Kit/_build/export.py"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import kitlib as K
import build_kit as B
from kitlib import C, text, badge, lockup_horizontal, lockup_vertical, sunburst, stripe, svg

OUT = {}


def avatar():
    W = 1080                                       # profile picture: badge only, safe inside a circle crop
    b = badge(W * 0.17, W * 0.17, W * 0.66, uid="av")
    OUT["05_Social/avatar-badge-1080"] = svg(W, W, b, "1080px", "1080px", "Profile picture (badge, circle safe)", C["white"])
    b = sunburst(W / 2, W / 2, W * 0.5, C["mist"]) + badge(W * 0.2, W * 0.2, W * 0.6, uid="av2")
    OUT["05_Social/avatar-badge-sunburst-1080"] = svg(W, W, b, "1080px", "1080px", "Profile picture (badge on sunburst)", C["white"])


def cover():
    W, H = 1500, 500                               # 3:1, works for X header, LinkedIn and Facebook with safe crops
    b = sunburst(1290, 80, 330, C["mist"])
    s, wd = lockup_horizontal(90, 120, 250, uid="cv"); b += s
    b += text("A Modern Industrial Address.", 1380, 300, 30, "Montserrat-SemiBold", C["charcoal"], 0.0, "end")
    b += f'<rect x="1230" y="322" width="150" height="7" fill="{C["red"]}"/>'
    b += text(B.PH, 1380, 386, 28, "Montserrat-ExtraBold", C["charcoal"], 0.02, "end")
    b += stripe(-(46), 450, W + 2 * (46), 50, 46)
    OUT["05_Social/cover-3to1-1500x500"] = svg(W, H, b, "1500px", "500px", "Cover banner 3:1", C["white"])


def post45():
    W, H = 1080, 1350                              # Instagram and Facebook portrait post
    b = sunburst(930, 200, 470, C["mist"])
    s, _ = lockup_horizontal(80, 90, 210, uid="p45"); b += s
    ts = min(128, 920 / max(K.width(l, "Montserrat-SemiBold", 1.0, 0.0) for l in B.CT["tagline"]))
    b += B.tag3(80, 700, ts, "start")
    b += f'<rect x="80" y="1010" width="130" height="9" fill="{C["red"]}"/>'
    b += text("Industrial Plot Available", 80, 1100, 40, "Inter-Medium", C["charcoal"], 0.0, "start")
    b += text(B.PH, 80, 1190, 46, "Montserrat-ExtraBold", C["charcoal"], 0.02, "start")
    b += stripe(-(72), 1270, W + 2 * (72), 80, 72)
    OUT["05_Social/post-4x5-1080x1350"] = svg(W, H, b, "1080px", "1350px", "Social post 4:5", C["white"])


for outline in (False, True):
    K.MODE["outline"] = outline; OUT.clear()
    avatar(); cover(); post45()
    sub = "outlined" if outline else "live"
    for rel, s in OUT.items():
        p = K.KIT / sub / (rel + ".svg"); p.parent.mkdir(parents=True, exist_ok=True); p.write_text(s, encoding="utf-8")
print("social templates", len(OUT))
