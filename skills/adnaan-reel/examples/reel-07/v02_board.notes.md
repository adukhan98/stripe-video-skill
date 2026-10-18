# v02_board — THE BOARD (first draw) — v6 Mode B (full canvas, no speaker)

122 frames (data-duration 4.0500). Blank starter on the shared runtime (paper.js / paper.css / marker.js untouched).
v6 pass: the small speaker card (and its video element) is gone; THE BOARD block is byte-identical to the v5 pass
(geometry, seeds, timings, final state); the freed space went to a wide, readable notebook and bigger type.
Focal pairs: board + "two problems" (0–1.1) → notebook + copies/"homework" (0.8–3.0) → board ✓ + "solved both" (3.1–4.05).

## Key poses

| frame | t | on screen | word |
|---|---|---|---|
| f0–16 | 0.00–0.54 | black-ink board frame draws like a hand (top, right, bottom, left), then the chalk ledge | He |
| f7–23 | 0.22–0.75 | wide white notebook card slides up at the bottom (tilted −2°, ruled, red margin, holes) | copied |
| f12–24 | 0.40–0.80 | "1." + problem-1 squiggle write themselves | copied two |
| f18 | 0.59 | "two" (ink 160) lands under the board, left | two |
| f23–34 | 0.76–1.12 | "2." + problem-2 squiggle write themselves | two problems |
| f30 | 0.99 | "problems" (ink 150) pops in, staggered right of "two" | problems |
| f24–47 | 0.80–1.55 | dotted arc draws down the RIGHT gutter; small copies pop out of the board, ride it and write into the notebook | problems off the board |
| f55–71 | 1.84–2.36 | the notebook's tab rises out from behind the page | thinking |
| f76–89 | 2.52–2.96 | "homework" written on the tab (Caveat ink 80), tape slaps on (2.86) | homework |
| f89 | 2.98 | "two problems" exits fast | And |
| f94–100 | 3.14–3.34 | red ✓ 1 on the board | solved |
| f99 | 3.31 | "solved" lands (180, full width under the board) | solved |
| f101–107 | 3.38–3.56 | red ✓ 2 on the board | both |
| f108 | 3.59 | "both" RED lands + 0.8 % punch = HERO BEAT | both |
| f111–121 | 3.70–4.03 | red underline under "both"; notebook nods; boil/float to the cut | of them |

## Layout (frame px)

- THE BOARD (black ink, no camera push): frame (114–952, 324–777), ledge y 800 (x 140–940); problems on y ≈ 450 / 620;
  red ✓ at (870,450) / (820,620), size 84.
- "two" 160 hero ink (x 84, base 932) / "problems" 150 hero ink (x 150, base 1050) — staggered under the board, left of
  the arc gutter (x ≥ 790). "solved both" 180 hero (x 84, base 1010, data-fit 880 → full width), "both" RED + underline.
- Notebook #nb x 120–930, y 1158–1420 (810×262), rotated −2°, ruled (wire grey) at 106/200/244, red margin, 3 holes,
  soft shadow; tab 300×104 on its top-right (x ≈ 620–920, visible y ≈ 1082–1158) with "homework" Caveat ink 80 + tape.
  Copies at 0.8 scale on rules 106 / 200 (≈ 464 px wide — readable as two written lines).
- Dotted arc (ink 6 px, "1 15") in the right gutter: M 790 818 → (884,1020) → (800,1150).
- White space: left of the board/words margin, the right gutter after 1.9 s, and the band y 1430–1480 stay empty.

## As built (scene seconds)

- 0.001 / 0.12 / 0.22 / 0.34 / 0.45: board top, right, bottom, left edges, ledge (0.12/0.10/0.12/0.10/0.09 s each).
- 0.22–0.75 notebook cardIn (y 30, tilt −4° → 0 on top of its −2° rest tilt, overshoot, settle), float 3 px.
- 0.40 "1." (Caveat 64), 0.48–0.80 problem 1 (8 strokes); 0.76 "2.", 0.82–1.12 problem 2 (7 strokes).
- 0.59 "two" (hero: anticipation sink, 106 % overshoot, settle); 0.99 "problems" (pop).
- 0.80–1.12 dotted arc draws, marches to 1.82, fades 1.76–1.92.
- Copy 1: 0.82 pops out of the board's empty bottom strip at (610,718) (scale 0 → .32 → .26), rides the arc 1.02–1.30
  (sine.inOut motion path via (780,800) (812,960) (760,1225), curviness 0.7, entering the page at line height), grows to 0.8 + tilts −2° onto notebook line 1; 1.26–1.48 written into the notebook; squash 1.30.
- Copy 2: 1.13 pops at (640,718), rides 1.33–1.55 (via … (760,1300), under copy 1), lands on line 2 on "board" (1.55); written 1.50–1.70; squash 1.55.
- 1.84 tab anticipation dip (3 f) → 1.94 rises with overshoot → settles 2.36 ("thinking").
- 2.52–2.96 "homework" written on the tab; 2.86 tape slaps on (back.out).
- 2.98 "two problems" exit up 16 px + blur (6 f, 2 f lag) — clears before "solved".
- 3.14–3.34 red ✓1; 3.31 "solved" (hero); 3.38–3.56 red ✓2; 3.59 "both" RED (hero, peak 110 %) + 0.8 % punch anchored at
  (780,880), back to 1.0 by 3.96 (board at exact frame px on the last frame); 3.60–4.08 notebook nods −3.2° → −2°.
- 3.70–3.92 red underline under "both". Continuous to the cut: boil on fours on every stroke, notebook float, grid drift.

## THE BOARD — exact code for v03 (copy verbatim; unchanged by the v6 pass)

Copy the block between `// ===… THE BOARD` and `// ===… /THE BOARD` from `hf/index.html` (functions `boardRng`,
`cursive`, `boardProblems`, `board`) and call it right after `const M = Marker.init(P)`:

    board(M, null);   // everything drawn at t = 0 = v02's final state

- Frame seeds 701 (top 114,331→950,329), 702 (right 948,324→950,772), 703 (bottom 952,770→116,772), 704 (left
  120,777→121,326); ledge 705 (140,800→940,800, width 10). Ink width 11, amp 1.8, `texture: false` (the felt-tip filter's
  bbox region clips straight strokes thin). Right edge centre-line x 950 (not 960) so the ink stays ≤ 960.
- Labels: `M.note("1.", 166, 413, …, {size:64, rot:-3, color:"ink"})`, `"2."` at (166, 583).
- Squiggles: loop shapes from rng seeds 711 / 712 (`boardProblems()`), strokes seeded 7110+k / 7120+k, ink width 7,
  amp 1.1, texture only on curved strokes (`pts.length > 2`).
- Checks: `M.check(870, 450, 84, …, {seed:721, width:12})`, `M.check(820, 620, 84, …, {seed:722, width:12})`.
- v03 must keep `#cam data-push="1"` (or start its board at scale 1) and declare Caveat. Verified: a t = 0 render of
  `board(M, null)` vs v02's last frame, board region — only boil-variant + grid-drift differences; `qa/seam_pair.png`.

## Principles checklist

- **Contact frames on words**: "two" 0.59, "problems" 0.99, "solved" 3.31, "both" 3.59 via runtime data-t; ✓ strokes start
  0.17 / 0.21 s before solved / both; "homework" note starts 0.15 s before the word; copy 2 lands on "board"; tab on "thinking".
- **Anticipation**: hero words sink before rising; tab dips 3 f before it rises; copies pop (scale 0 → overshoot) before travelling.
- **Overshoot + settle**: hero words 106/110 %, cardIn, tab −6 px → 0, tape back.out, copies .32 → .26.
- **Parts lag the whole**: board strokes one after another like a hand; "problems" exit lags "two" 2 f.
- **Arcs**: copies travel a curved motion path down the right gutter while scaling and tilting into the notebook.
- **Squash/stretch on shapes only**: notebook squash 4 % on each copy landing; no type squashed.
- **One focal point / two-element guideline**: board + "two problems" → notebook + copies/"homework" → board ✓ + "solved
  both". No speaker, no extras; nothing recedes (no ghosted words).
- **Secondary action, no dead hold ≥ 1 s**: slots.py "no dead holds"; boil, float, grid drift, arc march, nod.
- **One exaggerated hero beat**: "both" RED + 0.8 % punch + impact.
- **Exits faster than entrances**: "two problems" 6 f exit vs 10–16 f entrances; arc fades in 5 f.
- **One light direction**: card shadows down; the marker world is flat ink.
- **Not a static slide**: something draws, rides, rises or lands every ≤ 0.5 s.

## Richness

- HERO: the blackboard draws itself in ink (0–0.54), two squiggle problems write themselves with "1." "2." (0.40–1.12),
  then two red ✓ on "solved both" (3.14 / 3.38).
- MICRO 1: notebook slides in on "copied"; small ink copies pop out of the board and ride the dotted arc into it, writing
  themselves on its ruled lines (0.82–1.70); its tab rises on "thinking"; "homework" written + taped (2.52 / 2.86).
- MICRO 2: the notebook nods on "both"; red underline under "both" (3.70).

## Readability

- Zone measured (diff vs background-only render `qa/bg.mov`, threshold 24, every frame, `qa/bounds.py`):
  **x 72–958, y 314–1451, 0 frames outside x 60–960 / y 285–1480** (incl. riders, notebook shadow, punch).
- No strips. No semi-transparent text: words enter/exit in ≤ 6 f; nothing ghosted.
- Kinetic: "two" 160, "problems" 150, "solved both" 180. Handwriting: "homework" Caveat ink 80, labels "1." "2." Caveat
  ink 64. Notebook copies at 0.8 (stroke 7). Squiggles are illustrative (not readable claims).
- Marker strokes never cross words (arc + copies stay in the right gutter x ≥ 790 while the words end at x ≈ 770).
- Lower 40 % of the zone (y > 1002) holds the words + notebook from 0.25 s to the cut.

## Deviations

- Board right edge centre-line x 950 (SHARED says 960) so the 11 px ink + jitter stays ≤ 960.
- Camera push disabled (`#cam data-push="1"`) so the board is at exact frame px at the cut (v03 continuity); the hero punch
  is short (0.8 %, back to 1.0 by 3.96 s).
- Straight board strokes use `texture: false` (the runtime felt-tip filter clips straight lines thin); curves keep it.
- Notebook uses its own softer shadow (0 22px 34px −14px) instead of `--card-shadow`, so it can sit lower without its
  shadow spilling past y 1480.
- v6: no `scribble` beats (sparse structural SFX only).

## QA (v6 pass)

- `slots.py check --motion --at 0.45,0.59,0.99,1.3,1.95,2.67,3.31,3.59`: checks passed, no dead holds. ffprobe: 122 frames.
- Bounds x 72–958, y 314–1451, 0 violations. Seam: v02 last frame vs `board(M, null)` at t = 0, board region mean Δ 5/255
  (boil variant + grid drift only) — the board block is unchanged from the v5 pass.
