# v01_hook — NOTES

## Key poses (scene seconds / frame @30)
- f0 (0.00): text hook fully drawn (the most / in-demand + ocean underline / AI job of 2027), portrait card ~90 % settled (settle ends 0.32 s), paper pad fading the lower card.
- f2 (0.07): "There’s" (90 px, ABOVE "one", y base 1262) rises on the paper pad (contact 0.20); reads There’s -> one -> job.
- f19 (0.64): "one" ocean 220 px (base 1412), hero overshoot 1.10, lands on the word; f26 (0.86): "job" ink 200 px, right.
- f46-50 (1.5): phrase exits (6 f, staggered 2 f), clears for phrase 2.
- f55 (1.84-2.06): "everyone is" 112 px; f68 (2.26): "hiring" ocean 190 px, hero.
- f64-68 (2.12-2.3): job posting card cardIn (arrives with "hiring"); bars draw L->R 2 f apart; "Hiring" pill drops 5 f later; 4 f shake on impact (the one hero beat); pill dot pulses to the end.
- f103-110 (3.34-3.7): tray slides out under the posting card; 4 dashed empty seats deal in 3 f apart on "aren't enough".
- f105-117 (3.5-3.9): "aren't" / "enough" 100 px ink; f121 (4.03): "people" ink 170 px.
- f123-135 (4.1-4.5): third seat wobbles (hopeful), settles, stays empty; rings crawl to the cut; floats on card, hook, posting card.

## Principles checklist
- Contact frames on words: yes, runtime entrances start 0.13-0.2 s early; card lands with "hiring"; tray lands on "aren't".
- Anticipation: hero/pop words dip 3 f (runtime); cardIn/pillIn/enter do the same.
- Overshoot + settle: hero peaks 1.06-1.10, back.out settle; cards 1.01 -> 1; seats 1.06 -> 1.
- Parts lag the whole: bars +2 f each after card, pill +5 f, seats +3 f each, exits staggered 2-4 f, sheen lags.
- Long moves on arcs: card/tray via cardIn (tilt into travel); seats deal in on an x/y arc with rotation.
- Squash/stretch: pill only (pillIn squash); no type or logos.
- One focal point: posting card recedes (scale 0.97) when the seats arrive; one phrase at a time (exits before next).
- Secondary action: grid drift, camera push, card float/tilt, hook breathe 1 % + float, pulsing dot, apply bar breathes, crawling dashed rings; motion check: no dead holds.
- One exaggerated beat: P.shake(2.32, 2.5) as the posting card lands on "hiring".
- Exits faster than entrances: 6 f exits vs 10-16 f entrances.
- One light direction: shadows down-right from the runtime.
- Static slide? No: every second has the card float/tilt, video, grid drift and a moving object.

## Deviations
- Omitted spoken words that are filler/duplicates of the hook: "in AI", "for right now and there", "to fill". "aren't" typeset with a typographic apostrophe.
- Card is 760x776 at y 664 (brief ~760x880 / y 580-1460): the three-line hook needs y up to ~650 and the card edge must stay inside y 1480.
- Lower card fades to paper (.paper-strip inside the card) because ink/ocean words read badly on the navy sweatshirt.
- Measured bounds over all 144 frames: x 65-961, y 292-1480 (single frame f121 is 1 px past x 960; shadow-level).

## Creative pass (as built, scene seconds)
- Hook: per-letter shimmer wave across "in-demand" at 1.15 / 2.65 / 4.15 (letters hop 9 px, flash lighter, 2 f apart); underline wipes out and re-draws with a swelling flourish 1.50-2.20.
- "one": stamp-in (scale 1.45 -> 0.95 -> 1, lands 0.64) + 6-dot accent dust burst + 0.4 % camera punch.
- "hiring": letters cascade 2.02-2.30 (2.5 f apart), small letter wave at 2.85.
- Posting card (pop 2.12, unchanged): pill dot pulse + two sonar rings from 2.5 (every 0.9 s); cursor arcs in 2.55-2.97, presses "Apply" 3.02 (dip + ripple, no text), leaves 3.14.
- Seats: tray 3.34, seats deal at 3.34/3.44/3.54/3.64 (start of each deal), grey people drop into seats 1/2/4 at 3.95/4.10/4.25, squash, get bounced out (seat head-shakes); seat 3 hopeful wiggle 4.38-4.78. Seats stay empty.
- Bounds (all 144 frames): x 69-959, y 295-1479. Type scale 0.94 kept in brand.css.
