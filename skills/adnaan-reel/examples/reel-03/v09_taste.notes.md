# v09_taste — key poses (written before animating)

Full-screen opaque wrap-up scene, 1080x1920 @30, 10.167 s (305 f). Paper bg + 60px grid + vignette on every frame
(identical to v01_hook). Speaker clip (hf/assets/speaker.mp4, muted) lives in the tilted card the whole time and changes
size per beat: hero 868x600 → orbit centre 560 → small top-left 420.

| frame | t (s) | on screen | lands on |
|---|---|---|---|
| f0 | 0.00 | paper only; hero card starts rising (+70px, rotX 28°, rotY -22°, scale .9) | "You" (~0.0) |
| f3–13 | 0.10–0.44 | small line "you just need to" (Newsreader 64) word by word under the card | you / just / need / to |
| f17–35 | 0.56–1.18 | "give your AI agents" (Newsreader 96) | give … agents |
| f47–63 | 1.56–2.10 | "good *design* sense" (104 / Fraunces italic ink 124) | good, design, sense |
| f74 | 2.48 | "and" (84) | and |
| f80 | 2.68 | HERO "taste" Fraunces italic ocean 250 — pops to 110 %, settles; tiny camera punch | taste |
| f84–96 | 2.80–3.20 | lines 1–3 lift + blur out (2 f apart); "and taste" glides up-left on an arc and shrinks to 66 % | — |
| f94–112 | 3.14–3.74 | "they will not build" (88) | they … build |
| f119 | 3.98 | "slop" Fraunces italic ink 230 pops; ocean strike-through draws across it 4.04–4.30 | slop |
| f127–133 | 4.24–4.44 | "for you" (72) next to slop | for, you |
| f135–142 | 4.50–4.74 | all text lifts out; card shrinks (868→560) and drops to the centre (510, 900) | These / skills |
| f139–167 | 4.62–5.55 | dotted ink ring (r 380) draws clockwise from 12 o'clock behind the card | skills … that |
| f149/154/160/166/168 | 4.95/5.13/5.33/5.47/5.59 | coins 01–05 spiral out from behind the card, overshoot the ring, settle on it | will / help / you / do / that |
| f167–180 | 5.59–6.00 | ring slowly orbits (dots march), coins drift with it and float | — |
| f172–181 | 5.74–6.03 | coins retract behind the card (2 f apart), ring fades | literally |
| f178–192 | 5.94–6.40 | card arcs up-left and shrinks to 420 (top-left) | literally / just |
| f187–200 | 6.24–6.70 | black prompt box rises in (880x325), send button pops, caret blinks | — |
| f193 | 6.43 | "copy and" (Newsreader 120 / 72) right of the card | copy, and |
| f191–205 | 6.36–6.84 | cursor arcs in from lower right to the box | — |
| f207 | 6.91 | cursor click dip; HERO "paste" Fraunces italic ocean pops | paste |
| f209–221 | 6.96–7.36 | five white chips (01 Taste Skill · 02 Design & Refine · 03 Layers · 04 Meng To · 05 Hallmark) drop in, 3 f apart | these |
| f222 | 7.40 | caret jumps after the last chip; send button dips; cursor leaves | into |
| f230 | 7.65 | dotted path draws, black pill "Claude" pops below the box | Claude |
| f251 | 8.35 | second path, pill "Codex" | Codex |
| f270 | 8.99 | third path, pill "whatever" pops, then grows word by word: agent 9.27, you 9.65, use 9.79 | whatever … use |
| f294–304 | 9.80–10.167 | hold alive: pill float, caret blink, card float, grid drift, camera push; hard cut | — |

## As built (final render)

**What it shows:** full-screen opaque wrap-up on the shared paper/grid/vignette background. The live speaker clip
(muted, face-centred crop = 22.4–61.3 % of source height, which also keeps the laptop sticker out of frame) sits in the
same tilted card as v01_hook (868x600 at x62 y310, ocean edge + soft shadow) and changes size per beat: hero card over
a kinetic serif stack → 560 px card at the centre of a dotted orbit with coins 01–05 → 420 px card top-right over a
black prompt box that gets five skill chips pasted in and fans out to three agent pills.

**Timeline (slot seconds):**
- 0.00–0.62 card rises + 3D settle (rotX 28→5° with overshoot, inner video parallax, light sheen). 0.00–0.44 "you just need to" (64).
- 0.56–1.18 "give your AI agents" (96) · 1.56–2.10 "good *design* sense" (98 / Fraunces italic ink 120) · 2.48 "and" · 2.68 HERO "taste" (Fraunces italic ocean 250, 108 % pop + settle, 1.2 % camera punch).
- 2.72–2.98 lines lift out bottom-up (1.5 f apart) while "and taste" glides up-left on an arc to 66 % (2.80–3.14).
- 3.14–3.74 "they will not build" (88) · 3.98 "slop" (Fraunces italic ink 230) · 4.05–4.33 ocean strike-through draws across it · 4.24/4.44 "for you".
- 4.46–4.96 type lifts out (2 f apart), card shrinks 868→560 and drops to (510, 900) with a rotX settle; 4.62–5.57 dotted ring (r 380) draws clockwise from 12 o'clock.
- Coins 01–05 spiral out from behind the card and land on the ring at 4.95 / 5.13 / 5.33 / 5.47 / 5.59 (will / help / you / do / that), orbit overshoot + scale pop, then float; ring dots march and the orbit drifts 7°.
- 5.70–6.05 coins pop out (anticipation 2 f, 1.5 f apart), ring fades; 5.98–6.46 card arcs to the top-right (560→420).
- 6.26–6.76 black prompt box rises in, toolbar bars + ocean send button pop, caret blinks. 6.36–6.84 cursor arcs in from lower right.
- 6.43 "copy", 6.73 "and", 6.91 HERO "paste" (Fraunces italic ocean) + cursor click dip; 6.86–7.37 chips "01 Taste Skill · 02 Design & Refine · 03 Layers · 04 Meng To · 05 Hallmark" drop in 3 f apart; 7.38 caret jumps to the end, send button presses, cursor leaves.
- Dotted connectors draw, then pills pop: "Claude" 7.65, "Codex" 8.35, "whatever" 8.99 growing word by word (agent 9.27, you 9.65, use 9.79), staying centred.
- 9.80–10.167 hold alive: pill float, caret blink, card float + slow tilt, video push, grid drift, camera push 1.0→1.015. Hard cut, no exit.

**Deviations from the brief:**
- On-screen words match words.txt exactly, so "& taste" → "and taste", "copy & paste" → "copy and paste" (the ampersand would not be the spoken word), and the third pill reads "whatever agent you use" (spoken), not "any agent you use".
- Added the spoken "you just need to" (small 64 px line; "You" is missing from words.txt and is placed at ~0.0–0.1) and "for you" after "slop".
- Hero card 868x600 (same as the revised v01_hook) instead of 900x620: the 3D tilt widens the near edge, and 868 keeps it inside x 60–960.
- Coins land on "will … that" (4.95–5.59) rather than starting on "skills" (4.73): until ~4.95 the shrinking card still covers the top coin slot. The ring starts drawing on "these/skills" (4.62).
- Beat C: the small card goes top-RIGHT with "copy and paste" to its left, so the card's path from the centre never crosses the type; chips carry their muted coin numbers 01–05 for continuity; the prompt box has a generic ocean send button and two faint toolbar bars (no brand UI, no placeholder copy).
- Total camera push 1.5 % (+1.2 % punch on "taste") instead of 3 %, to stay inside the zone.
- Measured content bbox over all 305 frames (render without background, alpha > 50 %): x 62–958, y 286–~1477.
- Duration authored as 10.166 s so the render is exactly 305 frames.
