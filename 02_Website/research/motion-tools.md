# Motion tools for the IIP scroll story (research, 2026-11-12)

Labels: **verified** = measured or read at source by this run, **reported** = third party, **guess** = inference.
Budget: 30 KB JS total on a static Astro site. No em dashes anywhere.

## 1. Ranked recommendation

1. **Primary: CSS scroll-driven animations (`animation-timeline: scroll()/view()`) plus `motion/mini` `animate` as a thin helper.** Zero or about 3.7 KB gz. Runs off the main thread.
2. **Fallback A: Motion `scroll()` (vanilla)**, only if a scrub needs JS (for example syncing a SVG path or reading progress). About 4.3 KB gz.
3. **Fallback B: GSAP + ScrollTrigger**, only if pinning with complex timelines is unavoidable. About 46 KB gz, blows the budget. Not recommended.
4. **Lenis**: skip by default (5.5 KB gz, adds scroll-jacking feel, a common AI tell). Add only if the owner asks for smoothing.
5. **anime.js v4, Theatre.js**: not recommended (13 KB gz core, 19 KB with timeline and scroll; Theatre is an editor-driven toolchain, too heavy).

## 2. Library table

Sizes are **verified**: esbuild minify + gzip -9 of the named imports, 2026-11-12. Versions from `npm view`, same day.

| Library | Version | Licence | gz size (imports) | Fit for 30 KB budget |
|---|---|---|---|---|
| CSS scroll-driven animations | native | n/a | 0 KB | Best. Needs `@supports (animation-timeline: view())` fallback |
| Motion `motion/mini` animate | 14.12.0 | MIT | 3.7 KB | Good (WAAPI based) |
| Motion `scroll` | 14.12.0 | MIT | 4.3 KB | Good |
| Motion full `animate`+`scroll` from `"motion"` | 14.12.0 | MIT | 31.3 KB | Too big, import from `motion/mini` instead |
| Lenis | 1.3.27 | MIT | 5.5 KB | Fits, but not advised |
| anime.js | 4.5.0 | MIT | 13.3 KB (animate only), 19.1 KB (+timeline, onScroll) | Fits, no gain over Motion |
| GSAP core | 3.15.1 | GreenSock "no charge" (not OSI open source) | 28.5 KB | Too big |
| GSAP + ScrollTrigger | 3.15.1 | same | 46.4 KB | Over budget |
| Theatre.js core | 0.7.2 | Apache-2.0 | not measured | Over budget by design (guess) |

Notes:
- Motion docs state mini animate is about 3.2 KB (reported, https://motion.dev/docs/migrate-from-gsap-to-motion). Our measure of 3.7 KB is the real bundle. A one-line test `import {animate,scroll} from "motion/mini"` fails because `scroll` is not exported there; import `scroll` from `"motion"` (4.3 KB tree-shaken).
- GSAP licence: Webflow made all of GSAP including ScrollTrigger free for commercial use, licence dated 2025-04-30. Not open source, bars building a no-code animation product that competes with Webflow, and charging end users for a tool built on it needs a paid membership (reported, https://webflow.com/blog/gsap-becomes-free , https://gsap.com/standard-license). IIP is a marketing site, so allowed.
- CSS scroll-driven animations support: Chrome and Edge 115 (2023), Safari 26 (Sept 2025), Firefox reported Baseline in Firefox 159 per web.dev October 2026 roundup (reported, https://web.dev/blog/web-platform-10-2026). Older pages disagree on Firefox, so the builder must check MDN or caniuse before dropping the fallback (guess: keep fallback regardless). Safari guide: https://webkit.org/blog/17101/a-guide-to-scroll-driven-animations-with-just-css/ (reported).
- View Transitions: same-document supported in Chrome, Safari, Firefox; cross-document (MPA) `@view-transition { navigation: auto }` works in Chrome and Safari (reported, guess for Firefox). Good for page to page fades on a static Astro site, 0 JS. Not needed for the shed scroll story.

## 3. Installed

- `npm install motion@14.12.0 --save-exact` in `02_Website/site-v2` (package.json and package-lock.json changed, nothing imported yet, zero bytes shipped until used). Import only `motion/mini` and `scroll` from `motion`. Never `import ... from "motion"` for `animate` (pulls 31 KB).
- Claude skills copied as plain text (no scripts) to `~/.claude/skills/`, from https://github.com/emilkowalski/skills (MIT, 56,268 stars, pushed 2026-11-11, verified via gh api). Read in full or grep scanned for commands and injection phrases: none found.
  - `emil-design-eng` (frequency table, easing, durations, springs, `@starting-style`, clip-path)
  - `choreograph` (+RECIPES.md): lead/support/decoration roles, bans uniform stagger, one entrance per container
  - `review-animations` (+STANDARDS.md): audit gate with exact values
  - `animation-performance`: composite-only properties, will-change
- Not installed (available): `animate`, `improve-animations`, `find-animation-opportunities`, `remove-animations`, `break-ui`. Install later with `npx skills add https://github.com/emilkowalski/skills --skill <name>` (reported by https://awesome.ecosyste.ms/projects/github.com%2Femilkowalski%2Fskills). Not run, because it executes an unread installer.
- Already present locally and relevant: `impeccable` (has an animate mode), `taste-skill`, `gpt-tasteskill` (pushes GSAP ScrollTrigger heavily: do NOT follow its GSAP advice here, budget).

## 4. Other repos and lists (reported, not installed)

| Name | URL | Note |
|---|---|---|
| delphi-ai/animate-skill | https://github.com/delphi-ai/animate-skill | Third party, based on Emil's course. Unread, skip |
| Laith0003/ux-skill wiki, Anti AI slop ban list | https://github.com/Laith0003/ux-skill/wiki/Anti-AI-slop-ban-list | Ban list incl. fade-up default. Read-only reference |
| Nutlope/hallmark | https://instagit.com/Nutlope/hallmark/what-are-the-common-ai-design-patterns-hallmark-aims-to-avoid/ | 17 AI design patterns it avoids. Reference only |
| Emil rules summary | https://aiskill.market/blog/motion-that-doesnt-feel-cheap | Blog summary |
| Tell-by-tell fixes | https://capitalandcompute.net/blog/fix-ai-slop-design/ | Blog |

Star counts for third-party items were not verified.

## 5. AI tells and counter rules (builder checklist)

Tells reported across https://github.com/Laith0003/ux-skill/wiki/Anti-AI-slop-ban-list and https://instagit.com/emilkowalski/skills/what-are-common-animation-mistakes-made-by-ai-agents/ (reported, 2026-11-12). Numbers below are starting values, tune by eye.

- [ ] **Uniform fade-up on every block** (20 px up, 300 to 600 ms, same for all). Rule: only 3 to 5 moments per page animate. Everything else is simply there. Each moment has a reason (reveals structure, explains the build).
- [ ] **Same stagger on every group** (100 ms metronome). Rule: no uniform stagger. Lead element first and largest travel, supports shorter and smaller, decoration fade only. Vary delay 40 to 120 ms by importance. Never stagger a parent's entrance and its children both.
- [ ] **Default `ease` or `linear`, or `ease-in` for entrances.** Rule: hand-tuned curves. Start with `cubic-bezier(0.23, 1, 0.32, 1)` (out), `cubic-bezier(0.77, 0, 0.175, 1)` (move), `cubic-bezier(0.32, 0.72, 0, 1)` (drawer-like). Never `ease-in` on entering things. Define as CSS custom properties once.
- [ ] **Springs everywhere or bouncy overshoot.** Rule: springs only for drag or decorative cursor effects. If used: `{ duration: 0.5, bounce: 0.2 }`, bounce 0.1 to 0.3 max. Industrial brand: no bounce on structural elements.
- [ ] **Floating blobs, glow gradients, purple gradients, backdrop blur panels.** Rule: none. Colour comes from the locked IIP brand kit only. Background motion is allowed only if it depicts something real (shadow moving, dust, light on the roof).
- [ ] **Parallax on everything, scroll-jacking, Lenis smoothing by default.** Rule: native scroll only. One depth effect at most, and only where it explains space (ground plane vs structure). Never hijack wheel or block scroll.
- [ ] **Animating layout properties** (`width`, `height`, `top`, `margin`). Rule: animate `transform`, `opacity`, `clip-path`, `filter` (blur under 20 px) only. Check with `animation-performance` skill.
- [ ] **`transition: all`, `scale(0)` entrances.** Rule: list exact properties. Enter from `scale(0.95)` plus opacity, or `clip-path: inset()`.
- [ ] **Animation on hover for every card, bouncing icons.** Rule: hover affects only real controls (buttons `scale(0.97)` on `:active`, 100 to 160 ms).
- [ ] **No reduced motion path.** Rule: wrap in `@media (prefers-reduced-motion: no-preference)`, or show the final built state with a simple opacity step. The page must be fully readable and the shutter state must show without any scroll scrubbing.
- [ ] **No fallback.** Rule: `@supports not (animation-timeline: view())` shows the finished shed (or IntersectionObserver plus WAAPI one-shot per stage). JS off still shows content (SEO and AEO).
- [ ] **Durations.** UI feedback under 300 ms. Scroll story scrubs are tied to scroll distance, not time, so no duration rule there, but any triggered one-shot stays under 700 ms.
- [ ] **Performance gate.** Total motion JS under 10 KB gz of the 30 KB budget. No CLS (reserve space for the sticky stage). `will-change` only on the one actively scrubbing layer.
- [ ] **Proof rule.** The shed story is illustrative. Label it as an illustration, never imply a built structure, spec or dimension that has no proof on file. No AI warehouse photos as the park.

## 6. Five motion ideas for the shed build story

Pattern for all: one sticky stage (`position: sticky; height: 100svh`) inside a tall section (roughly 500 vh), progress from `animation-timeline: view()` or `scroll()` on the section. SVG line art in IIP brand colours. Each stage owns a scroll slice.

1. **Plot draws itself, pegs drop in.** Ground plane outline strokes in with `stroke-dashoffset` scrubbed to scroll (no JS). Four corner pegs then settle with a short translateY (8 px) plus opacity, uneven delays (0, 60, 150, 90 ms equivalents in scroll slices), small string lines stretch between them using `scaleX` from the peg. Purpose: shows survey and marking, the real first step.
2. **Foundation as clip-path reveal.** Footing rectangles open with `clip-path: inset(0 0 100% 0)` to `inset(0)` (grows from the ground line downward, then rises as plinth). Slow ease-out, no fade. Purpose: weight and permanence.
3. **Frame assembles by column then rafter, in sequence.** Columns rise (scaleY from the base, transform-origin bottom) left to right with decreasing travel (lead column biggest), then rafters swing in with `clip-path` along their length. The sequence is meaningful (load path), so staggering is justified. Strict order, no overlap between columns and rafters.
4. **Walls and roof as sliding sheets, roof lands last.** Wall cladding panels slide in from the sides along the frame (translateX 6 to 0 percent with opacity), then the roof sheet lowers a few pixels with a firm ease-out, plus a one-time shadow shift under it (opacity of a ground shadow). Everything before it dims 8 percent to push focus (single state change, not ongoing).
5. **Roller shutter lifts as the payoff, then rests.** Door slats are a stack with `clip-path: inset(0 0 var(--p) 0)` driven by scroll. The last 15 percent of the section: slats lift with a `cubic-bezier(0.77, 0, 0.175, 1)` feel and reveal a warm interior colour block (brand, not a photo) with the phone call-to-action fading up once. Then the stage unpins and nothing else moves. Reduced motion: show the lifted state statically.

## 7. Minimal code skeleton (guess, untested)

```css
:root { --ease-out: cubic-bezier(0.23, 1, 0.32, 1); --ease-move: cubic-bezier(0.77, 0, 0.175, 1); }
@media (prefers-reduced-motion: no-preference) {
  @supports (animation-timeline: view()) {
    .shed__foundation { animation: rise linear both; animation-timeline: view(); animation-range: entry 10% cover 40%; }
  }
}
@keyframes rise { from { clip-path: inset(0 0 100% 0); } to { clip-path: inset(0); } }
```

Use `motion/mini` `animate()` only for one-shot triggered moments (IntersectionObserver), and `scroll()` only where CSS cannot do it.
