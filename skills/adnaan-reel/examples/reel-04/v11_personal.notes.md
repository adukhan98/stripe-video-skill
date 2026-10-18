# v11_personal — key poses (written before animating)

Full-screen opaque WRAP-UP scene, 1080x1920 @30, 10.23 s (307 f). Paper bg + 60px grid + vignette on every
frame (copied from reel-03 v01_hook). Speaker (hf/assets/speaker.mp4, muted) in the tilted card the whole time:
hero 868x600 (beat A) → secondary 560x387 top-left (beat B), where four soft tiles snap into a frame shaped to it.

| frame | t (s) | on screen | lands on |
|---|---|---|---|
| f0 | 0.00 | paper; hero card rising (+130px, rotX 28°, rotY -22°, scale .88) | "our" |
| f2 | 0.06 | "our" (Newsreader 84) under the card | our |
| f16 | 0.54 | "features" (Fraunces italic ink ~186) pops to 107 %, settles | features |
| f35–43 | 1.17–1.45 | ocean strike-through draws across "features", word gets knocked down 4px | not |
| f66/71 | 2.20/2.36 | "keep you" (Newsreader 96) | keep, you |
| f79 | 2.64 | HERO "ahead" (Fraunces italic ocean 200) 110 % pop; black up-arrow chip pops at its left; 0.8 % punch | ahead |
| f85–102 | 2.82–3.40 | "of everyone else" (Newsreader 70) right-aligned at the bottom | of, everyone, else |
| f106–113 | 3.54–3.78 | beat-A type lifts out bottom-up (1.5 f apart) | I / think |
| f107–122 | 3.58–4.06 | card shrinks 868→560 and glides up-left to x72 y302 (top-left) | I think |
| f121 | 4.04 | "what's left of" (Newsreader 96) under the small card | what's, left, of |
| f155/170 | 5.16/5.66 | "software is" (Newsreader 110) right-aligned | software, is |
| f188 | 6.28 | HERO "personal" (Fraunces italic ocean ~210, full zone width) 110 % pop + 1.2 % punch; ocean underline draws 6.32–6.64; the two lines above blur up and out | personal |
| f192–205 | 6.40–6.85 | dotted slot outlines draw around the card (right column x2, bottom row x2) | built |
| f196/203 | 6.54/6.76 | "built for" (Newsreader 84) right side of the personal row | built, for |
| f200–220 | 6.66–7.34 | tiles snap into the slots one by one (T1 light, T2 deep, T3 slider, black day strip); card flattens a touch as the frame completes | built … how |
| f210–222 | 7.0–7.4 | "personal" + underline shrink to 62 % and rise next to "built for" | literally |
| f221/232 | 7.38/7.72 | "how you" (Fraunces italic ink 130) | how, you |
| f245 | 8.18 | HERO "work" (Fraunces italic ink 240) pops | work |
| f253–268 | 8.45–8.95 | secondary life: T2 toggle switches on (ocean), T3 slider knob slides, T1 bars grow (no words for "with these …") | with these … |
| f280–298 | 9.32–9.95 | day chips Mon→Fri tick ocean in a stagger | every single day |
| f283/294/301 | 9.45/9.79/10.05 | "every single day." (Newsreader 84) | every, single, day |
| f301–306 | 10.05–10.23 | hold alive: tile + card float, grid drift, camera push; hard cut | — |

## As built — V2 (Inter Tight / Inter, portrait hero card; final render)

**What it shows:** full-screen opaque wrap-up (every frame alpha 255). Type is Inter Tight 900 (heroes) / 800 / 700
(connective) with Inter 600 for UI labels; accent is colour only, no italics; all kinetic lines carry the paper glow
text-shadow. The muted speaker is in a PORTRAIT hero card 840x980 (x90–930, y306–1286, radius 34, rotY −6→−4.5°, rotX 3°;
crop window starts at 16.7 % of source height: full head + shoulders, face centre ≈ 42 % of card height).
- Beat A: the words land on the lower card (sweatshirt) and the paper below, never on the face: "our features" (ink, struck
  in ocean on "not") + "are not" → then "keep you" / "ahead" (ocean) with the up-arrow chip / "of everyone else".
- Beat B1: card scales to 700 wide (portrait, x160–860, y306–1123); "what's left of" (104) / "software is" (132) over its lower
  edge and the paper below.
- Beat B2: "personal" (ocean, ~238 px, fit 822 px) lands low-middle with punch + underline and holds 6.28–7.42 with "built for"
  small beneath; meanwhile the card reshapes to a 600x415 landscape secondary top-left and the tiles snap around it
  (bento x72–942, y310–845; day chips 70 px with Inter 34 labels). Then "personal" compacts into the "personal built for" row,
  "how you" (ink 130) and "work" (ink 240) land, day chips tick, "every single day." lands.

**Timeline (slot seconds):**
- 0.00–0.62 portrait card rises + 3D settle + sheen · 0.06 "our" · 0.54 "features" (104 % pop).
- 0.92 "are", 1.30 "not"; strike 1.17–1.45 · 1.88 "our features" + "are not" blur out.
- 2.20/2.36 "keep you" · 2.64 HERO "ahead" (106 %, 0.8 % punch) + chip 2.60 · 2.82/3.14/3.40 "of everyone else".
- 3.52–3.66 beat-A type lifts out · 3.58–4.06 card 840 → 700, centred.
- 4.04/4.42/4.62 "what's left of" · 5.16/5.66 "software is" · 5.92 both blur out.
- 6.28 HERO "personal" (105 %), punch 6.18–7.36, underline 6.32–6.64 · 6.54/6.76 "built for" beneath.
- 6.42–6.88 card reshapes to the 600x415 secondary (height + crop tween) · 6.64–7.2 dotted slots · tiles land 6.90/7.08/7.26/7.42.
- 7.42–7.76 "personal" compacts to the row (base 985) · 7.56–7.84 "built for" rises beside it · 7.64/7.72 "how you" · 8.18 "work".
- 8.42–9.0 toggle / slider / picked square · 9.30–9.92 day chips tick · 9.45/9.79/10.05 "every single day."

**Deviations:**
- Added the spoken "are not"; "softwares" never on screen. "how you" lands as a unit on "you" so "personal" holds until 7.42.
- Beat A is two phases (struck "our features / are not", then "keep you ahead / of everyone else") because the text band under
  the chin (≈ y 1060–1478) cannot hold all four lines at hero sizes.
- Secondary card is landscape 600x415 (card height and crop animate from portrait) so the bento + four text rows fit the zone.
- Overshoots reduced (104–106 %) to stay inside x 60–960 with Inter Tight widths. "else" is visible only ~0.25 s.
- Day chips Mon–Fri are UI labels per the brief.
- Measured content bbox over all 307 frames (background-free render, alpha > 50 %): x 61–958, y 287–1477; frame 0 paper only.
