"""Screenshots of built pages: python scripts/shots.py <outdir> <path>... (serves dist on 4322)."""
import subprocess, sys, time, pathlib
from playwright.sync_api import sync_playwright
from PIL import Image
out = pathlib.Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
pages = sys.argv[2:] or ["/"]
srv = subprocess.Popen([sys.executable, "-m", "http.server", "4322", "-d", "dist"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1.2)
try:
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        for w, h, tag in ((1440, 900, "d"), (390, 844, "m")):
            pg = b.new_page(viewport={"width": w, "height": h})
            for p in pages:
                p = "/" if p in ("-", "home") else ("/" + p.strip("/") + "/"); pg.goto("http://127.0.0.1:4322" + p); pg.wait_for_timeout(700)
                H = pg.evaluate("document.body.scrollHeight")
                for y in range(0, H, 400): pg.evaluate(f"window.scrollTo(0,{y})"); pg.wait_for_timeout(100)
                pg.evaluate("window.scrollTo(0,0)"); pg.wait_for_timeout(1800)
                name = (p.strip("/").replace("/", "_") or "home") + "-" + tag
                pg.screenshot(path=str(out / (name + ".png")), full_page=True)
                im = Image.open(out / (name + ".png")).convert("RGB"); im.thumbnail((w if w < 800 else 1100, 12000)); im.save(out / (name + ".webp"), quality=74); (out / (name + ".png")).unlink()
        b.close()
finally:
    srv.terminate()
