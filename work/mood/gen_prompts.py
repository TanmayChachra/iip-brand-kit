"""Writes 8 moodboard prompts (one per route) in the same board format as the user's liked ChatGPT boards."""
import pathlib
OUT = pathlib.Path(__file__).resolve().parent
BASE = r"""Use your built-in image generation tool to create ONE image, then copy it (Copy-Item from the file under C:\Users\anshc\.codex\generated_images, never base64 on the command line) to D:\SILVERLEAF_BUILDCON\03_Marketing\IIP Branding\work\mood\{name}.png and print the final path.

TASK: a premium brand-identity MOODBOARD for "Isapur Industrial Park" (an industrial park in Ghaziabad, India), shown as ONE landscape 3:2 presentation board, like a professional agency brand-direction sheet. Route name: "{title}".

LOGO (critical): the first attached image is the real logo, the yellow scalloped badge with red diamonds and green "IiP". Reproduce it EXACTLY, never redraw, recolour or restyle it. Place it ONLY as in the layout below. The wordmark beside it is set as: ISAPUR in bold, INDUSTRIAL PARK in wide-tracked capitals.

DIRECTION: {idea}

PALETTE (use only these, show them as labelled swatches with hex codes): {palette}
TYPE: {type}
GRAPHIC DEVICE (the one recurring element): {device}
MOOD / PHOTOGRAPHY: {photo}

BOARD LAYOUT (tidy modular grid, generous white space, thin hairline dividers, small caps section labels):
1. Top-left hero panel: logo + wordmark lockup on {hero_bg}, with the tagline "{tagline}".
2. Colour palette strip with swatches and hex codes, a typography specimen ("Aa" plus font names), 6 minimal line icons (plots, wide roads, power, water, connectivity, security).
3. Large central panel: a vertical electric-pole advertising board (portrait 2:3, matte, slim dark frame) mounted on a street-light pole beside a hedge-lined road, with a row of identical boards receding behind it. The board design follows the direction above: {pole}. Photorealistic, neutral overcast daylight.
4. Right column: (a) a highway hoarding (landscape) and (b) a gate/entrance fascia, both carrying the same identity; photorealistic.
5. Bottom row: {extras}.
Every board must look recognisable from far away by colour and shape alone, like Vodafone's red pole banners.

REALISM RULES: neutral true-colour daylight, NOT golden hour, no warm orange grade, no glow, no bloom, no HDR, no soft AI blur. Crisp sharp photographic mockups with natural grain. Text must be spelled exactly as given, no invented words, no gibberish, no phone numbers, no QR codes. Keep it minimal, calm and expensive, not cluttered.
"""
ROUTES = {
 "r1-quiet": dict(title="Quiet paper", idea="Maximum white space and breathing room. Warm white board, thin black frame, the badge, the name, one short red rule and one line. About 70 percent empty. Calm next to crowded competitor boards.",
   palette="Paper #F7F4EC, Ink #15171A, Brand red #EE1D23 (rule only), badge colours inside logo only", type="Montserrat ExtraBold for ISAPUR, Montserrat Medium wide-tracked for INDUSTRIAL PARK, Hind for Hindi",
   device="a short thin red horizontal rule under the name", photo="clean modern industrial buildings with metal cladding in soft overcast light, lots of sky and empty space",
   hero_bg="warm white paper", tagline="Room to build.", pole="warm white face, thin black frame, badge at top, ISAPUR and INDUSTRIAL PARK centred, red rule, the line 'Room to build.' and nothing else",
   extras="a visiting card and letterhead on a pale stone desk, a minimal wayfinding sign, a folded brochure"),
 "r2-portal": dict(title="Portal doorway", idea="The entrance as a symbol. The badge sits inside a flat vermilion arch (a tall rounded doorway) on warm ivory. The arch repeats on every item.",
   palette="Ivory #F4F0E6, Ink #15171A, Vermilion #D6311F (the arch only)", type="Sora Bold wide-tracked for ISAPUR, Sora Light for the line, Hind for Hindi",
   device="a tall flat vermilion arch holding the badge, standing on a thin black ground line", photo="a tiny person walking toward a tall bright doorway in a huge calm wall, architectural, quiet",
   hero_bg="warm ivory", tagline="Step in.", pole="ivory face with the vermilion arch holding the badge, ISAPUR wide-tracked below it, 'Step in.'",
   extras="a pole serial of four boards (three with rising red steps, then the doorway), a visiting card, a gate fascia detail"),
 "r3-ink": dict(title="Ink night", idea="The only dark board on the road. Charcoal with a thin cream frame, cream type and one fine yellow line ending in a dot, like a power line plugging in. Premium, works lit at dusk.",
   palette="Charcoal #121316, Cream #F4EFE3, Sun yellow #FEF102 (the line only)", type="Manrope ExtraBold for ISAPUR, Manrope Regular wide-tracked for INDUSTRIAL PARK",
   device="one thin yellow line ending in a round dot", photo="warehouse facades at blue hour with warm lit windows, dark cladding, long calm shadows",
   hero_bg="charcoal", tagline="Plug in. Build up.", pole="charcoal face, thin cream inner frame, badge, ISAPUR, INDUSTRIAL PARK, 'Plug in. Build up.', a thin yellow line with a dot at the bottom",
   extras="an illuminated pole box glowing at dusk, a black matte brochure with embossed badge, a visiting card"),
 "r4-heritage": dict(title="Institutional serif (DLF-style premium)", idea="Serious, trusted, institutional like a top real-estate developer. Deep warm stone and brass, a refined serif headline, huge confidence, very little ornament.",
   palette="Stone #E8E2D6, Deep umber #2A2420, Brass #B08D57, Ivory #FAF7F0", type="a refined high-contrast serif (like Cormorant or Playfair) for ISAPUR, a clean grotesque for small text",
   device="a thin brass hairline frame with a small corner notch", photo="architectural details: stone, brass, large industrial glazing, symmetrical building masses, soft daylight",
   hero_bg="stone", tagline="Built to last.", pole="stone face with a thin brass hairline frame, badge, ISAPUR in serif, 'Built to last.'",
   extras="a leather-bound brochure with brass foil, a stone entrance monolith sign, a visiting card"),
 "r5-mono": dict(title="Monochrome grid (Karyan-style)", idea="Black and white only, strict grid, heavy geometric sans, a one-line descriptor in capitals like 'INDUSTRIAL | WAREHOUSING | LOGISTICS'. The yellow badge is the only colour anywhere, so it pops.",
   palette="Pure white #FFFFFF, Black #0B0B0B, Mid grey #8A8A8A", type="a wide geometric sans (like Syne, Michroma or Montserrat Black) for ISAPUR, small caps descriptor with pipe dividers",
   device="a pipe-divided capital descriptor line under the name and a thick black bar at the board base", photo="black and white architectural photography of warehouses, high contrast, strong geometry",
   hero_bg="white", tagline="INDUSTRIAL | WAREHOUSING | LOGISTICS", pole="white face, thick black bar at the bottom, badge, ISAPUR in heavy black sans, the pipe descriptor line",
   extras="a black visiting card with the badge, a monochrome signage family, a truck side panel"),
 "r6-owned-colour": dict(title="One colour owned (Vodafone-style from afar)", idea="Recognisable from far away by colour alone. Every board is a full-bleed flat vermilion field with only the badge at large size and ISAPUR below, like Vodafone's red pole banners. Nothing else.",
   palette="Signal vermilion #D6311F, White #FFFFFF, Ink #15171A", type="a bold neutral grotesque (Inter Bold) for ISAPUR in white",
   device="the full-bleed colour field itself, repeated on every pole, rhythm of identical boards", photo="a long road with identical vermilion pole boards in perspective, rhythm and repetition, seen from afar",
   hero_bg="flat vermilion", tagline="(no tagline)", pole="full-bleed flat vermilion, white scalloped ring behind the badge, ISAPUR in white below, nothing else",
   extras="a pole-row perspective shot, a vermilion vehicle wrap, a vermilion gate fascia"),
 "r7-blueprint": dict(title="Blueprint plot grid", idea="The park as a planned grid. Faint technical drawing lines, plot numbers and a compass on warm paper; ink and a single yellow highlight. Says 'planned, ready to build' without photos.",
   palette="Drawing paper #F5F2EA, Ink #1B1D21, Pencil grey #B9B6AE, Highlight yellow #FEF102", type="a technical mono (like IBM Plex Mono) for labels and a bold grotesque for ISAPUR",
   device="a faint plot-grid pattern with a yellow highlighted single plot", photo="aerial top-down orderly industrial plots, site plan drawings, roads in perfect grid",
   hero_bg="drawing paper", tagline="Plot. Plan. Build.", pole="paper face with faint grid lines, one yellow highlighted plot square, badge, ISAPUR, 'Plot. Plan. Build.'",
   extras="a folded site plan, a surveyor stake sign, a visiting card with grid lines"),
 "r8-editorial": dict(title="Editorial concept adverts", idea="Conceptual editorial advertising, like your references: one human figure tiny against a huge calm space, big quiet headline, lots of empty space. A separate premium campaign layer.",
   palette="Warm white #F4F1EA, Concrete grey #8D8F91, Vermilion #D6311F (one accent), Ink #15171A", type="Montserrat Light large headlines, Hind for Hindi, tiny wide-tracked caps for the name",
   device="a single tiny human figure for scale", photo="a tiny person on a vast red staircase in an empty ivory hall; a tiny person walking into a doorway of light in a huge concrete wall; workers on a frame under a vast pale sky",
   hero_bg="warm white", tagline="Every factory begins with one step.", pole="portrait poster: the red staircase scene, headline 'Every factory begins with one step.', the badge at top-left",
   extras="two more conceptual posters (doorway of light 'Step in.', workers on a frame 'Building India's next factories.'), and a long hoarding"),
}
for n, r in ROUTES.items():
    (OUT / f"p-{n}.txt").write_text(BASE.format(name=n, **r), encoding="utf-8")
print(len(ROUTES))
