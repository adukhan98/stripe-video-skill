# v01_hook — key poses (written before animating)

Full-screen opaque scene, 1080x1920 @30, 3.867 s (116 f). Paper bg + 60px grid + vignette on every frame.
Speaker card (live video, 3D tilt, ocean edge) top; kinetic serif collage below it; five coins as secondary action.

| frame | t (s) | on screen | lands on |
|---|---|---|---|
| f0 | 0.00 | paper bg only; card starts rising from +120px, tilted back (rotX 26°, rotY -20°), scale 0.9 | "If" (0.00) |
| f4 | 0.13 | card fully opaque mid-rise; "if" lands | "if" |
| f9 | 0.30 | card readable (≈95% settled), face centred | — |
| f14 | 0.47 | card settled after a small rotX overshoot; line A "if you're trying to" built word by word | "to" (0.46) |
| f17 | 0.56 | "design" (Fraunces italic ocean) pops with extra overshoot | "design" (0.56) |
| f31 | 1.02 | line B "design with AI," complete | "AI," (1.02) |
| f36–43 | 1.20–1.44 | line A then line B slide up 46px, blur and fade (2 f apart) | — |
| f46 | 1.55 | "having" (small Newsreader) rises in | "having" (1.50) |
| f51 | 1.70 | "these" rises in | "these" (1.70) |
| f59 | 1.96 | "5" (Fraunces italic ocean 176px) hits peak overshoot 110%, settles | "five" (1.96) |
| f59–70 | 1.96–2.33 | coins 01→05 pop left→right on a gentle arc, 2 f apart, then float | "five" → "skills" |
| f67 | 2.22 | "skills" hits peak overshoot, settles | "skills" (2.22) |
| f77 | 2.56 | "is" | "is" (2.56) |
| f84 | 2.80 | "literally" | "literally" (2.80) |
| f96 | 3.20 | "a" (Fraunces italic ink) | "a" (3.16) |
| f102 | 3.40 | "cheat" pops; ocean underline starts its swipe; tiny camera push | "cheat" (3.40) |
| f107 | 3.56 | "code." lands, underline completes under "cheat code." | "code." (3.60) |
| f107–115 | 3.56–3.867 | hold alive: card float + slow tilt, coin float, camera push, grid drift; hard cut (no exit) | — |

## As built — v2 "GO BIGGER" revision (current render)

**What it shows:** the live speaker clip in a big tilted landscape card (868x600 at x62 y306; visually ~x 66-950 with the
tilt; rotY -9 to -6.5 deg, rotX 5 to 3.5 deg, ocean edge + soft drop shadow, face-centred crop = 20.5-59.4% of source height).
Below it a large kinetic serif collage fills the zone down to ~y 1470. Five white coins (92px, 01-05) pop on an arc that
hugs the card's lower-right corner (01-02 on the card's bottom seam, 03-05 climbing its right edge, clear of the face).
Full-screen opaque; hard cut out. Duration 3.866 s authored = exactly 116 frames.

**Type sizes:** "if you're trying to" 90 / "design" 150 (Fraunces italic ocean) / "with AI," 90 ·
"having" 86 + "these" 96 · "5 skills" 250 (Fraunces italic ocean) · "is literally" 100 + "a" 140 (Fraunces italic ink) ·
"cheat code." 164 (Fraunces italic ink) + ocean underline.

**Timeline (slot seconds, unchanged from v1):**
- 0.00-0.62 card rises 130px with a soft 3D settle (rotX 28->5 deg with overshoot, scale .88->1, inner video parallax 1.16->1, light sheen sweep); readable by ~0.13 s.
- 0.00-1.02 "if you're trying to / *design* with AI," word by word (design contact 0.56). 1.14-1.41 both lines slide up 64px + blur + fade (2 f apart).
- 1.55 "having", 1.70 "these" · 1.96 "5", 2.22 "skills" (pop to 108% / 106% on the word, settle) · coins start 1.86-2.13, 2 f apart, popping outward along the arc, then float.
- 2.56 "is", 2.80 "literally", 3.20 "a" · 3.40 "cheat", 3.56 "code." · 3.38-3.72 ocean underline swipe under "cheat code." + 0.8% camera push.
- Continuous: grid drift 20px, camera push 1.0->1.012 (origin 510,620), card float 4px + slow orbit, coin float, video push 1->1.035.

**Deviations:**
- "a cheat code." at ~190px is ~1170px wide and cannot fit the 900px zone, so "a" moved to the end of the "is literally" row
  (Fraunces italic 140) and "cheat code." sits alone at 164px (the widest that fits x 60-960 with the push).
- Added the spoken "having" before "these" (reads as said: "having these 5 skills is literally a cheat code."). "is", not "are".
- Card 868x600 rather than 900x620: the 3D tilt widens the near edge ~20px, so 868 is the widest that stays inside x 60-960.
- Total push is ~2% (1.012 slow + 1.008 punch) instead of 3%, because the content now fills the zone.
- Measured content bbox over all 116 frames: x 63-952, y 291-1469 (inside x 60-960, y 285-1480).
