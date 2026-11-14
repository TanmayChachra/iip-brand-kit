// Inner page copy: every "## " heading of a Markdown body becomes one section (h2 plus prose). Ordered lists become the home's numbered sunburst steps.
import { createMarkdownProcessor } from '@astrojs/markdown-remark';
import remarkFill from './remark-fill.mjs';
import { burst } from './burst.mjs';

let proc;
const bp = burst();
const COL = ['#FFD600', '#0F4D3A', '#E53935', '#0F4D3A', '#FFD600'];
const steps = (html) => html.replace(/<ol>([\s\S]*?)<\/ol>/g, (_, inner) => {
  let n = 0;
  const items = [...inner.matchAll(/<li>([\s\S]*?)<\/li>/g)].map((m) => {
    const c = COL[n % 5], lt = c !== '#FFD600' ? ' class="lt"' : '', t = m[1].match(/^<strong>(.*?)<\/strong>\s*([\s\S]*)$/);
    n++;
    return `<li><div class="num"><svg viewBox="0 0 800 800" aria-hidden="true"><polygon points="${bp}" fill="${c}"/></svg><b${lt}>${n}</b></div><div>${t ? `<h3>${t[1].replace(/\.$/, '')}</h3><p>${t[2]}</p>` : `<p>${m[1]}</p>`}</div></li>`;
  });
  return `<ol class="buy">${items.join('')}</ol>`;
});

export async function parts(body) {
  proc ??= await createMarkdownProcessor({ remarkPlugins: [remarkFill] });
  const out = [];
  for (const p of (body || '').split(/^## /m).slice(1)) {
    const i = p.indexOf('\n'), h = p.slice(0, i).trim(), md = p.slice(i + 1).trim();
    if (!md) continue;
    out.push({ h, html: steps((await proc.render(md)).code).replace(/<table>/g, '<table class="dist">').replace(/<td>([^<]{1,16})<\/td>/g, '<td class="nw">$1</td>') });
  }
  return out;
}
