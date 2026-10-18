# v08_hallmark — key poses (written before animating)

Full-screen opaque scene, 1080x1920 @30, 5.533 s (166 f). Paper bg + 60 px grid + vignette on every frame (same as v01).
Skill #5. Layout: header row (coin 05 · title · small speaker card) on top, demo cards in the middle, kinetic serif at the bottom.

| frame | t (s) | on screen | lands on |
|---|---|---|---|
| f0 | 0.00 | coin 05 (white, 210 px) mid-pop top-left; "fifth" rising; speaker card + real site card start rising | "Fifth" (0.00) |
| f5 | 0.15 | "one" lands; coin flips (rotY 180) to its ocean face | "one" (0.15) |
| f15 | 0.49 | "Hallmark." Fraunces italic ocean (~220 px) peaks at 110 %, settles by f22; site card (usehallmark.com) settled below, scrolling slowly | "Hallmark." (0.49) |
| f26–33 | 0.86–1.10 | "fifth one" lifts out, site card drops back and fades | — |
| f28–40 | 0.92–1.32 | "Hallmark." arcs up and shrinks into the header (turns ink), coin shrinks to 150 px | — |
| f30–43 | 1.00–1.42 | bland white design card rises centre with a soft 3D settle | — |
| f36 / f40 | 1.19 / 1.33 | "run" / "an" | "run", "an" |
| f44 | 1.47 | "audit" (Fraunces italic ocean) pops; ocean scan line starts sweeping down the card (1.40–2.15) | "audit" (1.47) |
| f46–58 | 1.54–1.95 | four grey pins drop on the problem spots as the scan passes them | "of your design" |
| f75–83 | 2.50–2.75 | "run an audit" clears | — |
| f78–90 | 2.60–3.00 | design card swings left on an arc; checklist card slides out from behind it to the right | "and they'll" (2.67–2.85) |
| f98 / f107 / f115 / f124 | 3.27 / 3.56 / 3.85 / 4.14 | checklist rows land one by one, grey ✗ pops: Generic layout · Weak hierarchy · Default styling · Cramped spacing | "all" … "improve" |
| f98–108 | 3.27–3.61 | kinetic "all the / things" (things = Fraunces italic ink) | "all", "the", "things" |
| f128–132 | 4.28–4.40 | "all the things" clears | — |
| f134–143 | 4.45–4.75 | rows flip to ocean ✓, 3 f apart; the matching pin pops off the design card | "and then go" |
| f135–153 | 4.50–5.10 | design card morphs into the polished deep-teal version (bg first, then each block re-lays out, 2 f stagger) | "go ahead" |
| f142–151 | 4.75–5.03 | "go ahead and" | "go", "ahead", "and" |
| f154 | 5.15 | "improve" Fraunces italic ocean peaks 110 %; polished card pops 102.5 % + ocean ring; tiny camera nudge | "improve" (5.15) |
| f161 | 5.38 | "it." lands | "it." (5.45) |
| f161–165 | 5.38–5.53 | hold alive (float, grid drift, push) into the hard cut | — |

## As built (final)

**What it shows:** skill #5 chapter, then a 3-beat demo of what Hallmark does. Full-screen opaque (paper + 60 px grid + vignette,
same as v01), hard cut in and out. Header row (all scene): coin 05 + title + a small live speaker card (330x230, top-right,
muted `assets/speaker.mp4`, face-centred crop 24.5–63.7 % of the source height, ocean edge, slow tilt + float).

**Timeline (slot seconds):**
- 0.00–0.65 CHAPTER: coin 05 (210 px) pops on frame 0 and flips (rotY 180, back.out) to its ocean face by ~0.45; "fifth" (on frame 0) / "one" (0.15) Newsreader 104 px; the real site (`assets/hallmark_site.png`, "Make your AI agent a designer.") rises in a tilted browser card (usehallmark.com) and scrolls slowly; "Hallmark." Fraunces italic ocean (fitted to 800 px wide) pops to 110 % at 0.49 and settles.
- 0.81–1.32 handoff: site card drops back and fades (gone by 1.03), "fifth one" lifts out, "Hallmark." shrinks fast, arcs up into the header beside the coin and turns ink; coin shrinks 210→150 px.
- 1.03–1.45 bland white design card (centred, wireframe: centred grey hero, grey button, generic image, three cramped cards) rises with a 3D settle. "run" 1.19, "an" 1.33 (Newsreader 120), "audit" Fraunces italic ocean 232 px pops at 1.47.
- 1.43–2.18 ocean scan line + soft glow sweeps down the card (linear, mechanical); four grey pins drop with a ping as it passes the heading (~1.55), button (~1.66), image (~1.73), card row (~1.95).
- 2.50–2.70 "run an audit" clears. 2.60–3.10 design card swings left on an arc (rotY +7, scale .97); the checklist card slides out from behind it (rotY −7).
- 3.27 / 3.56 / 3.85 / 4.14 rows land (grey ✗ pops, label slides in, matching pin pulses): Generic layout · Weak hierarchy · Default styling · Cramped spacing. Kinetic "all the" (3.27/3.47) + "things" Fraunces italic ink (3.61).
- 4.26–4.40 "all the things" clears. 4.45 / 4.55 / 4.65 / 4.75 rows flip to ocean ✓ (check draws on, row tints ocean), each matching pin pops off the card.
- 4.42–5.10 design card morphs to the polished deep-teal version (anticipation dip, bg → #0D2731, colours first, then every block re-lays out with a 2 f stagger: big left-aligned heading, ocean button, ocean image block, asymmetric cards; ocean edge appears).
- "go" 4.75, "ahead" 4.89, "and" 5.03 (Newsreader 100); "improve" Fraunces italic ocean pops at 5.15 with the card pop (102.5 %), ocean ring, light sweep and a small camera nudge; "it." lands 5.38. Holds alive into the hard cut.
- Continuous: grid drift 20 px, camera push 1.0→1.015 (+0.6 % nudge at the end), card/coin/speaker floats, speaker video push.

Measured content bbox over all 166 frames (pixels clearly off the paper): x 63–956, y 288–1477 — inside the safe zone.

**Deviations from the brief:**
- Added the small live speaker card in the header (the brief for this slot doesn't mention one; included because the video was to be embedded; same "small card, keep the speaker" pattern as v03).
- The chapter title doesn't leave: it shrinks into a header (coin 05 + "Hallmark.") for the demo, like the approved style_refine frame.
- ✗ / ✓ are drawn as SVG strokes: Geist has no U+2717/U+2713 glyphs (a fallback face would be used). Row labels are Geist 500 34 px.
- Kinetic words shown are exact words from words.txt: "fifth one", "Hallmark.", "run an audit", "all the things", "go ahead and improve it." ("of your design", "they'll give you", "that you should improve" are carried by the graphics, not set as type).
- "it." lands at 5.38 instead of 5.45 so it has settled before the cut. Hero sizes are fitted to the zone width ("Hallmark." 800 px wide, "improve it." 815 px wide, ≈ 195–205 px type) and overshoot origins chosen so pops never cross the safe zone.
- Duration authored as 5.533 s → exactly 166 frames.
