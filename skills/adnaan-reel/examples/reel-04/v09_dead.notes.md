# v09_dead — key poses + as built

Full-screen opaque scene, 1080x1920 @30, 5.233 s authored → 157 frames (coordinator: exactly 157; TASK.md said 158). Paper bg + 60 px grid
(drifts 20 px, linear) + vignette on every frame (first/last frame alpha min 255). Hard cut in, hard cut out.

Spoken (words.txt): "is software really dead and also that software is going to get really hard to protect".
On screen: is · software · really · dead? · software is going to get · really hard to · protect (fillers "and also that" omitted).

## Key poses (slot seconds)

| f | t | on screen | lands on |
|---|---|---|---|
| 0–9 | 0.00–0.30 | "is" (Newsreader 120, baseline 470) rising top-left (25 % opacity on f0) | is 0.07 |
| 12–19 | 0.39–0.65 | "software" (Newsreader 220, baseline 782) pops, 106 % overshoot → settle | software 0.55 |
| 26 | 0.86 | "really" (120, baseline 952) right-aligned to 930 | really 0.99 |
| 33–40 | 1.11–1.35 | HERO "dead?" (Fraunces italic ocean 260, baseline 1312, glyphs ~y 1115–1320) rises from 50 %, peaks 110 % on the word, settles; 1 % camera punch | dead 1.35 |
| 42–57 | 1.40–1.92 | dotted ink loop (fitted to the glyphs) draws round "dead?" (~y 1000–1424); "software" stays ink and sags 2.2° ("dead") | — |
| 59–78 | 1.96–2.58 | compaction: is → software → really fly on arcs into a two-line header (1.5 f stagger), "software" shifts right before rising (clears "is"); then "dead?" + loop (2.14) shrink first and glide up | also / that |
| 73–86 | 2.42–2.88 | deep app card rises (rotX 22→4, back.out) | — |
| 74–80 | 2.45–2.65 | soft white shield slams down over the card (130 % → 95 % → back.out settle), card squashes on impact | software 2.65 |
| 75–83 | 2.52–2.77 | "software" (104) pops bottom-left | software 2.65 |
| 80–88 | 2.68–2.93 | padlock drops in open, shackle snaps shut, ocean ring pulse | is 2.93 |
| 91–107 | 3.03–3.59 | small speaker card (336x252) pops in lower right, sheen; "is going to get" (76) word by word | going/to/get |
| 104–122 | 3.48–4.08 | light sweep across the sealed shield; "software is / going to get" blur up out bottom-up | — |
| 121–131 | 4.02–4.37 | "really" (96) | really 4.15 |
| 131–135 | 4.35–4.51 | "hard" pops; hairline crack zips down the shield + branch, shield shakes | hard 4.51 |
| 139–149 | 4.62–4.98 | shield SPLITS into 3 pieces (rotate −9/+6/+4°); padlock shackle pops open, lock tips; ocean glint stars + ocean glow | to 4.73 |
| 146–151 | 4.85–5.02 | HERO "protect" (Fraunces italic ink 220) rises, 106 % on the word, settles; glint flares again | protect (5.17, landed 0.15 early) |
| 151–156 | 5.02–5.233 | hold alive: pieces keep drifting apart, glow breathes, card float + tilt drift, video push, camera push, grid drift; hard cut | — |

## Layout (final pose)
Header "is software" (72/112, x 80, baseline 392) + "really" (72, x 164) / "dead?" (144, ocean, right edge 910, baseline
574) in its scaled dotted loop. Deep app card 600x400 at (110, 656), ocean edge. Shield 360x424 centred x 410 over it,
padlock 200x230 on top. Speaker card 336x252 at (612, 878), rotY −8→−6°, face-centred crop (24.5–66.7 % of source height,
face x ≈ 46 %). "really hard to" (96, x 80, baseline 1238), "protect" (220, right edge 930, baseline 1410).

## Measured bounds (no-background render, every frame, alpha > 128)
x 70–954, y 305–1470 — all 157 frames inside x 60–960, y 285–1480 (incl. camera push 1.2 %, punch, overshoots, tilt).
At alpha > 40 one frame (f146, protect at ~10 % opacity with 10 px blur) reaches y 1484.

## Deviations
- "protect" is spoken at 5.17 (brief said ~4.85): it lands at 5.02 (0.15 s early, per the contact rule). The crack is
  therefore split in two beats on the words before it — hairline crack + shake on "hard" (4.38–4.52), break-apart + padlock
  open + glint on "to" (4.62–4.98) — with a second glint flare when "protect" lands, so the broken shield reads before the cut.
- Added the spoken "software is going to get" (2.65–3.59) as small kinetic lines so the lower zone is not empty for 1.6 s
  between the compaction and "really hard to"; they blur out at 3.86.
- Speaker card 336x252 instead of ~330x230: this clip is framed close (forehead→beard ≈ 37 % of frame height), and a
  230 px card would crop the chin/forehead at card width. Card sits lower-right overlapping the app card's corner (the header
  needs the full width for the compacted "dead?" loop).
- "software" sags 2.2° on "dead" (small gag, stays ink); straightens as it compacts.
- Beat A stack spread over the whole zone (hold at 1.5–2.0 s spans x 81–946, y 371–1424).
- App card drawn in the v2_07 / v03 family (deep, ocean edge, white/grey wireframe bars, ocean image tile, three white tiles);
  v03_inside was being built in parallel, so details may differ slightly from that slot.

## V2 revision (2026-10-11, user request) — supersedes the type sizes / card size above
- Type: Inter Tight (variable, brand.css). Supporting words 800 / −0.03em, hero words 900 / −0.045em, line-height 0.88, no italics.
  Beat A: "is" 116 (800, baseline 468) · "software" 206 (900 ink, baseline 782) · "really" 116 (800, right 926, baseline 950) ·
  "dead?" 250 (900 ocean, baseline 1312) with the fitted dotted ellipse. Header: "is" 72 · "software" 108 (900) · "really" 72 ·
  "dead?" 140 (900 ocean, right edge 896). Beat B: "software" 100 (900) + "is" 80 (baseline 1252) · "going to get" 84 (right 912,
  baseline 1366) · "really hard to" 94 ("hard" 900, baseline 1252) · "protect" 214 (900 ink, right 928, baseline 1424).
- Font asserts: 900/700/800 100px "Inter Tight", 500/600 40px Inter.
- Speaker card 424x336 at (520, 832), video 424x754 at top −170 (window 22.5–67.1 % of source height: whole head incl. hair to beard),
  still overlapping the app card's lower-right corner. App card now 588x400 at (84, 656); shield (190, 628); padlock (270, 742).
  Crack pieces move slightly less to the right (RT +46, RB +8) so they stay clear of the bigger card.
- 157 frames (5.233 s). Measured bounds (no-bg render, all frames, alpha > 128): x 67–952, y 302–1475. Beat A hold (f45–62):
  x 70–944, y 365–1403. At alpha > 40 one frame (f146, "protect" ~10 % opacity, blurred) reaches y 1485.
