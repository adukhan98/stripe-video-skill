# t2_ceos — v7 MINT style test, TALK mode (fullscreen)

## Key poses (planned before authoring; frames @30)

Face map from the footage (measured on gridded frames, qa/grid4.jpg): hair top y ≈ 290, head left edge x ≈ 235–260,
beard bottom y ≈ 1095–1148 (lowest around 3.5 s), right hand x 650–1000 from y ≈ 1350, left hand gestures x 0–560 from
y ≈ 1510 (0.5 s) / x 0–300 from y ≈ 1420 (3.3–3.8 s). The space beside his head is ≤ 200 px wide, so every phrase lives
on his chest, y ≈ 1140–1470 — a 330 px band. Phrases are built as a "feed": when a new hero needs the room, the oldest
row blurs up and the remaining row glides up into its place.

| frame | s | on screen | lands on |
|---|---|---|---|
| f4 | 0.13 | row 1 "I talk to" rising (charcoal, 100) | talk |
| f20 | 0.67 | row 1 complete "I talk to a lot of" (a lot of at 0.9 em) | of |
| f25 | 0.83 | "CEOs," hero charcoal 210 lands under row 1 | CEOs |
| f32–44 | 1.08–1.46 | row 1 blurs up; CEOs, glides up 86 px into its place | (making room) |
| f44 | 1.45 | "founders" hero MINT 180, right-aligned under CEOs | founders |
| f58–63 | 1.92–2.12 | both blur up and are gone | people |
| f63–92 | 2.1–3.07 | him alone (breath; push continues) | who are actually running their |
| f97 | 3.23 | "day" pops (150) | day |
| f111 | 3.69 | "lives" pops beside it | lives |
| f125 | 4.17 | "businesses" hero MINT lands under them, 1 % punch | businesses |
| f129 | 4.30 | charcoal disc + white buildings glyph pops on his left shoulder, mint ring ripples | (businesses) |
| f128–138 | 4.26–4.60 | day·lives blur up; businesses glides up 123 px | (making room) |
| f137 | 4.58 | "on" rises into row 3 | on |
| f143 | 4.75 | "AI." pops; disc pulses once | AI |
| f155 | 5.17 | hold alive to the cut (push, punch settle, disc float) | — |

## As built (scene seconds) — `hf/index.html`

- 0.00–5.20 him full-screen (`.spk.full`, data-face 0.40, video push 1.0→1.02 linear); `#cam` push 1.0→1.004 on the words.
- 0.05/0.13/0.33 "I talk to" (sup 100) + 0.47/0.59/0.67 "a lot of" (0.9 em = 90) — one row, x 100, baseline 1215.
- 0.83 "CEOs," hero charcoal 210, x 170, baseline 1375 (anticipation 3 f, overshoot 1.06, back.out settle).
- 1.08 row 1 blurs up (6 f, dy −100); 1.16–1.46 CEOs, glides up 86 px (power3.inOut) into the freed row.
- 1.45 "founders" hero MINT 180 (fit 800), right edge 850, baseline 1445, rise 36.
- 1.92 founders exits, CEOs, 2 f later (bottom-up, 6 f blur-up) — gone by 2.13 ("people" 2.01).
- 2.13–3.07 him alone (breath between sentences; push continues, he gestures — slots.py: no dead holds).
- 3.23 "day", 3.69 "lives" — pops, charcoal 150, x 100, baseline 1278.
- 4.17 "businesses" hero MINT 190 (fit 790 → ≈172 on screen), right edge 845, baseline 1415, peak 1.07; P.punch 1 % (0.36 s).
- 4.30 icon disc (168 px charcoal, white Phosphor buildings glyph 46 %, var(--disc-shadow)) at (166, 1040) on his left shoulder:
  anticipation dip 0.3→0.22 (2 f) → 1.12 overshoot (5 f) → settle 1 (9 f, back.out); glyph rises from its base 2 f after the
  disc (scaleY 0.1→1.15→1); mint 6 px ring ripples out (1.0→1.18, fades 0.45 s); float −4 px yoyo; P.pulse 1.06 on "AI." 4.75.
- 4.26 "day lives" blur up (dy −100); 4.30–4.60 "businesses" glides up 123 px into row 1.
- 4.58 "on" rises (x 100, 124, baseline 1420); 4.75 "AI." pops. Holds alive to the cut (push, punch settling, disc float).
- No marker layer (marker.js/css not loaded, no Caveat), no red, no paper strip, no pills.

## Principles checklist (Lasseter)

- Contact frames on words: every word uses its words.txt time (runtime starts entrances 0.13–0.2 s early); disc lands 0.13 s
  after "businesses" so the word gets its own contact; "on" lands 0.07 s late (4.58 vs 4.51) to clear the glide — imperceptible.
- Anticipation before the hero moves: hero words sink 3 f before rising (runtime); the disc shrinks 2 f before it pops.
- Overshoot + settle: heroes 1.06–1.07 → back.out; disc 1.12 → 1; glyph 1.15 → 1.
- Parts lag the whole: glyph 2 f after the disc, ring on contact; exits bottom-up 2 f apart; feed glide starts 2–4 f after the exit.
- Long moves on arcs: the only long moves are the two vertical feed glides (single-axis, eased in/out) — no travel that needs an arc.
- Squash/stretch on shapes only: the buildings glyph stretches (scaleY 1.15) as it rises; no type is squashed.
- One focal point: one new element at a time (CEOs → founders → day → lives → businesses → disc → on AI.); older rows leave
  instead of dimming (words are never receded/ghosted).
- Secondary action / no dead hold ≥ 1 s: footage push, his gestures, punch settle, disc float + pulse; 2.13–3.07 is his
  face alone (0.94 s) — slots.py motion: "no dead holds".
- One exaggerated hero beat: "businesses" — 1.07 peak + 1 % camera punch + the disc arriving with a ring.
- Exits faster than entrances: exits 6 f, entrances 10–15 f.
- One light direction / contact shadows: disc shadow and the mint words' soft shadow both fall straight down (+6 px).
- Nothing reads as a static slide: every 0.3–0.5 s something lands, leaves or glides; final 0.4 s still has float/punch settle.

## Richness (fullscreen beat: expressive type + one object)

- Hero object: the buildings icon disc on "businesses" (pop with anticipation, glyph "buildings rise" from the baseline, mint ring ripple).
- Secondary 1: the caption FEED — oldest row blurs up and the survivor glides into its place (1.16 CEOs, 4.30 businesses).
- Secondary 2: disc pulses on "AI." (the businesses run on it) and floats.
- Secondary 3: 1 % punch on "businesses".

## Readability (measured / looked at)

- Zone measured over all 156 frames (render diff vs a words-free reference render, qa/bounds.py): threshold 24 → x 67–879,
  y 943–1462; threshold 10 → x 64–885, y 940–1484 (the 4 px past 1480 is a single frame, f38, of founders' blurred
  entrance drop-shadow at ≤ 9 % opacity). IG corner (x > 900, y > 1200): 0 px at threshold 10 (qa/igc.py).
- Sizes on screen: heroes 197 (CEOs,), 169 (founders), ≈172 (businesses, fitted from 190); supporting 94/85/141/117; nothing < 64.
- Face: words start at y ≥ 1145 (beard bottom 1095–1148); disc right edge 250 settled / 260 at overshoot vs his cheek at
  x ≈ 270–290 — close but never over the face. Hands: founders' last letters and "businesses" cross the white earphone cable /
  his right fist at x > 650 (still readable, see qa/full/trio.jpg).
- No ghosted text: exits take 6 f and leave nothing behind; no dimmed words.
- **Key question — charcoal-on-glow over the light-grey sweatshirt and warm room:** charcoal words (#232323) with the
  specified light glow read very well on the sweatshirt (dark on light grey, the glow just lifts the edges off the knit
  texture). MINT is the weak point: with the specified light glow, mint (#7CC49E) on his light heather-grey sweatshirt is
  low-contrast — the cream halo is lighter than the mint and the letters partly dissolve into it (qa/vt/compare.jpg, row 1).
  I tested four treatments (qa/vt/compare.jpg rows 1–4: spec glow / soft charcoal drop shadow / mixed / dark halo) and
  shipped row 2: mint hero words drop the light glow and take a soft charcoal drop shadow (0 6px 18px @ .45 + 0 1px 3px @ .35).
  That gives them a clean edge and depth; they read clearly at phone size but remain the softest-contrast element on screen
  (honest verdict: fine at 170+ px and Black weight, would NOT be readable at supporting sizes — keep mint for heroes only
  on this sweatshirt). The warm room never sits behind words in this scene (only the disc touches the hallway wall).

## Deviations

- Mint hero words use a soft charcoal drop shadow instead of the light glow (readability, above). Charcoal words use the spec glow.
- "I talk to / a lot of / CEOs, / founders" can't stack four rows in the 330 px chest band at the brief sizes, so the
  phrase builds as a feed: row 1 leaves as founders arrives and CEOs, glides up. Same for "day lives / businesses / on AI.".
  Final frame therefore reads "businesses / on AI." (+ disc), not the whole sentence.
- Sizes: CEOs, 210 / founders 180 / day·lives 150 as briefed; businesses authored 190 but data-fit 790 shrinks it (≈170–175 on
  screen) to stay ≤ 845 wide with overshoot; "on AI." 124 (brief ~120).
- Disc sits on his left shoulder (above-left of the phrase), not on the same row as "businesses": no row has 170 px spare
  beside a 790 px word. It pops 0.13 s after "businesses" and stays to the cut.
- Upper-left beside his head was not used: the gap between the frame edge and his head is ≤ 200 px.
- Sound: none tagged (brief) — beats.json lists contact frames only, all silent.
- Scratch: qa/ (bg reference render deleted after measuring; qa/bgref/index.html regenerates it). hf/.hyperframes/ is the CLI's own state.
