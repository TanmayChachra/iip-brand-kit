async page => {
  const base = 'http://127.0.0.1:4399';
  const pages = { home: '/', plots: '/industrial-plots/', location: '/location/', neighbours: '/neighbours/', faq: '/faq/', contact: '/contact/' };
  const sizes = { '1440': [1440, 900], '1024': [1024, 768], '390': [390, 844] };
  const out = {};
  const errs = [];
  page.on('console', m => { if (m.type() === 'error' || m.type() === 'warning') errs.push(m.type() + ': ' + m.text().slice(0, 160)); });
  page.on('requestfailed', r => errs.push('requestfailed: ' + r.url().slice(0, 120)));
  for (const [sz, [w, h]] of Object.entries(sizes)) {
    await page.setViewportSize({ width: w, height: h });
    for (const [name, path] of Object.entries(pages)) {
      await page.goto(base + path, { waitUntil: 'load' });
      await page.evaluate(async () => { const H = document.body.scrollHeight; for (let y = 0; y < H; y += 400) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 90)); } window.scrollTo(0, 0); await new Promise(r => setTimeout(r, 500)); });
      await page.screenshot({ path: `screenshots/${name}-${sz}.png`, fullPage: true });
      out[`${name}-${sz}`] = await page.evaluate((w) => {
        const q = s => [...document.querySelectorAll(s)];
        const vis = e => { const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0; };
        const small = q('a,button,input,select,textarea,summary').filter(vis).filter(e => { const r = e.getBoundingClientRect(); return (r.height < 44 || r.width < 44) && !e.closest('p,li,.prose') ; }).map(e => (e.textContent || e.getAttribute('aria-label') || e.tagName).trim().slice(0, 28) + ' ' + Math.round(e.getBoundingClientRect().width) + 'x' + Math.round(e.getBoundingClientRect().height));
        const imgs = q('img').map(i => ({ src: i.currentSrc.split('/').pop(), nw: i.naturalWidth, dw: Math.round(i.getBoundingClientRect().width), ok: i.complete && i.naturalWidth > 0, alt: i.alt }));
        return { scrollW: document.documentElement.scrollWidth, innerW: w, overflow: document.documentElement.scrollWidth > w + 1, h: document.documentElement.scrollHeight, h1: q('h1').length, small: small.slice(0, 12), smallN: small.length,
          badImgs: imgs.filter(i => !i.ok).map(i => i.src), upscaled: imgs.filter(i => i.ok && i.nw < i.dw * (window.devicePixelRatio || 1) * 0.95).map(i => i.src + ' ' + i.nw + '<' + i.dw), noAlt: imgs.filter(i => i.alt === null || i.alt === undefined).length, imgSrcs: imgs.map(i => i.src) };
      }, w);
    }
  }
  out.console = errs.slice(0, 30);
  return JSON.stringify(out);
}
