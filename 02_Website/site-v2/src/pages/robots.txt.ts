import type { APIRoute } from 'astro';
// One site URL for everything: PUBLIC_SITE_URL (astro.config.mjs). Search and AI retrieval bots are allowed.
const staging = import.meta.env.PUBLIC_ENV === 'staging';
export const GET: APIRoute = ({ site }) => new Response(staging ? 'User-agent: *\nDisallow: /\n' :
`User-agent: *
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: PerplexityBot
Allow: /

Sitemap: ${new URL('/sitemap-index.xml', site).href}
`, { headers: { 'Content-Type': 'text/plain; charset=utf-8' } });
