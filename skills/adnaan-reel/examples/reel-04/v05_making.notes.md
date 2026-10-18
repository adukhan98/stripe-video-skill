# v05_making — key poses + as built (v2 type: Inter Tight)

Full-screen opaque scene, 1080x1920 @30, 8.500 s (255 f). Paper + 60 px grid (drifts 20x14 px) + vignette
on every frame, camera push 1.000→1.012 (origin 540,900). B-ROLL COLLAGE: real game clips people made, in a
big desktop window, a second window and a big phone, then a fan of all three inside a cloud of app cards.
No speaker card (per brief).

V2 TYPE SWAP (SHARED.md "V2 UPDATE"): kinetic words are Inter Tight — hero words 900 / −0.045em, supporting and
connective lines 800 / −0.03em, line-height 0.88, NO italics; accent = colour ("games", "mobile" ocean; "desktop",
"software" ink). Font assert: 900/800/700 "Inter Tight" + 500/600 "Inter". Layout, media and timings unchanged except the
small re-fits listed under Deviations.

Earlier layout changes (coordinator): game media is the hero (window 860 px wide mid-zone, phone 384x665), kinetic words
live in the lower zone y ~1050–1470 in every beat, intro sits low and big with the empty window dealing in
above it, fan + app-card cloud ~1.15–1.25x and centred ~y 650, beat-C stack fills down to ~1470.

## Key poses

| frame | t (s) | on screen | lands on |
|---|---|---|---|
| f2–f24 | 0.06–0.79 | "people are" (Inter Tight 800, 160, base 1150) / "using it for" (150, right, base 1300) | people … for |
| f9–f28 | 0.30–0.92 | empty desktop window (860x537, ocean edge, chrome + 3 dots) deals in tilted above the words, y 420–957 | — |
| f19–f56 | 0.62–1.85 | wireframe blocks pop one by one, ocean progress bar fills — the thing "being made" | — |
| f29–f34 | 0.96–1.12 | "making" (120) rises in under the intro (base 1434) | making (1.12) |
| f49–f56 | 1.64–1.90 | intro + making lift out with blur, bottom line last | — |
| f57–f62 | 1.90–2.07 | minecraft clip bursts out of the build (circle wipe + inner zoom 1.18→1), window punch, 0.8 % camera punch; "games" Inter Tight 900 ocean 240 (base 1220) peaks 110 % | games (2.07) |
| f67–f85 | 2.22–2.84 | second window (sim clip, 400 px) deals in over the big window's lower-right; "desktop" Inter Tight 900 ink 170 (base 1420) | desktop (2.45) |
| f95–f105 | 3.16–3.50 | "games" lifts out, "desktop" glides up, "applications" (92) lands under it | applications (3.50) |
| f107–f128 | 3.56–4.28 | windows slide/shrink left (W2 arcs under W1), PHONE 384x665 (radius 52, dark bezel, island) rises into the right of the stack playing the fps clip; "mobile" Inter Tight 900 ocean 170 (base 1458) | mobile (3.85) |
| f125–f137 | 4.16–4.57 | desktop line lifts out, "mobile" glides up, "applications" lands | applications (4.55) |
| f155–f176 | 5.18–5.87 | text clears; windows + phone shrink and rotate into a fan centred ~(520, 650) | literally (5.45, base 1300) |
| f167–f195 | 5.56–6.5 | 12 plain wireframe app cards (play tile, chart, checklist, deep tile, phone app, chat, player, calendar, grid tile…) fly out from behind the fan, 2 f stagger, overshoot + settle; cloud spans y ~291–995 | every (5.97) |
| f193–f205 | 6.41–6.83 | "single piece of" lands low (base 1395) | single, piece, of |
| f204–f214 | 6.80–7.13 | both lines glide up 222 px to make room | — |
| f210–f216 | 7.0–7.19 | cards ripple outward by distance, phone pops, small camera punch; "software" Inter Tight 900 ink 200 (base 1355) peaks | software (7.19) |
| f218–f250 | 7.26–8.33 | "that they can make with it." (Inter Tight 800, 70, base 1454) word by word | that … it |
| f250–f254 | 8.33–8.47 | hold alive into the hard cut (clips play, float, push, drift) | — |

## As-built timeline (slot seconds)

- Words (entrance start → spoken contact): people 0.00→0.06, are 0.13→0.26, using 0.37→0.50, it 0.61→0.74,
  for 0.79→0.92, making 0.96→1.12 · intro/making out 1.64/1.67/1.70.
- W1 deal-in 0.30–0.92 (+ sheen 0.40) · wireframe 0.62–1.53 (0.13 s apart) · progress 1.00–1.85 · clip reveal 1.90–2.20,
  window punch 1.93–2.41 · games hero 1.87→peak 2.07→settle 2.39, out 3.16.
- W2 deal-in 2.22–2.84 (+ sheen 2.30) · desktop hero 2.25→2.45, glides up 250 px 3.27–3.57, out 4.16 · applications 3.37→3.50, out 4.19.
- Windows slide left 3.56–4.02 · phone deal-in 3.66–4.28 (+ sheen 3.76) · mobile hero 3.65→3.85, glides up 4.27–4.57, out 5.18
  · applications 4.42→4.55, out 5.21.
- Fan 5.24–5.87 · app cards start 5.56 + i·2 f (12 cards, scale 1.15) · literally 5.32→5.45, every 5.84→5.97,
  single 6.28→6.41, piece 6.46→6.59, of 6.70→6.83 · lines glide up 222 px at 6.80/6.83 · ripple + punch 7.0–7.5 ·
  software 6.99→7.19 · that 7.26→7.39 … it. 8.20→8.33 · hold to 8.5.
- Video (all muted, `class="clip"`, timing on the `<video>` only, same source chained to loop; each segment = full
  source length, next starts 1 frame early on top, so no gap / black frame ever):
  game_minecraft 1.9 / 3.767 / 5.633 / 7.5 · game_sim 2.233 / 3.6 / 4.967 / 6.333 / 7.7 · game_fps 3.667 / 5.533 / 7.4.

## QA

- `slots.py check --motion --at 0.5,1.12,2.07,2.45,3.5,3.85,4.55,6.0,7.19,8.33` → prores yuva444p12le 1080x1920 @30, 8.500 s,
  255 frames, no dead holds, checks passed.
- Bounds measured on every frame from a background-less render (alpha > 50 %): x 68–953, y 291–1476 — inside x 60–960, y 285–1480.
- Clips verified playing in render.mov: frame-to-frame diff inside every screen region is non-zero (the odd single static
  frame matches duplicate frames already in the source files); minimum luma in the screens 37 (dark game scene), never black.

## Deviations

- Type re-fit for Inter Tight (wider, taller x-height): "making" 130→120 and base 1428→1434, "using it for" base 1310→1300,
  desktop glide −240→−250, beat-C glide −212→−222, "software" 190→200 at base 1355 (758→798 px wide, inside x ≤ 960 with
  overshoot), last line base 1454. Intro 160/150 and "applications" 92 stay above the v2 floors (hero ≥170, supporting ≥84).
- The first window deals in during the intro as an empty wireframe that builds, and the game bursts into it on "games"
  (brief: deal in on "games").
- Shown words follow words.txt in order: adds the spoken "for", "literally" and "that"; omits "and" (4.93).
- Text works as a conveyor (new line pushes the previous one up, oldest lifts out) so each word gets its beat in the lower zone.
- App cards are 1.15x (not 1.25x): the cloud already spans the full zone width; the fan objects are 1.25x of v1.
- Loops are hard jump-cuts back to the clip's first frame. game_sim has no TikTok handle in the source; @systemface and
  @tinfoildurag stay uncropped and visible.
