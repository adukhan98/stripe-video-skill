# v14_cta — NOTES

## Key poses (scene seconds / frame)
- f0-3 (0.13): "Comment" hero 180 ink lands (contact 0.13), peak 1.05 then settle. Paper only before that.
- f10 (0.33): "FDE" hero 260 ocean in curly quotes, overshoot 1.10, camera punch 1.2 % (the one hero beat).
- f15-28 (0.5-0.95): dotted loop draws from under the quotes (right side) into the card; portrait card arcs up and settles (0.48-0.9), sheen sweep.
- f22-39 (0.73-1.29): "and I'll send you a" on the paper fade at the card's foot, one word per contact.
- f40-47 (1.3-1.57): black pill "-> roadmap" drops on the card's top-left corner (contact 1.53); headline recedes (0.94, dim, blur) at 1.42; roadmap card slides in at 1.5 on the right, overlapping the card's wall side.
- f52-65 (1.73-2.2): "to get" then "started." (136 px ocean, hero pop at 2.11); the phrase above exits at 1.5.
- f63-100 (2.1-3.4): roadmap path draws on, dots plant at 2.1 / 2.55 / 2.95, flag raises and settles at 3.35.
- f73-122 (2.42-4.05): headline returns to hero size (1.035 overshoot, settles by 2.98), pill pulses 2.9 and 3.55, card/roadmap float, loop and roadmap dots march, "FDE" breathes.

## As-built timeline
Comment 0.13 | FDE 0.33 | loop 0.5-1.05 | card at 0.9 | and 0.73 I'll 0.83 send 1.05 you 1.17 a 1.29 (exit 1.5) | pill 1.3 (contact 1.53) | roadmap card 1.5 | recede 1.42 | to 1.73 get 1.87 started. 2.11 | restore 2.42 | roadmap path 2.1-3.5, flag 3.35 | pulses 2.9, 3.55.

## Principles checklist
- Contact frames on words: yes, all entrances start 0.13-0.2 s before the word time (runtime), pill lands on "roadmap".
- Anticipation: hero words, card and pill dip first (runtime); flag/dots pop from 0.3 scale.
- Overshoot + settle: Comment 1.05, FDE 1.10, started. 1.08, headline return 1.035, card/pill/dots/flag back.out.
- Parts lag the whole: card -> sheen -> words; pill 3 f before card slide; dots lag the path.
- Long moves on arcs: card arc-in (runtime), roadmap card slides in with a rise + tilt (cardIn + x).
- Squash/stretch: pill landing squash only (shape); none on type or logos.
- One focal point: headline recedes while the pill / roadmap card are the focus, returns at 2.42.
- Secondary action: grid drift, camera push, card float, roadmap float, marching dots, FDE breathe, pill pulses; motion check "no dead holds".
- One exaggerated beat: FDE overshoot + 1.2 % punch at 0.33.
- Exits faster than entrances: phrase exit 6 f vs 16 f entrances.
- Light / contact shadows: all shadows down-right (runtime + card shadows).
- Not a static slide: something moves in every 0.3 s window through the hold.

## Deviations
- Card is 720x665 (not ~860 tall): zone ends at y 1480, and the headline stack needs y 310-715.
- The kinetic words sit on a paper fade (.cstrip, local CSS) inside the bottom 250 px of the card, because the navy sweatshirt made ink/ocean unreadable; one line each, over his chest below the chin.
- "FDE" headline wrapped in #head so it can recede without fighting breathe.
- Bounds: steady state x 62-956, y 292-1470. Transient overshoot only in f15-25 (0.5-0.83 s) when the card rises from below (runtime entrance, fading in): max y 1578. Nothing over x 960.
- Pill reads "roadmap" with an arrow glyph (the word is his).

## Creative pass (v2)
New: comment-box UI card types F-D-E (caret, send press) and its bubble flies into the headline; a paper plane leaves the speaker on "send you", flies a dotted arc and drops into a bigger roadmap card (340x420); milestones carry icons (book, wrench, code) with tick rings; flag raises and waves; FDE pulses on bubble landing and on the flag ding; rings on landing/flag. Hero times unchanged (FDE 0.33, roadmap 1.53, flag 3.35). type-scale 0.94 kept (inline "started." sized 128). Speaker card now enters at 1.0 (box owns 0.36-1.02).
Beats (scene s): tick 0.13 Comment | pop 0.33 FDE | whoosh 0.38 box rises | tick 0.52/0.60/0.68 typing | tick 0.75 send squash | impact 0.84 send press | whoosh 0.86-1.04 bubble | impact 1.04 bubble lands + FDE pulse | whoosh 0.62 card rises | whoosh 1.05 plane | ping 1.53 roadmap (pill + card, whoosh 1.5) | pop 2.11 started. | riser 2.1->2.42 then impact 2.42 headline returns | tick 2.1/2.55/2.95 milestones | ding 3.35 flag + ring + FDE pulse | tick 2.9, 3.55 pill pulses.
Bounds: x 62-956, y 302-1470 steady; transient y to 1578 only frames 18-27 (card rising in, runtime entrance).
