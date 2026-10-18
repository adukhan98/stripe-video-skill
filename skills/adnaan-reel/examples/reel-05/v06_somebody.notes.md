# v06_somebody — NOTES (opinion, 214 f, 1080x1920 @30)

## Key poses (scene seconds / frame)
- f0 (0.00): paper world, portrait card (760x860, x178 y520) already on screen, settling 3D; "but" rising.
- f14 (0.49) "somebody" ~205 px accent lands (hero, punch 0.4 %, camera punch); dotted ellipse draws 0.70-1.25 and marches.
- f27-40 (0.91-1.35) "still has to" 90 px on paper strip over the navy chest; f46 (1.53) "set" 170 ink hero; "that" 110; f57 "whole" 110; f62 (2.07) "thing" 140 hero.
- f68 (2.26) A words blur-up out (6 f), strip clears; f70-72 card anticipates (+4,+14), then arcs to top-left and shrinks to 0.8 (608 wide) 2.34-3.0.
- f83 (2.78) workflow card enters beside it (tucked behind the speaker); f90 (3.0) five wireframe steps drop in on 4 f staggers, dotted arrows draw.
- f104-115 (3.5-3.85) magnifier drops in on an arc; f115 (3.85) "understand" pops as the lens lands on box 1 (accent edge).
- f126 (4.2) box 2 "how"; f136 (4.53) box 3 "work" (accent 178 px); f149 (4.97) box 4 "actually"; f156 (5.2) box 5 "goes on".
- f157 (5.22) "how the work" exits; f167 (5.57) "in those"; f182 (6.07-6.21) boxes tuck, then fan out on "departments" (hero), lens rides box 5; f197 "in that"; f210 (7.01) "company" accent.
- f213 (7.10): hold alive to the cut (floats, marching dots, lens bob, card sway, breathing card).

## As-built timeline
Words from words.html only ("up" is not in words.html so not shown). Groups: A (but somebody / still has to / set that / whole thing) -> B1 (That person has to / understand) -> B2 (how the work / actually goes on) -> B3 (in those / departments / in that company). Group exits 6 f, bottom band y 1130-1470 always occupied.

## Principles checklist
- Contact frames on words: every .w starts 0.13-0.2 s before its word time (runtime); box lighting/lens landings on 3.85/4.2/4.53/4.97/5.2; ellipse after "somebody".
- Anticipation before hero moves: hero words sink 2 f (runtime); card dips back before the shift (2.24); boxes tuck (x/y/scale 0.985) 0.14 s before the fan-out; lens squashes before landing.
- Overshoot + settle: heroes 1.05-1.07, card shift back.out on y/scale, boxes fan with back.out(1.5), lens landing back.out.
- Parts lag the whole: card -> sheen (runtime); 4 f stagger on nodes, 3 f on fan-out, 1-2 f on group exits, arrow draws lag the box.
- Arcs: card shift (x power3.inOut vs y back.out), lens drop-in and node-to-node glides bow left (x sine arc vs y inOut) with rotation sway.
- Squash/stretch on shapes only: boxes, rings, lens glass (P.squash); never on type.
- One focal point: speaker recedes (opacity .82, blur 2.5) 3.45-5.5 while the lens works; A has one mover at a time.
- Secondary action: grid drift, camera push, speaker/workflow float, marching dotted lines, lens bob + sway, card breathing, lit-ring glow; no dead hold >= 1 s (slots.py: no dead holds).
- ONE exaggerated hero beat: camera punch on "somebody" (0.49). The fan-out is intentionally gentle (brief).
- Exits faster than entrances: 6 f blur-ups vs 0.3-0.5 s entrances.
- One light direction: all shadows down-right (boxes 8/16, lens 12/22, cards runtime); contact shadows under cards/lens.
- Not a static slide: yes, every hold has live motion.

## Deviations
- Beat A card is 760x860 (brief ~760x900) so the B shrink (x0.8) lands at 608 wide, >= 600.
- Brief says A words exit ~2.8-2.9: they exit at 2.26 (6 f) because "That person" (2.47) needs the lower band; the card shift starts 2.34.
- Words beyond the brief's list are shown (That person has to, in those departments in that company) per "words.html only"; "understand" is a 140 px pop, not a hero.
- Workflow card x 588-948 tucks ~80 px behind the speaker card (secondary card 608 wide leaves ~290 px beside it); boxes are 170 px wide, zig-zag.
- Transient (<= 0.3 s) rise/blur frames of entering/exiting words reach y 276-1490 (measured over all 214 f: x 58-962, y 276-1490; settled content y ~292-1474, x >= 60 apart from card shadow/tilt AA at 58).

## Creative pass (v2) — what changed
- Spotlight: paper vignette tightens onto the card on "somebody" (0.3-0.85), eases off by 2.55.
- Ellipse: hand-drawn wobble + overlap; dotted arrow flick leaves the loop and curls at him (draws 1.12-1.44, head 1.40).
- Kit: gear / plug / card tiles drop on that (1.71) / whole (1.89) / thing (2.07), click together at 2.10-2.19 with accent ping rings, exit 2.32.
- Magnifier magnifies: glass shows a 1.8x copy of the steps (mirrored move + counter-rotation), faint dotted trail per hop, accent tick + ping ring on each step reached.
- departments/company: the flow branches into 3 org-chart lanes (root + 3 heads + 5 sprouts), ticks cascade 6.51-7.0, root ping on "company" 7.0.
Beat times (scene s): pop 0.49 | tick 1.40 | pop 1.71, 1.89, 2.07 | impact 2.10-2.19 | whoosh 2.34 | pop 2.78 | whoosh 3.45 | ping 3.85, 4.20, 4.53, 4.97, 5.20 | riser 5.9-6.21 | impact 6.17-6.21 | tick 6.51, 6.60, 6.69, 6.78, 6.87 | ding 7.00.
Measured over 214 f: x 58-962, y 282-1488 (transients); backup of v1 in scratchpad/v06_qa/.
