// node scripts/check_inner.mjs [dist]: one h1 per page, internal links and ids resolve, banned strings absent, images have size and are not png/jpg
import fs from 'node:fs'; import path from 'node:path';
const D = process.argv[2] || 'dist-inner'; let bad = 0;
const files = []; (function w(d){ for (const e of fs.readdirSync(d,{withFileTypes:true})) { const p=path.join(d,e.name); e.isDirectory() ? (e.name!=='assets'||d!==D) && w(p) : p.endsWith('.html') && files.push(p); } })(D);
const exists = (u) => { u=u.split('#')[0].split('?')[0]; if(!u) return true; const p=path.join(D,u); return fs.existsSync(p)&&fs.statSync(p).isFile()||fs.existsSync(path.join(p,'index.html'))||fs.existsSync(p+'.html'); };
const say = (f, m) => { bad++; console.log('FAIL', f.replace(D,''), m); };
for (const f of files) {
  const h = fs.readFileSync(f,'utf8');
  const n = (h.match(/<h1[\s>]/g)||[]).length; if (n!==1) say(f,`h1 count ${n}`);
  for (const m of h.matchAll(/href="(\/[^"#]*)(#[^"]*)?"/g)) if (!exists(m[1])) say(f,'broken link '+m[1]);
  for (const m of h.matchAll(/href="(#[^"]+)"/g)) if (!h.includes(`id="${m[1].slice(1)}"`)) say(f,'broken anchor '+m[1]);
  for (const s of ['92195 49800','9219549800','98370 57800','9837057800','resale']) { if (/^(92195 49800|9219549800)$/.test(s) && /(industrial-shed-for-rent|faq)/.test(f) || path.join(D,'index.html')===f) continue; if (new RegExp(s,'i').test(h)) say(f,'banned '+s); }
  for (const m of h.matchAll(/<img[^>]*>/g)) { if(!/width=/.test(m[0])||!/height=/.test(m[0])) say(f,'img no size '+m[0].slice(0,60)); if(/\.(png|jpe?g)/i.test(m[0])) say(f,'non webp img'); }
}
console.log(files.length,'pages checked,',bad,'failures');
