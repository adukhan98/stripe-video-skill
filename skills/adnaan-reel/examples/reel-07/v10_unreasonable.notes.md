# v10_unreasonable — NOTES

84 frames @30 (2.800 s). Full-screen opaque paper scene, CHAPTER ② — "Second, set goals that sound unreasonable."
No speaker (2.8 s chapter beat; the speaker video element was removed, root `data-duration` 2.7833 kept).

## Key poses (planned before authoring)

| frame | s | on screen | lands on |
|---|---|---|---|
| 1 | 0.04 | red marker loop starts drawing top-left (chapter-number position) | — |
| 7 | 0.22 | ② digit (Inter Tight 900, 210, ink) popped inside the loop; loop closed by 0.46 | 'Second' 0.29 |
| 9 | 0.29 | 'second,' (90, 800) right of the ② | 'Second' 0.29 |
| 18 | 0.61 | 'set' (150, 900 ink) lands mid-left | 'set' 0.61 |
| 29 | 0.97 | 'goals' pops; black-marker MOUNTAIN ridge drawing left→right right of it (0.80–1.14), ground, pencil hatch, snow line | 'goals' 0.97 |
| 40 | 1.32 | tiny red FLAG: appears raised, lifts, stabs into the summit (summit dips), wobbles; 'that' (96) right | 'that' 1.21 |
| 44 | 1.47 | real strip art_unreasonable.png (0.92, card 862 px) has slid/flipped up at y 1196–1404, two tapes slap on; 'sound' pops | 'sound' 1.59 |
| 49–69 | 1.62–2.30 | highlighter swipes 'Pick unreasonable goals and tell' then 'the model that they're very rea-' | 'sound' → 'unreasonable' |
| 65–69 | 2.17–2.30 | anticipation: 12 red letters appear high, lift, then slam down in 4 waves | — |
| 70 | 2.33 | HERO contact: 'unreasonable' (red 900, fit 880 px) down; camera shake 4 px + punch; the mountain shoots up from its base (crouch 0.94 → 1.42 → settles 1.35) so the flag sits ridiculously high; strip + tapes jolt, 'that sound' flinches | 'unreasonable' 2.47 |
| 72–80 | 2.40–2.67 | per-letter shake 4 → 1 px decaying, red shake lines draw at both ends and vibrate | 'unreasonable' |
| 83 | 2.77 | holds alive: 1 px letter tremor on fours, boil on every stroke, grid drift, camera push | cut |

## As built (scene seconds)

- 0.04–0.46 red loop `M.circle(190, 428, 110, 111)` seed 1020, width 12 (≈ 240×245 drawn). Digit '2' `data-cx 190 data-base 492 data-size 210` (data-pop, t 0.22), centre ≈ (190, 420); settle wobble −3° 0.50 → 0 by 0.96.
- 0.29 'second,' (90, x 352, base 452).
- 0.61 'set' (data-accent) / 0.97 'goals' (data-pop) — one line, 150, x 78, base 772.
- Mountain (black marker, seeds 1501–1506): base y 832, x 704–944, summit (842, 576) → 240 × 256. Ridge `M.line` 0.80–1.14 left→right (width 11), ground line 1.12, pencil hatch on the right (shadow) face 1.22, snow-line zigzag 1.25. Strokes use `vector-effect: non-scaling-stroke` so they keep their width when the mountain stretches.
- Flag (separate group riding the summit, never stretched): red filled pennant + red outline + ink pole (80 px). 1.12 appears 40 px above the summit tilted −14°, lifts to −52 (anticipation), 1.22 stabs down (power3.in), contact 1.32: summit squashes scaleY 0.97 and the flag rides it, then wobbles −6° / 3° / −1.5° / 0 to 1.92.
- 1.21 'that' / 1.59 'sound' (pop) — 96, right-aligned to 944, base 922.
- 1.24 strip card flips up (rotationX 28→0, y 46→−5→0, rot −4.5 → −1.1, blur 6→0), settled 1.80. Tapes 1.48 (170,1170) and 1.56 (706,1166).
- Highlighter (multiply, behind the words): line 1 [66,9,809,75] 1.62–2.00; line 2 [66,93,796,75] 2.00–2.30.
- 2.17–2.37 slam: letters in 4 waves of 3 (centre-out order), each 2 f lift (y −70→−86) → 3 f slam (power3.in) to y +9 → 3 f settle. Edge letters (u, e) don't rotate and blur less (zone).
- 2.33 IMPACT: `P.shake(2.33, 4)`, `P.punch(2.33, 1.005)`; strip + tapes jolt +7 px → back.out; 'that sound' flinches −5 px.
- 2.23–2.33 the mountain crouches to scaleY 0.94 (anticipation), 2.33 shoots to 1.42 (5 f, power3.out), settles to 1.35 by 2.83 (back.out); the flag group follows the summit exactly (y = −256·(s−1)) and whips 10° → −5° → 2° → −1°. Final summit y ≈ 486, flag top ≈ 412.
- 2.43–2.63 per-letter shake every frame (4 → 1 px, ±rot), then a ±1 px tremor on fours to the cut.
- 2.40–2.63 ten red shake strokes: 3 radial ticks above each end of the word, 2 whoosh dashes under each end; they vibrate on twos until 2.86.
- Continuous: grid drift, camera push 1.004, marker boil on fours, letter tremor.

## Principles checklist
- Contact frames on words: yes — ② on 'Second', mountain on 'goals', flag stab just after 'that', mountain grows on the slam, strip on 'sound', slam contact 0.14 s before 'unreasonable'.
- Anticipation before the hero move: the letters appear high and lift 2 f before slamming; the mountain crouches 3 f before it shoots up; the flag lifts before it stabs; runtime pops dip before rising.
- Overshoot + settle: letters slam past the baseline (+9 px) and settle; mountain 1.42 → 1.35; flag wobble; strip −5 px overshoot → settle; digit wobble.
- Parts lag the whole: letters land in 4 waves 1 f apart; shake strokes stagger 1 f; strip → tape → tape; ridge → ground → hatch → snow line → flag; the flag lags/whips behind the growing summit.
- Long moves on arcs: strip flips up on a hinge (rotationX) while rising and de-rotating (y and rotation on different eases).
- Squash/stretch on shapes only: the mountain squashes under the flag stab and stretches on the slam (strokes non-scaling); never type.
- One focal point: ② → set goals/mountain+flag → strip highlighter → hero (the mountain's growth is part of the hero beat, on the same contact frame); no text receded.
- Secondary action / no dead hold ≥ 1 s: boil, grid, push, tremor; slots.py "motion: no dead holds".
- One exaggerated hero beat: the slam (shake + punch + per-letter shake + the mountain shooting up 1.35×) — the only `impact`.
- Exits faster than entrances: no exits needed (holds to the cut); recedes are 0.24 s.
- One light direction / contact shadows: card shadow down; tapes multiply.
- Not a static slide: something draws or moves on every frame.

## Richness
- Hero: per-letter slam of 'unreasonable' with anticipation, camera shake, per-letter jitter that settles into a tremor, red marker shake lines at both ends (on 'unreasonable').
- Micro 1: black-marker mountain drawn on 'goals'; a tiny red flag is planted on the summit (lift → stab → wobble) on 'that'; on 'unreasonable' the mountain grows 1.35× so the flag ends up ridiculously high.
- Micro 2: the real strip flips up, is taped, and the highlighter swipes the phrase ('sound' → 'unreasonable').
- Micro 3: the world reacts to the slam — strip and tapes jolt, 'that sound' flinches.
- Chapter continuity: ② circled top-left in the shared chapter-number style.

## Readability
- Zone measured (diff vs a background-only render, every frame, threshold 12): **x 62–958, y 292–1458** — inside 60–960 / 285–1480 on all 84 frames.
- Strip at 0.92 (card 862, strip 822 px wide, text ≈ 41 px); highlighter behind the words, not a loop.
- No semi-transparent text at rest: nothing recedes; all words fully opaque.
- Sizes: digit 210, set goals 150, that sound 96, second 90, hero fit to 880 px (≈ 148 px on screen). No handwriting notes.
- Nothing crosses text: shake lines sit above the x-height / under the baseline at the word ends; tapes on the card edge.

## Deviations
- Hero 'unreasonable' is fit-limited: 12 letters at ≤ 900 px wide give ≈ 148 px on screen (≈ 157 authored-equivalent), under the brief's ~180 / 170 floor — one line was kept rather than splitting the word. No scale overshoot on the slam (it overshoots in y), so the full width is usable.
- "Shake lines either side": the word fills the zone width, so the strokes sit above/below the two ends of the word (radial ticks + whoosh dashes) instead of left/right of it.
- Highlight line 2 widened from SHARED's [66,93,493,75] (which ends mid-'they're') to [66,93,796,75] to cover the full spoken phrase on that line ('the model that they're very rea-').
- Mountain + flag on 'goals' (coordinator revision, replacing a target doodle that repeated v07/v09).
- Lower 40 % of the zone is empty until ~1.25 s (the strip arrives on 'sound', as briefed).
- Final period of 'unreasonable.' dropped; 'Second,' shown lowercase ('second,') as in the house look.
- Speaker video removed (brief: no speaker).
