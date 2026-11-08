"""Writes placeholder-but-useful, claim-safe copy into site/src/content. The parent replaces it later with 06_Content/website-copy/*.md.
Allowed claims only (see 02_Website/DESIGN-DIRECTION.md). Run: python 02_Website/qa/gen_content.py"""
import pathlib, json
ROOT = pathlib.Path(__file__).resolve().parents[1] / "site/src/content"
(ROOT / "pages/location").mkdir(parents=True, exist_ok=True); (ROOT / "posts").mkdir(parents=True, exist_ok=True)


def fm(d):
    out = ["---"]
    for k, v in d.items():
        out.append(f"{k}: {json.dumps(v, ensure_ascii=False)}")
    out.append("---")
    return "\n".join(out) + "\n"


def write(rel, meta, body):
    p = ROOT / rel; p.parent.mkdir(parents=True, exist_ok=True); p.write_text(fm(meta) + "\n" + body.strip() + "\n", encoding="utf-8")


FAQ = [
    {"q": "Where is Isapur Industrial Park?", "a": "Isapur Industrial Park is on Hapur-Modinagar Road at Yusufpur Isapur, near Bhojpur, in Ghaziabad district, Uttar Pradesh (PIN 201022)."},
    {"q": "How far is it from the Delhi-Meerut Expressway?", "a": "By road it is 4.7 km, about 8 minutes, to the expressway on-ramp at Bhojpur (Google Maps driving, read on 6 November 2026). In a straight line it is about 3.9 km to the nearest point of the expressway."},
    {"q": "What plot sizes are available?", "a": "Industrial plots start from 300 sq yards. Call or WhatsApp us for the current plot list and sizes."},
    {"q": "What is the price of an industrial plot?", "a": "Price depends on plot size and location inside the park. Contact us for the current price list, and we will share it with the plot map."},
    {"q": "What facilities does the park offer?", "a": "The park is planned with 50 ft wide RCC roads, street lighting and planted greenery. Ask our team about power, water and other facilities for the plot you are considering."},
    {"q": "Can I visit the site before deciding?", "a": "Yes. Call 98370 57800 or 92195 49800, or message us on WhatsApp, and we will fix a site visit."},
    {"q": "Which cities and towns are nearby?", "a": "Modinagar is 11.4 km by road and Hapur 13.4 km by road. Meerut City railway station is 29.3 km and Ghaziabad railway station 34.7 km by road, using the expressway."},
    {"q": "Who is the park for?", "a": "Factory owners, manufacturers, warehousing and logistics businesses looking for an industrial plot in the Modinagar and Hapur belt."},
]

write("pages/home.md", dict(title="Industrial Plots in Modinagar | Isapur Industrial Park", description="Industrial plots on Hapur-Modinagar Road, Ghaziabad. 50 ft wide RCC roads, street lighting and planted greenery, 4.7 km by road from the Delhi-Meerut Expressway.",
      h1="Industrial plots on Hapur-Modinagar Road, 4.7 km from the Delhi-Meerut Expressway", lead="Isapur Industrial Park is a planned address for factories and warehouses in the Modinagar and Hapur belt. Plots start from 300 sq yards. Call us and visit the site this week.", pageType="home", schema=["Place"]),
      "Industrial plots in Ghaziabad district for factory owners.")
write("pages/industrial-plots.md", dict(title="Industrial Plots from 300 Sq Yards | Isapur Industrial Park", description="Industrial plots from 300 sq yards on Hapur-Modinagar Road, Ghaziabad. Ask for the plot list, plot map and price.", h1="Industrial plots from 300 sq yards", lead="Choose a plot size that fits your unit today and your growth tomorrow. We share the current plot list, plot map and price on call, WhatsApp or at the site.", pageType="plots", cta="plots"),
      """## What to ask for
- The current plot list and sizes.
- The plot map and road layout.
- The price for the plot you want.
- A site visit time that suits you.

## How to choose
Match plot size to the building you plan, the truck movement you expect and the room you want for expansion. Our guide [how to choose an industrial plot](/blog/how-to-choose-an-industrial-plot/) walks through it, and the [buying checklist](/blog/industrial-plot-buying-checklist/) lists what to verify before you book.""")
write("pages/amenities.md", dict(title="Roads, Street Lighting and Greenery | Isapur Industrial Park", description="Planned with 50 ft wide RCC roads, street lighting and planted greenery on Hapur-Modinagar Road, Ghaziabad.", h1="Built around wide roads, light and green space", lead="The park is planned around how factories actually work: trucks that need room, shifts that run after dark and a work place that is pleasant to be in.", pageType="amenities"),
      """## Roads
50 ft wide RCC roads give trucks and containers room to turn and cross.

## Street lighting
Street lighting along the roads supports evening and night shifts.

## Planted greenery
Planted greenery along the roads keeps the park cooler and more pleasant for workers and visitors.

Ask our team about other facilities for the plot you are considering. We will tell you what is ready and what is planned.""")
write("pages/location.md", dict(title="Location and Distances | Isapur Industrial Park", description="Isapur Industrial Park is 4.7 km by road from the Delhi-Meerut Expressway on-ramp at Bhojpur. Distances to Modinagar, Hapur, Meerut and Ghaziabad.", h1="On Hapur-Modinagar Road, close to the Delhi-Meerut Expressway", lead="Yusufpur Isapur, near Bhojpur, Ghaziabad. Under 5 km by road to the expressway on-ramp.", pageType="location", schema=["Place"]),
      """## Getting here
Take Hapur-Modinagar Road to Yusufpur Isapur. The Delhi-Meerut Expressway on-ramp at Bhojpur is 4.7 km, about 8 minutes, from the park. Use the directions button to start from where you are.

## Places we serve
We get most enquiries from Modinagar, Hapur, Ghaziabad, Meerut and the Delhi NCR belt. See our pages for industrial plots in [Modinagar](/location/industrial-plots-in-modinagar/), [Hapur](/location/industrial-plots-in-hapur/), [Ghaziabad](/location/industrial-plots-in-ghaziabad/), [near the Delhi-Meerut Expressway](/location/industrial-plots-near-delhi-meerut-expressway/) and [Bhojpur](/location/industrial-plots-in-bhojpur/).""")

LAND = {
    "industrial-plots-in-modinagar": ("Modinagar", "Industrial Plots in Modinagar | Isapur Industrial Park", "Industrial plots on Hapur-Modinagar Road, 11.4 km by road from Modinagar bus stand and 4.7 km from the Delhi-Meerut Expressway on-ramp.", "Industrial plots in Modinagar", "Modinagar bus stand is 11.4 km by road (about 28 minutes) from the park, 9.3 km in a straight line. The park sits on Hapur-Modinagar Road at Yusufpur Isapur, so Modinagar's factories, suppliers and workers are within a short drive.", [("Modinagar bus stand", "11.4 km", "28 min")]),
    "industrial-plots-in-hapur": ("Hapur", "Industrial Plots in Hapur | Isapur Industrial Park", "Industrial plots on Hapur-Modinagar Road, 13.4 km by road from Hapur bus stand. Plots from 300 sq yards, 4.7 km from the Delhi-Meerut Expressway.", "Industrial plots for Hapur businesses", "Hapur bus stand is 13.4 km by road (about 31 minutes) from the park, 13.0 km in a straight line. Hapur-Modinagar Road connects Hapur to the park directly.", [("Hapur bus stand", "13.4 km", "31 min")]),
    "industrial-plots-in-ghaziabad": ("Ghaziabad", "Industrial Plots in Ghaziabad District | Isapur Industrial Park", "Industrial plots in Ghaziabad district at Yusufpur Isapur. 34.7 km by road to Ghaziabad railway station via the Delhi-Meerut Expressway.", "Industrial plots in Ghaziabad district", "The park is in Ghaziabad district, on Hapur-Modinagar Road. Ghaziabad railway station is 34.7 km by road (about 47 minutes) using the Delhi-Meerut Expressway, which has tolls. Anand Vihar ISBT in Delhi is 46.0 km by road.", [("Ghaziabad railway station", "34.7 km", "47 min"), ("Anand Vihar ISBT, Delhi", "46.0 km", "89 min")]),
    "industrial-plots-near-delhi-meerut-expressway": ("the Delhi-Meerut Expressway", "Industrial Plots Near Delhi-Meerut Expressway | Isapur Industrial Park", "Industrial plots 4.7 km by road from the Delhi-Meerut Expressway on-ramp at Bhojpur. 3.9 km straight-line to the nearest point of the expressway.", "Industrial plots near the Delhi-Meerut Expressway", "The expressway on-ramp at Bhojpur is 4.7 km, about 8 minutes, by road. The nearest point of the expressway is 3.9 km in a straight line and the Bhojpur exit is 4.3 km straight-line. Meerut City railway station is 29.3 km by road using the expressway, which has tolls.", [("Expressway on-ramp, Bhojpur", "4.7 km", "8 min"), ("Meerut City railway station", "29.3 km", "56 min")]),
    "industrial-plots-in-bhojpur": ("Bhojpur", "Industrial Plots in Bhojpur Area | Isapur Industrial Park", "Industrial plots at Yusufpur Isapur near Bhojpur, Ghaziabad. The Bhojpur expressway on-ramp is 4.7 km by road.", "Industrial plots near Bhojpur", "Isapur Industrial Park is at Yusufpur Isapur, near Bhojpur. The Bhojpur on-ramp to the Delhi-Meerut Expressway is 4.7 km by road, about 8 minutes, and 4.3 km straight-line to the Bhojpur exit.", [("Expressway on-ramp, Bhojpur", "4.7 km", "8 min")]),
}
for slug, (place, title, desc, h1, para, rows) in LAND.items():
    body = f"""## Why this location
{para}

## The park in short
- Plots from 300 sq yards on Hapur-Modinagar Road, Yusufpur Isapur, Ghaziabad.
- 50 ft wide RCC roads, street lighting and planted greenery.
- 4.7 km, about 8 minutes, by road to the Delhi-Meerut Expressway on-ramp.

## Next step
Call or WhatsApp us for the plot list and a site visit. See also the [location page](/location/) and [industrial plot sizes](/industrial-plots/)."""
    write(f"pages/location/{slug}.md", dict(title=title, description=desc, h1=h1, lead=f"A planned industrial address for businesses in and around {place}.", pageType="landing", place=json.dumps(rows), schema=["Place"]), body)

write("pages/faq.md", dict(title="Industrial Plot FAQ | Isapur Industrial Park", description="Answers about industrial plots at Isapur Industrial Park: location, distance to the Delhi-Meerut Expressway, plot sizes, price and site visits.", h1="Questions factory owners ask us", lead="Short answers first. For anything else, call us.", pageType="faq", schema=["FAQPage"], faq=FAQ), "")
write("pages/about.md", dict(title="About Isapur Industrial Park", description="Isapur Industrial Park is a planned industrial address on Hapur-Modinagar Road, Yusufpur Isapur, Ghaziabad.", h1="A planned industrial address", lead="Isapur Industrial Park is made for factory owners who want room to grow in the Modinagar and Hapur belt.", pageType="about"),
      """## What we are building
A planned industrial park with wide roads, street lighting and planted greenery, close to the Delhi-Meerut Expressway.

## How we work
Call or WhatsApp us, ask for the plot list and map, and visit the site before you decide.""")
write("pages/contact.md", dict(title="Contact and Site Visit | Isapur Industrial Park", description="Call 98370 57800 or 92195 49800, WhatsApp us or send an enquiry for industrial plots at Isapur Industrial Park, Hapur-Modinagar Road.", h1="Talk to us and visit the site", lead="Call, WhatsApp or send the short form. We reply with the plot list and a visit time.", pageType="contact"), "")
write("pages/privacy.md", dict(title="Privacy | Isapur Industrial Park", description="How Isapur Industrial Park handles enquiry details and website analytics.", h1="Privacy", pageType="other"),
      """We collect the details you send in the enquiry form (name, phone, plot interest) only to reply to you. We do not sell them. This site uses analytics to understand which pages help visitors, and it does not use advertising pixels. To ask us to delete your details, call us on the numbers in the footer.""")
write("pages/neighbours.md", dict(title="Brands Around the Park", description="Draft: brands and services around the park.", h1="Brands around the park", pageType="brands", draft=True), "Draft. Needs owner confirmation and written permission before any brand is named.")
write("pages/approvals.md", dict(title="Approvals and Documents", description="Draft: approvals and documents.", h1="Approvals and documents", pageType="other", draft=True), "Draft. Published only when the documents are on file.")
write("pages/gallery.md", dict(title="Photos and Video", description="Draft: site photos and video.", h1="Photos and video", pageType="gallery", draft=True), "Draft. Needs the site shoot.")

write("posts/how-to-choose-an-industrial-plot.md", dict(title="How to Choose an Industrial Plot: 7 Checks", description="Seven practical checks to choose an industrial plot: size, shape, road width, access, power, water outflow and growth room.", h1="How to choose an industrial plot: 7 checks", date="2026-11-08"),
      """Choosing an industrial plot is a long term decision. These seven checks keep it simple.

## 1. Plot size for today and for growth
Draw your building, yard, loading area and parking first. Then add room for the expansion you expect in five years.

## 2. Plot shape and frontage
A regular shape with enough frontage makes layout and truck movement easier.

## 3. Road width and access
Trucks and containers need room to turn. Check the width of the road at the plot and at the park entrance.

## 4. Distance to the expressway
Ask for the driven distance to the nearest expressway on-ramp, not only the straight-line distance.

## 5. Power and water
Ask what power load is available and how water is supplied, then ask for it in writing.

## 6. Rainwater outflow and ground level
Check where rainwater goes after a storm and how the plot level sits against the road.

## 7. Papers
Ask which documents are available for the plot and read them with your advisor.

Want to see plots on Hapur-Modinagar Road? [Call or WhatsApp us](/contact/) and visit the site.""")
write("posts/industrial-plot-buying-checklist.md", dict(title="Industrial Plot Buying Checklist for Factory Owners", description="A checklist before you book an industrial plot: documents, layout, roads, utilities, access and total cost.", h1="Industrial plot buying checklist for factory owners", date="2026-11-08"),
      """Use this list when you visit any industrial park, including ours.

## Before the visit
- Write your plot size range, the type of building and the trucks you expect.
- Note your budget and when you want to start work.

## At the site
- Walk the roads and note their width and surface.
- Look at street lighting, rainwater outlets and greenery.
- Check the distance to the highway or expressway by road.
- Ask to see the plot map and mark your plot.

## Papers and money
- Ask for the list of documents for your plot and the payment schedule.
- Ask what is included in the price and what costs extra.
- Take time to read everything with your advisor.

## After the visit
Compare two or three parks on the same points. Then call us with your questions: [contact page](/contact/).""")
print("content written")
