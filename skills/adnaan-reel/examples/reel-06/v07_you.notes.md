# v07_you — FUNNEL, tier 3 = YOU (blank, bespoke) — 157 frames @30

Spoken: "After that is about 20 million or 0.2% of the people, which is where I think you land at."
Layout = the approved reference frame `verify/style_test_v2_red.png`, animated. No speaker card: none fits without covering the funnel, and the brief made it optional.

## Key poses (scene seconds / frame)
| t | f | on screen | word |
|---|---|---|---|
| 0.00 | 0 | shared funnel already drawn (FUN.draw(0), 3 dividers), tiers 0–1 pencil hatch, 9 stick people in tier 0, all boiling | — |
| 0.37 | 11 | real post strip `post_b3.png` (scale 0.864 = 828 px, card 860×400, −1.5°) has dropped in at the top; X chip pops on its corner (0.42) | After |
| 0.52–0.97 | 16–29 | red arrow draws down outside the left wall, tier 1 → tier 2 | that is about |
| 1.43 | 43 | highlighter (1.28–1.60) is behind "20M people (0.2%)"; "20" pops in at the right of the spout | 20 |
| 1.73 | 52 | "million" lands → "20 million" 100 ink | million |
| 2.37 | 71 | "0.2%" 236 RED hero lands bottom-left, a 2 px stamp shake, and tier 2 hatches red (2.27–2.75) | 0.2% |
| 3.30–3.70 | 99–111 | post card recedes (55 %, 2.5 px blur); the map pin draws on at the right (outline 3.42, red fill 3.66, hole 3.84), its contact shadow appears | people |
| 3.86–4.26 | 116–128 | pin bobs over its shadow; "20 million" blurs out at 4.16 to clear the arrow's path | which is where I |
| 4.27–4.45 | 128–134 | anticipation: the pin crouches (squash), then lifts 46 px with a stretch and lean; the shadow shrinks and fades | think |
| 4.45–4.67 | 134–140 | the drop: arc (x power1.inOut, y up then power2.in), leaning into travel, stretched | — |
| 4.67 | 140 | CONTACT in tier 2: squash 0.74/1.22, rebound, back.out settle, rotation wobble 9/−6/3/0; landing contact shadow; ink shockwave ellipse (4.60) expands and fades (4.78–5.2); 4 px shake + 0.6 % punch; "you" 190 ink lands bottom-right | you |
| 4.72–5.08 | 142–152 | red double underline under "you"; the stick people hop in a 2 f wave (4.77–5.13) | land |
| 4.84–5.18 | 145–155 | red arrow draws from "you" up to the pin; its head flicks on last | land at |
| 5.20 | 156 | held to the cut: boil, float, settle wobble ending, camera push | at |

## Principles checklist
- **Contact frames on words**: card (0.05 → contact ≈0.37 on "After" 0.19 … "that" 0.49), "20" 1.43, "million" 1.73, "0.2%" 2.37, red hatch begins 2.27, pin outline on "people" 3.53, pin + "you" 4.67. ✓
- **Anticipation before the hero move**: pin crouches (4 f squash) then lifts with a stretch before the drop; hero words use the runtime's 3 f dip. ✓
- **Overshoot + settle**: card (cardIn back.out), X chip pop, hero words 1.06 → 1, pin squash → rebound → back.out(2.5) + rotation wobble. ✓
- **Parts lag the whole (2–4 f)**: X chip 4 f after the card; pin fill after the outline, hole after the fill; stick-people hop staggered 2 f; underline 2nd pass after the 1st; arrow head after its shaft. ✓
- **Long moves on arcs**: the pin's 400 px drop (different x/y eases, lift first). ✓
- **Squash/stretch on shapes only**: the pin (and its shadows); never type or the X logo. ✓
- **One focal point**: post card in A (funnel static), the card recedes on 3.3 before the pin draws; "20 million" exits before the drop. "you" and the pin land on the same frame by design (same idea), then the arrow joins them. ✓
- **Secondary action, no dead hold ≥ 1 s**: boil on fours on every marker stroke, grid drift, camera push, card float, pin bob — `slots.py --motion`: no dead holds. ✓
- **One exaggerated hero beat**: 4.67 shake 4 px + punch 0.6 % (0.2% gets only a 2 px stamp shake). ✓
- **Exits faster than entrances**: "20 million" 6 f blur-up; shockwave fades in 0.42 s; card recede 0.4 s. ✓
- **One light direction / contact shadows**: card + X chip shadows fall down; the pin has a contact shadow while hovering (shrinks as it lifts) and a new one where it lands. ✓
- **Not a static slide**: every second has a drawing, landing or reaction. ✓

## Richness (house level)
- **Hero**: hand-drawn MAP PIN (M.line teardrop + M.circle hole, red fill, red-dark felt-tip edge) — draws on at the right on "people", hovers, crouches, lifts, drops on an arc into tier 2 on "you" with squash, wobble and a marker shockwave.
- **Secondary 1**: real post strip + highlighter swipe behind "20M people (0.2%)" on "20".
- **Secondary 2**: tier 2 hatches RED on the "0.2%" stamp (the funnel filling in tier by tier across the reel).
- **Secondary 3 (characters)**: the 6B stick people in tier 0 hop in a wave when the pin lands.
- **Secondary 4**: red marker arrows: tier 1 → tier 2 on "after that", and "you" → pin at the end; double underline on "you".

## Measured
- Frames: 157 (ffprobe). `slots.py check --motion`: checks passed; motion: no dead holds.
- Bounds (diff vs a background-only render, `qa/bounds.py`, all 157 frames): threshold 24 → x 62–955, y 292–1469; threshold 10 (incl. soft shadow tails) → x 62–958, y 292–1471. 0 frames outside x 60–960 / y 285–1480.
- Post strip scale 0.864 (≥ 0.85), card 860 px wide.

## Deviations
- No speaker card (optional in the brief; no room without covering the funnel).
- "20 million" sits at the right of the spout (x ≈ 500–952, baseline 1226), not above "0.2%" as in the reference: with the shared funnel geometry the spout reaches y ≈ 1214, so a stacked "20 million" would collide with it. It blurs out at 4.16 so the you → pin arrow has a clear path.
- The card drops only 16 px (plus scale and blur) so its corner never leaves the zone (y ≥ 292).
- The shockwave ellipse is ink, not red, because a red ring on the red hatch would not read.
- Below the funnel (y 1240–1480) the frame is empty until "0.2%" lands at 2.2 s. Tiers 1–3 and "20 million" (from 1.3 s) fill the lower 40 % of the zone in the meantime.
