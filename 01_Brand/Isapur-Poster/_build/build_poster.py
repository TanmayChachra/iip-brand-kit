import base64, io, sys
from PIL import Image
SRC, LOGO, OUT = sys.argv[1], sys.argv[2], sys.argv[3]   # reference webp (photo crop), logo svg, output svg
import re
im = Image.open(SRC).convert("RGB")
def b64(box):
    buf = io.BytesIO(); im.crop(box).save(buf, "WEBP", quality=80)
    return base64.b64encode(buf.getvalue()).decode()
logo_inner = re.sub(r"^<svg[^>]*>|</svg>$", "", open(LOGO, encoding="utf-8").read().strip()); photo = b64((8, 1105, 1820, 1635))

DK = "#101d1a"
S = f'fill="none" stroke="{DK}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"'
HEAD = "Montserrat"   # headings, no fallback
SUB = "Inter"         # sub heads, no fallback
def t(x, y, s, size, w=400, fill="#111", anchor="middle", extra="", id=None, fam=None):
    i = f' id="{id}"' if id else ""
    fam = fam or (HEAD if w >= 700 else SUB)
    return f'<text{i} font-family="{fam}" x="{x}" y="{y}" font-size="{size}" font-weight="{w}" fill="{fill}" text-anchor="{anchor}" {extra}>{s}</text>'
feat = [(273, ["Ideal for", "Manufacturing", "&amp; Warehousing"], 1747),
        (538, ["Reliable", "Power Supply"], 1755), (791, ["Assured", "Water Supply"], 1752),
        (1052, ["High-Speed", "Connectivity"], 1755), (1287, ["Legally", "Compliant"], 1757),
        (1557, ["Sustainable", "Development"], 1760)]
feat_svg = ""
for n, (cx, lines, y0) in enumerate(feat):
    feat_svg += f'<text id="feature-{n+1}" x="{cx}" font-size="27" fill="#666" text-anchor="middle">' + "".join(
        f'<tspan x="{cx}" y="{y0 + i*37}">{l}</tspan>' for i, l in enumerate(lines)) + "</text>\n"

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="1827" height="2000" viewBox="0 0 1827 2000" font-family="{SUB}">
<rect id="background" width="1827" height="2000" fill="#fdfdfd"/>
<g id="decor-leaves" fill="#ededed">
<path d="M1395 48C1560 100 1700 200 1760 300C1800 360 1810 380 1818 402C1730 400 1600 330 1530 240C1470 160 1420 100 1395 48Z"/>
<path d="M1462 292C1520 262 1620 235 1730 262C1700 300 1640 340 1560 330C1510 322 1480 308 1462 292Z"/>
<path d="M135 1800C100 1860 40 1920 12 1985C60 1960 110 1900 135 1800Z"/>
<path d="M10 1990C70 1930 160 1900 215 1905C190 1950 100 1985 10 1990Z"/>
</g>
<g id="logo" transform="translate(730 75) scale(0.296)">{logo_inner}</g>
{t(943, 618, "ISAPUR", 204, 800, "#151515", extra='letter-spacing="1"', id="title")}
<g id="subtitle-rules" stroke="#d9161c" stroke-width="6" stroke-linecap="round"><path d="M436 687H577"/><path d="M1235 687H1376"/></g>
{t(916, 706, "INDUSTRIAL PARK", 52, 700, "#151515", extra='letter-spacing="5.5"', id="subtitle")}
<g id="stats">
<g id="stat-dividers" stroke="#dcdcdc" stroke-width="3"><path d="M498 885V1062"/><path d="M887 885V1062"/><path d="M1282 885V1062"/></g>
<g id="stat-icons" {S}>
 <path d="M305 855L407 857L371 933L270 934Z"/>
 <g fill="#fdfdfd"><circle cx="305" cy="855" r="8"/><circle cx="407" cy="857" r="8"/><circle cx="371" cy="933" r="8"/><circle cx="270" cy="934" r="8"/></g>
 <path d="M625 852L693 826L762 852Z"/><path d="M634 862H752"/><path d="M646 868V924M668 868V924M690 868V924M712 868V924M734 868V924" stroke-width="7"/><path d="M638 926H750"/><path d="M624 937H762" stroke-width="8"/>
 <path d="M1060 832L1018 942"/><path d="M1108 832L1150 942"/><path d="M1084 832V855M1084 872V895M1084 912V942"/>
 <path d="M1480 838L1548 872L1480 905L1413 872Z"/><path d="M1413 897L1480 933L1548 897"/>
</g>
{t(322, 995, "100+", 40, 700)}{t(322, 1025, "Acres", 25, 500)}
{t(687, 986, "Approved by", 25, 500)}{t(697, 1030, "Zilla Panchayat", 40, 700)}
{t(1086, 995, "50 ft. Wide", 40, 700)}{t(1095, 1028, "RCC Roads", 25, 500)}
{t(1490, 975, "Plots Starting from", 25, 500)}{t(1481, 1015, "300 sq.yards", 40, 700)}
</g>
<image id="hero-photo" x="8" y="1105" width="1812" height="530" href="data:image/webp;base64,{photo}"/>
<g id="feature-dividers" stroke="#d6d6d6" stroke-width="3"><path d="M415 1660V1780"/><path d="M664 1660V1780"/><path d="M912 1660V1780"/><path d="M1173 1660V1780"/><path d="M1407 1660V1780"/></g>
<g id="feature-icons" {S}>
 <path d="M242 1703V1675L262 1690V1675L282 1690V1650H303V1703Z"/>
 <path d="M550 1650L522 1682H543L528 1706L558 1672H538Z"/>
 <path d="M790 1650C790 1650 770 1680 770 1690A20 20 0 0 0 810 1690C810 1680 790 1650 790 1650Z"/>
 <path d="M1015 1668Q1045 1645 1075 1668M1025 1680Q1045 1664 1065 1680M1035 1690Q1045 1682 1055 1690"/><circle cx="1045" cy="1697" r="4" fill="{DK}"/>
 <path d="M1287 1660L1313 1670V1695C1313 1710 1300 1718 1287 1722C1274 1718 1260 1710 1260 1695V1670Z"/><path d="M1274 1692L1284 1702L1302 1682"/>
 <path d="M1549 1712V1690"/><path d="M1549 1690C1549 1670 1530 1665 1518 1668C1518 1685 1532 1692 1549 1690Z"/><path d="M1549 1685C1549 1668 1565 1658 1582 1662C1582 1680 1568 1688 1549 1685Z"/>
</g>
<g id="features-text" font-family="{SUB}">
{feat_svg}</g>
<g id="cta">
<g stroke="#d9161c" stroke-width="6" stroke-linecap="round"><path d="M373 1890H516"/><path d="M1119 1884H1264"/></g>
<circle cx="624" cy="1892" r="45" fill="#0b2e2a"/>
<path transform="translate(595 1863) scale(2.4)" fill="#fff" d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/>
{t(698, 1910, "9837057800", 58, 800, "#111", "start", '', id="phone")}
</g>
<g id="corner-stripes"><path fill="#f9dc16" d="M1480 1990L1632 1828H1698L1566 1990Z"/><path fill="#e3131b" d="M1586 1990L1702 1828H1770L1650 1990Z"/><path fill="#0b4d3a" d="M1668 1990L1776 1828H1820V1990Z"/></g>
</svg>'''
open(OUT, "w", encoding="utf-8").write(svg)
print(len(svg))
