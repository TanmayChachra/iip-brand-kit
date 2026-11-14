"""Inner page screenshots + CLS: python -I scripts/shots_inner.py  (serves dist on 4324, writes 02_Website/qa/v3/screens/v3inner-*.png, full page at 1440 and 390)"""
import subprocess, sys, time, pathlib
from playwright.sync_api import sync_playwright
HERE = pathlib.Path(__file__).resolve().parent; SITE = HERE.parent
OUT = SITE.parent / "qa/v3/screens"; OUT.mkdir(parents=True, exist_ok=True)
PAGES = {"location": "/location/", "loc-modinagar": "/location/industrial-plots-in-modinagar/", "faq": "/faq/", "contact": "/contact/", "approvals": "/approvals/", "plotmaps": "/plot-maps/", "blog": "/blog/", "post": "/blog/how-to-choose-an-industrial-plot/", "plots": "/industrial-plots/", "amenities": "/amenities/", "neighbours": "/neighbours/", "about": "/about/", "privacy": "/privacy/", "404": "/404.html"}
only = sys.argv[1:] or list(PAGES)
srv = subprocess.Popen([sys.executable, "-m", "http.server", "4324", "-d", str(SITE / "dist")], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1.2)
CLS = "(()=>{let v=0;new PerformanceObserver(l=>{for(const e of l.getEntries())if(!e.hadRecentInput)v+=e.value}).observe({type:'layout-shift',buffered:true});window.__cls=()=>v})()"
try:
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        for w, h in ((1440, 900), (390, 844)):
            for k in only:
                pg = b.new_page(viewport={"width": w, "height": h}); pg.add_init_script(CLS)
                errs = []; pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
                pg.goto("http://127.0.0.1:4324" + PAGES[k]); pg.wait_for_timeout(1500)
                H = pg.evaluate("document.documentElement.scrollHeight")
                for y in range(0, H, 500): pg.evaluate("(y)=>scrollTo(0,y)", y); pg.wait_for_timeout(60)
                pg.evaluate("scrollTo(0,0)"); pg.wait_for_timeout(700)
                ow = pg.evaluate("document.documentElement.scrollWidth")
                pg.screenshot(path=str(OUT / f"v3inner-{k}-{w}.png"), full_page=True)
                print(k, w, "CLS", round(pg.evaluate("window.__cls()"), 4), "overflowX", ow > w, "h", H, "errors", errs[:2])
                pg.close()
finally:
    srv.terminate()
