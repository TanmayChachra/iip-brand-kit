# Website stack decision (researched 2026-11-08)

**Verdict:** Astro is the right choice. Build static pages, host on Cloudflare Pages (free), write content as Markdown, add the Keystatic CMS once there are about 30 pages.
**Evidence:** Astro docs show near-zero JavaScript by default, built-in hashed WEBP images with width, height and lazy loading, an official sitemap package and content collections. Reported only (blog posts, not verified): Astro sites pass Core Web Vitals 50 to 66 percent of the time, WordPress 38 to 48 percent, Next.js 25 to 30 percent.
**Caveat:** no neutral current HTTP Archive table ranks all frameworks, so run our own Lighthouse test on a prototype before launch.

Labels: V = verified at the source on 2026-11-08, R = reported by a third party, G = guess.

## Comparison for IIP (30 to 80 pages, slow 4G phones, local lead generation)

| Option | Fit | Notes |
|---|---|---|
| Astro | Best | Near-zero JS (G). Image pipeline built in (V, https://docs.astro.build/en/guides/images/). Sitemap package (V). Content collections suit 20+ location pages. |
| Next.js | Over-built | Ships a React runtime on every page (G). Best on Vercel, whose free tier bars commercial use (R). |
| Eleventy, Hugo | Good second choice | Fast, weaker built-in images and components. |
| WordPress | Only if owner must edit alone from day one | Speed depends on plugin discipline. |
| Plain HTML | Too manual | Unmanageable at 80 pages with repeated schema. |

Sources (R): https://searchenginejournal.com/core-web-vitals-wordpress-and-astro/575818/ , https://astro.build/blog/2023-web-framework-performance-report , https://www.corewebvitals.io/state-of-cwv/explorer/metrics.stack.framework , https://almanac.httparchive.org/en/2025/performance

Core Web Vitals targets (V, https://web.dev/articles/vitals): LCP 2.5 s or less, INP 200 ms or less, CLS 0.1 or less, at the 75th percentile.

## Exact stack (npm registry, V, 2026-11-08)
- astro 7.4.7 (needs Node 22.23.4 or newer), @astrojs/mdx 8.1.3, @astrojs/sitemap 3.7.4, sharp 0.35.5, tailwindcss 4.3.5 (optional).
- Own `SEO.astro` and `Schema.astro` components. Optional: astro-seo 1.2.0, astro-seo-schema 7.0.1.
- Later: @keystatic/astro 6.0.0 with @keystatic/core 0.6.9. @astrojs/cloudflare 14.4.6 only if server code is needed. @astrojs/partytown 2.1.9 optional.
- Pin exact versions, upgrade monthly.

## CMS
- Not now. Pages are Markdown in git: no extra scripts, no login surface.
- Later: Keystatic (git based, built for Astro; R, https://www.luckymedia.dev/compare/decap-cms-vs-keystatic). Decap is free but slower to build (R). Tina's Astro support is experimental (R). Sanity is hosted with per-seat pricing (R).

## Hosting
- **Cloudflare Pages free (recommended):** 500 builds per month, 20,000 files, 25 MiB per file, 20 minute build timeout (V, https://developers.cloudflare.com/pages/platform/limits/ , updated 2026-09-05). Commercial use allowed, bandwidth not metered (R).
- **GitHub Pages:** 1 GB site, 100 GB per month soft bandwidth, 10 builds per hour (V, https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits). Its terms bar using it as free web hosting to run an online business (V, https://docs.github.com/en/site-policy/github-terms/github-terms-for-additional-products-and-features). Fine for our boards, not for the lead site.
- Netlify is the backup (free tier numbers disagree between sources, R). Vercel Hobby is non-commercial (R). Re-read each pricing page on deploy day.

## Project layout (`02_Website/site/`, created when build starts)
`astro.config.mjs`, `package.json`; `public/` (robots.txt, llms.txt, _headers, _redirects); `src/content/` (plots, locations, faq, brands, posts); `src/components/` (SEO, Schema, Breadcrumbs, CTA, Gtm); `src/layouts/Base.astro`; `src/pages/`; `src/styles/`.

## Technical SEO checklist
- **Crawl:** one absolute https canonical per page, `site` set in config, robots.txt with sitemap line, sitemap-index.xml submitted to Google Search Console and Bing, clean keyword URLs, 301 map from day one, custom 404, breadcrumbs plus BreadcrumbList. hreflang not needed (English, one country).
- **Open Graph:** 1200 x 630 image. Use JPG or PNG for OG only, some social crawlers reject WEBP (G). All on-page images stay WEBP.
- **Schema, only what is visible and proven:** Organization plus LocalBusiness (name exactly "Isapur Industrial Park", address, geo, both phones, hours, areaServed, sameAs; developer name never shown), Place with geo and hasMap, WebSite, WebPage, BreadcrumbList, FAQPage, Article, ImageObject. Offer only if the price or "contact for price" is truthful. Section 80 and Zilla Panchayat markup only after proof is on file.
- **FAQPage:** Google shows FAQ rich results only for well-known government and health sites (V, https://developers.google.com/search/docs/appearance/structured-data/faqpage). Still add it for AI engines (G). LocalBusiness reference: https://developers.google.com/search/docs/appearance/structured-data/local-business
- **Speed budgets (G, stricter than Google's pass line):** Lighthouse mobile throttled: LCP 1.8 s or less, CLS 0, TBT under 150 ms, score 95 or more. HTML under 30 KB gzip, CSS under 30 KB, JS under 60 KB gzip, hero image under 100 KB, first load under 500 KB. Hero image `fetchpriority="high"`, never lazy. One self-hosted, Latin-subset variable font with `font-display: swap`.
- **GTM policy:** GTM is the only third-party script, every other tag goes through it. Launch tags: GA4, call click, WhatsApp click, form submit, later Clarity. Measure INP after launch; if it suffers, delay GTM until first interaction or try Partytown (can break some tags). No chat widgets, sliders or pop-ups.
- **CTAs:** `tel:` and `https://wa.me/91...` links first (no JS needed). The form goes to a form service or one Cloudflare Pages Function (G).

## AEO and GEO technical readiness
- Google says AI Overviews and AI Mode need no extra technical requirement, no special files or schema, only an indexed page that can show a snippet (V, https://developers.google.com/search/docs/appearance/ai-features). Allow crawling in robots.txt and the CDN, use internal links, text content, structured data that matches visible text, an up to date Business Profile.
- **llms.txt:** proposal at https://llmstxt.org/ (V). Google says none is needed. Low value, ten minutes of work (G). Add a short one.
- **OpenAI bots:** OAI-SearchBot (search) and GPTBot (training) are independent robots.txt settings (V, https://platform.openai.com/docs/bots). Plan: allow search and retrieval bots (OAI-SearchBot, ChatGPT-User, PerplexityBot). Check each vendor page before writing robots.txt (tokens for ClaudeBot, PerplexityBot, Google-Extended are R).
- **Format AI tools quote (G):** question heading, 40 to 60 word direct answer, then detail. Facts in tables. Same name, address and phone everywhere. Dates and a named organisation.
- **Measure:** OpenSEO AI visibility tracking plus 10 fixed weekly questions in ChatGPT, Gemini, Perplexity and Copilot, logged.

## Risks
1. Astro releases fast: pin versions.
2. Owner cannot edit alone until a CMS is added.
3. A static site needs a form backend.
4. GitHub Pages terms bar this site: use Cloudflare.
5. Wrong schema risks a manual action.
6. Third-party scripts are the usual cause of failed INP (G).
7. Benchmark data is secondary: run our own Lighthouse test on a prototype.
8. 20+ near-duplicate location pages can read as doorway pages. Each needs unique facts (distances, roads, brands, FAQs).

## OpenSEO (V: README and GitHub API, 2026-11-08)
- Repo https://github.com/every-app/open-seo , MIT licence, about 26.8k stars, last push 2026-11-07. Open-source Semrush and Ahrefs alternative: keyword research, rank tracking, competitors, backlinks, site audits, AI visibility.
- MCP server and agent skills: https://openseo.so/docs/mcp , https://openseo.so/docs/skills/setup
- Self-host with Docker or on your own Cloudflare account (free plan works). The first visitor becomes admin.
- Data comes from DataForSEO. Bring your own key, pay per use. Key lives in an env var on the server, never in git or chat.
- R (third-party page): local MCP endpoint `http://localhost:3001/mcp`, added with `claude mcp add --transport http --scope user openseo http://localhost:3001/mcp`. Search Console link needs your own Google OAuth client. Confirm both in the official docs.
- **Plug-in plan:** owner hosts it and shares the MCP URL. The SEO agent writes dated files to `03_SEO/keywords/` and `03_SEO/competitors/`. A weekly rank-tracking diff is added. The website agent reads only the final keyword map, so the two agents run in parallel. Owner sets a DataForSEO spend cap first.

## Needs owner
Domain, Cloudflare account, DataForSEO spend cap, OpenSEO host URL.
