"""ONE master SVG: Brand-Kit/IIP-master-assets.svg
  Part 1: the brand book as 13 editable A4 landscape artboards (copy any piece straight out of it).
  Part 2: every individual SVG asset as a named group (logo, patterns, icons, signage, social, stationery).
Text is outlined so it opens anywhere (VectorCraft, Inkscape, Illustrator, Figma).  Run after the other builders:  python 01_Brand/Brand-Kit/_build/build_master.py"""
import json, pathlib, re, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import kitlib as K
from kitlib import C, text, svg, width, badge, lockup_vertical, lockup_horizontal, stripe, sunburst, icon

KIT = K.KIT; SRC = KIT / "outlined"
CT = json.loads((KIT / "tokens/content.json").read_text())
PC = json.loads((KIT / "research/print-colors.json").read_text())["colors"]
K.MODE["outline"] = True
T1, T2 = CT["taglines"]["approved"]
CH, CI, CG, CM = C["charcoal"], C["gray"], C["green"], C["mist"]
PW, PH = 1123, 794                       # A4 landscape at 96 dpi
GAP = 60
_cache = {}


def parse(path):
    s = path.read_text(encoding="utf-8")
    vb = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', s); w, h = float(vb[1]), float(vb[2])
    inner = s[s.index(">", s.index("<svg")) + 1: s.rindex("</svg>")]
    pre = re.sub(r"[^a-z0-9]", "", path.stem.lower())[:24] + str(len(_cache)); _cache[path] = 1
    inner = re.sub(r'\bid="([^"]+)"', lambda m: f'id="{pre}-{m[1]}"', inner)
    inner = re.sub(r'url\(#([^)]+)\)', lambda m: f'url(#{pre}-{m[1]})', inner)
    inner = re.sub(r'(xlink:href|href)="#([^"]+)"', lambda m: f'{m[1]}="#{pre}-{m[2]}"', inner)
    return w, h, inner


def place(folder, stem, x, y, w, h, label=None):
    """Nested copy of an outlined asset, fitted inside the box (x, y, w, h)."""
    p = SRC / folder / f"{stem}.svg"
    if not p.exists(): return ""
    aw, ah, inner = parse(p); sc = min(w / aw, h / ah); dw, dh = aw * sc, ah * sc
    s = f'<svg x="{x + (w - dw) / 2:.1f}" y="{y + (h - dh) / 2:.1f}" width="{dw:.1f}" height="{dh:.1f}" viewBox="0 0 {aw} {ah}">{inner}</svg>'
    if label: s += text(label, x + w / 2, y + h + 22, 14, "Inter-Medium", CI, 0.0, "middle")
    return s


def head(n, title, sub=None):
    s = text(f"{n:02d}", 60, 78, 16, "Montserrat-ExtraBold", CH, 0.1) + f'<rect x="60" y="88" width="46" height="4" fill="{C["yellow"]}"/>'
    s += text(title, 60, 132, 34, "Montserrat-ExtraBold", CH, 0.01)
    if sub: s += text(sub, 60, 164, 15, "Inter-Medium", CI)
    s += stripe(0, PH - 14, PW, 14, 12)
    s += text("Isapur Industrial Park, Brand Book v1.1", 60, PH - 30, 11, "Inter-Medium", CI)
    return s


def lines(items, x, y, size=15, lead=24, font="Inter-Regular", fill=None, wrap=None):
    s = ""
    for i, t in enumerate(items): s += text(t, x, y + i * lead, size, font, fill or CH)
    return s


def artboards():
    A = []
    # 01 cover
    b = sunburst(900, 330, 380, CM) + sunburst(900, 330, 380, "none", C["line"], 3)
    s, h = lockup_vertical(300, 150, 230, uid="cv"); b += s
    b += text("BRAND BOOK", 560, 300, 20, "Montserrat-SemiBold", CH, 0.3) + text("Isapur Industrial Park", 560, 358, 46, "Montserrat-ExtraBold", CH)
    b += text("Version 1.1, 2026-11-06", 560, 394, 16, "Inter-Medium", CI) + text(T1 + "   " + T2, 560, 430, 15, "Inter-Medium", CI)
    b += stripe(0, PH - 40, PW, 40, 36)
    A.append(("cover", b))
    # 02 contents
    secs = ["Brand story", "Logo system", "Monotone and clear space", "Colour and print colours", "Typography", "Voice and taglines", "Icons", "Patterns and sunburst",
            "Signage", "Stationery and applications", "Social media", "Governance and claims"]
    b = head(2, "Contents") + "".join(text(f"{i + 1:02d}", 60 + (i // 6) * 500, 220 + (i % 6) * 62, 18, "Montserrat-ExtraBold", C["red"]) + text(t, 112 + (i // 6) * 500, 220 + (i % 6) * 62, 20, "Inter-Medium", CH) for i, t in enumerate(secs))
    b += text("Pages 3 to 13 are editable artboards. Individual assets follow after the artboards.", 60, 640, 14, "Inter-Medium", CI)
    A.append(("contents", b))
    # 03 story
    b = head(3, "Brand story and positioning")
    b += text("Isapur Industrial Park is a modern industrial address on the Hapur-Modinagar Road", 60, 220, 22, "Montserrat-SemiBold", CH)
    b += text("for local manufacturers who want a clear, legal, well laid plot without noise.", 60, 250, 22, "Montserrat-SemiBold", CH)
    cols = [("NAME", ["Isapur Industrial Park", "Short form IIP", "The developer is not named", "in public material."]),
            ("PROMISE", ["Plots you can verify.", "Facilities we can show.", "One number to call."]),
            ("PERSONALITY", ["Calm, exact, modern,", "trustworthy.", "A planner, not a salesman."]),
            ("AUDIENCE", ["Local factory owners and", "small industrial buyers on", "the Hapur-Modinagar Road."])]
    for i, (t, ls) in enumerate(cols):
        x = 60 + i * 260; b += text(t, x, 340, 13, "Montserrat-SemiBold", C["red"], 0.2) + lines(ls, x, 372, 15, 24)
    b += text("TAGLINES, ADAPTIVE (one per creative, never both)", 60, 540, 13, "Montserrat-SemiBold", C["red"], 0.2)
    b += text(T1, 60, 590, 30, "Montserrat-ExtraBold", CH) + text(T2, 60, 640, 30, "Montserrat-ExtraBold", CH)
    A.append(("story", b))
    # 04 logo system
    b = head(4, "Logo system", "The badge is never changed, recoloured or redrawn.")
    b += place("01_Logo", "logo-primary-vertical", 60, 190, 360, 440, "Primary lockup") + place("01_Logo", "logo-horizontal", 450, 220, 600, 200, "Horizontal lockup")
    b += place("01_Logo", "logo-badge-only", 560, 470, 180, 180, "Badge only")
    A.append(("logo", b))
    # 05 monotone + clear space
    b = head(5, "Monotone use and clear space")
    b += place("01_Logo", "logo-monotone-use", 40, 180, 520, 240) + place("01_Logo", "logo-clear-space-vertical", 580, 170, 500, 250) + place("01_Logo", "logo-clear-space-horizontal", 40, 450, 500, 250) + place("01_Logo", "logo-minimum-size", 580, 450, 500, 250)
    A.append(("space", b))
    # 06 colour
    b = head(6, "Colour and print colours", "Screen hex, RGB and CMYK (US Web Coated SWOP profile). Always approve a printer proof.")
    names = ["white", "charcoal", "yellow", "red", "green", "mist"]
    for i, n in enumerate(names):
        c = PC[n]; x = 60 + i * 170
        b += f'<rect x="{x}" y="200" width="150" height="150" rx="12" fill="{c["hex"]}" stroke="#E5E7EB"/>' + f'<rect x="{x}" y="360" width="150" height="26" rx="6" fill="{c["on_press_hex"]}"/>'
        b += text(n.title(), x, 420, 17, "Montserrat-ExtraBold", CH) + text(c["hex"], x, 446, 14, "Inter-Medium", CH)
        b += text("RGB " + ", ".join(map(str, c["rgb"])), x, 468, 12, "Inter-Regular", CI) + text("CMYK " + " / ".join(map(str, c["cmyk"])), x, 488, 12, "Inter-Regular", CI)
    b += text("Lower chip: approximate look on press.", 60, 520, 12, "Inter-Medium", CI)
    b += text("Badge colours, never retint:  yellow #FEF102   red #EE1D23   green #00A54F", 60, 570, 15, "Inter-Medium", CH)
    b += lines(["Small black text: 100% K only.", "Large dark areas: rich black, for example C60 M50 Y40 K100.", "Deep green is a murky CMYK mix, ask for a spot match.", "White on red is for large text only. Yellow needs charcoal text."], 60, 620, 14, 22)
    A.append(("colour", b))
    # 07 typography
    b = head(7, "Typography")
    b += text("Aa", 60, 300, 140, "Montserrat-ExtraBold", CH) + text("Montserrat", 60, 350, 28, "Montserrat-ExtraBold", CH) + text("Headlines, signage, advertising", 60, 380, 14, "Inter-Medium", CI)
    b += text("ISAPUR Industrial Park", 60, 440, 24, "Montserrat-ExtraBold", CH) + text("ABCDEFGHIJKLMNOPQRSTUVWXYZ 0123456789", 60, 475, 18, "Montserrat-SemiBold", CH)
    b += text("Aa", 600, 300, 140, "Inter-Medium", CH) + text("Inter", 600, 350, 28, "Inter-SemiBold", CH) + text("Subheads, body, digital", 600, 380, 14, "Inter-Medium", CI)
    b += text("Plots from 300 sq.yards", 600, 440, 24, "Inter-Medium", CH) + text("abcdefghijklmnopqrstuvwxyz 0123456789", 600, 475, 18, "Inter-Regular", CH)
    b += text("Both families are free (SIL Open Font License), free for commercial use.", 60, 560, 14, "Inter-Medium", CI)
    A.append(("type", b))
    # 08 voice
    b = head(8, "Voice and taglines")
    b += lines(["Plain English, short sentences, numbers instead of adjectives.", "State what is true and what we can show.", "English only. No superlatives we cannot prove."], 60, 210, 17, 28)
    b += text(T1, 60, 360, 34, "Montserrat-ExtraBold", CH) + text("Identity first: boards, gate, hoarding, letterhead, profile covers.", 60, 392, 14, "Inter-Medium", CI)
    b += text(T2, 60, 470, 34, "Montserrat-ExtraBold", CH) + text("Benefit first: plot offers, infrastructure posts, owner and investor messages.", 60, 502, 14, "Inter-Medium", CI)
    b += text("Choose one line per creative. Never print both together.", 60, 570, 15, "Montserrat-SemiBold", C["red"])
    A.append(("voice", b))
    # 09 icons
    b = head(9, "Icons", "24 line icons, 48 unit grid, 2.4 stroke, round caps and joins.")
    names = sorted(p.stem[5:] for p in (SRC / "03_Icons").glob("icon-*.svg"))
    for i, n in enumerate(names):
        x = 60 + (i % 8) * 128; y = 190 + (i // 8) * 170
        b += place("03_Icons", f"icon-{n}", x, y, 88, 88, n.replace("-", " "))
    A.append(("icons", b))
    # 10 patterns
    b = head(10, "Patterns and sunburst")
    for i, (f, n) in enumerate([("sunburst-outline", "Outline"), ("sunburst-solid-yellow", "Solid"), ("sunburst-ring-border", "Ring"), ("sunburst-repeat-pattern", "Pattern"), ("tri-colour-stripe", "Tri-colour stripe"), ("diagonal-panels", "Diagonal panels")]):
        b += place("02_Pattern", f, 60 + (i % 3) * 340, 190 + (i // 3) * 270, 300, 220, n)
    A.append(("patterns", b))
    # 11 signage
    b = head(11, "Signage", "Pole boards 20 x 32 in, hoardings, gate. Confirm sizes with the media owner.")
    b += place("04_Templates", "sign-pole-20x32in-A", 60, 190, 200, 320, "Pole board A") + place("04_Templates", "sign-pole-20x32in-B", 290, 190, 200, 320, "Pole board B")
    b += place("04_Templates", "sign-hoarding-40x20ft-A", 540, 190, 520, 260, "Hoarding A") + place("04_Templates", "sign-gate-fascia-4to1", 540, 490, 520, 130, "Gate fascia")
    A.append(("signage", b))
    # 12 stationery
    b = head(12, "Stationery and applications")
    for i, (f, n) in enumerate([("card-front-A", "Card A"), ("card-front-B", "Card B"), ("card-back", "Card back"), ("envelope-DL", "Envelope DL"), ("id-card-front", "ID card"), ("letterhead-A4", "Letterhead")]):
        b += place("06_Stationery", f, 60 + (i % 3) * 340, 190 + (i // 3) * 270, 300, 220, n)
    A.append(("stationery", b))
    # 13 social + governance
    b = head(13, "Social media and governance")
    b += place("05_Social", "avatar-badge-1080", 60, 190, 150, 150, "Profile") + place("05_Social", "cover-3to1-1500x500", 240, 200, 380, 126, "Cover 3:1") + place("05_Social", "post-4x5-1080x1350", 660, 180, 160, 200, "Post 4:5") + place("05_Social", "whatsapp-status-1080x1920", 860, 180, 112, 200, "Story 9:16")
    b += lines(["No claim on a board or post without its proof on file.", "Say straight-line or driving when you give a distance.", "Real photos only once they exist. AI assets are phase 3, kept in their own folder.", "Hashtags and content pillars: to be decided in the next phase."], 60, 470, 15, 26)
    b += lines(["Phones: " + " | ".join(CT["phones"]), "Address: " + CT["address"]], 60, 620, 14, 24, "Inter-Medium")
    A.append(("social", b))
    return A


body, y = "", 40
for i, (name, b) in enumerate(artboards(), 1):
    body += (f'<g id="artboard-{i:02d}-{name}"><title>Brand book page {i:02d}: {name}</title><rect x="40" y="{y}" width="{PW}" height="{PH}" fill="#FFFFFF" stroke="#D1D5DB"/>'
             f'<svg x="40" y="{y}" width="{PW}" height="{PH}" viewBox="0 0 {PW} {PH}">{b}</svg></g>')
    y += PH + GAP
TITLES = {"01_Logo": "LOGO SYSTEM", "02_Pattern": "PATTERNS AND SUNBURST", "03_Icons": "ICONS", "04_Templates": "SIGNAGE",
          "05_Social": "SOCIAL MEDIA", "06_Stationery": "STATIONERY AND APPLICATIONS"}
CW, CHH, COLS = 520, 400, 4
y += 40
body += text("INDIVIDUAL ASSETS", 40, y + 30, 40, "Montserrat-ExtraBold", CH, 0.02); y += 100
n = 0
for folder in sorted(p for p in SRC.iterdir() if p.is_dir()):
    files = sorted(folder.glob("*.svg"))
    if not files: continue
    body += text(TITLES.get(folder.name, folder.name.upper()), 40, y + 24, 28, "Montserrat-SemiBold", CH, 0.14)
    body += f'<rect x="40" y="{y + 44}" width="120" height="6" fill="{C["yellow"]}"/><rect x="160" y="{y + 44}" width="60" height="6" fill="{C["red"]}"/><rect x="220" y="{y + 44}" width="60" height="6" fill="{CG}"/>'
    y += 90; col = 0
    for f in files:
        w, h, inner = parse(f); sc = min((CW - 40) / w, (CHH - 90) / h); dw, dh = w * sc, h * sc; x0 = 40 + col * (CW + 40)
        body += (f'<g id="asset-{f.stem}"><title>{f.stem}</title><rect x="{x0}" y="{y}" width="{CW}" height="{CHH}" rx="12" fill="#FFFFFF" stroke="#E5E7EB"/>'
                 f'<svg x="{x0 + (CW - dw) / 2:.1f}" y="{y + 20 + (CHH - 90 - dh) / 2:.1f}" width="{dw:.1f}" height="{dh:.1f}" viewBox="0 0 {w} {h}">{inner}</svg>'
                 + text(f.stem, x0 + CW / 2, y + CHH - 24, 20, "Inter-Medium", CI, 0.0, "middle") + "</g>")
        n += 1; col += 1
        if col == COLS: col = 0; y += CHH + 40
    if col: y += CHH + 40
    y += 40
W = max(PW + 80, 40 * 2 + COLS * CW + (COLS - 1) * 40)
out = svg(W, y + 40, body, f"{W}px", f"{y + 40}px", "ISAPUR Industrial Park master file: brand book and all assets", CM)
(KIT / "IIP-master-assets.svg").write_text(out, encoding="utf-8")
print("master: 13 artboards,", n, "assets,", len(out) // 1024, "KB")
