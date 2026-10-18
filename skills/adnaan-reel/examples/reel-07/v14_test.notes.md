# v14_test — NOTES (v3: v6 three-mode system)

EXPLAINER, full-screen opaque, 1080x1920 @30, **140 frames** (data-duration 4.65 on root + speaker video).
Runtime (paper.js / paper.css / marker.js / marker.css, re-installed for v6) untouched. `<body data-face="0.41">`.
History: v1 150 f with a small corner card → v2 retimed to 140 f (dead air cut, second sentence −0.2667 s) → **v3 (this):
v6 SOP — corner card removed; Mode B for the checklist, Mode A split for the payoff.** Word times = v2 (Have 0.07 … scenario 2.59,
That's 3.013, how 3.193, you 3.313, know 3.493, actually 4.193, worked 4.573).

## Key poses (scene seconds)

| f | t | mode | on screen | lands on |
|---|---|---|---|---|
| 0 | 0.00 | B | paper only; big checklist card (1.08x, ≈ x 78–942, y 767–1393) starts rising | Have |
| 6 | 0.20 | B | "Have it" (sup 120, left, base 430) | Have it |
| 16–30 | 0.52–1.02 | B | row 1 "run a test" drops in; play button presses red, run-bar fills; red marker ✓ 1; segment 1 | test 0.69 |
| 27–36 | 0.89–1.36 | B | **check** (red 180, right-aligned, base 640) pops; red underline | check 1.05 |
| 39–60 | 1.30–2.0 | B | row 2 "a real number"; odometer rolls to ###; ✓ 2 | number 1.63 |
| 71–86 | 2.36–2.86 | B | row 3 "a real scenario"; pin drops, squashes, ripples; ✓ 3; 3/3 | scenario 2.59 |
| 73–80 | 2.42–2.67 | B | "Have it / check" blur up | — |
| 74–92 | 2.46–3.08 | B→A | checklist lifts 3 f, then glides DOWN and compacts into the bottom band (left, 0.62x, x 76–572, y 1040–1365); the footage band drops in from above like a shutter (splitIn via `data-at="2.95"`, starts 2.53) | That's |
| 88–105 | 2.95–3.49 | A | his footage edge to edge in the top half; "That's / how you / know" right-aligned (x ≤ 888) beside the compact checklist; ✓ boxes pulse + red underline on "know" | know 3.493 |
| 111–117 | 3.68–3.90 | A | words blur up (6 f), checklist drops out (6 f) | it |
| 118–131 | 3.93–4.37 | A | "actually" (ink 120, base 1180) | actually 4.193 |
| 131–139 | 4.373–4.63 | A | **worked** (RED hero 190, base 1420) peaks; big red marker ✓ stamp slams beside it (1.05 → 0.94 → 1); punch 4.393, shake 4.513; 4 sparkle ticks 4.52–4.58 | worked 4.573 |

## As built
- Mode B: no `.spk` on screen until 2.53. Card `#card` in a static 1.08x wrapper `#cardS` + float wrapper `#cardF`; `P.cardIn` 0.02 (rot −1.5).
  Rows drop at contact 0.52 / 1.46 / 2.42; ✓ at 0.80 / 1.74 / 2.70; segments fill +0.16 s. Icons: play press 0.62–0.98 + run-bar,
  odometer 1.30–2.07 (+kick), pin 2.36–2.56 (+squash, ripple 2.57). "Have it" 0.07/0.21 (120), "check" 1.05 (hero 180 red, pop) +
  underline 1.12; both exit 2.42 (+2 f).
- Switch: `<div id="split" class="spk split" data-h="960" data-at="2.95">` (runtime splitIn: −980 → +12 → 0, 2.53–2.95; push 1→1.02).
  Card: lift −10 px 2.46, then top 790→1043, left 110→108, scale →0.574 (0.62 effective), height 580→524, origin 0 0, 2.56–3.08;
  rows/slots/header tighten 2.60 + 2 f stagger.
- Mode A band words: That's 3.013 / how you 3.193·3.313 (84, right 888) / know 3.493 (pop 130, right 878) + red underline 3.42–3.64;
  ✓ boxes pulse 3.50 / +3 f / +6 f; pin bob 3.10–4.3, run-bar re-run 3.22. Exits: words 3.68 (dy −20, 6 f, lags 0/1/2 f), card
  exitDown 3.70. actually 4.093 (accent, s 3.93). **worked** 4.373 (hero 190, x76, peak 1.03, rise 24). Stamp ✓ (SX 797, SY 1360,
  size 164, width 20) 4.373–4.553, slam settle 4.513; sparkles −135/−108/−84/−60° at 4.52/4.54/4.56/4.58 (0.05 s each).
  `P.punch(4.393, 1.01, origin 520,1240)`, `P.shake(4.513, 2.5)`.

## Measured bounds (`qa/bounds_v6.py`, render.mov vs `qa/bg.mov` background-only, diff > 24, every frame)
- **Mode B (f 0–75): union x 77–960, y 336–1440** — inside x 60–960 / y 285–1480.
- **Mode A paper band (f 76–139, footage band y < 975 excluded): union x 66–942, y 975–1440.** After the band lands (f 89+):
  every frame y ≥ 1000, ≤ 1480 and x ≤ 900 below y 1200 — 0 violations.
- The only flagged frames are f 76–82 (2.53–2.73): the shutter is still dropping and the big checklist is mid-shrink on its way down
  (x ≤ 942 below y 1200) — a transition frame inside the Mode B zone, not a settled Mode A layout.
(Final numbers from the last render are in the report.)

## Principles checklist
- **Contact frames**: rows ≈ 0.17 s before test/number/scenario; ✓s right after; check / know / actually / worked via the runtime;
  the band lands on "That's" (2.95 vs 3.013); worked peaks 0.2 s before the spoken word so the stamp + sparkles finish before the cut.
- **Anticipation**: card lifts 3 f before dropping into the band; the band overshoots +12 and settles; play button and ✓ boxes dip;
  hero words sink first.
- **Overshoot + settle**: rows, card, odometer kick, pin, boxes, band, stamp slam, words.
- **Parts lag the whole**: odometer columns 1–3 f; rows compact 2 f apart; segments after their ✓; word exits 0/1/2 f; sparkles ~1 f.
- **Arcs**: the card's compaction mixes eases (scale/top/left) so it curves down-left; pin falls straight (gravity).
- **Squash/stretch on shapes only**: pin, icon box, ✓ boxes — never type.
- **One focal point / two-element guideline**: Mode B = checklist + "Have it / check"; A1 = compact checklist + "That's how you
  know"; A2 = "actually worked" + stamp (checklist gone).
- **Secondary action / no dead hold**: marker boil, card float, run-bar re-run, pin bob, footage push, grid drift; slots.py: no dead holds.
- **One exaggerated hero beat**: worked + stamp slam + punch + shake + sparkles.
- **Exits faster than entrances**: 6 f word exits, 6 f card drop-out, underlines leave with their words.
- **One light direction**: runtime shadows down; flat footage band (no shadow) per v6.
- **Not a static slide**: something drops, rolls, draws, pulses or boils on every frame.

## Richness
- Hero: the checklist — notification rows on their words, red marker ✓ in rhythm, header progress 1/3 → 3/3, compacting into the
  band, then the big red ✓ stamp + sparkles on "worked".
- Living icons: play press + run-bar ("test"), odometer to a value-free ### ("number"), pin drop + squash + ripple ("scenario").
- Marker: red underlines under "check" and "know"; ✓ boxes pulse on "know".

## Readability
- Mode B type: Have it 120, check 180 (hero), row labels Inter 600 56 px × 1.08 ≈ 60 px. Mode A: That's / how you 84, know 130,
  actually 120, worked 190 (hero ≥ 170). Compact-card labels ≈ 35 px while "That's how you know" plays (already read; it then exits).
- No semi-transparent lingering text: Mode-B words gone (2.67) before the band lands; A1 words + card gone (3.90) before "actually"
  rises (3.93). No words over his footage; all type on paper in the band. Nothing crosses the face or text; stamp clears "worked".
- White space: Mode B ≈ 40 % of the grid empty; Mode A band leaves y 1440–1480 + the right of "actually" open.

## Sound (beats.json, 18 structural beats, honest times; no scribble beats per v6)
Rows/checks/odometer/pin in Mode B; whoosh 2.62 on the mode switch; know pop + ✓ pulse tick; card drop-out whoosh 3.70;
actually 3.97; **impact 4.45 on "worked" + stamp**; ping 4.58 sparkles.

## Deviations
- Words omitted (connectives only): "or" ×2, "it" (4.00), full stops; "run a test / a real number / a real scenario" are row labels.
- "That's how you know" stacked as That's / how you / know (right column beside the compact checklist).
- "worked" 190 (brief ~250) so the stamp fits beside it at x ≤ 900 below y 1200; peaks at 4.373 (spoken 4.573) to settle by the cut.
- The checklist leaves at 3.70 (two-element guideline) instead of staying under the payoff.
