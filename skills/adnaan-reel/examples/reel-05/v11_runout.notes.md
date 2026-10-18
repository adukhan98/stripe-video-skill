# v11_runout — opinion + bespoke drain gauge

Full-screen opaque scene, 1080x1920 @30, **154 frames** (5.133 s; data-duration 5.1167 on root and video).
Opinion starter on the shared runtime (paper.js / paper.css untouched). `<body data-face="0.47">`.

Layout: portrait speaker card left (x 64, y 392, 680x780; whole head plus chest, face at about y 704). A tall soft white
tank card to its right (x 766–942, y 410–1192): status dot, wire bar, inset tank with 6 unlabelled ticks, 7 grey
"ghost" seats, 7 deep person icons, an accent fill with a 6 px accent surface line, and an ink valve under the tank. Kinetic
type: top row "Even with all that," (84, 800). Lower zone: "I think" (84), then the hero "run out" (230, 900, ocean,
baseline 1344, sits on paper just under the card's accent edge), "of people" (112), then "implement **AI**" (110, AI
ocean 900 + hand-drawn underline). No words over the navy chest. Everything except "run out" and "AI" is ink.

## Key poses (written before authoring, then adjusted to the build)

| frame | t | on screen | word |
|---|---|---|---|
| f0 | 0.00 | paper, portrait card about 90 % settled | them |
| f5 | 0.16 | "Even" lands top row | Even |
| f7–23 | 0.24–0.77 | tank card arcs up beside the card (16 f, tilt, overshoot) | with all |
| f16–34 | 0.52–1.12 | people pop in bottom-up (3 f stagger), fill rises under them to the brim | all that |
| f35–41 | 1.16–1.38 | "I think" lands in the lower zone | I think |
| f51–55 | 1.70–1.84 | anticipation: people hop up 10 px (top first), valve slides open | going to |
| f58 | 1.92 | "run" hero lands; bottom person drops out of the card | run |
| f67 | 2.24 | "out" hero lands (peak 110 %) + camera punch (the one hero beat); people cascade out on arcs | out |
| f78–81 | 2.60–2.70 | last person leaves; fill line hits zero; "of people" lands | people |
| f78–100 | 2.60–3.32 | the zero line wobbles flat; status dot rings and dims to muted; valve closes; card squash | who can |
| f112 | 3.72 | top row + "of people" clear (6 f) | actually |
| f120 | 4.00 | "implement" lands lower right | implement |
| f128–140 | 4.28–4.68 | "AI" pops in ocean; underline draws | AI |
| f140–153 | 4.68–5.10 | alive hold: card float + orbit, video push, gauge float, grid drift, camera push | in |

## As built (scene seconds)

- 0.00–0.32 speaker card 3D settle, sheen 0.00–0.75; float 4 px; video push. Recedes 1.80 (92 %, blur 1.5, 98.5 %), restored 3.40.
- 0.16 / 0.38 / 0.56 / 0.84 "Even with all that," (contact frames); recedes 1.78 (40 %, blur 4); exits 3.72.
- 0.24 tank card `P.cardIn` (fromY 110, rot 3). 0.38–1.18 fill rises to the brim. 0.52 + i·3 f people `P.pop` (peak 112 %) and ghosts appear.
- 0.70–1.90 fill surface sways ±1.6°; 1.08 people breathe (−4 px, 2 f apart).
- 1.16 "I" / 1.38 "think"; exits 2.14.
- 1.70 anticipation hop (top first, 1 f apart); 1.78 valve opens (5 f).
- 1.86 + i·2 f people fall: constant gravity (power2.in, g = 5000 px/s²), stretch 0.9/1.12 while falling. Once clear of the card
  they veer right on an arc (+40–68 px, rotate 16–32°) and fade or blur out by y ≈ 1290, right of "out".
- 1.90–2.60 fill drains (power1.in) → 2.60–2.74 lands on zero; wobble 4° → −3° → 1.8° → −0.8° → 0 (2.60–3.32).
- 1.92 "run", 2.24 "out" (heroes). 2.24 `P.punch` 0.8 % (origin 510 882).
- 2.46 "of", 2.70 "people" (pop). 2.86 status-dot ring, 2.90 card squash 2.5 %, 3.00 dot to muted, valve closes.
- 3.86 tank card recedes slightly (90 %, blur 1). 4.00 "implement", 4.28 "AI" (pop), 4.42 underline.

## Principles checklist

- **Contact frames on words**: every word uses the runtime entrances (contact at its words.txt time). Drain starts on "run", the tank hits zero on "people".
- **Anticipation before the hero moves**: hero words sink 3 f first; the people hop up 10 px and the valve slides open before the drain; the cards dip before they rise.
- **Overshoot + settle**: hero words reach 106 % ("out" 110 %) and settle; the card overshoots then settles with back.out; people pop to 112 %; the fill line wobbles past flat and settles.
- **Parts lag the whole (2–4 f)**: people pop 3 f apart and fall 2 f apart. The hop runs top-first, 1 f apart. Ghosts appear with their person. The card leads its people. Sheen lags the card.
- **Long moves on arcs**: every fall bends (y on gravity ease, x drift only after it clears the card, power1.out); the card arcs in with a tilt.
- **Squash/stretch on shapes only**: people icons stretch while falling, and the tank card gets a 2.5 % squash when empty. Type and the speaker card are never squashed.
- **One focal point**: "Even with all that," and "I think" recede or exit and the speaker card softens during the hero. The tank card steps back for "implement AI".
- **Secondary action, no dead hold ≥ 1 s**: grid drift, camera push, card float + orbit, video push, tank float, fill sway, people breathing, the dot ring and the AI underline. `slots.py check --motion`: no dead holds.
- **One exaggerated hero beat**: the camera punch on "out" with its 110 % overshoot.
- **Exits faster than entrances**: word exits 6 f (entrances 11–15 f); valve closes in 6 f; all finish before the last frame.
- **One light direction / contact shadows**: shadows fall down and right (card shadow, icon drop-shadows 2/5 px, inset tank shade from the top).
- **Not a static slide**: something moves on every frame, and the drain is the event of the scene.

## QA

- `slots.py check --motion`: checks passed (size, fps, duration, alpha); motion: no dead holds.
- ffprobe: 154 frames.
- Bounds (diff against a background-only render, all 154 frames, threshold 24): **x 60–959, y 297–1479**. Inside the zone.
- Face: whole head including hair in every frame. The ceiling lamp is outside the crop. No text over the face or the navy chest.

## Deviations

- Card is 680x780 (brief ~720x880): narrower to leave room for the tank beside it inside x ≤ 960. Shorter so "run out" lands on paper under the card edge, not on the navy chest.
- "I think" sits in the lower zone (where "of people" lands later), not near the top row. This keeps the lower 40 % filled before the hero, and it exits at 2.14, just before "of".
- "Even with all that," stays (receded) until 3.72, then exits with "of people". "implement AI" takes the lower zone alone; "run out" stays to the cut.
- Omitted: "them." (end of the previous sentence), "we're going to", "who can actually", "in" (connectives). Nothing was paraphrased.
- Lower-zone words use a shorter rise (14–30 px instead of 56–84) so their descenders never leave y 1480 mid-entrance. The punch is 0.8 % (not 1.2 %) to keep the top row inside y 285.

## Creative pass (v2) — what changed

Runtime is the reinstalled copy (untouched); `--type-scale: 0.94` in brand.css is kept, so the kinetic sizes are 94 % of
the data-size values ("run out" ≈ 216). v1 is backed up in scratchpad `v11_qa/` (index_v1.html, render_v1.mov).

- **Liquid**: the flat fill is now a body plus an SVG sine crest (λ 70, A 8) that travels continuously (linear, mechanical)
  and changes amplitude as the scene plays. It pours in choppy (0.38) and calms. It goes still on the anticipation (1.70), churns
  as the drain opens (1.86), sloshes when it hits bottom (2.60) and settles to a near-flat line at zero (2.72–4.6). The
  accent surface line keeps its width at every amplitude (non-scaling stroke). The tilt slosh on top is kept.
- **People with character**: each icon has two arms that pop up the moment it drops and flail in 3 f beats as it falls
  (left and right arms 1 f apart).
- **"out" drains**: its letters (o, u, t) sag 12 px one by one (3 f apart, from 2.56) and climb back with back.out. They are readable throughout.
- **Empty beat (2.86)**: the valve coughs a dust puff (6 soft muted blobs, 1 f apart). The tank card trembles for 4 f, then squashes. The status dot
  rings, turns grey and blinks twice (3.30, 3.62).
- **implement AI**: the underline is replaced by a tiny drawn wrench (ink). It swings in on an arc (4.16) and taps "AI" twice
  (lift 3 f, then strike, contact 4.48 and 4.70, back.out recoil). Each tap sends 3 accent sparks and nudges "AI" down 5 px.
  The type only moves in position, with no squash. The wrench bobs until the cut.
- "of people" now exits at 3.62 (was 3.72) so it never overlaps "implement".
- Unchanged hero times: drain 1.86, "run" 1.92, "out" punch 2.24, zero 2.60–2.74, empty 2.86.

### Beat times for SFX (scene s)

| t | tag | what |
|---|---|---|
| 0.24 | whoosh | tank card arrives |
| 0.52, 0.62, 0.72, 0.82, 0.92, 1.02, 1.12 | pop | people pop into the tank |
| 1.78 | tick | valve slides open |
| 1.86 | whoosh | drain starts (existing) |
| 1.92 | impact | "run" |
| 2.24 | impact | "out" + camera punch (hero) |
| 2.56, 2.66, 2.76 | tick | "out" letters sag |
| 2.60 | — | liquid sloshes at the bottom (riser tail optional, 1.86→2.60) |
| 2.86 | pop | tank empty: dust puff + tremble + dot ring (existing) |
| 3.00 | tick | valve closes |
| 3.30, 3.62 | ping | grey status dot blinks |
| 4.16 | whoosh | wrench swings in |
| 4.28 | pop | "AI" lands |
| 4.48 | tick | wrench taps "AI" (sparks) |
| 4.70 | ding | second tap (sparks) |

### QA (v2)

- `slots.py check --motion --at 1.86,2.24,2.62,2.86,4.16,4.48,4.70`: checks passed; motion: no dead holds.
- ffprobe: 154 frames.
- Bounds vs a background-only render, all frames: **x 60–959, y 300–1477**. The wrench enters from the upper left, so it stays inside x 960.
