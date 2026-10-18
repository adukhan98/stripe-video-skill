# CHAIN_SHARED — the 9-stage pipeline chain (m01_stages … m10_render)

One world geometry for all 10 chain scenes, in `chain_common.js` (owner m01_stages; copied byte-identical into every
m*/hf, never forked). Each scene opens on EXACTLY the previous chain scene's end state, so the cuts read as one camera.
Colours come from the tokens only (brand.css: accent `--brand-primary` = blurple, discs `--brand-deep` = slate).

## World (on #cam > #punch, world px)
Gentle S-wave left → right, disc d = 150, 4 px slate connector centre → centre, number tags 1–9 on each disc.
`y = 575 − 195·sin(π·i/4) − 60·(i − 4)`, `x = 300 + 300·i` (i = 0..8).

| # | label | icon | world centre |
|---|---|---|---|
| 1 | Transcribe | microphone | (300, 815) |
| 2 | Cut | scissors | (600, 617) |
| 3 | Brand | palette | (900, 500) |
| 4 | Assets | images | (1200, 497) |
| 5 | Plan | clipboard-text | (1500, 575) |
| 6 | Build | code | (1800, 653) |
| 7 | Sound | speaker-high | (2100, 650) |
| 8 | Assemble | film-strip | (2400, 533) |
| 9 | Check | check-circle | (2700, 335) |
| (m10) | Render | sparkle (no play icon in the set), d 170, accent | (3000, 250) |

Labels: Inter Tight 800, 51 px world, centred under the disc, top = y + 93 (on empty paper below, never in the row).
Heading (m01 only, world): "Nine" 225 px accent at (255, −55), "stages" 165 px ink at (390, 155).

## Camera poses `[cx, cy, s]` (C.pose)
- **WHOLE** `[1530, 575, 2/3]` — discs at screen x 140 … 1740 (200 px apart), labels 34 px on screen, heading top-left.
- **FOCUS n** `[x_n + 208, y_n + (540 − Y_n)/1.25, 1.25]` — disc n at screen (700, Y_n), Y_n = 430, except 320 for 3 and 4 (keeps disc n+3 above the speaker-card box); label 64 px on screen. Pushes bow the path with a negative lift (content rises mid-move, never dips into the box).
- **FINAL** `[1683.75, 575, 0.5926]` — m10 only: disc 1 at screen x 140, render disc at x 1740.
- Moves: `C.travel(segs, LAST)` — one pure function of time, x power2.inOut, y + scale power3.inOut, optional lift /
  breath / anticipation dip; rests exactly on the last pose.

## Scene chain (end state of each = frame 0 of the next)
| scene | frame 0 | end |
|---|---|---|
| m01_stages | discs 1–3 + labels close up (pose [620, 650, 1.05]), line undrawn | WHOLE, all slate, all 9 labels, heading |
| m02_transcribe | m01 end | FOCUS 1, disc 1 accent, label 1 |
| m03_cut … m08_sound | FOCUS n−1, disc n−1 accent, label n−1 | FOCUS n, disc n accent, label n |
| m09_check | FOCUS 7 | FOCUS 9 (via 8), disc 9 accent, label 9 |
| m10_render | FOCUS 9 | FINAL, discs 1–9 + render disc accent, phone chip above Check, "Render" label |
