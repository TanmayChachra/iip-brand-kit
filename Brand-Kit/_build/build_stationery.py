"""Round 5 applications, redone (additive). Writes live/ and outlined/ 06_Stationery/*.svg from kitlib + tokens/content.json.
Units: 10 user units = 1 mm for print pieces (width/height attributes carry the real mm size), 1 unit = 1 px for screen pieces.
Run: python Brand-Kit/_build/build_stationery.py   (then export.py)"""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import kitlib as K
from kitlib import C, text, badge, lockup_horizontal, lockup_vertical, sunburst, stripe, icon, svg, width

CT = json.loads((K.KIT / "tokens/content.json").read_text())
PH = "  |  ".join(CT["phones"])
ADDR1, ADDR2 = "Hapur-Modinagar Road, Yusufpur Isapur,", "Ghaziabad, UP 201022"
TAG = CT["taglines"]["approved"]
INK, MIST, GRAY, LINE, GREEN, YEL, RED = C["charcoal"], C["mist"], C["gray"], C["line"], C["green"], C["yellow"], C["red"]
OUT = {}


def page(wmm, hmm, body, title, bg="#FFFFFF", unit=10, px=False):
    W, H = round(wmm * unit), round(hmm * unit)
    wa, ha = (f"{wmm}px", f"{hmm}px") if px else (f"{wmm}mm", f"{hmm}mm")
    return svg(W, H, body, wa, ha, title, bg)


def crop(W, H, inner, uid):
    return f'<clipPath id="cp{uid}"><rect width="{W}" height="{H}"/></clipPath><g clip-path="url(#cp{uid})">{inner}</g>'


def tri(x, y, w, h, cols, sk=None):
    """Stripe in any three colours (stripe() is fixed to yellow, red, green)."""
    sk = sk if sk is not None else h * 0.9; unit = (w - sk) / 3.0; s = ""
    for i, c in enumerate(cols):
        x0 = x + i * unit
        s += f'<polygon points="{x0 + sk:.1f},{y:.1f} {x0 + sk + unit * 1.05:.1f},{y:.1f} {x0 + unit * 1.05:.1f},{y + h:.1f} {x0:.1f},{y + h:.1f}" fill="{c}"/>'
    return s


def centred(fn, W, cy, *a, **k):
    """Place a horizontal lockup centred on x=W/2 and on y=cy. Returns svg."""
    s0, wd = fn(0, 0, *a, **k); h = a[0]
    return f'<g transform="translate({(W - wd) / 2:.1f} {cy - h / 2:.1f})">{s0}</g>'


# ---------------- business cards 88.9 x 50.8 mm ----------------
def card_front_A():
    W, H = 889, 508
    b = crop(W, H, sunburst(835, 70, 250, MIST), "a")
    s, h = lockup_vertical(W / 2, 70, 172, uid="cfa"); b += s
    b += stripe(0, 456, W, 52, 46)
    OUT["06_Stationery/card-front-A"] = page(88.9, 50.8, b, "Business card front A, vertical lockup")


def card_front_B():
    W, H = 889, 508
    b = crop(W, H, sunburst(60, 460, 230, MIST), "b")
    b += centred(lockup_horizontal, W, 228, 150, uid="cfb")
    b += stripe(0, 456, W, 52, 46)
    OUT["06_Stationery/card-front-B"] = page(88.9, 50.8, b, "Business card front B, horizontal lockup")


def card_back():
    W, H = 889, 508; WH = "#FFFFFF"
    b = f'<rect width="{W}" height="{H}" fill="{GREEN}"/>'
    b += crop(W, H, sunburst(800, 420, 330, "none", WH, 3, opacity=0.16) + sunburst(800, 420, 250, "none", WH, 3, opacity=0.10), "c")
    s, _ = lockup_horizontal(62, 62, 96, ink=WH, mono=(WH, GREEN), uid="cb"); b += s
    b += text(TAG[1], 62, 262, 38, "Montserrat-SemiBold", WH)
    b += f'<rect x="62" y="288" width="86" height="6" fill="{YEL}"/>'
    b += text(CT["phones"][0] + "  |  " + CT["phones"][1], 62, 360, 30, "Montserrat-ExtraBold", WH, 0.02)
    b += text(ADDR1, 62, 400, 20, "Inter-Regular", WH, 0.0, "start", 0.88) + text(ADDR2, 62, 428, 20, "Inter-Regular", WH, 0.0, "start", 0.88)
    b += tri(0, 478, W, 30, [YEL, RED, WH])
    OUT["06_Stationery/card-back"] = page(88.9, 50.8, b, "Business card back, deep green")


def visiting_card():
    W, H = 889, 508
    b = badge(724, 56, 108, uid="vc")
    b += text("Full Name", 62, 150, 50, "Montserrat-ExtraBold", INK) + text("Designation", 62, 192, 25, "Inter-Medium", GRAY)
    b += f'<rect x="62" y="222" width="70" height="6" fill="{RED}"/>'
    b += icon("phone", 58, 262, 30, INK, 2.2) + text(PH, 104, 286, 24, "Inter-Medium", INK)
    b += icon("location-pin", 58, 312, 30, INK, 2.2) + text(ADDR1, 104, 331, 20, "Inter-Regular", INK) + text(ADDR2, 104, 357, 20, "Inter-Regular", INK)
    b += text("ISAPUR", 62, 435, 28, "Montserrat-ExtraBold", INK, 0.04) + text("INDUSTRIAL PARK", 190, 435, 16, "Montserrat-SemiBold", INK, 0.3)
    b += stripe(0, 466, W, 42, 38)
    OUT["06_Stationery/visiting-card"] = page(88.9, 50.8, b, "Visiting card with name and designation placeholders")


# ---------------- letterhead, header strip, notepad ----------------
def letterhead():
    W, H = 2100, 2970
    b = crop(W, H, sunburst(1900, 2420, 640, MIST), "l")
    s, _ = lockup_horizontal(200, 170, 150, uid="lh"); b += s
    b += text(PH, 1900, 232, 27, "Montserrat-ExtraBold", INK, 0.02, "end")
    b += text(ADDR1 + " " + ADDR2, 1900, 280, 20, "Inter-Regular", GRAY, 0.0, "end")
    b += f'<rect x="200" y="400" width="1700" height="2" fill="{INK}" fill-opacity=".18"/>'
    b += text("Ref. No.", 200, 500, 21, "Inter-Medium", GRAY) + text("Date", 1900, 500, 21, "Inter-Medium", GRAY, 0.0, "end")
    b += text(TAG[0], 1050, 2815, 21, "Inter-Medium", GRAY, 0.0, "middle")
    b += stripe(0, 2890, W, 80, 70)
    OUT["06_Stationery/letterhead-A4"] = page(210, 297, b, "Letterhead A4")


def doc_header():
    W, H = 2100, 350
    s, _ = lockup_horizontal(200, 85, 150, uid="dh"); b = s
    b += text("QUOTATION", 1900, 160, 46, "Montserrat-ExtraBold", INK, 0.04, "end")
    b += text("Ref. No.            Date", 1900, 212, 21, "Inter-Medium", GRAY, 0.0, "end")
    b += stripe(0, 310, W, 40, 36)
    OUT["06_Stationery/doc-header-strip"] = page(210, 35, b, "Invoice and quotation header strip")


def notepad():
    W, H = 1480, 2100
    b = crop(W, H, sunburst(1320, 1930, 520, MIST), "n")
    s, _ = lockup_horizontal(130, 130, 118, uid="np"); b += s
    b += f'<rect x="130" y="330" width="{W - 260}" height="2" fill="{INK}" fill-opacity=".18"/>'
    for y in range(450, 1900, 64): b += f'<rect x="130" y="{y}" width="{W - 260}" height="2" fill="{LINE}"/>'
    b += text(PH, W / 2, 2000, 22, "Montserrat-ExtraBold", INK, 0.02, "middle")
    b += stripe(0, 2042, W, 58, 52)
    OUT["06_Stationery/notepad-A5"] = page(148, 210, b, "Notepad sheet A5")


# ---------------- envelopes ----------------
def envelope(wmm, hmm, name, title):
    W, H = round(wmm * 10), round(hmm * 10); k = H / 1100
    b = crop(W, H, sunburst(W - 130 * k, 90 * k, 420 * k, MIST), name)
    s, _ = lockup_horizontal(110 * k, 110 * k, 110 * k, uid="en" + name); b += s
    b += text("Isapur Industrial Park", 110 * k, 880 * k, 24 * k, "Montserrat-ExtraBold", INK, 0.02)
    b += text(ADDR1 + " " + ADDR2, 110 * k, 925 * k, 18 * k, "Inter-Regular", GRAY) + text(PH, 110 * k, 962 * k, 18 * k, "Inter-Medium", GRAY)
    b += stripe(0, H - 56 * k, W, 56 * k, 50 * k)
    OUT[f"06_Stationery/{name}"] = page(wmm, hmm, b, title)


# ---------------- ID card 54 x 86 mm ----------------
def id_front():
    W, H = 540, 860
    b = f'<rect x="{W / 2 - 60}" y="38" width="120" height="26" rx="13" fill="none" stroke="{GRAY}" stroke-width="2" stroke-dasharray="8 6"/>'
    b += text("slot 12 x 2.5 mm", W / 2, 90, 11, "Inter-Medium", GRAY, 0.0, "middle")
    s, h = lockup_vertical(W / 2, 120, 118, uid="idf"); b += s
    b += f'<rect x="170" y="392" width="200" height="250" rx="14" fill="{MIST}" stroke="{LINE}" stroke-width="2"/>'
    b += text("PHOTO", 270, 525, 20, "Inter-Medium", GRAY, 0.1, "middle")
    b += text("Full Name", W / 2, 700, 42, "Montserrat-ExtraBold", INK, 0.0, "middle") + text("Designation", W / 2, 738, 22, "Inter-Medium", GRAY, 0.0, "middle")
    b += text("ID No.", W / 2, 782, 20, "Inter-Medium", GRAY, 0.0, "middle")
    b += stripe(0, 820, W, 40, 36)
    OUT["06_Stationery/id-card-front"] = page(54, 86, b, "ID card front, 54 x 86 mm")


def id_back():
    W, H = 540, 860
    b = crop(W, H, sunburst(470, 760, 300, MIST), "ib")
    b += badge(W / 2 - 40, 90, 80, uid="idb")
    b += text("If found, please return to", W / 2, 240, 20, "Inter-Medium", GRAY, 0.0, "middle")
    b += text("ISAPUR", W / 2, 305, 52, "Montserrat-ExtraBold", INK, 0.04, "middle") + text("INDUSTRIAL PARK", W / 2, 340, 17, "Montserrat-SemiBold", INK, 0.3, "middle")
    b += f'<rect x="{W / 2 - 35}" y="372" width="70" height="5" fill="{RED}"/>'
    b += text(ADDR1, W / 2, 430, 20, "Inter-Regular", INK, 0.0, "middle") + text(ADDR2, W / 2, 458, 20, "Inter-Regular", INK, 0.0, "middle")
    b += text(CT["phones"][0], W / 2, 520, 28, "Montserrat-ExtraBold", INK, 0.02, "middle") + text(CT["phones"][1], W / 2, 560, 28, "Montserrat-ExtraBold", INK, 0.02, "middle")
    b += text("Blood group", 70, 650, 18, "Inter-Medium", GRAY) + f'<rect x="200" y="652" width="270" height="2" fill="{LINE}"/>'
    b += text("Emergency no.", 70, 700, 18, "Inter-Medium", GRAY) + f'<rect x="200" y="702" width="270" height="2" fill="{LINE}"/>'
    b += stripe(0, 820, W, 40, 36)
    OUT["06_Stationery/id-card-back"] = page(54, 86, b, "ID card back, 54 x 86 mm")


# ---------------- screen pieces ----------------
def email_signature():
    b = badge(10, 22, 100, uid="es")
    b += f'<rect x="132" y="26" width="2" height="108" fill="{INK}"/>'
    b += text("Full Name", 154, 54, 21, "Montserrat-ExtraBold", INK) + text("Designation, Isapur Industrial Park", 154, 76, 13, "Inter-Medium", GRAY)
    b += f'<rect x="154" y="90" width="44" height="3" fill="{RED}"/>'
    b += text("T  " + PH, 154, 116, 14, "Inter-Medium", INK) + text(ADDR1 + " " + ADDR2, 154, 138, 12, "Inter-Regular", GRAY)
    b += stripe(0, 160, 600, 8, 7)
    OUT["06_Stationery/email-signature"] = page(600, 168, b, "Email signature, 600 px wide", unit=1, px=True)


def catalogue():
    W = 1080
    b = crop(W, W, sunburst(840, 300, 520, MIST), "cat")
    s, _ = lockup_horizontal(80, 80, 120, uid="ct"); b += s
    b += text("Industrial", 80, 560, 128, "Montserrat-ExtraBold", INK) + text("Plots", 80, 690, 128, "Montserrat-ExtraBold", INK)
    b += f'<rect x="80" y="740" width="150" height="10" fill="{RED}"/>'
    b += text("Plot list, layout map and documents", 80, 820, 38, "Inter-Medium", GRAY)
    b += text(PH, 80, 960, 40, "Montserrat-ExtraBold", INK, 0.02)
    b += stripe(0, 1010, W, 70, 62)
    OUT["06_Stationery/catalogue-cover-1080"] = page(W, W, b, "WhatsApp catalogue cover 1080", unit=1, px=True)


# ---------------- folder, helmet, vest, stamp ----------------
def folder():
    W, H = 2100, 2970
    b = f'<polygon points="0,2150 {W},1730 {W},{H} 0,{H}" fill="{MIST}"/>'
    b += f'<clipPath id="fcl"><polygon points="0,2150 {W},1730 {W},{H} 0,{H}"/></clipPath><g clip-path="url(#fcl)">{sunburst(1750, 2430, 800, "#FFFFFF")}</g>'
    s, _ = lockup_horizontal(200, 200, 140, uid="fo"); b += s
    b += text("The Groundwork", 200, 1090, 172, "Montserrat-ExtraBold", INK, -0.01) + text("for Growth.", 200, 1290, 172, "Montserrat-ExtraBold", INK, -0.01)
    b += f'<rect x="200" y="1370" width="260" height="14" fill="{RED}"/>'
    b += text("Industrial plots on the Hapur-Modinagar Road", 200, 1480, 46, "Inter-Medium", GRAY)
    b += text(PH, 200, 2700, 56, "Montserrat-ExtraBold", INK, 0.02) + text(ADDR1 + " " + ADDR2, 200, 2760, 30, "Inter-Regular", GRAY)
    b += stripe(0, 2880, W, 90, 80)
    OUT["06_Stationery/folder-cover-A4"] = page(210, 297, b, "Folder or brochure cover A4")


def helmet():
    W, H = 2100, 1480; MG = "#E5007D"
    b = text("HELMET DECALS", 150, 130, 30, "Montserrat-SemiBold", INK, 0.14)
    x = 150
    for mm in (60, 45, 30):
        s = mm * 10
        b += badge(x, 520 - s / 2, s, uid=f"hd{mm}")
        b += f'<circle cx="{x + s / 2}" cy="520" r="{s / 2 + 6}" fill="none" stroke="{MG}" stroke-width="3" stroke-dasharray="14 8"/>'
        b += f'<path d="M{x} {520 + s / 2 + 52}H{x + s}" stroke="{GREEN}" stroke-width="3"/><path d="M{x} {520 + s / 2 + 42}v20M{x + s} {520 + s / 2 + 42}v20" stroke="{GREEN}" stroke-width="3"/>'
        b += text(f"{mm} mm", x + s / 2, 520 + s / 2 + 108, 28, "Inter-Medium", INK, 0.0, "middle")
        x += s + 210
    b += stripe(150, 1000, 1500, 120, 100)
    b += f'<rect x="144" y="994" width="1512" height="132" fill="none" stroke="{MG}" stroke-width="3" stroke-dasharray="14 8"/>'
    b += text("Side stripe decal 150 x 12 mm", 150, 1190, 28, "Inter-Medium", INK)
    b += text("Magenta dashed line = cut contour. Print on white or reflective vinyl and cut to contour. Confirm material and size with the helmet supplier.", 150, 1330, 23, "Inter-Regular", GRAY)
    OUT["06_Stationery/helmet-decals"] = page(210, 148, b, "Safety helmet decal sheet")


VEST = "M130 0H190Q240 {neck}290 0H350L400 40Q388 150 420 190L400 640H80L60 190Q92 150 80 40Z"


def vest(front, tx, uid):
    neck = 90 if front else 36
    d = VEST.replace("{neck}", f"{neck} ")
    g = f'<clipPath id="vc{uid}"><path d="{d}"/></clipPath><path d="{d}" fill="{YEL}" stroke="{INK}" stroke-width="2" stroke-linejoin="round"/>'
    bands = ''.join(f'<rect x="40" y="{y}" width="420" height="48" fill="#D5D9DF"/>' for y in (330, 470))
    bands += '<rect x="138" y="0" width="46" height="330" fill="#D5D9DF"/><rect x="296" y="0" width="46" height="330" fill="#D5D9DF"/>'
    g += f'<g clip-path="url(#vc{uid})">{bands}</g>'
    g += f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="2" stroke-linejoin="round"/>'
    if front:
        g += f'<path d="M240 {neck - 2}V640" stroke="{INK}" stroke-width="1.5" stroke-dasharray="6 5"/>'
        g += f'<circle cx="360" cy="190" r="50" fill="#FFFFFF" stroke="{INK}" stroke-width="1.5"/>' + badge(320, 150, 80, uid=f"vb{uid}")
    else:
        g += f'<rect x="100" y="110" width="280" height="180" rx="14" fill="#FFFFFF" stroke="{INK}" stroke-width="1.5"/>'
        s, wd = lockup_horizontal(0, 0, 66, uid=f"vl{uid}")
        g += f'<g transform="translate({240 - wd / 2:.1f} 167)">{s}</g>'
    return f'<g transform="translate({tx} 250) scale(4)">{g}</g>'


def vest_layout():
    W, H = 4200, 2970
    b = text("SAFETY VEST PRINT LAYOUT", 160, 130, 54, "Montserrat-SemiBold", INK, 0.14)
    b += vest(True, 240, "f") + vest(False, 2040, "b")
    b += text("FRONT", 1200, 2860, 40, "Montserrat-SemiBold", INK, 0.2, "middle") + text("BACK", 3000, 2860, 40, "Montserrat-SemiBold", INK, 0.2, "middle")
    b += text("Left chest: badge 80 mm on a white 100 mm patch", 1200, 2925, 34, "Inter-Medium", GRAY, 0.0, "middle")
    b += text("Back: horizontal lockup on a white patch, 280 x 180 mm", 3000, 2925, 34, "Inter-Medium", GRAY, 0.0, "middle")
    b += text("Drawn at 1:2.5. Yellow is the brand yellow, check hi-vis class and reflective band spec with the vest maker.", 160, 210, 30, "Inter-Regular", GRAY)
    OUT["06_Stationery/vest-layout"] = page(420, 297, b, "Safety vest print layout")


def stamp():
    W = 500
    s, h = lockup_vertical(W / 2, 60, 170, ink="#000000", mono=("#000000", "#FFFFFF"), line="#000000", uid="st")
    b = s + f'<rect x="20" y="20" width="{W - 40}" height="{h + 80}" rx="30" fill="none" stroke="#E5007D" stroke-width="3" stroke-dasharray="14 8"/>'
    OUT["06_Stationery/stamp-one-colour"] = page(50, round((h + 120) / 10, 1), b, "One colour badge and wordmark for stamps (magenta = guide, do not print)")


for outline in (False, True):
    K.MODE["outline"] = outline; OUT.clear()
    card_front_A(); card_front_B(); card_back(); visiting_card(); letterhead(); doc_header(); notepad()
    envelope(220, 110, "envelope-DL", "Envelope DL 220 x 110 mm"); envelope(229, 162, "envelope-C5", "Envelope C5 229 x 162 mm")
    id_front(); id_back(); email_signature(); catalogue(); folder(); helmet(); vest_layout(); stamp()
    sub = "outlined" if outline else "live"
    d = K.KIT / sub / "06_Stationery"; d.mkdir(parents=True, exist_ok=True)
    for rel, s in OUT.items(): (K.KIT / sub / (rel + ".svg")).write_text(s, encoding="utf-8")
print("stationery", len(OUT))
