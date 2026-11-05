"""Cleaner final site. Reuses build5 (assets, home, kit, mockups, downloads) and replaces Research, Site, Adapt, Archive. Rebuild: python work/build6.py"""
import re, pathlib
from playwright.sync_api import sync_playwright
import build as B
import build4 as X
import build5 as P
import content as C

ROOT, DOCS, A = B.ROOT, B.DOCS, B.A
KIT = ROOT.parent / "Brand-Kit"
w, img, fig, head, shell = B.webp, B.img, B.fig, X.head, P.shell
PRO = [("Canny Creative: 10-step branding process", "https://www.canny-creative.com/blog/branding-process-successful-business-branding/"),
       ("JUST Creative: brand strategy and design process", "https://justcreative.com/brand-strategy-design-process/")]


def render_examples():
    out = ROOT / "gen" / "examples"; out.mkdir(exist_ok=True)
    with sync_playwright() as p:
        br = p.chromium.launch()
        for f in sorted((KIT / "examples").glob("*.svg")):
            s = f.read_text(encoding="utf-8")
            vw, vh = map(float, re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', s).groups())
            k = 1400 / max(vw, vh); W, H = round(vw * k), round(vh * k)
            pg = br.new_page(viewport={"width": W, "height": H})
            pg.set_content('<body style="margin:0">' + re.sub(r"<\?xml[^>]*\?>", "", re.sub(r"<svg", f'<svg style="width:{W}px;height:{H}px"', s, 1)) + "</body>")
            pg.wait_for_timeout(120); pg.screenshot(path=str(out / (f.stem + ".png"))); pg.close()
            w(out / (f.stem + ".png"), "ex-" + f.stem.lower().replace("__", "-") + ".webp", 1300, 86)
        br.close()


def research():
    anat = [("Logo system", "Lockups, clear space, minimum size, one-colour and reversed versions."), ("Colour", "Screen and print values, usage balance, contrast pairs."),
            ("Typography", "Two typefaces at most and how each is used."), ("Graphic elements", "The one or two recurring shapes that make the brand recognisable: here the sunburst and the stripe."),
            ("Templates", "Real layouts at real sizes: boards, hoardings, cards, letterhead, social."), ("Rules", "What never changes, what is safe to change, who approves, what to check before print.")]
    rows = "".join(f"<tr><td><b>{a}</b></td><td>{b}</td></tr>" for a, b in anat)
    brands = [("McDonald's India", "Fixed visual core, local everything else", "Arches, red and yellow, packaging and layout stay uniform while the menu and messages adapt."),
              ("Bata India", "A colour taken from the logo", "Red and white stores mirror the logo; the name is written in local scripts. Trust compounds over decades."),
              ("boAt", "Identity, not specifications", "Case studies describe lifestyle, a named community and bold design rather than technical talk."),
              ("Vodafone poles", "Recognised from far away", "Your own reference: one colour repeated on every pole reads at distance.")]
    cards = "".join(f'<div class="card"><div class="kick">{n}</div><h3>{h}</h3><p style="margin:0;color:var(--mut)">{t}</p></div>' for n, h, t in brands)
    src = "".join(f'<li><a href="{u}" target="_blank" rel="noopener">{t}</a></li>' for g, items in C.SOURCES for t, u in items)
    body = head("Research", "What we studied before building.", "Brand kit anatomy, rooted Indian brands, hoarding legibility and file formats. Short version below; full reading list at the end.") + f"""
<section class="first"><div class="wrap"><div class="kick">1</div><h2>What a brand kit contains</h2><div class="card scroll" style="padding:6px 14px"><table><tr><th style="width:170px">Section</th><th>What it contains</th></tr>{rows}</table></div>
<p class="lead" style="margin-top:16px;font-size:17px">Consensus across the guidelines reviewed: put the most recognisable assets first, define each value once, and write it so someone who has never met the brand can use it correctly.</p></div></section>
<section><div class="wrap"><div class="kick">2</div><h2>What rooted Indian brands show</h2><div class="grid g2">{cards}</div></div></section>
<section><div class="wrap"><div class="kick">3</div><h2>Rules applied to the boards</h2><div class="grid g3">
<div class="card"><h3>Few words</h3><p style="margin:0">Seven words or fewer, simple sans-serif, high contrast, generous empty space. So each board carries the logo, one line and two numbers.</p></div>
<div class="card"><h3>Test at scale</h3><p style="margin:0">Letter-height rules range from 1 in per 10 ft to 1 in per 30 ft of viewing distance. Check at full size from the approach lane.</p></div>
<div class="card"><h3>True vector</h3><p style="margin:0">Print needs vector. Tracing a PNG is not the same as an original vector logo, so keep looking for the original.</p></div></div></div></section>
<section><div class="wrap"><div class="kick">Sources</div><h2>Reading list</h2><div class="card"><ul style="columns:2;column-gap:30px">{src}</ul></div>
<p style="color:var(--mut);margin-top:12px">Process references: {" · ".join(f'<a href="{u}" target="_blank" rel="noopener">{t}</a>' for t, u in PRO)}</p></div></section>"""
    return shell("research.html", "IIP research", body)


def site():
    rows = [("Shri Balaji Industrial Park", "Sarawa bus stand, Hapur-Modinagar Road", "Blue sky gradient, gold type", "Industrial plot, approval stamp, two numbers, rendered township"),
            ("Shri Haridas Industrial Park", "Ishapur, Bhojpur, Modinagar", "White and navy, Hindi headline", "Approval claim, rendered gate, road widths, security, two numbers"),
            ("Shivansh Industrial Park", "Not stated on the board", "Navy and gold, red phone bar", "All sizes of plots available, two numbers"),
            ("CKS Industrial Park", "Hapur-Modinagar Road (listing)", "Not photographed", "Per-yard price and approval claim in public listings, unverified"),
            ("Atom Industrial Park", "Ishapur (Google Maps)", "Not photographed", "Listed on Google Maps, about 3 km down the road")]
    tr = "".join(f"<tr><td><b>{a}</b></td><td>{b}</td><td>{c}</td><td>{d}</td></tr>" for a, b, c, d in rows)
    body = head("Site", "The road and the competition.", "IIP Phase 1 is on the Hapur-Modinagar Road at Yusufpur Isapur, about 540 m from SHD and 690 m from CKS. Pin positions are approximate.") + f"""
<section class="first"><div class="wrap">{fig("map-isapur.webp", "Satellite view, north up. Imagery Esri, Maxar, Earthstar Geographics, a few years old.")}
<div class="grid g2" style="margin-top:20px">{fig("field-pole-1.webp", "Shri Balaji board, Sarawa (your photo)")}{fig("field-pole-stack.webp", "Three boards on one pole (your photo)")}</div></div></section>
<section><div class="wrap"><h2>Competitors</h2><div class="card scroll" style="padding:6px 14px"><table><tr><th>Park</th><th>Where</th><th>Look</th><th>What it says</th></tr>{tr}</table></div>
<div class="note" style="margin-top:20px"><b>Finding:</b> every board uses navy, gold or red with dense copy: stamp, price, rendered township, two numbers. At 40 km/h only the numbers are readable. White space, one logo and one line is the gap IIP fills. Details are read from photographs and public listings and are not verified.</div></div></section>"""
    return shell("site.html", "IIP site", body)


def adapt():
    ex = lambda n, cap: fig(n, cap)
    body = head("How to adapt", "Change one thing, keep the brand.", "Anyone can extend this kit correctly because values live in two small files and every layout reads from them.") + f"""
<section class="first"><div class="wrap"><div class="grid g3">
<div class="card"><h3>1 · Tokens</h3><p style="margin:0">Colours, fonts, clear space, minimum sizes. Change a colour once and every asset follows.</p></div>
<div class="card"><h3>2 · Content</h3><p style="margin:0">Words, phone numbers, address, proof lines on or off. A new campaign line is one edit.</p></div>
<div class="card"><h3>3 · Templates</h3><p style="margin:0">The layouts: pole board, hoarding, cards, letterhead, social. They read layers 1 and 2, so they cannot drift.</p></div></div>
<div class="grid g2" style="margin-top:18px"><div class="card"><h3>Never change</h3><ul><li>The badge: recolour, stretch, rotate, effects.</li><li>Clear space and minimum size.</li><li>More than 7 words on a board.</li></ul></div>
<div class="card"><h3>Safe to change</h3><ul><li>Tagline, numbers, address.</li><li>The photo in the <code>hero-photo</code> slot.</li><li>Proof lines on or off. Which size.</li></ul></div></div></div></section>
<section><div class="wrap"><div class="kick">Worked examples</div><h2>Two edits, six new boards</h2>
<p class="lead">Edit A switched the proof lines on. Edit B also changed the line to <i>Industrial Plots Available.</i> Nothing else was touched. Each took one rebuild.</p>
<h3 style="margin-top:22px">A · Proof lines on</h3><div class="grid g3">{ex("ex-a-proof-lines-on-pole-board-20x32in-photo.webp", "Pole board")}{ex("ex-a-proof-lines-on-street-pole-24x36in-2to3.webp", "Street pole 24 x 36 in")}{ex("ex-a-proof-lines-on-hoarding-40x15ft.webp", "Hoarding 40 x 15 ft")}</div>
<h3 style="margin-top:26px">B · New line</h3><div class="grid g3">{ex("ex-b-new-line-plots-available-pole-board-20x32in-photo.webp", "Pole board")}{ex("ex-b-new-line-plots-available-street-pole-24x36in-2to3.webp", "Street pole 24 x 36 in")}{ex("ex-b-new-line-plots-available-hoarding-40x15ft.webp", "Hoarding 40 x 15 ft")}</div>
<p style="color:var(--mut);margin-top:12px">SVG sources of these are in the download zip under <code>examples/</code>. Proof wording is as stated by the owner and must match the documents before print.</p></div></section>
<section><div class="wrap"><div class="kick">Steps</div><h2>To make a new asset</h2><div class="card"><ol><li>Edit <code>tokens/content.json</code> (words) or <code>brand.tokens.json</code> (colour, fonts).</li><li>Run <code>python Brand-Kit/_build/build_kit.py</code> to regenerate all SVG, then <code>export.py</code> for PDF and PNG.</li><li>Or open any file in <code>live/</code> in Inkscape, Illustrator, Figma or CorelDRAW and edit by hand. Install the fonts first.</li><li>Send the <code>outlined/</code> or PDF version to the printer.</li></ol></div>
<div class="note" style="margin-top:16px"><b>Still to do on your side:</b> find the original vector logo, confirm proof wording, replace the AI warehouse photo with a real site photo, ask the printer for exact flex size and bleed, and print a small colour proof of yellow, red and green first.</div></div></section>"""
    return shell("adapt.html", "IIP how to adapt", body)


def main():
    P.assets()
    render_examples()
    wr = B.write
    P.X.NAV[:] = P.NAV
    for fn, h in [("index.html", P.home()), ("kit.html", P.kit()), ("mockups.html", P.mockups()), ("downloads.html", P.downloads()),
                  ("adapt.html", adapt()), ("research.html", research()), ("site.html", site()), ("archive.html", P.archive())]:
        wr(fn, h)
    (DOCS / ".nojekyll").write_text("")
    print("ok", round(sum(f.stat().st_size for f in DOCS.rglob("*") if f.is_file()) / 1e6, 1), "MB")


if __name__ == "__main__":
    main()
