"""Final site: built around the user's finalized kit + editable Brand-Kit. Rebuild: python work/build5.py"""
import re, shutil, zipfile, pathlib, datetime
import build as B
import build4 as X
import content as C

ROOT, DOCS, A = B.ROOT, B.DOCS, B.A
KIT = ROOT.parent / "Brand-Kit"
w, img, fig = B.webp, B.img, B.fig
FT = ROOT.parent / "References/final-thread"
NAV = [("index.html", "Home"), ("kit.html", "Brand kit"), ("mockups.html", "On the road"), ("downloads.html", "Editable files"), ("adapt.html", "How to adapt"),
       ("research.html", "Research"), ("site.html", "Site"), ("archive.html", "Earlier rounds")]
X.NAV[:] = NAV
STAMP = datetime.date.today().strftime("%d %b %Y")
head = X.head


def shell(fn, title, body, extra=""):
    X.NAV[:] = NAV
    return X.shell(fn, title, body, extra).replace("family=Archivo:", "family=Montserrat:wght@500;600;800&family=Inter:wght@400;500;600&family=Archivo:", 1)


def assets():
    X.assets()  # logo, map, field photos, reference images, moodboards (for the archive)
    for n, f in [("final-kit", "iipfinal-0-final-kit-input.png"), ("final-essentials", "iipfinal-4-essentials-kit.png"), ("final-sunburst", "iipfinal-5-sunburst-assets.png"), ("final-street-pole", "iipfinal-6-street-pole-2x3.png"), ("final-green", "iipfinal-2-green-set.png")]:
        w(FT / f, n + ".webp", 1600, 84)
    M = KIT / "05_Mockups"
    for n in ("hoarding-next-to-competitors", "pole-under-balaji", "pole-under-stack"):
        w(M / f"{n}.jpg", n + ".webp", 1600, 88)
    png = KIT / "export/png"
    for p in png.glob("*.png"):
        w(p, "kit-" + p.stem + ".webp", 1400, 86)
    for p in (KIT / "examples").glob("*.svg"):
        pass
    # downloads
    dl = DOCS / "kit"; dl.mkdir(exist_ok=True)
    for sub in ("live", "outlined", "tokens", "fonts", "editable-pptx", "examples"):
        shutil.copytree(KIT / sub, dl / sub, ignore=shutil.ignore_patterns("*-VF.ttf"))
    shutil.copytree(KIT / "export/pdf", dl / "pdf")
    shutil.copy(KIT / "README.md", dl / "README.md")
    zp = DOCS / "downloads"; zp.mkdir(exist_ok=True)
    with zipfile.ZipFile(zp / "IIP-Brand-Kit-editable.zip", "w", zipfile.ZIP_DEFLATED) as z:
        for f in KIT.rglob("*"):
            if f.is_file() and "__pycache__" not in str(f) and f.suffix != ".jpg" or (f.is_file() and f.name == "hero-warehouse.jpg"):
                if "_build" in f.parts and f.suffix not in (".py", ".json"): continue
                if f.name.endswith("-VF.ttf"): continue
                z.write(f, "IIP-Brand-Kit/" + str(f.relative_to(KIT)).replace("\\", "/"))
    print("zip", round((zp / "IIP-Brand-Kit-editable.zip").stat().st_size / 1e6, 1), "MB")


def home():
    body = head("Isapur Industrial Park · brand kit", "Your finalised brand, now fully editable.",
                "We took the kit you finalised, rebuilt every asset as editable vector files driven by one tokens file, and tested the hoarding next to a real competitor board.") + f"""
<section class="first"><div class="wrap">{fig("hoarding-next-to-competitors.webp", "Your 40 x 15 ft hoarding (right) and a pole board, placed next to the real Shri Balaji board on the Hapur-Modinagar road.")}
<div class="grid g3" style="margin-top:22px"><div class="card"><h3>The brand</h3><p>White, charcoal, brand yellow, red accent and deep green. Montserrat for headlines, Inter for text. The sunburst from the badge as the graphic device. Line: A Modern Industrial Address.</p><a href="kit.html">Open the brand kit</a></div>
<div class="card"><h3>Editable</h3><p>34 assets as live-text SVG, outlined SVG, PDF, PNG and PowerPoint. Change a phone number or colour in one file and rebuild all of them.</p><a href="downloads.html">Get the files</a></div>
<div class="card"><h3>Easy to adapt</h3><p>The guide for you and any designer: what to change, what never to change, and worked examples with new lines and proof lines.</p><a href="adapt.html">How to adapt</a></div></div></div></section>
<section><div class="wrap"><div class="kick">What you finalised</div><h2>The kit as designed in ChatGPT</h2><p class="lead">Kept exactly: logo lockups, palette, typography, icons, tagline, sunburst asset type, pattern and the pole advert.</p>
<div class="grid g2">{fig("final-kit.webp", "Your finalised brand kit")}{fig("final-street-pole.webp", "Your 2:3 street pole advert")}</div></div></section>"""
    return shell("index.html", "IIP brand kit", body)


def kit():
    T = KIT / "tokens/brand.tokens.json"
    import json
    tok = json.loads(T.read_text())
    pal = "".join(f'<div class="sw"><div class="c" style="background:{v["value"]};color:{"#fff" if k in ("charcoal","red","green") else "#111827"}">{k.title()}</div><div class="m"><b>{v["value"]}</b>RGB {B.rgbs(v["value"])}<br>CMYK ~{B.cmyk(v["value"])}<br><span style="color:var(--mut)">{v["use"]}</span></div></div>' for k, v in tok["color"].items())
    thumb = lambda n, cap: fig(f"kit-{n}.webp", cap)
    body = head("Brand kit", "The system on one page.", "Everything below is generated from two small files, so every asset stays consistent.") + f"""
<section class="first"><div class="wrap"><div class="kick">1 · Logo</div><h2>Lockups</h2><div class="grid g3">{thumb("logo-primary-vertical", "Primary vertical lockup")}{thumb("logo-horizontal", "Horizontal lockup")}{thumb("logo-badge-only", "Badge only: favicon, social avatar, helmet, stamp")}</div>
<div class="grid g3" style="margin-top:18px">{thumb("logo-mono-black", "Single colour black (stamps, fax, newspaper)")}{thumb("logo-reversed-on-charcoal", "Reversed, for dark backgrounds")}{thumb("logo-clear-space-guide", "Clear space: 0.25 x badge width on every side")}</div>
<div class="note" style="margin-top:18px"><b>Minimum size:</b> full lockup 30 mm print or 120 px screen. Badge alone 16 px. <b>Never</b> recolour, stretch, rotate, outline or add shadows to the badge. Badge artwork is a trace of the supplied file (no vector exists yet).</div></div></section>
<section><div class="wrap"><div class="kick">2 · Colour</div><h2>Palette</h2><div class="grid g4 keep2">{pal}</div><p style="font-size:13px;color:var(--mut)">CMYK values are approximate. Approve a printed proof. The badge keeps its own measured colours (#FEF102, #EE1D23, #00A54F).</p></div></section>
<section><div class="wrap"><div class="kick">3 · Type</div><h2>Typography</h2><div class="grid g2"><div class="card"><div style="font:800 54px Montserrat">Aa ISAPUR</div><b>Montserrat</b> 800 / 600 / 500. Headlines, signage, advertising.</div><div class="card"><div style="font:500 54px Inter">Aa Subhead</div><b>Inter</b> 400 / 500 / 600. Subheads, body, digital. Both free (SIL OFL).</div></div></div></section>
<section><div class="wrap"><div class="kick">4 · Graphic elements</div><h2>Sunburst, stripe, icons</h2><div class="grid g3">{thumb("tri-colour-stripe", "Tri-colour stripe: base line, tags, CTAs")}{thumb("sunburst-ring-border", "Sunburst ring: frame or border")}{thumb("cta-badges", "Sunburst badges: offers and features")}</div>
<div class="grid g2" style="margin-top:18px">{thumb("sunburst-repeat-pattern", "Repeating pattern, subtle background only")}{fig("final-sunburst.webp", "Your sunburst asset sheet, kept as reference")}</div>
<div class="grid g4 keep2" style="margin-top:18px">{"".join(thumb("icon-" + n, n.replace("-", " ").title()) for n in ("industrial-plots", "wide-roads", "power-supply", "water-supply"))}</div></div></section>
<section><div class="wrap"><div class="kick">5 · Templates</div><h2>Ready-to-edit layouts</h2><div class="grid g3">{thumb("pole-board-20x32in-photo", "Pole board 20 x 32 in, with photo")}{thumb("pole-board-20x32in-clean", "Pole board, clean (type only)")}{thumb("street-pole-24x36in-2to3", "Street pole advert 24 x 36 in (2:3), with icons and CTA")}</div>
<div class="grid g2" style="margin-top:18px">{thumb("hoarding-40x20ft", "Hoarding 40 x 20 ft (2:1)")}{thumb("hoarding-40x15ft", "Hoarding 40 x 15 ft (8:3)")}</div>
<div class="grid g3" style="margin-top:18px">{thumb("business-card-front", "Business card front")}{thumb("business-card-back", "Business card back")}{thumb("letterhead-A4", "Letterhead A4")}</div>
<div class="grid g3" style="margin-top:18px">{thumb("id-card-54x86mm", "ID card")}{thumb("whatsapp-status-1080x1920", "WhatsApp status 9:16")}{thumb("social-post-1080x1080", "Social post 1:1")}</div></div></section>"""
    return shell("kit.html", "IIP brand kit", body)


def mockups():
    body = head("On the road", "Next to the competition.", "The competitor board is your own photograph of the Shri Balaji board, flattened and placed back into a neutral-light scene. The IIP boards are the exact kit artwork in true perspective.") + f"""
<section class="first"><div class="wrap">{fig("hoarding-next-to-competitors.webp", "IIP pole board (below) and 40 x 15 ft hoarding (right) beside the Shri Balaji board")}
<div class="grid g2" style="margin-top:22px">{fig("pole-under-balaji.webp", "IIP pole board directly under the Shri Balaji board on your Sarawa photo. Same width, shape and mounting.")}{fig("pole-under-stack.webp", "At the foot of the three-board stack")}</div>
<div class="note" style="margin-top:20px"><b>What this shows:</b> the competitor board is dense: stamp, price, two numbers, a rendered township. The IIP board is the opposite: one logo, one line, two numbers, a photo. White space is the differentiator. <b>Caveat:</b> the empty scene was generated, so tree and road details are illustrative. The sizes are by scale from your photos, to be confirmed with the media owner.</div></div></section>"""
    return shell("mockups.html", "IIP on the road", body)


def downloads():
    rows = ""
    tree = [("01_Logo", ["logo-primary-vertical", "logo-horizontal", "logo-badge-only", "logo-mono-black", "logo-reversed-on-charcoal", "logo-clear-space-guide"]),
            ("02_Pattern", ["tri-colour-stripe", "sunburst-outline", "sunburst-solid-yellow", "sunburst-ring-border", "sunburst-repeat-pattern", "diagonal-panels", "cta-badges"]),
            ("04_Templates", ["pole-board-20x32in-photo", "pole-board-20x32in-clean", "street-pole-24x36in-2to3", "hoarding-40x20ft", "hoarding-40x15ft", "business-card-front", "business-card-back", "letterhead-A4", "id-card-54x86mm", "whatsapp-status-1080x1920", "social-post-1080x1080"])]
    for folder, names in tree:
        for n in names:
            rows += f'<tr><td><b>{n}</b><br><span style="color:var(--mut);font-size:13px">{folder}</span></td><td><a href="kit/live/{folder}/{n}.svg">Editable SVG</a></td><td><a href="kit/outlined/{folder}/{n}.svg">Print SVG</a></td><td><a href="kit/pdf/{n}.pdf">PDF</a></td></tr>'
    body = head("Editable files", "Everything, ready to edit.", "Live SVG has real text you can edit. Print SVG and PDF have text converted to shapes for the print shop. All are true vector.") + f"""
<section class="first"><div class="wrap"><div class="grid g3"><div class="card"><h3>Download all</h3><p>One zip with every file, fonts, tokens, PowerPoint files, examples and the build scripts.</p><a class="pill dk" href="downloads/IIP-Brand-Kit-editable.zip" style="text-decoration:none">IIP-Brand-Kit-editable.zip</a></div>
<div class="card"><h3>Open with</h3><p>Illustrator, Inkscape (free), Figma, Affinity, CorelDRAW for SVG. PowerPoint, Keynote, Google Slides or Canva for the PPTX files. Install the fonts first.</p><a href="kit/fonts/">Fonts</a></div>
<div class="card"><h3>PowerPoint versions</h3><ul><li><a href="kit/editable-pptx/pole-board-20x32in.pptx">Pole board 20 x 32 in</a></li><li><a href="kit/editable-pptx/hoarding-40x20ft-scaled-1in-per-ft.pptx">Hoarding (1 in = 1 ft)</a></li><li><a href="kit/editable-pptx/business-card-front-3.5x2in.pptx">Card front</a></li><li><a href="kit/editable-pptx/business-card-back-3.5x2in.pptx">Card back</a></li></ul></div></div>
<h2 style="margin-top:30px">Single files</h2><div class="card scroll" style="padding:6px 14px"><table><tr><th>Asset</th><th>Edit</th><th>Print</th><th>PDF</th></tr>{rows}</table></div>
<div class="note" style="margin-top:20px"><b>Tokens:</b> <a href="kit/tokens/brand.tokens.json">brand.tokens.json</a> and <a href="kit/tokens/content.json">content.json</a>. Edit these, re-run the builder, and all 34 assets regenerate.</div></div></section>"""
    return shell("downloads.html", "IIP editable files", body)


def adapt():
    ex = lambda n, cap: f'<figure>{img(n, cap)}<figcaption>{cap}</figcaption></figure>'
    body = head("How to adapt", "Change one thing, keep the brand.", "A brand kit is useful only if anyone can extend it correctly. This is how this one is structured, and what we found in the research.") + f"""
<section class="first"><div class="wrap"><div class="kick">The three layers</div><h2>What lives where</h2><div class="grid g3">
<div class="card"><h3>1 · Tokens</h3><p>Colours, fonts, clear space, minimum sizes. One file. Changing a colour here changes every asset. Studios call this a single source of truth.</p></div>
<div class="card"><h3>2 · Content</h3><p>Words, phone numbers, address, tagline, proof lines on or off. One file. A new campaign line is one edit.</p></div>
<div class="card"><h3>3 · Templates</h3><p>The layouts. Pole board, hoarding, card, letterhead, status. They read layers 1 and 2, so they cannot drift out of brand.</p></div></div>
<div class="grid g2" style="margin-top:20px"><div class="card"><h3>Never change</h3><ul><li>The badge: no recolour, stretch, rotate, effects.</li><li>Clear space and minimum size.</li><li>The wordmark proportions.</li><li>More than 7 words on a board.</li></ul></div>
<div class="card"><h3>Safe to change</h3><ul><li>Tagline, phone numbers, address.</li><li>Photo in the photo slot (<code>hero-photo</code>).</li><li>Proof lines on or off.</li><li>Which template and size you use.</li></ul></div></div></div></section>
<section><div class="wrap"><div class="kick">Worked examples</div><h2>Same kit, two new boards</h2><p class="lead">Only <code>content.json</code> changed. Everything else regenerated.</p>
<div class="grid g3">{ex("kit-pole-board-20x32in-photo.webp", "Original: tagline, phones")}{ex("kit-street-pole-24x36in-2to3.webp", "Street pole 2:3 with icons and CTA")}{ex("kit-hoarding-40x15ft.webp", "Hoarding 40 x 15 ft")}</div>
<p style="margin-top:12px">Variants with proof lines on, and with the line <i>Industrial Plots Available.</i>, are in <a href="kit/examples/">examples</a> as SVG.</p></div></section>
<section><div class="wrap"><div class="kick">Research summary</div><h2>What the sources say, and what we did</h2><div class="grid g2">
<div class="card"><h3>Structure</h3><ul><li>Order sections from most recognisable to most nuanced: logo, colour, type, graphic elements, templates (<a href="https://www.4over4.com/content-hub/stories/brand-guidelines-checklist" target="_blank" rel="noopener">4over4</a>).</li><li>Three token layers (primitive, semantic, component), and every value defined in exactly one file (<a href="https://brandyhq.com/blog/living-brand-guidelines-vs-static-style-sheets/" target="_blank" rel="noopener">Brandy HQ</a>). We use two files, tokens and content, because the kit is small.</li><li>Write it so a freelancer who has never met the brand can produce on-brand work on the first brief.</li></ul></div>
<div class="card"><h3>Files</h3><ul><li>Master vector, then export the rest. AI is the editable master, EPS or PDF for print, SVG for web, PNG as fallback (<a href="https://www.brandcloud.pro/en/blog/vector-graphics-formats-when-to-use-svg-ai-eps-or-pdf" target="_blank" rel="noopener">BrandCloud</a>, <a href="https://justcreative.com/2020/03/23/logo-design-file-formats-guide/" target="_blank" rel="noopener">JUST Creative</a>). We use SVG as the editable master because it opens everywhere and is free.</li><li>Converting a raster to vector does not make a true vector logo. The badge here is a trace, so find the original.</li><li>CMYK for print, RGB for screens. Confirm CorelDRAW needs with your printer: export PDF or EPS from the SVG.</li></ul></div>
<div class="card"><h3>Hoardings and poles</h3><ul><li>Common Indian hoarding sizes: 20 x 10 ft medium, 40 x 20 ft large (<a href="https://smartads.in/services/outdoor/outdoor-advertising-for-medium-hoarding" target="_blank" rel="noopener">SmartAds</a>). We drew 40 x 20 and 40 x 15.</li><li>Seven or fewer words, simple sans-serif, high contrast, leave generous empty space (<a href="https://macmyths.com/how-to-design-a-billboard-that-stays-readable-at-highway-speed/" target="_blank" rel="noopener">MacMyths</a>, <a href="https://billboardinsider.com/design-tips-by-porlier-outdoor/" target="_blank" rel="noopener">Porlier</a>).</li><li>Letter height: rules range from 1 in per 10 ft to 1 in per 30 ft of distance. We assume the cautious end for the 40 x 20 hoarding. Check at full scale from the approach lane.</li></ul></div>
<div class="card"><h3>What you do next</h3><ol><li>Find the original vector logo, or approve a redraw.</li><li>Decide proof lines on or off, and match wording to documents.</li><li>Replace the AI warehouse photo with a real site photo when possible.</li><li>Ask the printer for exact flex size, bleed and file type.</li><li>Print a small colour proof of yellow, red and green before the full run.</li></ol></div></div></div></section>"""
    return shell("adapt.html", "IIP how to adapt", body)


def archive():
    html = X.routes()
    inner = re.search(r"</nav>(.*?)<footer>", html, re.S).group(1)
    inner = inner.replace("Eight territories, two chosen.", "Earlier rounds, kept for the record.")
    return shell("archive.html", "IIP earlier rounds", inner, ".gal figure img{width:100%}")


def main():
    assets()
    wr = B.write
    X.NAV[:] = NAV
    for fn, h in [("index.html", home()), ("kit.html", kit()), ("mockups.html", mockups()), ("downloads.html", downloads()), ("adapt.html", adapt()), ("archive.html", archive())]:
        wr(fn, h)
    wr("research.html", shell("research.html", "IIP research", re.search(r"</nav>(.*?)<footer>", B.research_page(), re.S).group(1)))
    wr("site.html", shell("site.html", "IIP site", re.search(r"</nav>(.*?)<footer>", B.site_page(), re.S).group(1)))
    (DOCS / ".nojekyll").write_text("")
    print("ok", round(sum(f.stat().st_size for f in DOCS.rglob("*") if f.is_file()) / 1e6, 1), "MB")


if __name__ == "__main__":
    main()
