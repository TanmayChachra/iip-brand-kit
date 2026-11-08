"""Round 5 pattern fixes (additive, run after build_kit.py):
 - sunburst-ring-border: the real ring cut out of the badge artwork (exact diamonds and yellow rim), transparent centre.
 - sunburst-repeat-pattern: larger cells, firmer line, high resolution.   python 01_Brand/Brand-Kit/_build/build_patterns2.py"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import kitlib as K
from kitlib import C, svg, sunburst, BADGE

W = BADGE["w"]; c = W / 2
P = BADGE["paths"]; col = BADGE["colors"]


def ring():
    Ro, Ri = W * 0.53, W * 0.35                       # keep only the diamond band, cut from the real badge artwork
    clip = (f'<clipPath id="rg"><path clip-rule="evenodd" d="M{c - Ro} {c}a{Ro} {Ro} 0 1 0 {2 * Ro} 0a{Ro} {Ro} 0 1 0 {-2 * Ro} 0z '
            f'M{c - Ri} {c}a{Ri} {Ri} 0 1 0 {2 * Ri} 0a{Ri} {Ri} 0 1 0 {-2 * Ri} 0z '
            f'M{0.0342 * W - 0.016 * W} {0.5267 * W}a{0.016 * W} {0.016 * W} 0 1 0 {0.032 * W} 0a{0.016 * W} {0.016 * W} 0 1 0 {-0.032 * W} 0z"/></clipPath>')   # last circle removes a stray speck in the source trace
    body = (f'<g clip-path="url(#rg)"><path d="{P["red"]}" fill="{col["base"]}" stroke="{col["base"]}" stroke-width="46" stroke-linejoin="round" fill-rule="evenodd"/>'
            f'<path d="{P["red"]}" fill="{col["red"]}" fill-rule="evenodd"/></g>')
    return svg(W, W, body, "1200px", "1200px", "Sunburst ring, cut from the badge artwork", None, clip)


def repeat():
    cells = "".join(sunburst(150 + 250 * cc + (125 if r % 2 else 0), 130 + 217 * r, 116, C["mist"], "#B4BCC8", 3.5, depth=0.12) for r in range(7) for cc in range(7))
    return svg(1800, 1500, cells, "1800px", "1500px", "Sunburst repeating pattern", C["white"])


for outline in (False, True):
    K.MODE["outline"] = outline
    sub = "outlined" if outline else "live"
    (K.KIT / sub / "02_Pattern/sunburst-ring-border.svg").write_text(ring(), encoding="utf-8")
    (K.KIT / sub / "02_Pattern/sunburst-repeat-pattern.svg").write_text(repeat(), encoding="utf-8")
print("patterns2 ok")
