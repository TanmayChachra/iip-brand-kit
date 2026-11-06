"""Builds the single page brand kit: Brand-Kit/site/index.html (+ site/assets).  Run: python Brand-Kit/_build/build_site.py
Inputs: tokens, research/sections.json, live/ outlined/ export/ reference/, Isapur-Poster PDF.  Words live in site_content.py."""
import json, pathlib, shutil, sys, html, datetime
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from PIL import Image
import site_content as S

KIT = pathlib.Path(__file__).resolve().parents[1]
ROOT = KIT.parent
SITE = KIT / "site"; A = SITE / "assets"
TOK = json.loads((KIT / "tokens/brand.tokens.json").read_text())
CT = json.loads((KIT / "tokens/content.json").read_text())
RES = json.loads((KIT / "research/sections.json").read_text())
VERSION = "1.0"; TODAY = datetime.date.today().isoformat()
e = html.escape

SITE.mkdir(exist_ok=True)
for c in SITE.iterdir(): shutil.rmtree(c) if c.is_dir() else c.unlink()   # keep the folder itself (a shell may be inside it)
for d in ("p", "svg", "svg-live", "pdf", "fonts", "ref", "files"): (A / d).mkdir(parents=True, exist_ok=True)


# ---------- asset plumbing ----------
def thumb(png, name, long=1100):
    im = Image.open(png).convert("RGBA"); k = min(1, long / max(im.size))
    if k < 1: im = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
    im.save(A / "p" / f"{name}.webp", quality=82, method=6)


def prep(stem, folder):
    png = KIT / "export/png" / f"{stem}.png"
    if png.exists(): thumb(png, stem, 1600 if "hoarding" in stem else 1100)
    for src, dst in ((KIT / "outlined" / folder / f"{stem}.svg", "svg"), (KIT / "live" / folder / f"{stem}.svg", "svg-live"), (KIT / "export/pdf" / f"{stem}.pdf", "pdf")):
        if src.exists(): shutil.copy(src, A / dst / src.name)


def card(a):
    stem, folder, label, note = a; prep(stem, folder)
    links = "".join(f'<a href="assets/{d}/{stem}.{x}" download>{n}</a>' for d, x, n in
                    (("svg", "svg", "SVG"), ("svg-live", "svg", "SVG editable"), ("pdf", "pdf", "PDF")) if (A / d / f"{stem}.{x}").exists())
    img = f'<img src="assets/p/{stem}.webp" alt="{e(label)}">' if (A / "p" / f"{stem}.webp").exists() else ""
    return f'<figure class="card"><div class="thumb">{img}</div><figcaption><b>{e(label)}</b><span>{e(note)}</span><div class="dl">{links}</div></figcaption></figure>'


def grid(items, cls=""): return f'<div class="grid {cls}">' + "".join(card(a) for a in items) + "</div>"


def ref(name, label, cls=""):
    shutil.copy(KIT / "reference/mockups" / f"{name}.webp", A / "ref" / f"{name}.webp")
    return f'<figure class="card"><div class="thumb"><img src="assets/ref/{name}.webp" alt="{e(label)}"></div><figcaption><b>{e(label)}</b></figcaption></figure>'


def board(n, label):
    f = {1: "board-1-brand-kit-extended", 2: "board-2-sunburst-asset-type", 3: "board-3-brand-kit-final"}[n]
    shutil.copy(KIT / f"reference/{f}.webp", A / "ref" / f"{f}.webp")
    return f'<figure class="card wide"><div class="thumb"><img src="assets/ref/{f}.webp" alt="{e(label)}"></div><figcaption><b>{e(label)}</b><span>The finalised board supplied by the owner (raster reference).</span></figcaption></figure>'


# ---------- colour maths ----------
def rgb(h): h = h.lstrip("#"); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
def lum(c):
    f = lambda v: (v / 255 / 12.92) if v / 255 <= 0.03928 else (((v / 255 + 0.055) / 1.055) ** 2.4)
    r, g, b = (f(x) for x in c); return 0.2126 * r + 0.7152 * g + 0.0722 * b
def contrast(a, b): la, lb = sorted((lum(rgb(a)), lum(rgb(b))), reverse=True); return (la + 0.05) / (lb + 0.05)
def cmyk(h):
    r, g, b = (x / 255 for x in rgb(h)); k = 1 - max(r, g, b)
    return (0, 0, 0, 100) if k == 1 else tuple(round(100 * v) for v in ((1 - r - k) / (1 - k), (1 - g - k) / (1 - k), (1 - b - k) / (1 - k), k))


COL = [(k, v["value"], v["use"]) for k, v in TOK["color"].items()]
EXTRA_COL = [("Pure white", "#FFFFFF", "Backgrounds"), ("Light gray", "#E6E8EB", "Hairlines, panels"), ("Gray", "#C9CED6", "Disabled, borders"),
             ("Dark gray", "#6B7280", "Secondary text"), ("Black", "#000000", "Mono print only")]


def swatches(items):
    out = '<div class="sw">'
    for n, h, u in items:
        c = contrast(h, "#FFFFFF"); c2 = contrast(h, "#111827")
        out += (f'<div class="s"><i style="background:{h}"></i><b>{e(n.title() if n.islower() else n)}</b><code>{h}</code>'
                f'<span>RGB {", ".join(map(str, rgb(h)))}<br>CMYK about {" / ".join(map(str, cmyk(h)))}</span>'
                f'<span>On white {c:.1f}:1 &middot; on charcoal {c2:.1f}:1</span><em>{e(u)}</em></div>')
    return out + "</div>"


def table(head, rows, cls=""):
    return (f'<div class="tw"><table class="{cls}"><thead><tr>' + "".join(f"<th>{e(h)}</th>" for h in head) + "</tr></thead><tbody>" +
            "".join("<tr>" + "".join(f"<td>{c if str(c).startswith('<') else e(str(c))}</td>" for c in r) + "</tr>" for r in rows) + "</tbody></table></div>")


def tag(t): return f'<span class="tg {t.lower().replace(" ", "-")}">{e(t)}</span>'


def dd(items, ok=True):
    return '<ul class="dd ' + ("ok" if ok else "no") + '">' + "".join(f"<li>{e(i)}</li>" for i in items) + "</ul>"


# ---------- sections ----------
SEC = []  # (id, title, status, html)
def sec(i, title, status, body): SEC.append((i, title, status, body))

sec("story", "Brand story and positioning", "draft", f"""
<p class="lead">Isapur Industrial Park is a modern industrial address on the Hapur-Modinagar Road for local manufacturers who want a clear, legal, well laid plot without noise.</p>
<div class="two"><div><h4>Positioning</h4><p>For factory owners and small industrial buyers along the Hapur-Modinagar Road, IIP is the industrial park that says less and shows more: wide roads, clean papers, a name you can read from a moving vehicle.</p>
<h4>Promise</h4><p>Plots you can verify. Facilities we can show. One number to call.</p><h4>Tagline</h4><p class="big">{e(CT['tagline_one_line'])}</p></div>
<div><h4>Audience</h4><p>Primary: local factory owners and small industrial buyers. Secondary candidates (owner to confirm): warehouse and logistics operators, investors, brokers.</p>
<h4>Personality</h4><p>Calm, exact, modern, trustworthy. A planner, not a salesman.</p><h4>What makes us different here</h4><p>Competitor boards on this road use navy, gold or red, dense copy, stamps and rendered townships. IIP uses white space, one logo and one line, so it is read first and remembered.</p></div></div>
<p class="note">{tag('DRAFT')} Story, promise and personality are proposed from the owner's decisions. Please confirm or edit. Registered company name and developer entity are still unknown.</p>""")

sec("logo", "Logo system", "have", f"""
<p class="lead">The badge is never changed, recoloured or redrawn. Every lockup uses the same badge, the Montserrat ExtraBold wordmark and the red accent line.</p>
<div class="two"><div><h4>Construction</h4><ul><li><b>Brand mark</b>: the rosette badge (sunburst, IiP monogram, circuit dots).</li><li><b>Logotype</b>: IiP monogram alone.</li><li><b>Wordmark</b>: ISAPUR over INDUSTRIAL PARK.</li><li><b>Accent line</b>: red rule beside INDUSTRIAL PARK.</li></ul></div>
<div><h4>Rules of thumb</h4><ul><li>Clear space: a quarter of the badge width on every side.</li><li>Minimum size: full lockup 30 mm in print, 120 px on screen. Badge alone 16 px.</li><li>Source: no vector original exists. The badge is a traced vector of the supplied artwork, good up to hoarding size. Find the designer's original for very large or very close print.</li></ul></div></div>
{grid(S.LOGO)}""")

sec("misuse", "Logo usage and misuse", "have", f"""
<div class="two"><div><h4>Do</h4>{dd(["Use approved lockups only.", "Keep clear space and minimum size.", "Use brand colours as per the palette.", "Use Montserrat for headlines, Inter for body.", "Put the logo on white, mist gray or charcoal."])}</div>
<div><h4>Do not</h4>{dd(["Change the logo colours.", "Distort, stretch or rotate the logo.", "Add outlines, shadows or effects.", "Place it on low contrast or busy backgrounds.", "Rebuild the wordmark in another typeface."], False)}</div></div>
{grid(S.LOGO[-1:], "one")}""")

sec("colour", "Colour system", "partial", f"""
<p class="lead">White first, charcoal for text, yellow for highlight, red as a thin accent, deep green as the quiet secondary. The badge keeps its own measured colours (yellow #FEF102, red #EE1D23, green #00A54F) and is never retinted.</p>
{swatches(COL)}<h4>Supporting neutrals</h4>{swatches(EXTRA_COL)}
<h4>Proportion guide {tag('DRAFT')}</h4><p>About 70% white and mist, 20% charcoal, 6% yellow, 2% red, 2% green. Red is a line, not a block.</p>
<p class="note">CMYK values are a simple conversion for planning. Ask the printer for a colour proof and tune from the proof. Contrast ratios are computed (WCAG), text needs 4.5:1 or more.</p>""")

sec("type", "Typography", "have", """
<p class="lead">Two free families (SIL Open Font License, free for commercial use).</p>
<div class="two"><div class="spec" style="font-family:Montserrat"><b style="font-size:64px;font-weight:800">Aa</b><h4>Montserrat</h4><p style="font-weight:800;font-size:28px">ISAPUR Industrial Park</p><p>Headlines, signage, advertising. ExtraBold 800 for wordmark and headlines, SemiBold 600 for tagline and subheads.</p></div>
<div class="spec" style="font-family:Inter"><b style="font-size:64px;font-weight:500">Aa</b><h4>Inter</h4><p style="font-weight:500;font-size:28px">Plots from 300 sq.yards</p><p>Subheads, body, digital. Regular 400, Medium 500, SemiBold 600.</p></div></div>
<h4>Scale (print) """ + tag("DRAFT") + """</h4>""" + table(["Role", "Font", "Size rule"], [
    ("Hoarding headline", "Montserrat 800", "Cap height readable at 100 m: about 1 ft per 100 ft viewing distance"),
    ("Pole board tagline", "Montserrat 600", "Max 7 words, 3 lines"),
    ("Phone numbers", "Montserrat 800", "Biggest element after the logo"),
    ("Stat value", "Montserrat 700", "40 px on the poster grid"),
    ("Stat label, body", "Inter 500 / 400", "25 px on the poster, 9 to 11 pt in documents")]) +
    '<p><a class="btn" href="assets/files/IIP-fonts.zip" download>Download fonts (zip)</a></p>')

sec("voice", "Voice and tone", "draft", f"""
<p class="lead">Plain English, short sentences, numbers instead of adjectives. We state what is true and what we can show.</p>
<div class="two"><div><h4>We sound</h4>{dd(["Clear and direct.", "Confident, never loud.", "Specific: 50 ft roads, not great roads.", "Local and practical, English only."])}<h4>Words to use</h4><p>plots, approved, wide roads, power, drainage, street lighting, greenery, expressway, site visit, call.</p></div>
<div><h4>We avoid</h4>{dd(["Superlatives we cannot prove: best, world class, premium.", "Dream, luxury, lifestyle language.", "Hindi mixed into English copy (owner decision).", "Claims without a document on file (see Governance).", "Random word strings (owner rejected 'Plug in. Build up.')."], False)}</div></div>
<h4>Taglines: adaptive, not fixed</h4><p>Two approved lines. Pick the one that fits the creative, never print both together.</p>{table(["Line", "Best for"], [("A Modern Industrial Address.", "Identity first: boards, gate, hoarding, letterhead, profile covers. Says what and where."), ("The groundwork for growth.", "Benefit first: plot offers, infrastructure posts, investor and owner messages, social captions. Says why. Works with roads, drainage, lights, greenery."), ("Neither", "Pure fact posts (distance, road width, site visit) can stand with just the logo and phones.")])}<p class="small">Parked, not in use: Where Industry Moves Forward. Built for Business. Designed for Growth. The Next Address of Industry. Space for What's Next. Rejected: Plug in. Build up.</p>
<h4>Examples {tag('DRAFT')}</h4>{table(["Where", "Line"], [("Pole board", "A Modern Industrial Address. Call 9837057800 | 9219549800"), ("WhatsApp status", "Industrial plots available. Visit the site this week."), ("Social caption", "50 ft wide RCC roads, street lighting and planted greenery. IIP, Hapur-Modinagar Road."), ("Reply to a lead", "Thank you for your interest. We will share the layout map and plot list. When can you visit the site?")])}""")

sec("imagery", "Photography and imagery", "partial", f"""
<p class="lead">Real photos of the real park, in neutral daylight. No warm filters, no glow, no AI softness. Photos can be cropped into the sunburst shape.</p>
<div class="two"><div><h4>Style</h4>{dd(["Real site photos, neutral hazy daylight, true colours.", "Wide roads, gate, drainage, street lights, trees, plots staked.", "Clean crops, level horizon, no heavy grade.", "People only with consent (workers in safety gear)."])}</div>
<div><h4>Today's gap</h4><p>The warehouse picture on the pole board and poster is AI generated, not IIP. It must not imply buildings that do not exist. Replace it with real site photos.</p></div></div>
<h4>Shot list for the next shoot {tag('DRAFT')}</h4>{table(["Shot", "Why"], [("Gate and signage, straight on and from the road", "Recognition from a moving vehicle"), ("50 ft road, long lens", "Proves the road width"), ("Street lights lit at dusk", "Proves street lighting"), ("Tree-lined edge and plantation", "Proves planted greenery"), ("Drainage line and the naala outfall", "Proves drainage"), ("Plots with boundary pegs, wide", "Shows the product"), ("Drone view with the expressway side", "Shows location"), ("Pole board and hoarding in place", "Proof of presence")])}
<div class="grid">{''.join(ref(n, l) for n, l in S.SUNMOCK[:1])}</div>""")

sec("icons", "Iconography", "have", f"""
<p class="lead">Line icons on a 48 unit grid: 2.6 stroke, round caps and joins, charcoal on white. One icon per fact.</p>
<h4>Base set</h4>{grid(S.ICONS_BASE, "icons")}<h4>Park claims (added)</h4>{grid(S.ICONS_EXTRA, "icons")}""")

sec("graphic", "Graphic elements and sunburst", "have", f"""
<p class="lead">The sunburst comes from the badge. It works as an outline, a solid shape, a ring, a pattern, a photo mask and a badge. Yellow, red and green appear together as a stripe.</p>
{grid(S.PATTERN)}<h4>Sunburst as an asset type (reference)</h4><div class="grid">{''.join(ref(n, l) for n, l in S.SUNMOCK)}</div>{board(2, "Sunburst asset type board")}""")

sec("layout", "Layout and grid", "partial", f"""
<p class="lead">One logo, one line, lots of white. Safe margin 6% of the shorter side. Maximum seven words on a board.</p>
{table(["Format", "Size", "Layout rule"], [("Pole board", "20 x 32 in (5:8)", "Lockup top, tagline right aligned, phones bottom. Same size as competitor boards."), ("Hoarding", "40 x 20 ft or 40 x 15 ft", "Lockup left, one line right, phones big."), ("Poster", "1827 x 2290 px master", "3 x 2 facts grid, hero picture, 6 facility icons in a row."), ("Social", "1:1, 4:5, 9:16", "Lockup top, line, phones, stripe at the foot."), ("Stationery", "Card 3.5 x 2 in, A4", "Lockup and stripe, generous margins")])}
<h4>Poster (print master)</h4><div class="grid"><figure class="card wide"><div class="thumb"><img src="assets/ref/poster.webp" alt="IIP poster"></div><figcaption><b>Isapur Industrial Park poster</b><span>Facts grid, facilities row. Claims shown must match the claims table in Governance.</span><div class="dl"><a href="assets/files/isapur-industrial-park-poster.pdf" download>PDF</a><a href="assets/files/isapur-industrial-park-poster.svg" download>SVG editable</a></div></figcaption></figure></div>""")

sec("apps", "Applications: stationery, ID and workwear", "have", f"""
<p class="lead">Editable templates and reference mockups (raster) for stationery, ID and safety gear.</p>
{grid(S.STATIONERY)}<h4>Reference mockups</h4><div class="grid">{''.join(ref(n, l) for n, l in S.MOCKS[:7])}</div>{board(1, "Brand kit extended board")}""")

sec("signage", "Signage, hoardings and poles", "partial", f"""
<p class="lead">Boards are sized to match the competitors on the road so IIP is read as an equal, then won by white space.</p>
{grid(S.SIGNAGE)}<h4>In context</h4><div class="grid">{''.join(ref(n, l) for n, l in S.MOCKS[7:])}</div>
<div class="grid"><figure class="card wide"><div class="thumb"><img src="assets/ref/hoarding-next-to-competitors.webp" alt="Hoarding next to competitors"></div><figcaption><b>Hoarding next to competitors</b><span>Realistic composite on the real road, exact artwork, no AI drawn text.</span></figcaption></figure></div>
<p class="note">Hoarding and pole sizes are recommendations. Confirm exact panel size, bleed and material with the media owner before print. Ask the printer for a colour proof.</p>
{board(3, "Final brand kit board")}""")

sec("social", "Social media guidelines", "new", f"""
<p class="lead">Starter kit for the next phase. One profile picture everywhere, the same colours and lines, one clear call to action: call or visit.</p>
{grid(S.SOCIAL)}<h4>Sizes by platform (typical, re-check before upload)</h4>{table(["Platform", "Item", "Size", "Note"], S.SOCIAL_SPECS)}
<div class="two"><div><h4>Content pillars {tag('DRAFT')}</h4><ul><li>Site proof: roads, lights, greenery, drainage, dated photos.</li><li>Location: expressway, Modinagar, Hapur (with the distance type stated).</li><li>Approvals and papers (only documented ones).</li><li>Plot offers and site visit days.</li><li>Industry owners and neighbours (with consent).</li></ul></div>
<div><h4>Caption formula {tag('DRAFT')}</h4><p>1 fact, 1 proof, 1 action. Example: 50 ft wide RCC roads laid across the park. See them yourself, visit this week. Call 9837057800.</p><h4>Hashtags {tag('DRAFT')}</h4><p>#IsapurIndustrialPark #IIP #IndustrialPlots #ModinagarIndustrial #HapurModinagarRoad</p></div></div>
<h4>Rules</h4>{dd(["Tagline is adaptive: A Modern Industrial Address. or The groundwork for growth. Choose per post, never both.", "Profile picture is the badge only, on white.", "Never post a claim that is not VERIFIED or accepted in writing by the owner.", "Say 'straight-line' when a distance is straight-line.", "Reply to every call and message the same day.", "Real photos beat renders. Label renders as renders."])}
<p class="note">Handles, website and email are UNKNOWN today. Send them and they are added to the knowledge file and this page.</p>""")

sec("digital", "Digital and web presence", "draft", f"""
<p class="lead">Where a buyer looks after seeing the board: map, phone, WhatsApp, then a web page. Each place carries the same badge, line and numbers.</p>
{table(["Channel", "What it needs", "Status"], [("Google Business Profile", "Name, category (industrial park), address, phones, real photos, map pin on the gate", "to set up"), ("WhatsApp Business", "Profile picture, catalogue of plots, greeting message, quick replies", "to set up"), ("Website, one page", "Hero, facts grid, location map with distances, plot list, documents, call button", "to build"), ("Email signature", "Horizontal lockup, name, two phones, address", "to do"), ("QR code", "Opens the map pin or the WhatsApp chat, printed on boards and card", "to do"), ("Online listings", "Consistent name, address and phone everywhere", "to do")])}
<p class="note">{tag('DRAFT')} Proposed structure. Domain, handles and platforms are the owner's choice.</p>""")

sec("motion", "Motion", "draft", """
<p class="lead">Calm and exact, like the brand. Motion is optional and always simple.</p>
""" + table(["Rule", "Spec"], [("Style", "Fade and slide, no bounce, no spin"), ("Timing", "200 to 400 ms, ease out"), ("Logo", "Badge fades in, wordmark follows, accent line draws left to right"), ("Sunburst", "Slow scale or rotate under 10 degrees, background only"), ("Video end card", "White, lockup, tagline, phones, 3 seconds"), ("Sound", "None required")]) + '<p class="note"><span class="tg draft">DRAFT</span> Proposed. No motion assets exist yet.</p>')

sec("files", "Assets and file formats", "partial", f"""
<p class="lead">Every asset in the kit is a file you can open. SVG editable files need the fonts installed. SVG outlined files and PDFs have text converted to shapes and are safe for print shops.</p>
{table(["Folder", "What", "Open with"], [("live/", "SVG with real text", "Illustrator, Inkscape, Figma, Affinity, CorelDRAW"), ("outlined/", "SVG with text as shapes", "Anything, safe for printers"), ("export/pdf/", "Vector PDFs at true size", "Print shop"), ("export/png/", "PNG previews", "Local only"), ("editable-pptx/", "PowerPoint versions", "PowerPoint, Keynote, Canva import"), ("tokens/", "brand.tokens.json and content.json", "Text editor"), ("fonts/", "Montserrat and Inter", "Install")])}
<p><a class="btn" href="assets/files/IIP-Brand-Kit-editable.zip" download>Whole editable kit (zip)</a> <a class="btn" href="assets/files/ISAPUR-Brand-Book.pdf" download>Brand book (PDF)</a> <a class="btn" href="brief.html">Brand brief</a> <a class="btn" href="assets/files/IIP-fonts.zip" download>Fonts (zip)</a> <a class="btn" href="assets/files/brand.tokens.json" download>Tokens (JSON)</a> <a class="btn" href="assets/files/content.json" download>Content (JSON)</a></p>
<p class="note">Images shown on this page are WEBP. Masters stay local. Original badge vector from the designer would replace the trace.</p>""")

sec("facts", "Park facts sheet", "have", f"""
<p class="lead">The facts every post, board and reply should use. Distances are straight-line from an approximate pin (about 200 m) until a driven distance is measured.</p>
<h4>Identity</h4>{table(["Item", "Value"], [("Name", "ISAPUR INDUSTRIAL PARK (IIP)"), ("Address line", CT["address"]), ("Phones", " | ".join(CT["phones"])), ("Language", "English only"), ("Tagline", CT["tagline_one_line"])])}
<h4>Distances</h4>{table(["To", "Straight-line", "Driving"], S.DISTANCES)}
<h4>Competitors on the road</h4>{table(["Park", "Where", "What we see"], S.COMPETITORS)}
<p class="note">Full detail, sources and change history live in the central knowledge file <code>00_ISAPUR_KNOWLEDGE.md</code>.</p>""")

sec("governance", "Governance, claims and updates", "draft", f"""
<p class="lead">Nothing goes on a printed board unless its proof is on file or the owner accepts the risk in writing.</p>
{table(["Claim", "Status", "Proof to file"], [(c, tag(s), p) for c, s, p in S.CLAIMS])}
<div class="two"><div><h4>Approvals {tag('DRAFT')}</h4><ul><li>Owner approves every new asset and claim.</li><li>Claims checked against the table above before print.</li><li>Printer proof signed before bulk print.</li></ul></div>
<div><h4>Versioning</h4><ul><li>This kit is v{VERSION}, {TODAY}.</li><li>Words, phones, address: edit tokens/content.json and rebuild.</li><li>Colours and fonts: edit tokens/brand.tokens.json and rebuild.</li><li>All decisions are logged in the central knowledge file.</li></ul></div></div>""")

rows = []
for r in RES:
    st = r["iip_status"]; src = " ".join(f'<a href="{u}">source</a>' for u in r.get("sources", [])[:3])
    rows.append((r["title"], r["why"], ", ".join(r["contains"][:5]), tag({"have": "HAVE", "partial": "PARTIAL", "missing": "NEW"}[st]), src))
sec("research", "Research behind this kit", "have", f"""
<p class="lead">What a complete brand kit contains, from public guides, and how IIP covers each part. Sources agree on 15 to 17 sections. Findings are reported from search results, not full page reviews.</p>
{table(["Section", "Why", "Contains", "IIP", "Sources"], rows)}
<p><a class="btn" href="assets/files/brand-kit-anatomy.md" download>Research notes (markdown)</a></p>
<p class="note">No published industrial park brand manual with hoarding specs was found. Signage guidance above is adapted from general signage manuals and the owner's field photos.</p>""")

# ---------- files ----------
FONTS = KIT / "fonts"
import zipfile
with zipfile.ZipFile(A / "files/IIP-fonts.zip", "w", zipfile.ZIP_DEFLATED) as z:
    for f in sorted(FONTS.glob("*")):
        if f.suffix.lower() in (".ttf", ".txt"): z.write(f, f.name)
with zipfile.ZipFile(A / "files/IIP-Brand-Kit-editable.zip", "w", zipfile.ZIP_DEFLATED) as z:   # the whole editable kit
    for sub in ("live", "outlined", "export/pdf", "editable-pptx", "tokens", "fonts"):
        for f in sorted((KIT / sub).rglob("*")):
            if f.is_file(): z.write(f, "IIP-Brand-Kit/" + f.relative_to(KIT).as_posix())
    z.write(KIT / "README.md", "IIP-Brand-Kit/README.md")
for f in ("Montserrat-ExtraBold.ttf", "Montserrat-SemiBold.ttf", "Inter-Regular.ttf", "Inter-Medium.ttf"): shutil.copy(FONTS / f, A / "fonts" / f)
shutil.copy(KIT / "tokens/brand.tokens.json", A / "files"); shutil.copy(KIT / "tokens/content.json", A / "files")
shutil.copy(KIT / "research/brand-kit-anatomy.md", A / "files")
PD = ROOT / "Isapur-Poster/03_Design"
shutil.copy(PD / "00_LATEST_isapur-industrial-park.pdf", A / "files/isapur-industrial-park-poster.pdf")
shutil.copy(PD / "01_LATEST_isapur-industrial-park.svg", A / "files/isapur-industrial-park-poster.svg")
Image.open(PD / "02_LATEST_preview.png").convert("RGB").save(A / "ref/poster.webp", quality=82, method=6)
shutil.copy(KIT / "05_Mockups/hoarding-next-to-competitors.jpg", A / "ref/_h.jpg")
Image.open(A / "ref/_h.jpg").convert("RGB").save(A / "ref/hoarding-next-to-competitors.webp", quality=82, method=6); (A / "ref/_h.jpg").unlink()

# ---------- page ----------
CSS = (pathlib.Path(__file__).resolve().parent / "site.css").read_text(encoding="utf-8")
nav = "".join(f'<li><a href="#{i}"><span>{n:02d}</span>{e(t)}</a></li>' for n, (i, t, s, b) in enumerate(SEC, 1))
body = "".join(f'<section id="{i}"><header><span class="num">{n:02d}</span><h2>{e(t)}</h2>{tag({"have": "Have", "partial": "Partial", "new": "New", "draft": "Draft"}[s])}</header>{b}</section>' for n, (i, t, s, b) in enumerate(SEC, 1))
fontface = "".join(f"@font-face{{font-family:'{fam}';font-weight:{w};src:url('assets/fonts/{f}')}}" for fam, w, f in
                   (("Montserrat", 800, "Montserrat-ExtraBold.ttf"), ("Montserrat", 600, "Montserrat-SemiBold.ttf"), ("Inter", 400, "Inter-Regular.ttf"), ("Inter", 500, "Inter-Medium.ttf")))
page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>ISAPUR Brand Kit</title><meta name="description" content="Brand kit for Isapur Industrial Park: logo, colour, type, icons, applications, signage, social and governance, with downloadable assets.">
<style>{fontface}{CSS}</style></head><body>
<aside id="side"><a class="brand" href="#top"><img src="assets/p/logo-badge-only.webp" alt=""><b>ISAPUR</b><small>Brand kit v{VERSION}</small></a><nav><ol>{nav}</ol></nav>
<p class="side-foot">Central facts: <code>00_ISAPUR_KNOWLEDGE.md</code><br>Updated {TODAY}</p></aside>
<main id="top"><div class="hero"><img src="assets/p/logo-primary-vertical.webp" alt="ISAPUR Industrial Park logo"><div><p class="eyebrow">Brand kit, version {VERSION}</p><h1>ISAPUR Industrial Park</h1><p class="lead">The groundwork for growth. Everything needed to make, check and post on-brand work: rules on the left, assets next to them, files ready to download.</p>
<p><a class="btn" href="#logo">Start with the logo</a> <a class="btn ghost" href="#files">All downloads</a></p>
<p class="small">{tag('Have')} complete &nbsp; {tag('Partial')} needs inputs &nbsp; {tag('New')} added for social &nbsp; {tag('Draft')} proposed, owner to confirm</p></div></div>
{body}<footer>ISAPUR Industrial Park brand kit v{VERSION}, {TODAY}. Logo is never changed. English only. Phones {" | ".join(CT["phones"])}.</footer></main></body></html>"""
(SITE / "index.html").write_text(page, encoding="utf-8")
print("site", len(page) // 1024, "KB", sum(f.stat().st_size for f in SITE.rglob("*") if f.is_file()) // 1024, "KB total")
