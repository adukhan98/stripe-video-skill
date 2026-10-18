# CHAIN_SHARED — the 11-habit disc chain (every map scene: m00_teaser, m01–m11_push, m12/m13_recap)

One fixed world geometry for all 14 chain scenes. A chain scene opens on EXACTLY the previous chain scene's end state
(same camera pose, same mint disc, same labels and check tags), so the cuts between them read as one continuous camera.

## World (on #cam; world px, B.camSet / V.cam take world points)
Serpentine, 4 columns × 3 rows, disc d = 150, connector 4 px charcoal centre→centre in order 1→11:

| # | label (his words) | icon | world centre |
|---|---|---|---|
| 1 | Try it yourself first | pencil-simple-line | (300, 300) |
| 2 | Make AI ask you questions | question | (660, 300) |
| 3 | Ask for the why | lightbulb-filament | (1020, 300) |
| 4 | Explain it back | chalkboard-teacher | (1380, 300) |
| 5 | Quiz yourself | exam | (1380, 640) |
| 6 | The delegation check | shield-check | (1020, 640) |
| 7 | Make AI show you things | presentation-chart | (660, 640) |
| 8 | Actually read what it writes | book-open-text | (300, 640) |
| 9 | Give your agent rules | list-checks | (300, 980) |
| 10 | Keep up with the new tools | rocket-launch | (660, 980) |
| 11 | Be more ambitious | mountains | (1020, 980) |

```js
const CH_PTS = [[300,300],[660,300],[1020,300],[1380,300],[1380,640],[1020,640],[660,640],[300,640],[300,980],[660,980],[1020,980]];
const CH_ICONS = ["pencil-simple-line","question","lightbulb-filament","chalkboard-teacher","exam","shield-check",
                  "presentation-chart","book-open-text","list-checks","rocket-launch","mountains"];
const CH_LABELS = ["Try it yourself first","Make AI ask you questions","Ask for the why","Explain it back","Quiz yourself",
                   "The delegation check","Make AI show you things","Actually read what it writes","Give your agent rules",
                   "Keep up with the new tools","Be more ambitious"];
const ch = V.chain("#punch", { points: CH_PTS, icons: CH_ICONS, d: 150, tags: CH_PTS.map((_, i) => i + 1) });
```
`tags` puts the habit number on each disc's edge (`.v7-tag`, charcoal); keep them.

## Camera poses (B.camSet(cx, cy, s) at frame 0; V.cam(t, cx, cy, s, {dur: 1.0}) to travel)
- **WHOLE** (whole chain left of his card): `(1146, 640, 0.85)`. Chain spans screen x ≈ 177–1223, y ≈ 187–893.
- **FOCUS n** (disc n at screen (640, 430), scale 1.2): `(x_n + 267, y_n + 92, 1.2)`. The label sits to the right of the disc.
- Travel between FOCUS poses with `V.cam(t, …, {dur: 1.0})`. The connector between the two discs is already drawn.

## Labels, tags, current item
- Current habit: its disc turns mint (`V.mintTo(ch.discs[n-1], t)`), the previous current goes back to charcoal (`V.charcoalTo`).
- Label (world, inside #punch so it travels with the chain; built ONLY by `C.label(n, t)` in chain_common.js v2, never
  repositioned in a scene): Inter Tight 800, 70 px world (84 px on screen at 1.2), on EMPTY paper between the rows,
  left-aligned with the disc (left = x_n - 75). ABOVE the disc (top = y_n - 165) for habits 1, 2, 3, 4, 8, 10, 11; BELOW it
  (top = y_n + 147) for 5, 6, 7, 9 (a turn connector would cross the text above). Kicker `HABIT n OF 11` 42 px above the label,
  Inter 600 28 px world, letter-spacing .12em, muted. (v1 put labels in the disc row at x+110 — they ran over the next discs;
  rejected 2026-10-17.) Only the CURRENT habit's label is ever shown; the previous label exits (6 f) as the camera leaves.
- Done habits (1..n-1 in m(n)_push) carry a small mint check disc at their top-left: `V.check("#punch", x - 55, y - 55, t, {size: 48})`
  (at frame 0: already drawn, so build it with its end state: no draw-on, see below).
- End state of m(n)_push = FOCUS n pose, disc n mint, label n shown, checks on 1..n-1. m(n+1)_push frame 0 = that state.

## Opening on a previous end state
`V.chainEnd(ch)` (connector drawn, all discs shown); `gsap.set(ch.discs[n-1], {backgroundColor: "#7CC49E"})`; labels and
checks created at their final state (B.in with an `at` < 0 is NOT allowed: just don't animate them). B.camSet the pose.
The chain-scene owner writes the code ONCE as `animations/chain_common.js` (a function `buildChain(V, B, {current, done,
labels})`), and every chain scene copies that file into its hf/ and calls it, so all 14 match to the pixel.

## Per scene (word times are in each TASK.md)
- m00_teaser: the chain is BORN (see its brief); ends on WHOLE, all charcoal, no labels, no checks.
- m01_push: opens on WHOLE (m00's end), travels to FOCUS 1. Later pushes open on FOCUS n-1 and travel to FOCUS n.
- m04_push also has the 'sounds obvious' label; m06_push the 'for work' label.
- m12_recap: opens on WHOLE with checks on 1–11 (habit 11 checked: the episode is over), all charcoal; glides through
  discs 1–5 as he names them (each flips mint and gets its label; the previous one goes back to charcoal and its label EXITS —
  labels overlap if two are shown, so only the current one is ever on screen).
- m13_recap: opens on m12's end, discs 6–11 the same way, ends on WHOLE with all discs mint (ripple) on 'aim higher'.
