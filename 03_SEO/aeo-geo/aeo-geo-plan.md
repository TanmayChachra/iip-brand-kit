# AEO and GEO plan (answer engines and AI search)

**Verdict:** Do normal good SEO first, then make every key page answer-first, consistent and crawlable by AI bots. Skip llms.txt as a ranking tactic; add it only as a cheap extra.
**Evidence:** Two large studies found no link between llms.txt and AI citations, and Google's own guidance says AI features need no special files or schema (see sources, 2026-11-08). Strong signals are crawlability, clear text answers, Bing and Google indexing, consistent entity data and third-party mentions.
**Caveat:** Most "how to get cited" guides are vendor blogs and inferred from what gets cited, not documented by Perplexity or OpenAI. Treat them as hypotheses, test with the tracking steps below.

## What each engine uses (reported unless noted)

| Engine | How it finds sources | What to do |
|---|---|---|
| Google AI Overviews and AI Mode | Normal Google index. Google says no special markup or llms.txt is needed (reported from coverage of Google's AI features page) | Index in Search Console, fast pages, answer in visible text, structured data that matches the page, strong Google Business Profile |
| ChatGPT search | Own crawler OAI-SearchBot plus Bing results (reported) | Allow OAI-SearchBot and ChatGPT-User in robots.txt. GPTBot only controls training. Index in Bing |
| Perplexity | PerplexityBot plus Bing (reported, sources disagree on share) | Allow PerplexityBot. Short answer near the top, dates, original numbers. Reddit and Quora help (reported) |
| Microsoft Copilot | Bing index | Bing Webmaster Tools, IndexNow, Bing Places |
| Gemini | Google index and Maps data | Same as Google, plus complete Maps listing |
| Apple Intelligence and Siri | Apple Maps, Business Connect, Apple's own web crawler (Applebot, reported) | Apple Business Connect listing, allow Applebot |

## The plan, in order

### 1. Foundations (when the site goes live)
- robots.txt: allow Googlebot, Bingbot, OAI-SearchBot, ChatGPT-User, PerplexityBot, Applebot. Decide about training bots (GPTBot, Google-Extended, CCBot) as a business choice, it does not affect search citations.
- XML sitemap, canonical tags, clean HTML text (no key facts inside images only), fast pages (Astro suits this).
- Submit to [Google Search Console](https://search.google.com/search-console) and [Bing Webmaster Tools](https://www.bing.com/webmasters). Turn on [IndexNow](https://www.indexnow.org/) for instant Bing updates.
- Structured data that matches visible text: Organization, LocalBusiness or a fitting type for the park, FAQPage where real FAQs exist, BreadcrumbList, Place with geo coordinates. Google says AI features need no special type, it still helps normal search.

### 2. Answer-first content
- Every key page opens with a 40 to 60 word direct answer, then detail. Examples of questions: "Where can I buy industrial plots near Modinagar?", "How far is the Delhi-Meerut Expressway from Isapur?", "What is the cost of an industrial plot in Hapur-Modinagar?", "Is Isapur Industrial Park approved?" (answer only with proof on file).
- Real FAQ blocks, short, with a date. Update dates when facts change.
- Original facts only we have: road width 50 ft RCC, distances (say driving or straight-line), plot sizes from 300 sq yards (once confirmed).
- Compare pages (parks near the expressway) written fairly, with sources. AI tools like neutral tables.

### 3. Entity building (so AI knows who we are)
- One name and one NAP everywhere (see 05_Local-Presence/citations/citations-targets.md).
- Same-as links in Organization schema: Google Business Profile, Facebook, LinkedIn, YouTube, Instagram, X, 99acres page.
- Wikidata item only after 3 or more independent references exist. A Google Knowledge Panel usually follows a clean entity, you cannot request it directly, you can claim it once it appears.
- Brand mentions on third-party sites beat on-site tricks. Google says inauthentic brand mentions are discouraged, so only earn real ones (see backlinks.md).

### 4. Where to be listed
- Maps: Google, Bing, Apple (all P0 in citations list).
- Social and video: YouTube (AI Overviews cite it often, reported), LinkedIn, Facebook.
- Q&A: Reddit and Quora with honest answers (strict rules, disclose affiliation).
- Property portals and B2B marketplaces: they are the pages AI tools show for "industrial plots in Modinagar".
- Perplexity Publishers Program: aimed at established publishers, not a lever for us now (reported).

### 5. llms.txt: decision
- Evidence: SE Ranking study of about 300,000 domains found no correlation; Trakkr scan of 37,894 cited sites found 6.8 vs 6.7 average citations, not significant; Google guidance says it is not needed (reported).
- Decision: skip as a priority. Optional: add a plain `/llms.txt` that lists the 8 main pages. It costs 10 minutes and can help some AI agents navigate, but expect no ranking effect.

## How to track AI citations

| Tool | Cost | Covers | Link |
|---|---|---|---|
| Manual prompt audit (a fixed list of 20 questions, run monthly in ChatGPT, Perplexity, Gemini, Copilot, Google AI Mode) | Free | All | log in `03_SEO/aeo-geo/prompt-audit.csv` |
| Ahrefs AI Visibility Checker | Free, no signup (reported) | ChatGPT, Gemini, Perplexity, Copilot, AI Overviews | [ahrefs.com](https://ahrefs.com/) (find the AI visibility checker page) |
| Semrush AI search visibility checker | Free option (reported) | ChatGPT, Gemini, AI Overviews | [semrush.com](https://www.semrush.com/) |
| SE Ranking AI visibility | Free checker plus paid tracker (reported) | Several engines | [seranking.com](https://seranking.com/ai-visibility-tracker.html) |
| Google Search Console | Free | Google AI Overviews and AI Mode traffic is counted within search performance (reported) | [search.google.com/search-console](https://search.google.com/search-console) |
| Bing Webmaster Tools AI performance | Free (reported) | Copilot and Bing | [bing.com/webmasters](https://www.bing.com/webmasters) |
| GA4 referrals from chatgpt.com, perplexity.ai, gemini.google.com, copilot.microsoft.com | Free | Real visits from AI tools | see 04_Analytics when written |
| Otterly, Profound, Peec AI | Paid | Many engines | skip until traffic justifies |

Audit questions (start list, 20 total in the CSV later): who has industrial plots near Modinagar, best industrial park on Hapur-Modinagar road, industrial plots near Delhi-Meerut Expressway, cost of industrial plot in Hapur, is Isapur Industrial Park legal, nearby factories.

## Sources (read 2026-11-08, all via search results, primary pages not re-opened)

- [SE Ranking: llms.txt data](https://visible.seranking.com/blog/llms-txt/) and [Search Engine Journal on the 300k domain study](https://www.searchenginejournal.com/llms-txt-shows-no-clear-effect-on-ai-citations-based-on-300k-domains/)
- [Trakkr web data](https://trakkr.ai/data/web?lens=category)
- [Google Search Central: AI features and your website](https://developers.google.com/search/docs/appearance/ai-features)
- [Previsible on Google's AI search guide](https://previsible.io/seo-ai-news/google-published-its-first-guide-to-ai-search-optimization/)
- [Perplexity SEO guide (vendor)](https://www.gogochimp.com/blog/perplexity-seo) and [GEO Toolbox Perplexity guide (vendor)](https://geotoolbox.ai/blog/perplexity-seo.md)
- [Free AEO and GEO checks (guide)](https://guptadeepak.com/how-to-check-aeo-and-geo-visibility-for-free-2026/) and [Backlinko LLM tracking tools](https://backlinko.com/llm-tracking-tools)
