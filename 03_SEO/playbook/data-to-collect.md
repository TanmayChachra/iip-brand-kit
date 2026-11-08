# Data to collect to optimise IIP content

Written 2026-11-08. Part A comes from the owner. Part B is collected from visitors and prospects once the site is live.

**Verdict:** The site wins on specific, provable facts: plot sizes, approvals, distances, roads, power and the neighbours. Most of these must come from the owner and sales team, not from research.
**Evidence:** Ahrefs says AI assistants and buyers need clear answers on what, who for, cost, differences and where to start, and suggests mining sales calls for the questions (verified, ahrefs.com/blog/ai-search-strategy). Google asks for first hand expertise and depth (verified).
**Caveat:** Nothing here is published until the proof is on file. See the claims rule in 00_ISAPUR_KNOWLEDGE.md. Items marked "ask owner" block specific pages.

Source labels: V = verified by reading, R = reported, G = guess.

## Part A: from the owner and sales team

### A1. Legal and proof (blocks the Approvals page)
| Data | Why | Source |
|---|---|---|
| Section 80 document (what it is, issue date, who issued it) | A claim on any page needs proof; trust is the centre of E-E-A-T (V) | [Google helpful content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content), [Haynes](https://www.mariehaynes.com/the-december-2025-core-update-observations-on-4-sites-that-did-well/) |
| Zilla Panchayat approval or map pass, reference number, date | Same | same |
| Land title status, any RERA or other registration number if applicable (ask owner whether it applies) | Buyers ask first; avoids a wrong claim (G) | project |
| Power sanction (load, utility, substation) | Industrial buyers decide on power (G) | project |
| Naala and drainage proof | Poster says "Waste Water Drainage"; proof still open in knowledge file | 00_ISAPUR_KNOWLEDGE.md |
| Written permission to name neighbour brands (Amul, Inox Air, Patanjali and others), what each is (inside or nearby), distance, plant type | Brand mentions are valuable for AI and trust (V, Ahrefs) but naming without permission or proof is a risk | [Ahrefs](https://ahrefs.com/blog/ai-search-strategy/) |

### A2. Inventory and offer
| Data | Why |
|---|---|
| Plot sizes available (poster says starting from 300 sq yd), total plots, phases, number sold, number available | Powers the plots page and "plot size" keyword pages |
| Price bands per sq yd, or the decision to show "on request" | Needed for test T5 (price shown vs request); price is a top question (G) |
| Payment plan, bank loan support, registry and possession process and timeline | Reduces objections |
| Permitted industry types and banned types | Buyers filter by this (G) |
| Plot size most requested and why | Content focus (G) |

### A3. Site facts
| Data | Why |
|---|---|
| Exact GPS pin and full postal address as it should appear everywhere | One address across GBP, site, portals (V, Ahrefs on consistent profiles) |
| Road width and surface by lane (the "50 ft RCC" claim) with photo | Proof |
| Water, drainage, street lighting, greenery, security, boundary wall, gate | Amenity pages |
| Petrol pump at the park exit: operator brand, name, fuel, hours, truck access, photos | Unique local asset; strong for Maps and "near" queries (G) |
| Verified distances: expressway on-ramp 4.7 km driving (on file), Modinagar bus stand 11.4 km, Hapur bus stand 13.4 km (on file); add railway, ICD, dry port, Meerut, Ghaziabad, Delhi, labour towns | Linkable distance table |
| Nearby industrial clusters and employers | Context, natural mentions |

### A4. Sales intelligence (the most useful and cheapest data)
| Data | Why | Source |
|---|---|---|
| Top 20 questions callers and visitors ask, in their words | FAQ page and AI prompts. Ahrefs: sales and support calls are great prompt sources (V) | [Ahrefs](https://ahrefs.com/blog/ai-search-strategy/) |
| Top 10 objections and why deals were lost | Page copy, proof placement | [Sparktoro audience research](https://sparktoro.com/blog/in-2026-less-than-one-third-of-google-searches-still-send-a-click/) (R) |
| Typical buyer: industry, current location (Delhi, Ghaziabad, Meerut, Hapur), size, local or outside | Persona, keywords, location pages |
| Where each lead came from last 6 months (board, referral, broker, GBP, ads, walk in) | Prioritise channels |
| Phone call themes from last 50 calls and WhatsApp chats (remove personal details) | Content gaps |
| Competitors buyers compare IIP with and what they said | Comparison content, competitor gap |
| Site visit to booking rate and typical time between first call and booking | Sets realistic test lengths (see ab-tests.md) |

### A5. Profiles
| Data | Why |
|---|---|
| GBP owner access (manager invite) | Needed for audit and edits |
| Business hours, WhatsApp Business number, one sales email | Consistent contact data |
| Social handles and domain choice | Entity consistency |
| Photo and video library with dates and captions | GBP, gallery, YouTube |

## Part B: from visitors and prospects (collect through the site)

### B1. Google Search Console fields to export monthly
Queries, pages, clicks, impressions, CTR, average position, country, device. AI Overview and AI Mode traffic is counted in the "Web" performance report (verified in [Google AI features](https://developers.google.com/search/docs/appearance/ai-features)). Use [Search Console and Analytics together](https://developers.google.com/search/docs/monitor-debug/google-analytics-data-search-console) (URL not checked, open to confirm).

### B2. GA4 events (spec lives in 04_Analytics)
Call click, WhatsApp click, directions click, form start, form submit, brochure download, plot size selected, section viewed, scroll depth, outbound click, FAQ opened. See [GA4 event help](https://support.google.com/analytics/answer/9267735). Mark call, WhatsApp, directions and form submit as key events.

### B3. Enquiry form fields (keep it short; test length in T4)
Required: name, phone. Optional: industry or product, plot size needed, when they want to buy or visit, where they are now. Hidden: source page, UTM fields, click ID. Do not ask for sensitive IDs. India's Digital Personal Data Protection law applies to collecting phone numbers, so show a short consent line and a privacy page (R, check with a lawyer).

### B4. UTM scheme
`utm_source` (google, gmb, facebook, whatsapp, justdial, indiamart, board_qr, print_qr, youtube, broker), `utm_medium` (organic, cpc, referral, qr, listing, social), `utm_campaign` (short stable names such as plots_launch, expressway_video), `utm_content` (variant, used in tests). Always tag the GBP website link, QR codes on boards and every listing, so offline and listing traffic shows up (G, standard practice).

### B5. Reviews
Prompt every visitor within 24 h of a site visit with a one tap Google review link (Google lists reviews as ranking help, V). Record how many requests are sent and how many convert.

### B6. Behaviour data
Free session recordings and heatmaps (Microsoft Clarity, [clarity.microsoft.com](https://clarity.microsoft.com/), free, checked page exists) to see where mobile users stop. Call tracking numbers per channel are optional (G, provider choice open).

### B7. AI visibility log
Monthly: same 20 to 30 prompts in ChatGPT, Gemini, Perplexity and Copilot; record whether IIP is named, correct or wrong, and which sources are cited (method from Ahrefs, V).

## Priority order if time is short
1. A1 proof, A3 address and distances, A4 top 20 questions. These unblock the site.
2. A2 plot sizes and price decision.
3. B2 events and B4 UTM live on day one.
