"""Builds the single page brand kit: Brand-Kit/site/index.html (+ site/assets).  Run: python Brand-Kit/_build/build_site.py
Inputs: tokens, research/, live/ outlined/ export/ reference/, Isapur-Poster PDF, _build/parts/print_guide.html.  Words live in site_content.py."""
import json, pathlib, shutil, sys, html, datetime, zipfile
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from PIL import Image
import site_content as S

KIT = pathlib.Path(__file__).resolve().parents[1]
ROOT = KIT.parent
SITE = KIT / "site"; A = SITE / "assets"
TOK = json.loads((KIT / "tokens/brand.tokens.json").read_text())
CT = json.loads((KIT / "tokens/content.json").read_text())
RES = json.loads((KIT / "research/sections.json").read_text())
PC = json.loads((KIT / "research/print-colors.json").read_text())["colors"]
VERSION = "1.1"; TODAY = datetime.date.today().isoformat()
e = html.escape
T1, T2 = CT["taglines"]["approved"]

SITE.mkdir(exist_ok=True)
for c in SITE.iterdir(): shutil.rmtree(c) if c.is_dir() else c.unlink()   # keep the folder itself (a shell may be inside it)
for d in ("p", "svg", "svg-live", "pdf", "fonts", "ref", "files"): (A / d).mkdir(parents=True, exist_ok=True)


# ---------- asset plumbing ----------
def thumb(png, name, long=1100):
    im = Image.open(png).convert("RGBA"); k = min(1, long / max(im.size))
    if k < 1: im = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
    im.save(A / "p" / f"{name}.webp", quality=84, method=6)


def prep(stem, folder):
    png = KIT / "export/png" / f"{stem}.png"
    if png.exists(): thumb(png, stem, 1800 if ("hoarding" in stem or "master" in stem) else 1200)
    for src, dst in ((KIT / "outlined" / folder / f"{stem}.svg", "svg"), (KIT / "live" / folder / f"{stem}.svg", "svg-live"), (KIT / "export/pdf" / f"{stem}.pdf", "pdf")):
        if src.exists(): shutil.copy(src, A / dst / src.name)


def card(a):
    stem, folder, label, note = a; prep(stem, folder)
    if not (A / "svg" / f"{stem}.svg").exists(): return ""            # asset not built yet, skip quietly
    links = "".join(f'<a href="assets/{d}/{stem}.{x}" download>{n}</a>' for d, x, n in
                    (("svg", "svg", "SVG"), ("svg-live", "svg", "SVG editable"), ("pdf", "pdf", "PDF")) if (A / d / f"{stem}.{x}").exists())
    img = f'<img src="assets/p/{stem}.webp" alt="{e(label)}">' if (A / "p" / f"{stem}.webp").exists() else ""
    return f'<figure class="card"><div class="thumb">{img}</div><figcaption><b>{e(label)}</b><span>{e(note)}</span><div class="dl">{links}</div></figcaption></figure>'


def grid(items, cls=""): return f'<div class="grid {cls}">' + "".join(card(a) for a in items) + "</div>"


def ref(name, label, cls="", note=""):
    src = KIT / "reference/mockups" / f"{name}.webp"
    if not src.exists(): return ""
    shutil.copy(src, A / "ref" / f"{name}.webp")
    return f'<figure class="card {cls}"><div class="thumb"><img src="assets/ref/{name}.webp" alt="{e(label)}"></div><figcaption><b>{e(label)}</b><span>{e(note)}</span></figcaption></figure>'


# ---------- colour maths ----------
def rgb(h): h = h.lstrip("#"); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
def lum(c):
    f = lambda v: (v / 255 / 12.92) if v / 255 <= 0.03928 else (((v / 255 + 0.055) / 1.055) ** 2.4)
    r, g, b = (f(x) for x in c); return 0.2126 * r + 0.7152 * g + 0.0722 * b
def contrast(a, b): la, lb = sorted((lum(rgb(a)), lum(rgb(b))), reverse=True); return (la + 0.05) / (lb + 0.05)


MAIN = [("white", "Primary board and page background"), ("charcoal", "Text, contrast, wordmark"), ("yellow", "Highlight, stripe, call to action"),
        ("red", "Accent line and highlight only"), ("green", "Secondary: stripe, back of cards, sustainability"), ("mist", "Surfaces, panels, subtle sunburst")]
SUPPORT = [("light gray", "Hairlines, panels"), ("dark gray", "Secondary text"), ("gray", "Disabled, borders")]


def sw(name, use):
    c = PC[name]; h = c["hex"]; kk = c["cmyk"]
    badge = {"close match": "ok", "slightly duller on press": "mid"}.get(c["verdict"], "low")
    return (f'<div class="s"><div class="chips"><i style="background:{h}"></i><i style="background:{c["on_press_hex"]}" title="Approximate look on press"></i></div>'
            f'<b>{e(name.title())}</b><code>{h}</code><span>RGB {", ".join(map(str, c["rgb"]))}</span>'
            f'<span class="cm">CMYK {kk[0]} / {kk[1]} / {kk[2]} / {kk[3]}</span><span class="v {badge}">{e(c["verdict"])}</span><em>{e(use)}</em></div>')


def swatches(items): return '<div class="sw">' + "".join(sw(n, u) for n, u in items if n in PC) + "</div>"


PAIRS = [("charcoal", "white"), ("charcoal", "yellow"), ("charcoal", "mist"), ("white", "charcoal"), ("white", "green"), ("yellow", "charcoal"), ("yellow", "green"), ("red", "white"), ("white", "red")]
def pairs():
    out = '<div class="pairs">'
    for fg, bg in PAIRS:
        fh, bh = PC[fg]["hex"], PC[bg]["hex"]; r = contrast(fh, bh)
        verdict = "Text and large" if r >= 4.5 else "Large text only" if r >= 3 else "Do not use"
        out += f'<div class="p" style="background:{bh};color:{fh}"><b>Aa</b><span>{fg} on {bg}</span><em>{r:.1f}:1, {verdict}</em></div>'
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

sec("story", "Brand story and positioning", "have", f"""
<p class="lead">Isapur Industrial Park is a modern industrial address on the Hapur-Modinagar Road for local manufacturers who want a clear, legal, well laid plot without noise.</p>
<div class="two"><div><h4>Name</h4><p>The name is <b>Isapur Industrial Park</b>, short form <b>IIP</b>. The developer is not named in any public material.</p>
<h4>Positioning</h4><p>For factory owners and small industrial buyers along the Hapur-Modinagar Road, IIP is the industrial park that says less and shows more: wide roads, clean papers, a name you can read from a moving vehicle.</p>
<h4>Promise</h4><p>Plots you can verify. Facilities we can show. One number to call.</p><h4>Taglines, adaptive</h4><p class="big">{e(T1)}</p><p class="big">{e(T2)}</p></div>
<div><h4>Audience</h4><p>Primary: local factory owners and small industrial buyers. Secondary candidates: warehouse and logistics operators, investors, brokers.</p>
<h4>Personality</h4><p>Calm, exact, modern, trustworthy. A planner, not a salesman.</p><h4>What makes us different on this road</h4><p>Competitor boards use navy, gold or red, dense copy, stamps and rendered townships. IIP uses white space, one logo and one line, so it is read first and remembered.</p></div></div>""")

sec("logo", "Logo system", "have", f"""
<p class="lead">The badge is never changed, recoloured or redrawn. Every lockup uses the same badge and the Montserrat ExtraBold wordmark.</p>
<div class="two"><div><h4>Construction</h4><ul><li><b>Brand mark</b>: the rosette badge (sunburst, IiP monogram, circuit dots).</li><li><b>Logotype</b>: the IiP monogram alone.</li><li><b>Wordmark</b>: ISAPUR over INDUSTRIAL PARK.</li><li><b>Accent line</b>: the red rule beside INDUSTRIAL PARK in the vertical lockup.</li></ul></div>
<div><h4>Source</h4><p>No vector original exists. The badge is a traced vector of the supplied artwork, good up to hoarding size. Find the designer's original for very large or very close print.</p></div></div>
{grid(S.LOGO)}<h4>Monotone use</h4><p>For one colour jobs: newspaper, stamp, embossing, engraving, a single colour print, or a dark background.</p>{grid(S.MONO)}""")

sec("misuse", "Logo usage: space, size and misuse", "have", f"""
<p class="lead">Keep the logo clear, readable and untouched.</p>
<div class="two"><div><h4>Do</h4>{dd(["Use approved lockups only.", "Keep clear space and minimum size.", "Use brand colours as per the palette.", "Use Montserrat for headlines, Inter for body.", "Put the logo on white, mist gray or charcoal."])}</div>
<div><h4>Do not</h4>{dd(["Change the logo colours.", "Distort, stretch or rotate the logo.", "Add outlines, shadows or effects.", "Place it on low contrast or busy backgrounds.", "Rebuild the wordmark in another typeface."], False)}</div></div>
{grid(S.GUIDES, "wideimg")}""")

sec("colour", "Colour system and print colours", "have", f"""
<p class="lead">White first, charcoal for text, yellow for highlight, red as a thin accent, deep green as the quiet secondary. The badge keeps its own measured colours (yellow #FEF102, red #EE1D23, green #00A54F) and is never retinted.</p>
<div class="strip"><i style="background:#fff;flex:70;border:1px solid var(--line)"></i><i style="background:#F2F4F6;flex:6"></i><i style="background:#111827;flex:14"></i><i style="background:#FFD600;flex:6"></i><i style="background:#E53935;flex:2"></i><i style="background:#0F4D3A;flex:2"></i></div>
<p class="small">Proportion guide: about 70% white, 6% mist, 14% charcoal, 6% yellow, 2% red, 2% green. Red is a line, not a block.</p>
<h4>Core palette: screen colour and how it prints</h4>{swatches(MAIN)}
<p class="note">Each swatch shows two chips: the screen colour (left) and its approximate look on press (right), converted through the US Web Coated SWOP profile. CMYK values are a starting point for the printer. Yellow, red and the badge colours print close to screen. Charcoal and deep green print darker and duller, so approve a printer proof and tune from it.</p>
<h4>Supporting neutrals</h4>{swatches(SUPPORT)}<h4>Badge colours (never retint)</h4>{swatches([("badge yellow", "Badge artwork"), ("badge red", "Badge artwork"), ("badge green", "Badge artwork")])}
<h4>Colour pairs</h4>{pairs()}
<div class="two"><div><h4>Print rules</h4>{dd(["Small black text: 100% K only, never four colour black.", "Large dark areas (hoarding background): rich black, for example C60 M50 Y40 K100, ask the printer.", "Deep green is a murky CMYK mix. For stationery ask for a spot match.", "Always approve a printed proof before bulk print.", "Flex, vinyl and paper print each colour a little differently."])}</div>
<div><h4>Screen rules</h4>{dd(["Use the hex values on screens.", "Charcoal text on white passes contrast (about 17:1).", "White on red is for large text only.", "Yellow needs charcoal text, never white."])}</div></div>""")

sec("type", "Typography", "have", """
<p class="lead">Two free families (SIL Open Font License, free for commercial use).</p>
<div class="two"><div class="spec" style="font-family:Montserrat"><b style="font-size:72px;font-weight:800">Aa</b><h4>Montserrat</h4><p style="font-weight:800;font-size:26px;line-height:1.2">ISAPUR Industrial Park<br>ABCDEFGHIJKLMNOPQRSTUVWXYZ<br>0123456789</p><p>Headlines, signage, advertising. ExtraBold 800 for wordmark and headlines, SemiBold 600 for taglines and subheads.</p></div>
<div class="spec" style="font-family:Inter"><b style="font-size:72px;font-weight:500">Aa</b><h4>Inter</h4><p style="font-weight:500;font-size:26px;line-height:1.2">Plots from 300 sq.yards<br>abcdefghijklmnopqrstuvwxyz<br>0123456789</p><p>Subheads, body, digital. Regular 400, Medium 500, SemiBold 600.</p></div></div>
<h4>Hierarchy example</h4><div class="spec hier"><small>INDUSTRIAL PLOTS</small><b>The Groundwork for Growth.</b><p>50 ft wide RCC roads, street lighting and planted greenery on the Hapur-Modinagar Road.</p><strong>9837057800 | 9219549800</strong></div>
<h4>Scale (print)</h4>""" + table(["Role", "Font", "Size rule"], [
    ("Hoarding headline", "Montserrat 800", "Cap height readable at 100 m: about 1 ft per 100 ft viewing distance"),
    ("Pole board tagline", "Montserrat 600", "Max 7 words, 3 lines"), ("Phone numbers", "Montserrat 800", "Biggest element after the logo"),
    ("Stat value", "Montserrat 700", "40 px on the poster grid"), ("Stat label, body", "Inter 500 / 400", "25 px on the poster, 9 to 11 pt in documents")]) +
    '<p><a class="btn" href="assets/files/IIP-fonts.zip" download>Download fonts (zip)</a></p>')

sec("voice", "Voice and tone", "have", f"""
<p class="lead">Plain English, short sentences, numbers instead of adjectives. We state what is true and what we can show.</p>
<div class="two"><div><h4>We sound</h4>{dd(["Clear and direct.", "Confident, never loud.", "Specific: 50 ft roads, not great roads.", "Local and practical, English only."])}<h4>Words to use</h4><p>plots, approved, wide roads, power, drainage, street lighting, greenery, expressway, site visit, call.</p></div>
<div><h4>We avoid</h4>{dd(["Superlatives we cannot prove: best, world class, premium.", "Dream, luxury, lifestyle language.", "Hindi mixed into English copy (owner decision).", "Claims without a document on file (see Governance).", "Random word strings (owner rejected one earlier line)."], False)}</div></div>
<h4>Taglines: adaptive, not fixed</h4><p>Two approved lines. Pick the one that fits the creative, never print both together.</p>{table(["Line", "Best for"], [(T1, "Identity first: boards, gate, hoarding, letterhead, profile covers. Says what and where."), (T2, "Benefit first: plot offers, infrastructure posts, owner and investor messages, captions. Says why. Works with roads, drainage, lights, greenery."), ("Neither", "Pure fact posts (distance, road width, site visit) can stand with just the logo and phones.")])}
<p class="small">Parked, not in use: Where Industry Moves Forward. Built for Business. Designed for Growth. The Next Address of Industry. Space for What's Next.</p>
<h4>Examples</h4>{table(["Where", "Line"], [("Pole board", f"{T2} Call 9837057800 | 9219549800"), ("WhatsApp status", "Industrial Plots Available. Visit the site this week."), ("Social caption", "50 ft wide RCC roads, street lighting and planted greenery. IIP, Hapur-Modinagar Road."), ("Reply to a lead", "Thank you for your interest. We will share the layout map and plot list. When can you visit the site?")])}""")

sec("imagery", "Photography direction and shoot plan", "have", f"""
<p class="lead">There is no photography yet. This is the plan for the first shoot: real photos of the real park, in neutral daylight. No warm filters, no glow, no AI softness. Photos can be cropped into the sunburst shape.</p>
<div class="two"><div><h4>Style</h4>{dd(["Real site photos, neutral hazy daylight, true colours.", "Wide roads, gate, drainage, street lights, trees, plots staked.", "Clean crops, level horizon, no heavy grade.", "People only with consent (workers in safety gear)."])}</div>
<div><h4>Until then</h4><p>Boards and posts use the logo, sunburst, stripe and type only. No building or warehouse picture is used, because none of it exists yet.</p></div></div>
<h4>Shot list for the first shoot</h4>{table(["Shot", "Why"], [("Gate and signage, straight on and from the road", "Recognition from a moving vehicle"), ("50 ft road, long lens", "Proves the road width"), ("Street lights lit at dusk", "Proves street lighting"), ("Tree-lined edge and plantation", "Proves planted greenery"), ("Drainage line and the naala outfall", "Proves drainage"), ("Plots with boundary pegs, wide", "Shows the product"), ("Drone view with the expressway side", "Shows location"), ("Pole board and hoarding in place", "Proof of presence")])}""")

sec("icons", "Iconography", "have", f"""
<p class="lead">Line icons on a 48 unit grid: 2.4 stroke, round caps and joins, charcoal on white, at most two detail strokes. One icon per fact. All 24 icons share one drawing style.</p>
{grid(S.ICONS_ALL, "icons")}""")

sec("graphic", "Graphic elements and sunburst", "have", f"""
<p class="lead">The sunburst comes from the badge. It works as an outline, a solid shape, a ring, a pattern and a badge. Yellow, red and green appear together as a stripe. Every element is an independent SVG, and all assets are also in one master file.</p>
{grid(S.PATTERN)}<p><a class="btn" href="assets/files/IIP-master-assets.svg" download>Master file, every SVG asset (one file)</a></p>""")

sec("layout", "Layout and grid", "have", f"""
<p class="lead">One logo, one line, lots of white. Safe margin 6% of the shorter side. Maximum seven words on a board. Diagrams with trim, bleed and safe markings for every format are in the Print guide that follows.</p>
{table(["Format", "Size", "Layout rule"], [("Pole board", "20 x 32 in (5:8)", "Lockup top, tagline right aligned, phones bottom. Same size as competitor boards."), ("Hoarding", "40 x 20 ft or 40 x 15 ft", "Lockup left, one line right, phones big."), ("Poster", "1827 x 2290 px master", "3 x 2 facts grid, 6 facility icons in a row."), ("Social", "1:1, 4:5, 9:16", "Lockup top, line, phones, stripe at the foot."), ("Stationery", "Card 3.5 x 2 in, A4", "Lockup and stripe, generous margins")])}
<h4>Poster (print master)</h4><div class="grid"><figure class="card wide"><div class="thumb"><img src="assets/ref/poster.webp" alt="IIP poster"></div><figcaption><b>Isapur Industrial Park poster</b><span>Facts grid and facilities row. Claims shown must match the claims table in Governance.</span><div class="dl"><a href="assets/files/isapur-industrial-park-poster.pdf" download>PDF</a><a href="assets/files/isapur-industrial-park-poster.svg" download>SVG editable</a></div></figcaption></figure></div>""")

PG = KIT / "_build/parts/print_guide.html"
sec("print", "Print guide: bleed, trim, safe zone and file prep", "new",
    '<p class="lead">Read this before sending any file to a printer. It explains bleed and the other terms in plain English, with marked diagrams for every IIP format.</p>' +
    (PG.read_text(encoding="utf-8") if PG.exists() else '<p class="note">Print guide fragment missing.</p>'))

sec("apps", "Applications: stationery, ID and workwear", "have", f"""
<p class="lead">Every piece is an editable vector file at true size. Business cards come in two wordmark styles: vertical and horizontal.</p>
{grid(S.STATIONERY)}<h4>Flat lay</h4><div class="grid">{ref("flatlay-stationery", "Stationery set", "wide", "Exact artwork on a neutral surface")}</div>""")

sec("signage", "Signage, hoardings and poles", "have", f"""
<p class="lead">Boards are sized to match the competitors on the road so IIP is read as an equal, then won by white space. Two tagline variants for each major board. No photographs, because none exist yet.</p>
{grid(S.SIGNAGE)}<h4>In context</h4><div class="grid">{''.join(ref(n, l, "", "Concept reference from the owner's board") for n, l in S.CONTEXT)}</div>
<div class="grid">{''.join(ref(f.stem, f.stem.replace("ctx-", "").replace("-", " ").title(), "wide", "Exact artwork composited on the real road") for f in sorted((KIT / "reference/mockups").glob("ctx-*.webp")))}</div>
<p class="note">Hoarding and pole sizes are recommendations. Confirm exact panel size, bleed and material with the media owner before print. Ask the printer for a colour proof.</p>""")

sec("social", "Social media guidelines", "new", f"""
<p class="lead">Starter kit for the next phase. One profile picture everywhere, the same colours and lines, one clear call to action: call or visit.</p>
{grid(S.SOCIAL)}<h4>Sizes by platform (typical, re-check before upload)</h4>{table(["Platform", "Item", "Size", "Note"], S.SOCIAL_SPECS)}
<div class="two"><div><h4>Content pillars {tag('To decide')}</h4><p>To be decided after the corrections, with ChatGPT's help. Candidates: site proof, location, approvals, plot offers, neighbours.</p></div>
<div><h4>Hashtags {tag('To research')}</h4><p>Open todo: research with an Apify actor, then choose. The owner supplies the API key as an environment variable. Nothing is chosen yet.</p></div></div>
<h4>Rules</h4>{dd(["Tagline is adaptive: choose one line per post, never both.", "Profile picture is the badge only, on white.", "Never post a claim that is not verified or accepted in writing by the owner.", "Say straight-line or driving when you give a distance.", "Reply to every call and message the same day.", "Real photos only once they exist. Never show an AI picture as the park."])}""")

sec("digital", "Digital and web presence", "next", """
<p class="lead">All online presence is to be built in the next phase. This section only lists where it will live.</p>
""" + table(["Channel", "Plan"], [("Google Business Profile", "Next phase"), ("WhatsApp Business", "Next phase"), ("Website, one page", "Next phase"), ("Social profiles", "Next phase, handles to be confirmed"), ("Email signature and QR code", "Template ready in the stationery set, set up in the next phase")]))

sec("motion", "Motion", "parked", """
<p class="lead">Calm and exact, like the brand. Motion is optional and always simple. Experiments are parked until the owner has a free day.</p>
""" + table(["Rule", "Spec"], [("Style", "Fade and slide, no bounce, no spin"), ("Timing", "200 to 400 ms, ease out"), ("Logo", "Badge fades in, wordmark follows, accent line draws left to right"), ("Sunburst", "Slow scale or rotate under 10 degrees, background only"), ("Video end card", "White, lockup, tagline, phones, 3 seconds")]))

sec("files", "Assets and file formats", "have", f"""
<p class="lead">Every asset is a file you can open. Editable SVG files need the fonts installed. Outlined SVG files and PDFs have text converted to shapes and are safe for print shops. Each asset is an independent file, and one master file holds all of them.</p>
{table(["Folder", "What", "Open with"], [("live/", "SVG with real text", "VectorCraft (free, open source, ArtCraft family), Inkscape, Figma, Affinity, Illustrator, CorelDRAW"), ("outlined/", "SVG with text as shapes", "VectorCraft, Inkscape or any browser, safe for printers"), ("IIP-master-assets.svg", "Every SVG asset in one file", "VectorCraft, Inkscape, Illustrator, Figma"), ("export/pdf/", "Vector PDFs at true size", "Print shop, any PDF viewer, VectorCraft"), ("editable-pptx/", "PowerPoint versions", "PowerPoint, Keynote, Canva import"), ("tokens/", "brand.tokens.json and content.json", "Text editor"), ("fonts/", "Montserrat and Inter", "Install")])}
<p><a class="btn" href="assets/files/IIP-Brand-Kit-editable.zip" download>Whole editable kit (zip)</a> <a class="btn" href="assets/files/IIP-master-assets.svg" download>Master SVG</a> <a class="btn" href="assets/files/ISAPUR-Brand-Book.pdf" download>Brand book (PDF)</a> <a class="btn" href="brief.html">Brand brief</a> <a class="btn" href="assets/files/IIP-fonts.zip" download>Fonts (zip)</a> <a class="btn" href="assets/files/brand.tokens.json" download>Tokens (JSON)</a> <a class="btn" href="assets/files/content.json" download>Content (JSON)</a></p>
<p class="note">Images shown on this page are WEBP. Masters stay local. An original badge vector from the designer would replace the trace.</p>""")

sec("facts", "Park facts sheet", "have", f"""
<p class="lead">The facts every post, board and reply should use. Driving distances come from Google Maps (2026-11-06, live traffic, from an approximate pin). Straight-line distances are shown for reference.</p>
<h4>Identity</h4>{table(["Item", "Value"], [("Name", "Isapur Industrial Park (IIP)"), ("Address line", CT["address"]), ("Phones", " | ".join(CT["phones"])), ("Language", "English only"), ("Taglines", f"{T1}  /  {T2}")])}
<h4>Distances</h4>{table(["To", "Driving", "Straight-line"], S.DISTANCES)}
<h4>Competitors on the road</h4>{table(["Park", "Where", "What we see"], S.COMPETITORS)}
<p class="note">Full detail, sources and change history live in the central knowledge file <code>00_ISAPUR_KNOWLEDGE.md</code>.</p>""")

sec("governance", "Governance, claims and updates", "have", f"""
<p class="lead">Nothing goes on a printed board or post unless its proof is on file or the owner accepts the risk in writing.</p>
{table(["Claim", "Status", "Proof to file"], [(c, tag(s), p) for c, s, p in S.CLAIMS])}
<div class="two"><div><h4>Approvals</h4><ul><li>Owner approves every new asset and claim.</li><li>Claims checked against the table above before print.</li><li>Printer proof signed before bulk print.</li></ul></div>
<div><h4>Versioning</h4><ul><li>This kit is v{VERSION}, {TODAY}.</li><li>Words, phones, address, taglines: edit tokens/content.json and rebuild.</li><li>Colours and fonts: edit tokens/brand.tokens.json and rebuild.</li><li>All decisions are logged in the central knowledge file, open work in TODOS.md.</li></ul></div></div>
<h4>Use of AI</h4><p>The kit is deliberately hand-crafted so it keeps a distinct character that generic AI tools cannot easily copy. AI generated assets are a later phase (phase 3) and live in their own folder, never mixed into the kit. Logo and text are always composited from the real vector files, never drawn by a model.</p>""")

rows = []
for r in RES:
    st = r["iip_status"]; src = " ".join(f'<a href="{u}">source</a>' for u in r.get("sources", [])[:3])
    rows.append((r["title"], r["why"], ", ".join(r["contains"][:5]), tag({"have": "HAVE", "partial": "PARTIAL", "missing": "NEW"}[st]), src))
sec("research", "Research behind this kit", "have", f"""
<p class="lead">What a complete brand kit contains, from public guides, and how IIP covers each part. Sources agree on 15 to 17 sections. Findings are reported from search results, not full page reviews.</p>
{table(["Section", "Why", "Contains", "IIP", "Sources"], rows)}
<p><a class="btn" href="assets/files/brand-kit-anatomy.md" download>Research notes (markdown)</a></p>
<p class="note">No published industrial park brand manual with hoarding specs was found. Signage guidance is adapted from general signage manuals and the owner's field photos.</p>""")

# ---------- files ----------
FONTS = KIT / "fonts"
with zipfile.ZipFile(A / "files/IIP-fonts.zip", "w", zipfile.ZIP_DEFLATED) as z:
    for f in sorted(FONTS.glob("*")):
        if f.suffix.lower() in (".ttf", ".txt"): z.write(f, f.name)
for f in ("Montserrat-ExtraBold.ttf", "Montserrat-SemiBold.ttf", "Inter-Regular.ttf", "Inter-Medium.ttf"): shutil.copy(FONTS / f, A / "fonts" / f)
if (KIT / "IIP-master-assets.svg").exists(): shutil.copy(KIT / "IIP-master-assets.svg", A / "files/IIP-master-assets.svg")
with zipfile.ZipFile(A / "files/IIP-Brand-Kit-editable.zip", "w", zipfile.ZIP_DEFLATED) as z:   # the whole editable kit
    for sub in ("live", "outlined", "export/pdf", "editable-pptx", "tokens", "fonts"):
        for f in sorted((KIT / sub).rglob("*")):
            if f.is_file(): z.write(f, "IIP-Brand-Kit/" + f.relative_to(KIT).as_posix())
    for extra in ("README.md", "IIP-master-assets.svg"):
        if (KIT / extra).exists(): z.write(KIT / extra, "IIP-Brand-Kit/" + extra)
shutil.copy(KIT / "tokens/brand.tokens.json", A / "files"); shutil.copy(KIT / "tokens/content.json", A / "files")
shutil.copy(KIT / "research/brand-kit-anatomy.md", A / "files")
PD = ROOT / "Isapur-Poster/03_Design"
shutil.copy(PD / "00_LATEST_isapur-industrial-park.pdf", A / "files/isapur-industrial-park-poster.pdf")
shutil.copy(PD / "01_LATEST_isapur-industrial-park.svg", A / "files/isapur-industrial-park-poster.svg")
Image.open(PD / "02_LATEST_preview.png").convert("RGB").save(A / "ref/poster.webp", quality=84, method=6)
for n in ("logo-badge-only", "logo-primary-vertical", "sunburst-outline", "sunburst-solid-yellow"):
    p = KIT / "export/png" / f"{n}.png"
    if p.exists(): thumb(p, n)

# ---------- page ----------
CSS = (pathlib.Path(__file__).resolve().parent / "site.css").read_text(encoding="utf-8")
LABEL = {"have": "Ready", "partial": "Partial", "new": "New", "draft": "Draft", "next": "Next phase", "parked": "Parked"}
nav = "".join(f'<li><a href="#{i}"><span>{n:02d}</span>{e(t)}</a></li>' for n, (i, t, s, b) in enumerate(SEC, 1))
body = "".join(f'<section id="{i}"><header><span class="num">{n:02d}</span><h2>{e(t)}</h2>{tag(LABEL[s])}</header><div class="bar"><i></i><i></i><i></i></div>{b}</section>' for n, (i, t, s, b) in enumerate(SEC, 1))
fontface = "".join(f"@font-face{{font-family:'{fam}';font-weight:{w};src:url('assets/fonts/{f}')}}" for fam, w, f in
                   (("Montserrat", 800, "Montserrat-ExtraBold.ttf"), ("Montserrat", 600, "Montserrat-SemiBold.ttf"), ("Inter", 400, "Inter-Regular.ttf"), ("Inter", 500, "Inter-Medium.ttf")))
page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>ISAPUR Brand Kit</title><meta name="description" content="Brand kit for Isapur Industrial Park: logo, colour, type, icons, applications, signage, print guide, social and governance, with downloadable assets.">
<style>{fontface}{CSS}</style></head><body>
<aside id="side"><a class="brand" href="#top"><img src="assets/p/logo-badge-only.webp" alt=""><b>ISAPUR</b><small>Brand kit v{VERSION}</small></a><nav><ol>{nav}</ol></nav>
<p class="side-foot">Central facts: <code>00_ISAPUR_KNOWLEDGE.md</code><br>Updated {TODAY}</p></aside>
<main id="top"><div class="hero"><img src="assets/p/logo-primary-vertical.webp" alt="ISAPUR Industrial Park logo"><div><p class="eyebrow">Brand kit, version {VERSION}</p><h1>Isapur Industrial Park</h1><p class="lead">{e(T2)} Everything needed to make, check and post on-brand work: rules on the left, assets next to them, files ready to download.</p>
<p><a class="btn" href="#logo">Start with the logo</a> <a class="btn ghost" href="#files">All downloads</a></p>
<p class="small">{tag('Ready')} complete &nbsp; {tag('Partial')} needs inputs &nbsp; {tag('New')} added &nbsp; {tag('Next phase')} to be built &nbsp; {tag('Parked')} later</p></div><div class="bar big"><i></i><i></i><i></i></div></div>
{body}<footer>Isapur Industrial Park brand kit v{VERSION}, {TODAY}. Logo is never changed. English only. Phones {" | ".join(CT["phones"])}.</footer></main></body></html>"""
(SITE / "index.html").write_text(page, encoding="utf-8")
print("site", len(page) // 1024, "KB", sum(f.stat().st_size for f in SITE.rglob("*") if f.is_file()) // 1024, "KB total")
