// node scripts/build.mjs staging|production
// Loads ONLY .env.<mode> into process.env (highest Vite priority), so .env / .env.local can never leak production values into staging.
// Output: dist-<mode>. Staging gets noindex headers; robots.txt and the ribbon switch on PUBLIC_ENV.
import fs from 'node:fs'; import { spawnSync } from 'node:child_process';
const mode = process.argv[2];
if (!['staging', 'production'].includes(mode)) { console.error('usage: build.mjs staging|production'); process.exit(2); }
for (const l of fs.readFileSync(`.env.${mode}`, 'utf8').split(/\r?\n/)) { const m = l.match(/^([A-Z_]+)=(.*)$/); if (m) process.env[m[1]] = m[2]; }
const out = `dist-${mode}`; process.env.IIP_OUT = out;
fs.rmSync(out, { recursive: true, force: true });
const r = spawnSync('npx', ['astro', 'build', '--mode', mode], { stdio: 'inherit', shell: true });
if (r.status) process.exit(r.status);
if (mode === 'staging') { // same headers as production plus noindex on everything
  const h = fs.readFileSync('public/_headers', 'utf8').replace(/^\/\*\r?\n/m, (s) => s + '  X-Robots-Tag: noindex, nofollow, noarchive\n');
  fs.writeFileSync(`${out}/_headers`, h);
}
console.log(`built ${mode} -> ${out}`);
