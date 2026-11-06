"""Brand book PDF (A4 landscape) printed from the kit page. Run after build_site.py:  python Brand-Kit/_build/build_book.py
Output: Brand-Kit/site/assets/files/ISAPUR-Brand-Book.pdf"""
import pathlib, re
from playwright.sync_api import sync_playwright

KIT = pathlib.Path(__file__).resolve().parents[1]
SITE = KIT / "site"
OUT = SITE / "assets/files/ISAPUR-Brand-Book.pdf"
CSS = """
@page{size:A4 landscape;margin:12mm 12mm 14mm}
html{scroll-behavior:auto}body{display:block;font-size:12px;line-height:1.5}#side{display:none}
main{max-width:none;padding:0;zoom:1.3}
.hero{display:grid;grid-template-columns:90mm 1fr;min-height:176mm;break-after:page;border:0;padding:0;align-content:center}.hero:before{width:150mm;height:150mm;right:-30mm;top:-20mm;opacity:.5}.hero .bar.big{position:absolute;left:0;right:0;bottom:0;margin:0;height:14px}section .bar{margin-bottom:8px}
.hero h1{font-size:44px}.hero .btn,.hero p.small{display:none}
section{break-before:page;padding:0;border:0}section:first-of-type{break-before:auto}
section header{margin-bottom:6px}section h2{font-size:24px}.lead{font-size:14px;max-width:none}
.grid{grid-template-columns:repeat(4,1fr);gap:10px;margin:8px 0}.grid.icons{grid-template-columns:repeat(8,1fr)}.grid.one{grid-template-columns:1fr 1fr}
.card{break-inside:avoid}.card.wide{grid-column:1/-1}.thumb{min-height:0;padding:8px}.thumb img{max-height:48mm}.card.wide .thumb img{max-height:120mm;width:auto}
.dl,.btn{display:none!important}figcaption{padding:6px 8px;font-size:10px}figcaption b{font-size:11px}
table{font-size:10.5px}th,td{padding:5px 7px}h4{margin:12px 0 5px}.two{gap:16px}.sw{grid-template-columns:repeat(6,1fr)}.s i{height:40px}
.toc{break-after:page}.toc ol{columns:2;font-size:15px;line-height:2;list-style:none;padding:0}.toc span{color:#6B7280;margin-right:10px}
footer{display:none}
"""
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1123, "height": 794})
    pg.goto((SITE / "index.html").as_uri()); pg.wait_for_timeout(1500)
    pg.add_style_tag(content=CSS)
    pg.evaluate("""()=>{const n=[...document.querySelectorAll('#side nav li a')].map(a=>`<li><span>${a.querySelector('span').textContent}</span>${a.textContent.slice(2)}</li>`).join('');
      const d=document.createElement('div');d.className='toc';d.innerHTML='<h2 style="font:800 30px Montserrat">Contents</h2><ol>'+n+'</ol>';
      document.querySelector('.hero').after(d)}""")
    pg.emulate_media(media="print")
    pg.pdf(path=str(OUT), format="A4", landscape=True, print_background=True, display_header_footer=True,
           header_template="<span></span>", margin={"top": "12mm", "bottom": "14mm", "left": "12mm", "right": "12mm"},
           footer_template='<div style="font:8px Inter,Arial;color:#6B7280;width:100%;padding:0 12mm;display:flex;justify-content:space-between"><span>ISAPUR Industrial Park, Brand Book v1.0</span><span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>')
    b.close()
print("pdf", OUT.stat().st_size // 1024, "KB")
