# v02_world — NOTES (fullscreen, 119 f)

## Key poses (scene seconds)
- 0.00  him edge to edge, footage live (video push 1.0 -> 1.03). Strip rises 0 -> 0.42.
- 0.04-0.40 "people in the" (88, ink, .kin) low-left on the strip.
- 0.78 / 1.18  "entire" / "world." (132, ink, pop) right-aligned collage. Both blur-up out at 1.28 (2 f lag).
- 1.44-2.22  "and yet you still" (88) low-left. Exits 2.58.
- 2.40 / 2.66  "haven't" / "seen" (118, ink, pop). RED double underline sweeps left->right 2.42-2.88 (hand a step ahead of "seen"), wiped 2.76 and the line exits 2.78.
- 2.86  "the" (92) small, up-left.
- 3.08 / 3.34  "real" / "power" hero RED (170 authored, 160 on screen, overshoot 1.1, anticipation dip). 1 % camera punch on "power".
- 3.28 -> 3.70 RED marker loop around "real power" (starts 0.06 s before the word), then boils on fours to the cut.
- 3.52 / 3.80  "of" / "AI." (100) up-right; hold alive on the boiling loop + video push.

## Principles checklist
- Contact frames on words: every .w lands 0.13-0.2 s before its word time (runtime), underline/loop start before the word.
- Anticipation: hero words sink 3 f before rising; the strip rises before the first word.
- Overshoot + settle: hero 1.1 -> 1 back.out; pops 1.05 -> 1.
- Parts lag the whole: line exits lag 2 f; underline second pass follows the first; loop ends overshoot (1.12 turns).
- Long moves on arcs: none needed (type + marker only); the loop is a drawn arc.
- Squash/stretch: none on type (shapes only; no shapes here).
- One focal point: one phrase at a time, previous phrase exits (blur-up 6 f) before the next hero lands; face never covered.
- Secondary action: video push, strip rise, marker boil on fours, grid is hidden behind footage; no hold >= 1 s is dead (him talking + boil).
- ONE exaggerated beat: "power" (impact + 1 % punch + red loop).
- Exits faster than entrances: 6 f blur-up vs 10-16 f entrances.
- One light direction: soft paper glow, no hard shadows. Not a static slide: footage is live.

## Richness
Hero: "real power" (red, overshoot, punch) + the marker loop. Secondary: double underline sweeping under "haven't seen" on the words; paper strip rising as the words begin; collage layout shifting right/left per phrase; boiling marker. Fullscreen beat kept minimal (marker is the one object).

## Deviations
- Hero authored 170 (not ~200): at 200 "real power" is ~880 px wide and the loop would leave x 60-960; fit=800 keeps the loop inside the zone.
- Added the spoken connective words "people in the" and "and yet you still" (small, from words.txt) and "the" / "of AI." so the sentence reads whole.
- Double underline starts at 2.42 (on "haven't"), not 2.22 ("still"): the words are not on screen at 2.22 and an underline under empty strip looked wrong.
- Strip is taller/stronger than the default (760 px) so the 88-132 px words read over the dark polo; words sit y 1160-1470, a little above 1250 for the small lines/hero.
- marker_beats.json has 2 entries (the scene has only two strokes).

## Revision 2 (coordinator fixes)
- Footage is the corrected (flipped) speaker.mp4: face clear in every frame, no word lands on a hand (all words are on paper).
- Paper strip: fade only y 1115-1151 (above the chin line), fully opaque paper from y 1151 down, so every word sits on solid paper.
- Connective lines bumped: "people in the" / "and yet you still" 100 authored (94 px rendered), "the" 104, "of AI." 108; hero stays 170 (160 px).
- Nudged for the zone: "entire world." base 1430 with a 40 px rise, hero base 1398, loop rx trimmed. Measured over all 119 frames incl. glow and entrance trails: x 72-948, y 1141-1465 (solid content x 73-947, y 1155-1455). Nothing below y 1480 or left of x 60.
- Deviation note above about words sitting above y 1250 still applies (connectives at y ~1170-1262, hero 1275-1450).
