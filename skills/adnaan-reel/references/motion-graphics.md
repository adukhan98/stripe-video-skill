# Motion graphics

> **adnaan-reel:** every beat is an opaque `scene` slot built in the house style — `references/style.md`
> and `references/scenes.md` win over anything below. The transparent-overlay / EDL-layout guidance here is
> inherited from video-edit and applies only to rare extras (e.g. a corner badge over a full-bleed demo).


Graphics are **transparent overlay videos** composited over the cut by `render.py`. Each one is a
*slot*: one HyperFrames project, built by one sub-agent, rendered to ProRes 4444 with alpha, checked
over the real footage before it goes in. Slots are independent, so build them all in parallel.

Slots come from the **approved storyboard**: each graphic beat's description and motion notes
become its brief. The look comes from the chosen style (this file for clean brand graphics,
video-edit's creator preset (not used in adnaan-reel) for creator reels, which are mostly EDL layouts and need few slots). The movement comes from `animation-principles.md`, which every slot
follows.

## Workflow

1. **Render the cut first** — graphics are timed against it:
   `render.py edl.json -o edit/base.mp4 --base-only` (writes `timeline.json` too).
2. **Plan slots** in `edit/animations/slots.json`, using output-timeline times (read them off
   `takes_packed.md` + `timeline.json`, or a `timeline_view` of `base.mp4`):

   ```json
   [
     {"id": "s1_hook", "start": 0.0, "duration": 3.2, "layout": "top",
      "brief": "Logo mark pops, then 'Muse is everywhere.' — 'everywhere' lands on 'Instagram' (~2.2 s) in primary."},
     {"id": "s2_list", "start": 13.75, "duration": 7.2, "layout": "split", "crop_y": 340,
      "brief": "Checklist panel, 3 rows appearing on 'easy' (0.9 s), 'familiar' (2.6 s), 'WhatsApp' (4.8 s)."}
   ]
   ```

   Write each brief like a director: what appears, in what order, landing on which words, which
   colours/logo variant, what it must not cover. Name the **key poses** and the principle doing
   the work ("card anticipates, rises on an arc, overshoots 4 % on 'billion', settles; labels
   stagger 3 f; slow push-in through the hold"). Include exact copy — sub-agents never invent
   claims. Give asset paths for every real clip, screenshot or logo, plus the source label text
   for commentary clips.
3. **Prepare**: `slots.py prepare --edit-dir edit` creates per slot `TASK.md`, `slot.json`,
   `words.txt` (words in slot seconds), `refs/` (frames underneath), and `hf/` — a HyperFrames project
   already set to the canvas, the slot duration and a transparent background, with the brand kit
   installed. It also writes `animations/SLOT_BRIEF.md` (shared rules) and prints one prompt per slot.
   `words.txt` comes from the source transcript mapped through the EDL. With local whisper, check it
   against verified per-segment times and overwrite it: agents trust these numbers.
   **Shared art direction.** When several slots must read as one system (a series of split panels, a
   recurring widget), write `animations/SHARED.md` before spawning, and start every brief with
   "FIRST read SHARED.md". It holds the exact layout grid, background treatment, enter/exit motion,
   continuity state per slot (e.g. what the wallet holds at the start and end of each panel), and
   the paths of shared assets such as photos or scans, the **motion strength** (subtle/playful),
   shadow direction, border width and highlight colour. Without it, the panels drift apart in size, position and motion.
4. **Spawn one sub-agent per slot in a single message**, appending to the printed prompt "read
   SHARED.md" and any asset paths. Each authors `hf/index.html`, renders `render.mov`, runs
   `slots.py check`, fixes, and reports. If an agent dies mid-task (rate limit), resume it with
   SendMessage ("continue from where you left off"). It keeps its context.
5. **Review** every `check_sheet.jpg` and `motion_strip.jpg` yourself, then add the slots to the EDL `overlays` (with
   `"layout": "split"` and `crop_y` for split slots). Set each overlay's `duration` to the
   `ffprobe` duration of its `render.mov`, because renders round to whole frames (4.65 s → 4.667 s).
   Then render a preview.

### Real-object graphics (photos, scans, product shots)
Abstract "number + icon" panels read as templates. When the topic has a physical object, put the
real thing on screen. One shipped reel used public-domain US banknote scans that were broken into
change, zapped into a plug, wired to a switch and shredded by a fan. Brief agents on:
- **Treatment:** small radius, contact shadow, a sheen sweep on landing, perspective 1200–1400 px
  with ≤ 25° tilts, blur only while moving fast, a deterministic flutter.
- **Integrity:** never recolour or crop away identifying detail (a banknote's denomination, a
  product's logo). Flip only edge-on, so mirrored text never shows.
- **Story verbs:** the object breaks, flies, slots into, gets zapped or shredded. That gives each
  beat its own action.
- **A continuity widget:** the same object in a small tray (a wallet, a cart, a battery), so the
  state carries from panel to panel.

## Layouts and zones

Zones are computed from the platform safe zone (`platforms.py`) — `TASK.md` states the exact pixels.

| Layout | Zone (vertical 1080x1920, Reels) | Notes |
|---|---|---|
| `full` | the whole safe zone | Backgrounds may bleed to the edges; keep the caption band quiet. Covers the speaker — use for openers, end cards, big moments. |
| `top` | top ~30% of the safe zone (y 285–643) | The face stays visible below. Hook titles, callouts. |
| `lower_third` | just above the caption band | Name/role straps. In, hold, out. |
| `split` | opaque panel on the top half, content inside it | The compositor moves the speaker (`crop_y` = top row of the face crop) into the bottom half while the panel is fully opaque (`swap_inset`, 0.15 s after it lands / before it leaves); captions jump to the seam. |
| `corner` | top-right corner of the safe zone | Small marks. A static logo bug is easier as a PNG overlay in the EDL. |

Not slots, but EDL overlay layouts for plain media (video-edit's creator preset (not used in adnaan-reel)): `split` with a video/image
fills the top half (`fit` cover/contain), and `full_pip` puts the media full-canvas with the
speaker in a circle top-right inside the safe zone.

Landscape (`youtube`) uses the same layouts: `top` becomes a top band, `lower_third` sits above the
caption band, `split` puts the panel on the top half.

## The graphic vocabulary

Pick per video — not every edit needs all of these. Fewer, better graphics beat a busy screen.

- **Hook title** (first 1–3 s): the promise of the video in ≤ 6 words, logo optional. Lands on the
  key spoken word. Kinetic type (word-by-word reveals, a highlighted keyword in the primary colour).
- **Lower third**: name + role/handle the first time a person appears; ≥ 3 s on screen.
- **Keyword / stat callout**: the number or phrase the speaker stresses, big; count-ups for numbers
  (land the final value on the spoken number). Source every stat in NOTES.md / project.md.
- **List / checklist / comparison panel** (split): items appear one by one on their words.
- **Quote / testimonial card**: short pull-quote in the heading font, attribution in body.
- **Logo sting**: ≤ 1.5 s, mark animates in (scale/rotate/draw), wordmark follows. Opener or bumper.
- **End card + CTA** (over `end_hold` or the final seconds): logo, handle/URL, one clear ask. Keep it
  on screen ≥ 2 s; duck or fade the music under it.
- **Progress bar / chapter markers** for tutorials; **icon pops** for lists; **chat bubbles / UI
  mocks** when the story is about a product — built from brand tokens, not screenshots of other
  brands.
- **Transitions**: a brand-colour wipe between sections is a full-layout slot of ~0.6 s; use sparingly.
- **Real clip in a frame**: the launch film, keynote moment or news clip the speaker refers to,
  playing muted inside a rounded frame (full layout, or the top panel of a split), with a small
  `Source: <owner>` label. The frame scales in 96 → 100 % with a slight overshoot and pushes in
  slowly while the clip plays. Never full-bleed, and never picture-in-picture over the speaker's face.
- **Screenshot / post / website**: a real capture (Claude in Chrome, a screenshot, or `npx hyperframes
  capture <url>`), logged with `fetch.py log`, in a browser frame or card. It holds with a slow push,
  and a highlight or circle lands on the line that matters. Highlighter: a rect behind the words
  in the accent at ~55 % with `mix-blend-mode: multiply`, growing `scaleX 0 → 1` from the left over
  10–14 f, landing on the spoken word. Scale the capture until the highlighted text is ≥ 34 px at
  1080 wide. Never fabricate a capture; an illustrative mock-up is labelled as one on screen.
- **Annotations**: circles, underlines and arrows as SVG paths that draw on (`stroke-dashoffset`,
  10–16 f, `power2.out`). Arrows point at the focal element; labels in brand-font pill tags.
- **Cut-out photo / presenter**: `npx --yes hyperframes remove-background photo.jpg -o cut.png`
  (video works too: `.webm`/`.mov`) lifts a product, person or the speaker off their background,
  so they can stand in front of a graphic. Slow on video, so cut the segment first.

Non-slot tools in the EDL: `zooms` (punch-ins, hard cuts to a 1.1–1.2× framing — energy on static
stretches; `{"mode": "alternate"}` alternates across every jump cut), media `split` / `full_pip`
overlays, `sfx` on any item, PNG overlays (logo bug, badges), b-roll overlays (`fit: cover`), `end_hold`.

## Timing rules

The full set, with recipes, is in `animation-principles.md`. The essentials:

- **Land on the word**: the *contact frame* (first frame at full size/position, the overshoot peak)
  coincides with the spoken word. Start the anticipation + main action that many frames earlier
  (~0.15–0.3 s). Without this, graphics feel disconnected.
- **One new thing at a time.** The eye can't track two new elements. Stagger separate ideas
  0.1–0.2 s minimum; parts of one group overlap 2–4 frames (never a rigid block).
- **Anticipate, overshoot, settle** on the hero element of every graphic. Logos: uniform scale only.
- **Arcs** for moves over ~200 px (tween x and y with different eases).
- **Readable at 1×**: sync-to-narration cards 3–7 s (complex diagrams 8–14 s); beat-synced accents
  0.5–2 s. Hold the final state ≥ 1 s before the exit, **with secondary action** (slow push-in,
  drift, a pulse), never frozen.
- **Over speech**: a graphic's duration ≥ the narration it illustrates + ~1 s.
- **Easing**: ease out on entrances (`power3.out`, `back.out(1.2–1.6)` for pops), `power2.inOut` for
  moves, `power2.in` exits, faster than the entrance. Linear only for continuous mechanical motion
  (marching dashes, tickers).
- **First and last frame fully transparent**: the exit must finish *before* the last frame
  (duration − 1/fps) — `slots.py check` fails otherwise.

## HyperFrames notes

- Composition contract: `#root` carries `data-composition-id`, `data-start`, `data-duration`,
  `data-width`, `data-height`; timed elements carry `class="clip"` plus `data-start`,
  `data-duration`, `data-track-index`; the GSAP timeline is created `paused: true` and registered
  as `window.__timelines["main"]`. Everything must be seek-safe and deterministic.
- If the `hyperframes`, `hyperframes-core`, `hyperframes-animation`, `hyperframes-keyframes` or
  `hyperframes-registry` skills are installed, slot sub-agents can load them for deeper patterns
  (text effects, registry blocks for charts, glitch, confetti…). Registry blocks must still be
  restyled with brand tokens.
- `npx --yes hyperframes lint .` before rendering; a nested-structure warning is fine for overlay slots.
- `npx --yes hyperframes render . --format mov -o ../render.mov` → ProRes 4444, `yuva444p12le`, alpha.
  `--quality draft` for quick looks. `--format webm` (VP9 alpha) also works; render.py decodes it with
  libvpx so the alpha survives.
- `hyperframes init` refuses a non-empty folder — that's why the project lives in `<slot>/hf/`.
  `prepare` handles it; if you scaffold by hand: `cd <slot> && HYPERFRAMES_SKIP_SKILLS=1 npx --yes
  hyperframes init hf --example blank --non-interactive --resolution portrait`, then set the duration
  and a transparent `html, body, #root` background, then `brand_kit.py install hf --edit-dir <edit>`.
- Graphics that must sit *between* shots (an opaque intro card, a full-screen title with its own
  sound) can instead be rendered as opaque MP4 (`--format mp4`) and placed as a **range** in the EDL
  with `"grade": "none"`; render.py adds silence if the file has no audio.

## Colour accuracy

render.py composites overlays and captions in RGB and converts to BT.709 once, so brand hex values
survive (measured within a few levels of the source hex after H.264). HyperFrames' ProRes output
is untagged and decodes correctly with ffmpeg's defaults. Don't "fix" colours by eye in a slot —
if a colour looks off, check the hex in DESIGN.md first.

## QA checklist (per slot)

`slots.py check <slot_dir>` verifies size, fps, duration (±1 frame), alpha, transparent first/last
frame and safe-zone spill, then writes `check_sheet.jpg` — 8 frames of the render over the real cut,
safe zone in red, caption band in yellow. Then look:

- Everything inside the red box; the caption band quiet while captions show.
- The brand font is actually rendering (compare letterforms with `board.png`).
- Logo crisp, correct variant for its background, untouched.
- Text legible at phone size (≥ 30 px at 1080 wide; headlines 64–110 px).
- Reveals line up with their words (pull single frames at the word times if unsure).
- Motion: `slots.py check <slot> --motion --at <landing times>` → `motion_strip.jpg` shows every
  2nd frame of the entrance, each landing and the exit. Look for anticipation before the main move,
  the overshoot and settle, siblings arriving staggered, and an exit that finishes early. No dead-hold
  WARN. For paths, use `npx --yes hyperframes keyframes hf --shot arcs.png --selector <el>` (onion
  skin: a straight line where you wanted an arc is visible at a glance).
- It doesn't cover the face (except `full`/`split` by design) or fight the b-roll underneath.
