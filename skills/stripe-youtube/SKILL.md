---
name: stripe-youtube
description: Long-form YouTube editing (16:9, 5–15 min explainers, talks and walkthroughs) in a company's brand — Stripe by default. Turns a camera take (plus any screen recordings, or a Cap project) into a finished video: the adnaan-reel v7 design system on a 16:9 board, re-coloured from ONE brand file (brand/stripe.json: blurple accent, slate discs and ink, cool paper, the official wordmark) — a gridded paper board with a strong vignette most of the time, the speaker's plain camera in a fixed rounded card with an accent ring, full-frame talk as punctuation with full-coverage kinetic captions, disc-chain maps the camera travels along, flat white cards, real pages with a highlighter, data in one data colour, screen recordings in a window card with click-planned zooms, before/after inserts that carry their own sound, sparse structural SFX and a ducked ElevenLabs music bed ~5 dB under the voice. Cuts every pause, retake and look-down; builds only the designed moments as HyperFrames scenes in parallel, composites the rest with ffmpeg, verifies lip sync, and delivers final.mp4 + captions.srt + chapters.txt + a description + thumbnail stills. Use for "/stripe-youtube", "edit this YouTube video in our brand", a long take that should become a branded 16:9 video, or to swap in another company's brand file. Plans in two approvals (chapter outline, then beat table). For vertical reels use /adnaan-reel.
---

# stripe-youtube

The Stripe edition of Adnaan's long-form skill (adnaan-youtube): the same pipeline and the v7 design system on the 16:9
board, with every colour taken from **one brand file**. The default brand is Stripe (`brand/stripe.json`, written from
Stripe's public brand page: blurple `#533AFD` accent, slate `#061B31` discs and ink, cool paper `#EEF1F6`, white cards,
strawberry for data only). Another company = another brand file (`$Y/brand.py init --edit-dir edit --brand acme.json`);
nothing else changes. **Before anything, look at `assets/style/stripe_youtube_sheet.jpg`** (real frames of the first
video made with it) and skim `examples/stripe-v1/` (its beat table and scenes) and `examples/yt-01-v7/`. The art
direction is binding and lives in `references/style.md`; chapters, windows and cadence are `references/planning.md`; the
description is `references/description.md`. (The older Greg Light/Dark marker look is kept only on request.)

**How the brand gets in:** `edit/brand/brand.json` → `$Y/brand.py` writes `brand.css` (it re-points the runtime's
tokens) → `board.py` links it after `v7yt.css` in every scene it prepares, and talkcaps.py does the same for the caption
overlays; the runtime tweens (V.mintTo / V.charcoalTo) read the tokens too, and compose's plates follow the file. Scenes
never type a hex. Logos the brand file names are fetched from the official kit into `edit/logos/` (never redrawn).

This skill is the long-form sibling of `adnaan-reel` and **reuses its helpers** (transcription, cutting, verify, page
captures, logo/photo/icon fetchers, the render/loudness pipeline, the SFX kit, head pose). It must be installed at
`~/.claude/skills/adnaan-reel`. Run every helper with that project's environment:
`uv run --project ~/.claude/skills/adnaan-reel python <helper> …` — `R=~/.claude/skills/adnaan-reel/helpers`,
`Y=~/.claude/skills/stripe-youtube/helpers` below.

## How long-form is built (why it differs from the reels)

A reel makes every beat a full HyperFrames scene. A long video can't (hours of rendering, and tiring to watch). Here:

1. **The cut** (`$R/render.py --base-only`) → `base.mp4`: his camera, cut, 1920x1080, with the voice (built in one
   sample-accurate pass — see Anti-patterns, lip-sync drift), then `$Y/lookdowns.py` holds a frame over look-downs.
2. **Designed moments** are HyperFrames scenes (`$Y/board.py`): canvas, map, board, proof (opaque, 3–10 s) and callout
   overlays — typically 25–45 per video, built in parallel by agents. **Talk captions** are generated overlays
   (`$Y/talkcaps.py`), one per full-frame talk window.
3. **Everything else is composited** (`$Y/compose.py`): talk = base full frame + captions; screen = board plate + his screen
   recording (cut with the same ranges, zoomed by `$Y/zoomplan.py`) + the speaker card; scene windows = the render + the
   card; overlays on top; SFX + the levelled music bed; −14 LUFS. ~40 s of compositing per minute of video.

## Principles

1. **The board is the base, he is on the card.** ~70–85 % of the runtime is a board layout with his plain camera in the
   card (fixed spot, moves only on a cut, accent ring); full-frame talk is the punctuation (intro, opinions, stories, CTA).
   No matte by default — he likes the plain card.
2. **One look, one brand file.** Paper + grid + strong vignette, the brand's primary as the ONE accent (Stripe blurple),
   its deep colour for discs with white Phosphor glyphs and ink (Stripe slate), flat white cards, clean vector strokes,
   Inter Tight / Inter (Stripe's own typeface is not public). The data colour (strawberry `#E8435A`) for numbers only.
   No marker, no Caveat, no pastel hues, no hex typed in a scene.
3. **Talk is captioned, every word.** Full-frame talk windows carry full-coverage kinetic captions (white, one hero word
   per phrase in the brand's light accent, left column on a calm part of his background). Board windows carry the words inside the design. The SRT
   is still delivered. Words on screen are words he says.
4. **Show the real thing.** Every page, paper, post, study he names appears for real (readable strip in a white card,
   brand-tint highlighter on the spoken phrase); every tool/company gets its official logo; people get real photos. Never
   invent numbers, quotes, screens.
5. **Screens are the walkthrough.** His Cap recording in a window card, zoomed on what he clicks (his Cap zooms win,
   then click clusters, then manual targets), callouts drawn after the zoom lands. Waiting is cut, never sped up.
6. **Two approvals, then build everything.** Chapter outline → beat table → pilot (2–3 scenes + the captions in the
   look) → build all moments in parallel → compose → self-check → deliver. Autopilot ("just do it") skips the waits.
7. **Never a dead board.** Every designed moment has a hero object that acts out the sentence + 1–3 micro-animations; the
   camera travels; frame 0 of every scene already shows its heading or main object.
8. **Sound supports the voice.** Structural SFX only (~1 per 30–60 s, low & warm v6 kit), a calm ducked music bed ~5 dB
   under his voice (he could not hear a quieter one), voice on top, −14 LUFS.
9. **Verify before showing.** Frame counts exact, lip sync checked at every cut, every window boundary on a sheet,
   captions read against the cut, loudness measured. He should never be the one who finds a sync or level problem.

## Hard rules

1. **Outline approved, then beat table approved, before any scene is built** (unless autopilot).
2. **The cut rules of adnaan-reel apply unchanged**: word-boundary cuts, every filler cut and every join verified with
   `$R/verify_cuts.py` (read the ⚠ TAIL/HEAD flags), never render a test EDL into `edit/`, 30 ms fades.
3. **Start from his Cap trims** (`source/cap.json` "trims"). Then remove retakes: keep the LAST complete take of each
   line, never stitch one line from two attempts, drop anything he rejects out loud ("no", "again", "scratch that") and
   bloopers; check the end of the session for a re-recorded hook. **Find repeats by transcribing every kept range on its
   own** and then each join with its neighbours — whisper over the long cut merges two takes of the same line into one.
4. **No dead air**: trim every range to its speech (noise floor + 7 dB, 0.07 s before / 0.09 s after) and split internal
   pauses ≥ 0.22 s (`$R/audio_env.py tighten --margin 7 --min-gap 0.22`). He asked twice for "all pauses" cut — the
   0.3–0.9 s of air the first pass kept read as pauses.
5. **Screens are cut with the SAME ranges as the camera** (compose.py does it from timeline.json).
6. **Scenes**: exactly their frame count (board.py presets it, `board.py check` verifies); the runtime (`board.css/js`,
   `v7yt.css/js`) is installed, never edited per scene; a global look change is made ONCE in `templates/runtime/` →
   `board.py runtime`. Card zone clear; frame 0 not empty.
7. **Render only through `board.py render`** (agents too, `--only <id>`): it picks ProRes 4444 .mov for overlays (an h264
   .mov is opaque — the talk windows showed paper instead of him) and shares render slots machine-wide. **Never `pkill`
   renders** — one agent's pkill killed every other agent's render.
8. **Callout positions come from `compose.py where <out_t> <sx> <sy>`**, never guessed.
9. **One sub-agent per scene (or per family of scenes that share an object, e.g. the chain), all spawned in one message**;
   review each scene's stills as they land, send fixes with SendMessage to the same agent. A shared object has ONE owner
   who writes the shared module + notes; other agents copy, never fork it. Trust file timestamps, not reports.
10. **Downloads through `$R/fetch.py`, captures through `$R/capture.py`** (logged for credits.md); all outputs in
    `<project>/edit/`; never write inside a skill directory during an edit.
11. **Mirror check** on the camera before cutting (zoom into any print on his clothes/background in a full-res still).
12. **In shell loops, ffmpeg gets `-nostdin`** (it eats the loop's stdin otherwise).

## Helpers

| Helper | What it does |
|---|---|
| `$Y/cap.py find` / `info <p.cap>` / `ingest <p.cap> --edit-dir E` | Cap projects (newest first) → `source/cam.mov`, `source/screen.mp4`, `source/cap.json` (clicks, moves, trims, zooms) |
| `$R/transcribe.py source/cam.mov --edit-dir E --vocab "…"` | word-level transcript → `transcripts/cam.json` (cached) |
| `$R/pack_transcripts.py` · `$R/audio_env.py` · `$R/verify_cuts.py` · `$R/timeline_view.py` | read the take, tighten, verify every join (adnaan-reel) |
| `$R/headpose.py source/cam.mov --start 0 --end <s> > E/headpose_report.txt` | head pitch over the take → look-down spans |
| `$R/render.py edl.json -o base.mp4 --base-only` | the cut → `base.mp4` + `timeline.json` (sample-accurate voice) |
| `$Y/lookdowns.py --edit-dir E` | holds an on-camera frame over look-downs at line starts/ends; re-run after every base render |
| `$Y/sync_check.py --edit-dir E [--final final.mp4]` | lip sync per segment (picture vs voice vs source) and final vs base; exit 1 if off |
| `$R/capture.py` · `$R/fetch.py logo/photo/icon/url/credits` | readable page strips, official logos, real photos, Phosphor icons, downloads, credits.md |
| `$Y/board.py prepare/runtime/render/check --edit-dir E [--only ids]` | scene projects from `animations/scenes.json` (v7 runtime + icons + starter + assets + TASK.md); slot-limited render; exact-frame / alpha check |
| `$Y/talkcaps.py --edit-dir E [--dry-run]` | full-coverage talk captions: one generated `cNN_talk` overlay per talk window (re-run after any cut/scene change) |
| `$Y/compose.py plan` / `where <t> <sx> <sy>` / `render -o final.mp4 [--preview] [--only-window N]` / `sheet <video>` | window table; callout coordinates; the composite (windows + card + overlays + SFX + levelled music + −14 LUFS); boundary sheet |
| `$Y/zoomplan.py` | the zoom camera (library) |
| `$Y/deliver.py srt` / `chapters` / `stills <video> t…` | `deliver/captions.srt`, `deliver/chapters.txt` (validated for YouTube), thumbnail stills |
| `$Y/brand.py init / css / apply --edit-dir E [--brand x.json]` | the brand file → `brand.css` → every scene (board.py and talkcaps.py call it; `apply` re-installs by hand) |
| `$Y/review.py --edit-dir E <ids>` | per-scene review sheet (5 frames, card box outlined) → `verify/review/<id>.jpg` |
| `$Y/inserts.py clip / splice / shift --edit-dir E` | clips with their own audio on a brand board → spliced frame-exact into the composite → SRT + chapters shifted |

Starters (`templates/scenes/`): `canvas`, `map`, `board`, `proof` (opaque), `callout_overlay`, `talk_overlay`
(transparent) and `talk_captions` (talkcaps.py's template). Runtime headers (`board.js`, `v7yt.js`) list every primitive.
Reference scenes: `examples/stripe-v1/` (the Stripe video: beat table, scene list, chain + brand card + page modules)
and `examples/yt-01-v7/` (chain map + shared module, data bars, proof page, board flow, captions).

## Layout

```
<project>/
└── edit/
    ├── project.md                 session memory
    ├── source/ (cam.mov, screen.mp4, cap.json)        transcripts/ (cam.json raw, CAM.json corrected)
    ├── edl.json, base.mp4 (+ base_unfrozen.mp4), timeline.json, headpose_report.txt, layout.json
    ├── brand/ (brand.json, brand.css)   captures/ logos/ photos/ icons/ downloads/ music/ inserts/
    ├── animations/ (scenes.json, <id>/{hf/, TASK.md, render.mp4|mov, beats.json, qa/}, cNN_talk/ generated)
    ├── compose/ (plates, screen_cut.mp4, windows/)   verify/
    └── final.mp4, deliver/ (captions.srt, chapters.txt, description.txt, thumb_*.png), credits.md
```

## The process

1. **Resume.** If `edit/project.md` exists, summarise the last session in one line and ask whether to continue.
2. **Intake.** If he gives no path: `$Y/cap.py find` and confirm the recording. Not Cap: link the camera file as
   `source/cam.mov` (screen recordings as `source/screen.mp4` on one clock; a minimal `cap.json`). Collect the script,
   links and anything he wants shown. **Brand:** `$Y/brand.py init --edit-dir edit` (Stripe; `--brand x.json` for
   another company), then fetch the logos the brand file names from its official kit into `edit/logos/`. Test one
   scene in the brand before building the rest.
3. **Ingest + read.** `ffprobe`; a full-res still for the mirror check; `$R/transcribe.py source/cam.mov --edit-dir edit
   --vocab "<every name from script/links>"`; `$R/pack_transcripts.py`; `$R/headpose.py` over the whole take →
   `headpose_report.txt` (he reads notes between lines — the look-downs must go).
4. **Cut.** Cap trims → remove retakes, fillers (listed for veto), bloopers, dead air (Hard rules 3–4). Write `edl.json`
   (source `CAM`, 1920x1080 @ 30, fit crop, `grade: "auto"`, `end_hold: 0`), `$R/render.py edl.json -o edit/base.mp4
   --base-only`, `$R/verify_cuts.py edl.json` and fix every clipped word. **Transcribe every kept range on its own and
   every join with its neighbours**; drop any line that is still there twice, fragments of other takes, and slivers at
   range edges. Then `$Y/lookdowns.py --edit-dir edit` and `$Y/sync_check.py --edit-dir edit` (must say OK).
5. **Corrected transcript.** Build `transcripts/CAM.json` from per-range transcription mapped back to source time (the
   whole-file transcript smears word times at joins, ~1 s off), fix name spellings and misheard words, delete cut words.
   Captions, talk captions and scene words all come from it.
6. **Chapter outline → approval #1** (`references/planning.md` §1). Wait.
7. **Reference pass.** Everything he names: verify the real source (paper, study, post — read it, note the exact
   numbers), `$R/capture.py --readable --phrases`, `$R/fetch.py logo` / `photo` / `icon`; one sheet of logos/photos,
   confirm each (a "coat of arms" photo once turned out to be a jug — look at every asset).
8. **Beat table → approval #2** (`references/planning.md` §2). Wait.
9. **Build.**
   - Write `layout.json` (card face position from a still, windows, zoom targets, chapters, music, captions) and
     `animations/scenes.json` (`"look": "v7"`; each moment: id, type, start, duration, assets, brief in v7 terms with
     exact words + times, hero object + micro-animations, the one structural SFX if any). `$Y/compose.py plan`.
   - Callouts: `$Y/compose.py where <out_t> <sx> <sy>` → frame coordinates in the brief.
   - `$Y/board.py prepare --edit-dir edit`.
   - **Pilot**: build 2–3 representative scenes (one map/chain, one data, one board) and run `$Y/talkcaps.py`, render
     them, and show him stills before building the rest. Then one sub-agent per scene/family, all in one message (template
     scenes: `model: "sonnet"`; bespoke hero objects: the default model). Prompt:

     > Build scene `<id>`. Read `<skill>/references/style.md`, look at `<skill>/assets/style/stripe_youtube_sheet.jpg` and
     > the relevant file in `<skill>/examples/stripe-v1/` or `examples/yt-01-v7/`, then `<edit>/animations/<id>/TASK.md`. Work only inside
     > `<edit>/animations/<id>`. Do not ask questions. hf/index.html is the `<type>` starter on the runtime (read the
     > hf/board.js and hf/v7yt.js headers): keep the runtime and hf/brand.css untouched, colours only from the brand
     > tokens, write the copy, positions and the hero object. Frame 0 must show the heading or main object; no frame is
     > bare paper; nothing ever enters the speaker-card box.
     > EXACTLY the frame count in TASK.md. Snapshot the landings first, fix, then render ONLY with the board.py render
     > command in TASK.md and check the count. Never pkill or killall anything. Write beats.json (structural SFX only,
     > usually none). Scratch in qa/. Stop every background process before replying. Report path, frames, what the hero
     > object does, deviations.

   - Review every scene as it lands with `$Y/review.py --edit-dir edit <ids>` (frames 0 / 25 / 50 / 75 % / last with the
     card box outlined): frame 0 not empty, no bare-paper frame mid-travel, card zone clear at every pose, one focal point,
     readable, brand colours only, real assets, labels not over neighbours, on-screen words exactly his words. SendMessage
     fixes to the same agent. `$Y/board.py check` when all are in.
   - **Talk captions**: `$Y/talkcaps.py --edit-dir edit --dry-run` (read the phrases), check a still of each talk window
     for a calm caption area (`captions.y`), then run it for real and `board.py render --only <the cNN_talk ids>`.
10. **Music (default on for videos > 5 min).** ElevenLabs Music (`eleven_music_v2_5`), instrumental, calm, no vocals;
    describe the sound and a gentle arc. Generate 2 takes, pick the steadier one (lower LRA), and build a bed exactly the
    video's length: if the take is shorter, splice a second pass at a matching spot with a short (0.25 s) crossfade rather
    than letting it loop audibly; 1.5 s fade-in. Save to `edit/music/bed.mp3`, set `layout.json "music"`, log it in
    credits. Level: compose puts the ducked bed `music_under_voice_db` (default 5) under his voice — don't pre-gain files.
11. **Compose.** `$Y/compose.py render --edit-dir edit -o edit/preview.mp4 --preview` → `$Y/compose.py sheet --edit-dir
    edit edit/preview.mp4` → self-eval → `$Y/compose.py render --edit-dir edit -o edit/final.mp4` → `$Y/sync_check.py
    --edit-dir edit --skip-base --final final.mp4`. Cut a 25 s music/caption check clip for him if the mix changed.
    **Inserts** (a clip with its own sound, e.g. a reel's before/after mix — compose can't pause his voice for it): render
    compose to `final_raw.mp4`, build each with `$Y/inserts.py clip --edit-dir edit --src clip.mp4 --label before`
    (`--accent` for the "after"), pick each splice frame from the word times (after the line that introduces it, and
    before the next caption fades in), `$Y/inserts.py splice --edit-dir edit final_raw.mp4 final.mp4 --at F:clip …`,
    then look at the frames on both sides of every splice and check audio vs base after each one.
12. **Deliver.** `$Y/deliver.py srt`, `$Y/deliver.py chapters` (with inserts: `$Y/inserts.py shift --edit-dir edit
    --at F:seconds …` after both), `$Y/deliver.py stills edit/final.mp4 <2–4 strong
    moments>`, `$R/fetch.py credits`, **`deliver/description.txt` per `references/description.md`** (all lowercase, his
    newsletter + every link), append `project.md`. Copy final.mp4 (+ srt, chapters, description) to where he wants them
    (he has used ~/Downloads, md5-verified). Hand over + the reel-able moments (offer /adnaan-reel) + honest notes.
    Thumbnail: his Canva uploads hold photos of him; Canva's background remover needs a paid plan.

## Self-eval (before he sees anything)

- `ffprobe`: 1920x1080, 30 fps, frame count = base.mp4; audio −14 LUFS (±0.5), true peak < −1 dBTP.
- **Lip sync**: `sync_check.py` OK on the base AND the final (worst reliable offset ≤ 0.08 s). Watch his mouth at 3
  timestamps in the last third, where drift is largest.
- `compose.py sheet`: no raw/blank flash at any window boundary, card identical across windows, frame 0 of every scene
  shows content, **talk windows show HIM under the captions** (not paper — an opaque overlay).
- Talk captions: every talk window has them, readable on his background, no words running together, phrases break at
  sense points, every hero is a meaningful word.
- Music: compose printed the bed ~5 dB under the voice; listen to 20 s with speech and 5 s without.
- Every chapter opens with its map/heading; chapters.txt has no "!" warnings.
- Every named tool/company has its official logo; every page readable at 1080p (≥ 30 px text in frame).
- Base mix ≈ 70–85 % board; nothing static > 40 s without a reason.
- Captions SRT: read 3 random stretches against the video — words and timing right, names spelled right.
- Last 20 s: nothing important in the end-screen area.

## Memory — `project.md`

Append per session: source, look, chapters, cut decisions (Cap trims kept, retakes/fillers/bloopers removed, repeats
found per range, clipped-word fixes, look-down holds), moments with types, what he liked or rejected, music level,
outstanding items.

## Anti-patterns (each one happened — don't repeat)

- **Lip-sync drift**: per-range AAC clips joined with `-c copy` each keep ~17 ms of priming, so the voice slid later at
  every cut (+1.5 s by 4:00). render.py now builds the voice in one pass; `sync_check.py` must pass on base and final.
- **A music bed he can't hear**: a fixed −24 dB bed under wall-to-wall talk sat ~30 dB under him; he asked three times.
  compose levels it to ~5 dB under the voice now — don't hand-tune by pre-gaining files.
- **compose hanging at the end** (ffmpeg with `-stream_loop -1` + sidechain wrote a full mix and never exited): the bed is a
  plain/concat input atrim'd to the picture now. If a run sits at 0 % CPU with the mix written, kill only that ffmpeg pid.
- **Captions only on a few talk lines** — he asked where the rest were. Every full-frame talk window gets full coverage.
- **Captions over white buildings** — unreadable; place the column on a calm area (`captions.y`), check stills first.
- **Words running together** in tight Inter Tight 800 (`-.04em`) — keep `word-spacing: .16em`.
- **An overlay rendered as h264 .mov** — opaque, talk windows showed paper. Render through `board.py render` only.
- **Chain labels in the disc row** ran over the neighbours — labels go on empty paper above/below; one label at a time.
- **Agents each inventing a fix for a shared object** (chain labels) — fix it once in the shared module, re-render all.
- **`pkill -f "hyperframes render"`** from one agent killed every other agent's render.
- **Pauses left in** (0.3–0.9 s heads) and **a line said twice** (whisper merged two takes) — tighten per Hard rule 4,
  transcribe per range.
- **Look-downs at line starts** — hold a frame with lookdowns.py; don't leave the head coming back up.
- **An empty board at a scene's first frames** — entrances are `fromTo` with immediate render; frame 0 shows content.
- **Passing selector strings where elements are expected** — if a scene "does nothing" after a point, check the console.
- **Briefs written in the old marker vocabulary** — write v7 briefs (discs, rings, bars, cards) so agents don't translate.
- **A wrong asset** (a "coat of arms" that was a jug) — look at every downloaded image.
- **Guessing callout coordinates** — the zoom moves the screen; use `compose.py where`.
- **Accent flashing the old mint** — the runtime tweened two hard-coded colours that brand.css could not reach; V.mintTo
  / V.charcoalTo read the tokens now. Never type a hex in a scene.
- **Bare paper mid-scene** — a camera travel between two pages showed an empty board for half a second; overlap the move
  with the next object's entrance. Frame 0 AND every frame in between show content.
- **A zoomed card running through the speaker box** — at a close camera pose a table's rows sat under his card; clip the
  world out of the card box in screen space (a `#clip` around `#cam`) or move the pose.
- **Paraphrased words on screen** ("Technically correct" for "Technically it's correct") — on-screen text is his exact
  words; check every kinetic line against CAM.json.
- **Insert splices drifting** — each AAC insert carried ~12 ms of padding, so the voice after the splice was late; inserts.py
  trims every insert to its exact frame length. A splice placed before the caption change left the old caption on screen
  for 5 frames after the insert; splice just before the next phrase's caption fades in.
- **Whisper inventing a retake** ("…for you. Do it…") over one clean line — probe the range before cutting a "repeat".
- **Everything from adnaan-reel's anti-pattern list that applies** (invented data, words he didn't say, a test EDL in
  edit/, unverified joins, agents sharing a scratchpad, lingering monitors).
