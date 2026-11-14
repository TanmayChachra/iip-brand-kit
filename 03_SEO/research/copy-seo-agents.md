# Copywriter plus SEO agent: tools and content plan

Research date: 2026-11-13. Research only, no website edits, nothing committed. Labels: **verified** (read at the source or via `gh api`, dated), **reported** (third party), **guess**.
Stars, licence and push dates below are **verified** with `gh api repos/<owner>/<repo>` on 2026-11-13.

## 1. What we already have (do not duplicate)
- Own voice system: `06_Content/voice/` (VOICE, APPROVED, REJECTED, FEEDBACK-LOG) and skill `iip-copywriter` (reads the bank, 3 options, self-check, logs reactions).
- Installed: marketingskills (copywriting, copy-editing, seo-audit, ai-seo, programmatic-seo, site-architecture), brand-voice, claude-seo core (technical, schema, sitemap, local, geo), astro-seo, static-seo, metadata-check, 12 OpenSEO skills.
- Data: OpenSEO MCP (connected). `real-volumes-2026-11-09.md`: only 6 of 92 phrases show any volume, the biggest is "industrial plots" at 590 a month. So new pages are **trust and AI-answer content**, not a traffic plan.

## 2. Ranked tools (fit to this project)
| # | Tool | Covers | Licence | Stars | Last push | Install | Status | Risks |
|---|---|---|---|---|---|---|---|---|
| 1 | AgriciDaniel/claude-seo, skills `seo-content-brief` and `seo-programmatic` | (a) briefs with SERP gap scoring, intent, info gain, E-E-A-T list, internal links; (c) thin and duplicate gates (under 40% unique body text flags, 30% hard stop, batches of 50 to 100) | MIT | 28,939 | 2026-11-11 | **Installed today** by copying the two folders into `~/.claude/skills/` (see section 5) | installed | Brief skill is US and AU flavoured (excluded-domain list has AU sites), no India local rules. It cites a `quality-gates.md` we do not have (harmless). Its claim that Google retired FAQ rich results on 2026-05-07 is reported, matches 9 secondary articles, official page not read |
| 2 | vale-cli/vale | (b) deterministic voice linter: banned words (`existence` rule), em dash, sentence length, regex for "not X, just Y", "no A, no B" lists | MIT | 6,386 | 2026-11-12 | Download the release binary from https://github.com/vale-cli/vale/releases (exact package-manager name not checked, guess `choco install vale`). Put rules in `06_Content/voice/vale/` | not installed | Needs a one-time rules file made from VOICE sections 5 to 7. Rules catch form only, not meaning. Free, offline, no LLM cost |
| 3 | promptfoo/promptfoo | (b) eval harness: run the copywriter on 20 fixed prompts, assert `not-contains` banned words, `javascript` word counts, `llm-rubric` for tone, APPROVED lines as few-shot, REJECTED lines as must-fail cases | MIT | 27,133 | 2026-11-13 | `npx promptfoo@latest init` inside `06_Content/voice/evals/` (run only after owner OK, it needs a judge model key in an env var) | not installed | Company agreed to be acquired by OpenAI, announced about 2026-03-09, stays MIT per its own blog (reported, https://www.promptfoo.dev/blog/promptfoo-joining-openai/), deal status unclear. LLM judge costs tokens, so keep the suite small |
| 4 | anthropics/knowledge-work-plugins, marketing plugin (`brand-review`, `content-creation`, `draft-content`) | (b) severity-ranked brand review with before and after fixes, a pattern to copy | Apache-2.0 | 35,642 | 2026-11-13 | Not installed. Read the 13 KB `brand-review/SKILL.md` and copy the severity table into our own claim-check skill | pattern only | Written for Cowork with connectors and a team style guide. Duplicates `iip-copywriter` if installed whole |
| 5 | AgriciDaniel/claude-seo, rest: `seo-cluster`, `seo-content`, `seo-hreflang`, `seo-maps`, `seo-competitor-pages` | (a) SERP-overlap topic clusters, E-E-A-T and thinness check, local maps | MIT | 28,939 | 2026-11-11 | Not installed. They call `scripts/claude-seo run ...` helper scripts and a missing `references/` folder, so a copy alone is half broken. Plugin installer (`install.sh`, curl-style) was deliberately skipped in the 2026-11-08 gate | held | Needs Python scripts and heavy WebSearch (hundreds of calls for clustering). Our whole keyword set has almost no volume, so clustering by SERP overlap buys little. Do by hand in the keyword map instead |
| 6 | Sarvam AI: sarvamai/skills (`translate/`, `sarvam-mcp`) | (e) machine translation to Hindi and others, SDK code skills | Apache-2.0 | 73 | 2026-11-13 | Not installed | held | Needs a paid or credit API key (env var). Machine translation of land and legal wording must be read by a native reviewer. **Hindi is blocked by the owner rule today** (see 4.9). Skills teach SDK use, they are not a Hindi copywriter |
| 7 | AI4Bharat/IndicTrans2 | (e) open translation model, 22 Indian languages | MIT | 495 | 2025-10-03 | Not installed | held | Research model, needs GPU setup (the RTX 5070 Ti would run it), translation only, no brand voice, push is a year old |
| 8 | blader/humanizer | (b) strips AI tells from prose | MIT | 68,704 | 2026-11-10 | Not installed | skip | 32 KB skill plus scripts and agents. Overlaps `copy-editing` (already removes AI tells) and could pull our voice toward its own style. Use Vale rules for the same job |

Considered and not recommended:
- DataForSEO official MCP (dataforseo/mcp-server-typescript, 261 stars, Apache-2.0, 2026-11-02) and Search Console MCPs (saurabhsharma2u/search-console-mcp 322 stars, MIT, 2026-10-21): OpenSEO already wraps DataForSEO and Search Console (`get_search_console_performance`, `get_search_opportunities`). A second path adds keys and cost for nothing.
- Tiny GitHub "local SEO skill" and "seo content agent" repos (1 to 3 stars each, no licence file seen): not trusted, not read.
- stanford-oval/storm (31,872 stars, MIT, last push 2025-09-30): writes cited research reports. Useful idea, but our pages need owner facts, not web synthesis.
- Hindi and Hinglish writing quality: no credible open project found that scores Hinglish copy. The only safe quality gate is a native reader (owner or a hired editor). Label: gap.
- India local B2B land SEO skill: none found. Our own `seo-local`, `local-seo` and OpenSEO local tools (`get_local_rank_grid`, `search_local_businesses`, `get_business_profile`) are the stack.

**Top 3 to use:** (1) claude-seo content-brief plus programmatic gates (installed), (2) Vale voice linter, (3) promptfoo voice evals.

## 3. (d) Content gap analysis with OpenSEO (needs owner yes for credits)
OpenSEO rule: confirm before batches over 2,000 credits. Suggested cheap order, each with `estimate` first:
1. `find_serp_competitors` for "industrial plots in ghaziabad" and "industrial plot for sale" (who ranks: CKS, SHD, Atom, portals).
2. `get_ranked_keywords` for CKS and SHD domains, then diff against `keyword-map.md` to list phrases they hold and we have no page for.
3. `get_search_opportunities` on our own site once indexed (GSC), then `get_keyword_metrics` for the new page titles in section 4.
4. One Hindi and Hinglish volume check (only to give the owner data on 4.9).
Output goes to `03_SEO/keywords/` with dates. Plans do not change from this alone.

## 4. Content plan: depth without fluff
Rules for every page: voice from VOICE.md, facts only from VOICE section 8, `00_ISAPUR_KNOWLEDGE.md` section 3 and the two research files. One tagline at most. No price, water, security, resale, returns, brand names, developer name. Phone 98377 64222 only. Page title, meta, canonical, schema stay with the build (astro-seo, keyword-map). Target keywords are **guess** unless noted. Length: 500 to 900 useful words, never padded (floors in `seo-content` are floors, not goals, reported by the repo and by Google statements it quotes).

Known conflicts to fix before writing:
- `keyword-map.md` still shows phones 98370 57800 and 92195 49800. 92195 49800 is HELD until about 2026-11-19 and 9837057800 is no longer the sale line. Update the map first.
- Expressway figure: 4.7 km (Google Maps, 2026-11-06), 4.3 km straight-line, 4.2 km (OSRM, 2026-11-13). Owner picks one number and one pin for the whole site before the new pages use it.
- Knowledge file section 1 lists 100+ acres and Section 80, VOICE bans both. Do not reuse.

### 4.1 /how-buying-works/ (priority 1)
- Keyword: how to buy industrial plot in Ghaziabad (already a secondary in keyword-map). Intent: informational leading to commercial.
- Outline: see what is open; pick and walk the plot; papers on the table with your advisor; payments made through IIP; registry (owner says about 3 months, no time promise on page unless owner OKs); what to bring on the visit.
- Proof needed: owner fact 2026-11-12 (IIP shows inventory, mediates, payments through IIP, registry timing). Owner to confirm each step order and who signs what.
- Supplier: owner (steps and order); copywriter drafts; owner reads.

### 4.2 /location/roads-and-freight/ (priority 2)
- Keyword: industrial plots near Delhi Meerut Expressway (exists as landing), new angle "freight from Hapur Modinagar Road". Intent: commercial.
- Outline: distance ladder from `connectivity.md` (expressway entry, Modinagar about 11 km, Hapur about 14, Muradnagar about 21, Meerut about 30, Ghaziabad about 34, Anand Vihar about 46, India Gate about 55, Noida about 48); "reach the Eastern Peripheral Expressway in about 18 km" (junction name is reported, so say it softly); how a container goes by truck to Dadri then by train to a port (plain version of `dadri-shipping.md` section 3, Dadri about 44 km to Dadri town); each figure labelled "by road from the park, free-flow, traffic not included".
- Proof: OSRM runs dated 2026-11-13 (verified, pin approximate), Wikipedia and trade press for the corridors (reported, use none on page except as a "read more" if the owner wants). Never say "on the freight corridor", "Modinagar exit" or "goods station nearby".
- Gap to close first: exact Dadri terminal pin, one expressway number (see conflicts). Supplier: research agent reruns OSRM with the pin; owner picks the figure.

### 4.3 /shops/ (priority 3)
- Keyword: shop in industrial park Modinagar (G, none competition). Intent: commercial.
- Outline: "Shops for the people who serve the factories" (approved line) as H1 support; who they serve; trades named by the owner (confectionery, quick food, tyre repair); how a shop owner books; visit hours.
- Proof: owner facts only (all commercial, any trade). Needed: shop sizes, whether sold or leased, count, location in the layout. No footfall claim, no income claim.
- Supplier: owner supplies size and sale terms; copywriter drafts.

### 4.4 /guides/check-layout-approval/ (priority 4)
- Keyword: how to check layout approval industrial plot UP (G). Intent: informational, builds trust. High AI-answer value.
- Outline: what a sanctioned layout map shows (number, date, stamp, plot numbers, road widths); how to ask for it; what to compare with the registry papers and the site; "bring your advisor, we show every paper". Warm tone, no disclaimer wording (REJECTED rule).
- Proof: `06_Content/approvals-facts.md`, the Zila Panchayat map number and date (open question 2 in the knowledge file), and a lawyer or CA read of the checklist so it is not wrong.
- Supplier: owner supplies documents and the advisor read; copywriter drafts. Use the wording "Layouts sanctioned by Zila Panchayat Ghaziabad, subject to conditions" only on the papers page and here once.

### 4.5 FAQ expansion on /faq/ (priority 5, cheap)
- Keyword: industrial plot questions answered; PAA style. Intent: informational.
- Add 12 to 16 questions in four groups: buying, papers, getting here, running a unit. Answers 40 to 60 words, answer first, link to the guide pages above.
- Proof: each answer maps to a fact id. Questions we cannot answer yet (price, water, drainage, security) are left out, not dodged.
- Schema: FAQ rich results were retired by Google on 2026-05-07 (reported, secondary sources). Keep the content, treat FAQPage markup as optional and low value, never claim a rich result.

### 4.6 /guides/plot-size-guide/ (priority 6)
- Keyword: 300 sq yard industrial plot (G, in keyword-map as medium). Intent: informational and commercial.
- Outline: sq yd to sq ft to sq m (9 sq ft and 0.836 sq m per sq yd, arithmetic); what 300 sq yd, 500, 750 and 2000 to 2500 look like against a 50 ft road and a truck turn; questions to ask before choosing size.
- Proof: owner range (300 up, largest 2000 to 2500). Counts by band are DF (drawing figure) and stay off the page until the owner OKs. Anything about what shed fits needs the architect or owner (permitted coverage is unknown, do not guess).
- Supplier: owner or architect for two real examples (a unit that runs here, no brand).

### 4.7 /neighbours/ (draft exists, priority 7)
- Keyword: industrial units near Modinagar Hapur road (G). Intent: commercial investigation.
- Outline: running units by trade with no brand names (tile-bonding chemicals, comfort cushions, PVC pipes; the water tank unit stays out because the word is banned); why neighbours matter (shared roads, suppliers, shift-change tea stalls); what a new unit can expect.
- Proof: owner confirms units are running and allows the trades to be named. Photos when the site shoot happens. Partner brands only after the owner confirms and presence is verified.
- Supplier: owner.

### 4.8 /investors/ (priority 8, hold)
- Keyword: industrial plot investment Ghaziabad (G). Intent: commercial.
- Only safe content: who buys (investors are on the owner buyer list), what to look at (location, road, papers, access), how to visit. Words returns, appreciation, resale, guaranteed are banned and have no proof. This page would be thin today. Build after the buying and approvals pages exist, as a short page that links to them. Owner to say what an investor is offered.

### 4.9 Hindi page (priority: owner decision first)
- Conflicts with the owner decision 2026-11-02 (knowledge file section 1, REJECTED: "Hindi taglines and Hindi text") and VOICE section 5. Do not build or draft.
- Offer the owner data: a Hindi and Hinglish volume check in OpenSEO (cost estimate first). If volume shows and he reopens it, make one `/hi/` page with its own hreflang, written by a native editor with the Sarvam or IndicTrans2 draft as a helper only.

### 4.10 Deepen existing pages (no new URL)
- Home and `/amenities/`: one short block per fact (50 ft RCC roads, lighting, greenery, power 24/7 from Modinagar and Hapur lines, pump at entry and exit), each saying what it means for a truck or a night shift. Use APPROVED rhythm.
- `/location/` landing pages stay unique (distances, roads); do not template-swap names. Run `seo-programmatic` uniqueness gate over the five (body unique text 40% or more, metadata shapes differ).
- `/blog/` has 2 posts. Each guide above can live under `/guides/` or `/blog/`, one choice for the whole site, to avoid two hubs.

### 4.11 Order of work
1. Fix phones and distance number conflicts. 2. Buying, roads and freight, shops (facts mostly in hand). 3. Approvals guide, FAQ, plot size once the owner supplies items. 4. Neighbours after owner permission. 5. Investor page and Hindi only on owner decision.

## 5. Agent workflow (one agent, eight gates, files in `06_Content/briefs/` and `06_Content/drafts/`)
| Gate | Who or what | Output | Fail rule |
|---|---|---|---|
| 1 Brief | `seo-content-brief` plus OpenSEO SERP and keyword calls | `briefs/<slug>.md`: intent, outline, info gain, internal links, fact ids needed | Any outline section with no fact id is marked "owner to supply" |
| 2 Draft | `iip-copywriter` (reads VOICE, APPROVED, REJECTED, last 20 FEEDBACK lines) | `drafts/<slug>.md`, 3 options for headline and intro, body once | Uses only the brief's fact ids |
| 3 Voice check | Vale rules, then promptfoo case (APPROVED as pass examples, REJECTED as must fail) | pass or list of hits | Any banned word, em dash, disclaimer, bait question, sentence over limits |
| 4 Claim check | read-only agent (tools Read, Grep only) | table: each number and claim, fact id, source, label | One untagged number or any held or banned item (92195 49800, water, security, price, resale, returns, brand, developer, 100 acres) fails the page |
| 5 SEO check | `seo-content` style checks by hand, `metadata-check`, `astro-seo`, keyword-map placement (title, H1, slug, first 100 words), uniqueness gate, internal links 3 to 5, no override of page title, meta, canonical or schema | checklist in the draft footer | Thin, duplicate, or a claim in schema with no proof |
| 6 Owner approval | batch to the owner as short options, no internal notes in page text | verdict per page | Nothing publishes without a yes |
| 7 Log feedback | `iip-copywriter` learning loop, same turn | FEEDBACK-LOG line, then APPROVED or REJECTED with reason; merge repeated rejections into VOICE section 10 | Each new rejection becomes a Vale rule or a promptfoo must-fail case |
| 8 Ship and record | web agent builds, docs synced per project CLAUDE.md | KNOWLEDGE change log, TODOS, CHANGELOG | Do not edit `02_Website` from the copy agent, hand off through the contract files |

Build steps (not done now, owner OK first): (1) `claims-allowed.json` extracted from VOICE section 8 so gate 4 is mechanical; (2) Vale rules file; (3) 20 promptfoo cases seeded from APPROVED and REJECTED; (4) one agent file `iip-seo-writer` that runs gates 1 to 5 and stops at gate 6.

## 6. Install record (2026-11-13)
Read in full before copy: `seo-content-brief/SKILL.md` (11 KB), its three `references/*.md`, `seo-programmatic/SKILL.md` (10 KB), both `LICENSE.txt` (MIT notice). Pulled with `gh api` from github.com/AgriciDaniel/claude-seo into the session scratchpad, no script run, no installer run. Grep for curl, wget, eval, base64, pip, npm, subprocess found nothing in either skill; `seo-programmatic` mentions one optional helper script `metadata_template.py` that we did not copy (the skill still works without it). Installed to `~/.claude/skills/seo-content-brief/` (3 files plus references) and `~/.claude/skills/seo-programmatic/` (2 files). Loads in the next session. Read but not installed: `seo-cluster`, `seo-content` (script dependent), knowledge-work-plugins `brand-review` (head only), Sarvam `translate/text` (head only).
