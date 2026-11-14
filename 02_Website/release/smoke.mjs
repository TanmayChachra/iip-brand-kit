// node release/smoke.mjs <baseUrl> <staging|production>
// Live smoke test. Exit 1 on any failure.
const base = (process.argv[2] || '').replace(/\/$/, ''); const env = process.argv[3];
if (!base || !['staging', 'production'].includes(env)) { console.error('usage: smoke.mjs <baseUrl> <staging|production>'); process.exit(2); }
const PROD = 'https://isapurindustrialpark.com';
const pages = ['/', '/industrial-plots/', '/industrial-shed-for-rent/', '/location/', '/plot-maps/', '/contact/', '/faq/', '/privacy/'];
const bad = []; const ok = (c, m) => { if (!c) bad.push(m); };
const get = async (p) => { for (let i = 0; i < 8; i++) { try { const r = await fetch(base + p, { redirect: 'manual', headers: { 'cache-control': 'no-cache' } }); const t = await r.text(); if (r.status < 500 || i == 7) return { r, t }; } catch (e) { if (i == 7) throw e; } await new Promise((s) => setTimeout(s, 6000)); } };  // retries cover new-project edge propagation
for (const p of pages) {
  const { r, t } = await get(p); const h = r.headers; const xr = h.get('x-robots-tag') || '';
  ok(r.status === 200, `${p} status ${r.status}`);
  const gtm = /googletagmanager\.com\/gtm\.js|GTM-[A-Z0-9]{5,}/.test(t); const canon = (t.match(/rel="canonical" href="([^"]*)"/) || [])[1] || '';
  if (env === 'staging') {
    ok(/noindex/i.test(xr), `${p} staging lacks X-Robots-Tag noindex`); ok(!gtm, `${p} staging has GTM`); ok(t.includes('data-staging-ribbon'), `${p} staging ribbon missing`);
  } else {
    ok(!/noindex/i.test(xr), `${p} production has noindex header`); ok(!/name="robots"[^>]*noindex/i.test(t), `${p} production has noindex meta`);
    ok(gtm, `${p} production lacks GTM`); ok(canon.startsWith(PROD + '/'), `${p} canonical ${canon}`); ok(!t.includes('data-staging-ribbon'), `${p} production shows ribbon`);
    ok(/content-security-policy/i.test([...h.keys()].join(',')), `${p} no CSP`); ok(h.get('strict-transport-security'), `${p} no HSTS`);
  }
}
const rb = await get('/robots.txt');
if (env === 'staging') ok(/^Disallow: \/\s*$/m.test(rb.t) && !/^Allow: \//m.test(rb.t), 'staging robots.txt must Disallow: /');
else ok(/^Allow: \//m.test(rb.t) && !/^Disallow: \/\s*$/m.test(rb.t), 'production robots.txt must Allow: /');
const sm = await get('/sitemap-index.xml'); ok(sm.r.status === 200, 'sitemap-index.xml status ' + sm.r.status);
console.log(bad.length ? 'SMOKE FAIL ' + env + ' ' + base + '\n' + bad.join('\n') : `SMOKE PASS ${env} ${base} (${pages.length} pages)`);
process.exit(bad.length ? 1 : 0);
