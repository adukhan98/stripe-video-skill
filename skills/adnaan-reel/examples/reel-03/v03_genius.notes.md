# v03_genius — key poses (written before animating; rows updated to the final build)

Full-screen opaque scene, 1080x1920 @30, 6.567 s (197 f; root authored as 6.566 s so the render is exactly 197 frames).
Paper bg + 60px grid + vignette on every frame (identical to v01_hook). Hard cut in, hard cut out.

Spoken (words.txt): "You also don't have to be a genius to set up a skill. Just copy these links and give them to your
agents and they should be able to use them immediately."

| frame | t (s) | on screen | lands on |
|---|---|---|---|
| f0 | 0.00 | paper bg; hero speaker card starts rising (+120px, rotX 24°, rotY -18°, scale .9); "you" rising | "You" (0.00) |
| f3 | 0.10 | "you also" readable; card opaque, mid-rise | "also" (0.09) |
| f10 | 0.35 | card settled (rotY -6°, rotX 5°) after small overshoot; "don't" (larger) lands | "don't" (0.35) |
| f15–24 | 0.49–0.81 | line 2 "have to be a" word by word, indented right | "have…a" |
| f27 | 0.91 | HERO: "genius" (Fraunces italic ocean ~236px) peaks at 112 % on the word, settles by f36 | "genius" (0.91) |
| f29–42 | 0.97–1.40 | hand-drawn dotted ellipse draws around "genius" (follow-through) | — |
| f37–61 | 1.25–2.05 | "to set up a" then "skill." (Fraunces italic ink) pops | "to"…"skill." (2.05) |
| f67–72 | 2.24–2.42 | Beat A type drops 30px + blur + fade, lines 2 f apart | — |
| f68–84 | 2.26–2.80 | card anticipates (102 %), then shrinks on an arc to a small card top-left (scale .645, rotY → +7° so it turns to face the action), overshoot + settle | "Just" (2.43) |
| f76–84 | 2.52–2.80 | black agent puck (robot face, ocean eyes) pops in top-right, eyes blink on | "copy" (2.55) |
| f86–94 | 2.87–3.13 | five white link pills pop in, 2 f stagger, last one lands on "links" | "these links" (2.89–3.13) |
| f96 | 3.20 | cursor (arrived on an arc) clicks pill 1's copy icon; icon → ocean check; "Copied ✓" flash | "links" → "and" |
| f103–127 | 3.44–4.23 | pills dip, then zip to chips and fly on arcs (right under the card, then up) into the puck, 3 f apart; puck bumps on each arrival; skeleton rows appear in the vacated slots | "give them to your" |
| f127 | 4.23 | last pill swallowed: puck gulp (squash 110/92 → settle), eyes squint | "agents" (4.19) |
| f131–160 | 4.38–5.32 | five skeleton "install" rows fill with ocean progress bars, eyes glance left/right | "and they should be able" |
| f151–160 | 5.02–5.32 | ocean ring closes round the puck → pulse | "to" (5.23) |
| f161–173 | 5.37–5.77 | five black notification pills stack in over the skeleton rows (rise + overshoot, 3 f stagger), last one lands on "immediately" | "use them immediately." |
| f173–196 | 5.77–6.567 | hold alive: notifications float, puck blinks, ring rotates, card floats, camera push, grid drift; hard cut | — |

## As built (final render)

**What it shows:** full-screen paper scene (same bg/grid/vignette/card treatment as v01_hook). Beat A: the live speaker clip in
the hero card (868x600 at x62 y302, rotY -9 → -7°, rotX 5 → 3.8°, ocean edge + soft shadow, face-centred crop = 23.7–62.5 % of
source height for this clip) with the kinetic serif sentence below, "genius" circled by a hand-drawn dotted ink loop.
Beat B: the card shrinks to a small top-left card (~560x387, turns to rotY +6° to face the action), a black/deep-teal agent puck
(robot face, ocean eyes) sits top-right, five white link pills (real slugs) pop in, the cursor copies one, the pills zip into
the puck, five "install" skeleton rows fill with ocean progress, the puck closes an ocean ring, and five black "ready"
notifications stack into the same rows. Hard cut in and out (no exit).

**Type sizes:** "you also" 84 + "don't" 112 (Newsreader 600) · "have to be a" 92 · "genius" 228 (Fraunces 700 italic, ocean) ·
"to set up a" 80 + "skill." 108 (Fraunces italic, ink). Pills: Geist 500 48px (owner muted / repo ink). Notifications: Geist
600/500 46px. Tooltip: Geist 600 36px.

**Timeline (slot seconds):**
- 0.00–0.60 card rises 120px with a 3D settle + light sheen; readable by ~0.15 s. Words land on words.txt: you 0.00, also 0.09,
  don't 0.35, have 0.49, to 0.61, be 0.71, a 0.81.
- 0.67–1.27 "genius" rises from 50 %, peaks at 112 % on 0.91, settles (back.out). 0.96–1.42 dotted loop draws round it (the loop
  is fitted at build time to the real glyphs: ≥15px clear of "genius", ≥10px clear of the lines above/below, inside x 66–952).
- 1.25 to, 1.57 set, 1.83 up, 1.95 a, 2.05 "skill." (pop, contact on the word).
- 2.24–2.44 Beat A type drops + blurs out (2 f between lines). 2.23 card anticipation (100.8 %), 2.33–2.73 shrink to 62.5 %
  pinned at its top-left, settle to 64.5 % by 2.97, rotY swings -7° → +6°.
- 2.50–2.98 agent puck pops (to 108 %, settle), eyes blink on 2.76; antenna light pulses from 2.9.
- Link pills contacts 2.87, 2.93, 3.00, 3.07, 3.13 ("links") — rise 60px, overshoot 103 %, settle; link icons spin in.
- Cursor fades in 2.78 at lower right, arcs to pill 1's copy icon, click contact 3.20 (scale dip), copy icon → ocean check,
  "Copied ✓" tooltip 3.23–3.55, cursor drifts off and fades by 3.58.
- 3.44 + 3 f per pill: 2 f dip, then each pill zips to a ~42 % chip while x leads and y follows late (power3.in), so it swings
  right under the card and rises into the puck from below; arrivals 3.87, 3.96, 4.05, 4.14, 4.23. Puck bumps on each, gulps
  (squash 112/90 → elastic settle) on the last = "agents" (4.19); eyes squint; ocean glow breathes.
- Each pill's slot is replaced by a soft skeleton row as it leaves; 4.38–5.32 the five ocean progress bars fill (staggered
  0.08 s), eyes glance left/right ("and they should be able to").
- 5.02–5.32 ocean ring closes round the puck ("to" 5.23), ring/puck pulse 5.24–5.6, ring then rotates slowly.
- Notification contacts 5.37, 5.47, 5.57, 5.67, 5.77 ("immediately") — 3 f stagger, rise 46px + blur → overshoot → settle, check
  circle pops, the skeleton underneath dissolves.
- 5.77–6.567 hold alive: notifications float ±4px (staggered), puck float, blink at 6.12, ring rotation, card float + tilt drift,
  video push 1.0 → 1.03, camera push 1.0 → 1.012, grid drift 20px. Hard cut.

**Measured bounds** (getBoundingClientRect on every frame, incl. camera push and 3D tilt): card x 66–954 / y 290–1010, loop
x 83–923 / y 1115–1429, pills x 77–935, notes x 87–933 / y 779–1470, puck/ring x 649–951. No flying pill ever overlaps the card.

**Deviations from the brief:**
- Copy click lands at 3.20, not 2.55: "copy" (2.55) is spoken before "these links" (2.89–3.13), so a click on 'copy' would hit an
  empty screen. The pills land on "these links" as briefed (last on 3.13), the cursor arrives during them and clicks right after.
- "you **also** don't have to be a" — words.txt has "also", so it is on screen (the brief's phrase omitted it). "don't" is set
  larger (112) for rhythm; "skill." in Fraunces italic ink.
- "genius" 228px (brief ~250) so the dotted loop can enclose its g-descender and i-dot without touching the lines above/below.
- Added secondary action for 4.25–5.37 (the brief had no beat there and the lower 60 % would have been empty): skeleton
  "install" rows with ocean progress bars in the pill slots, which the black notifications then land on; an ocean completion ring
  round the puck. The puck is a deep-teal→ink gradient (reads black; SHARED names deep teal for the agent puck).
- ✓ in the notification texts is drawn as the ocean check circle (Geist has no ✓ glyph); "Copied ✓" uses an SVG check.
- Card 868x600 (matches v01_hook) instead of 900x620 — the tilt widens the near edge; camera push 1.2 % instead of 3 %.
- Root duration authored as 6.566 s so the render is exactly 197 frames (6.567 rounds up to 198).
