# v09_bigger — OPINION (portrait): "The model can handle the bigger goal. Most of us just don't ask for it."

102 frames @30 (3.400 s). Runtime untouched (paper.js / marker.js). Everything bespoke lives in `hf/index.html`.

## Key poses (scene seconds)
| t | pose |
|---|---|
| 0.00 | portrait card (700x700, face centred, navy hoodie, whole head in) already on screen; "the" lands 0.05 |
| 0.27 | "model" pops (ink 100) |
| 0.50-0.99 | small black-marker target (3 rings, scale 1/3) draws in beside the card top-right; "can" 0.53, "handle" pops 0.83 |
| 0.95 | intro lines exit (6 f) |
| 1.00-1.09 | ANTICIPATION: target squeezes 0.333 -> 0.30 |
| 1.19 | HERO: "bigger" (red 240) lands with overshoot 1.12 -> 1.0 AND the target grows 3x (0.30 -> 1.06 -> 1.0). Impact + 1.2 % camera punch + 4 f shake. "the" (ink 100) above it from 0.99 |
| 1.18-1.50 | red arrow flies in on an arc and thunks into the bullseye on "goal" (1.47); arrow wobbles 3 keys, red bullseye hatch, 3 sparkle ticks |
| 1.47 | "goal." ink 170 lands bottom-right |
| 1.50-1.62 | "the" / "bigger" / "goal." exit up (6 f, faster than the entrance) |
| 1.77 | "most of us" (ink 100) lands on the paper under the card |
| 2.20-2.50 | target + arrow shrink back to 0.62 and dim (OBJECTS recede, never words): most of us ask for little |
| 2.23 | "just" pops |
| 2.51 | "don't" (ink 200) lands |
| 2.91 | "ask" (red 200) lands, letters ripple, 0.8 % punch |
| 2.95-3.25 | red double underline scribbles under "don't ask" |
| 3.09 / 3.33 | "for" / "it." land low-right; hold alive (card float, target sway, boil) to the cut |

## Principles checklist
- Contact frames on words: every `.w` has `data-t` = the spoken time; entrances start 0.13-0.2 s early (runtime). Target grow contact = 1.19, arrow contact = 1.47.
- Anticipation: runtime hero/pop dip before every landing; target squeezes 0.333 -> 0.30 before the 3x grow.
- Overshoot + settle: "bigger" peak 1.12 -> 1.0; target 1.06 -> 1.0 (back.out); arrow wobble -5 / +3 / -1.5 / 0.
- Parts lag the whole: "bigger" letters swell 2 f apart after landing, "ask" letters ripple, sparkle ticks 2 f apart, goal exits 2 f after bigger, can/handle exit lag 2 f.
- Arcs: arrow is a bent curve (`M.arrow` bend 0.14); runtime words rise on arcs.
- Squash/stretch: only on the target/arrow shapes (scale squeeze/stretch), never on type (type only scales as the runtime's hero overshoot).
- One focal point: intro -> bigger+target -> (target recedes) don't ask. Phrases exit before the next lands; the target dims/shrinks when "don't ask" takes over.
- Secondary action / no dead hold: grid drift, camera push, card float + 3D settle, target breathes while small, target sways in phase B, marker boil on fours, letter ripples.
- ONE exaggerated hero beat: 1.19 (target 3x + "bigger" + impact/punch/shake).
- Exits faster than entrances: all exits 6 f.
- One light direction / contact shadows: runtime card shadow only; no extra shadows.
- Not a static slide: something moves on every 4 f window (check: slots.py --motion "no dead holds").

## Richness
- Hero object: black-marker TARGET (3 rings, seeded) that grows 3x on "bigger" + red arrow thunk on "goal" (hatch bullseye, sparkle ticks).
- Micro 1: per-letter ripple/swell of "bigger" (1.42) and "ask" (3.06).
- Micro 2: target shrinks back + dims on "just/don't" (2.2) — the doodle acts out "most of us don't ask".
- Micro 3: red double underline scribble on "don't ask" (2.95) + 0.8 % punch on "ask".
- Micro 4: small target draws itself on during "can handle" (0.5-0.8).

## Readability
- Zone measured over all 102 frames (see report) against a background-only render: x 60-960, y 285-1480.
- No words over his face; no word touches the hoodie (card is 700x700, words sit on bare paper below it).
- Type authored: bigger 240 (hero), goal 170, don't/ask 200, supporting 100-110, smallest 90 ("for it."). Scaled by the house 0.94.
- No ghosted text: every word is full-ink/red or in its 6 f exit; objects (target) recede, not words.
- No notes/handwriting in this scene; no real pages; marker width 11-14.

## Deviations
- Card is 700x700 (brief ~760x860): a taller card put the chin-to-chest area where the words must sit, and the navy hoodie needs a solid strip; instead the card stops under the shoulders and all words sit on bare paper (no `.paper-strip` needed). An earlier version with a strip looked like a pale box.
- The target is drawn over the card's top-right corner (background area of his room, not near his face).
- Words near the bottom enter from above (`data-rise` negative) so the entrance never leaves the zone.
- "the" appears twice (the model / the bigger) as spoken.

## As-measured (final, after review fixes)
- Frames: 102 (ffprobe). `slots.py check --motion`: passed, no dead holds.
- Bounds over ALL 102 frames (diff vs background-only render, streamed): x 65-955, y 291-1475, 0 violations.
- Review fixes: intro "the model can handle" exits in 5 f (0.86 -> 1.027) before "bigger" starts (0.99); "bigger" drops in from above (rise -40) and the lines no longer share space (intro y>=1328, bigger y<=1318). "most of us just" sits right-aligned at y 1100, x>=~280 (no glyph of "bigger"/"goal." under it); "the"/"bigger" exit 1.5, "goal." 1.58 (5 f each) so no frame overlaps.
- "for it." is now a 110 ink line (right-aligned, base 1468) under the double underline; "for" 3.07, "it." 3.27 so "it." is on screen ~0.13 s fully before the cut.
- Don't ask is 190 authored (hero >= 170), base 1335.


## v6 style pass — Mode A (split)
- Card replaced by `<div class="spk split" data-h="960">`: footage edge to edge in the top half from frame 0 (face centred, no border/tilt/float/shake).
- Everything else lives on the paper in the bottom band (y 1000-1480, x <= 900 below y 1200): "the model can handle" (y 1180/1290), "the bigger goal" ("the" 1092, bigger red 240 base 1295, goal. ink 170 right-aligned 890), "most of us just" (y 1092) / "don't ask" (190, base 1310) / "for it." (110, right 880) with the red double underline.
- The black-marker target now sits at the top-right of the band (centre 830,1100; rings 98/63/29, never touching the footage): draws small (x0.333) during "can handle", squeezes at 1.0, grows 3x on "bigger" (1.19) with overshoot, red arrow thunks in on "goal." (1.47), shrinks/dims back on "just" (2.2).
- Same 102 frames, same word times. Dropped: sparkle ticks (decor), camera shake (would expose the footage's top edge), scribble beats (SOP). Punch kept (1.2 %).
- Two-element guideline: only the target + the current phrase on screen (phrases exit in 5 f before the next); lower ~40 % of the band stays paper.

### Mode A as-measured (final)
- Frames 102 (ffprobe); `slots.py check --motion` passed, no dead holds.
- Bounds of everything below the footage (y >= 970, diff vs background-only render, ALL 102 frames): x 65-961, y 988-1471. Only one frame (48, t=1.6 s) leaves the band: the red arrow's tail during its thunk wobble reaches x 961 (1 px past 960) and y 988 (12 px above 1000, still 28 px under the footage edge). Every other frame is inside x 65-955, y 1000-1471.
- Final geometry: target centre (840,1112), rings 92/60/28 (grows to 1.06 then 1.0), bigger x 112 base 1295, goal right 890.
