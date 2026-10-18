# v08_perfect — speaker + verdict (V2: portrait card, Inter Tight)

Full-screen opaque scene, 1080x1920 @30, 3.800 s (114 frames). Shared paper + 60 px grid + vignette on every frame
(frame 0 is paper only; the card rises from frame 1). v1 is backed up in `edit/animations_v1/`.

**V2 look:** a PORTRAIT hero card (820x1072 at x100 y304, radius 34, gentle tilt rotY -5→-4°, rotX 3→2.5°, ocean
edge, shadow, sheen, float), card styling from v01_hook. Video 820x1458, top -252 → window 17.3–90.8 % of the source
height: full head + shoulders + sweatshirt, face centre ≈ 34 % of the card, hair never cut. The kinetic stack sits
OVER the lower part of the card (on the sweatshirt, below the beard) and on the paper just below it. Type is Inter
Tight 900 (heroes) / 800 (supporting) with the paper-glow text-shadow, accent = colour, no italics. Pills are in Inter 600.
Font asserts: 900/800/700 'Inter Tight', 500/600 Inter.

## Key poses

| frame | t (s) | on screen | word |
|---|---|---|---|
| f0 | 0.00 | paper only; card starts at +120 px, rotX 16°, rotY -14°, scale .88 | now |
| f3–8 | 0.10–0.25 | card readable; "are" (Inter Tight 800, 100) rises over the sweatshirt | are |
| f11 | 0.37 | "they" | they |
| f21 | 0.69 | HERO "perfect?" (Inter Tight 900 ink, 220, baseline 1316) hits 102 %, settles | perfect |
| f24–32 | 0.80–1.06 | ocean strike-through draws across it; black pill "✗ no" pops under the "?" (it is part of the word's line) | no |
| f29–38 | 0.95–1.28 | "are they" blurs out; "perfect?" + strike + pill shrink up together as one row (42 %, baseline 1090); the pill then slides out right and rises beside the word | but |
| f35–42 | 1.16–1.39 | "do they" (800, 84, baseline 1191) | do, they |
| f47 | 1.57 | HERO "work?" (900 ocean, 196, baseline 1362, sitting just above the card's ocean edge) hits 106 %, settles | work |
| f58–63 | 1.94–2.11 | black pill on the "do they" row: ocean check disc draws + "definitely" | definitely |
| f68–74 | 2.26–2.48 | pill grows, "yes" lands; big ocean ✓ draws beside "work?"; 1 % camera punch; "work?" bumps 4 % | yes |
| f80–92 | 2.66–3.06 | the "perfect? ✗ no" row fades to 50 % | which actually |
| f91–107 | 3.02–3.55 | "makes me" (800, 68) then "wonder" (900 ink, 88) on the paper under the card, baseline 1466 | makes, me, wonder |
| f103–113 | 3.44–3.80 | dotted "?" loop draws after "wonder", ocean dot pops | — |

## As built (slot seconds)

- 0.00–0.56 card rise + 3D settle (y 120→0, rotX 16→3, rotY -14→-5, inner video 1.16→1), sheen 0.06–0.75; float 3 px.
- 0.10 "are", 0.24 "they" · 0.49–0.69 "perfect?" pop (peak 102 %, no rotation), settle to 1.01.
- 0.80–1.06 strike · 0.74 pill "✗ no" pop (contact 0.91), ✗ strokes draw 0.84 / 0.94.
- 0.95 "are they" exits · 0.98–1.26 the row shrinks up; pill slides right 1.08–1.26, rises 1.13–1.28 inside the row.
- 1.16 "do", 1.26 "they" · 1.37–1.57 "work?" pop, settle to 1.89.
- 1.94 pill "definitely" (contact 2.11) · 2.31 grows, "yes" 2.33 · 2.26–2.56 big ✓ · 2.36 punch 1 % · 2.40 "work?" bump.
- 2.66–3.06 the "perfect?" row dims · 3.02 "makes", 3.20 "me", 3.39 "wonder" (contact 3.55) · 3.44–3.74 dotted "?", 3.66 dot.
- Continuous: grid drift, camera push 1→1.008, card float + slow orbit, video push 1→1.03, pill float, ✓ breathe.

## Deviations

- Card is 820x1072 (brief ~840x1050): it is narrower so his face is smaller and the chin ends higher (≈ y 990), leaving room for the 4-row stack below the beard. It is taller so its bottom edge (y 1376) sits in the gap between "work?" and "makes me wonder" and never cuts through a word. The edge reads as an underline under "work?".
- Type sizes are set by the vertical room under the face (y ~1020–1478): "perfect?" 220 (fits the width, overshoot 102 %), "work?" 196, compact "perfect?" ≈ 92, "do they" 84, "makes me" 68 + "wonder" 88.
- "work?" gets a slightly wider third glow layer, because it sits over his hand.
- The row shrinks on "but" (0.98), not on "work", so "do they" (spoken 1.23) has room; "do they" lands ~0.06 s late.
- Omitted the spoken "now", "but" and "which actually".
- An inline copy of the brand.css @font-face rules is in index.html to satisfy the renderer's font guard.

## Bounds

Rendered without the background (alpha > 50 %), all 114 frames: **x 62–955, y 286–1478**. Text never overlaps the face:
the stack's top (≈ y 1020) stays below the beard (≈ y 990–1010 across the clip).
