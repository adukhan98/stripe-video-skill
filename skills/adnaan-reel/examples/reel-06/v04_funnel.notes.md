# v04_funnel — THE FUNNEL IS DRAWN (bespoke hero scene)

Full-screen opaque scene, 1080x1920 @30, **278 frames** (data-duration 9.2500 on root + video). Blank starter on the
shared runtime (paper.js / paper.css / marker.js untouched). `<body data-face="0.42">`.

## Key poses (planned before authoring)

| frame | t | on screen | word |
|---|---|---|---|
| f0 | 0.00 | post card (post_funnel.png, 873 wide, taped, X chip) top of zone; paper | And |
| f14–23 | 0.47–0.77 | red highlighter swipes behind "sharp funnel" | describes |
| f7 / f19 | 0.24 / 0.64 | "he describes" lands lower band | he / describes |
| f26–37 | 0.85–1.25 | funnel rim draws (hand drawing it), walls follow | it as a |
| f36–41 | 1.20–1.38 | post card dips (anticipation) then whips up/out, blur | a |
| f44 | 1.46 | "funnel." RED hero lands top-left, 1 % camera punch = HERO BEAT | funnel |
| f57–73 | 1.90–2.43 | "biggest" / "chunk" land lower band; 3 dividers draw in quick succession | biggest chunk |
| f58–87 | 1.92–2.90 | 13 stick people pop in at top-right, tumble on arcs INTO the rim, squash + hop, pile in tier 0 | chunk is about |
| f90–104 | 3.02–3.47 | tier 0 hatches pencil grey under the pile | 75% |
| f96 | 3.20 | "75%" RED stamps lower-right; the pile hops (centre outward) | 75% |
| f117 | 3.90 | "people," lands lower-left | people |
| f109–127 | 3.62–4.25 | "funnel." clears; small speaker card arcs in top-right | which makes |
| f149–174 | 4.96–5.80 | ODOMETER 6,000,000,000 rolls in under 75 %, digits lock left→right ('6' locks on "6") | about 6 billion |
| f163 / f170 | 5.42 / 5.66 | red Caveat "6B" writes beside tier 0, short arrow into tier 0 | billion |
| f187 / f206 | 6.22 / 6.86 | "the entire" / "world" top-left; top-row people wave | entire world |
| f219–233 | 7.30–7.77 | empty red CHAT BUBBLE draws right of tier 0 (lower band stays fully opaque) | never |
| f224 | 7.46 | "never" RED pops top-left | never |
| f237–262 | 7.90–8.75 | typing dots appear and bounce (nobody's typing anything) | interacted with AI |
| f265–273 | 8.82–9.10 | black marker ✗ slashes across the bubble, bubble shakes once | at all |
| f269–277 | 8.97–9.25 | "at all." lands; boil, float, bob hold alive to the cut | at all |

## Layout (frame px)

- Post card: x 80–953, y 345–576, rot −1°, strip at 0.87 scale (833 px wide), tapes top-left + bottom-right, X chip
  (assets/x.png, copied from v03's supplied assets) on the top-right corner. Exits 0.98–1.28.
- Funnel: SHARED geometry `M.funnel({x:150,y:820,w:560,h:330,neck:.16,tiers:4,split:[0,.38,.66,.86,1],spout:56,color:"ink"})`.
- Top band (y 285–770): "funnel." 220 red (x 90, base 495) 1.26–3.70 → small speaker card 420×360 at x 510, y 300
  (data-face-at 0.62: hair to chin in) from 4.25 → top-left column (x 76–496, data-fit 410): "the entire / world"
  (base 425/565), then "never" 150 red (440), "interacted" 92 (545), "with AI" 92 (645), "at all." 92 (745).
- Right column (x 740–960): stick people fall 1.92–2.83; "6B" Caveat 104 red at (784, 776) + arrow into tier 0;
  chat bubble x 742–938, y 878–1044 (tail), ✗ 176 px centred (840, 952).
- Lower band (y 1190–1480): "he describes / it as a" (base 1330 / 1440) → "biggest / chunk" 110 (1340 / 1450) →
  "75%" 230 red right-aligned 935 (base 1350), "people," 100 (x 76, base 1322), odometer 110 900 ink (x 76, base 1446).

## As built (scene seconds)

- 0.00 post card on screen (float 3 px); 0.47–0.77 red highlighter behind "sharp funnel" (strip rect 273,139,259,54).
- 0.24 / 0.64 "he describes", 0.90–1.24 "it as a"; both exit 1.30 (6 f, 2 f lag).
- 0.85 FUN.draw (dur 0.8): rim 0.85–1.20, left wall 1.27–1.51, right wall 1.58–1.83, spout lip 1.90–1.97.
- 0.98 card anticipation dip (3 f), 1.08–1.28 card whips up 34 px + scale .94 + blur 10 + fade (exit 6 f).
- 1.46 "funnel." hero (anticipation sink, 106 % overshoot, settle) + P.punch 1 % = THE hero beat. Exits 3.60.
- 1.95 / 2.07 / 2.19 dividers 0–2 (0.24 s each).
- 1.90 "biggest", 2.18 "chunk" (pop); exit 2.96.
- 1.92 + i·0.045 (i = 0…12): stick person i pops in (5 f back.out) at the top-right, falls on an arc (y power1.in =
  gravity, x power2.in = sucked in late), tumbling 1–1.5 turns (power2.out) to its tilt; lands 2.36–2.83: arms flip
  from \o/ to down, squash 1.2/0.76 on the feet (2 f), back.out settle, 9 px hop.
- 3.02–3.47 tier 0 pencil hatch (opacity .45) under the pile.
- 3.20 "75%" hero (peak 108 %); 3.21 + |dx|/65 f the pile jolts 8 px (centre outward).
- 3.60+ each figure breathes 1.8 px on its own period (0.55–0.82 s) to the cut.
- 3.90 "people,". 3.83–4.45 small speaker card arcs in (runtime data-at 4.25), sheen, float.
- 4.96 odometer enters (accent rise 10 px); reels roll and lock: '6' at 5.30, zeros 5.355 … 5.795 left → right.
- 5.42 red Caveat "6B" written; 5.66 arrow (shaft then head) into tier 0.
- 6.22 / 6.56 "the entire", 6.86 "world"; 6.88 the top row of the pile waves twice (\o/ ↔ down, 2 f stagger). Exit 7.04 (clear before "never").
- 7.30 (coordinator pass: NO recede — the lower band stays fully opaque to the cut; the bubble is staged by its own
  draw-on, typing dots, ✗ and shake) 7.30–7.78 red chat bubble draws, 7.82 tail,
  7.92–8.06 three dots; 8.12–8.75 typing-indicator wave (2 cycles) … nothing arrives.
- 7.46 "never" red (pop), 8.00 "interacted", 8.30 / 8.60 "with AI", 8.97 / 9.12 "at all.".
- 8.82–9.21 black marker ✗ (two slashes); 9.00 the bubble shakes once (rot 4° → −3° → 0, 9 f).
- Continuous: grid drift, camera push 1.006, boil on fours on every stroke, card float, figure breathing.

## Pile table (for v05 / v07 / v10 — rebuild at t = 0)

Feet (x, y, tilt°), figure scale 0.86 (head r 5.7 at (0,−23.2); body (0,−16.8)→(0,0); legs ±6.9,12; arms down
(±9.5,−2.6)→(0,−12)); wrap origin = hips = feet − 12 px; ink, width 5, amp 0.7, seed 7000 + i·61 + k·7:
row 1 (305,966,−8) (557,966,−6) (431,975,−3) (368,972,5) (494,972,9);
row 2 (274,930,12) (526,934,8) (400,937,4) (337,935,−10) (463,937,−14);
row 3 (368,900,−12) (494,900,15) (431,897,6).

## Principles checklist

- **Contact frames on words**: every kinetic word via runtime data-t; marker strokes start ~0.15 s before their word
  (highlight 0.47 → "describes" 0.64; ✗ 8.82 → "at" 8.97; "6B" 5.42 → "billion" 5.46; bubble 7.30 → "never" 7.46).
- **Anticipation**: post card dips before it whips out; "funnel."/"75%" hero sink 3 f before rising; card enters from behind/below.
- **Overshoot + settle**: heroes 106–108 % → back.out; figures squash + hop on landing; bubble shake settles back.out.
- **Parts lag the whole**: line exits lag 2 f; figures 1.35 f apart; pile jolt centre→out 1 f per 65 px; dots 0.1 s wave;
  arrow head after shaft; ✗ second slash after first.
- **Arcs**: figures fall on true arcs (x and y eased differently); speaker card arcs in (runtime).
- **Squash/stretch on shapes only**: stick figures (feet squash); no squash on type, logo or card.
- **One focal point**: card leaves before "funnel." lands; top-left words clear before the card enters; the bubble is staged by its own motion (draw-on, typing dots, ✗, shake) while the lower band stays fully readable.
- **Secondary action, no dead hold ≥ 1 s**: boil, breathing pile, wave on "world", typing dots, float, grid, push.
  Longest gap between new events ≈ 0.5 s (5.9–6.4, covered by boil/breathing/float).
- **One exaggerated hero beat**: 1 % camera punch on "funnel." only (75% stamp gets the pile jolt, not a second punch).
- **Exits faster than entrances**: card 6 f, type 6 f vs 10–16 f entrances.
- **One light direction / contact shadows**: card + speaker shadows down; marker world flat (felt-tip, no shadows).
- **Not a static slide**: every frame has something drawing, falling, rolling, breathing or boiling.

## Richness (house level)

- Hero object: THE FUNNEL drawn by hand (rim → walls → spout → 3 dividers) on "funnel", hatched on "75%".
- Characters: 13 stick people with personality — thrown in flailing \o/, tumble, squash-land, pile up; jolt on the stamp,
  breathe, the top row waves on "world".
- Number that rolls to its real value: 6,000,000,000 odometer, '6' locks on "6", zeros lock left→right through "billion".
- Hand-drawn object acting out the sentence: an empty red chat bubble whose typing dots bounce with nothing to say,
  slashed by a black ✗ on "at all" + shake.
- Marker annotations: highlighter on the real post, red "6B" note + arrow.

## QA

- `slots.py check --motion --at 1.46,2.6,3.2,5.8,7.46,9.0`: checks passed (size, fps, duration, alpha); motion: no dead holds.
- ffprobe: 278 frames.
- Bounds (every frame, diff vs background-only render `qa/bg.mov`, threshold 24): **x 66–958, y 286–1476, 0 frames
  outside x 60–960 / y 285–1480** (incl. card shadow, speaker card entrance, marker strokes, notes, descenders, punch + push).
- Fixed along the way: my own svgs inherited fill (blobs) → `fill:none`; "funnel." overlapped the leaving post card →
  card exit moved to 1.08; odometer commas + "chunk"/"it as a" rises spilled below 1480 → bases/rises lowered; speaker
  card entrance hit x 970 → card x 510; "never" collided with the exiting "world" → exit 7.04; pile rows offset so the
  figures don't stack into columns.

## Deviations

- Card look: v03 is not built yet, so the post card is my reading of its brief (white card, 2 tapes, X chip). x.png
  copied into hf/assets from v03's supplied assets (official file, not drawn).
- "75%" sits right-aligned (x ~500–935) instead of left so the odometer can sit under it inside the zone without
  touching the spout; "people," sits to its left. The odometer is 6,000,000,000 under "75%" as asked.
- Speaker card enters at 4.25 (not during the whole of B): the top-right column is the people's flight path in B,
  and "funnel." must clear first.
- Bubble is red marker (✗ black) so the black ✗ reads across it.
- Words omitted (fillers / covered by objects): "And", "The", "is about", "which makes up to about", "billion" (the
  odometer), "people in", "who have". No paraphrase.

## Coordinator pass (v2)

- Removed the 7.30 recede: "people, 75%" + "6,000,000,000" stay fully opaque to the cut (no half-faded text).
- Re-rendered with the corrected (un-mirrored) speaker.mp4; card crop re-checked at 4.6 / 6.5 / 8.0 / 9.2 s — whole
  head incl. hair, chin and collar in every frame (data-face-at 0.62 unchanged).
- Re-check: slots.py checks passed, no dead holds; ffprobe 278; bounds x 66–958, y 286–1476, 0 frames outside the zone.
