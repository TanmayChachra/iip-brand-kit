# ISAPUR INDUSTRIAL PARK: brand kit (editable)

Built from the kit you finalised in ChatGPT (white board, charcoal text, yellow/red/green accents, Montserrat + Inter, sunburst device, "A Modern Industrial Address."). The badge is your supplied artwork, traced, never redrawn.

## Folder map
| Folder | What | Open with |
|---|---|---|
| `tokens/` | `brand.tokens.json` (colours, fonts, rules) and `content.json` (words, phones, address). The single source of truth. | any text editor |
| `live/` | SVG files with real, editable text | Illustrator, Inkscape (free), Figma, Affinity, CorelDRAW. Install the fonts in `fonts/` first |
| `outlined/` | Same SVGs with text converted to shapes. Safe to send to a print shop, no fonts needed | same, or any browser |
| `export/pdf/` | Vector PDFs at true physical size (pole 20x32 in, card 3.5x2 in, A4 letterhead) | print shop |
| `export/png/` | 2400 px previews (4000 px hoardings), transparent where relevant | social, WhatsApp, slides |
| `editable-pptx/` | PowerPoint versions of pole board, hoarding, business cards | PowerPoint, Keynote, Google Slides, Canva import |
| `05_Mockups/` | Hoarding next to competitors, pole under Balaji board | presentation |
| `examples/` | Worked adaptation examples | reference |
| `fonts/` | Montserrat and Inter (SIL Open Font License, free for commercial use) | install |
| `_build/` | The scripts that generate everything | developers only |

## Changing things the easy way
1. Words, phone numbers, address, proof lines on/off: edit `tokens/content.json`.
2. Colours or fonts: edit `tokens/brand.tokens.json`.
3. Run `python Brand-Kit/_build/build_kit.py`, then `python Brand-Kit/_build/export.py`.
Every asset updates together, so nothing drifts out of brand.

## Changing things the visual way
Open any file in `live/` in Inkscape or Illustrator. Edit the text, drag the `hero-photo` image to swap the photo. Layers have names (`badge-*`, `hero-photo`).

## Honest limits
- No vector logo exists. The badge is a high-resolution trace of the supplied PNG, accurate for boards and print up to hoarding size at a distance, but an original vector from whoever designed it is better. Find it before very large or very close print.
- Montserrat is an approximation of the wordmark face. If the original wordmark used another typeface, tell us and we swap it.
- The pole board photo (`assets/hero-warehouse.jpg`) was AI generated in your ChatGPT thread. Replace with a real site photo once the park has buildings. Marketing should not imply built facilities that do not exist yet.
- Proof lines (Section 80, Zila Panchayat map) are in the kit but switched off by default. Match wording to your documents before printing.
- Hoarding and pole sizes are recommendations. Confirm exact panel size with the media owner before print.
