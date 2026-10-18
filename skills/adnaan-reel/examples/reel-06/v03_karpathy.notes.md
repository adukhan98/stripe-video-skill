# v03_karpathy — key poses (written before animating)

204 f @30 (6.7833 s data-duration). Spoken: "Andrej Karpathy, who is the co-founder of OpenAI now at Anthropic,
posted a breakdown of how differently people are using AI across the spectrum."

| t (s) | on screen | lands on |
|---|---|---|
| 0.00–0.17 | real avatar as a POLAROID (360x420, -5°) arcs in top-left, overshoots; small speaker card (440x370) top-right already settling | Andrej |
| 0.15 / 0.39 | "Andrej" (130 ink) left + "Karpathy" (150 ink) right-aligned below the polaroid | Andrej / Karpathy |
| 0.22 | masking tape pressed onto the polaroid top (polaroid dips) ; photo "develops" 0.1–1.4 | — |
| 1.21 / 1.59 | "co-founder of" (84 ink) | co-founder / of |
| 1.77 | BIG OpenAI chip (72 px logo + "OpenAI" Inter 600 56) pops lower-left under "co-founder of" | OpenAI |
| 1.98–2.43 | RED marker arrow draws (shaft, then head) from the OpenAI chip down-right; Caveat "now at" (72) writes on the arrow | now / at |
| 2.49 | BIG Anthropic chip (same size) swings in on a pendulum, squash-lands lower-right at the arrow head | Anthropic |
| 2.68–3.40 | name clears; OpenAI chip/arrow/note fade 2.84–2.9; speaker card shrinks out; polaroid AND the Anthropic chip fly up into the top-right cluster (chip sticks on the polaroid's corner, 0.6 scale, stays all of beat B) | — |
| 3.14 | REAL post card (header + "sharp funnel" strip, 840 wide = 0.877 scale) rises into the lower-middle, 2 tapes pressed on, camera punch = HERO beat | posted |
| 3.42 | X logo chip pops on the card's top-right corner | — |
| 3.70 | "breakdown" (150 ink) lands top-left under "posted a"; at 4.0 the letters of "down" sag one by one | breakdown |
| 4.22–4.62 | post card glides up to the top; the REAL stats strip slides out from under it | — |
| 4.50–4.80 | black marker underlines "6.2m Views" on the strip; kinetic "6.2m views" (120 RED) flies out of it, odometer 0.0→6.2 locks | differently |
| 5.06–5.80 | black ticks under 1.9k / 5.6k / 42k / 29k in rhythm | people / are / using / AI |
| 6.00–6.55 | red spectrum wave draws left→right under everything, 4 ink tick marks | across |
| 6.12–6.62 | "across the" (72) + "spectrum" (130 ink) | across / the / spectrum |
| 6.62–6.78 | hold alive into the cut (boil, float, push, grid) | — |

## As built (scene seconds)
- Polaroid 360x420 (photo 320², real `karpathy_avatar.jpg`) at (96,322), frame tilted -5°. Arcs in 0–0.17 from lower-right *inside* the zone
  (x power2.out / y power3.out, scale .6→1.05→1, tilt -12→1.5→0), tape pressed 0.22 (frame dips .975), photo develops 0.12–1.42
  (sepia/washed/blur → full colour), 3 px float. Recedes to .75 at 1.62. 2.76 anticipation dip, 2.86–3.36 flies to the top-right corner
  (x leads on power2.out, y + scale on power2.inOut, 0.42 scale, rotates to +5°), above the exiting speaker card.
- Small speaker card 440x370 at (500,336), face-at .56 (whole head + collar), on from frame 0; shrinks/blurs out 2.84–3.07.
- "Andrej" 130 / "Karpathy" 150 (ink, hero) 0.15 / 0.39; recede 1.62; exit 2.74–2.96. "co-founder of" 84 on 1.21/1.59, exit 2.72.
- OpenAI chip 120 tall (official logo 72 px + Inter 600 56 px) at (76,1150), pops 1.77. Red marker arrow (286,1286)→(470,1362) 1.98–2.43
  (shaft then head flick). Caveat "now at" 72 px on the arrow 2.12–2.50. Anthropic chip, same size, at (486,1300)–(~886,1420): pendulum
  (pivot above it, -14° → 5° → -2° → 0) 2.12–2.49, squash-lands 2.49. OpenAI chip, arrow and note fade 2.84–2.90.
  The Anthropic chip is KEPT: anticipation dip 2.68, flies 2.78–3.20 (y power2.inOut, x power2.in → arc; scale 0.6; tilt -8 → -4 back.out)
  to the polaroid's top-left corner (centre ≈ 740,342), above the post card in z-order, squash-sticks 3.22, visible to the cut.
- REAL post card = post_header.png + post_funnel.png as one white card, 840 wide (0.877 scale), first lands lower-middle (top 960):
  rise 110 + blur + rotX 2.98 → contact 3.14 (overshoot 1.02, settle back.out) + 0.8 % camera punch (HERO). Tapes 3.22 / 3.30 (card dips),
  X logo chip pops on the corner 3.42. 3 px float.
- "posted a" 72 (3.14/3.34), "breakdown" 150 hero 3.70 (peak 1.04); 4.0–4.2 the letters of "down" sag 14 px one by one and bounce back.
- 4.20–4.64 card glides up to top 535; the REAL stats strip (post_stats.png, 840 wide) slides out from under it 4.28–4.82.
- 4.48–4.72 black marker underline under "6.2m Views" on the strip; "6.2m views" (120 RED) flies out of that stat 4.50 → lands 4.80,
  odometer digits roll 0→6 (locks 4.80) and 0→2 (locks 4.90); pulse 5.9.
- 4.93 / 5.11 / 5.37 / 5.67 black ticks under 1.9k / 5.6k / 42k / 29k (on people / are / using / AI).
- 6.00–6.55 red spectrum wave (1.5 periods) draws left → right at y≈1446; 4 ink tick marks 6.18 / 6.29 / 6.40 / 6.51.
  "across the" (≈70 px) 6.12/6.34 + "spectrum" 124 hero 6.62. Holds alive into the cut (boil on fours, floats, grid drift, push).

## Principles checklist
- Contact frames on words: every kinetic word uses the runtime entrance (0.13–0.2 s early); polaroid lands 0.15 (Andrej), chip pops 1.77,
  Anthropic lands 2.49, post card contact 3.14 (posted), number lands 4.80 (differently ~4.74), ticks on people/are/using/AI, "spectrum" 6.62.
- Anticipation: hero words dip (runtime); polaroid dips 3 f before it flies to the corner; squash pre-stretch on the Anthropic chip; card dips under each tape.
- Overshoot + settle: polaroid 1.05 → 1; post card 1.02 → 1 back.out; number 1.05 → 1; chips pop 1.08 → 1; pendulum overshoots -5° → 2° → 0.
- Parts lag the whole: tape after polaroid (+2 f); arrow head after shaft; note after arrow; tapes 3.22/3.30 then X chip 3.42; stats lag the card's glide by 3 f; "down" letters 3 f apart; odometer digits lock 0.1 s apart.
- Long moves on arcs: polaroid in and to the corner (x/y on different eases), number flies out of the stat on an arc (x power2.out / y power3.out), chip on a pendulum.
- Squash/stretch on shapes only: the Anthropic chip (as briefed) and the polaroid/post card press dips; type never squashed.
- One focal point: name + polaroid recede when the chips take over; beat A clears before the post lands; speaker card leaves for beat B.
- Secondary action, no dead hold ≥ 1 s: photo developing, live speaker video, marker boil, floats, grid drift, camera push, letter sag, odometer, stat ticks (slots.py: "no dead holds").
- One exaggerated hero beat: post card lands on "posted" with the camera punch (impact).
- Exits faster than entrances: 6–7 f exits vs 10–16 f entrances.
- One light direction / contact shadows: all cards/chips use the runtime's down-right soft shadows.
- Nothing reads as a static slide: something moves in every second.

## Richness (hero + micro-animations)
- HERO: taped polaroid of the real avatar → OpenAI → Anthropic marker arrow between official logo chips → the real X post taped on.
- Polaroid DEVELOPS from washed-out to full colour while "Andrej Karpathy" lands (0.12–1.42).
- Anthropic chip swings in like a hung sign and squash-lands at the arrow head ("Anthropic"), then flies up and sticks onto the polaroid so "now at Anthropic" stays visible through beat B.
- "breakdown": the letters of "down" sag one by one (pun, readable).
- "6.2m views" flies OUT of the real stat after a marker underline and rolls like an odometer ("differently").
- Rhythmic black ticks under the real 1.9k / 5.6k / 42k / 29k ("people are using AI").
- Spectrum wave + 4 ticks drawn left → right ("across the spectrum"), setting up the 4-tier funnel.

## QA
- Frames: 204 (ffprobe). slots.py check: "motion: no dead holds · checks passed: size, fps, duration, alpha channel".
- Bounds (diff vs a background-only render, every frame, threshold 24): x 62–951, y 287–1478 — 0 frames outside x 60–960 / y 285–1480.
- Post text shown at 0.877 scale (840 px card) — readable.

## Deviations
- Speaker card is in beat A only (exits at 2.84): beat B has no room for a ≥420 px card without covering post text or dropping "breakdown".
- Revision 2 (coordinator): chips rebuilt big in the lower half; the Anthropic chip flies with the polaroid into the top-right cluster and
  stays through beat B (OpenAI chip/arrow/note exit). Speaker clip replaced with the un-mirrored one; crop re-checked (whole head + collar).
  During its 0.4 s flight the chip briefly passes over the polaroid while the post card is still fading in.
- "now at" is a Caveat handwritten note beside the arrow rather than a kinetic line; "who is the", "how differently people are using AI"
  are not shown as words (they are acted out by the underline/number/ticks instead).
- "6.2m views" at 120 (brief ~110), "co-founder of" 84 (brief ~80, house minimum for supporting), "Karpathy" 150 / "Andrej" 130 (brief ~120).
- Post card first lands lower-middle (fills the lower zone) and glides to the top at 4.2 to make room for the stats strip.
- Tapes sit on the top edge of the card (inside the zone) rather than hanging over the corners; the X chip takes the top-right corner.
