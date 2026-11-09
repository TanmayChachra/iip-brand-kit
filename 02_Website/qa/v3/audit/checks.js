async page => {
  const base='http://127.0.0.1:4399'; const out={};
  await page.setViewportSize({width:1440,height:900});
  await page.goto(base+'/',{waitUntil:'load'}); await page.waitForTimeout(1200);
  // Tab walk
  const walk=[]; for(let i=0;i<22;i++){ await page.keyboard.press('Tab'); walk.push(await page.evaluate(()=>{const e=document.activeElement; if(!e||e===document.body) return 'body'; const r=e.getBoundingClientRect(); const cs=getComputedStyle(e); const hdr=document.querySelector('header.nav')?.getBoundingClientRect().bottom||0; return (e.tagName+' '+(e.textContent||e.getAttribute('aria-label')||'').trim().slice(0,24)+' | outline '+cs.outlineStyle+' '+cs.outlineWidth+' | top '+Math.round(r.top)+(r.top<hdr&&r.top>=0?' UNDER-HEADER':'')+(r.width===0?' ZERO':''));})); }
  out.tab=walk;
  // contrast
  out.contrast=await page.evaluate(()=>{
    const lum=c=>{const [r,g,b]=c.map(v=>{v/=255;return v<=0.03928?v/12.92:Math.pow((v+0.055)/1.055,2.4)});return .2126*r+.7152*g+.0722*b};
    const parse=s=>{const m=s.match(/rgba?\(([^)]+)\)/); if(!m) return null; const p=m[1].split(/[ ,\/]+/).map(Number); return {c:p.slice(0,3),a:p.length>3?p[3]:1}};
    const bgOf=e=>{let n=e; while(n){const p=parse(getComputedStyle(n).backgroundColor); if(p&&p.a>0.5) return p.c; n=n.parentElement} return [243,245,239]};
    const ratio=(a,b)=>{const l1=lum(a),l2=lum(b);return (Math.max(l1,l2)+.05)/(Math.min(l1,l2)+.05)};
    const sel=['.nav__link','main p','.rows__name','.rows__value','.type-moment','h1','h2','.btn--primary','.btn--secondary','.footer__col a','.footer__legal span','.footer__phones a','label','.credits summary','.visit__rows','.eyebrow','small','.note','.form__hint','input'];
    const res=[]; for(const s of sel){ const e=document.querySelector(s); if(!e) continue; const cs=getComputedStyle(e); const fg=parse(cs.color); if(!fg) continue; const bg=bgOf(e); const r=ratio(fg.c,bg); res.push(s+' '+cs.fontSize+'/'+cs.fontWeight+' '+r.toFixed(2)+(r<4.5?' FAIL':'')); }
    return res;});
  // type scale and spacing
  out.type=await page.evaluate(()=>{const g=s=>{const e=document.querySelector(s); if(!e) return null; const c=getComputedStyle(e); return s+': '+c.fontFamily.split(',')[0]+' '+c.fontSize+' w'+c.fontWeight+' lh '+c.lineHeight+' ls '+c.letterSpacing};
    const sec=[...document.querySelectorAll('main > section')].map(s=>{const c=getComputedStyle(s); return s.id+' '+Math.round(s.getBoundingClientRect().height)+'h pad '+c.paddingTop+'/'+c.paddingBottom+' bg '+c.backgroundColor});
    const btn=document.querySelector('.btn--primary'); const bc=getComputedStyle(btn);
    return {t:['h1','h2','h3','main p','.nav__link','.btn--primary','.rows__name'].map(g),sections:sec,btn:bc.height+' pad '+bc.padding+' radius '+bc.borderRadius+' font '+bc.fontSize, yellow: [...document.querySelectorAll('*')].filter(e=>/255, 214, 0|ffd600/i.test(getComputedStyle(e).backgroundColor+getComputedStyle(e).color+getComputedStyle(e).borderColor)).length, flag: !!document.querySelector('[class*=flag]')}});
  // reduced motion
  await page.emulateMedia({reducedMotion:'reduce'}); await page.goto(base+'/',{waitUntil:'load'}); await page.waitForTimeout(1500);
  out.reduced=await page.evaluate(()=>{const anims=document.getAnimations().filter(a=>a.playState==='running').length; const hidden=[...document.querySelectorAll('main *')].filter(e=>{const c=getComputedStyle(e);return c.opacity==='0'&&e.getBoundingClientRect().height>20}).length; return {runningAnimations:anims, hiddenEls:hidden}});
  await page.emulateMedia({reducedMotion:'no-preference'}); await page.goto(base+'/',{waitUntil:'load'}); await page.waitForTimeout(800);
  out.motion=await page.evaluate(()=>({anims:document.getAnimations().length, scrollListeners:'n/a', tdAll:[...document.styleSheets].flatMap(s=>{try{return [...s.cssRules]}catch(e){return []}}).filter(r=>r.cssText&&/transition:\s*all/.test(r.cssText)).length}));
  // forms
  await page.goto(base+'/contact/',{waitUntil:'load'});
  out.form=await page.evaluate(()=>[...document.querySelectorAll('input,select,textarea')].map(i=>({n:i.name,type:i.type,ac:i.autocomplete,label:!!(i.labels&&i.labels.length)||!!i.getAttribute('aria-label'),req:i.required,im:i.inputMode})));
  out.markdownLeaks=await page.evaluate(()=>{const t=document.body.innerText; return (t.match(/\*\*[^*]+\*\*/g)||[]).slice(0,5)});
  for(const p of ['/faq/','/contact/','/industrial-plots/']){ await page.goto(base+p,{waitUntil:'load'}); out['leaks'+p]=await page.evaluate(()=>{const t=document.body.innerText; return {bold:(t.match(/\*\*[^*]+\*\*/g)||[]).slice(0,4), links:(t.match(/\]\(\/[^)]*\)/g)||[]).slice(0,4)}}); }
  return JSON.stringify(out,null,1);
}
