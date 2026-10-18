# v12_cta — CTA end card (V2 type + portrait card)

Full-screen opaque scene, 1080x1920 @30, 9.699 s = exactly 291 frames. Paper background, 60 px grid (drifts 20/12 px) and vignette on every frame. v1 is backed up in `edit/animations_v1/`.

**Type:** Inter Tight 900 for hero words (-0.045em), Inter Tight 800 for supporting words (-0.03em). Accent is colour only; there are no italics. Every kinetic word has the paper glow text-shadow.
**Labels:** chip and pills use Inter 600.
**Font assert:** Inter Tight 900/800/700 and Inter 500/600 are checked before anything renders.

## Layout and timeline (scene seconds)

**Portrait hero card, beats A and B**
- 800x1000 at x124 y298, radius 34, gentle tilt (rotY 5°→3.8°, rotX 3°), ocean edge, shadow, sheen, float.
- Crop covers 16.4–86.7 % of the source height: full head (hair at ~8 % of the card), face centre at ~40 %, shoulders and sweatshirt below.
- Words land only over the sweatshirt (below the chin, about y 1010) and on the paper under the card.

**Beat A**
- 0.04–0.96 "if you also" (64) + "want to try" (96), baseline 1092.
- 1.26 **REA** (230, ocean) peaks at 108 %. The agent puck (150 px) pops under it at 1.06, lights up on "REA" and bobs.
- 1.68 / 1.94 "or reverse" (64/88) and 2.30 "engineer" (96) stack to the right of REA.
- 2.68 **anything** (130, ink) on the paper under the card; the puck nods.
- 2.98–3.24 everything clears bottom-up.

**Beat B**
- 3.36 **Comment** (144) and 3.70 **“reverse”** (186, ocean, curly quotes) land over the sweatshirt, with a punch and a card dip.
- 4.12–4.74 "I'll send you the" (72/92) + **link** (124, ink) on the paper below.
- 4.60 a white chip "github.com/morluto/rea" (Inter 600, 27 px) pops on the card's top-right corner, clear of the head. It pulses on "repository" (5.48).

**Re-layout (5.50–6.24)**
- The words clear. The card compacts to 0.76 (608x760 at x100 y628).
- "Comment “reverse”" re-lands at the top as the hero (Comment baseline 410, “reverse” baseline 585).
- The "→ your inbox" pill (Inter 600, 36 px) pops on the card's right edge at shoulder height (5.98).
- The chip drops into the pill (6.10–6.38).
- 5.84–6.10 "straight to your" lands over the sweatshirt.
- 6.46 **inbox** (170, ocean) peaks; the pill pulses and its arrow turns ocean. "straight to your" clears at 6.44 to make room.
- 6.30–6.76 a dotted loop draws from "reverse" into the card's right edge, then marches to the end.

**Beat C**
- 6.62–6.98 "Just be a little" (64).
- "inbox" clears at 7.00.
- 7.28 **careful** (170, ink) peaks; the caution pill (drawn ocean triangle) pops at 7.38 and wobbles.
- 7.48–7.92 "of what you do." (72).

**End hold (8.04–9.699)**
- The card grows to 0.83 (664x830, the largest portrait that fits under the CTA), carrying the inbox pill on its right edge.
- The caution block compacts over the sweatshirt: "Just be a little" (64) + **careful** (116) on one line, then "of what you do." (64) with the caution pill.
- "reverse" gets one more pop and quote wiggle at about 8.44.
- Kept alive until the cut: header breathes, card floats with an inner push, pills pulse (8.6, 8.95, 9.3), sheen passes at 8.55–9.36, dots march, slow camera push (1.01), grid drift.
- The final frames show "Comment “reverse”" as the hero, a large face card with "→ your inbox", and the compact caution block.

## QA
- `slots.py check --motion --at 1.26,3.70,4.74,6.46,7.28,7.92,8.46,9.68`: checks passed (size, fps, duration, alpha); "motion: no dead holds".
- Bounds measured on every frame: I rendered a copy with the background hidden and took the alpha bbox (alpha > 40; shadows, glows and text glow excluded).
  Result: **x 79–957, y 289–1480**, with 0 frames outside x 60–960, y 285–1480.

## Deviations
- **Duration is 9.699 s** (291 frames, as the coordinator asked) rather than TASK.md's 9.717 / 292.
- **Extra on-screen words, all spoken:** "if you also", "or", "I'll send you the link".
- **Spoken words not shown:** "out", "just", "and", "to the repository" (the chip stands in for the repository).
- **Header in beat B:** it sits over the sweatshirt (it can't fit above the 1000 px card), then re-lands at the top when the card compacts.
- **"careful" shrinks to 116 px in the end hold** so the CTA stays the hero.
