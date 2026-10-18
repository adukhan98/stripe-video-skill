# v07_outcome — CHAPTER ① "ask for the outcome instead of the task" (blank, bespoke, no speaker)

> **RETIMED (coordinator, dead air cut):** the scene is now **69 frames** (data-duration 2.2833). The 0.2333 s before "First" was
> cut, so EVERY time in this file below this note is 0.2333 s later than built — subtract 0.2333 s. Word times now: First 0.217,
> ask 0.497, for 0.677, the 0.797, outcome 1.157, instead 1.517, of 1.677, the 1.777, task 2.097. Hero hit 1.157; loop 0.087
> (dur 0.32); "1" pop contact 0.167; rings 0.747–1.067; arrow 0.927–1.07, snap 1.157, shiver to 1.657; recede 1.887; strike pass 1
> 2.107–2.197, return pass 2.20–2.25 (finishes by 2.25). Frame 0 is still paper only. Re-measured over all 69 frames: **x 67–956,
> y 294–1474**. slots.py check passes, motion "no dead holds", ffprobe 69. beats.json shifted by −0.2333.
> Chapter-number code for v10/v13: same geometry, loop call is now `M.circle(198, 428, 108, 112, 0.087, { width: 11, dur: 0.32, tilt: -6, seed: 7101 })`
> with the digit `data-t` = word − 0.05 and the loop at word − 0.13 (pattern unchanged).

## Key poses (planned before authoring; scene seconds / frame @30)

| t | f | on screen | lands on |
|---|---|---|---|
| 0.00 | 0 | paper + drifting grid only (hard cut in) | — |
| 0.40 | 12 | ink "1" (Inter Tight 900, 210 authored) pops top-left, digit centre ≈ (198, 428) | "First" (0.45) |
| 0.32–0.64 | 10–19 | red marker loop draws round the "1" | "First" |
| 0.45 | 13–14 | "first" (800, 90) beside the loop | "First" |
| 0.73–1.03 | 22–31 | "ask for the" (800, 100) left, under the ① | "ask" / "for" / "the" |
| 0.98–1.30 | 29–39 | black-marker target: 3 rough rings draw outer → inner, centre (560, 880) | "the" → "outcome" |
| 1.16–1.30 | 35–39 | red arrow (shaft + fletching) draws nocked up-right of the target, pulls back (anticipation) | — |
| 1.39 | 42 | HERO: arrow thunks into the bullseye, bullseye floods red hatch, impact ticks, target jolt, camera shake + 1 % punch; giant red "outcome" peaks | "outcome" |
| 1.39–1.85 | 42–55 | arrow wobbles about its tip (damped), "outcome" settles | — |
| 1.75–2.01 | 52–60 | "instead of the" (800, 84) lower-left | "instead" / "of" / "the" |
| 2.33 | 70 | "task" (900 ink, 170) pops lower-right; target recedes a touch (object only) | "task" |
| 2.34–2.50 | 70–75 | red two-pass scribble-strike through "task" (rides the word; it stays readable) | "task" (strike on 2.45) |

## SHARED CHAPTER-NUMBER CODE (v07 ① — copy verbatim into v10 ② / v13 ③, change only the digit, the word and its times)

HTML (inside `#punch`, before the other lines):

```html
<div id="lNum" class="line hero ink" data-cx="198" data-base="500" data-size="210">
  <span id="wNum" class="w" data-t="0.40" data-pop>1</span>
</div>
<div id="lFirst" class="line sup" data-x="350" data-base="466" data-size="90">
  <span class="w" data-t="0.45" data-accent>first</span>
</div>
```

JS (after `const M = Marker.init(P)`), loop starts ~0.08 s before the digit's contact frame:

```js
M.circle(198, 428, 108, 112, 0.32, { width: 11, dur: 0.32, tilt: -6, seed: 7101 });
```

Geometry: digit centre ≈ (198, 428), 210 authored (197 px on screen), loop rx 108 / ry 112 (≈ 240×250 drawn incl. the spiral-out);
word at x 350, baseline 466, Inter Tight 800, 90 authored. Measured: loop's left edge x ≈ 67, top y ≈ 293 incl. shake/push — do
NOT move it further up/left. Use seed 7101 in every chapter scene so the loop is the same drawing (v10/v13 may keep it, the
digit differs). Timing pattern: digit `data-pop` at (spoken word − 0.05), loop at (word − 0.13), word `data-accent` at word time.

## As built (scene seconds)

- 0.19–0.40 "1" pops (data-pop, contact 0.40); 0.32–0.64 red loop draws round it, boils on fours to the cut.
- 0.29–0.45 "first" (data-accent) lands beside it.
- 0.57 / 0.78 / 0.90 "ask" (pop) / "for" / "the" land, x 90, baseline 664, 100 authored.
- 0.98–1.13 outer ring, 1.12–1.23 middle ring, 1.22–1.30 inner ring (black marker, seeds 7201–7203), target group lands with
  0.94 → 1.02 → 1.0 scale (anticipation → overshoot → settle) about the bullseye (560, 880).
- 1.16–1.30 red arrow draws nocked 80 px up-right of the target (shaft seed 7301, 4 fletching strokes 7311–7314);
  1.24–1.36 pulls back to 104 px (anticipation); 1.29–1.33 two red speed lines.
- 1.39 HERO CONTACT: arrow snaps in (power4.in, 3 f) and sinks 10 px past (then back), target squashes (0.965 × 1.025, 2 f) and
  springs back, 3 red thunk ticks flick out on the far side, P.shake(3 px) + P.punch(1 %); "outcome" (900, red, fit 850, peak
  1.08) peaks on the same frame. 1.40–1.54 bullseye floods red hatch.
- 1.39–1.89 arrow shivers about its tip: 6° → −4.5 → 3 → −1.8 → 0.8 → 0 (3 f each, damped). 1.98 thunk ticks wiped (0.1 s).
- 1.62 / 1.78 / 1.88 "instead" / "of" / "the" (84 authored, baseline 1334).
- 2.12–2.42 target group recedes to 0.84 opacity (object only, words untouched) as focus moves down.
- 2.17–2.33 "task" (900 ink, 170, data-pop, rise 26) pops low-right; 2.34–2.43 red strike pass 1, 2.45–2.50 return pass —
  both drawn in an svg INSIDE the word span, so the strike rides the word's settle; "task" stays readable under it.
- Everything boils to the hard cut (frame 75).

## Principles checklist

- Contact frames on words: yes — 1 (0.40)/first (0.45), ask 0.73, outcome + arrow hit 1.39 same frame, task 2.33, strike on 2.45.
- Anticipation before the hero move: arrow pulls back 24 px (1.24–1.36) before the snap; target shrinks before its land;
  "outcome" uses the runtime's hero anticipation dip.
- Overshoot + settle: outcome peak 1.08 → back.out; arrow sinks 10 px past and returns; target 1.02 → 1.0; task 1.05 → 1.0.
- Parts lag the whole: rings stagger outer → inner; fletching lags the shaft 1–2 f; speed lines 1 f apart; thunk ticks 1 f apart;
  "ask/for/the" and "instead/of/the" stagger on their word times.
- Long moves on arcs: the only travel is the arrow's 114 px straight flight (an arrow flies straight — exception noted); its
  wobble is rotational about the tip.
- Squash/stretch on shapes only: target squashes on the hit; no type is squashed.
- One focal point: number → ask → target/arrow → outcome → task; the target recedes (opacity 0.84) when "task" takes focus.
- Secondary action / no dead hold ≥ 1 s: grid drift, camera push, line boil on every stroke, arrow shiver, staggered words;
  slots.py motion: "no dead holds".
- One exaggerated hero beat: the arrow thunk on "outcome" (impact, shake, 1 % punch). Nothing else is exaggerated.
- Exits faster than entrances: no exits needed (hold to the cut); speed lines and thunk ticks wipe in 0.1 s.
- One light direction / contact shadows: flat marker drawing on paper, no objects with shadows in this scene.
- Not a static slide: every frame has something drawing, boiling or settling.

## Richness

- HERO object: the hand-drawn target + red arrow that thunks into the bullseye on "outcome" (anticipation pull-back, speed lines,
  hit, sink, damped shiver, bullseye floods red, target squash, thunk ticks).
- Micro 1: the ① chapter loop drawn round the "1" on "First" (shared chapter style).
- Micro 2: "task" crossed out by a two-pass red scribble-strike that rides the word (lands 2.45).
- Micro 3: the target lands with weight while drawing (scale anticipation/overshoot) and recedes as "task" takes focus.

## Readability checks

- Zone measured over all 76 frames (diff vs a background-only render, qa/bounds.py): **x 67–956, y 293–1474** — inside
  x 60–960 / y 285–1480 incl. shake, punch and push. (First pass had task's rise reach y 1487 at f66 → rise 26; fixed.)
- Sizes (authored): 1 = 210, outcome = 250 → fit to 850 (≈ 229 on screen settled ~856 px wide), task = 170, ask for the = 100,
  first = 90, instead of the = 84. Nothing under 64.
- No semi-transparent text: words only fade during their 0.16–0.2 s entrances; the only dimming is the target drawing (object).
- No real page/strip in this scene; no notes; no speaker card (no face, no clothing).
- Marker never crosses words: loop clears the digit; rings/arrow/ticks sit between "ask for the" and "outcome"; the strike on
  "task" is the intended cross-out (word stays legible).
- Lower 40 % of the zone (y ≥ 1002): the target's bottom from 1.0 s, "outcome" from 1.2 s, then "instead of the" + "task".
  0–1.0 s the lower zone is empty (the scene opens on the ① chapter beat at the top) — accepted, see Deviations.

## Deviations

- No speaker card / `speaker.mp4` video element removed (brief: "No speaker (2.5 s chapter beat)"); root data-duration kept
  (2.5167). The asset file is left untouched.
- Lower zone empty for the first ~1.0 s (chapter number + "ask for the" build top-down before the target draws).
- "first" shown lowercase without the comma (brief: small 'first').
- Arrow flight is straight, not an arc (an arrow flies straight); flight kept short (≈ 114 px) so the nocked arrow stays in zone.
- Target recede is opacity 0.84 only (no blur) — SVG group.
