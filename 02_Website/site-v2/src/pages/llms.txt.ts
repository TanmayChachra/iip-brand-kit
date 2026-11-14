import type { APIRoute } from 'astro';
import { PHONES, HOURS_TEXT } from '../lib/phones.mjs';
// Short machine-readable summary. URLs follow PUBLIC_SITE_URL; phones follow phones.mjs.
export const GET: APIRoute = ({ site }) => {
  const u = (p: string) => new URL(p, site).href;
  return new Response(
`# Isapur Industrial Park

> Industrial plots on Hapur-Modinagar Road, Yusufpur Isapur, Ghaziabad, Uttar Pradesh. Plots from 300 sq yards. 50 ft wide RCC roads, street lighting, planted greenery. 4.2 km by road (about 5 minutes) to the Delhi-Meerut Expressway on-ramp at Bhojpur.

Contact: ${PHONES[0].display} (call or WhatsApp). ${HOURS_TEXT} Address: Hapur-Modinagar Road, Yusufpur Isapur, Ghaziabad, UP 201022.

## Pages
- [Industrial plots](${u('/industrial-plots/')}): plot sizes and how to buy
- [Amenities](${u('/amenities/')}): roads, lighting, greenery
- [Location](${u('/location/')}): distances and directions
- [Industrial areas in Ghaziabad](${u('/industrial-areas-in-ghaziabad/')}): a short guide to the areas
- [Around the park](${u('/neighbours/')}): what is nearby, with distances
- [FAQ](${u('/faq/')}): short answers
- [Plot maps](${u('/plot-maps/')}): the three phases, plot by plot
- [Approvals](${u('/approvals/')}): layouts sanctioned by Zila Panchayat Ghaziabad
- [How buying works](${u('/how-buying-works/')}): the steps from call to registry
- [Layout approvals](${u('/layout-approvals/')}): what the approval means
- [Roads and freight](${u('/roads-and-freight/')}): trucks, expressway, rail depot
- [Shops](${u('/shops/')}): commercial shops inside the park
- [Contact](${u('/contact/')}): call, WhatsApp, book a site visit
`, { headers: { 'Content-Type': 'text/plain; charset=utf-8' } });
};
