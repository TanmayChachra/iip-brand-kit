# ISAPUR Industrial Park: brand kit (v1.1)

Facts and decisions live in `../00_ISAPUR_KNOWLEDGE.md`. Rules for every chat are in `../CLAUDE.md`.

## What is where
| Path | What | Open with |
|---|---|---|
| `IIP-master-assets.svg` | ONE file: the brand book as 13 editable A4 artboards, then every SVG asset as a named group. Text is outlined. | VectorCraft, Inkscape, Illustrator, Figma |
| `live/` | Independent SVG files with real, editable text (install `fonts/` first). Folders: `01_Logo`, `02_Pattern`, `03_Icons`, `04_Templates` (signage), `05_Social`, `06_Stationery` | VectorCraft, Inkscape, Figma, Affinity, Illustrator |
| `outlined/` | Same files with text as shapes. Safe to send to a printer | any browser or vector app |
| `export/pdf/`, `export/png/` | Vector PDFs at true size, PNG previews (PNG stays local) | print shop, preview |
| `tokens/` | `brand.tokens.json` (colours, fonts) and `content.json` (words, phones, address, taglines). Single source of truth | text editor |
| `fonts/` | Montserrat and Inter (SIL Open Font License) | install |
| `research/` | Brand kit anatomy research, driving distances (Google Maps), print colours (ICC conversion) | read |
| `reference/` | The owner's finished boards and mockups (raster) and the new context mockups `ctx-*.webp` | reference |
| `site/` | Source of the web page, brand brief and brand book PDF (copied to `../docs/` by `publish.py`) | browser |
| `_build/` | Generators. `build_all.py` rebuilds every asset, `publish.py` rebuilds the pages and copies them to `docs/` | developers |

## Rebuild
```
python Brand-Kit/_build/build_all.py   # all SVG, PDF, PNG, master file, print colours
python Brand-Kit/_build/publish.py     # page, brand book PDF, brief, copy to docs/
```
Change words, phones, taglines in `tokens/content.json`. Change colours or fonts in `tokens/brand.tokens.json`. Then rebuild.

## Honest limits
- No vector logo exists. The badge is a trace of the supplied artwork. Find the designer's original before very large or very close print.
- Signage and stationery are first versions of the redesign. The sunburst crop on hoardings is pale and may need to be bolder.
- Context mockups use the owner's real photos for the poles. The hoarding, row and gate mockups sit on AI generated blank scenes, so they are not photos of the park.
- CMYK values come from the US Web Coated SWOP profile and are starting points. Approve a printer proof.
- Sizes of poles and hoardings are recommendations. Confirm with the media owner and printer.
- The master SVG is about 12 MB because text is outlined. Open it in a desktop vector app, not a browser tab.
- PowerPoint versions were dropped with the old designs and are a todo.
