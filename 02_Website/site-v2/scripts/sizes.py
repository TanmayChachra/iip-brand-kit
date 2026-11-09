import subprocess, sys, time
from playwright.sync_api import sync_playwright
srv = subprocess.Popen([sys.executable, "-m", "http.server", "4323", "-d", "dist"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
try:
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        for w in (1440, 390):
            pg = b.new_page(viewport={"width": w, "height": 900 if w > 800 else 844}); pg.goto("http://127.0.0.1:4323" + (sys.argv[1] if len(sys.argv) > 1 else "/")); pg.wait_for_timeout(600)
            print(w, pg.evaluate("[...document.querySelectorAll('h1,h2,.fact b,.type-moment a')].map(e=>e.tagName+'.'+e.className+' '+getComputedStyle(e).fontSize+' '+e.textContent.trim().slice(0,20)).join(' | ')"))
        b.close()
finally: srv.terminate()
