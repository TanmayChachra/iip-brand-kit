// Hero map, loaded by home.mjs after first paint. Fetches the map body, appends it in small slices (no long task), then wires pan, zoom and the phase chips.
const $ = (s, r = document) => r.querySelector(s), $$ = (s, r = document) => [...r.querySelectorAll(s)];
const still = matchMedia('(prefers-reduced-motion: reduce)').matches;
let body; // one fetch shared by the hero map and the sizes map
export default function initMap(mm) {
// Hero master map: drag to pan, wheel or pinch to zoom (fast, with a short lerp), double click or double tap to zoom to the pointer, buttons plus, minus and reset.
  const vp = $('.mm__vp', mm), svg = $('.mm__svg', mm), cam = $('.cam', mm), tip = $('.mm__tip', mm);
  const [bx, by, bw, bh] = svg.dataset.vb.split(' ').map(Number);
  // the user space rectangle the viewport really shows (the svg letterboxes the viewBox, so a tall or wide viewport shows more than the viewBox); s0 = px per unit at camera scale 1
  let vx = bx, vy = by, vw = bw, vh = bh, s0 = 1;
  const view = () => { const w = vp.clientWidth || 1, h = vp.clientHeight || 1; s0 = Math.min(w / bw, h / bh); vw = w / s0; vh = h / s0; vx = bx + bw / 2 - vw / 2; vy = by + bh / 2 - vh / 2; };
  view();
  const boxes = JSON.parse(svg.dataset.boxes), bb = Object.values(boxes);
  const cx0 = Math.min(...bb.map((b) => b[0])) - 40, cx1 = Math.max(...bb.map((b) => b[0] + b[2])) + 40, cy0 = Math.min(...bb.map((b) => b[1])) - 40, cy1 = Math.max(...bb.map((b) => b[1] + b[3])) + 40;
  const KMIN = 0.9, KMAX = 10, WHEEL = 0.0045, PINCH = 1.6;
  let base = 0.9, k = 1, x = 0, y = 0, T = { k: 1, x: 0, y: 0 }, raf = 0, last = 0, tau = 70, moved = 0, hideT = 0, tap = { t: 0, x: 0, y: 0 }, lastDbl = 0;
  const pts = new Map();
  const put = () => { cam.setAttribute('transform', `translate(${x.toFixed(1)} ${y.toFixed(1)}) scale(${k.toFixed(4)})`); mm.classList.toggle('zoomed', k > base * 1.04); };
  const user = (cx, cy) => { const p = svg.createSVGPoint(); p.x = cx; p.y = cy; return p.matrixTransform(svg.getScreenCTM().inverse()); };
  const touched = () => mm.classList.add('touched');
  // keep the content covering the viewport (or centred when it is smaller)
  const axis = (c0, c1, v0, vl, kk, p) => { const lo = v0 + vl - kk * c1, hi = v0 - kk * c0; return lo > hi ? (lo + hi) / 2 : Math.min(hi, Math.max(lo, p)); };
  const clamp = () => { T.x = axis(cx0, cx1, vx, vw, T.k, T.x); T.y = axis(cy0, cy1, vy, vh, T.k, T.y); };
  const sync = () => { cancelAnimationFrame(raf); raf = 0; k = T.k; x = T.x; y = T.y; put(); lab(); };
  const tick = (t) => {
    const dt = Math.min(64, t - last || 16); last = t;
    const a = 1 - Math.exp(-dt / tau);
    k += (T.k - k) * a; x += (T.x - x) * a; y += (T.y - y) * a;
    if (Math.abs(T.k - k) < 0.001 && Math.abs(T.x - x) < 0.05 && Math.abs(T.y - y) < 0.05) { sync(); tau = 70; return; }
    put(); raf = requestAnimationFrame(tick);
  };
  const go = (slow) => { clamp(); if (still) { sync(); return; } tau = slow ? 170 : 70; if (!raf) { last = 0; raf = requestAnimationFrame(tick); } };
  const zoomAt = (u, f, slow) => { const nk = Math.min(KMAX, Math.max(KMIN, T.k * f)); T.x = u.x - ((u.x - T.x) / T.k) * nk; T.y = u.y - ((u.y - T.y) / T.k) * nk; T.k = nk; go(slow); };
  const centre = () => ({ x: vx + vw / 2, y: vy + vh / 2 });
  const fit = (b) => { const pad = b ? 0.95 : 0.9; if (!b) b = [bx, by, bw, bh]; const kk = pad * Math.min(vw / b[2], vh / b[3]); return { k: kk, x: vx + vw / 2 - kk * (b[0] + b[2] / 2), y: vy + vh / 2 - kk * (b[1] + b[3] / 2) }; };
  // animated fly to a target view, 400 ms, gentle ease in and out. T follows the current view, so a touch mid flight just takes over.
  const ease = (u) => (u < 0.5 ? 4 * u * u * u : 1 - Math.pow(-2 * u + 2, 3) / 2);
  const fly = (to) => {
    cancelAnimationFrame(raf); raf = 0; Object.assign(T, to); clamp(); const e = { ...T };
    if (still) { base = e.k; sync(); return; }
    const f = { k, x, y }; let t0 = 0;
    const step = (t) => {
      t0 = t0 || t; const u = Math.min(1, (t - t0) / 400), q = ease(u);
      k = f.k * Math.pow(e.k / f.k, q); x = f.x + (e.x - f.x) * q; y = f.y + (e.y - f.y) * q; T.k = k; T.x = x; T.y = y; put();
      if (u < 1) raf = requestAnimationFrame(step); else { raf = 0; Object.assign(T, e); base = e.k; sync(); }
    };
    raf = requestAnimationFrame(step);
  };
  // plot numbers: raised to at least 5 px on screen (at most 2.4x their drawn size), hidden when that is not enough; refreshed 120 ms after the zoom settles
  let labs = null, lt = 0, lk = 0;
  const lab = (force) => {
    clearTimeout(lt); if (!labs) return;
    lt = setTimeout(() => {
      if (!force && Math.abs(Math.log(T.k / (lk || 1))) < 0.03) return; lk = T.k;
      for (const l of labs) { const px = l.fs * l.sc * s0 * T.k, f = Math.max(1, 5 / px), hide = f > 2.4; if (hide !== l.h) { l.el.style.display = hide ? 'none' : ''; l.h = hide; } const fz = hide || f === 1 ? '' : (l.fs * f).toFixed(2); if (fz !== l.z) { l.el.style.fontSize = fz; l.z = fz; } }
    }, force ? 0 : 120);
  };
  Object.assign(T, fit(null)); base = T.k; sync();
  new ResizeObserver(() => { view(); Object.assign(T, mm.dataset.focus ? fit(boxes[mm.dataset.focus]) : fit(null)); clamp(); sync(); lab(true); }).observe(vp);
  const setChip = (ph) => { $$('.mm__chip', mm).forEach((o) => o.setAttribute('aria-pressed', o.dataset.ph === String(ph) ? 'true' : 'false')); if (+ph) mm.dataset.focus = ph; else delete mm.dataset.focus; };
  const hover = (e, force) => {
    const pl = e.target.closest && e.target.closest('.plot');
    if (!pl || (!force && e.pointerType !== 'mouse')) { if (!force) tip.hidden = true; return; }
    const r = vp.getBoundingClientRect();
    tip.textContent = `Plot ${pl.dataset.plot}, about ${pl.dataset.a} sq yd`;
    tip.style.left = `${e.clientX - r.left}px`; tip.style.top = `${e.clientY - r.top}px`; tip.hidden = false;
    if (force) { clearTimeout(hideT); hideT = setTimeout(() => (tip.hidden = true), 3000); }
  };
  const dbl = (cx, cy) => { lastDbl = performance.now(); touched(); tip.hidden = true; if (T.k > KMAX * 0.7) { fly(fit(null)); setChip(0); } else zoomAt(user(cx, cy), 2.6, true); };
  $$('.mm__chip', mm).forEach((c) => c.addEventListener('click', () => { const ph = c.dataset.ph; setChip(ph); touched(); fly(fit(+ph ? boxes[ph] : null)); }));
  $$('[data-z]', mm).forEach((b) => b.addEventListener('click', () => {
    touched(); const z = b.dataset.z;
    if (z === 'reset') { fly(fit(null)); setChip(0); } else zoomAt(centre(), z === 'in' ? 1.9 : 1 / 1.9, true);
  }));
  vp.addEventListener('pointerdown', (e) => { if (e.target.closest('.mm__zoom')) return; touched(); sync(); vp.setPointerCapture(e.pointerId); pts.set(e.pointerId, { x: e.clientX, y: e.clientY }); moved = 0; });
  vp.addEventListener('pointermove', (e) => {
    const p = pts.get(e.pointerId);
    if (!p) { hover(e); return; }
    if (pts.size === 1) {
      const s = 1 / (svg.getScreenCTM().a || 1);
      T.x += (e.clientX - p.x) * s; T.y += (e.clientY - p.y) * s; moved += Math.abs(e.clientX - p.x) + Math.abs(e.clientY - p.y); clamp(); sync(); tip.hidden = true;
    } else if (pts.size === 2) {
      const [i0, i1] = [...pts.keys()], o0 = pts.get(i0), o1 = pts.get(i1), n0 = i0 === e.pointerId ? { x: e.clientX, y: e.clientY } : o0, n1 = i1 === e.pointerId ? { x: e.clientX, y: e.clientY } : o1;
      const f = Math.pow(Math.hypot(n0.x - n1.x, n0.y - n1.y) / Math.max(1, Math.hypot(o0.x - o1.x, o0.y - o1.y)), PINCH);
      const c = user((n0.x + n1.x) / 2, (n0.y + n1.y) / 2), oc = user((o0.x + o1.x) / 2, (o0.y + o1.y) / 2);
      T.x += c.x - oc.x; T.y += c.y - oc.y; zoomAt(c, f); sync(); moved += 9;
    }
    pts.set(e.pointerId, { x: e.clientX, y: e.clientY });
  });
  const up = (e) => {
    if (pts.has(e.pointerId) && pts.size === 1 && moved < 6 && e.pointerType !== 'mouse') {
      const now = performance.now();
      if (now - tap.t < 320 && Math.hypot(e.clientX - tap.x, e.clientY - tap.y) < 32) { tap.t = 0; dbl(e.clientX, e.clientY); } else { tap = { t: now, x: e.clientX, y: e.clientY }; hover(e, true); }
    }
    pts.delete(e.pointerId);
  };
  vp.addEventListener('pointerup', up); vp.addEventListener('pointercancel', (e) => pts.delete(e.pointerId));
  vp.addEventListener('pointerleave', (e) => { if (e.pointerType === 'mouse') tip.hidden = true; });
  vp.addEventListener('dblclick', (e) => { if (e.target.closest('.mm__zoom')) return; if (performance.now() - lastDbl > 700) dbl(e.clientX, e.clientY); });
  // wheel zooms about 3x faster than before; at the fit zoom a scroll down still moves the page on
  vp.addEventListener('wheel', (e) => {
    const dy = e.deltaY * (e.deltaMode === 1 ? 16 : e.deltaMode === 2 ? 100 : 1);
    if (!e.ctrlKey && dy > 0 && T.k <= 1.001) return;
    e.preventDefault(); touched(); zoomAt(user(e.clientX, e.clientY), Math.exp(-dy * (e.ctrlKey ? 0.014 : WHEEL)));
  }, { passive: false });
  vp.addEventListener('keydown', (e) => {
    const s = 80 / (svg.getScreenCTM().a || 1), m = { ArrowLeft: [s, 0], ArrowRight: [-s, 0], ArrowUp: [0, s], ArrowDown: [0, -s] }[e.key];
    if (m) { e.preventDefault(); touched(); T.x += m[0]; T.y += m[1]; go(); } else if (e.key === '+' || e.key === '=') { touched(); zoomAt(centre(), 1.6); } else if (e.key === '-') { touched(); zoomAt(centre(), 1 / 1.6); } else if (e.key === '0') { touched(); fly(fit(null)); setChip(0); }
  });
  if (mm.hasAttribute('data-mm')) window.__mm = { get k() { return k; }, get T() { return T; } }; // read only, for QA

  // inject the body in slices of about 8 ms, one slice per frame
  (body || (body = fetch(vp.dataset.src).then((r) => r.json()))).then((chunks) => {
    const host = {}; $$('.ph', mm).forEach((g) => (host[g.dataset.ph] = g.querySelector('svg')));
    let i = 0;
    const slice = () => {
      const t0 = performance.now();
      while (i < chunks.length && performance.now() - t0 < 8) { const [n, h] = chunks[i++]; host[n].insertAdjacentHTML('beforeend', h); }
      if (i < chunks.length) requestAnimationFrame(slice); else {
        mm.classList.add('in');
        labs = $$('.ph', mm).flatMap((g) => { const sc = g.transform.baseVal.consolidate().matrix.a; return $$('.pn', g).map((el) => ({ el, sc, fs: +el.getAttribute('font-size') || 3 })); });
        lab(true);
      }
    };
    requestAnimationFrame(slice);
  }).catch(() => {});
}
