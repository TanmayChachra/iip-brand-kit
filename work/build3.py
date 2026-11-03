"""Single living page: docs/index.html. Re-run after any change, then commit and push."""
import pathlib, shutil, html
from PIL import Image
import build as B
import build2 as B2
import content as C

ROOT, DOCS, A = B.ROOT, B.DOCS, B.A
MOOD = ROOT / "mood"
w = B.webp

MOODS = [("r1-quiet", "1 · Quiet paper", "Maximum white space. One red rule. The calmest board on a loud road."),
         ("r2-portal", "2 · Portal doorway", "The badge inside a vermilion arch. One ownable shape."),
         ("r3-ink", "3 · Ink night", "The only dark board. Cream type, one yellow power line."),
         ("r4-heritage", "4 · Institutional serif", "DLF-style trust. Stone, brass, serif."),
         ("r5-mono", "5 · Monochrome grid", "Karyan-style black and white. The yellow badge is the only colour."),
         ("r6-owned-colour", "6 · One colour owned", "Vodafone-style. Recognisable from far away by colour alone."),
         ("r7-blueprint", "7 · Blueprint plot grid", "The park as a planned grid. Technical, honest, ready to build."),
         ("r8-editorial", "8 · Editorial concept", "Your conceptual adverts as a separate premium layer.")]

STEPS = [
 ("1", "Brief and audit", "Logo, existing assets, what the board must decide. We read your files, photos and iterations.", "done"),
 ("2", "Research", "How kits are built, rooted Indian brands, the road, the satellite view, every competitor board.", "done"),
 ("3", "Strategy", "One rule: be recognisable from afar with almost no words. Own a shape or colour nobody on the road owns.", "done"),
 ("4", "Territories", "Eight different routes as moodboards, from calm white to editorial. Volume first, then narrow.", "now"),
 ("5", "Narrow and build kits", "You pick two or three routes. Each becomes a full kit: logo rules, colour, type, boards, hoarding, gate, paper.", "next"),
 ("6", "Test in context", "Exact artwork on your real photos at true scale, next to live competitor boards.", "next"),
 ("7", "Guidelines and rollout", "One-page rules, print specs, phases, budget structure, open items.", "next"),
 ("8", "Handover", "Print masters at 300 dpi, editable files, a PDF on request, vendor brief.", "next")]
GATES = ["After step 4: which 2 or 3 territories do you want developed, and what do you hate in the others?",
         "After step 5: does the kit feel right to your dad and the board? Anything to simplify?",
         "After step 6: which size and which poles first? Which phone number and address line go on boards?"]
PRO = [("Canny Creative: 10-step branding process", "https://www.canny-creative.com/blog/branding-process-successful-business-branding/"),
       ("JUST Creative: brand strategy and design process", "https://justcreative.com/brand-strategy-design-process/"),
       ("Brandy HQ: step-by-step agency guide", "https://www.brandyhq.com/blog/building-a-startup-branding-agency-a-step-by-step-guide"),
       ("Prose Media: discovery to delivery", "https://www.prosemedia.com/vertical-tab-groups/our-branding-process-from-discovery-to-delivery")]

CSS3 = """
.flow{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;counter-reset:s}
@media(max-width:860px){.flow{grid-template-columns:1fr 1fr}}
.step{position:relative;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px}
.step .n{font:900 28px 'Archivo';line-height:1}.step.done{border-color:#2f7d4f}.step.done .n{color:#2f7d4f}
.step.now{border:2px solid var(--ink)}.step.now .n{color:#d6311f}.step .st{position:absolute;top:12px;right:12px;font:700 10px 'Archivo';letter-spacing:.1em;text-transform:uppercase;color:var(--mut)}
.mood{background:var(--card);border:1px solid var(--line);border-radius:14px;overflow:hidden}.mood .t{padding:14px 16px}.mood h3{font-size:18px;margin:0 0 4px}
details{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px 18px;margin-top:14px}summary{cursor:pointer;font:800 18px 'Archivo'}
"""


def prep_extra():
    for p in sorted(MOOD.glob("r*.png")):
        if p.stat().st_size > 100000: w(p, f"mood-{p.stem}.webp", 1800, 82)
    for k in ("jamun", "gulaal", "kora"):
        if (ROOT / f"mock/{k}-hoarding.jpg").exists():
            w(ROOT / f"mock/{k}-hoarding.jpg", f"r1-{k}-hoarding.webp", 1200, 80)
            w(ROOT / f"mock/{k}-10x14-pole.jpg", f"r1-{k}-pole.webp", 920, 84, crop=(420, 500, 840, 1130), up=2)


def page():
    img, fig = B.img, B.fig
    steps = "".join(f'<div class="step {s}"><div class="st">{ {"done":"done","now":"in progress","next":"next"}[s] }</div><div class="n">{n}</div><h3 style="margin:8px 0 4px;font-size:17px">{t}</h3><p style="margin:0;font-size:14px;color:var(--mut)">{d}</p></div>' for n, t, d, s in STEPS)
    gates = "".join(f"<li>{g}</li>" for g in GATES)
    pro = "".join(f'<li><a href="{u}" target="_blank" rel="noopener">{t}</a></li>' for t, u in PRO)
    have = {p.stem: p for p in MOOD.glob("r*.png") if p.stat().st_size > 100000}
    moods = "".join(f'<div class="mood">{img(f"mood-{k}.webp", t) if k in have else "<div style=padding:40px;color:var(--mut)>generating</div>"}<div class="t"><h3>{t}</h3><p style="margin:0;color:var(--mut);font-size:14px">{d}</p></div></div>' for k, t, d in MOODS)
    # round 2 directions
    k2 = ""
    for k, K in B2.KITS.items():
        k2 += (f'<div class="card"><div class="kick">Direction {K["num"]}</div><h3>{K["name"]}</h3><p><b>{K["one"]}</b> {K["verdict"]}</p>'
               f'<div class="grid g3" style="gap:10px">{img(f"{k}-pole-10x14.webp", K["name"] + " pole")}{img(f"{k}-hoarding.webp", K["name"] + " hoarding")}{img(f"{k}-gate.webp", K["name"] + " gate")}</div>'
               f'<p style="margin:12px 0 4px">{img(f"{k}-row.webp", K["name"] + " pole row")}</p>'
               f'<details><summary>Sizes 10x10, 10x12, 10x14 and details</summary><div class="sizes" style="margin-top:12px">'
               + "".join(f'<figure style="width:150px">{img(f"{k}-board-{s}.webp", s)}<figcaption>{s} in</figcaption></figure>' for s in B2.SIZES)
               + f'</div><p style="margin-top:12px">{K["idea"]}</p><p><b>Risk:</b> {K["risk"]}</p></details></div>')
    r1 = "".join(f'<figure>{img(f"r1-{k}-hoarding.webp", k)}<figcaption>{k.capitalize()}, round 1</figcaption></figure>' for k in ("jamun", "gulaal", "kora"))
    cn = f'<div class="grid g3">{fig("c-steps.webp", "Every factory begins with one step.")}{fig("c-build.webp", "Building India\'s next factories.")}{fig("c-door.webp", "Step in.")}</div><div class="grid g2" style="margin-top:18px;align-items:center">{fig("c-steps-hoarding.webp", "As a hoarding")}{fig("c-steps-row.webp", "On every street-light pole")}</div>'
    refs = "".join(f'<figure>{img(f"ref-{n}.webp", n)}<figcaption>{c}</figcaption></figure>' for n, c in [
        ("markefy-red-stairs-we-build-the-next-step", "Markefy: red stairs."), ("avyukta-building-tomorrow-minimal", "Avyukta: quiet construction."),
        ("vodafone-red-pole-boards-series", "Vodafone: one colour, recognised from afar."), ("imtiaz-ooh-long-billboard-dubai", "Imtiaz: long-format hoarding."),
        ("kofi-kafi-blue-lightbox-field-photo", "Kofi Kafi: one colour lightbox.")])
    body = f"""
<header class="wrap" style="padding-top:56px;padding-bottom:20px"><div class="kick">Isapur Industrial Park · living brand document</div><h1>Everything in one place.</h1>
<p class="lead">This single page is updated in place as the work moves. Last build: {__import__("datetime").date.today():%d %b %Y}. Jump to any part below.</p>
<p>{"".join(f'<a class="pill" href="#{i}" style="text-decoration:none;margin:0 6px 6px 0">{t}</a>' for i, t in [("flow","Process"),("research","Research"),("site","Site"),("moods","8 moodboards"),("round2","Minimal kits"),("concept","Concept route"),("round1","Round 1"),("feedback","Feedback")])}</p></header>
<section id="flow"><div class="wrap"><div class="kick">How studios do it</div><h2>The process we are following</h2>
<p class="lead">Professional studios run the same arc: discover, research, strategise, explore widely, narrow with the client, build, test in context, hand over. Feedback gates sit between rounds so nothing is built on a guess.</p>
<div class="flow" style="margin-top:20px">{steps}</div>
<div class="grid g2" style="margin-top:20px"><div class="card"><h3>Feedback gates</h3><ol>{gates}</ol></div><div class="card"><h3>Sources for this process</h3><ul>{pro}</ul></div></div></div></section>
<section id="research"><div class="wrap"><div class="kick">Step 2</div><h2>Research summary</h2><div class="grid g2">
<div class="card"><h3>What a brand kit contains</h3><p>Logo with clear space and minimum size, colour with screen and print values, typography, graphic device, imagery, voice, applications and misuse. Left out of this pitch: full tone manuals, icon libraries, vendor contracts.</p></div>
<div class="card"><h3>What rooted Indian brands show</h3><p><b>McDonald's:</b> fixed visual core, local everything else. <b>Bata:</b> colour straight from the logo, name written in Hindi too. <b>boAt:</b> sells identity, not specs. <b>Vodafone poles:</b> one colour, recognised from far away. <b>Kofi Kafi:</b> one saturated colour, one symbol.</p></div></div>
<h3 style="margin-top:24px">Inspiration you supplied</h3><div class="grid g3">{refs}</div></div></section>
<section id="site"><div class="wrap"><div class="kick">Step 2</div><h2>The road and the competitors</h2>
{fig("map-isapur.webp", "Satellite view. IIP Phase 1 about 540 m from SHD and 690 m from CKS. Pins approximate; imagery Esri, Maxar, Earthstar Geographics.")}
<div class="grid g2" style="margin-top:20px">{fig("field-pole-1.webp", "Shri Balaji board, Sarawa (your photo).")}{fig("field-pole-stack.webp", "Shri Haridas, Shri Balaji and Shivansh on one pole (your photo).")}</div>
<div class="note" style="margin-top:20px"><b>Finding:</b> every competitor uses navy, gold or red with dense copy, prices, stamps, rendered gates and two phone numbers. At speed only the numbers are readable. The gap is clarity: one logo, one name, one line.</div></div></section>
<section id="moods"><div class="wrap"><div class="kick">Step 4 · feedback needed</div><h2>Eight territories</h2><p class="lead">Each is a different answer to the same road. They are moodboards, not finished kits. Tell us which to develop and which to kill.</p><div class="grid g2">{moods}</div></div></section>
<section id="round2"><div class="wrap"><div class="kick">Step 5 · early build</div><h2>Three minimal kits, already built</h2><p class="lead">Quiet, Portal and Ink match territories 1 to 3. Exact artwork, true scale, on your real photos.</p><div class="grid" style="gap:20px">{k2}</div></div></section>
<section id="concept"><div class="wrap"><div class="kick">Isolated route</div><h2>Conceptual adverts</h2><p class="lead">Kept separate from the main recommendation so the board can approve the kit without them.</p>{cn}</div></section>
<section id="round1"><div class="wrap"><details><summary>Round 1 (rejected): Jamun, Gulaal, Kora</summary><p style="color:var(--mut)">Loud colour-led directions. Kept for the record only.</p><div class="grid g3">{r1}</div></details></div></section>
<section id="feedback"><div class="wrap"><div class="kick">Your turn</div><h2>What we need from you</h2><div class="card"><ol><li>Which territories to develop (1 to 3), and why the others fail.</li><li>Real phone number, address line and call or WhatsApp.</li><li>Vector logo master (CDR, AI or SVG).</li><li>Language order on boards: Hindi first or English first.</li><li>Whether the concept route goes to the board.</li></ol><p style="color:var(--mut);margin-bottom:0">Reply in chat. This page then updates at the same link.</p></div></div></section>"""
    return B.shell("index.html", "IIP brand kit: living document", body, CSS3)


def main():
    B.NAV[:] = []
    B2.prep(); prep_extra()
    # prune pages from the old multi-page site
    (DOCS / "index.html").write_text(page(), encoding="utf-8")
    assert "—" not in (DOCS / "index.html").read_text(encoding="utf-8")
    (DOCS / ".nojekyll").write_text("")
    print("ok", sum(f.stat().st_size for f in DOCS.rglob("*") if f.is_file()) // 1024, "KB")


if __name__ == "__main__":
    main()
