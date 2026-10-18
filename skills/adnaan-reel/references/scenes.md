# Scene grammar — planning and briefing adnaan-reel scenes

The reel is a sequence of **8–14 full-screen scenes** laid back to back over the locked cut. The voice
runs continuously underneath; each scene shows what is being said at that moment.

## 0. v7 "MINT" grammar (house default since 2026-10-17 — `init-brand --look mint`; the v6 sections below = paper look)

| Mode / type | Use for | Starter | Notes |
|---|---|---|---|
| **TALK** `talk` | hook, transitions, opinions, payoffs, CTA — ~50 % of the reel | `talk.html` | him full-screen; kinetic captions charcoal + glow, ONE mint hero word; usually captions only, occasionally one icon disc |
| **TALK + depth** `talk_depth` | "behind me" moments (photos, an object sliding out from behind his shoulders) | `talk_depth.html` | footage → `.v7-behind` → his matte (auto `speaker_cut.webm`) → words; never cover his face |
| **VISUAL** `visual` | every explanation, list item, example, real page | `visual.html` | board + strong vignette, world layer + travelling camera, icon discs, flat vector props, readable cards + mint highlighter; ≤ ~8 s without him |
| **CHAIN** `chain` | the list/key-point map appearing (usually right after the hook) | `chain.html` | TALK → the signature shrink into disc 1; connector draws, discs pop as it arrives; geometry fixed in SHARED.md |
| **CARD** `card` | a visual that needs him visibly present | `card.html` | shrink into the small rounded card (left side, ~360×460), the visual plays beside it, grow back on the payoff; 0–2 per reel |

- **Signature shrink** 1–3 per reel: into the current item's chain disc, else the small card. A scene after a shrink opens on
  its exact end state (`V.placed`, `V.chain` + `V.chainEnd`), checked with `scenes.py seam`.
- Chapters of a list open by travelling to (or flipping) their disc; the CTA pulls back to the whole chain.
- Variety still applies across reels: the chain, the board and the discs are the frame; the hero objects inside each
  VISUAL beat are new every reel (flat vector, palette fills, personality in motion).

## 1. Splitting the cut into scenes

- Run `scenes.py words --edit-dir edit` — it prints every cut segment with its output start and its
  words. Scene boundaries go **on segment starts** (a sentence or topic start), so a scene never
  starts mid-word.
- One scene per idea. Typical lengths 3.5–7 s; the hook is the first sentence (~3–4 s); the CTA is
  the last sentence plus the end hold (~4 s). A beat longer than ~7 s is a question, not a rule: would
  the viewer see a *new picture* if it were two compositions (e.g. "the funnel is drawn" / "the funnel
  fills")? Splitting is what raises visual turnover; a camera push inside one scene does not read at
  thumbnail size (reel-06 A/B test). Keep it as one scene when the drawing itself is the continuity.
- For a list reel ("5 skills / 3 tools / 7 tips") each item gets its own scene, opened by a chapter beat.
- **Speaker presence (PAPER look — v6, the three-mode system; mint look: §0) — `references/style.md` "v6"):** every beat picks a MODE in the
  beat table's **Mode** column: **A** split (him edge to edge in the top half, words + doodle on the paper below — the
  primary talking layout: hook, transitions, punchlines, opinions, CTA), **B** full canvas (no speaker — frameworks,
  diagrams, step-by-steps, examples), **C** full screen for a 1–2 s punch or a **cutout** of him standing in front of a
  big article/screenshot card. Modes can change INSIDE a scene on a sentence boundary (`P.splitIn/splitOut/fullToSplit`).
  Full screen: 2–4 per reel, never adjacent. Floating cards (portrait/secondary/small) only 0–2 per reel. Keep Mode B
  stretches under ~12 s — bring him back in Mode A on the payoff line.
- Variety across reels (he asked to keep this in mind): the world, type and accent are fixed, but the
  hero objects are not a fixed kit. Don't reach for coins + pills + puck + dotted path by reflex; pick the
  object the topic suggests (a file tree, a timeline, a before/after, a stack, a map…) and check the last
  two reels' `project.md` scene lists so the same mechanism doesn't headline three reels in a row.

## 2. Scene types — PAPER look (each has a starter on the shared runtime — set `"type"` in slots.json; mint-look types: §0)

`slots.py prepare` writes `hf/index.html` from `templates/scenes/<type>.html`: the world, the speaker MODE,
the kinetic words, exits and one bespoke object are already wired to `paper.js`. The agent fills copy and
positions and shapes the hero object. **v6 starter modes:** Mode A split — `hook`, `opinion`, `wrapup`, `cta`;
Mode B canvas — `blank`, `explainer`, `mechanism`, `chapter_page`; Mode C — `fullscreen`, `cutout` (he stands in
front of a big page; `cut-speaker` makes `speaker_cut.webm`); `demo` keeps its small card (cards are rare, not banned).
The example column below describes the v4/v5 reels — the IDEAS still apply, the speaker cards in them do not. `"bespoke": true` marks scenes whose hero object must be invented (default for explainer / mechanism /
blank) → give those to the strong model; template scenes can go to a smaller one.

| Type | Use for | What happens | Starter → example |
|---|---|---|---|
| **Hook** | first sentence, the promise | optional user-written text hook readable on frame 0 at the top; PORTRAIT hero speaker card (full head + shoulders) settles by 0.3 s; kinetic stack lands word by word on his chest / below; the list's coins pop on the number word; accent underline + 1 % punch on the payoff word | `hook` → `v01_hook` |
| **Explainer** | "X is just …", a concept | graphics only after a short card+phrase beat: a hero object (deep-teal card/envelope) opens, real ingredients fly in on their words, it seals and rides a dotted path into the agent puck | `explainer` → `v02_skills` |
| **Reassure + action** | "you don't need to be …, just do Y" | hero card + one giant accent word circled by a dotted loop; then the action as UI: real link pills → copied → into the puck → stacked "ready" notifications | `opinion` + pills → `v03_genius` |
| **Chapter + real page** | list item named; "I've used this…" | coin N rolls in and turns accent, item name giant in accent colour; real site in a browser card + stat pill + secondary speaker card; a closing metaphor (slop pile vacuumed into one crisp card, word struck through) | `chapter_page` → `v04_taste` |
| **Chapter + mechanism** | what the item does, step by step | header compacts (coin + name + slug); the mechanism as objects: variations deal into a fan → cursor picks → picked cards flip deep and merge → drop into a "</> codebase" pill | `mechanism` → `v05_refine` |
| **Chapter + structure** | frameworks, layers, steps | real named parts as 3D slabs stacking on their words; the agent lands on top; compass needle + dotted path on "direction" | `blank` + slabs from `v06_layers` |
| **Chapter + demo flow** | "record X → give to agent → it builds Y" | real repo page + real chip names → favourite chip pulled out → REC card → dotted path into puck → result builds block by block | `chapter_page` + chips → `v07_mengto` |
| **Chapter + before/after** | audits, fixes, improvements | real site behind the chapter; bland card + accent scan line + pins → checklist with ✗ → rows flip to ✓ → card upgrades to deep version on "improve" | `chapter_page` + uicards → `v08_hallmark` |
| **Wrap-up** | the thesis restated, "copy & paste into …" | hero card + big accent word and a struck-through word; card shrinks, coins orbit it on a dotted ring; prompt box gets the items pasted; tool names as plain text pills (no logos) | `wrapup` → `v09_taste` |
| **CTA** | "Comment X and I'll send …" | "Comment" + “X” giant in accent colour, in quotes; dotted loop down to a PORTRAIT speaker card; end hold returns the CTA to hero size; coins stack into a "→ your inbox" pill; freeze-frame end hold stays alive | `cta` → `v10_cta` |

**Full-screen speaker** → `fullscreen` (him edge to edge, words low, nothing else; `P.growFull` for a card
that becomes full screen on the hero word). A long screen recording where the screen action is the point → **`demo`** (full-bleed recording, small speaker
card, phrase at the bottom; `flashcheck --allow` for its window).

reel-04 (non-list, opinion reel) adds: **Opinion / verdict** (`reel-04/v08_perfect` — portrait hero,
struck word + ✗ pill, then accent word + ✓ pill), **Thesis object** (`v09_dead` — huge accent question
with dotted ellipse, then one object that breaks: shield + padlock cracking), **B-roll collage**
(`v05_making` — real clips looping inside desktop-window and phone cards, then fanning into many app
cards), **Real list with real logos** (`v07_adobe` — official icons → names on chips, ticks on the
spoken word), **Mechanism with the agent** (`v03_inside`, `v10_copy` — puck scans an app card, layers,
a copy peels off).

Non-list reels use the same grammar without coins (or coins for the 2–3 key points). Invent new scene
types when the content needs it — but keep the world: paper, heavy grotesk type, soft objects, one accent.

## 3. Writing a scene brief (slots.json)

Each entry: `{"id", "start", "duration", "layout": "scene", "type": "<starter>", "bespoke": bool, "brief",
"assets": [...], "sfx": ...}`.
Write the brief like a director, with exact copy and exact word times from `scenes.py words`:

```
FIRST read animations/SHARED.md and look at the style frames it lists. FULL-SCREEN OPAQUE scene — <type>.
Spoken: '<the exact sentence(s) in this window>' (exact times in words.txt).
CHAPTER (0–1.2): coin 03 turns accent, 'third one' small, 'Layers' Inter Tight 900 ~240 in accent lands ~0.51.
<BEAT NAME> (a–b): <what appears, on which word (time), which object, which real asset from hf/assets/>.
...
Hold alive to the cut.
```

- Name the **key poses** and the word each lands on. Give real data (repo slugs, star counts, layer
  names, headings) — sub-agents never invent claims.
- List every asset the scene gets in `"assets"` (captured pages, user screenshots/recordings, and the
  **official logos** from `logos/` for every tool/company named in the scene); `scenes.py cut-speaker`
  copies them to `hf/assets/` next to the speaker clip. The brief says where each logo goes (chip, pill,
  app card) and where each photo goes (polaroid, taped print, avatar chip) — a named tool without its logo,
  or a named person without their real photo, on screen is a review fail. Photos come from `fetch.py photo`
  (Wikipedia/Commons, licence logged) or from him; never AI-generated, never a lookalike. A face the audience
  would not recognise is dead b-roll — a niche person is shown through their work (post, repo, product).

  **What the line is → what goes on screen** (source the point, not the keyword):

  | He says… | Show |
  |---|---|
  | a number / stat ("$24 a month", "750 sign-ups") | the figure on the real page — pricing page strip, dashboard, chart; the number rolls to its value on the word |
  | "people are saying" / "everyone's talking about" | real posts, headlines, search results (`fetch.py tweet`, `capture.py --readable`) |
  | a quote / "he wrote" | the authentic post or article strip with the highlighter — never a synthetic quote card |
  | growth / "went viral" | a chart going up, or the viral post with its metrics visible |
  | decline / "tanking" | a chart going down, the error screen, the failing thing |
  | "research shows" | the paper's title/headline strip or the expert on camera |
  | "X vs Y" | sequential singles, each on its word — never an agent-built split-screen (he rejected those) |
  | "how it works" / steps | his own recording in a device card, or the Mode B diagram built from the real part names |
  | a named person | their work first; a photo (polaroid / taped print) only when the face is known; a clip only when it shows the *moment* the line describes |
  | a named product / company | its official logo + the real UI (current version) |
  | a metaphor ("like a rocket") | the marker doodle acting it out — not stock of a rocket |
  | a story with actions ("every morning he'd…") | doodles and chips that act out the places and actions, never a literal re-enactment |
- Name the starter (`"type"`) and, for a bespoke hero object, the closest finished scene to study for the
  *idea* (`examples/reel-04/v03_inside.html` for slabs, `v10_copy` for the peel…) — the agent builds it on the
  runtime's primitives, never by pasting old scene code.
- **Richness (house level since reel-05)**: besides the hero object, name 2–3 secondary micro-animations per paper
  scene, each on its word, from `references/motion-ideas.md` (a cursor that does the thing, a real number rolling to
  its value, icons coming alive, physics, a character with personality, a type effect on the hero word, a hero icon
  landing on its word). Fullscreen beats: expressive type + at most one small object.
- **Sound**: no `"sfx"` field needed any more — each agent writes `beats.json` (contact frames tagged
  pop/tick/impact/riser/whoosh/ping/ding) and `scenes.py edl` mixes them from the ElevenLabs house kit
  (`assets/sfx/`). Name the hero beat(s) that get `impact` in the brief. `subdrop` stays on the first cut range.
  A legacy `"sfx"` on a slot is used only when that scene has no beats.json.

## 4. Reviewing a scene (you, when its agent reports back)

Open its `check_sheet.jpg` and `motion_strip.jpg`:
- **v7 mint**: the planned type/mode; TALK captions readable over his clothing (charcoal + glow; mint only on one hero word
  at hero size); no red, no marker boil, no Caveat; icon discs with the house glyph size and shadow; the camera moves on
  arcs and nothing leaves the zone mid-move; a shrink lands exactly on its disc/card and the next scene opens on it
  (`scenes.py seam`); words = his words (reel-08: chat pills saying "I wrote it" when he said "you wrote it" were sent back).
- **first scene**: frame 0 (the thumbnail) shows only finished, true content — no random/transient values, nothing mid-entrance.
- **v6**: the right MODE (A/B/C) for the beat; no floating corner card unless the beat table says so; about two focal
  elements at a time (content-dependent); ~35–50 % of the grid empty; nothing right of x 900 below y 1200 (IG icons);
  beats.json tags only hook/structural beats with a role (everything else stays silent); doodles still carry the scene.
- the paper world is identical to the other scenes (grid, vignette, same card styling)?
- type big enough (hero ≥ 190 px), collage-staggered, words = spoken words?
- speaker face centred and uncropped in the card? real assets legible?
- nothing outside x 60–960, y 285–1480; no collisions mid-motion; no empty lower half for long?
- the principles checklist in its NOTES.md is answered honestly (anticipation, overshoot, overlap, arcs,
  staging, secondary action, one exaggerated beat)? The motion strip shows them?
- **richness**: hero object + 2–3 secondary micro-animations that act out the sentence (not decoration), one focal
  point at a time? Ask "could this be more alive without getting busier?" — if yes, send concrete ideas from
  `motion-ideas.md`.
- **marker**: does the hand-drawn layer do real work (a loop/underline on the hero word, an arrow or doodle that acts
  out the sentence, a note that labels), drawn ON its word, boiling, never across text or the face?
- **readability** (style.md, binding): every pixel in the zone (their measured bounds), real pages as strips ≥ 0.85,
  no semi-transparent text lingering, words over clothing on solid paper, notes ≥ 60 px, chips/logos/doodles/stickers
  phone-sized? Check the newest `render.mov` timestamp is after the last input change before you approve.
- `beats.json` present, 8–20 kit beats + `scribble` beats (with `dur`) for the marker strokes, `impact` only on the
  hero beat(s), times matching the render?
If not, SendMessage the same agent with concrete fixes (it keeps its context) — don't respawn.

## 5. Recurring drawings (continuity across scenes — reel-06's funnel)

When one hand-drawn object carries the reel (a funnel filled tier by tier, a map, a stack, a chart), it must read
as ONE drawing being worked on:
- Put its **fixed geometry and seeds** in SHARED.md "Project specifics" (e.g. `M.funnel({x:150, y:820, w:560, h:330,
  neck:.16, split:[0,.38,.66,.86,1], spout:56})`), plus which scene adds which part.
- The first scene draws it; every later scene opens with it **already drawn in the previous scene's final state**
  (`draw(0)`, earlier fills at 0, the same characters/pins at the same coordinates and seeds — tell the agent to read
  the previous scene's hf/index.html + NOTES and copy that code) and adds only its own part.
- Adjacent scenes that share it: `scenes.py seam A B --edit-dir E` and look — nothing in the shared drawing may jump.
- Brief the scenes in order of the story; if a later scene finishes first, have it match the earlier one afterwards.

## 6. Reference builds — mint: `examples/reel-08-v7/` (v7, the house look); paper: reel-06 (v5) below

`examples/reel-06/` — 14 scenes, hook → full-screen verdict → the source (polaroid + logos + the real post as strips)
→ the recurring funnel (draws, fills tier by tier, magnifier) with comedic and mechanism scenes in between → the
bubble → zoom-out → the gap chart → portrait sunrise → full-screen padlock CTA. Every paper scene: hero object +
2–3 micro-animations + marker work; one fix pass per scene for size/readability/continuity.
