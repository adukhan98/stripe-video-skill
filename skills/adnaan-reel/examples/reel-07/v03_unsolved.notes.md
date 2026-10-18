# v03_unsolved — THE BOARD + "unsolved" rubber stamp (blank, bespoke) — 87 frames @30

Spoken: "They were two famous unsolved problems in statistics."

## Key poses (planned before authoring; rows updated to the final build)
| t | f | on screen | word |
|---|---|---|---|
| 0.00 | 0 | THE BOARD exactly in v02's final state (frame, ledge, both squiggle problems, "1." "2.", two red ✓), boiling | — |
| 0.03–0.23 | 1–7 | "They were" (84 ink) rises under the board, left | They were |
| 0.41 | 12 | "two" (130 ink) pops right-aligned below; the board labels "1." "2." bob in turn (counting) | two |
| 0.72–1.0 | 22–30 | red marker star draws above problem 1, three ink sparkle ticks flick around it; "famous" (130 ink) lands | famous |
| 1.11–1.30 | 33–39 | the stamp appears in the air above the board (big, tilted, soft shadow far below) and winds up | — |
| 1.41 | 42 | CONTACT: stamp slams to 0.94 over the board's lower half, board jolts 6 px, red dust burst, ✓✓ wobble, punch | unsolved |
| 1.42–1.65 | 43–50 | "They were / two famous" blur up out; stamp settles to 1.0 | — |
| 1.52–1.88 | 46–56 | the real article strip flips up into the lower zone, tape slaps on both ends | problems |
| 1.81 | 54 | "problems" (130 ink) lands where phrase 1 was | problems |
| 1.95–2.6 | 58–78 | highlighter: "They were two unsolved" then "problems in statistics." | in statistics |
| 2.49 | 75 | "statistics." (130 ink) lands right-aligned | statistics |
| 2.9 | 87 | held alive to the cut: boil, grid drift, dust settling | — |

## As built (scene seconds)
- **0.00** THE BOARD in v02's final state. The block between `// === THE BOARD` and `// === /THE BOARD` is copied verbatim from `../v02_board/hf/index.html` (final version: right edge centre-line x 950, straight strokes `texture:false`, ✓ size 84, seeds 701–705 / 7110+k / 7120+k / 721 / 722). It is called as `board(M, null)` right after `Marker.init`. `#cam data-push="1"`, as in v02. Seam: `verify/seam_v02_board__v03_unsolved.jpg` has a mean diff of 18.0 (v02's words, notebook and speaker disappear at the cut). The board-region difference, `qa/seamcmp.png`, shows only boil-variant edges: the geometry is identical.
- **0.03 / 0.23** "They were" (84 ink, x 92, base 958). **0.41** "two" pops (130 ink, right-aligned 940, base 1128). **0.38 / 0.51** the board's "1." and "2." bob in turn (scale 1.2, back.out), so they count off on "two".
- **0.70–0.96** red star (seed 731, r 28) draws above problem 1 and pops 0.7 → 1.18 → 1 (0.84–1.28). **0.80–1.0** seven ink sparkle ticks flick on 1 f apart, four around the star and three over the end of problem 1 (seeds 741–747). **0.87** "famous" (130 ink) lands with an accent rise.
- **1.11** the stamp appears in the air: scale 1.14 → 1.17, offset (+70…80, −70…−86), −14°, blur clearing, with a soft shadow far below. **1.23** wind-up (anticipation): 1.2, −96 px. **1.30 → 1.41** SLAM: power3.in to 0.94, −8°, 3 px motion blur. **1.41** CONTACT: the shadow vanishes; overshoot 1.015, then settles to 1.0 by 1.71. The board (marker layer + labels) jolts y +6 / −3 / +1.5 / 0 over 8 f. Camera punch 1.006 about (960, 650). 18 seeded red dust dots burst from the stamp's edges and fade (0.3–0.5 s). Both ✓ wobble (−14° / +9° / −4° / 0, scale 1.12), the second 2 f after the first.
- **1.42 / 1.45** phrase 1 blurs up out (6 f, bottom line first).
- **1.52–1.92** the real strip `art_unsolved.png` (0.9 scale = 805 px, white card 840 × 200 at (100, 1196), −1.2°) flips up from its bottom edge: rotationX 64 → 0, rise 50 px, back.out.
- **1.81** "problems" (130 ink, x 84, base 1000) pops. **1.90 / 1.96** tape on the left and right ends.
- **1.98–2.26** highlighter behind "They were two unsolved" ([220,9,578,75]). **2.30–2.60** highlighter behind "problems in statistics." ([66,93,513,75]).
- **2.09** "in" (0.62 em). **2.49** "statistics." (130 ink, right-aligned 940, base 1150) lands.
- **2.6–2.9** held alive to the cut: boil on fours, the dust fade ending, grid drift.

## Principles checklist
- **Contact frames on words**: "two" 0.41 (labels bob 0.38). The star draws from 0.70 so it is down on "famous" 0.87. Stamp contact on "unsolved" 1.41. "problems" lands 1.81 as the strip lands. The highlighter's second swipe finishes on "statistics." 2.49–2.6. ✓
- **Anticipation**: the stamp hovers, then lifts and grows (1.23) before it slams. Words dip via the runtime. The strip starts folded flat before flipping up. ✓
- **Overshoot + settle**: stamp 0.94 → 1.015 → 1.0; star 1.18 → 1; labels 1.2 → 1; the strip's back.out; ✓ wobble decays. ✓
- **Parts lag the whole (2–4 f)**: ✓2 is 2 f after ✓1; dust in 3 waves 1 f apart; the 2nd label 4 f after the 1st; tapes 2 f apart; ticks 1 f apart; phrase-1 lines 1 f apart. ✓
- **Long moves on arcs**: the stamp comes down diagonally from the upper right (x and y eased differently, power3.in) while it rotates. ✓
- **Squash/stretch on shapes only**: there is no squash on type. The stamp only scales (0.94 contact). The dust shrinks. ✓
- **One focal point**: words share the stage with the board until the slam. Phrase 1 leaves right after the hit so the strip and highlighter take over. ✓
- **Secondary action / no dead hold ≥ 1 s**: boil on every stroke, grid drift, label bob, star pop, dust, ✓ wobble, highlighter swipes. `slots.py --motion` reports no dead holds. ✓
- **One exaggerated hero beat**: the stamp slam (jolt, punch, dust, impact). ✓
- **Exits faster than entrances**: phrase 1 leaves in 6 f; the dust fades in about 0.2 s; entrances take 0.3–0.46 s. ✓
- **One light direction / contact shadows**: the card and the stamp's air shadow fall downward. The stamp loses its shadow on contact, because ink on paper has none. ✓
- **Not a static slide**: something draws, lands or reacts on every beat. ✓

## Richness
- **Hero**: the red rubber STAMP "unsolved" (Inter Tight 900, rough red double rectangle that boils, −8°). It slams over problem 2 / the board's lower half on "unsolved", with a board jolt and a red dust burst.
- **Micro 1 ("famous")**: a red marker star pops above problem 1, with ink sparkle ticks around it and over the end of the line.
- **Micro 2 ("problems … statistics")**: the real article strip flips up and is taped at both ends. Two highlighter swipes behind "They were two unsolved / problems in statistics.".
- **Micro 3 (on the hit)**: the two red ✓ from v02 wobble.
- **Bonus ("two")**: the board labels "1." and "2." bob in turn, so the board counts.

## Readability
- **Zone (measured)**: every frame was diffed against a background-only render (`qa/bounds.py`, all 87 frames). Threshold 24: x 71–957, y 318–1437. Threshold 10: x 71–957, y 318–1458. No frame is outside x 60–960 / y 285–1480.
- **Strip**: 0.9 scale (805 px image in an 840 px card), text ≈ 41 px, one strip, highlighter behind the text, no loop.
- **No ghosted text**: the stamp has a solid paper fill, so problem 2 and "2." are fully hidden under it, not half-visible. Phrase 1 exits in 6 f before "problems" arrives (no overlap). `.mk-hl path { fill: none !important; }` is in the scene's style, so there is no dark strike line mid-swipe (checked at f68).
- **Sizes**: kinetic words are 130 authored (supporting) and 84 (connective); "in" is 0.62 em of 130 = 81. Stamp text is 156 authored × 0.94 = 147 px. Labels are Caveat 64 ink (v02's).
- Nothing crosses text. There is no speaker in this scene (per the brief), so there is no face issue.

## Deviations
- **Stamp size and anticipation**: the stamp text is 156 authored (~147 px), not ~190, and the anticipation scale is 1.14–1.2, not 1.4. At −8° the stamp has to fit between x ≥ 60 and v02's ✓ at (820, 620). At ~190 it would cover the ✓, and at 1.4 it would leave the zone. The air pose is offset right so the 1.2 scale stays inside.
- **Board jolt**: mostly vertical (+6 / −3 y, −2 / +1 x), so the right edge never crosses x 960.
- **Strip timing**: the strip arrives on "problems" (1.52–1.92), not on "statistics", so the briefed highlighter window 1.9 → 2.6 can run. The second swipe finishes on "statistics".
- **Kinetic words**: the briefed 'famous ~120 ink' is 130 (to match "two" on the same line). A second phrase, "problems / in statistics.", replaces phrase 1 so the captions follow the speech.
- **No speaker card / no speaker.mp4 in the composition**: per the brief, "No speaker in this scene". The same approach as reel-06 v07_you.
- **No camera push**: matches v02 for the seam, as the coordinator asked. Life comes from grid drift, boil and the hit.
- **Board's bottom-right**: the stamp covers most of problem 2. The last ~20 px of problem 2's final squiggle shows between the stamp and ✓2. This is the real board under the stamp, and I left it.

## Fix pass (coordinator review)
- "work." (tail of the previous sentence) on line 1 of the strip is hidden by a rectangle in the captured page's own colour rgb(247,245,239) (strip px 56,18 158x64, under the highlighter). Line 1 now reads "They were two unsolved". No visible patch (qa/strip_fix.png). Re-rendered: 87 frames, bounds unchanged (x 71-957, y 318-1458), slots check passed.
