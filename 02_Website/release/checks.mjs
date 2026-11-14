// node release/checks.mjs <distDir> [staging|production]
// Static release checks. Writes release/last-checks.json (status, time, commit, dist, failures). Exit 1 on FAIL.
import fs from 'node:fs'; import path from 'node:path'; import { fileURLToPath } from 'node:url'; import { execSync, spawnSync } from 'node:child_process';
const here = path.dirname(fileURLToPath(import.meta.url));
const D = path.resolve(process.argv[2] || path.join(here, '../site-v2/dist-staging')); const env = process.argv[3] || 'staging';
const B = JSON.parse(fs.readFileSync(path.join(here, 'banned.json'), 'utf8'));
const fix = (p) => p.split(path.sep).join('/');
const fails = []; const say = (f, m) => fails.push(`${fix(path.relative(D, f))}: ${m}`);
const files = []; (function w(d) { for (const e of fs.readdirSync(d, { withFileTypes: true })) { const p = path.join(d, e.name); e.isDirectory() ? w(p) : p.endsWith('.html') && files.push(p); } })(D);
const exists = (u) => { u = u.split('#')[0].split('?')[0]; if (!u) return true; const p = path.join(D, decodeURIComponent(u)); return (fs.existsSync(p) && fs.statSync(p).isFile()) || fs.existsSync(path.join(p, 'index.html')); };
const text = (h) => h.replace(/<script[\s\S]*?<\/script>|<style[\s\S]*?<\/style>/g, ' ').replace(/<[^>]+>/g, ' ');
const held = new RegExp(B.heldNumber + '|9219549800');
for (const f of files) {
  const h = fs.readFileSync(f, 'utf8'); const rel = fix(path.relative(D, f));
  if (rel === '404.html') continue;
  const n = (h.match(/<h1[\s>]/g) || []).length; if (n !== 1) say(f, `h1 count ${n}`);
  const t = (h.match(/<title>([^<]*)<\/title>/) || [])[1]; if (!t || t.length < 15 || t.length > 70) say(f, `title length ${t ? t.length : 'missing'}`);
  const d = (h.match(/<meta name="description" content="([^"]*)"/) || [])[1]; if (!d || d.length < 70 || d.length > 170) say(f, `description length ${d ? d.length : 'missing'}`);
  for (const m of h.matchAll(/href="(\/[^"#]*)(#[^"]*)?"/g)) if (!exists(m[1])) say(f, 'broken link ' + m[1]);
  for (const m of h.matchAll(/href="(#[^"]+)"/g)) if (!h.includes(`id="${m[1].slice(1)}"`)) say(f, 'broken anchor ' + m[1]);
  for (const m of h.matchAll(/<img[^>]*>/g)) { if (!/width=/.test(m[0]) || !/height=/.test(m[0])) say(f, 'img without size'); if (/\.(png|jpe?g)/i.test(m[0])) say(f, 'non webp img'); }
  for (const s of B.everywhere) if (new RegExp(s, 'i').test(h)) say(f, 'banned ' + s);
  if (held.test(h) && !B.heldNumberAllowedIn.some((a) => rel === a || rel.startsWith(a))) say(f, 'held number outside rent pages');
  const tx = text(h); for (const s of B.oldDistances) if (new RegExp(s, 'i').test(tx)) say(f, 'old distance ' + s);
}
for (const must of ['robots.txt', '_headers', 'sitemap-index.xml']) if (!fs.existsSync(path.join(D, must))) fails.push(`missing ${must}`);
let vale = 'skipped (vale.exe not found)'; const v = 'C:/Users/anshc/tools/vale/vale.exe'; const ini = path.join(here, '../../06_Content/voice/.vale.ini');
if (fs.existsSync(v)) {
  if (fs.existsSync(ini)) { const r = spawnSync(v, ['--config=' + ini, '--output=line', path.join(here, '../site-v2/src/content/pages')], { encoding: 'utf8' }); vale = r.status ? 'FAIL' : 'ok'; if (r.status) fails.push('vale: ' + (r.stdout || r.stderr).split('\n').slice(0, 5).join(' | ')); }
  else vale = 'skipped (no .vale.ini at 06_Content/voice)';
}
const git = (c) => { try { return execSync(c, { cwd: here, encoding: 'utf8' }).trim(); } catch { return ''; } };
const out = { status: fails.length ? 'FAIL' : 'PASS', time: new Date().toISOString(), commit: git('git rev-parse HEAD'), branch: git('git rev-parse --abbrev-ref HEAD'), dirty: !!git('git status --porcelain -- ../site-v2/src ../site-v2/public ../site-v2/scripts ../site-v2/package.json'), dist: fix(D), env, pages: files.length, vale, failures: fails };
fs.writeFileSync(path.join(here, 'last-checks.json'), JSON.stringify(out, null, 2));
console.log(fails.join('\n')); console.log(`${out.status}: ${files.length} pages, ${fails.length} failures, vale ${vale}`);
process.exit(fails.length ? 1 : 0);
