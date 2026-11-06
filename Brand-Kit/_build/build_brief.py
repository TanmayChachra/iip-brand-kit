"""Brand brief: short web page (site/brief.html) and 2 to 3 page PDF (site/assets/files/ISAPUR-Brand-Brief.pdf).
Run after build_site.py:  python Brand-Kit/_build/build_brief.py"""
import json, pathlib, html, datetime
from playwright.sync_api import sync_playwright

KIT = pathlib.Path(__file__).resolve().parents[1]; SITE = KIT / "site"
CT = json.loads((KIT / "tokens/content.json").read_text()); TOK = json.loads((KIT / "tokens/brand.tokens.json").read_text())
CSS = (pathlib.Path(__file__).resolve().parent / "site.css").read_text(encoding="utf-8")
e = html.escape; TODAY = datetime.date.today().isoformat()
fontface = "".join(f"@font-face{{font-family:'{fam}';font-weight:{w};src:url('assets/fonts/{f}')}}" for fam, w, f in
                   (("Montserrat", 800, "Montserrat-ExtraBold.ttf"), ("Montserrat", 600, "Montserrat-SemiBold.ttf"), ("Inter", 400, "Inter-Regular.ttf"), ("Inter", 500, "Inter-Medium.ttf")))
sw = "".join(f'<div class="s"><i style="background:{v["value"]}"></i><b>{k.title()}</b><code>{v["value"]}</code><em>{e(v["use"])}</em></div>' for k, v in TOK["color"].items() if k in ("white", "charcoal", "yellow", "red", "green", "mist"))
QUESTIONS = [
    ("Logo", "Does an original vector file exist (from the designer or printer)? The kit uses a trace of the supplied artwork.", "Before very large or close print"),
    ("Approvals", "Copy of the Zilla Panchayat sanctioned map (number, date) and the document behind 'Section 80'. What exact wording is legally right?", "Before any approval claim is printed"),
    ("Poster wording", "The poster says 4 km (straight-line). By road it is 4.7 km. Which wording do you want, 5 km or 4.7 km?", "Before the poster is printed"),
    ("Drainage", "Photo of the naala, where the park outfall meets it, and any pollution control board consent.", "Before drainage is advertised"),
    ("Facilities", "Which of these exist now: street lights, 24x7 security and CCTV, gated entry, truck parking, water supply, power load? How many acres are developed?", "To choose true bottom-row claims"),
    ("Site photos", "A shoot of the real gate, roads, lights, trees, plots, drainage. No photos exist yet.", "Boards and posts with real proof"),
    ("Registrations", "Any RERA or other registration number and GST for invoices that may appear on stationery. The developer name stays unpublished.", "Legal line, letterhead"),
    ("Plots", "Plot sizes, price per sq.yard or 'on request', phase 1 and phase 2 scope, launch date.", "Offer posts and plot list"),
    ("Online", "Preferred handle, website domain, email, Google Business and WhatsApp numbers already owned.", "Social and web setup"),
    ("Print", "Panel sizes and media owners for poles and hoardings, printer, material, budget.", "Final print files"),
]
body = f"""<main style="display:block;max-width:1000px;margin:0 auto;padding:30px clamp(16px,4vw,40px)">
<div class="hero"><img src="assets/p/logo-primary-vertical.webp" alt="ISAPUR Industrial Park"><div><p class="eyebrow">Brand brief, version 1.0, {TODAY}</p><h1>ISAPUR Industrial Park</h1>
<p class="lead">A short brief of who we are, how we look and sound, where the brand shows up, and what we still need from you. Full rules are in the <a href="index.html">brand kit</a> and the <a href="assets/files/ISAPUR-Brand-Book.pdf">brand book PDF</a>.</p></div></div>
<section><header><span class="num">1</span><h2>The brand on one page</h2></header>
<div class="two"><div><h4>Idea</h4><p>A modern industrial address on the Hapur-Modinagar Road for local manufacturers: clear plots, real facilities, one number to call.</p>
<h4>Taglines (adaptive, pick one per creative)</h4><p class="big">A Modern Industrial Address.</p><p class="big">The Groundwork for Growth.</p>
<h4>Type</h4><p><b>Montserrat</b> for headlines and signage, <b>Inter</b> for body. Free fonts.</p><h4>Rules</h4><ul><li>The logo is never changed.</li><li>English only. Maximum 7 words on a board.</li><li>No claim without a document on file.</li></ul></div>
<div><h4>Colour</h4><div class="sw" style="grid-template-columns:repeat(3,1fr)">{sw}</div></div></div></section>
<section><header><span class="num">2</span><h2>Who, where, how to reach</h2></header>
<div class="tw"><table><tbody><tr><th>Audience</th><td>Local factory owners and small industrial buyers (primary). Warehouse and logistics operators, investors, brokers (to confirm).</td></tr>
<tr><th>Address</th><td>{e(CT['address'])}</td></tr><tr><th>Phones</th><td>{" | ".join(CT['phones'])}</td></tr>
<tr><th>Location</th><td>By road (Google Maps): 4.7 km to the Delhi-Meerut Expressway on-ramp, 11.4 km to Modinagar bus stand, 13.4 km to Hapur bus stand.</td></tr>
<tr><th>Competitors</th><td>Shri Balaji, Shri Haridas (SHD), Shivansh, CKS, Atom, Mahamaya. Their boards use navy, gold or red with dense copy. IIP uses white space, one logo, one line.</td></tr></tbody></table></div></section>
<section><header><span class="num">3</span><h2>Where the brand appears</h2></header>
<div class="grid"><figure class="card"><div class="thumb"><img src="assets/p/sign-pole-20x32in-A.webp" alt="Pole board"></div><figcaption><b>Pole boards</b><span>20 x 32 in, same size as competitors.</span></figcaption></figure>
<figure class="card"><div class="thumb"><img src="assets/p/sign-hoarding-40x20ft-A.webp" alt="Hoarding"></div><figcaption><b>Hoardings</b><span>40 x 20 ft and 40 x 15 ft.</span></figcaption></figure>
<figure class="card"><div class="thumb"><img src="assets/ref/poster.webp" alt="Poster"></div><figcaption><b>Poster</b><span>Facts grid and facilities row.</span></figcaption></figure>
<figure class="card"><div class="thumb"><img src="assets/p/card-front-A.webp" alt="Business card"></div><figcaption><b>Stationery, ID, workwear</b><span>Card, letterhead, ID, helmet, vest.</span></figcaption></figure></div></section>
<section><header><span class="num">4</span><h2>Next phase: social and online presence</h2></header>
<ol><li><b>Week 1.</b> Confirm handles, set profile picture (badge), cover and bio on Instagram, Facebook, LinkedIn, YouTube, WhatsApp Business, Google Business Profile.</li>
<li><b>Week 1 to 2.</b> Site photo shoot (gate, 50 ft road, lights, greenery, drainage, plots, drone).</li><li><b>Week 2 onward.</b> Three posts a week: one fact, one proof, one action. Status and story daily for WhatsApp.</li>
<li><b>Month 1.</b> One page website with map, distances (stating straight-line or driven), plot list, documents and a call button.</li></ol>
<p class="note">Proposed plan. Starter templates are in the brand kit under Social media.</p></section>
<section><header><span class="num">5</span><h2>What we need from you</h2></header>
<div class="tw"><table><thead><tr><th>Topic</th><th>Question</th><th>Needed for</th></tr></thead><tbody>{"".join(f"<tr><td><b>{e(a)}</b></td><td>{e(b)}</td><td>{e(c)}</td></tr>" for a, b, c in QUESTIONS)}</tbody></table></div></section>
<footer>ISAPUR Industrial Park brand brief v1.0. Central facts live in 00_ISAPUR_KNOWLEDGE.md.</footer></main>"""
page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>ISAPUR Brand Brief</title>
<style>{fontface}{CSS}body{{display:block}}@page{{size:A4;margin:12mm}}@media print{{.hero{{grid-template-columns:50mm 1fr}}section{{break-inside:auto;padding:18px 0}}.card{{break-inside:avoid}}.thumb img{{max-height:38mm}}.grid{{grid-template-columns:repeat(4,1fr)}}}}</style></head><body>{body}</body></html>"""
(SITE / "brief.html").write_text(page, encoding="utf-8")
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 900, "height": 1200}); pg.goto((SITE / "brief.html").as_uri()); pg.wait_for_timeout(1200)
    pg.emulate_media(media="print")
    pg.pdf(path=str(SITE / "assets/files/ISAPUR-Brand-Brief.pdf"), format="A4", print_background=True, display_header_footer=True, header_template="<span></span>",
           margin={"top": "12mm", "bottom": "14mm", "left": "12mm", "right": "12mm"},
           footer_template='<div style="font:8px Arial;color:#6B7280;width:100%;padding:0 12mm;display:flex;justify-content:space-between"><span>ISAPUR Industrial Park, Brand Brief v1.0</span><span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>')
    pg.emulate_media(media="screen"); pg.set_viewport_size({"width": 1100, "height": 900}); pg.screenshot(path="C:/Users/anshc/AppData/Local/Temp/claude/d662b24522fc92eb/71152788-1591-462b-b0c9-2a184ec619a9/scratchpad/brief.png")
    b.close()
print("brief ok")
