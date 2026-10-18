# v10_labs — NOTES

189 frames @30 (6.300 s). Full-screen opaque paper scene. FUNNEL tier 3 = ~5,000 → the top AI labs.

## Key poses (planned before authoring)

| frame | s | on screen | lands on |
|---|---|---|---|
| 0 | 0.00 | shared funnel drawn (tiers 0–1 pencil hatch, tier 2 red hatch), 10 stick people in tier 0, red pin in tier 2, all boiling | — |
| 24 | 0.80 | hand-drawn MAGNIFIER has swung in from upper right on an arc and parks over tier 3 / spout (squash on contact); 'after that,' (96) lower-left | 'after' 0.39 / 'that' 0.69 |
| 45 | 1.50 | ~30 red dots have popped into tier 3, one by one — inside the lens they read at 2×; post strip post_b4 slides up at the top, tape, highlighter behind '~5,000 people' | 'about' 1.07 → '5,000' |
| 47 | 1.55 | HERO: '5,000' (220, red) stamps down in the lower zone, shake + punch, lens pulses, dots pulse | '5,000' 1.55 |
| 57 | 1.90 | '~5,000' red Caveat note written right of tier 3; 'people' (88) right of the number | 'people' 1.91 |
| 74 | 2.45 | red marker arrow from the note up to where the door will be; post strip recedes (exit up) | 'work at' 2.39 |
| 102 | 3.41 | 'top AI' (124) + 'labs' (140) top-left; LAB DOOR (frame, panel, window, knob, padlock + strap) drawn top-right; red light leaks under the door | 'top' 2.83 / 'labs' 3.41 |
| 118 | 3.95 | padlock CLICK: lifts (anticipation) → drops, squash, shackle snaps, three tiny red click ticks | 'access' 3.95 |
| 135–151 | 4.49–5.03 | doodled server stack, then a cube appear inside the door window, window glows red | 'systems' / 'models' |
| 177 | 5.91 | three red ')))' sound-wave arcs pulse out from the door (staggered); 'heard about' (104) under 'labs' | 'heard' 5.91 / 'about' 6.21 |
| 188 | 6.27 | holds alive: boil, lens bob, door glow flicker, waves pulsing | cut |

## As built (scene seconds)

- 0.00 funnel (shared geometry, `FUN.draw(0)`, dividers 0–2, tiers 0–1 pencil hatch @0.45, tier 2 red hatch), 9 stick people in one row in tier 0 + the filled red map pin (tip 430,1080, R 40, card hole) with its contact shadow in tier 2 — reproduced from v07_you's code (same coordinates and seeds 900+/1300+/1700+/2100+, 5151, 6161; funnel fills/dividers in the same seed order), so frame 0 matches v07's last frame; the lens copy mirrors them — all boiling.
- 0.20–0.78 magnifier swings in from (700,690) on an arc (x power2.out / y power2.in, tilt 22° → −7° → 0), grows 0.62→1; rim loop drawn 0.22 (0.36 s), handle 0.46–0.74; lands 0.80 with squash, settles back.out by 1.10. Parks at (430,1108), R 135 glass (≈300 px with rim).
  The glass is a live 2× copy: a second `Marker.init(P)` layer re-draws the same seeded funnel/pin/dots (same boil timing) inside `#magIn` (scale 2, clipped by a 270 px circle); every lens move/rotation is mirrored on the copy (`gl()`), so the glass truly magnifies what is under its centre (incl. grid drift).
- 0.26 / 0.53 'after' / 'that,' (96 ink, lower-left), exit 1.22.
- 0.96–1.38 30 red dots pop centre-out into tier 3 (big and legible inside the lens).
- 1.16 real strip post_b4.png (0.87 scale, card 862 px) cardIn at the top; tape 1.34; highlighter behind '~5,000 people' 1.40.
- 1.35→1.55 HERO '5,000' (220 red, stamps DOWN from above) + punch + 4 px shake, lens pulses 1.06 (extra zoom flash), dot cluster throbs.
- 1.62 Caveat note '~5,000' right of tier 3; 1.78 'people' (88 ink).
- 2.28 red marker arrow from the note up to where the door will be ('work at'); 2.50 post strip exits up (6 f); 2.75 the funnel drawing (world #fz + lens copy #fz2, identically) steps back to opacity .72; '5,000' and 'people' stay FULLY opaque the whole scene (no semi-transparent text).
- 2.67 / 2.97 'top' 'AI' (124 ink), 3.25 'labs' (140 ink) top-left.
- 2.98 door frame, 3.24 floor, 3.34 panel, 3.44 red light line under the door + glow (flickers to the cut), 3.50 window, 3.58 knob, 3.60–3.80 padlock (shackle, card-filled body, red keyhole, strap to frame).
- 3.74 padlock lifts (shackle pops open) → 3.94 drops, squash, shackle snaps shut, three red click ticks (erased 4.32).
- 4.30 window glows; server stack doodle + red LEDs (systems), 4.86 cube doodle (models).
- 5.72/5.80/5.88 three red ')))' arcs drawn outward, then pulse; door glow swells. 5.75 'heard', 6.05 'about' (104 ink) under 'labs'.
- Continuous: boil on fours, lens bob ±4 px + sway ±1.6° (copy follows), grid drift, camera push, glow flicker.

## Principles checklist
- Contact frames on words: yes — words via runtime (0.13–0.2 s early); lens lands on 'after that', dots on 'about', stamp on '5,000', door on 'labs', click on 'access', doodles on 'systems'/'models', waves on 'heard'.
- Anticipation: '5,000' anticipation dip (runtime hero), padlock lifts before it clicks, lens enters small/tilted before it drops.
- Overshoot + settle: lens tilt −7° → 0 back.out, position back.out, '5,000' 1.06 → 1, padlock squash → back.out, dots 1.5 → 1.
- Parts lag the whole: lens rim → handle → glass highlight; door frame → floor → panel → window → knob → lock → strap; waves stagger 0.08 s; dots stagger ~1 f.
- Long moves on arcs: lens swing (x/y eased differently).
- Squash/stretch on shapes only: lens (squash on landing), padlock; never type.
- One focal point: beat A lens + '5,000'; beat B the door, with the funnel drawing (+ its lens copy) stepped back to .72 and the post strip gone; all text stays fully opaque.
- Secondary action / no dead hold ≥ 1 s: boil, lens bob/sway, glow flicker, waves pulse — slots.py: "no dead holds".
- One exaggerated hero beat: '5,000' (shake + punch + lens zoom flash) — only impact sfx.
- Exits faster than entrances: 'after that,' and post strip exit in 6 f; ticks erase in 0.14 s.
- One light direction: shadows down-right (lens drop-shadow, card shadow), glass highlight top-left.
- Not a static slide: every second has drawing-on or motion.

## Richness
- Hero: magnifier that really magnifies (2× live copy of the drawing, clipped) on 'after that' → '5,000'.
- Numbers come alive: 30 red dots pop in one by one inside the glass on 'about 5,000'; cluster throbs on the stamp.
- Real source: post_b4 strip with highlighter behind '~5,000 people' + tape.
- Hand-drawn lab door: light leaking (flickering glow), padlock clicks on 'access', systems/models doodles in the window, ')))' waves on 'heard about'.
- Connective arrow from the 5,000 to the door on 'work at'.

## QA (re-render 2, after coordinator fixes)
- render.mov: 189 frames (ffprobe), 1080x1920 @30, prores 4444.
- slots.py check --motion: "checks passed: size, fps, duration, alpha channel"; "motion: no dead holds".
- Bounds (diff vs background-only render, all 189 frames, threshold 12): x 66–954, y 298–1472 — inside 60–960 / 285–1480.
- Post strip at 0.87 scale (card 862 px wide). Smallest kinetic type 88 authored; note 66 px.

## Deviations
- No speaker card (brief is a full-screen funnel scene; the zone is full) — speaker video element removed.
- "Systems and models behind the door crack": the doodles appear in a small window in the door (a crack would be too thin to read); the light still leaks from the gap under the door.
- Only key words shown: 'after that,' '5,000' 'people' 'top AI labs' 'heard about' (others omitted, none paraphrased; final period dropped).
- The lens (parked so the '5,000' row stays clear) magnifies tier 2's lower half + the pin tip + tier 3, so the red dots sit in the lower half of the glass.
- (fixed) Stick people / pin now copied from v07_you's finished code (was re-created from briefs in the first pass).
- (fixed) No receded text: the earlier '5,000 people' fade was replaced by receding the funnel drawing.
