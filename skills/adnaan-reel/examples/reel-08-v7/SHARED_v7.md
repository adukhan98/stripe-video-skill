# v7 "MINT" STYLE TEST — this OVERRIDES everything below it in SHARED.md wherever they conflict

Adnaan approved a new house look (2026-10-17) from two reference reels. Look at these before you build:
- `~/Desktop/reels/reel-08/edit/style_v7/refs/ref1_talk_frames.jpg` — the TALK reference (_k.elsie): speaker full-screen, words around/behind her.
- `~/Desktop/reels/reel-08/edit/style_v7/refs/ref2_visual_frames.jpg` + `ref2_visual_contact.jpg` — the VISUAL reference (gregisenberg): grey board, strong
  vignette, white Phosphor-style glyphs inside mint/charcoal discs chained by thin lines, the camera travelling along the chain,
  clean flat vector props (magnifier, film strip, pie chart, polaroid, phone mockup), soft shadows, NO hand-drawn anything.
- `~/Desktop/reels/reel-08/edit/style_v7/refs/his_still.jpg` — Adnaan in this take: light heather-grey sweatshirt, warm room. Not mirrored.

## What stays (his explicit choices)
- **Our kinetic, dynamic captions**: Inter Tight 900 (+ 800/700 supporting) phrases on their spoken words, collage-staggered,
  hero 170–270 authored, nothing under 64, words = his words only. NO continuous subtitles. NO serif fonts.
- The runtime (`hf/paper.js`) for words, entrances, exits, punch, floats; Lasseter principles; exact frame counts; safe zone
  x 60–960 / y 285–1480 and nothing right of x 900 below y 1200 (IG icons); readability rules; frame 0 = thumbnail.

## What changes
- **No red anywhere. No hand-drawn marker layer**: no boiling loops/underlines/doodles, no Caveat notes, no felt-tip texture.
  If a line must draw itself (a connector, an underline bar, a magnifier rim) use clean vector strokes — e.g.
  `M.line(pts, at, {boil:false, texture:false, amp:0, width:6, color:'var(--brand-deep)'})` or plain SVG + GSAP drawSVG
  via strokeDashoffset. Clean, even width, round caps.
- **Palette** (tokens in hf/brand.css): mint `--brand-primary` #7CC49E (hero word colour = the runtime's `.ocean` class, active
  disc, rings); deep mint `--brand-primary-dark` #2F8A63 (small accent text, highlighter edge); charcoal `--brand-deep` #2B2B2B
  (ink discs, dark cards); ink `--brand-text` #232323; `--mint-soft` #CFEAD9 (highlighter, soft panels); `--peach` #F2A07B
  = DATA ONLY (charts, result bars, rolling numbers). `--disc-shadow`, `--vignette-strong` are provided.
- **Two modes**:
  - **TALK** = him full-screen (`.spk.full`, data-face 0.40). Our kinetic captions on top: CHARCOAL ink words with a soft light
    glow (`text-shadow: 0 0 22px rgba(240,236,230,.95), 0 0 8px rgba(240,236,230,.9)`), hero word in mint with the same glow,
    no paper strip. Usually captions only; occasionally ONE icon disc. No pills.
  - **VISUAL** = the board, no speaker: our paper + grid but the vignette much stronger (overlay `--vignette-strong` on #bg);
    content lives on a WORLD layer larger than the frame and the CAMERA travels across it (GSAP x/y/scale on a #world
    container, eased power3/expo, never linear; 1 move per sentence). Hard cuts between scenes.
- **Icon discs** (the signature object): white Phosphor FILL glyphs (SVGs in `hf/assets/icons/`, `fill="currentColor"`) centred
  in a circle — charcoal disc = default, mint disc = the current item. Glyph ≈ 46 % of the disc. `box-shadow: var(--disc-shadow)`.
  Pop in with anticipation + overshoot (scale 0 → 1.12 → 1), glyph lands 2 frames after its disc.
  Discs are chained by a thin charcoal line (4 px, round caps) that draws on between them.
- **Hero objects** = clean flat vector illustration: flat fills from the palette, soft shadows, no outlines that wobble — with
  the same personality in motion (anticipation, overshoot, squash, secondary action).
- **Real pages/strips**: big readable white cards (soft shadow), highlighter in `--mint-soft` with a `--brand-primary-dark` edge;
  phone/polaroid mockups only sometimes.
- **Signature transition** (his footage shrinks into the board): the full-screen footage's clip-path animates from the full
  frame to a CIRCLE (or small rounded card) while it scales/translates to its target on the board as the camera pulls out;
  anticipation dip first, overshoot on landing, the board fades up behind it (paper visible around the shrinking footage).

## Shared geometry — THE HABIT CHAIN (t3 builds it, t4 opens on exactly t3's final state)
Six discs, diameter **180**, centres (frame px, world = frame at the end of t3):
  1 (300, 560) · 2 (620, 700) · 3 (330, 880) · 4 (640, 1030) · 5 (330, 1190) · 6 (600, 1360)
Icons (hf/assets/icons): 1 microphone · 2 eye · 3 chat-circle-dots · 4 magnifying-glass · 5 folder-open · 6 watch.
Connector: 4 px charcoal line centre→centre in order 1→6 (drawn behind discs). All discs charcoal except the active one.
End state of t3: disc 1 = HIS FACE in a circle (the shrunk footage, mint 8 px ring) at (300, 560), discs 2–6 charcoal with
white glyphs, connector drawn. t4 frame 0 must match that exactly (copy t3's chain code; scenes.py seam will compare).
