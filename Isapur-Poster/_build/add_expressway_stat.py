"""Top row: add Delhi-Meerut Expressway as the 5th stat (same style as '50 ft. Wide / RCC Roads'), respace the row.
Bottom feature 3 becomes 'Highway / Connectivity'.  Edits 03_Design/01_LATEST_isapur-industrial-park.svg in place
(backup: isapur-industrial-park.before-expressway-stat.svg).  Re-render with render.py pdf."""
import re, shutil, pathlib

M = pathlib.Path(__file__).resolve().parents[1] / "03_Design/01_LATEST_isapur-industrial-park.svg"
shutil.copy(M, M.with_name("_archive/before-expressway-stat.svg"))
s = M.read_text(encoding="utf-8")

# new column centres (old text centre -> new) and dividers, content widths measured from the render
OLD = {322: 168.5, 697: 503.5, 1086: 878.5, 1480.98: 1226, 1481: 1226}
DIV = [293.5, 713.5, 1043.5, 1408.5]
NEW_C = 1596

i = s.index('<g id="stats"')
j = s.index('<g id="hero-photo"') if '<g id="hero-photo"' in s else None
st_end = s.index("</g>", s.index('<g id="stat-icons"'))  # first </g> only closes a nested group, so find real end below
# depth-matched end of stats group
depth, k = 0, i
for m in re.finditer(r"<g\b[^>]*>|</g>", s[i:]):
    depth += 1 if m.group(0).startswith("<g") else -1
    if depth == 0:
        k = i + m.end(); break
stats = s[i:k]

# icons: split into the four existing icons and shift each
ic0 = stats.index('<g id="stat-icons">') + len('<g id="stat-icons">')
depth, ic1 = 1, ic0
for m in re.finditer(r"<g\b[^>]*>|</g>", stats[ic0:]):
    depth += 1 if m.group(0).startswith("<g") else -1
    if depth == 0:
        ic1 = ic0 + m.start(); break
els = re.findall(r"<g>.*?</g>|<(?:polygon|line|path|polyline)\b[^>]*/>", stats[ic0:ic1], re.S)
assert len(els) == 12, len(els)
shifts = [168.5 - 322, 503.5 - 697, 878.5 - 1086, 1226 - 1481]
groups = [els[0:2], els[2:7], els[7:10], els[10:12]]
icons = "".join(f'<g transform="translate({dx:.1f} 0)">' + "".join(g) + "</g>" for dx, g in zip(shifts, groups))
DK = '#101d1a'; S = f'fill="none" stroke="{DK}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"'
c = NEW_C  # expressway icon: gantry sign with up arrow on two posts, ground line
icons += (f'<g id="icon-expressway"><rect x="{c-56}" y="832" width="112" height="56" rx="8" {S}/>'
          f'<path d="M{c} 876V846M{c-12} 858L{c} 846L{c+12} 858" {S}/>'
          f'<path d="M{c-30} 888V938M{c+30} 888V938" {S}/>'
          f'<line x1="{c-66}" y1="942" x2="{c+66}" y2="942" {S} stroke-width="8"/></g>')

divs = "".join(f'<line x1="{x}" y1="885" x2="{x}" y2="1062" fill="#000000" stroke="#dcdcdc" stroke-width="3"/>' for x in DIV)

# texts: move x of the four existing columns
def mv(m):
    x = float(m.group(1)); return f'transform="matrix(1 0 0 1 {OLD[x]} {m.group(2)})"'
body = stats[ic1:]
body = body[body.index("</g>") + 4:] if body.lstrip().startswith("</g>") else body
texts = re.findall(r"<text .*?</text>", stats, re.S)
texts = [re.sub(r'transform="matrix\(1 0 0 1 ([\d.]+) ([\d.]+)\)"', mv, t) for t in texts]
new_t = (f'<text id="stat-expressway-value" transform="matrix(1 0 0 1 {c} 995)" x="0" y="0" xml:space="preserve" font-family="Montserrat, sans-serif" font-size="40" font-weight="bold" fill="#111111" text-anchor="middle"><tspan x="0" y="0">4 km away</tspan></text>'
         f'<text id="stat-expressway-label" transform="matrix(1 0 0 1 {c} 1028)" x="0" y="0" xml:space="preserve" font-family="Inter, sans-serif" font-size="25" font-weight="500" fill="#111111" text-anchor="middle"><tspan x="0" y="0">Delhi-Meerut Expressway</tspan></text>')
new_stats = ('<g id="stats" transform="translate(-14 0)"><g id="stat-dividers">' + divs + '</g><g id="stat-icons">' + icons + '</g>' + "".join(texts) + new_t + '</g>')
s = s[:i] + new_stats + s[k:]

# bottom feature 3
t3 = re.search(r'<text id="feature-3" transform="matrix\(1 0 0 1 791 1752\)".*?</text>', s, re.S).group(0)
n3 = re.sub(r"<tspan.*</tspan>", '<tspan x="0" y="0">Highway</tspan><tspan x="0" y="37">Connectivity</tspan>', t3, flags=re.S).replace("791 1752", "791 1755")
s = s.replace(t3, n3)
M.write_text(s, encoding="utf-8")
print("ok")
