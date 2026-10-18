# v05_article — rev 3: v6 Mode C cutout (Adnaan's SOP)

225 f @30 (data-duration 7.4833 s on root + video). Spoken: 'I read this in an article recently called "How to be more ambitious:
a tutorial for humans with models". It's written by Felix, who is an engineer working on Claude.'

What changed from rev 2:
- The framed portrait card is gone. HE is now a `.spk cutout` using `assets/speaker_cut.webm` (background removed, VP9 alpha). He stands
  on the bottom edge IN FRONT of the big dark real page.
- The beat-A words moved to a paper strip between the title and his head.
- In beat B he sinks lower in the frame (instead of the card shrinking), making room for the words above his head.
- Earlier versions are kept at qa/index_v1_light.html (light strips) and qa/index_v2_card.html (portrait card).

## Key poses
| t (s) | on screen | lands on |
|---|---|---|
| 0.00–0.6 | HE (cutout, full frame width, dropped 392 px) stands on the bottom edge on the paper; hair ≈ y 760 | I read this |
| 0.48–0.82 | solid paper strip slides in at y 592–752 | in an |
| 0.62–0.85 | the REAL page (dark, felixrieseberg.com chrome) rises in BEHIND him; the full serif title sits at y ≈ 379–586, above the strip and his head | article |
| 0.65 / 0.85 | "an article" (120 ink) on the strip | an / article |
| 0.9–4.7 | red reading-progress bar under the chrome fills as he reads the title | How … models |
| 2.47 | "an article" exits (6 f) | — |
| 2.62 / 2.92 | highlighter (screen blend, glows on the dark page) swipes "ambitious:" in the real title; red marker underline in the line gap | ambitious |
| 2.79 | "ambitious" (172 RED hero) lands on the strip; 3.12–3.4 letters reach up one by one; 4.62 pulse on "models" | ambitious |
| 4.92–5.62 | page dips, then scrolls fast (blur) past the etching to "I work on Claude. It's an interesting experience: …"; card compacts to 3 lines (y 310–576); "ambitious" + strip exit 4.98–5.2 | written |
| 5.08–5.85 | he rises 10 px (anticipation) then sinks 262 px, settling 6 px back (hair ≈ 1016+) | written / by |
| 5.44 / 5.52 / 5.88 | Caveat "by Felix" (74 ink) beside the card; highlighter on "I work on Claude"; red underline | Felix |
| 6.18–6.46 | "an engineer" (108 ink) | an / engineer |
| 6.78 / 7.06 | "working on" (108 ink) | working / on |
| 6.86–7.25 | red marker arrow swoops from "on" to the hang point | on |
| 7.08–7.28 | HERO: the official Claude chip swings in on the arrow's end like a hung sign and squash-lands; camera punch + shake; "Claude" (170 RED) lands 7.26 | Claude |
| 7.36–7.48 | tape on the chip, pendulum back-swing, boil, push — alive into the cut | — |

## As built
- Speaker: `<div class="spk cutout" data-w="1080" data-x="0" data-drop="392">` + `speaker_cut.webm`.
  - Full width, so both side crops of the footage sit on the frame edges. The bottom crop is the frame edge.
  - Only his hair/head/shoulders silhouette is a cut edge, and it looks clean on the sheet.
  - Face centre ≈ (540, 1180) in beat A, ≈ (540, 1436) in beat B. The runtime adds a 1.0 → 1.015 push.
  - The wrapper `#spkW` does the beat-B sink.
- Page: `#pcW` (rotate -1°) > `.browser#pc` 848x1082 at (88,310), dark chrome, viewport bg rgb(18,17,14).
  - `art_page_dark.png` is 900 px wide (0.714 scale) at x -16. Beat A scroll y -199 (title ink at frame y 379–586); beat B y = 24 − 0.714·2072.
  - cardIn 0.62 (fromY 40, rot -1.5). Compaction 5.10–5.62 to 66+200 px. Scroll 5.05–5.61, power3.inOut, blur 0→5→0.
- Highlights: `M.highlight(#pg, …)` with `.mk-hl { mix-blend-mode: screen }` and `.mk-hl path { fill: none !important; }`.
  Boxes: [48,384,509,88]·0.714 and [48,2058,408,72]·0.714, opacity 0.62.
  The underline under "ambitious:" is drawn on the page's own svg (seed 5051), so it rides the tilt and the scroll.
- Strip `#strip`: solid paper, 770x160 at (64,592), scaleX 0.2→1 at 0.48, exits at 5.0.
- Kinetic:
  - "an article" 120 (base 716) and "ambitious" 172 (base 732, rise 22, peak 1.03), both on the strip.
  - "an engineer" 108 (base 692), "working on" 108 (base 812), "Claude" 170 red (base 986).
- Marker: note "by Felix" 74 px at (652,584) 5.44; underline 5.88 (seed 5071); arrow B (seed 5091) 6.86.
- Chip: `.chip.big` (claude.png 72 px + "Claude" Inter 600 50 px), right edge 928, top 872.
  - Pendulum -11° → 3° → -2°; squash 7.28; tape 7.36; P.punch(1.006) + P.shake(3) 7.28.

## Principles checklist
- Contact frames on words: runtime entrances 0.13–0.2 s early. The page lands on "article"; highlight + word on "ambitious"; scroll on
  "written"; highlight on "Felix"; chip + word on "Claude".
- Anticipation: page dips before the scroll; he rises 10 px before sinking; hero words dip (runtime); squash pre-stretch on the chip.
- Overshoot + settle: page card 1.01 → 1; the sink overshoots 6 px and settles; chip pendulum; words (runtime).
- Parts lag the whole: sheen lags the page card 3 f; strip leads the words; compaction lags the scroll 2 f; the sink starts 1 f
  after the scroll; ambitious letters 2 f apart; arrow head after shaft; tape after the chip lands.
- Long moves on arcs: chip pendulum, curved arrow. The sink is a straight vertical move (a cutout standing on the frame edge must not
  drift sideways).
- Squash/stretch on shapes only: the chip (7 %).
- One focal point: beat A — title + highlight + "ambitious" over his head; beat B — highlighted line → words → chip. Two-element
  guideline: page + its words, then words + chip.
- Secondary action, no dead hold ≥ 1 s: live footage, progress bar, letter wave, pulse, boil, grid drift, push (slots.py: no dead holds).
- One exaggerated hero beat: Claude chip (punch + shake, impact).
- Exits faster than entrances (6 f vs 10–16 f).
- One light direction: runtime soft down-right shadows; the page card has a deeper soft shadow.
- Nothing reads as a static slide.

## Richness (hero + micro-animations)
- HERO: he stands in front of the real dark page → the page scrolls to "I work on Claude." → the official Claude chip swings in on a
  red marker arrow (Claude).
- Reading-progress bar fills as he reads the title and jumps with the scroll.
- Paper strip slides in; "ambitious" letters reach up one by one; pulse on "models".
- He sinks to make room for the words while the page compacts (written).
- Handwritten "by Felix" + red underline — no photo of Felix.

## Readability
- The page is shown at 0.714 scale (coordinator spec); title ≈ 53 px serif, paragraph ≈ 36 px. Only the title is in view in beat A and
  only 3 lines in beat B. Highlighter behind the phrase, no loops.
- No semi-transparent text. Words sit on the solid strip or on paper, never over his face. Nothing crosses the title.
- No content in the bottom 20 % (all words/chip ≤ y 1000). x ≤ 900 below y 1200 holds: nothing but him is below y 1000.
- Sizes (authored): hero 172 / 170, supporting 120 / 108 / 108; note 74 px ink; chip logo 72 px.

## QA
- Frames: 225 (ffprobe -count_packets). slots.py check --motion: "motion: no dead holds · checks passed: size, fps, duration, alpha channel".
- Content bounds: every frame of a speaker-less render (qa/nospk.mov) was diffed against a background-only render (qa/bg.mov), threshold 24
  (qa/bounds_nospk.py). Result: x 69–956, y 288–1430, 0 frames outside x 60–960 / y 285–1480. All words and the chip stay ≤ y 1000.
  Fixed on the way: the page card's overshoot at its top-right (y 282 → card top 310) and the chip's swing (x 962 → right edge 928).
- Full render: the speaker cutout covers x 0–1080, y ≈ 800–1920 by design (Mode C: he stands on the bottom edge). Only he is outside
  the content zone.
- Cutout edge (qa/edge.jpg, sheet): the hair/head silhouette is clean against the dark page and the paper, with no visible crop lines
  (side and bottom crops sit on the frame edges). A faint warm fringe from the matte shows beside one ear in a few beat-A frames
  against the dark page; it is only visible up close.
- Highlighter mid-swipe: no fill line (the scene CSS fix is kept).

## Deviations
- Cutout width is 1080 (full frame) rather than 760–900. At 840 the footage's left crop showed as a hard vertical edge through his
  hoodie (his shoulders reach the source's edges). A feathered mask still read as a band. Full width puts every crop on the frame
  edge. He is dropped 392 px so his hair clears the title + strip; his head is big (Mode C emphasis), face centred rather than right of centre.
- No marker arrow at the title (text on every side of "ambitious:"). It gets a red underline in the line gap + the highlighter.
- "an engineer" is one line at 108 (brief ~110). "working on" (108) and "Claude" (170) are split.
- The scene is 225 frames now, so the hero chip lands at 7.28 with ~0.2 s before the cut: the pendulum settle and the punch's
  ease-back finish past the cut.
