# v05_departments — key poses (written before authoring)

Full-screen opaque MECHANISM scene, 1080x1920 @30, EXACTLY 202 frames (data-duration 6.7167). No speaker card.

| frame | t (s) | on screen | lands on |
|---|---|---|---|
| 0 | 0.00 | paper + grid drift, "every" already rising | in 0.00 |
| 5 | 0.17 | "every" (Inter Tight 900, ink) contact, top-left | every 0.29 |
| 11–43 | 0.36–1.42 | 3x3 department tiles deal out of a centre deck on arcs (2 f wave, overlap) | — |
| 18 | 0.60 | "single" (800) beside "every" | single 0.73 |
| 31 | 1.03 | "department" (900, OCEAN) contact, right-aligned under it | department 1.23 |
| 44 | 1.47 | "at the" (800) left, below the grid | at 1.63 / the 1.81 |
| 54–57 | 1.80–1.90 | every tile dips 5 % (anticipation) | — |
| 57–61 | 1.90–2.03 | ALL nine tiles flip at the same frame (rotationY 0→90) | — |
| 61 | 2.03 | deep faces swap in, accent dots light, grid punches 1 %, "same" OCEAN 200 contact | same 2.03 |
| 63–76 | 2.08–2.55 | light ripple sweeps diagonally across the deep tiles | — |
| 65 | 2.17 | "time" OCEAN contact; tiles overshoot 105 % and settle | time 2.33 |
| 71–147 | 2.35–4.9 | accent progress bars fill in every tile (secondary action) | — |
| 95–101 | 3.16–3.36 | phrases exit bottom-up (blur-up, 6 f) | — |
| 99–118 | 3.30–3.95 | grid anticipates, then shrinks to 70 % up to the top of the zone on a slight arc | — |
| 114–135 | 3.80–4.50 | three dotted paths draw from the bottom tiles down into the lower zone, then march | — |
| 142 | 4.75 | grid recedes (dim + blur) — pills become the focal point | — |
| 144–152 | 4.80–5.07 | black pill "time" (clock icon) rises into the bottom slot, squash on contact | time 5.21 |
| 159 | 5.30 | stack pushes up one slot (anticipation of the next arrival) | — |
| 165–173 | 5.50–5.77 | pill "money" (coin icon) rises into the bottom slot | money 5.91 |
| 181 | 6.05 | stack pushes up again (money, then time 2 f later) | — |
| 187–196 | 6.25–6.52 | pill "effort" (bolt icon) rises in; settles into the cut | effort 6.68 |
| 201 | 6.70 | grid / time / money / effort stack alive into the hard cut | — |

# As built (scene seconds) — render.mov, 202 frames

| t | what |
|---|---|
| 0.11→0.31 | "every" Inter Tight 900 ink 134 (x 78, baseline 392): anticipation sink, rise to 106 %, settle (contact 0.31 ≈ word 0.29). Frames 0–3 are paper + grid only. |
| 0.36 | centre tile (chat bubble, the "deck") pops 50→106→100 % |
| 0.44→1.42 | 8 ring tiles dealt clockwise from the deck, 2 f apart, 14 f each: x power3.out / y power1.out (arcs), tilt ±4–9° into travel, scale 72→104→100 % |
| 0.57 | "single" Inter Tight 800 104 (data-accent rise) |
| 1.03→1.23 | "department" Inter Tight 900 OCEAN 182, right edge 928 (baseline 566) |
| 1.50 / 1.68 | "at" / "the" Inter Tight 800 84, left under the grid (baseline 1294) |
| 1.80 | all 9 tiles dip to 95 % (anticipation) |
| 1.90→2.03 | ALL tiles rotateY 0→80° together (same frame, no stagger) |
| 2.03 | swap to deep faces (--brand-deep, white icons, accent dot + glow); rotateY −80→0 back.out(1.6) by 2.33; scale 105 % → settle; 1 % punch of the whole scene (origin = grid centre) — the one hero beat; "same" 900 OCEAN 204 contact |
| 2.10→2.60 | light ripple: per-tile sheen sweep staggered 1.5 f per diagonal (r+c); accent dots ring 30→135→100 % with the same diagonal stagger |
| 2.13→2.33 | "time" 900 OCEAN 204 (right edge 932, baseline 1446) |
| 2.35→4.9 | accent progress bars fill in every deep tile (2 f apart, unlabelled, no numbers) |
| 3.16 / 3.23 / 3.27 | phrases exit bottom-up (6 f blur-up; top line dy −22 so it stays inside the zone) |
| 3.26 | grid anticipation dip (+14 px, 101 %) |
| 3.39→3.97 | grid shrinks to 76 % and rises 390 px (top ≈ 300), slight left arc (x −22, rot −1.2° and back) |
| 3.84→4.58 | three dotted feeds draw from the bottom tiles (centre one accent) down to the stack, then march (linear, continuous) |
| 4.72 | grid recedes (55 %, blur 3, 97 %) — focal point moves to the pills |
| 4.80→5.07 | black pill "time" (Inter 600 84, accent clock) rises into the bottom slot (top 1276), squash on contact (word 5.21) |
| 5.30 | stack pushes up one slot (186 px) before the next arrival |
| 5.50→5.77 | pill "money" (accent coin) rises in (word 5.91) |
| 6.03 / 6.10 | stack pushes up again: top pill leads, next lags 2 f |
| 6.25→6.52 | pill "effort" (accent bolt) rises in (word 6.68), settling into the cut |
| 5.07 / 5.77 / 6.52 | each landing pings the grid's accent dots (½ f stagger) |
| continuous | grid drift, camera push 1.006, per-tile float 3 px (own periods), marching feeds |

Final pose: dimmed deep grid at top (x 247–773, y ≈ 300–753) → three dotted feeds → stack time / money / effort (staggered x −120 / +100 / −40, rot −1 / 0.8 / −0.6°) y ≈ 904–1432.

## QA
- `slots.py check --motion`: checks passed: size, fps, duration, alpha channel; motion: no dead holds.
- ffprobe: 202 frames.
- Bounds (every frame, diff vs a background-only render): diff>40 x 62–960, y 294–1474; diff>12 (shadow halo) x 62–960, y 293–1480. 0 px outside the zone on any frame.

## Principles checklist
- **Contact frames on words**: every/single/department/at/the/same/time land on their word times via data-t; pills land 0.14–0.16 s before time/money/effort; the deep swap is exactly on "same" (2.03).
- **Anticipation**: hero words sink before rising; all tiles dip 5 % before the flip; grid dips +14 px before shrinking; the stack pushes up before each new pill arrives.
- **Overshoot + settle**: tiles 104–106 % → back.out on deal and flip; flip rotation back.out(1.6); words 106 % peak; pills overshoot 6 px + squash.
- **Parts lag the whole**: deal 2 f stagger; ripple 1.5 f per diagonal; progress bars 2 f; push: top pill leads, next 2 f later; dot pings ½ f.
- **Long moves on arcs**: deal (x/y eased differently + tilt into travel); grid rise with a sideways arc + rotation.
- **Squash/stretch on shapes only**: pills (runtime pillIn squash), nothing on type.
- **One focal point**: words + grid in beat A; the grid is the focus during the shrink; it recedes at 4.72 when the pills take over.
- **Secondary action, no dead hold ≥ 1 s**: tile floats, progress bars, marching feeds, dot pings, grid drift, camera push (motion check: no dead holds).
- **One exaggerated hero beat**: the same-frame flip of all nine tiles + 1 % punch + light ripple on "same time".
- **Exits faster than entrances**: phrase exits 6 f vs 0.36–0.5 s entrances.
- **One light direction / contact shadows**: tiles use the runtime card/deep shadows (down), pills the runtime pill shadow; same direction throughout.
- **Not a static slide**: at every frame something deals, flips, sweeps, fills, marches or stacks.

## Deviations
- "in" (0.00) not shown, following the brief's 'every single department'. Frames 0–3 are paper only because the "every" entrance starts at 0.11.
- Brief said the pills "drop in". They rise into the bottom slot and push the stack up (chat style) so the final read is time / money / effort top to bottom, the lower zone fills from the first pill on, and pills never cross mid-motion.
- Pill text is 84 px (brief ~64) and grid tiles are 236x184 (brief ~240x200) so the 3x3 grid, "department" and "same time" all fit the zone.
- Added accent progress bars inside the deep tiles (unlabelled, no numbers) and three dotted feeds from the grid to the stack as Beat B secondary action and connective tissue.
- No speaker card: the .spk block and its <video> were removed. hf/assets/speaker.mp4 is unused.

# Revision 2 (coordinator: fill 3.3–5.0 s, bigger pills) — supersedes the Beat B rows above
| t | what |
|---|---|
| 2.82 / 2.86 | phrases exit bottom-up (were 3.16/3.2) so the grid can rise under "because that's" |
| 2.81 | grid anticipation dip; 2.94→3.48 grid shrinks to 76 % and rises 390 px (power2.inOut), slight left arc |
| 3.15→3.28 | "where" Inter Tight 800 ink 112 (x 84, baseline 1170) — 0.23 s after the spoken 3.05 so it never ghosts under the rising grid |
| 3.25→3.38 | "they" (800 ink 112) |
| 3.30→3.50 | "see" Inter Tight 900 OCEAN 224 (right edge 930, baseline 1392), overshoot + settle (word 3.47) |
| 3.5→4.56 | hold: progress bars fill, tile floats, grid drift ("cost of value" not shown) |
| 4.36→4.98 | dotted feeds draw from the grid into the stack, then march |
| 4.56 / 4.63 | "see", then "where they", blur up out of the way, gone before the "time" pill lands (5.07) |
| 4.80 / 5.50 / 6.25 | pills rise in (Inter 600 96, height 176, icon 92); stack pushes 200 px per arrival (5.30; 6.03 top leads, next +2 f) |

Final pose: dimmed grid (y ≈ 300–753) → feeds → time / money / effort centred near x 510 (offsets −60 / +50 / −20), y ≈ 856–1432.
QA after the revision: slots.py check passed, no dead holds; 202 frames; bounds diff>40 x 62–960, y 294–1474 (diff>12 x 62–960, y 292–1479); 0 px outside the zone.
Extra deviation: "where" lands at 3.28 instead of 3.05, so it never collides with the grid while the grid is still rising.

# Creative pass (runtime reinstalled; --type-scale 0.94 honoured — "single" size moved to em so it scales too)
Hero times unchanged: deal 0.36, all-flip 2.03, pills 5.07 / 5.77 / 6.52. 202 frames.

New:
- **Live company**: after the flip every deep icon gets its own micro-action, booting in a diagonal wave (2.38 + (r+c)·2 f, 2.38–2.65):
  briefcase handle lifts and bobs · chart bars grow (back.out) then keep breathing, the middle one in accent · second person pops in (accent) and nods ·
  gear turns continuously (300° to the cut, linear = mechanical) · chat bubble shows accent typing dots · document lines write in (and re-write at 3.70) ·
  shield check draws on · truck idles back and forth with accent speed lines · dollar coin keeps flipping.
- **Network pulse**: 12 accent connectors in the gutters between neighbouring tiles light up outward from the centre tile at 2.36 and 3.62 (3 f per step), then top→bottom at 4.16 so the pulse runs straight into the dotted feeds (4.36).
- **"see"**: camera focus brackets snap onto the word (3.43→3.50; scale anchored on the right edge so the snap stays inside x 960), hunt for focus once (3.63–3.80), then breathe. An accent 4-point glint/halo pops on the top-right of the word at 3.66 and twinkles. Both leave with the phrase at 4.56.
- **Feed dots**: a glowing accent dot rides one dotted feed into each pill and is absorbed on contact (time via the left feed, 4.63→5.07; money via the right, 5.33→5.77; effort via the centre, 6.08→6.52).
- **Pills**: soft accent ripple ring on each contact (0.45 s) on top of the runtime squash. Clock minute hand sweeps a full turn (5.07–5.62), then keeps ticking round; coin spins (5.77–6.10), then wobbles; bolt flickers (6.40–6.57) and pops to 130 % on 6.52.

QA (creative pass): slots.py check passed, no dead holds; ffprobe 202; bounds diff>40 x 67–960, y 294–1475 (diff>12 y 294–1479); 0 px outside the zone (bg-only reference in scratchpad/v05_qa/).

SFX cue list (scene seconds): see the coordinator report.
