"""Generates citations-targets.csv and citations-targets.md from one list. Run: python _gen_citations.py"""
import csv, pathlib
H = pathlib.Path(__file__).resolve().parent
# priority, platform, group, signup_url, cost, link_type, relevance, asset_needed, notes
R = [
 ("P0","Google Business Profile","Core map","https://business.google.com/create","Free","nofollow (reported)","Highest: local pack and Maps","Photos, category, hours, phone, address pin, website when live","Claim or verify the existing listing first, do not create a duplicate. Primary category: Industrial Park (verify wording in the category list). Details in 05_Local-Presence/gmb/."),
 ("P0","Bing Places for Business","Core map","https://www.bingplaces.com/","Free","nofollow (reported)","High: feeds Bing, Copilot, ChatGPT search and Perplexity (reported)","Same as GBP","Can import from GBP. Do it the day the GBP is clean."),
 ("P0","Apple Business Connect","Core map","https://businessconnect.apple.com/","Free","none","High for iPhone users: Apple Maps and Siri","Logo, photos, hours, pin","Needs a verification call or document. Use the same phone as GBP."),
 ("P0","Facebook Page","Social profile","https://www.facebook.com/pages/create","Free","nofollow (reported)","Medium: entity and sameAs signal, ads later","Logo, cover, about text, phone, address","Page name exactly: Isapur Industrial Park. Add website when live."),
 ("P0","LinkedIn Company Page","Social profile","https://www.linkedin.com/company/setup/new/","Free","nofollow (reported)","High for B2B buyers (factory owners, procurement)","Logo, banner, tagline, about","Needs a personal LinkedIn profile to create. Developer name stays hidden: use the park name only."),
 ("P0","YouTube channel","Social profile","https://www.youtube.com/create_channel","Free","nofollow (reported)","High: video results in Google, AI Overviews cite YouTube often (reported)","Banner, avatar, first drone or walkthrough video","Do not upload AI warehouse clips as if they were the park. Wait for the site shoot."),
 ("P0","WhatsApp Business app","Messaging","https://business.whatsapp.com/products/business-app","Free","none","High: main enquiry channel for local owners","Business profile, catalogue, greeting message","Use the same number as the main phone: 9837057800. Add a click-to-chat link on the site."),
 ("P0","Justdial","India directory","https://www.justdial.com/Free-Listing","Free listing (paid upsell)","unknown, test","High: strong local trust and traffic in India","Phone OTP, address, photos, categories","Expect sales calls. Decline paid packages for now. Verify listing wording."),
 ("P0","IndiaMART","B2B marketplace","https://seller.indiamart.com/","Free basic (paid upsell)","unknown, test","High: factory owners search here","Product: Industrial plots, photos, GST optional","List as a service or product 'Industrial Plots'. Check that real estate is allowed in the category before paying anything."),
 ("P0","TradeIndia","B2B marketplace","https://www.tradeindia.com/","Free basic (paid upsell)","unknown, test","Medium to high: B2B buyers","Company profile, photos","Same NAP. Skip paid membership at the start."),
 ("P0","99acres (developer or owner posting)","Property portal","https://www.99acres.com/","Free basic posting (paid boosts)","unknown, test","High: plot buyers, industrial land filter","Plot sizes, price per sq yard, photos, map","Needs real plot sizes and a price range from the owner. Do not post claims without proof on file."),
 ("P0","MagicBricks","Property portal","https://www.magicbricks.com/","Free basic posting","unknown, test","High","Same as 99acres","Check the commercial or industrial land category."),
 ("P0","Housing.com","Property portal","https://housing.com/","Free basic posting","unknown, test","Medium (more residential)","Same as 99acres","Industrial plots exist on the site but are rare (verified in search results, 2026-11-08)."),
 ("P0","OpenStreetMap","Map data","https://www.openstreetmap.org/","Free","unknown","Medium: feeds many apps and AI datasets","Accurate pin and tags","Needs a free OSM account. Add the park as a landuse=industrial area with name, website, phone tags."),
 ("P0","Foursquare Places","Map data","https://foursquare.com/add-place","Free","unknown","Medium: feeds Apple, Snap and others (reported)","Pin, category, phone","Sync with Apple data pipeline is reported, not verified."),
 ("P1","Sulekha","India directory","https://www.sulekha.com/","Free listing","unknown, test","Medium","Phone OTP, address","Lower priority than Justdial."),
 ("P1","ExportersIndia","B2B marketplace","https://www.exportersindia.com/","Free basic","unknown, test","Medium","Company profile","Mostly export products, weak fit. Do last."),
 ("P1","Yellow Pages India (Yellowpages.in)","India directory","https://www.yellowpages.in/","Free","unknown, test","Low to medium","NAP","Citation only."),
 ("P1","Instagram","Social profile","https://www.instagram.com/accounts/emailsignup/","Free","nofollow (reported)","Medium: brand and reels","Avatar, bio, link","Switch to a professional account. Handle should match the Facebook name."),
 ("P1","X (Twitter)","Social profile","https://x.com/i/flow/signup","Free","nofollow (reported)","Low to medium","Avatar, bio","Mainly for brand name protection and news mentions."),
 ("P1","Pinterest Business","Social profile","https://www.pinterest.com/business/create/","Free","nofollow (reported)","Low to medium: visual search","Brand assets","Use brand textures and infographics later."),
 ("P1","Quikr (Homes)","Classifieds","https://www.quikr.com/homes","Free basic","unknown, test","Medium","Photos, price","Quality of leads is mixed."),
 ("P1","OLX","Classifieds","https://www.olx.in/","Free basic","unknown, test","Low to medium","Photos","Do not spam. One clean ad per plot size."),
 ("P1","RealEstateIndia","Property portal","https://www.realestateindia.com/","Free basic","unknown, test","High: already lists Modinagar, Hapur Road and Sahibabad industrial land (verified in search results, 2026-11-08)","Plot details","Competitor parks are listed there, so presence matters."),
 ("P1","SquareYards","Property portal","https://www.squareyards.com/","Free basic","unknown, test","High: lists industrial plots in Modinagar (verified, listing page updated 2026-01-12)","Plot details","Check if direct developer listing is allowed."),
 ("P1","PropertyWala","Property portal","https://propertywala.com/","Free basic","unknown, test","Medium: has Meerut Road industrial area page (verified)","Plot details","Citation plus leads."),
 ("P1","CommonFloor","Property portal","https://www.commonfloor.com/","Free basic","unknown, test","Low to medium","Plot details","Check if site is still active and indexing."),
 ("P1","NoBroker","Property portal","https://www.nobroker.in/","Free for owners","unknown, test","Low (residential focus)","Plot details","Optional."),
 ("P1","Proptiger","Property portal","https://www.proptiger.com/","Developer onboarding","unknown, test","Low (residential focus)","Project data","Optional, residential first."),
 ("P1","HERE WeGo / Map Creator","Map data","https://wego.here.com/","Free","none","Low to medium: car navigation data","Pin","Suggest a place edit."),
 ("P1","TomTom MapShare","Map data","https://www.tomtom.com/","Free","none","Low to medium: car navigation data","Pin","Report a missing place through the map report tool."),
 ("P1","UP MSME Connect: Pledge Park listing","Government portal","https://msme1connect.up.gov.in/","Unknown (government scheme)","unknown","High if eligible: government portal lists pledge parks with plots and contacts (verified a Hapur park listing exists, 2026-11-08)","UPSIDA or scheme approval papers","Only if the park qualifies under the UP pledge park scheme. Ask the owner. Do not claim approval without proof."),
 ("P1","UPSIDA (state industrial authority)","Government portal","https://upsida.up.gov.in/","Free to contact","unknown","Medium: authority mentions and links are strong trust signals","Approval papers","Not a listing. Relationship: ask whether private parks are referenced anywhere."),
 ("P1","Invest UP","Government portal","https://invest.up.gov.in/","Free to contact","unknown","Medium","Investor pitch","Relationship, not a self-serve listing."),
 ("P1","NSIC","Government body","https://www.nsic.co.in/","Free to contact","unknown","Low to medium: MSME audience","Pitch","Relationship only."),
 ("P1","Udyam portal (MSME)","Government portal","https://udyamregistration.gov.in/","Free","none","Low: registers enterprises, not parks","None","Mention: tenants will use Udyam. Content opportunity, not a listing."),
 ("P1","Hapur-Pilkhuwa Development Authority (HPDA)","Government body","https://hpda.in/","Free to contact","unknown","Medium: local authority mentions","Pitch","Domain not verified. Confirm before use."),
 ("P1","PHD Chamber of Commerce and Industry","Association","https://www.phdcci.in/","Paid membership","unknown","Medium (named as a Hapur cluster body, reported)","Membership","Paid. Decide later."),
 ("P1","Laghu Udyog Bharti","Association","https://www.laghuudyogbharti.org/","Low cost membership (reported)","unknown","Medium: MSME owners are the target buyers","Membership","Domain not verified. Confirm before use."),
 ("P1","Indian Industry Association (Pilkhuwa)","Association","not verified","Unknown","unknown","Medium (named as a Hapur cluster body, reported)","Membership","Find the real site or contact. Reported in a cluster profile, undated."),
 ("P1","FICCI, CII, ASSOCHAM chapters","Association","https://ficci.in/ ; https://www.cii.in/ ; https://www.assocham.org/","Paid membership","unknown","Low for a small park, high for authority","Membership","Paid. Park-level membership may not be worth it yet."),
 ("P1","Local news and portals (Dainik Jagran, Amar Ujala, Hindustan Hapur and Ghaziabad editions)","Local media","not a self-serve listing","Free to pitch","unknown","High: local news backlinks and brand mentions","Press release","See backlinks.md. Content stays English, press release can be translated by the media."),
 ("P2","Crunchbase","Company database","https://www.crunchbase.com/","Free profile","nofollow (reported)","Low to medium: entity signal for AI models","Company description","Only if the owner agrees to publish a company page. Developer name stays hidden."),
 ("P2","Wikidata","Knowledge graph","https://www.wikidata.org/","Free","none","Medium for entity building, but only with independent references","Press and portal references","Notability needed. Do not create a page now. Plan it after 3 or more independent mentions exist."),
 ("P2","Medium","Publishing","https://medium.com/","Free","nofollow (reported)","Low to medium: article reuse and mentions","Articles","Repost site articles with a canonical link to the site."),
 ("P2","Substack","Publishing","https://substack.com/","Free","nofollow (reported)","Low","Newsletter","Optional, later."),
 ("P2","Quora","Q&A","https://www.quora.com/","Free","nofollow (reported)","Medium: AI tools quote Quora threads (reported)","Answers","Answer real questions, disclose affiliation, no spam."),
 ("P2","Reddit","Q&A","https://www.reddit.com/","Free","nofollow (reported)","Medium: heavily cited by AI tools (reported)","Honest answers","Strict self-promotion rules per subreddit (r/IndiaBusiness, r/indianstartups). Read each rule. Bans are common."),
]
cols = ["priority","platform","group","signup_url","cost","link_type","relevance","asset_needed","notes"]
with open(H / "citations-targets.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(cols); w.writerows(R)

md = """# Citation and listing targets for Isapur Industrial Park

**Verdict:** 15 listings first (P0), done in week 1, give most of the local and map value. The rest are cheap follow-ups or relationship work.
**Evidence:** URLs are the well-known public sign-up pages; they were not re-opened today, so sign-up flows may have moved. Items marked verified were seen in search results on 2026-11-08.
**Caveat:** Link type (follow or nofollow) is reported or unknown for almost every site. Test after listing with a free backlink checker. Do not buy any paid package until the website is live.

## One identity everywhere (NAP rules)

Copy these exactly on every listing. One mismatch weakens all the others.

| Field | Value |
|---|---|
| Name | Isapur Industrial Park |
| Address | Hapur-Modinagar Road, Yusufpur Isapur, Ghaziabad, UP 201022 |
| Primary phone | +91 98370 57800 (second number 92195 49800 in the description only) |
| Website | add the same https URL everywhere once live (one canonical, no tracking parameters) |
| Description (short) | Industrial plots on Hapur-Modinagar Road near the Delhi-Meerut Expressway. 50 ft wide RCC roads, street lighting, planted greenery. |
| Do not write | the developer or company name, any claim without proof on file (see knowledge file section 3), distances without saying straight-line or driving |

## Order of work

1. Week 1: all P0 rows. Claim the Google listing first, then copy the clean data to the others.
2. Weeks 2 to 3: P1 portals, then P1 authority and association relationships.
3. After the website and 3 or more independent mentions exist: P2 rows.

## Table

"""
md += "| Pri | Platform | Cost | Link type | Relevance | Sign-up or claim URL | Assets needed | Notes |\n|---|---|---|---|---|---|---|---|\n"
for p, n, g, u, c, l, r, a, nt in R:
    md += f"| {p} | {n} | {c} | {l} | {r} | {u} | {a} | {nt} |\n"
md += """
## Sources used for the verified items

- Property portals with industrial plots in this area: [RealEstateIndia Ghaziabad industrial land](https://www.realestateindia.com/ghaziabad-property/industrial-lands-for-sale.htm), [SquareYards Modinagar commercial](https://www.squareyards.com/sale/commercial-properties-in-modinagar-ghaziabad), [PropertyWala Meerut Road industrial area](https://propertywala.com/meerut_road_industrial_area_ghaziabad), seen 2026-11-08.
- UP pledge park listing example: [UP MSME Connect pledge park page](https://msme1connect.up.gov.in/Home/pledgeparkdetails?id=5), seen 2026-11-08.
- Hapur cluster bodies (undated profile, reported): [ODOP UP Hapur](https://odopup.in/en/article/hapur).
- Free listing roundups (vendor blogs, reported, domain authority numbers are rough): [w3era](https://www.w3era.com/blog/seo/free-business-listing-sites-india/), [BrightLocal dofollow list](https://www.brightlocal.com/resources/local-citation-sites-with-nofollow-dofollow-links/).

Machine copy: `citations-targets.csv` in this folder.
"""
(H / "citations-targets.md").write_text(md, encoding="utf-8")
print(len(R), "rows")
