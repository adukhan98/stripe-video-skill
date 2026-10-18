# v08_job (fullscreen, 113 f)

## Key poses (scene s / frame)
- f0: him edge to edge, push 1.0 -> 1.03 starts; paper strip fades in 0-0.3 s.
- 0.10-0.23 (f3-7) "the", 0.34 / 0.47 (f10-14) "job" pop, 0.61 / 0.77 "of", 0.84 / 0.97 "the": low-left stack (96 px ink).
- 0.93 anticipation, 1.13 (f34) FDE contact (hero, overshoot 1.10, settle), 1 % camera punch on 1.13.
- 1.45-2.55 FDE breathes 1.8 % (secondary action) while the push and his gestures carry the hold.
- 2.40-2.50 phase 1 exits (blur-up 6 f, lines lag 2-3 f).
- 2.60 (f78) "aren't" pop at 2.76; 3.06 "that" (f92); 3.32 (f100) "many" accent back.out; hold alive to f112.

## As-built
Words low, left stack (96 / 108 px ink) + right hero (FDE 260 -> fit, many 210 accent), baselines 1424-1466 so everything sits under his beard (chin reaches y~1300 when he leans in). Nothing else on screen.

## Principles checklist
- Contact frames on words: entrances start 0.13-0.2 s before data-t (runtime).
- Anticipation: FDE sinks 2-3 f before rising; pops dip.
- Overshoot + settle: FDE 1.10 -> 1.0 (back.out 1.6); many back.out 2.2.
- Parts lag the whole: second stack row exits +2 f, FDE +3 f; words stagger 2-6 f.
- Long moves on arcs: none (no travelling objects; brief forbids objects).
- Squash/stretch on shapes only: no shapes, none applied to type.
- One focal point: one phrase on screen at a time (phase swap at 2.4-2.6); speaker is the context.
- Secondary action: 1.03 video push, 0.6 % cam push, FDE breathe, his live video; no static hold >= 1 s (motion check: no dead holds).
- One exaggerated hero beat: FDE overshoot + 1 % punch at 1.13.
- Exits faster than entrances: 6 f blur-up vs 12-14 f entrances.
- One light direction / contact shadows: paper glow only, no objects.
- Not a static slide: footage + push + breathing + staggered type.

## Deviations
- Brief wanted ~150 px "aren't that many" and all words y >= 1380. His chin/beard reaches y ~1300 and the zone ends at 1480, so a 150 px line fits nowhere without covering the chin. Built as 108 px stacked "aren't / that" + 210 px "many" and 96 px "the job / of the" + FDE (fit-shrunk from 260). FDE is ~260 nominal; width fit 860.
- Phrase 1 split over two rows ("the job" / "of the"); paper strip 700 px tall, fades in. "of" after "many" and "that's"/"and right now" omitted (not in brief).
- Small non-hero rise (data-rise 34) to keep entrances inside the zone.
- #fde breathe added via a timeline tween in the script (no runtime change).

## Creative pass (v2)
- FDE: letters F/D/E are separate blocks that drop 55 px (blur-in, slight rotation, power3.in slam) with contact at 1.000 / 1.067 / 1.133 (2 f apart); last block = IMPACT 1.133: shared hop (-10 px, 1.03) + back.out settle, 1 % camera punch, thin accent shockwave ellipse (rx 30 -> 262) + paper-white echo ring 3 f later, both behind the type and inside the zone.
- many: letters m,a,n,y rise 2 f apart (m contact 3.32, blur clears in 5 f), then 'a' (3.44) and 'n' (3.47) flicker down and settle at 50 % / 70 % opacity ("not many" thinning, still readable).
- type scale 0.94 honoured (brand.css), runtime untouched. Bounds 69..961 x 1227..1480 (961 = ring tail at 1.47), 113 frames.
