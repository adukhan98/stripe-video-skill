# adnaan-reel

Adnaan's house reel style, as a Claude Code skill. A raw talking-head take (+ optional script, links,
screen recordings) becomes a vertical reel where every beat is a full-screen animated scene in the
editorial "paper world": grey paper with a drifting grid, kinetic grotesk phrases (Inter Tight 900 + Inter) instead of subtitles,
the speaker as a floating tilted video card, soft tactile objects (numbered coins, UI cards, black
pills, an agent puck, dotted paths), real pages and repos in browser cards, one accent (Ocean), SFX only.

Forked from the `video-edit` skill (same cutting/transcription/render toolchain) and specialised:

- `SKILL.md` — the process (cut → beat table → parallel scene build → assemble → verify)
- `references/style.md` — binding art direction; `references/scenes.md` — scene grammar + briefs
- `assets/style/` — frames of the approved reference reel (`v2_contact_sheet.jpg`) + accent options
- `assets/fonts/` — Inter Tight, Inter, Geist Mono (OFL); `assets/fonts/editorial/` — Newsreader, Fraunces italic, Geist (the v1 serif look, `init-brand --type editorial`)
- `examples/reel-04/` — the twelve scene compositions of the current reference reel (v2: grotesk type, portrait cards) + notes + slots + EDL
- `examples/reel-03/` — the ten scenes of the earlier editorial (serif) reel — still good component code
- `templates/runtime/` — `paper.css` + `paper.js`, the shared scene runtime (world, speaker cards, kinetic type, primitives, Lasseter-principled moves); installed into every scene by `slots.py prepare`, re-installed by `scenes.py runtime`
- `templates/scenes/` — one starter per scene type (hook, chapter_page, explainer, mechanism, opinion, wrapup, cta, demo, blank) built on the runtime; a scene is ~120–200 lines of copy, positions and one bespoke object
- `helpers/scenes.py` — brand init, scene planning, speaker clips, scene EDL (flash-free), preview, flashcheck
- `helpers/capture.py` — phone-width page captures for browser cards
- `helpers/fetch.py logo|photo|tweet` — official logos (App Store icon first), Wikipedia/Commons photos with licences, X post text + media without login

Install: `git clone https://github.com/adukhan98/adnaan-reel ~/.claude/skills/adnaan-reel && cd ~/.claude/skills/adnaan-reel && uv sync` (private repo).
Use: drop the footage in a folder and say "edit this reel" (or `/adnaan-reel`).
Setup: see `install.md` (ffmpeg, uv, transcription, Node 22+, Chrome). Model cache is shared with
video-edit (`~/.cache/video-edit/models`).
