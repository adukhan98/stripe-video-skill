# v04_evidence — evidence → build (full-screen opaque scene)

1080x1920 @30, 3.966 s authored = exactly 119 frames. Paper bg + 60px grid + vignette on every frame (identical to v01_hook),
grid drifts 20px, camera push 1.000→1.012 (origin 540,900) + 0.8% punch on "software".

## Key poses (written before animating)

| frame | t (s) | on screen | lands on |
|---|---|---|---|
| f0 | 0.00 | the 3 REA slabs from v03 (01 Decode branches / 02 Trace calls / 03 Recover the rule, top one ocean) stacked centre | "show" (0.09) |
| f0–6 | 0.00–0.20 | slabs squeeze together, labels fade, slabs flatten out | — |
| f4–20 | 0.13–0.69 | white EVIDENCE card lifts out of the merged slab top face (rotX 60→4, yaw -11→0) and slides up, overshoot/settle | "you" (0.27) |
| f9–17 | 0.30–0.56 | 6 lines of illustrative Geist Mono pseudo-code write in, 2 f apart | "the" (0.61) |
| f22–28 | 0.73–0.93 | "evidence" Fraunces italic ocean 198 pops to 108% and settles; dotted ink ellipse draws around it | "evidence" (0.93) |
| f30–36 | 1.01–1.21 | pin 1: ocean highlight on `"search.index"`, ocean pin, dotted connector, black pill "string ref" | "for" (1.21) |
| f36–42 | 1.21–1.41 | pin 2 on `idx.match(q)`, pill "call trace" | "it" (1.41) |
| f45–51 | 1.51–1.71 | pin 3 on `if hits == 0 { … }`, pill "branch" | "and" (1.71) |
| f53–60 | 1.78–2.0 | beat A type blurs up; pills retract into pins; evidence card parks top-left (scale .56, turns to face right) | "then" (1.87) |
| f60–64 | 2.00–2.13 | deep-teal app card shell rises (overshoot), header bar block lands | "build" (2.13) |
| f63–80 | 2.10–2.67 | blocks build 3 f apart: header 2.10, hero 2.20, tiles 2.30/2.40/2.50, button 2.60; dotted path draws evidence→app; three ocean riders carry the pins' evidence along it | "you" (2.27) |
| f69–73 | 2.29–2.45 | black pill "→ a version" pops on the app card's lower-left corner | "a" (2.43) |
| f74–80 | 2.47–2.67 | "version" Fraunces italic ink 206 pops; button ring pulse + light flash on the app | "version" (2.67) |
| f82–96 | 2.74–3.2 | small speaker card (350x245, face centred) rises in lower-left with 3D settle + sheen | "of" (2.85), "that" (2.99) |
| f92–100 | 3.08–3.4 | ocean ✓ badge pops on the app card, tick draws, ring pulse; evidence highlights blink in answer | "same" (3.23) |
| f106–118 | 3.53–3.966 | "software" pops; camera punch; hold alive (floats, tilt drift, pill bob, push) into the hard cut | "software" (3.69) |

## As built

- Type: "show you the" Newsreader 96 · "evidence" Fraunces italic ocean 198 · "build you a" Newsreader 96 ·
  "version" Fraunces italic ink 206 · "of that same software" Newsreader 84. Code Geist Mono 35 (copied GeistMono-Medium.ttf
  into hf/fonts), pills Geist 600 28/33.
- Speaker video: `hf/assets/speaker.mp4`, muted, `data-start 0 / data-duration 3.966` on the `<video>` only; the card is hidden
  until 2.74 s. Crop window 21.5–60.9% of source height.
- Measured content bounds over all 119 frames (transparent-background render, alpha > 24, shadows included):
  **x 78–959, y 291–1478** — inside x 60–960, y 285–1480.
- `slots.py check --motion --at 0.3,0.93,1.21,1.71,2.13,2.43,2.67,3.23,3.69` → 1080x1920, 30 fps, 3.967 s, alpha OK, no dead holds.

## Deviations

- Label pill reads "→ a version" instead of the brief's "→ your version": "your" is not spoken ("build you a version"),
  and SHARED.md allows only spoken words (same call as v05_refine's "my codebase").
- "for it and then" (1.21–1.87) is not set as type (brief omits it); the three evidence pins/pills land on those words instead.
- "evidence" is 198 px (brief ~230) and the ellipse rx is capped at 418 so the loop stays inside x 60–960.
- v03 had not been rendered when this was built, so the frame-0 slabs reuse the v06_layers slab geometry with REA's three real
  step names (top slab ocean); adjust if v03's final slabs differ.
- Speaker card included (optional in brief) as a small 350x245 card after "version" so the lower-left is not empty.
- Pseudo-code is illustrative and generic (`func search(query) … idx.match(q) … if hits == 0`), as the brief allows.

## V2 revision (user request — supersedes type sizes and speaker card above)

- Type: Inter Tight replaces Newsreader/Fraunces, upright, no italics. "show you the" 800/96 · "evidence" 900/182 ocean ·
  "build you a" 800/96 · "version" 900/204 ink · "of that same software" 800/84. Hero tracking −0.045em, supporting −0.03em,
  line-height 0.88. Pills ("string ref", "call trace", "branch", "→ a version") and slab labels in Inter 600/500; code stays Geist Mono.
- Baselines: a1 1024, a2 1284 (ellipse rx capped 418), b1 1194, b2 1378, b3 1462; pill moved up to y 1036.
- Speaker card 440x308 at (94, 662), crop 21.5–60.9% of source height; its right ~50 px tucks behind the app card, so the face sits
  centred in the visible part. Gentler tilt (rotY 18→6→5).
- Font assert: 900/800/700 "Inter Tight", 500/600 "Inter", 500 "Geist Mono".
- Timeline unchanged. 119 frames. Measured bounds (all frames, transparent-bg render): x 75–957, y 291–1474.
- check --motion: no dead holds; size/fps/duration/alpha passed.
