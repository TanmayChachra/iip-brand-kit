"""Round 3: drop the straight-line note, fix duplicate stroke-width (SVG would not open), new bottom labels
(Manufacturing, Power, Highway, Drainage, Street Lights with lamp icon, Planted Greenery).  The legal claim moves to the top grid."""
import re, sys, pathlib
import xml.dom.minidom as md

M = pathlib.Path(sys.argv[1])
s = M.read_text(encoding="utf-8")

# 1. remove the straight-line note
s = re.sub(r'<text id="stat-expressway-note".*?</text>', "", s, flags=re.S)

# 2. duplicate stroke-width on the expressway ground line
def fix_dup(m):
    tag = m.group(0)
    attrs = re.findall(r'\s([\w:-]+)="[^"]*"', tag)
    for name in set(a for a in attrs if attrs.count(a) > 1):
        hits = list(re.finditer(rf'\s{name}="[^"]*"', tag))
        for h in reversed(hits[:-1]):   # keep the last (the intended override)
            tag = tag[:h.start()] + tag[h.end():]
    return tag
s = re.sub(r"<(?:line|path|rect|circle|polygon|polyline)\b[^>]*/>", fix_dup, s)

def tx(i, lines, y=None):
    global s
    t = re.search(r'<text id="feature-%d".*?</text>' % i, s, re.S).group(0)
    n = re.sub(r"<tspan.*</tspan>", "".join(f'<tspan x="0" y="{37*k}">{l}</tspan>' for k, l in enumerate(lines)), t, flags=re.S)
    if y: n = re.sub(r"(matrix\(1 0 0 1 [\d.]+) [\d.]+\)", rf"\1 {y})", n, count=1)
    s = s.replace(t, n)

tx(1, ["Manufacturing", "&amp; Warehousing"], 1755)
tx(2, ["Reliable", "Power Supply"], 1755)
tx(5, ["Street", "Lighting"], 1755)
tx(6, ["Planted", "Greenery"], 1755)

# 3. street lamp icon replaces the shield (slot 5, centre x 1287)
a = s.index('<path d="M1287 1660 L1313 1670')
b = s.index("/>", s.index('<polyline points="1274,1692'))+2
S = 'fill="none" stroke="#101d1a" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"'
lamp = (f'<g id="icon-5-street-light"><path d="M1272 1722V1668C1272 1656 1280 1652 1292 1652H1304" {S}/>'
        f'<path d="M1298 1652H1322L1317 1664H1303Z" {S}/>'
        f'<path d="M1310 1674V1684M1298 1672L1294 1680M1322 1672L1326 1680" {S}/>'
        f'<path d="M1262 1722H1282" {S}/></g>')
s = s[:a] + lamp + s[b:]

md.parseString(s.encode("utf-8"))  # must be well-formed XML
M.write_text(s, encoding="utf-8")
print("ok")
