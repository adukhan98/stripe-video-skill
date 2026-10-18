# v06_github — key poses (written before animating)

Full-screen opaque scene, 1080x1920 @30, 4.25 s (128 f). Paper bg + 60px grid + vignette every frame.
Spoken: "it's growing crazy on GitHub and you can try to just type in this command".

| frame | t (s) | on screen | lands on |
|---|---|---|---|
| f0 | 0.00 | browser card (github.com/trending, real page) rising + 3D settle; "it's" rising | "it's" (0.05) |
| f4–24 | 0.12–0.80 | page scrolls + zooms inside the card from the "Trending" header to the #1 row morluto / rea | — |
| f10–24 | 0.34–0.80 | "growing" lands; ocean ring draws round the morluto / rea row | "growing" (0.47) |
| f28–39 | 0.93–1.30 | HERO "crazy" (Fraunces italic ocean 250) peaks 110 % on the word; camera punch; black pill "★ 25,585 stars today" + "#1 Trending" tag pop | "crazy" (1.13) |
| f39–51 | 1.30–1.71 | "on GitHub" builds, right-aligned | "on"/"GitHub" |
| f54–60 | 1.80–2.00 | "it's growing" + "crazy" blur up and out (bottom-up) | — |
| f59–80 | 1.98–2.66 | "you can *try* to" builds; pills leave; browser card anticipates then shrinks back to top-left (60 %) | "you…try" (2.11–2.51) |
| f68–84 | 2.25–2.80 | secondary speaker card (560x390, face centred) swings in on the right | — |
| f72–86 | 2.40–2.85 | black terminal card rises in under it | "try" (2.51) |
| f79–112 | 2.62–3.72 | `$ npx rea-agents@latest setup` types character by character, ocean block cursor | "try to just type in this" |
| f88–106 | 2.92–3.53 | "just type in *this*" builds | "just…this" |
| f110–116 | 3.67–3.87 | HERO "command" (Fraunces italic ink 172) peaks 106 % on the word | "command" (3.87) |
| f105–119 | 3.50–3.96 | white cursor arcs down from the card edge to the Copy chip, click dip | — |
| f119–127 | 3.96–4.25 | chip flashes "Copied ✓" (ocean check + ring pulse); caret blinks; hold alive into the hard cut | — |

## As built (final render)

**What it shows:** Beat A: the real GitHub Trending capture (`assets/gh_trending.png`, dark theme) in a big tilted browser
card (840x580 at x76 y306, light chrome, URL "github.com/trending", rotY -7 → -4.5°, rotX 4 → 2.5°). Inside the card the page
scrolls from the "Trending" header down to the #1 row and zooms in (scale .78 → .95 → .985), an ocean ring (8 px, rounded,
soft ocean fill) draws round the `morluto / rea` row, a black "#1 Trending" tag pins onto the ring's top-right and the black
stat pill "★ 25,585 stars today" pops over the card's bottom-right edge. Beat B: the browser card shrinks back to the top-left
(60 → 61.5 %, origin top-left), the secondary speaker card (560x390 at x380 y452, rotY +8 → +6°, face-centred crop = 23.3–62.5 %
of source height) swings in on the right, and a black terminal card (848x182 at x96 y880) types `$ npx rea-agents@latest setup`
(Geist Mono 42 px, one char per step) with an ocean block caret; the white cursor arcs down to the "Copy" chip, clicks, and the
chip flips to "Copied ✓" (ocean check, ocean flash + ring pulse). Caret blinks into the hard cut.

**Type sizes:** "it's" 78 + "growing" 124 (Newsreader) · "crazy" 250 (Fraunces italic ocean) · "on GitHub" 114 ·
"you can … to" 80 + "try" 118 (Fraunces italic ocean) · "just type in" 98 + "this" 134 (Fraunces italic ink) ·
"command" 172 (Fraunces italic ink). Pills Geist 600 38/32 px, URL 30 px, chip 30 px.

**Timeline (slot seconds):**
- 0.00–0.62 browser rises 120 px with 3D settle + sheen; "it's" 0.00 (spoken 0.05).
- 0.16–0.78 page scroll + zoom to the #1 row; 0.33–0.75 ring draws; "growing" pop starts 0.31 (contact 0.47).
- 0.93 "crazy" hero rise → 110 % peak at 1.13 → settle; ring-fill pulse 1.06; camera punch 1.06 (+0.8 %);
  "#1 Trending" 0.94 (contact 1.12), stat pill 1.05 (contact 1.23).
- "on" 1.30, "GitHub" 1.58 (contacts 1.43 / 1.71).
- 1.80 "crazy" then "it's growing" blur up and out; 1.90 pills out; 2.00 browser anticipation (3 f lift) then 2.10–2.60 shrink
  back to top-left; 2.78 "on GitHub" out.
- "you" 1.98, "can" 2.16, "try" 2.35 (accent, contact 2.51), "to" 2.66.
- 2.28 speaker card swings in (readable ~2.40); 2.36 terminal rises in (readable 2.51 "try"); caret blink 2.46/2.54.
- 2.62–3.72 typing, 29 characters evenly; caret follows; blinks every 0.17 s from 3.92.
- "just" 2.92, "type" 3.14, "in" 3.26, "this" 3.37 (pop, contact 3.53); "command" 3.67 → 106 % peak 3.87 → settle; second
  punch 3.72 (to 1.2 %).
- 3.50 cursor appears at the card edge, arcs to the Copy chip; click contact 3.96 (scale dip), chip → "Copied ✓" 3.96–4.16,
  cursor fades by 4.16. Hold alive: grid drift, cam push 1.0 → 1.012, card floats + slow orbit, video push, caret blink.

**Measured bounds** (no-background render, all 128 frames): alpha>128 x 76–958, y 290–1456; alpha>40 (incl. soft shadows /
blur tails) x 73–958, y 290–1480. Every frame opaque (min alpha 255, first and last included). 128 frames exactly.

**Deviations:**
- The brief put the rea row at PNG y ~680–830; in the actual capture it is y 983–1284 (1080-wide PNG), so the framing uses that.
- Added the spoken "it's" (small, before "growing") and "you can try to" (2.11–2.79) so the lower zone isn't empty between
  "on GitHub" and "just type in"; "this" is Fraunces italic ink 134 on the "just type in" row and "command" sits alone at 172
  (Fraunces bold italic "this command" at ~180 is ~1000 px and cannot fit the 900 px zone; "command" alone at 180+ with
  overshoot also crossed x 60, so 172 with a 106 % peak).
- Geist Mono (not in the brand kit) copied into `hf/fonts/` from the user's own reel-03 storyboard fonts for the terminal
  command; declared in index.html and asserted loaded.
- "Copied ✓" is an in-place flip of the Copy chip (plus ocean ring pulse) rather than a separate tooltip above it, which would
  have sat on top of the speaker card.

## V2 revision (current render — supersedes type sizes, card size and duration above)

- **Duration:** root/video authored 4.233 s → exactly **127 frames** (was 128).
- **Type v2:** Inter Tight, no italics, accent = colour. Supporting words 800 (−0.03em), hero words 900 (−0.045em),
  line-height 0.88. "it's" 84 (700) + "growing" 128 · "crazy" 250 (900, ocean, peak 108 %) · "on GitHub" 116 ·
  "you can … to" 86 + "try" 124 (900, ocean) · "just type in" 92 + "this" 128 (900, ink) · "command" 190 (900, ink, peak 106 %).
  Each line has a max-width auto-fit (none needed to shrink at these sizes; "command" measures 742 px).
  Baselines: a1 1040, a2 1258, a3 1420, b1 1180, b2 1308, b3 1447.
- **Pills/UI:** Inter 600 (stat pill 38, tag 32, chip 30), URL Inter 500 30. Terminal command stays Geist Mono 42.
- **Speaker card:** 620x432 at x330 y438 (was 560x390), face-centred crop = 23.4–62.6 % of source height
  (video 620x1102, top −258). Terminal moved to y902, 848x172.
- **Font asserts:** 900/800/700 100px "Inter Tight", 500/600 40px "Inter", 500 42px "Geist Mono".
- **Timings unchanged** from the as-built list above (click 3.96, "Copied ✓" holds to the cut).
- **Measured bounds** (no-bg render, all 127 frames): alpha>128 x 73–957, y 290–1463; alpha>40 x 73–958, y 290–1478.
  Every frame opaque (min alpha 255).
