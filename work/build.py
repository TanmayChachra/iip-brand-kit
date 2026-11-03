"""Static site generator: writes ../docs (GitHub Pages). Images are converted to WEBP."""
import json, pathlib, shutil, re, html
from PIL import Image
import content as C

ROOT = pathlib.Path(__file__).resolve().parent
DOCS = ROOT.parent / "docs"
A = DOCS / "assets"
AN = json.load(open(ROOT / "analysis.json"))
DIST = json.load(open(ROOT / "gen/dist.json"))
KITS = C.KITS
SIZES = ["10x10", "10x12", "10x14"]


def webp(src, name, maxw=1600, q=80, crop=None, up=1):
    im = Image.open(src)
    if crop: im = im.crop(crop)
    if up > 1: im = im.resize((im.width * up, im.height * up), Image.LANCZOS)
    has_a = im.mode in ("RGBA", "LA")
    im = im.convert("RGBA" if has_a else "RGB")
    if im.width > maxw: im = im.resize((maxw, round(im.height * maxw / im.width)), Image.LANCZOS)
    im.save(A / name, "WEBP", quality=q, method=6)
    return f"assets/{name}"


def prep_assets():
    if DOCS.exists(): shutil.rmtree(DOCS)
    A.mkdir(parents=True)
    webp(ROOT / "logo/iip-master-1x.png", "iip-logo.webp", 700, 92)
    webp(ROOT / "src/real-pole-1.jpg", "field-pole-1.webp", 1200, 82)
    webp(ROOT / "src/real-pole-stack.jpg", "field-pole-stack.webp", 1200, 82)
    webp(ROOT / "gen/map-annotated.png", "map-isapur.webp", 2000, 80)
    webp(ROOT / "gen/scene-hoarding-a.png", "scene-hoarding-blank.webp", 1600, 80)
    webp(ROOT / "gen/scene-gate-a.png", "scene-gate-blank.webp", 1000, 80)
    webp(ROOT / "mock/gulaal-serial.jpg", "gulaal-serial.webp", 1600, 84)
    for k in KITS:
        for s in SIZES:
            webp(ROOT / f"boards/{k}-{s}.png", f"{k}-board-{s}.webp", 1200, 82)
            webp(ROOT / f"mock/{k}-{s}-pole.jpg", f"{k}-pole-{s}.webp", 920, 86, crop=(420, 500, 840, 1130), up=2)
            webp(ROOT / f"mock/{k}-{s}-stack.jpg", f"{k}-stack-{s}.webp", 1200, 84)
        webp(ROOT / f"mock/{k}-18x25-pole.jpg", f"{k}-pole-18x25.webp", 920, 86, crop=(420, 500, 840, 1130), up=2)
        webp(ROOT / f"wide/{k}-hoarding.png", f"{k}-art-hoarding.webp", 1600, 82)
        webp(ROOT / f"wide/{k}-gate.png", f"{k}-art-gate.webp", 1600, 82)
        webp(ROOT / f"mock/{k}-hoarding.jpg", f"{k}-site-hoarding.webp", 1600, 84)
        webp(ROOT / f"mock/{k}-gate.jpg", f"{k}-site-gate.webp", 1086, 84, crop=(0, 120, 1086, 800))
    for i in (1, 2, 3):
        webp(ROOT / f"boards/gulaal-teaser-{i}.png", f"gulaal-teaser-{i}.webp", 800, 82)


CSS = """
:root{--paper:#F6F4EF;--ink:#15131A;--mut:#5E5B66;--line:#DAD6CC;--card:#fff;--yel:#FEF102;--max:1180px}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--paper:#121016;--ink:#F1EFEA;--mut:#A29FAA;--line:#2E2B35;--card:#1A1720}}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.6 'Hind','Segoe UI',system-ui,sans-serif}
img{max-width:100%;display:block}a{color:inherit}
.wrap{max-width:var(--max);margin:0 auto;padding:0 20px}
nav.top{position:sticky;top:0;z-index:20;background:color-mix(in srgb,var(--paper) 92%,transparent);backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
nav.top .wrap{display:flex;gap:6px;align-items:center;overflow-x:auto;white-space:nowrap;padding-top:8px;padding-bottom:8px}
nav.top a{text-decoration:none;font-size:14px;font-weight:600;padding:7px 12px;border-radius:99px;color:var(--mut)}
nav.top a.on,nav.top a:hover{background:var(--ink);color:var(--paper)}
nav.top .brand{display:flex;align-items:center;gap:8px;margin-right:10px;padding:0;color:var(--ink)}nav.top .brand img{height:32px;width:32px}
nav.top .brand:hover{background:none;color:var(--ink)}
h1,h2,h3{font-family:'Archivo','Hind',sans-serif;line-height:1.1;margin:0 0 .4em;letter-spacing:-.015em}
h1{font-size:clamp(34px,6vw,68px);font-weight:900}h2{font-size:clamp(26px,3.6vw,40px);font-weight:800}h3{font-size:20px;font-weight:800}
p{margin:0 0 1em}.lead{font-size:clamp(18px,2.2vw,22px);color:var(--mut);max-width:760px}
.kick{font:700 12px 'Archivo';letter-spacing:.16em;text-transform:uppercase;color:var(--mut);margin-bottom:10px}
section{padding:56px 0;border-top:1px solid var(--line)}section.first{border-top:0}
.grid{display:grid;gap:20px}.g2{grid-template-columns:repeat(2,1fr)}.g3{grid-template-columns:repeat(3,1fr)}.g4{grid-template-columns:repeat(4,1fr)}
@media(max-width:860px){.g2,.g3,.g4{grid-template-columns:1fr}.g4.keep2{grid-template-columns:1fr 1fr}}
.card{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:22px}
.card.flat{padding:0;overflow:hidden}
figure{margin:0}figcaption{font-size:13px;color:var(--mut);margin-top:8px}
.zoom{cursor:zoom-in;border-radius:10px}
.pill{display:inline-block;font:700 12px 'Archivo';letter-spacing:.08em;text-transform:uppercase;padding:5px 10px;border-radius:99px;border:1px solid var(--line);color:var(--mut)}
.pill.dk{background:var(--ink);color:var(--paper);border-color:var(--ink)}
.note{border-left:4px solid var(--yel);background:color-mix(in srgb,var(--yel) 18%,var(--card));padding:14px 18px;border-radius:0 12px 12px 0;font-size:15px}
table{width:100%;border-collapse:collapse;font-size:15px}th,td{text-align:left;padding:10px 12px;border-bottom:1px solid var(--line);vertical-align:top}th{font:700 12px 'Archivo';letter-spacing:.1em;text-transform:uppercase;color:var(--mut)}
.scroll{overflow-x:auto}
.sw{border-radius:14px;overflow:hidden;border:1px solid var(--line);background:var(--card)}.sw .c{height:110px;display:flex;align-items:flex-end;padding:10px;font:700 13px 'Archivo'}.sw .m{padding:10px 12px;font-size:13px}
.sw .m b{display:block;font-size:15px}
.bar{display:flex;height:34px;border-radius:10px;overflow:hidden;border:1px solid var(--line)}
.dots{display:flex;gap:4px;margin:6px 0}.dots i{width:14px;height:14px;border-radius:50%;background:var(--line);display:block}.dots i.f{background:var(--ink)}
.hero{display:grid;grid-template-columns:1.1fr .9fr;gap:34px;align-items:center}@media(max-width:860px){.hero{grid-template-columns:1fr}}
.kitcard{display:block;text-decoration:none;border-radius:18px;overflow:hidden;border:1px solid var(--line);background:var(--card);transition:transform .2s}.kitcard:hover{transform:translateY(-4px)}
.kitcard .t{padding:18px 20px 22px}.kitcard img{width:100%;aspect-ratio:16/10;object-fit:cover}
.stat{font:900 44px 'Archivo';line-height:1}.stat small{display:block;font:500 14px 'Hind';color:var(--mut);margin-top:6px}
.chips{display:flex;gap:4px;flex-wrap:wrap}.chip{width:26px;height:26px;border-radius:6px;border:1px solid rgba(0,0,0,.15)}
dialog{border:0;padding:0;background:transparent;max-width:96vw;max-height:96vh}dialog::backdrop{background:rgba(0,0,0,.82)}dialog img{max-height:92vh;border-radius:8px}
footer{padding:40px 0 60px;border-top:1px solid var(--line);font-size:13px;color:var(--mut)}
.sizes{display:flex;gap:18px;align-items:flex-end;flex-wrap:wrap}.sizes figure{flex:0 0 auto}
.kitband{padding:70px 0 54px}
.donts{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}@media(max-width:860px){.donts{grid-template-columns:1fr 1fr}}
.dont{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px;text-align:center;font-size:13px}.dont .t{height:120px;display:flex;align-items:center;justify-content:center;position:relative;margin-bottom:8px}
.dont .t img{max-height:100px;width:auto}.dont .x{position:absolute;top:0;right:0;background:#d4202a;color:#fff;border-radius:50%;width:22px;height:22px;font:700 14px/22px 'Archivo'}
.stage{padding:26px;border-radius:18px;display:flex;justify-content:center;align-items:center;flex-wrap:wrap;gap:22px}
"""

JS = """
document.addEventListener('click',e=>{const i=e.target.closest('img.zoom');if(!i)return;const d=document.createElement('dialog');
d.innerHTML='<img src="'+i.currentSrc+'" alt="">';document.body.appendChild(d);d.showModal();d.addEventListener('click',()=>{d.close();d.remove()})});
"""

NAV = [("index.html", "Overview"), ("research.html", "Research"), ("site.html", "Site and competitors"),
       ("kit-jamun.html", "01 Jamun"), ("kit-gulaal.html", "02 Gulaal"), ("kit-kora.html", "03 Kora"), ("compare.html", "Compare and decide")]


def shell(fname, title, body, extra_css=""):
    nav = "".join(f'<a class="{"on" if fname==h else ""}" href="{h}">{t}</a>' for h, t in NAV)
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><meta name="robots" content="noindex"><link rel="icon" href="assets/iip-logo.webp" type="image/webp">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..900&family=Hind:wght@400;500;600;700&family=Teko:wght@500;600;700&family=Yatra+One&family=Baloo+2:wght@600;700;800&display=swap" rel="stylesheet">
<style>{CSS}{extra_css}</style></head><body>
<nav class="top"><div class="wrap"><a class="brand" href="index.html"><img src="assets/iip-logo.webp" alt="IIP"><b>IIP Brand Kit</b></a>{nav}</div></nav>
{body}
<footer><div class="wrap"><p>Isapur Industrial Park brand kit, concept stage for board review. All mockups are visualisations: the logo is the supplied artwork, unchanged. Phone numbers shown as {C.PHONE} are placeholders. Competitor details are read from field photographs and public listings and are not verified. Satellite imagery: Esri, Maxar, Earthstar Geographics. Prepared November 2026.</p></div></footer>
<script>{JS}</script></body></html>"""


def img(src, alt, cls="zoom", extra=""):
    return f'<img class="{cls}" src="assets/{src}" alt="{html.escape(alt)}" loading="lazy" {extra}>'


def fig(src, cap, alt=None, style=""):
    return f'<figure style="{style}">{img(src, alt or cap)}<figcaption>{cap}</figcaption></figure>'


# ---------- kit components (pure HTML/CSS, themed by kit) ----------
KIT_CSS = """
.k-jamun{--bg:#4B1DA6;--ink:#fff;--acc:#FEF102;--soft:#1F0E5C;--paper:#fff;--pink:#1F0E5C;--h:'Teko';--b:'Hind'}
.k-gulaal{--bg:#E4007C;--ink:#FFF4DC;--acc:#FEF102;--soft:#1A0B2E;--paper:#FFF4DC;--h:'Yatra One';--b:'Baloo 2'}
.k-kora{--bg:#FBF6E9;--ink:#14110F;--acc:#FEF102;--soft:#14110F;--paper:#FBF6E9;--h:'Archivo';--b:'Hind'}
.cmp{position:relative;overflow:hidden;font-family:var(--b);container-type:inline-size}
.cmp .logo{display:block}
.card3{aspect-ratio:3.5/2;width:min(100%,420px);background:var(--bg);color:var(--ink);border-radius:6px;box-shadow:0 10px 30px rgba(0,0,0,.25);display:flex;align-items:center;justify-content:center;gap:5cqw;padding:5cqw}
.card3 .logo{width:34cqw}.card3 .nm{font-family:var(--h);font-weight:700;font-size:8.5cqw;line-height:.95}.card3 .nm span{display:block;font:600 4cqw var(--b);margin-top:2cqw;color:var(--acc)}
.k-kora .card3{border:1.4cqw solid #14110F;box-shadow:0 10px 30px rgba(0,0,0,.18)}.k-kora .card3 .nm span{color:#14110F}
.cardb{aspect-ratio:3.5/2;width:min(100%,420px);background:var(--paper);color:#14110F;border-radius:6px;box-shadow:0 10px 30px rgba(0,0,0,.2);padding:6cqw;display:flex;flex-direction:column;justify-content:space-between;position:relative;overflow:hidden}
.cardb .logo{width:15cqw}.cardb b{font:700 5.4cqw var(--b)}.cardb p{margin:0;font-size:3.7cqw;line-height:1.5}
.cardb:after{content:"";position:absolute;left:0;right:0;bottom:0;height:3.4cqw;background:var(--acc)}
.k-jamun .cardb:after{height:5cqw;background:var(--acc) url("DIAMOND") repeat-x;background-size:5cqw}
.lh{aspect-ratio:1/1.414;width:min(100%,360px);background:#fff;color:#14110F;box-shadow:0 10px 30px rgba(0,0,0,.2);position:relative;overflow:hidden;font-family:var(--b)}
.lh .top{background:var(--bg);color:var(--ink);padding:5cqw 6cqw;display:flex;align-items:center;gap:4cqw}.lh .top .logo{width:16cqw}.lh .top b{font:700 6cqw var(--h);line-height:1}
.k-kora .lh .top{border-bottom:1.2cqw solid #14110F}
.lh .ln{height:1.2cqw;background:#e5e5e5;margin:3cqw 6cqw}.lh .bot{position:absolute;bottom:0;left:0;right:0;background:var(--acc);padding:2.4cqw 6cqw;font-size:3cqw;color:#14110F}
.phone{width:min(100%,250px);aspect-ratio:9/19;background:#111;border-radius:30px;padding:9px;box-shadow:0 14px 36px rgba(0,0,0,.35)}
.phone .scr{height:100%;border-radius:22px;overflow:hidden;background:var(--bg);color:var(--ink);display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;gap:4cqw;padding:7cqw;position:relative;container-type:inline-size;font-family:var(--h)}
.phone .logo{width:62cqw}.phone .big{font-size:15cqw;line-height:1;font-weight:700}.phone .sm{font:600 6.2cqw var(--b);color:var(--acc)}
.phone .cta{font:700 6cqw var(--b);background:var(--acc);color:#14110F;padding:3cqw 6cqw;border-radius:99px}.k-kora .phone .sm{color:#14110F}
.broc{aspect-ratio:1/1.414;width:min(100%,360px);background:var(--bg);color:var(--ink);box-shadow:0 10px 30px rgba(0,0,0,.25);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:5cqw;padding:8cqw;text-align:center;position:relative;font-family:var(--h)}
.broc .logo{width:62cqw}.broc .big{font-size:11cqw;font-weight:700;line-height:1}.broc .sm{font:600 4.4cqw var(--b);color:var(--acc)}.k-kora .broc{border:2cqw solid #14110F}.k-kora .broc .sm{color:#14110F}
.k-jamun .broc:after{content:"";position:absolute;left:0;right:0;bottom:0;height:8cqw;background:var(--acc) url("DIAMOND") repeat-x;background-size:8cqw}
.k-gulaal .broc:before{content:"";position:absolute;inset:3cqw;border:1.2cqw solid #FFF4DC;border-radius:3cqw}
.way{width:min(100%,360px);aspect-ratio:2.6/1;background:var(--bg);color:var(--ink);position:relative;display:flex;align-items:center;gap:4cqw;padding:0 12cqw 0 5cqw;clip-path:polygon(0 0,86% 0,100% 50%,86% 100%,0 100%);font-family:var(--h)}
.way .logo{width:19cqw}.way b{font-size:11cqw;font-weight:700;line-height:1}.way small{display:block;font:600 4.6cqw var(--b);color:var(--acc)}.k-kora .way small{color:#14110F}
.k-kora .way{outline:0;box-shadow:inset 0 0 0 1.4cqw #14110F}
"""


def components(k):
    k_ = KITS[k]
    name = {"jamun": "ISAPUR INDUSTRIAL PARK", "gulaal": "इसापुर इंडस्ट्रियल पार्क", "kora": "ISAPUR INDUSTRIAL PARK"}[k]
    big = k_["tagline_hi"] if k != "kora" else k_["tagline_en"]
    lg = '<img class="logo" src="assets/iip-logo.webp" alt="IIP logo">'
    card_a = f'<div class="cmp k-{k}"><div class="card3">{lg}<div class="nm">ISAPUR<br>INDUSTRIAL<br>PARK<span>{k_["tagline_hi"]}</span></div></div></div>'
    card_b = (f'<div class="cmp k-{k}"><div class="cardb"><div style="display:flex;justify-content:space-between;align-items:flex-start">'
              f'<div><b>Name Surname</b><p>Director, Isapur Industrial Park</p></div>{lg}</div>'
              f'<p>{C.PHONE}<br>sales@your-domain.in<br>{C.ADDRESS}</p></div></div>')
    lh = (f'<div class="cmp k-{k}"><div class="lh"><div class="top">{lg}<b>ISAPUR INDUSTRIAL PARK</b></div>'
          + ''.join('<div class="ln"></div>' for _ in range(9)) + f'<div class="bot">{C.ADDRESS} · {C.PHONE}</div></div></div>')
    wa = (f'<div class="cmp k-{k}"><div class="phone"><div class="scr">{lg}<div class="big">{big}</div><div class="sm">ISAPUR INDUSTRIAL PARK</div>'
          f'<div class="cta">Site visit: {C.PHONE}</div></div></div></div>')
    br = f'<div class="cmp k-{k}"><div class="broc">{lg}<div class="big">{big}</div><div class="sm">ISAPUR INDUSTRIAL PARK</div></div></div>'
    wy = f'<div class="cmp k-{k}"><div class="way">{lg}<div><b>IIP</b><small>Phase 1 · 500 m</small></div></div></div>'
    return dict(card_a=card_a, card_b=card_b, lh=lh, wa=wa, br=br, wy=wy)


def cmyk(h):
    r, g, b = [int(h[i:i+2], 16) / 255 for i in (1, 3, 5)]
    k = 1 - max(r, g, b)
    if k == 1: return "0 / 0 / 0 / 100"
    c, m, y = [(1 - v - k) / (1 - k) for v in (r, g, b)]
    return " / ".join(str(round(v * 100)) for v in (c, m, y, k))


def rgbs(h): return ", ".join(str(int(h[i:i+2], 16)) for i in (1, 3, 5))


DIAMOND_URI = None


def kit_page(k):
    K = KITS[k]
    cmp_ = components(k)
    an = AN["brands"][k]
    con = AN["contrast"][k]
    hero_bg = K["color"]
    light = k == "kora"
    fg = "#14110F" if light else ("#fff" if k == "jamun" else "#FFF4DC")
    bg_hero = "#FBF6E9" if light else hero_bg
    pal = "".join(
        f'<div class="sw"><div class="c" style="background:{h};color:{"#14110F" if h.upper() in ("#FEF102","#FFFFFF","#FFF4DC","#FBF6E9") else "#fff"}">{n}</div>'
        f'<div class="m"><b>{h}</b>RGB {rgbs(h)}<br>CMYK ~{cmyk(h)}<br><span style="color:var(--mut)">{pct} · {use}</span></div></div>' for n, h, pct, use in K["palette"])
    ratio = "".join(f'<div style="flex:{float(p[2].rstrip("%"))};background:{p[1]}" title="{p[0]}"></div>' for p in K["palette"])
    fonts = "".join(
        f'<div class="card"><div class="kick">{use}</div><div style="font-family:\'{f}\',sans-serif;font-size:44px;line-height:1.05;margin:6px 0 10px;{"font-weight:700" if f in ("Teko","Baloo 2") else ""}">{sample}</div>'
        f'<b>{f}</b><p style="color:var(--mut);margin:4px 0 0">{spec}</p></div>' for f, use, spec, sample in K["fonts"])
    tag = "".join(f'<tr><td style="font-family:\'{"Yatra One" if k=="gulaal" else "Hind"}\';font-size:20px"><b>{a}</b></td><td>{b}</td></tr>' for a, b in K["taglines"])
    dists = "".join(f'<tr><td>{n}</td><td>{v}</td><td style="width:38%"><div style="height:10px;border-radius:5px;width:{min(100,v*2)}%;background:{K["color"] if not light else "#14110F"}"></div></td></tr>' for n, v in an["deltaE"].items())
    why = "".join(f"<li>{x}</li>" for x in K["why"])
    donts_txt = "".join(f"<li>{x}</li>" for x in K["donts"])
    risks = "".join(f"<li>{x}</li>" for x in K["risks"])
    sizes = "".join(
        f'<figure style="width:{int(w*150/10)}px;max-width:44vw">{img(f"{k}-board-{s}.webp", f"{K["name"]} pole board {s} inch")}<figcaption><b>{s} in</b> · print file {int(s.split("x")[0])*300} x {int(s.split("x")[1])*300} px</figcaption></figure>'
        for s, w in [(s, 10) for s in SIZES])
    poles = "".join(fig(f"{k}-pole-{s}.webp", f"{s} inch, flush on a pole face, directly under a live competitor board (Sarawa, Modinagar-Hapur road)") for s in SIZES)
    stacks = "".join(fig(f"{k}-stack-{s}.webp", f"{s} inch at the foot of the three-board competitor stack") for s in ["10x14"])
    logo_stage = lambda bg, extra="": f'<div class="stage" style="background:{bg}">{extra}</div>'
    lg = '<img src="assets/iip-logo.webp" alt="IIP logo" style="width:{w}px">'
    donts_logo = [
        ("Stretched or squashed", '<img src="assets/iip-logo.webp" style="width:110px;height:70px" alt="">'),
        ("Recoloured", '<img src="assets/iip-logo.webp" style="width:90px;filter:hue-rotate(120deg) saturate(1.4)" alt="">'),
        ("Rotated or tilted", '<img src="assets/iip-logo.webp" style="width:90px;transform:rotate(18deg)" alt="">'),
        ("Shadow, glow or outline", '<img src="assets/iip-logo.webp" style="width:90px;filter:drop-shadow(0 0 6px #000) drop-shadow(4px 6px 3px rgba(0,0,0,.6))" alt="">'),
    ]
    dont_html = "".join(f'<div class="dont"><div class="t">{h}<span class="x">x</span></div>{t}</div>' for t, h in donts_logo)
    serial = ""
    if k == "gulaal":
        serial = f"""<section><div class="wrap"><div class="kick">Campaign idea</div><h2>The pole serial</h2>
<p class="lead">Four consecutive poles, one line each. Three teasers, then the reveal. It is the Burma-Shave idea applied to the Hapur-Modinagar road, and it is the only concept here that turns the small board size into an advantage.</p>
<figure>{img("gulaal-serial.webp", "Gulaal four pole serial")}<figcaption>Poles 1 to 4 (left to right). Each board costs the same, the story compounds. Sequence is placed in the direction of traffic from Bhojpur.</figcaption></figure>
<div class="grid g3" style="margin-top:20px">{"".join(fig(f"gulaal-teaser-{i}.webp", t) for i, t in [(1, "Teaser 1: pink, cream. 'Where will you set up your factory?'"), (2, "Teaser 2: yellow. 'Still thinking?'"), (3, "Teaser 3: ink. 'Stop thinking. Let's go.'")])}</div></div></section>"""
    css = KIT_CSS.replace("DIAMOND", DIAMOND_URI)
    body = f"""
<header class="kitband" style="background:{bg_hero};color:{fg}"><div class="wrap hero">
<div><div class="kick" style="color:{fg};opacity:.8">Direction {K["num"]}</div><h1 style="font-family:{"Teko" if k=="jamun" else ("Yatra One" if k=="gulaal" else "Archivo")};{"text-transform:uppercase" if k!="gulaal" else ""}">{K["name"]}</h1>
<p class="lead" style="color:{fg};opacity:.92;font-weight:600">{K["one_liner"]}</p><p style="max-width:560px;opacity:.9">{K["verdict"]}</p>
<p><span class="pill" style="border-color:{fg};color:{fg}">{K["tagline_hi"]}</span> <span class="pill" style="border-color:{fg};color:{fg}">{K["tagline_en"]}</span></p></div>
<div>{img(f"{k}-site-hoarding.webp", f"{K['name']} hoarding on the Hapur-Modinagar road", extra='style="border-radius:12px;box-shadow:0 20px 50px rgba(0,0,0,.35)"')}</div></div></header>

<section class="first"><div class="wrap"><div class="kick">1 · Strategy</div><h2>The idea</h2><p class="lead">{K["idea"]}</p>
<div class="grid g2" style="margin-top:24px"><div class="card"><h3>Why it wins on this road</h3><ul>{why}</ul></div>
<div class="card"><h3>Memory device: {K["device_name"]}</h3><p>{K["device"]}</p><h3 style="margin-top:18px">Voice</h3><p>{K["voice"]}</p><p><b>Best for:</b> {K["best_for"]}</p></div></div></div></section>

<section><div class="wrap"><div class="kick">2 · Logo</div><h2>The logo, unchanged</h2>
<p class="lead">The supplied rosette is used exactly as drawn. Only the white page, the faint die-cut outline and a '1/1' screenshot marker were removed to make a transparent master. Please supply the original vector (CDR or AI) before any large print.</p>
<div class="grid g3">
<div class="card"><div class="stage" style="background:{K["color"] if k!="kora" else "#FBF6E9"}">{lg.format(w=170)}</div><p style="margin-top:12px"><b>Primary.</b> The full-colour badge, on the direction's own field. The only version used on boards.</p></div>
<div class="card"><div style="position:relative;display:inline-block;margin:6px 0 10px"><img src="assets/iip-logo.webp" style="width:170px" alt=""><div style="position:absolute;inset:-17px;border:1.5px dashed #d4202a"></div></div><p><b>Clear space.</b> Keep a margin of one-tenth of the badge width on every side (the red dashed line). On pole boards, never less than 5 percent of the board width.</p></div>
<div class="card"><div style="display:flex;gap:16px;align-items:flex-end;margin:10px 0 14px"><img src="assets/iip-logo.webp" style="width:80px" alt=""><img src="assets/iip-logo.webp" style="width:40px" alt=""><img src="assets/iip-logo.webp" style="width:24px" alt=""></div><p><b>Minimum size.</b> 24 px on screen, 18 mm in print. On a pole board the badge is never below 45 percent of the board width.</p></div></div>
<h3 style="margin:26px 0 12px">Never</h3><div class="donts">{dont_html}</div></div></section>

<section><div class="wrap"><div class="kick">3 · Colour</div><h2>Palette, and proof it stands out</h2>
<div class="grid g4 keep2">{pal}</div><div class="bar" style="margin-top:16px">{ratio}</div><p style="font-size:13px;color:var(--mut)">Usage balance. CMYK values are mathematical approximations; approve a printed proof before the run.</p>
<div class="grid g2" style="margin-top:22px"><div class="card"><h3>Distance from what is on the road</h3><p style="color:var(--mut);font-size:14px">CIEDE2000 colour difference between {an["main"]} and the dominant colours measured in your field photographs. Above about 20 is clearly different; above 40 is unmistakable.</p>
<div class="scroll"><table><tr><th>Measured against</th><th>Distance</th><th></th></tr>{dists}</table></div></div>
<div class="card"><h3>Legibility</h3><table>{"".join(f"<tr><td>{a}</td><td><b>{b}:1</b></td></tr>" for a, b in con.items())}</table><p style="color:var(--mut);font-size:14px;margin-top:10px">4.5:1 is the accessibility benchmark for body text and 3:1 for large display text.</p>
<h3 style="margin-top:18px">Risks to manage</h3><ul>{risks}</ul></div></div></div></section>

<section><div class="wrap"><div class="kick">4 · Type</div><h2>Typography</h2><div class="grid g2">{fonts}</div>
<h3 style="margin-top:28px">Line bank</h3><div class="card scroll"><table><tr><th>Line</th><th>Use</th></tr>{tag}</table></div></div></section>

<section><div class="wrap"><div class="kick">5 · Pole boards</div><h2>The electric pole boards: 10x10, 10x12, 10x14 inch</h2>
<p class="lead">Artwork is sized for a board that is as wide as the pole face (about 10 inches). Print masters are 300 dpi at actual size. Add 3 mm bleed at production.</p>
<div class="sizes">{sizes}</div>
<h3 style="margin:34px 0 12px">On a real pole, next to the competition</h3>
<p style="color:var(--mut)">These are your own photographs from the Sarawa stretch of the Modinagar-Hapur road. The IIP board is the exact artwork placed at true scale.</p>
<div class="grid g3">{poles}</div>
<div class="grid g2" style="margin-top:20px">{stacks}<figure>{img(f"{k}-pole-18x25.webp", "Optional competitor-class size")}<figcaption><b>Option:</b> the 10x14 artwork scaled to about 18 x 25 inch, the width of the Shri Balaji board. Same file, no redesign. See 'Compare and decide'.</figcaption></figure></div></div></section>
{serial}
<section><div class="wrap"><div class="kick">6 · The landmark</div><h2>Hoarding and gate</h2>
<div class="grid g2" style="align-items:center"><figure>{img(f"{k}-site-hoarding.webp", "Highway hoarding")}<figcaption>Highway hoarding, about 2.4:1 (for example 24 x 10 ft). Placed into a neutral-light photo of a blank hoarding beside a two-lane Uttar Pradesh road.</figcaption></figure>{fig(f"{k}-art-hoarding.webp", "Hoarding artwork, flat")}</div>
<div class="grid g2" style="margin-top:24px;align-items:center"><figure>{img(f"{k}-site-gate.webp", "Gate fascia")}<figcaption>Gate fascia above the entrance pillars, about 4:1. Placed into a photo of a new compound gate with raw plaster walls.</figcaption></figure>{fig(f"{k}-art-gate.webp", "Gate fascia artwork, flat")}</div></div></section>

<section><div class="wrap"><div class="kick">7 · Paper and phone</div><h2>Stationery, brochure, WhatsApp, wayfinding</h2>
<div class="grid g3"><div><div class="kick">Visiting card front and back</div><div class="grid" style="gap:14px">{cmp_["card_a"]}{cmp_["card_b"]}</div></div>
<div><div class="kick">Letterhead</div>{cmp_["lh"]}</div><div><div class="kick">Brochure cover</div>{cmp_["br"]}</div></div>
<div class="grid g3" style="margin-top:34px;align-items:start"><div><div class="kick">WhatsApp status (9:16)</div>{cmp_["wa"]}</div>
<div><div class="kick">Wayfinding arrow</div>{cmp_["wy"]}<p style="color:var(--mut);font-size:14px;margin-top:14px">Directional signs at the Bhojpur junction and the Modinagar junction. Distances are examples to be measured on the ground.</p></div>
<div class="card"><h3>Dos</h3><ul><li>Same logo, same colour, same sentence on every surface.</li><li>One message per board. Maximum three lines.</li><li>Pair every Hindi line with the English name.</li><li>Keep the phone number on a bar of its own, at the base.</li></ul><h3>Don'ts</h3><ul>{donts_txt}</ul></div></div></div></section>
"""
    return shell(f"kit-{k}.html", f"IIP {K['name']} brand kit", body, css)


def index_page():
    cards = "".join(
        f'<a class="kitcard" href="kit-{k}.html">{img(f"{k}-site-hoarding.webp", K["name"], cls="")}<div class="t"><div class="kick">Direction {K["num"]}</div><h3 style="font-size:28px">{K["name"]}</h3><p style="margin:0 0 8px"><b>{K["one_liner"]}</b></p><p style="color:var(--mut);font-size:15px;margin:0">{K["verdict"]}</p></div></a>'
        for k, K in KITS.items())
    body = f"""
<header class="wrap" style="padding-top:60px;padding-bottom:50px"><div class="hero"><div>
<div class="kick">Board review · Isapur Industrial Park</div><h1>Be the board nobody can mistake on the Modinagar road.</h1>
<p class="lead">Three complete brand directions for IIP, built from the logo as it is, tested against the road, the greenery and every competitor board we could photograph. Approve one, and the same kit runs from a 10 inch pole board to a 24 foot hoarding.</p>
<p><a class="pill dk" href="compare.html" style="text-decoration:none;padding:10px 18px;font-size:13px">Go to the decision page</a> <a class="pill" href="#kits" style="text-decoration:none;padding:10px 18px;font-size:13px">See the three directions</a></p></div>
<div>{img("jamun-site-hoarding.webp", "Jamun hoarding", extra='style="border-radius:14px;box-shadow:0 24px 60px rgba(0,0,0,.28)"')}</div></div></header>

<section class="first"><div class="wrap"><div class="kick">The situation</div><h2>A crowded road, and the same four colours</h2>
<div class="grid g4 keep2" style="margin:22px 0"><div class="stat">{DIST["SHD"]} m<small>from IIP Phase 1 to the SHD park</small></div><div class="stat">{DIST["CKS"]} m<small>to the CKS park</small></div><div class="stat">3.1 km<small>to Atom Industrial Park</small></div><div class="stat">4 of 4<small>competitor boards use navy, gold or red</small></div></div>
<div class="grid g2"><figure>{img("field-pole-stack.webp", "Competitor stack on a pole")}<figcaption>Your own photograph: Shri Haridas, Shri Balaji and Shivansh stacked on one pole. Dense copy, prices, badges, rendered gates, phone numbers.</figcaption></figure>
<div><p class="lead" style="font-size:19px">Everything here sells the same way: a rendered gate, a price, a 'government approved' badge and two phone numbers, in navy, gold and red. The road is green, the poles are grey and yellow, the sky is hazy.</p>
<p class="lead" style="font-size:19px">IIP has something none of them has: a distinctive, ownable symbol, and a position on the road that is first for anyone arriving from the Bhojpur side. What it lacks is a system that makes that symbol impossible to miss.</p>
<div class="note"><b>The core strategic idea:</b> do not out-shout the stack. Use a colour no one owns, one clear symbol, and almost no words. The logo does the work.</div></div></div></div></section>

<section id="kits"><div class="wrap"><div class="kick">The three directions</div><h2>Pick a route, not a board</h2><div class="grid g3">{cards}</div></div></section>

<section><div class="wrap"><div class="kick">How to read this deck</div><h2>Seven pages, one decision</h2>
<div class="grid g3"><div class="card"><h3>Research</h3><p>What a brand kit contains, how Kofi Kafi, boAt, McDonald's and Bata root themselves, and how this was built.</p><a href="research.html">Open research</a></div>
<div class="card"><h3>Site and competitors</h3><p>Satellite view of Isapur, the competitor cluster on the same road, a colour audit of their boards.</p><a href="site.html">Open site analysis</a></div>
<div class="card"><h3>Compare and decide</h3><p>Scorecard, the pole size question, rollout phases, three budget tiers and the open items.</p><a href="compare.html">Open the decision page</a></div></div></div></section>"""
    return shell("index.html", "IIP Brand Kit: three directions", body)


def research_page():
    anatomy = [("Strategy", "Who it is for, what it stands for, one sentence of positioning.", "Yes, one page", "Brand archaeology, long surveys"),
               ("Logo system", "Primary version, clear space, minimum size, backgrounds, misuse.", "Yes", "Redrawing the logo (not allowed here)"),
               ("Colour", "Values for screen and print, usage balance, contrast pairs.", "Yes", "Ten-shade palettes"),
               ("Typography", "Two typefaces at most, Hindi and English behaviour, hierarchy.", "Yes", "Full font licensing detail"),
               ("Graphic devices", "The one or two recurring shapes or patterns that make the brand recognisable.", "Yes", "Icon libraries"),
               ("Voice", "How it speaks: sentence length, language mix, a line bank.", "Yes", "Full tone-of-voice manual"),
               ("Applications", "Real examples at real scale: boards, hoardings, gate, paper, phone.", "Yes, the heart of the pitch", "Every possible item"),
               ("Governance", "File list, print specs, who approves, what to check before print.", "Short version", "Vendor contracts")]
    rows = "".join(f"<tr><td><b>{a}</b></td><td>{b}</td><td>{c}</td><td style='color:var(--mut)'>{d}</td></tr>" for a, b, c, d in anatomy)
    cases = [
        ("McDonald's India", "A fixed visual core, local everything else.", "The arches, the red and yellow, packaging and store layout stay uniform, while the menu and communication are localised. Trade press records that early on the arches meant nothing to Indian customers, so signs needed words like 'Family Restaurant'.", "Keep the logo and colour identical everywhere; let words and offers flex."),
        ("Bata India", "Colour taken straight from the logo, then repeated until it is the shop.", "Red and white stores mirror the logo, and the name is written in Hindi, Bengali, Odia and other scripts where Bata trades. Trust compounds over decades.", "Write the name in Hindi as well as English, and keep one colour pair as the brand's skin."),
        ("boAt", "Sells identity, not specifications.", "Cases describe a brand built on lifestyle, a named community ('boAtheads'), influencers and bold youth-led design rather than technical talk.", "Give the road a voice and a community word; do not list features on a board."),
        ("Kofi Kafi", "One saturated colour, one face, hyper-local naming.", "No published case study was found. From your photograph: a single deep blue light-box, a white wordmark with a smile curve, the outlet named after the place ('Vishwavidyalay'), the menu visible through the glass. We treat this as an observation, not research.", "One colour, one symbol, name the place. A board you can recognise from the far end of the street."),
    ]
    cases_html = "".join(f'<div class="card"><div class="kick">{n}</div><h3>{h}</h3><p>{p}</p><p class="note"><b>What we took:</b> {t}</p></div>' for n, h, p, t in cases)
    src = "".join(f'<div class="card"><h3>{g}</h3><ul>' + "".join(f'<li><a href="{u}" target="_blank" rel="noopener">{t}</a></li>' for t, u in items) + '</ul></div>' for g, items in C.SOURCES)
    body = f"""
<header class="wrap" style="padding-top:60px;padding-bottom:30px"><div class="kick">Research</div><h1>How a brand kit is built, and what makes a brand stick.</h1>
<p class="lead">Before drawing anything we studied what a working brand kit contains, how a board should be presented, and the repeatable mechanics behind brands that became part of everyday India.</p></header>
<section class="first"><div class="wrap"><div class="kick">1 · Anatomy</div><h2>What a brand kit includes, and what it leaves out</h2>
<div class="card scroll" style="padding:6px 14px"><table><tr><th>Section</th><th>What it contains</th><th>In this pitch?</th><th>Left out for now</th></tr>{rows}</table></div>
<p class="note" style="margin-top:20px">Consensus across the guidelines we reviewed: logo with clear space and minimum size, colour with digital and print values, typography, imagery, applications and misuse. Voice is optional in some kits and included here because the road is a place where words matter.</p></div></section>
<section><div class="wrap"><div class="kick">2 · Presenting to a board</div><h2>The order that gets a decision</h2>
<div class="grid g4 keep2">{"".join(f'<div class="card"><div class="stat">{i}</div><h3 style="margin-top:8px">{h}</h3><p style="margin:0;color:var(--mut);font-size:15px">{t}</p></div>' for i,(h,t) in enumerate([("The situation","The road, the competitors, the gap."),("The directions","Three ideas, each with a one-line reason."),("The proof","Real photos, true scale, measured colour."),("The decision","Scorecard, size question, phases, tiers.")],1))}</div>
<p style="margin-top:18px;color:var(--mut)">What a pitch should not claim: approvals, utilities, road widths, plot availability, prices or investment returns that have not been signed off. This deck uses none.</p></div></section>
<section><div class="wrap"><div class="kick">3 · Rooted brands</div><h2>Four Indian brands and the mechanic each shows</h2><div class="grid g2">{cases_html}</div>
<div class="card" style="margin-top:20px"><h3>Five mechanics we applied to IIP</h3><ol><li><b>Own a colour</b> nobody around you owns (Jamun, Gulaal).</li><li><b>One symbol</b>, never redrawn: the rosette stays exactly as drawn.</li><li><b>One repeated sentence</b> that people can say back to you.</li><li><b>Say it in Hindi</b> and write the name in both scripts.</li><li><b>Consistent placement:</b> the same board at the same pole height, at every pole.</li></ol></div></div></section>
<section><div class="wrap"><div class="kick">4 · How this was made</div><h2>Method and honesty notes</h2>
<div class="grid g2"><div class="card"><ul><li>The logo is the supplied artwork, cleaned to a transparent master. Nothing redrawn.</li><li>Every board, hoarding and gate is exact artwork placed into photographs, so the logo and text are never re-drawn by AI.</li><li>The blank scenes (hoarding, gate) were generated with ChatGPT image generation from your own roadside photo as the lighting reference, with a neutral-light, unedited-phone-photo prompt, then the artwork was warped into the blank panel keeping the panel's own shading.</li><li>The pole mockups use your own photographs at true scale (pole face about 10 inch).</li><li>Colour distance is measured with CIEDE2000 on colours sampled from your photographs.</li></ul></div>
<div class="card"><ul><li>Public search found no authoritative description of IIP or its Phase 1 and Phase 2. We used the brief and the Google Maps listing.</li><li>Competitor claims (approvals, prices, road widths) are what their boards say; none verified.</li><li>No cost figures are quoted because none were supplied; the decision page gives structure and cost drivers.</li></ul></div></div></div></section>
<section><div class="wrap"><div class="kick">Sources</div><h2>Reading list</h2><div class="grid g2">{src}</div></div></section>"""
    return shell("research.html", "IIP research", body)


def site_page():
    ch = lambda cols: '<div class="chips">' + "".join(f'<i class="chip" style="background:{c}"></i>' for c in cols) + '</div>'
    comp_rows = [
        ("Shri Balaji Industrial Park (SBJ)", "Sarawa bus stand, Hapur-Modinagar Road", "Blue sky gradient with gold type; a second board in red, brown and gold", "'Industrial plot', 'Government approved' stamp, a per-square-yard price, two phone numbers, rendered township"),
        ("Shri Haridas Industrial Park (SHD)", "Ishapur, Bhojpur, Modinagar, Ghaziabad", "White and navy, Hindi headline", "'Section 80 approved project', rendered gate, 100 ft and 60 ft road, 24 hour electricity and security, monthly maintenance, two phone numbers"),
        ("Shivansh Industrial Park", "Not stated on the board", "Navy and gold, red phone bar", "'All size of industrial plots available', two phone numbers"),
        ("CKS Industrial Park", "Hapur-Modinagar Road (public listing)", "Not photographed", "Public listings quote freehold plots from around Rs 21,990 per sq yd and an approval claim; unverified"),
        ("Atom Industrial Park", "Ishapur, Kilhauda (Google Maps)", "Not photographed", "Listed on Google Maps, 3.1 km down the road"),
        ("Mahamaya Industrial Park", "Near Nahali (Google Maps)", "Not photographed", "Listed on Google Maps"),
    ]
    rows = "".join(f"<tr><td><b>{a}</b></td><td>{b}</td><td>{c}</td><td>{d}</td></tr>" for a, b, c, d in comp_rows)
    body = f"""
<header class="wrap" style="padding-top:60px;padding-bottom:30px"><div class="kick">Site and competitors</div><h1>The road, the rivals and the empty space between them.</h1>
<p class="lead">IIP Phase 1 sits on the Hapur-Modinagar Road at Yusufpur Isapur. For traffic arriving from the Bhojpur side it is the first park on the road, ahead of SHD and CKS, which are both within 700 metres.</p></header>
<section class="first"><div class="wrap"><div class="kick">Locality</div><h2>Satellite view</h2>
{fig("map-isapur.webp", "Satellite view along the Hapur-Modinagar Road, north up. Pins are approximate, taken from Google Maps listings. Imagery is a few years old, so the parks themselves are not yet visible.")}
<div class="grid g3" style="margin-top:20px"><div class="card"><h3>What the land is</h3><p>Flat, intensely farmed land: green and tan field patchwork, tree lines, a handful of villages (Isapur, Bhadola, Kilhauda, Nahali). From the road, boards are seen against foliage, concrete and hazy sky. This is why neither green nor sky blue will work for IIP.</p></div>
<div class="card"><h3>How people arrive</h3><p>Modinagar connects to the Delhi-Meerut Expressway through the Bhojpur exit, which is on the northwest side of IIP. Most visitors from Delhi and Ghaziabad will pass the IIP site first, then the competitor cluster.</p></div>
<div class="card"><h3>Nearby on the Maps listing</h3><p>Pragati Automobile Agriculture Implements, Namaste India plant, Kirpa Ram Dairy, Bhojpur Public School, and a roadside liquor shop near CKS. A mix of agricultural and light industrial neighbours.</p></div></div></div></section>
<section><div class="wrap"><div class="kick">Competitor audit</div><h2>What the other boards say</h2>
<div class="card scroll" style="padding:6px 14px"><table><tr><th>Park</th><th>Where</th><th>Look</th><th>What the board or listing says</th></tr>{rows}</table></div>
<div class="grid g2" style="margin-top:24px">{fig("field-pole-1.webp", "Shri Balaji board, Sarawa. Photo supplied by you.")}{fig("field-pole-stack.webp", "Shri Haridas, Shri Balaji and Shivansh stacked on one pole. Photo supplied by you.")}</div></div></section>
<section><div class="wrap"><div class="kick">Colour audit</div><h2>What is already taken</h2>
<div class="grid g3"><div class="card"><h3>The environment</h3><p style="color:var(--mut);font-size:14px">Dominant colours sampled from the photos.</p>{"".join(f'<p style="margin:10px 0 4px"><b>{n}</b></p>{ch(c)}' for n, c in AN["env"].items())}</div>
<div class="card"><h3>Competitor boards</h3>{"".join(f'<p style="margin:10px 0 4px"><b>{n}</b></p>{ch(c)}' for n, c in AN["comp"].items())}</div>
<div class="card"><h3>What nobody uses</h3><ul><li>Violet or purple</li><li>Rani or magenta pink</li><li>Warm ivory with a heavy black frame</li><li>White space</li><li>A symbol other than a monogram or a house icon</li><li>Hindi as the main language of the headline, except SHD</li></ul></div></div>
<div class="note" style="margin-top:22px"><b>Pattern across every competitor:</b> a rendered gate or township image, a price or approval badge, two phone numbers, navy, gold or red. Copy density is high, so on a pole at 40 km/h only the phone numbers are readable. That is the gap: IIP can be recognised from far away because it carries almost no copy.</div></div></section>"""
    return shell("site.html", "IIP site and competitors", body)


def compare_page():
    cols = list(KITS)
    hdr = "".join(f"<th>{KITS[k]['name']}</th>" for k in cols)
    rows = ""
    tot = {k: 0 for k in cols}
    for crit, a, b, c, note in C.SCORES:
        vals = dict(zip(cols, (a, b, c)))
        for k, v in vals.items(): tot[k] += v
        rows += f"<tr><td><b>{crit}</b><br><span style='color:var(--mut);font-size:13px'>{note}</span></td>" + "".join(f'<td><div class="dots">{"".join("<i class=f></i>" if i < vals[k] else "<i></i>" for i in range(5))}</div>{vals[k]}/5</td>' for k in cols) + "</tr>"
    rows += "<tr><td><b>Total</b></td>" + "".join(f"<td><b>{tot[k]}/{5*len(C.SCORES)}</b></td>" for k in cols) + "</tr>"
    dist_rows = "".join(f"<tr><td>{n}</td>" + "".join(f"<td>{AN['brands'][k]['deltaE'][n]}</td>" for k in cols) + "</tr>" for n in AN["brands"]["jamun"]["deltaE"])
    steps = "".join(f'<div class="card"><h3>{h}</h3><p style="margin:0">{t}</p></div>' for h, t in C.STEPS)
    tiers = "".join(f'<div class="card {"" }"><div class="kick">{n}</div><h3>{d}</h3><p style="color:var(--mut);margin:0">Cost drivers:<br>{c}</p></div>' for n, d, c in C.TIERS)
    body = f"""
<header class="wrap" style="padding-top:60px;padding-bottom:30px"><div class="kick">Compare and decide</div><h1>One recommendation, four decisions.</h1>
<p class="lead">Our recommendation is <b>Jamun</b> as the identity, with Gulaal's pole serial held as an optional campaign layer. Kora is the fallback if the board wants the most conservative route.</p></header>
<section class="first"><div class="wrap"><div class="grid g3">{"".join(f'<a class="kitcard" href="kit-{k}.html">{img(f"{k}-pole-10x14.webp", K["name"], cls="")}<div class="t"><div class="kick">Direction {K["num"]}</div><h3>{K["name"]}</h3><p style="margin:0;color:var(--mut);font-size:15px">{K["one_liner"]}</p></div></a>' for k, K in KITS.items())}</div>
<h2 style="margin-top:40px">Scorecard</h2><div class="card scroll" style="padding:6px 14px"><table><tr><th>Criterion</th>{hdr}</tr>{rows}</table></div>
<p style="color:var(--mut);font-size:14px;margin-top:8px">Scores are our judgement from the measurements on each kit page. Change the weights if the board values something differently.</p></div></section>
<section><div class="wrap"><div class="kick">Proof</div><h2>Colour distance from everything on the road</h2><div class="card scroll" style="padding:6px 14px"><table><tr><th>Measured against</th>{hdr}</tr>{dist_rows}</table></div>
<p style="color:var(--mut);font-size:14px;margin-top:8px">CIEDE2000, main colour of each direction. Above 20 is clearly different, above 40 unmistakable. Kora ivory is closest to hazy sky (16.5), which is why its black frame is mandatory.</p></div></section>
<section><div class="wrap"><div class="kick">Decision 1</div><h2>The pole board size</h2>
<div class="grid g2"><div><p class="lead" style="font-size:19px">A 10 inch board is as wide as the pole face, so it sits neatly, but the competitor boards on the same pole are 18 to 30 inches wide. In the photographs, the Shri Balaji board is roughly twice the width of the pole and the three-board stack is almost four times.</p>
<p class="lead" style="font-size:19px">The kits are designed so that a pole-width board is recognised by colour and logo first. We still recommend pricing one larger option, because the design scales without change.</p>
<div class="note"><b>Recommendation:</b> run 10x14 as the base pole board, and price an 18x25 version for the 15 to 20 poles nearest the competitor cluster.</div></div>
{fig("jamun-pole-18x25.webp", "Same Jamun artwork at 18 x 25 inch, directly under a Shri Balaji board.")}</div></div></section>
<section><div class="wrap"><div class="kick">Decision 2</div><h2>Rollout in five phases</h2><div class="grid g3">{steps}</div></div></section>
<section><div class="wrap"><div class="kick">Decision 3</div><h2>Budget structure: three tiers</h2><p class="lead">No rupee figures are shown because none were supplied. Each tier lists what drives its cost, so vendor quotes can be dropped straight in.</p><div class="grid g3" style="margin-top:20px">{tiers}</div></div></section>
<section><div class="wrap"><div class="kick">Decision 4 and open items</div><h2>What we need from you</h2>
<div class="grid g2"><div class="card"><ul><li><b>Direction:</b> Jamun, Gulaal, Kora, or a named combination.</li><li><b>Phone number</b> (shown as {C.PHONE}) and whether it is a call or WhatsApp line.</li><li><b>Address line.</b> Currently "{C.ADDRESS}", taken from the Google Maps listing. Please confirm.</li><li><b>Vector logo</b> (CDR, AI or SVG) for hoardings and large print.</li></ul></div>
<div class="card"><ul><li><b>Language:</b> Hindi first, or English first.</li><li><b>Claims allowed on boards:</b> approvals, plot sizes, prices. Boards currently carry none.</li><li><b>Phase 1 and Phase 2 naming:</b> small marker on boards or not.</li><li><b>Hoarding sites:</b> exact poles and sites for the highway approaches.</li></ul></div></div></div></section>"""
    return shell("compare.html", "IIP compare and decide", body)


def write(name, s):
    assert "—" not in s and "–" not in s, f"dash in {name}"
    (DOCS / name).write_text(s, encoding="utf-8")


def main():
    global DIAMOND_URI
    import boards as B
    DIAMOND_URI = B.DIAMOND
    prep_assets()
    write("index.html", index_page()); write("research.html", research_page()); write("site.html", site_page())
    for k in KITS: write(f"kit-{k}.html", kit_page(k))
    write("compare.html", compare_page())
    (DOCS / ".nojekyll").write_text("")
    print("ok", sum(f.stat().st_size for f in DOCS.rglob("*") if f.is_file()) // 1024, "KB")


if __name__ == "__main__":
    main()

