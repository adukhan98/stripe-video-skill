# v09_anthropic — key poses (written before animating)

175 f @30 (5.8167 s). Spoken: "In fact, Anthropic has committed a hundred million dollars to train 10,000 people by the end of 2027."

| t (s) | on screen | lands on |
|---|---|---|
| 0.07 / 0.41 | "In fact," (sup 84) top-left; real Claude Frontier Academy page in a tilted browser card slides up from 0.2 | In / fact |
| 0.81 | official Anthropic logo chip (top-right) pops; "Anthropic" hero 170 ink | Anthropic |
| 0.5–2.0 | page scrolls inside the card from the title to the stat block ($100M / 10,000 / 2027) | — |
| 0.73–1.15 | secondary speaker card (600x420) swings in tucked over the page's right side | — |
| 1.0 | Claude logo chip pops above the card (left) | — |
| 1.21 / 1.61 | "has" + "committed" (ocean) right-aligned | has / committed |
| 1.78–1.95 | header clears bottom-up (6 f blur-up exits), page card recedes (opacity .55, blur) | — |
| 1.75–2.05 | ring draws round the "$100M" stat; "$100" (230 ocean) arcs OUT of it, lands | hundred |
| 2.03–2.33 | "million" (170 ocean) arcs out of the same stat, right-aligned, staggered | million |
| 2.89 / 3.23 | "to train" (72) beside it | to / train |
| 3.39–3.69 | ring round "10,000"; "10,000" (190 ink) arcs out; "people" (80) pops at 4.43 | 10,000 / people |
| 4.63–5.07 | "by the / end of" bottom-right, page recedes a 2nd step (opacity .3) | by the end of |
| 5.05–5.27 | ring round "2027"; "2027." (220 ocean) arcs out, camera punch 1.2 %, underline draws 5.42 | 2027 |
| 5.3–5.82 | hold alive: grid drift, camera push, page drift-scroll, speaker video, float | — |

## As built
Browser card 840x680 at (90,780), URL `claude.com/programs/frontier-academy`, real capture scrolled 380 → 1029 px (power2.inOut, 0.5–2.0) then a linear
drift to 1062 until the cut. Rings are inside the scrolling page so they stay glued to the stat rows. Number lines are `.line.hero` with the
runtime hero entrance, plus a line-level arc from the stat's screen position (x power2.out, y power3.out, scale .25–.4 → 1, 0.3 s) ending on the word.
Each number has the paper glow. Speaker card 600x420 at (350,835), face-at .52, whole head in. Words omitted: "a" and "dollars" (rendered as "$100 million").

## Principles checklist
- Contact frames on words: every `.w` uses the runtime entrance (starts 0.13–0.2 s early); number arcs end on the word time.
- Anticipation: hero words dip (runtime); speaker/browser cards dip before travelling; ring draws before the number leaves.
- Overshoot + settle: hero peak 1.07–1.09 then back.out; cards back.out; chips via P.enter.
- Parts lag the whole: sheen lags card 3 f; "million" lags "$100" 8 f; ring leads number; chips staggered.
- Arcs: numbers leave the page on x/y with different eases; card slides in on a rotated arc.
- Squash/stretch: none needed (no coins/pills); logos and type never squashed.
- One focal point: page recedes (twice) as numbers land; header exits before $100 arrives.
- Secondary action: grid drift, camera push, page drift scroll, card float, live video, ring pulses, number pulses — no hold >= 1 s is dead.
- One exaggerated beat: "2027." punch + underline.
- Exits faster than entrances: 6 f exits vs 10–16 f entrances.
- Light/shadow: runtime shadows down-right, contact shadow under cards.
- Not a static slide: something moves in every second (scroll, floats, pulses).

## Deviations
Speaker card sits mid-right (x350–950, y835–1255) rather than a corner, so the stacked numbers and "2027" wrap around it. "a"/"dollars" not shown.

## Measured (175 frames, dark/blue-pixel bbox incl. soft card shadows)
Settled holds: x 69–962, y 292–1481 (the 1-2 px over 960/1480 is card shadow / punch+push). Entrance transients only: card slide-in y to 1510 (frames 8-9), left x 47 and right 971 during the Anthropic chip/card overshoot (frames 22-25, ~0.1 s). A faint blurred ghost of the page's own "2027" sits behind the landed number (accepted).

# CREATIVE PASS (v2)

New in this pass (runtime untouched, `--type-scale 0.94` kept, 175 f, hero times unchanged):
- **Cursor + marker swipes** on the real page: a cursor arcs in, clicks (dip), drags an accent marker across each stat just before it pops out; the page "wakes" (restore) when visited and recedes as the number leaves it.
- **Numbers pop OUT of the page and roll**: "$100" and "10,000" roll like odometer reels (per-digit vertical roll, digits lock left to right on the word), "2027." flips like a split-flap board (per-digit squash flip). Every digit locks on its real value; final values are exactly $100 / 10,000 / 2027.
- **People field**: a 28x4 field of tiny person pictograms (ocean, soft) fills in behind "10,000 people" in a radial wave from the landed number, a bright ripple runs left to right on "people" and a lighter return sweep leads into 2027. No count implied.
- **Anthropic chip**: 3D flip-in (rotateY, perspective), Claude chip pings (pulse + wobble) as the cursor finds the stat.
- Header clears a touch earlier so the first number can rise into its space; million lands from the same stat.

## New beat times (scene-local s)
| t | tag | what |
|---|---|---|
| 0.20 | whoosh | page card slides up behind |
| 0.81 | pop | Anthropic chip flip-lands + hero word (unchanged) |
| 1.00 | pop | Claude chip lands |
| 1.38 | ping | Claude chip pings |
| 1.45 | whoosh | cursor arcs onto "$100M" |
| 1.47 | tick | cursor click |
| 1.49-1.67 | whoosh | marker swipe across "$100M" |
| 1.65-2.13 | tick | odometer digits lock: hundreds 1.97, tens 2.05, ones 2.13 (rolling ticks 1.65-2.0) |
| 2.05 | pop | "$100" lands (unchanged) |
| 2.33 | pop | "million" lands |
| 3.11 | tick | cursor click on "10,000" |
| 3.13-3.31 | whoosh | marker swipe |
| 3.60-3.84 | tick | digits lock left to right |
| 3.62-4.15 | whoosh/riser | people field fills in a wave |
| 3.69 | pop | "10,000" lands (unchanged) |
| 4.43 | ping | "people" pop + bright ripple across the field |
| 4.70 | tick | cursor click on "2027" |
| 4.72-4.92 | whoosh | marker swipe |
| 4.79-5.27 | riser | split-flap digits flipping |
| 5.15 / 5.23 / 5.31 / 5.39 | tick | flap digits lock |
| 5.27 | impact | "2027." impact + 1.2 % punch (unchanged) |
| 5.50 | ding | accent underline draws |
