// The hero map body, fetched after first paint by src/scripts/home-map.mjs: [[phase, svgChunk], ...] in drawing order.
import { splitMaster } from '../../lib/mastermap.mjs';
export const GET = () => new Response(JSON.stringify(splitMaster().chunks), { headers: { 'content-type': 'application/json' } });
