"""Section copy for the brand kit page. Plain data: edit words here, then run build_site.py.
Truth labels: DRAFT = proposed by us, owner to confirm. OWNER = owner stated. UNVERIFIED = no document seen."""

# asset tuples: (stem, folder, label, note)  folder = subfolder under live/ and outlined/
LOGO = [
    ("logo-primary-vertical", "01_Logo", "Primary lockup (vertical)", "Default. Badge over ISAPUR over INDUSTRIAL PARK with the red accent line."),
    ("logo-horizontal", "01_Logo", "Horizontal lockup", "Badge, rule, ISAPUR over INDUSTRIAL PARK. Wide spaces: letterhead, web header, hoarding corners."),
    ("logo-badge-only", "01_Logo", "Badge only", "Icon, favicon, social avatar, helmet, stamps."),
]
MONO = [
    ("logo-mono-black", "01_Logo", "Mono black", "Newspaper, fax, one colour print."),
    ("logo-reversed-on-charcoal", "01_Logo", "Reversed on charcoal", "Dark backgrounds."),
    ("logo-badge-mono-green", "01_Logo", "Badge, one colour (deep green)", "Traced from the supplied emblem. Stamps, embossing, one colour print."),
    ("logo-monotone-use", "01_Logo", "Monotone use sheet", "Black, deep green and white versions."),
]
GUIDES = [
    ("logo-clear-space-vertical", "01_Logo", "Clear space, vertical", "Keep X free, X is a quarter of the badge width."),
    ("logo-clear-space-horizontal", "01_Logo", "Clear space, horizontal", "Same X rule."),
    ("logo-minimum-size", "01_Logo", "Minimum size", "Print and screen limits."),
    ("logo-misuse-sheet", "01_Logo", "Misuse", "What not to do."),
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
ICON_NAMES = [("industrial-plots","Industrial plots"),("wide-roads","Wide roads"),("power-supply","Power supply"),("water-supply","Water supply"),("connectivity","Connectivity"),
 ("sustainable","Sustainable"),("secure","Secure"),("business-support","Business support"),("plug-and-play","Plug and play"),("growth","Growth"),
 ("expressway","Expressway"),("highway-truck","Highway and trucks"),("drainage","Waste water drainage"),("street-light","Street lighting"),("planted-greenery","Planted greenery"),
 ("section-80","Section 80"),("acres","Acres"),("zilla-panchayat","Zilla Panchayat"),("plot-layers","Plot layers"),("manufacturing","Manufacturing"),
 ("warehouse","Warehouse"),("location-pin","Location"),("phone","Phone"),("site-visit","Site visit")]
ICONS_ALL = [(f"icon-{n}", "03_Icons", t_, "") for n, t_ in ICON_NAMES]
STATIONERY = [(s, "06_Stationery", l, n) for s, l, n in [
    ("card-front-A", "Business card front, vertical lockup", "3.5 x 2 in"), ("card-front-B", "Business card front, horizontal lockup", "3.5 x 2 in"),
    ("card-back", "Business card back", "Deep green back"), ("letterhead-A4", "Letterhead", "A4"), ("envelope-DL", "Envelope DL", "220 x 110 mm"),
    ("envelope-C5", "Envelope C5", "229 x 162 mm"), ("id-card-front", "ID card front", "54 x 86 mm"), ("id-card-back", "ID card back", "54 x 86 mm"),
    ("notepad-A5", "Notepad cover", "A5"), ("folder-cover-A4", "Folder cover", "A4"), ("doc-header-strip", "Quotation and invoice header", "Strip"),
    ("email-signature", "Email signature", "600 px"), ("helmet-decals", "Helmet decals", "Badge decal sizes"), ("vest-layout", "Safety vest layout", "Chest badge and back lockup"),
    ("catalogue-cover-1080", "WhatsApp catalogue cover", "1080 x 1080")]]
SIGNAGE = [(s, "04_Templates", l, n) for s, l, n in [
    ("sign-pole-20x32in-A", "Pole board A", "20 x 32 in, tagline A Modern Industrial Address."), ("sign-pole-20x32in-B", "Pole board B", "20 x 32 in, tagline The Groundwork for Growth."),
    ("sign-street-pole-24x36in", "Street pole board", "24 x 36 in"), ("sign-hoarding-40x20ft-A", "Hoarding 40 x 20 ft, A", "Confirm panel size with the media owner"),
    ("sign-hoarding-40x20ft-B", "Hoarding 40 x 20 ft, B", "Tagline B"), ("sign-hoarding-40x15ft", "Hoarding 40 x 15 ft", "Wide format"),
    ("sign-gate-fascia-4to1", "Gate fascia", "4:1"), ("sign-pole-20x32in-A-print", "Pole board A, print file", "1 in bleed and crop marks"),
    ("sign-hoarding-40x20ft-A-print", "Hoarding A, print file", "3 in bleed and crop marks")]]
SOCIAL = [
    ("avatar-badge-1080", "05_Social", "Profile picture", "Badge on white, circle safe."),
    ("avatar-badge-sunburst-1080", "05_Social", "Profile picture, sunburst", "Badge on a soft sunburst."),
    ("cover-3to1-1500x500", "05_Social", "Cover banner 3:1", "X header, LinkedIn and Facebook with safe crops."),
    ("post-4x5-1080x1350", "05_Social", "Post 4:5", "Instagram and Facebook portrait."),
    ("whatsapp-status-1080x1920", "05_Social", "WhatsApp status and story 9:16", "Also Instagram story and reel cover."),
]
CONTEXT = [("pole-board-street", "Street pole board"), ("hoarding-billboard", "Hoarding"), ("gate-fascia", "Gate fascia")]

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
    ("4.7 km by road to the Delhi-Meerut Expressway on-ramp", "MEASURED", "Google Maps driving, 2026-11-06. Poster still says 4 km (straight-line), update to match"),
    ("Waste water drainage (naala at the back)", "OWNER", "Dated naala photo, outfall on the plan, pollution board consent"),
    ("Reliable power supply", "OWNER", "Connection or sanctioned load letter"),
    ("Street lighting", "OWNER", "Dated photo of the lit road"),
    ("Planted greenery", "OWNER", "Dated site photos"),
    ("Any warehouse or building picture", "NOT REAL", "No photos exist yet. Never show an AI picture as the park"),
]

DISTANCES = [  # to, driving (Google Maps, 2026-11-06), straight-line
    ("Delhi-Meerut Expressway on-ramp (NE 3, Bhojpur)", "4.7 km, about 8 min", "3.9 km"),
    ("Modinagar bus stand", "11.4 km, about 28 min", "9.3 km"),
    ("Hapur bus stand", "13.4 km, about 31 min", "13.0 km"),
    ("Meerut City railway station", "29.3 km, about 56 min (NE 3, tolls)", ""),
    ("Ghaziabad railway station", "34.7 km, about 47 min (NE 3, tolls)", ""),
    ("Anand Vihar ISBT, Delhi", "46.0 km, about 89 min (NE 3, tolls)", ""),
    ("Shri Haridas (SHD) Industrial Park", "0.65 km, 2 min", "0.54 km"),
    ("CKS Industrial Park", "0.7 km, 1 min", "0.69 km"),
    ("Atom Industrial Park", "3.1 km, 4 min", "3.1 km"),
]
COMPETITORS = [
    ("Shri Balaji Industrial Park", "Sarawa bus stand", "Blue gradient and gold type, rendered township, approval stamp, two numbers"),
    ("Shri Haridas (SHD)", "Ishapur, Bhojpur", "White and navy, Hindi headline, rendered gate, road widths, two numbers"),
    ("Shivansh Industrial Park", "not stated", "Navy and gold, red phone bar, all plot sizes"),
    ("CKS Industrial Park", "Hapur-Modinagar Road", "Not photographed. Listings quote price per yard"),
    ("Atom Industrial Park", "Ishapur", "Not photographed"),
    ("Mahamaya", "same road (owner)", "Unknown"),
]
