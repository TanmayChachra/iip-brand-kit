# ISAPUR Industrial Park (IIP): brand project

Start here. The single source of truth for facts and decisions is **`00_ISAPUR_KNOWLEDGE.md`** (never delete or move it, append to its change log).

## Folder map
| Folder | What | Status |
|---|---|---|
| `00_ISAPUR_KNOWLEDGE.md` | Central knowledge: identity, distances, claims and proof, competitors, decisions, tokens, research, open questions | Permanent |
| `Brand-Kit/` | The finished kit: tokens, live and outlined SVG, PDF, PPTX, social templates, reference boards, research, build scripts | Current |
| `Brand-Kit/site/` | Source of the brand kit page and brief (built by `Brand-Kit/_build/publish.py`) | Current |
| `docs/` | Published copy of the page for GitHub Pages: `index.html` (brand kit), `brief.html` (brand brief), downloads | Current, generated |
| `Isapur-Poster/` | Poster. `03_Design/00_LATEST...pdf` is the print file, `01_LATEST...svg` the master, older versions in `_archive/` | Current |
| `IIP Assets/` | Supplied logo files (logo.jpeg, dark green emblem) | Source, do not edit |
| `References/` | Competitor photos, inspiration ads, the final ChatGPT thread images | Reference |
| `Archive/` | Old work kept for reference: `work-v1/` (earlier generators, boards, mockups), `docs-site-v1/` (earlier site), moodboards, process log. Git ignores this folder | Archived |

## Rebuild
```
python Brand-Kit/_build/build_kit.py      # core SVG assets from tokens
python Brand-Kit/_build/build_social.py   # social templates
python Brand-Kit/_build/build_icons_extra.py
python Brand-Kit/_build/export.py         # PNG and PDF
python Brand-Kit/_build/publish.py        # page, brand book PDF, brief, copy to docs/
```
Words, phones, tagline pool: `Brand-Kit/tokens/content.json`. Colours and fonts: `Brand-Kit/tokens/brand.tokens.json`.

## Rules followed
Logo is never changed. English only. Tagline is adaptive (two approved lines). Images online are WEBP. No claim on a board without proof on file (see the knowledge file, section 3). No em dashes, no co-author lines in git.
