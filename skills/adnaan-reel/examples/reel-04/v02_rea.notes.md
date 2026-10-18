# v02_rea: key poses and as-built notes (V2 revision applied, see the V2 section at the end)

Full-screen opaque scene, 1080x1920 @30, 6.866 s (206 frames). Paper background, 60 px grid drift and vignette are the same as reel-03 v01_hook.
Spoken: "There's a new open-source repo called Reverse Engineer Anything that lets Codex or Claude Code or any coding agent that you use"

## Key poses (slot seconds)

| t | frame | on screen | word |
|---|---|---|---|
| 0.00–0.62 | f0–19 | Real repo page (rea_repo.png) rises in a tilted 820x680 browser card (URL "github.com/morluto/rea"): 3D settle, sheen sweep. Slow internal scroll starts at 0.40. | There's / a / new |
| 0.22–0.82 | f7–25 | Speaker card (460x320, ocean edge) tucks in over the browser's lower-right corner. Face crop runs brow to chin. | new |
| 0.50 / 0.56 | f15 / f17 | Ocean dot pops, then the muted Geist label "open-source" (50 px) | open-source (0.70) |
| 1.12 | f34 | "repo" joins the label | repo (1.26) |
| 1.08→1.26 | f32→38 | Black stat pill "★ 100.8k on GitHub" pops over the page header (overshoot 108 %, settles) | repo (1.26) |
| 1.56 | f47 | Label lifts away with a blur | called |
| 1.60–2.10 | f48–63 | Page group glides down and back: browser to y 894 at 78 %, pill follows 1 f later, speaker card 2 f later | called |
| 2.06 | f62 | "Reverse": Fraunces italic ocean 206 px, overshoot peak | Reverse (2.06) |
| 2.48 | f74 | "Engineer": Newsreader 150 px, right-aligned pop | Engineer (2.48) |
| 3.00 | f90 | "Anything.": Fraunces italic ink 184 px, overshoot, plus a 0.8 % camera punch | Anything (3.00) |
| 3.34–3.82 | f100–115 | Speaker card drops away. Title compacts to a 43 % header (top-left). Browser shrinks to 42 % at the top-right. Stat pill tucks under it at 86 % | that / lets |
| 3.76→3.92 | f113→118 | "Codex" (Fraunces italic ocean 156) lands; black tool pill "Codex" pops lower-left | Codex (3.92) |
| 4.28 / 4.44 / 4.60 | f128 / f133 / f138 | "or" (80) / "Claude" / "Code" (Fraunces italic ink 134). Pill "Claude Code" pops lower-right | or / Claude Code |
| 4.92–5.90 | f148–177 | "or any coding agent" (Newsreader 92, "or" at 72) word by word. Pill "any coding agent" pops centre at 5.08 | or / any / coding / agent |
| 5.68→5.90 | f170→177 | Black agent puck (210 px, visor, dim ocean eyes) drops in centre-low; squash on contact | agent (5.90) |
| 5.84–6.15 | f175–185 | Three dotted ink paths draw from the pills into the puck. Dots then march along them for the rest of the scene | that |
| 5.98–6.48 | f179–194 | Pills dip, then ride their paths under the puck (3 f apart) and shrink away. Puck gulps on each arrival, ring and eyes light ocean | that / you |
| 6.46–6.92 | f194– | Glow blooms, puck bobs (peak 6.52, settles 6.62–6.92), blink at 6.76. Holds alive into the hard cut | use (6.62) |

Continuous through the whole scene: grid drift (−20/−12 px, linear), camera push 1.000→1.012, card float and orbit, page scroll, video push inside the speaker card, pill float, dots marching, puck float.

## Bounds (measured on all 206 frames from a background-less alpha render)
- Solid content (alpha > 100): x 60–957, y 290–1465. All frames are inside x 60–960, y 285–1480.
- Faint soft-shadow tails (alpha 16–40 %) reach x 958, y 1487 (the drop shadows under the browser card and puck). Nothing solid goes past 1480.

## Deviations
- "Anything." is 184 px, not ~210. At 206 px it measures 943 px wide, which is wider than the zone. "Reverse" stays at 206 px.
- The speaker card exits when beat B starts (3.34), the way reel-03 v02_skills does it, so beat B has room for the rows, pills and puck. The video clip is timed 0–3.9 s.
- The browser card's URL bar reads "github.com/morluto/rea". The stat pill covers the page's GitHub header and part of the tab row. It does not cover the URL.
- The tool pills carry a small generic ocean prompt glyph (chevron plus underscore) drawn as SVG next to the plain Geist text. No logos.
- Not shown on screen (by the brief): "There's a new", "called", "that lets", "that you use". The puck bob carries "use".
- Duration is written as 6.866 so the frame count comes out at exactly 206.

## V2 revision (2026-10-11)
- Type: everything is Inter Tight or Inter now; no italics anywhere.
  - "Reverse" Inter Tight 900, ocean, 220 px.
  - "Engineer" Inter Tight 900, ink, 170 px, right-aligned at x 928.
  - "Anything." Inter Tight 900, ink, 188 px.
  - "Codex" Inter Tight 900, ocean, 170 px (the one ocean word in beat B).
  - "Claude Code" Inter Tight 900, ink, 130 px. Its "or" is Inter Tight 700, 84 px.
  - "any coding agent" Inter Tight 800, 92 px. Its "or" is 700, 72 px.
  - Hero letter-spacing −0.045em, supporting −0.03em, line-height 0.88.
  - Label, URL, stat pill and tool pills are Inter 600 (URL Inter 500).
  - The compact header (43 %) keeps every word at 73 px or more.
- The font check now covers Inter Tight 900, 800 and 700 plus Inter 500 and 600.
- Speaker card is 600x418 in beat A, tucked over the browser's lower-right corner (x 340–940, y 972–1390).
  - After the 1.60 glide it is 95 % (570x397) at x 370–940, y 1020–1417.
  - Video is 610 px wide, window about 26.5–65 % of the source height. The face is centred and the chin is not cut.
- The stat pill sits 10 px higher after the glide (y 935) to clear the bigger card.
- Re-measured over all 206 frames:
  - Solid content (alpha > 100): x 70–959, y 290–1465.
  - Soft shadow tails (alpha > 40): x 70–960, y 290–1487, from the drop shadows under the browser and speaker cards.
