# v03_work — EXPLAINER (bespoke: work cards + enterprise window)

Full-screen opaque scene, 1080x1920 @30, **167 frames** (5.567 s, data-duration 5.5500). Built on the shared runtime
(paper.js / paper.css untouched). `<body data-face="0.47">`.

## Key poses (scene seconds)

| f | t | on screen | word |
|---|---|---|---|
| 0 | 0.00 | small speaker card (440x344, top-right) settling in; "It's" rising under the card (right-aligned 936, base 736) | It's |
| 11 | 0.36 | "because" (84) after "It's" | because 0.49 |
| 21–27 | 0.71–0.91 | HERO "AI" (ocean 340, x84 base 1064, centred ≈ y 940) overshoots and settles | AI 0.91 |
| 35 | 1.16 | "is" (80) leads the next line, right side | is 1.29 |
| 47–53 | 1.56–1.77 | "It's because" blurs out (−30 px); "is reliably" (130, right-aligned 944, base 1196) completes | reliably 1.77 |
| 60 | 2.00 | "getting" (120, left, base 1318) | getting 2.11 |
| 69–74 | 2.31–2.47 | "good" (ink 190, pop, right-aligned 944, base 1420) | good 2.47 |
| 72–85 | 2.40–2.82 | "is / reliably / getting / good" blur up in turn; AI dips (anticipation) and travels up on an arc (y −452) to the top-left, shrinking to 250-equivalent (×0.735) | (at) |
| 85–99 | 2.84–3.31 | WORK CARD 1 deals in on an arc from upper-right, tilting into travel, overshoot 1.025 → settle; AI recedes (staging) | business 3.19 |
| 96–108 | 3.19–3.57 | "business" header (Inter Tight 900, 68) lands; checkbox squares + wireframe bars draw in, 3 f apart; "work" (ocean) | business / work |
| 105–114 | 3.50–3.80 | row ticks 1→4, 3 f stagger: box flips to accent with overshoot, white ✓ draws, squash on contact, bars dim (done) | work 3.57 |
| 111–125 | 3.70–4.17 | card 1 recedes (72 %, blur 2); WORK CARD 2 deals up from below on an arc; "and" in the lower zone | and 3.85 |
| 124–134 | 4.15–4.47 | "knowledge" header, then "work" (ocean) | knowledge 4.15 / work 4.47 |
| 132–141 | 4.40–4.70 | card 2 row ticks 1→4 (3 f stagger, squash each) | work |
| 137–148 | 4.56–4.92 | "in" connective in the lower zone; card 1 restores | in 4.69 |
| 149–155 | 4.98–5.17 | cards gather inward (anticipation); the deep ENTERPRISE WINDOW grows from 78 % behind/around both, tips flat | — |
| 155 | 5.17 | window contact (1.02 → settle); sheen sweeps; 0.6 % camera punch (the ONE hero beat); cards pop back out 2 f apart; chrome dots blip | — |
| 154–166 | 5.13–5.53 | HERO "enterprises" (ink, fitted ≈170, base 1432) rises under the window, overshoot 1.03, settles — hold alive into the cut | enterprises 5.33 |

## As built (scene seconds)

- Speaker card: `.spk.small` x496 y302 440x344, face-at 0.522 → video window ≈ 24–68 % of the source (whole hair + chin, ceiling lamp out of frame). Float + slow orbit + inner push from the runtime.
- Beat A words: It's 0.00 / because 0.49 (exit 1.56, dy −30) · AI 0.91 hero 340 · is 1.29 + reliably 1.77 (line exit 2.48) · getting 2.11 (exit 2.52) · good 2.47 pop 190 (exit 2.62). Beat A now fills y ≈ 680–1470 (coordinator revision).
- AI: anticipation dip 2.40, arc to top-left 2.50–2.96 (y −452, scale 0.735, x swing +26 → 0), recede 3.00 (55 %, blur 2).
- Card 1 `#wc1` (106, 768, 384x498): deal 2.84 (arc fromX 250 / fromY −170 / tilt −8, 14 f; scale 0.84 → 1.025 → 1), rows draw 3.17+, ticks 3.50 / 3.60 / 3.70 / 3.80, recede 3.72, restore 4.80.
- Card 2 `#wc2` (530, 768): deal 3.70 (fromX 70 / fromY 180 / tilt 7), ticks 4.40 / 4.50 / 4.60 / 4.70.
- Connectives: and 3.85 (exit 4.40), in 4.69 (exit 4.92), both 84 px at x76 base 1440.
- Enterprise window `#ewin` (`.browser` primitive, deep viewport, 80–940 x 676–1292): gather 4.98, grow 4.97 → contact 5.17 → settle 5.50, sheen 5.10, punch 5.17, card pop-back 5.14/5.21.
- "enterprises" 5.33 (data-fit 900 → ≈170 px, data-peak 1.03).
- Continuous: grid drift, camera push 1→1.006, card floats (3 px, 1.3 s / 1.5 s), speaker float/orbit/video push.

## QA

- `slots.py check --motion`: **checks passed: size, fps, duration, alpha channel · motion: no dead holds**.
- ffprobe: **167** frames, 1080x1920, 30/1.
- Bounds (render diffed against a background-only render of the same runtime, threshold 40, all 167 frames): **x 69–960, y 290–1476** — inside x 60–960 / y 285–1480.

## Principles checklist

- **Contact frames on words**: every kinetic word via the runtime (hero 0.2 s / pop 0.16 s / default 0.13 s before its time); card 1 arrives ~3.07 for "business" 3.19, card 2 ~4.03 for "knowledge" 4.15; tick cascades start on each "work"; window contact 5.17 = 0.16 s before "enterprises".
- **Anticipation before the hero moves**: AI dips 3 f before its arc; cards gather inward 4 f (scale .965) before the window lands; hero words sink 3 f before rising; squash() stretches before each tick contact.
- **Overshoot + settle**: cards 1.025 → back.out; window 1.02 → back.out(1.8); tick fill 1.08 → 1; cards pop 1.015 → 1 after the window lands; hero words 1.06 (enterprises 1.03 for bounds).
- **Parts lag the whole (2–4 f)**: card → checkbox squares (3 f apart) → bars (2 f apart) → header word → ticks (3 f) → bar dimming (2 f); window → sheen (lag) → cards pop back (2 f apart) → chrome dots (2 f).
- **Long moves on arcs**: both cards via `P.arc` (x/y eased differently + tilt into travel); AI's 348 px rise has an x swing out-and-back.
- **Squash/stretch on shapes only**: `P.squash` on each checkbox on its tick; never on type, cards, or the speaker.
- **One focal point (recede the rest)**: AI recedes when card 1 arrives; card 1 recedes while card 2 deals and ticks; restored before the window gathers both.
- **Secondary action, no dead hold ≥ 1 s**: grid drift, camera push, card floats, speaker float/orbit/video push, tick cascades, bar dimming; `--motion` reports no dead holds.
- **One exaggerated hero beat**: the enterprise window landing — 0.6 % camera punch + cards popping back + sheen.
- **Exits faster than entrances**: runtime exits are 6 f blur-ups vs 10–16 f entrances.
- **One light direction / contact shadows**: all cards/window use the runtime's down-right soft shadows (`--shadow-card`, browser shadow); no hard outlines or offset shadows.
- **Nothing reads as a static slide**: every frame has a moving element (deal, tick, gather, grow, word land, float, drift).

## Deviations

- **"at" (2.83) is not shown.** It is a connective, and the lower zone is cleared at that moment for card 1's deal. **"It's", "is", "and" and "in"** are shown as small connectives (66–84 px).
- **Card headers are kinetic Inter Tight**: "business"/"knowledge" are 900 ink and "work" is 800 ocean, all at 68 px, landing on the spoken word. The brief allowed kinetic headers at ~64–80 instead of Inter 600 labels. 68 is the largest size at which "knowledge" fits the card.
- **The cards are 384x498, not ~400x520.** They have to fit inside the 860 px window (which keeps x ≥ 60 at its overshoot), with the speaker card above and "enterprises" below.
- **Beat A follows the coordinator's revised layout**: "It's because" sits under the speaker card, "AI" is 340 px, and the stack fills down to about y 1470. "good" is 190 rather than ~200, so it clears "getting" (120) side by side.
- **AI travels up on an arc** to the top-left at 2.5 s and stays there, receded, as the subject of the sentence for Beat B, instead of exiting.
- **The speaker card is 440x344 at the top-right** (small preset, ≥420). It is taller than the preset so the whole head and the chin fit.
- **"enterprises"** is auto-fitted to about 170 px with the hero peak reduced to 1.03, so its overshoot stays inside x ≤ 960.
- **The @font-face rules are copied inline** into index.html for the renderer's font guard. paper.js asserts the fonts.

## Creative pass (coordinator request; runtime reinstalled with `--type-scale: 0.94`, hero/SFX times unchanged)

New on top of the layout above (all on `P.*` + GSAP, brand tokens only):
- **AI glint + ping (0.84–1.41)**: a soft white light band sweeps left→right through the "AI" letters (background-clip text, `--sx` tweened) as it lands; a 7 px accent ring pings out from the word's centre at 0.91 (0.55 → 1.3, fades over 0.5 s, sized to stay inside x ≥ 60).
- **"getting good" meter (1.62–2.82)**: a white pill track under "good" (right-aligned, y 1448–1470, "good" raised to base 1396) pops in on "reliably" at 1.62. Its accent fill rises smoothly 1.70–2.44 (power1.inOut, no numbers) and **snaps** full at 2.44–2.47: the track squashes 1.05/1.25 → back.out and a glint sweeps across. It exits with "good" at 2.60.
- **AI dotted trail (2.52–3.16)**: an accent dotted path draws behind "AI" along its arc to the corner (drawn with mask + marching), then fades as card 1 arrives.
- **Cursor ticks the boxes**: the house cursor arcs in 3.18 → 3.47 to card 1 row 1 and clicks on every tick (3.50 / 3.60 / 3.70 / 3.80): a 1.5 f dip in and a 1.5 f release, stepping down a row between clicks. It arcs to card 2 at 3.96 → 4.38, clicks 4.40 / 4.50 / 4.60 / 4.70, and slides out at 4.84. Each tick now fills the row's first wireframe bar with accent left→right (7 f, starting 1 f after the click); the second bar dims.
- **Cards breathe** (1.008 at 1.4 s / 1.6 s periods) on top of their float.
- **Enterprise window**: a 28 x 21 grid of building lights in the deep frame switches on in a bottom-left → top-right cascade (5.14 → 5.47); about 9 % are lit accent, the rest are white at 42 % or 12 %. The cards pop (1.015), then **sink into the frame** to 0.93, revealing the lights around them. The frame then drifts back (0.994) for parallax depth.
- QA: `slots.py check --motion` passed (no dead holds); 167 frames; bounds **x 69–959, y 290–1476** (diff vs background-only render in scratchpad/v03_qa).
