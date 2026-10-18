# v04_impossible (fullscreen) - NOTES

## Key poses (scene s / frame)
- 0.00-0.74 (f0-22): him edge to edge, push 1.0 -> 1.03, nothing else (no words before "nobody").
- 0.74-1.04: solid paper strip slides up from below (top y 1195, soft 46 px top edge) so words sit on paper, not navy.
- 1.08 (f32): "nobody" lands (~94 px ink, baseline 1266); "told" 1.30, "him" 1.46 each pop, 2-3 f staggers.
- 2.26 (f68): "impossible." hero ~188 px ink lands, baseline 1426, right-aligned at 932 (collage vs left phrase above); overshoot 1.03.
- 2.36-2.58: RED scribble-strike (7-pass zig-zag, 15 px) crosses out "im" only.
- 2.50 (f75): "possible." tweens to accent red, 1 % camera punch + 3 px shake, impact.
- 2.66-2.84: both lines + strike blur up and out in 6 f (before "That's" 2.81).
- 3.03: "the" (small) / 3.29 (f99): "problem" ~160 px red hero lands, baseline 1312.
- 3.40-3.70: red wobbly underline under "problem"; 3.52 three spark ticks at its right end.
- 3.99-4.75: "most of us use AI." ~103 px ink, baseline 1464, one word per spoken word.
- 3.75-end: "problem" breathes 1.5 %, underline + ticks boil, push continues - no hold dead.

## Principles checklist
- Contact frames on words: every .w starts 0.13-0.2 s before its word time (runtime).
- Anticipation: hero words dip 3 f before rising (runtime); the "im" strike winds up via the tiny pause 2.26->2.36 before the scribble.
- Overshoot + settle: "impossible" 1.05, "problem" 1.08, then back.out settle; "possible" colour change plus 1 % punch.
- Parts lag the whole: nobody/told/him staggered by word time; strip arrives 0.3 s before the first word; underline then ticks lag "problem".
- Arcs: not applicable (no long moves; words rise on short arcs via rotation); no object travels.
- Squash/stretch: none (type only, by rule).
- One focal point: only one phrase at a time; phrase 1 is cleared (6 f) before phrase 2 lands.
- Secondary action: push on him, marker boil on fours, "problem" breathing, spark ticks.
- ONE exaggerated beat: strike -> "possible" red -> punch + shake + impact at 2.50.
- Exits faster than entrances: 6 f blur-up exit vs 5-12 f entrances.
- One light direction: n/a (flat paper strip, soft top edge, video unchanged).
- Not a static slide: him is live video with a push; words and marker move every ~0.3 s.

## Richness (fullscreen = minimal)
Hero: the strike-out on "im" with "possible" turning red on its word. Secondary: (1) paper strip slides in under the words,
(2) underline + three spark ticks on "problem", (3) "problem" breathing 1.5 % to the cut. No object other than the marker.

## Readability
- Measured over all 149 frames (diff of the render vs a render of the same scene with words + marker hidden): words + marker
  union x 65-941, y 1168-1476 (the 1168 pixel is the spark tick) - inside x 60-960 / y 285-1480 on every frame. The paper strip itself
  runs from y 1195 to the frame bottom by design (starter .paper-strip) and is outside the "content" measure.
- Type sizes (after --type-scale 0.94): nobody told him ~94, impossible ~188 (authored 200), the ~96, problem ~160, most of us use AI ~103 (authored 110) (all >= 64; hero >= 160 on screen).
- No ghosted text (words fade only during their 5-12 f entrances / 6 f exits). No notes, logos, real pages.
- Nothing over his face: the strip's soft edge (y 1195-1241) only overlaps the bottom of his beard; no type above y 1199.
- Strike crosses the word "im" by brief design (hero beat); no other marker crosses text.

## Deviations
- "He solved them because" and "it was" are not shown (brief lists only the phrases above), so 0-1.0 s is him alone.
- Strip top is 1195, not 1180, with a soft top edge, because his beard reaches ~y 1190 in this take.
- Spark ticks beside "problem" added (small, marker) as the only extra doodle.
- Reference render for bounds (qa/refB.mov) keeps the video and hides words + marker (the runtime needs the video element).

## Review fix (collision between the two phrase-1 lines)
- "nobody told him" authored 100 (was 120), baseline 1266; "impossible." authored 200 (was 210), baseline 1426, entrance rise 44, peak 1.03.
  Measured row gaps on the render (settled frames 71-90): line 1 bottom 1286 -> line 2 top 1304-1306 = 18-20 px clear air; the strike stays inside the letters of "im".
  During frames 66-68 the word is still entering (blurred, scaling) and its halo overlaps the gap for 3 frames - transient.
- Phase 2: "the problem" baseline 1312, underline bottom 1361, "most of us use AI." baseline 1464 (top 1382) = 21 px clear. Measured bounds 65-941 x 1168-1476, 149 frames, strip top unchanged (1195).

## Re-time after the 7-frame air cut (scene is now EXACTLY 142 frames, data-duration 4.7167 on root + video)
Phrase 1 unchanged (nobody 1.08, told 1.30, him 1.46, impossible 2.26). The hero beat was compressed to fit before "That's" (2.577):
- 2.30-2.46 red scribble-strike on "im" (dur 0.16, was 0.22); 2.40 "possible." turns red; 2.42 1 % punch + shake + impact.
- Phrase 1 exits in 4 f (was 6): "nobody told him" 2.50-2.63, "impossible." + strike 2.54-2.67 (a 6 f exit would not fit; exits remain faster than entrances).
  The red "possible." is readable ~0.12 s before it leaves - a trade-off of the cut. Tail of the exit overlaps the first frame of "the" (f80) by one frame.
- Phrase 2 is 0.2333 s earlier: the 2.797, problem 3.057 (underline 3.167, ticks 3.267, breathing from 3.517), most 3.757, of 3.897, us 4.057, use 4.237, AI 4.517.
- beats.json re-timed to match. Strip, push, grid, boil unchanged (run from 0).
- Re-measured (refB.mov re-rendered at 142 frames): words + marker union x 65-941, y 1165-1476, no violations. Line gaps: 18-20 px between the two phrase-1 lines
  (rows 1286 / 1304-1306), 21+ px between underline and "most of us use AI." (1362 / 1388).

## Final timing tweak (hold the red)
Phrase 1 now holds with red "possible." until 2.64 (red from 2.40 = ~0.24 s), exits in 4 f 2.64-2.77 (strike goes with it); "the" is held hidden (visibility) until 2.78 and lands on 2.797: zero frames show both (checked f83 = fading phrase 1 only, f84 = "the" only). beats.json whoosh moved to 2.66. 142 frames, bounds x 65-941 / y 1168-1476, check passes.

## v6 three-mode pass (Mode C -> A)
Phrase 1 is unchanged Mode C full screen (strike on "im", red "possible." held to 2.64). At 2.62 `P.fullToSplit("#spk", 2.62, { h: 960 })` shrinks the footage to the top half (face centred, 0.5 s); the solid paper strip is only a bridge for phrase 1 / the first frames of "the" and drops away at 2.94-3.19 so the bottom half is real paper + grid. Phrase 2 sits on that paper: "the problem" baseline 1275 (problem red ~160 px, underline y 1315-1325), "most of us use AI." baseline 1440 (~103 px, right edge 900); spark ticks moved above-right at y 1101-1180. Word times, exits and 142 frames unchanged.
Measured over all frames (words + marker): x 65-940, y 1101-1473; in phase 2 nothing right of x 900 below y 1200 (max 900), 39 px between underline and the last line; nothing in the footage half after the shrink. beats.json: the 2.66 whoosh is now the shutter whoosh at 2.62. No scribble beats removed (kept; scribbles still audible honest times).
