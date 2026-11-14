// Splits the master map svg (src/assets/master.svg.html) into a tiny inline shell and a fetched, chunked body.
// The shell keeps each phase's sheet rectangle and an empty nested <svg>; chunks are appended after first paint (home-map.mjs).
import raw from '../assets/master.svg.html?raw';

const phRe = /(<g class="ph" data-ph="(\d)"[^>]*>)(<rect[^>]*\/>)(<svg[^>]*>)([\s\S]*?)<\/svg><\/g>/g;
const elRe = /\s*<(path|text|g|polygon|circle|line|rect|polyline|ellipse)\b[^>]*?(?:\/>|>[\s\S]*?<\/\1>)/y;

// top-level pieces inside a group's inner html (elements only, no nested g expected below the first level)
function pieces(inner) {
  const out = []; let i = 0;
  while (i < inner.length) {
    elRe.lastIndex = i;
    const m = elRe.exec(inner);
    if (!m) { out.push(inner.slice(i)); break; }
    out.push(m[0]); i = elRe.lastIndex;
  }
  return out;
}

export function splitMaster(limit = 4000) {
  const chunks = []; let shell = raw;
  for (const m of raw.matchAll(phRe)) {
    const [whole, gOpen, n, rect, svgOpen, body] = m;
    shell = shell.replace(whole, `${gOpen}${rect}${svgOpen}</svg></g>`);
    // body = sequence of top-level groups
    let i = 0;
    while (i < body.length) {
      const o = body.indexOf('<g', i);
      if (o < 0) { if (body.slice(i).trim()) chunks.push([+n, body.slice(i)]); break; }
      if (body.slice(i, o).trim()) chunks.push([+n, body.slice(i, o)]);
      const tagEnd = body.indexOf('>', o) + 1, open = body.slice(o, tagEnd);
      let depth = 1, p = tagEnd; const re = /<g[\s>]|<\/g>/g; re.lastIndex = tagEnd;
      let mm; while ((mm = re.exec(body)) && depth) { depth += mm[0] === '</g>' ? -1 : 1; p = re.lastIndex; }
      const inner = body.slice(tagEnd, p - 4);
      let cur = '';
      for (const piece of pieces(inner)) { cur += piece; if (cur.length > limit) { chunks.push([+n, `${open}${cur}</g>`]); cur = ''; } }
      if (cur) chunks.push([+n, `${open}${cur}</g>`]);
      i = p;
    }
  }
  // initial camera = the "fit" the map script uses (0.9 of the full viewBox, centred), so there is no jump when the script loads
  const [vx, vy, vw, vh] = /data-vb="([^"]+)"/.exec(raw)[1].split(' ').map(Number);
  shell = shell.replace('<g class="cam">', `<g class="cam" transform="translate(${(0.1 * (vx + vw / 2)).toFixed(1)} ${(0.1 * (vy + vh / 2)).toFixed(1)}) scale(0.9000)">`);
  return { shell, chunks };
}
