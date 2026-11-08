// Replaces {{phone1}} style tokens in Markdown text and link targets at build time (see phones.mjs).
import { fill } from './phones.mjs';
const walk = (n) => { if (typeof n.value === 'string') n.value = fill(n.value); if (typeof n.url === 'string') n.url = fill(n.url); (n.children || []).forEach(walk); };
export default function remarkFill() { return (tree) => walk(tree); }
