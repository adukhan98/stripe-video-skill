# v03_inside: key poses and as-built timeline

Full-screen opaque scene, 1080x1920 @30, 7.133 s (214 f). It uses the paper + 60px grid + vignette background (copied from v01_hook) on every frame.
Explainer: a sealed deep-teal app card. The agent puck dives inside it. "no source code / no information" get struck through. The card tips back and
splits into 3 axonometric slabs (geometry from v06_layers) carrying REA's real step names. Feature rows tick in, ending on "works.".
A small speaker card sits top-right for the whole scene.

## Key poses (scene seconds)

| f | t | on screen | word |
|---|---|---|---|
| 0 | 0.00 | card, puck and speaker card already rising (hard cut in); "take" mid-rise | take 0.05 |
| 5–8 | 0.16–0.27 | padlock badge pops onto the card's top-left corner; dotted path draws from puck to card | a / look |
| 8–11 | 0.26–0.37 | puck squash (anticipation) + ocean rim | — |
| 11–18 | 0.36–0.60 | puck rides the dotted path, shrinking, and dives into the card's hero block | — |
| 17 | 0.57 | "inside" (Fraunces italic ocean 224) at its overshoot peak | inside 0.57 |
| 18–23 | 0.60–0.76 | ripple, card squash; the agent's visor (two ocean eyes) lights up INSIDE the card | — |
| 32–57 | 1.06–1.9 | eyes look around inside, dots march, card floats (hold alive) | — |
| 50–53 | 1.66–1.76 | "take a look inside" blurs up and out | — |
| 55/65 | 1.84/2.16 | "no" "source" (Newsreader 112) | no 1.97, source 2.29 |
| 75–80 | 2.45–2.65 | "code" (Fraunces italic ink 214) at its peak, then the ocean strike draws (2.60–2.84); padlock rattles, eyes glance at it | code 2.65 |
| 94/109 | 3.12/3.62 | "no information" (Newsreader 90); strike draws 3.82; padlock rattles again | no 3.25, information 3.75 |
| 122–127 | 4.06–4.23 | phrase exits bottom-up | — |
| 128–135 | 4.26–4.52 | eyes widen; ocean scan line sweeps the card; padlock shackle opens and the badge pops off | figure 4.49 |
| 133–140 | 4.42–4.68 | card tips back (rotX 60 / rotZ −22, orthographic) into the top-slab pose and crossfades into slab 01 | — |
| 140 | 4.68 | slab 01 (deep) contact squash; "01 Decode branches" slides in along its face; puck hops out and lands on top (4.95) | out 4.81 |
| 153 | 5.10 | slab 02 (white) drops out from under the stack; "02 Trace calls"; the slabs above spring up | how 5.11 |
| 160–167 | 5.34–5.56 | "figure out how" exits | — |
| 168 | 5.60 | slab 03 (ocean) drops out; "03 Recover the rule"; ground shadow | — |
| 171 | 5.71 | row 1 check (feature row, accent check drawn) + "every" | every 5.71 |
| 182 | 6.07 | row 2 check + "single" | single 6.07 |
| 192 | 6.39 | row 3 check + "feature" (Fraunces italic ink 202, back-out) | feature 6.39 |
| 208 | 6.95 | "works." (Fraunces italic ocean 212) at its peak, row 4 check; puck rim + glow + bob; 0.8% camera punch; speaker-card sheen | works 6.95 |
| 208–213 | 6.95–7.13 | hold alive into the hard cut | — |

Continuous: grid drift 20px, camera push 1.0 to 1.012, speaker card float/orbit/inner push, card float, eye saccades and blinks, stack breathing, puck bob.

## As built
- Speaker card 330x230 at (600, 314), tilt rotY −9 to −6 and rotX 5 to 3.5. The video window is 25.5–64.7% of the source height (face centred, chin kept).
- App card 580x700 at (160, 336), deep with the accent edge. Its wireframe UI is SVG and is redrawn on slab 01's top face, so the tip-back crossfade is seamless.
- Slabs: SW 500 / SD 440 / ST 72 (plane units), yaw −22°, elevation 30°, gap 20. The labels are Geist 41 in face space (auto-fit to the face, floor 36), about 35px on screen.
- Feature rows: 228x82 white cards at x 712, y 588–964, with a drawn SVG check (circle + stroke) and wireframe bars.
- Measured bounds over all 214 frames (render diffed against a background-only render, threshold 40): x 64–948, y 296–1471. Nothing leaves the zone.

## Deviations
- The app card is 580x700, not ~640x780: it has to share the zone with the top-right speaker card, the side puck and a full-width kinetic band underneath. The speaker card overlaps the app card's top-right corner on purpose (layered, the face is never covered).
- "code" is set as a Fraunces italic ink hero (214) instead of Newsreader 110, so the "no source code" phrase gets a hero word (house size floor). "no source" stays Newsreader 112.
- I added the spoken words "figure out how" as kinetic type (4.3–5.5) so the lower band is not empty while the slabs split.
- Omitted words: "an app that it has" and "or". The brief's chosen phrases are kept exactly.
- Slab palette: 01 deep (the app surface, with its UI on top), 02 white, 03 ocean (the recovered rule is the accent). The order reads top-down, going deeper into the app.

## V2 revision (2026-10-11, user request; v1 is backed up in edit/animations_v1/)
- **Type:** Inter Tight replaces Newsreader/Fraunces. There are no italics, and the accent is carried by colour only. Hero words are Inter Tight 900 at −0.045em; supporting words are Inter Tight 800 at −0.03em; line-height is 0.88. Lines with data-maxw are auto-fitted to the zone, but none needed shrinking.
  Sizes: "take a look" 100 · "inside" 270 ocean · "no source" 112 · "code" 236 ink (+ ocean strike) · "no information" 90 (+ strike) · "figure" 236 ink · "out how" 112 · "every single" 94 · "feature" 214 ink · "works." 204 ocean.
- **Slab labels:** Inter 600 at 38 in face space (all three fit without shrinking), about 33px on screen. The number is coloured, the name is ink or white.
- **Font asserts:** 900/800/700 "Inter Tight" and 500/600 "Inter".
- **Speaker card:** 330x230 became 420x290 at (516, 304). The video window is 25.7–64.5% of the source height, so the face is centred and the chin kept.
- **Layout changes to fit the bigger speaker card:**
  - App card: 540x660 at (96, 340), was 580x700 at (160, 336). Its UI SVG is stretched to the card, and the padlock sits at its corner.
  - Puck entry point moved to (366, 542).
  - Slabs: 480x360x60, gap 14, stack centre (354, 742). This keeps the top-right edge under the speaker card.
  - Feature rows: 268x76 at x 666, y 640–980.
  - The tip-back x move arcs right first, so the card's swinging corner stays inside x ≥ 60. The padlock now pops off to the right.
- **Baselines:** a1 1206, a2 1444, b1 1156, b2 1340, b3 1456, c1 1262, c2 1432, d1 1128, d2 1310, d3 1467.
- **Timings:** unchanged from v1 (table above).
- **Measured bounds (v2, all 214 frames):** x 62–955, y 288–1479. 0 frames out of zone.
