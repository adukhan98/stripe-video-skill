# v01_hook — NOTES (77 frames, data-duration 2.55 s, Mode A split hook)

## Layout (Mode A, v6 SOP)
- Top half: `<div class="spk split" data-h="960" data-face-at="0.44">` — his footage edge to edge y 0-960, flat (no card, border, shadow or float), whole head in with margin, chin at about y 790.
- A solid paper strip (`#hookstrip`, y 872-972, soft top edge) straddles the split line so the text hook sits on paper, never over his face.
- Text hook on frame 0: "How to be more" (base 984, 112 authored) / **ambitious** red (base 1106, 156) with a red marker double underline already drawn / "with AI" (base 1232, 112). 14+ px between lines, the underline has its own gap.
- Bottom half content band y 1000-1480, everything below y 1200 at x <= 900. One focal pair at a time:
  1. Hero lane (row y 1312-1470, right): the split-flap 1939 (230 authored), four BLANK paper flap tiles on frame 0, a flicker digit at 0.40-0.49, digits lock left to right 0.65 / 0.71 / 0.77 / 0.83, impact on 0.83, clears (exit down, 6 f) at 1.55.
  2. Left lane (same row): the black-marker student with a backpack (~172 px tall, ~10 px felt-tip) runs in from the left edge from 1.20, skids to a stop at 1.96, hops on "class".
  3. Right of "with AI": a compact black-marker alarm clock (outline ~125 px on a 150 px paper disc) — hands spin past the hour and it jiggles on "late".
  4. The row reads left to right as spoken: student -> "late" (126, red underline) -> "class" (126, hero overshoot).
- Grid breathing room: the band under the hook is otherwise empty paper; nothing in the bottom 20 %.

## Key poses (scene seconds)
| t | f | on screen |
|---|---|---|
| 0.00 | 0 | footage top half, text hook + double underline, four blank flap tiles |
| 0.40-0.49 | 12-15 | flicker digits flip in on the tiles |
| 0.83 | 25 | 1939 locked: IMPACT, 1.008 punch + 3 px shake |
| 0.95-1.40 | 28-42 | clock disc pops in, outline + ears drawn; student runs in at 1.20 |
| 1.46-1.72 | 44-52 | clock ticks and hands drawn; hands wind back at 1.76 |
| 1.55 | 47 | 1939 exits down (6 f) |
| 1.78 / 1.87 | 53 / 56 | red underline scribbles / "late" lands; hands spin 760 deg, clock jiggles, red ringing ticks |
| 1.96 | 59 | student skids to a stop |
| 2.31 | 69 | "class" lands, student hops with squash |

## Principles checklist
- Contact frames on words: 1939 locks on 0.83; "late" contact 1.87 (underline 1.78); "class" 2.31 (hero entrance 0.2 s earlier); student starts 0.13 s before "student".
- Anticipation: collapsed flap before each flip, clock hands wind back -26 deg, student leans back while braking.
- Overshoot + settle: digits lock at scaleY 1.07 then back.out; "class" peaks 1.1; student hop squashes on landing.
- Parts lag the whole: digits 0.06 s apart, hands lag the jiggle, ringing ticks 1 f apart, legs vs body bob.
- Arcs: student run decelerates (power2.out), hop is an up/down arc, hands spin on power3.inOut.
- Squash/stretch: flap cells, the student drawing and the clock disc only; never on words.
- One focal point: hook (static) + hero 1939, then student + clock, then late, then class; the 1939 clears before late lands.
- Secondary action: boil on every stroke, footage push, grid drift, student idle bob; no dead hold >= 1 s.
- ONE exaggerated hero beat: the 1939 impact (the clock jiggle is a small micro-beat).
- Exits faster than entrances: 1939 exits in 6 f; the rest holds alive to the cut.
- One light direction (shadows down-right on tiles and disc).
- Not a static slide: a new beat every ~0.3-0.5 s.

## Richness
- Hero object: split-flap 1939 (red Inter Tight 900, paper tiles with seam, flicker faces, squash-flip lock).
- Micro 1 on "student" (1.33): stick-figure student with a backpack runs in, legs on fours, skid, hop on "class".
- Micro 2 on "late" (1.87): alarm clock hands spin and the clock jiggles, red ringing ticks, red underline under "late".
- Micro 3 on "class" (2.31): "class" hero slam at the end of the row, answered by the student's hop.

## Readability
- Bounds measured on all 77 frames below the split (diff vs a background-only render) — see the report; nothing past y 1480, nothing right of x 900 below y 1200.
- No real page strips. No ghosted text (hook static; words readable or gone). Hook text sits on solid paper, not over his face or the footage. Marker strokes 9-11 px; student ~172 px; clock ~125 px; type: hook 105 / 147 / 105 px, late and class 118 px, 1939 216 px.

## Deviations
- Clock is ~125 px outline (not 170): the bottom half only allows a compact doodle beside "with AI".
- 1939 clears at 1.55 so the row can hold student -> late -> class (one focal pair at a time).
- The hook straddles the split line on a paper strip (y 872-972) instead of living wholly in y >= 1000, so all three hook lines plus the hero fit in the bottom half.
- The student is pre-drawn and slides in clipped at x 68 (not drawn stroke by stroke) so the legs can cycle.
