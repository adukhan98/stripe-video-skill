# v13_early - opinion, portrait card + big hand-drawn sunrise (115 f, 3.834 s) - v2 re-stage

## Key poses (scene s)
- 0.00 portrait card (590x515 at x305,y765, centred under the sun) settled from frame 0; low-right slot: "We're actually" (0.00/0.36, one small line, ~66 px).
- 0.20-0.66 ink horizon line (M.line) x80-938 at y760, passes BEHIND the card (drawing layer sits under the card); pen settle 0.62.
- 1.04 "incredibly" (98, ink) top row left. 1.42 "early" (200, red hero, peak 1.07, 1 % punch) top row right on the same baseline.
- 1.18-1.9 sun (r185, ~370 px, marker outline 1.30 + hatch 1.58) sinks, rises from behind the horizon (clipped at y758), overshoots 18 px, squash, settles; glow warms in.
- 1.64-2.24 "and this is such a" in the same low-right slot (never two connective lines at once), cleared 2.2.
- 2.31-2.98 eleven rays (65-95 px) draw outward one by one, 2 f stagger, contact on "golden" 2.48; then boil + rotate 4 deg; glow pulse 2.4.
- 2.48 "golden" (130, red) low-left, letter wave 2.78, sparkles 2.62/2.70/2.78. 3.00 "opportunity" (116, ink) drops in, double underline 3.10. 3.26/3.44 "that we" in the low-right slot.

## Principles checklist
Contact frames: words land 0.13-0.2 s before their time; strokes start ~0.15 s early. Anticipation: sun sinks before rising; hero words dip (runtime). Overshoot+settle: sun back.out, hero words, pen settle, sparkles. Parts lag: hatch after outline, glow after sun, rays and letters 2 f stagger. Arcs: rays rotate about the sun, card 3D settle. Squash/stretch on the sun only. One focal point at a time (sun/early, then golden); connective line single and cleared before the next focus. Secondary action: boil, sun breathing, glow, ray rotation, sparkles, card float - no dead hold (slots.py). One hero beat: "early" + sun overshoot with 1 % punch (only impact). Exits 6 f, 8 px. One light direction (runtime shadows). Not a static slide.

## Richness
Hero: hand-drawn sunrise (horizon, clipped red marker sun, rays). Secondaries: ray boil + slow rotation on "golden"; letter waves on early/golden; sparkles; sun glow + breathing; double underline on "opportunity"; 1 % punch.

## Deviations
- Card 590x515 (y765-1280), not 600x660: it ends at ~1280 so "golden / opportunity" fit on paper below it (y1294-1475); head + shoulders kept.
- "incredibly" is 98 authored (brief ~110) so "incredibly early" fits on one baseline row (y~310-505); the sun is r185 (370 px) and rays 65-95 px so nothing touches the top row.
- Connective lines shown one at a time in the low-right slot at 64-70 px; "that we" reuses it.
- Bounds measured over all 115 frames against a background-only render (qa/bounds.py, qa/b2.py): x 64-956, y 296-1472.
