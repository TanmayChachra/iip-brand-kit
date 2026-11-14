"""Map section shots: python scripts/shots_map.py  (serves dist on 4324, writes 02_Website/qa/v3/screens/v3map-*.png, prints CLS)"""
import subprocess, sys, time, pathlib
from playwright.sync_api import sync_playwright
HERE = pathlib.Path(__file__).resolve().parent; SITE = HERE.parent
OUT = SITE.parent / "qa/v3/screens"; OUT.mkdir(parents=True, exist_ok=True)
srv = subprocess.Popen([sys.executable, "-m", "http.server", "4324", "-d", str(SITE / "dist")], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1.2)
CLS = "(()=>{let v=0;new PerformanceObserver(l=>{for(const e of l.getEntries())if(!e.hadRecentInput)v+=e.value}).observe({type:'layout-shift',buffered:true});window.__cls=()=>v})()"
try:
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        for w, h, tag in ((1440, 900, "1440"), (390, 844, "390")):
            pg = b.new_page(viewport={"width": w, "height": h}); pg.add_init_script(CLS)
            pg.goto("http://127.0.0.1:4324/"); pg.wait_for_timeout(1500)
            pg.evaluate("()=>{const e=document.querySelector('.regmap');window.scrollTo(0,e.getBoundingClientRect().top+scrollY-(innerHeight-e.offsetHeight)/2)}")
            pg.wait_for_timeout(300); pg.screenshot(path=str(OUT / f"v3map-start-{tag}.png"))
            pg.wait_for_timeout(3200)
            pg.locator(".regmap").screenshot(path=str(OUT / f"v3map-fig-{tag}.png"))
            pg.screenshot(path=str(OUT / f"v3map-section-{tag}.png"))
            pg.wait_for_timeout(1000); pg.screenshot(path=str(OUT / f"v3map-ping-{tag}.png"), clip=None)
            print(tag, "state", pg.evaluate("()=>[document.querySelector('.regmap').dataset.m,document.querySelector('.regmap').hasAttribute('data-live')]"), "cls", pg.evaluate("window.__cls()"))
            pg.evaluate("window.scrollTo(0,0)"); pg.wait_for_timeout(300)
            print(tag, "state-off", pg.evaluate("()=>document.querySelector('.regmap').hasAttribute('data-live')"))
finally:
    srv.terminate()
