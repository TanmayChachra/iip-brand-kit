async page => {
  const base='http://127.0.0.1:4399'; const out={};
  for (const [w,h] of [[1440,900],[390,844]]) {
    await page.setViewportSize({width:w,height:h});
    for (const p of ['/','/industrial-plots/','/location/','/neighbours/','/contact/']) {
      await page.goto(base+p,{waitUntil:'load'}); await page.waitForTimeout(500);
      out[w+p]=await page.evaluate(()=>{
        const nameOf=e=>(e.getAttribute('aria-label')||e.textContent||[...e.querySelectorAll('img')].map(i=>i.alt).join(' ')||'').trim();
        const links=[...document.querySelectorAll('a')].filter(a=>a.getBoundingClientRect().width>0);
        const hs=[...document.querySelectorAll('h1,h2,h3,h4')].map(h=>+h.tagName[1]); let skip=0; for(let i=1;i<hs.length;i++) if(hs[i]>hs[i-1]+1) skip++;
        const hero=document.querySelector('main img'); const imgs=[...document.querySelectorAll('main img')];
        const srcs=imgs.map(i=>(i.currentSrc||'').split('/').pop().replace(/-(hero|43|sq|m)-\d+/,'').replace('.webp',''));
        const dup=srcs.filter((s,i)=>srcs.indexOf(s)!==i);
        const fs=[...document.querySelectorAll('main p, main li')].map(e=>parseFloat(getComputedStyle(e).fontSize)); 
        return {unnamedLinks:links.filter(a=>!nameOf(a)).length, headingSkips:skip, dupPhotos:dup, heroFetch:hero&&hero.getAttribute('fetchpriority'), heroLoading:hero&&hero.loading, imgNoDims:imgs.filter(i=>!i.getAttribute('width')||!i.getAttribute('height')).length, minBody:Math.min(...fs), themeColor:document.querySelector('meta[name=theme-color]')?.content, viewport:document.querySelector('meta[name=viewport]')?.content, title:document.title.length, desc:(document.querySelector('meta[name=description]')?.content||'').length, canon:!!document.querySelector('link[rel=canonical]'), ld:document.querySelectorAll('script[type="application/ld+json"]').length, mapImg: !!document.querySelector('img[src*="map-park"]'), words:document.body.innerText.split(/\s+/).length}
      });
    }
  }
  return JSON.stringify(out);
}
