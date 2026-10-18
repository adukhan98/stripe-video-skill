# v07_adobe — key poses + as built (V2 type)

**V2 revision (2026-10-11):** type system swapped per SHARED.md "V2 UPDATE": kinetic words Inter Tight (heroes 900, −0.045em;
supporting 800, −0.03em; line-height 0.88), accent = colour, no italics. Heroes: "seven" 250 + "AI" 270 ocean; "someone"/"else" 176,
"rebuild" 170, "open source." 140 ink. Supporting: "last week" 100, "also" 96 / "used" 120, "to" 100, "applications of" 82 / "Adobe" 96.
UI text (chip names 42/slugs 23, "★ 47.2k stars", "all open source", URL, coin numbers) = Inter 600/500. Font asserts:
900/800/700 100px "Inter Tight", 500/600 40px "Inter". Re-fit: page card shrinks to 0.34 (was 0.37) so "seven" clears it;
coins dealt 0.08 s later (contacts 3.20…3.60) so they no longer cross the exiting beat-A words.

Full-screen opaque scene, 1080x1920 @30, **167 frames** (authored `data-duration` 5.549 s; the renderer ceils 166.47 → 167, as the assembler needs: placed at frame 1054, next scene at 1221).
Same paper bg + 60 px grid drift + vignette, kinetic serif system, coins and browser card as reel-03 v01_hook / v04_taste / v03_genius.
No speaker card (per brief); `assets/speaker.mp4` is unused.

## Key poses (slot seconds)

| t | on screen | word |
|---|---|---|
| 0.00 | paper only; "last" starts rising | last 0.05 |
| 0.27 | "last week" (Inter Tight 800, 100) | week 0.27 |
| 0.30–0.92 | real storytold/photocraft page in a tilted browser card rises with 3D settle + sheen (820x560, URL "github.com/storytold/photocraft") | — |
| 0.57 | "someone" (Inter Tight 900 ink 176) | someone 0.57 |
| 0.77 | "else" (Inter Tight 900 ink 176, right) pops | else 0.77 |
| 0.94–1.21 | phrase 1 lifts away bottom-up, 1 f apart | — |
| 1.17 / 1.53 | "also" 96 / "used" 120 | also, used |
| 1.10–1.58 | black pill "★ 47.2k stars" pops on the card's lower-left as the page's star row scrolls into view | — |
| 1.81 | "AI" (Inter Tight 900 OCEAN 270) hero pop to 108 %, settle | AI 1.81 |
| 1.90–2.40 | page scrolls down to the README; 2.16–2.50 ocean selection highlight sweeps "clean-room reimplementation / of Adobe Photoshop, rebuilt in pure Rust." | — |
| 2.07 / 2.49 | "to" 100 / "rebuild" (Inter Tight 900 ink 170) pop | to, rebuild |
| 2.44–2.96 | card anticipates (1 %) then shrinks on an arc into the top-left (scale 0.37, tilts the other way) | — |
| 2.62–2.93 | star pill + phrase 2 exit bottom-up | — |
| 2.93 | "seven" (Inter Tight 900 OCEAN 250, baseline 682) hero pop to 109 % + 1.2 % camera punch | seven 2.93 |
| 2.78–3.52 | coins 01–07 (46 px, Inter numbers) dealt up from the bottom of the stack on arcs (2 f stagger, roll + squash, contacts 3.20…3.60) to the RIGHT end of each slot; each blank white chip (428x104, wireframe placeholders) unfurls leftward out of its coin; 2 columns x 70–498 / 512–940, rows y 842/956/1070/1184 | — |
| 3.47 / 3.71 / 3.89 | "applications of Adobe" (Inter Tight 800, 82 / "Adobe" 96, plain text) | applications, of, Adobe |
| 3.58–4.42 | the REAL Adobe app icons (hf/assets/adobe_*.svg as img, 64 px, unmodified) pop in on the placeholder square (1.5 f stagger, contacts 3.72…4.02 around "Adobe" 3.89, overshoot 112 % + settle), a muted drawn arrow appears, and the Craft name (Inter 600 42 px) + storytold/<lowercase> slug (Inter 500 23 px muted) slides out from behind the icon: Photoshop→PhotoCraft, Illustrator→VectorCraft, Premiere Pro→FilmCraft, Lightroom→LightCraft, Acrobat→PdfCraft, After Effects→EffectCraft, InDesign→DesignCraft | Adobe 3.89 |
| 4.46–4.90 | light sheen runs down the finished stack | and, make |
| 4.72–4.95 | stack dips 6 px (anticipation) | them, all |
| 4.94–5.40 | every coin (right end of each chip) flips (scaleX) to the ocean face and a white ✓ draws on (1.5 f stagger) | open 5.17 |
| 5.00–5.30 | black pill "✓ all open source" (Inter 600 38, ~395 px wide) stamps into the empty slot beside DesignCraft (x ~530–926, no overlap): 1.12 blurred → 0.95 sharp at 5.12 → settled 1.0 / rot −2 by 5.30; chips 06/07 flinch 3 px | all 4.95, open 5.17 |
| 4.98 / 5.24 | "open" / "source." (Inter Tight 900 ink 140, one row, baseline 1414, ~50 px clear below the pill) snap in; "source." settled by 5.51 | open 5.17, source 5.43 |
| → 5.549 | hold alive (grid drift, camera push, page drift, chip float) into the hard cut | — |

Continuous: grid drift 20x12 px, camera push 1.000→1.010 (origin 510,880), card float + slow orbit, page drift, chip floats.

## Measured bounds (render without background, every frame)
- alpha > 40/255 (content incl. dense shadow): x 62–954, y 289–1478 over all 167 frames — inside x 60–960, y 285–1480.
- alpha > 12/255 (faint shadow halo only): x 59–968, y 292–1520 (browser card/chip drop shadows).

## Deviations
- On-screen words follow words.txt (the spoken "also" is shown although the brief skipped it). Omitted: "and make them all" as a phrase (covered by the stack sheen/dip; "all" appears in the brief's pill "all open source").
- Sizes: brief asked "used AI" Newsreader ~110 and "to rebuild" Newsreader ~96; built "AI" as an ocean hero (v2: Inter Tight 900, 270) and "rebuild" an ink hero (Inter Tight 900, 170) so Beat A has house-style hero contrast. "someone else" split on two lines at 176 (one line at 160 is ~930 px, wider than the zone). "open source." at 140 (160 is ~945 px wide). "applications of Adobe" 82/96 in v2 so the line fits (~840 px).
- Coins are dealt up from the bottom of the stack rather than rolled in from the side: a side roll would start outside the safe zone or cross other chips/words mid-motion.
- v07-only exception (user request, SHARED.md): the real Adobe app icons are shown from the supplied SVGs (never redrawn or recoloured); the coin numbers moved to each chip's right end and are the tick target.
- Stamp sits in the empty slot beside chip 07 (not overlapping it) rather than over the middle of the stack, so all seven app names stay legible; final pose reads seven / applications of Adobe / 7 ticked chips / pill / open source.
- Added a black "★ 47.2k stars" pill (real number from the captured page header) like v04's GitHub pill.
- Duration 5.549 s authored = exactly 167 frames.
