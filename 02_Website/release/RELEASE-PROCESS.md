# Release process (staging then production)

Rule: every change goes to staging first. Production only moves through `promote.ps1`, after the owner types GO LIVE.

## Environments
| | Staging | Production |
|---|---|---|
| Pages project | `iip-staging` | `iip-site` |
| URLs | https://staging.isapurindustrialpark.com, https://iip-staging.pages.dev | https://isapurindustrialpark.com |
| Git branch | `staging` (all work happens here) | `main` (always equals what is live) |
| Build | `npm run build:staging` into `dist-staging` | `npm run build:production` into `dist-production` |
| Env file | `site-v2/.env.staging` | `site-v2/.env.production` |
| Search engines | `X-Robots-Tag: noindex, nofollow, noarchive`, robots `Disallow: /` | indexable, robots `Allow: /` |
| Analytics | none (`PUBLIC_GTM_ID` empty) | GTM-KMBRGVSD with consent |
| Canonical | staging URL | https://isapurindustrialpark.com |
| Marker | red STAGING ribbon bottom left | none |
| Deploy | `release/deploy-staging.ps1` | `release/promote.ps1` only |

`scripts/build.mjs` reads only `.env.<mode>`, so the local `.env` can never leak production values into staging.

## Normal change
1. `git switch staging`. Edit.
2. `powershell -File 02_Website/release/deploy-staging.ps1`: builds staging, runs `checks.mjs` (links, one h1, title and description length, banned strings, Vale if configured), deploys to iip-staging, smoke tests it.
3. Look at https://staging.isapurindustrialpark.com on a phone.
4. Commit on `staging` (the checks record the commit, so commit, then run step 2 again).
5. Owner approves. Run `powershell -File 02_Website/release/promote.ps1` (try `-DryRun` first). It refuses unless: branch is staging, tree clean, checks PASS for this commit and under 24 hours old, staging was deployed from this commit, staging smoke passes, `main` can fast-forward. Then you type GO LIVE. It merges into main, builds production, checks it, tags `prod-YYYYMMDD-HHMM`, deploys, smoke tests production, logs a line in `RELEASES.md`, commits that line on main and fast-forwards staging to it.
6. `git push origin main staging --tags`.

## Emergency hotfix
Same path, just shorter: fix on `staging`, `deploy-staging.ps1`, commit, `promote.ps1`. There is no direct production deploy. If staging holds unfinished work, set it aside first (`git stash` or move it to its own branch), so only the fix gets promoted.

## Rollback
- Quickest and safest (seconds, no build): Cloudflare dashboard, Workers and Pages, `iip-site`, Deployments, pick the last good one, "Rollback to this deployment". (wrangler has no rollback command.)
- Scripted: `powershell -File 02_Website/release/rollback.ps1 [-Tag prod-...] [-DryRun]`. Lists the last 5 production deployments, rebuilds an earlier release tag in a temp worktree and redeploys it after GO LIVE. Default is the release before the newest.
- Afterwards main is ahead of production: fix forward on `staging`, then promote.

## Who can do what
| Who | Allowed |
|---|---|
| Helpers | edit on `staging`, run `deploy-staging.ps1`. Never wrangler against `iip-site`, never DNS changes, never merge to main |
| Lead | everything helpers do, plus run `promote.ps1` or `rollback.ps1` only after the owner typed GO LIVE |
| Owner | types GO LIVE, Cloudflare dashboard rollback |

## Owner, once
1. Optional: Cloudflare Zero Trust Access policy on `staging.isapurindustrialpark.com` and `iip-staging.pages.dev` (email OTP for you and the team) so staging is private, not only noindex.
2. Optional: GitHub, Settings, Branches, protect `main` (no direct pushes except from you).
3. Tell the lead to switch the working tree: `git switch staging`.
4. Set Pages project `iip-staging` production branch stays `main` (already). No secrets exist in this setup; wrangler uses your `wrangler login`.
