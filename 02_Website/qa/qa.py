"""QA for 02_Website/site/dist: serve locally, screenshots (WEBP), internal links, one H1 + one canonical per page, claim scan, bytes per page.
Run after `npm run build` in 02_Website/site:  python 02_Website/qa/qa.py   Writes qa/screenshots/*.webp and qa/qa.json"""
import functools, http.server, json, pathlib, re, socketserver, threading, gzip
from PIL import Image
from playwright.sync_api import sync_playwright

Q = pathlib.Path(__file__).resolve().parent
DIST = Q.parent / "site/dist"
SHOTS = Q / "screenshots"; SHOTS.mkdir(exist_ok=True)
NOT_ALLOWED = ["section 80", "zilla panchayat", "drainage", "24 hour", "24-hour", "24x7", "security", "amul", "inox", "patanjali", "petrol", "approved", "legally compliant"]  # claims without proof
PORT = 4399


class H(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass


def serve():
    h = functools.partial(H, directory=str(DIST)); s = socketserver.TCPServer(("127.0.0.1", PORT), h); s.allow_reuse_address = True
    threading.Thread(target=s.serve_forever, daemon=True).start(); return s


pages = sorted(p.relative_to(DIST).as_posix() for p in DIST.rglob("index.html"))
urls = {p: "/" + p.replace("index.html", "") for p in pages}
res = {"pages": {}, "broken_links": [], "claims_hits": [], "problems": []}
known = set(urls.values()) | {"/404.html"}
for p in DIST.rglob("*"):
    if p.is_file() and p.suffix not in (".html",): known.add("/" + p.relative_to(DIST).as_posix())
for rel, url in urls.items():
    html = (DIST / rel).read_text(encoding="utf-8")
    h1 = len(re.findall(r"<h1[ >]", html)); can = len(re.findall(r'<link rel="canonical"', html))
    size = len(html.encode()); gz = len(gzip.compress(html.encode()))
    res["pages"][url] = {"h1": h1, "canonical": can, "html_kb": round(size / 1024, 1), "html_gzip_kb": round(gz / 1024, 1), "schema": len(re.findall("application/ld\\+json", html)), "title": (re.search(r"<title>(.*?)</title>", html) or [0, ""])[1], "desc_len": len((re.search(r'name="description" content="(.*?)"', html) or [0, ""])[1])}
    if h1 != 1 or can != 1: res["problems"].append(f"{url}: h1={h1} canonical={can}")
    for href in set(re.findall(r'href="(/[^"#?]*)', html)) | set(re.findall(r'src="(/[^"#?]*)', html)):
        if href not in known and not (DIST / href.lstrip("/")).exists(): res["broken_links"].append(f"{url} -> {href}")
    text = re.sub(r"<script.*?</script>|<style.*?</style>", "", html, flags=re.S); text = re.sub(r"<[^>]+>", " ", text).lower()
    for c in NOT_ALLOWED:
        if c in text: res["claims_hits"].append(f"{url}: '{c}'")
s = serve()
with sync_playwright() as pw:
    b = pw.chromium.launch()
    for name, w, h in (("mobile", 390, 844), ("desktop", 1280, 900)):
        pg = b.new_page(viewport={"width": w, "height": h})
        for slug in ("", "industrial-plots/", "location/", "faq/", "contact/"):
            pg.goto(f"http://127.0.0.1:{PORT}/{slug}"); pg.evaluate("async()=>{for(let y=0;y<document.body.scrollHeight;y+=400){window.scrollTo(0,y);await new Promise(r=>setTimeout(r,80))}window.scrollTo(0,0)}"); pg.wait_for_timeout(600)
            out = SHOTS / f"{name}-{slug.strip('/') or 'home'}.png"; pg.screenshot(path=str(out), full_page=True)
            im = Image.open(out).convert("RGB"); im.thumbnail((1000, 6000)); im.save(out.with_suffix(".webp"), quality=70, method=6); out.unlink()
        if name == "mobile": res["mobile_overflow_x"] = pg.evaluate("document.documentElement.scrollWidth>window.innerWidth")
    b.close()
s.shutdown()
(Q / "qa.json").write_text(json.dumps(res, indent=1), encoding="utf-8")
print("pages", len(pages), "problems", res["problems"], "broken", len(res["broken_links"]), "claims", res["claims_hits"][:8], "overflow", res.get("mobile_overflow_x"))
