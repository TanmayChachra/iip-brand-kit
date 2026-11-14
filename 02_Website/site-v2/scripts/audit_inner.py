"""Mobile audit of every built inner page: python -I scripts/audit_inner.py [dist-folder] [port]. Overflow, tap targets under 44px, text under 16px, img without size, tables."""
import subprocess, sys, time, pathlib, json
from playwright.sync_api import sync_playwright
SITE = pathlib.Path(__file__).resolve().parent.parent
D = sys.argv[1] if len(sys.argv) > 1 else "dist-inner"; PORT = sys.argv[2] if len(sys.argv) > 2 else "4331"
pages = sorted(str(p.parent.relative_to(SITE / D)).replace("\\", "/") for p in (SITE / D).rglob("index.html"))
pages = [p for p in pages if p != "."] + ["404.html"]
JS = """()=>{
 const vw=innerWidth, out={ow:document.documentElement.scrollWidth>vw+1,small:[],tap:[],img:[],wide:[],hover:0};
 const vis=e=>{const r=e.getBoundingClientRect(),s=getComputedStyle(e);return r.width>0&&r.height>0&&s.visibility!='hidden'&&s.display!='none'};
 document.querySelectorAll('a,button,summary,input:not([type=hidden]),select,textarea').forEach(e=>{if(!vis(e)||e.closest('[hidden]'))return;const r=e.getBoundingClientRect();if(e.matches('a')&&getComputedStyle(e).display=='inline'&&e.closest('p,li:not(.keep li),dd'))return;if(r.height<43.5||r.width<43.5)out.tap.push((e.textContent||e.name||'').trim().slice(0,24)+' '+Math.round(r.width)+'x'+Math.round(r.height)+' '+(e.className||e.tagName))});
 document.querySelectorAll('main p,main li,main td,main dd,main summary,.foot p,.foot li,.foot a').forEach(e=>{if(!vis(e))return;const fs=parseFloat(getComputedStyle(e).fontSize);if(fs<15.5&&e.textContent.trim().length>2)out.small.push(fs+' '+(e.className||e.tagName)+' '+e.textContent.trim().slice(0,20))});
 document.querySelectorAll('img').forEach(e=>{if(!e.getAttribute('width')||!e.getAttribute('height'))out.img.push(e.src.slice(-30))});
 document.querySelectorAll('*').forEach(e=>{if(!vis(e)||e.closest('svg'))return;const r=e.getBoundingClientRect();if(r.right>vw+1&&getComputedStyle(e).position!='fixed'&&out.wide.length<4&&!e.closest('.pm,.mm__scroll'))out.wide.push(e.tagName+'.'+e.className+' '+Math.round(r.right))});
 return out}"""
srv = subprocess.Popen([sys.executable, "-m", "http.server", PORT, "-d", str(SITE / D)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1.2)
try:
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        for w, h in ((360, 800), (390, 844), (412, 915), (768, 1024), (1440, 900)):
            print("=====", w)
            for p in pages:
                pg = b.new_page(viewport={"width": w, "height": h}, has_touch=w < 768)
                pg.goto(f"http://127.0.0.1:{PORT}/" + (p if p.endswith(".html") else p + "/")); pg.wait_for_timeout(500)
                r = pg.evaluate(JS)
                bad = {k: (v if not isinstance(v, list) else v[:6]) for k, v in r.items() if v}
                if bad and (w in (360, 768, 1440) or r["ow"]): print(p, json.dumps(bad)[:900])
                pg.close()
finally:
    srv.terminate()
