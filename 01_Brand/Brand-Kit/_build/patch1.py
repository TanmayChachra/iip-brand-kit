import pathlib
p = pathlib.Path(__file__).resolve().parent / "build_kit.py"
s = p.read_text(encoding="utf-8")
rep = [
 ("b += hero(0, y0 + 220, W, 760, 150)\n        b += tag3(930, y0 + 90, 88, \"end\")\n        b += proof(500, 1432, 28)",
  "b += hero(0, 660, W, 740, 150)\n        b += tag3(930, y0 + 90, 88, \"end\")\n        b += proof(500, 1446, 28)"),
 ("s, wd = lockup_horizontal(130, 260, 400, uid=\"ho\"); b += s\n    b += f'<rect x=\"{1000 - 4}\" y=\"250\" width=\"6\" height=\"440\"",
  "s, wd = lockup_horizontal(110, 340, 290, uid=\"ho\"); b += s\n    b += f'<rect x=\"{1030 - 4}\" y=\"250\" width=\"6\" height=\"440\""),
 ("b += tag3(1090, 400, 150, \"start\")", "b += tag3(1120, 400, 150, \"start\")"),
 ("b += tag3(540, 840, 110, \"middle\")\n    b += f'<rect x=\"480\" y=\"1250\"", "b += tag3(540, 930, 110, \"middle\")\n    b += f'<rect x=\"480\" y=\"1300\""),
 ("sunburst(100 + 170 * c + (85 if r % 2 else 0), 100 + 150 * r, 80, \"none\", C[\"line\"], 2)", "sunburst(100 + 170 * c + (85 if r % 2 else 0), 100 + 150 * r, 80, \"none\", \"#D1D5DB\", 2)"),
]
for a, b in rep:
    assert a in s, a[:50]
    s = s.replace(a, b)
p.write_text(s, encoding="utf-8")
