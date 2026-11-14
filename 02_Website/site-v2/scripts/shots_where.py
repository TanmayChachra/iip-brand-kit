"""Where section shots: python scripts/shots_where.py (serves dist on 4325, writes qa/v3/screens/v3where2-*.png, prints CLS and payload)"""
import subprocess, sys, time, pathlib
from playwright.sync_api import sync_playwright
HERE = pathlib.Path(__file__).resolve().parent; SITE = HERE.parent
OUT = SITE.parent / "qa/v3/screens"; OUT.mkdir(parents=True, exist_ok=True)
srv = subprocess.Popen([sys.executable, "-m", "http.server", "4325", "-d", str(SITE / "dist")], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1.2)
CLS = "(()=>{let v=0;new PerformanceObserver(l=>{for(const e of l.getEntries())if(!e.hadRecentInput)v+=e.value}).observe({type:'layout-shift',buffered:true});window.__cls=()=>v})()"
try:
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        for w, h, tag in ((1440, 900, "1440"), (390, 844, "390")):
            pg = b.new_page(viewport={"width": w, "height": h}); pg.add_init_script(CLS)
            reqs = []; pg.on("response", lambda r: reqs.append(r.url))
            pg.goto("http://127.0.0.1:4325/"); pg.wait_for_timeout(1200)
            print(tag, "data loaded before scroll:", any("where-region" in u for u in reqs))
            pg.evaluate("()=>{const e=document.querySelector('.wr__stage');window.scrollTo(0,e.getBoundingClientRect().top+scrollY-Math.max(70,(innerHeight-e.offsetHeight)/2))}")
            pg.wait_for_timeout(1000); pg.screenshot(path=str(OUT / f"v3where2-{tag}-1s.png"))
            pg.wait_for_timeout(5000); pg.screenshot(path=str(OUT / f"v3where2-{tag}-6s.png"))
            pg.locator(".wr__stage").screenshot(path=str(OUT / f"v3where2-{tag}-map.png"))
            pg.evaluate("()=>{const e=document.querySelector('.lad');window.scrollTo(0,e.getBoundingClientRect().top+scrollY-120)}"); pg.wait_for_timeout(1500)
            pg.screenshot(path=str(OUT / f"v3where2-{tag}-ladder.png"))
            pg.evaluate("()=>{const e=document.querySelector('.wr__stage');window.scrollTo(0,e.getBoundingClientRect().top+scrollY-Math.max(70,(innerHeight-e.offsetHeight)/2))}")
            pg.click(".wr__tab[data-v=park]"); pg.wait_for_timeout(900)
            pg.screenshot(path=str(OUT / f"v3where2-{tag}-park.png")); pg.locator(".wr__stage").screenshot(path=str(OUT / f"v3where2-{tag}-parkmap.png"))
            pg.click(".wr__tab[data-v=region]"); pg.wait_for_timeout(500)
            pg.hover(".lad__r[data-k=meerut]") if w > 700 else None; pg.wait_for_timeout(500)
            pg.locator(".wr__stage").screenshot(path=str(OUT / f"v3where2-{tag}-hover.png"))
            print(tag, "cls", pg.evaluate("window.__cls()"), "data-m", pg.evaluate("document.querySelector('[data-wr]').dataset.m"))
            pg.close()
        b.close()
finally:
    srv.terminate()
