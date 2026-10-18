# v12_faster — explainer (bespoke: demand vs supply two-bar chart)

192 frames @30 (6.400 s). Spoken: "…businesses. Companies and organizations are going to want this way faster
than there are FDEs and consultants that are left who can actually do this work."

## Layout (px, 1080x1920)

- Small speaker card top-left: x 70, y 300, 440 x 340 (data-face-at 0.53 so hair → chin is inside).
- Beat A words below the card: "Companies &" (96, x 76, base 750) · "organizations" (96, right 960, base 855) ·
  "want this" (110, x 76, base 960; "want" hero ocean).
- Hero object: one soft white chart card x 90–930, y 1000–1420 (lower zone, from 0.62 s to the cut). Two tracks
  (left = demand, accent bar; right = supply, ink bar), floor, one wireframe placeholder, a black pill
  "FDEs & consultants" under the right bar, a dotted bracket from the demand level down to the supply top, and a
  soft accent tint over the empty part of the supply track = the GAP. Unlabelled: no axes, no numbers, no %.
- Beat B words: "way" (150 ink, x 560 base 520 — right of the card) · "faster" (220 ocean, right 942, base 880).
- Beat C words: "who can" (100, x 560, base 520) · "actually do" (100, x 76, base 790) · "this work" (170 hero ink,
  right 935, base 960).

## Key poses (frame = scene frame @30)

| f | t | on screen | lands on |
|---|---|---|---|
| 0 | 0.00 | paper, small card settling, empty zone below | — |
| 8 | 0.27 | "Companies" | Companies |
| 15 | 0.49 | "&" | and |
| 19–27 | 0.62–0.90 | chart card rises into the lower zone; bar stubs pop (3 f apart) | (between words) |
| 31 | 1.03 | "organizations" | organizations |
| 56 | 1.87 | "want" (ocean hero) lands; demand bar nudges up | want |
| 64 | 2.13 | "this" | this |
| 66–72 | 2.20–2.40 | Beat A blurs up bottom-up; speaker recedes; demand bar crouches (anticipation) | — |
| 76 | 2.53 | "way" lands top-right; demand bar launched to ~75 % of its track (stretched thin) | way |
| 90 | 2.99 | "faster" 220 ocean; bar overshoots past the top of its track to the card edge, squashes, ring flash, 4 f shake + punch (THE hero beat) | faster |
| 98 | 3.25 | supply bar's first tiny creep step | than |
| 112 | 3.73 | black pill "FDEs" pops under the supply bar; 2nd creep step | FDEs |
| 119–134 | 3.95–4.45 | dotted bracket draws demand level → supply top | — |
| 128 | 4.27 | 3rd (last) creep step; gap tint fades in | and |
| 137 | 4.57 | pill extends to "FDEs & consultants"; gap pulses | consultants |
| 147–152 | 4.90–5.08 | "faster", "way" blur up; speaker restores; chart recedes a touch | — |
| 159 / 163 | 5.29 / 5.43 | "who" "can" (top-right, where "way" was) | who / can |
| 171 / 176 | 5.71 / 5.85 | "actually" "do" | actually / do |
| 181 / 187 | 6.03 / 6.23 | "this" "work" 170 ink heroes | this / work |
| 191 | 6.37 | hold alive into the cut (gap pulsing, demand bar straining, dots marching) | — |

(As built, "organizations" is right-aligned at 946 and "faster" at 926, pulled in from 960/942 because their overshoot crossed x 960.)

## As-built timeline (scene seconds)

- 0.00 small card on screen, 3D settle by 0.32, sheen sweep, video push, float 4 px; grid drift + camera push 1.006 run throughout.
- 0.14 / 0.36 "Companies" / "&" rise in (contact 0.27 / 0.49).
- 0.62 the chart card comes in (cardIn, 16 f, tilts into travel, overshoot then settle). 0.86 / 0.96 the bar stubs pop (3 f apart), 1.06 the wire placeholder slides in.
- 0.87 "organizations" (accent rise, contact 1.03).
- 1.67 "want" ocean hero (anticipation sink, overshoot 1.06, settle). 1.72 the demand bar nudges 34→84. 2.00 "this".
- 2.20 / 2.27 / 2.33 Beat A exits bottom-up (6 f blur-up, 2 f lag). 2.30 the speaker recedes (0.72 opacity, 2 px blur, 97 %).
- 2.30 the demand bar crouches (3 f, widens 7 %). 2.40 it launches on expo.out to 228 px, stretched to 90 % width. 2.33 "way" hero (contact 2.53).
- 2.79 "faster" 220 ocean hero (contact 2.99). 2.82 second kick: the bar overshoots to 390 px, past the top of its 260 px track and above the card edge. 2.99 it drops back to the track top with a squash (108 % width, back.out settle), an accent ring flash at 3.00, a 4 f shake of 4 px at 3.00 and a 0.6 % punch at 2.99.
- 3.25–6.38 the demand bar strains 260↔268 px (sine yoyo). This is the secondary action.
- 3.25 / 3.73 / 4.27 the supply bar creeps 34→46→58→70 px, a small squash on each step. 5.10 a last drift to 74 px.
- 3.57 the black pill "FDEs" pops under the supply bar (contact 3.73, squash on landing). 4.44 it extends to "FDEs & consultants" (contact 4.57).
- 3.95–4.45 the dotted bracket draws (demand level → across → down to the supply top). It marches from 4.45 to the cut.
- 4.27 the gap tint fades in, flashes at 4.50, then pulses 4.64→cut.
- 4.90 / 4.97 "faster" then "way" exit with a blur-up. 5.00 the speaker restores. 5.05 the chart recedes slightly (0.86 opacity, 1 px blur, 98.5 %). The chart group floats 3 px.
- 5.16 / 5.30 "who" / "can". 5.58 / 5.72 "actually" / "do". 5.83 / 6.03 "this" / "work" 170 ink heroes (contacts 6.03 / 6.23). The scene stays alive into the cut at f191.

## Principles checklist

- **Contact frames on words:** yes. Every word's entrance starts 0.13–0.2 s before its words.txt time. The bar's launch lands on "way", the overshoot on "faster", the pill on "FDEs" and its extension on "consultants".
- **Anticipation before the hero moves:** yes. The demand bar crouches 3 f before launching, the hero words sink before rising (runtime), the pill pops from 40 % and the chart card tilts into travel.
- **Overshoot + settle:** yes. The bar overshoots to 390 px against a 260 px track and settles with a squash and back.out. Hero words reach 106 %. The card, stubs and pill all use back.out settles.
- **Parts lag the whole (2–4 f):** yes. The card lands, then the stubs pop 3 f apart, then the wire placeholder. Beat A exits with a 2 f lag, bottom-up. "faster" exits 2 f before "way".
- **Long moves on arcs:** the only long travel is the chart card's entrance, and cardIn rotates it into travel. The bar is a vertical growth, not a travel, so no arc is needed.
- **Squash/stretch on shapes only:** yes. The demand bar stretches thin on launch and squashes wide on the settle. The supply bar squashes on each creep step and the pill on landing. No type or logos are squashed.
- **One focal point:** yes. The speaker recedes during Beat B while the chart is the focal point and restores in Beat C, when the chart recedes slightly so the words lead.
- **Secondary action, no dead hold ≥ 1 s:** yes. Grid drift, camera push, card float, chart float, the demand bar straining, marching bracket dots and the gap pulse. `slots.py --motion` reports no dead holds.
- **One exaggerated hero beat:** yes. "faster" at 2.99: the overshoot above the card, the ring flash, the 4 f shake and the punch. Nothing else is exaggerated.
- **Exits faster than entrances:** yes. Exits take 6 f; entrances take 10–16 f.
- **One light direction / contact shadows:** yes. All shadows fall down (cards, bars, pill), the tracks have inset top shadows and the bars carry their own drop shadow.
- **Nothing reads as a static slide:** yes. Something moves on every frame.

## Deviations

- "businesses." (0.00) is not shown: it is the tail of the previous sentence and the brief starts the beat at "Companies". "are going to", "than there are", "that are left" are also left out, matching the brief's phrase list. Every word shown is a spoken word. "&" stands for the spoken "and".
- "want this" is in ink with "want" in ocean (the brief gave no colour). "way" is 150 ink and "faster" 220 ocean, so the 220 accent lands on the hero word and the pair fits the width.
- The label is a black `.pill.sm` (Inter 600, 34 px) instead of a white chip, because a white chip disappears on the white chart card.
- The small card is 440x340 with `data-face-at 0.56` (preset 0.5) so the hair stays fully inside the card.

## Revision 2 (coordinator: make the chart the hero) — supersedes the layout and timings above where they differ

- **Chart:** card x 90–930, y 725–1435 (710 tall). Tracks are 510 tall and bars 200 wide (demand at abs x 180–380, supply at 610–810). The card is in at full size by 0.68 (cardIn at 0.14) and the stubs pop at 0.50 / 0.60.
- **Demand bar** (heights in px): 40 → 110 on "want" (1.72) → crouch to 92 (2.30) → launches to 330 on "way" (2.40, expo.out, stretched to 88 % width) → second kick to 620 (2.82–2.99), about 60 px past the card top → drops to 485, about 95 % of the track, with a squash (2.99–3.15) → ring flash, 4 f shake and punch at 3.10–3.12 → strains 485↔495 until the cut.
- **Supply bar** creeps 40 → 47 → 54 → 61 px (3.25 / 3.73 / 4.27), about 12 %, then drifts to 64 at 5.1. The bracket path is now M 392 800 → 860 800 → 860 1224, and the gap tint covers the right track from y 800 to 1224.
- **Phrase 1 (band y 300–705):** small card 420x310 at 70,300 (face-at 0.56). "Companies" (84) right of the card, base 395. "want this" (100, "want" ocean hero) right of the card, base 530. "& organizations" (96) just below the card, right edge 946, base 705. They exit at 2.10–2.23, bottom-up.
- **"way faster":** "way" (150) right of the card, base 440. "faster" (200 ocean) lands over the upper right of the chart (right edge 930, base 930) while the bar is still climbing. At 3.42 it glides up and shrinks to 78 % beside "way", clearing the chart for the pill, bracket and gap. Both clear at 4.88 / 4.92.
- **Phrase 3 (band y 300–700):** at 4.96 the speaker card shrinks out in place. "who can" (100, x 76, base 395), "actually do" (100, right edge 940, base 515), "this work" (170, x 76, base 680). "work" is a pop with contact 6.20, settled by about 6.30 and held to the cut.
- **New deviation:** the speaker card leaves the frame for the last 1.4 s. The 170 px "this work" cannot share the y 300–700 band with a 420 px card.

## Creative pass (rev 3) — new on top of rev 2 (runtime reinstalled, --type-scale 0.94 kept)

- **Demand rocket:** speed streaks rush down past the bar in two bursts (2.40, 2.82). The riser peaks at 2.99 with 7 accent/white sparks bursting off the bar tip on arcs. IMPACT at 3.10 (moved from 2.99–3.15 to land exactly on the SFX): drop to ~95 %, squash, ring flash, camera shake, punch, and a 4 f jolt of the chart card.
- **"faster" rides the bar tip** from 2.80 to 2.93, with a blurred two-ghost trail as motion blur. It detaches above the bar, gets nudged by the impact at 3.10, then glides up beside "way" at 3.42.
- **Supply bar tries (twice):** anticipation dip, strains up trembling, sinks back (strains at 3.32 and 4.06, sinks at ~3.94 and ~4.68). Two soft accent sweat drops fly off at 4.40 / 4.46. It creeps to ~12 % from 5.00.
- **Gap:** the bracket now draws 4.62–5.04 (after the second sink), then marches and pulses. The gap tint fades in at 4.72 with a marching diagonal accent hatch (linear, seamless 30 px tile).
- **"who can actually do this work":** five soft person icons pop on the floor (5.22, 2 f stagger). Two hop onto the supply bar and turn ocean (land 5.80 / 6.00). Three jump short and bonk back down grey (6.09 / 6.13 / 6.17).
- **Checks:** bounds x 67–957, y 294–1474 (0 frames out); 192 frames; slots.py: no dead holds, all checks passed.
