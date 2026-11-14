// Link and SEO checker over dist. Run: node ../qa/v3/check.mjs <distDir>
import fs from 'node:fs'; import path from 'node:path';
const dist = path.resolve(process.argv[2] || 'dist');
const walk = d => fs.readdirSync(d,{withFileTypes:true}).flatMap(e => e.isDirectory()? walk(path.join(d,e.name)) : [path.join(d,e.name)]);
const rel = f => '/'+path.relative(dist,f).split(path.sep).join('/'); const files = walk(dist).filter(f=>!rel(f).startsWith('/assets/')); // /assets is public/assets tooling, excluded from packaging
const set = new Set(files.map(rel)); const html = files.filter(f=>f.endsWith('.html'));
const out = {broken:[],h1:[],title:[],desc:[],canon:[],gtm:[],jsonld:[],imgs:[],tel:[],badwords:[]};
const titles = new Map(), descs = new Map();
const exists = u => { u=decodeURIComponent(u); if(set.has(u)) return true; if(u.endsWith('/')) return set.has(u+'index.html'); return set.has(u+'/index.html')||set.has(u); };
const bad = [/92195 ?49800/,/98370 ?57800/,/9219549800/,/9837057800/,/\bresale\b/i,/\b3\.9 km\b/,/\b9\.3 km\b/,/\b13\.0 km\b/];
for (const f of html) {
  const s = fs.readFileSync(f,'utf8'); const r = rel(f);
  const h1 = (s.match(/<h1[\s>]/g)||[]).length; if (h1!==1) out.h1.push(r+' '+h1);
  const t = (s.match(/<title>([^<]*)<\/title>/)||[])[1]; if(!t||t.length>60) out.title.push(r+' len '+(t||'').length+': '+t);
  if (titles.has(t)) out.title.push(r+' duplicate of '+titles.get(t)); titles.set(t,r);
  const d = (s.match(/<meta name="description" content="([^"]*)"/)||[])[1]; if(!d||d.length>155) out.desc.push(r+' len '+(d||'').length);
  if (descs.has(d)) out.desc.push(r+' dup of '+descs.get(d)); descs.set(d,r);
  const c = (s.match(/<link rel="canonical" href="([^"]*)"/)||[])[1]; if(!c||!c.startsWith('https://isapurindustrialpark.com/')) out.canon.push(r+' '+c);
  if (r!=='/404.html'){ const g=(s.match(/GTM-KMBRGVSD/g)||[]).length; out.gtm.push(r+' '+g); }
  for (const m of s.matchAll(/<script type="application\/ld\+json"[^>]*>([\s\S]*?)<\/script>/g)) { try{JSON.parse(m[1]);}catch(e){out.jsonld.push(r+' '+e.message);} }
  for (const m of s.matchAll(/(?:href|src)="([^"#?]+)[^"]*"/g)) { const u=m[1]; if(/^(https?:|mailto:|tel:|data:|\/\/)/.test(u)) continue; let p=u; if(!p.startsWith('/')) p=path.posix.join(path.posix.dirname(r),p); if(!exists(p)) out.broken.push(r+' -> '+u); }
  for (const m of s.matchAll(/(?:href|src)="([^"]+\.(?:jpg|jpeg|png|gif))"/gi)) out.imgs.push(r+' '+m[1]);
  for (const m of s.matchAll(/(?:tel:|wa\.me\/|phone=)\+?(\d+)/g)) if(!/^(919837764222|9837764222)$/.test(m[1])) out.tel.push(r+' '+m[1]);
  for (const b of bad) if (b.test(s)) out.badwords.push(r+' '+b);
}
for (const f of files.filter(f=>/\.(txt|xml)$/.test(f))) { const s=fs.readFileSync(f,'utf8'); for (const b of bad) if (b.test(s)) out.badwords.push(rel(f)+' '+b); }
const gtmBad = out.gtm.filter(x=>!/ 1$/.test(x)); out.gtm = gtmBad;
const sm = fs.readFileSync(path.join(dist,'sitemap-0.xml'),'utf8'); const locs=[...sm.matchAll(/<loc>([^<]+)/g)].map(m=>m[1]);
out.sitemapBad = locs.filter(l=>!l.startsWith('https://isapurindustrialpark.com/'));
out.sitemapMissing = html.map(rel).filter(r=>r!=='/404.html').map(r=>'https://isapurindustrialpark.com'+r.replace('index.html','')).filter(u=>!locs.includes(u));
out.imageFiles = files.filter(f=>/\.(jpg|jpeg|png)$/i.test(f)).map(rel);
console.log(JSON.stringify({pages:html.length,...out},null,1));
