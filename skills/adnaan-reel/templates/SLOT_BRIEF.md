# Shared brief for every adnaan-reel scene (read fully, then your slot's TASK.md)

You are building ONE full-screen opaque scene for an adnaan-reel edit. Nothing else. Work only inside
your slot folder. Do not touch other slots, base.mp4, edl*.json or anything else in `{{EDIT_DIR}}`.

The user has an established house style and rejects anything bland. Your scene must look like it
belongs in the approved reel. **Which look?** `{{EDIT_DIR}}/brand/brand.json` → `"look"`:
- **`mint` (v7, the house default since reel-08)**: open `{{SKILL_DIR}}/assets/style/v8_contact_sheet.jpg` now — his face
  full-screen in TALK beats with our kinetic captions (charcoal + mint), a grey board with a strong vignette and white-glyph
  icon discs in VISUAL beats, the camera travelling, the signature shrink into a disc/card. No red, no hand-drawn marker.
  The scenes behind it are in `{{SKILL_DIR}}/examples/reel-08-v7/`.
- **`paper` (legacy v6)**: `{{SKILL_DIR}}/assets/style/v6_contact_sheet.jpg` — paper world + kinetic type + a hand-drawn
  red marker layer + readable real pages (reel-06/07).

1. **The runtime is the style.** `hf/paper.css` + `hf/paper.js` (copies of `{{SKILL_DIR}}/templates/runtime/`)
   draw the paper world, the speaker cards, the kinetic type, the exits, the floats and every tactile primitive
   (coins, pills, chips, UI/browser/terminal cards, agent puck, dotted paths, cursor). **Never edit or
   re-implement them** — a scene that hand-rolls its own card or word entrance is wrong even if it looks close.
   Read the header of `hf/paper.js` once: it lists the data attributes and the `P.*` helpers.
   **Mint look: `hf/v7.css` + `hf/v7.js`** are the v7 layer — the starter already runs `const V = V7.init(P)`. Read its
   header: icon discs, the disc chain, the signature shrink/grow into a disc or the small card, the camera, the zone mask.
   **Paper look: `hf/marker.css` + `hf/marker.js`** are the hand-drawn layer (v5) — `const M = Marker.init(P)`: loops,
   underlines, arrows, ✗/✓, hatch, highlighter, Caveat notes, tape, `M.line` for any doodle (style.md "The marker layer").
2. **Your `hf/index.html` is already the starter for your scene type** (`{{SKILL_DIR}}/templates/scenes/`).
   Keep its structure. You change: the copy (from `words.html`), positions/sizes (`data-x/right/cx`, `data-base`,
   `data-size`, `data-fit`), emphasis (`data-hero` / `data-pop` / `data-accent`, `.ocean` (= the accent class; red by default) on 1–2 words per phrase),
   phrase exits (`data-exit`), the cards' `data-x/y/w/h/at`, and the **bespoke hero object** (its markup, a few
   CSS rules with brand tokens, and its timeline on `tl` using `P.*`). Everything else stays as scaffolded.
   Need a mechanism the starters don't have? Study the closest finished scene in `{{SKILL_DIR}}/examples/reel-06/`
   (v5 reference) or `examples/reel-05/` / `reel-04/`
   for the idea, then build it on the runtime (its primitives + GSAP), not by pasting old code.
3. **Art direction is binding**: `{{EDIT_DIR}}/animations/SHARED.md` (sizes, palette, objects, project specifics —
   face position, accent, real data you may show). Hero words ≥ 170 px, supporting ≥ 84, connective ≥ 64; staggered
   collage, never a centred block; lower 40 % of the zone never empty for long; nothing outside x 60–960 / y 285–1480.
   Those are the `data-size` values you author: the runtime multiplies every kinetic line by `--type-scale`
   (house 0.94, set once at the end of `hf/brand.css` — never edit it). Any inline type size you add yourself
   must be in **em** of its line so the scale reaches it.
3b. **Readability (binding — he asked for it; the coordinator fails a scene on any of these)**: every pixel inside
   the zone on every frame (measure); real pages/posts as strips at ≥ 0.85 (text ≈ 40–45 px) with a highlighter
   behind the spoken phrase (mint: `.v7-hl`; paper: `M.highlight`), never a loop across lines; NO semi-transparent text — a word is readable or gone,
   recede objects not words; words over his clothing: paper look on solid paper, mint look charcoal + `.g7` glow
   (mint only at hero sizes); handwriting ≥ 60 px ink/dark accent; chips,
   logos (≥ 56 px), stickers and doodles sized for a phone.
4. **Words**: on-screen words = `words.html` (= words.txt) only. Fix ASR spellings of names; omit fillers; never
   paraphrase; no invented stats, quotes, posts or documents. Words over a portrait card get `class="kin"` and
   sit on his chest — never over the face.
5. **Media is in `hf/assets/`**: `speaker.mp4` (cut to this scene; keep `id`, `class="clip"`, muted,
   `data-duration` = the preset) and the captured pages / user media named in the brief. Real logos only from
   files the coordinator supplied (`<img>`), never drawn or recoloured.
6. **Animate by the principles** (`{{SKILL_DIR}}/references/animation-principles.md` — Lasseter's, applied by the
   runtime): key poses in `NOTES.md` first; contact frames on words; anticipation before the hero move; overshoot
   + settle; parts lag the whole (2–4 f staggers); long moves on arcs (`P.arc`, `P.cursorTo`); squash/stretch on
   shapes only (`P.squash`); one focal point (`P.recede` the rest); secondary action so no hold ≥ 1 s is dead; ONE
   exaggerated hero beat (`P.punch`/`P.shake`); exits faster than entrances; one light direction. If a frame could
   be a static slide, it is not finished.
6b. **Richness is the house level (v4).** The user asked for "more creative, more engaging" motion and approved the
   result as the default. Beyond the hero object, every paper scene carries **2–3 secondary micro-animations** from
   `{{SKILL_DIR}}/references/motion-ideas.md` (or better, your own in the same spirit): a cursor that DOES the thing,
   numbers that count/roll/flip to their real value, icons that come alive, physics (lanyard, rope, liquid),
   characters with personality (eyes that track, a squint, a strain), type effects on the hero word (per-letter slam,
   cascade, echoes, thinning), a hero icon landing exactly on its word (a padlock snapping on "lock"). Each is tied to
   a spoken word, stays in the palette and the zone, and never competes with the focal point (stage it). Before you
   render, ask: *could this be more alive without getting busier?* `fullscreen` scenes stay minimal — expressive type
   and at most one small object.
6c. **Sound beats** (both looks follow the v6 30 % rule in TASK.md: only beats tagged `"role"` sound; the legacy tag list
   below still names the contact frames). Write `<slot_dir>/beats.json` — every visual contact frame that deserves a sound, as
   `[{"t": 2.80, "sfx": "impact", "what": "FDE lands"}]` (scene seconds; `sfx` ∈ pop, tick, impact, riser, whoosh,
   ping, ding, **scribble** — one per audible marker stroke with its `"dur"`, e.g. `{"t": 1.10, "sfx": "scribble",
   "dur": 0.35, "what": "loop round 0.2%"}`, ≥ 0.1 s apart, not the boil; optional `"gain_db"` to make one quieter). `impact` only on the 1–2 hero beats; `riser` names the HIT
   time (its cue starts 0.45 s earlier); ticks for checks/typing/clicks/digits; ~8–20 beats per scene, never two
   loud ones within 0.1 s. `scenes.py edl` turns them into the mix — re-write the file if you retime.
7. **Snapshot, then render** (from `hf/`):

   ```bash
   npx --yes hyperframes lint . && npx --yes hyperframes snapshot . --at <landing times>   # seconds, look at the PNGs
   npx --yes hyperframes render . --format mov -o ../render.mov                           # only when the stills are right
   ```
8. **QA — do not skip**:

   ```bash
   uv run --project {{SKILL_DIR}} {{SKILL_DIR}}/helpers/slots.py check <slot_dir> --motion --at <landing times>
   ffprobe -v error -count_packets -select_streams v:0 -show_entries stream=nb_read_packets -of csv=p=0 render.mov
   ```

   The frame count must equal TASK.md exactly. Measure your bounds over every frame (diff against a render with the
   content removed). Open `check_sheet.jpg`, `motion_strip.jpg` and 2–3 full-size frames: no collisions mid-motion,
   type at the SHARED.md sizes, whole head in every card, real assets legible, no dead holds. Fix and re-render.
9. **Write `NOTES.md`** (key poses, as-built timeline in scene seconds, the principles checklist from TASK.md, the
   richness list, the readability checks, deviations) and `beats.json`, then **reply** with: render path, check line, frame count, measured
   bounds, key timings, what is new/bespoke, deviations.

**Housekeeping (each of these went wrong once):** scratch files (bounds scripts, background-only reference renders,
extracted frames) go in `<slot_dir>/qa/` — never a shared scratchpad (other agents overwrite it), and never delete
anything outside your slot. **Before your final reply, stop every background process and monitor you started**
(renders, previews, watchers) — a lingering one re-sends your report to the coordinator again and again.

Do not ask questions. If anything is ambiguous, pick the interpretation closest to the starter and the examples.

Anti-list: no subtitles or caption bars; no words the speaker didn't say; no stats, quotes or claims beyond the
brief; no drawn brand logos; no hard outlines or offset shadows; no second accent colour; no linear easing except
continuous mechanical motion (grid, marching dots, page scroll); no dead holds; nothing outside the zone; no
emoji; no full-bleed raw footage except in the `fullscreen` / `demo` types; no objects crowding a fullscreen
scene; no re-implemented runtime pieces; no hard-coded hex.
