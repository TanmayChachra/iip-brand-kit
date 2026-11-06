"""Extra line icons for the claims shown on the poster (48 grid, same stroke rules as the base set). Additive.
Run: python Brand-Kit/_build/build_icons_extra.py"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import kitlib as K
from kitlib import C, icon, svg

EXTRA = {
    "expressway": '<rect x="8" y="6" width="32" height="18" rx="3"/><path d="M24 20V10M19 14l5-5 5 5"/><path d="M16 24v16M32 24v16"/><path d="M6 42h36"/>',
    "street-light": '<path d="M12 42V18c0-6 4-9 10-9h10"/><path d="M28 9h12l-2 6H30z"/><path d="M35 19v4M30 18l-2 4M40 18l2 4"/><path d="M8 42h10"/>',
    "planted-greenery": '<path d="M24 42V27M24 35l-6-6M24 32l6-6"/><path d="M16 31C7 30 6 15 15 14c0-7 14-9 17-2 7-4 14 4 8 10 5 5 0 11-6 9"/>',
    "drainage": '<path d="M7 28l5 14h24l5-14"/><path d="M13 35c3-3 5 3 9 0s6 3 9 0 4 2 4 0"/><path d="M24 6s-7 8-7 12a7 7 0 0 0 14 0c0-4-7-12-7-12z"/>',
    "section-80": '<path d="M24 5l14 6v13c0 9-7 15-14 18-7-3-14-9-14-18V11z"/><path d="M16 24l6 6 10-12"/>',
    "highway-truck": '<path d="M5 33V15h21v7h7l6 6v5z"/><path d="M31 22v6h8"/><circle cx="14" cy="37" r="4"/><circle cx="32" cy="37" r="4"/><path d="M4 44h40" stroke-dasharray="6 4"/>',
}
K.ICONS.update(EXTRA)
for outline in (False, True):
    K.MODE["outline"] = outline
    sub = "outlined" if outline else "live"
    for n in EXTRA:
        p = K.KIT / sub / f"03_Icons/icon-{n}.svg"
        p.write_text(svg(48, 48, icon(n, 0, 0, 48, C["charcoal"], 2.6), "256px", "256px", n), encoding="utf-8")
print("extra icons", len(EXTRA))
