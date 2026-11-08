# AI entry points: how agents work in parallel without breaking each other

Every agent (a chat, a fork, a scheduled task) starts here. Rules in 6 lines:
1. Read `CLAUDE.md`, `00_ISAPUR_KNOWLEDGE.md`, then your own folder's `AGENT.md`.
2. Write only inside your own folder. Other folders are read only.
3. Hand off work only through the contract files below. Never edit a contract you do not own.
4. Questions for the owner and fact proposals go to `_ops/inbox/` (one file per item). Only the lead appends to the knowledge file.
5. Finish by writing `result.json` and updating your row in `_ops/status.json`. The lead rebuilds the board.
6. Do not commit or push. The lead commits per batch.

## Agents and folders
| Agent | Owns (write) | Reads | Typical job |
|---|---|---|---|
| brand | `01_Brand/` | knowledge file | kit, poster, new assets |
| web | `02_Website/` | `03_SEO/keywords/keyword-map.md`, `05_Local-Presence/citations/nap.md`, `04_Analytics/event-spec.md`, `01_Brand/Brand-Kit/tokens` | build pages, schema, Astro project |
| seo | `03_SEO/` | knowledge file, `04_Analytics/` exports | research, keyword map, playbook, AEO and GEO, weekly watch |
| analytics | `04_Analytics/` | `02_Website/` page list | GTM, GA4, event spec, dashboards, A/B test log |
| local | `05_Local-Presence/` | `03_SEO/keywords/` | GBP, listings, reviews, citations |
| content | `06_Content/` | keyword map, brand tokens | pillars, posts, blog drafts |
| lead | `_ops/`, `docs/`, root files | everything | integrate, verify, commit, publish |

## Contract files (the only hand-offs)
| File | Written by | Read by | Contains |
|---|---|---|---|
| `03_SEO/keywords/keyword-map.md` | seo | web, content, local | one row per page: URL slug, primary keyword, secondary, intent, title, meta, H1, schema types |
| `05_Local-Presence/citations/nap.md` | local | web, seo, content | the one canonical name, address, phone block, hours, categories, description |
| `04_Analytics/event-spec.md` | analytics | web | dataLayer events, triggers, naming, conversion list |
| `02_Website/pages.md` | web | seo, analytics | the live page list and URLs (so tracking and keyword map match) |
| `00_ISAPUR_KNOWLEDGE.md` | lead only | all | facts, proof status, decisions |
| `_ops/status.json` | each agent updates its own row | lead, board | state, last run, next step |

## Example of safe parallel work
- Agent A (seo) researches keywords and writes `keyword-map.md` while Agent B (web) builds the page shells from `02_Website/pages.md`. When the map lands, B applies titles and H1s. Neither touches the other's folder.
- Agent C (analytics) writes `event-spec.md`; B adds the data attributes. If C changes the spec it bumps a version line at the top.

## Scheduled research
Weekly task writes `03_SEO/watch/YYYY-MM-DD.md` (new SEO, AEO, GEO tactics and tool changes worth acting on, with sources). It proposes only. A human or the lead decides. It must not edit plans, code or other folders.

## Inbox format (`_ops/inbox/<date>-<slug>.md`)
First line: `TYPE: question | fact-proposal | risk`, then the item, the reason and the options. Lead clears the inbox into the knowledge file or the owner question list.
