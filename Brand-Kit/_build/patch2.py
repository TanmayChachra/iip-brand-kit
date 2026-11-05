import pathlib
p = pathlib.Path(__file__).resolve().parent / "build_kit.py"
s = p.read_text(encoding="utf-8")
rep = [
 ('lockup_horizontal(110, 340, 290, uid="ho")', 'lockup_horizontal(90, 330, 330, uid="ho")'),
 ('x="{1030 - 4}" y="250" width="6" height="440"', 'x="{1070 - 4}" y="270" width="6" height="440"'),
 ('b += tag3(1120, 400, 150, "start")', 'b += tag3(1150, 400, 124, "start")'),
]
for a, b in rep:
    assert a in s, a
    s = s.replace(a, b)
p.write_text(s, encoding="utf-8")
