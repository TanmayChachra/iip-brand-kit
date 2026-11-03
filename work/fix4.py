s = open('boards3.py', encoding='utf-8').read()
s = s.replace('lw = {10: (24 if proof else 30), 12: (34 if proof else 40), 14: (42 if proof else 48), 18: 54}[h]', 'lw = {10: (24 if proof else 30), 12: (34 if proof else 40), 14: (42 if proof else 48), 16: (44 if proof else 50), 18: 54}[h]')
s = s.replace('big = {10: 10.5, 12: 11.5, 14: 12.5, 18: 13}[h]', 'big = {10: 10.5, 12: 11.5, 14: 12.5, 16: 14, 18: 14}[h]')
s = s.replace('ph = {10: 5.2, 12: 5.8, 14: 6.4, 18: 7}[h]', 'ph = {10: 5.2, 12: 5.8, 14: 6.4, 16: 7, 18: 7}[h]')
s = s.replace('pr = {10: 3.1, 12: 3.4, 14: 3.7, 18: 4}[h]', 'pr = {10: 3.1, 12: 3.4, 14: 3.7, 16: 4, 18: 4}[h]')
s = s.replace('for h in (10, 12, 14, 18):', 'for h in (16, 18):')
s = s.replace('B.shot(br, pole(k, h, proof), 1000, h * 100, OUT / f"{k}-{tag}-10x{h}.png", 3)', 'B.shot(br, pole(k, h, proof), 1000, h * 100, OUT / f"{k}-{tag}-20x{h * 2}.png", 2)')
open('boards3.py', 'w', encoding='utf-8').write(s)

m = open('mock4.py', encoding='utf-8').read()
a = m.index('    for k in ("quiet", "ink"):')
b = m.index('            W.composite(ROOT / "gen/scene-hoarding-a.png"')
new = '''    for k in ("quiet", "ink"):
        for tag in ("clean", "proof"):
            art = Image.open(B3 / f"{k}-{tag}-20x32.png")
            # same width, shape and mounting as the Shri Balaji board directly above (190 x 307 px in the photo)
            on_pole(pole1, art, 650, 846, 190, 304).save(OUT / f"{k}-{tag}-pole.jpg", quality=92)
            on_pole(stack, art, 652, 1338, 172, 275).save(OUT / f"{k}-{tag}-stack.jpg", quality=92)
'''
m = m[:a] + new + m[b:]
m = m.replace('B3 / f"{k}-{tag}-10x18.png"', 'B3 / f"{k}-{tag}-20x36.png"')
open('mock4.py', 'w', encoding='utf-8').write(m)
