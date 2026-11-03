p = 'wide.py'
s = open(p, encoding='utf-8').read()
rep = [
 ('font-size:42cqh;font-weight:700;letter-spacing:.02em">ISAPUR', 'font-size:{30 if r<3 else 42}cqh;font-weight:700;letter-spacing:.02em;white-space:nowrap">ISAPUR'),
 ('font-size:{27 if r<3 else 25}cqh;font-weight:600;letter-spacing:.05em">', 'font-size:{17 if r<3 else 25}cqh;font-weight:600;letter-spacing:.05em;white-space:nowrap">'),
 ('font-size:{22 if r<3 else 20}cqh;font-weight:600;color:#FEF102;margin-top:3cqh', 'font-size:{15 if r<3 else 20}cqh;white-space:nowrap;font-weight:600;color:#FEF102;margin-top:3cqh'),
 ('font-size:{36 if r<3 else 31}cqh">', 'font-size:{25 if r<3 else 31}cqh;white-space:nowrap">'),
 ('font-size:{25 if r<3 else 22}cqh;line-height:1.02', 'font-size:{17 if r<3 else 22}cqh;white-space:nowrap;line-height:1.02'),
]
for a, b in rep:
    assert a in s, a
    s = s.replace(a, b)
open(p, 'w', encoding='utf-8').write(s)
