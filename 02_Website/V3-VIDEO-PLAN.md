# V3 scroll film plan (2026-11-13, research only, no site code touched, not committed)

Labels: **verified** = measured by us on 2026-11-13 (browser pane, curl, ffprobe, page source). **reported** = third party or memory, not checked today. **guess** = our estimate.
Note: `02_Website/DESIGN-LANGUAGE.md` does not exist. The locked language used below comes from `02_Website/V3-HOME.md` (Erode headlines, Inter, flag stripe, 24 tooth sunburst, tokens #FFD600 #E53935 #0F4D3A #00A54F #F2F4F6 #111827, no photos, no AI imagery passed off as the park).

## A. What the two gold standard sites actually do

### freightconsol.com (verified)
- Built in Webflow. Three full HD videos, each pinned on screen while you scroll, and the scroll position sets the video time. Code is the plain recipe: GSAP ScrollTrigger, `scrub: true`, `end: "bottom+=200% top"`, then `tl.to(video, { currentTime: video.duration })` once metadata loads. No canvas, no WebGL. About 15 lines per video (page source, lines 1166 to 1240).
- Files (ffprobe): `fc-shot01..03-web.mp4`, each about 15.0 MB, H.264 Main, 1920x1080, **60 fps**, 15.07 s, 904 frames, 7.96 Mbps, yuv420p, no B-frames, **452 keyframes of 904 (a keyframe every 2 frames)**, moov atom at the front (faststart). Served from a Bunny CDN with range requests. Total about 45 MB, tags are `preload="auto"` so all three download early.
- Touch devices: the code calls `play()` then `pause()` once on the first touch so iOS allows seeking. No separate mobile file, no reduced motion branch (grep found none).
- Loader: a Lottie loader covers the page first (6 s animation). In our browser pane the page stayed white behind it during the test, so we could not watch the film itself. Treat the film look as reported from the markup, not seen.
- SEO: real HTML text. Three `h1` tags exist (should be one), titles and paragraphs are plain text. Stills `scene-02-still.webp` (252 KB) and `scene-03-still.webp` (564 KB) are CSS backgrounds. Videos have no poster and no aria-hidden. Page JS 155 KB site file plus jQuery, GSAP, ScrollTrigger, Splide.
- Why it feels premium: (1) you hold the remote, scroll IS time, so a 15 second shot becomes something you perform by hand; (2) 60 fps source plus a keyframe every 2 frames means the scrub never judders, it feels like turning a physical dial; (3) one continuous camera move per shot, no cuts; (4) a short line of text sits on calm areas of the picture; (5) the film carries the story, copy stays small. What they pay for it: 45 MB and a loader. We copy the feel, not the weight.

### terminal-industries.com (verified unless marked)
- Nuxt (Vue) site, Lenis smooth scroll plus GSAP ScrollTrigger in the main bundle (`B4erEYb0.js`, 228 KB).
- **Hero is an image sequence on a `<canvas>` (2D context), class `video-sequence`.** A Web Worker fetches the frames as blobs: first frame first, then 8 frames every 50 ms in the background. Scroll progress maps to `Math.floor(progress * (frames-1))` and `drawImage` paints it, cover-fitted. Hero section is 2304 px tall with a "Scroll to explore" cue. Frame count, format and URLs were NOT found (the worker's fetches are hidden from the page's resource list): **unknown**.
- Look (screenshots): dusk, warm orange sky fading to near black ground, one heavy truck sliding into a lit yard with dock doors and stacked containers. It is a pre-rendered 3D scene (their own file names say `prerender`), not footage.
- Four more MP4s further down (carousel, not scrubbed): 1440x1440, H.264 Main, 24 fps, 5.04 s, 121 frames, 3.97 Mbps, about 2.5 MB each (curl), `loop`, `autoplay` off, `preload="auto"`. Posters empty, no aria-hidden.
- SEO and speed: SSR HTML, `h1` is real text ("The yard of the future starts today."), JSON-LD present (Organization, WebSite, WebPage, ReadAction), fonts self hosted woff2 about 33 KB each. Heavy third parties (ContentSquare, Apollo, factors.ai, LinkedIn, GA): 132 requests on load. The string `prefers-reduced-motion` is in the HTML styles, behaviour for the canvas not tested.
- Why it feels premium: (1) one hero idea, a truck arriving, readable in one second; (2) dark low key colour with warm light, a "lit window" look that hides render imperfection; (3) very little text; (4) the camera never lets go of the hero object; (5) smooth scroll damping (Lenis) makes frames glide instead of tick.

### What to take for IIP (the thinking)
The film is not decoration, it is the product demo: a plot becomes a working shed and trucks leave. Scroll lets a factory owner "build their unit" with their own hand. Keep: one continuous camera, dusk warm light on charcoal, 6 big beats, almost no words on the film, text in HTML beside it. Drop: loaders, 45 MB downloads, triple h1, no fallbacks.

## B. How to do it safely

### Scrub technique comparison
| Technique | Smoothness | Weight | Risk | Verdict |
|---|---|---|---|---|
| `video.currentTime` scrub (freightconsol) | Good with GOP 1 to 3, seeks can stutter on Safari and cheap Android | one file, 3 to 6 MB at 720p (guess) | main thread seek cost, iOS needs the play/pause unlock | **Primary** |
| Image sequence on canvas (terminal) | Perfect, any browser, any direction | 100 to 150 WEBP frames x 25 to 45 KB = 3 to 6 MB (guess), many requests | memory on phones (decoded frames), more JS | **Fallback for Safari/iOS if scrub stutters** |
| WebCodecs decode | Best | same as video | not Safari-wide enough (reported), complex | skip |
| WebGL / three.js live 3D | Great | model plus 150 KB+ JS | LCP, battery, SEO risk | skip |
| Lottie | Vector only | small | cannot do a 3D render | skip |
| CSS only (SVG shed we already have) | Good | tiny | looks flat | **keep as the reduced-motion/save-data version** |

### Encoding recipe (ffmpeg, guess sizes, verify after first render)
Render at 24 fps, 25 s = 600 frames, 16:9, source PNG sequence in `work/film/frames/%04d.png`.
```
# desktop 1280x720, GOP 3 (a keyframe every 3 frames), no B-frames, faststart, no audio
ffmpeg -framerate 24 -i frames/%04d.png -vf scale=1280:720:flags=lanczos \
  -c:v libx264 -profile:v main -pix_fmt yuv420p -crf 27 -preset slower \
  -g 3 -keyint_min 3 -sc_threshold 0 -bf 0 -movflags +faststart -an film-1280.mp4
# mobile 720x1280 portrait crop (re-render the camera, do not crop landscape), 540 wide is enough
ffmpeg -framerate 24 -i framesP/%04d.png -vf scale=540:960 -c:v libx264 -profile:v main \
  -pix_fmt yuv420p -crf 28 -preset slower -g 3 -bf 0 -movflags +faststart -an film-540.mp4
# optional smaller twin, serve first via <source> order (Chrome/Firefox/Safari 17+ reported)
ffmpeg -i film-1280.mp4 -c:v libvpx-vp9 -crf 36 -b:v 0 -g 3 -an film-1280.webm   # skip AV1 and WebM at first
# poster, first frame, WEBP quality 78 (target 40 to 60 KB)
cwebp -q 78 -resize 1280 0 frame0001.png -o film-poster.webp    # or sharp
```
- All-intra (`-g 1`) is smoothest but 3x to 5x the size (guess). `-g 3` is our default; freightconsol uses a keyframe every 2 frames at 60 fps. If seeking stutters in testing, try `-g 2`.
- Budget (guess): desktop file at most 6 MB, mobile at most 3 MB, poster at most 60 KB. Only the poster and about 2 KB of JS are in the initial load: **under 100 KB initial**.
- Colour: flat shaded art with big gradients bands in H.264. Add a little noise/grain in render (0.5 percent) or use `-crf 24` if banding appears.
- Do not commit big videos to git without a plan: store the encoded files in `02_Website/site-v2/public/film/` only after approval, keep PNG frames out of git (`work/` is local).

### Loading and SEO safety
- All words (h1, captions, step labels) are real HTML on the page, never in the film. The film's wrapper is `aria-hidden="true"`, the `<video>` has `muted playsinline preload="none" poster="..." tabindex="-1"`. Page keeps exactly one `h1` (the page already owns title, canonical, schema: the film must not touch them).
- No layout shift: wrapper has a fixed `height: 400vh` (scroll length) and a `position: sticky; top: 0; height: 100svh` stage with `aspect-ratio`; the poster `<img>` has width and height.
- Poster is an `<img>` (not CSS background) so it can be the LCP candidate if ever above the fold. The film section is BELOW the hero, so the LCP stays the hero map.
- Lazy load: an `IntersectionObserver` with `rootMargin: 100% 0px` sets `video.src` (and picks mobile or desktop file) when the section is one screen away, and only after `requestIdleCallback`. JS is about 40 lines, no GSAP needed: `sticky` CSS plus a `requestAnimationFrame` loop reading `scrollY` and easing (lerp 0.15) toward `currentTime`. Skip Lenis (page scroll feel stays native, better INP).
- Do not use `preload="auto"` on all clips (the freightconsol mistake). One film only.
- Core Web Vitals risks: LCP (keep film off the hero), CLS (reserved height), INP (no heavy scroll handler: one rAF, write only `currentTime`), memory (one video, not six), data (honour fallbacks below).
- Phones (the main audience): `Save-Data`, `navigator.connection.effectiveType` of `2g/3g`, or `deviceMemory <= 2` mean no download: show the poster plus the existing SVG shed section. On touch, run the iOS unlock (`play()` then `pause()` on first touch). Use the 540 px portrait file on `max-width: 700px`. If `seeked` lags more than 120 ms three times in a row, switch to the poster sequence of 6 key stills (cross fade).
- `prefers-reduced-motion: reduce`: no scrub, no download, show six still posters stacked as a normal section with the same HTML captions (or the current SVG shed). Provide a visible "Skip the film" link? Not needed since it is not a trap: the stage is plain scroll length of 400vh, keep it at most 3 screens on mobile.
- Accessibility: the captions carry the meaning, the film adds none. Add `figcaption`: "Artist's impression, not to scale."
- Test gates before release: Lighthouse mobile at least 90 performance, LCP under 2.5 s on 4G throttle, CLS 0, total initial transfer under 100 KB for the film, 6 MB deferred, check on a real mid-range Android and an iPhone.

## C. How to PRODUCE the footage with our own art, ranked

Local facts (verified): GPU NVIDIA GeForce RTX 5070 Ti Laptop, 12 GB VRAM; ffmpeg at `C:\ffmpeg\bin\ffmpeg.exe`; Python 3.12.10; Node installed. **Blender is NOT installed** (`where blender` fails). `pip install bpy` found no matching distribution for this Python 3.12 (verified; the bpy wheel is tied to one exact Python, reported 3.11 for Blender 4.x). Route: portable Blender 4.5 LTS zip from blender.org (about 400 MB, GPL, owner OK needed for the download), run `blender -b -P script.py`. Blackwell cards need Blender 4.4 or newer for OptiX/CUDA (reported).

Data for the real park (verified in `01_Brand/Plot-Maps`): `data/plots.json` holds 389 plots with id, phase, plot no., block, type, area, centroid and bbox only (NO polygons). The polygons are `<path class="plot" id="p1-001">` in `svg/phase1.svg`, `phase2.svg`, `phase3.svg`, in PDF units. Scales (README): 0.4480, 0.5768, 0.9218 units per foot for phases 1, 2, 3, so feet = units / scale. Roads are grey band shapes with width labels (50 ft roads agree). **Gaps (verified, knowledge file): the sheets are not georeferenced, the phases' true relative positions, the gate position and the plot boundary are UNKNOWN.** So the film may show each phase correctly sized but staged side by side, with an invented gate, and must say so.

| Rank | Route | Effort | Quality | Cost | Risk |
|---|---|---|---|---|---|
| 1 | Blender headless 3D, stylised architectural model | 2 to 3 sessions to first film, then cheap to change | Highest, same family as terminal-industries' pre-render, camera path is exact so scrub is perfect | 0 (own GPU, free software, a render of 600 frames at 720p to 1080p about 1 to 3 h guess) | Needs one install, learning curve is on us not the owner; the gate and layout are staged (label it) |
| 2 | Remotion or ffmpeg from our SVG (2.5D: plan drawing, isometric shear, plots lighting up, shed as layered SVG) | 1 to 2 sessions | Good, flat, on brand, matches the kit, looks like a drawing not a world | 0 | Looks "motion graphic" not "premium film"; limited camera depth |
| 3 | AI video (Wan 2.2 or LTX-Video on local GPU or RunPod, or Kling/Veo/Runway) | Fast to try, slow to control | Pretty clips, but camera path and building details drift, cannot hit exact scrub, text and logos garble | Local 0 but 12 GB is tight (5B models, 480 to 720p); RunPod RTX 4090 about 0.3 to 0.7 USD/h reported, roughly 1 to 3 USD per finished minute of 5 s clips (guess); paid cloud tools roughly 0.05 to 0.50 USD per second (reported, varies) | **Owner rule: AI imagery must not pass as the real park.** Only stylised, clearly labelled, never plots or the gate. Licences (reported, check each): Wan 2.x Apache 2.0, LTX-Video own open licence, HunyuanVideo Tencent community licence with regional limits |

Decision: Route 1 is the pipeline. Use Route 3 only for a sky or dusk background plate if wanted, never for the park itself. Route 2 is the fallback and also the reduced-motion version (reuse the existing SVG shed).

## D. Recommended pipeline and storyboard

### Pipeline (all scripted, one folder `07_Film/` or `work/film/`, own agent folder: ask the owner which)
1. `svg_to_geo.py`: read the three SVGs with `svgelements`, convert path to polygons, feet via the scales above, `shapely` clean (buffer 0), write `plots_geo.json` (id, phase, ring in metres, height 0).
2. `build_scene.py` (runs inside Blender): extrude plots 0.15 m (plinth), roads flat 0.02 m, grass base; one procedural PEB shed (columns, rafters, purlins, sheet panels that scale in), low-poly trucks (boxes plus cab) on road polylines, street lights on 50 ft roads, tree blobs; matte "clay model" materials in brand tokens: ground #111827 at dusk, plots #F2F4F6 with #FFD600 and #00A54F accents, roof #E53935 or #0F4D3A, sunburst badge decal on the shed sign board.
3. Camera on one Bezier path, constant arc length speed, ease only at ends, so scroll maps linearly. Render Eevee Next (fast) first for a preview, Cycles + OptiX denoise 64 samples for final.
4. `ffmpeg` encode as in B. `sharp` poster WEBP. File sizes noted in docs.
5. Site: one Astro component (`FilmStage.astro`, additive, own CSS, no change to `index.astro` core beyond one tag) with the 40 line script; SVG shed as fallback. Home polish helper owns site-v2 now: hand over through TODOS, do not edit in parallel.

### 6 shot storyboard, 24 s at 24 fps (600 frames), about 4 s each, one camera, no cuts
| # | Shot | Page section it sits next to | Frames | What the viewer sees |
|---|---|---|---|---|
| 1 | The plot | where it sits | 0 to 100 | High angle on one empty plot in dusk blue, pegs and string pull taut, flag stripe pennants (red, yellow, green) |
| 2 | The build | inside the park | 100 to 200 | PEB shed assembles: footing, columns, rafters, roof sheets, fascia with the badge. No claim text |
| 3 | Road in | the road in | 200 to 300 | Camera drops to the wide road, lane markings, street lights switch on, greenery strip |
| 4 | Trucks out | shops, sizes | 300 to 400 | Shutter lifts, a truck leaves the shed and joins the road, a second arrives |
| 5 | Gate at dusk | the papers, how buying works | 400 to 500 | Stylised gate (invented, label it), warm light, trucks passing under it |
| 6 | The visit | visit | 500 to 600 | Camera rises above the whole layout, three phases side by side, ends on the 24 tooth sunburst badge |
Use ONE tagline for the page, either "The Groundwork for Growth." or "A Modern Industrial Address." In HTML, never in the film. Never show distances or partner brands in frames.

### Time and token estimate (guess)
- Claude tokens: about 70k to 110k in total (svg to geo 15k, Blender scene and shed 30k, trucks and camera 20k, encode and component 15k, QA and fixes 20k). Delegate bulk rendering to the GPU, polish to nobody else.
- Owner time: about 20 minutes (approve Blender download, send items below). Our wall clock: 3 working sessions plus 2 to 4 h of unattended render.
- Milestones: day 1 preview flythrough in Eevee at 540p (20 s per test), day 2 shed and trucks, day 3 final render, encode, component, Lighthouse check.

### Owner must supply
1. KML or KMZ of the park boundary and the three phases (Google Earth, Save place as), or a Google Earth screenshot with the north arrow visible, taken by the owner (nothing scraped).
2. Two known reference points per phase (for example two corner plots) so we can place the sheets on the ground, otherwise the phases are staged side by side.
3. Where the gate is and which road is the main entry, or confirmation that a stylised gate is acceptable with the caption "Artist's impression, not to scale".
4. Yes to download Blender 4.5 LTS portable (about 400 MB, blender.org) and to a 6 MB film on the site.
5. Later: real photos, then swap the clay model for photo plates where possible.

## Risks to watch
- Film claims anything not on file (gate, facilities): keep the film to shapes the owner has already stated (50 ft roads, plots, sheds).
- Weight creep: one film only, desktop at most 6 MB, mobile at most 3 MB, nothing above the fold.
- Safari seek stutter: first fallback is the canvas image sequence at 100 frames.
- Sources: freightconsol.com and terminal-industries.com pages, markup, JS and files read 2026-11-13 (verified). Nothing was copied from either site: recreate as original work, record the reference in the project docs and tell the owner before any commit (source attribution rule).
