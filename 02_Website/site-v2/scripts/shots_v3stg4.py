"""Staging round 5 QA: python -I scripts/shots_v3stg4.py  full-page shots of dist-staging at 1100,1280,1440,1920 plus 390 and 768 checks."""
import subprocess, sys, time, pathlib
from playwright.sync_api import sync_playwright
HERE = pathlib.Path(__file__).resolve().parent; SITE = HERE.parent
OUT = SITE.parent / "qa/v3/screens"; OUT.mkdir(parents=True, exist_ok=True)
srv = subprocess.Popen([sys.executable, "-m", "http.server", "4326", "-d", str(SITE / "dist-staging")], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1.2)
CLS = "(()=>{let v=0;new PerformanceObserver(l=>{for(const e of l.getEntries())if(!e.hadRecentInput)v+=e.value}).observe({type:'layout-shift',buffered:true});window.__cls=()=>v})()"
try:
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        for w, h in ((390, 844), (768, 1024), (1100, 800), (1280, 800), (1440, 900), (1920, 1080)):
            pg = b.new_page(viewport={"width": w, "height": h}); pg.add_init_script(CLS)
            pg.goto("http://127.0.0.1:4326/"); pg.wait_for_timeout(4000)
            # scroll through so content-visibility and scroll animations settle
            H = pg.evaluate("document.documentElement.scrollHeight")
            for y in range(0, H, 500): pg.evaluate(f"scrollTo(0,{y})"); pg.wait_for_timeout(60)
            pg.evaluate("scrollTo(0,0)"); pg.wait_for_timeout(500)
            print(w, "hscroll", pg.evaluate("document.documentElement.scrollWidth>innerWidth"), "cls", round(pg.evaluate("__cls()"), 4), "H", H)
            if w >= 1100:
                for sid in ("where","inside","gate","shops","sizes","rent","papers","buying","faq"):
                    r = pg.evaluate(f"(()=>{{const e=document.querySelector('#{sid}').getBoundingClientRect();return [Math.round(e.left),Math.round(e.width),Math.round(e.height)]}})()")
                    print("  ", sid, r)
                for sid in ("where","inside","gate","shops","sizes","rent","papers","buying","faq"):
                    pg.evaluate(f"(()=>{{const e=document.querySelector('#{sid}');const r=e.getBoundingClientRect();scrollTo(0,scrollY+r.top-Math.max(60,(innerHeight-r.height)/2))}})()"); pg.wait_for_timeout(1200)
                    pg.screenshot(path=str(OUT / f"v3stg4-{w}-{sid}.png"))
            else:
                pg.screenshot(path=str(OUT / f"v3stg4-{w}-top.png"))
            pg.close()
finally:
    srv.terminate()
