# stripe-youtube

The Stripe edition of Adnaan's long-form YouTube skill, for Claude Code. It is the 16:9 sibling of `adnaan-reel`.
A Cap recording (or a camera take plus screen recordings) becomes a 5–15 min explainer, talk or walkthrough. It uses the
v7 design system on a 16:9 board, coloured from **one brand file**. Stripe is the default (`brand/stripe.json`: blurple
accent, slate discs and ink, cool paper, white cards). A finished video has:
- the speaker's plain camera in a fixed rounded card with an accent ring
- full-frame talk with full-coverage kinetic captions
- icon discs and disc-chain maps, flat white cards, real pages with a highlighter, data in one data colour
- zoomed screen recordings in a window card, and before/after inserts that carry their own sound
- a ducked music bed ~5 dB under the voice, with lip sync verified
- an SRT, chapters and a description

For another company, write another brand file and run `helpers/brand.py init --brand x.json`.

- `SKILL.md` — the process (ingest → cut → look-downs → chapter outline → beat table → pilot → build moments in parallel →
  talk captions → music → compose → sync check → deliver)
- `references/style.md` — the binding look; `references/planning.md` — chapters, beats, cadence;
  `references/description.md` — the YouTube description and his links
- `brand/stripe.json` — the default brand (colours, captions, logo sources; logos themselves are not vendored)
- `assets/style/stripe_youtube_sheet.jpg` — frames of the first Stripe-brand video; `v7_youtube_sheet.jpg` — the same system in mint (`greg_light/dark.jpg` = legacy)
- `assets/icons/` — Phosphor fill icons board.py copies into every v7 scene
- `examples/stripe-v1/` — the Stripe video: beat table, layout, chain/brand-card/page/table modules
- `examples/yt-01-v7/` — reference scenes: chain map + shared module, data bars, proof page, board flow, talk captions
- `templates/runtime/` — `board.css/js` (16:9 board world, motion) + `v7yt.css/js` (v7 tokens, discs, chains, cards,
  rings, highlighter) + `marker.css/js` (legacy)
- `templates/scenes/` — starters: canvas, map, board, proof, talk_overlay, callout_overlay, talk_captions
- `helpers/cap.py` (Cap ingest), `board.py` (scene projects, v7 runtime, slot-limited render), `talkcaps.py`
  (full-coverage talk captions), `lookdowns.py` (hold frames over look-downs), `sync_check.py` (lip sync, base + final),
  `zoomplan.py` (click-driven zoom camera), `compose.py` (the long-form compositor, auto-levelled music),
  `deliver.py` (SRT, chapters, thumbnails), `brand.py` (brand file → brand.css → every scene),
  `review.py` (per-scene review sheets), `inserts.py` (clips with their own audio, spliced frame-exact)

Requires `~/.claude/skills/adnaan-reel` (its helpers and Python environment are reused):
`uv run --project ~/.claude/skills/adnaan-reel python helpers/<name>.py …`. Plus ffmpeg, Node 22+ (`npx hyperframes`),
Chrome (captures). Tests: `uv run --project ~/.claude/skills/adnaan-reel --group dev pytest -q tests`.
