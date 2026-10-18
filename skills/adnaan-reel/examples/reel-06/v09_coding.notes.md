# v09_coding — opinion, portrait card + big marker doodles (98 f, 3.267 s) — revision 2

## Key poses (scene seconds)
- 0.00–0.97  card settled (540x660 at x270 y450 (centred in the zone, doodles + stars moved down 120 px with it), corrected un-mirrored clip); ONE lead-in line "You're probably using it for" (80 authored, fit to 880) low in the zone; cleared by a 4 f exit at 0.97 before "coding" rises
- 1.04–1.34  red `</>` (~210 px wide, stroke 14) upper-left, overlapping the card's left edge (hair/wall, never the face); contact "coding" 1.26 (190 red)
- 1.32–1.7  `</>` squat -> hop -> bounce.out settle, then idle tilt; "and" pops 1.48
- 1.52–2.32  ink doc doodle (170x210, stroke 11) right, overlapping the card's right edge in the lower half: page, folded corner, then 3 scribbled lines written at 1.90 / 2.04 / 2.18 while "knowledge" (1.74) / "work" (2.02) land (120 ink)
- 1.84/1.88 coding + and clear (4 f); 2.20–2.56 "and all these" (right, above the lower rows); 2.50 knowledge work clears; 2.62 both doodles erased (0.12 s); 2.64 "and all these" clears
- 2.84  HERO: "fancy" (215 red) slams, camera punch + 4 f shake, 8 red 4-point sparkle stars (60–96 px, two above the card) pop 2.84–3.04 around the card and twinkle; ink underline under the whole word "fancy" 3.02 (stops before "stuff."); "stuff." pops 3.14 (contact)

## Principles checklist
- contact frames on words: runtime starts words 0.13–0.2 s early; doodle strokes end on the spoken word (</> 1.26, doc lines 1.9/2.04/2.18, stars 2.84+).
- anticipation: hero words sink 2 f first; `</>` squats 3 f before its hop; stars start tiny and rotated.
- overshoot + settle: hero 1.1 then back.out; `</>` bounce.out; stars 1.28 -> 1 back.out(2.2); doc back.out(1.4).
- parts lag the whole: `</>` strokes 0.08–0.1 s apart; doc page -> corner -> lines; stars staggered 0.03–0.04 s.
- arcs: `</>` hop with tilt; doc swings in with rotation.
- squash/stretch only on shapes: the `</>` doodle (scaleY 0.94/1.06); never on type.
- one focal point: both doodles and all phrases are cleared before the "fancy" beat.
- secondary action: boil on fours on every stroke, doc sway, `</>` idle tilt, looping star twinkle (scale + 9 deg), grid drift, camera push, card float.
- ONE exaggerated beat: "fancy" (punch 1.012 + shake + stars + impact).
- exits faster than entrances: 4 f crisp exits (opacity/slide, no lingering ghosts); doodles erase in 0.12 s.
- one light direction: runtime card shadow down-right; flat marker strokes.
- not a static slide: yes.

## Richness
Hero object: marker doodle set + sparkle burst around the portrait card.
Secondary: (1) `</>` that hops on "coding"; (2) doc that writes its own scribbles on "knowledge work" and sways; (3) 8 sparkle stars that pop and twinkle on "fancy"; plus ink swash under "fancy" and the camera punch/shake.

## Deviations
- Lead-in line is ~66 px on screen (80 authored, fitted to 880 px so it stays ONE line); "and all these" is kept as a small supporting line (90 authored). 
- "fancy" is 215 authored, "coding" 190, "knowledge work" 120, "stuff." 160. Right-aligned lines sit at x 938–940 so overshoot + camera push stay under 960.
- Lines clear with a custom 4 f exit instead of the runtime's 6 f blur-up, to avoid semi-transparent leftovers.

## QA
check: size/fps/duration/alpha passed, motion: no dead holds. 98 frames. Bounds (diff vs bg-only render, qa/bounds.py): x 63–954, y 305–1477.
