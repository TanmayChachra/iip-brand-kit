"""Top facts as a 3 x 2 grid.  Row 1 = scale and legitimacy (Acres, Zilla Panchayat, Section 80).
Row 2 = layout and location (50 ft roads, plot size, Delhi-Meerut Expressway).  Everything below moves down by DY and the
canvas grows by DY.  usage: python grid_3x2.py <master.svg>   (run on the one-row version, see _archive/v09)."""
import re, sys, pathlib
import xml.dom.minidom as md

M = pathlib.Path(sys.argv[1]); s = M.read_text(encoding="utf-8")
DY, H0 = 290, 2000
CX = [393.5, 913.5, 1433.5]            # three column centres (page centre 913.5, pitch 520)
DIV = [653.5, 1173.5]

def block(src, start):
    i = src.index(start); depth = 0
    for m in re.finditer(r"<g\b[^>]*>|</g>", src[i:]):
        depth += 1 if m.group(0).startswith("<g") else -1
        if depth == 0: return i, i + m.end()
    raise ValueError(start)

a, b = block(s, '<g id="stats"'); stats = s[a:b]
ia, ib = block(stats, '<g id="stat-icons"')
inner = stats[ia + len('<g id="stat-icons">'): ib - 4]
kids, depth, start = [], 0, None                       # top level children of stat-icons
for m in re.finditer(r"<g\b[^>]*>|</g>", inner):
    if m.group(0).startswith("<g"):
        if depth == 0: start = m.start()
        depth += 1
    else:
        depth -= 1
        if depth == 0: kids.append(inner[start:m.end()])
assert len(kids) == 5, len(kids)
strip = lambda g: g[g.index(">") + 1: g.rindex("</g>")]
ic = {"acres": strip(kids[0]), "zilla": strip(kids[1]), "road": strip(kids[2]), "plots": strip(kids[3]), "expr": strip(kids[4])}
old_cx = {"acres": 322, "zilla": 697, "road": 1086, "plots": 1481, "expr": 1596}   # text centre x each icon was laid out against

texts = {re.search(r"<tspan[^>]*>(.*?)</tspan>", t).group(1): t for t in re.findall(r"<text .*?</text>", stats, re.S)}

def place(t, cx, dy):
    def f(m): return f'transform="matrix(1 0 0 1 {cx} {float(m.group(1)) + dy:g})"'
    return re.sub(r'transform="matrix\(1 0 0 1 [\d.]+ ([\d.]+)\)"', f, t, count=1)

cells = [  # key, column, row, text keys
    ("acres", 0, 0, ["100+", "Acres"]),
    ("zilla", 1, 0, ["Approved by", "Zilla Panchayat"]),
    ("s80",   2, 0, []),
    ("road",  0, 1, ["50 ft. Wide", "RCC Roads"]),
    ("plots", 1, 1, ["Plots Starting from", "300 sq.yards"]),
    ("expr",  2, 1, ["4 km away", "Delhi-Meerut Expressway"]),
]
out_icons, out_text = [], []
S = 'fill="none" stroke="#101d1a" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"'
for key, col, row, tk in cells:
    cx, dy = CX[col], row * DY
    if key == "s80":                                   # shield with tick, scaled to the other icons (stroke 3 x 1.7 = about 5)
        out_icons.append(f'<g id="icon-section80" transform="translate({cx} {887 + dy}) scale(1.7) translate(-1287 -1691)">'
                         f'<path d="M1287 1660 L1313 1670 L1313 1695 C1313 1710 1300 1718 1287 1722 C1274 1718 1260 1710 1260 1695 L1260 1670 Z" {S}/>'
                         f'<polyline points="1274,1692 1284,1702 1302,1682" {S}/></g>')
        out_text.append(f'<text id="stat-section80-value" transform="matrix(1 0 0 1 {cx} {995 + dy})" x="0" y="0" xml:space="preserve" font-family="Montserrat, sans-serif" font-size="40" font-weight="bold" fill="#111111" text-anchor="middle"><tspan x="0" y="0">Section 80</tspan></text>')
        out_text.append(f'<text id="stat-section80-label" transform="matrix(1 0 0 1 {cx} {1028 + dy})" x="0" y="0" xml:space="preserve" font-family="Inter, sans-serif" font-size="25" font-weight="500" fill="#111111" text-anchor="middle"><tspan x="0" y="0">Legally Compliant</tspan></text>')
        continue
    out_icons.append(f'<g transform="translate({cx - old_cx[key]:g} {dy})">{ic[key]}</g>')
    out_text += [place(texts[k], cx, dy) for k in tk]

divs = "".join(f'<line x1="{x}" y1="{885 + r * DY - 40}" x2="{x}" y2="{1062 + r * DY - 40}" fill="#000000" stroke="#dcdcdc" stroke-width="3"/>' for r in (0, 1) for x in DIV)
new = '<g id="stats"><g id="stat-dividers">' + divs + '</g><g id="stat-icons">' + "".join(out_icons) + "</g>" + "".join(out_text) + "</g>"
s = s[:a] + new + s[b:]

for gid in ["hero-photo", "feature-dividers", "feature-icons", "features-text", "decor-leaf-bottom"]:   # push the rest down
    x, y = block(s, f'<g id="{gid}"')
    s = s[:x] + f'<g id="shift-{gid}" transform="translate(0 {DY})">' + s[x:y] + "</g>" + s[y:]
s = s.replace(f'height="{H0}" viewBox="0 0 1827 {H0}"', f'height="{H0 + DY}" viewBox="0 0 1827 {H0 + DY}"', 1)
s = s.replace(f'width="1827" height="{H0}" fill="#ffffff"/>', f'width="1827" height="{H0 + DY}" fill="#ffffff"/>', 1)
md.parseString(s.encode("utf-8"))
M.write_text(s, encoding="utf-8"); print("ok")
