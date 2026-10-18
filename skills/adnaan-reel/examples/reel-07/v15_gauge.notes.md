# v15_gauge — THE GAUGE (explainer, bespoke) — 160 f @30 (5.334 s) — v6 three-mode pass

Spoken: "And the biggest takeaway is that AI can do so much more than what most of us ask it for."
Modes: **Mode A** (split, 0–1.40) → `P.splitOut("#spk", 1.40)` → **Mode B** (full canvas, 1.70–5.33). The small speaker card is gone.

## Key poses
| t | f | on screen | word |
|---|---|---|---|
| 0.49 | 15 | Mode A: HE edge to edge in the top half (y 0–960); "the" / **biggest** (red hero) on the paper band below | biggest |
| 0.91 | 27 | "takeaway" (ink) under it; red underline under "biggest" | takeaway |
| 1.40 | 42 | Beat A has blurred up; the footage band dips 3 f and shoots up out of the frame (gone 1.70) → Mode B | that |
| 1.77 | 53 | gauge outline drawing up from the bottom centre (both halves at once), first ticks; "AI" top-left | AI |
| 2.25 | 68 | outline closed at the top, 5 ticks on; "AI can do" ink top-left | do |
| 2.61–3.19 | 78–96 | "so much more" note writes at the top-left of the bar; "so much" + **more** (red hero) under "AI can do"; spark | so … more |
| 3.19 | 96 | HERO: "more" lands, spark springs out of the bar top, punch + shake (impact) | more |
| 3.75–4.35 | 113–131 | hero words gone; "what most / of us" lands LOW-left; red hatch at the bar bottom (2 passes) | what … us |
| 4.69 | 141 | "ask it for" low-left; red-dark note "ask it for" by the hatch | ask |
| 4.72–5.23 | 142–157 | red curly brace draws UP the right side from the hatch to the top: the gap | ask … for |
| 5.33 | 159 | final = SHARED.md gauge state (v16 continues), held alive (boil) into the cut | for |

Layout idea: the words sit next to the part of the gauge they name — "AI can do / so much more" at the TOP of the left column
(next to the bar's top + the "so much more" note), "what most of us ask it for" at the BOTTOM (next to the tiny red hatch). The
empty middle of the left column is the gap the brace measures (white space ≈ 45 % of the zone in Mode B).

## As-built timeline (scene seconds)
- Always on: grid drift, camera push 1.006, marker boil on fours, footage push 1.0→1.02 (Mode A).
- MODE A 0–1.40: `<div class="spk split" data-h="960">` from frame 0 (video top −307 → face centred in the band, whole head in).
  0.12 "the" (96, base 1078) · 0.29–0.79 **biggest** (200 authored, red hero, base 1236, x 150) · 0.60–0.84 red underline (y 1304)
  · 0.75 "takeaway" (160 ink pop, base 1432, rise 36). Beat A exits 1.30 / 1.33 / 1.37 (6 f blur-up), underline erased 1.30–1.42.
- 1.30–1.40 band dips 10 px · 1.40–1.70 band shoots up out of the frame (power3.in) → MODE B.
- 1.61 "AI" pop · 1.94 "can" · 2.12 "do" (126, base 562) — exit 3.45.
- 1.66–2.18 **gauge outline draws itself bottom→top** (two halves at once, sine.inOut, closes on "do"); ticks 1.84 (1240), 1.90 (1060),
  1.95 (880), 2.00 (700), 2.06 (520), 0.07 s each, 1 f after the pen passes.
- 2.48 "so" · 2.74 "much" (130, base 724) · 2.50–3.13 note "so much more" (Caveat ink 92 px).
- 2.99–3.49 **more** (230 authored, red hero, base 910) · 3.08 / 3.15 / 3.21 red spark flicks spring out of the bar top (scale .3 → 1.18 → 1)
  · 3.19 punch 1.008 + 3 px shake (impact) · 3.30–3.70 "more" swells to 1.04 · "so much / more" exit 3.56 / 3.63.
- 3.62 "what" · 3.87 "most" (accent rise) · 4.04 "of" · 4.19 "us" (110, base 1062 / 1176).
- 3.90–4.10 red hatch pass 1 (seed 911) · 4.20–4.38 pass 2 (seed 910, cross-hatch) · 4.42–4.82 hatch squashes once (scaleY .86 → back.out).
- 4.52–5.02 red-dark note "ask it for" (Caveat 84 px) · 4.53 "ask" pop · 4.76 "it" · 5.06 "for" (120, base 1296).
- 4.72–4.96 brace lower half (hatch → nib y 845) · 4.99–5.23 upper half (nib → y 360). Held boiling to the cut.

## Principles checklist
- **Contact frames on words**: every word 0.13–0.2 s early (runtime); outline closes on "do", spark on "more", hatch on "most"/"us", brace ends on "for".
- **Anticipation**: the footage band dips 3 f before it shoots up; hero words sink before rising; spark compressed (.3) before it springs; hatch squash.
- **Overshoot + settle**: biggest / more ×1.06 → back.out; spark 1.18 → 1; hatch back.out(2.2).
- **Parts lag the whole (2–4 f)**: Beat A lines exit 1 f apart; spark flicks 2 f apart; ticks follow the pen; brace upper half 1 f after the lower.
- **Long moves on arcs**: the outline is the long move (eased up both sides); the band exit is a fast vertical shutter (runtime splitOut).
- **Squash/stretch on shapes only**: hatch squash, spark spring — never type.
- **One focal point / two elements**: Mode A = HE + "the biggest takeaway"; Mode B = the gauge + its words (top group, then bottom group). No card now.
- **Secondary action, no dead hold ≥ 1 s**: boil on fours, "more" swelling, grid + push; slots.py: "no dead holds".
- **One exaggerated hero beat**: "more" — punch 1.008 + 3 px shake + spark + impact.
- **Exits faster than entrances**: phrase exits 6 f, underline erased 0.12 s, band out in 0.3 s.
- **One light direction / contact shadows**: no shadows left in this scene (flat footage band, flat marker on paper).
- **Not a static slide**: something draws, lands or boils on every frame.

## Richness (hero + secondary)
- HERO: THE GAUGE — ink bar draws itself bottom→top, "so much more" at its top, a tiny red hatch at the bottom, the red brace measuring the gap.
- 1. Ticks tick on one by one as the pen passes them (1.84–2.06).
- 2. Red spark springs out of the bar top on "more" (3.08) with the punch/shake.
- 3. Mode switch: the footage band shoots up and hands the whole canvas to the drawing (1.40).
- 4. The hatch squashes once after its two passes ("almost nothing", 4.42); red underline under "biggest" (0.60); "more" swells.

## Readability checks
- Mode A content in the bottom band y 1000–1480, x ≤ 900 below y 1200 ("biggest" x 150–~800, "takeaway" x 80–~600).
- No semi-transparent text lingering: each group exits in 6 f; Beat C lands low, away from the exiting hero words (checked 3.60 / 3.75).
- Kinetic: biggest 200 / more 230 (hero ≥ 170), takeaway 160, so much 130, AI can do 126, ask it for 120, what most / of us 110, the 96.
- Handwriting: "so much more" 92 px ink, "ask it for" 84 px dark accent. Nothing crosses text or the face; no words over his clothing.
- All kinetic lines end ≤ x 630 in Mode B, clear of the ticks (x 650–681).

## QA
- Render: `render.mov`, **160 frames** (ffprobe count), prores 4444 1080x1920 @30.
- slots.py check (--motion --at 0.49,0.91,1.5,2.2,3.19,4.4,5.25): size, fps, duration, alpha passed; motion: no dead holds.
- Bounds (diff vs `qa/bg2.mov` = paper + the same Mode A footage band + splitOut, so only my content is measured; every frame,
  `qa/bounds.py`): diff > 40 → x 64–925, y 292–1466; diff > 16 → x 64–925, y 292–1469; **0 frames out of x 60–960 / y 285–1480**.
  (First v6 render had one frame, 0.77 s, of "takeaway" rising to y 1490 → baseline 1440 → 1432, rise 84 → 36.)
- Mode A footage band y 0–960 by design (SOP); Mode A words in y 1012–1469, x ≤ 790 below y 1200.

## THE GAUGE — exact code (v16: copy verbatim) and final state (UNCHANGED by the v6 pass)
Final frame (5.30 s) = SHARED.md "RECURRING DRAWING 2": ink rounded bar x 680–840 / y 340–1420 (r 70, width 11, seeds 901 left half /
903 right half), 5 ink ticks x 650→681 at y 520/700/880/1060/1240 (seeds 931–935, width 9; 931 = 1240 … 935 = 520), note "so much more"
Caveat 700 ink 92 px, top 340, rot −4°, right end x 646; red spark: three flicks (760,330)→(761,303), (736,333)→(716,312),
(784,333)→(804,312), seeds 905/906/907, width 9, scale 1 at rest; red hatch of the bar polygon y 1340–1420: pass 1 seed 911 spacing 19
angle −32 width 13, pass 2 seed 910 spacing 24 angle +38 width 11 (opacity .85, scale 1 at rest); red-dark note "ask it for" Caveat 84 px,
top 1338, rot −4°, right end x 650; red brace (width 11) lower half seed 921 (860,1330)→nib (920,845), upper half seed 923 nib→(860,360).
v15 ends in **Mode B** (no speaker on screen); the left column at the cut holds "what most / of us / ask it for" (110/110/120, x 84–~600,
y ~985–1296) — v16 brings its own words.
v16: paste the function below and call `const G = gauge(M, P, { outline: 0, notes: 0, spark: 0, hatch1: 0, hatch2: 0, askNote: 0, brace: 0 });`
(all drawn at frame 0, boiling). Erase the brace with `M.erase(G.braceLo)` / `M.erase(G.braceHi)`; G.hatchPoly = the bar-bottom polygon.
Camera: `#cam` push 1.006 (origin 510 880) — v16 starts at 1.0, so v15's last frame is ≤ 5 px larger at the bar ends.

```js
      // ================================================================================================
      // THE GAUGE — reel-07 recurring drawing 2 (geometry + seeds fixed in SHARED.md). v16: copy this
      // function VERBATIM and call   gauge(M, P, { outline: 0, notes: 0, spark: 0, hatch1: 0, hatch2: 0, askNote: 0, brace: 0 })
      // to open with the final state already drawn (every part at <= 0 = drawn at frame 0, boiling).
      // ================================================================================================
      function gauge(M, P, T) {
        const { tl, F } = P;
        const X0 = 680, X1 = 840, Y0 = 340, Y1 = 1420, R = 70, CX = 760;
        const arc = (cx, cy, a0, a1, n = 6) => Array.from({ length: n + 1 }, (_, k) => {
          const a = ((a0 + (a1 - a0) * (k / n)) * Math.PI) / 180;
          return [cx + Math.cos(a) * R, cy + Math.sin(a) * R];
        });
        const out = {};
        // 1. outline: two halves from the bottom centre UP to the top centre, drawn at the same time (seed 901 / 903)
        const LEFT = [[CX, Y1], ...arc(X0 + R, Y1 - R, 90, 180), [X0, Y0 + R + 470], ...arc(X0 + R, Y0 + R, 180, 270), [CX, Y0]];
        const RIGHT = [[CX, Y1], ...arc(X1 - R, Y1 - R, 90, 0), [X1, Y0 + R + 470], ...arc(X1 - R, Y0 + R, 0, -90), [CX, Y0]];
        const OUT_DUR = 0.52;
        out.left = M.line(LEFT, T.outline, { color: "ink", width: 11, amp: 2.4, dur: OUT_DUR, seed: 901 });
        out.right = M.line(RIGHT, T.outline, { color: "ink", width: 11, amp: 2.4, dur: OUT_DUR, seed: 903 });
        if (T.outline > 0) {
          // the hand accelerates up the long straight and eases into the top (sine.inOut overrides the default power2.out)
          [...out.left.paths, ...out.right.paths].forEach((p) => {
            const len = p.getTotalLength() + 2;
            tl.fromTo(p, { strokeDashoffset: len }, { strokeDashoffset: 0, duration: OUT_DUR, ease: "sine.inOut", immediateRender: false }, T.outline);
          });
        }
        // 2. ticks on the LEFT edge (x 650→680), each ticking on 1 f after the pen passes its height (seeds 931–935)
        const HALF = 10 + (Math.PI / 2) * R + (Y1 - Y0 - 2 * R) + (Math.PI / 2) * R + 10;
        out.ticks = [1240, 1060, 880, 700, 520].map((y, i) => {
          const p = (10 + (Math.PI / 2) * R + (Y1 - R - y)) / HALF;              // fraction of the half-stroke at height y
          const u = Math.acos(1 - 2 * p) / Math.PI;                                   // invert sine.inOut
          const at = T.outline > 0 ? T.outline + u * OUT_DUR + F : T.outline;
          return M.line([[650, y + 1], [681, y]], at, { color: "ink", width: 9, amp: 0.8, dur: 0.07, seed: 931 + i });
        });
        out.tickTimes = out.ticks.map((_, i) => T.outline + (Math.acos(1 - 2 * ((10 + (Math.PI / 2) * R + (Y1 - R - [1240, 1060, 880, 700, 520][i])) / HALF)) / Math.PI) * OUT_DUR + F);
        // 3. TOP label: "so much more" (Caveat ink 92 px), right end at x 646, centred y ~380
        out.top = M.note("so much more", 0, 340, T.notes, { size: 92, rot: -4, color: "ink", cps: 19 });
        out.top.style.left = 646 - out.top.offsetWidth + "px";
        // 4. spark above the bar top (seeds 905–907): three red flicks fanning up, top ≥ y 300
        const SP = [[[CX, 330], [CX + 1, 303]], [[CX - 24, 333], [CX - 44, 312]], [[CX + 24, 333], [CX + 44, 312]]];
        out.spark = SP.map((pts, i) => M.line(pts, T.spark > 0 ? T.spark + i * 2 * F : T.spark, { width: 9, amp: 0.8, dur: 0.07, seed: 905 + i }));
        // 5. BOTTOM fill: red marker hatch of the bar polygon y 1340–1420 = "what most of us ask it for"
        //    two quick passes: seed 911 (−32°) then seed 910 (+38°, cross-hatch). v16 floods with 912–919.
        out.hatchPoly = [[X0, 1340], ...arc(X0 + R, Y1 - R, 180, 90), ...arc(X1 - R, Y1 - R, 90, 0), [X1, 1340]];
        out.hatch1 = M.hatch(out.hatchPoly, T.hatch1, { seed: 911, spacing: 19, angle: -32, dur: 0.2 });
        out.hatch2 = M.hatch(out.hatchPoly, T.hatch2, { seed: 910, spacing: 24, angle: 38, dur: 0.18, width: 11 });
        // 6. red-dark note "ask it for" left of the hatch (84 px), right end at x 650, centred y ~1380
        out.ask = M.note("ask it for", 0, 1338, T.askNote, { size: 84, rot: -4, cps: 20 });
        out.ask.style.left = 650 - out.ask.offsetWidth + "px";
        // 7. GAP brace: red curly brace on the RIGHT of the bar, x 860–920, drawn UP from y 1330 to y 360 (seeds 921 / 923)
        const NX = 920, NY = 845, SX = 889;
        const BR_LO = [[860, 1330], [877, 1325], [886, 1310], [SX, 1286], [SX, 1080], [SX, 905], [893, 872], [905, 854], [NX, NY]];
        const BR_HI = [[NX, NY], [905, 836], [893, 818], [SX, 786], [SX, 600], [SX, 404], [886, 380], [877, 365], [860, 360]];
        out.braceLo = M.line(BR_LO, T.brace, { width: 11, amp: 1.6, dur: 0.24, seed: 921 });
        out.braceHi = M.line(BR_HI, T.brace > 0 ? T.brace + 0.24 + F : T.brace, { width: 11, amp: 1.6, dur: 0.24, seed: 923 });
        return out;
      }
```
v15 calls it with `T = { outline: 1.66, notes: 2.5, spark: 3.08, hatch1: 3.9, hatch2: 4.2, askNote: 4.52, brace: 4.72 }`.

## Deviations
- SHARED.md says "6 tick marks" but lists five heights; drew the five listed.
- Seeds not in SHARED.md: hatch pass 2 = 910 (keeps 912–919 free for v16), brace halves 921 + 923, spark 905–907, ticks 931–935.
- Spark is red, tips at y ≈ 300. Notes 92 / 84 px (above the 72 minimum).
- splitOut at 1.40 (brief "~1.45") so the band is fully gone at 1.70, before "AI" rises into the top of the left column.
- "And", "is that", "than" not shown. beats.json is now sparse (structural beats only, no scribbles) per the v6 SOP.
- Renders use the cached hyperframes 0.8.159 binary directly (concurrent `npx` installs failed with ENOTEMPTY).
