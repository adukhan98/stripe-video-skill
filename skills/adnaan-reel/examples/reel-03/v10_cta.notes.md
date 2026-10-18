# v10_cta — CTA end card (last shot of the reel)

Full-screen opaque scene, 1080x1920 @30, 4.033 s = 121 frames. Same paper bg + 60px grid (20px drift) + vignette as v01_hook.
No exit: the reel ends on this frame.

## What it shows
- **"Comment"**: Newsreader 600 ink, 144 px, centred, baseline 410.
- **“design”**: Fraunces 700 italic ocean, 196 px, with the quotes at 0.78 em, centred, baseline 602.
- **Hand-drawn dotted line**: ink, 3.2 px, dasharray 2 12, round caps. It starts just under the "g" of design, loops once and
  tucks under the top edge of the speaker card. It draws on through a mask, and its dots march slowly for the whole slot.
- **Speaker card**: muted live video, 580x415 at x98 y770. It is tilted (rotY 8° to 6°, rotX 5° to 3.5°, rotZ -2° to -1.4°) and has
  the ocean edge and a soft drop shadow. The face-centred crop covers 24.2–64.4 % of the source height. The video freezes from 2.43 s, as in the asset.
- **Coin tower**: five white neumorphic coins, 110 px, numbered 01–05. They stack up out of a black pill reading "→ your inbox"
  (Geist 600 36 px, 280x84). The pill overlaps the card's bottom-right corner. Each coin rolls out from behind the card on an
  arc and drops onto the stack with a small squash, and the coins below and the pill take the weight (a 5 px bump).
- **Kinetic phrase**: "and I will **send these**" (66/88 px) / "straight to your" (70/64 px) + ***inbox*** (Fraunces italic ocean 134 px).
  The on-screen words are exactly the words in words.txt.

## Timeline (slot seconds)
| t | frame | what happens | word |
|---|---|---|---|
| 0.00–0.11 | f0–f3 | "Comment" rises from 25 % opacity with blur; contact f3, 4 px overshoot, settles by ~0.35 | comment (0.00) |
| 0.02–0.32 | f1–f10 | opening quote pops (back.out 2.2) and leads the eye | — |
| 0.04–0.21 | f1–f6 | "design" rises from 55 % scale with blur; **peaks at 107 % on 0.21**, then settles with back.out by 0.55 | design (0.21) |
| 0.22–0.52 | f7–f16 | closing quote pops | — |
| 0.40–1.00 | f12–f30 | dotted line draws down from "design", loops, reaches the card | — |
| 0.44–1.06 | f13–f32 | card rises 56 px, scale .84→1, rotX 28°→5° with overshoot, inner video parallax 1.16→1, light-sheen sweep | — |
| 0.59 / 0.81 / 0.97 | — | "and" / "I" / "will" rise in (0.38 s power3.out, starting 0.13 s early) | and / I / will |
| 0.86–1.28 | f26–f38 | pill pops (to 106 %, settles) and is ready to receive the coins | — |
| 1.13 | f34 | coin 01 lands in the pill; "send" | send (1.15) |
| 1.33 | f40 | coin 02 lands on the stack; "these" | these (1.35) |
| 1.54 | f46 | coin 03; "straight" | straight (1.57) |
| 1.84 | f55 | coin 04; "to" | to (1.87) |
| 2.00 | f60 | coin 05 tops the stack; "your" | your (2.03) |
| 2.17 | f65 | **"inbox" peaks at 106 %** and settles; pill pulses to 108 %, the arrow nudges 9 px and turns ocean, 1 % camera punch | inbox (2.17) |
| 2.40–4.03 | f72–f120 | end hold, speaker frozen. Still moving: coin stack and pill float 6 px, each coin rocks ±5° (staggered), dots march, card float 6 px + slow orbit + inner push to 1.04, second sheen pass 2.7–3.6, camera push 1→1.016, grid drift | — |

## QA
- `slots.py check --motion --at 0.1,0.21,1.0,1.13,1.54,2.0,2.17` reports size, fps, duration and alpha OK, and "motion: no dead holds". The only
  PROBLEM lines are "first/last frame is not fully transparent", which is expected for a v2 opaque scene.
- Measured content bbox over all 121 frames: x 79–954, y 293–1476, inside the zone x 60–960, y 285–1480.

## Deviations from the brief
- **“design” is 196 px, not ~230.** At 230 px the word plus its quotes is about 930 px wide, more than the 900 px zone. 196 px, with the quotes at 0.78 em,
  is the largest size that stays inside x 60–960 through the overshoot and the camera push.
- **The card is 580x415.** The brief asks for ~620x430 and SHARED SCALE gives ~560x390 for a secondary card. 580x415 is the largest card that fits with the
  big header, the loop and the two-line phrase; it also keeps a clear gap between the card and the phrase.
- **"inbox" is 134 px, not ~140.** This is the widest size that keeps "straight to your inbox" on one line inside the zone.
- **"Comment" is 144 px, not ~150.**
- **The spoken "and" is shown on screen** (Newsreader 66 px), so the on-screen text matches words.txt exactly.
- **How the coins "slide into the pill":** they roll out from behind the speaker card and stack upward out of the pill, which acts as the tray / inbox. There is one coin per word:
  send, these, straight, to, your.
- **The camera push totals about 2.6 %** (1.016 slow push + 1.01 punch), not 3 %, so the full-frame content stays inside the safe zone.
- **Kinetic text runs through the caption band** (y 1250–1480). This is intended: v2 has no subtitles.
