# v05_refine — key poses (written before animating)

Full-screen opaque scene, 1080x1920 @30, 8.466 s (254 f). Paper bg + 60px grid + vignette on every frame
(identical to v01_hook). Content zone x 60–960, y 285–1480.

| frame | t (s) | on screen | lands on |
|---|---|---|---|
| f0 | 0.00 | paper bg; coin 02 (220px, white) popping in; speaker card + README card start rising | "Second" (0.00) |
| f6 | 0.21 | coin 02 turns ocean (clip wipe + pulse); "second one," Newsreader 76 | "one," (0.21) |
| f17 | 0.55 | "Design" Newsreader 156 pops | "Design" (0.55) |
| f26 | 0.85 | "&" Fraunces italic ocean 190, extra overshoot | "and" (0.85) |
| f32 | 1.05 | "Refine." Newsreader 156 | "Refine." (1.05) |
| f34 | 1.12 | slug "0xdesign/design-plugin" Geist muted slides in | — |
| f38–47 | 1.28–1.55 | README card + speaker card exit (drop + fade, 2 f apart); "second one," exits up | — |
| f41–53 | 1.36–1.76 | coin + "Design & Refine." + slug compact to a header row at the top | — |
| f47 | 1.57 | "it" (T1 row 1) | "It" |
| f54 | 1.80 | card 1 dealt into the fan (arc + overshoot) | "actually" (1.79) |
| f63 | 2.09 | card 2 dealt; "makes" | "makes" (2.09) |
| f69 | 2.30 | card 3 dealt | — |
| f72 | 2.41 | "5" Fraunces italic ocean 220 hero pop | "five" (2.41) |
| f74 | 2.48 | card 4 dealt | — |
| f80 | 2.65 | card 5 dealt (last card) + "variations" Newsreader 136 | "variations" (2.65) |
| f96–111 | 3.19–3.71 | "of any UI"; ripple wave across the fan on "UI" | "of", "any", "UI" |
| f126 | 4.20 | black pill "</> my codebase" slides up under the fan | "from"/"my" (4.09–4.43) |
| f132–146 | 4.40–4.85 | dotted lines draw up from the pill to each card | "code base." (4.65–4.93) |
| f149–155 | 4.96–5.16 | T1 lines exit up; dotted lines fade; cursor enters on an arc | — |
| f156 | 5.19 | "I" | (I ~5.2, not in words.txt) |
| f161 | 5.37 | cursor clicks card 2 → lifts + flips to deep teal; "pick" Newsreader 204 hero | "pick" (5.37) |
| f177 | 5.91 | cursor clicks card 4 → lifts + flips; "what I like," complete | "like" (5.91) |
| f185 | 6.17 | T2 exits; unpicked cards recede (fade, blur, shrink); "and" | "and" (6.17) |
| f191 | 6.37 | picked cards fly together; "then" | "then" (6.37) |
| f198 | 6.59 | fuse → larger deep-teal merged card pops, ocean flash, tiny camera punch; "merges" Fraunces italic ocean 184 | "merges" (6.59) |
| f203 | 6.78 | black "merged" pill pops on the card corner | — |
| f207–228 | 6.91–7.59 | "it", "into my entire" | "it", "into", "my", "entire" |
| f225–237 | 7.50–7.90 | merged card anticipates up, then shrinks and drops into the codebase pill | — |
| f237 | 7.90 | contact: pill squashes, ocean ✓ badge pops; "code" | "code" (7.89) |
| f245 | 8.17 | ✓ stroke done, ring pulse; "base." | "base." (8.17) |
| f245–253 | 8.17–8.466 | hold alive (camera push, grid drift, float, ring); hard cut | — |

## As built (final)

**What it shows:** Skill #2 chapter. Coin 02 (220px) pops in white and turns ocean on "one,"; "second one," and then
"Design" / "&" (Fraunces italic ocean) / "Refine." land on the words. Behind them sit the live speaker card (560x390, the same
treatment as v01_hook: 3D tilt, ocean edge, face-centred crop at 20.5–59.6% of the source height, muted video) and the REAL README
(hf/assets/refine.png) in a tilted browser card (URL github.com/0xdesign/design-plugin), scrolled to its "Design and Refine" heading.
The title then compacts into a header row (coin 150px + "Design & Refine." + slug) that stays for the rest of the scene. Five white
wireframe cards are dealt into a fan. A black pill "</> my codebase" slides up under the fan, and dotted lines draw from the pill to
each card. The cursor clicks card 2, then card 4: each lifts and flips (real 3D) to deep teal with ocean accents. The picked cards fly
together and fuse into a larger deep-teal card with an ocean flash, a "merged" pill and a tiny camera punch, while the unpicked cards
recede. The merged card then drops and tucks into the codebase pill (squash, ocean ✓ badge, ring pulse) and holds into the hard cut.

**Timeline (slot seconds):**
- 0.00–0.62: the coin, speaker card and README card rise in and settle (all three are already on screen at frame 0). Coin turns ocean 0.12–0.44.
- 0.08 "second", 0.24 "one,", 0.55 "Design", 0.85 "&" (extra overshoot), 1.05 "Refine.", 1.10 slug.
- 1.20–1.47: README card, then speaker card, exit (drop + fade). 1.30: "second one," exits up.
- 1.34–1.85: the title compacts into the header ("Design" first; "& Refine." and the slug travel together on an arc).
- Deals: 1.56, 1.80, 2.00, 2.20, 2.40 (each card settles about 0.4 s later). "it" 1.57, "actually" 1.79, "makes" 2.09,
  "5" 2.41 (hero), "variations" 2.65, "of" 3.19, "any" 3.43, "UI" 3.71. A ripple runs across the fan from 3.50 to 3.95.
- 3.98–4.48: the pill rises in (contact ~4.2). 4.36–4.88: the dotted lines draw in (centre first, then outward). 4.80–5.1: T1 exits. 5.06–5.28: the lines fade.
- 4.98: the cursor arcs in. Clicks at 5.30–5.40 (card 2 lifts and flips from 5.37) and 5.83–5.93 (card 4 from 5.91). The cursor leaves at 6.04–6.28.
- "I" 5.19, "pick" 5.37 (hero), "what" 5.61, "I" 5.79, "like," 5.91. T2 exits at 6.02.
- 6.15: the unpicked cards recede. 6.28–6.52: the picked cards fly together. 6.48–6.61: the merged card pops (contact 6.59 on "merges"), with the flash and a 1% camera punch.
  6.70: the "merged" pill. "and" 6.17, "then" 6.37, "it" 6.49, "merges" 6.59 (hero), "it" 6.91, "into" 7.09, "my" 7.35, "entire" 7.59.
- 7.48: the "merged" pill fades. 7.56: the card anticipates upward. 7.66–7.90: it drops and tucks into the pill. 7.90: the pill squashes and grows to 116%. 7.86–8.22: the ✓ badge pops and its tick draws.
  8.00: ring pulse. "code" 7.89, "base." 8.17. It holds alive until 8.466 (camera push, grid drift, pill bob); there is no exit, because the scene ends on a hard cut.
- Continuous: 20px grid drift, camera push 1.0→1.015, card floats, coin bob.

**Measured content bounds over all 254 frames** (render diffed against a background-only render): x 64–957, y 296–1473. That is inside the 60–960 / 285–1480 zone.

**Deviations from the brief:**
- The kinetic text matches words.txt instead of the still's paraphrases: "I pick what I like," (not "pick what you like,"), and
  "and then / it merges it / into my entire / code base." (not "it merges them"). The "I" before "pick" is missing from words.txt, so it is placed at ~5.19 s.
  "5" for "five" and "&" for "and" follow the brief and the approved still.
- The pill reads "</> my codebase" instead of "</> your codebase", to match the spoken "from my code base".
- A secondary speaker card was added to the chapter beat (as instructed: embed the speaker video). It sits in front of the README browser card
  and clears at 1.2–1.47 s, before the fan deals in.
- The merged card does not vanish into the pill. It tucks into it (about 60% visible above it) so the end frame still shows the result.
- Fan cards are 188x276 (spacing 160, ±8° outer tilt), not the still's wider spread, which ran past x 960.
- The header is set at 0.575× the chapter size (90px) so "Refine." clears x 960 under the camera push and punch.
- Words near the bottom of the zone ("of any UI", "what I like,", "code base.") land from slightly above rather than rising through the zone edge.
