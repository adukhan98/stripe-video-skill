# stripe-v1: the first video made with this skill

A 6-minute walkthrough of how the editing pipeline works, edited in Stripe's brand (11,027 frames at 30 fps, −14 LUFS).
Frames are in `../../assets/style/stripe_youtube_sheet.jpg`.

| file | what it is |
|---|---|
| `beat_table.md` | the approved beat table (approval #2): every moment with its words, times, type and hero object |
| `scenes.json` | the scene list board.py prepared (briefs written in v7 terms) |
| `layout.json` | card position, windows, chapters, music, caption placement |
| `brand.json` | the brand file the video used (same as `brand/stripe.json`, minus the logo note) |
| `scenes/m01_stages/` | the disc-chain map plus its shared module (`chain_common.js`, `CHAIN_SHARED.md`), which m02–m10 copied |
| `scenes/s04_chores/` | a stacked-card list that drops in under the heading |
| `scenes/s17_brandfile/` | a real brand.json card with highlighted keys, branching to what each key controls |
| `scenes/s19_table/` | a zoomed table card, clipped out of the speaker-card box at every camera pose |
| `scenes/s25_list/` | a real page with the highlighter on the spoken phrase |

These files are `hf/index.html` plus the scene's own modules only. Running one needs the runtime (`board.py prepare`
installs board.css/js, v7yt.css/js, brand.css, icons and fonts). The renders are not included.
