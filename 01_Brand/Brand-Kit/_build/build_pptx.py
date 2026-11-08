"""Editable PowerPoint versions (open in PowerPoint, Keynote, Google Slides or import into Canva).
Text is native (Montserrat / Inter), shapes are native, badge and photo are pictures. One .pptx per template."""
import json, pathlib
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

KIT = pathlib.Path(__file__).resolve().parents[1]
TOK = json.loads((KIT / "tokens/brand.tokens.json").read_text()); CT = json.loads((KIT / "tokens/content.json").read_text())
C = {k: v["value"] for k, v in TOK["color"].items()}
BADGE = KIT.parent / "work/logo/iip-master-3x.png"
HERO = KIT / "assets/hero-warehouse.jpg"
OUT = KIT / "editable-pptx"; OUT.mkdir(exist_ok=True)
rgb = lambda h: RGBColor.from_string(h.lstrip("#").upper())


class Slide:
    def __init__(self, w_in, h_in, units_w, units_h):
        self.p = Presentation(); self.p.slide_width = Inches(w_in); self.p.slide_height = Inches(h_in)
        self.s = self.p.slides.add_slide(self.p.slide_layouts[6])
        self.kx = w_in / units_w; self.ky = h_in / units_h; self.k = self.kx
        self.bg("#FFFFFF")

    def bg(self, col):
        f = self.s.background.fill; f.solid(); f.fore_color.rgb = rgb(col)

    def rect(self, x, y, w, h, col, shape=MSO_SHAPE.RECTANGLE):
        r = self.s.shapes.add_shape(shape, Inches(x * self.kx), Inches(y * self.ky), Inches(w * self.kx), Inches(h * self.ky))
        r.fill.solid(); r.fill.fore_color.rgb = rgb(col); r.line.fill.background(); return r

    def para(self, x, y, w, h, txt, size_units, font, col, bold=False, align="l", spacing=None):
        tb = self.s.shapes.add_textbox(Inches(x * self.kx), Inches(y * self.ky), Inches(w * self.kx), Inches(h * self.ky))
        tf = tb.text_frame; tf.word_wrap = True; tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        tf.vertical_anchor = MSO_ANCHOR.TOP
        lines = txt if isinstance(txt, list) else [txt]
        for i, l in enumerate(lines):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.alignment = {"l": PP_ALIGN.LEFT, "c": PP_ALIGN.CENTER, "r": PP_ALIGN.RIGHT}[align]
            r = p.add_run(); r.text = l; r.font.name = font; r.font.bold = bold; r.font.size = Pt(size_units * self.k * 72); r.font.color.rgb = rgb(col)
        return tb

    def pic(self, path, x, y, w, h=None):
        return self.s.shapes.add_picture(str(path), Inches(x * self.kx), Inches(y * self.ky), Inches(w * self.kx), Inches(h * self.ky) if h else None)

    def stripe(self, x, y, w, h):
        unit = w / 3
        for i, c in enumerate((C["yellow"], C["red"], C["green"])):
            fb = self.s.shapes.build_freeform(Inches((x + i * unit + h * .9) * self.kx), Inches(y * self.ky))
            fb.add_line_segments([(Inches((x + (i + 1) * unit + h * .9 + 4) * self.kx), Inches(y * self.ky)), (Inches((x + (i + 1) * unit + 4) * self.kx), Inches((y + h) * self.ky)), (Inches((x + i * unit) * self.kx), Inches((y + h) * self.ky))])
            sh = fb.convert_to_shape(); sh.fill.solid(); sh.fill.fore_color.rgb = rgb(c); sh.line.fill.background()

    def save(self, name): self.p.save(OUT / name)


def lockup(sl, cx, y, bw, ink=None):
    ink = ink or C["charcoal"]
    sl.pic(BADGE, cx - bw / 2, y, bw, bw * 1.0)
    sl.para(cx - bw * 1.2, y + bw * 1.08, bw * 2.4, bw * .6, "ISAPUR", bw * .48 * 1.0, "Montserrat ExtraBold", ink, True, "c")
    sl.para(cx - bw * 1.2, y + bw * 1.08 + bw * .62, bw * 2.4, bw * .2, "INDUSTRIAL PARK", bw * .13, "Montserrat SemiBold", ink, False, "c")


def pole():
    sl = Slide(20, 32, 1000, 1600)
    lockup(sl, 500, 80, 250)
    sl.pic(HERO, 0, 660, 1000, 740 * 0 + 530)
    sl.para(120, 520, 810, 330, CT["tagline"], 88, "Montserrat SemiBold", C["charcoal"], False, "r")
    sl.para(0, 1450, 1000, 70, "   |   ".join(CT["phones"]), 58, "Montserrat ExtraBold", C["charcoal"], True, "c")
    sl.stripe(0, 1556, 1000, 44); sl.save("pole-board-20x32in.pptx")


def hoarding():
    sl = Slide(40, 20, 2000, 1000)  # 1 inch per foot. Scale up 12x when printing.
    sl.pic(BADGE, 90, 330, 330)
    sl.para(520, 380, 520, 160, "ISAPUR", 112, "Montserrat ExtraBold", C["charcoal"], True)
    sl.para(520, 530, 520, 60, "INDUSTRIAL PARK", 30, "Montserrat SemiBold", C["charcoal"])
    sl.rect(1066, 270, 6, 440, C["line"])
    sl.para(1150, 270, 800, 520, CT["tagline"], 124, "Montserrat SemiBold", C["charcoal"])
    sl.para(0, 800, 2000, 120, "   |   ".join(CT["phones"]), 92, "Montserrat ExtraBold", C["charcoal"], True, "c")
    sl.stripe(0, 940, 2000, 60); sl.save("hoarding-40x20ft-scaled-1in-per-ft.pptx")


def card():
    for side in ("front", "back"):
        sl = Slide(3.5, 2, 1050, 600)
        if side == "front":
            sl.pic(BADGE, 70, 130, 340)
            sl.para(470, 190, 520, 130, "ISAPUR", 100, "Montserrat ExtraBold", C["charcoal"], True)
            sl.para(470, 330, 520, 50, "INDUSTRIAL PARK", 30, "Montserrat SemiBold", C["charcoal"])
        else:
            sl.para(70, 120, 700, 80, "Name Surname", 60, "Montserrat ExtraBold", C["charcoal"], True)
            sl.para(70, 215, 700, 40, "Director", 30, "Inter", C["gray"])
            sl.para(70, 310, 800, 120, CT["phones"], 36, "Montserrat SemiBold", C["charcoal"])
            sl.para(70, 435, 900, 40, "sales@yourdomain.in", 30, "Inter", C["charcoal"])
            sl.pic(BADGE, 790, 70, 190)
        sl.stripe(0, 560, 1050, 40); sl.save(f"business-card-{side}-3.5x2in.pptx")


pole(); hoarding(); card()
print(sorted(p.name for p in OUT.iterdir()))
