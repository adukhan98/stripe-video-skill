# v16_further — THE GAUGE floods (explainer, bespoke) — 171 f @30 (5.700 s)

Spoken: "Most people are still using AI for emails and quick questions. But you can get so much further than that."

## Key poses (planned before authoring)
| t | f | on screen | word |
|---|---|---|---|
| 0.00 | 0 | THE GAUGE exactly as v15 ends: black bar x 680–840 / y 340–1420 + 5 ticks, "so much more" note top-left of the bar, spark above it, red sliver hatch y 1340–1420, "ask it for" note, red gap brace right; small card x 90–540 / y 760–1150 | (cut) |
| 0.17 | 5 | "Most people" lands top of the left column | Most |
| 1.29 | 39 | "still using" under it; the card steps back (scale 0.8 from its bottom-left corner) to make room | using |
| 1.63 | 49 | "AI for" third line | AI |
| 2.37 | 71 | A1 gone; "emails" (150) lands; black-marker envelope doodle drawing bottom-left | emails |
| 2.70 | 81 | envelope flap flips open … | (and) |
| 2.83 | 85 | … "quick" lands; speech bubble with red "?" pops beside the envelope; flap closes | quick |
| 3.43 | 103 | "questions" lands; both doodles shrink and slide toward the red sliver | questions |
| 3.94 | 118 | A2 gone; "you can get" | you |
| 4.36 | 131 | anticipation: the bar squashes down, the sliver trembles, the doodles lean back | get |
| 4.66–4.88 | 140–146 | "so much" | so / much |
| 5.11 | 153 | HERO: the red brace un-draws upward into a red arrow that shoots up beside the bar, head flicks at the top; red hatch floods the bar in 8 stacked passes; **further** (red) lands; punch + shake; doodles hop | further |
| 5.34 | 160 | "further" rode up with the flood; red ✓ beside "so much more" | than |
| 5.68 | 170 | held alive (boil, push, float) into the cut | that |

## As-built timeline (scene seconds)
- 0.00 THE GAUGE = v15's `gauge(M, P, T)` pasted VERBATIM, called with every time 0 (outline 901/903, ticks 931–935,
  "so much more" 92 px ink, spark 905–907, sliver hatch 911 + 910, "ask it for" 84 px red-dark, brace 921/923), boiling.
  Card = v15's spot (small, x 90 y 760 450×380, ry 6). `scenes.py seam v15_gauge v16_further`: mean diff 8.9, the gauge lines up exactly; only words differ.
- 0.04/0.36 "Most people" (92) · 0.86/1.16 "still using" (100) · 1.12 card swells 3 f then steps back to 0.8 from its
  bottom-left corner (back.out) · 1.50/1.88 "AI for" (100) · exits: lines 1–2 at 1.86 (6 f blur-up), "AI for" 2.16
- 2.17 "emails" hero 150 (overshoot + settle) · 2.20–2.48 envelope body (ink, seed 1601) · 2.50 flap V · 2.65/2.72 folds
- 2.66 speech bubble loop (ink, 1611) pops from 0.55 → 1.1 → 1 · 2.67 "quick" pop · 2.86 tail · 2.92 red "?" (1613) + dot 3.10
- 2.76 flap presses 2 f, flips open (scaleY −0.56) · 3.18 snaps shut, envelope squashes · 3.0–3.7 bubble wobbles ±4°
- 3.27 "questions" pop · 3.40 "?" bounces · 3.30/3.43 doodles anticipate left, then shrink to 0.82 and slide toward the red sliver
- 3.56 A2 exits (bottom-up lag) · 3.81/4.01/4.23 "you can get" (84) · 4.40 card recedes a touch (0.82, blur 2)
- 4.36–4.86 anticipation: the bar + ticks + sliver squash down (scaleY 0.985, loading), the sliver trembles ±2 px, doodles lean back 5°
- 4.50/4.72 "so much" (120, accent rise) · 4.88 bar springs up (1.014) → back.out settle 5.04
- 4.88–5.04 red ARROW shaft shoots up x 892 from y 1400 to 382 (power1.in), the brace un-draws exactly at the rising
  tip (braceLo 4.92–5.00, braceHi 5.00–5.04) — the gap turns into the arrow · 5.11 arrowhead flicks
- 4.91–5.17 red hatch FLOODS the bar: 8 stacked passes (seeds 912–919, −32°, spacing 19), each starting as the tip passes its band, then boiling
- 5.11 "further" hero (authored 180, data-fit 560 → ~154 px on screen, RED) + punch 1.008 + 3 px shake; doodles hop 22 px and bounce down
- 5.00–5.60 "further" line rides up 16 px with the flood and settles at −12 · 5.28–5.50 red ✓ left of "so much more" (seed 1721)
- Always on: grid drift, camera push 1.006 (origin 510 700), marker boil on fours, card float + 3D drift.

## Principles checklist
- **Contact frames on words**: every word entrance 0.13–0.2 s before its words.txt time (runtime); envelope on "emails" (2.20→2.37), bubble on "quick" (2.66→2.83), "?" bounce on "questions" 3.40, anticipation on "get" 4.36, arrowhead + impact on "further" 5.11, ✓ on "than" 5.28.
- **Anticipation**: bar squashes 0.5 s before the flood, the sliver trembles, doodles lean back; flap presses down 2 f before flipping; doodles dip left before sliding; card swells 3 f before stepping back; hero words sink before rising.
- **Overshoot + settle**: bar springs to 1.014 → back.out; bubble 1.1 → 1; "further" ×1.06 → settle and its ride-up overshoots 16 → 12; flap snaps shut with back.out; card step-back back.out.
- **Parts lag the whole (2–4 f)**: envelope body → flap → folds; bubble loop → tail → "?" → dot; exits staggered 2 f bottom-up; flood passes chase the tip in sequence; arrow shaft → head.
- **Long moves on arcs**: doodles slide with rotation into travel (x and y eased together but scale/rotation lead); the arrow has a slight bend; the flood climbs on the shaft's accelerating curve. (No long cross-frame moves in this scene.)
- **Squash/stretch on shapes only**: the bar (loading squash + spring), the envelope on shutting, the "?" bounce — never type.
- **One focal point**: Beat A = words + doodles while the gauge just boils; hero = the bar (card recedes, words stack beside it).
- **Secondary action, no dead hold ≥ 1 s**: boil on fours, card float/drift, bubble wobble, flap, "?" bounce, sliver tremble, grid + push. slots.py motion: "no dead holds".
- **One exaggerated hero beat**: "further" — the flood + arrow + punch + shake + impact SFX.
- **Exits faster than entrances**: phrase exits 6 f; the brace un-draws in 0.12 s (v15 drew it in 0.5 s).
- **One light direction / contact shadows**: only the card carries the runtime's down-right shadow; marker strokes are flat ink on paper.
- **Not a static slide**: something draws, moves or boils on every frame.

## Richness (hero + secondary)
- HERO: THE GAUGE floods on "further" — the red gap brace un-draws INTO a red arrow shooting up beside the bar while 8 stacked red hatch passes fill the bar to the top; "further" rides up with it; ✓ on "so much more".
- 1. Envelope doodle draws on "emails" and its flap flips open and snaps shut (2.37–3.3).
- 2. Speech bubble with a red "?" pops on "quick", wobbles, and the "?" bounces on "questions" (2.83–3.6).
- 3. Both doodles shrink and slide to the tiny red sliver — that's all they fill (3.43); they lean back during the anticipation and hop on the impact (5.11).
- 4. The bar itself loads like a spring on "get" (squash + tremble) before it floods.

## Readability
- Zone measured (qa/bounds.py, every frame diffed against qa/bg.mov, a render with all content removed, threshold 20): **x 64–925, y 296–1437, 0 frames out of x 60–960 / y 285–1480**.
- Kinetic sizes (authored): emails 150, quick/questions 120, so much 120, still using / AI for 100, Most people 92, you can get 84 (≥ 64), further 180 (fit to 560 → ~154 on screen).
- No ghosted text: phrases exit in 6 f; the two-step A1 exit leaves "emails" a clear band (checked at 1.8–2.3 s).
- Notes: v15's 92 px ink and 84 px red-dark Caveat (≥ 60). Doodles 200 / 170 px wide (phone-sized; 0.82 after the slide).
- Nothing crosses text or the face; no words over his hoodie (the type sits on paper above the card). The open flap was reduced (scaleY −0.56) so it clears the card's red edge.
- Whole head incl. hair in the card on every frame (check_sheet).

## QA
- render.mov: prores 4444 1080x1920 @30, **171 frames** (ffprobe). slots.py check: size, fps, duration, alpha passed; motion: no dead holds.
- Seam v15→v16: verify/seam_v15_gauge__v16_further.jpg, mean diff 8.9, the gauge identical, only the scene words differ.

## Deviations
- "further" is authored 180 with `data-fit="560"` (~154 px on screen), not ~230: at 230 it is ~750 px wide and would cross the gauge (x 650–920 is the bar + ticks + arrow). It fits the left column next to the bar.
- The speaker card starts in v15's exact spot and at 1.12 s steps back to 0.8 (from its bottom-left corner, so its bottom edge stays at y 1140) to make room for the 3-line phrases ("emails / quick / questions"). It does not fit the 300 px band above the full-size card.
- Words shown: Most people / still using / AI for / emails / quick / questions / you can get / so much / further. Not shown: "are", "and", "But", "than that".
- The brace erases by un-drawing in step with the arrow's tip (in the same lane at x 889–920), not by fading, so the gap visibly becomes the arrow.
- "ask it for" stays after the flood, labelling the original sliver.

## Revision v6 — Mode B (coordinator style pass, 2026-10-15)
- **Mode B (full canvas)**: the small speaker card and its video were removed entirely (v15 now ends in Mode B). The gauge is unchanged:
  v15's `gauge()` is still pasted verbatim and called with every time at 0 (function checked byte-identical to v15's).
- The freed left column (x 76–650) now holds the words and the doodles, with more space around them:
  - A1 "Most people" (100) base 600 / "still using" (110) 735 / "AI for" (110) 870. Lines 1–2 exit at 1.86, "AI for" at 2.16.
  - A2 "emails" (150) base 580, "quick" (120) 700, "questions" (120) 820. All three exit at 3.56 (6 f, ≤ 1 f lag) so they clear before "you" at 3.81.
  - The envelope is bigger (260×160, x 100–360, y 905–1065) and sits under the words. The "?" bubble is ×1.25 (x 400–610, y 886–1075).
    The flap open/shut, the bubble pop + wobble and the "?" bounce keep the same times as before.
  - At 3.50–4.16 both doodles lift 10 px (anticipation), then drop on an arc (x power2.out, y power2.in) about 280 px down into the
    corner beside the red sliver. They shrink to 0.72/0.70 and land with a squash at 4.10/4.16. They lean back on "get" and hop on "further".
  - Hero words lower and bigger: "you can get" (90) base 640, "so much" (120) 790, "further" (180, fit 560) 975.
- Removed: the card step-back at 1.12 and the card recede at 4.40 (no card). The earlier "card steps back" deviation no longer applies.
- beats.json is now sparse and structural (no scribble beats, per the v6 SOP). Same times as before; the card whoosh is gone and the doodle drop/landing were added.
- QA (re-render): 171 frames · slots.py check passed (size, fps, duration, alpha) · motion: no dead holds ·
  bounds x 64–925, y 296–1437, 0 frames out (threshold 20 vs qa/bg.mov).
- Seam: mean diff 17.0 against the v15 render.mov currently on disk (21:09 on 10-14, which still shows v15's card).
  The gauge code is identical, so it should drop back once v15 is re-rendered in Mode B.
