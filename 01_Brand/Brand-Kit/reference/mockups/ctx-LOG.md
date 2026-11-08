# Context mockups log (2026-11-06)

Verdict: 6 realistic composites of the NEW signage, 2400 px wide WEBP q88. Exact artwork only, no AI drawn logo or text, no ChatGPT used this round.
Evidence: each file viewed at full size (corners, panel seams and shading, scale, edges). Caveat: base scenes are the earlier AI-generated blank scenes (scene-*.png) and the owner's two real pole photos, so the three scene-based images are not photographs of the park.

## Method
- Script: `Brand-Kit/_build/build_ctx_mockups.py` (new, additive). Reuses `Archive/work-v1/warp.py` (perspective warp, panel luminance re-applied, grain) and `mock4.py` (`on_pole`).
- Scenes are upscaled 2x (cubic) first so the artwork stays crisp, then each board is warped into its blank panel; art with a different aspect is padded with near white (like flex on a larger frame).
- Quads are the ones measured earlier (mock5.py, mock2.py). Output sharpened lightly (unsharp 1.2, 60).
- Run time about 40 s. Tools: Python, OpenCV, Pillow. No browser, no prompts.

## Files
| File | Scene | Art |
|---|---|---|
| ctx-hoarding-beside-competitors | scene-versus: real Shri Balaji board flattened from the owner's photo above, IIP pole board below, hoarding on the right | sign-pole-20x32in-A, sign-hoarding-40x15ft |
| ctx-hoarding-roadside-A / -B | scene-hoarding-a (blank 2:1 hoarding on a pole) | sign-hoarding-40x20ft-A / -B |
| ctx-street-pole-row | scene-poles-a (lamp posts with blank boards) | sign-street-pole-24x36in |
| ctx-gate-fascia | scene-gate-a (concrete gate, blank fascia), cropped to remove empty road | sign-gate-fascia-4to1 |
| ctx-pole-boards-on-real-poles | two real photos (Shri Balaji pole, stacked competitor pole) | sign-pole-20x32in-A and B at the same 20x32 in scale as the board above |

## Notes
- The pale sunburst crop in the art reads as a faint crack on a weathered panel in the hoarding scenes. Consider making it a touch more distinct or removing it for hoardings.
- Competitor boards in the real photos are the owner's own field photos (UNVERIFIED third party material, shown for scale only).
- Not used: scene-gate golden hour test (warm light is rejected by the owner).
