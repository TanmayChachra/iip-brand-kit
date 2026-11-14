"""Staging round 3 QA: python -I scripts/shots_v3stg3.py  (serves dist-staging on 4325, writes 02_Website/qa/v3/screens/v3stg3-*.png)
Measures overlaps of visible text in the hero map for All and each phase at 360, 390, 1440 (target zero), horizontal scroll, CLS, hero fold at 1440x900, cookie link style."""
import subprocess, sys, time, pathlib, json
from playwright.sync_api import sync_playwright
HERE = pathlib.Path(__file__).resolve().parent; SITE = HERE.parent
OUT = SITE.parent / "qa/v3/screens"; OUT.mkdir(parents=True, exist_ok=True)
srv = subprocess.Popen([sys.executable, "-m", "http.server", "4325", "-d", str(SITE / "dist-staging")], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1.2)
CLS = "(()=>{let v=0;new PerformanceObserver(l=>{for(const e of l.getEntries())if(!e.hadRecentInput)v+=e.value}).observe({type:'layout-shift',buffered:true});window.__cls=()=>v})()"
MEAS = """()=>{const vp=document.querySelector('.mm[data-mm] .mm__vp').getBoundingClientRect();const r=[];
for(const t of document.querySelectorAll('.mm[data-mm] text')){if(t.style.display==='none')continue;const b=t.getBoundingClientRect();if(b.width<1||b.height<1)continue;
if(b.right<vp.left||b.left>vp.right||b.bottom<vp.top||b.top>vp.bottom)continue;r.push([b.left,b.top,b.right,b.bottom,t.textContent.trim().slice(0,14)])}
let o=[];for(let i=0;i<r.length;i++)for(let j=i+1;j<r.length;j++){const a=r[i],c=r[j];if(Math.min(a[2],c[2])-Math.max(a[0],c[0])>0.6&&Math.min(a[3],c[3])-Math.max(a[1],c[1])>0.6)o.push(a[4]+'|'+c[4])}
return {n:r.length,o:o.slice(0,8),no:o.length}}"""
try:
    with sync_playwright() as pw:
        b = pw.chromium.launch(); bad = 0
        for w, h in ((360, 780), (390, 844), (412, 880), (1100, 800), (1280, 800), (1440, 900), (1920, 1080)):
            pg = b.new_page(viewport={"width": w, "height": h}); pg.add_init_script(CLS)
            pg.goto("http://127.0.0.1:4325/"); pg.wait_for_timeout(5000)
            sx = pg.evaluate("document.documentElement.scrollWidth>innerWidth"); cls = pg.evaluate("__cls()")
            print(w, "hscroll", sx, "cls", round(cls, 4))
            if w in (360, 390, 1440, 1920): pg.screenshot(path=str(OUT / f"v3stg3-hero-{w}.png"))
            if w >= 1100:
                print("  fold: directions bottom", pg.evaluate("document.querySelector('[data-cta-id=directions]').getBoundingClientRect().bottom"), "of", h)
            pg.locator(".mm[data-mm] .mm__vp").scroll_into_view_if_needed()
            if w < 700: pg.evaluate("document.querySelector('.mm[data-mm]').scrollIntoView()")
            for ph in (0, 1, 2, 3):
                pg.click(f".mm[data-mm] .mm__chip[data-ph='{ph}']"); pg.wait_for_timeout(1100)
                m = pg.evaluate(MEAS); bad += m["no"]; print(f"  phase {ph}: texts {m['n']} overlaps {m['no']} {m['o']}")
                if w in (360, 390, 1440) and ph in (0, 2): pg.screenshot(path=str(OUT / f"v3stg3-map-ph{ph}-{w}.png"))
            # zoom in with wheel at desktop, buttons on phones
            for _ in range(3): pg.click(".mm[data-mm] .mm__zoom [data-z=in]"); pg.wait_for_timeout(500)
            m = pg.evaluate(MEAS); bad += m["no"]; print(f"  zoomed: texts {m['n']} overlaps {m['no']} {m['o']}")
            if w in (360, 1440): pg.screenshot(path=str(OUT / f"v3stg3-map-zoom-{w}.png"))
            if w in (360, 390, 1440, 1920):
                pg.evaluate("window.scrollTo(0,document.body.scrollHeight)"); pg.wait_for_timeout(500)
                st = pg.evaluate("""()=>{const a=document.querySelector('.flegal a'),c=document.querySelector('[data-consent-open]'),A=getComputedStyle(a),C=getComputedStyle(c);const p=['fontFamily','fontSize','fontWeight','color','backgroundColor','borderTopWidth','textDecorationLine'];return {a:p.map(k=>A[k]),c:p.map(k=>C[k]),h:c.getBoundingClientRect().height}}""")
                print("  cookie", st)
                pg.locator(".flegal").screenshot(path=str(OUT / f"v3stg3-foot-{w}.png"))
            pg.close()
        print("TOTAL OVERLAPS", bad)
finally:
    srv.terminate()
