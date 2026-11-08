import pathlib
p = pathlib.Path(__file__).resolve().parent / "build_kit.py"
s = p.read_text(encoding="utf-8")
add = '''

def hoarding_wide():
    """40 x 15 ft (8:3), the wide hoarding format."""
    W, H = 2000, 750
    b = sunburst(1780, 400, 430, C["mist"]) + sunburst(1780, 400, 430, "none", C["line"], 4)
    s, wd = lockup_horizontal(90, 215, 260, uid="hw"); b += s
    b += f'<rect x="{1010 - 3}" y="190" width="6" height="330" fill="{C["charcoal"]}" fill-opacity=".25"/>'
    b += tag3(1080, 290, 108, "start")
    b += proof(1000, 560, 34)
    b += phones(1000, 650, 74)
    b += stripe(0, 705, W, 45, 40)
    return svg(W, H, b, "40ft", "15ft", "Hoarding 40 x 15 ft (8:3)", C["white"])
'''
marker = "\n\ndef business_cards():"
assert marker in s
s = s.replace(marker, add + marker, 1)
s = s.replace('put("04_Templates/hoarding-40x20ft", hoarding())', 'put("04_Templates/hoarding-40x20ft", hoarding()); put("04_Templates/hoarding-40x15ft", hoarding_wide())')
p.write_text(s, encoding="utf-8")
