"""1) Replace the pixel-stepped halo polygon and the separate dark outline with ONE continuous smooth stroke (the 22-point
die-cut star, fitted to the measured tips and valleys of the supplied logo).  2) Update feature icons and labels for the
new text (Highway connectivity, Drainage).  Edits 03_Design/01_LATEST_isapur-industrial-park.svg and 02_Logo/iip-logo.svg in place;
originals are kept as *.before-*.svg."""
import re, math, pathlib, numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[1]
MASTER = ROOT / "03_Design/01_LATEST_isapur-industrial-park.svg"
LOGO = ROOT / "02_Logo/iip-logo.svg"
cx, cy, R, r, a0 = np.load(pathlib.Path(__file__).resolve().parent / "_star.npy")
N = 22


def star_pts():
    pts = []
    for i in range(N * 2):
        ang = a0 + math.pi * i / N
        rad = R if i % 2 == 0 else r
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    return pts


def block(s, start_tag):
    """Return (start, end) of the <g ...> element beginning at start_tag, depth matched."""
    i = s.index(start_tag); depth = 0
    for m in re.finditer(r"<g\b[^>]*>|</g>", s[i:]):
        depth += 1 if m.group(0).startswith("<g") else -1
        if depth == 0: return i, i + m.end()
    raise ValueError(start_tag)


def nums(txt): return [float(x) for x in re.findall(r"-?\d+\.?\d*", txt)]


# ---- source logo px -> master page px, fitted to the yellow and red layers (k=0.2974, measured) ----
lg = LOGO.read_text(encoding="utf-8")
ms = MASTER.read_text(encoding="utf-8")
bs, be = block(ms, '<g id="logo-halo"')
k, tx, ty = 0.29738, 729.22, 74.56

pts = star_pts()
path_src = "M" + " L".join(f"{x:.2f} {y:.2f}" for x, y in pts) + "Z"
path_master = "M" + " L".join(f"{x * k + tx:.2f} {y * k + ty:.2f}" for x, y in pts) + "Z"
STROKE = '#CFCFCF'

# ---- master ----
new_halo = (f'<g id="logo-halo-outline"><title>Die-cut outline: one continuous stroke</title>'
            f'<path id="halo" d="{path_master}" fill="#FFFFFF" stroke="{STROKE}" stroke-width="1.1" stroke-linejoin="miter" stroke-miterlimit="6"/></g>')
ms = ms[:bs] + new_halo + ms[be:]
os_, oe = block(ms, '<g id="outline"'); ms = ms[:os_] + ms[oe:]          # separate dark outline removed

# icons: highway connectivity (truck on the road) and drainage (open channel with flow)
DK = "#101d1a"; S = f'fill="none" stroke="{DK}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"'
truck = (f'<path id="icon-highway" d="M758 1686V1658H795V1668H809L821 1680V1686Z" {S}/>'
         f'<path d="M802 1673V1680H814" {S}/>'
         f'<circle cx="773" cy="1694" r="7" {S} fill="#fdfdfd"/><circle cx="807" cy="1694" r="7" {S} fill="#fdfdfd"/>'
         f'<path d="M752 1708H830" {S} stroke-dasharray="14 10"/>')
drain = (f'<path id="icon-drainage" d="M1018 1684L1030 1710H1074L1086 1684" {S}/>'
         f'<path d="M1031 1698C1037 1691 1044 1705 1052 1698C1060 1691 1067 1705 1073 1698" {S}/>'
         f'<path d="M1052 1648C1052 1648 1042 1660 1042 1665A10 10 0 0 0 1062 1665C1062 1660 1052 1648 1052 1648Z" {S}/>')
fs, fe = block(ms, '<g id="feature-icons"')
fi = ms[fs:fe]
# drop the old water drop (path with C790 1650) and the wifi arcs + dot
fi = re.sub(r'\s*<path d="M790 1650[^>]*/>', "", fi)
fi = re.sub(r'\s*<path d="M1015 1668[^>]*/>', "", fi)
fi = re.sub(r'\s*<circle cx="1045" cy="1697"[^>]*/>', "", fi)
fi = fi.replace("</g>", "<g id=\"icon-3-highway\">" + truck + "</g><g id=\"icon-4-drainage\">" + drain + "</g></g>", 1) if fi.count("</g>") == 1 else fi.rstrip()[:-4] + "<g id=\"icon-3-highway\">" + truck + "</g><g id=\"icon-4-drainage\">" + drain + "</g></g>"
ms = ms[:fs] + fi + ms[fe:]

# labels: consistent Title Case, stray split removed
t3 = re.search(r'<text id="feature-3".*?</text>', ms, re.S).group(0)
n3 = re.sub(r"<tspan.*</tspan>", '<tspan x="0" y="0">Highway</tspan><tspan x="0" y="37">Connectivity</tspan>', t3, flags=re.S).replace('x="3.797"', 'x="0"')
ms = ms.replace(t3, n3)
MASTER.write_text(ms, encoding="utf-8")

# ---- standalone logo ----
hs, he = block(lg, '<g id="halo"')
lg = lg[:hs] + (f'<g id="halo"><title>Die-cut outline: one continuous stroke</title><path d="{path_src}" fill="#FFFFFF" stroke="{STROKE}" stroke-width="3" stroke-linejoin="miter" stroke-miterlimit="6"/></g>') + lg[he:]
try:
    os2, oe2 = block(lg, '<g id="outline"'); lg = lg[:os2] + lg[oe2:]
except ValueError:
    pass
LOGO.write_text(lg, encoding="utf-8")
print("done")
