# A/B tests for a low traffic IIP site

Written 2026-11-08.

**Verdict:** A new local site will not have enough traffic for small tests. Test only big, bold changes, use clicks on call and WhatsApp as the main measure, run two way tests, and use before and after checks in Search Console for SEO changes.
**Evidence:** Sample sizes below are computed with the standard two proportion formula (95% confidence, 80% power). Seer Interactive, Convert, Optimizely and Portent all say low traffic sites should test large differences and higher volume metrics (read: Seer; others reported). SearchPilot says SEO split tests need many similar pages and traffic, which a new site lacks.
**Caveat:** Numbers depend on the baseline rate, which IIP does not know yet. Re-run the table once 4 weeks of GA4 data exist.

Labels: V = read, R = reported, G = my judgement.

## Reality check
Visitors needed per variant to detect a given lift (computed 2026-11-08):

| Baseline to target | Relative lift | Visitors per variant | Both variants |
|---|---|---|---|
| 2% to 4% | 100% | 1,143 | 2,286 |
| 3% to 6% | 100% | 750 | 1,500 |
| 3% to 4.5% | 50% | 2,519 | 5,038 |
| 5% to 7.5% | 50% | 1,472 | 2,944 |
| 8% to 12% | 50% | 884 | 1,768 |
| 8% to 16% | 100% | 260 | 520 |

Example: if the site gets 600 visitors a month, a 3% to 6% test takes 1,500 / 600 = 2.5 months. A 8% to 16% micro conversion (call or WhatsApp click) takes about 1 month. Rule from practitioners: if the sample needed divided by weekly traffic is more than about 8 weeks, test a bigger change, use a higher volume metric, or skip the randomised test (R, Single Grain, Convert style guidance).

Rules (R from [Seer](https://www.seerinteractive.com/insights/not-enough-traffic-for-ab-testing), [Optimizely](https://support.optimizely.com/hc/en-us/articles/4410283325325), [Convert](https://convert.com/blog/a-b-testing/i-dont-have-enough-traffic-to-a-b-test-now-what/)):
1. Two variants only (A and B).
2. Test big changes (offer, structure, headline angle), not colours.
3. Choose the stop rule before starting. Do not stop early because it "looks significant".
4. Primary metric is a micro conversion (click on call, WhatsApp or directions), secondary is form submit. Real enquiries are the tie breaker, since volume is too low.
5. One test at a time per page.
6. Split by device if mobile is over 80% of traffic, because phone and desktop behave differently (G).

## CRO tests (change the page, split visitors)

| ID | Test | A | B | Metric | Notes |
|---|---|---|---|---|---|
| T1 | CTA wording | "Call now" | "Book a site visit" | Click on CTA, then enquiries | Big change in intent, likely detectable |
| T2 | Contact method | Sticky bar with call only | Sticky bar with WhatsApp and call | Total contact clicks | Mobile only; WhatsApp is usually the lower friction option in India (G) |
| T3 | Hero | Image first (warehouse render) | Proof first (Section 80, approvals, 50 ft roads, 4.7 km) | Scroll depth, contact clicks | Do not publish a proof line before the proof is on file |
| T4 | Form length | 2 fields (name, phone) | 5 fields (add industry, plot size, timeline) | Submit rate and lead quality (sales rating) | Short usually gets more leads; sales may prefer longer (G). Judge on qualified leads |
| T5 | Price | Price band shown | "Request price" | Contact clicks and enquiries | Highest impact, decide with owner first |
| T6 | Proof placement | Approvals section lower on page | Approvals right under hero | Contact clicks | |
| T7 | Distance phrasing | "4.7 km driving to expressway on-ramp" | "About 8 minutes to the expressway" | Contact clicks, page time | Both from the Google Maps measurement on file |
| T8 | Neighbour brands | Logos shown | Text only | Scroll and clicks | Only after permission |

## SEO tests (change search appearance, measure in Search Console)
A split test needs many similar pages and heavy traffic (SearchPilot rule of thumb: 100+ similar pages and 10,000+ monthly organic visits, R from [SearchPilot](https://searchpilot.com/resources/blog/what-is-seo-split-testing) and a vendor adjacent guide). IIP will not have that, so use before and after.

| ID | Test | Method | Window |
|---|---|---|---|
| S1 | Title tag and meta description rewrite on the 3 pages with most impressions | Record CTR and position for 28 days before, change, record 28 days after. Compare against a page you did not change | 8 weeks |
| S2 | GBP primary photo and description changes | GBP Insights (calls, directions, views) 4 weeks before and after. Change one thing at a time | 8 weeks |
| S3 | Add FAQ block or distance table to a page | GSC impressions and CTR for that page, 28 days before vs after | 8 weeks |
| S4 | Internal links from home to the plots page | Position and clicks for the plots page | 8 weeks |

Cautions: seasonality, Google updates and new links change results. Keep a change log (04_Analytics/changelog) with dates, so results are not blamed on the wrong change. Google allows A/B tests if you do not cloak and use canonical or temporary redirects correctly, see [Google website testing guidance](https://developers.google.com/search/docs/crawling-indexing/website-testing) (page exists, rules not read in full).

## Free tools (checked that the sites load; features R or G)
- [Microsoft Clarity](https://clarity.microsoft.com/): free heatmaps and recordings.
- [GrowthBook](https://www.growthbook.io/): open source experiment tool, can be self hosted, works with GA4 data.
- [PostHog](https://posthog.com/): product analytics with free tier and experiments.
- GA4 plus Search Console (free).
- Static site split: Cloudflare edge or a small script that assigns a variant and adds `utm_content` (G).
- Google Optimize is closed (R, ended 2023), do not plan on it.

## What to measure always
Contact clicks (call, WhatsApp, directions), form submits, qualified leads rated by sales, site visits booked, cost per lead where there is paid traffic, GBP calls and directions, branded search impressions.

## Order of tests
1. T2 and T1 first (cheap, high intent, mobile).
2. T3 and T6 after the proof pages exist.
3. T5 only with the owner's decision.
4. S1 once Search Console has 4 weeks of data.
