"""Print colour data: converts each brand colour from sRGB to CMYK through a real ICC profile (US Web Coated SWOP, shipped with Windows)
and back, to show how much it shifts on press. Writes research/print-colors.json.  Run: python 01_Brand/Brand-Kit/_build/print_colors.py"""
import json, pathlib
from PIL import Image, ImageCms
from skimage import color

KIT = pathlib.Path(__file__).resolve().parents[1]
ICC = r"C:\Windows\System32\spool\drivers\color\RSWOP.icm"
TOK = json.loads((KIT / "tokens/brand.tokens.json").read_text())
srgb = ImageCms.createProfile("sRGB"); cmyk = ImageCms.getOpenProfile(ICC)
to_cmyk = ImageCms.buildTransform(srgb, cmyk, "RGB", "CMYK", renderingIntent=ImageCms.Intent.RELATIVE_COLORIMETRIC)
back = ImageCms.buildTransform(cmyk, srgb, "CMYK", "RGB", renderingIntent=ImageCms.Intent.RELATIVE_COLORIMETRIC)
rgb = lambda h: tuple(int(h.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))

items = {k: v["value"] for k, v in TOK["color"].items()}
items.update({"badge yellow": "#FEF102", "badge red": "#EE1D23", "badge green": "#00A54F", "dark gray": "#6B7280", "light gray": "#E6E8EB"})
out = {}
for n, h in items.items():
    im = Image.new("RGB", (1, 1), rgb(h)); c = to_cmyk.apply(im); cm = tuple(round(x / 255 * 100) for x in c.getpixel((0, 0)))
    r = back.apply(c).getpixel((0, 0))
    d = float(color.deltaE_ciede2000(color.rgb2lab([[list(x / 255 for x in rgb(h))]]), color.rgb2lab([[list(x / 255 for x in r)]]))[0][0])
    out[n] = {"hex": h, "rgb": rgb(h), "cmyk": cm, "on_press_hex": "#%02X%02X%02X" % r, "delta_e": round(d, 1),
              "verdict": "close match" if d < 4 else "slightly duller on press" if d < 9 else "noticeably duller on press, ask for a proof"}
(KIT / "research/print-colors.json").write_text(json.dumps({"profile": "US Web Coated SWOP (RSWOP.icm), relative colorimetric", "note": "Planning values. Always approve a printer proof; offset, flex and vinyl each print a little differently.", "colors": out}, indent=1), encoding="utf-8")
for n, v in out.items(): print(n, v["hex"], v["cmyk"], v["delta_e"], v["verdict"])
