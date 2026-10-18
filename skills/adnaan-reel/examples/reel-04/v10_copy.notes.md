# v10_copy — "copy in minutes" (MECHANISM)

Full-screen opaque scene, 1080x1920 @30, authored 8.5 s = exactly 255 frames (placed at frame 1492; next scene at 1747). Paper bg + 60px grid + vignette
(identical to v01_hook) on every frame; first/last frame alpha 255. Content zone x 60–960, y 285–1480.

## Key poses (written before animating)

| frame | t (s) | on screen | lands on |
|---|---|---|---|
| f0 | 0.00 | deep-teal app card (shown 564x679 at x80 y740, art drawn at 490x590 ×1.15) 30% visible, rising with a 3D settle | "because" |
| f10 | 0.32 | "your app" black pill pops on the card corner; "if an" (Newsreader 84) top | "if" 0.32 |
| f20 | 0.68 | "AI" Fraunces italic ink 190 peaks; agent puck (253, centre ~796,1080) pops in at right | "AI" 0.68 |
| f33 | 1.10 | "agent" peaks; puck settles, eyes light ocean + glow | "agent" 1.10 |
| f40–56 | 1.34–1.88 | "if an" gone; "AI agent" recedes; "can look at your" builds; puck eyes turn to the card | "can…your" |
| f66 | 2.20 | LOOK 1: ocean scan cone sweeps the whole card, glow + wash + bump; "app" Fraunces italic ocean 220 | "app" 2.20 |
| f72–86 | 2.40–2.86 | repeated "can look at your" hop word by word; "app" clears | repeats |
| f98 | 3.28 | LOOK 2: scanline wipes the card to its code layer (mono bars); "software" Fraunces italic ink 192 | "software" 3.28 |
| f107–117 | 3.55–3.91 | "can look at" hop again; "your" lifts away | repeats |
| f124/129 | 4.13/4.29 | "all the" Fraunces italic ocean 120 in place of "your" | "all", "the" |
| f140 | 4.65 | LOOK 3: scan wipes to feature rows, four ocean ✓ pop row by row; "features" Fraunces italic ocean 190 | "features" 4.65 |
| f148–160 | 4.94–5.35 | beat A type clears; card compacts left; puck docks centre; speaker card rises top | — |
| f158 | 5.27 | light translucent COPY peels off the card; dotted path draws; "build" | "build" 5.27 |
| f168 | 5.61 | copy mid-arc over the puck; "someone else" pill popped at the destination | "someone" 5.61 |
| f176 | 5.85 | copy lands under the pill (squash + settle), solid | "else" 5.85 |
| f189 | 6.31 | "version" Fraunces italic ink 200; copy sheen + hop | "version" 6.31 |
| f222–249 | 7.40–8.31 | type clears; stopwatch ring (r 92) around the puck; ocean arc sweeps a full circle; "a couple of" Newsreader 96 (baseline 1268) | "couple" 7.67 |
| f249 | 8.31 | ring complete + crown press + puck pop + 1% camera punch; "minutes." Fraunces italic ocean 204 | "minutes" 8.31 |

## As built (scene seconds)

- Beat A group (card + puck) spans y ~740–1450 (card 564x679, soft shadow 0 26px 40px -16px), text stays at the top.
- Card: 0.00–0.62 rise 50px, scale .86→1, rotX 26→4, rotY −14→7; float 4px. Pill 0.32.
- Words: if 0.32, an 0.38, AI 0.68, agent 1.10 (hero), can 1.34, look 1.56, at 1.76, your 1.88, app 2.20 (hero),
  software 3.28 (hero), all 4.13, the 4.29, features 4.65 (hero), build 5.27, someone 5.61, else 5.85, a 6.07,
  version 6.31 (hero), a 7.59, couple 7.67, of 7.95, minutes. 8.31 (hero). Each entrance starts 0.13–0.2 s early.
- Repeat hops: can 2.40/3.55, look 2.56/3.71, at 2.68/3.91, your 2.86. "your" exits 3.86.
- Exits: "if an" 1.03; "AI agent" recedes 1.24, clears 1.80; app 2.92; software 4.20; features/all the/can look at 4.94–5.04;
  version 7.32, build… 7.39.
- Puck: pop 0.62 (peak ~0.92), eyes lit 1.06, blink 1.30, eyes turn 1.48; leans into each look.
- Looks (sine.inOut sweeps, cone + dotted edges + in-card scanline): 1.94–2.44, 3.03–3.53 (→ code layer), 4.36–4.86 (→ ✓ rows).
- Beat B: card compacts 4.92–5.38 to scale .5 (282x340, centre 240,950; pill follows to y 744); puck docks 4.94–5.38 (scale .54, arcs over); speaker card 4.98–5.6
  (v01 3D settle, sheen), face-centred crop 27–67% of source height. Dotted path draws 5.22–5.62, dots march to the end.
  Copy: appears 5.20 light/translucent, peels 5.22, rides the arc 5.38–5.84, solid by ~5.88, squash on contact 5.84.
  "someone else" pill 5.46 (bounce 5.84). Sheen on "version" 6.14.
- Timer: ring in 7.40, cards dim to 72% 7.42, arc sweep 7.60–8.26, ring pulse/crown press/puck pop 8.24–8.34, cards back
  to 100% 8.26, punch 1.01 at 8.26. Holds alive to the hard cut.
- Ends: "a couple of" (96, baseline 1268) / "minutes." (204, baseline 1466) fill the bottom of the zone.
- Continuous: grid drift 20px, camera push 1.0→1.014, card/copy/puck/speaker floats, video push.

**Measured content bounds over all 255 frames** (diff vs. a background-only render, threshold 14/255):
x 60–960, y 288–1480 — inside the zone.

## Deviations

- "because" and "of it in the matter of" are not on screen (omitted, not paraphrased). "if an" + "AI agent" shown before
  the first look so the top isn't empty while the puck arrives.
- "can look at your" is one persistent line whose words hop on each repetition; "your" swaps for "all the" in look 3
  (so "all the" is 120 px on line 1 and "features" 190 px on the hero line rather than one 170 px phrase — 170 px would not fit).
- "minutes." is 204 px (−0.03em), not ~240: at 240 the word is ~1000 px wide and breaks x 960 with the overshoot. Centred.
  "software" 192 px (−0.03em) for the same reason.
- The timer ring is a stopwatch ring around the docked puck (between the two cards) rather than a free-standing ring —
  it keeps clear of the type and says "the agent did it in minutes".
- Speaker card is 560x400 (not 390) so more of the face fits; slight hair crop at the top, chin kept.

## V2 revision (type system + bigger speaker card) — current render

- Type: Inter Tight (hero 900 / −0.045em, supporting 800 / −0.03em, line-height .88), accent = colour, no italics.
  Ocean: "app" 220, "features" 190, "minutes." ~207 (fit to 820 px, centred), "all the" 120. Ink: "AI agent" 190,
  "software" ~198 (fit to 790 px), "version" 200. Supporting: "if an" / "can look at your" / "build someone else a" 84,
  "a couple of" 96. Hero lines auto-fit to a max width in JS (data-maxw) before baseline layout; all heroes ≥ 170 px.
- Pills ("your app", "someone else") Inter 600 36 px. Font assert: 900/800/700 "Inter Tight", 500/600 "Inter".
- Beat B speaker card 640x506 at x190 y324 (was 560x400); source scaled to 640x1138, window 18.5–63 % of the source
  height → full head with hair kept, face centred horizontally; inner push zooms from 50 % 85 % so the hair never crops.
- Beat B row moved down to make room: cards at scale .42 (centre y 1040), pills y 862, timer ring r 80 at (515,1040),
  dotted path "M366,990 C428,862 602,862 664,990". Text: "build someone else a" baseline 1290 / "version" 1466;
  "a couple of" 1274 / "minutes." 1460.
- Removed the 1 % camera punch on "minutes." (the taller speaker card sits at the top of the zone); the payoff is the
  word's overshoot + timer pulse + puck pop.
- Measured bounds (full-res diff vs. a background-only render with the video removed), all 255 frames:
  x 63–960, y 285–1477.
