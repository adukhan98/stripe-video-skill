# t4_stanford — v7 "MINT" VISUAL mode with camera travel (152 f, 5.05 s)

Spoken: "One, talk to it instead of typing. A Stanford study showed that speaking was three times faster than typing."

## Build idea
- **One world, two areas, one camera.** Everything lives on world layers (`#worldM`, `#worldU`) that share the same GSAP
  camera tweens (x / y / scale, origin 0 0). World = frame at pose 0 (t3's end). Each AREA container carries the inverse
  of the camera pose that frames it, so its contents are authored in plain screen px:
  - pose 0 = identity (THE HABIT CHAIN, t3's last frame)
  - pose A = scale 1.70, t (−200, −352): push in on disc 1 (disc 1 → screen (310, 600), Ø306)
  - pose B = scale 1.50, t (−716.5, −1240.6): area B sits 360/620 world px down/right of area A
- **Feathered zone mask** (`#viewM`): the travelling layer is masked to the content zone (minus the IG corner) with a
  16 px-σ soft edge, so things leaving during a camera move dissolve before the zone edge instead of crossing it. The mask
  starts 80 px low and tightens over 0.03–0.23 s so frame 0 is t3's frame exactly (disc 6 + shadow intact). The wide
  area-B objects that never travel (strip card, race, 3×, "faster") live on the unmasked `#worldU`.
- **Chain = t3's HABIT CHAIN block, copied verbatim** (CSS + JS between the BEGIN/END markers, re-copied after t3's final
  FACE change) — `buildHabitChain` + `setHabitChainEnd` at t = 0. The flip uses t3's built-but-hidden mint backing disc
  (microphone glyph) as the back face.

## Key poses (scene s → what lands, on which word)
| t | pose | word |
|---|---|---|
| 0.00 | THE HABIT CHAIN exactly as t3 ends: his face in disc 1 (mint 8 px ring), discs 2–6 charcoal, connector | (cut) |
| 0.03–0.10 | anticipation: face disc squashes 0.93, camera pulls back 1.5 % on disc 1 | One |
| 0.10–0.20 | face (with its mint backing) turns edge-on (rotateY 90) | One |
| 0.20–0.42 | mint MIC side swings round (back.out), scale 1.1 → 1, glyph lands 2 f later | One |
| 0.06–0.36 | connector + discs 2–6 slide outward with the world and dissolve (1 f stagger) | — |
| 0.10–0.52 | camera push 1.0 → 1.7 on disc 1 (power3.inOut) | — |
| 0.36 | '1' tag (charcoal pill, Inter 700) pops on the disc edge | — |
| 0.43 / 0.85 | "talk" (mint hero) / "to" "it"; mint sound rings + disc pulse on talk & it | talk / it |
| 1.01 | charcoal keyboard disc pops (0 → 1.12 → 1), glyph +2 f; "instead" | instead |
| 1.27 / 1.39 | "of" / "typing." (pop) | of / typing |
| 1.33–1.55 | clean strike (charcoal 11 px over a paper-coloured 26 px under-stroke) draws across the keyboard; it droops −7° | typing |
| 1.56–1.64 | travel anticipation: camera nudges up-left 10/14 px | — |
| 1.64–2.22 | CAMERA TRAVEL down/right on an arc (x power2.inOut, y power3.inOut), scale 1.715 → 1.5 | A, Stanford |
| 1.97 | Stanford wordmark card pops (arrives during the travel) | Stanford |
| 2.21 | "study" (Inter 600, 64) | study |
| 2.32–2.57 | REAL strip (stanford_2.png at 1.0, 880 wide) slides up into place, settles back.out | showed |
| 2.70–3.0 | race card in; mic (mint) + keyboard (charcoal) icons pop 2 f apart | speaking |
| 3.02 | race starts: both bars run on the same ease, typing at exactly 1/3 the distance | speaking |
| 3.36–3.62 | mint-soft highlighter (deep-mint edge) swipes behind "3.0x faster" | three |
| 3.47 → 3.94 | PEACH 3× pops as "1×", odometer rolls 1 → 2 (3.62) → 3 (3.80, back.out) + pulse | three times |
| 3.93 | HERO: mint bar hits the finish — stretch 4 f before, squash (0.95 × 1.2) on contact, finish line kicks, mint flag pops 0 → 1.2 → 1; "faster" (190, charcoal hero) lands; camera punch | faster |
| 3.93–5.05 | typing bar keeps crawling (1/3 → 0.4), keyboard keys keep tapping, flag flutters, camera drift 1.5 → 1.515 | than |
| 4.47–4.95 | typing keyboard slumps and wobbles | typing |

## Principles checklist
- **Contact frames on words**: every word/object lands on its words.txt time (hero/pop entrances start 0.16–0.2 s early);
  mic on One, keyboard on instead, strike on typing, wordmark on Stanford, strip on showed, highlighter + 3× on three, finish on faster.
- **Anticipation**: disc squash before the flip; 1.5 % camera pull-back before the push; 10/14 px counter-nudge before the
  travel; stretch before the bar's contact; runtime dips on hero words; pop() anticipation on discs/tag/card.
- **Overshoot + settle**: flip back.out, disc scale 1.1 → 1, pops 1.12–1.14 → 1, strip −6 px/1.004 → 0, odometer back.out, flag 1.2 → 1, 3× 1.08/1.07 → 1.
- **Parts lag the whole**: glyphs 2 f after their discs; chain discs dissolve with 1 f stagger; race icons 2 f apart; strike under-stroke → top stroke 1 f.
- **Arcs**: the travel bows (x and y on different eases); the push is anchored on disc 1.
- **Squash/stretch on shapes only**: face disc, mint bar, flag — never type or the wordmark.
- **One focal point**: area A (mic vs struck keyboard → words), then wordmark → strip → race; the old area leaves the
  frame with the camera instead of competing; discs 2–6 dissolve as the push starts.
- **Secondary action / no dead hold ≥ 1 s**: sound rings + disc pulses (0.4–1.4), keyboard droop, camera drift A (0.52–1.56),
  odometer, keys tapping (3.0–4.9), flag flutter, typing crawl, keyboard slump, camera drift B. `slots.py --motion`: no dead holds.
- **One exaggerated hero beat**: 3.93 — bar squash + flag + "faster" + camera punch.
- **Exits faster than entrances**: nothing exits; area A leaves with the 0.58 s camera move; chain dissolves in 0.15 s.
- **One light direction**: all discs/cards cast soft shadows straight down (disc-shadow / card shadows), no outlines.
- **Not a static slide**: the camera is always moving (push, drift, travel, drift).

## Richness (hero + secondary)
- Hero: the flat speaking-vs-typing RACE (mint bar 3× faster, finish squash + flag) — on "speaking" → "faster".
- Secondary 1: face → mint microphone FLIP (3D rotateY) + '1' tag + mic sound rings — on "One", "talk", "it".
- Secondary 2: the struck keyboard disc that droops — on "instead of typing".
- Secondary 3: PEACH odometer 1× → 2× → 3× — on "three times"; typing keyboard keeps tapping then slumps — on "typing".

## Readability
- Zone measured (diff vs background-only render `qa/bg.mov`, every frame, `qa/bounds.py`):
  threshold 24 → **x 63–956, y 306–1466, 0 frames outside x 60–960 / y 285–1480, 0 in the IG corner (x > 900, y > 1200)**;
  threshold 10 (faint shadows) → x 61–958, y 298–1477, 0 violations. Includes the camera moves, overshoots and punch.
- Real strip: stanford_2.png at scale **1.0** (text ≈ 38 px, 3 lines, 880-wide card), highlighter behind the spoken phrase
  "3.0x faster" (multiply, mint-soft + deep-mint edge). One strip.
- Kinetic sizes (authored): talk to it 200 (hero), instead of 110, typing. 120, faster 190 (hero), 3× 200 (fit 228);
  labels: study 64 (Inter 600), race labels 44 px Inter 600 (UI labels inside a card).
- No semi-transparent text at rest: words only pass through the soft mask edge while the camera travels (≈ 4 f).
- Logo: real Stanford wordmark SVG (supplied file, not recoloured — its cardinal is the real thing), 410 px on a white card.
- No red accent, no marker layer, no Caveat (marker.css/js not loaded). Peach only on the 3× data.

## Seam with t3_six
`scenes.py seam t3_six t4_stanford` → mean diff **4.0** (whole frame; t3's "I'd steal from them." words are the
difference). Chain region (x 180–760, y 600–1480) mean Δ 0.9; disc 1 ring/position identical — only the footage inside the
face circle differs (his head moves between t3's last source frame and this window's first frame: continuous take).

## Deviations
- Strip card is 880 wide (x 70–950), not ≥ 900: a 900 card + shadow would leave the zone; the image is at scale 1.0
  (> 0.85), so it is as readable as briefed.
- "study" is 64 px (brief ~56) to respect the 64 px floor.
- The structural pop sits at 0.20 (the visible contact: the mint side swinging in), not 0.10 (the flip starts at 0.10).
- The chain discs 2–6 dissolve while the world pushes in (pure camera geometry would leave disc 3 under "talk to it").
- The typing bar reaches exactly 1/3 at 3.93, then keeps crawling to 0.4 by the cut (alive, honest).
- "One", "A", "showed that", "was", "than typing" are not set as kinetic words (the '1' tag, the strip, the race labels and
  the slumping keyboard carry them).
