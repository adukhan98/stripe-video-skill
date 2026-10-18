# v07_hookup: key poses and as-built timeline

Full-screen opaque MECHANISM scene, 1080x1920 @30, EXACTLY 197 f (6.567 s, data-duration 6.5500 — re-timed after the coordinator extended the edit so "works" is spoken ≈ 6.0–6.35).
Spoken: "then hook up all the AI to the systems that the company uses for getting their work done and then make sure it actually works."
The agent puck is the hub: it drops in, four system cards deal out of it, dotted cables connect them, a pulse rides each cable,
and a big accent check pops on top of the puck on "actually works".

## Layout (scene px)

- Speaker card: small, 420x330 at (526, 302), face-at 0.55 (shows 22.7–66.9 % of the source height: hair to chest). Top-right all scene.
- Puck: 300 px built at scale 0.7 → 210 px disc, centre (510, 940).
- System cards 220x180 (wrapper `.sys` = deal/hop, inner `.uicard` = float): database (76, 668), inbox (724, 668), docs (76, 1018), CRM (724, 1018).
  Drawn icon tile, Inter 600 label, status dot (grey, turns accent), one wire bar.
- Cables: 4 dotted cubic paths from the puck rim (420/600, 880/1000) to each card's inner edge (296/724, 800/1080).
- Check badge: 200 px white disc centred (510, 770), sitting on the puck's top edge.
- Type slots: TOP-LEFT (x 76–~505, y 300–590, beside the speaker card) and LOWER (y 1220–1475).

## Key poses (written before animating)

| f | t | on screen | lands on |
|---|---|---|---|
| 0 | 0.00 | paper, speaker card settling top-right; empty centre | (then) |
| 9 | 0.30 | "hook" 130 ink top-left at contact | hook 0.41 (start 0.28) |
| 13 | 0.45 | puck hits the floor: squash, shadow full | between hook / up |
| 20 | 0.67 | "up" 130 offset right under "hook" | up 0.67 |
| 31/39 | 1.03/1.29 | "all the" 84 lower-right | all, the |
| 45 | 1.49 | "AI" 240 OCEAN hero peaks next to "all the"; puck eyes light + glow ring (puckFeed) | AI 1.49 |
| 59 | 1.95–2.0 | phrase A blurs up and out | — |
| 64–75 | 2.12–2.52 | puck squashes, four system cards deal OUT of it on arcs (4 f apart, clockwise) | systems 2.31 |
| 69 | 2.31 | "systems" 190 ink hero lower-left | systems 2.31 |
| 79–98 | 2.62–3.28 | four dotted cables draw puck → card, 3.6 f apart; dots start marching | — |
| 93 | 3.11 | "company" 110 top-left; first pulse leaves the puck (eyes glance at the card) | company 3.11 |
| 102 | 3.39 | "uses" under it; pulse 1 arrives, database dot turns accent | uses 3.39 |
| 111/119 | 3.70/3.96 | pulses 2/3 arrive (inbox, CRM) | — |
| 121 | 4.03–4.23 | "work" 120 OCEAN top-left | work 4.23 |
| 127 | 4.22 | pulse 4 arrives (docs); puck glow: all connected | — |
| 134 | 4.47 | "done" offset under "work" | done 4.47 |
| 145 | 4.85 | "work done" exits | — |
| 154/160 | 5.13/5.33 | "make" / "sure" 130 top-left; puck eyes scan left → right; card dots blink as the eyes pass | make, sure |
| 166 | 5.55 | "systems" exits (lower zone handed over) | — |
| 177 | 5.89 | "actually" 100 lower-left | actually 5.89 |
| 174–179 | 5.80–5.95 | puck squashes (anticipation) and the CHECK badge shoots up out of it, 115 % overshoot, accent ring burst, 3 px camera shake, cards hop 2 f apart | actually |
| 179–184 | 5.95–6.12 | check stroke draws; "make sure" recedes | — |
| 181 | 6.05 | "works" 240 OCEAN hero lower-right at peak | works (see deviations) |
| 182–188 | 6.07–6.30 | settle, glow, dots marching, floats — alive into the hard cut | — |

Continuous: grid drift, camera push 1.0→1.006, speaker-card float/tilt/inner push, puck bob, card floats (different periods),
cable dots marching (linear, mechanical), eye glances.

## As built (scene seconds)

- Puck: falls from the upper left on an arc (x −260→0 sine.inOut, y −480→0 power2.in, tilt −16→0), visible from frame 0 and clear of
  the speaker card. It stretches 0.32 s and lands with a squash at 0.45; the contact shadow grows with it. Eyes are dim (22 %) until 1.44, then puckFeed at 1.49 ("AI").
- Words: hook 0.41, up 0.67 (pop 130); all 1.03, the 1.29 (88), AI 1.49 (hero 240 ocean); phrase A exits 1.88–2.0, bottom-up.
  systems 2.31 (hero 190 ink, exits 5.52); company 3.11, uses 3.39 (100, exit 3.70); work 4.23 (124 ocean), done 4.47 (exit 4.80);
  make 5.13, sure 5.33 (130, recede 5.96); actually 5.89 (pop 100); works 6.05 (hero 240 ocean, peak 1.1).
- Deal: puck squash 2.14; cards 2.12 / 2.25 / 2.38 / 2.52 (clockwise), each arcs out of the puck (16 f, scale .3→1.04→1, tilt ±10).
- Cables draw at 2.62 / 2.74 / 2.86 / 2.98 (0.3 s each), then the dots march linearly to the end.
- Pulses leave at 3.08 / 3.34 / 3.60 / 3.86 (0.34 s ride); the eyes glance at each card 6 f before; the card's dot turns accent at 3.42 / 3.68 / 3.94 / 4.20 with a 3.5 % card pulse.
  Eyes recentre 4.24; puckFeed 4.26 (all connected).
- Eye scan 4.98–5.6 (−16 → +16 → 0 px); the card dots blink as the gaze passes (left 5.10/5.14, right 5.38/5.42).
- Check: puck anticipation squash 5.66, badge launches 5.79, peaks at 5.96 (115 %, +3° rotation) and settles by 6.29. Stroke draws 5.89–6.07,
  accent ring burst 5.96, glow 5.96 (holds at 45 %), 3 px camera shake 5.96, cards hop 2 f apart from 5.96.
- Speaker card: small, 420x330 at (526, 302), face-at 0.55. The whole head (hair to chest) is in on every frame; the ceiling lamp is out of frame.
- **Measured bounds over all 197 frames** (render diffed against a background-only render with no video, threshold 30): **x 66–952, y 286–1478**, 0 frames out of zone.
- Frame count 197 (ffprobe). Hold 6.3–6.567: eye blink 6.38, badge drifts up 6 px, dots march, floats. `slots.py check --motion`: checks passed; motion: no dead holds.

## Principles checklist

1. **Contact frames on words**: every word lands on its words.txt time (runtime offsets of 0.13–0.2 s). Puck contact 0.45 on "hook up", eyes on "AI",
   deal on "systems", scan on "make sure", check peak 5.96 right after "actually" (5.89).
2. **Anticipation**: the puck stretches before contact and squashes before it deals; it squashes down 9 f before the badge launches; the eyes glance before each pulse; hero/pop words sink first (runtime).
3. **Overshoot and settle**: badge 115 % → back.out; cards 104 % → back.out; dots 130 % → back.out; "AI" / "systems" / "works" overshoot (runtime hero; works peaks at 1.1).
4. **Parts lag the whole (2–4 f)**: cards deal 4 f apart, cables draw 3.6 f apart, the check stroke lags the badge, the ring and glow lag the stroke, the cards hop 2 f apart, and two-line phrases exit 2 f apart, bottom-up.
5. **Arcs**: the puck drop (x and y eased differently), the card deal (P.arc), and the pulses ride curved cables (P.ride).
6. **Squash / stretch on shapes only**: the puck disc and nothing else. No squash on type, the speaker card or cards (cards use a uniform scale pulse).
7. **One focal point**: A puck → "AI"; B the cards/cables (type is secondary at 100–124 px); C the check + "works", while "make sure" recedes (P.recede).
8. **Secondary action, no dead hold ≥ 1 s**: marching dots, card floats on 4 different periods, puck bob, eye glances and blinks, grid drift, camera push, speaker-card float. `--motion` reports no dead holds.
9. **One exaggerated hero beat**: the check badge launch at 5.96 (115 %, ring burst, shake, card hop). Nothing else shakes or punches.
10. **Exits faster than entrances**: exits are 6 f blur-ups (runtime) against 10–16 f entrances. All exits finish by 5.72; the scene holds alive into the cut.
11. **One light direction / contact shadows**: every shadow falls down-right (runtime cards, puck shadow, badge shadow); the puck has a contact shadow that grows as it lands.
12. **Not a static slide**: every frame has the dots marching plus at least one moving part.

## Deviations

- RESOLVED by the coordinator (range now ends 44.747, scene 197 f): **"works" was not in words.txt.** The EDL range ends at 44.48 s and the next starts at 45.17 s. The ASR puts "works." at 44.54–45.22, and
  source audio shows a soft tail at 44.5–44.75, so the spoken "works" is cut out of the edit. I still show "works" (hero 240 ocean, landing 6.05 s)
  because the brief asks for it and it completes "actually works". The coordinator may want to extend that range end to ~44.75, or drop the word.
- Omitted spoken words: then, all-but-"systems" of "to the systems", "that the", "for getting their", "and then", "it". "the" is kept in "all the AI".
  No words were paraphrased. "company uses" and "work done" are added as smaller top-left phrases so the captions track the speech.
- "hook up all the AI" is split: "hook / up" top-left (beside the speaker card), "all the AI" lower-right under the puck. This keeps the lower
  zone filled and puts "AI" right under the agent. The lower zone is empty only from 0 to ~0.9 s while the puck falls.
- The speaker card is 420x330 (taller than the 306 preset) with face-at 0.55, so the whole head fits a landscape card.
- The check badge sits on top of the puck's upper edge rather than covering it, so the eyes stay visible.

## Creative pass (coordinator request) — still 197 f, same hero times, runtime untouched (`--type-scale: 0.94` honoured; "AI" now sized in em so it scales too)

New on top of the approved v1 (backup: scratchpad/v07_qa/index.v1.html):
- **Puck personality**: a drawn antenna (ink stem + bulb) trails while falling and whips with drag/follow-through on every jolt (land 0.45, "AI" 1.49, each deal flick 2.12–2.52, 2.6, hop 4.6, launch 5.79). The bulb lights with the eyes on "AI" and flashes as each pulse leaves.
  The eyes now FOLLOW each pulse out along its cable. When all four connect (4.26) the puck does a happy ^^ squint plus a hop: anticipation squash 4.13, up 4.23, land squash 4.60. The glow ring flashes, then breathes 4.95–5.75.
  It squints happily again from 5.99 through "works" and reopens at 6.36.
- **Rope cables**: each cable draws out sagging under gravity, then snaps taut with an elastic rope wobble (from 2.72 / 2.84 / 2.96 / 3.08, 0.5 s). Riders follow invisible taut ghost paths, so the render is deterministic.
- **Data flow**: after each card connects, accent packets flow out to it and smaller dark-accent packets flow back. They loop every 0.62 s until the cut.
- **Cards come alive on arrival**: database storage layers stack in; inbox gets a new-mail dot sliding in as the tray dips; CRM's avatar fills accent and its rows shuffle twice; docs' page lines write themselves.
  Each card also fills an accent progress bar (CRM shuffles instead).
- **"actually works"**: a ring of 16 accent and accent-dark dots bursts from behind the check badge, then drifts down and fades (5.96–6.52). The cables flash accent once. All four cards do a synchronized happy hop (tiles lag 2 f), and a smaller second bounce follows at 6.26.
- Measured bounds over all 197 frames: x 66–952, y 292–1478, 0 out of zone. ffprobe 197. `slots.py check --motion`: passed, no dead holds.

### Beat times (scene s) for SFX
whoosh 0.00 (puck fall) · pop 0.45 (land) · ping 1.49 (wakes: eyes + bulb + ring) · tick 2.12 / 2.25 / 2.38 / 2.52 (deal) ·
whoosh 2.62 (cables draw, through 3.08) · tick 2.72 / 2.84 / 2.96 / 3.08 (rope snaps taut) · ping 3.42 / 3.68 / 3.94 / 4.20 (pulse arrives, card wakes) ·
pop 4.26 (all connected: squint + hop + ring) · impact 4.60 (hop lands, soft) · whoosh 4.98 (eye scan) · riser 5.66→5.79 (squash before launch) ·
ding 5.79 (badge launch) · impact 5.96 (badge peak + shake + confetti + cable flash + card hop) · pop 6.26 (second card bounce).
