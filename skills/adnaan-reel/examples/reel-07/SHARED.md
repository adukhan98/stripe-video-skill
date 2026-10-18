# adnaan-reel style — the binding art direction

This is Adnaan's house style. Every edit made with this skill must look like it belongs to the same
series as the approved reference reel. **Look before you build:**

- `assets/style/v6_contact_sheet.jpg` — twelve frames of the current approved reel (**reel-06 "the AI funnel",
  v5: the canonical look** — he: "I love this edit, every part of it … I want all other reels to be like this")
- `assets/style/v6_*.jpg` — the same frames full size
- `examples/reel-06/*.html` — the fourteen scene compositions that produced it, on the v5 runtime (paper + marker),
  with their `beats.json` and NOTES (key poses, principles, deviations). Study them for the ideas AND the rules.
- `assets/style/v3_*` + `examples/reel-04/`, `examples/reel-05/` — the earlier v3/v4 reels (same world and type,
  no marker layer, Ocean accent): still good idea banks for bespoke objects
- `assets/style/v2_*` + `examples/reel-03/` — the earlier **editorial** variant (serif type, landscape cards);
  still valid component code (coins, slabs, browser cards, puck), but its type and card sizes are superseded

The look in one line: **soft, tactile, modern — a grey paper world where heavy kinetic grotesk type and
soft 3D objects explain what the speaker says, a RED felt-tip marker draws over everything by hand (loops,
underlines, arrows, hatch fills, doodles, handwritten notes — all boiling like hand animation), real pages appear
as big readable strips with a highlighter behind the spoken phrase, and the speaker floats in as a tilted video
card — big and portrait whenever he is the subject.**

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
- **Text hook** (optional, user-written): a short headline readable on **frame 0** (it is the thumbnail)
  at the top of the hook scene, staying the whole scene — Inter Tight 900, one word in accent with a
  hand-drawn underline, staggered over 2–3 lines (see `examples/reel-04/v01_hook.html`).
- **Editorial variant** (`init-brand --type editorial`): Newsreader 600 + Fraunces 700 *italic* accent
  + Geist labels, as in reel-03 — only when he asks for the serif look.

## The marker layer (v5 — `hf/marker.js`, read its header)

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
  whole; no cookie dialogs accepted in captures.
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
- **Richness (house level since reel-05)**: a hero object plus 2–3 secondary micro-animations that act out the
  sentence — `references/motion-ideas.md` is the idea bank (cursor that does the thing, real numbers rolling to
  their value, icons that come alive, soft physics, characters with personality, type that performs, hero icons
  landing on their word). A scene may use its own soft spotlight vignette for staging (flashcheck tolerates it).
- **Sound follows motion**: every contact frame worth hearing goes in the scene's `beats.json`
  (pop · tick · impact · riser · whoosh · ping · ding — the ElevenLabs house kit in `assets/sfx/` — plus
  **scribble** with a `dur` for every audible marker stroke: the felt-tip on paper sound), mixed well under the voice.
  `impact` only on the hero beat(s).
- Measure your bounds: render-check every frame stays inside x 60–960, y 285–1480 including
  overshoots and the camera push; shrink the push before shrinking the type. (HyperFrames still draws a
  video inside a hidden container — remove the video, don't just hide it, when rendering a background-only
  reference for bounds.)
- **Exact length**: a scene is EXACTLY the frame count in its TASK.md (data-duration is preset to
  `(frames − 0.5) / fps` because the renderer rounds up). One frame short leaves a gap at the cut; one over
  overlaps the next scene. `slots.py check` fails on any other count.



## Project specifics — reel-07 "be more ambitious" (Felix Rieseberg's article)

- **Reel**: In 1939 a student (George Dantzig — the ARTICLE names him; Adnaan never says the name) showed up late,
  copied two problems off the board thinking they were homework, solved both — they were two famous unsolved problems
  in statistics. He solved them because nobody told him it was impossible. That's how most of us use AI. Source: the
  article "How to be more ambitious: A tutorial for humans with models" by Felix, **an engineer working on Claude**
  (NO photo of Felix anywhere — Adnaan's decision). Three takeaways: (1) ask for the outcome, not the task (one slide →
  the whole deck to convince your boss); (2) set goals that sound unreasonable (10 s → don't ask for 5, ask for 200 ms
  and tell it to keep going); (3) don't let AI grade its own work (a test, a real number, a real scenario). Biggest
  takeaway: AI can do so much more than what most of us ask it for (emails, quick questions). You just need to ask.
  CTA: "Comment ambitious".
- **Accent: RED** #E5484D (dark #C7353A, deep #1A1A1A) — the runtime's accent class `.ocean` = red. One accent.
- **Text hook (v01 only, Adnaan wrote it)**: "How to be more ambitious with AI" — "ambitious" in red with a marker underline.
- **List continuity: the THREE MARKER-CIRCLED NUMBERS ①②③** (no coins, no puck, no dotted-path-into-puck). Drawn number =
  Inter Tight 900 digit ~210 px ink inside a red marker loop (`M.circle`, seeded). In chapter scenes (v07 ①, v10 ②,
  v13 ③) the active number sits TOP-LEFT: digit centre ≈ (190, 420), loop ≈ 260×260. v06 introduces all three.
- **Speaker**: NAVY hoodie (DARK clothing), beard, short dark hair, holds a small white lav-mic cable loop in his right
  hand at chest height; warm apartment, ceiling lamp, paper lantern left, shelf right. 1080x1920 un-mirrored. Face
  centre ≈ x 50 %, **y 41 % of frame height** (hair top ~21 %, eyes ~38 %, chin ~60 %) → `<body data-face="0.41">`.
  Check your sheet: whole head incl. hair in every card. Words over the hoodie MUST sit on a solid `.paper-strip`
  (paper glow alone fails on navy) — prefer landing big words on paper beside/below the card.
- **The marker layer** is house runtime (`hf/marker.js`, read its header: circle/underline/arrow/cross/check/strike/
  hatch/highlight/note/tape/line/erase). Red felt-tip for emphasis, black ink for drawings, grey pencil only for hatch.
  Strokes start ~0.15 s before their word, then boil. Strokes never cross text or his face.

### RECURRING DRAWING 1 — THE BOARD (v02 draws it, v03 opens with it already drawn — must not jump at the cut)
- A hand-drawn blackboard in BLACK ink (`M.line`, seed 701): outer frame rect (120,330)→(960,330)→(960,770)→(120,770)
  closed, a chalk ledge line (140,800)→(940,800). Inside, two scribbled "problems" written by hand (illustrative
  squiggle equations, NOT readable claims): problem 1 on y≈450 from x 240→820, problem 2 on y≈620 from x 240→760,
  labels "1." at (175,450) and "2." at (175,620) as Caveat ink 64 px (`M.note`). Seeds 711/712 for the squiggles.
- v02 final state: board + both problems + two RED ✓ (`M.check`, seeds 721/722) at (870,450) and (820,620).
- v03 copies v02's board code verbatim (`draw(0)` = drawn at t=0) and adds its own part. Run seam check A/B.

### RECURRING DRAWING 2 — THE GAUGE (v15 draws it, v16 opens with it already drawn)
- A tall hand-drawn bar in BLACK ink (seed 901): rounded rectangle x 680–840, y 340–1420 (corner radius ~70),
  6 tick marks on its LEFT edge at y 520, 700, 880, 1060, 1240 from x 650→680.
- TOP label: Caveat note "so much more" (ink, ≥ 72 px) written left of the bar top, its right end ≤ x 650, y ≈ 380. A small spark
  doodle (seed 905) above the bar at (760, 315) ONLY if it stays inside y ≥ 285.
- BOTTOM fill: RED marker hatch (`M.hatch`, seed 911) of the bar polygon y 1340–1420 = "what most of us ask it for";
  red-dark note "ask it for" left of it at y ≈ 1380.
- GAP brace: a curly brace in red (seed 921) on the RIGHT of the bar, x 860–920, from y 360 to y 1330.
- v16 opens with ALL of that already drawn (draw(0)), adds an envelope doodle + "?" speech-bubble doodle in the bottom
  sliver's left area (y 1180–1420, x 120–640), then on "further" the red hatch floods UPWARD to y 360 (hatch passes
  stacked, seeds 912–919) with a red arrow drawn up beside the bar; the brace erases as the gap closes.
- Left column x 80–620 is for kinetic type + the small speaker card in both scenes; keep the gauge fixed.

### READABILITY (binding — review fails on any)
- Safe zone absolute: every pixel inside **x 60–960, y 285–1480** for the whole scene incl. the push. Measure it.
- Article strips are 894 px wide with ~45 px serif text (light paper #F7F5F0 page colour, real page). Show them in a
  white card at **≥ 0.9 scale (≥ 805 px wide)**, ONE strip at a time, taped (`M.tape`) or in the browser card;
  highlight with `M.highlight` BEHIND the words (boxes below × your scale) — never a loop across lines.
- No semi-transparent text lingering; kinetic hero ≥ 170 authored, nothing under 64; notes ≥ 60 px, ≤ 4 words.
- Chips/logos ≥ 56 px, doodles phone-sized (reel-06 had to scale most doodles 1.3–1.6× — start big).

### Words on screen
- On-screen words = words.txt only, plus the v01 text hook. Real labels from the article are allowed as data:
  the article title, "13 October 2026", "8 min", "felixrieseberg.com", "I work on Claude.", the strips' own text.
- Spell: Claude, Felix. He says "a tutorial" (ASR heard "editorial"), "grade" (ASR "grid"), "200 milliseconds".
- Illustrative UI labels allowed: "10 s", "5 s", "200 ms" (he says these), "A+" on the self-graded test paper (v13),
  "fix" on a slide, slide wireframes. Never invent stats, quotes or a Felix photo.

### Real assets (in hf/assets/ when your slot lists them)
- `art_title.png` 894×598 — date + "How to be more ambitious: / A tutorial / for humans / with models" (serif title).
  Highlight "ambitious:" line = [0,116,509,144].
- `art_claude.png` 894×99 — "I work on Claude. It's an interesting". Highlight "I work on Claude" = [0,9,408,75].
- `art_dantzig.png` 894×604 — "Accomplish hard things by believing them to be possible: In 1939, George Dantzig showed
  up late to a statistics class at Berkeley, copied two problems off the blackboard, and handed in his solutions
  thinking they were homework. They were two unsolved". Highlight "copied two problems off the blackboard" ≈ line 4–5.
- `art_unsolved.png` 894×183 — "work. They were two unsolved / problems in statistics." Highlight = [220,9,578,75] + [66,93,513,75].
- `art_unreasonable.png` 894×183 — "• Pick unreasonable goals and tell the model that they're very reasonable…".
  Highlight = [66,9,809,75] + [66,93,493,75].
- `art_200ms.png` 894×267 — "You need your website to load in 5s instead of 10s? Ask for 200ms. Does…".
  Highlight "Ask for 200ms" = [660,93,174,75] + [66,177,157,75]; "5s instead of 10s" is on line 2 (y 93).
- `art_judge.png` 894×183 — "• Use an outside judge: Do not ask the model to judge itself. I assume". Highlight =
  [605,9,247,75] + [66,93,577,75]. All strips captured light-mode from the real page.
- `claude.png` — official Claude app icon (1024², coral square with the white spark; App Store, seller Anthropic PBC).
  Use as `<img>` in a white chip with "Claude" Inter 600. Never redrawn or recoloured.

### Sound
beats.json: house kit (pop/tick/impact/riser/whoosh/ping/ding) + `scribble` beats with `dur` for every audible marker
stroke. `impact` only on the hero beat named in your brief.

## v6 — THE THREE-MODE SYSTEM (Adnaan's SOP, 2026-10-15) — supersedes the speaker-card rules above
Keep everything that makes the house look: the paper + grid, bold kinetic type (black + red), and the SKETCHBOOK
DOODLES (board, target, mountain, robot, tall bar, stick figures…) — he loves them. What changes is how HE appears:

- **Mode A — split (primary talking layout)**: `<div class="spk split" data-h="960">` → his footage edge to edge in the
  TOP half (y 0–960, no border/radius/shadow/tilt/float, face centred). The paper + grid + kinetic words + doodles own the
  BOTTOM half: usable content band **y 1000–1480** (nothing in the bottom 20 %, nothing in the lower-right icon corner:
  keep x ≤ 900 below y 1200). Use for hooks, transitions, punchlines, his verdicts, the CTA.
- **Mode B — full canvas**: no speaker at all; doodles + kinetic type + cards own the whole zone (x 60–960, y 285–1480).
  Use for frameworks, step-by-steps, diagrams, examples.
- **Mode C — emphasis**: `.spk full` for a 1–2 s punch, or `.spk cutout` + `assets/speaker_cut.webm` (background removed
  with `hyperframes remove-background`) standing on the bottom edge in front of a big article/screenshot card.
- **Switch modes inside a scene** on a sentence boundary with the runtime helpers (read hf/paper.js):
  `P.splitIn(sel, t)` (B→A, band drops in, lands at t), `P.splitOut(sel, t)` (A→B, band shoots up from t),
  `P.fullToSplit(sel, t)` (C→A), `P.splitToFull(sel, t)` (A→C). A split declared with `data-at="t"` drops in at t.
- **Floating speaker cards** (portrait/secondary/small) are allowed but RARE (0–2 per reel) — this reel uses none.
- **Two-element guideline** (content-dependent, not a hard rule): one focal pair at a time — e.g. doodle + its words,
  or card + its words. Cut decorative extras that compete; let the hero doodle and the type breathe.
- **White space**: leave roughly 35–50 % of the grid empty so it reads clean on a phone (content-dependent).
- **Sound**: SFX are now sparse (structural beats only) and chosen centrally — keep writing beats.json with honest
  times as before; no `scribble` beats needed.
