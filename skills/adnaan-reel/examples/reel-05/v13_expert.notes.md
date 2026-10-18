# v13_expert — fullscreen via P.growFull (250 f, 1080x1920 @30)

## Key poses
- f0 (0.0): portrait card (760x860 @ x160,y520, face-at 0.38) settling on paper, sheen sweep.
- 0.47–1.11: "how work gets done" (110, work ocean) top-left; 1.29–1.71 "in your field" (96) right-offset.
- 2.47: "domain" 200 ink on chest (strip A under it); top lines recede. 3.03: "expert" 220 ACCENT, hand-drawn underline.
- 3.1–3.3: paper words exit (6 f). 3.35: card anticipation dip; 3.45 'lock': card grows to full frame (0.6 s).
- 3.45/3.71 "lock in" 240 accent on strip B (1 % punch @3.5). 4.11 "learn" 170 ink + "how to do" 84.
- 4.93–5.49 "all of this stuff" 110. 5.79 "now" 220 accent. 6.11 "because / that" stack.
- 6.87 "where this" 120. 7.67 "industry" 170 ink (+ "is" 96). 8.09 "headed" 240 accent, alone, holds to the cut.

## As-built timeline (scene seconds)
Beat A 0–3.3 paper; exits a1 3.0, a2 3.05, a3 3.08, a4 3.1, underline 3.06. growFull 3.45–4.05.
Beat B swaps (4 f blur-up exits ending as the next phrase begins): b1 3.84, b2 4.72, b3 5.5, b4 6.68, b5 7.38, b6 7.82.

## Principles checklist
- Contact frames on words: yes, runtime starts every entrance 0.13–0.2 s before the word time.
- Anticipation before hero moves: hero words (runtime dip) and growFull (card 0.985 dip 3 f before 3.45).
- Overshoot + settle: hero peak 1.08–1.1 then back.out; card grow power3.inOut; punch 1.01.
- Parts lag the whole: sheen lags card; "how to do" lags "learn"; exit-lag staggers.
- Arcs: card settle rotation (rotationX/Y) arc; words rise-and-turn. No long object travel in this minimal beat.
- Squash/stretch: none (no shapes; type is never squashed).
- One focal point: top phrases P.recede when "domain/expert" land; one phrase at a time in beat B.
- Secondary action: grid drift, card float + tilt (A), video push + cam push (B), sheen, underline draw; no hold >= 1 s is dead (now 5.79–6.68 has because/that).
- One exaggerated hero beat: the card growing to full frame on 'lock' + 1 % punch.
- Exits faster than entrances: 6 f / 4 f exits vs 12–14 f entrances.
- One light direction: shadows down-right from runtime; nothing hand-rolled.
- Not a static slide: yes.

## Deviations
- Words omitted: "if you know", "and you're the", "and" (3.93), "is" (6.71, merged into the swap to "where"); comma dropped from "expert,".
- Added spoken connectives (not in the brief): "how to do", "all of this stuff", "because that" to fill the learn→now stretch.
- "learn" does not persist until "now": it swaps to "how to do" / "all of this stuff" because the usable low band (y 1290–1480, under his chin) fits one row only.
- Final line is "industry is" then "headed" alone (no room for a 2-row collage under the chin).
- Runtime untouched; the scene script trims the runtime's slow card tilt tween to end at 3.3 and uses its own float so growFull ends flush.
## Bounds (measured, glyph diff vs background-only render)
Settled words x 63–962, y 295–1481. Transients (hero overshoot, entrance rise from below at 6.4/7.1) reach y ~1489; side overshoot of expert/headed fixed by data-right 925 (max x 967).

## Revision 2 (swap overlaps + finale)
- Every outgoing phrase now finishes a 4 f blur-up at least 1 f before the next phrase's first visible frame (A: domain/expert exit 3.083, underline same; B: lock in 3.783, learn 4.633, where-this 7.3, industry 7.76, now/because/that 6.57), or sits on the other side of the frame: "all of this stuff" (84, left) / "now" (152, right) share no pixels.
- Beat B now: lock in (hero) > learn (pop, 170) > all of this stuff (84) + now (152, right) > because/that (left, with now) > where this (120) > industry (hero 170) > headed alone (240 accent, custom hero landing at 8.09: rise-from-blur to 1.12, back.out settle, 1.2 % punch).
- Dropped "how to do" and "is" (both would force an overlap); "industry is" + "headed" cannot fit together under his chin (190 px band), so "headed" is alone.
- Full all-frames bounds (250 frames, words-only render vs empty render, diff > 200): x 61-956, y 296-1485; only entrance-rise frames (6.37, 6.40, 7.10, 7.97) reach y 1481-1485.

## Creative pass (scene seconds; runtime untouched, --type-scale 0.94 kept)
New objects (all soft accent/deep/card shapes, one light direction): star-seal check badge, padlock, clock tile, dotted trail + arrow.
- 2.83-3.03 seal flies up from below-right and STAMPS the card corner on 'expert' (3.03): squash 2 f, ring ping, settles with back.out; pops off 3.36-3.5.
- 3.20-3.46 padlock swings in on an arc from the right (shackle open); shackle SNAPS shut 3.35-3.45 (4-power-in) exactly on 'lock' 3.45: body squash, ring ping, 4 px shake, with growFull + 1 % punch.
- 3.84 lock shrinks (0.55) to sit right of the words; float + glints at 4.11 and 5.00; pops out 5.40-5.54 before 'now'.
- 5.79 'now': pulse ring; clock tile lands 5.74-5.86; minute hand ticks at 5.99, 6.19, 6.39; clock exits 6.57 with the phrase.
- 6.95-7.95 dotted trail draws under the last phrases with an accent arrow leading (marching dots); arrow pulls back 8.0-8.09 and FLIES OFF right on 'headed' (8.09-8.35); the dotted trail stays under 'headed'.
- Word baselines lifted 6-12 px in the trail band (where this 1444, industry 1426, headed 1456).
Bounds (all 250 frames, diff > 200): text x 62-954, y 295-1490 (only entrance-rise frames 5.03/5.07/6.37/6.40 exceed 1480); objects: settled inside the zone; transients: seal and lock fly in from the right (x to ~1074) 2.87-3.37, arrow tip y 1481 at 7.57-7.6.
