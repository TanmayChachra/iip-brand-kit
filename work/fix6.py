s = open('boards3.py', encoding='utf-8').read()
s = s.replace('line_txt="Room to build."', 'line_txt="A Modern Industrial Address."').replace('line_txt="Plug in. Build up."', 'line_txt="A Modern Industrial Address."')
s = s.replace("font-weight:500;font-size:{6.2 if h>10 else 5.4}cqw\">{t['line_txt']}", "font-weight:500;font-size:{4.6 if h>10 else 4}cqw;white-space:nowrap\">{t['line_txt']}")
s = s.replace("font-size:{10 if r<3 else 11}cqh;white-space:nowrap\">{t['line_txt']}", "font-size:{7.2 if r<3 else 8.5}cqh;white-space:nowrap\">{t['line_txt']}")
open('boards3.py', 'w', encoding='utf-8').write(s)

b = open('build4.py', encoding='utf-8').read()
b = b.replace('line="Room to build."', 'line="A Modern Industrial Address."').replace('line="Plug in. Build up."', 'line="A Modern Industrial Address."')
b = b.replace('"The yellow line echoes the badge and the idea of plugging in to ready infrastructure."', '"The thin yellow line echoes the badge and keeps the board from feeling heavy."')
b = b.replace('("routes.html", "Routes"),', '("routes.html", "Routes"), ("palettes.html", "Palettes"),')
b = b.replace('"Round 3: Quiet', '"Round 4: 14 ChatGPT-web boards in many palettes (new Palettes page). The line Plug in. Build up. is retired; all boards now use A Modern Industrial Address. Round 3: Quiet')
add = '''
PAL = [("quiet-chatgpt-web", "Quiet", "Warm white, black frame, one red rule. Calmest on a crowded road.", "#F7F4EC"),
       ("terracotta", "Terracotta", "Fired-brick red-brown. Warm, earthy, nothing on the road looks like it.", "#B5502F"),
       ("orange", "Safety orange", "Hi-vis and machinery colour. The loudest, seen from furthest.", "#F26B1D"),
       ("claret", "Claret", "Deep wine. Premium like a top developer, dark against green.", "#6E1423"),
       ("petrol", "Petrol", "Dark blue-teal with sand. Calm, industrial, darker than the foliage.", "#0B3C49"),
       ("cocoa", "Cocoa", "Rich brown with a sand phone band. Grounded and trustworthy.", "#3E2A1E"),
       ("cobalt", "Cobalt", "Flat vivid blue with white. Crisp, modern, very legible.", "#1740B8"),
       ("ink2", "Ink", "Charcoal and cream with one thin yellow line. The dark minimal option.", "#121316"),
       ("plum", "Plum", "Aubergine with cream. Distinctive, no one uses it.", "#2E1740"),
       ("mono", "Mono", "Black and white grid with INDUSTRIAL | WAREHOUSING | LOGISTICS.", "#0B0B0B"),
       ("signal", "Signal", "White with a thick yellow band, high visibility.", "#FEF102"),
       ("concrete", "Concrete", "Pale concrete grey, architectural and quiet.", "#C9C9C5"),
       ("blueprint", "Blueprint", "Drawing paper with a faint plot grid and one yellow plot.", "#F5F2EA")]


def palettes():
    cells = "".join(f\'<div class="mood">{img(f"web-{k}.webp", t)}<div class="t"><h3 style="display:flex;gap:8px;align-items:center"><i style="width:18px;height:18px;border-radius:5px;background:{c};border:1px solid rgba(0,0,0,.2);display:inline-block"></i>{t}</h3><p style="margin:0;color:var(--mut);font-size:14px">{d}</p></div></div>\' for k, t, d, c in PAL)
    steps = f\'<figure>{img("web-concept-steps.webp", "Concept route")}<figcaption>Concept route (isolated): Every factory begins with one step.</figcaption></figure>\'
    body = head("Palettes", "Thirteen colour directions, one layout.", "Same logo, same layout, same line, same phone numbers. Only the colour changes, so you can judge colour on its own. These were generated in ChatGPT; the logo is reproduced faithfully but check fine detail before print. The pole mockups here are illustrative, not true to scale; see Boards for scale.") + f"""
<section class="first"><div class="wrap"><div class="grid g2">{cells}</div>
<div class="note" style="margin-top:20px"><b>What the colours need to do:</b> beat green foliage, hazy grey sky, dusty roads and competitor navy, gold and red. Warm earth tones (terracotta, cocoa, claret) feel industrial and trustworthy. Orange and cobalt are the loudest. Petrol and plum are the most distinctive. White and ivory are the calmest.</div></div></section>
<section><div class="wrap"><div class="kick">Isolated route</div>{steps}</div></section>"""
    return shell("palettes.html", "IIP palettes", body)

'''
b = b.replace("\ndef main():", add + "\ndef main():", 1)
b = b.replace('("routes.html", routes()),', '("routes.html", routes()), ("palettes.html", palettes()),')
# assets
b = b.replace('    for n in ("steps", "build", "door"): w(CN', '    for p in sorted((ROOT / "web").glob("iip-r[45]-*.png")):\n        w(p, "web-" + p.stem.replace("iip-r4-", "").replace("iip-r5-", "").replace("-chatgpt-web", "-chatgpt-web") + ".webp", 1500, 82)\n    for n in ("steps", "build", "door"): w(CN')
open('build4.py', 'w', encoding='utf-8').write(b)
