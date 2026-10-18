# v01_hook — notes (V2 revision, 2026-10-11)

v1 is backed up in edit/animations_v1/v01_hook. V2 changes: Inter Tight 900/800 replaces Newsreader/Fraunces (no italics; accent = colour);
PORTRAIT hero card shows him at full height; kinetic words land OVER the lower card (on the sweatshirt) with the paper glow.

Full-screen opaque scene, 1080x1920 @30, 4.433 s = 133 frames (verified). Paper bg + 60px grid (drifts 20x12 px) + vignette on every frame.
Font assert: 900/800/700 100px "Inter Tight", 500/600 40px "Inter".

## Layout
- Text hook (user copy, landed on frame 0, stays all scene): "Software is" Inter Tight 900 92 (x76, base 368) / "cooked" 900 184 ocean,
  right-aligned to 940 (base 508) + hand-drawn ocean underline / "and finished" 900 92 (x84, base 612). Hook spans y 296–614.
  Slow 1% punch + 3px float.
- Portrait speaker card 740x810 at x140 y630 (bottom 1440, ocean edge to ~1454), radius 34, rotY -10→-5→-3.5, rotX 8→3→2.2.
  Video 740x1316, window 16.5%–78% of source height: full head (about 36 px above the hair), shoulders, sweatshirt, hands; eyes ≈ 40% of card height.
  ~90% settled on frame 0 (y -10, scale .97, small extra tilt), settles by 0.32 s. Sheen 0–0.7 s, float 4 px, video push 1→1.012 (origin at the eyes).
- Kinetic words sit below his chin (beard bottom ≈ y 1235–1260) over the sweatshirt, with text-shadow glow; nothing crosses his face.
- App tiles: isometric stack of 5 (card / deep, wireframe glyphs, no logos), ~1.25x the v1 size (scale 1.5 vs 1.2, 25 px layer pitch), centred x 800,
  y ~1120–1475, overlapping the card's lower-right edge, to the right of his beard.

## Timeline (scene seconds)
| t | on screen | word |
|---|---|---|
| 0.00 | thumbnail: hook + card ~90% settled | Is |
| 0.00–0.20 | "is it" (800, 96, x76 base 1298, left of his beard) | is, it |
| 0.40→0.56 | "possible" (900, 176, ink, base 1438) pops | possible |
| 0.68–0.95 | "is it / possible" blur up | — |
| 0.88→1.08 | "reverse" (900, 170, ocean, base 1372) hero pop to 108%, settle; 0.4% camera punch | reverse |
| 1.28→1.44 | "engineer" (900, 120, ink, right-aligned 936, base 1446) | engineer |
| 1.62–1.89 | reverse / engineer blur up (2 f apart) | — |
| 1.75–1.95 | "all" "the" (800, 96, base 1418) | all, the |
| 2.12→2.32 | "apps" (900, 190, ocean) hero pop to 108% | apps |
| 2.92–3.12 | blur up | — |
| 3.12→3.25 | "every" (800, 70, base 1322); tiles drop in, 3 f stagger 3.14–3.54 | every |
| 3.72→3.85 | "single"; top tile lifts (anticipation) and sinks back | single |
| 4.09→4.29 | "day?" (900, 150, ocean, base 1442) hero pop to 110%; top tile splits into 3 exploded layers + dotted guides | day? |
| 4.29–4.433 | hold alive to the hard cut | — |

Measured content bbox over all 133 frames (diff vs background-only render, threshold 24): x 65–954, y 287–1479.

## Deviations
- Card 740 wide (coordinator: ~840). At 840 the face fills the card and leaves only ~130 px of sweatshirt under the chin, which isn't
  enough for the words without crossing his face or cutting off his hair. 740 gives eyes at 40% and ~200 px of sweatshirt.
- Card height 810 (bottom 1440 rather than 1470): the hook needs y 296–614, and the card's soft shadow has to stay inside y 1480.
- "engineer" 120, "every single" 70 and "day?" 150 sit under the hero floors so two rows fit in the strip between his chin and y 1480.
- "to" (of "is it possible to") and "that you use" are omitted: they collided with the next phrase in the short strip under his chin.
- Tile stack ~1.25x (not 1.5x): at 1.5x its exploded layers reach his cheek.
