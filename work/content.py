"""All words and numbers for the site. No em dashes anywhere."""

PHONE = "9837057800  |  9219549800"
ADDRESS = "Hapur-Modinagar Road, Yusufpur Isapur, Ghaziabad, UP 201022"

KITS = {
"jamun": dict(
    name="Jamun", num="01", color="#4B1DA6",
    one_liner="Own the colour nobody on the road owns.",
    tagline_hi="बड़े काम की जगह", tagline_en="A place for big work",
    verdict="The safest bold move. Premium, easy to scale to every touchpoint, and the yellow badge glows on it.",
    idea=("Every competitor board on the Hapur-Modinagar road is built from the same four colours: navy, gold, red and white. "
          "Violet is nowhere on that road, and nowhere in the fields around it. Jamun takes that empty colour and makes it IIP's, "
          "the way purple belongs to Cadbury or blue belongs to Kofi Kafi. Your logo is a yellow sun badge, and yellow against violet is a "
          "complementary pair, so the rosette does not just sit on the board, it glows."),
    why=["Violet is 23 to 54 colour-distance units (CIEDE2000) away from every colour measured on site, the nearest being the Shri Haridas navy.",
         "White on violet reads at 10.4:1 contrast and yellow on violet at 8.8:1, both far above the 4.5:1 accessibility benchmark.",
         "Keeps the board calm and credible for investors and factory owners, but unmistakable at 60 metres.",
         "Works at every scale: a 10 inch pole board, a 24 foot hoarding, a visiting card, a WhatsApp status."],
    device_name="The Sunburst and the Diamond Frieze",
    device=("Two pieces borrowed from the logo itself. The Sunburst: rays that radiate from the rising sun of the logo across any surface, drawn in a "
            "lighter violet at 7 percent. The Diamond Frieze: a band of the red diamonds from the rosette's border on a yellow strip, used as a base line on boards, "
            "walls and documents. Neither is new artwork, so nothing competes with the logo."),
    voice="Calm authority. Short declarative lines, Hindi first, English name. No exclamation marks, no prices, no promises that need approval.",
    taglines=[("बड़े काम की जगह", "A place for big work (primary)"), ("यहीं से शुरू", "Start right here"), ("Build big. Start here.", "English secondary"),
              ("अपना कारखाना, अपना पता", "Your factory, your address"), ("Isapur ka naya udyog pata", "Hinglish for social")],
    palette=[("Jamun Violet", "#4B1DA6", "60%", "Backgrounds, boards, walls"), ("Deep Night", "#1F0E5C", "10%", "Dark panels, night hoardings, text on yellow"),
             ("Sun Yellow", "#FEF102", "20%", "Logo field, frieze, key words (taken from the logo)"), ("White", "#FFFFFF", "10%", "Headlines and body text on violet")],
    fonts=[("Teko", "Headlines, both Hindi and English", "Teko 700 uppercase, tight leading .9", "ISAPUR INDUSTRIAL PARK"),
           ("Hind", "Subheads and body, Hindi and Latin", "Hind 500 to 700", "बड़े काम की जगह")],
    donts=["Never put the logo on violet shades darker than Deep Night; the red diamonds lose their edge.", "Never use green anywhere outside the logo.",
           "Never fill the board with photos or renders; the colour is the picture.", "Never stack more than three lines of text on a pole board."],
    risks=["Violet printed in flex can shift towards blue. Approve a physical colour proof before the full print run.", "Premium tone is less playful; it will not get the street smile that Gulaal does."],
    best_for="Brand-building over 3 to 5 years, investor and factory-owner trust, a single identity across every touchpoint.",
),
"gulaal": dict(
    name="Gulaal", num="02", color="#E4007C",
    one_liner="Talk the way the highway talks.",
    tagline_hi="कारखाना यहीं लगाओ!", tagline_en="Set up your factory right here!",
    verdict="The loudest and most memorable. A cheap pole-by-pole teaser serial that nobody on the road can ignore.",
    idea=("Indian highways have their own visual language: painted truck art, hand-lettered shop boards, cheeky lines on the back of trucks. "
          "Gulaal speaks in that language. Rani pink with cream borders, lettering with a hard drop shadow, and an imperative Hindi line that sounds like a person, not a developer. "
          "Because the pole boards are small, we use the 'Burma-Shave' idea: four consecutive poles carry one line each, three teasers and then the reveal with the logo. "
          "A driver reads a story across 200 metres instead of a brochure on one pole."),
    why=["Rani pink has no neighbour: 25 to 45 units away from every colour measured, and nothing in a farm landscape is this pink.",
         "The yellow rosette on pink is the loudest pairing of the three directions.",
         "The serial turns a weakness (small boards) into the strength: curiosity. Each pole costs the same, the message compounds.",
         "Hindi imperative lines are also the lines people repeat, forward and photograph."],
    device_name="The Painted Frame and the Pole Serial",
    device=("The Painted Frame: a cream border with a yellow dashed inner line and rounded corners, the way a sign painter outlines a board. Lettering always carries a hard offset shadow in Night Ink. "
            "The Pole Serial: boards numbered by position along the road, three teasers in pink, yellow and ink, then the reveal board with the logo."),
    voice="Cheeky, warm, imperative. One idea per board, never more than five words per line. Plain village-market Hindi, no English jargon.",
    taglines=[("कारखाना यहीं लगाओ!", "Set up your factory right here (primary)"), ("कारखाना कहाँ लगाओगे?", "Where will you set up your factory? (teaser 1)"),
              ("सोच रहे हो?", "Still thinking? (teaser 2)"), ("सोचना बंद। चलो।", "Stop thinking. Let's go. (teaser 3)"), ("प्लॉट नहीं, पूरा पता।", "Not just a plot, a full address (social)")],
    palette=[("Gulaal Pink", "#E4007C", "55%", "Board background, hoarding field"), ("Cream", "#FFF4DC", "20%", "Frame, headlines"),
             ("Sun Yellow", "#FEF102", "15%", "Logo field, name bar, teaser 2"), ("Night Ink", "#1A0B2E", "10%", "Shadows, teaser 3, text on yellow")],
    fonts=[("Yatra One", "Headlines (Devanagari), hand-painted feel", "Yatra One with 2 to 4 percent offset shadow", "कारखाना यहीं लगाओ!"),
           ("Baloo 2", "Name bars, English, supporting copy", "Baloo 2 800 uppercase, +4% tracking", "ISAPUR INDUSTRIAL PARK")],
    donts=["Never use pink on pink: the name bar is always yellow.", "Never set cream text below 40 mm cap height on pink; the contrast is 4.2:1, large text only.",
           "Never mix the Gulaal frame with the Jamun frieze.", "Never run the serial out of order; the reveal board needs the three teasers before it."],
    risks=["Playful tone must be approved by the board; it can read as informal to some investors.", "Pink fades faster in sun on cheap flex. Use UV-stable print."],
    best_for="Fast local recall, small boards on many poles, cheap experimentation. Best as a campaign, or as the main identity if the target is local small manufacturers.",
),
"kora": dict(
    name="Kora", num="03", color="#14110F",
    one_liner="Be the quiet board on the loudest pole.",
    tagline_hi="जहाँ उद्योग शुरू होता है", tagline_en="Where industry begins.",
    verdict="The premium contrarian. Wins by saying less than everyone else, but depends on a clean frame to survive the hazy sky.",
    idea=("Look at the stacks of competitor boards: price, phone numbers, badges, a rendered gate, a stamp. Everyone is shouting the same things at once. "
          "Kora does the opposite. A warm ivory board, a heavy black frame, the logo at the biggest size that fits, one line, one yellow bar. "
          "Seventy percent of the board is empty on purpose. In a stack of crowded boards, the empty one is the loudest. "
          "It also signals what a premium park signals: confidence that it does not need to list its features on a pole."),
    why=["Ivory is 24 to 47 units from every competitor colour measured. Its closest neighbour is the hazy sky at 16.5, which is why the black frame is mandatory.",
         "Ink on ivory reads at 17.4:1, the strongest contrast of the three. The words are legible from furthest away.",
         "Lowest cost to extend: black ink and ivory print cheaply and also work in single colour on walls, gates and forms.",
         "Lets the full-colour rosette do all the talking. It is the only colour on the board."],
    device_name="The Underline",
    device=("The logo carries a thick red underline beneath IIP. Kora lifts that gesture: one heavy black underline rule above every headline, a yellow base bar below, and a black frame that makes the board a defined rectangle on any pole. "
            "The rule is the only graphic element. If a design needs a second one, it is too busy."),
    voice="Restrained, factual, premium. English-first headline with a Hindi pair. No exclamation marks, no price, no adjectives that need proof.",
    taglines=[("Where industry begins.", "Primary"), ("जहाँ उद्योग शुरू होता है", "Hindi pair"), ("Isapur Industrial Park", "Name alone is enough"),
              ("Built for factories.", "Secondary, only after facts are approved"), ("Phase 1 · Phase 2", "Phase marker, small")],
    palette=[("Kora Ivory", "#FBF6E9", "60%", "Board background, paper"), ("Ink", "#14110F", "25%", "Frame, rule, headlines"),
             ("Sun Yellow", "#FEF102", "15%", "Logo field, base bar")],
    fonts=[("Archivo", "Headlines and name, variable width", "Archivo 900 at 80% width for headlines, 800 at 112% width and +20% tracking for the name", "WHERE INDUSTRY BEGINS."),
           ("Hind", "Hindi pair and body", "Hind 500 to 700", "जहाँ उद्योग शुरू होता है")],
    donts=["Never print the ivory board without the black frame; against hazy sky it disappears.", "Never add a second rule, icon or photo.",
           "Never let the logo shrink below 45 percent of the board width on pole boards.", "Never put a price or amenity list on the board."],
    risks=["Light boards show dust and fade first; plan a yearly reprint.", "Reads as quiet; it relies on the neighbours being loud to win."],
    best_for="Investor and developer credibility, premium positioning, brand that must also work on paper and in presentations.",
),
}

SCORES = [  # criterion, jamun, gulaal, kora, note
    ("Stands out from the competitor boards", 5, 5, 4, "Measured colour distance, plus how different the layout is from a crowded board."),
    ("Not lost in greenery", 5, 5, 4, "Ivory leans on its frame; violet and pink have no equal in the fields."),
    ("Legible at speed (colour and logo first)", 5, 4, 5, "Pink with cream text is the weakest contrast at 4.2:1."),
    ("Fit with the logo's own colours", 5, 4, 4, "Violet makes the yellow glow; pink and the red diamonds are close cousins."),
    ("Trust with investors and the board", 4, 3, 5, "Premium and serious versus playful."),
    ("Cost to extend across touchpoints", 4, 4, 5, "Kora works in one colour; Gulaal needs more colour passes."),
    ("Memorability and shareability", 4, 5, 3, "Gulaal's lines get repeated; Kora wins by restraint."),
]

STEPS = [
    ("Phase 0 · Decide (week 1 to 2)", "Board picks a direction and the size question (below). Fix the phone number, address line and which claims may appear. Get a vector master of the logo."),
    ("Phase 1 · The road (week 3 to 6)", "Pole boards along the Hapur-Modinagar corridor from the Bhojpur side to past the competitor cluster. Every pole within sight of a competitor stack gets one. Cost driver: number of poles."),
    ("Phase 2 · The landmark (week 5 to 10)", "Two highway hoardings (the Bhojpur approach and the Modinagar approach) and the gate fascia at the park entrance. Cost drivers: monthly site rent, structure, printing."),
    ("Phase 3 · The paper and the phone (week 6 to 8)", "Visiting cards, letterhead, one-page brochure, WhatsApp status pack, site-visit message. Almost free once the kit is approved."),
    ("Phase 4 · Measure (week 8 onward)", "A single call-back number or WhatsApp number per board family, and a tally of enquiries by source. Only then decide whether to scale or switch the creative."),
]

TIERS = [
    ("Lean", "Pole boards only, one size, one family, plus the gate fascia.", "Pole boards (quantity x unit print)<br>Gate fascia (1)<br>Visiting cards"),
    ("Standard (recommended)", "Pole boards in two sizes, two highway hoardings, the gate fascia, the WhatsApp pack and stationery.", "Pole boards in 2 sizes<br>Hoardings (2 sites, monthly rent)<br>Gate fascia<br>Stationery and WhatsApp pack"),
    ("Full", "Standard plus the pole serial (Gulaal) or wayfinding family, vehicle branding and site boundary painting.", "Everything above<br>Wayfinding family<br>Vehicle and wall branding"),
]

SOURCES = [
    ("What belongs in a brand guideline", [
        ("4over4: brand guidelines checklist, six core components", "https://www.4over4.com/content-hub/stories/brand-guidelines-checklist"),
        ("Brandkit: what to include in brand guidelines", "https://brandkit.com/asset-page/830375-what-should-you-include-in-brand-guidelines"),
        ("GOV.UK brand guidelines", "https://www.gov.uk/government/publications/govuk-brand-guidelines"),
        ("EUDA visual identity manual", "https://www.euda.europa.eu/drugs-library/euda-visual-identity-manual_en")]),
    ("Industrial parks and wayfinding", [
        ("VEELLAGE business parks case study", "https://saentys.com/work/veellage/"),
        ("Fareham Industrial Park case study", "https://bewonder.co.uk/our-work/fareham-industrial-park/"),
        ("Silver Hill Technology Park wayfinding", "https://idsignsystems.com/capabilities/industrial-park-wayfinding/"),
        ("Crosspoint Industrial brand launch", "https://www.hughespr.com.au/case-studies/139/crosspoint-brand-launch/")]),
    ("Indian brands that rooted themselves", [
        ("McDonald's: lessons learned from India (NRN)", "https://www.nrn.com/fast-casual/mcdonald-s-lessons-learned-from-india"),
        ("McDonald's India localisation (Business Today, 2001)", "https://archives.digitaltoday.in/businesstoday/20011125/feature1.html"),
        ("Bata red store concept for India (FashionNetwork)", "https://in.fashionnetwork.com/news/Bata-introduces-new-red-store-concept-for-India,973632.html"),
        ("Bata global and local brand strategy (YourStory)", "https://yourstory.com/2025/02/bata-global-local-brand-strategy"),
        ("boAt case study: tapping youth culture (afaqs)", "https://www.afaqs.com/casestudies/the-boat-case-study-tapping-youth-culture-in-indias-audio-market-11068745"),
        ("boAt branding case study (StartupTalky)", "https://startuptalky.com/boat-case-study/")]),
    ("Locality and competitors", [
        ("Google Maps: Yusufpur Isapur", "https://www.google.com/maps/place/Yusufpur+Isapur,+Uttar+Pradesh+201022"),
        ("Modinagar (Wikipedia), Bhojpur exit of the Delhi-Meerut Expressway", "https://en.wikipedia.org/wiki/Modinagar"),
        ("Satellite imagery: Esri World Imagery", "https://www.arcgis.com/home/item.html?id=10df2279f9684e4a9f6a7f08febac2a9")]),
]

