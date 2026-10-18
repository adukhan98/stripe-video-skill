# t1_hook — v7 "MINT" style test, TALK mode, two variants

- **A (depth)**: `hf/` → `render.mov` — footage → CEO cards → his matte (`speaker_cut.webm`, same timing, same 1.02 push, exactly over `speaker.mp4`) → name tags → hook + kinetic words. The cards start hidden behind his head and slide out from behind it.
- **B (flat)**: `hf_b/` → `render_b.mov` — same file with `VARIANT = "B"`, no matte. The cards are smaller and sit in front of him, over his hair and ears only, and pop in at the same times.
- Both are 96 frames, 1080x1920 @ 30, `data-face 0.40`. The timing is the same in both. No red, no marker, no Caveat.

## Key poses (scene seconds → frame)
| t | f | on screen | word |
|---|---|---|---|
| 0.00 | 0 | THUMBNAIL: the text hook is finished: "How to use AI" / "like the top" (Inter Tight 900 charcoal, light halo) / "0.1%" (mint) with a solid mint bar. It sits over his hair and forehead, above his brows. No cards yet. | The |
| 0.30–0.51 | 9–15 | The cards set off one after another: Satya (TL), Sam (TR), Jensen (ML), Elon (MR). Each takes a 3-frame anticipation tuck, then arcs out. In A they come from behind his head and his matte hides them on the way out. | top (0.41) |
| 0.59 | 18 | HERO BEAT: the hook's 0.1% dips (0.96), punches to 1.09 and settles with back.out. The bar flexes 1 f later. 1 % camera punch on the hook. | 0.1% |
| 0.56–0.80 | 17–24 | The cards land with a tilt overshoot (1.7× rot, scale 1.03 → 1). Each white name tag pops 3 f after its card. | 0.1% |
| 1.1–2.4 | 33–72 | Hold, kept alive: the cards breathe 2–3 px (each on its own period), plus the footage push and his own motion. | aren't using |
| 2.17 | 65 | "AI" in the hook nods: a 7 px dip with slight squash, then back with overshoot. | AI |
| 2.45 / 2.61 | 74 / 78 | "the way" (100 authored, charcoal) rises on his chest, y ≈ 1200–1285. | the way |
| 2.73 | 82 | "you" (180 authored, mint, hero overshoot 1.08). | you |
| 2.91 | 87 | "are." pops (charcoal) and holds alive to the cut. | are. |

## As-built
- Hook: `#h1` cx 521, base 350, 80; `#h2` cx 558, base 424, 80; `#h3` "0.1%" cx 512, base 518, 126, mint. `#bar` is 13 px with round caps, under the 0.1%, at y ≈ 528. The hook is centred-staggered over his crown. The tightest fit on this framing is between the zone top (285) and his brows (≈ 550).
- A cards (box incl. 8 px white border, radius 22): Satya 80,300 188x232 −5°; Sam 770,302 178x222 +5°; Jensen 80,622 188x232 +4°; Elon 778,630 172x214 −4°.
  - Each photo is a headshot crop computed from the face position in the source, so the CEO face sits in the part of the card his head does not cover.
  - Slide-out: x power3.out / y power2.out = an arc of 0.42 s, starting 200–240 px inside his silhouette.
- B cards: Satya 84,308 160x198; Sam 782,308 156x194; Jensen 84,608 160x198; Elon 790,626 152x190. They pop from 40 px beside his head (0.42 → 1.07 → 1).
- Tags: Inter 600 38 px, two lines (first / last name), white with radius 14 and a soft shadow. They sit under each card, aligned to its outer edge. In A they are in front of the matte so they always read.
- Kinetic: `#kWay` x 104, base 1264, 100; `#kYou` x 80, base 1424, 180 ("you" mint hero, "are." pop).

## Checks
- `slots.py check --motion` (A): `motion: no dead holds · checks passed: size, fps, duration, alpha channel`.
- ffprobe `-count_packets`: render.mov **96**, render_b.mov **96** (prores 4444, 1080x1920, 30/1).
- Bounds: every frame diffed against a footage-only render of the same push (`qa/ref.mov`, `qa/bounds.py`). Glow halos and shadows count.
  - **A: x 70–956, y 286–1476**
  - **B: x 68–954, y 286–1472**
  - 0 frames outside x 60–960 / y 285–1480, and 0 px right of x 900 below y 1200.
- Matte alignment (A): render vs reference over his face/hair with no overlays → mean diff ≈ 5, which is VP9-vs-H.264 encode noise.
  - The only larger diffs are the card edge showing through soft hair alpha where it is tucked.
  - Edge crops (`qa/a_f14_edge.png`, `qa/zoomTR.png`, `qa/zoomL.png`) show no double edges and no halo.
- Frame 0 (`qa/f0_end_AB.png`): the finished hook, him, nothing mid-entrance, and no cards yet (true content only).

## Principles checklist
- Contact frames on words: 0.1% punch at 0.59. The cards land through "top → 0.1%". "AI" nods at 2.17. "the/way/you/are." use the runtime contacts (2.45 / 2.61 / 2.73 / 2.91).
- Anticipation: each card tucks 3 f further in (A) or dips (B) before it moves. The 0.1% shrinks to 0.96 for 3 f before its punch. The hero "you" uses the runtime pre-sink.
- Overshoot + settle: cards (tilt 1.7×, scale 1.03 → back.out 2), tags (1.08 → 1), 0.1% (1.09 → back.out 2.4), bar (scaleX 1.06), "you" (1.08).
- Parts lag the whole: the cards are 2 f apart, tags trail their card by 3 f, and the bar trails the 0.1% by 1 f.
- Long moves on arcs: card slide-outs ease x and y differently and rotate into the travel.
- Squash/stretch on shapes only: there is none on photos or type, apart from a 4 % squash on the "AI" nod, which is a type nod rather than a stretch. Photos and logos are never deformed.
- One focal point: hook (0–0.5) → cards + 0.1% punch (0.3–0.8) → his face (1–2.4) → "you are." (2.45+). The cards are settled, untouched by anything else, while the kinetic line lands.
- Secondary action, no dead hold ≥ 1 s: cards breathe, the footage pushes 1.00 → 1.02, the words layer pushes 1.006, and the AI nod at 2.17 breaks the 1.1–2.4 stretch. `slots.py` reports no dead holds.
- One exaggerated hero beat: the 0.1% punch at 0.59, with the camera punch (the stamp SFX).
- Exits faster than entrances: nothing exits. The scene holds alive into the hard cut.
- One light direction / contact shadows: all card and tag shadows fall straight down and soft. There are no outlines and no hard offsets.
- Nothing reads as a static slide: each sampled frame has something in motion.

## Richness (TALK = minimal)
- Hero object: the CEO photo cards. In A they slide out from **behind his head** (true occlusion by the matte); in B they pop beside it.
- Micro 1: the hook's 0.1% punch + bar flex on "0.1%".
- Micro 2: name tags pop after their cards. Cards breathe.
- Micro 3: "AI" nods on "AI".

## Readability
- The zone was measured on every frame (above).
- No strips or real pages.
- No semi-transparent text at rest. Only the runtime entrance blur and opacity apply to words and tags (≤ 6 f).
- No handwriting.
- Nothing covers his face: the hook bar sits ≥ 10 px above his brows. In B the cards overlap only his hair and ears.
- Faces of all four CEOs are fully visible in both variants.
- Type sizes:
  - Kinetic hero 180 and supporting 100.
  - Hook lines 80, with the 0.1% at 126. This is under the 170 hero size; see deviations.
  - Tags 38 px.
- Contrast:
  - The hook sits over his black hair. It uses a tighter, brighter three-step halo, so the charcoal reads as ink rather than a grey haze.
  - **Mint words use a soft dark shadow, not the light glow.** Mint on a light halo, or on his light-grey sweater, loses contrast.

## Recommendation: **A**
A is the Ref 1 look Adnaan asked for ("behind me"). The CEOs slide out from behind his head, which only the matte can do: real depth, and a hook moment you can't get from a flat overlay. The matte sits on identical pixels, so its errors are invisible: at most a few soft hair-edge pixels show where a card is tucked.

B is cleaner and its cards are fully visible. But it reads like a standard sticker overlay, and its cards have to shrink to stay off his face.

A's one cost: the right-hand cards are only partly visible, because his head fills x ≈ 213–874. The headshot crops shift each face into the visible part to cover this.

## Deviations
1. **No giant 0.1% in A.**
   - His head fills x ≈ 213–874 from the zone top (y 285) down to his shoulders. The free background in the zone is two lanes, ≤ 155 px (left) and 85–130 px (right) wide, measured from the union of the matte over all 96 frames.
   - A 300-authored "0.1%" is ≈ 625 px wide. Behind him it would be ~80 % hidden, i.e. unreadable text, which breaks the "readable or gone" rule. The top band is taken by the hook.
   - The depth beat is carried by the cards sliding out from behind his head instead.
2. **Hook type is smaller than a usual hook (80/80 + 126 for the 0.1%).** It has to fit between the zone top and his brows (≈ 265 px) and between the TL/TR cards. A wider two-row hook would push the cards into lanes too narrow for faces plus names.
3. **Names on two lines (first / last), 38 px.** Single-line 40 px tags are 233–260 px wide and do not fit beside his head. In A the tags sit in front of the matte so they stay readable; the cards stay behind him.
4. **Mint words ("0.1%", "you") use a soft dark shadow, not the light glow.** This is for readability (above).
5. The marker layer is not initialised, per v7; `marker.js` and `marker.css` are still loaded as scaffolded. The runtime files are untouched.

## Files
- `hf/` (A), `hf_b/` (B), `render.mov`, `render_b.mov`, `beats.json` (shared by both variants).
- `check_sheet.jpg` and `motion_strip.jpg` (A). Scratch is in `qa/`: snapshots, `ref.mov`, `bounds.py`, `union.png`, edge crops.
