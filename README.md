# ISAPUR Industrial Park (IIP): marketing and visibility home

Everything about IIP marketing, brand, website, SEO, local presence and content lives in this folder. Start with `CLAUDE.md` (rules for every chat), then `00_ISAPUR_KNOWLEDGE.md` (single source of truth, never delete or move, append to its change log). Open work: `TODOS.md`. History: `CHANGELOG.md`. AI agents: `_ops/AGENTS.md`.

Live boards (GitHub Pages): brand kit https://tanmaychachra.github.io/iip-brand-kit/ , phase 2 board https://tanmaychachra.github.io/iip-brand-kit/board/ , poster lab https://tanmaychachra.github.io/iip-brand-kit/experiments/poster-lab/

## Folder map
| Path | What | Owner agent |
|---|---|---|
| `CLAUDE.md`, `00_ISAPUR_KNOWLEDGE.md`, `TODOS.md`, `CHANGELOG.md`, `README.md` | Rules, facts and decisions, open work, history, this map. Permanent, keep current | lead |
| `01_Brand/` | Brand kit (`Brand-Kit/`, v1.2 with Erode, design language, voice, plot maps pages), poster (`Isapur-Poster/`), plot maps (`Plot-Maps/`), supplied logo files, references, poster lab (`Experiments/`), `AI-Assets/` (phase 3 only) | brand |
| `02_Website/` | The website: information architecture, page specs, the Astro project (`site/`, when build starts) | web |
| `03_SEO/` | `research/` (stack, tooling), `competitors/`, `keywords/`, `backlinks/`, `aeo-geo/`, `playbook/`, `watch/` (scheduled research output) | seo |
| `04_Analytics/` | GTM and GA4 plan, event spec, dashboards, A/B test log | analytics |
| `05_Local-Presence/` | Google Business Profile audit (`gmb/`), listings and citations (`citations/`), reviews | local |
| `06_Content/` | Content pillars, blog and social calendar, copy drafts (later) | content |
| `_ops/` | Tech stack record (`TECH-STACK.md`), agent entry points, status board data (`status.json`), logs, inbox for questions | lead |
| `docs/` | Published copy for GitHub Pages (kit, brief, `board/`, `experiments/`). Generated, do not hand edit | generated |
| `Archive/` | Old work. Git ignores it | archived |

## Rebuild (brand kit and its Pages copy)
```
python 01_Brand/Brand-Kit/_build/build_all.py   # every SVG, PDF, PNG, master file, print colours
python 01_Brand/Brand-Kit/_build/build_site.py  # local preview of the kit page, then build_brief.py and build_book.py (no publish)
python 01_Brand/Brand-Kit/_build/publish.py     # page, brand book PDF, brief, copy to docs/ (keeps docs/board and docs/experiments). Only after the owner has seen the local build
python _ops/board/build_board.py                # phase 2 board into docs/board/
```

## Rules
Logo never changes. English only. Display font Erode, text Inter, Montserrat only in the logo. One public phone, 98377 64222. Taglines are adaptive (two approved lines, one per creative). Developer is not named. Only claims on the owner's allowed list. Online images are WEBP. No em dashes, no co-author lines in git. Secrets live only in env vars the owner sets.
