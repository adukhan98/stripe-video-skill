# stripe-youtube — style (binding)

**The look: v7 — the adnaan-reel design system on the 16:9 board, coloured by the project's brand file.** This edition
ships Stripe as the default brand (`brand/stripe.json`). Look first at `assets/style/stripe_youtube_sheet.jpg` (the first
video made with it) and `assets/style/v7_youtube_sheet.jpg` (the same system in Adnaan's mint), then read the scenes in
`examples/stripe-v1/` and `examples/yt-01-v7/`. Default tokens live in `templates/runtime/v7yt.css` (+ `board.css`
underneath); the project's `brand/brand.json` → `brand.py` → `brand.css` re-points them in every scene. Never colour per
scene; a brand change goes in brand.json (`brand.py apply`), a global look change in `templates/runtime/` (then `board.py
runtime`). The older Greg Light/Dark marker look is at the end, only on request.

The STRUCTURE is unchanged from the original youtube system: the board on screen most of the time with his plain camera
in a fixed card bottom-right, full-frame talk as punctuation, screen recordings in a window card.

## Palette (tokens from brand.css; never hard-code a colour)

| token | brand.json key | Stripe | use |
|---|---|---|---|
| `--bg` paper + 64 px grid + `--vignette-strong` | background | #EEF1F6 | every opaque scene |
| `--brand-primary` | primary | #533AFD blurple | THE accent: the current item, the hero word (`.mint` / `.emph` — class names kept from v7), rings, check discs, bars, the ring around his card |
| `--brand-primary-dark` | primary_dark | #3B22E0 | small accent text, the highlighter edge |
| `--brand-deep` | deep | #061B31 slate | icon discs, dark cards, connectors, clean strokes, tags, grid and shadows |
| `--ink` | text | #061B31 | all other text |
| `--brand-card` | card | #FFFFFF | flat white cards, real pages |
| `--mint-soft` | soft | #E4DFFF | highlighter, soft panels |
| `--mint-panel` | panel | #B9ADFF | stronger soft panels |
| `--strawberry` | data | #E8435A | DATA ONLY: chart bars, result numbers, rolling counters, gauges. The "good" result may be the accent. |
| `--muted` | muted | #6B7C93 | small caps kickers, secondary labels |
| captions hero | captions.hero (else primary_light) | #9D8CFF | the one hero word per phrase in white talk captions (light enough on his background) |

One accent per frame: the brand primary. No other hue, no pastel tiles with rims, no category hues (stray hue classes
collapse onto the accent in v7yt.css). scenes.json `hue` is ignored by the look. Logos come from the brand's official kit
(the Stripe wordmark is not in this repo: download it from https://stripe.com/newsroom/brand-assets into `edit/logos/`).

## Type

Inter Tight 900 hero (≥ 120 px; mint for at most 1–2 hero words per frame), 800/700 supporting (≥ 60 px), Inter 600/500
labels (≥ 34 px), small caps kickers (Inter 600, letter-spacing .12em, muted). Geist Mono for code. Kinetic phrases are
collage-staggered (lines offset, sizes vary), never a centred block of equal-size text. NO Caveat, no handwriting.
Words on screen are words he says.

## Objects (hf/v7yt.js — read its header)

- **Icon discs** (the signature): `V.disc(parent, {x, y, d, icon, mint, tag})` + `V.discIn(el, t)` — a white Phosphor FILL
  glyph in a charcoal disc; mint = current (`V.mintTo` / `V.charcoalTo`). Icons in `assets/icons/` (board.py copies them to
  hf/assets/icons). Another icon: `$R/fetch.py icon --edit-dir <edit> <phosphor-name>`, then copy `<edit>/icons/<name>.svg`
  into the scene's hf/assets/icons (and into this skill's assets/icons if it will be reused).
- **Disc chain** for a list / framework / map: `V.chain` + `V.chainDraw` (connector draws 1→N, each disc pops as the line
  reaches it). One shared module for every chain scene (`examples/yt-01-v7/chain_common.js`): each push opens on the previous
  push's exact end state, so the cuts read as one camera. **Labels sit on empty paper above or below the disc, never in the
  row** (in-row labels ran over the next discs — rejected). Only the current item's label is on screen.
- **Flat vector hero objects**: flat palette fills, soft shadows (`var(--shadow)`, `var(--disc-shadow)`), rounded geometry,
  personality in motion (anticipation, overshoot, squash, secondary action). No outlines that wobble, no hatching.
- **Cards**: `.v7-card` (white, r 28, soft shadow), `.v7-card.dark`, `.v7-card.mint`. Chat bubbles, prompt boxes,
  clipboards, phones, browser windows are flat white cards.
- **Real pages**: big readable white cards (text ≥ 34 px on screen), `V.hl(card, [x, y, w, h], t)` = mint highlighter ON the
  spoken phrase. Official logos stay official `<img>` (in a small white chip).
- **Clean strokes**: `V.line` (connectors, arrows with a small solid triangle head, curves allowed), `V.ringRect` /
  `V.ringCircle` (a mint ring that draws on), `V.bar` (solid underline bar), `V.check` / `V.cross` (in a small disc).
  Even width 5–8 px, round caps, no boil, no texture.

| an older brief / habit says | do |
|---|---|
| marker loop / circle | `V.ringRect` / `V.ringCircle`, mint, drawn on the spoken word |
| marker underline | `V.bar` |
| marker arrow / bracket | `V.line` charcoal with a solid head |
| handwritten note | Inter Tight 800 label ≥ 44 px, ink or deep mint, still only his words |
| check / cross | `V.check` / `V.cross` |
| strike-through | a solid charcoal bar across, drawn left → right |
| pastel tile with a rim | flat white card, or a charcoal disc with an icon; the current/answer one mint |
| yellow highlighter | `V.hl` |
| number coin | charcoal disc with an Inter 700 number (`.coin`), mint when current |
| hatch fill | flat muted fill #D6CFC8 |
| tape on a polaroid | none: a soft shadow is enough |

## Motion and camera

Lasseter defaults (`B.in` / `B.word` / `B.punch` / `V.discIn`): anticipation, overshoot + settle, overlap, arcs, exits ~40 %
faster than entrances, no linear moves except mechanical drift. Opaque scenes: a WORLD on `#cam` that may be bigger than the
frame and a camera that TRAVELS (`V.cam(t, cx, cy, s, {dur})` — x and y on different eases = an arc; `B.camSet` for frame 0),
one move per sentence. The paper grid drifts (board.js). Something moves every 1–2 s; no dead holds; no ghosted text.
Pops 5–8 f, moves 10–16 f, camera moves 0.8–1.2 s. Hold text ≥ 0.3 s per word + 0.5 s. Every entrance is a `fromTo` with
an immediately rendered start state (seek-safe) — frame 0 already shows the heading or main object.

## Layout (16:9)

- **His card**: plain camera, rounded 24 px, 6 px white rim, soft shadow, at x 1600 y 640 w 260 h 346 for the WHOLE video
  (moves only on a cut), composited by `compose.py`; v7yt.js draws a mint ring around it in every opaque scene. Keep the card
  zone x 1574–1886, y 614–1012 clear (an unlabelled background disc may pass behind it). No matte by default.
- **Title-safe** x 96–1824, y 54–1026. Keep the last 20 s clear of CTAs and important text (YouTube end screens).
- **One focal point**: a hero object + 1–3 micro-animations; recede objects, never words.

| Layout | What is on screen | Built by |
|---|---|---|
| talk | him full frame (base.mp4) **+ full-coverage talk captions** | compose.py + talkcaps.py (generated overlays) |
| screen | board + window card with his screen recording, zoomed on what he clicks/names, + card | compose.py (zoomplan) |
| screen + callout | + a `callout_overlay` (mint ring / charcoal arrow) on the target after the zoom lands | board.py (mov) + compose.py |
| canvas | one real thing or one bespoke flat object + a kinetic number/phrase | board.py (mp4) + card |
| map | the video's framework as a disc chain; the camera travels to the current item; doubles as the chapter card | board.py + card |
| board | numbered heading + a flow of discs/cards + one plain line | board.py + card |
| proof | the real page/post/paper in a white card, V.hl on the phrase, official logo chip, his line as kinetic type | board.py + card |

## Talk captions (full-frame talk windows)

He asked for captions on **every** full-frame talk window ("for all the ones where I am full screen, add the captions
there"), so they are not sparse accents any more — `helpers/talkcaps.py` generates them from the transcript; never
hand-build them. Look: WHITE Inter Tight 800 (`.w7`), ONE mint hero word per phrase (900, 1.3×), left column x 96–720
beside his head, never over his face, no boxes, no underline, only a very soft radial scrim. Words pop on their spoken
times (blur-up), a phrase blurs away as the next starts, the stack exits in the last 6 frames; first and last frames fully
transparent. Phrases ≤ 7 words split at sense points (commas, conjunctions, breaths — never after "the" / "to"), 2–3
words per line, `word-spacing: .16em` (without it words ran together). **Place the column on a calm, darker area of his
background** (`layout.json captions.y`): on IMG_2533 the first version sat over white buildings and was unreadable; y 280
(the sky) fixed it — check a still of every talk window before rendering. The SRT is still delivered for YouTube.

## Sound

SFX only on structural beats (low & warm v6 kit: stamp, clunk, thud, paper, whoosh, pop) — a chapter/map landing, a big
page sliding in, the CTA — about 1 per 30–60 s, tagged in beats.json with a "role", mixed at −18 dB. **Music bed on by
default** for videos > 5 min: a calm ElevenLabs instrumental, ducked under the voice and levelled so the ducked bed sits
**~5 dB under his voice** (`layout.json music_under_voice_db`, compose.py measures and sets the gain). At the old fixed
level he could not hear it at all ("I still can't hear it") — he talks almost wall-to-wall, so the sidechain keeps the bed
ducked nearly all the time. Voice always on top; final −14 LUFS, true peak < −1 dBTP.

---

## Legacy: Greg Light / Greg Dark (only when he asks for it — scenes.json `"look": "greg"`)

Approved 2026-10-16, replaced by v7 as the default on 2026-10-17. References: `assets/style/greg_light.jpg`,
`greg_dark.jpg`. Light: warm paper #E4DED9, pastel tiles with a 4 px rim of the same hue, black marker ink, number coin in
the chapter hue. Dark: charcoal #1E1E1E with a dot grid, saturated tiles, white marker, orange tag #D9611B, yellow emphasis
#FFD43B. Hues (Open Color) are categories — blue, green, yellow, violet, orange, teal — one per chapter and one per list
item; no red accent. Marker layer (`marker.css/js`): loops, arrows, underlines, Caveat 700 notes ≥ 46 px. Real pages stay
light with a yellow highlighter; callouts on screen recordings use `--callout` (ink on light, orange on dark).
