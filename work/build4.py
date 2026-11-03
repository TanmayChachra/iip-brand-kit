"""Multipage site (docs/). Quiet and Ink are the live directions. English only. Rebuild with: python work/build4.py"""
import re, shutil, datetime
import build as B
import build2 as B2
import build3 as B3
import content as C

ROOT, DOCS, A = B.ROOT, B.DOCS, B.A
MK, B3D, CN, MOOD = ROOT / "mock4", ROOT / "b3", ROOT / "concept", ROOT / "mood"
w, img, fig = B.webp, B.img, B.fig
PH = "9837057800 | 9219549800"
STAMP = datetime.date.today().strftime("%d %b %Y")

NAV = [("index.html", "Home"), ("process.html", "Process"), ("research.html", "Research"), ("site.html", "Site"), ("routes.html", "Routes"),
       ("kit-quiet.html", "Quiet"), ("kit-ink.html", "Ink"), ("boards.html", "Boards"), ("concept.html", "Concept"), ("decide.html", "Decide")]
KITS = {
 "quiet": dict(name="Quiet", fam="Montserrat", one="Let the badge breathe.", line="Room to build.",
   verdict="Warm white board, thin black frame, the full-colour badge, one red rule. The calmest board on the road.",
   idea=("Every competitor board is crowded: price, stamps, rendered gates, two phone numbers. Quiet does the opposite. About 70 percent of the board is empty on purpose. "
         "That gives the viewer breathing space and makes it the clearest thing on the pole, while the badge's yellow and red carry all the colour."),
   pal=[("Paper", "#F7F4EC", "70%", "Board background"), ("Ink", "#15171A", "20%", "Name, frame"), ("Brand red", "#EE1D23", "2%", "The one rule"), ("Badge colours", "#FEF102", "8%", "Only inside the logo")],
   type=[("Montserrat 800", "ISAPUR"), ("Montserrat 500, +40% tracking", "INDUSTRIAL PARK"), ("Inter 700", PH)],
   risk="White boards show dust first. The black frame stops the board dissolving into hazy sky."),
 "ink": dict(name="Ink", fam="Manrope", one="The one dark board on the road.", line="Plug in. Build up.",
   verdict="Charcoal board, thin cream frame, one yellow line. Premium, strongest at dusk and when lit.",
   idea=("White, navy and gold are everywhere on this road. A charcoal board with a thin cream frame is the only dark one, so it reads at distance and at night. "
         "The yellow line echoes the badge and the idea of plugging in to ready infrastructure."),
   pal=[("Charcoal", "#121316", "70%", "Board background"), ("Cream", "#F4EFE3", "25%", "Text, frame"), ("Sun yellow", "#FEF102", "5%", "The line only (from the logo)")],
   type=[("Manrope 800", "ISAPUR"), ("Manrope 500, +40% tracking", "INDUSTRIAL PARK"), ("Inter 700", PH)],
   risk="Dark boards absorb heat and show chalky dust. Print on UV-stable flex or ACP and proof the badge colours first."),
}
MOODS = B3.MOODS
STATUS = {"r1-quiet": ("kept", "Chosen: becomes the Quiet kit."), "r3-ink": ("kept", "Chosen: becomes the Ink kit."),
          "r2-portal": ("dropped", "Dropped: the red door was not used thoughtfully and read as a bad omen."),
          "r4-heritage": ("parked", "Parked: serif and brass is premium but adds colours and weight."), "r5-mono": ("parked", "Parked: black and white grid. Karyan-style."),
          "r6-owned-colour": ("parked", "Parked: Vodafone-style single colour. The lesson (recognised from afar) is already in Quiet and Ink."),
          "r7-blueprint": ("parked", "Parked: planned-grid idea, but busy."), "r8-editorial": ("route", "Kept separate as the Concept route.")}


def assets():
    if DOCS.exists(): shutil.rmtree(DOCS)
    A.mkdir(parents=True)
    w(ROOT / "logo/iip-master-1x.png", "iip-logo.webp", 700, 92)
    w(ROOT / "src/real-pole-1.jpg", "field-pole-1.webp", 1200, 82)
    w(ROOT / "src/real-pole-stack.jpg", "field-pole-stack.webp", 1200, 82)
    w(ROOT / "gen/map-annotated.png", "map-isapur.webp", 2000, 80)
    for k in KITS:
        for tag in ("clean", "proof"):
            w(B3D / f"{k}-{tag}-20x32.png", f"{k}-{tag}-board.webp", 1000, 84)
            w(MK / f"{k}-{tag}-pole.jpg", f"{k}-{tag}-pole.webp", 1200, 88, crop=(380, 440, 940, 1300))
            w(MK / f"{k}-{tag}-hoarding.jpg", f"{k}-{tag}-hoarding.webp", 1600, 86)
            w(MK / f"{k}-{tag}-row.jpg", f"{k}-{tag}-row.webp", 1448, 86)
            w(B3D / f"{k}-{tag}-hoarding.png", f"{k}-{tag}-art-hoarding.webp", 1400, 84)
        w(MK / f"{k}-gate.jpg", f"{k}-gate.webp", 1086, 86, crop=(0, 120, 1086, 800))
        w(B3D / f"{k}-gate.png", f"{k}-art-gate.webp", 1400, 84)
    for n in ("steps", "build", "door"): w(CN / f"{n}.png", f"c-{n}.webp", 1000, 86)
    w(ROOT / "mock2/concept-steps-hoarding.jpg", "c-steps-hoarding.webp", 1600, 86)
    w(ROOT / "mock2/concept-steps-row.jpg", "c-steps-row.webp", 1448, 86)
    for p in sorted(MOOD.glob("r*.png")):
        if p.stat().st_size > 100000: w(p, f"mood-{p.stem}.webp", 1800, 82)
    for d in ("inspiration-ads", "inspiration-ads2"):
        for p in sorted((ROOT.parent / "References" / d).glob("*")):
            if p.suffix.lower() in (".png", ".webp", ".jpg"): w(p, f"ref-{p.stem}.webp", 900, 78)
    for p in sorted((ROOT.parent / "References" / "iterations-chatgpt").rglob("*.png")):
        w(p, f"iter-{p.parent.name}-{p.stem}.webp".lower(), 1400, 78)


def shell(fname, title, body, extra=""):
    B.NAV[:] = NAV
    html = B.shell(fname, title, body, B3.CSS3 + extra)
    return re.sub(r"<footer>.*?</footer>", f'<footer><div class="wrap"><p>Isapur Industrial Park brand kit. Last updated {STAMP}. Mockups are visualisations: the logo is the supplied artwork, unchanged, and all text on boards is set exactly. Claims such as Section 80 and the Zila Panchayat map approval are as stated by the owner and must be matched to documents before print. Competitor details are read from field photographs and public listings and are not verified. Satellite imagery: Esri, Maxar, Earthstar Geographics.</p></div></footer>', html, flags=re.S)


def head(kick, h1, lead): return f'<header class="wrap" style="padding-top:56px;padding-bottom:24px"><div class="kick">{kick}</div><h1>{h1}</h1><p class="lead">{lead}</p></header>'


def home():
    cards = "".join(f'<a class="kitcard" href="kit-{k}.html">{img(f"{k}-clean-hoarding.webp", K["name"]).replace("zoom", "")}<div class="t"><div class="kick">Direction</div><h3 style="font-size:28px">{K["name"]}</h3><p style="margin:0 0 6px"><b>{K["one"]}</b></p><p style="color:var(--mut);font-size:15px;margin:0">{K["verdict"]}</p></div></a>' for k, K in KITS.items())
    body = head("Isapur Industrial Park · brand kit", "Clear beats loud.", "Two minimal directions chosen from eight territories. White space and one clear message make IIP the board nobody mistakes on the Modinagar road.") + f"""
<section class="first"><div class="wrap"><div class="grid g2">{cards}</div></div></section>
<section><div class="wrap"><div class="kick">Where we are</div><h2>Decisions made so far</h2><div class="grid g3">
<div class="card"><h3>Chosen</h3><p>Quiet and Ink. Minimal, white or dark, still standing out on a crowded road.</p></div>
<div class="card"><h3>Set</h3><p>English only. Phones {PH}. No vector logo yet, so the badge is cleaned from the supplied file.</p></div>
<div class="card"><h3>Pending</h3><p>Whether boards show the proof lines (Section 80, Zila Panchayat map) or stay clean. Both are drawn.</p></div></div>
<p style="margin-top:20px"><a class="pill dk" href="boards.html" style="text-decoration:none;padding:10px 18px">See the boards on the pole</a> <a class="pill" href="process.html" style="text-decoration:none;padding:10px 18px">Process and next steps</a></p></div></section>
<section><div class="wrap"><div class="kick">The situation</div><h2>A crowded road</h2><div class="grid g2"><figure>{img("field-pole-stack.webp", "Competitor stack")}<figcaption>Your photo: three boards on one pole, dense with copy, prices and badges.</figcaption></figure>
<div><p class="lead" style="font-size:19px">Every competitor sells the same way: a rendered gate, a price, an approval stamp, two phone numbers, in navy, gold or red. At 40 km/h only the numbers are readable.</p><p class="lead" style="font-size:19px">A board with almost nothing on it, the badge, the name and the numbers, is recognisable from further away than any of them. That is the whole strategy.</p></div></div></div></section>"""
    return shell("index.html", "IIP brand kit", body)


def process():
    steps = "".join(f'<div class="step {s}"><div class="st">{ {"done":"done","now":"in progress","next":"next"}[s] }</div><div class="n">{n}</div><h3 style="margin:8px 0 4px;font-size:17px">{t}</h3><p style="margin:0;font-size:14px;color:var(--mut)">{d}</p></div>' for n, t, d, s in [
        ("1", "Brief and audit", "Logo, files, photos, what the board decides.", "done"), ("2", "Research", "Kit anatomy, Indian brands, road, satellite, competitors.", "done"),
        ("3", "Strategy", "Recognisable from afar with almost no words.", "done"), ("4", "Territories", "Eight moodboards. Two chosen.", "done"),
        ("5", "Build kits", "Quiet and Ink: logo rules, colour, type, boards, hoarding, gate.", "now"), ("6", "Test in context", "Exact artwork on your real photos at the competitor board size.", "now"),
        ("7", "Guidelines and rollout", "Rules, print specs, phases, budget structure.", "next"), ("8", "Handover", "Print masters, editable files, vendor brief.", "next")])
    log = [("4 Nov", "Round 3: Quiet and Ink only. Boards now match the competitor board size and shape on the pole. English only, real phone numbers, proof-line variants. Site rebuilt as multiple pages."),
           ("4 Nov", "Eight moodboards generated. Doorway, serif, mono, one-colour and editorial parked or dropped."),
           ("3 Nov", "Round 2: minimal kits, concept route, references sorted."), ("2 Nov", "Round 1 (loud colour directions) rejected.")]
    body = head("Process", "How studios do it, and where we are.", "Discover, research, strategise, explore widely, narrow with the client, build, test in context, hand over. Feedback gates sit between rounds.") + f"""
<section class="first"><div class="wrap"><div class="flow">{steps}</div>
<div class="grid g2" style="margin-top:20px"><div class="card"><h3>Next feedback gate</h3><ol><li>Clean boards or proof lines (Section 80, Zila Panchayat map)?</li><li>Quiet or Ink as the main, the other as the night option?</li><li>Which poles first, and how many?</li></ol></div>
<div class="card"><h3>Sources</h3><ul>{"".join(f'<li><a href="{u}" target="_blank" rel="noopener">{t}</a></li>' for t, u in B3.PRO)}</ul></div></div>
<h2 style="margin-top:36px">Change log</h2><div class="card"><table>{"".join(f"<tr><td style='width:90px'><b>{d}</b></td><td>{t}</td></tr>" for d, t in log)}</table></div></div></section>"""
    return shell("process.html", "IIP process", body)


def routes():
    cells = ""
    for k, t, d in MOODS:
        st, why = STATUS[k]
        cells += f'<div class="mood"><div style="position:relative">{img(f"mood-{k}.webp", t)}<span class="pill dk" style="position:absolute;top:10px;left:10px">{st}</span></div><div class="t"><h3>{t}</h3><p style="margin:0 0 4px;color:var(--mut);font-size:14px">{d}</p><p style="margin:0;font-size:14px"><b>{why}</b></p></div></div>'
    refs = [p.stem for d in ("inspiration-ads", "inspiration-ads2") for p in sorted((ROOT.parent / "References" / d).glob("*")) if p.suffix.lower() in (".png", ".webp", ".jpg")]
    gal = "".join(f'<figure>{img(f"ref-{r}.webp", r)}<figcaption>{r.replace("-", " ")}</figcaption></figure>' for r in refs)
    body = head("Routes", "Eight territories, two chosen.", "Each moodboard was a different answer to the same road. They are mood only, not final artwork: the logo may drift slightly in the generated boards.") + f"""
<section class="first"><div class="wrap"><div class="grid g2">{cells}</div></div></section>
<section><div class="wrap"><div class="kick">Inspiration</div><h2>What you shared</h2><p class="lead">Real-estate adverts, Vodafone and Nescafe colour ownership, Emirates and Lufthansa restraint, Karyan, DLF and SG as developer benchmarks. Useful patterns: one colour owned, one clear idea, generous empty space.</p><div class="grid g3 gal" style="margin-top:20px">{gal}</div></div></section>"""
    return shell("routes.html", "IIP routes", body, ".gal figure img{width:100%}")


def kit(k):
    K = KITS[k]
    pal = "".join(f'<div class="sw"><div class="c" style="background:{h};color:{"#14110F" if h in ("#F7F4EC","#FEF102","#F4EFE3") else "#fff"}">{n}</div><div class="m"><b>{h}</b>RGB {B.rgbs(h)}<br>CMYK ~{B.cmyk(h)}<br><span style="color:var(--mut)">{p} · {u}</span></div></div>' for n, h, p, u in K["pal"])
    bar = "".join(f'<div style="flex:{float(p[2].rstrip("%"))};background:{p[1]}"></div>' for p in K["pal"])
    ty = "".join(f'<tr><td><b>{a}</b></td><td style="font-family:{K["fam"]};font-weight:700">{b}</td></tr>' for a, b in K["type"])
    body = head("Direction", K["name"], f'{K["one"]} {K["verdict"]}') + f"""
<section class="first"><div class="wrap">{img(f"{k}-clean-hoarding.webp", K["name"] + " hoarding")}</div></section>
<section><div class="wrap"><div class="kick">1 · Idea</div><h2>Why it works here</h2><p class="lead">{K["idea"]}</p><div class="note" style="margin-top:16px"><b>Risk:</b> {K["risk"]}</div></div></section>
<section><div class="wrap"><div class="kick">2 · Logo</div><h2>The logo, unchanged</h2><div class="grid g3"><div class="card"><img src="assets/iip-logo.webp" style="width:150px" alt="IIP logo"><p style="margin-top:12px"><b>Primary.</b> The full-colour badge, as supplied. No vector exists yet, so print only after the original is found.</p></div>
<div class="card"><div style="position:relative;display:inline-block;margin:6px 0 10px"><img src="assets/iip-logo.webp" style="width:150px" alt=""><div style="position:absolute;inset:-15px;border:1.5px dashed #d4202a"></div></div><p><b>Clear space.</b> At least one tenth of the badge width on every side.</p></div>
<div class="card"><div style="display:flex;gap:14px;align-items:flex-end;margin:10px 0 12px"><img src="assets/iip-logo.webp" style="width:70px" alt=""><img src="assets/iip-logo.webp" style="width:36px" alt=""><img src="assets/iip-logo.webp" style="width:24px" alt=""></div><p><b>Minimum size.</b> 24 px on screen, 18 mm in print. On boards never below 30 percent of the board width.</p></div></div>
<p style="margin-top:14px">Never stretch, recolour, rotate, outline or add shadow to the badge.</p></div></section>
<section><div class="wrap"><div class="kick">3 · Colour and type</div><h2>Palette and typography</h2><div class="grid g4 keep2">{pal}</div><div class="bar" style="margin-top:14px">{bar}</div><p style="font-size:13px;color:var(--mut)">CMYK values are approximate: approve a printed proof.</p>
<div class="card" style="margin-top:16px"><table>{ty}</table><p style="margin:10px 0 0;color:var(--mut)">English only. Line: <b>{K["line"]}</b></p></div></div></section>
<section><div class="wrap"><div class="kick">4 · Boards</div><h2>Pole board, two versions</h2><p class="lead">Same board as the competitor boards on the pole: about 20 x 32 inches, portrait. Clean carries only the phone numbers. Proof adds two legal lines.</p>
<div class="grid g2">{fig(f"{k}-clean-board.webp", "Clean: logo, name, line, phone numbers")}{fig(f"{k}-proof-board.webp", "Proof: adds Section 80 approved and Map passed by Zila Panchayat")}</div>
<p style="margin-top:12px"><a href="boards.html">See them on the real pole next to the competition</a></p></div></section>
<section><div class="wrap"><div class="kick">5 · Site</div><h2>Hoarding and gate</h2><div class="grid g2" style="align-items:center">{fig(f"{k}-clean-hoarding.webp", "Highway hoarding about 2.4:1")}{fig(f"{k}-proof-hoarding.webp", "Hoarding with proof lines")}</div>
<div class="grid g2" style="margin-top:22px;align-items:center">{fig(f"{k}-gate.webp", "Gate fascia about 4:1")}{fig(f"{k}-art-gate.webp", "Gate fascia artwork, flat")}</div></div></section>"""
    return shell(f"kit-{k}.html", f"IIP {K['name']}", body)


def boards():
    sized = ""
    for tag, lab in (("clean", "Clean"), ("proof", "Proof lines")):
        sized += f'<div class="grid g2" style="margin-top:20px">{fig(f"quiet-{tag}-pole.webp", "Quiet, " + lab + ": same width, shape and mounting as the Shri Balaji board above it")}{fig(f"ink-{tag}-pole.webp", "Ink, " + lab + ": same position on the same pole")}</div>'
    body = head("Boards", "On your real pole, at the competitor's size.", "Your own photograph from the Sarawa stretch. The IIP board takes the same width, shape and mounting as the Shri Balaji board directly above it, about 20 x 32 inches by scale from the pole. Earlier 10 inch boards looked like stamps next to it, so they are retired.") + f"""
<section class="first"><div class="wrap"><h2>Clean and proof versions</h2>{sized}
<div class="note" style="margin-top:20px"><b>Recommendation:</b> clean boards on the poles (phone numbers only, maximum space), proof lines on the hoarding and at the gate where there is time to read them. Section 80 and Zila Panchayat claims must match the documents before print.</div></div></section>
<section><div class="wrap"><div class="kick">Street-light poles</div><h2>The rhythm effect</h2><p class="lead">If the park gets lit pole boxes on street lights, the same board repeats down the road, like Vodafone's red banners: recognised from afar.</p>
<div class="grid g2">{fig("quiet-clean-row.webp", "Quiet on every street-light pole")}{fig("ink-clean-row.webp", "Ink on every street-light pole")}</div></div></section>"""
    return shell("boards.html", "IIP boards", body)


def concept():
    refs = "".join(f'<figure>{img(f"ref-{n}.webp", n)}<figcaption>{c}</figcaption></figure>' for n, c in [
        ("markefy-red-stairs-we-build-the-next-step", "Red stairs, one figure."), ("avyukta-building-tomorrow-minimal", "Quiet construction, huge sky."), ("step-into-marketing-text-path", "A figure walking into the message."), ("emirates-minimal-ivory-triptych", "Restraint and ivory.")])
    body = head("Concept route · isolated", "Conceptual adverts.", "A separate route, not part of the brand recommendation, so the kit can be approved without it. Backgrounds are generated; the logo and every word are set exactly. English only.") + f"""
<section class="first"><div class="wrap"><div class="grid g3">{fig("c-steps.webp", "Every factory begins with one step.")}{fig("c-build.webp", "Building India's next factories.")}{fig("c-door.webp", "Step in.")}</div>
<div class="grid g2" style="margin-top:22px;align-items:center">{fig("c-steps-hoarding.webp", "As a hoarding")}{fig("c-steps-row.webp", "On every street-light pole")}</div></div></section>
<section><div class="wrap"><div class="kick">Built from</div><div class="grid g4 keep2">{refs}</div></div></section>"""
    return shell("concept.html", "IIP concept route", body)


def decide():
    S = [("Calm next to crowded boards", 5, 5), ("Not lost in greenery or hazy sky", 3, 5), ("Legible at speed", 4, 5), ("Credible to investors", 5, 5), ("Cheap to print and extend", 5, 4), ("Works on paper and screen", 5, 4), ("Stands out at dusk and night", 2, 5)]
    rows = "".join(f"<tr><td><b>{a}</b></td><td>{b}/5</td><td>{c}/5</td></tr>" for a, b, c in S) + f"<tr><td><b>Total</b></td><td><b>{sum(s[1] for s in S)}/35</b></td><td><b>{sum(s[2] for s in S)}/35</b></td></tr>"
    body = head("Decide", "Quiet by day, Ink by night.", "Both are minimal. Quiet is the safer daytime board. Ink is the one that stands out most and works lit. Our suggestion: Ink as the main pole board, Quiet for the hoarding and paper.") + f"""
<section class="first"><div class="wrap"><div class="card scroll" style="padding:6px 14px"><table><tr><th>Criterion</th><th>Quiet</th><th>Ink</th></tr>{rows}</table></div><p style="color:var(--mut);font-size:14px;margin-top:8px">Our judgement, not measurements.</p></div></section>
<section><div class="wrap"><div class="kick">Rollout</div><h2>Five phases</h2><div class="grid g3">{"".join(f'<div class="card"><h3>{h}</h3><p style="margin:0">{t}</p></div>' for h, t in C.STEPS)}</div></div></section>
<section><div class="wrap"><div class="kick">Budget</div><h2>Three tiers</h2><p class="lead">No rupee figures because none were supplied. Each tier lists its cost drivers.</p><div class="grid g3" style="margin-top:16px">{"".join(f'<div class="card"><div class="kick">{n}</div><h3>{d}</h3><p style="color:var(--mut);margin:0">Cost drivers:<br>{c}</p></div>' for n, d, c in C.TIERS)}</div></div></section>
<section><div class="wrap"><div class="kick">Open items</div><h2>Still needed</h2><div class="card"><ul><li>Clean or proof boards. Documents for Section 80 and the Zila Panchayat map to confirm the exact wording.</li><li>Address line, currently "{C.ADDRESS}" from Google Maps.</li><li>The original logo file, if any exists (CDR, AI, PDF or a print-shop file). If not, we can have the badge redrawn as a vector with your approval.</li><li>Which poles first, and the count.</li><li>Whether the concept route goes to the board.</li></ul></div></div></section>"""
    return shell("decide.html", "IIP decide", body)


def main():
    assets()
    wr = B.write
    for fn, html in [("index.html", home()), ("process.html", process()), ("routes.html", routes()), ("kit-quiet.html", kit("quiet")), ("kit-ink.html", kit("ink")),
                     ("boards.html", boards()), ("concept.html", concept()), ("decide.html", decide())]:
        wr(fn, html)
    B.NAV[:] = NAV
    wr("research.html", shell("research.html", "IIP research", re.search(r"</nav>(.*?)<footer>", B.research_page(), re.S).group(1)))
    wr("site.html", shell("site.html", "IIP site", re.search(r"</nav>(.*?)<footer>", B.site_page(), re.S).group(1)))
    (DOCS / ".nojekyll").write_text("")
    print("ok", sum(f.stat().st_size for f in DOCS.rglob("*") if f.is_file()) // 1024, "KB")


if __name__ == "__main__":
    main()

