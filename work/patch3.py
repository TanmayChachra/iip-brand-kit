s = open('boards2.py', encoding='utf-8').read()
s = s.replace("}[h]", "}[hh]")
for fn in ("quiet", "portal", "ink"):
    s = s.replace(f"def {fn}(h):\n", f"def {fn}(h):\n    hh = 14 if h > 14 else h\n", 1)
s = s.replace("SIZES = [(10, 10), (10, 12), (10, 14)]", "SIZES = [(10, 10), (10, 12), (10, 14), (10, 18)]")
open('boards2.py', 'w', encoding='utf-8').write(s)
