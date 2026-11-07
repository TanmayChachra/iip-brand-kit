"""Builds index.html (the experiment page) from variants.json and thumbs/. Run after build_lab.py."""
import json, pathlib, html
H = pathlib.Path(__file__).resolve().parent
V = json.load(open(H / "variants.json"))
REFS = [("Fareham Industrial Park (type-led industrial identity)", "https://bewonder.co.uk/our-work/fareham-industrial-park/"),
        ("Humber Enterprise Park (branding from site heritage)", "https://greyhound-krill-msfz.squarespace.com/projects/humber-enterprise-park"),
        ("Crosspoint brand launch (standing out among industrial parks)", "https://www.hughespr.com.au/case-studies/139/crosspoint-brand-launch/"),
        ("Foundry Geelong (commercial property brochure)", "https://10turtle.com/work/brochure-design-commercial-property-brochure-design-foundry-geelong"),
        ("Refero style references (bone #f0eeeb, warns against pure white)", "https://styles.refero.design/style/38f3a11c-ac61-40f3-934e-088d8dbb9467"),
        ("Neo minimalism reference (paper grain at 2 to 5 percent)", "https://chrislemke.github.io/website_designs/examples/Neo_Minimalism.html"),
        ("Fonts for construction and engineering (Barlow, Anton)", "https://fontalternatives.com/best-fonts-for/construction/"),
        ("Google font pairings 2026 (Archivo, Space Grotesk, Bricolage)", "https://www.thebrief.ai/blog/google-font-pairings/")]
def card(v):
    return f'''<figure class="card"><a href="png/{v['id']}.png" target="_blank"><img src="thumbs/{v['id']}-s.webp" alt="{html.escape(v['name'])}" loading="lazy"></a>
<figcaption><b>{html.escape(v['name'])}</b><span class="fonts">{html.escape(v['font'][0])} + {html.escape(v['font'][1])}</span><span class="sw"><i style="background:{v['bg']}"></i>{v['bg']}</span><p>{html.escape(v['note'])}</p>
<a class="dl" href="svg/{v['id']}.svg" download>SVG</a> <a class="dl" href="png/{v['id']}.png" download>PNG</a></figcaption></figure>'''


cards = "".join(card(v) for v in V if v["id"][:3].isdigit())
mix_cards = "".join(card(v) for v in V if v["id"].startswith("mix-"))
img_cards = "".join(card(v) for v in V if v["id"].startswith("img-"))
refs = "".join(f'<li><a href="{u}" target="_blank" rel="noopener">{html.escape(t)}</a></li>' for t, u in REFS)
page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>IIP Poster Lab</title>
<style>:root{{--bg:#F4F0E8;--ink:#111827;--mut:#5b6472;--card:#fffdf8;--line:#e3dccd}}@media(prefers-color-scheme:dark){{:root{{--bg:#0f1512;--ink:#f1ece0;--mut:#a9b3ad;--card:#18211c;--line:#2a362f}}}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:16px/1.5 Inter,system-ui,sans-serif}}main{{max-width:1240px;margin:0 auto;padding:32px 16px 64px}}
h1{{font-size:clamp(28px,4vw,44px);margin:0 0 6px;letter-spacing:-.02em}}p.lead{{color:var(--mut);max-width:70ch;margin:0 0 28px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(270px,1fr));gap:20px}}.card{{margin:0;background:var(--card);border:1px solid var(--line);border-radius:14px;overflow:hidden}}
.card img{{width:100%;display:block;aspect-ratio:1827/2290;object-fit:cover}}figcaption{{padding:14px 16px 16px}}figcaption b{{display:block;font-size:17px}}
.fonts{{display:block;color:var(--mut);font-size:14px}}.sw{{display:inline-flex;align-items:center;gap:6px;font-size:13px;color:var(--mut);margin:4px 0}}.sw i{{width:14px;height:14px;border-radius:50%;border:1px solid var(--line);display:inline-block}}
figcaption p{{margin:6px 0 10px;font-size:14px}}.dl{{font-size:13px;margin-right:10px;color:inherit}}h2{{margin:40px 0 10px}}ul{{padding-left:20px}}a{{color:inherit}}
.rules{{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px 18px}}</style></head><body><main>
<h1>IIP poster lab</h1><p class="lead">Same layout and same text as the final poster. Only the font, background texture and background colour change. Pure white is replaced by warm or tinted bases, and the photo is multiplied into the base so it never sits in a white box. The final poster is untouched.</p>
<h2>Fonts, textures and colours</h2><div class="grid">{cards}</div>
<h2>Image experiments</h2><p class="lead">Same bone paper background and same Montserrat and Inter as the final, only the hero picture changes. Cards starting with "AI" are AI generated concepts, not photos of the park. Real site photos replace any of these once the shoot happens.</p><div class="grid">{img_cards}</div>
<h2>Mix and shuffle</h2><p class="lead">Final round: the best fonts, textures and images crossed with each other. Layout and text are still identical to the final poster.</p><div class="grid">{mix_cards}</div>
<h2>How to read this</h2><div class="rules"><ul><li>Tap a poster for the full size PNG. SVG files open in a browser or vector app (fonts load from Google Fonts).</li><li>Badge, text, icons and CTA are identical in every card. The brand colours (yellow, red, green) and the thin flag are unchanged.</li><li>Card 09 is the control: the original Montserrat and Inter on bone only, so you can judge what the background alone does.</li><li>Card 07 is the boldest: brand green canvas, cream text, photo as a rounded window.</li><li>Any pick would still need a print test: textures and tints print differently from screens.</li></ul></div>
<h2>References</h2><ul>{refs}</ul></main></body></html>'''
(H / "index.html").write_text(page, encoding="utf-8"); print("page ok")
