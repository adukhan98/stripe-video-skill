# SHARED art direction — reel-03 v2 "Ocean editorial" (READ FULLY before building)

The user rejected a bland edit and chose this look from THEIR reference reel. Match the reference's
craft: soft, tactile, editorial, everything floats and settles. Look at these first:
- `animations/ref_grid.jpg`, `animations/ref_detail.jpg` — frames from the user's reference reel (style only; never copy its content)
- `animations/style_hook.png`, `animations/style_refine.png` — the approved still style frames for THIS reel (Ocean palette)

## Canvas & scene type
- 1080x1920 @30. Every v2 scene is a FULL-SCREEN OPAQUE scene: the grey-paper background covers the whole frame
  for the entire slot (first and last frame opaque too — scenes butt against each other with hard cuts).
  `slots.py check` will report "first/last frame is not fully transparent" — that is EXPECTED for v2 scenes;
  every other check (size, fps, duration, motion) must pass.
- Background (every scene, identical so cuts between scenes feel like one world):
  `#E4DED9` + 60px grid lines `rgba(20,20,20,.055)` 1.5px + vignette
  `radial-gradient(ellipse at 50% 45%, transparent 45%, rgba(90,80,72,.22) 100%)`. Very slow drift on the grid
  (e.g. 20px over the whole slot) so the bg is never dead.
- Important content inside the reels safe zone x 60–960, y 285–1480 (no subtitles in v2 — the kinetic serif
  phrases ARE the captions, so use the whole zone).

## SCALE — the user asked to GO BIGGER (after seeing the hook test). Fill the frame like the reference:
- Hero speaker card: ~900x620 (x 60–960), not 780. Secondary/small speaker card: ~560x390.
- Kinetic serif: hero words 190–260 px, supporting words 90–130 px, smallest connective words ≥ 64 px.
  A phrase stack should span most of the zone width. Never leave the bottom 40% of the zone empty.
- UI objects/coins/cards also scaled up so each scene reads instantly on a phone.

## Palette (brand.css tokens only)
- `--brand-background` #E4DED9 paper · `--brand-card` #FBFAF8 card white · `--brand-text` #141414 ink
- `--brand-primary` #2E9CCB ocean accent (key words, active coin, card edge) · `--brand-primary-dark` #1F7EA8
- `--brand-deep` #0D2731 deep teal (hero/"picked" UI cards, agent puck) · `--brand-muted` #8E8780
- One accent only. Accent on 1–2 key words per phrase.

## Type
- Kinetic serif phrases: Newsreader 600 (regular words, ink) mixed with Fraunces 700 ITALIC (key words, usually
  ocean, sometimes ink), lowercase, letter-spacing -0.01 to -0.02em, line-height ~0.95. Sizes vary per word
  (64–190 px) and words stack in a staggered collage (offset left/right per line) like the reference.
- Labels/numbers: Geist 500/600. Repo names in Geist 500, muted, small.
- Assert fonts loaded (document.fonts) before rendering.

## Objects (soft, no outlines, no hard offset shadows)
- **Speaker card**: the live speaker video in a landscape rounded card (radius 30), slight 3D tilt
  (perspective ~1600px, rotateY ±6–10°, rotateX ~5°), an ocean "edge" under it (`box-shadow: 0 16px 0 -2px #2E9CCB`)
  plus a soft drop shadow `0 50px 70px -10px rgba(40,30,20,.35)`. Video is muted, object-fit cover, face
  centred (the face sits around y 35–55% of the source frame).
- **Coins**: white neumorphic discs `radial-gradient(circle at 35% 30%, #fff, #F1EEEA 70%)`, shadow
  `0 18px 30px rgba(60,50,40,.22)`, Geist numbers. Active coin = ocean gradient with deep-teal text.
- **UI cards**: #FBFAF8, radius 24–28, soft shadow `0 30px 50px -12px rgba(60,50,40,.30)`, grey wireframe bars
  `#E5E0DA`. "Picked"/hero cards turn deep teal #0D2731 with ocean accents.
- **Pills/notifications**: black #141414 rounded pills with white Geist text (like the reference's stacked notifications).
- **Dotted paths**: ink, 3px, dasharray "2 12", round caps — connect things, draw on with strokeDashoffset.
- **Cursor**: white arrow with ink stroke, moves on eased arcs, clicks with a quick scale dip.
- Never draw the Claude logo or any brand logo. Real pages are provided as images when needed.

## Motion (strength: smooth + tactile, like the reference)
- Entrances: rise 40–80px + fade + slight scale (0.94→1) with `power3.out` / `back.out(1.4)`, 0.35–0.6 s.
  Overlap and stagger 2–4 frames. Things settle with a small overshoot. Exits are quick (0.2–0.3 s) or
  the scene simply holds into the hard cut.
- Kinetic serif: each word/line lands on its spoken word (contact frame on the word time from words.txt,
  start ~0.15 s earlier). Mask-reveal or rise-in per word; accent italic words get a little extra overshoot.
- Continuous life: gentle float (2–4px sine drift) on cards/coins, slow camera push (1.00→1.03) on the scene.
  No dead holds.
- One focal point at a time.

## Continuity across scenes
- The five white coins 01–05 are the continuity object: they appear in the hook, each skill scene features ITS coin
  (turns ocean when that skill is named), and the wrap-up scene orbits all five.
- Each skill scene opens with a "chapter" beat on the spoken "First one / Second one …": its coin (ocean, ~220px)
  + the skill name in big kinetic serif, landing on the name. Then the demo graphic for that skill takes over.
- Real pages (when provided in hf/assets/) appear inside a soft browser card (rounded, light chrome bar with three
  grey dots and the URL in Geist muted), tilted slightly, slow internal scroll — never full-bleed, never flat.
- Speaker video, when provided at hf/assets/speaker.mp4, is already cut to the slot (starts at slot 0, muted, 1080x1920).
