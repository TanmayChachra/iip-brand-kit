// Home page behaviour. Everything works without it: size chips are plain links, the drawing shows every plot, the finished shed is shown.
// motion/mini is loaded on first use (finder click), not at page load
const animate = (...a) => import('motion/mini').then((m) => m.animate(...a));
const $ = (s, r = document) => r.querySelector(s), $$ = (s, r = document) => [...r.querySelectorAll(s)];
const root = document.documentElement;
const EASE = [0.23, 1, 0.32, 1];
const still = matchMedia('(prefers-reduced-motion: reduce)').matches;

// 1. Open now (Asia/Kolkata). Hours: 8 am to 8 pm every day except Tuesday.
$$('[data-open-now]').forEach((el) => {
  try {
    const p = {};
    new Intl.DateTimeFormat('en-GB', { timeZone: 'Asia/Kolkata', weekday: 'short', hour: 'numeric', minute: 'numeric', hourCycle: 'h23' }).formatToParts(new Date()).forEach((x) => (p[x.type] = x.value));
    const m = +p.hour * 60 + +p.minute, d = p.weekday, open = d !== 'Tue' && m >= 480 && m < 1200;
    el.textContent = open ? 'Open now, until 8 pm' : d === 'Tue' ? 'Closed today, opens Wednesday at 8 am' : m < 480 ? 'Closed now, opens today at 8 am' : d === 'Mon' ? 'Closed now, opens Wednesday at 8 am' : 'Closed now, opens tomorrow at 8 am';
    el.classList.toggle('is-closed', !open);
  } catch (e) { /* keep the static text */ }
});

// 2. Size finder: chips light up plots on the layout and scale the shed footprint on the plan.
const lay = $('.lay'), out = $('#find-out'), ask = $('#find-ask'), chips = $$('[data-band]');
if (lay && out && chips.length) {
  const base = out.innerHTML, cap = $('#find-cap');
  let cur = '';
  const swap = (fn) => { fn(); if (!still) animate(out, { opacity: [0, 1], transform: ['translateY(6px)', 'none'] }, { duration: 0.28, ease: EASE }); };
  const pick = (c) => {
    const b = c && c.dataset.band !== cur ? c.dataset.band : '';
    cur = b;
    chips.forEach((x) => x.setAttribute('aria-pressed', x === c && b ? 'true' : 'false'));
    const sc = b ? c.dataset.sc : '';
    $$('.shedsvg[data-shed=ghost]').forEach((s) => (sc ? s.style.setProperty('--sc', sc) : s.style.removeProperty('--sc')));
    if (cap) cap.textContent = b ? `A shed on a plot of ${c.dataset.label}.` : 'A shed on a plot.';
    if (b) {
      lay.setAttribute('data-sel', b);
      swap(() => (out.innerHTML = `<b>${c.dataset.n} plots</b> in this size<small>Lit up on the map.</small>`));
      ask.href = c.dataset.wa;
      if (ask.hidden) { ask.hidden = false; if (!still) animate(ask, { opacity: [0, 1], transform: ['translateY(6px)', 'none'] }, { duration: 0.28, ease: EASE }); }
    } else {
      lay.removeAttribute('data-sel'); swap(() => (out.innerHTML = base)); ask.hidden = true;
    }
  };
  chips.forEach((c) => {
    c.setAttribute('role', 'button'); c.setAttribute('aria-pressed', 'false');
    c.addEventListener('click', (e) => { e.preventDefault(); pick(c); });
    c.addEventListener('keydown', (e) => { if (e.key === ' ') { e.preventDefault(); pick(c); } });
  });
}

// 3. Ink drawings: keep every line about 1.25 px wide at any size (--sw is in drawing units).
const setSw = (s) => { const vb = s.viewBox.baseVal, r = s.getBoundingClientRect(), sc = Math.min(r.width / vb.width, r.height / vb.height); if (sc > 0) s.style.setProperty('--sw', `${Math.min(3.2, 1.25 / sc).toFixed(2)}px`); };
const inkInit = () => { if ('ResizeObserver' in window) { const ro = new ResizeObserver((es) => es.forEach((e) => setSw(e.target))); $$('.ink').forEach((s) => ro.observe(s)); } else $$('.ink').forEach(setSw); };
('requestIdleCallback' in window ? requestIdleCallback(inkInit, { timeout: 1500 }) : setTimeout(inkInit, 600));

// 4. Browsers without scroll-driven animations: the same keyframes are scrubbed (paused, position set by --t) from motion's scroll(). Nothing runs where CSS timelines work.
if (!CSS.supports('animation-timeline', 'view()') && !still) {
  root.classList.add('nosd');
  const gs = (el, n) => getComputedStyle(el).getPropertyValue(n);
  const ks = $$('.k').map((el) => ({ el, tl: gs(el, '--tl').trim(), i: +gs(el, '--i') || 0, s: +gs(el, '--s') || 0, e: +gs(el, '--e') || 1, r0: +gs(el, '--r0') || 0, rw: +gs(el, '--rw') || 0, rh: +gs(el, '--rh') || 0 }));
  import('motion').then(({ scroll }) => {
    const link = (target, tl) => {
      const list = ks.filter((q) => q.tl === tl);
      if (!target || !list.length) return;
      scroll((p) => {
        const d = ((p * (target.offsetHeight + innerHeight)) / innerHeight) * 100; // in svh, the unit the CSS ranges use
        list.forEach((q) => { const a = q.r0 + q.i * q.rh + q.rw * q.s, b = q.r0 + q.i * q.rh + q.rw * q.e; q.el.style.setProperty('--t', Math.min(1, Math.max(0, (d - a) / (b - a))).toFixed(4)); });
      }, { target, offset: ['start end', 'end start'] });
    };
    link($('.bsteps'), '--build'); link($('.fin__run'), '--fin');
    scroll((p) => root.style.setProperty('--gp', p));
  });
}

// 5. Hero map: the body (plots, roads, labels) and its interaction code load after first paint and idle, or at the first touch on the map.
const mm = $('[data-mm]');
if (mm) {
  let started = false;
  const start = () => { if (started) return; started = true; import('./home-map.mjs').then((m) => m.default(mm)); };
  mm.addEventListener('pointerdown', start, { once: true, passive: true });
  mm.addEventListener('focusin', start, { once: true });
  const idle = () => ('requestIdleCallback' in window ? requestIdleCallback(start, { timeout: 2500 }) : setTimeout(start, 1500));
  if (document.readyState === 'complete') idle(); else addEventListener('load', () => setTimeout(idle, 300), { once: true });
}
