"""Home screenshots: python -I scripts/shots_home.py  (serves dist on 4323, writes 02_Website/qa/v3/screens/v3r3-*.png)
Round 3: one viewport shot per section, the six scrubbed build stages (text step centred), a mid-stage, the finder lit, the map zoomed, the visit shutter at five scroll positions, CLS."""
import subprocess, sys, time, pathlib
from playwright.sync_api import sync_playwright
HERE = pathlib.Path(__file__).resolve().parent; SITE = HERE.parent
OUT = SITE.parent / "qa/v3/screens"; OUT.mkdir(parents=True, exist_ok=True)
srv = subprocess.Popen([sys.executable, "-m", "http.server", "4323", "-d", str(SITE / "dist")], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1.2)
SECS = ["build", "where", "road", "inside", "gate", "shops", "sizes", "papers", "buying", "faq"]
CLS = "(()=>{let v=0;new PerformanceObserver(l=>{for(const e of l.getEntries())if(!e.hadRecentInput)v+=e.value}).observe({type:'layout-shift',buffered:true});window.__cls=()=>v})()"
try:
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        for w, h, tag in ((1440, 900, "1440"), (390, 844, "390")):
            pg = b.new_page(viewport={"width": w, "height": h})
            pg.add_init_script(CLS)
            pg.goto("http://127.0.0.1:4323/"); pg.wait_for_timeout(6500)
            pg.screenshot(path=str(OUT / f"v3r3-01-hero-{tag}.png"))
            vp = pg.locator(".mm__vp").bounding_box(); cx, cy = vp["x"] + vp["width"] / 2, vp["y"] + vp["height"] / 2
            if w > 700:
                pg.mouse.move(cx, cy)
                for _ in range(4): pg.mouse.wheel(0, -100); pg.wait_for_timeout(30)
                pg.wait_for_timeout(600)
                pg.screenshot(path=str(OUT / f"v3r3-01-hero-zoomed-{tag}.png"))
                pg.click(".mm__rst"); pg.wait_for_timeout(800)
            pg.click(".mm__chip[data-ph='2']"); pg.wait_for_timeout(900)
            pg.screenshot(path=str(OUT / f"v3r3-01-hero-phase2-{tag}.png"))
            pg.click(".mm__chip[data-ph='0']"); pg.wait_for_timeout(700)
            for i, s in enumerate(SECS, start=2):
                pg.evaluate("(id)=>{const e=document.getElementById(id);const o=document.querySelector('.nav').offsetHeight;window.scrollTo(0,e.getBoundingClientRect().top+scrollY-o)}", s); pg.wait_for_timeout(700)
                pg.screenshot(path=str(OUT / f"v3r3-{i:02d}-{s}-{tag}.png"))
            q = 0.5 if w > 1023 else 0.68
            for i in range(6):
                y = pg.evaluate("([i,q])=>{const li=document.querySelector('.bsteps').children[i];const r=li.getBoundingClientRect();return r.top+scrollY+r.height/2-innerHeight*q}", [i, q])
                pg.evaluate("(y)=>scrollTo(0,y)", y); pg.wait_for_timeout(500)
                pg.screenshot(path=str(OUT / f"v3r3-stage-{i + 1}-{tag}.png"))
            pg.evaluate("(y)=>scrollTo(0,y)", y - 160); pg.wait_for_timeout(400)
            pg.screenshot(path=str(OUT / f"v3r3-stage-mid-{tag}.png"))
            pg.evaluate("(id)=>{const e=document.getElementById(id);window.scrollTo(0,e.getBoundingClientRect().top+scrollY-document.querySelector('.nav').offsetHeight)}", "sizes"); pg.wait_for_timeout(500)
            pg.click("[data-band=b2]"); pg.wait_for_timeout(800)
            pg.screenshot(path=str(OUT / f"v3r3-finder-b2-{tag}.png"))
            top = pg.evaluate("(()=>{const e=document.querySelector('.fin__run');return e.getBoundingClientRect().top+scrollY})()")
            for nm, off in (("1-closed", 0.92), ("2-lifting", 1.2), ("3-lifted", 1.45), ("4-truck", 1.7), ("5-end", 1.95)):
                pg.evaluate("(y)=>scrollTo(0,y)", top - 72 + (off - 0.92) * h); pg.wait_for_timeout(600)
                pg.screenshot(path=str(OUT / f"v3r3-visit-{nm}-{tag}.png"))
            pg.evaluate("window.scrollTo(0,document.body.scrollHeight)"); pg.wait_for_timeout(700)
            pg.screenshot(path=str(OUT / f"v3r3-bottom-{tag}.png"))
            print(tag, "page height", pg.evaluate("document.body.scrollHeight"), "screens", round(pg.evaluate("document.body.scrollHeight") / h, 1), "CLS", pg.evaluate("window.__cls()"))
            pg.close()
        b.close()
finally:
    srv.terminate()
