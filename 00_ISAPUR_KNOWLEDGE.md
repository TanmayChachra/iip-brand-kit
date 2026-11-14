# ISAPUR INDUSTRIAL PARK: central knowledge file

**This file is the single source of truth. Never delete or move it. Append to the change log on every update.**

Project root: `D:\SILVERLEAF_BUILDCON\03_Marketing\IIP Branding`
Owner / contact person in git: Tanmay Chachra. Created 2026-11-06.

Truth labels used below: **VERIFIED** (read on a primary source or measured), **OWNER-STATED** (owner told us, no document seen), **UNVERIFIED** (third party, estimate or guess), **UNKNOWN** (no information found).

## Table of contents
1. Identity and contact
2. Location and distances
3. Amenities and claims
4. Competitors
5. Audience
6. Brand decisions and rejected options
7. Visual system summary (tokens)
8. Asset inventory and paths
9. Research index with source URLs
10. Tool and process log
11. Open questions for owner
12. Change log (append only)

---

## 1. Identity and contact
| Item | Value | Status |
|---|---|---|
| Name | ISAPUR INDUSTRIAL PARK (short form IIP) | OWNER-STATED (name as used in all supplied files) |
| Descriptor line | INDUSTRIAL PARK | in logo artwork |
| Phones | 9837057800, 9219549800 | OWNER-STATED (2026-11-02) |
| Address line used on assets | Hapur-Modinagar Road, Yusufpur Isapur, Ghaziabad, UP 201022 | OWNER-STATED location, pin code from public listing (UNVERIFIED) |
| Nearby village or town names used | Yusufpur Isapur (also written Ishapur), Bhojpur, Modinagar, Hapur, Sarawa | UNVERIFIED spelling variants |
| Phases | Owner speaks of Phase 1 and Phase 2. Google Maps lists Phase 1, 2 and 3 as separate places. Scope of each is UNKNOWN. | UNKNOWN details |
| Legal registered name, developer entity | DECISION 2026-11-06: the name is "Isapur Industrial Park" and the developer is NOT revealed anywhere in public material. Link with "Shri Hari Das" is UNKNOWN. A project called Shri Hari Das Industrial Park (SHD) exists at the same village, treated here as a competitor. | UNKNOWN |
| Website, social handles, email | UNKNOWN (social media phase is next) | UNKNOWN |
| Business | Industrial plots, 100+ acres, plots from 300 sq.yards (poster claim) | OWNER-STATED, see section 3 |
| Language | English only. Hindi was tried and rejected by the owner on 2026-11-02 ("i dont think hindi will work at all"). | DECISION |
| Tagline in use | "A Modern Industrial Address." | DECISION, from the owner's own ChatGPT kit |

## 2. Location and distances
IIP Phase 1 is on the Hapur-Modinagar Road at Yusufpur Isapur, near Bhojpur, Modinagar, Ghaziabad district, Uttar Pradesh. Pin used in all maps: lat 28.7812, lon 77.6559 (`work/maps.py`, comment says "approximate, read from Google Maps; verify against imagery"). Estimated accuracy about 200 m. Map centre used for the satellite image: 28.7755, 77.6695.

### 2.1 Distances from the IIP pin
Two kinds of figure. **Driving** distances were read from Google Maps (driving mode, 2026-11-06, about 6:50 PM IST, live traffic, source `Brand-Kit/research/driving-distances.json`). **Straight-line** distances were computed earlier (haversine to OpenStreetMap geometry). The pin (28.7812, 77.6559) is approximate (about 200 m). Maps snapped it to a factory address in Yusufpur Isapur. Maps lists Isapur Industrial Park Phase 1 (28.78090, 77.65588), Phase 2 (28.78165, 77.65564) and Phase 3 (28.78655, 77.65830, Isapur-Kharkoda Rd). Phase 3 distances differ by 0.1 to 1.2 km.

| To | Driving (Google Maps) | Straight-line | Note |
|---|---|---|---|
| Delhi-Meerut Expressway on-ramp (Get on NE 3 in Bhojpur) | **4.7 km, about 8 min** | 3.9 km nearest expressway point, 4.3 km Bhojpur exit node | Use the driving figure on boards. |
| Modinagar bus stand | 11.4 km, 28 min | 9.3 km | via Modinagar Rd |
| Hapur bus stand | 13.4 km, 31 min | 13.0 km | via Modinagar Rd |
| Meerut City railway station | 29.3 km, 56 min | n/a | via NE 3, tolls |
| Ghaziabad railway station | 34.7 km, 47 min | n/a | via NE 3, tolls |
| Anand Vihar ISBT, Delhi | 46.0 km, 89 min | n/a | via NE 3, tolls |
| SHD Industrial Park | 0.65 km, 2 min | 0.54 km | competitor |
| CKS Industrial Park | 0.7 km, 1 min | 0.69 km | competitor |
| Atom Industrial Park | 3.1 km, 4 min | 3.1 km | competitor |

Poster wording in use: "4 km away / Delhi-Meerut Expressway" is the straight-line figure and understates the 4.7 km drive. Decision pending (see TODOS.md).

### 2.2 Other location facts
- The Hapur-Modinagar road runs through Sarawa (bus stand, Shri Balaji board photographed there), Yusufpur Isapur and Bhojpur.
- Satellite imagery: Esri World Imagery (Esri, Maxar, Earthstar Geographics), a few years old. Pins approximate. File: `docs/assets/map-isapur.webp`.
- Ground-truth gaps: exact plot map, gate position, plot boundary. UNKNOWN.

## 3. Amenities and claims
Rule: nothing goes on a printed board unless the status is VERIFIED or the owner accepts the risk in writing in the change log.

| Claim as shown on poster or kit | Status | Proof to file |
|---|---|---|
| 100+ Acres | OWNER-STATED (from the poster image supplied) | Registry area statement or layout plan |
| Plots starting from 300 sq.yards | OWNER-STATED (poster) | Price/plot list approved for advertising |
| Approved by Zilla Panchayat (also "Map passed by Zila Panchayat") | OWNER-STATED | Sanctioned layout map with Zila Panchayat stamp and number |
| Section 80 / Legally Compliant | OWNER-STATED. Exact legal meaning not confirmed in this project. | Document that names Section 80, its authority and date. Wording must match it. |
| 50 ft. Wide RCC Roads | OWNER-STATED (poster). Competitor boards also advertise road widths. | Layout plan with road widths, site photo of laid road |
| Delhi-Meerut Expressway 4 km away | Straight-line figure computed from approximate pin (see section 2) | Driven distance with date |
| Highway Connectivity | Follows from the expressway distance | same as above |
| Waste Water Drainage | OWNER-STATED on 2026-11-06: the park has an industrial drainage and a naala at the back to dispose into. No public source found for this naala or for effluent rules at this site. | Dated photo of the naala, layout plan marking the outfall, any UPPCB (pollution board) consent. Industrial discharge into a naala normally needs a consent, UNVERIFIED for this site. |
| Reliable Power Supply | OWNER-STATED (poster) | Electricity connection or sanctioned load letter |
| Street Lighting (street lamps) | OWNER-STATED (owner asked for it to be highlighted on 2026-11-06) | Site photo of lit road, installed count |
| Planted Greenery | OWNER-STATED ("greenery hai humare yahha bohot"). Chosen label 2026-11-06. | Dated site photos |
| Manufacturing and Warehousing use | OWNER-STATED | Land-use approval |
| Warehouse hero image on poster and pole board | AI-generated visual, NOT a photo of IIP. Must not imply built facilities that do not exist yet. | Replace with a real site photo |

Wording notes (decisions, 2026-11-06):
- "Storm Water Drainage" was proposed and **rejected** by the owner. Use "Waste Water Drainage". "Sewerage" (underground pipe network to a treatment plant) was explained and is **not** used, because the park drains to an open naala, not a sewer.
- Industry terms found (UPSIDA press releases and investor material): storm water drains, sewerage network, CETP/STP. These are announcements for UPSIDA estates, not IIP specs.
- Other possible features (NOT claimed, only if true): 24x7 security and CCTV, gated entry, truck parking, water supply, labour dormitory. Weak evidence base, from park marketing and UPSIDA upgrade announcements.

## 4. Competitors
All details read from the owner's field photographs and public listings. UNVERIFIED unless stated.

| Park | Where | Board look | What it says |
|---|---|---|---|
| Shri Balaji Industrial Park | Sarawa bus stand, Hapur-Modinagar Road | Blue sky gradient, gold type; also a red board | Industrial plot, approval stamp, two numbers, rendered township |
| Shri Haridas Industrial Park (SHD) | Ishapur, Bhojpur, Modinagar. About 540 m from IIP. | White and navy, Hindi headline | Approval claim, rendered gate, road widths, security, two numbers |
| Shivansh Industrial Park | Not stated on board | Navy and gold, red phone bar | All sizes of plots available, two numbers |
| CKS Industrial Park | Hapur-Modinagar Road (listing). About 690 m from IIP. | Not photographed | Per-yard price and approval claim in public listings, unverified |
| Atom Industrial Park | Ishapur (Google Maps). About 3.1 km away. | Not photographed | Listed on Google Maps |
| Mahamaya | Named by owner as a competitor on the same road | Not photographed | UNKNOWN |

Findings:
- Every board uses navy, gold or red with dense copy: stamp, price, rendered township, two numbers. At 40 km/h only the numbers are readable.
- Measured board colours (`work/analysis.json`): Shri Balaji blue board grey-blue #A8B5B5 / tan #968973; Shri Balaji red board brown #845647; SHD navy #31333B and #555863; Shivansh charcoal #37383A and brown #795145. Roadside foliage olive greens (#595F4B, #464D3D, #6E745D), dust #5E5A48 / #958467, hazy sky #BFCCD9.
- Gap IIP fills: white space, one logo, one line.
- **Pole board size to match competitors: 20 x 32 in** (about 190 x 304 px at the pole in the mockup scale). 10 inch "stamp" boards were rejected by the owner because they looked tiny next to the competitors. Original owner request listed 10x10, 10x12, 10x14 in; superseded.
- Competitor photos: `References/competitors/competitor-boards.jpeg`, `competitor-boards-2.jpeg`.

## 5. Audience
- Primary: local factory owners and small industrial buyers along the Hapur-Modinagar road (owner, 2026-11-02).
- Secondary candidates (not confirmed by owner): warehouse and logistics operators, investors, brokers.
- Viewing condition: roadside at 40 km/h, so the board needs very few words (max 7 words on a board) and big phone numbers.
- Language: English only (owner decision, 2026-11-02).
- Owner's father (decision maker) dislikes conceptual adverts, so conceptual work is kept on an isolated route.

## 6. Brand decisions and rejected options
| Date | Decision or rejection | Why |
|---|---|---|
| 2026-11-02 | Logo is never changed. | Owner rule. Badge colours measured: yellow #FEF102, red #EE1D23, green #00A54F. |
| 2026-11-02 | Boards must not blend with greenery or competitor boards. | Owner rule. |
| 2026-11-02 | Mockups must look real: neutral light, no warm tones, no "ChatGPT softness". | Owner rule. Method: exact artwork warped into photo panels, never AI-drawn logo or text. |
| 2026-11-02 | No vector logo exists. | Owner. Badge in the kit is a trace of the supplied PNG. |
| 2026-11-02 | Proof lines (Section 80, Zila Panchayat) optional, default off on boards. | Owner: "empty is also good". |
| 2026-11-03 | Phones fixed as 9837057800 and 9219549800. | Owner. |
| 2026-11 | Route 2 "Portal doorway" (red door) rejected. | Owner: red door not used thoughtfully, bad vibe. |
| 2026-11 | Routes 1 (Quiet paper) and 3 (Ink night) liked for simplicity and white space. Others parked. | Owner. |
| 2026-11 | Tagline "Plug in. Build up." rejected. | Owner: sounded like random words. |
| 2026-11 | Hindi taglines and Hindi text dropped. | Owner, English only. |
| 2026-11 | Jamun violet, Gulaal pink, Kora ivory directions all dropped. | Owner told us to stop trying one palette or the QUIET theme and start from scratch; later supplied own finalised kit. |
| 2026-11-04 | Owner's own ChatGPT kit adopted as final: white board, charcoal text, yellow, red, deep green, Montserrat + Inter, sunburst device, "A Modern Industrial Address." | Owner: "finalized branding that I created". |
| 2026-11-05 | Hoarding placed next to competitors. Google Maps image supplied by owner to be ignored. | Owner. |
| 2026-11-06 | Poster layout: top facts as 3 x 2 grid (Acres, Zilla Panchayat, Section 80 / Legally Compliant, 50 ft roads, plot size, Expressway 4 km). Bottom row: Manufacturing & Warehousing, Reliable Power Supply, Highway Connectivity, Waste Water Drainage, Street Lighting, Planted Greenery. | Owner requests and our recommendation. |
| 2026-11-06 | "Straight-line distance" caption removed from the poster. Distances remain straight-line internally. | Owner. |
| 2026-11-06 | "Sustainable Development" replaced by "Planted Greenery". "Legally Compliant (Section 80)" three-line label replaced by "Section 80 / Legally Compliant" in the top grid. | Owner dislike, layout. |
| 2026-11-06 | New final brand assets supplied (3 boards). Old kits to be archived. A central knowledge file is required. | Owner. |
| 2026-11-06 | Tagline is ADAPTIVE: "A Modern Industrial Address." and "The groundwork for growth." both approved, chosen per creative, never both together. | Owner: likes both, does not want one fixed line. Stored in `Brand-Kit/tokens/content.json` under `taglines`. |
| Standing | Images online are WEBP. Never write Co-Authored-By lines. No em dashes anywhere. | Owner's global rules. |

Inspiration cited by owner: Vodafone poles (recognised from afar), Kofi Kafi blue, Nescafe, Emirates and Lufthansa restraint, real estate groups Karyan, DLF, SG. Files under `References/inspiration-ads*`.

## 7. Visual system summary (tokens)
Source: `Brand-Kit/tokens/brand.tokens.json` and `content.json`.

| Token | Hex | Use |
|---|---|---|
| White | #FFFFFF | Primary board and page background |
| Charcoal | #111827 | Text, contrast, wordmark |
| Yellow | #FFD600 | Highlight, stripe, CTA (badge keeps its own #FEF102) |
| Red | #E53935 | Accent line and highlight only |
| Deep green | #0F4D3A | Secondary: stripe, sustainability badge |
| Mist | #F2F4F6 | Surfaces, panels |
| Gray | #6B7280 | Secondary text |
| Line | #E5E7EB | Hairlines |
| Badge yellow / red / green | #FEF102 / #EE1D23 / #00A54F | Measured from supplied artwork. Never retint. |

The newest supplied board lists charcoal as #111827, yellow #FFD600, red #E53935, deep green #0F4D3A, mist #F2F4F6, plus neutrals #FFFFFF #E6E8EB #C9CED6 #6B7280 #000000. Poster ink colour used: #101d1a, grey text #666666.

- Fonts: Montserrat (display: 500, 600, 800; ExtraBold for ISAPUR) and Inter (text: 400, 500, 600). Both SIL Open Font License. Montserrat is an approximation of the original wordmark face (UNVERIFIED).
- Logo: clear space 0.25 x badge width; minimum size 30 mm print, 120 px digital, 16 px badge alone. Lockups: primary vertical, horizontal, stacked, badge only, mono black, reversed on charcoal.
- Layout: safe margin 6% of shorter side, max 7 words on a board.
- Graphic elements: 22-point sunburst (die-cut star, regular, centre 539.3 / 544.9, tip radius 543.8, valley 482.3 in logo source px), tri-colour stripe (yellow, red, green diagonal), diagonal panels, accent line, sunburst ring border, repeating pattern, CTA badges ("PLOTS AVAILABLE NOW").
- Icon style: line/outline icons, stroke about 5 px at poster scale, round caps. Set: industrial plots, wide roads, power supply, water supply, connectivity, sustainable development, secure infrastructure, business support, plug and play, growth opportunity. Poster-only added: truck (highway), drainage channel, expressway gantry sign, street lamp, tree, shield and tick.
- Tagline options in kit: "A Modern Industrial Address." (selected), "Where Industry Moves Forward.", "Built for Business. Designed for Growth.", "The Next Address of Industry.", "Space for What's Next."
- Pole advert: 2:3 street pole 24 x 36 in version also exists.

## 8. Asset inventory and paths
All paths relative to the project root.

| Path | What |
|---|---|
| `00_ISAPUR_KNOWLEDGE.md` | This file |
| `IIP Assets/logo.jpeg`, `IIP Assets/Dark Green IIP Rosette Emblem.png` | Supplied logo files (read by `work/logo/prep.py`, do not rename) |
| `Brand-Kit/tokens/` | `brand.tokens.json`, `content.json` (single source of truth for the generators) |
| `Brand-Kit/live/`, `Brand-Kit/outlined/` | 34 editable and outlined SVGs: 01_Logo (6), 02_Pattern (7), 03_Icons (10), 04_Templates (11) |
| `Brand-Kit/export/pdf`, `export/png`, `Brand-Kit/editable-pptx/` | PDF at true size, PNG previews, PowerPoint versions |
| `Brand-Kit/05_Mockups/`, `Brand-Kit/examples/` | Hoarding next to competitors, worked adaptation examples |
| `Brand-Kit/_build/` | Generators: `build_kit.py`, `export.py`, `build_pptx.py`, `kitlib.py` |
| `Isapur-Poster/03_Design/00_LATEST_isapur-industrial-park.pdf` | Latest poster PDF (1827 x 2290). Master SVG `01_LATEST_...svg`, preview `02_LATEST_preview.png`, older versions in `_archive/v01..v09` |
| `Isapur-Poster/02_Logo/` | Poster logo SVG with one continuous halo stroke, PDF, preview |
| `Isapur-Poster/_build/` | `render.py`, `fix_round3.py`, `grid_3x2.py`, `add_expressway_stat.py` and earlier fixers |
| `docs/` | GitHub Pages site (7 pages). Live: https://tanmaychachra.github.io/iip-brand-kit/ . Repo: github.com/TanmayChachra/iip-brand-kit (public). |
| `docs/downloads/IIP-Brand-Kit-editable.zip` | Download of the whole kit |
| `work/` | Older generators, mockups, moodboards, prompts (`work/gen/p-*.txt`) |
| `References/` | `competitors/`, `final-thread/` (owner's ChatGPT kit images), `inspiration-ads/`, `inspiration-ads2/`, `iterations-chatgpt/` |
| `Archive/00_Brand_Kit_Project/` | Earlier local-only research and photo moodboards (Stage 01, 2 Nov 2026) |

Git state (2026-11-06): `Isapur-Poster/` committed locally (6a15046, f19c20f), NOT pushed. Root README.md and .gitignore have uncommitted owner or other-session edits.

## 9. Research index with source URLs
Brand kit anatomy and process:
- https://www.gov.uk/government/publications/govuk-brand-guidelines
- https://www.euda.europa.eu/drugs-library/euda-visual-identity-manual_en
- https://www.4over4.com/content-hub/stories/brand-guidelines-checklist
- https://brandkit.com/asset-page/830375-what-should-you-include-in-brand-guidelines
- https://www.canny-creative.com/blog/branding-process-successful-business-branding/
- https://justcreative.com/brand-strategy-design-process/

Industrial park identity examples:
- https://saentys.com/work/veellage/
- https://bewonder.co.uk/our-work/fareham-industrial-park/
- https://idsignsystems.com/capabilities/industrial-park-wayfinding/
- https://www.hughespr.com.au/case-studies/139/crosspoint-brand-launch/

Rooted Indian brands:
- https://www.nrn.com/fast-casual/mcdonald-s-lessons-learned-from-india
- https://yourstory.com/2025/02/bata-global-local-brand-strategy
- https://in.fashionnetwork.com/news/Bata-introduces-new-red-store-concept-for-India,973632.html
- https://startuptalky.com/boat-case-study/
- https://www.afaqs.com/casestudies/the-boat-case-study-tapping-youth-culture-in-indias-audio-market-11068745
- https://archives.digitaltoday.in/businesstoday/20011125/feature1.html

Location and map:
- https://www.google.com/maps/place/Yusufpur+Isapur,+Uttar+Pradesh+201022
- https://en.wikipedia.org/wiki/Modinagar
- https://www.arcgis.com/home/item.html?id=10df2279f9684e4a9f6a7f08febac2a9 (Esri World Imagery)
- OpenStreetMap Overpass (expressway geometry), no single URL saved.

Amenity and wording research (2026-11-06):
- NGT order on Dhaulana, Hapur: https://indiaenvironmentportal.org.in/in-court/order-of-the-national-green-tribunal-regarding-water-pollution-caused-by-cloth-and-printing-industry-dhaulana-district-hapur-uttar-pradesh-26042019
- New Hapur Industrial Pledge Park (drains and STP example): https://msme1connect.up.gov.in/Home/pledgeparkdetails?id=5
- UPSIDA Amausi revamp: https://www.constructionworld.in/policy-updates-and-economic-news/upsida-invests-rs-310-million-to-revamp-amausi-industrial-area/77851
- UPSIDA Sandila upgrade: https://www.constructionworld.in/policy-updates-and-economic-news/up-govt-invests-rs-1.05-billion-in-sandila-industrial-upgrade/77846
- UPSIDA CEO inspection: https://dailypioneer.com/news/upsida-ceo-inspects-ex-lida-sarojini-nagar-industrial-areas
- NGT report on Modinagar sewage treatment (OA 859 of 2022): https://www.greentribunal.gov.in/sites/default/files/news_updates/REPORT%20BY%20CS,%20UP%20IN%20OA%20NO.%20859%20of%202022%20Abhisht%20Kusum%20Gupta%20VS%20State%20of%20Uttar%20Pradesh%20&Ors.pdf

Design rules learned: seven words or fewer on a board, letter height 1 in per 10 to 30 ft of viewing distance, put the most recognisable assets first, define each value once, test at full size from the approach lane.

## 10. Tool and process log
| Date | What | Tool | Output |
|---|---|---|---|
| 2026-11-02 | Brief, research, 8 moodboard routes, Quiet and Ink kits | Claude, ChatGPT via Codex CLI (`work/gen/cx.ps1`) | `docs/`, `work/mood/` |
| 2026-11-02 | Blank hoarding and gate scenes | Codex CLI image generation, owner's ChatGPT login, prompts `work/gen/p-scene-*.txt` | `work/gen/scene-*.png` |
| 2026-11-02 | Satellite map | Esri World Imagery tiles (`work/maps.py`, `work/annot.py`) | `docs/assets/map-isapur.webp` |
| 2026-11-02 | Colour distance (CIEDE2000, k-means) | scipy, scikit-image (`work/analysis.py`) | `work/analysis.json` |
| 2026-11-03 | Mockups: perspective warp of exact artwork | OpenCV, Pillow (`work/mock*.py`, `work/warp.py`) | `docs/assets/*` |
| 2026-11-04 | Final kit rebuilt as editable assets driven by tokens | Python generators, fontTools, uharfbuzz, Playwright, vtracer | `Brand-Kit/` |
| 2026-11-05 | Site published, hoarding beside competitors | GitHub Pages from `/docs` | Live URL above. Large pushes needed `http.postBuffer` 524288000. |
| 2026-11-06 | Poster recreated as editable SVG, halo as one continuous 22-point star, new icons, labels, 3x2 grid | Python, Playwright render | `Isapur-Poster/` |
| 2026-11-06 | Distance and drainage wording research | Claude web search, OpenStreetMap, haversine | section 2, 3 |

Known tool failures: Codex "command too long" (error 206) when base64 pasted, eight parallel Codex jobs wrote duplicate images (sequential works), OSRM driving route unreliable, PowerShell `Set-Content` corrupts Hindi (use UTF-8 explicitly), duplicate SVG attributes break strict editors.
Mockup prompt rules: use real photo as lighting reference, ask for an unedited phone photo with neutral hazy light, forbid golden hour, glow, HDR, bokeh, vignette, ask for blank matte white panel and place exact artwork yourself.
Delegation rule: lowest-limit model (Claude) does decisions, edits, verification and git; image generation and bulk jobs go to browser ChatGPT, local GPU tools, or free models. Document every run.

## 11. Open questions for owner
1. Original vector logo: does the designer have one? (Current badge is a trace.)
2. Exact legal meaning of "Section 80" and the document to match the wording; Zila Panchayat map number and date.
3. Driven distances: gate to Bhojpur exit, to Delhi-Meerut Expressway, to Modinagar, to Hapur.
4. Naala behind the park: photo, plan, pollution-board consent for industrial discharge.
5. Confirm 100+ acres, 50 ft RCC roads, plot size from 300 sq.yards, power supply and street lights as built.
6. Is "Shri Hari Das" connected to IIP or only a competitor? Registered legal name.
7. Phase 1 and Phase 2: what is in each, what is sold now.
8. Real site photos to replace the AI warehouse image.
9. Printer: exact flex size, bleed, and a physical colour proof of yellow, red and green.
10. Confirm Mahamaya details (location, board look).
11. Social media and website names and handles (next phase).
12. Audience priority beyond local factory owners.
13. Should `Isapur-Poster/` be pushed to the public repo?

## 12. Change log (append only)
- 2026-11-06: File created from project READMEs, tokens, work scripts, docs pages, archived research and decisions of this conversation. Nothing invented; unknowns marked UNKNOWN.
- 2026-11-06: Tagline made adaptive (two approved lines). New assets: dark green emblem trace, 6 extra icons, 4 social templates, brand kit page `Brand-Kit/site/`. Orchestrator skill updated with the ArtCraft family (on demand only).
- 2026-11-06: Folders reorganised. Old `work/` moved to `Archive/work-v1/`, old site to `Archive/docs-site-v1/`, PROCESS.md to `Archive/PROCESS-v1.md`. New site in `docs/` (index.html brand kit, brief.html brand brief). Brand book PDF `docs/assets/files/ISAPUR-Brand-Book.pdf`, brief PDF `ISAPUR-Brand-Brief.pdf`. Rebuild with `Brand-Kit/_build/publish.py`. Not pushed to GitHub yet.
- 2026-11-06 (round 6): Owner feedback applied page by page. Decisions: story approved, developer never revealed; horizontal logo = badge, rule, ISAPUR over INDUSTRIAL PARK (from the owner's image); deep green badge is a monotone variant only; clear space and minimum size guides redrawn accurately; tagline cased "The Groundwork for Growth."; icons redrawn in the park-claims style; ring and pattern rebuilt; old signage, stationery and AI mockups dropped and redone; imagery section is a shoot plan only (no imagery yet); content pillars later with ChatGPT help; hashtags via an Apify actor (key from owner, open todo); presence build is next phase; motion parked; AI-driven assets are phase 3 in `AI-Assets/`; kit keeps a distinctive human-crafted character; driving distances measured on Google Maps; project docs (CLAUDE.md, TODOS.md, CHANGELOG.md) added, modelled on gstack document-release.
- 2026-11-06 (round 7, built while the owner was away): rebuilt kit v1.1 and brand book per page-by-page feedback. Wide-roads icon restored and 2.4 stroke on all icons (owner request). Signage and stationery redesigned, 6 context mockups (`Brand-Kit/reference/mockups/ctx-*.webp`, pole boards on the owner's real photos, others on AI blank scenes). Master file `Brand-Kit/IIP-master-assets.svg` holds the brand book artboards and all assets. Print colours from ICC conversion in `Brand-Kit/research/print-colors.json`. Old kit moved to `Archive/kit-v1-*`. Nothing pushed to GitHub after round 5; the live site still shows v1.0.
- 2026-11-07: signage taglines set in SemiBold, smaller than the wordmark (hierarchy fix); tri-colour line added to the poster bottom; stripes bleed edge to edge; old clear-space-guide removed.
- 2026-11-07: CTA wording set to "Industrial Plots Available" across poster, kit tokens, post, badge; footer strip exported as separate file.
- 2026-11-07: poster declared FINAL by owner (CTA pill, thin tri-colour flag). Wording "4 km away" still to be decided vs 4.7 km driving.
- 2026-11-08: phase 2 (visibility) started. Folder layout is now numbered workstreams (01_Brand, 02_Website, 03_SEO, 04_Analytics, 05_Local-Presence, 06_Content, _ops). This file stays at the root. Decision pending owner review: website on Astro, hosted on Cloudflare Pages (research in 03_SEO/research/stack/findings.md). Kit v1.1 and the poster are the locked main brand kit.
- 2026-11-08 owner answers (phase 2): (1) Second phone is 9837764222 for now, to be swapped for 9219549800 later (one swap point per system: kit tokens content.json, website phones.mjs). (2) Price: "Contact for price"; plots start from 300 sq yards. (3) Approvals: left open, owner to ask family; no approval claim published until documents are on file. Owner-stated sales answer (not yet proven): maps are passed by the Zilla Panchayat. (4) Neighbours: owner says an INOX Air plant is next to the park and Namaste India is a few km away; INOX Air Modinagar plant VERIFIED by press release, distance to the park not yet measured, Namaste India only reported; Amul and Patanjali unverified. Atom brochure PDF not found yet. (5) Phase 1, 2 and 3 are independent units and stay as separate Google profiles (Phase 1 is primary). Phase 1 and 2 are resale, a few own plots in Phase 3. The website does not mention phases or resale. (6) Sales hours: 8 am to 8 pm every day except Tuesday. (7) Budget: DataForSEO about 5K per month, no Google or Meta ads planned for now. (8) Hindi or Hinglish pages are welcome later. (9) No site photos yet. (10) OpenSEO host and Google account for GTM, GA4, Search Console come later (owner, by evening 2026-11-08). (11) Domain: owner will buy, research in 02_Website/domain-email.md.
- 2026-11-09: global MCPs added at user scope (cloudflare-api, astro-docs, openseo). Owner's OpenSEO is already hosted on Cloudflare at openseo.tanmay-hq.in behind Access, MCP waits for Managed OAuth. Owner will supply plotting maps for Phase 1, 2, 3 and Phase 1 extension and a Google Earth project (KML) for SVG plot maps in 01_Brand/Plot-Maps (reusable asset, future plot selector). On-ground photos within about a week, 360 degree traversal in 3 to 4 months (Insta360), A/B testing program starts once the draft site is live.
- 2026-11-09: tech record created at _ops/TECH-STACK.md. Cloudflare, OpenSEO and DataForSEO MCPs connected and verified via Claude Desktop connectors; DataForSEO balance 1 USD, no funds yet. Never delete the project MCPs listed there.

- 2026-11-12: Owner facts. Architect layouts (not the sanctioned ones) are the source for plot maps. Phase 1 PDF includes the Phase 1 extension (topmost section). IIP (the owner) owns Phase 1 and Phase 2, Phase 3 follows in a day or two. Minimum plot size is 300 sq yd, larger sizes vary (owner statement, not in the approvals). Photos: wait for real ones, a few may be taken from the Google profile listing but need optimising (real photos only, edited or enhanced, never AI scenes passed off as the park). Approvals read: see 06_Content/approvals-facts.md.

- 2026-11-12 correction: IIP owns Phase 3 too. Only the Google Business Profile transfer from the old manager to the business Gmail is pending. Include Phase 3 in site claims and maps.

- 2026-11-12: Phones changed by the owner. Call number 92195 49800 first, 98377 64222 second and the WhatsApp number. 98370 57800 retired everywhere (site, copy, NAP file updated; Google profile and listings still to change). Reference sites the owner likes: vipcutlery.com, rajasthansweets.in, reliablevacation.com (logo rises as sun, living-room wall scroll concept, footer), healixhealthcare.ae (unique palette, hands joining). v3 aesthetic: creative and meaningful, SEO kept safe.

- 2026-11-12: Very small plots are commercial shops, keep them on the maps (type shop). OpenSEO MCP reconnected (new connector id, tools work, project Isapur Industrial Park still has domain isapurindustrialpark.in, the primary domain is now isapurindustrialpark.com).

- 2026-11-12 owner decisions (final, no questions): (1) Claims STAY on the site: 50 ft RCC roads, street lighting installed, greenery planted, plots from 300 sq yd; photos to follow as proof later. (2) Max plot size in Isapur is 2000 to 2500 sq yd. (3) Primary contact and WhatsApp: 98377 64222. Secondary 92195 49800 is HELD OFF the site, schema and copy until about 2026-11-19, owner will say when to add it. 98370 57800 retired. (4) Font: Erode (Fontshare, free commercial licence) approved for headings, download into the project. (5) V3-DIRECTION concepts rejected as non-original and too technical: owner wants an ORIGINAL idea built from IIP context, borrowing only the non-conceptual changes (navbar mark, calmer hero scale, address block, facts layout, zoomed-out map). v3 scope: HOME PAGE ONLY until approved.

- 2026-11-12: Erode (Fontshare, Indian Type Foundry, free commercial licence) is now the brand display typeface for headlines, banners and signage. Montserrat stays only in the logo wordmark and old artwork. Inter stays for text. Tokens updated (01_Brand/Brand-Kit/tokens/brand.tokens.json), file in Brand-Kit/fonts. Brand kit page and brand book not rebuilt yet. Owner feedback on v3 home: concept far better, design language drifted from the brand, shutter not premium, wants 8 to 10 sections, motion design, original concept thinking (scroll story: a factory shed builds itself on the plot, tagline The Groundwork for Growth). Petrol pump copy: at the entry and exit, light boast, no straight-line wording.

- 2026-11-12 owner facts: payment about 3 months on average (negotiable later, say average only if used); power 24/7; say NOTHING about water, security, permitted uses or price policy (offline sales). 

- 2026-11-12 owner facts (buying and neighbours): ALL plots are sold, IIP works on a RESALE basis, shows available inventory, mediates, payments flow through IIP, registry after about 3 months, IIP will resell the land if the owner needs. Buyers: factories, warehouses, godowns, investors. Running units (no brand names): tile-bonding chemicals, comfort cushions, industrial water tanks, PVC pipes. Shops: all commercial, free use (confectionery, quick food, tyre repair at Phase 2 entry). Power: government lines from both Modinagar and Hapur sides, 24/7. Security (gate, 12 hour night guard) known but NOT for the site. Satellite view: owner supplies own Google Earth screenshots and KML, never scrape imagery. Remove old website images from the board.

- 2026-11-12 context only (do NOT mark or label on any map or page): the whole E sector in the Phase 1 layout is the Phase 1 extension.

- 2026-11-13: v3 home design language LOCKED by the owner (see 02_Website/DESIGN-LANGUAGE.md). Illustrations are architect style ink drawings, the shed build is scroll scrubbed beside six text steps, the visit shutter lift is scrubbed, hero map zoom 3x faster with plus, minus, reset and double tap. Hedging disclaimers removed from the page; all changed lines listed in 02_Website/V3-HOME.md for the copywriter.

- 2026-11-13 owner: the "no AI imagery" rule drops once the photographic direction is finalised. Open task photodirection (TODOS.md, board). Blender film route: research a lot, use open-source helpers and learn from existing work (RESEARCH-BLENDER.md).

- 2026-11-13: Owner supplied Google Earth boundaries of the three phases (Sites.kml, not 100 percent accurate). Cleaned copy with only the 3 phase polygons: 01_Brand/Plot-Maps/data/phase-boundaries.geojson (other placemarks in the KML are personal, never copied or used). Use for real placement of phases on the hero map, the where map and the 3D film.

- 2026-11-13 owner feedback: print update of hoardings and pole signs (CTA block) rejected as unprofessional and childish; redo before the kit goes online. Owner loves the ink-drawing illustration style and the short yellow line bullet: add both to the brand kit. Kit publish blocked until the CTA redo is approved.
- 2026-11-14: Website live at https://isapurindustrialpark.com (Cloudflare Pages iip-site). Home Lighthouse mobile 87 to 89 (other pages 96 to 98), CLS 0. Core analytics: Cloudflare Web Analytics (owner enables the toggle in Pages), GA4 after consent, Clarity later through GTM after consent. Open: print CTA redo, kit additions, Business Profile edits, AI search (GEO) research after the weekly reset.

- 2026-11-14 owner: do NOT say on the site, in print or in marketing that cash or payments flow through IIP or that our name is attached to every sale and buy. Remove everywhere. The help-you-sell-later line stays unless the owner says otherwise.
- 2026-11-14 owner decision (approval wording): no document proves the original Phase 1 layout. The site claims approval for PHASES 2 AND 3 ONLY, worded "Approved by Zila Panchayat Ghaziabad" (badge: "Approved by Zila Panchayat"). No "map", "layout map", "stamped map", "sanctioned" or "subject to conditions" in approval lines. No claim about Phase 1 or the Phase 1 extension. Site-v2 content reworked to match (see 06_Content/approvals-facts.md top note).

- 2026-11-14 owner: 92195 49800 is now USED, only for renting and leasing (call number on the rent section, the rent page and rent FAQ). WhatsApp stays 98377 64222 everywhere. All other pages, print and listings keep 98377 64222 only.
- 2026-11-14 owner decision (replaces the Phases 2 and 3 line above): the claim is "Approved by Zila Panchayat Ghaziabad" for all three phases on the owner's word, no phase scoping, no map, sanction numbers or dates. Phase 1 original approval document still to be found and filed (TODO owner). Rent and lease facts from the owner's father: plots plus sheds and factories for rent or lease, a factory on a 100 sq yard plot is for rent now, no amounts or terms. New page industrial-shed-for-rent, brief 03_SEO/content-briefs/rent-lease.md.

- 2026-11-14 owner APPROVED the staging and production workflow (work on staging, show the staging link, promote only on the owner typing GO LIVE) and approved both optional extras: Cloudflare Access lock on staging (owner email only) and GitHub protection of main. GitHub protection of main set 2026-11-14: no force pushes, no deletion, linear history, admins not enforced. Access lock on staging pending (applied after the running staging helper finishes, because it changes how smoke tests reach staging).
