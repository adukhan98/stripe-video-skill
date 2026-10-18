# v02_fde: key poses (planned before authoring)

Full-screen opaque explainer, 1080x1920 @30, 174 frames (5.800 s). Bespoke object: a lanyard ID badge that
receives an accent "FDE" stamp, then an unlabelled rising chart line.

| t (s) | frame | on screen | word |
|---|---|---|---|
| 0.00 | f0 | Small speaker card (440x340) top-right, settling; paper world | Yes |
| 0.10–1.20 | f3–36 | ID badge swings in on its lanyard from the pin (arc + pendulum overshoot −4°/+2°/−1°), settles centre-left | I'm / talking |
| 0.64 / 0.94 | f19 / f28 | "talking" / "about" (84, right of the badge, under the card) | talking / about |
| 1.38 | f41 | "forward" (hero 170, ink) lands low-left | forward |
| 1.72 | f52 | "deployed" right-aligned | deployed |
| 2.18 | f65 | "engineer" lands lowest — lower zone full | engineer |
| 2.50–2.78 | f75–83 | words collapse into their first letters; f / d / e fly on arcs to the FDE slots, turning accent | or / the |
| 2.80 | f84 | ONE giant accent "FDE" (270) pops with overshoot + 1 % camera punch — the hero beat | FDE |
| 3.18–3.40 | f95–102 | FDE flies on an arc onto the badge and stamps its label slot (badge jolts and swings) | (gap) |
| 3.40–3.85 | f102–115 | badge (+ FDE label) compacts upward toward its pin | and |
| 3.70–4.28 | f111–128 | "hiring for this role" (96–120) | hiring / for / this / role |
| 4.10–4.60 | f123–138 | soft chart card (no labels) slides up into the lower zone | this / role |
| 4.55–5.46 | f137–164 | accent line draws on, rising steeply; tip dot rides it | is only going to go |
| 5.46 | f164 | line tip + "up" (200, accent) land together | up |
| 5.59 | f168 | second "up" (240, accent) steps higher; line steps up, arrowhead pops | up |
| 5.77 | f173 | everything still settling / breathing into the hard cut | |

## As built (scene seconds) — render.mov, 174 frames

| t | what happens |
|---|---|
| 0.00 | speaker card small 440x340 at x 506–946, y 302–642 (face-at 0.52 → window ≈ 24–68 % of source: full head incl. hair, chin, collar); runtime 3D settle + sheen |
| 0.08–1.30 | ID badge (v2, coordinator fix: 350x560 body at x 95–445, y 364–924, pin at 270,306; ink strap, clip, 160 px avatar placeholder, wire bars, empty label slot) swings in from its pin on an arc from the right: x +30→0 (power3.out), y +10→0 (power1.out), scale 0.9→1 back.out, blur 6→0; pendulum −8° → +3° → −1.6° → +0.7° → −0.3°; slow sway ±0.7° to 3.3 |
| 0.64 / 0.94 | "talking" / "about" (Inter Tight 800, 84) right-aligned under the card; blur-up exit 2.46 / +2 f |
| 1.38 / 1.72 / 2.18 | "forward" / "deployed" / "engineer" (Inter Tight 900, 180, ink, hero overshoot) — collage: left x 80 / right-aligned to 930 / left x 84, bases 1092 / 1260 / 1428 (moved down to clear the bigger badge) |
| 2.40–2.57 | each word's tail slides left under its first letter (clip, no distortion), 2 f apart |
| 2.47–2.80 | f / d / e fly on arcs (x and y eased differently) to the F / D / E slots, growing ×1.56 and turning accent; fade 2.62–2.72 as the giant word rises out of them |
| 2.80 | giant accent "FDE" (280, peak 1.12, letters lag 1 f each) + 1 % camera punch — the one exaggerated beat |
| 3.00–3.32 | FDE swells (anticipation), then flies on an arc onto the badge, shrinking to the 140 px label; stamp contact 3.32: label pops 1.3→0.94→1 at −2°, badge body dips 12 px and the badge swings from the hit |
| 3.36–3.76 | badge + FDE label compact upward/left toward the pin (scale 0.45, 3.36–3.78 → badge ≈ 158x252 at x ~95–250, y 300–580; label ≈ 63 px), pendulum lag −2.6° / +1.4° / −0.6° |
| 3.62–4.15 | chart card (860x540, four faint wire gridlines, no labels or numbers) slides up into the lower zone (cardIn), then floats 3 px |
| 3.70–4.28 | "hiring" (900, 124, pop) "for" "this" "role" (800, 96), base 802 |
| 4.36–5.46 | accent line draws on (power2.in → steepening), tip dot rides it, area fill reveals behind; badge recedes (4.5) |
| 5.20 | "hiring for this role" recedes (60 %, blur 1.5) |
| 5.46 | line tip reaches level 1 + "up" (accent 200, x 140, base 1190) lands; card nods 1.2 % |
| 5.46–5.60 | line steps higher to the top-right; second "up" (accent 240, x 380, base 1000) contact 5.593 (4 f later); arrowhead pops 5.53 → 1.25 → settles |
| → 5.77 | settles, sways, floats, grid drift and camera push into the hard cut |

## Measured

- Frame count 174 (ffprobe). `slots.py check --motion`: checks passed, no dead holds.
- Bounds over all 174 frames (diff vs a background-only render, per-channel > 40): x 62–958, y 288–1479 → all inside x 60–960, y 285–1480.
- Faint soft-shadow tails only (diff 12–40): to x 56 (badge shadow during the swing) and x 978 (speaker-card runtime drop shadow) and y 1517 (chart-card shadow during its slide-in). Nothing solid outside.

## Principles checklist

- Contact frames on words: every word uses the runtime contact timing (hero/pop/default start 0.13–0.2 s early); FDE peaks on 2.80, line tip and "up" share 5.46, arrow + 2nd "up" ~5.59.
- Anticipation: hero words sink 3 f (runtime); FDE swells 3 f before its flight; the speaker card/arrow/tip use dip-or-small-start pops.
- Overshoot + settle: badge pendulum decays through 4 overshoots; hero words 106–112 %; label 1.3→0.94→1; arrow 1.25→1; cardIn back.out.
- Parts lag the whole: word tails 2 f apart, flying letters 2 f apart, FDE letters 1 f, badge body dip vs strap swing, sheen on cards.
- Long moves on arcs: badge entrance, f/d/e flights, FDE stamp flight (x/y different eases); tip rides a curved path.
- Squash/stretch on shapes only: none on type (the "collapse" is a clip-slide, not a squeeze); the stamp impact is a uniform dip.
- One focal point: talking/about exit before the collapse; badge recedes when the chart takes over; "hiring for this role" recedes when the ups land.
- Secondary action / no dead hold ≥ 1 s: grid drift, camera push, card float + video push, badge sway, chart float, line drawing (check: no dead holds).
- One exaggerated hero beat: giant FDE + 1 % punch at 2.80.
- Exits faster than entrances: 6 f blur-up exits; FDE flight 0.22 s.
- One light direction / contact shadows: all shadows fall straight down/down-right (runtime tokens); pin has its own small contact shadow.
- Nothing reads as a static slide: something moves on every frame.

## Deviations

- "talking about" (spoken) is shown in beat A so the right side and the run-up to "forward" are not empty; "Yes, I'm", "the", "or the", "and", "is only going to go" are not shown (omitted, not paraphrased).
- Stack words are 180 px, giant FDE 280 (brief ~270), measured inside the zone incl. overshoot.
- v2 (coordinator): badge enlarged to 350x560 and swings in from the right (a swing from the left would push the big badge out past x 60); "talking about" stays right of the badge under the card (y ~670–830); stack moved down 30–60 px and to 180 px; compaction goes to 45 %.
- The words "collapse" by sliding their tails under the first letter rather than squeezing (no squash/stretch on type, per the house rules).
- The giant FDE itself flies onto the badge and becomes its accent label (the badge then carries it upward). The lower zone is empty for ~0.4 s (3.2–3.62) between the FDE leaving and the chart card arriving.
- The badge already hangs at the top of the zone, so "compact upward" is a shrink toward its pin (66 %) plus a slide left.
- Second "up" lands at 5.593 (4 f after the first) instead of the ASR 5.48, per the brief's 3–4 f stagger.
- Punch origin is 510,700 (not the default) so the top row stays inside y 285 during the 1 % punch.
- After the collapse the emptied source words are set visibility:hidden (removes a 1 px render seam seen at frames 79–90).

## Creative pass (2026-10-12) — runtime reinstalled, brand.css `--type-scale: 0.94` honoured

New, all on `tl` with P.* + GSAP (hero times unchanged: FDE 2.80, stamp 3.32, up 5.46, up 5.593):
- Lanyard physics: the strap skews against the pendulum (lags it, 0.08–1.46 and again 3.36–4.44); the clip trails the swing; on the stamp (3.32) the strap stretches 1.16 → 0.95 → 1 and the clip jiggles −11° / +8° / −4° / 0.
- Glint: a soft light band sweeps the badge plastic at 0.95–1.55 and 3.36–3.78.
- Avatar wakes on the stamp: eyes pop in (3.35, 1 f stagger), head turns to camera, accent ring pulse; blinks at 4.30 and 5.25. Label slot flashes accent on contact.
- Collapse: each flying f / d / e drags two motion-blur ghosts (1.5 f / 3 f behind, blur 2 / 4 px); the FDE flight to the badge drags two blurred copies (1 f / 2 f).
- FDE land 2.80: two thin accent shockwave rings (3 f apart, expand + thin + fade 0.5 s) and ten dust dots flying outward.
- Chart: gridlines draw left → right (3.82, 3 f apart); the card tilts toward camera as the line climbs (4.36–5.46, rotX 7° / rotY −5°, eases back 5.47); 16 accent particles shed where the tip passes and drift off; arrowhead kicks forward 22 px with three speed lines (5.57–5.75); accent ray bursts on each "up" (5.44 / 5.57).
- Type sizes now follow `--type-scale` (stack 169, FDE 263, "hiring" 1.29 em); the flight/label math reads the real font sizes.
- Measured: 174 frames; check passed, no dead holds; solid bounds x 63–958, y 288–1477; faint shadow tails x 56–978, y ≤ 1517.
