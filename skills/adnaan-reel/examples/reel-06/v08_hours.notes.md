# v08_hours — NOTES

## Key poses (planned before authoring; frame @30 fps, scene seconds)

| frame | t | on screen | lands on |
|---|---|---|---|
| 0 | 0.00 | small speaker card top-left (420x380, whole head) on paper | "You" |
| 15 | 0.50 | "using" / "more" collage top-right of the card | "using more" |
| 29 | 0.97 | **agentic** (RED hero 200) lands low-left, ink loop draws around it | "agentic" |
| 49 | 1.63 | "capabilities" (110 ink) lands right-aligned under it | "capabilities" |
| 85 | 2.85 | words glide up 175 px; dark terminal card slides up into the lower zone, Claude Code chip drops onto its top edge, prompt line types glyph blocks | "Claude Code" |
| 112 | 3.75 | Codex chip squash-lands beside it, 2nd prompt line types | "Codex" |
| 120 | 4.00 | beat A words blur up; terminal glides to the top-right corner at 0.5x and recedes | "to" |
| 135 | 4.51 | hand-drawn 3x7 calendar draws on fast (box, header, rings, grid); "complete" lands | "complete" |
| 151 | 5.03 | "tasks" lands; tiny task scribbles appear in the days | "tasks" |
| 163–174 | 5.43–5.81 | "used to" / "take" top-right column | "used to take" |
| 186 | 6.21 | "weeks" (ink 150) lands; RED zig-zag strikes all 21 days in one sweep | "weeks" |
| 192 | 6.40 | red strike through "weeks"; calendar collapses into the clock centre | "in" |
| 199 | 6.63 | hand-drawn alarm clock pops; minute hand starts two full turns, speed ticks | "couple" |
| 211 | 7.03 | **hours** (RED hero 220) lands bottom-left, 1 % punch, bells rattle | "hours" |
| 216 | 7.20 | clock still spinning/boiling, all held alive into the cut | — |

## As built — v2 (coordinator pass: bigger objects, band of words, no ghosted text, corrected clip)

| t | event |
|---|---|
| 0.00 | small speaker card (x76 y314, 420x380, face-at 0.52) — corrected (un-mirrored) clip; whole head + collar in every frame |
| 0.43 / 0.65 | "using" (96) / "more" (130, pop) top-right — exit 3.80 |
| 0.97 | **agentic** RED hero 180 (x130 base 1010); 1.12–1.52 ink loop around it (clears the word), wiped 2.24 |
| 1.63 | "capabilities" 110 ink |
| 2.28–2.80 | dip → both lines glide up 160 px (capabilities lags 2 f) |
| 2.62 | terminal card (--brand-deep, 850x320) rises; **Claude Code chip 1.6x** (official claude.svg 56 px + Inter 600 44 px) pops up out of its top edge, contact ~2.97 |
| 2.97–3.6 | glyph prompt line 1 types (P.typeIn), caret rides the typing |
| 3.75 | **Codex chip 1.6x** (official codex.png 56 px) falls 40 px stretching and squash-lands, nudges the Claude chip; line 2 types 3.70–4.1, caret blinks on to the cut |
| 3.80–3.98 | beat-A words exit (6 f) |
| 3.94–4.44 | terminal + chips glide on an arc to the top-right corner at **0.6x, fully opaque**, tucked behind the speaker card (DOM order) — chips still read |
| 4.32–4.92 | **calendar 820x360** (x100–920, y800–1160): box (closes on "complete"), header + pencil hatch, binder rings, 6 columns 1 f apart, 2 rows; lands 0.94→1.02→1 |
| 4.51 / 5.03 | band: "complete" (110, row 1 left, base 1310) / "tasks" (140, row 2 right, base 1452) — both exit cleanly 5.30 (6 f, lag 2 f) |
| 4.92–5.29 | ten task scribbles in the days on "tasks" |
| 5.43–5.81 | band: "used to" (104, row 1 right) / "take" (140, row 2 left) — exit 5.98 |
| 6.06–6.36 | RED zig-zag (17 px) through all 21 days, contact mid-sweep on "weeks" |
| 6.21 | **weeks** 150 ink hero, band row 1 left (base 1290); red strike 6.40–6.60 |
| 6.36–6.58 | calendar swells 3 f, twists and collapses into the clock centre |
| 6.50–6.70 | **alarm clock** centre (510, 980), rim R 172 + bells/legs → ~y 760–1185 (~425 px tall): pops 0.35→1.08→1 with a twist; ticks, hands |
| 6.63 / 6.83 | "couple of" (100, band row 1 right, base 1290) |
| 6.64–7.20 | minute hand (red) two full turns, hour hand (ink) 10 → 12 o'clock; 4 red speed ticks chase it, each wiped 0.16 s later |
| 7.03 | **hours** RED hero 204 (row 2 left, base 1464, peak 1.08) + 1 % punch; bells rattle ±4°, red ring marks; boil/caret/push keep it alive to the cut |

End frame: card + opaque terminal (top), clock (middle), "~~weeks~~ couple of / **hours**" (band). Nothing semi-transparent.

## Measured bounds (render.mov vs a background-only render, every frame, diff > 24)
union x 63–960, y 300–1479 — 0 of 217 frames outside x 60–960 / y 285–1480 (marker strokes, loop, rotated card corners, chips, overshoots, push + punch included).

## Principles checklist
- **Contact frames on words**: kinetic words on their words.html times (runtime leads 0.13–0.2 s); calendar box closes on "complete", scribbles on "tasks", zig-zag mid-sweep on "weeks", clock pops on "couple", hours + punch at 7.03 (0.14 s ahead of the spoken 7.17 so it settles before the cut).
- **Anticipation**: hero words sink first; A-words dip before gliding; calendar swells before collapsing; Codex chip stretches while falling.
- **Overshoot + settle**: words, calendar (1.02→1), clock (1.08→1, −3°→0), chips, terminal.
- **Parts lag the whole**: capabilities 2 f behind agentic; sheen 3 f behind the terminal; band rows exit 2 f apart; calendar columns 1 f, rows 2 f, scribbles 1 f; bells/legs/hands after the rim.
- **Arcs**: terminal travels to the corner on an arc; the collapse twists as it pulls in.
- **Squash/stretch on shapes only**: chips only, never type.
- **One focal point**: band words are replaced, not stacked; the terminal sits in the corner behind the card while the calendar/clock is the hero.
- **Secondary action / no dead hold ≥ 1 s**: marker boil on fours, caret typing/blinking, grid drift, camera push, card float; slots.py: "no dead holds".
- **One exaggerated hero beat**: "hours" — peak 1.08, 1 % punch, bells rattle.
- **Exits faster than entrances**: word exits 6 f, loop wipe 0.12 s, collapse 0.16 s, speed-tick wipes 0.1 s.
- **One light direction / contact shadows**: runtime shadows down; marker strokes flat on the paper.
- **Not a static slide**: something draws, types, spins or boils on every frame.

## Richness (hero + secondaries)
- **Hero**: big hand-drawn 3x7 calendar → one red zig-zag through 21 days ("weeks") → collapses into a big hand-drawn alarm clock; minute hand spins two turns while the hour hand moves exactly two hours ("couple of hours"); bells rattle on "hours".
- Working terminal: official Claude Code chip pops out of the card edge on "Claude Code", glyph prompt types with a riding caret, Codex chip squash-lands on "Codex" and nudges its neighbour; then it parks behind the speaker card.
- Ink marker loop around "agentic"; the words physically make room for the terminal.
- Task scribbles fill the days on "tasks"; red strike through "weeks"; speed ticks chase the minute hand.

## Deviations
- Words omitted (connectives only, never paraphrased): "You are", "and using tools like" (chips carry the names), "to", "that", "in a", the full stop.
- "agentic" authored at 180 (brief ~200) so the loop clears the word inside x ≥ 60.
- "hours" authored at 204 (≥ 170 hero) so its ascender clears row 1 ("weeks / couple of") in the 255 px band.
- "hours" peaks at 7.03 (spoken 7.17) to be settled before the hard cut at 7.233.
- The weeks → hours red arrow from v1 was dropped (it would cross the bigger clock / band).
- Band rows alternate sides (complete L / tasks R, used to R / take L, weeks L + couple of R / hours L) — staggered collage, each phrase replaced cleanly.
