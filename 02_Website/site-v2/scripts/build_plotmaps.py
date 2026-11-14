"""Optimise the three finished plot maps (01_Brand/Plot-Maps/svg/phase1-3.svg) for inline use on /plot-maps/.
Drops the style block (page CSS owns it), the nali (drain) shapes and legend entry, hover titles (JS tooltip reads data-a),
repeated points, and prefixes group ids. Run: python scripts/build_plotmaps.py"""
import re, pathlib, json
src = pathlib.Path(__file__).resolve().parents[3] / '01_Brand/Plot-Maps/svg'
out = pathlib.Path(__file__).resolve().parents[1] / 'src/assets/plotmaps'
css = re.search(r'<style>(.*?)</style>', (src / 'phase1.svg').read_text('utf8'), re.S).group(1)
(out / 'plotmaps.css').write_text(css.replace('svg{font-family:Inter,\'Helvetica Neue\',Arial,sans-serif}', '.pm svg{font-family:Inter,\'Helvetica Neue\',Arial,sans-serif}'), 'utf8')
def dedupe(m):
    pts = re.findall(r'[MLZ][^MLZ]*', m.group(2)); o = []
    for p in pts:
        if not o or p != o[-1]: o.append(p)
    return m.group(1) + ''.join(o) + m.group(3)
legend = {}
for n in (1, 2, 3):
    s = (src / f'phase{n}.svg').read_text('utf8')
    s = re.sub(r'<style>.*?</style>\s*', '', s, flags=re.S)
    g = re.search(r'<g id="legend">(.*?)</g>', s, re.S).group(1)
    legend[n] = [[a, b, c] for a, b, c in re.findall(r'<rect[^>]*fill="(#\w+)" stroke="(#\w+)"[^>]*/><text[^>]*>([^<]*)</text>', g) if 'Nali' not in c]
    ly = float(re.search(r'<text[^>]*y="([\d.]+)"[^>]*>Legend', g).group(1))
    s = re.sub(r'<g id="legend">.*?</g>\s*', '', s, flags=re.S)
    vb = [float(x) for x in re.search(r'viewBox="([^"]+)"', s).group(1).split()]
    vb[3] = round(ly - 14 - vb[1], 1)
    s = re.sub(r'viewBox="[^"]+"', 'viewBox="' + ' '.join(str(x) for x in vb) + '"', s, 1)
    s = re.sub(r'<g id="nali">.*?</g>\s*', '', s, flags=re.S)
    s = re.sub(r'<rect[^>]*fill="#7A92A8"[^>]*/><text[^>]*>Nali \(drain\)</text>\s*', '', s)
    s = re.sub(r'(<path [^>]*>)<title>([^<]*)</title></path>', lambda m: (m.group(1)[:-1] + (f' data-a="{re.search(r"(\d+) sq yd", m.group(2)).group(1)}"' if re.search(r'(\d+) sq yd', m.group(2)) else '') + '></path>'), s)
    s = re.sub(r'(\sd=")([^"]+)(")', dedupe, s)
    s = re.sub(r' id="(roads|labels|road-labels|north|legend|public-road|phase-\d)"', lambda m: f' id="pm{n}-{m.group(1)}"', s)
    s = s.replace('<svg ', '<svg class="pmsvg" preserveAspectRatio="xMidYMid meet" ', 1).replace(' xmlns="http://www.w3.org/2000/svg"', '')
    s = re.sub(r'\s*\n\s*', '', s)
    (out / f'phase{n}.svg.html').write_text(s, 'utf8')
    print(n, len(s))
(out / 'legend.json').write_text(json.dumps(legend), 'utf8')
