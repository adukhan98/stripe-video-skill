---
name: adnaan-reel
description: Adnaan's house reel style. Turns a raw talking-head take (plus an optional script, links, screen recordings or screenshots) into a finished vertical reel where EVERY beat is a full-screen animated scene in the v7 "MINT" look (house default since 2026-10-17) — TALK beats with him full-screen and our heavy kinetic grotesk captions (Inter Tight 900 + Inter; charcoal with a soft glow, one mint hero word) instead of subtitles, sometimes with objects sliding out from BEHIND him (depth via his background-removed matte); VISUAL beats on a grey paper board with a strong vignette where white Phosphor glyphs sit in mint/charcoal icon discs, a disc CHAIN maps the list, the camera travels across a world bigger than the frame, and props are clean flat vector illustrations; the SIGNATURE SHRINK (his full-screen footage shrinks into the current chain disc or a small left-side card, and grows back for the payoff); an optional frame-0 text hook; the real pages/posts/repos he mentions as big READABLE cards with a mint highlighter behind the spoken phrase; the official logo of every tool/company he names; mint + charcoal with peach for data only (no red, no hand-drawn marker); rich motion on Lasseter's principles; IG safe zones (nothing in the lower-right icon corner); sparse low & warm ElevenLabs SFX on structural beats only (the 30 % rule) and an ElevenLabs music bed ducked under the voice. The legacy red paper + hand-drawn marker look stays available (init-brand --look paper). Use whenever Adnaan drops footage and says "edit this reel", "edit this like the last one", "/adnaan-reel", or wants a reel/short/TikTok made from a talking-head take. Cuts tight on word boundaries (fillers out automatically), shows a beat table for approval, then builds all scenes in parallel with HyperFrames, assembles, self-checks and renders. Offers a 16:9 version.
---

# adnaan-reel

Adnaan's footage in → a reel that looks exactly like the approved reference edit out. Before anything
else, **look at `assets/style/v8_contact_sheet.jpg`** — the approved reel-08 style test of the **v7 "MINT" look**, the house
default since 2026-10-17 (scenes in `examples/reel-08-v7/`): TALK beats with him full-screen + our kinetic captions, VISUAL
beats on a grey board with icon discs, a disc chain and a travelling camera, the signature shrink. **Read
`references/style.md` "v7" first** — it overrides the older sections wherever they conflict; the v6 sound rules, safe zones,
readability rules and motion principles still apply. The art direction is binding and lives in `references/style.md`; the
scene grammar (how a reel is split into scenes and which scene types exist) is in `references/scenes.md`. **The look is
code**: the shared runtime `templates/runtime/paper.css` + `paper.js` (world, kinetic type, primitives, Lasseter-principled
motion) + `v7.css` + `v7.js` (v7: icon discs, the disc chain, shrink/grow into a disc or card, camera, zone mask) plus one
starter per scene type in `templates/scenes/` (v7: `talk`, `talk_depth`, `visual`, `chain`, `card`); `slots.py prepare`
installs them into every scene, so a scene is ~150 lines of copy, positions and one bespoke object.
**The legacy PAPER look** (red paper + hand-drawn marker layer `marker.css`/`marker.js`, split band, reel-06/07 —
`assets/style/v6_contact_sheet.jpg`, `v7_contact_sheet.jpg`, `examples/reel-06/`, `reel-07/`) is `init-brand --look paper`,
only when he asks for it. Older idea banks: `examples/reel-04/`, `reel-05/` and `references/motion-ideas.md` (the serif
editorial look: `examples/reel-03/`, `init-brand --type editorial`).

You never watch the video — you **read** it: a word-level transcript, filmstrips at decision points,
and verify tools that transcribe the joins.

## Principles

1. **Every beat is a scene, in one of two MODES (v7).** The whole reel is 8–18 full-screen HyperFrames scenes back
   to back over the locked cut, and every beat picks a mode in the beat table: **TALK** (him full-screen, our kinetic
   captions on him — hook, transitions, opinions, payoffs, CTA; `talk`, or `talk_depth` when something sits BEHIND him)
   and **VISUAL** (no speaker; the board, icon discs, flat vector props, real pages, a travelling camera — every
   explanation, list item, example; `visual`). He is on screen about **50 %** of the reel; no Visual stretch over ~8 s
   without him. The **signature shrink** (1–3 per reel: his footage shrinks into the current chain disc or the small
   left-side card, `chain` / `card`; `V.grow` brings him back for the payoff) links the modes. The small card appears
   0–2 times. A list reel's map is the **disc chain** (`V.chain`). A long screen recording is the `demo` type.
2. **The words are the captions.** No subtitles. Kinetic Inter Tight 900 phrases land on their spoken
   words, big (hero 170–270 px authored, ×0.94 house `--type-scale`; accent by colour, no italics; v7: charcoal with a
   soft glow on his footage, ONE mint hero word, mint only at hero size). On-screen words are only words he actually
   says (ASR spellings of names fixed) — plus an optional **text hook** he writes (frame-0 headline).
3. **Show the real thing, with the real logo.** Every product, repo, site, file or framework he names appears
   for real: captured page in a browser card, real repo slugs, star counts, real headings and part names.
   **Every tool or company he names gets its official logo** (`fetch.py logo`, logged as `official`), shown
   unaltered as an `<img>` in a chip/pill next to the name or on the app card — never redrawn, recoloured
   or substituted with a text-only pill when a logo exists. Illustrative UI is fine; invented numbers,
   quotes or posts are not.
4. **Approve the plan, then build everything.** One beat table → approval → all scenes built in
   parallel → assembled → self-checked → delivered. Autopilot ("just do it") skips the wait.
5. **Never bland, always animated.** Each scene has a hero idea with real motion (things deal, open, merge,
   stack, ride dotted paths, flip from grey to accent) plus continuous life, and every move obeys Lasseter's
   principles (`references/animation-principles.md`: anticipation, overshoot + settle, overlap, arcs, staging,
   secondary action, one exaggerated beat, exits faster than entrances). The runtime does this by default;
   bespoke objects must too. If a scene could be a static slide, redo it. **Richness is the house level
   (reel-05), tempered by v6:** about two focal elements at a time and 35–50 % of the grid empty (content-dependent
   guidelines, not hard gates) — a hero object + 1–3 secondary micro-animations that act out the sentence — a cursor that does
   the thing, real numbers rolling to their value, icons that come alive, soft physics, characters with
   personality, type that performs, hero icons landing on their word (`references/motion-ideas.md`).
6. **Clean flat vector on top (v7) — no hand-drawn marker in the mint look.** Icon discs with white Phosphor glyphs
   (`fetch.py icon`, `V.disc`), clean vector strokes that draw themselves (connectors, an underline bar, a magnifier rim —
   even width, no boil), flat vector hero objects with personality in motion, a mint highlighter behind real text.
   Peach is for data only. (The legacy paper look keeps the red felt-tip marker + Caveat notes, `hf/marker.js`.)
7. **Readable, always.** Everything inside the safe zone (measured), real pages as big strips (≥ 0.85, ~45 px text)
   with a highlighter behind the spoken phrase, no semi-transparent text, words over his clothing legible (v7: charcoal +
   glow, mint at hero size; paper look: on solid paper),
   chips/logos/doodles big enough for a phone. He asked for this explicitly. **IG safe zones (v6):** nothing in the
   bottom 20 % and nothing right of x 900 below y 1200 (Like/Comment/Share) — CTAs sit bottom-left/centre.
8. **Sound supports the voice — the 30 % rule (v6).** No Mickey-Mousing: 1–2 punchy tactile sounds in 0:00–0:04, then
   only structural transitions (point 1/2/3, a mode switch, a big screenshot sliding in, the CTA landing) — ~10–14 cues in
   70 s, from the low & warm v6 kit (`assets/sfx/v6_*`: stamp, clunk, thud, paper, whoosh, pop), low-passed at 5 kHz.
   Agents tag those beats `"role": "hook" | "structural"` in `beats.json`; `scenes.py edl` (default `--sfx-policy sop`)
   leaves everything else silent. **Mix:** voice up front, SFX −16…−22 dB, an ElevenLabs Music bed (instrumental, timed to
   the arc) −22…−26 dB under speech via `--music`, +2.5 dB over the final 3 s.
9. **Verify before showing.** Every join transcribed, every scene check-sheeted, the assembled reel
   flash-scanned and sampled. If you wouldn't post it, don't present it.

## Hard rules

1. **Beat table approved before scenes are built** (unless autopilot).
2. **Per-segment extract → lossless concat** for the cut (render.py), 30 ms audio fades at joins,
   never cut inside a word, pad edges, word-level transcripts only, cached per source.
3. **Every filler cut and every join verified** with `verify_cuts.py` — whisper ends words early, and
   `audio_env.py tighten` eats soft word endings ("code", "immediately", "base", "use" were all clipped
   in the reference edit; "works" lost its "s" on reel-05 while ASR still read "works"). Read every join
   line AND its ⚠ TAIL/HEAD energy flag (deliberate filler cuts flag too — that's expected); extend a range
   end to the suggested time when a real word is cut, re-probe until clean.
4. **Never render a partial or test EDL from `edit/`.** render.py writes `base.mp4` and `timeline.json`
   next to the EDL — a test EDL in `edit/` overwrites the real base. Preview one scene with
   `scenes.py preview <id>`; test cuts with `verify_cuts.py --probe`.
5. **Scene EDLs come from `scenes.py edl` only.** It frame-snaps every scene, pre-rolls 12 ms and holds
   each scene 0.1 s under the next — without that, render.py's overlay sync leaks ONE raw footage frame
   at every scene boundary. Then `scenes.py flashcheck <render> --edit-dir edit`: 0 unexpected raw-footage
   frames (it compares every frame with base.mp4 — reel-05's ceiling was paper-coloured, so the old corner test
   was blind; the planned `fullscreen` / `demo` windows come from slots.json and are expected).
6. **One sub-agent per scene, all spawned in one message.** Review each `check_sheet.jpg` /
   `motion_strip.jpg` as they land; send fixes to the same agent with SendMessage (it keeps context).
   Every scene is **exactly** its TASK.md frame count (slots.py presets it and `check` enforces it) —
   verify all counts with ffprobe before `scenes.py edl`; a 1-frame miss is a gap or an overlap at a cut.
7. **Brand fidelity through the runtime.** Scenes use `paper.css`/`paper.js` + `v7.css`/`v7.js` (mint) or `marker.css`/`marker.js` (paper) as installed — never edited,
   never re-implemented per scene (a scene with its own card or word engine is rejected at review). Only
   brand.css tokens; bundled fonts asserted loaded; never draw or recolour a logo (real ones from official
   files only, logged); one accent. Never clone a paid font — if he wants a commercial face, he buys the
   licence and drops the file in; until then use the closest OFL face (Bootzy TM → Inter Tight 900, the
   current default). A global change (font, card size, easing) is made ONCE in `templates/runtime/`, then
   `scenes.py runtime` + `scenes.py rerender`.
8. **Downloads through `fetch.py`, captures through `capture.py`** (both log source + rights);
   `fetch.py credits` → `credits.md` before delivery. Third-party pages are shown as commentary on the
   thing he's recommending, framed in browser cards, never passed off as his.
9. **All outputs in `<project>/edit/`.** Never write inside the skill directory.
10. **Mirror check before the cut**: zoom into any text or logo on his clothing/background in a full-res still
    (the filmstrip is too small — reel-06's backwards "SAN DIEGO" patch was only caught at scene review and cost a
    re-cut of every speaker clip). Backwards → `"mirror": true`.
11. **Readability is a review gate** (style.md "Readability"): a scene with an out-of-zone pixel, an unreadable page,
    ghosted text, words on dark fabric or a phone-small chip/doodle goes back to its agent.
12. **Trust timestamps, not reports**: after an agent says "re-rendered", check `render.mov` is newer than its inputs
    (reel-06 v01 reported a re-render that never landed).

## Setup

Same toolchain as video-edit (details in `install.md`): ffmpeg/ffprobe with libass + zscale, `uv`
(helpers run as `uv run --project <skill_dir> <skill_dir>/helpers/<name>.py …`), transcription
(ElevenLabs key → Scribe; else Apple Silicon `mlx` via `uv sync --extra mlx`; else whisper.cpp), Node 22+
for HyperFrames (`npx --yes hyperframes …`), Google Chrome for `capture.py`. `<skill_dir>` is the folder
containing this file (`~/.claude/skills/adnaan-reel`).

**Freshness (once per session, before any render):** the skill calls `npx --yes hyperframes` unpinned, which
resolves to the newest published CLI (scene `package.json` pins are only used by `npm run`, which we never
call). Confirm with `npx --yes hyperframes --version` vs `npm view hyperframes version`, and run
`npx --yes hyperframes skills check` → `npx --yes hyperframes skills update` when any HyperFrames skill is
outdated (they were 10 behind on 2026-10-14). Note the CLI version in `project.md`; if a render looks
different from the previous reel after a bump, say so.

## Helpers

| Helper | What it does |
|---|---|
| `scenes.py init-brand --edit-dir E [--look mint\|paper] (mint = v7 house default) [--accent red\|ocean\|…\|#hex] (paper look only; red default) [--type grotesk\|editorial] [--type-scale 0.94] --frame still.jpg` | Copy bundled fonts (grotesk default: Inter Tight + Inter + Geist Mono; editorial: Newsreader + Fraunces + Geist), write `brand.json` (house palette + accent + `"look"`), copy `references/style.md` → `animations/SHARED.md`, run `brand_kit.py build`, append `--type-scale` (house 0.94) and — mint look — the v7 tokens (charcoal ink, mint-soft, mint panel, peach, disc shadow, strong vignette) to brand.css |
| `fetch.py icon <name…> --edit-dir E [--weight fill]` | v7 icon-disc glyphs: Phosphor (MIT) SVGs → `icons/<name>.svg`, logged `open-source`; list them in a slot's `"assets"` as `icons/<name>.svg`, use as `V.disc({icon: name})` (names: phosphoricons.com) |
| `scenes.py words --edit-dir E` | Every cut segment with output start, frame and words — choose scene boundaries here |
| `scenes.py cut-speaker --edit-dir E [--only ids]` | Per scene: `base.mp4` window → `hf/assets/speaker.mp4` (muted; frame-exact seek; last scene padded with the end-hold freeze) + `speaker_cut.webm` (his matte) for `talk_depth` / `cutout` scenes + copy the scene's `"assets"`; `--only` after a mid-build cut fix |
| `scenes.py edl --edit-dir E [--beat-gain-offset -3]` | `edl.json` + `animations/slots.json` + renders → `edl_scenes.json` (frame-snapped, pre-roll, 0.1 s holds, no captions) + every scene's `beats.json` → timed `audio[]` cues from the ElevenLabs kit |
| `scenes.py preview <id> --edit-dir E` | One scene with its voice → `verify/<id>_preview.mp4` (safe: never touches base) |
| `scenes.py flashcheck <video> --edit-dir E [--allow]` | Frames that match base.mp4 (= raw footage showing) outside the planned `talk`/`talk_depth`/`chain`/`card`/`fullscreen`/`demo` windows (must be 0); without `--edit-dir` a corner-colour test that tolerates a scene's own vignette |
| `scenes.py runtime --edit-dir E` / `scenes.py rerender --edit-dir E [--jobs 4] [--only ids]` | Re-install the shared runtime into every scene / re-render all scenes in parallel and verify frame counts — a whole-reel restyle (new font, card size, easing) in minutes |
| `capture.py <url> --edit-dir E --name n --readable --phrases "a\|b" [--context 1] [--selector article]` | **v5 default for anything whose text is read on screen** (posts, articles, READMEs): light mode, narrow @3x → `captures/n.png` + one whole-line strip per phrase `n_<k>.png` + `n.strips.json` (each strip's highlight box for `M.highlight`) + `n.layout.json` (all line boxes, to cut header/stats strips by hand) |
| `scenes.py seam A B --edit-dir E` | Continuity: A's last frame beside B's first + mean diff → `verify/seam_A__B.jpg` (a recurring drawing must not jump at the cut) |
| `capture.py <url> --edit-dir E --name n --uploader owner [--simple]` | Chrome via puppeteer-core (installed once to `.cache/`): desktop UA (gets past bot walls), scrolls the page so scroll-reveal content renders, strips cookie banners/fixed overlays → 540 px @2x tall `captures/n.png`, logged for credits |
| `slots.py prepare --edit-dir E` / `slots.py check <slot_dir> --motion --at …` | Scaffold scene projects: HyperFrames init + brand kit + **runtime (paper.css/js + v7.css/js + marker) + the `type` starter (mint look default: first/last `talk`, others `visual`) as hf/index.html (duration preset) + `words.html`** (every spoken word as a timed span) + TASK.md with the principles checklist; QA a scene render |
| `transcribe.py` / `transcribe_batch.py` (`--vocab "Names, Products"`), `pack_transcripts.py` | Word-level transcript (cached) → `takes_packed.md` |
| `audio_env.py islands / tighten --min-gap 0.25 / snap / profile` | Real speech spans; tight jump-cut ranges; quiet cut points |
| `verify_cuts.py edl.json` / `--source v --probe a:b,c:d` | Transcribe every join / candidate joins; ⚠ TAIL (sound continues after a range end — a clipped soft ending, with a suggested end) / HEAD (onset before a start) energy flags |
| `headpose.py --edl edl.json` | Edges where he looks down at notes |
| `timeline_view.py <video> <start> <end> -o png` | Filmstrip + waveform (keep ranges ≤ ~15 s) |
| `render.py <edl> -o out.mp4 [--base-only] [--preview] [--reuse-base] [--sheet]` | Cut → composite scenes → SFX → loudness (−14 LUFS) |
| `fetch.py logo "<Name>" --edit-dir E [--domain site] [--github org] [--simple slug]` | Official logo of a named tool/company → `logos/<slug>.svg|png`, logged `official` (GitHub org avatar → the site's own icon → Simple Icons → favicon; else ask for the press-kit file) |
| `fetch.py tweet <x.com URL or id> --edit-dir E [--check "phrase he reads"]` | Real text, author, date and attached images/video of a public X post, no login (the embed syndication endpoint) → `posts/<id>/media-k.jpg|mp4` + `posts/<id>.json`, logged `commentary`. `--check` prints OK / NOT IN POST for the phrase he shows. Long posts come back cut at ~280 chars (says so) — the readable strip still comes from `capture.py --readable` on the x.com URL; the embed URL it prints is the fallback when x.com shows a login wall |
| `fetch.py photo "<Name or thing>" --edit-dir E [--min-width 800] [--n 2]` | Real photo of a person/place/thing → `photos/<slug>.jpg|png`: Wikipedia lead image, then Wikimedia Commons (ranked by title match, then size), licence + author logged for credits; falls back to a smaller file with a WARNING; never AI, never watermarked |
| `fetch.py url / find / search / log / credits` | yt-dlp downloads and rights log; `credits.md` |
| `assets/sfx/` (README) | ElevenLabs SFX v2 house kit: pop, tick, impact, riser (peaks 0.45 s in), whoosh, ping, ding + `scribble` (felt-tip on paper, 3 variants, trimmed to the stroke's `dur`) — default gains in `scenes.py` `BEAT_GAIN_DB`; legacy synth `subdrop`/`chime`/`flick`/`ticks` |
| `brand_kit.py`, `captions.py`, `grade.py`, `platforms.py`, `storyboard.py`, `sfx_synth.py` | Inherited from video-edit; used indirectly (`sfx_synth.py` never overwrites the ElevenLabs whoosh/ping) |

## Layout

```
<project>/
├── <source take(s), untouched>        (often ~/Downloads/<UUID>.MP4 — find with mdfind if not given)
└── edit/
    ├── project.md                      session memory
    ├── transcripts/<source>.json       raw (cached) + corrected copy named after the EDL source key
    ├── takes_packed.md, edl.json, base.mp4, timeline.json
    ├── brand/ (brand.json, brand.css, DESIGN.md, fonts/)
    ├── captures/ (page screenshots)  downloads/ (manifest.json)
    ├── animations/ (SHARED.md, SLOT_BRIEF.md, slots.json, <id>/hf/{index.html,assets/}, <id>/render.mov …)
    ├── edl_scenes.json, preview.mp4, final.mp4 (+ final_16x9.mp4), credits.md, verify/
```

## The process

1. **Resume.** If `edit/project.md` exists, summarise the last session in one line and ask whether to
   continue. Otherwise start fresh — never reuse another reel's scenes or assets unless asked.
2. **Intake.** Find the take (path in chat, the project folder, or `mdfind` recent movies in Downloads/
   Desktop — confirm the right one from a still: same outfit/setting as any screenshot he sent). Collect
   the script, links and any screen recordings/screenshots. Don't ask about format or style — this is the
   house style. Ask only what the material raises (e.g. a CTA word that differs between script and take:
   default to what he says on camera).
3. **Footage.** `ffprobe` (often 4K HEVC 30 fps); `transcribe.py --vocab` with every name from the script
   and links; `pack_transcripts.py`; one `timeline_view` of the opening — **text reads backwards → front
   camera → `"mirror": true`** — and since the filmstrip is too small to read, also pull a full-res still and zoom
   into any print/logo on his clothes or the background (Hard rule 10); `audio_env.py islands`.
4. **Cut.** `audio_env.py tighten <take> 0-<end> --min-gap 0.25` → ranges. **Fillers cut automatically**
   (listed in the beat table for veto): sentence-start "So", throat-clearers, a sentence that restates the
   previous one, "and you should see results"-type tails before the CTA. `verify_cuts.py --probe` each
   filler cut. Write `edl.json`: `output` 1080x1920@30 `fit: crop`, `mirror`, `grade: "auto"`,
   `end_hold: 1.6`, no zooms, no captions. `render.py edl.json -o edit/base.mp4 --base-only` (full
   quality — scenes embed it), then `verify_cuts.py edl.json` and fix every clipped word (Hard rule 3),
   `headpose.py --edl`. Re-render the base after fixes.
5. **Corrected transcript.** Copy the raw transcript to `transcripts/<EDL source key>.json`, fix name
   spellings (e.g. "TasteKill" → "Taste Skill", "cloud" → "Claude", "mentor" → "Meng To") and delete the
   words you cut — scenes' `words.txt` is generated from it.
6. **Brand.** `ffmpeg -ss 3 -i base.mp4 -frames:v 1 edit/still.jpg`;
   `scenes.py init-brand --edit-dir edit --frame edit/still.jpg` (the **mint look** is the default since 2026-10-17;
   `--look paper` = the legacy red paper + marker, only if he asks). Note his clothing from the still: dark clothing →
   TALK captions in white (`.w7`) instead of charcoal + glow; write it in SHARED.md "Project specifics".
7. **Reference pass.** List every concrete thing he names — and every **implicit artifact**: a number, a quote,
   "people are saying", "I read / I saw", "X did Y" almost always has a real post, headline, pricing page or
   chart behind it; it goes on the list even without a proper noun. For each entry write **one sentence: what is
   this line actually about?** and source *that*, not the keyword ("Zaria from Duolingo" is about the account
   she built, not the Duolingo logo; "what Karpathy said" is his post, not his face; "the show" is the show's
   branding, not one episode). Find and **verify** the real source (WebSearch;
   `curl https://api.github.com/repos/<owner>/<repo>` for repos — stars, description; raw README for
   details), then capture: **`capture.py --readable --phrases …`** for anything whose words are read on screen (a
   post, an article, a README section — one strip per spoken number/phrase, highlight boxes included), plain
   `capture.py` for a page that is only scrolled as a visual. **For every tool and company named**
   (Claude Code, Cursor, Adobe, GitHub, Figma…): `fetch.py logo "<Name>" --edit-dir edit --domain <site>
   [--github <org>]` → `logos/` (the App Store icon is tried first for apps — 1024 px colour icon, seller
   printed; then the site's icon, Simple Icons, GitHub avatar, favicon). **Every person he names**:
   `fetch.py photo "<Name>"` → `photos/` (Wikipedia/Commons, licence logged) — **but a face the audience
   would not recognise is dead on screen**: for a niche person show their *work* (the post, repo, product, talk)
   and keep the photo small or drop it; famous faces appear in context, not as a static portrait. **Posts**:
   `fetch.py tweet <url> --check "<phrase he shows>"` verifies the quote against the real text and saves the
   attached image/video at full size. **Clips of a person** (`fetch.py find`): search the *moment*, not the name —
   "<person> <what the line says they did/said>" — and before using one fill in "in this clip X is <doing what,
   where, when>"; if that sentence can't be filled, it is not the clip. **Product demos must be the current
   version** — check the upload date, prefer his own recording > the official channel > nothing. Open `logos/` + `photos/` as
   one sheet and confirm each is the real mark / the right person, current version, not a lookalike org
   or a parent-company logo. If none is found, ask him for the press-kit file or photo. **Asset rules** (from
   mistakes, ours and others'): no stand-in logo (parent company, older version, sister product); no
   AI-generated images; no watermarked files; icons ≥ 512 px, pictures ≥ 800 px wide or flagged; a borrowed
   clip appears once per reel and freezes on its moment before it cuts to anything off-topic; never accept
   cookie/terms dialogs while capturing (close them or use another page); a whole page shrunk to phone size
   is unreadable — crop to the phrase and highlight it on the spoken word (the readable strip). List every
   logo/photo/capture/clip in the scene's `"assets"`. Note real data for briefs (star counts, file headings,
   part names, skill names). **Source by source, not by beat**: one `--readable` capture of a page gives every
   strip that page is quoted for, one official video gives every window it is used for — fetch once, crop
   many; never re-fetch for a second beat. **Fail fast**: a method that fails once is switched (another
   fetcher, another page, Claude in Chrome), a second failure marks the asset MISSING in the beat table and
   moves on — never a third attempt, never a stand-in. Map his own media to the words it illustrates:
   screenshots / short clips → inside browser or device cards in a scene; a long recording where the
   screen action itself is the point → a **full-bleed demo scene** (recording fills the frame, small
   floating speaker card top-right, kinetic phrase at the bottom; `flashcheck --allow` for that window).
8. **Plan → beat table → approval.** `scenes.py words` → choose 8–14 scene boundaries on segment starts
   (`references/scenes.md` §1) and a scene type for each (§2). Show ONE compact table and wait:

   | # | Time | He says | Scene | What happens on screen | Real assets | Hero beat |
   |---|---|---|---|---|---|---|

   "What happens on screen" names the hero object AND its 2–3 secondary micro-animations (motion-ideas.md) AND
   (mint look) the icon discs / chain / camera move / shrink, (paper look) what the marker draws;
   "Hero beat" is the word that gets the `impact`. "Real assets" starts with the one-line *about* from step 7
   when the asset is not the obvious noun ("about: the account she built → her profile strip, not the logo").

   Add a **Mode** column (v7 mint): `TALK` (him full-screen; `TALK+depth` when something sits behind him) / `VISUAL`
   (board) / `SHRINK→disc` or `SHRINK→card` for the signature transition (1–3 per reel; `GROW` for the reverse) / `CARD`
   (0–2 per reel, left side). TALK for the hook, transitions, opinions, payoffs, CTA — about **50 %** of the reel; VISUAL
   for every explanation, list item, example. A list reel gets a **disc chain** (icons per item; geometry fixed in
   SHARED.md); key-point reels a 2–3 disc chain; story/opinion reels none. (Paper look: the v6 `A`/`B`/`C` modes.) Also
   list the **SFX cues** (≈ 10–14: the 1–2 hook sounds and each structural beat) and the **music** plan (ElevenLabs Music,
   instrumental, how it builds). Two **content-dependent checks** go in the table as notes, never as hard
   rules: (a) **Absence** — a VISUAL stretch longer than ~8 s gets a reason or a TALK/CARD beat; (b) **Length** — any beat longer than ~7 s gets a note on whether it should be two scenes (a second
   composition is what makes the picture visibly change; pushes and micro-motion don't read at thumbnail
   size). Under it: running time, the filler cuts made, name fixes, CTA word, look (mint unless he asks for paper),
   the logos and icons fetched (and any missing), open questions, "Want a text hook on the first frame?" (if he hasn't given one) and
   "Want a 16:9 version too?". Iterate until approved.
9. **Build.** Write `animations/slots.json` (`layout: "scene"`, **`"type"`** = starter per
   `references/scenes.md` §2, `"bespoke": true` where the hero object must be invented, briefs per §3 with
   exact copy and word times, the MODE(s) and any switch time, the hero object + 1–3 named micro-animations, the
   structural beat(s) that get a sound, `"assets"` (incl. `icons/<name>.svg` from `fetch.py icon`); v7 types: `talk`,
   `talk_depth` (→ `cut-speaker` makes `speaker_cut.webm`, his matte), `visual`, `chain`, `card`),
   fill the "Project specifics" section of
   `animations/SHARED.md` (list length/coins, **face centre as a fraction of source height** — it becomes
   `<body data-face>`, his clothing colour (light → charcoal + glow captions; dark → white `.w7`), the real assets with
   their strip highlight boxes, the real labels allowed as data, and the **fixed geometry + icons of the disc chain**
   (points, diameter, icon per item, which scene shrinks into which disc) — see `examples/reel-08-v7/SHARED_v7.md`
   for the pattern), then `slots.py prepare --edit-dir edit` → `scenes.py cut-speaker --edit-dir
   edit` (prepare BEFORE cut-speaker: HyperFrames init refuses a non-empty folder). `prepare` prints one
   prompt per scene tagged *template* or *bespoke*. Spawn **one sub-agent per scene in a single message**:
   template scenes (`talk` captions-only, `demo`; paper look: `hook`, `chapter_page`, `opinion`, `wrapup`, `cta`) →
   `model: "sonnet"`; bespoke scenes (`visual`, `chain`, `card`, `talk_depth`, anything with a new object) → the default
   strong model. Prompt:

   > Build scene `<id>`. Read `<edit>/animations/SLOT_BRIEF.md`, then `<edit>/animations/SHARED.md` (fully;
   > look at the style images it lists — v8_contact_sheet / the v7 mint look is the target), then
   > `<edit>/animations/<id>/TASK.md`. Work only inside `<edit>/animations/<id>`. Do not ask questions. hf/index.html is
   > already the `<type>` starter on the shared runtime (hf/paper.js and hf/v7.js — read both headers; no marker layer in
   > the mint look): keep the runtime untouched, paste the words from words.html, set sizes/positions, and build the
   > bespoke object on `P.*` + `V.*` + GSAP [bespoke: the idea is `<what it does>`; study
   > `<skill_dir>/examples/reel-08-v7/<closest>.html` for the idea only]. EXACTLY the
   > frame count in TASK.md. Snapshot your landings before rendering; render; slots.py check --motion --at;
   > ffprobe the count; measure bounds; answer the principles + richness + readability checklists in NOTES.md;
   > write beats.json (tag only the hook/structural beats that get a sound with "role"); fix collisions, cropped faces, small or
   > unreadable type, ghosted text, empty lower zone, dead holds. Scratch files go in
   > `<slot>/qa/`. Stop every background process before replying. Report path, check line, frames, bounds,
   > key timings, what is new, deviations.

   Template scenes take ~10–15 min, bespoke ~20–30 at the house richness level; keep working while they run.
   Review every sheet as it lands (`references/scenes.md` §4, incl. the richness AND readability questions) and
   SendMessage concrete fixes (reel-06/08 sent ~1 fix pass per scene: bigger cards/chips/icons, no ghosted text, words
   = his words, continuity with the previous scene — expect it, it is where the polish comes from). After a
   speaker-clip fix (`cut-speaker --only`) ask that scene's agent to re-render. For scenes sharing a drawing, run
   `scenes.py seam A B`. If an agent keeps re-sending its report, it left a monitor running: tell it to stop, then
   TaskStop it.
   **A cut fix after scenes exist** (e.g. a clipped tail found by an agent): change the range, re-render the
   base, add the delta to that scene's `duration` and to every later `start` in slots.json (the content of later
   scenes is unchanged), `scenes.py cut-speaker --only <id>`, update its TASK.md/slot.json frame count and have
   its agent extend the scene — later scenes need no re-render.
10. **Music (v6, default).** Generate the bed with ElevenLabs Music (full ElevenLabs connector; `eleven_music_v2_5`,
    `lyrics_type: instrumental`, `duration_seconds` = reel length + 0.5): describe the SOUND and how its energy follows the
    reel's arc (quiet hook story, lift into point 1, a layer per point, swell on the payoff line, resolve under the CTA).
    3 takes; pick by a 2 s loudness curve against the beat times (`edit/music/`); log it in credits.md.
11. **Assemble.** `scenes.py edl --edit-dir edit --music music/<take>.mp3` (sop SFX policy + ducked bed + CTA lift)
    → `render.py edl_scenes.json -o edit/preview.mp4 --preview --reuse-base --sheet` → `scenes.py flashcheck
    edit/preview.mp4 --edit-dir edit` → self-eval (SFX count ≈ 10–14; voice clearly on top) → final:
    `render.py edl_scenes.json -o edit/final.mp4 --reuse-base` → flashcheck again → `fetch.py credits`
    → append `project.md` → deliver the file with a short scene list and the honest notes (illustrative
    elements, anything off-palette, words omitted).
12. **Restyle (if he asks for a global change after seeing it).** Fonts, card sizes, easing strength,
    palette: change `templates/runtime/` (or brand.css) once → `scenes.py runtime --edit-dir edit` →
    `scenes.py rerender --edit-dir edit` → `scenes.py edl` → render → flashcheck. No agents involved.
13. **16:9 (if asked).** Separate pass: an EDL copy with `output` 1920x1080 in `edit/landscape/`
    (its own base + timeline there, paths `../`), slots re-prepared at 1920x1080 with the same briefs
    re-laid out (speaker card left ~⅓, kinetic stack right, safe zone from `platforms.py youtube`),
    re-rendered scenes, `final_16x9.mp4`.

## Self-eval (before he sees anything)

- `scenes.py flashcheck --edit-dir edit` → 0 unexpected raw-footage frames (talk/chain/card/fullscreen/demo windows expected).
- Every VISUAL scene has its hero object + micro-animations (+ marker work in the paper look); every scene has a `beats.json`.
- **v7 mint**: him ~50 % of the reel (TALK), no VISUAL stretch > ~8 s without him, the small card ≤ 2 and left side only,
  the signature shrink 1–3 times and landing exactly on its disc/card, the chain identical across scenes (`scenes.py seam`),
  no red and no marker boil anywhere, peach only on data, mint words only at hero size over his footage.
- **v6 (both looks)**: each beat in its planned MODE; no unplanned floating card; about two focal elements at a time and real white
  space; nothing right of x 900 below y 1200; ~10–14 SFX cues, none high or sharp; music under the voice, lifted for the CTA.
- Readability: strips readable at phone size, no ghosted text, everything in the zone (style.md "Readability").
- `scenes.py seam` clean on every cut between scenes that share a drawing.
- Every named tool/company shows its official logo (compare `logos/` with the beat table's names).
- **Borrowed footage auto-reject** (no judgement call — any one fails the scene): burned-in captions or
  subtitles from the source, a stranger's name-tag / lower third, a watermark or channel bug, letterboxing
  inside the card, a page still showing a consent dialog, a stand-in logo or old version, a photo of someone
  the audience would not recognise standing in for their work.
- Absence + length notes from the beat table honoured: no unexplained VISUAL stretch > ~8 s without him, no
  unexplained scene > ~7 s. **Muted test**: watch 0–3 s with the sound off — topic clear, reason to stay?
- Contact sheet (`--sheet`) and one frame per scene at full size: same board/paper world in every VISUAL scene, type
  at the style.md sizes, collage-staggered phrases, accent on 1–2 words, whole head in every split band / card,
  no text over his face, lower 40 % of the zone not left empty,
  real assets legible, nothing outside x 60–960 / y 285–1480, no scene reads as a static slide.
- **Lip sync**: compare the face in 3–5 scene cards with `base.mp4` at the same output times — mouth
  shapes must match (a mis-trimmed speaker clip shows here).
- On-screen words vs `words.txt` per scene: no paraphrase, no invented claims, names spelled right.
- `verify_cuts.py edl.json` reads as the intended script at every join; no pause ≥ 0.25 s left.
- Audio: render.py prints LUFS/peak — expect ≈ −14 LUFS, < −1 dBTP; SFX quieter than speech. Voice Isolator
  (ElevenLabs) only if the room noise between sentences is above −45 dB (`verify_cuts` prints the floor; reel-05: −54).
- `ffprobe` final: 1080x1920, 30 fps, expected duration.

## Cut craft

- Audio-first: cut on word boundaries and silences (≥ 0.4 s cleanest; 0.15–0.4 s usable with a check).
- `tighten --min-gap 0.25` keeps natural rhythm; 0.16 chops mid-phrase. Islands are the truth when
  whisper smears pauses into one long word.
- Fillers glued to the next word have no silence: find the dip (`audio_env.py profile`), probe 2–4
  points with `verify_cuts.py --probe`, keep the one that transcribes clean.
- Head moves are cut edges too: end tight (≤ 30 ms) when he looks down after a line.
- Never reason audio and video independently — every cut must work on both.

## EDL notes

`edl.json` is the cut only (ranges, output, mirror, grade, end_hold). `edl_scenes.json` adds the scene
overlays (written by `scenes.py edl` — don't hand-edit timing), `sfx_gain_db: -13`, the hook `subdrop`
on range 0, and `audio[]` — one cue per `beats.json` entry (kit file, scene start + t − 0.02 s, riser 0.45 s
earlier, per-tag gain). A slot's legacy `"sfx"` is used only when it has no beats.json. SFX only — no music
unless he asks (then `fetch.py` CC bed, `duck: true`, two options).

## Memory — `project.md`

Append per session: source, brand/accent, cut decisions (fillers removed, clipped-word fixes), scene list
with types, deviations, what he liked or rejected, outstanding items.

## Anti-patterns (each one happened once — don't repeat it)

- **Mint words at supporting size over his footage** (reel-08 v7 test): mint on a light glow or a light-grey sweatshirt
  washes out. Charcoal + glow for everything; ONE mint hero word at ≥ 170 with the dark shadow.
- **A giant word "behind" him with no room** (reel-08 hook): his head fills the frame; behind-him objects slide out from
  behind his SHOULDERS where they stay readable — never a hero word 80 % hidden.
- **A chain that jumps at the cut**: the next scene opens on the previous scene's exact end state (`V.chain` + `V.chainEnd`
  + `V.placed` with the same geometry); `scenes.py seam` before approving.
- **One frame of the previous take on a scene's frame 0** (reel-08): `cut-speaker` used to seek to a rounded start; it is
  frame-exact now — don't hand-cut speaker clips with `-ss {start:.3f}`.
- **A floating corner box on every scene** (reel-06/07 v5: small/secondary/portrait cards everywhere). His SOP: split /
  canvas / full-or-cutout; cards are a rare choice, not the frame of every beat.
- **Mickey-Mousing the sound** (reel-07 v5: 330 cues — a pop, tick or scribble on every word, check and stroke). Sound on
  ~30 % of the moves: hook 1–2, then structural beats only, low & warm, under the voice.
- **High, sharp SFX** (dings, ticks, marker squeaks, rising whistles) that fight vocal consonants on phone speakers.
- **A CTA or pill in the lower-right corner** under the Like/Comment/Share icons.
- **Removing the doodles to "clean up"** — he explicitly keeps the sketchbook doodles; v6 cleans up by mode and spacing.
- **A real post shrunk into an unreadable card** (reel-06 style frame 1: "way too small to even read"). Narrow
  `--readable` capture, one strip at a time, ≥ 0.85.
- **Marker loops drawn across lines of page text** — they cover the words. Highlighter behind the phrase instead.
- **Ghosted text**: phrases receding to 50–70 % and lingering (reel-06 v04, v05, v10, v12 first passes). Text is
  fully readable or gone; recede objects, not words.
- **Doodles, chips and stickers at "desktop" size** (70 px doodles, 32 px chip labels). Size for a phone.
- **Words on dark clothing** with only a glow behind them. Solid paper strip/panel.
- **A recurring drawing that jumps at a cut** (stick-people pile differing between v04 and v05). Copy the previous
  scene's final state; `scenes.py seam`.
- **A mirrored take not noticed until scene review**. Zoom into clothing text before cutting.

- **The bland edit**: raw face beats + scrolling screenshots + two small cards. Every beat is a designed scene.
- **The keyword asset**: the Duolingo logo for a line about the person who ran the account; a headshot for
  "what she wrote"; a bare-name clip of a famous person that has nothing to do with the sentence. Write
  "what is this line about?" first (step 7), then source that.
- **The third attempt**: an hour on one stubborn capture while the edit waits. Switch once, then mark MISSING.
- **A face circle cropped to the forehead.** Cards, not circles; always crop to the face and look.
- **Small type.** He asked for bigger: hero ≥ 170 px (Inter Tight), nothing under 64 px, fill the zone.
- **Landscape cards that crop his hair / a small face on his own opinion beats.** He wants to see more of
  himself: since v6 that is the Mode A split band (edge to edge, whole head) or a full/cutout beat.
- **Scenes off by one frame** (`round(dur × fps)` instead of the frame-snapped window) → a gap or overlap at
  a cut. Exact counts from TASK.md; ffprobe every render.
- **Top-heavy scenes**: graphics in the upper half, empty lower 40 % for seconds. Fill the zone.
- **Hard outlines, offset shadows, cream paper, coral-on-cream "brutalist" cards** — rejected looks.
- **A text-only pill for a tool that has a logo**, or a logo redrawn as a glyph. Fetch the official file.
- **Full screen everywhere** (or never): it is a per-beat decision — 2–4 beats (Mode C), the ones about him.
- **Words he didn't say** ("are literally" for "is literally", "pick what you like" for "I pick what I like").
- **A test render from `edit/`** that silently replaced `base.mp4` and `timeline.json`.
- **Hand-built scene overlays** → one raw frame flashing between every scene. Use `scenes.py edl`.
- **Trusting tighten's ranges** without `verify_cuts` → clipped word endings.
- **Inventing data** (scores, fake posts). Real numbers from the real page, or none.
- **Spawning scene agents one by one**, or respawning instead of SendMessage-ing fixes.
- **Twelve agents re-typing the same 450 lines** (world, card, word engine) with drift between scenes, and a
  restyle that rebuilt every scene (reel-04 v1→v2: 23 min). The runtime + starters exist so that never
  happens again; a scene that re-implements them is sent back.
- **Rendering to find out** — a full render is 35–80 s per try; `hyperframes snapshot --at` is seconds.
- **Tweens without principles**: fade+slide "template" motion, no anticipation, nothing overshoots, groups
  moving as a block, linear eases on things that stop. Lasseter's list is the floor.
- **Correct but not engaging** (reel-05 v2): every scene right, but one object per scene. He asked for "more
  creative, more engaging". The richness level (motion-ideas.md) is now the first-pass floor.
- **A clipped soft ending the transcript didn't show** ("works" → "work"): read the ⚠ TAIL flags.
- **Agents sharing one scratchpad** — they overwrote each other's bounds scripts and reference renders, and one
  `rm -rf`'d another's folder. Scratch lives in `<slot>/qa/`.
- **An agent with a lingering monitor** re-sent its report a dozen times. Agents stop their background work
  before replying; TaskStop the stragglers.
- **Hand-placed SFX cues** (reel-05: a 193-cue script by hand). Agents write beats.json; `scenes.py edl` mixes.
