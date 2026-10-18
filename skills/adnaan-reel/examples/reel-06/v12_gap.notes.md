# v12_gap — THE GAP (explainer, bespoke) — 165 f @30 (5.5 s)

Spoken: "The gap in what AI can do and what people believe it can do is the greatest opportunity we have in our hands."

## Key poses (scene s / frame)
| t | f | on screen | word |
|---|---|---|---|
| 0.27 | 8 | "The **gap**" (110 ink + 190 red hero) top-left, pencil y-axis drawing | gap |
| 0.62 | 19 | axes done (L, arrowheads, no numbers); red curve starts at left | what |
| 1.60 | 48 | red curve has bent up to vertical at x≈874; dust burst + 3 zings off the tip; "what AI can do" being written beside the tip | do |
| 2.55 | 77 | flat ink line across the same span, low; "what people believe" written under it | believe |
| 3.12 | 94 | red curly bracket between the red tip and the ink line's end, nib pointing left into the gap; red curve climbs a bit more, bracket stretches | can do |
| 3.60 | 108 | "The gap" + axes gone; whole chart has glided up 255 px; "the / greatest" upper-left | greatest |
| 4.11 | 123 | **opportunity** (red) lands IN the gap, bracket nib flicks at it, camera punch | opportunity |
| 4.75 | 143 | small speaker card has risen from the bottom-left corner; "in our" right of it | in |
| 5.33 | 160 | "hands" (ink) lands, red underline draws under it; held alive into the cut | hands |

## As-built timeline (scene seconds)
- 0.01 "The" (rise) · 0.27 "gap" hero (overshoot+settle; hidden until its contact) · 0.70–2.90 g/p of "gap" drift apart ±10 px (the gap widening) · exit 3.08 (6 f blur-up)
- 0.12–0.38 pencil y-axis, 0.30–0.60 x-axis, arrowheads 0.40/0.62 · erased 3.00 (0.14 s)
- 0.62–1.60 RED curve (`M.line`, hand accelerates: power1.in so it whips into the vertical) · 1.00–1.78 note "what AI can do" (Caveat 700, 84 px, ink, left of the curve's vertical part)
- 1.60–2.20 dust burst (7 dots on gravity arcs) · 1.62–1.76 three marker zings, erased 2.25
- 1.84–2.54 INK flat line · 2.08–2.94 note "what people believe" (Caveat 700, 84 px, ink, under the flat line) — both notes stay fully opaque to the cut
- 2.80–3.14 red curly bracket (two strokes meeting at a sharp nib) · 3.06–3.48 red curve climbs 40 px more · 3.08–3.74 bracket stretches (scaleY to 1.062 with overshoot, scaleX 0.9→1 volume)
- 3.06 chart anticipation dip (+8) → 3.16–3.58 glide up 255 (power3.inOut) → 3.58 back.out settle
- 3.37 "the" · 3.63 "greatest" (accent rise)
- 4.11 "opportunity" hero (data-size 170, data-fit 820, red) + P.punch 1.01 · 4.06–4.58 bracket nib flick (scaleX 1.55 → back.out) · 4.62 second smaller flick
- 4.33–4.95 speaker card (small, 430×334, face-at 0.63; corrected un-mirrored clip) rises out of the zone's bottom edge (slot clip at y≈1472, opened 4.50–4.75 so the soft shadow shows) · 4.75 "in" · 4.95 "our" · 5.33 "hands" pop · 5.24–5.44 red underline
- Always on: grid drift, camera push 1.006, marker boil on fours, card float + 3D drift.

## Principles checklist
- **Contact frames on words**: every word entrance 0.13–0.2 s before its words.txt time; curve tip lands on "do" (1.60/1.63), bracket on "can do" (2.93–3.05), opportunity 4.11, hands 5.33.
- **Anticipation**: chart dips 8 px before gliding up; hero words dip/sink before rising (runtime); card starts low/behind before arcing in; the bracket squeezes (scaleX 0.9) as it stretches.
- **Overshoot + settle**: hero words (gap, opportunity) ×1.06 then back.out; bracket stretch overshoots 3 % then settles; chart glide overshoots then back.out; card overshoot.
- **Parts lag the whole (2–4 f)**: dust dots staggered 1 f; zings 1 f apart; bracket upper then lower stroke; "in"→"our"→"hands"; card → sheen → video push.
- **Long moves on arcs**: card enters on the runtime arc (x and y eased differently); dust on gravity arcs; chart glide is a straight vertical camera-like move (short, eased).
- **Squash/stretch on shapes only**: bracket (stretch with the climb, nib flick) — never on type.
- **One focal point**: curve → ink line → bracket → opportunity → card/hands; axes erased before Beat B; the notes stay fully opaque (readability rule) and sit outside every word's box.
- **Secondary action, no dead hold ≥ 1 s**: marker boil on fours, gap letters drifting, red curve still climbing, card float/3D drift, grid + push. slots.py motion: "no dead holds".
- **One exaggerated hero beat**: "opportunity" — punch 1.01 + nib flick + impact SFX ("gap" gets the first impact SFX but no punch).
- **Exits faster than entrances**: "The gap" 6 f blur-up, axes erased in 0.14 s, zings 0.16 s.
- **One light direction / contact shadows**: only the speaker card carries a shadow (runtime, down); marker strokes are flat ink on paper.
- **Not a static slide**: something draws, moves or boils on every frame.

## Richness (hero + secondary)
- HERO: the hand-drawn gap chart — red curve whips up to vertical, flat ink "belief" line, red curly bracket measuring the gap, nib pointing at "opportunity".
- 1. Dust burst + marker zings off the red tip as it goes vertical ("do", 1.60).
- 2. The bracket stretches as the red curve keeps climbing ("can do", 3.06), and its nib flicks at the word ("opportunity", 4.11).
- 3. Type that performs: the letters of "gap" drift apart while the chart's gap opens (0.7–2.9).
- 4. Red marker underline lands under "hands" (5.24); he rises out of the bottom edge "in our hands".

## QA
- Render: render.mov, 165 frames (ffprobe), prores 4444 1080x1920 @30.
- slots.py check: size, fps, duration, alpha passed; motion: no dead holds.
- Bounds (diff vs a background-only render, qa/bg.mov, every frame): solid content (diff > 60) x 65–941, y 288–1480, 0 frames out; at diff > 24 the only pixels past y 1480 are the card's soft drop shadow (to 1519) from 4.53 s on.
- Card crop (corrected, un-mirrored speaker.mp4): whole head incl. hair top, beard and collar in every frame (checked zoomed at 4.62 / 5.0 / 5.45).

## Revision 2 (coordinator pass)
- Caveat notes 66/64 → 84 px, fully opaque to the cut (removed the 72 % recede). "what AI can do" moved left of the vertical part (x 350), "what people believe" under the flat line (x 330).
- Made room: flat ink line raised 40 px (1300 → 1260), bracket bottom 1250 and nib re-aimed, red climb to y 560, chart shift 240 → 255, "opportunity" baseline 995 → 935, card y 1126 h 334.
- Re-checked the card crop on the replaced (un-mirrored) clip.

## Deviations
- "opportunity" is authored 170 (house hero floor) but `data-fit="820"` shrinks it to ~150 px on screen so it fits IN the gap left of the bracket nib — the brief's ~190 would be ~930 px wide in Inter Tight 900 and could not fit the zone at all.
- Added unlabelled pencil axes in Beat A (no numbers/labels) so the chart reads as a chart and the lower zone isn't empty before the lines draw; erased at the restage.
- Beat B restage: "The gap" exits and the whole chart glides up 255 px (3.1–3.6) to free the bottom band for the speaker card + "in our hands".
- Words shown: The gap / the greatest / opportunity / in our hands; the notes are the spoken phrases "what AI can do", "what people believe". "and", "it can do", "is", "we have" are not shown as kinetic type.
- The card entrance (runtime: rises from 140 px below) is clipped by a full-frame slot at the zone's bottom edge so it never draws below y 1480; the clip opens after it lands so its shadow is soft, not cut.
