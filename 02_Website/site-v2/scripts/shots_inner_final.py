"""Final inner screenshots at 360 and 1440: python scripts/shots_inner_final.py [dist] [port] -> 02_Website/qa/v3/screens/v3final-inner-<page>-<w>.png (full page, CLS printed)"""
import subprocess, sys, time, pathlib
from playwright.sync_api import sync_playwright
SITE = pathlib.Path(__file__).resolve().parent.parent
D = sys.argv[1] if len(sys.argv) > 1 else "dist-inner"; PORT = sys.argv[2] if len(sys.argv) > 2 else "4332"
OUT = SITE.parent / "qa/v3/screens"; OUT.mkdir(parents=True, exist_ok=True)
pages = {p.parent.relative_to(SITE / D).as_posix().replace("/", "_"): "/" + p.parent.relative_to(SITE / D).as_posix() + "/" for p in (SITE / D).rglob("index.html") if p.parent != SITE / D and not p.parent.relative_to(SITE / D).as_posix().startswith("assets")}
pages["404"] = "/404.html"
CLS = "(()=>{let v=0;new PerformanceObserver(l=>{for(const e of l.getEntries())if(!e.hadRecentInput)v+=e.value}).observe({type:'layout-shift',buffered:true});window.__cls=()=>v})()"
srv = subprocess.Popen([sys.executable, "-m", "http.server", PORT, "-d", str(SITE / D)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1.2)
try:
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        for w, h in ((360, 800), (1440, 900)):
            for k, u in pages.items():
                pg = b.new_page(viewport={"width": w, "height": h}, has_touch=w < 768); pg.add_init_script(CLS)
                pg.goto(f"http://127.0.0.1:{PORT}{u}"); pg.wait_for_timeout(900)
                H = pg.evaluate("document.documentElement.scrollHeight")
                for y in range(0, H, 500): pg.evaluate("(y)=>scrollTo(0,y)", y); pg.wait_for_timeout(40)
                pg.evaluate("scrollTo(0,0)"); pg.wait_for_timeout(400)
                pg.screenshot(path=str(OUT / f"v3final-inner-{k}-{w}.png"), full_page=True)
                print(k, w, "CLS", round(pg.evaluate("window.__cls()"), 4), "ow", pg.evaluate("document.documentElement.scrollWidth") > w, "h", H)
                pg.close()
finally:
    srv.terminate()
