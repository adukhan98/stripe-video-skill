# adnaan-reel style — the binding art direction

This is Adnaan's house style. Every edit made with this skill must look like it belongs to the same
series as the approved reference reel. **Look before you build:**

- `assets/style/v3_contact_sheet.jpg` — ten frames of the current approved reel (reel-04, v2: the canonical look)
- `assets/style/v3_*.jpg` — the same frames full size
- `examples/reel-04/*.html` — the twelve scene compositions that produced it (pre-runtime code: study for the
  *ideas* of the bespoke objects; the shared parts are now `templates/runtime/`)
- `assets/style/v2_*` + `examples/reel-03/` — the earlier **editorial** variant (serif type, landscape cards);
  still valid component code (coins, slabs, browser cards, puck), but its type and card sizes are superseded

The look in one line: **soft, tactile, modern — a grey paper world where heavy kinetic grotesk type and
soft 3D objects explain what the speaker says, and the speaker floats in as a tilted video card — big
and portrait whenever he is the subject.**

## The runtime is the style (v3)

`templates/runtime/paper.css` + `paper.js` implement everything in this file that is the same in every scene:
the world, the three speaker-card presets (face crop from one `data-face`), the kinetic type system and its
four entrances, exits, floats, and the primitives (coins, pills, chips, UI/browser/terminal cards, agent puck,
dotted paths, cursor) with Lasseter's principles built into every move (`references/animation-principles.md`).
`slots.py prepare` installs it into each scene with a per-type starter (`templates/scenes/`); scenes contain
only copy, positions and one bespoke hero object. **To restyle a whole reel** (a new font, a card size, an
easing): edit the runtime, `scenes.py runtime --edit-dir E`, `scenes.py rerender --edit-dir E` — minutes, not a
rebuild. Scene agents never edit or re-implement the runtime; a finished scene that hand-rolls its own card or
word entrance is rejected. The sizes and rules below still bind the parts the agent chooses.

## Canvas and scene type

- 1080x1920 @30 (landscape deliveries: 1920x1080, see SKILL.md). Every beat of the reel is a
  **FULL-SCREEN OPAQUE SCENE** (slot layout `scene`): the paper background covers the whole frame on
  every frame, first and last included. Scenes cut hard into each other. The raw footage is never shown
  full-bleed — the speaker appears only as the embedded `hf/assets/speaker.mp4`: inside a card, or filling
  the frame in a planned `fullscreen` scene (see Objects); the other non-paper type is the `demo` recording.
- **Background, identical in every scene** (so cuts feel like one world):
  `#E4DED9` paper + 60 px grid lines `rgba(20,20,20,.055)` 1.5 px + vignette
  `radial-gradient(ellipse at 50% 45%, transparent 45%, rgba(90,80,72,.22) 100%)`.
  The grid drifts slowly (~20 px over the scene, linear) so the background is never dead.
- **Safe zone**: all important content inside x 60–960, y 285–1480. There are **no subtitles** — the
  kinetic phrases are the captions, so the whole zone is usable down to y 1480.

## Palette (brand.css tokens only — never hard-code hex in a scene)

| Token | Default (Ocean) | Role |
|---|---|---|
| `--brand-background` | `#E4DED9` | grey paper — every scene |
| `--brand-card` | `#FBFAF8` | soft UI cards, coins |
| `--brand-text` | `#141414` | ink: kinetic phrases, labels, black pills, agent puck |
| `--brand-primary` | `#2E9CCB` | THE accent: key words, active coin, speaker-card edge, checks |
| `--brand-primary-dark` | `#1F7EA8` | accent gradient bottom, pressed states |
| `--brand-deep` | `#0D2731` | hero / "picked" / "after" UI cards |
| `--brand-muted` | `#8E8780` | small Inter labels, repo slugs, URLs |

- **One accent only.** Accent on 1–2 key words per phrase, the active coin, ticks, progress.
- Accent presets (pick with `scenes.py init-brand --accent <name>`): ocean (default), cobalt, terracotta,
  lilac, mustard, blush, olive, red, mint — see `assets/style/accent_options.jpg`. Paper, ink and card
  never change. A brand-specific video may use the brand's colour as `--accent "#hex"`.
- Off-palette colour is allowed only when it is the real thing (a red REC dot, a real logo, a real page).

## Type (v2 default — Inter Tight + Inter)

Bundled in `assets/fonts/` (OFL): `InterTight-Variable.ttf`, `Inter-Variable.ttf`, `GeistMono-Medium.ttf`.
`scenes.py init-brand` installs them and brand.css declares them (variable weight ranges).

- **Kinetic phrases** (the captions): **Inter Tight 900** for hero words, **800/700** for supporting and
  connective words. Letter-spacing −0.045em on hero words, −0.03em on supporting, line-height ~0.88.
  Case as spoken (lowercase except proper nouns / sentence starts).
- **Accent = colour, never italics.** Key words in `--brand-primary`, the other hero words ink. Emphasis
  comes from size contrast + weight + colour. No italics anywhere.
- **Sizes — big**: hero words 170–270 px (fit each to ≤ 900 px wide *including overshoot* — Inter Tight
  is wide; measure, don't guess), supporting 84–130, smallest connective ≥ 64. A phrase stack spans most
  of the zone width. Never leave the lower 40 % of the zone empty for long.
- Words in a phrase **stack as a staggered collage**: lines offset left/right, sizes varying per word
  (see `v3_01`, `v3_04`, `v3_08`). Never a centred block of equal-size text.
- **Every on-screen word must be a word the speaker actually says** (from `words.txt`), with ASR
  spelling fixed (brand and product names). You may omit filler words; you may not paraphrase.
  Exceptions: `&` for a spoken "and" in a title-like phrase, and a **text hook** the user wrote (see below).
- Labels, pills, numbers, repo slugs, URLs, UI text, chip names: **Inter 500/600**. Code / terminal: Geist Mono.
  Use drawn SVG icons for ✓ ✗ ⚠.
- **Text over a speaker card** (portrait cards): only over his chest/clothes, never over the face, with a
  paper glow so it always reads: `text-shadow: 0 0 28px rgba(228,222,217,.95), 0 0 6px rgba(228,222,217,.9)`.
- Assert the fonts before anything renders (`document.fonts.check` for "900 100px 'Inter Tight'",
  "800 100px 'Inter Tight'", "500 40px Inter", "600 40px Inter", + Geist Mono if used) — a fallback face
  is a failed scene. Also declare the @font-face rules inside index.html (copy them from brand.css): the
  renderer's font guard can flag a family declared only in the linked stylesheet.
- **Text hook** (optional, user-written): a short headline readable on **frame 0** (it is the thumbnail)
  at the top of the hook scene, staying the whole scene — Inter Tight 900, one word in accent with a
  hand-drawn underline, staggered over 2–3 lines (see `examples/reel-04/v01_hook.html`).
- **Editorial variant** (`init-brand --type editorial`): Newsreader 600 + Fraunces 700 *italic* accent
  + Geist labels, as in reel-03 — only when he asks for the serif look.

## Objects (soft — no outlines, no hard offset shadows)

- **Full-screen speaker** (`.spk.full`, scene type `fullscreen`): he fills the frame edge to edge — no card,
  no tilt, no accent edge, only a slow push (1.0→1.03); kinetic words land low (y ≥ 1400) on his chest with
  the paper glow, optional `.paper-strip` behind them if the background is busy; **nothing else on screen**
  (one small object only if the brief names it). It is the minimal beat: for the hook, a verdict, the
  wrap-up or the CTA — chosen per beat (2–4 per reel, never adjacent, never default). A portrait card can
  also grow into it mid-scene on the hero word (`P.growFull`).
- **Speaker card**: the live speaker video in a rounded card, 3D tilt (perspective ~1600 px), accent edge
  underneath (`box-shadow: 0 16px 0 -2px var(--brand-primary), 0 50px 70px -10px rgba(40,30,20,.35)`),
  a light sheen sweep as it lands, slow float. Never a circle. Three sizes:
  - **Portrait hero** (~740–840 wide x ~810–1070 tall, radius 34, rotateY ±4–6°, rotateX ~3°): for the
    hook and every beat where *he* is the subject — opinions, verdicts, the wrap-up, the CTA. Shows the
    **full head (no hair cut) + shoulders + some chest**, face centre ≈ 35–42 % down the card; the kinetic
    words land on his chest and the paper below (examples/reel-04 v01, v08, v11, v12).
  - **Secondary** (landscape, ≥ 600 px wide, radius 30): item / product scenes, tucked over a browser card.
  - **Small** (≥ 420 px wide): explainer scenes where the graphic is the hero.
  **Crop to the face**: the video is 1080x1920 scaled to the card width; choose the vertical window so
  the whole head is in and the face centred; check the crop on your sheet. A landscape card cannot hold
  the full head at hero size — that is what portrait cards are for.
- **Coins**: white neumorphic discs `radial-gradient(circle at 35% 30%, #fff, #F1EEEA 70%)`, shadow
  `0 18px 30px rgba(60,50,40,.22)`, Inter 600 numbers, four tiny tick marks. Active coin = accent gradient.
  Coins are the **continuity object** for any list (01…N): they appear in the hook, each item's scene
  features its coin, the wrap-up orbits them, the CTA stacks them.
- **UI cards**: `--brand-card`, radius 24–28, soft shadow `0 30px 50px -12px rgba(60,50,40,.30)`,
  grey wireframe bars `#E5E0DA`. "Picked"/"after" cards flip to `--brand-deep` with accent details.
- **Browser card** (real pages): rounded, light chrome bar with three grey dots and the URL in Inter
  muted, slight tilt, slow internal scroll of the captured page. Never full-bleed, never flat.
- **Black pills**: `--brand-text` rounded pills with white Inter 600 text — notifications, stat pills
  ("★ 94.5k on GitHub"), labels ("</> my codebase", "→ your inbox"). Stack them like notifications.
- **Agent puck**: black disc with a simple robot face (two accent eye-dots), glows/bobs when fed.
- **Dotted paths**: ink 3 px, dasharray "2 12", round caps, drawn on with strokeDashoffset; things
  ride them (cards into the puck, a line from the CTA word down to the speaker card).
- **Cursor**: white arrow with ink stroke, moves on eased arcs, clicks with a quick scale dip.
- **Real things over abstractions**: real pages, repos, star counts, file headings, product names.
  Illustrative UI (wireframes, checklists) is fine; invented numbers or quotes are not.
- **Every named tool or company shows its official logo** as an `<img>` (`.chip img`, a pill, or on an app
  card), fetched with `fetch.py logo` (logged `official`) or from a press-kit file he supplies. Never drawn,
  recoloured, cropped into a different shape or replaced by a text-only pill when a logo exists. Monochrome
  Simple Icons marks are acceptable when no colour icon exists; the brand's own app icon is preferred.

## Motion

- Entrances: rise 40–110 px + fade + blur(6–10px→0) + scale 0.55–0.94→1, `power3.out` /
  `back.out(1.4–2.2)`, 0.3–0.6 s. Hero words overshoot to ~106–112 % on their spoken word and settle.
- **Contact frame on the word**: start the entrance ~0.13–0.2 s before the word time in `words.txt`.
- Stagger siblings 2–4 frames. Groups exit bottom-up or as a quick blur-up (0.2–0.3 s) to make room.
- Continuous life: grid drift, slow camera push (1.0→~1.015–1.02, keep everything in the zone),
  2–4 px sine float on cards/coins, a 1 % punch on the scene's biggest word. **No dead holds.**
- One focal point at a time. Scenes hold alive into the hard cut — no exit animation needed.
- Measure your bounds: render-check every frame stays inside x 60–960, y 285–1480 including
  overshoots and the camera push; shrink the push before shrinking the type. (HyperFrames still draws a
  video inside a hidden container — remove the video, don't just hide it, when rendering a background-only
  reference for bounds.)
- **Exact length**: a scene is EXACTLY the frame count in its TASK.md (data-duration is preset to
  `(frames − 0.5) / fps` because the renderer rounds up). One frame short leaves a gap at the cut; one over
  overlaps the next scene. `slots.py check` fails on any other count.


## Project specifics (edit per project)

- Reel: "the most in-demand AI job of 2027" — the forward deployed engineer (FDE): AI is getting good at business/knowledge work, companies will want it in every department at once, somebody has to understand the work, hook the AI up to the company's systems and make sure it works. Anthropic committed $100M to train 10,000 by end of 2027; Salesforce tripled its FDE team in six months; we'll run out of people; domain experts should lock in and learn. CTA: comment "FDE" → roadmap.
- Accent: Ocean #2E9CCB (dark #1F7EA8, deep #0D2731). One accent.
- List / coins: none. Do NOT reach for coins. Recurring objects in this reel: soft UI cards (job posting, work cards, system cards), black pills, the agent puck ONLY in v07, dotted paths.
- Speaker: NAVY-BLUE sweatshirt, beard, plain apartment (ceiling light above his head). Source is 1080x1920 un-mirrored; face centre ≈ x 50 %, **y 47 % of frame height** (hair top ~27 %, eyes ~44 %, chin ~64 %) → set `<body data-face="0.47">`. Check the crop on your sheet: full head incl. hair, no ceiling lamp dominating.
- Text over his chest: the sweatshirt is DARK navy — ink and ocean words read badly on it. Over a card/full-screen chest use the `.paper-strip` behind the phrase or the strong paper glow; prefer landing the big kinetic words on paper below/beside the card.
- Real data you may show (verified 2026-10-12): Claude Frontier Academy (claude.com/programs/frontier-academy, announced Oct 2 2026) — page stats "$100M initial investment", "10,000 Frontier Deployed Engineers by the end of 2027". Salesforce newsroom article "How Forward Deployed Engineers Are Proving AI Makes Tech Jobs More Human" (salesforce.com/news, March 18 2026) — Salesforce says it tripled its FDE team in six months. No other numbers anywhere: charts/gauges in this reel are unlabelled (no axis numbers, no percentages).
- Logos: official files only (hf/assets/anthropic.png, claude.png, salesforce.png) as <img>, never redrawn/recoloured. Only v09 (Anthropic + Claude) and v10 (Salesforce) name companies.
- Words: on-screen words = words.txt only (exception: the v01 text hook the user wrote). The acronym is always "FDE" (plural "FDEs").
