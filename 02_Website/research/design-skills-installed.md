# Design skills and tools installed (2026-11-08)

**Verdict:** done. 3 new or updated skills plus the Playwright CLI. The other 3 requested skills were already installed.
**Evidence:** upstream repos shallow cloned, every SKILL.md read, grep security gate run, Playwright CLI smoke test passed (screenshot of the local site).
**Caveat:** the security gate is targeted greps, not a full code audit. New skills load in the next session. Skills folder count is now 111 (was 109).

| Item | Result | Source and version |
|---|---|---|
| Taste Skill (design-taste-frontend) | UPDATED from the old single file (87 KB) to tasteskill 2.5.1 with assets, library, references and scripts (39 MB). Old copy kept in the session scratchpad. | https://github.com/Leonxlnx/taste-skill (commit f6b7657, 2026-11-07). The owner link used LeonxInx, the real repo is Leonxlnx |
| Image to Code | KEPT as installed. Upstream no longer ships it as a separate skill (the new taste skill covers reference images and a browser check). Older variants live in https://github.com/Leonxlnx/taste-skill-classics (opt in, not installed) | local copy unchanged |
| Web Design Guidelines | KEPT, identical to upstream | https://github.com/vercel-labs/agent-skills/tree/main/skills/web-design-guidelines |
| Awesome Design | KEPT. It is a pointer skill to https://github.com/VoltAgent/awesome-design-md (84 brand DESIGN.md files fetched on demand) | local copy unchanged |
| Impeccable | INSTALLED 4.8.1 (58 files, 2.3 MB), skill folder only | https://github.com/pbakaus/impeccable (commit 924bbd1, 2026-11-07). Installer not run |
| Playwright CLI | INSTALLED CLI 0.1.23 (npm global @playwright/cli) and the playwright-cli skill | https://github.com/microsoft/playwright-cli |

## Security notes
- Taste Skill scripts spawn local Chrome and open local pages (127.0.0.1) to check pages; no remote code fetch. Some templates load Google Fonts, jsdelivr, picsum, Wikimedia.
- Impeccable: `scripts/impeccable` is a shell wrapper that downloads an engine binary with curl or wget from its GitHub release the first time you run it (impeccable.style, github). I did not run it. Treat the first run as downloading code from that repo.
- No eval, no pipe to shell, no hidden unicode found in what was copied (the minified screenshot library only contains base64 font inlining code).

## Smoke test
Served `02_Website/site/dist` on port 4477, `playwright-cli open` read the page title "Isapur Industrial Park | Industrial Plots, Modinagar", `screenshot` wrote a 155 KB PNG, browser closed, server stopped.
