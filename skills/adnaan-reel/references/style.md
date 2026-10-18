# adnaan-reel style — the binding art direction

This is Adnaan's house style. Every edit made with this skill must look like it belongs to the same
series as the approved reference. **Look before you build** — which reference depends on the reel's LOOK
(`brand/brand.json` → `"look"`, set by `scenes.py init-brand --look`):

- **`mint` — v7, THE HOUSE DEFAULT since 2026-10-17**: `assets/style/v8_contact_sheet.jpg` + `examples/reel-08-v7/`
  (the approved reel-08 style test). Rules: the "v7" section right below. Where v7 is silent, the v6 sound rules, the
  safe zones, the readability rules, the type sizes and the motion principles below still apply.
- **`paper` — legacy v6 (reel-06/07)**: `assets/style/v7_contact_sheet.jpg` (reel-07, three-mode system) and
  `assets/style/v6_contact_sheet.jpg` (reel-06, paper + marker); `examples/reel-06/`, `examples/reel-07/`. Only when he
  asks for the red paper look.
- Older idea banks: `assets/style/v3_*` + `examples/reel-04/`, `reel-05/`; editorial serif: `assets/style/v2_*` + `examples/reel-03/`.

## v7 — the MINT look (house default; Adnaan's restyle from two reference reels, 2026-10-17)

He liked two reels more than the red paper style: one where the creator is full-screen with type around and *behind* her,
and one (gregisenberg) with a grey board, white glyphs in mint/charcoal discs on a chain, the camera travelling, clean flat
vector props and no hand-drawn anything. Decided with him, item by item:

**Two modes (the old split band and the marker are gone):**
- **TALK** — him full-screen (`talk` starter, `.spk.full`). **Our kinetic captions stay** (Inter Tight 900 phrases on their
  words, collage-staggered, hero 170–270 authored; NOT continuous subtitles): charcoal ink with a soft light glow (`.g7`);
  mint (`.ocean`) only on 1 hero word at hero size — mint gets a soft dark shadow (it washes out on light clothing).
  Dark clothing that reel → white (`.w7`). Words low on his chest (y ~1150–1470) or beside his head; never over his face.
  Usually captions only; occasionally ONE icon disc. No pills. No fake punch-ins / angle changes.
- **VISUAL** — no speaker (`visual` starter): our paper + grid with a much **stronger vignette** (`V.board()`), a world layer
  bigger than the frame and a **camera that travels** across it (one move per sentence; x and y on different eases = an arc;
  hard cuts between scenes). 1–2 full-bleed **mint panels** per reel as punctuation.
- **Presence**: about **50 %** of the reel is him (TALK) — the same presence as before, now full-screen. No Visual stretch
  longer than ~8 s without him. A **small card** of him (rounded portrait ~360×460, mint ring, LEFT side only, never in the
  IG corner) is allowed **0–2 times per reel**, while a visual needs him visibly present (`card` starter).
- **Depth ("behind me")**: footage → objects → his matte → words (`talk_depth`, `cut-speaker` makes the matte). Approved on
  the reel-08 hook (CEO photo cards slide out from behind his head). Never cover his face; text that must stay readable
  goes in front.

**The signature transition** (1–3 per reel): his full-screen footage shrinks into the board (`V.shrink`): into the
**chain disc** of the current item when the reel has a chain, otherwise into the **small card**; `V.grow` brings him back
full-screen for the payoff line. Anticipation dip, clip morphs frame → rounded → circle/card, arc, overshoot on landing,
the board + vignette fade up around him, a mint ring draws on.

**List continuity = the disc chain** (replaces circled ①②③ / coins): one icon disc per item, joined by a thin 4 px charcoal
line (`V.chain`): the current item mint, the rest charcoal. Chapters open by travelling to their disc; the CTA pulls back to
the whole chain. Key-point reels get a 2–3 disc chain; story / opinion reels get none. Fixed geometry + icons per reel in
SHARED.md "Project specifics"; a scene after a chain scene opens on its exact end state (`scenes.py seam`).

**Look:**
- Palette (brand.css, `init-brand --look mint`): mint `#7CC49E` (`--brand-primary`), deep mint `#2F8A63` (small accents,
  highlighter edge), charcoal `#2B2B2B` (`--brand-deep`, ink discs/cards), ink `#232323`, `--mint-soft` highlighter,
  `--mint-panel`, **peach `#F2A07B` = data only** (charts, result bars, rolling numbers). **No red anywhere.**
- Fonts: Inter Tight 900 + Inter, as before. No serif, no Caveat.
- **No hand-drawn marker layer.** Lines that draw themselves are clean vector strokes (even width, round caps, no boil).
- **Icon discs**: white Phosphor FILL glyphs (MIT; `fetch.py icon <name>`) masked into a mint or charcoal disc with the soft
  disc shadow (`V.disc`, `V.discIn`: anticipation + overshoot, glyph 2 f later). Official logos stay official (`<img>`).
- **Hero objects are flat vector illustrations** (flat palette fills, soft shadows, simple flat characters) with the same
  personality in motion as before (anticipation, overshoot, squash, secondary action).
- **Real pages** stay big readable cards/strips by default (≥ 0.85, highlighter behind the spoken phrase — `.v7-hl`, mint);
  phone or polaroid mockups only sometimes.

**Unchanged from v6**: the frame-0 text hook (mint key word, a clean solid underline bar instead of the marker), the sound
rules (30 % rule, low & warm kit, ducked music bed), the IG safe zones, the readability rules, the beat-table approval.

## v6 — Adnaan's SOP (reel-07, 2026-10-15) — the PAPER look; its sound, safe-zone and layout guidelines also bind v7

Core philosophy (his words): *high retention through clean editorial design, bold kinetic typography and vocal clarity —
modern, spacious, intentional; the audio supports the voiceover, never competes with it.* What stays exactly as is: the
grey paper + grid (he chose to keep it), bold black + red kinetic type, the red marker layer and the **sketchbook doodles**
(chalkboard, target, mountain, robot, stick figures, tall progress bar — he loves them; they are the signature). What
changes is how HE appears, how much is on screen at once, where things sit, and the sound.

**The three-mode system — every beat of the beat table picks one (column "Mode"):**
- **Mode A — split (primary talking layout).** `.spk.split` — his footage edge to edge in the TOP half (y 0–960; no border,
  radius, shadow, tilt or float; face centred). The paper below is the stage: kinetic words + one doodle/card in the
  band **y 1000–1480**. Use for the hook, transitions, punchlines, his opinions/verdicts, the CTA.
- **Mode B — full canvas.** No speaker: doodles, kinetic type, UI cards and real-page strips own the whole zone. Use when
  explaining a framework, a step-by-step, a diagram, an example.
- **Mode C — emphasis.** `.spk.full` for a 1–2 s punch (a hero line), OR `.spk.cutout` + `speaker_cut.webm` (his
  background removed with `hyperframes remove-background`) standing on the bottom edge in front of a big article /
  screenshot card.
- Switch modes INSIDE a scene on a sentence boundary with `P.splitIn / splitOut / fullToSplit / splitToFull` — a mode
  change is a structural beat (it may carry a soft whoosh).
- **Floating speaker cards** (portrait / secondary / small) are allowed but **rare: 0–2 per reel**, only where presence
  matters and the graphic needs most of the frame. Never the default, never in a corner by reflex.
- Speaker absence: Mode B stretches are fine while a framework is explained; bring him back (Mode A) on the payoff line —
  avoid > ~12 s without him.

**Layout guidelines (content-dependent — judgement, not hard gates):**
- **Two-element guideline**: about two things competing for attention at once (speaker + text, doodle + text, card + text).
  Cut decorative extras that compete; a richer moment is fine when the content needs it.
- **White space**: leave roughly 35–50 % of the grid empty so it reads high-end on a phone.

**IG Reels safe zones (binding):** nothing important in the bottom 20 % (below y 1536 — the house zone already stops at
1480) and **nothing in the lower-right corner below y 1200 right of x 900** (Like/Comment/Share). CTAs and pills sit
bottom-left/centre.

**Sound — the 30 % rule (binding):** no Mickey-Mousing. 0:00–0:04 gets 1–2 punchy tactile sounds (stamp, clunk) with
space between them; after that only structural transitions (point 1/2/3, a mode switch, a big screenshot sliding in, the
CTA landing) — ~10–14 cues in a 70 s reel. Palette low & warm (v6 kit: thud, stamp, clunk, paper slide, soft whoosh, warm
pop), low-passed at 5 kHz. No dings, alarms, ticking clocks, typewriter rattles, marker squeaks, rising whistles.
**Mix:** voice is king (peaks ≈ −3…−6 dB), SFX −16…−22 dB, music bed −22…−26 dB under speech (ducked), +2–3 dB over the
final 3 s for the CTA lift. Music is now part of the default (ElevenLabs Music, instrumental, timed to the beats).

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

**v5: `marker.js` + `marker.css` are part of the runtime** (the hand-drawn layer — see "The marker layer" below);
every starter inits it (`const M = Marker.init(P)`), Caveat is a bundled font.

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
- **Safe zone (absolute)**: EVERYTHING — type incl. descenders and overshoot, cards incl. rotated corners,
  logos, notes, marker strokes — inside x 60–960, y 285–1480 on every frame, incl. the camera push. Measured
  (diff every frame against a background-only render), never eyeballed. There are **no subtitles** — the
  kinetic phrases are the captions ("dynamic captions" in his words), so the whole zone is usable down to y 1480.

## Palette (brand.css tokens only — never hard-code hex in a scene)

| Token | Default (Red) | Role |
|---|---|---|
| `--brand-background` | `#E4DED9` | grey paper — every scene |
| `--brand-card` | `#FBFAF8` | soft UI cards, coins |
| `--brand-text` | `#141414` | ink: kinetic phrases, labels, black pills, agent puck |
| `--brand-primary` | `#E5484D` | THE accent: key words, the marker, speaker-card edge, checks |
| `--brand-primary-dark` | `#C7353A` | handwriting in accent (contrast on paper), pressed states |
| `--brand-deep` | `#1A1A1A` | hero / "picked" / "after" UI cards, terminal |
| `--brand-muted` | `#8E8780` | small Inter labels, repo slugs, URLs |

- **One accent only.** Accent on 1–2 key words per phrase, the active coin, ticks, progress.
- Accent presets (pick with `scenes.py init-brand --accent <name>`): **red (house default since v5 / reel-06)**,
  ocean (v2–v4 default), cobalt, terracotta, lilac, mustard, blush, olive, mint — see `assets/style/accent_options.jpg`. Paper, ink and card
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
  is wide; measure, don't guess), supporting 84–130, smallest connective ≥ 64. These are the authored
  `data-size` values; `--type-scale` (house **0.94** since reel-05 — he asked for the text "a tiny bit smaller",
  written to brand.css by `init-brand`) scales every kinetic line at layout, so on screen they read ~160–254 /
  79–122 / ≥ 60. A whole-reel nudge is one line in brand.css + `scenes.py runtime` + `rerender`; inline sizes an
  agent adds must be in em so the scale reaches them. A phrase stack spans most
  of the zone width. Never leave the lower 40 % of the zone empty for long.
- Words in a phrase **stack as a staggered collage**: lines offset left/right, sizes varying per word
  (see `v3_01`, `v3_04`, `v3_08`). Never a centred block of equal-size text.
- **Every on-screen word must be a word the speaker actually says** (from `words.txt`), with ASR
  spelling fixed (brand and product names). You may omit filler words; you may not paraphrase.
  Exceptions: `&` for a spoken "and" in a title-like phrase, and a **text hook** the user wrote (see below).
- Labels, pills, numbers, repo slugs, URLs, UI text, chip names: **Inter 500/600**. Code / terminal: Geist Mono.
  Use drawn SVG icons for ✓ ✗ ⚠.
- **Text over a speaker card** (portrait cards): only over his chest/clothes, never over the face, and on
  SOLID light paper — a `.paper-strip` / soft paper panel that is opaque where the words sit (the paper glow alone is
  not enough over dark clothing; reel-06 fixed every full-screen beat this way). Glow: `text-shadow: 0 0 28px
  rgba(228,222,217,.95), 0 0 6px rgba(228,222,217,.9)`.
- Assert the fonts before anything renders (`document.fonts.check` for "900 100px 'Inter Tight'",
  "800 100px 'Inter Tight'", "500 40px Inter", "600 40px Inter", + Geist Mono if used) — a fallback face
  is a failed scene. Also declare the @font-face rules inside index.html (copy them from brand.css): the
  renderer's font guard can flag a family declared only in the linked stylesheet.
- **Frame 0 is the thumbnail — finished, true content only** (reel-07: a split-flap showed a random "7254" on frame 0): no transient values (odometers, split-flaps, counters start BLANK or on their real value), nothing mid-entrance, no half-drawn strokes in the hook text; check `frame-00` of your snapshot before rendering.
- **Text hook** (optional, user-written): a short headline readable on **frame 0** (it is the thumbnail)
  at the top of the hook scene, staying the whole scene — Inter Tight 900, one word in accent with a
  hand-drawn underline, staggered over 2–3 lines (see `examples/reel-04/v01_hook.html`).
- **Editorial variant** (`init-brand --type editorial`): Newsreader 600 + Fraunces 700 *italic* accent
  + Geist labels, as in reel-03 — only when he asks for the serif look.

## The marker layer (v5 — PAPER LOOK ONLY; v7 mint has no marker — `hf/marker.js`, read its header)

The hand-drawn layer is what makes the house look feel made by a person. **Every paper scene uses it**, on top of
(never instead of) the kinetic type and the soft objects:

- **Red felt-tip** (`--marker` = accent) for emphasis: a loose loop around the hero number/word, a (double) wobbly
  underline, an arrow that flicks its head after the shaft, a strike, ✗ / ✓, sparkle ticks on a stamp. **Black
  felt-tip** (`ink`) for drawings: diagrams, doodles, stick people, clocks, doors, globes. **Grey pencil** only for
  hatch fills, never for words.
- **Drawn ON the spoken word** (stroke starts ~0.15 s before), loops 0.3–0.45 s, underlines 0.2–0.3 s, then the line
  **boils** (3 seeded variants on fours) to the cut — held drawings are alive. Stroke width 8–14 px, felt-tip edge.
- **Doodles that act out the sentence**, built from `M.line` / `M.circle` / `M.hatch` (crown on a search bar for
  "glorified", a price tag swinging for "free", a calendar struck through collapsing into a clock for "weeks → hours",
  a magnifier that really magnifies, a sunrise behind his card for "early", a padlock snapping shut on "lock").
- **Handwritten notes** (`M.note`, Caveat 700): ≤ 4 words, ≥ 60 px (80+ when they label a chart), ink or dark accent,
  written on left→right. Only spoken words or real labels from the real source ("6B", "~5,000").
- **Highlighter behind text** (`M.highlight(card, rect)`, multiply) on real pages/posts — never a loop across lines.
- **Tape** (`M.tape`) to stick polaroids, post cards and logo chips onto the paper.
- **Recurring diagrams** (the reel-06 funnel): one fixed geometry + seeds in SHARED.md, the first scene draws it,
  later scenes open with it ALREADY drawn in the previous scene's final state (copy its code) and add their part —
  check every such cut with `scenes.py seam A B`.
- Marker strokes and doodles never cross text or the face; they sit beside them, on the card edge, or behind.

## Readability (binding — he asked for this explicitly; a scene fails review on any of these)

- **Real pages / posts are READABLE**: capture them with `capture.py --readable` (light mode, narrow @3x) and show
  ONE strip of 2–6 lines at a time at **≥ 0.85 scale (card ≥ 815 px wide, text ≈ 40–45 px)** — never a whole page
  shrunk into a thumbnail. The spoken number/phrase gets the highlighter.
- **No semi-transparent text.** A word is fully readable or gone (exit it in ~6 f). Stage focus by receding/dimming
  OBJECTS (cards, diagrams), never words; no ghosted half-faded lines lingering under the next phrase.
- Kinetic hero ≥ 170 authored, nothing under 64; handwriting ≥ 60; logos in chips ≥ 56 px; UI cards, chips,
  stickers, doodles big enough to read on a phone (reel-06 scaled most of them 1.3–1.6× after the first pass).
- High contrast only: ink or accent on paper; words over his clothing on solid paper.
- Lower 40 % of the zone never empty for long; no big empty band between a card and the words.

## Objects (soft — no outlines, no hard offset shadows)

- **Full-screen speaker** (`.spk.full`, scene type `fullscreen`): he fills the frame edge to edge — no card,
  no tilt, no accent edge, only a slow push (1.0→1.03); kinetic words land low (y ≥ 1400) on his chest with
  the paper glow, optional `.paper-strip` behind them if the background is busy; **nothing else on screen**
  (one small object only if the brief names it). It is the minimal beat: for the hook, a verdict, the
  wrap-up or the CTA — chosen per beat (2–4 per reel, never adjacent, never default). A portrait card can
  also grow into it mid-scene on the hero word (`P.growFull`).
- **v6: Mode A split band** (`.spk.split`, data-h 960) is the primary way he appears; **Mode C cutout** (`.spk.cutout`)
  stands him on the bottom edge in front of a big page. The card presets below are now the RARE option (0–2 per reel).
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
- **Real things over abstractions**: real pages, repos, star counts, file headings, product names, real
  photos of named people (`fetch.py photo`, in a polaroid / taped print). Illustrative UI (wireframes,
  checklists) is fine; invented numbers or quotes are not. Never AI-generated pictures, never a stand-in
  logo or an old version, never a watermarked file; icons ≥ 512 px, pictures ≥ 800 px wide; a borrowed clip
  once per reel, frozen on its moment before it cuts off-topic; pages cropped to the phrase, never shrunk
  whole; no cookie dialogs accepted in captures; a face the audience would not recognise is replaced by the
  person's work; product UI is the current version (upload date checked); a quoted post is verified against
  its real text (`fetch.py tweet --check`).
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
- **Richness (house level since reel-05, tempered by v6's two-element guideline)**: a hero object plus 1–3 secondary
  micro-animations that act out the sentence — but only one focal pair competes at a time and 35–50 % of the grid stays
  empty; cut what only decorates. Previously:
  sentence — `references/motion-ideas.md` is the idea bank (cursor that does the thing, real numbers rolling to
  their value, icons that come alive, soft physics, characters with personality, type that performs, hero icons
  landing on their word). A scene may use its own soft spotlight vignette for staging (flashcheck tolerates it).
- **Sound (v6, the 30 % rule)**: the motion stays rich, the SOUND does not follow every move. `beats.json` still lists the
  contact frames, but only beats tagged `"role": "hook"` (≤ 2 in 0–4 s) or `"role": "structural"` with a v6 tag
  (`stamp thud clunk paper whoosh pop`) make a sound; everything else moves silently. No `scribble` beats.
- Measure your bounds: render-check every frame stays inside x 60–960, y 285–1480 including
  overshoots and the camera push; shrink the push before shrinking the type. (HyperFrames still draws a
  video inside a hidden container — remove the video, don't just hide it, when rendering a background-only
  reference for bounds.)
- **Exact length**: a scene is EXACTLY the frame count in its TASK.md (data-duration is preset to
  `(frames − 0.5) / fps` because the renderer rounds up). One frame short leaves a gap at the cut; one over
  overlaps the next scene. `slots.py check` fails on any other count.
