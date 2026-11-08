# GTM, GA4 and measurement plan

Goal: know exactly which pages, keywords, listings and CTAs produce calls, WhatsApp chats and enquiries, so effort goes where it pays and stops where it does not.

## Stack (all free to start)
| Tool | Job | Setup note |
|---|---|---|
| Google Tag Manager (one web container) | Only third-party script on the site, loads everything else | Container ID is public, not a secret. Publish with version notes |
| GA4 | Events, conversions, acquisition | Mark `click_call`, `click_whatsapp`, `generate_lead`, `click_directions` as key events. Retention 14 months. Link to Search Console |
| Google Search Console | Queries, pages, indexing, Core Web Vitals | Domain property (DNS verify). Submit sitemap. Export monthly (API or OpenSEO link) |
| Bing Webmaster Tools | Bing and Copilot visibility, IndexNow | Import from Search Console |
| Microsoft Clarity | Heatmaps and session recordings, free | Via GTM, mask all form inputs |
| Looker Studio | One owner dashboard: GA4 + GSC + GBP | Build after 2 weeks of data |
| GBP Insights export | Calls, direction requests, search terms | Needs owner login, monthly export into `05_Local-Presence/gmb/exports/` |
| Call tracking (later) | Which source made the call | `tel:` click is a proxy. Add a tracked number only when volume justifies it |

## Tags (launch set)
1. GA4 configuration (all pages).
2. GA4 events from dataLayer: one tag per event in `event-spec.md` using a single Custom Event trigger pattern.
3. Scroll depth (25, 50, 75, 90) via the built-in trigger.
4. Clarity (all pages).
5. Later: Google Ads and Meta pixel, only when ads start, behind consent.

## Testing checklist before launch
- GTM Preview and GA4 DebugView show every event with its parameters on a real phone.
- Click a call, WhatsApp, directions and brochure link on mobile and desktop: each fires once.
- Submit a test lead (test value) and confirm `generate_lead` fires only after success.
- Lighthouse mobile after GTM is added: still within the budget in `03_SEO/research/stack/findings.md`. If INP suffers, delay GTM until first interaction.

## Monthly review: what to double down on and what to drop
Run on the first Monday of each month, write `04_Analytics/reviews/YYYY-MM.md` (3 lines of verdict first).
- **Double down** when a page, query or listing has: conversions per 100 sessions above the site median, or impressions growing 3 months in a row with CTR under 3 percent (fix title and meta), or position 4 to 15 for a money keyword (add content and links).
- **Fix** pages with traffic and no conversions (CTA position, proof, speed). Check Clarity recordings first.
- **Drop or merge** a page with under 20 impressions and no conversion after 120 days, unless it supports a cluster. Listings with no referral sessions or calls after 6 months stay only if they give a usable citation.
- **Channels:** compare cost (time) per lead by source (organic search, GBP, directories, WhatsApp share, QR). Keep the top three.
- Log decisions in the A/B test log (`ab-test-log.md`): hypothesis, change, dates, metric, result.

## Owner data needed
GA4 and GTM container created under the owner's Google account (add the agent's email as editor only if the owner wants), Search Console domain verification, GBP access for Insights exports.
