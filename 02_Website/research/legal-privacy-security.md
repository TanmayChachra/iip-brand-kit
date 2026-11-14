# Legal, privacy and security review for the IIP site

Written 2026-11-14 for go-live. Labels: verified (read at the source on this date), reported (third party or search summary), guess (reasoned, not sourced). This is research, not legal advice. Items marked LAWYER need a qualified Indian lawyer before relying on them.

## A. India

### A1. DPDP Act 2023 and DPDP Rules 2025
- Rules notified 13 or 14 Nov 2025 (sources differ by a day). Phase I (board and definitions) in force from notification. Phase II (consent manager registration) due about 13 Nov 2026. Phase III, the duties that touch a business website (Rules 3 and 5 to 16, 22, 23), start 18 months after notification, about 13 May 2027. reported: https://www.legal500.com/firms/237811-saga-legal/c-india/news-and-developments/the-privacy-timer-starts-now-analysing-the-dpdp-rules-and-its-18-month-countdown , https://ksandk.com/data-protection-and-data-privacy/dpdp-act-rules-2026-compliance-deadline/ (2026-11-14).
- Status in 2026: Board posts were still being filled in May 2026. We found no source confirming a change to the May 2027 date. Check the Gazette or MeitY before relying on it. reported (2026-11-14).
- What a contact-form site must do from Phase III (reported, same sources plus https://www.scconline.com/blog/post/2025/12/26/digital-personal-data-protection-rules-2025-key-highlights/ , https://www.dsci.in/files/content/knowledge-centre/2025/Insight-Brief-on-DPDP-Rules.pdf):
  - Notice (Rule 3): plain language, separate from other text, says what data, why, how to withdraw consent, how to use rights, how to complain.
  - Consent: free, specific, informed, unambiguous, with a clear yes action. Withdrawal as easy as giving it.
  - Grievance (Rule 14): a published contact and a reply within a reasonable time, at most 90 days.
  - Erasure and retention (Rule 8): erase when the purpose ends or after the Third Schedule period or inactivity (sources differ on 3 years inactivity applying to which classes; the schedule targets large platforms). Logs kept one year.
  - Children (Rule 10): under 18 needs verifiable parent consent; no tracking or targeted ads aimed at children. IIP serves factory owners, so the site should state it is not for children and collect nothing from them knowingly.
  - Security safeguards and breach notice to the Board and people affected.
- guess: a visitor who types their own name and phone to be called back is the "voluntarily provided, for the purpose given" case, which the Act treats as a legitimate use without a separate consent box. The Act text for s.7 was not read today. LAWYER to confirm. Our plan does not rely on it: the form states the purpose beside the button and links the privacy page.
- We already meet most of this early: notice page in plain English, one grievance contact, retention stated, rights listed, children line, equal-weight consent for analytics.

### A2. IT Act 2000 and IT Rules
- Section 43A and the SPDI Rules 2011 (reasonable security practices) stay in force until the DPDP Act replaces them in Phase III. guess from general knowledge, not re-read today. A privacy policy and a grievance officer are expected under Rule 4/5 of the SPDI Rules for sensitive data; a name and phone number are not "sensitive" there. LAWYER to confirm.
- CERT-In Directions 2022: report incidents within 6 hours, keep logs 180 days for ICT systems. reported, general knowledge; the Cloudflare-hosted static site has no server logs of its own. LAWYER or host to confirm.
- IT (Intermediary) Rules apply to platforms hosting user content. The site has none (no comments, no uploads). guess.

### A3. Advertising and consumer rules
- Consumer Protection Act 2019 s.2(28) defines misleading advertisement; CCPA Guidelines for Prevention of Misleading Advertisements 2022 require truthful claims, no disguised ads, and disclaimers that cannot contradict the claim. reported/general knowledge, not re-read today. Real-estate ads are within scope. LAWYER to confirm penalties.
- ASCI Code: claims need proof on file, comparisons and numbers need substantiation, a disclaimer must be legible and not hide a material limit. reported. Matches the repo rule "no claim without proof" in CLAUDE.md.
- Site practice that follows from this: distances labelled "by road" or "straight-line", the approvals page holds the sanction wording, no price, return or appreciation claims, no partner brand names until confirmed.

### A4. RERA
- RERA 2016 covers "development of land into plots" for sale. Whether it reaches plots sold for industrial use is contested. A Tamil Nadu tribunal view reportedly held the Act does not split plots into residential, commercial and industrial. reported: https://corpbiz.io/learning/tnrera-tribunal-rera-applies-to-plots-under-industrial-projects/ (2026-11-14). A Supreme Court summary ties promoter status to there being a sale. reported (same search). We found no UP RERA authority either way.
- UP RERA sets size thresholds for registration (about 500 sq m or more than 8 plots, general knowledge, guess) and an ad should carry the registration number if registered.
- Plain statement for the owner: it is unknown from the research whether the layouts need UP RERA registration. LAWYER must answer this before launch ads, billboards or paid media, because if registration applies, every ad needs the number and the site must show it. The site makes no RERA claim today and must not until the answer is on file.

### A5. Cookie consent practice in India
- No India law names cookies. DPDP consent rules apply to personal data processing, and analytics cookies and device identifiers tied to a person are treated by most advisers as personal data. reported/guess. Practice among Indian business sites in 2026 is a banner with Accept and Reject.
- Our choice: a banner with equal buttons, nothing analytics loads before Accept, choice kept 6 months, easy reopen. This also covers the few EEA or UK visitors (GDPR/ePrivacy style).

## B. Microsoft Clarity
- Collects interaction events (click, scroll, mouse move, input, resize), diagnostics, page events and a DOM replay with privacy-sensitive fields masked. verified: https://learn.microsoft.com/en-us/clarity/setup-and-installation/clarity-data (2026-11-14).
- Cookies `_clck` and `_clsk`. Consent Mode: since 31 Oct 2025 Clarity enforces consent signals for visits from the EEA, UK and Switzerland; consent mode is on by default there; site owners pass consent through a supported CMP (CookieYes) or the Clarity Consent API. verified: https://learn.microsoft.com/en-us/clarity/consent-mode (page updated 2025-12-05; read 2026-11-14).
- Free, no traffic cap, from Microsoft. reported (Microsoft site). Script is loaded async and is small, but still adds a third-party script and network calls; measure with Lighthouse after adding. guess for IIP numbers.
- GA4 has no heatmaps or recordings, so Clarity does not duplicate GA4 events; it overlaps only in page and device counts. Mask: strict mode, or "balanced" with the form fields marked `data-clarity-mask`. The site form takes name and phone, so use strict masking.
- Recommendation: USE, but after launch day, only through GTM, only after analytics consent, strict masking. Reasons: it answers "where do people stop on the plot maps page", which GA4 cannot; it is free; consent gating already exists. Not at launch because traffic is near zero and the GA4 event check should pass first. The privacy page already names it as optional. If the owner wants no recordings, skip it and nothing on the site changes.

## C. Google Consent Mode v2 with GTM and GA4
- v2 adds `ad_user_data` and `ad_personalization` to `ad_storage` and `analytics_storage`. Defaults must be set before any Google tag runs; an update call follows the choice. reported/general knowledge, matches https://developers.google.com/tag-platform/security/guides/consent (not re-read today). Required for EEA audiences using Google ads features; India has no such rule.
- Implementation here is stricter than the minimum: defaults set to denied, and the GTM container is not requested at all until the visitor accepts. After Accept: consent update (granted for analytics_storage only; ads signals stay denied because we run no ads), then GTM loads. Reject keeps GTM unloaded. Tradeoff: no cookieless modelled pings, so GA4 counts only consenting visitors. For a site that mostly serves India with low volume this undercounts; accept it, the owner chose proper consent over volume.
- In GTM set GA4 and Clarity tags to need `analytics_storage` (built-in consent checks). Mapping is in `04_Analytics/gtm-plan.md`.

## D. Security review tools

Stats read via the GitHub API on 2026-11-14 (verified). Community views are from general knowledge unless marked.

| Tool | Stars | Last push | Open issues | Licence | Runs | Notes and scariest issues | Verdict |
|---|---|---|---|---|---|---|---|
| anthropics/claude-code-security-review | 6,888 | 2026-02-11 | 102 | MIT | GitHub Action, sends the PR diff to the Claude API | Quiet for 9 months. Open issues: later commits not reported after the first review comment (#168, #169). README warns it is not hardened against prompt injection (reported). Sends code off-machine. | Reject. Needs PRs and API spend, stale, and a static site has little to scan. |
| Anthropic /security-review (built in) | n/a | n/a | n/a | n/a | Local session command, code goes to Claude as in any session | No extra install | Keep as an occasional manual pass, not a tool to adopt. |
| garrytan/gstack cso | 141,468 | 2026-11-14 | 126 | MIT | Local skill in the session | Huge and active; issues are mostly workflow bugs (e.g. #1651, #4345). Telemetry search found no open exfiltration issue. Broad suite, more than needed. | Reject for this site: heavy, overlaps npm audit and header checks. |
| trailofbits/skills | 8,177 | 2026-11-12 | 159 | CC-BY-SA-4.0 | Local Claude skills | Credible authors. Skills target smart contracts, C/C++, Semgrep and CodeQL work; open issues are shell shim bugs (#515). Little fits a static Astro site. | Reject (not a fit). |
| zaproxy/zaproxy | 16,184 | 2026-11-13 | 888 | Apache-2.0 | Local or Docker; baseline is passive spider and rules | Mature OWASP project. Large issue count is normal for its scope. Needs Docker, which is stopped on this machine. | SHORT LIST, run later when Docker runs. |
| GoogleChrome/lighthouse-ci | 7,144 | 2026-11-12 | 151 | Apache-2.0 | Local | Lighthouse already covers best-practices and perf; CI wrapper adds little for a manual deploy. | Reject, use plain Lighthouse. |
| semgrep/semgrep | 17,662 | 2026-11-13 | 998 | LGPL-2.1 | Local CLI; metrics on by default unless `--metrics=off` (reported) | Telemetry default is the main caution. Rules cover JS/TS. The site has about 200 lines of own JS. | Optional, only with `--metrics=off` and local rules. Not on the list. |
| google/osv-scanner | 11,511 | 2026-11-13 | 125 | Apache-2.0 | Local, queries OSV.dev with package names and versions | Fine for lockfiles, but `npm audit` gives the same result here with no extra binary. | SHORT LIST as a second opinion on `package-lock.json`. |
| mdn/mdn-http-observatory | 149 | 2026-11-10 | 26 | MPL-2.0 | Hosted scan by MDN, or self-run | The old mozilla/http-observatory repo is archived (last push 2024-10-22). Successor is active. Sends only the host name. | SHORT LIST (header grade after deploy). |
| securityheaders.com | n/a | n/a | n/a | closed service | Hosted, sends host name | Same checks as the curl header review. | Use once after go-live, no install. |
| npm audit | built in | n/a | n/a | n/a | Local, sends package names to npm | 0 vulnerabilities in production deps today (verified, run 2026-11-14). | SHORT LIST. |
| Cloudflare review material | n/a | n/a | n/a | n/a | n/a | No Cloudflare-published code review skill found for static sites. Pages Security Insights and Web Analytics sit in the dashboard. | Use the dashboard, no tool. |

### Final short list (5)
1. npm audit: free, local, 0 findings now. Run before every deploy.
2. OSV-Scanner on `package-lock.json`: second source for the same risk, one binary, runs offline against the lockfile with a network lookup.
3. MDN HTTP Observatory (and securityheaders.com) after deploy: proves the CSP, HSTS and other headers actually reach visitors.
4. Own CSP browser test (Chromium console on built pages): the check that matters most for a script-gated site.
5. OWASP ZAP baseline via Docker: passive scan once Docker runs; official image only.

Rejected: claude-code-security-review (stale, needs PRs and sends code out), gstack cso and Trail of Bits skills (not a fit, heavy), Lighthouse CI (plain Lighthouse is enough), Semgrep (telemetry default, little code to scan).

### Runs on 2026-11-14
- `npm audit --omit=dev` in site-v2: 0 vulnerabilities (verified).
- Headers on https://iipreview-v3.pages.dev/ (preview, noindex by design): has nosniff and Referrer-Policy; no CSP, no HSTS, no Permissions-Policy, `Access-Control-Allow-Origin: *` (Pages default). The production `_headers` below adds them.
- ZAP baseline: not run, Docker engine not running. OSV-Scanner and Observatory: not run (not installed, not needed to ship).
- CSP browser test: see section E.

## E. What was built (2026-11-14)
- `src/components/Gtm.astro` (head): consent defaults denied, storage with 6 month expiry, GTM loaded only after Accept.
- `src/components/Consent.astro` (body end): banner, Cookie settings reopen, Accept and Reject equal weight.
- `/privacy/` (content/pages/privacy.md) rewritten, `/terms/` added. Vale: see DEPLOY.md note.
- `public/_headers` production headers with CSP. Preview headers stay in `previews/package.mjs`.
- CSP test results are appended in DEPLOY.md.

## F. Needs the owner or a lawyer
1. RERA: does UP RERA cover the layouts. Before any paid ad.
2. DPDP s.7 reading and the notice wording from May 2027.
3. Grievance contact: sales@isapurindustrialpark.com is used; name a person if the owner wants.
4. Whether the sanction wording on the papers page satisfies ASCI and CCPA.

## Checkpoint 2026-11-14 (state so far)
- Research A to D: done (above). Privacy page and /terms/ written, Vale clean (0 findings, no exemption needed). Consent banner and Gtm.astro gate built, footer links added (Foot.astro, one include in Home.astro). Build to dist-legal OK (26 pages).
- Still to do: analytics alternatives verdict (owner update, section G), browser test of consent gate, public/_headers with CSP and browser CSP test, DEPLOY.md and gtm-plan.md notes.

## G. Analytics choice after the owner update (2026-11-14)
GitHub figures verified via API on 2026-11-14. Pricing and free-tier limits are reported or guess (not read at the vendor page today), so the owner should check them before paying anything.

| Option | Stars | Last push | Open issues | Licence | Cookies | Consent needed | Cost | Data location, speed, notes |
|---|---|---|---|---|---|---|---|---|
| Cloudflare Web Analytics | closed | n/a | n/a | closed service | none, no localStorage (reported: https://blog.cloudflare.com/de-de/free-privacy-first-analytics-for-a-better-web/ , https://www.ctrl.blog/entry/review-cloudflare-analytics/) | no banner needed in India, guess, LAWYER to confirm | free | Already on the owner's account. One small beacon, no personal identifiers. Page views, referrers, country, device, Core Web Vitals. No events or funnels. Ad blockers block it (reported). |
| Umami | 40,125 | 2026-11-12 | 125 | MIT | none by default | no, guess | cloud free tier (reported, unverified) or self-host | Self-host needs a server and database. Has custom events. Duplicates Cloudflare for page counts. |
| Plausible | 29,844 | 2026-11-13 | 54 | AGPL-3.0 | none | no, guess | paid from about 9 USD a month (reported, unverified); self-host free | EU hosted, light script, goals and events. Pays for what Cloudflare plus GA4 already give. |
| PostHog | 40,776 | 2026-11-14 | 4,420 | mixed (NOASSERTION, open core) | cookie or localStorage | yes for recordings | free tier (reported, unverified) | Heatmaps, recordings, funnels, flags. Big script, big product, 4,420 open issues. Too heavy for a one-goal static site. |
| Hotjar | closed | n/a | n/a | closed | cookies | yes | free plan with limits, paid above (reported, unverified) | Same job as Clarity with limits and a price. |
| Matomo | 22,027 | 2026-11-13 | 2,556 | GPL-3.0 | optional cookieless mode | depends on setup | cloud paid or self-host PHP and MySQL | Strong and can sit in India, but needs a server. Overkill. |
| Microsoft Clarity | 2,786 (SDK) | 2026-11-12 | 166 | MIT (SDK), service closed | `_clck`, `_clsk` | yes | free, no cap (reported) | Heatmaps and recordings with masking. Consent mode enforced for EEA, UK, CH only (verified, https://learn.microsoft.com/en-us/clarity/consent-mode). |
| GA4 only | closed | n/a | n/a | closed | `_ga` cookies | yes under our policy | free | Needed for key events, Search Console link, later Google Ads. Loses non-consenting visitors. |

### Verdict
1. Core measurement: Cloudflare Web Analytics. Cookieless, free, already on the account, nothing to host. It counts every visitor without a banner, which covers the gap GA4 leaves when visitors reject. The owner turns it on in the Pages project (Settings, Web Analytics, Enable). Pages then injects the beacon at the edge, so no site code changes. The CSP already allows `static.cloudflareinsights.com` and `cloudflareinsights.com`.
2. Conversion events: GA4 through GTM, after consent only (built and tested). It carries `click_call`, `click_whatsapp`, `generate_lead` from `event-spec.md`.
3. Recordings and heatmaps: Clarity, through GTM only, after consent, strict masking, switched on after the launch checks pass. Cheapest option with real masking and no cap, and its consent API fits our banner. If the owner wants no recordings, drop it and nothing else changes.
4. Rejected: Plausible and Umami (duplicate Cloudflare for page counts, one costs money, one needs a server), Matomo (needs a server, overkill), PostHog (heavy, huge open issue list, one-goal site), Hotjar (Clarity's job with limits and a price).
5. Legal note, guess, LAWYER: a cookieless page counter with no persistent identifier is widely treated as outside cookie-consent rules in the EU, and India has no cookie law. DPDP (from May 2027) covers personal data, and Cloudflare processes the IP address for the country lookup. The privacy page says plainly what Cloudflare counts. The banner stays for GA4 and Clarity.

## Checkpoint 2026-11-14 late
Done: research, privacy and terms (Vale clean), consent gate and banner (browser tested: GTM absent before a choice and after Reject, loads after Accept, defaults denied then update granted), headers file and CSP browser test (no violations on /, /plot-maps/, /about/; a deliberate foreign script was blocked, which proves the check logs), analytics verdict. Left: DEPLOY.md and gtm-plan.md notes.
