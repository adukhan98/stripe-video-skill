# adnaan-reel style — the binding art direction

This is Adnaan's house style. Every edit made with this skill must look like it belongs to the same
series as the approved reference reel. **Look before you build:**

- `assets/style/v2_contact_sheet.jpg` — ten frames of the approved reel (the canonical look)
- `assets/style/v2_*.jpg` — the same frames full size
- `examples/reel-03/*.html` — the ten scene compositions that produced it (working code to copy from)

The look in one line: **soft, tactile, editorial — a grey paper world where kinetic serif type and
soft 3D objects explain what the speaker says, and the speaker floats in as a tilted video card.**

## Canvas and scene type

- 1080x1920 @30 (landscape deliveries: 1920x1080, see SKILL.md). Every beat of the reel is a
  **FULL-SCREEN OPAQUE SCENE** (slot layout `scene`): the paper background covers the whole frame on
  every frame, first and last included. Scenes cut hard into each other. The raw footage is never shown
  full-bleed — the speaker appears only as the embedded `hf/assets/speaker.mp4` inside a card (exception:
  a full-bleed screen-recording demo, see SKILL.md "User media").
- **Background, identical in every scene** (so cuts feel like one world):
  `#E4DED9` paper + 60 px grid lines `rgba(20,20,20,.055)` 1.5 px + vignette
  `radial-gradient(ellipse at 50% 45%, transparent 45%, rgba(90,80,72,.22) 100%)`.
  The grid drifts slowly (~20 px over the scene, linear) so the background is never dead.
- **Safe zone**: all important content inside x 60–960, y 285–1480. There are **no subtitles** — the
  kinetic serif phrases are the captions, so the whole zone is usable down to y 1480.

## Palette (brand.css tokens only — never hard-code hex in a scene)

| Token | Default (Ocean) | Role |
|---|---|---|
| `--brand-background` | `#E4DED9` | grey paper — every scene |
| `--brand-card` | `#FBFAF8` | soft UI cards, coins |
| `--brand-text` | `#141414` | ink: serif phrases, labels, black pills, agent puck |
| `--brand-primary` | `#2E9CCB` | THE accent: key words, active coin, speaker-card edge, checks |
| `--brand-primary-dark` | `#1F7EA8` | accent gradient bottom, pressed states |
| `--brand-deep` | `#0D2731` | hero / "picked" / "after" UI cards |
| `--brand-muted` | `#8E8780` | small Geist labels, repo slugs, URLs |

- **One accent only.** Accent on 1–2 key words per phrase, the active coin, ticks, progress.
- Accent presets (pick with `scenes.py init-brand --accent <name>`): ocean (default), cobalt, terracotta,
  lilac, mustard, blush, olive, red, mint — see `assets/style/accent_options.jpg`. Paper, ink and card
  never change. A brand-specific video may use the brand's colour as `--accent "#hex"`.
- Off-palette colour is allowed only when it is the real thing (a red REC dot, a real logo, a real page).

## Type

- **Kinetic serif phrases** (the captions): `Newsreader` 600 for regular words (ink) mixed with
  `Fraunces` 700 *italic* for key words (accent, sometimes ink). Lowercase as spoken (keep proper
  nouns), letter-spacing −0.01 to −0.02 em, line-height ~0.95.
- **Sizes — big** (the user asked for bigger after the first test; this is the floor, not the ceiling):
  hero words 190–260 px, supporting words 90–130 px, the smallest connective words ≥ 64 px. A phrase
  stack spans most of the zone width. Never leave the lower 40 % of the zone empty for long.
- Words in a phrase **stack as a staggered collage**: lines offset left/right, sizes varying per word
  (see `v2_01`, `v2_06`, `v2_09`). Never a centred block of equal-size text.
- **Every on-screen word must be a word the speaker actually says** (from `words.txt`), with ASR
  spelling fixed (brand and product names). You may omit filler words; you may not paraphrase.
  Only exception: `&` for a spoken "and" in a title-like phrase.
- Labels, numbers, repo slugs, UI text: `Geist` 500/600. Use drawn SVG icons for ✓ ✗ (Geist lacks the glyphs).
- Assert the fonts loaded before anything renders (`document.fonts.check`) — a fallback face is a failed scene.

## Objects (soft — no outlines, no hard offset shadows)

- **Speaker card**: the live speaker video in a landscape rounded card (radius 30), 3D tilt
  (perspective ~1600 px, rotateY ±6–10°, rotateX ~3–5°), accent edge underneath
  (`box-shadow: 0 16px 0 -2px var(--brand-primary), 0 50px 70px -10px rgba(40,30,20,.35)`), a light
  sheen sweep as it lands, slow float. Hero size ~868x600 (the widest that survives the tilt inside
  x 60–960); secondary ~560x390; small ~330x230. **Crop to the face**: the video is 1080x1920, scaled
  to the card width; pick the vertical window so the face is centred (see `v01_hook.html` `#speaker`).
  Never a circle.
- **Coins**: white neumorphic discs `radial-gradient(circle at 35% 30%, #fff, #F1EEEA 70%)`, shadow
  `0 18px 30px rgba(60,50,40,.22)`, Geist numbers, four tiny tick marks. Active coin = accent gradient.
  Coins are the **continuity object** for any list (01…N): they appear in the hook, each item's scene
  features its coin, the wrap-up orbits them, the CTA stacks them.
- **UI cards**: `--brand-card`, radius 24–28, soft shadow `0 30px 50px -12px rgba(60,50,40,.30)`,
  grey wireframe bars `#E5E0DA`. "Picked"/"after" cards flip to `--brand-deep` with accent details.
- **Browser card** (real pages): rounded, light chrome bar with three grey dots and the URL in Geist
  muted, slight tilt, slow internal scroll of the captured page. Never full-bleed, never flat.
- **Black pills**: `--brand-text` rounded pills with white Geist text — notifications, stat pills
  ("★ 94.5k on GitHub"), labels ("</> my codebase", "→ your inbox"). Stack them like notifications.
- **Agent puck**: black disc with a simple robot face (two accent eye-dots), glows/bobs when fed.
- **Dotted paths**: ink 3 px, dasharray "2 12", round caps, drawn on with strokeDashoffset; things
  ride them (cards into the puck, a line from the CTA word down to the speaker card).
- **Cursor**: white arrow with ink stroke, moves on eased arcs, clicks with a quick scale dip.
- **Real things over abstractions**: real pages, repos, star counts, file headings, product names.
  Illustrative UI (wireframes, checklists) is fine; invented numbers or quotes are not.
- Never draw a brand's logo. Real logos only from supplied/captured files.

## Motion

- Entrances: rise 40–110 px + fade + blur(6–10px→0) + scale 0.55–0.94→1, `power3.out` /
  `back.out(1.4–2.2)`, 0.3–0.6 s. Hero words overshoot to ~106–112 % on their spoken word and settle.
- **Contact frame on the word**: start the entrance ~0.13–0.2 s before the word time in `words.txt`.
- Stagger siblings 2–4 frames. Groups exit bottom-up or as a quick blur-up (0.2–0.3 s) to make room.
- Continuous life: grid drift, slow camera push (1.0→~1.015–1.02, keep everything in the zone),
  2–4 px sine float on cards/coins, a 1 % punch on the scene's biggest word. **No dead holds.**
- One focal point at a time. Scenes hold alive into the hard cut — no exit animation needed.
- Measure your bounds: render-check every frame stays inside x 60–960, y 285–1480 including
  overshoots and the camera push; shrink the push before shrinking the type.


## Project specifics (edit per project)

- Reel: "Reverse Engineer Anything" (REA) — an open-source repo (github.com/morluto/rea) that lets coding agents inspect apps without source code, explain how features work with evidence, and build a version. Then: AI rebuilt 7 Adobe apps (storytold "Craft" apps); "is software dead?"; what's left of software is personal. CTA: comment "reverse".
- Accent: Ocean #2E9CCB (dark #1F7EA8, deep #0D2731). One accent.
- Coins: only scene v07 uses a list (coins 01–07 for the seven rebuilt apps). Other scenes: no coins.
- Speaker: grey sweatshirt, green glasses, plain apartment background. Source is 1080x1920 un-mirrored; face centre ≈ x 50 %, y 42–45 % of frame height (eyes ~41 %, chin ~65 %). Crop the speaker card so the face is centred — check every card on your check sheet.
- Recurring objects in this reel: the black **agent puck** (= REA / the coding agent), dark **app cards** (`--brand-deep`) for "an app", light UI cards, black terminal/stat pills, dotted paths. Keep them looking identical across scenes (copy from v01_hook.html / v02_skills.html).
- Real data you may show (verified 2026-10-11): morluto/rea — "Reverse engineer anything with agents, from app behavior down to native binaries." ★ 100.8k stars, 22.2k forks, MIT. Install command: `npx rea-agents@latest setup`. GitHub Trending (today): morluto/rea #1, "25,585 stars today". REA's own step names (rea.tools): "Decode branches", "Trace calls", "Recover the rule". The 7 Adobe rebuilds (github.com/storytold, Rust, clean-room): PhotoCraft (photocraft, 47.2k ★), VectorCraft, FilmCraft, LightCraft, PdfCraft, EffectCraft, DesignCraft. EXCEPTION (user request): v07 shows the REAL Adobe app icons (official SVGs in hf/assets/adobe_*.svg) next to each Craft app — never redraw them. Never draw any brand logo (GitHub, Adobe, Claude, OpenAI…) — tool names as plain text pills.
- Words: on-screen words = words.txt only (exception: the opening text hook in v01, which the user wrote). Never put the word "softwares" on screen.

## V2 UPDATE (2026-10-11) — supersedes the Type section and the speaker-card sizes above

**Type system v2 — Inter Tight + Inter (both OFL, in hf/fonts/, declared at the end of hf/brand.css).**
Newsreader, Fraunces and Geist are retired for this reel (Geist Mono may stay for code/terminal text).
- Kinetic phrases: **Inter Tight 900**, letter-spacing −0.045em on hero words, −0.03em on supporting words, line-height ~0.88. Supporting/connective words: Inter Tight 700–800, smaller. Case as spoken (lowercase except proper nouns / sentence-start where it already was).
- **Accent = colour, not italics.** Key words in `--brand-primary`; the other hero words ink. NO italics anywhere. Emphasis comes from size contrast + weight + colour, still collage-staggered (lines offset left/right, sizes varying).
- Inter Tight is wider than the old serif: re-fit every hero word to the zone width (≤ 900 px incl. overshoot). Hero floor 170 px; supporting ≥ 84; smallest connective ≥ 64.
- Labels, pills, repo slugs, URLs, UI text, stat pills, chip names: **Inter 500/600** (was Geist).
- Keep ornaments: ocean underlines, strike-throughs, dotted ellipses/paths.
- Font assert: `document.fonts.check` for "900 100px 'Inter Tight'", "700 100px 'Inter Tight'", "500 40px Inter", "600 40px Inter" (+ Geist Mono if you use it). A fallback face is a failed scene.

**Speaker cards v2 — show more of him.**
- New **portrait hero card** for face-first beats: ~800–860 px wide x ~960–1100 px tall, radius 34, gentler tilt (rotateY ±4–6°, rotateX ~3°), same accent edge + shadow + sheen + float. Crop shows the full head + shoulders + some sweatshirt (no hair cut off): face centre ≈ 40 % of the card height.
- Kinetic words may sit OVER the lower part of a portrait card (over his light-grey sweatshirt) — ink and ocean read there; add a soft paper-coloured glow behind the text (`text-shadow: 0 0 28px rgba(228,222,217,.95), 0 0 6px rgba(228,222,217,.9)`) so it always reads. Never over his face.
- Elsewhere: secondary cards ≥ 600 px wide, small cards ≥ 420 px wide (were 560 / 330) where the layout allows.
