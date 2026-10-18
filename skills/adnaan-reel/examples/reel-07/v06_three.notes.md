# v06_three - Mode A (split): footage top half, paper world below (85 f, 2.833 s)
v2 of this scene (style pass v6): the floating portrait card + paper strip + tape are gone; the old file is qa/index_v1_card.html.

## Key poses (scene s)
- 0.00 `.spk split data-h=960`: footage edge to edge y 0-960 from frame 0 (no radius/shadow/float). Paper half below, content band y 1000-1480, x <= 900 below y 1200.
- 0.01-0.87 phrase 1 on paper: "you should read" (78 / 78 / ~117 px) base 1085, "the whole thing" (hero ~123 px) base 1205, x 100. Red marker underline under "whole thing" 0.74-1.0.
- 0.22-0.78 ink open-book doodle (two pages, spine, text lines, red highlighter line) at (450, 1362), bobs; phrase 1 + book = the first focal pair.
- 1.36-1.38 book, underline and phrase 1 exit (6 f) so the digits' flight path is clear.
- 1.50 digits tuck under the footage band's bottom edge; 1.62 / 1.72 / 1.82 digits 1, 2, 3 (Inter Tight 900, 196 px) spring out from behind the band on arcs and land at y 1345, x 220/480/740. IMPACT + 4 f shake at 1.64.
- 1.70 / 1.90 / 2.10 red marker loop (R 104) round each digit, 0.2 s apart; each digit pops under the pen.
- 1.95 "three" (red, 150 authored, hero), 2.07 "key", 2.29 "takeaways" (130 authored) above the numbers; numbers + phrase 2 = the second focal pair.
- 2.38 / 2.50 sparkle ticks off the 3 (right) and the 1 (left); digits sway, loops boil, footage keeps talking, grid drifts, camera push to the cut.

## Principles checklist
Contact frames on words (runtime 0.13-0.2 s early; strokes ~0.15 s early; digits 0.17 s before "three"). Anticipation: digits tuck up 14 px / shrink 3 f before springing, hero words dip. Overshoot + settle: digits back.out(1.45) + 1.12 scale then settle, pop under each loop. Parts lag: digits 6 f apart, loops 0.2 s, line 2 exit +1 f, sparkle strokes 2 f. Arcs: x power3.out vs y back.out + tilt. Squash: none (type only). One focal pair at a time: phrase 1 + book, then numbers + phrase 2 (phrase 1 gone before digits fly). One hero beat: impact + shake on digit 1. Exits 6 f (faster than entrances). One light direction (runtime). No static slide: boil, sway, sparkles, grid, push; motion check "no dead holds".

## Richness
Hero: the three numbers springing from behind the footage band, each marker-circled. Secondary: book doodle acting out "read the whole thing" + underline; sparkle ticks + sway on the circled digits; the numbers' flight out from behind the band (staging, band as the "curtain").

## Readability
Paper half measured over all 85 frames against a background-only render (qa/bounds2.py, y >= 965): x 72-900, y 965-1473 (965 = digits emerging under the band edge during their flight; nothing below y 1473; nothing right of x 900 below y 1200). Footage band y 0-960 untouched, face centred, whole head in. No text over the face or the footage. Type authored: hero 123-150, supporting 78-84 (>= 64), digits 196 px. No ghosted text (only 6 f exits). Grid breathing room: ~60 % of the paper half is empty at all times.

## Deviations
- "but here are my" still not shown (connective); "you should" shown small before "read the whole thing".
- "three" lands 1.95, just before "key" (brief said on 2.07).
- Phrase 1 exits at 1.38 (earlier than the card version) so the digits do not cross it; 'thing' is on screen 0.71-1.38.
- Digits are hidden behind the split band (z 5) until they cross y 960, which is above the 1000 content band start by design.
- beats.json: no scribble beats (per the v6 SOP).
