import sys, threading, http.server, socketserver, functools, pathlib
from playwright.sync_api import sync_playwright
ROOT = pathlib.Path(__file__).resolve().parent
DOCS = ROOT.parent / "docs"
OUT = ROOT / "shots"; OUT.mkdir(exist_ok=True)
H = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(DOCS))
H.log_message = lambda *a, **k: None
srv = socketserver.TCPServer(("127.0.0.1", 8765), H); threading.Thread(target=srv.serve_forever, daemon=True).start()
pages = sys.argv[1:] or ["index", "research", "site", "kit-jamun", "kit-gulaal", "kit-kora", "compare"]
with sync_playwright() as p:
    br = p.chromium.launch()
    for w, tag in [(1280, "d"), (390, "m")]:
        ctx = br.new_context(viewport={"width": w, "height": 900}, device_scale_factor=1)
        for n in pages:
            pg = ctx.new_page(); errs = []
            pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
            pg.goto(f"http://127.0.0.1:8765/{n}.html"); pg.wait_for_load_state("networkidle"); pg.wait_for_timeout(600)
            # force lazy images to load
            pg.evaluate("document.querySelectorAll('img').forEach(i=>i.loading='eager')"); pg.wait_for_timeout(800)
            hs = pg.evaluate("document.documentElement.scrollWidth > innerWidth")
            pg.screenshot(path=str(OUT / f"{n}-{tag}.png"), full_page=True)
            print(n, tag, "hscroll" if hs else "ok", errs[:2]); pg.close()
        ctx.close()
    br.close()
