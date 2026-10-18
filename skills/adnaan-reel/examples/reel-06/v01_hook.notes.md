# v01_hook — notes

## Key poses (scene seconds)
| t | on screen | lands on |
|---|---|---|
| 0.00 | Hook "you're in the top" (ink 112) + "0.2%" (red 196) with the red marker loop already drawn, card ~90 % settled (portrait 740x786 at x110 y626) | frame 0 / thumbnail |
| 0.32 | card fully settled, sheen sweep done | - |
| 0.50 / 2.00 | light-wave shimmer runs through the hook's 0.2% letters | secondary |
| 1.04 / 2.44 | hook "you're" hops (on "you"); 2.50 a red marker underline is drawn under it | "you" 1.16 / 2.56 |
| 1.20-1.54 | paper strip fades in at the card's lower third | - |
| 1.54 | "built" (ink 120) pops left | built |
| 1.92 | "anything" (ink 120) pops right, letters cascade 2 f apart | anything |
| 2.12 | "with" (88) | with |
| 2.34 | "AI" (red 170) hero rise + overshoot, two ghost echoes fan out and snap back | AI |
| 2.96-3.2 | the four words blur up and out (6 f, staggered 2 f) | - |
| 3.40 | red arrow starts leaving the hook's loop, curving down the right side | anticipation |
| 3.50 | "top" (ink 110) pops | top |
| 3.76 | "0.2%" (red 230) STAMP 1.55 -> 0.95 -> 1.0, 1 % punch + 4 f shake = IMPACT; arrow head lands beside it | 0.2% |
| 3.82-3.94 | six red sparkle ticks flick out, then boil | - |
| 3.93 | black-marker DOUBLE underline scribbles under the stamp | - |
| 4.0-4.58 | everything boils on fours, hook + loop breathe, card floats, no dead hold | hold into the cut |

## As-built timeline
Exact frames: 138. Markers: loop (t=0, boils from 0.3 s), you're underline 2.50, arrow 3.40-3.82 (+ head), sparkles 3.82-3.93, double underline 3.93-4.3. Sound: beats.json (14) + marker_beats.json (5 audible strokes; this scene simply has few strokes).

## Principles checklist
- Contact frames on words: every entrance starts 0.13-0.2 s before its word (built 1.54, anything 1.92, with 2.12, AI 2.34, top 3.50, stamp lands 3.76).
- Anticipation before the hero: the stamp word hovers at 1.5x as a faint ghost from 3.50, arrow starts 3.40, AI hero dips 3 f first (runtime).
- Overshoot + settle: stamp 0.95 -> back.out to 1.0; AI peak 1.10; pops 1.05.
- Parts lag the whole: card -> sheen -> words; letters of "anything" 2 f apart, hook letters 3 f apart, echoes 2 f apart, sparkle ticks 1 f apart, double underline's 2nd stroke after the first.
- Long moves on arcs: arrow is a curved quad bulging out of the card's right edge; card enters on the runtime arc.
- Squash/stretch: none on type (rule); the stamp's 1.55 -> 0.95 is a scale impact, not squash on a shape.
- One focal point: hook sits calm while the lower words perform; during the stamp the previous phrases are already gone.
- Secondary action: breathing hook + loop, loop/strokes boil on fours, shimmer, "you're" hop, card float + video push, grid drift, camera push.
- One exaggerated beat: the 0.2% stamp (punch + shake + sparkles + double underline).
- Exits faster than entrances: 6 f blur-up vs 0.3-0.5 s entrances.
- Light/contact: shadows down-right as the runtime; paper glow (.kin) + paper strip so the words land on paper not the dark polo.
- Not a static slide: yes, every 0.5 s something moves.

## Richness
Hero object: the marker-drawn loop + arrow + stamp system (hook 0.2% -> kinetic 0.2%).
Secondaries: (1) letter-wave shimmer on the hook 0.2% (0.5, 2.0); (2) "you're" hop + red underline on the word "you" (1.16 / 2.56); (3) per-letter cascade on "anything" (1.92); (4) echoes of "AI" (2.34); (5) sparkle ticks + double underline on the stamp (3.76).

## Deviations
- v2 (approved with changes): speaker.mp4 replaced by the flipped clip (face re-checked: full head, centred); hook line 1 raised to 112 authored (about 105 px on screen) and the hook/card re-spaced (card 740x786 at y626). Hook baselines nudged (line 1 at 385, 0.2% at 578) after a 1 px top spill at the punch peak. Bounds re-measured on the re-rendered file: x 62-940, y 288-1466, 0 violations, 138 frames.
- Card is 740x786 (brief ~820) so the red accent edge clears the stamp's underline; the kinetic rows straddle the card's bottom edge on paper glow.
- The kinetic "0.2%" is a `.wx` span (not `.w`) so the runtime's hero entrance does not override the custom 1.55 -> 0.95 -> 1 stamp.
- Words "you are probably in the" are not shown as kinetic (the hook carries them).
