# v13_grade — chapter ③ "don't let AI grade its own work" (blank, bespoke)

## RETIME (coordinator, dead air cut): 63 frames, words −0.2 s, tail compressed

Third 0.15, don't 0.45, let 0.75, AI 1.03, grade 1.23, its 1.43, own 1.61, work 1.93; cut at 2.10. Root data-duration 2.0833.
Everything shifted −0.2 s (incl. the per-frame pen/arm track), then the tail compressed so it all reads before the cut:

| t | as built (63-frame version) | word |
|---|---|---|
| 0.02–0.34 | red loop round the 3; 3 + "third" pop (contact 0.15) | Third |
| 0.20 | test paper deals in; answers type 0.42–0.85 | — |
| 0.29–1.03 | "don't let AI" lands | don't / let / AI |
| 0.36–0.96 | robot draws itself on; arm 0.70–0.82, hand 0.93, pen 0.96 | — |
| 0.92–1.05 | bulb lights red + rays, blinks 1.18–1.54 | AI |
| 0.84–1.05 | pen lift → anticipation → dart to the A | — |
| 1.05–1.23 | robot writes the A; "grade" lands red; punch 1.008 + shake 3 (impact 1.23) | grade |
| 1.26–1.47 | crossbar + "+", sparkles 1.50/1.56, head-bob 1.50–1.73 | its |
| 1.26–1.70 | real strip slides in low (×0.9), tapes 1.50/1.55 | — |
| 1.44–1.62 | ✗ stroke 1 | own (1.61) |
| 1.65–1.83 | ✗ stroke 2 — ✗ complete 1.83 | — |
| 1.68–2.08 | droop: sad eyes/frown/bulb out 1.68, head down 1.85 (settled 2.05), antenna sags; marker drops 1.68, lands 1.92, bounces, rests 2.08 | work (1.93) |
| 1.52–1.67 / 1.70–1.94 | highlighter "Do not ask" / "the model to judge itself" — done 1.94 | — |
| 1.94–2.10 | hold alive (boil, push, float) | — |

Measured (63-frame render): ffprobe 63 frames; bounds x 64–953, y 291–1465 (all 63 frames vs a 63-frame background-only render, threshold 40); slots.py check --motion: checks passed, no dead holds. beats.json re-timed: 19 beats, last at 1.92, scribbles ≥ 0.1 s apart, impact only at 1.23.
The pre-retime 78-frame source is kept at qa/index_78f.html. Sections below describe the 78-frame version; the structure, sizes, layout, principles and deviations are unchanged except the times above (the strip now arrives at 1.26, so the empty band y 1110–1480 lasts 0–1.26 s).

## Key poses (original 78-frame plan) (planned before authoring)

| f | t | pose | word |
|---|---|---|---|
| 6–11 | 0.20–0.36 | "3" pops top-left (centre ≈ 190,420), red loop draws round it; "third" lands beside it | Third (0.35) |
| 12–27 | 0.40–0.90 | test paper card (400×480, tilted 4°) deals in centre-right; answer bars type themselves | — |
| 15–33 | 0.52–1.10 | "don't let AI" lands right of the ③; the robot draws itself on in black marker to the left of the paper | don't / let |
| 37 | 1.23 | robot complete, antenna bulb flashes red and blinks; "AI" pops | AI |
| 36–43 | 1.20–1.43 | robot winds the marker back (anticipation) then writes the "A" — contact on grade; "grade" lands RED; punch + shake | grade (1.43) |
| 43–51 | 1.43–1.71 | crossbar + "+" written, sparkles tick off the A+, head bobs with pride | its (1.63) |
| 46–55 | 1.52–1.85 | the real strip (art_judge.png ×0.9) slides in low, two tapes slap on | — |
| 50–57 | 1.68–1.90 | ✗ stroke 1 over robot + paper (not over the A+) | own (1.81) |
| 58–64 | 1.95–2.15 | ✗ stroke 2; robot droops (head down, antenna sags, sad eyes, frown), marker drops and bounces | work (2.13) |
| 62–76 | 2.08–2.53 | highlighter "Do not ask" → "the model to judge itself" | — |
| 75–77 | 2.50–2.58 | hold alive (boil, pen settle, push) to the cut | — |

## As built (scene seconds; render.mov = 78 frames, 1080x1920 @30)

- 0.18–0.54 red loop round the "3" (M.circle 195,422 r110, seed 1303); "3" (Inter Tight 900, data-size 210, ink, cx 195 / base 492) + "third" (800, 90, x 345) pop, contact 0.35.
- 0.40 test paper (uicard 400×480 at 530,605, static 4° tilt) deals in via P.cardIn; answer bars type themselves 0.62–1.05 (steps).
- 0.49 "don't" / 0.82 "let" / 1.07 "AI" (pop) — line 800 weight, data-size 120, x 345 base 532.
- 0.56–1.16 the robot draws itself on in black felt-tip (M.line/M.circle, seeds 1311–1327): head, antenna + bulb, smug half-lidded eyes, smirk, body, chest dots, legs, hand-on-hip arm. Rubber-hose writing arm draws 0.90–1.02, glove-hand pops 1.13, marker pops 1.16.
- 1.12–1.25 on "AI": antenna bulb flips red with overshoot, three red rays, then blinks (1.40–1.80).
- 1.04–1.25 pen wind-up: lift, anticipation pull back down-left, dart to the A start.
- 1.25–1.43 the robot writes the red "A" (pen tip tracks the stroke with the same power2.out); contact 1.43 = "grade" (hero, RED, data-size 176) lands with overshoot; P.punch(1.008) + P.shake(3) — the one hero beat. Head tips back (chin up), smirk widens.
- 1.46–1.71 crossbar + "+" written; 1.74/1.80 two smug sparkles; 1.80–2.07 head-bob of pride (antenna lags).
- 1.47 "its" / 1.65 "own" (accent rise) / 1.97 "work" (pop) — 800, data-size 130, right 940 base 1198.
- 1.52–1.85 real strip art_judge.png at exactly 0.9 (805×165 img in an 849×205 white card, -1° tilt) slides in low on a short arc (x 95–944, y 1240–1445); tapes slap on 1.84 / 1.89; floats 2 px.
- 1.68–1.90 ✗ stroke 1 (contact "own" 1.81), 1.95–2.15 ✗ stroke 2 (contact "work" 2.13) — big red marker X over robot + paper, both strokes pass below the A+.
- 1.98–2.35 droop: head sinks + tilts 13° (overshoot, settle 10°), antenna sags 34°→26° 2 f later, eyes swap to sad lids, smirk → frown, bulb goes out, body slumps (squash 0.95/1.03 → 0.97); the hand drops and dangles; the marker falls under gravity, lands flat at 2.28 on the paper's foot, bounces twice, rests by 2.48.
- 2.08–2.26 highlighter "Do not ask"; 2.27–2.53 highlighter "the model to judge itself". Hold alive to 2.58 (boil on fours, arm boil, strip float, push 1.004, grid drift).

## Measured

- Frames: 78 (ffprobe -count_packets).
- Bounds (all 78 frames diffed against a background-only render of the same runtime, threshold 40 — qa/bounds.py, qa/bounds.txt): **x 64–952, y 291–1466** — inside x 60–960 / y 285–1480 on every frame (incl. push, punch, shake, overshoots, tape pops).
- slots.py check --motion: checks passed (size, fps, duration, alpha); motion: no dead holds.

## Principles checklist

- Contact frames on words: ③/third 0.35, don't 0.65, AI 1.23 (bulb + pop), grade 1.43 (A completes + hero word + punch), own 1.81 (✗ stroke 1 mid-swipe), work 2.13 (✗ stroke 2 lands, droop starts). Yes.
- Anticipation before the hero move: the pen lifts then pulls back down-left (1.12–1.20) before darting to the A; "grade" uses the runtime hero anticipation; cards dip (cardIn). Yes.
- Overshoot + settle: "grade" 1.06 → settle, bulb 1.35 → 1, strip scale 1.012 → 1, head droop overshoots then settles, pen bounces twice. Yes.
- Parts lag the whole (2–4 f): antenna lags the head nod and the droop (2 f / 6 f), smirk widens after the A, hand → pen pop 3 f apart, tapes 5 f apart, answer bars 3 f apart, ✗ strokes staggered. Yes.
- Long moves on arcs: pen travel (x/y on separate eases), strip P.arc, falling pen drifts on a parabola. Yes.
- Squash/stretch on shapes only: robot body slump, smirk scaleX; never type. Yes.
- One focal point: number → robot drawing → A+ write → ✗ → highlighter, staged in sequence; nothing receded (receding the paper would ghost the A+, which is handwriting). Yes.
- Secondary action / no dead hold ≥ 1 s: answer typing, bulb blink, arm + marker boil, head-bob, pen bounce, strip float, grid drift, push. check: no dead holds.
- One exaggerated hero beat: "grade" 1.43 punch 1.008 + 3 px shake (impact). Yes.
- Exits faster than entrances: no exits needed (scene holds to the hard cut); the bulb rays erase in 0.12 s.
- One light direction / contact shadows: runtime card shadows (down), the strip's shadow; doodles are flat ink. Yes.
- Nothing reads as a static slide: every frame after 0.2 s has something drawing, landing or boiling. Yes.

## Readability checks

- Zone measured (x 64–952, y 291–1466). Strip at 0.9 scale (805 px wide image, serif text ≈ 40 px), one strip, M.highlight behind the phrase, no loop across lines; taped.
- No semi-transparent text: every word lands fully opaque and stays; the bulb blink is a light, not text.
- Kinetic sizes (authored): 3 = 210, grade = 176 (hero ≥ 170), its own work = 130, don't let AI = 120, third = 90 — nothing under 64. "A+" handwriting ≈ 140 px tall in marker red, readable.
- No collisions: grade ↔ paper ≥ 20 px, ✗ passes below the A+ and above "its own work", marker strokes never cross words. No speaker in this scene (no face).
- Lower zone: paper + robot reach y 1100 from 0.4–1.0 s, strip + "its own work" fill y 1110–1445 from 1.5 s.
- `.mk-hl path { fill: none }` added in the scene CSS: without it the highlighter path's default black fill showed as a thin "strike" line through the strip text while the swipe drew on (scene CSS only; runtime untouched — worth fixing in marker.css for every scene).

## Richness (hero + micro)

- HERO: the robot doodle writing its own A+ with a tracked pen on a rubber-hose arm (grade 1.43), then crossed out and drooping (own work 1.81–2.13).
- Micro 1: answer lines type themselves on the paper (don't let, 0.62–1.05).
- Micro 2: the antenna bulb lights red, rays + blinks on "AI" (1.23).
- Micro 3: smug sparkles + head-bob of pride after the A+ (1.74–2.07).
- Micro 4: the marker drops out of the robot's hand and bounces on the floor (work, 2.0–2.48).
- Micro 5: the real strip slides in, tapes slap on, highlighter swipes (1.52–2.53).

## Deviations

- Paper is 400×480 (brief ~420×520) so its 4°-rotated corners stay inside x ≤ 960 and clear "its own work".
- "grade" authored 176 (brief ~170) and "its own work" 130 (brief ~170): the full phrase at 170 is ~1300 px wide; "grade" carries the size + red, the rest sits on one 130 line low-right.
- "third" lowercase without the comma (as in the brief); "work" without the period.
- ③ digit/loop centre at (195, 422) not (190, 420): at 190 the boiling loop touched x 59 on 4 frames.
- y 1110–1480 is empty from 0.2 s to 1.5 s (the strip is timed to ~1.6 per brief); the lower 40 % still holds the paper bottom and the robot from 0.4 / 1.0 s.
- No speaker card (brief: no speaker); the starter's .spk + speaker video were removed, root data-duration kept (2.5833).
