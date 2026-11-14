// Splits a Markdown body at its "## " headings and groups the chunks into at most `max` page sections
// (one h2 each; the headings folded into a group become h3). Each group is rendered to HTML with the same
// remark plugin the content collections use, so phone tokens are filled.
import { createMarkdownProcessor } from '@astrojs/markdown-remark';
import remarkFill from './remark-fill.mjs';
import { fill } from './phones.mjs';

let proc;
const weight = (md) => md.split(/\s+/).filter(Boolean).length + (md.match(/^\|.*\|$/gm) || []).length * 12;

export async function sections(body, max = 5, extra = 0) {
  proc ??= await createMarkdownProcessor({ remarkPlugins: [remarkFill] });
  const parts = (body || '').split(/^## /m);
  parts.shift(); // text before the first heading is not used
  const cta = /^(\[WhatsApp|More:|Next:|Related:|\[Get directions\]|\[See |\[Send an enquiry|\[Book a site visit)/;
  const chunks = parts.map((p) => { const i = p.indexOf('\n'); return { h: p.slice(0, i).trim(), md: p.slice(i + 1).split('\n').filter((l) => !cta.test(l.trim())).join('\n').trim() }; }).filter((c) => c.md);
  const total = chunks.reduce((n, c) => n + weight(c.md), 0) + extra;
  const target = Math.max(1, Math.min(max, chunks.length, Math.ceil(total / 125)));
  const per = total / target;
  const groups = [];
  for (const c of chunks) {
    const w = weight(c.md);
    const cur = groups[groups.length - 1];
    if (!cur || (cur.w >= per * 0.8 && groups.length < target)) groups.push({ h: c.h, items: [{ h: null, md: c.md }], w });
    else { cur.items.push({ h: c.h, md: c.md }); cur.w += w; }
  }
  for (const g of groups) {
    g.html = (await Promise.all(g.items.map(async (it) => (it.h ? `<p class="sub"><strong>${fill(it.h)}</strong></p>` : '') + (await proc.render(it.md)).code))).join('');
    g.html = g.html.replace(/<input[^>]*>\s*/g, '').replace(/<a href="https:\/\/wa\.me[^>]*>[^<]*<\/a>(\s*·\s*)?/g, '').replace(/\s*·\s*(?=<\/p>)/g, '').replace(/<table>/g, '<table class="dist">').replace(/<td>([^<]{1,14})<\/td>/g, '<td class="nw">$1</td>');
    g.map = /map|find us|distance/i.test(g.h + ' ' + g.items.map((i) => i.h || '').join(' '));
  }
  return groups;
}
