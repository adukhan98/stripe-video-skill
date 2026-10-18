# Animation principles for motion graphics (Lasseter, applied)

John Lasseter's *Principles of Traditional Animation Applied to 3D Computer Animation* (SIGGRAPH 1987)
took Disney's principles off the drawing board and onto a computer. His eleven (squash and stretch, timing,
anticipation, staging, follow-through and overlapping action, straight-ahead vs pose-to-pose, slow in and
slow out, arcs, exaggeration, secondary action, appeal) plus solid drawing are **mandatory in every
adnaan-reel scene** — not a style option. The shared runtime (`templates/runtime/paper.js`) applies them
by default; §"In the runtime" below maps each principle to the code that does it, and the per-slot
checklist at the end is answered in every scene's NOTES.md. Motion graphics have the same
problem he described: a computer will happily interpolate between two keys and call it animation.
Tweens that only fade and slide read as "template". These principles are what makes them read as
*animated*.

They are written for HyperFrames/GSAP slots at 30 fps. At other rates, scale frame counts by
`fps / 30`. Frames, not seconds, are the unit you think in: `f = 1/30` s.

## Two strengths — pick one per video, write it in SHARED.md

| | **subtle** (default: brand work, explainers) | **playful** (creator reels, hype, kids, memes) |
|---|---|---|
| Anticipation | 2–3 f, 2–4 % / 4–10 px | 4–6 f, 6–10 % / 15–30 px |
| Overshoot | 2–6 % (`back.out(1.2–1.6)`) | 8–15 % (`back.out(2–2.6)`) |
| Squash & stretch | shapes only, ≤ 6 % | shapes only, 10–20 % |
| Settle | 6–10 f | 10–16 f, can wobble twice |
| Exaggeration | one hero beat per graphic | one per beat |

Restraint is the brand look: motion is clean and confident, and the life comes from texture,
camera drift and overlap — not from bounce. Cartoon physics on a serious explainer reads as cheap.

## The principles, as recipes

### 1. Timing — weight and personality
Heavy things (full panels, documents, photos) move slower and settle longer; light things (icons,
tags, dots) snap. The same move at a different speed says a different thing.

| Action @ 30 fps | Frames | Seconds |
|---|---|---|
| Pop / flash / icon | 4–6 | 0.13–0.2 |
| Small element in | 8–12 | 0.27–0.4 |
| Card / panel in | 12–18 | 0.4–0.6 |
| Settle after overshoot | 6–10 | 0.2–0.33 |
| Stagger between siblings | 2–4 | 0.07–0.13 |
| Exit (faster than the entrance) | 6–9 | 0.2–0.3 |
| Camera push / drift over a hold | 30–150 | 1–5 |
| Minimum readable hold | ≥ 30 | ≥ 1 |

### 2. Slow in and slow out
Ease everything that starts or stops. `power3.out` / `expo.out` entrances, `power2.inOut` moves,
`power2.in` exits. **Linear only for continuous mechanical motion**: a marching dashed line, a
spinner, a ticker, a progress bar that represents real time.

### 3. Anticipation — tell the eye where to look
A small move the opposite way before the main action. Before a card rises, it dips 6 px; before a
pop, it shrinks to 94 %; before an arrow shoots right, its tail pulls back left.
```js
// pop with anticipation, landing on the word at time W (contact = first frame at full size)
tl.to(el, { scale: 0.94, duration: 3/30, ease: "power2.in" }, W - 9/30)
  .to(el, { scale: 1.05, duration: 6/30, ease: "power3.out" }, W - 6/30)
  .to(el, { scale: 1.00, duration: 8/30, ease: "sine.inOut" });
```
**Land the contact frame on the word**, not the start of the tween: start the anticipation
`anticipation + main` frames before the word's time in `words.txt` (≈ 0.25–0.3 s for a pop).

### 4. Follow-through and overlapping action — nothing stops all at once
- **Overshoot and settle**: the main element passes its mark and comes back (`back.out`, or the
  explicit 3-key version above, which you control better).
- **Parts lag the whole**: a card lands → its shadow settles 2 f later → its title arrives 3–6 f
  after the card → the underline draws after the title. Children of a group stagger 2–4 f; never
  move a group as one rigid block.
- **Drag**: a trailing element (a label under a logo, a tail on a pin) starts 2–3 f late and
  catches up.

### 5. Arcs — natural things travel on curves
Anything moving more than ~200 px takes a curved path. No plugin needed: tween `x` and `y` with
different eases and the path bends.
```js
tl.to(card, { x: 0, duration: 16/30, ease: "power3.out" }, t)
  .to(card, { y: 0, duration: 16/30, ease: "power1.out" }, t)       // y lags x → a curve
  .fromTo(card, { rotation: -4 }, { rotation: 0, duration: 18/30, ease: "back.out(1.4)" }, t);
```
A thrown cut-out tilts slightly into its direction of travel and straightens as it settles.
Verify the path with `npx --yes hyperframes keyframes hf --shot arcs.png --selector .card`.

### 6. Squash and stretch — mass and flexibility
Volume-preserving (`scaleX × scaleY ≈ 1`): stretch along the motion while fast, squash on
contact, recover.
```js
tl.to(dot, { scaleX: 0.9, scaleY: 1.1, duration: 4/30 }, t)        // stretching while falling
  .to(dot, { scaleX: 1.1, scaleY: 0.9, duration: 2/30 }, t + 6/30) // squash on contact
  .to(dot, { scaleX: 1, scaleY: 1, duration: 8/30, ease: "back.out(2)" });
```
**Only on shapes**: dots, pills, bubbles, buttons, plain cut-out photos. **Never on logos or brand
type** (Hard Rule 13: no stretching, rotating or re-lettering a logo). A logo animates with
uniform scale, opacity and position only, and anticipation as a uniform scale dip is fine.

### 7. Staging — one idea, unmistakably
- One focal point at a time. When something new enters, what was there recedes: dim to 40–60 %,
  blur 4–8 px, or scale to 97 %.
- Lead the eye: arrows, highlighter swipes and camera moves point at the focal element.
- Silhouette test: at thumbnail size (the motion strip), the key frame still reads as a shape.
- The speaker counts as a focal point: a graphic beside a talking face must be calmer than one on
  a full-screen board.

### 8. Pose-to-pose (and straight-ahead where it fits)
Block first, polish second. Before writing any tweens, write the **key poses** in `NOTES.md`:
frame number, what's on screen, which word it lands on. Then animate between them, then add
overlap and secondary action. Use straight-ahead (frame-by-frame, deterministic noise) only for
organic things: paper flutter, scribbles, particles, hand-drawn line boil.

### 9. Secondary action — holds are never dead
While the main idea holds, something small keeps living: a slow push-in 100 → 103 % over the hold,
a 6–12 px drift, parallax layers drifting at different rates, one pulse on the key number, a
breathing glow, a cursor blink. It supports the main action and never competes with it: small
amplitude, slow, one at a time. `slots.py check --motion` flags any visible hold ≥ 1 s with
nothing moving.

### 10. Exaggeration — push the beat that matters
One hero moment per graphic gets more: a bigger overshoot, a scale to 115 %, a 2–4 px camera shake
for 4 f on impact, a colour flash. Everything else stays restrained, so the hero reads as big.

### 11. Solid drawing (depth)
Lasseter dropped this for 3D; motion graphics need it back. One light direction for every shadow
in the video. Contact shadows under objects that land. Perspective tilts (1200–1400 px
perspective, ≤ 25°) share one vanishing point across a board. Parallax: near layers move more.

### 12. Appeal
Simple, readable shapes. Generous spacing. One accent colour doing one job. If a graphic needs
explaining, it isn't finished.

## In the runtime (`paper.js`) — what each principle maps to

| Principle | Runtime default | You add |
|---|---|---|
| Timing | weight-based durations: word pop 5–6 f, pill 8+9 f, card 16 f, exits 6 f (faster than entrances) | heavy things slower, light things snap |
| Slow in / slow out | every helper eased (`power3.out` in, `power2.in` out, `power2.inOut` moves); linear only in `world()` grid drift, `marchPath`, `scrollPage` | never `ease: "none"` on an object that starts or stops |
| Anticipation | `data-hero` words sink 3 f before rising; `enter()`/`pop()`/`cursorClick()`/`squash()` dip the other way first; a late speaker card starts low and behind | `tl.to(el,{scale:.94,duration:3*F,ease:"power2.in"}, t-9*F)` before a bespoke pop |
| Follow-through & overlap | overshoot → `back.out` settle on words, cards, pills, coins; `data-exit-lag`, `stagger` (3 f) on siblings; sheen lags the card 3 f | children of your hero object 2–4 f apart; never move a group as one block |
| Straight-ahead / pose-to-pose | pose-to-pose: words land on their contact frame; you write key poses in NOTES.md first | straight-ahead only for organic boil/particles (deterministic noise) |
| Arcs | `arc()`, `cursorTo()`, `coinIn()`, `ride()` bend x/y with different eases or a path | anything moving > 200 px uses one of these |
| Squash & stretch | `squash()` (volume-preserving) on coins, pills, pucks; `pillIn`/`coinIn`/`puckFeed` call it on contact | shapes only; never type, logos or the speaker card |
| Staging | `recede()` / `restore()` dim+blur+97 % what is not the focal point; the world is calm (subtle drift) | one focal point at a time; recede the header when the page lands |
| Secondary action | grid drift, camera push (`#cam[data-push]`), `[data-float]`, `[data-breathe]`, `[data-pulse]`, video push on cards, marching dots | one small living thing per hold, never competing |
| Exaggeration | `[data-punch]` / `punch()` (0.4 % camera), `shake()` (4 f), `data-peak` on the hero word, `coinActive` ring flash | exactly ONE hero beat per scene gets more |
| Solid drawing | one light direction (shadows down-right), contact shadows (`.coin-shadow`, `.puck-shadow`, `.ground`), shared perspective 1400–1600 px | keep your object's shadow consistent with the primitives' |
| Appeal | simple shapes, generous spacing, one accent, type ≥ 64 px | if it needs explaining, it isn't finished |

Strength presets (`#root[data-strength="subtle|playful"]`): subtle is the house default (overshoot 6 %,
`back.out(1.6)`, 3 f anticipation); playful (10 %, `back.out(2.2)`, 4 f) only when the brief asks for it.

## The edit obeys them too
- **Anticipation**: a J-cut (the audio of the next shot starts 4–8 f early); a whoosh that starts
  2–3 f before the visual it carries.
- **Timing**: cut rhythm. Quick cuts for energy, a held shot after a punchline (the reaction is
  the follow-through).
- **Staging**: punch-ins frame the face for the line that matters.
- **Exaggeration**: the hero line gets the speed ramp, the freeze frame or the full-screen card.

## Per-slot checklist (answered in NOTES.md before reporting — a scene without it is not finished)
1. Key poses written in NOTES.md, each contact frame on a word from `words.txt`.
2. The main entrances have anticipation; the hero element overshoots and settles.
3. Groups overlap (children 2–4 f apart), and nothing moves as a rigid block.
4. Long moves travel on arcs.
5. No dead holds (`slots.py check --motion` passes without a WARN), and secondary action is subtle.
6. One focal point at a time, so everything else recedes when something new enters.
7. Squash and stretch only on shapes, never on logos or type.
8. Exits are faster than entrances and finish before the last frame.
9. The strength matches SHARED.md (subtle/playful).
