"""Section copy for the brand kit page. Plain data: edit words here, then run build_site.py.
Truth labels: DRAFT = proposed by us, owner to confirm. OWNER = owner stated. UNVERIFIED = no document seen."""

# asset tuples: (stem, folder, label, note)  folder = subfolder under live/ and outlined/
LOGO = [
    ("logo-primary-vertical", "01_Logo", "Primary lockup (vertical)", "Default. Badge over ISAPUR over INDUSTRIAL PARK with red accent line."),
    ("logo-horizontal", "01_Logo", "Horizontal lockup", "Wide spaces: letterhead, web header, hoarding corners."),
    ("logo-badge-only", "01_Logo", "Badge only", "Icon, favicon, social avatar, helmet, stamps."),
    ("logo-badge-mono-green", "01_Logo", "Badge, one colour (deep green)", "Traced from the supplied dark green emblem. For embossing, single colour print, stamps."),
    ("logo-mono-black", "01_Logo", "Mono black", "Newspaper, fax, one colour print."),
    ("logo-reversed-on-charcoal", "01_Logo", "Reversed on charcoal", "Dark backgrounds."),
    ("logo-clear-space-guide", "01_Logo", "Clear space guide", "Keep X (a quarter of the badge width) free on every side."),
]
PATTERN = [
    ("sunburst-outline", "02_Pattern", "Sunburst outline", "Base shape. Subtle background element, corner crop."),
    ("sunburst-solid-yellow", "02_Pattern", "Sunburst solid", "Filled badge and highlight shape."),
    ("sunburst-ring-border", "02_Pattern", "Sunburst ring", "Border or frame made of the red and yellow diamonds."),
    ("sunburst-repeat-pattern", "02_Pattern", "Repeating pattern", "Very subtle background texture."),
    ("tri-colour-stripe", "02_Pattern", "Tri-colour stripe", "Yellow, red, green. Dividers, tags, call to action."),
    ("diagonal-panels", "02_Pattern", "Diagonal panels", "Layer or section divider."),
    ("cta-badges", "02_Pattern", "Call to action badges", "Plots Available Now, Growth Ready, Strategic Location, Sustainable Development."),
]
ICONS_BASE = [(f"icon-{n}", "03_Icons", n.replace("-", " ").title(), "") for n in
              ["industrial-plots", "wide-roads", "power-supply", "water-supply", "connectivity", "sustainable", "secure", "business-support", "plug-and-play", "growth"]]
ICONS_EXTRA = [(f"icon-{n}", "03_Icons", t, "Added for the park claims shown on the poster.") for n, t in
               [("expressway", "Expressway"), ("highway-truck", "Highway and trucks"), ("drainage", "Waste water drainage"),
                ("street-light", "Street lighting"), ("planted-greenery", "Planted greenery"), ("section-80", "Section 80 compliance")]]
STATIONERY = [
    ("business-card-front", "04_Templates", "Business card, front", "3.5 x 2 in"), ("business-card-back", "04_Templates", "Business card, back", "Deep green back."),
    ("letterhead-A4", "04_Templates", "Letterhead", "A4"), ("id-card-54x86mm", "04_Templates", "ID card", "54 x 86 mm"),
]
SIGNAGE = [
    ("pole-board-20x32in-clean", "04_Templates", "Pole board, clean", "20 x 32 in, matches competitor boards. No photo."),
    ("pole-board-20x32in-photo", "04_Templates", "Pole board with photo", "Replace the AI placeholder with a real site photo."),
    ("street-pole-24x36in-2to3", "04_Templates", "Street pole board 2:3", "24 x 36 in"),
    ("hoarding-40x20ft", "04_Templates", "Hoarding 40 x 20 ft", "Confirm panel size with the media owner."),
    ("hoarding-40x15ft", "04_Templates", "Hoarding 40 x 15 ft", "Wide format."),
]
SOCIAL = [
    ("avatar-badge-1080", "05_Social", "Profile picture", "Badge on white, circle safe."),
    ("avatar-badge-sunburst-1080", "05_Social", "Profile picture, sunburst", "Badge on a soft sunburst."),
    ("cover-3to1-1500x500", "05_Social", "Cover banner 3:1", "X header, LinkedIn and Facebook with safe crops."),
    ("post-4x5-1080x1350", "05_Social", "Post 4:5", "Instagram and Facebook portrait."),
    ("social-post-1080x1080", "04_Templates", "Post 1:1", "Square."),
    ("whatsapp-status-1080x1920", "04_Templates", "WhatsApp status and story 9:16", "Also Instagram story and reel cover."),
]

MOCKS = [("stationery-letterhead-envelope", "Stationery"), ("business-card", "Business card"), ("id-card", "ID card"), ("safety-helmet", "Safety helmet"),
         ("safety-vest", "Safety vest"), ("wall-sign", "Wall sign"), ("envelope-sunburst", "Envelope with sunburst"),
         ("pole-board-street", "Street pole board"), ("hoarding-billboard", "Hoarding"), ("gate-fascia", "Gate fascia"), ("boundary-wall", "Boundary wall")]
SUNMOCK = [("sunburst-image-mask", "Image mask (photos)"), ("sunburst-feature-badge", "Feature badge (icon + text)"),
           ("sunburst-cta-badge", "CTA badge"), ("sunburst-variations", "Colour variations")]

SOCIAL_SPECS = [  # platform, item, size, note   (typical sizes, reported, re-check before upload)
    ("Instagram", "Profile picture", "320 x 320 shown, upload 1080 x 1080", "Circle crop. Use the badge only."),
    ("Instagram", "Feed post", "1080 x 1350 (4:5) or 1080 x 1080", "Portrait takes the most screen."),
    ("Instagram", "Story, reel cover", "1080 x 1920 (9:16)", "Keep text out of the top and bottom 250 px."),
    ("Facebook", "Profile picture", "170 x 170 shown, upload 1080 x 1080", "Circle crop."),
    ("Facebook", "Cover", "820 x 312 on desktop (upload 1640 x 624)", "Phones crop the sides, keep the logo central."),
    ("LinkedIn", "Company logo", "300 x 300", "Square."),
    ("LinkedIn", "Company cover", "1128 x 191", "Very wide and short, use the horizontal lockup only."),
    ("YouTube", "Avatar and banner", "800 x 800 and 2560 x 1440 (safe area 1546 x 423)", "Everything important inside the safe area."),
    ("X", "Avatar and header", "400 x 400 and 1500 x 500", "Header is 3:1, use cover-3to1."),
    ("WhatsApp Business", "Profile, status", "640 x 640 and 1080 x 1920", "Status is the cheapest reach for local buyers."),
    ("Google Business Profile", "Logo and cover", "720 x 720 and 16:9 photo", "Add real site photos. The map pin is the most seen asset."),
]

CLAIMS = [  # claim, status, proof to file
    ("100+ acres", "OWNER", "Registry area statement or layout plan"),
    ("Plots from 300 sq.yards", "OWNER", "Approved price and plot list"),
    ("Approved by Zilla Panchayat", "OWNER", "Sanctioned map with stamp and number"),
    ("Section 80, legally compliant", "OWNER", "Document that names Section 80, its authority and date"),
    ("50 ft. wide RCC roads", "OWNER", "Layout plan with road widths, dated road photo"),
    ("4 km to Delhi-Meerut Expressway", "COMPUTED", "Straight-line from an approximate pin. Needs a dated driven distance"),
    ("Waste water drainage (naala at the back)", "OWNER", "Dated naala photo, outfall on the plan, pollution board consent"),
    ("Reliable power supply", "OWNER", "Connection or sanctioned load letter"),
    ("Street lighting", "OWNER", "Dated photo of the lit road"),
    ("Planted greenery", "OWNER", "Dated site photos"),
    ("Warehouse picture on boards", "NOT REAL", "AI generated, not IIP. Replace with a real photo before print"),
]

DISTANCES = [  # to, straight-line, driving
    ("Delhi-Meerut Expressway (nearest point)", "3.9 km", "not measured"),
    ("Bhojpur exit (expressway)", "4.3 km", "not measured"),
    ("Modinagar town centre", "9.3 km", "not measured"),
    ("Hapur town centre", "13.0 km", "not measured"),
    ("Shri Haridas Industrial Park (SHD)", "about 0.54 km", "not measured"),
    ("CKS Industrial Park", "about 0.69 km", "not measured"),
    ("Atom Industrial Park", "about 3.1 km", "not measured"),
]
COMPETITORS = [
    ("Shri Balaji Industrial Park", "Sarawa bus stand", "Blue gradient and gold type, rendered township, approval stamp, two numbers"),
    ("Shri Haridas (SHD)", "Ishapur, Bhojpur", "White and navy, Hindi headline, rendered gate, road widths, two numbers"),
    ("Shivansh Industrial Park", "not stated", "Navy and gold, red phone bar, all plot sizes"),
    ("CKS Industrial Park", "Hapur-Modinagar Road", "Not photographed. Listings quote price per yard"),
    ("Atom Industrial Park", "Ishapur", "Not photographed"),
    ("Mahamaya", "same road (owner)", "Unknown"),
]
