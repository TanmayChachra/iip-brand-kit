import type { APIRoute } from 'astro';
import { PHONES, HOURS_TEXT } from '../lib/phones.mjs';
// Short machine-readable summary. URLs follow PUBLIC_SITE_URL; phones follow phones.mjs.
export const GET: APIRoute = ({ site }) => {
  const u = (p: string) => new URL(p, site).href;
  return new Response(
`# Isapur Industrial Park

> Industrial plots on Hapur-Modinagar Road, Yusufpur Isapur, Ghaziabad, Uttar Pradesh. Plots from 300 sq yards, contact for price. 50 ft wide RCC roads, street lighting, planted greenery. 4.7 km by road (about 8 minutes) to the Delhi-Meerut Expressway on-ramp at Bhojpur.

Contact: ${PHONES[0].display}, ${PHONES[1].display}. ${HOURS_TEXT} Address: Hapur-Modinagar Road, Yusufpur Isapur, Ghaziabad, UP 201022.

## Pages
- [Industrial plots](${u('/industrial-plots/')}): plot sizes and how to buy
- [Amenities](${u('/amenities/')}): roads, lighting, greenery
- [Location](${u('/location/')}): distances and directions
- [Industrial areas in Ghaziabad](${u('/industrial-areas-in-ghaziabad/')}): a short guide to the areas
- [Around the park](${u('/neighbours/')}): what is nearby, with distances
- [FAQ](${u('/faq/')}): short answers
- [Contact](${u('/contact/')}): call, WhatsApp, book a site visit
`, { headers: { 'Content-Type': 'text/plain; charset=utf-8' } });
};
