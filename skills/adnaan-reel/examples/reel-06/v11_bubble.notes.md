# v11_bubble — THE BUBBLE → ZOOM OUT

Render: `render.mov` — 307 frames, 1080x1920 @30, ProRes 4444. `slots.py check --motion`: passed, no dead holds.
Bounds (diff vs background-only render, every frame, threshold 24): **x 60–959, y 287–1479**, 0 frames outside the zone.

## Key poses (as built, scene seconds)

| frame | s | on screen | lands on |
|---|---|---|---|
| 0 | 0.00 | secondary speaker card 560x500 centred (510,885), whole head in | "From" |
| 25 | 0.85 | "AI" (red, 176) | "AI" |
| 26–39 | 0.86–1.28 | red marker loop r≈392 round him; "bubble" lands at 1.01 | "bubble" |
| 39–46 | 1.30–1.55 | ink soap-bubble highlight arc + dash, upper-left inside the loop | — |
| 63/67/72 | 2.10/2.24/2.40 | ChatGPT, Claude, Codex stickers slap on (bubble flinches each time) | "taken over" |
| 90 | 3.00 | Anthropic sticker | "the" |
| 101–110 | 3.37–3.67 | "entire world." bottom-right (exits 4.62), red ✦ at 3.52 | "entire world" |
| 128–167 | 4.26–5.55 | OpenAI, Claude, ChatGPT, Anthropic stickers + 3 more ✦ | "every single place" (4.84/5.26/5.70) |
| 183–186 | 6.10–6.22 | "AI bubble" blurs up; "every single place." gets sucked into the pull | — |
| 185–188 | 6.18–6.28 | anticipation: 3-frame push IN to 1.035 | "you" |
| 188–214 | 6.28–7.13 | camera pull-back 1.035 → 0.125 (log scale, power3.out); paper grid zooms 3 octaves and lands on the identical grid; the bubble becomes a ~100 px red speck | "zoom" (IMPACT 6.30) |
| 195–216 | 6.50–7.2 | globe (screen r 340, centre 510,990) scales in with the camera from 8x, outline drawn as it arrives; latitudes, meridians, 4 continents | "out" 6.72 |
| 217–232 | 7.24–7.76 | pencil hatch on continents; red loop round the speck at 7.40 | "realize" |
| 259 | 8.62 | "zoom out" exits | — |
| 269 | 8.98 | "barely" (ink, 128) top-left | "barely" |
| 277–287 | 9.24–9.58 | 3 tiny red scratch marks on the globe just below the speck; "scratched" (red, 118) top-right | "scratched" |
| 290–306 | 9.68–10.2 | "the surface." under the globe; continents keep turning, strokes boil to the cut | "the surface" |

## Build

- Camera: `#zwrap > #zwrap2 > #zoom` (own wrapper inside #punch; #cam keeps the runtime's 1.006 push). `#zoom` scale = the camera,
  origin = bubble centre (510,880) = the speck. Two feathered CSS masks (vars parked off-frame until 6.15) clamp the
  camera layer to the zone during the move; top edge drops to y 540 at 6.38 so nothing sweeps under "zoom out".
- Globe in its own svg (`#gsvg`), drawn in screen units with `M.circle`/`M.line`/`M.hatch`, its group scaled 8.28 → 1 on the
  same ease as the camera; every globe stroke counter-scaled (stroke-width tween) so it lands at house weight. Continents in a
  globe-clipped group that drifts −34 px (rotation).
- Bubble loop strokes thicken 13 → 36 local units during the pull so the speck stays a readable red ring (~4.5 px).
- Zoom grid: `#zg1` (60 px) / `#zg2` (120 px) scale ×0.5 per octave with a cross-fade, same drift as #grid, swapped in/out.
- Beat A words live inside the camera (they get sucked away); "zoom out", "barely", "scratched", "the surface." are outside it.
- Stickers: official files only (`openai.png`, `anthropic.png`, `chatgpt.svg`, `claude.svg`, `codex.png`) on white die-cut discs/
  rounded squares with a soft shadow that tightens as they press down.

## Principles checklist

- **Contact frames on words**: hero words via runtime (start 0.2 s before); stickers contact on 2.10/2.24/2.40/3.00/4.26/4.70/5.12/5.55; loop starts 0.86 for "bubble" 1.01; pull starts 6.28 for "zoom" 6.44; speck loop 7.40 for "realize" 7.56; scratches 9.24–9.58 around "scratched" 9.40.
- **Anticipation**: 3-frame push-in before the pull-back; stickers start lifted & big (1.55) before slapping; hero words dip first.
- **Overshoot + settle**: stickers press to 0.93 + squash then back.out to rest; hero words 106 % → settle; doodles back.out(2.4).
- **Parts lag the whole**: bubble flinches 0–2 f after each slap; card → sheen; globe outline → latitudes → continents → hatch (staggered 0.06–0.12 s).
- **Arcs**: stickers fall with rotation into place; the camera move is radial about the speck (grid flows in on rays).
- **Squash/stretch on shapes only**: stickers (5 %, the paper sticker, per brief "tiny squash"), bubble loop wobble; never on type.
- **One focal point**: words → loop → each sticker in turn → camera → speck/loop → scratches. Beat A words leave before "zoom" lands.
- **Secondary action / no dead hold**: grid drift, soap-bubble wobble (1.3–6.2), sticker idle sway, doodle twinkle, marker boil on fours, continents turning, "zoom out" breathing, card float. slots.py: no dead holds.
- **One exaggerated beat**: the 1 → 0.125 camera yank on "zoom" (IMPACT), with the grid zoom.
- **Exits faster than entrances**: word exits 6 f blur-up; entrances 0.3–0.46 s.
- **One light direction / contact shadows**: sticker and card shadows down; stickers' shadows tighten on contact.
- **Not a static slide**: every frame moves (camera, boil, drift, wobble).

## Richness (hero + secondary)

- Hero: the bubble → camera pull-back → hand-drawn globe with the bubble as a speck ("zoom" / "out").
- Stickers slapping onto the inside of the bubble, bubble flinching (on "taken over", "every single place").
- Infinite-zoom paper grid during the pull-back ("zoom").
- Red loop calling out the speck ("realize"); 3 scratch marks on the surface ("scratched").
- Globe slowly turning + boiling to the cut (Beat C hold); ✦ doodles twinkling (Beat A).

## Deviations

- Bubble loop r≈392 (≈ 840 px incl. overshoot) rather than 900, to keep the loop's spiral-out end inside x 60–960.
- Card 560x500 (brief ~600 wide) so its corners clear the loop and the whole head (hair → chest) fits.
- Pass 2 (coordinator): stickers enlarged to 140–146 px outer (logo ~105–120 px, die-cut border scaled), re-laid round the ring, overlapping card edges/ring but never his face; highlight arc moved to 193–230° so it clears them; card face-at 0.555 for hair headroom with the corrected (un-mirrored) speaker.mp4.
- 8 stickers: the 5 official logos, with ChatGPT, Claude and Anthropic used twice, to crowd the bubble.
- Camera ends at 0.125 (brief ~0.12) so the grid zoom lands on exactly 3 octaves.
- Words shown are only the ones the brief names (AI bubble / entire world / every single place / zoom out / barely / scratched the surface); connectives omitted. "scratched the surface" split into "scratched" (top-right) + "the surface." (under the globe) because it does not fit one line at 110.
- Globe ≈ 690 px (brief ~800) to leave room for "zoom out"/"barely scratched" above it and "the surface." below it.
- Lint: 1 warning (duplicate img sources, intended re-use of logos).
