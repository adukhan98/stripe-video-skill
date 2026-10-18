# examples/reel-07 — "be more ambitious" (Felix Rieseberg's article), the first reel on the v6 three-mode system

18 scenes, 70.4 s. Built first on the v5 look (floating cards, dense SFX), then rebuilt on Adnaan's SOP (2026-10-15):
- **Mode A split**: v01 hook, v04 (after "impossible"), v06, v09, v14 (payoff), v15 (opening), v18 CTA.
- **Mode B canvas**: v02 board, v03, v07 ①, v08 deck/boss, v10 ②, v11 200 ms, v13 ③ robot, v14 checklist, v15 gauge, v16.
- **Mode C**: v04 "impossible" + v12 "surprised" + v17 "ask" full screen; **v05 cutout** in front of the real dark article.
- Mode switches inside scenes: v04 `fullToSplit`, v14 `splitIn` (data-at), v15 `splitOut`.
- Sound: `sound_v6.py` — the 12 hand-placed cues this reel shipped with (stamp + clunk hook; thud on ①②③; paper on the
  strip/article; whoosh on mode switches; pop on the takeaways list and the CTA) + the ElevenLabs Music bed with the
  +2.5 dB CTA lift. The skill now does this from beats.json roles (`scenes.py edl --sfx-policy sop --music …`).
- `freeze_lookdowns.py` — holds the last eyes-on-lens frame where he glanced at his notes at a cut edge (video only).
Recurring drawings: THE BOARD (v02→v03), THE GAUGE (v15→v16), circled ①②③. Contact sheet: assets/style/v7_contact_sheet.jpg.
