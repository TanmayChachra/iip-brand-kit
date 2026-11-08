# Website design direction (v1, 2026-11-08)

Performance and SEO come first. Design is secondary but must follow the locked brand kit (`01_Brand/Brand-Kit/`, tokens in `01_Brand/Brand-Kit/tokens/brand.tokens.json`). The owner does NOT want a mostly black and white site: use the brand colours with confidence.

## Palette (from the kit, plus warm neutrals proven in the poster lab)
| Role | Hex | Use |
|---|---|---|
| Yellow | #FFD600 | CTA buttons, highlights, rule accents, badge halo |
| Red | #E53935 | Short accent lines, small highlights only |
| Green | #0F4D3A | Full-width bands (cream text), headings accent, footer |
| Charcoal | #111827 | Body text and wordmark only. Never a big background |
| Bone | #F4F0E8 | Default page background (no pure white pages) |
| Sage | #EEF2EE | Alternate section background |
| Cream yellow | #FFF6CC | Soft highlight band |
| Mist | #F2F4F6, gray #6B7280, line #E5E7EB | Cards, secondary text, hairlines |
Section rhythm (top to bottom): bone hero with sunburst, green band, sage, cream yellow, bone, green footer. At least 40 percent of the scroll height has colour (green, yellow or a coloured illustration).

## Type
Montserrat (800 for H1 and H2, 600 for H3) and Inter (400, 500, 600) as in the kit. Self-host Latin subset variable fonts, `font-display: swap`, preload the heading font. Tagline in SemiBold, smaller than the wordmark (the signage lesson). The wordmark and badge come from kit SVGs and are never altered.

## Motifs from the kit (use, do not invent new logo variants)
- The thin tri-colour flag (about 1 percent of the width) as section dividers and under the header.
- The 22 point sunburst as large faint hero background, and as a seal behind stats.
- Textures from the poster lab, at low opacity: sunburst tiles, road lanes, plot plan, halo rings (`01_Brand/Experiments/poster-lab/textures/`).
- The 24 kit icons (`01_Brand/Brand-Kit/live/03_Icons/`), stroke 2.4.
- Yellow pill CTA with charcoal text (as on the poster).

## Imagery rules
- The owner has no real photos yet. Never present AI or illustrated images as the park. All artwork is illustrative and labelled "Illustration, not to scale" where it could be mistaken for the site.
- Real photo slots are built in (aspect ratio boxes with a swap path) so photos drop in later.
- Fresh assets for the site are created by the assets agent into `02_Website/assets/` and copied to `02_Website/site/public/img/`: hero illustration, isometric plot layout schematic, road and expressway distance diagram, section spot illustrations, plot size card graphics, OG images, favicon set.

## Layout and UX principles
- Mobile first (390 px), then desktop. One clear job per page, one primary CTA per screen.
- Sticky bottom bar on mobile: Call, WhatsApp. Header CTA on desktop. `tel:` and `wa.me` links only, no JS needed.
- Hierarchy: name, proof (only proven), plots, location, CTA. Proof lines appear only when the document is on file.
- Hero: H1 states what it is and where (keyword aligned), 2 CTAs, 3 proof chips that are verified (50 ft RCC roads, street lighting, planted greenery, 4.7 km driving to the Delhi-Meerut Expressway on-ramp). Approvals chips stay hidden until proof is on file.
- Accessibility: contrast AA, focus rings, skip link, alt text, 44 px tap targets.

## Performance budget (hard)
HTML under 30 KB gzip, CSS under 30 KB, JS under 60 KB gzip (GTM counted separately and loaded after interaction), hero image under 100 KB, first load under 500 KB, Lighthouse mobile 95 plus, CLS 0, LCP 1.8 s.

## Claims
Allowed now (verified in the knowledge file): 50 ft RCC roads, street lighting, planted greenery, Delhi-Meerut Expressway 4.7 km driving to the on-ramp (about 8 min) and 3.9 km straight-line, Bhojpur exit 4.3 km straight-line, Modinagar bus stand 11.4 km driving, Hapur bus stand 13.4 km driving, plots from 300 sq yards (poster). NOT allowed until proof: Section 80, Zilla Panchayat approval, drainage, 24 hour power, security, brand neighbours (Amul, Inox Air, Patanjali), petrol pump details. Draft pages for those exist with `draft: true` and are excluded from the build.
