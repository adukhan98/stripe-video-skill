# v06_sloppy — EXPLAINER (bespoke, comedic: the misuse)

Full-screen opaque scene, 1080x1920 @30, **156 frames** (5.200 s, data-duration 5.1833 on root + speaker).
Built on the shared runtime (paper.js / paper.css untouched) and the reel-06 marker layer (marker.js / marker.css
untouched). `<body data-face="0.42">`. `P = await Paper.init({ extraFonts: ['700 60px "Caveat"'] }); M = Marker.init(P)`.

Spoken: "But they're using it as a glorified search engine or to write their stupid emails or their sloppy LinkedIn posts."

## Key poses (scene seconds)

| f | t | on screen | word |
|---|---|---|---|
| 0 | 0.00 | secondary speaker card (600x540, top centre, whole head + collar) settling; "But" rising under it | But 0.01 |
| 6 | 0.19 | "But they're" (96) under the card, left | they're 0.19 |
| 12–21 | 0.40–0.71 | "using it" (150, 900, right-aligned) pops on the paper below | using 0.53 / it 0.71 |
| 15–31 | 0.50–1.02 | speaker card dips (anticipation), then glides on an arc to the top-right corner, ×0.7 → 420x378 | — |
| 24–33 | 0.80–1.10 | SEARCH-BAR card deals in on an arc (−7° tilt into travel, 0.84 → 1.025 → 1); "as a" top-left | as 0.87 / a 1.01 |
| 31–40 | 1.03–1.33 | red marker CROWN draws onto the search bar in one stroke; HERO "glorified" (red 180) overshoots and settles | glorified 1.19 |
| 40–48 | 1.34–1.60 | jewel dots on the crown points, crown wobbles on its base (damped) and ends askew; two sparkle ticks | — |
| 47–60 | 1.58–2.05 | magnifier swings and peeks along the empty field; "search engine" (108) lands right | search 1.73 / engine 2.05 |
| 66–82 | 2.20–2.73 | "glorified / search engine" blur out; search card recedes; EMAIL card deals down-right on an arc; "or to" top-left | or 2.25 / to 2.39 |
| 74–92 | 2.48–3.06 | body lines type themselves word-by-word with a leading caret; "write their" | write 2.57 / their 2.73 |
| 85–96 | 2.85–3.34 | "stupid" (ink 132, one line "stupid emails") pops; red marker underline under it | stupid 3.01 |
| 98–106 | 3.27–3.53 | "emails" pops after it; send button squashes (pressed) | emails 3.43 |
| 107–118 | 3.58–3.95 | search card slips out, email card recedes and tucks up 120 px behind; LINKEDIN POST card deals in from below-left; logo pops, post lines draw 2 f apart; "or their" | or 3.73 / their 3.95 |
| 126–137 | 4.20–4.57 | HERO BEAT: red marker SCRAWLS a fast messy zig-zag across the post (0.35 s); "sloppy" (red 210) slams in; 1 % punch + 4 px shake; post lines tremble | sloppy 4.37 |
| 137–155 | 4.56–5.17 | red loop around the LinkedIn logo + logo pulse; "LinkedIn" (100) then "posts"; reaction row pops 2 f apart; "sloppy" letters boil out of line on fours — hold alive to the cut | LinkedIn 4.69 / posts 5.01 |

## As built

- Speaker `.spk.secondary` x240 y306 600x540, face-at 0.555 (source window ≈ 14–65 %: hair + beard + collar in).
  Wrapped in `#spkMove` (full-frame) so the runtime float stays intact: anticipation scale 1.015 at 0.50, then
  scale 0.7 / y −79 (power3.inOut) / x +187 (power2.inOut) 0.60–1.02 → corner box ≈ x 517–937, y 308–686.
- Cards (positioned wrapper at on-screen size → float → static fan tilt → static scale layer `.sc` (design px) → `.uicard` + card-local
  marker svg, so the crown/scrawl/loop scale and ride with their card). **Pass 2: cards scaled ~1.25–1.3×** (coordinator: read small on a phone).
  - `#w1` search bar **700x188** at (80, 760) = design 560x150 ×1.25, tilt −3.5°: magnifier, empty field, blinking caret (12 f), mic.
    Deal 0.80 (fromX −30, level). Crown `M.line` 1.03 (0.30 s, frame x ≈ 225–485 — left of the corner speaker), jewels 1.34/1.37/1.40,
    wobble 1.36–2.0 then sway, sparkles 1.46 (left) / 1.60 (right foot). Magnifier swing 1.58–2.0 + peek. Recede 2.28; slips out (6 f) 3.60.
  - `#w2` email **736x437** at (196, 836) = design 566x336 ×1.3, tilt +3.5°: envelope icon, title bar, To / Subject wire rows, 3 body lines typed
    with `steps()` + caret 2.48–3.06, caret blinks to 3.62, red send pill squashes at 3.43. Deal 2.34 (fromX −40, fromY −50). Recede + tuck up 120 px 3.62–3.96.
  - `#w3` post **780x400** at (90, 738) = design 624x320 ×1.25, tilt −1.5°: avatar + name bars, **official LinkedIn logo 64 px** (`assets/linkedin.png`, `<img>`),
    4 text bars, reaction row. Deal 3.62 (fromX −20, fromY 60), logo pop 3.90, lines 3.82. Scrawl `M.line` (20 seeded points) 4.22–4.57; lines tremble 4.37;
    punch 4.37 (1.01, origin 510 1260); shake 4.37 (4 px); logo loop `M.circle` 4.56; pulse 4.62; reactions 4.92+.
  - On-screen marker widths stay 9–14 px (design widths divided by the card scale).
- Kinetic lines: But they're (96, exit 0.58) · using it (150, exit 0.96) · as a (100, top-left, exit 1.92) · glorified (180 red hero, base 1302, exit 2.22) ·
  search engine (108, exit 2.22+2f) · or to / write their (96, top-left, exit 3.34) · "stupid emails" one line (132, data-fit 880, base 1424, pops 3.01 / 3.43, exit 3.62) ·
  or their (100, top-left, stays) · sloppy (210 red hero, base 1312, peak 1.08, stays) · LinkedIn posts (100, base 1446, stays).
- Camera: `#cam data-push="1.004" data-origin="510px 1000px"` (smaller push so the 1 % punch stays inside the zone).

## QA

- `slots.py check --motion`: **checks passed: size, fps, duration, alpha channel · motion: no dead holds**.
- ffprobe: **156** frames, 1080x1920, 30/1.
- Bounds (render diffed against a background-only render of the same runtime — `qa/bounds.py`, threshold 40, all 156 frames):
  **x 63–959, y 295–1477** (pass 2; pass 1 was y 295–1471) — inside x 60–960 / y 285–1480 (marker strokes, notes, card corners, shadows' solid part and descenders included).
- Fixed along the way: card 2 deal from x+120 overran x 988; accent/pop rises of "search engine", "LinkedIn", "posts" pushed descenders to
  y 1489; "sloppy" entrance rotation reached x 54 (moved to x 96); exit/entrance overlaps of the top-left connectives and of
  "glorified" vs "stupid"; card 1 dealing over the exiting "But they're".

## Principles checklist

- **Contact frames on words**: runtime words (hero 0.2 s / pop 0.16 s / default 0.13 s before); crown stroke starts 1.03 (0.16 s before "glorified");
  magnifier swing contact 1.68 for "search" 1.73; typing starts 2.48 for "write" 2.57; underline 3.08 just after "stupid"; send press on "emails" 3.43;
  scrawl starts 4.22 (0.15 s before "sloppy") with punch/shake on 4.37; logo loop 4.56 → closes on "LinkedIn" 4.69; reactions on "posts" 5.01.
- **Anticipation before the hero moves**: speaker card dips (scale 1.015, 3 f) before its glide; magnifier winds back +14° before its swing; hero words sink 3 f;
  send button stretches before its squash; each deal fades in low/small before the overshoot.
- **Overshoot + settle**: deals 0.84 → 1.025 → back.out; crown lifts −9° then damped wobble 7/−4/2 → rests −6°; magnifier 1.14 → 1; logo 1.12 → 1; hero words 1.06/1.08.
- **Parts lag the whole (2–4 f)**: card → logo (+8 f) → post lines (2 f stagger); crown band → jewels (3 f apart) → sparkles; typed lines 2 f apart;
  reactions 2 f apart; trembling lines 1 f apart; "write their" exits 2 f after "or to".
- **Long moves on arcs**: speaker glide (x power2 / y power3 — curved path); all three cards via `P.arc` with tilt into travel.
- **Squash/stretch on shapes only**: `P.squash` on the send pill only; never type, logo or cards.
- **One focal point (recede the rest)**: search card recedes when the email deals; email recedes and search card slips out when the post deals.
- **Secondary action, no dead hold ≥ 1 s**: grid drift, camera push, card floats, speaker float/orbit/video push, caret blinks, crown sway, marker boil on fours,
  sloppy letters boil; `--motion` reports no dead holds.
- **One exaggerated hero beat**: the scrawl on "sloppy" — 1 % punch + 4 px shake + post lines tremble + the impact SFX.
- **Exits faster than entrances**: 6 f blur-ups for words and the search card vs 10–16 f entrances.
- **One light direction / contact shadows**: runtime card shadows (down-right soft), no outlines or offset shadows.
- **Nothing reads as a static slide**: every frame has something landing, drawing, typing, wobbling or boiling.

## Richness (hero + secondary micro-animations)

- **Hero**: the three-card misuse deck, punctuated by the red marker — crown on the search bar ("glorified") and the scrawl over the LinkedIn post ("sloppy").
- **Crown with personality** (glorified 1.19): drawn on, jewels dot on, wobbles on its base and ends cheaply askew, two sparkle ticks, keeps swaying.
- **Search bar alive** (search 1.73): blinking caret in the empty field; the magnifier swings and peeks along the empty field.
- **Email writes itself** (write 2.57): body lines typed word by word with a leading caret; send pill pressed on "emails" 3.43; red underline on "stupid" 3.08.
- **Sloppy type** (sloppy 4.37): the letters of "sloppy" boil out of line on fours (±4.5°, ±5 px) after landing; the scrawled post's lines tremble.
- **Logo loop** (LinkedIn 4.69): red loop around the official logo + pulse; reaction row pops on "posts".

## Deviations

- **Kinetic sizes**: "glorified" is authored at 180 (the brief said ~150; SHARED's hero floor is 170); "stupid emails" one line at 132
  (brief ~120); "search engine" 108; "sloppy" 210. All connectives are 96–100 (≥ 64).
- **"stupid emails" is ink** as the brief asks; the accent on that phrase is a red marker underline under "stupid" (it crosses the p stem, like the approved "you" style test).
- **Connectives sit top-left** beside the corner speaker card ("as a", "or to / write their", "or their"), punchlines in the lower zone.
- **The search card leaves the stack** (6 f exit) when the post deals in, instead of staying receded: the post card covers it, and its crown would otherwise float above the post.
  The receded email card tucks up 120 px behind the post so it does not hang into "sloppy".
- **The speaker card is 600x540** (secondary preset width ≥ 600, but taller than the 432 default) so the whole head and collar fit, then ×0.7 = 420x378 in the corner.
- **Lower zone** is briefly empty at 0–0.4 s, 0.96–1.0 s and 2.42–2.85 s (the email card's lower edge fills it) and 3.74–4.17 s (phrase handovers); the lower 40 % of the zone is otherwise occupied.
- Every word spoken is shown; none omitted.

## Pass 2 (coordinator)

- Cards scaled ~1.25–1.3× via a static `.sc` layer (search 700, email 736, post 780 wide; logo 64 px); crown/scrawl/loop scale with them.
  Re-balanced: email card lower-right (836–1273), "stupid emails" back on one line below it, post card 738–1138, "sloppy" base 1312,
  crown and sparkles kept left of the corner speaker card; phrase-1 words exit 2.22 before the email deals (2.34); deal arcs tightened to stay inside x ≥ 60.
- Speaker clip replaced with the un-mirrored source: corner and top cards re-checked on the sheet — whole head, beard and collar in every frame.
- Re-rendered: 156 frames, check passed (no dead holds), bounds x 63–959 / y 295–1477.
