# reel-08 v7 "mint" style test — the reference for the v7 look (approved 2026-10-17, hook variant A)

Four consecutive beats of reel-08 (0–15.7 s), built on the reel-08 runtime + scene-level code that is now `v7.css`/`v7.js`:

| scene | mode | what it shows | now in the runtime as |
|---|---|---|---|
| `t1_hook.html` | TALK + depth | frame-0 text hook, CEO photo cards slide out from BEHIND his head (matte layering), captions on his chest | `talk_depth` starter, `.spk.matte`, `.v7-behind` |
| `t1_hook_variantB.html` | TALK | the rejected flat variant (cards in front) — kept for comparison | — |
| `t2_ceos.html` | TALK | charcoal + glow captions as a "feed", mint hero words with a dark shadow, one icon disc | `talk` starter, `.g7`, `V.disc` |
| `t3_six.html` | TALK → shrink | his footage shrinks into disc 1 of the habit chain; connector draws, discs pop as it arrives; greedy tug | `chain` starter, `V.shrink`, `V.chain`, `V.chainDraw` |
| `t4_stanford.html` | VISUAL | opens on t3's exact end state; face disc flips to the mint mic disc; camera pushes in, travels to the real strip (mint highlighter), flat race, peach 3× | `visual` starter, `V.placed`/`V.chainEnd`, `V.cam`/`V.pose`, `.v7-zone`, `.v7-hl` |

`SHARED_v7.md` is the brief the agents had; `slots.json` the four briefs. Contact sheet: `assets/style/v8_contact_sheet.jpg`.
Lessons: mint words over light clothing need a dark shadow and hero size (supporting words stay charcoal); the TALK chest band
is only ~330 px tall, so phrases build as a feed; in depth shots there is little room beside his head — slide objects out from
behind his shoulders rather than placing a giant word behind him.
