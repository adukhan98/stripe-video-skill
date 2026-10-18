# t3_six — v7 "MINT" style test · TALK → SIGNATURE SHRINK → THE HABIT CHAIN

Render: `render.mov` · 68 frames (ffprobe) · 1080x1920 @30 · `slots.py check --motion`: checks passed, no dead holds.

## Key poses (as built)

| frame | t (s) | on screen | lands on |
|---|---|---|---|
| 0–8 | 0.00–0.27 | him full-screen (TALK); 'Here' rises low on his chest (y ≈ 1357–1440), charcoal + v7 light glow | Here 0.05 |
| 10 | 0.33 | 'Here are' settled; 'six' (200, mint) rising top-right over the ceiling | are 0.35 |
| 11–14 | 0.38–0.48 | ANTICIPATION: footage pushes 1.0 → 1.015 on his face (3 f); 'Here are' blurs up and out (0.36–0.56) | — |
| 15 | 0.49 | 'six' peaks (hero overshoot) | six |
| 14–26 | 0.48–0.88 | THE SHRINK: clip-path rect → rounded card → circle (power3.out, leads), log-space zoom 1.015 → 0.2368 (power2.out), arc to (300,560) (x power3.out, y power2.out); paper board revealed around it; grid zooms 2× → 1× toward disc 1 (camera pull-out); strong vignette fades up with the clip | six → habits |
| 22 | 0.72–0.96 | mint ring (8 px) draws clockwise round the face circle | — |
| 22 | 0.75 | 'habits' (165, charcoal) lands under 'six' | habits |
| 26–33 | 0.88–1.10 | LANDING: face disc pops 1.0 → 1.06 → 1.0; mint disc backing + disc shadow appear under it | — |
| 26–38 | 0.86–1.28 | connector draws 1 → 6 (4 px charcoal); discs 2–6 pop 0 → 1.12 → 1 as the tip arrives (2 f stagger: peaks 1.017, 1.083, 1.150, 1.217, 1.283), glyphs 2 f after their disc | structural pop ~1.02 |
| 28–36 | 0.93–1.20 | 'six' then 'habits' (2 f lag) blur up and out | — |
| 35 | 1.17 | 'I'd' (110) pops in top-right | I'd |
| 41–56 | 1.36–1.86 | 'steal' (200, mint) peaks at 1.43; GREEDY TUG: face disc yanks 4 px up-left (3 f), discs 2–6 lean 6 px toward disc 1 with 1 f lag down the chain, settle back.out(2) | steal |
| 49–60 | 1.63–2.00 | 'from them.' (90) lands under 'steal' | from 1.63 / them 1.81 |
| 55–66 | 1.83–2.19 | mint ripple breathes out of disc 1 (1 → 1.5, fades to 0 before the cut); his live face keeps talking in the disc | them |
| 67 | 2.233 | END STATE = SHARED habit chain exactly + 'I'd steal from them.' | — |

## End-state geometry (frame 67 — t4 frame 0 must match)

- Discs: diameter 180, centres (300,560) (620,700) (330,880) (640,1030) (330,1190) (600,1360); discs 2–6 `--brand-deep`
  with white Phosphor-fill glyphs at 46 % (eye, chat-circle-dots, magnifying-glass, folder-open, watch); `--disc-shadow`.
  Measured on frame 67: ring bbox x 210–389, y 470–649 (centre 299.5, 559.5, Ø 180); dark discs centred within 1–2 px of spec.
- Disc 1 = HIS FACE: `#spk` (full 1080x1920 speaker.mp4, video unscaled — `data-push="1"`) with
  `transform-origin: 550px 735px; transform: translate(-250px, -175px) scale(0.236842)` and
  `clip-path: inset(355px 150px 805px 170px round 380px)` (source circle R 380 around (550,735)); mint ring = SVG circle inside
  #spk, 8 px on screen (+1 px past the clip so no footage fringe). Under it: a mint backing disc (`.hc-disc.face`, carries the
  shadow; its microphone glyph is built but `visibility:hidden` — t4's flip reveals it).
- Connector: one path centre→centre 1→6, `--brand-deep`, 4 px, round caps/joins, fully drawn, behind the discs.
- World = frame (no camera transform at the end): `#board` scale 1, `#grid` offset (0,0) (I override the runtime drift so it
  runs (20,12) → (0,0) at the same speed — t4's grid starts at 0,0), `#vig7` (`--vignette-strong`) opacity 1 over the house `#vignette`.
- Words on the last frame (t4 does not need them): 'I'd' (x 404, base 380), 'steal' (right 924, base 495), 'from them.' (right 930, base 578).
- Code: `hf/index.html` → "HABIT CHAIN (v7) — CSS — BEGIN/END" and "HABIT CHAIN (v7) — JS — BEGIN/END".
  `buildHabitChain(world, spk)` builds it; `setHabitChainEnd(chain, spk)` gsap.sets the exact end state (what t4 calls at 0).
  `HC.faceEnd` holds the transform/clip numbers.

## Principles checklist (Lasseter)

- **Contact frames on words**: every word enters on its words.txt time (runtime: hero −0.2 s, pop −0.16, default −0.13); the face lands 'habits'→landing at 0.88, the chain pop on the structural beat, the tug on 'steal' (1.43), the ripple on 'them' (1.83). ✔
- **Anticipation before the hero move**: 3 f push-in 1.0 → 1.015 before the shrink; the face disc yanks back before the chain leans in on 'steal'; hero words sink 3 f before rising. ✔
- **Overshoot + settle**: face disc 1.06 → 1 on landing; discs 0 → 1.12 → 1 (disc 6: 1.06, zone floor); glyphs 1.15 → 1; tug settles with back.out(2). ✔
- **Parts lag the whole**: glyphs 2 f after discs; discs 2 f apart along the line; the tug ripples 1 f per disc down the chain; 'habits' exits 2 f after 'six'. ✔
- **Long moves on arcs**: the shrink's x leads its y (power3.out vs power2.out) → curved path into the slot. ✔
- **Squash/stretch on shapes only**: the face disc's landing pop and the disc pops are shape scales; type is never squashed. ✔
- **One focal point**: 0–0.48 him + caption; 0.48–0.9 the shrinking footage (words sit clear of it); 0.9–1.3 the chain building; 1.3–2.2 'steal' + the tug. ✔
- **Secondary action, no dead hold ≥ 1 s**: live footage in the disc, grid drift, ring draw, ripple, settles; check: no dead holds. ✔
- **One exaggerated hero beat**: the shrink-and-land (footage → disc) is THE beat. ✔
- **Exits faster than entrances**: word exits 6 f (runtime); the shrink is 12 f, the entrance pops 13 f. ✔
- **One light direction / contact shadows**: `--disc-shadow` falls straight down on every disc incl. the face disc's backing. ✔
- **Nothing reads as a static slide**: every frame has something moving (see motion strip). ✔

## Richness (fullscreen beat → expressive type + the one named object)

Hero object: the signature shrink into THE HABIT CHAIN. Secondary micro-animations:
1. Mint ring draws itself round his face as it lands (0.72–0.96) — on 'habits'.
2. Domino build: the connector runs disc to disc and each disc pops as the line arrives, glyph spinning in 2 f later (0.86–1.28).
3. Greedy tug on 'steal' (1.43): face disc yanks, the chain leans toward it and springs back.
4. Mint ripple off disc 1 on 'them' (1.83), gone before the cut.

## Readability

- Zone measured over all 68 frames (diff vs a background-only render with words/world/speaker hidden — `qa/bounds.py`,
  `qa/bounds.txt`; the footage itself is drawn in both, so the diff isolates everything we add): x 70–948, y 286–1481.
  Only exceptions: f15 (0.50 s) — the footage card at the first frame of the shrink, still ~full-frame (planned non-paper footage);
  y 1481 = 1 px of disc 6's soft shadow during its overshoot (geometry fixed by SHARED: disc 6 bottom = 1450).
- IG corner (x > 900, y > 1200): 0 px in every frame except f15 (the full-frame footage itself).
- Sizes: hero 'six' 200, 'steal' 200; supporting 'habits' 165, 'I'd' 110, 'Here are' 100, 'from them.' 90 (all ≥ 64 authored; × 0.94).
- No semi-transparent text except the 6 f runtime exits/entrances; no ghost lines left under the next phrase.
- Nothing over the face: 'Here are' sits on his chest; 'six' rises over the ceiling/hair top-right before the shrink; 'habits' only appears once the face circle has moved left of x 490.
- No marker layer, no Caveat, no red; clean vector strokes only (connector, ring).

## Deviations

- Type sizes: 'six' 200 (brief ~230) and 'habits' 165 (brief ~190) — the only free space that never touches the chain is the
  top-right pocket x 400–960 / y 285–600 (disc 2's top is at y 610); at the brief sizes the pair either left the zone on the hero
  overshoot or touched disc 2's pop. 'steal' 200 and the rest are at brief size.
- 'six' briefly overlaps the top of his hair (not the face) during 0.33–0.48, before the shrink.
- marker.css/marker.js are no longer included (v7 forbids the marker layer); runtime files themselves untouched.
- Grid drift overridden to end at (0,0) (seam match with t4); the runtime's own drift tween is still there, mine wins.
- Shrink is driven by one pure function of time (a clock tween on the timeline, `onUpdate → apply(t)`) — seek-safe; its eases live inside the function.
- Disc 6 overshoot 1.06 instead of 1.12 (its shadow sits on the zone floor).
- Contacts: chain pops span 1.017–1.283 (structural pop tagged at 1.02, brief "~1.05").
