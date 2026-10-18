# v18_cta — CTA, MODE A (split) + freeze-frame end hold, 151 frames (5.033 s)

Mode A (v6 three-mode SOP): `<div class="spk split" data-h="960">` — his footage edge to edge in the top half (y 0-960) from frame 0 to
the last frame (slow push only, no card/tilt/float). Paper + grid + kinetic words + the paper plane own the bottom band (y 1000-1480).
Nothing sits in the lower-right icon corner (everything below y 1200 is x <= 860) and nothing below y 1480.

## Key poses (scene seconds)
- 0.17 `Comment` (ink hero 141) lands at the top of the band. 0.63 `“ambitious”` (red hero, ~150 px, fit 840) lands with a 4 f shake + 1.2 % punch = the IMPACT; 0.60-1.02 red double underline under word + quotes (marker never crosses type).
- 1.0-1.3 staging: the headline steps back (scale 0.68 from its top-left, words never fade) to make room for the one object; 1.00-1.78 `I'll send you the article` on the bottom row (base y 1458, text ~1410-1472), `article` in the accent.
- 1.28 the REAL art_title.png strip (first two lines, 468 px wide, ~56 px text, y 1258-1392) drops in ABOVE the phrase with >= 20 px of clear air to its text (top ~1416), settles with overshoot. 1.50-1.57 anticipation, 1.57-1.77 FOLD 1 (top half flips down in 3D), 1.77-1.90 FOLD 2 (strip cut to a dart), 1.90 paper plane pops.
- 1.86-1.99 the `→ your inbox` pill (50 px Inter 600, ~380x92, x 440-820, y 1288-1380 = bottom-centre) drops in. 1.96-2.03 plane tilts back (anticipation); 2.03-2.30 it flies a small arc to the pill's arrow, a dotted accent trail draws with it and stays.
- 2.29 pill squash + double ripple, 2.33 check badge pops. 2.44-3.13 `you can read it too.` (bottom row, `read` accent).
- 2.85-3.05 the pill, badge and trail leave (4-5 f blur-out) once delivered. 3.05-3.3 FINAL ENERGY LIFT: the headline returns from 0.68 to full hero size (power3.out, no overshoot so x stays <= 860) with a 1 % punch; `ambitious` pulses 1.02 at 3.3.
- 3.3-5.03 end hold: headline at full size, `ambitious` breathes 1.2 %, underline boils on fours, `you can read it too.` below, his footage keeps talking and pushes 1.0 -> 1.02, grid drifts.

## Principles checklist
- Contact frames on words: yes (words start 0.13-0.2 s early; plane launch 2.03, arrival 2.29).
- Anticipation: top half lifts before fold 1; plane tilts back before launch; hero words sink before rising.
- Overshoot + settle: sheet 1.04 -> 1.0, plane 1.06 -> 1.0, badge 1.12 -> 1.0, pill back.out.
- Parts lag the whole: rings 3 f apart, badge after the pill.
- Arcs: sheet drops with an arc, plane flies a cubic arc (autoRotate).
- Squash/stretch: pill only (a shape), never type or the real title.
- One focal point (two-element guideline): CTA word, then ONE object at a time (headline steps back by scale, never by fading words).
- Secondary action: no hold >= 0.5 s is static (end hold list above).
- One exaggerated beat: `ambitious` impact (shake + punch + underline).
- Exits faster than entrances: `I'll send you the article` leaves in 4 f at 1.78.
- One light direction / contact shadows: tight shadows down-right, nothing trails below y 1480.
- Not a static slide: footage, boiling marker, bobbing pill and marching trail run to the last frame.

## Richness
Hero object: the real article title strip folds twice (3D flip, then dart cut) into a paper plane and flies into the inbox pill. Secondary: double marker underline + shake on `ambitious`; ripple + delivered-check badge on arrival; dotted trail that stays.

## Readability / safe zone
- Pill 50 px Inter 600; title strip text ~56 px; bottom-row phrases 66 px; hero ~150/141 px in the end hold.
- Lower-right icon corner kept clear: below y 1200 everything is x <= 860 (measured); nothing below y 1480 (measured); no text over his face (the band is paper).
- Measured on all 151 frames of the final render vs a background-only render (half-res diff, coords x2), paper band y >= 962: visible content (diff > 60/255) x 66-850, y 1002-1478; incl. faint shadow pixels (diff > 24) x 62-850, y 1000-1480; max x below y 1200 = 850; zero violations (qa/bounds_final.txt).

## Deviations
- `right away` is not shown (Mode A brief lists Comment / ambitious / I'll send you the article / you can read it too): the plane launches on `right away` with no word on screen. `and` and `so` omitted (fillers).
- `ambitious` is authored 210 but `data-fit 770` (incl. quote marks + overshoot, x <= 860 below y 1200) shrinks it to ~150 px; it steps back to 0.68 scale while the object plays and returns to full size at 3.05-3.3 for the end hold (the pill leaves first).
- The previous speech-bubble doodle, dotted word path and burst rays were cut (two-element guideline).
- Title strip is the first two lines of art_title.png, 468 px wide (band is only ~220 px tall under the headline).
- The pill is gone for the last ~2 s (it delivers at 2.29, leaves at 2.85) because the full-size headline needs its space; the plane trail leaves with it.
