"""Round 2 site: minimal directions + isolated concept route. Writes ../docs."""
import shutil, html, pathlib
from PIL import Image
import build as B
import content as C

ROOT = B.ROOT; DOCS = B.DOCS; A = B.A
B2, MK, CN = ROOT / "b2", ROOT / "mock2", ROOT / "concept"

KITS = {
 "quiet": dict(name="Quiet", num="01", one="Let the badge breathe.", hi="बनाने की जगह", en="Room to build.",
   verdict="The safest. Warm white paper, one red rule, the full-colour badge. Nothing competes with the logo.",
   idea=("Every competitor board on this road is crowded: price, stamps, rendered gates, two phone numbers. Quiet does the opposite. "
         "A warm white board, a thin black frame, the logo, the name, one red rule and one line. About 70 percent of the board is empty on purpose, "
         "which gives the viewer breathing space and makes the board the calmest thing on the pole. The yellow and red of your badge supply all the colour."),
   pal=[("Paper", "#F7F4EC", "70%", "Board background"), ("Ink", "#15171A", "20%", "Name, frame"), ("Brand Red", "#EE1D23", "2%", "The one rule (taken from the logo)"), ("Badge colours", "#FEF102", "8%", "Only inside the logo")],
   fonts=[("Montserrat", "Name and headline", "800 for ISAPUR, 500 for the line, wide tracking on INDUSTRIAL PARK"), ("Hind", "Hindi pair", "500")],
   lines=["Room to build.", "बनाने की जगह", "A modern industrial address.", "Where industry moves forward."],
   risk="White boards show dust and fade first. The black frame stops it dissolving into hazy sky."),
 "portal": dict(name="Portal", num="02", one="One red doorway. Step in.", hi="अंदर आइए", en="Step in.",
   verdict="Quiet's cousin with one idea added: a red doorway that holds the badge. Memorable, still minimal.",
   idea=("Taken from the Portal element you liked in your own iterations: the entrance as a symbol. The badge sits inside a vermilion arch on warm ivory, the way a gateway frames a view. "
         "The arch is the only graphic device. It repeats on every board, on the gate fascia and as a stamp, so people learn it. It also gives a pole serial: three boards of rising red steps, then the doorway."),
   pal=[("Ivory", "#F4F0E6", "70%", "Background"), ("Ink", "#15171A", "15%", "Text, frame, base line"), ("Vermilion", "#D6311F", "12%", "The doorway only"), ("Badge colours", "#FEF102", "3%", "Only inside the logo")],
   fonts=[("Sora", "Name and line", "700 with wide tracking for ISAPUR, 300 for the line"), ("Hind", "Hindi pair", "500")],
   lines=["Step in.", "अंदर आइए", "Every factory begins with one step.", "A modern industrial address."],
   risk="Vermilion next to the badge's own red needs care: keep the arch large and flat, never gradient."),
 "ink": dict(name="Ink", num="03", one="The quiet board that glows at dusk.", hi="जुड़ें, बनाएँ", en="Plug in. Build up.",
   verdict="Dark and premium. Cream type, a single yellow line. Strongest contrast, works best if boards are lit.",
   idea=("Everyone else uses white or navy. A charcoal board with a thin cream frame is the only dark board on the stretch, so it reads at distance and at night. "
         "The yellow line and dot echo the badge and read as a power line plugging in, which matches the Plug. Build. Scale. thought in your iterations."),
   pal=[("Charcoal", "#121316", "70%", "Background"), ("Cream", "#F4EFE3", "25%", "Text, frame"), ("Sun Yellow", "#FEF102", "5%", "The line and dot (from the logo)")],
   fonts=[("Manrope", "Name and line", "800 for ISAPUR, 400 wide tracking for INDUSTRIAL PARK"), ("Hind", "Hindi pair", "500")],
   lines=["Plug in. Build up.", "जुड़ें, बनाएँ", "A modern industrial address."],
   risk="The badge sits on dark without its own white field, so the yellow rosette must be printed with a crisp edge. Proof it before the run."),
}
SIZES = ["10x10", "10x12", "10x14"]


def prep():
    if DOCS.exists(): shutil.rmtree(DOCS)
    A.mkdir(parents=True)
    w = B.webp
    w(ROOT / "logo/iip-master-1x.png", "iip-logo.webp", 700, 92)
    w(ROOT / "src/real-pole-1.jpg", "field-pole-1.webp", 1200, 82)
    w(ROOT / "src/real-pole-stack.jpg", "field-pole-stack.webp", 1200, 82)
    w(ROOT / "gen/map-annotated.png", "map-isapur.webp", 2000, 80)
    for k in KITS:
        for s in SIZES + ["10x18"]:
            w(B2 / f"{k}-{s}.png", f"{k}-board-{s}.webp", 1000, 84)
        for s in SIZES:
            w(MK / f"{k}-{s}-pole.jpg", f"{k}-pole-{s}.webp", 920, 86, crop=(420, 500, 840, 1130), up=2)
        w(MK / f"{k}-10x14-stack.jpg", f"{k}-stack.webp", 1200, 86)
        w(MK / f"{k}-18x25-pole.jpg", f"{k}-pole-18x25.webp", 920, 86, crop=(420, 500, 840, 1130), up=2)
        w(MK / f"{k}-hoarding.jpg", f"{k}-hoarding.webp", 1600, 86)
        w(MK / f"{k}-gate.jpg", f"{k}-gate.webp", 1086, 86, crop=(0, 120, 1086, 800))
        w(MK / f"{k}-row.jpg", f"{k}-row.webp", 1448, 86)
        w(B2 / f"{k}-hoarding.png", f"{k}-art-hoarding.webp", 1400, 84)
        w(B2 / f"{k}-gate.png", f"{k}-art-gate.webp", 1400, 84)
    w(MK / "portal-serial.jpg", "portal-serial.webp", 1600, 86)
    for n in ("steps", "build", "door"): w(CN / f"{n}.png", f"c-{n}.webp", 1000, 86)
    w(MK / "concept-steps-hoarding.jpg", "c-steps-hoarding.webp", 1600, 86)
    w(MK / "concept-steps-row.jpg", "c-steps-row.webp", 1448, 86)
    w(CN / "steps-hoarding.png", "c-steps-wide.webp", 1600, 84)
    ref = ROOT.parent / "References"
    for p in ref.rglob("*"):
        if p.is_file() and p.suffix.lower() in (".png", ".webp", ".jpg"):
            w(p, "ref-" + p.stem.lower().replace(" ", "-").replace("(", "").replace(")", "") + ".webp", 900, 78)


def img(s, alt): return B.img(s, alt)
fig = B.fig


def kit_page(k):
    K = KITS[k]
    pal = "".join(f'<div class="sw"><div class="c" style="background:{h};color:{"#14110F" if h in ("#F7F4EC","#F4F0E6","#FEF102","#F4EFE3") else "#fff"}">{n}</div>'
                  f'<div class="m"><b>{h}</b>RGB {B.rgbs(h)}<br>CMYK ~{B.cmyk(h)}<br><span style="color:var(--mut)">{p} · {u}</span></div></div>' for n, h, p, u in K["pal"])
    bar = "".join(f'<div style="flex:{float(p[2].rstrip("%"))};background:{p[1]}"></div>' for p in K["pal"])
    fonts = "".join(f'<div class="card"><div class="kick">{u}</div><div style="font-family:\'{f}\',Hind,sans-serif;font-size:42px;line-height:1.1;margin:6px 0 10px;font-weight:700">ISAPUR</div><b>{f}</b><p style="color:var(--mut);margin:4px 0 0">{s}</p></div>' for f, u, s in K["fonts"])
    lines = "".join(f'<tr><td style="font-size:20px"><b>{l}</b></td></tr>' for l in K["lines"])
    sizes = "".join(f'<figure style="width:{150}px">{img(f"{k}-board-{s}.webp", f"{K["name"]} {s}")}<figcaption><b>{s} in</b></figcaption></figure>' for s in SIZES)
    poles = "".join(fig(f"{k}-pole-{s}.webp", f"{s} inch on a pole, under a live competitor board") for s in SIZES)
    serial = ""
    if k == "portal":
        serial = f'<section><div class="wrap"><div class="kick">Option</div><h2>The pole serial</h2><p class="lead">Four poles in a row: three red steps rising, then the doorway. One idea told across 200 metres.</p>{fig("portal-serial.webp", "Poles 1 to 4")}</div></section>'
    body = f"""
<header class="wrap" style="padding-top:56px;padding-bottom:36px"><div class="kick">Direction {K["num"]}</div><h1>{K["name"]}</h1><p class="lead">{K["one"]} {K["verdict"]}</p>
<div style="margin-top:22px">{img(f"{k}-hoarding.webp", f"{K['name']} hoarding")}</div></header>
<section class="first"><div class="wrap"><div class="kick">1 · Idea</div><h2>Why it works here</h2><p class="lead">{K["idea"]}</p>
<div class="note" style="margin-top:18px"><b>Risk:</b> {K["risk"]}</div></div></section>
<section><div class="wrap"><div class="kick">2 · Logo</div><h2>The logo, unchanged</h2><p class="lead">Used exactly as supplied, at 33 to 54 percent of the board width, with generous clear space (at least one tenth of its width). Never recoloured, stretched, rotated or given effects. Please supply the vector master before large print.</p></div></section>
<section><div class="wrap"><div class="kick">3 · Colour and type</div><h2>Palette and typography</h2><div class="grid g4 keep2">{pal}</div><div class="bar" style="margin-top:14px">{bar}</div>
<p style="font-size:13px;color:var(--mut)">Balance of colour. CMYK values are approximate: approve a printed proof.</p>
<div class="grid g2" style="margin-top:20px">{fonts}</div><div class="card" style="margin-top:18px"><h3>Line bank</h3><table>{lines}</table></div></div></section>
<section><div class="wrap"><div class="kick">4 · Pole boards</div><h2>10x10, 10x12, 10x14 inch</h2><div class="sizes">{sizes}</div>
<h3 style="margin:30px 0 10px">On your real poles, next to the competition</h3><div class="grid g3">{poles}</div>
<div class="grid g2" style="margin-top:20px">{fig(f"{k}-stack.webp", "10x14 at the foot of the competitor stack")}{fig(f"{k}-pole-18x25.webp", "Option: same artwork at about 18 x 25 inch")}</div></div></section>
{serial}
<section><div class="wrap"><div class="kick">5 · Street and site</div><h2>Pole row, hoarding, gate</h2>
{fig(f"{k}-row.webp", "The same board on every street-light pole (10x18 proportion, an option for lit pole boxes)")}
<div class="grid g2" style="margin-top:22px;align-items:center">{fig(f"{k}-hoarding.webp", "Highway hoarding about 2.4:1")}{fig(f"{k}-art-hoarding.webp", "Hoarding artwork, flat")}</div>
<div class="grid g2" style="margin-top:22px;align-items:center">{fig(f"{k}-gate.webp", "Gate fascia about 4:1")}{fig(f"{k}-art-gate.webp", "Gate fascia artwork, flat")}</div></div></section>"""
    return B.shell(f"kit-{k}.html", f"IIP {K['name']} direction", body)


def index_page():
    cards = "".join(f'<a class="kitcard" href="kit-{k}.html">{img(f"{k}-row.webp", K["name"]).replace("zoom", "")}<div class="t"><div class="kick">Direction {K["num"]}</div><h3 style="font-size:28px">{K["name"]}</h3><p style="margin:0 0 6px"><b>{K["one"]}</b></p><p style="color:var(--mut);font-size:15px;margin:0">{K["verdict"]}</p></div></a>' for k, K in KITS.items())
    body = f"""<header class="wrap" style="padding-top:60px;padding-bottom:40px"><div class="kick">Board review · Isapur Industrial Park · round 2</div><h1>Quiet boards win on a crowded road.</h1>
<p class="lead">Three minimal directions with space to breathe, built from your own iterations and your logo as it is. The competitors shout; IIP can simply be clear.</p></header>
<section class="first"><div class="wrap"><div class="grid g3">{cards}</div></div></section>
<section><div class="wrap"><div class="kick">The situation</div><h2>A crowded road</h2><div class="grid g2"><figure>{img("field-pole-stack.webp", "Competitor stack")}<figcaption>Your photo: three boards on one pole, dense with copy, prices and badges.</figcaption></figure>
<div><p class="lead" style="font-size:19px">Everything on this road sells the same way: a rendered gate, a price, an approval stamp, two phone numbers, in navy, gold or red. At 40 km/h only the numbers are readable.</p><p class="lead" style="font-size:19px">A board with almost no copy, plenty of empty space and your badge is recognisable from further away than any of them. That is the whole strategy.</p>
<div class="note"><b>Rule for every board:</b> one logo, one name, one line, one number. Details come later, on paper and online.</div></div></div></div></section>
<section><div class="wrap"><div class="kick">Next</div><h2>Compare, then decide</h2><p><a class="pill dk" href="compare.html" style="text-decoration:none;padding:10px 18px">Compare and decide</a> <a class="pill" href="research.html" style="text-decoration:none;padding:10px 18px">Research</a> <a class="pill" href="site.html" style="text-decoration:none;padding:10px 18px">Site and competitors</a></p></div></section>"""
    return B.shell("index.html", "IIP brand kit round 2", body)


def compare_page():
    cols = list(KITS)
    S = [("Calm next to crowded boards", 5, 5, 4), ("Not lost in greenery or hazy sky", 3, 5, 5), ("Legible at speed", 4, 5, 5), ("Memorable on its own", 3, 5, 4),
         ("Credible to investors", 5, 4, 5), ("Cheap to print and extend", 5, 4, 4), ("Works on paper and screen", 5, 4, 4)]
    tot = [sum(r[i + 1] for r in S) for i in range(3)]
    hdr = "".join(f"<th>{KITS[k]['name']}</th>" for k in cols)
    rows = "".join(f"<tr><td><b>{r[0]}</b></td>" + "".join(f"<td>{r[i+1]}/5</td>" for i in range(3)) + "</tr>" for r in S) + "<tr><td><b>Total</b></td>" + "".join(f"<td><b>{t}/35</b></td>" for t in tot) + "</tr>"
    body = f"""<header class="wrap" style="padding-top:56px"><div class="kick">Compare and decide</div><h1>One recommendation: Portal.</h1><p class="lead">Quiet is the safest. Portal is the same calm plus one ownable symbol, which is what makes a minimal brand recognisable. Ink is the premium night option.</p></header>
<section class="first"><div class="wrap"><div class="card scroll" style="padding:6px 14px"><table><tr><th>Criterion</th>{hdr}</tr>{rows}</table></div><p style="color:var(--mut);font-size:14px;margin-top:8px">Scores are our judgement, not measurements.</p>
<div class="grid g3" style="margin-top:24px">{"".join(f'<a class="kitcard" href="kit-{k}.html">{img(f"{k}-pole-10x14.webp", k).replace("zoom","")}</a>' for k in cols)}</div></div></section>
<section><div class="wrap"><div class="kick">Decision 1</div><h2>Pole board size</h2><div class="grid g2"><div><p class="lead" style="font-size:19px">A 10 inch board is about as wide as the pole face. Competitor boards on the same pole are 18 to 30 inches wide. With so much white space the board still stands out, but a larger one stands out more.</p>
<div class="note"><b>Recommendation:</b> 10x14 as the base, and price an 18x25 version for 15 to 20 poles nearest the competitor cluster. Same artwork scales unchanged.</div></div>{fig("portal-pole-18x25.webp", "Portal at about 18 x 25 inch under a competitor board")}</div></div></section>
<section><div class="wrap"><div class="kick">Decision 2</div><h2>Rollout</h2><div class="grid g3">{"".join(f'<div class="card"><h3>{h}</h3><p style="margin:0">{t}</p></div>' for h, t in C.STEPS)}</div></div></section>
<section><div class="wrap"><div class="kick">Decision 3</div><h2>Budget structure</h2><p class="lead">No rupee figures because none were supplied. Each tier lists its cost drivers.</p><div class="grid g3" style="margin-top:18px">{"".join(f'<div class="card"><div class="kick">{n}</div><h3>{d}</h3><p style="color:var(--mut);margin:0">Cost drivers:<br>{c}</p></div>' for n, d, c in C.TIERS)}</div></div></section>
<section><div class="wrap"><div class="kick">Open items</div><h2>What we need from you</h2><div class="card"><ul><li>Direction choice, or a named combination.</li><li>Real phone number (shown as {C.PHONE}) and call or WhatsApp.</li><li>Address line, currently "{C.ADDRESS}" from the Google Maps listing.</li><li>Vector logo (CDR, AI or SVG).</li><li>Claims allowed on boards. They currently carry none.</li><li>Whether the concept route is shown to the family at all.</li></ul></div></div></section>"""
    return B.shell("compare.html", "IIP compare and decide", body)


def concept_page():
    refs = "".join(f'<figure>{img(f"ref-{n}.webp", n)}<figcaption>{c}</figcaption></figure>' for n, c in [
        ("markefy-red-stairs-we-build-the-next-step", "Your reference: red stairs, one figure, tiny against the space."),
        ("avyukta-building-tomorrow-minimal", "Your reference: workers on a frame, a huge calm sky, quiet type."),
        ("vodafone-red-pole-boards-series", "Your reference: one board repeated down a road.")])
    body = f"""<header class="wrap" style="padding-top:56px"><div class="kick">Concept route · isolated</div><h1>Three conceptual adverts.</h1>
<p class="lead">A separate route for the adverts you like. Not part of the main recommendation, so the board can approve the brand kit without these. The photographic backgrounds were generated, but the logo and every word is set exactly, never AI-drawn.</p></header>
<section class="first"><div class="wrap"><div class="grid g3"><figure>{img("c-steps.webp", "Every factory begins with one step")}<figcaption><b>One step.</b> Built from your red-stairs reference. Hindi pair included.</figcaption></figure>
<figure>{img("c-build.webp", "Building India's next factories")}<figcaption><b>Building.</b> Built from the Avyukta workers reference, with hand-written notes.</figcaption></figure>
<figure>{img("c-door.webp", "Step in")}<figcaption><b>Step in.</b> Concrete wall, one door of light, one figure.</figcaption></figure></div></div></section>
<section><div class="wrap"><div class="kick">On the road</div><h2>The steps concept as a hoarding and a pole row</h2><div class="grid g2" style="align-items:center">{fig("c-steps-hoarding.webp", "Highway hoarding")}{fig("c-steps-row.webp", "The same advert on every street-light pole")}</div></div></section>
<section><div class="wrap"><div class="kick">References</div><h2>What these were built from</h2><div class="grid g3">{refs}</div></div></section>"""
    return B.shell("concept.html", "IIP concept adverts", body)


def main():
    B.NAV[:] = [("index.html", "Overview"), ("research.html", "Research"), ("site.html", "Site"), ("kit-quiet.html", "01 Quiet"), ("kit-portal.html", "02 Portal"), ("kit-ink.html", "03 Ink"), ("compare.html", "Compare and decide")]
    prep()
    wr = B.write
    wr("index.html", index_page()); wr("compare.html", compare_page()); wr("concept.html", concept_page())
    for k in KITS: wr(f"kit-{k}.html", kit_page(k))
    wr("research.html", B.research_page()); wr("site.html", B.site_page())
    (DOCS / ".nojekyll").write_text("")
    print("ok", sum(f.stat().st_size for f in DOCS.rglob("*") if f.is_file()) // 1024, "KB")


if __name__ == "__main__":
    main()

