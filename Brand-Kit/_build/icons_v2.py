"""IIP icon set v2: 48 unit grid, drawn for kitlib.icon (stroke 2.6, round caps and joins, fill none).
Only path/rect/circle/line, no fill or stroke attributes. Content sits inside 6..42 so every icon has the same optical size.
Use:  import icons_v2; kitlib.ICONS.update(icons_v2.ICONS_V2)"""
import math


def _acres():
    pts = [(13, 14), (38, 12), (33, 35), (9, 36)]; r = 3.4; d = ""
    for (x1, y1), (x2, y2) in zip(pts, pts[1:] + pts[:1]):       # sides trimmed to the corner circles
        L = math.hypot(x2 - x1, y2 - y1); ux, uy = (x2 - x1) / L, (y2 - y1) / L
        d += f"M{x1 + ux * r:.1f} {y1 + uy * r:.1f}L{x2 - ux * r:.1f} {y2 - uy * r:.1f}"
    return f'<path d="{d}"/>' + "".join(f'<circle cx="{x}" cy="{y}" r="{r}"/>' for x, y in pts)


def _gear():
    n, ro, ri, pts = 8, 18, 14, []
    for i in range(n):
        a = 2 * math.pi * i / n
        for da, r in ((-0.20, ri), (-0.12, ro), (0.12, ro), (0.20, ri)):
            pts.append((24 + r * math.cos(a + da), 24 + r * math.sin(a + da)))
    return '<path d="M' + "L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + 'Z"/><circle cx="24" cy="24" r="6"/>'


ICONS_V2 = {
    # base set, redrawn
    "industrial-plots": '<path d="M6 42V22l11 6v-6l11 6V10h8v32z"/><path d="M13 42v-6h8v6"/>',
    "wide-roads": '<path d="M16 42L21 7M32 42L27 7"/><path d="M24 10v6M24 22v7M24 35v7"/>',
    "power-supply": '<path d="M27 5L11 27h12l-3 16 17-24H25z"/>',
    "water-supply": '<path d="M24 6s-12 13-12 22a12 12 0 0 0 24 0C36 19 24 6 24 6z"/><path d="M18 29a6 6 0 0 0 5 6"/>',
    "connectivity": '<circle cx="24" cy="24" r="5"/><circle cx="9" cy="11" r="3.5"/><circle cx="39" cy="11" r="3.5"/><circle cx="24" cy="41" r="3.5"/><path d="M20.5 20.5L11.5 13.5M27.5 20.5l9-7M24 29v8.5"/>',
    "sustainable": '<path d="M10 38C10 20 20 10 38 10c0 18-10 28-28 28z"/><path d="M12 36L30 18"/>',
    "secure": '<rect x="11" y="21" width="26" height="20" rx="4"/><path d="M16 21v-5a8 8 0 0 1 16 0v5"/><path d="M24 28v6"/>',
    "business-support": '<path d="M10 28v-4a14 14 0 0 1 28 0v4"/><rect x="6" y="27" width="8" height="12" rx="3"/><rect x="34" y="27" width="8" height="12" rx="3"/><path d="M38 39c0 3-4 5-9 5h-3"/>',
    "plug-and-play": '<path d="M18 6v8M30 6v8"/><path d="M12 14h24v8a12 12 0 0 1-24 0z"/><path d="M24 34v8"/>',
    "growth": '<rect x="9" y="32" width="7" height="10" rx="1.5"/><rect x="20.5" y="27" width="7" height="15" rx="1.5"/><rect x="32" y="22" width="7" height="20" rx="1.5"/><path d="M8 24l10-7 7 4 13-11M31 10h7v7"/>',
    # park claims (approved), unchanged
    "expressway": '<rect x="8" y="6" width="32" height="18" rx="3"/><path d="M24 20V10M19 14l5-5 5 5"/><path d="M16 24v16M32 24v16"/><path d="M6 42h36"/>',
    "highway-truck": '<path d="M5 33V15h21v7h7l6 6v5z"/><path d="M31 22v6h8"/><circle cx="14" cy="37" r="4"/><circle cx="32" cy="37" r="4"/><path d="M4 44h40" stroke-dasharray="6 4"/>',
    "drainage": '<path d="M7 28l5 14h24l5-14"/><path d="M13 35c3-3 5 3 9 0s6 3 9 0 4 2 4 0"/><path d="M24 6s-7 8-7 12a7 7 0 0 0 14 0c0-4-7-12-7-12z"/>',
    "street-light": '<path d="M12 42V18c0-6 4-9 10-9h10"/><path d="M28 9h12l-2 6H30z"/><path d="M35 19v4M30 18l-2 4M40 18l2 4"/><path d="M8 42h10"/>',
    "planted-greenery": '<path d="M24 42V27M24 35l-6-6M24 32l6-6"/><path d="M16 31C7 30 6 15 15 14c0-7 14-9 17-2 7-4 14 4 8 10 5 5 0 11-6 9H16z"/>',
    "section-80": '<path d="M24 5l14 6v13c0 9-7 15-14 18-7-3-14-9-14-18V11z"/><path d="M16 24l6 6 10-12"/>',
    # new
    "acres": _acres(),
    "zilla-panchayat": '<path d="M7 18L24 8l17 10z"/><path d="M14 23v13M21 23v13M28 23v13M35 23v13"/><path d="M8 41h32"/>',
    "plot-layers": '<path d="M24 8L42 17 24 26 6 17z"/><path d="M6 25l18 9 18-9"/><path d="M6 33l18 9 18-9"/>',
    "manufacturing": _gear(),
    "warehouse": '<path d="M6 42V18L24 8l18 10v24z"/><path d="M15 42V27h18v15"/><path d="M15 34.5h18"/>',
    "location-pin": '<path d="M24 43S10 30 10 19a14 14 0 0 1 28 0c0 11-14 24-14 24z"/><circle cx="24" cy="19" r="5"/>',
    "phone": '<rect x="14" y="5" width="20" height="38" rx="4"/><path d="M21 10h6"/><path d="M22 38h4"/>',
    "site-visit": '<path d="M14 42V7"/><path d="M14 8h20l-5 7 5 7H14"/><path d="M8 42h20"/>',
}

if __name__ == "__main__":      # contact sheet: python icons_v2.py  -> _icons_v2_sheet.png
    import pathlib
    from playwright.sync_api import sync_playwright
    wrap = lambda s, px: f'<svg viewBox="0 0 48 48" width="{px}" height="{px}" fill="none" stroke="#111827" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round">{s}</svg>'
    cells = "".join(f'<div class="c">{wrap(v, 150)}<small>{k}</small><div class="s">{wrap(v, 28)}</div></div>' for k, v in ICONS_V2.items())
    html = f'<body style="margin:0;background:#fff;font:12px Arial"><style>.g{{display:grid;grid-template-columns:repeat(8,170px);gap:6px;padding:10px}}.c{{text-align:center;border:1px solid #e5e7eb;padding:8px;position:relative}}.c small{{display:block;margin-top:4px;color:#555}}.s{{position:absolute;right:4px;top:4px}}</style><div class="g">{cells}</div>'
    out = pathlib.Path(__file__).with_name("_icons_v2_sheet.png")
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1440, "height": 700}); pg.set_content(html); pg.screenshot(path=str(out), full_page=True); b.close()
    print(len(ICONS_V2), "icons ->", out.name)
