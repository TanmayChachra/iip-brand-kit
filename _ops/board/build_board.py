"""Builds docs/board/index.html (phase 2 visual board) from _ops/status.json plus the content below.
Run: python _ops/board/build_board.py   Output is public (GitHub Pages): keep secrets, phone lists beyond the brand numbers and private owner data out."""
import json, html, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "docs/board"; OUT.mkdir(parents=True, exist_ok=True)
S = json.loads((ROOT / "_ops/status.json").read_text(encoding="utf-8"))
GH = "https://github.com/TanmayChachra/iip-brand-kit/blob/main/"
e = html.escape


def a(path, label=None): return f'<a href="{GH}{path}" target="_blank" rel="noopener">{e(label or path)}</a>'


FINDINGS = [
    ("Competitors", "Only CKS and Shree Haridas (SHD) have real sites. CKS is the one to beat: schema, FAQ, geo pages, llms.txt, 5.0 stars on 40 reviews. SHD has a price-only H1, leftover apartment copy and no schema. Nobody has video, and nobody mentions the petrol pump.", "03_SEO/competitors/findings.md"),
    ("Our Google profile", "Three separate profiles (Phase 1: 4.5 stars, 11 reviews, 27 photos; Phase 2: 5.0, 3; Phase 3: none) plus 2 unclaimed duplicate pins. No website, description or services on any. Phase 1 ranks 4th for 'industrial park Modinagar' and is absent for 'industrial plots in Modinagar'.", "05_Local-Presence/gmb/audit.md"),
    ("Stack", "Astro, static pages, Cloudflare Pages (free, commercial use allowed), Markdown content, Keystatic CMS later. GitHub Pages terms bar business hosting, so it stays for our boards only. Budget: LCP 1.8 s, JS under 60 KB, first load under 500 KB.", "03_SEO/research/stack/findings.md"),
    ("Clean slate", "A search for 'Isapur Industrial Park' returns nothing of ours. Own the place names (Isapur, Bhojpur, Modinagar-Hapur Road) first, then the generic plot keywords where portals dominate.", "03_SEO/competitors/serp-notes.md"),
    ("AEO and GEO", "Google says no special files or schema are needed for AI Overviews. llms.txt shows no citation effect in the studies we found: cheap, but not a tactic. What works: allow AI search bots, Bing Webmaster and IndexNow, answer-first FAQs, consistent name, address and phone, a monthly prompt audit.", "03_SEO/aeo-geo/aeo-geo-plan.md"),
    ("Partner brands", "We could not find a source placing Amul, Inox Air or Patanjali in Modinagar or on the expressway. A competitor mentions only an 'Inox oxygen centre'. We name a brand only after you confirm it and give permission.", "03_SEO/backlinks/backlinks.md"),
]

FIRST = [
    ("Week 1 to 2", "Fix the Google profile (one main profile, categories, description, services, phone numbers, website link). Create GA4, GTM, Search Console. Collect your data (questions below). Start review requests."),
    ("Day 15 to 45", "Launch the core pages and proof pages. Submit the sitemap. Distance table. Consistent profiles on Bing, Apple, Facebook, LinkedIn, YouTube and the free listing sites. First site video."),
    ("Day 46 to 75", "Neighbour brand pages (with permission), first local link asks, tests T1 (CTA wording) and T2 (call vs WhatsApp), first AI visibility check, first dashboard."),
    ("Day 76 to 90", "Read what Search Console shows, double down on the two best pages, start careful location pages, decide what to drop."),
]

OLD_QUESTIONS = [
    "Domain: which name do you want (for example isapurindustrialpark.com or .in), and will you buy it? Same for the email address.",
    "Plot sizes you sell, and the price approach: show a starting price, show ranges, or 'contact for price'? (SHD shows a price, CKS does not.)",
    "Approvals: which documents can we publish (Zilla Panchayat map approval, Section 80, UPSIDA or pledge park status)? We publish no approval claim without a document.",
    "Neighbour brands: which of Amul, Inox Air, Patanjali (and others) are really in or beside the park, and may we name them and use their logos?",
    "Petrol pump at the park exit: brand, operator, distance from the gate, open 24 hours, trucks allowed, a photo.",
    "Google profile: which Google account owns Phase 1, Phase 2 and Phase 3, which one is the main office, and is 9837764222 your number? Are the two 'Building' pins on Isapur-Kharkoda Road real gates?",
    "Competitor Shivansh: which listing is it (nearby look-alikes exist)? Any other park you watch?",
    "Sales truth: the 20 questions callers ask most, the objections, how many calls and site visits per week now, and which number is on WhatsApp.",
    "Photos and video: date of the site shoot (gate, road, lights, trees, plots, petrol pump, drone).",
    "Budget limits: DataForSEO spend cap per month for OpenSEO, and whether Google or Meta ads are planned (decides the consent setup).",
    "OpenSEO: the host URL and when the MCP will be connected. Google account for GTM, GA4 and Search Console.",
    "Phases: which of Phase 1, 2 and 3 are on sale and what we may say about each.",
    "Languages: the site stays English. Do you want Hindi or Hinglish pages later, since many local searches are in Hindi?",
    "Sales office hours and visit booking rules (Phase 3 shows 24 hours, which looks wrong).",
]

TOOLS = [
    ("OpenSEO (every-app/open-seo)", "Install now", "One MCP for keywords, rank tracking, competitors, backlinks, audits, AI visibility, local map grid, GSC and GA4. You host it, you set a DataForSEO spend cap.", "https://github.com/every-app/open-seo"),
    ("Astro Docs MCP", "Install now", "Official Astro docs search while we build.", "https://docs.astro.build/en/guides/build-with-ai/"),
    ("Google Analytics MCP (official)", "After launch", "Ask Claude about GA4 reports, read only.", "https://github.com/googleanalytics/google-analytics-mcp"),
    ("Search Console MCP", "After launch", "Queries, clicks, indexing, sitemaps.", "https://github.com/AminForou/mcp-gsc"),
    ("Tag Manager MCP", "After launch", "Edit GTM from chat. You approve every write.", "https://github.com/stape-io/google-tag-manager-mcp-server"),
    ("Cloudflare MCP", "After launch", "Pages and DNS from chat. Approval needed for DNS.", "https://github.com/cloudflare/mcp-server-cloudflare"),
    ("Playwright MCP", "Later", "Test forms and tracking events. Heavy on RAM.", "https://github.com/microsoft/playwright-mcp"),
    ("Skip", "Skip", "Ahrefs (local repo archived, paid), Semrush (paid), Brave, Perplexity and Exa (duplicates), community Google Business Profile MCPs (tiny, unproven), GitHub MCP (gh CLI works).", ""),
]
SKILLS = [
    ("OpenSEO agent skills", "Now", "Pre-built SEO workflows on the OpenSEO MCP", "https://openseo.so/docs/skills/setup"),
    ("coreyhaines31/marketingskills", "Now (pick about 12)", "seo-audit, schema, site-architecture, ai-seo, directory-submissions, conversion-tracking, ab-testing, cro, copywriting", "https://github.com/coreyhaines31/marketingskills"),
    ("AgriciDaniel/claude-seo (core only)", "Now", "seo-technical, seo-schema, seo-sitemap, seo-local. Skip its extension installers that use curl | bash", "https://github.com/AgriciDaniel/claude-seo"),
    ("jdevalk/skills", "While building", "astro-seo, static-seo, metadata-check", "https://github.com/jdevalk/skills"),
    ("onvoyage-ai/gtm-engineer-skills", "After launch", "audit-website-aeo, improve-aeo-geo", "https://github.com/onvoyage-ai/gtm-engineer-skills"),
]
LISTINGS = [
    ("Google Business Profile", "https://business.google.com/create"), ("Bing Places", "https://www.bingplaces.com/"), ("Apple Business Connect", "https://businessconnect.apple.com/"),
    ("Facebook Page", "https://www.facebook.com/pages/create"), ("LinkedIn company page", "https://www.linkedin.com/company/setup/new/"), ("YouTube channel", "https://www.youtube.com/create_channel"),
    ("WhatsApp Business", "https://business.whatsapp.com/products/business-app"), ("Justdial free listing", "https://www.justdial.com/Free-Listing"), ("IndiaMART", "https://seller.indiamart.com/"),
    ("TradeIndia", "https://www.tradeindia.com/"), ("99acres", "https://www.99acres.com/"), ("MagicBricks", "https://www.magicbricks.com/"), ("Housing.com", "https://housing.com/"),
    ("OpenStreetMap", "https://www.openstreetmap.org/"), ("Foursquare", "https://foursquare.com/add-place"),
]
TESTS = [("T1", "CTA wording: 'Call now' vs 'Book a site visit'"), ("T2", "Sticky bar: call only vs WhatsApp and call"), ("T3", "Hero: image first vs proof first (only with documents on file)"), ("T4", "Form length: 2 fields vs 5 fields")]
DOCS = [("Competitor findings", "03_SEO/competitors/findings.md"), ("Stack decision", "03_SEO/research/stack/findings.md"), ("Top SEO strategies (23 tactics)", "03_SEO/playbook/top-seo-strategies.md"),
        ("Data to collect", "03_SEO/playbook/data-to-collect.md"), ("A/B tests", "03_SEO/playbook/ab-tests.md"), ("Backlink ideas", "03_SEO/backlinks/backlinks.md"), ("AEO and GEO plan", "03_SEO/aeo-geo/aeo-geo-plan.md"),
        ("MCP shortlist", "03_SEO/research/tooling/mcp-servers.md"), ("Claude skills shortlist", "03_SEO/research/tooling/claude-skills.md"), ("Google profile audit", "05_Local-Presence/gmb/audit.md"),
        ("Listing targets (48)", "05_Local-Presence/citations/citations-targets.md"), ("GTM and GA4 plan", "04_Analytics/gtm-plan.md"), ("Event spec", "04_Analytics/event-spec.md"), ("AI entry points", "_ops/AGENTS.md")]

STATE_CLASS = {"built (local)": "ok", "copy done": "ok", "locked": "ok", "live": "ok", "research done": "ok", "audit done": "ok", "spec written": "ok", "planned": "wait", "waiting": "wait"}


FINDINGS = [f for f in FINDINGS if f[0] != "Partner brands"] + [
    ("Neighbours (checked on Google Maps)", "INOX Air Products plant about 0.6 km from Phase 1 and Namaste India plant about 0.7 km (straight-line), both verified. IndianOil pump (Captain Filling Station) is about 190 m from Phase 1 and 60 m from Phase 2, open 6 am to 10 pm, not 24 hours. Amul has no plant or depot near us, Patanjali only shops: both stay off the site. The Atom brochure PDF could not be found.", "05_Local-Presence/neighbours/maps-findings.md"),
    ("Domain and email", "Best pick: isapurindustrialpark.in (also unregistered: .com, protect it with a redirect). Backups isapurindustrial.in and isapurpark.in. All 116 names checked were free. Hostinger India lists .in at about Rs 899 a year. Email: start free with Zoho Mail Forever Free (webmail), fallback Cloudflare Email Routing.", "02_Website/domain-email.md"),
    ("Two unclaimed Google pins", "Both 'Building' pins sit at one spot on open farmland about 240 m from the Phase 3 pin, no gate or building visible. They look like junk duplicates. Best handled by a suggest-an-edit report, not a claim.", "05_Local-Presence/neighbours/building-pins.md"),
]
DONE = [
    "Website built (Astro, 17 pages, colourful, mobile first): Lighthouse mobile 98 to 100 on quiet runs, about 160 KB per page, SEO 100.",
    "Keyword map for every page plus 44 backlog keywords, and written copy for all pages, 22 FAQ answers and 2 blog posts.",
    "Fresh vector assets in brand style: hero scene, plot layout, location diagram, spot art, OG images, favicons.",
    "Neighbours page live in the build from verified Maps data (text only, no logos). Contact for price. Hours 8 am to 8 pm except Tuesday.",
    "Phone numbers behind one swap point (second number 9837764222 now, 9219549800 later). Brand kit rebuilt with it.",
    "32 Claude skills installed (marketingskills 12, claude-seo core 5, jdevalk 3, OpenSEO 12). They load from the next session.",
    "Sales questions list in Hinglish and English with safe draft answers. Domain and email research. Google profile fix list ready.",
]
STILL = [
    "Approvals: documents for Zilla Panchayat and Section 80 (until then no approval claim is public).",
    "Domain: buy isapurindustrialpark.in (and the .com), then I set up Cloudflare Pages, Search Console and Zoho or routing mail.",
    "OpenSEO host URL and the Google account for GTM, GA4 and Search Console (you said tonight).",
    "Real photos and video of the park, petrol pump and plots.",
    "Real caller questions and objections from your dad, to replace the guessed list.",
    "Which number is on WhatsApp (the site assumes 9837057800).",
    "Approve the Google profile edits (description, services, categories). The safety check blocked me from editing your profile, so I left the paste-ready text in the audit.",
    "Plot sizes beyond 300 sq yards, payment plan, power and drainage facts (these stay off the site until confirmed).",
]


def task_card(t):
    def lk(l, u):
        href = u if u.startswith("http") else GH + u
        return f'<a href="{href}" target="_blank" rel="noopener">{e(l)}</a>'
    steps = "".join(f"<li>{e(x)}</li>" for x in t["steps"])
    links = " ".join(lk(l, u) for l, u in t["links"])
    st = t["state"]
    return (f'<article class="card task"><span class="pill {"ok" if st == "done" else "wait"}">{e(st)}</span><span class="note"> {e(t["time"])}</span>'
            f'<h3>{e(t["title"])}</h3><p>{e(t["why"])}</p><ol>{steps}</ol><p class="more"><b>Unlocks:</b> {e(t["unlocks"])}</p><p class="more">{links}</p></article>')


OWNER = "".join(task_card(t) for t in S.get("owner_tasks", []))


def cards(rows):
    return "".join(f'<article class="card"><h3>{e(t)}</h3><p>{e(b)}</p><p class="more">{a(p, "Read the full note")}</p></article>' for t, b, p in rows)


ws = "".join(f'<article class="card ws"><span class="pill {STATE_CLASS.get(w["state"], "wait")}">{e(w["state"])}</span><h3>{e(w["id"])}</h3><p>{e(w["summary"])}</p><p class="next"><b>Next:</b> {e(w["next"])}</p></article>' for w in S["workstreams"])
def link(u): return f'<a href="{u}" target="_blank" rel="noopener">link</a>' if u else ""


tools = "".join(f'<tr><td><b>{e(n)}</b></td><td><span class="pill {"ok" if "now" in w.lower() else "wait"}">{e(w)}</span></td><td>{e(d)}</td><td>{link(u)}</td></tr>' for n, w, d, u in TOOLS)
skills = "".join(f'<tr><td><b>{e(n)}</b></td><td><span class="pill ok">{e(w)}</span></td><td>{e(d)}</td><td><a href="{u}" target="_blank" rel="noopener">link</a></td></tr>' for n, w, d, u in SKILLS)
first = "".join(f'<li><b>{e(t)}</b><span>{e(b)}</span></li>' for t, b in FIRST)
qs = "".join(f"<li>{e(q)}</li>" for q in STILL)
done = "".join(f"<li>{e(d)}</li>" for d in DONE)
lst = "".join(f'<a class="chip" href="{u}" target="_blank" rel="noopener">{e(n)}</a>' for n, u in LISTINGS)
tst = "".join(f"<li><b>{e(i)}</b> {e(t)}</li>" for i, t in TESTS)
docs = "".join(f'<li>{a(p, t)}</li>' for t, p in DOCS)

PAGE = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>IIP Phase 2 Board</title>
<style>:root{{--bg:#F6F3EC;--card:#FFFDF8;--ink:#111827;--mut:#5b6472;--line:#e2dccd;--green:#0F4D3A;--yel:#FFD600;--red:#E53935}}
@media(prefers-color-scheme:dark){{:root{{--bg:#0f1512;--card:#18211c;--ink:#f1ece0;--mut:#a9b3ad;--line:#2a362f}}}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:16px/1.55 Inter,system-ui,sans-serif}}main{{max-width:1180px;margin:0 auto;padding:28px 16px 80px}}
.flag{{height:6px;background:linear-gradient(90deg,var(--yel) 0 33%,var(--red) 33% 66%,var(--green) 66%);border-radius:3px;margin-bottom:22px}}
h1{{font-size:clamp(28px,4.4vw,46px);margin:0 0 6px;letter-spacing:-.02em}}h2{{margin:44px 0 12px;font-size:24px}}h3{{margin:6px 0 6px;font-size:17px}}p{{margin:6px 0}}.lead{{color:var(--mut);max-width:72ch}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));gap:16px}}.card{{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px 16px}}
.more,.next{{font-size:14px;color:var(--mut)}}.pill{{display:inline-block;font-size:12px;padding:2px 10px;border-radius:99px;border:1px solid var(--line);text-transform:uppercase;letter-spacing:.04em}}
.pill.ok{{background:rgba(15,77,58,.14);color:var(--green)}}@media(prefers-color-scheme:dark){{.pill.ok{{color:#7fd1b0}}}}.pill.wait{{background:rgba(255,214,0,.25)}}
ol.steps{{list-style:none;padding:0;display:grid;gap:12px}}ol.steps li{{background:var(--card);border:1px solid var(--line);border-left:6px solid var(--yel);border-radius:12px;padding:12px 16px}}ol.steps b{{display:block}}ol.steps span{{color:var(--mut)}}
table{{width:100%;border-collapse:collapse;background:var(--card);border:1px solid var(--line);border-radius:12px;overflow:hidden;font-size:15px}}td{{padding:10px 12px;border-bottom:1px solid var(--line);vertical-align:top}}tr:last-child td{{border-bottom:0}}
.wrap{{overflow-x:auto}}.chips{{display:flex;flex-wrap:wrap;gap:8px}}.chip{{border:1px solid var(--line);background:var(--card);border-radius:99px;padding:6px 14px;text-decoration:none;color:inherit;font-size:14px}}.chip:hover{{border-color:var(--green)}}
ul.q li{{margin:8px 0}}a{{color:inherit}}.two{{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:16px}}.note{{font-size:13px;color:var(--mut)}}.shots{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:16px;align-items:start}}.shots figure{{margin:0;background:var(--card);border:1px solid var(--line);border-radius:12px;overflow:hidden}}.shots img{{width:100%;display:block;max-height:640px;object-fit:cover;object-position:top}}.shots figcaption{{padding:8px 12px;font-size:13px;color:var(--mut)}}</style></head><body><main>
<div class="flag"></div><h1>IIP Phase 2: visibility board</h1>
<p class="lead">Website, SEO, local presence, AEO and GEO, analytics. Updated {e(S["updated"])}. Brand kit and poster are locked. Everything below is research and plan, nothing is built or published on the new site yet.</p>
<h2>Workstreams</h2><div class="grid">{ws}</div>
<h2>What the research found</h2><div class="grid">{cards(FINDINGS)}</div>
<h2>Done while you were away</h2><ul>{done}</ul>
<h2>Website preview (screenshots of the local build)</h2><p class="lead">Not published on a domain yet. Colour comes from the brand kit: green, yellow, bone and sage, charcoal only for text. All artwork is illustration, labelled not to scale.</p>
<div class="shots"><figure><img src="site/home-desktop.webp" alt="Home page desktop" loading="lazy"><figcaption>Home, desktop</figcaption></figure><figure class="mob"><img src="site/home-mobile.webp" alt="Home page mobile" loading="lazy"><figcaption>Home, mobile</figcaption></figure><figure><img src="site/location-desktop.webp" alt="Location page" loading="lazy"><figcaption>Location</figcaption></figure><figure><img src="site/neighbours-desktop.webp" alt="Around us page" loading="lazy"><figcaption>Around us</figcaption></figure></div>
<h2>First 90 days</h2><ol class="steps">{first}</ol>
<h2>Your tasks (in order, I tick them when you tell me)</h2><div class="grid">{OWNER}</div><h2>Smaller items</h2><ol class="q">{qs}</ol>
<h2>Free listings to claim first</h2><p class="lead">Exact sign-up pages. Use one identical name, address and phone everywhere. The full list of 48 with link type and notes is in the listing targets note.</p><div class="chips">{lst}</div>
<h2>Tests we will run</h2><ul>{tst}</ul><p class="note">Low traffic means big changes first (details and sample sizes in the A/B note).</p>
<h2>MCP servers that boost the workflow</h2><div class="wrap"><table>{tools}</table></div>
<h2>Claude skills to add (install by name, not whole packs)</h2><div class="wrap"><table>{skills}</table></div>
<h2>All notes</h2><div class="two"><ul>{docs}</ul><div class="card"><h3>How agents work in parallel</h3><p>Each folder has one owner agent and an AGENT.md entry point. Hand-offs happen only through contract files: keyword map, canonical name-address-phone, event spec, page list. A weekly scheduled task writes new SEO findings to <code>03_SEO/watch/</code> and only proposes.</p><p class="more">{a("_ops/AGENTS.md", "Read the rules")}</p></div></div>
<p class="note" style="margin-top:36px">Truth labels in every note: verified (read at the source), reported (third party), guess. Source and competitor facts are as of 2026-11-08.</p></main></body></html>'''
(OUT / "index.html").write_text(PAGE, encoding="utf-8")
print("board", len(PAGE) // 1024, "KB")
