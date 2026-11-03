# IIP brand kit (Isapur Industrial Park)

Three brand directions (Jamun, Gulaal, Kora) for board review. The live deck is the `docs/` folder served by GitHub Pages.

## What is here

| Path | What |
|---|---|
| `docs/` | The published site (7 pages, WEBP images). Regenerate with `python work/build.py`. |
| `work/*.py` | Generators: boards, hoarding art, mockup compositing, map, colour analysis, site build. |
| `work/gen/p-*.txt`, `work/gen/cx.ps1` | The exact image-generation prompts and the runner used. |
| `work/boards/` (local only) | 300 dpi print masters: `{kit}-10x10.png`, `-10x12.png`, `-10x14.png`, teaser boards. |
| `work/wide/` (local only) | Hoarding (2.4:1) and gate fascia (4:1) masters. |

Local-only folders are listed in `.gitignore` because they are large PNG masters and source photographs.

## Rules followed

- **Logo untouched.** `work/logo/prep.py` only removes the white page, the faint die-cut outline and the '1/1' screenshot marker from `IIP Assets/logo.jpeg`. Colours measured from the artwork: yellow #FEF102, red #EE1D23, green #00A54F.
- **No AI-drawn logos or text.** Every board, hoarding and gate is exact artwork. AI was used only to make blank scenes.
- **Images online are WEBP.** PNG masters stay local.

## AI and tool log

| What | Tool | How | Output |
|---|---|---|---|
| Blank hoarding scene | ChatGPT image generation, via the signed-in Codex app CLI (`codex exec`), your account | Prompt `work/gen/p-scene-hoarding.txt`, your roadside photo as reference | `work/gen/scene-hoarding-a.png` |
| Blank gate scene | same | `work/gen/p-scene-gate.txt` | `work/gen/scene-gate-a.png` |
| Test scene (rejected, golden hour look) | same | `work/gen/p-test.txt` | `work/gen/test-blank-hoarding.png` |
| Satellite map | Esri World Imagery tiles (free, attribution on the image) | `work/maps.py`, `work/annot.py` | `docs/assets/map-isapur.webp` |
| Colour distance | scipy k-means and scikit-image CIEDE2000 | `work/analysis.py` | `work/analysis.json` |
| Compositing | OpenCV and Pillow | `work/mock.py` (poles), `work/warp.py` (hoarding, gate) | `docs/assets/*` |

### Prompt rules learned for realistic mockups

1. Give the model your real photo as the lighting and colour reference.
2. Ask for an unedited phone photo: neutral hazy daylight, true colours, sensor noise, JPEG compression, dust and litter.
3. Forbid the AI look explicitly: no golden hour, no warm grade, no glow, no HDR, no bokeh, no soft focus, no vignette, no smooth surfaces.
4. Ask for a blank matte white panel and no text, then place the exact artwork yourself with a perspective warp, keeping the panel's own shading.

## Concepts and inspirations (source attribution)

All artwork is original. Ideas borrowed at concept level only:

- Owning one colour: Cadbury purple, Kofi Kafi blue (observed in a supplied photo).
- Pole serial (Gulaal): the Burma-Shave roadside serial idea, applied to electric poles.
- Painted frame (Gulaal): Indian truck art and hand-lettered shop boards.
- Research sources are listed on the Research page of the site.

## Open items

Phone number (placeholder `98XXX XXXXX`), confirmed address line, vector logo master, language order, allowed claims.
