# v02_skills — key poses (written before animating; the "As built" section below has the final timings)

Full-screen opaque scene, 1080x1920 @30, 6.533 s (196 f). Same paper bg + 60px grid + vignette as v01_hook.
Spoken: "And if you're new to AI, don't worry. Skills are just an easy way of repackaging instructions and
resources and giving it to your agents."

| frame | t (s) | on screen | lands on |
|---|---|---|---|
| f0 | 0.00 | paper bg; secondary speaker card (560x390) already 30% visible, rising, tilted back | "And" |
| f2 | 0.08 | "if" rises in under the card (Newsreader 84) | "if" (0.08) |
| f7 | 0.22 | "you're" | "you're" (0.22) |
| f11 | 0.38 | "new" Fraunces italic ocean 240 px hits its overshoot peak; card settles ~f13 | "new" (0.38) |
| f17 | 0.56 | "to" (italic ocean 120) pops beside it | "to" (0.56) |
| f22 | 0.72 | "AI," Fraunces italic ocean 240 px peak, right-shifted line | "AI," (0.72) |
| f34 / f39 | 1.14 / 1.30 | "don't" / "worry." Newsreader 130 px | "don't" / "worry." |
| f43–51 | 1.44–1.70 | card + four lines exit up with blur, 2 f apart | — |
| f52 | 1.74 | deep-teal SKILL.md envelope card (680x480) hits its overshoot after rising 120 px | "Skills" (1.74) |
| f53 | 1.76 | "skills" Fraunces italic ocean 250 px peaks above the card | "Skills" |
| f56–63 | 1.86–2.1 | ocean dot pops, wireframe bars draw | — |
| f72 | 2.40 | ocean ping ring from the dot | "easy" (2.47) |
| f90–99 | 3.00–3.30 | "skills" glides up + shrinks to make room; card squashes (anticipation), flap presses, flips open | — |
| f99 | 3.32 | flap fully open (overshoot past flat, settles); "repackaging" lands | "repackaging" (3.32) |
| f110–115 | 3.66–3.84 | "skills" + "repackaging" exit up | — |
| f120 | 4.00 | "instructions" (Fraunces italic ocean 116) lands; strip 1 dunks into the card at 4.02 | "instructions" (4.00) |
| f123 / f127 | 4.12 / 4.22 | strips 2 and 3 dunk in, staggered 3 f, card dips on each contact; headings stay readable as index tabs | — |
| f133 | 4.43 | "+" lands | "and" (4.43) |
| f134–141 | 4.46–4.70 | four chips (Aa, swatch, image, </>) arc in from the sides, 2–3 f apart, apex over the opening, drop in | "resources" (4.58) |
| f137 | 4.58 | "resources" lands | "resources" |
| f147–152 | 4.90–5.06 | strips sink, flap slaps shut, ocean seal dot stamps (contact 5.06) | "card seals" (~5.0) |
| f152–158 | 5.04–5.26 | "instructions" / "+ resources" exit; card compacts to 50 % | "and" (5.14) |
| f160 | 5.34 | black agent puck (300 px, visor + two dim ocean eyes) pops in top-centre | — |
| f159–171 | 5.30–5.70 | dotted ink path draws from the card to the puck | — |
| f162 | 5.40 | card dips (anticipation), then slides along the path, shrinking, under the puck by 6.02 | "giving" (5.40) |
| f173 / f177 | 5.78 / 5.90 | "to" / "your" (Fraunces italic ink 124) | "to" / "your" |
| f180 | 6.00 | puck gulps (uniform squash), lights ocean (rim + glow + bright eyes) | — |
| f183 | 6.10 | "agents." Fraunces italic ocean 220 peaks; puck bob peaks | "agents." (6.10) |
| f183–195 | 6.10–6.533 | hold alive: dots march into the puck, eye blink, glow breathing, puck float, camera push; hard cut | — |

## As built (final)

**What it shows:** full-screen opaque paper scene (same bg/grid/vignette as v01_hook). Beat A: the live speaker clip in a
560x390 tilted card (ocean edge, soft shadow, face-centred crop = 21.6–60.8 % of source height) with the kinetic serif
"if you're / *new to* / *AI,* / don't worry." below it. Beat B: a deep-teal envelope card "SKILL.md" (Geist 600, ocean dot)
rises, its lid flips open, three real taste-skill headings drop in as index tabs, four resource chips (Aa, swatch, image,
</>) hop in and drop behind them, the lid slaps shut with an ocean seal, the card compacts and rides a drawing dotted path
under a black agent puck that lights ocean and bobs on "agents". Hard cut out (no exit).

**Timeline (slot seconds):**
- 0.00–0.56 card rises 96 px with 3D settle (rotX 24°→5°, back.out), sheen sweep, inner video parallax 1.14→1.
- 0.08 "if", 0.22 "you're" (Newsreader 84) · 0.38 "new" (Fraunces italic ocean 240, overshoot 110 %) · 0.56 "to" (124) ·
  0.72 "AI," (240, overshoot) · 1.14 "don't", 1.30 "worry." (Newsreader 130).
- 1.34–1.50 card + upper lines lift away (1 f apart); 1.48–1.64 "don't worry." drops away.
- 1.56–1.96 SKILL.md card rises (back.out, contact ~1.74), 1.80 "skills" (Fraunces italic ocean 270) lands under it;
  1.80 ocean dot pops, 1.86 bars draw, 2.38 ping ring (on "easy"); float + slow tilt orbit through the hold.
- 3.00 "skills" pushed out · 3.04 squash + lid press (anticipation) · 3.08–3.40 card sets down 160 px · 3.14–3.57 lid flips
  open (back.out overshoot, open ~3.33) · 3.32 "repackaging" (Newsreader 128) · 3.64 it clears.
- 4.00 "instructions" (Fraunces italic ocean 124) · strips "0. Brief inference" 4.00, "0.A Read these signals first" 4.14,
  "0.D Anti-default discipline" 4.28 fall into the pocket (card dips on each contact).
- 4.43 "+" · 4.58 "resources" (Newsreader 104) · chips Aa / swatch / image / </> hang at 4.46 / 4.54 / 4.62 / 4.70, drop in
  behind the strips (2.4 f apart).
- 4.80 strips sink · 4.92–5.08 lid slaps shut (contact 5.08, small rebound) · 5.08 ocean seal stamps · 5.06 labels clear ·
  5.12–5.44 card compacts to 50 %.
- 5.20 agent puck pops in top-centre (dim eyes) · 5.30–5.72 dotted ink path draws card→puck · 5.36 card dips ·
  5.44–6.02 card rides the path (arc, lean, shrinks to 20 %) and slides under the puck.
- 5.78 "to", 5.90 "your" (Fraunces italic ink 124) · 5.98 puck gulps · 6.02 lights ocean (rim, glow, bright eyes) ·
  6.10 "agents." (Fraunces italic ocean 220, overshoot) + puck bob peak · 6.30 blink.
- Continuous: grid drift 20 px, camera push 1.00→1.02, payoff punch +1 % at 6.02, dots march into the puck from 5.30,
  glow breathing, puck float.

**Deviations from the brief:**
- "SKILL.md" is set in Geist SemiBold, not a mono face: no Geist Mono ships in the brand kit (brand.css has Newsreader,
  Fraunces, Geist only), so I stayed on-brand instead of loading JetBrains Mono.
- Added two spoken words as kinetic captions so beat B is never uncaptioned: "skills" (on "Skills", 1.80) and
  "repackaging" (3.32). Both match words.txt (lowercased, like the hook).
- Beat B captions sit under the card (y 1060–1440) rather than beside the objects; the space above the card is kept for
  the open lid, the falling strips, the chips and later the puck. "instructions" carries the italic accent, "+ resources"
  is Newsreader ink.
- "to your agents." is all Fraunces italic, split into ink "to your" (124 px) + ocean "agents." (220 px).
- The puck is black (#141414 gradient) as the brief asks, not DESIGN.md's deep teal, so it reads apart from the deep-teal
  card.
- "And" (0.02) is not shown; the brief's on-screen text starts at "if you're".
- The speaker video clip is timed 0–1.8 s only (the card is gone by 1.50).
- Laid out at x 78–939, y 296–1471 (measured over all 196 frames) so the camera push, punch and overshoots stay inside the
  safe zone.
