# v05_free — FUNNEL tier 2 ("free version") — key poses (planned before authoring)

| t (s) | frame | on screen | lands on |
|---|---|---|---|
| 0.00 | 0 | shared funnel drawn, tier 0 pencil hatch + 11 stick people (boiling); small speaker card top-right | — |
| 0.45 | 13 | red arrow drawn down the left of the funnel, head flicks into tier 1 | "After that" (0.13) |
| 1.19 | 36 | tier 1 hatching pencil; "20%" RED stamps bottom-left, camera punch + shake (HERO) | "20%" |
| 2.30 | 69 | real post strip (post_b2, 862 px card) flipped up top-left, speaker receded | "or about" |
| 2.45 | 74 | highlighter swipe behind "1-2B (~20%)" | "2" (2.37) |
| 2.71 | 81 | "2 billion" ink lands right of 20%; Caveat "1-2B" written right of tier 1 | "billion" |
| 3.20 | 96 | 4 stick people tumble from tier 0 into tier 1 | "people" (3.13) |
| 4.15 | 125 | post recedes + exits, speaker restores | "using" |
| 4.30 | 129 | tape slaps top-left, string drops, price tag swings in on it | "the" |
| 4.65 | 140 | "free" RED lands beside the swinging tag | "free" |
| 4.95 | 149 | red underline under "free" | "version" |
| 5.81 | 174 | ChatGPT chip drops, squash-lands, tape pressed on, right of tier 1 | "ChatGPT" |
| 6.73 | 202 | Claude chip drops, squash-lands, tape pressed | "Claude" |
| 6.93 | 207 | hold alive: tag sway, boil, card float, grid drift | cut |

## As built (scene seconds) — pass 2 (coordinator fixes + v04 continuity)

- **0.00** frame 0 matches v04_funnel's last frame:
  - same funnel geometry, same outline seed (4242), tier-0 hatch seed 1954, divider seeds 2931/3908/4885;
  - the 13-figure pile rebuilt from v04's pile table (feet, tilt, S 0.86 geometry, seeds 7000+i·61+k·7, arms down);
  - the camera starts at v04's end push (1.006 about 510,880) and goes to 1.009;
  - speaker card at v04's spot (x510, 420x360, face-at 0.62), y 304 instead of 300 to keep the punch inside the zone.
  - Checked side by side in `qa/pile_compare.png`: hatch and pile land on v04's positions; the leftover offset was the camera push, now matched.
- **0.02–0.55** red arrow down the left of the funnel into tier 1. **0.96–1.44** tier 1 pencil hatch.
- **1.19** "20%" (230, red) stamps, with camera punch 1.008 and a 3 px shake (hero beat).
- **1.86** the speaker card gets out of the way: it shrinks into its top-right corner with fade and blur (7 f). It is gone by 2.09.
- **1.96** post_b2 card (862 px, strip at 0.87) flips up. **2.22** highlighter behind "1-2B (~20%)".
- **2.37 / 2.71** "2" and "billion" (110, ink). **2.60** Caveat "1-2B".
- **2.73–3.43** four front-row pile figures (feet 305, 368, 431, 494) leave the pile: crouch, stretch, hop out with arms up, one tumble on an arc, squash-land in tier 1 (land 3.13 + k·3 f), arms drop, bounce. All 13 figures breathe 1.8 px, as in v04.
- **3.86** post recedes, **3.94** exits (6 f).
- **4.08–4.5** the speaker card returns with the runtime's card entrance (a second identical card, `data-at` 4.5; its video is trimmed with `data-media-start` 3.8 so it stays in sync).
- **4.18** tape. **4.22** string (≈100 px). **4.30** price tag, 142 wide x 246 tall, drops and swings −10°→+1.6°→−1.2°→+0.8°, then sways ±0.6° to the cut. The body lags about its hole. **4.48/4.52** hole + red ring.
- **4.45→4.65** "free" (150, red) lands at x 248–~500; the speaker card starts at 510. **4.86** red underline.
- **4.32** 20% and 2 billion settle to scale 0.97, anchored bottom-left. They stay fully opaque to the cut.
- **5.81 / 6.73** ChatGPT / Claude chips drop, the chip backgrounds squash, tape goes on (5.91 / 6.83).

## Principles checklist
- Contact frames on words: arrow 0.02 ("After" 0.13), 20% 1.19, highlight 2.22 → "2" 2.37, billion 2.71, people 3.13, free 4.65, underline 4.86 ("version" 4.95), ChatGPT 5.81, Claude 6.73.
- Anticipation: hero words sink before rising; pile figures crouch before the hop; tape before the tag; string before the tag; chips lift then fall.
- Overshoot + settle: 20% peaks at 1.12, free at 1.06; the pendulum decays; the chips and the card re-entry settle with back.out.
- Parts lag the whole: tag body lags the string; chip content lags the chip background by 2 f; figures 3 f apart; arrow head after the shaft.
- Arcs: figures hop and tumble on arcs (x and y eased differently); the tag swings on a pendulum arc; the speaker card arcs back in (runtime).
- Squash/stretch on shapes only: stick figures and chip backgrounds; never type or logos.
- One focal point: the speaker card leaves while the post is up; 20% / 2 billion settle back (motion only, fully opaque) while the tag is the focus.
- Secondary action, no dead hold ≥ 1 s: boil on fours, figures breathe, tag sways, card floats, grid drift, camera push. `slots.py --motion` reports no dead holds.
- One exaggerated hero beat: 20% (punch + shake + impact).
- Exits faster than entrances: the card leaves in 7 f, the post in 6 f; entrances take 16 f.
- One light direction / contact shadows: shadows fall downward on the cards, chips and tag.
- Not a static slide: something draws, lands, swings or breathes in every frame.

## Richness
- Hero object: the hand-drawn price tag swinging on its string ("free").
- Characters: v04's pile carried over; four figures leave it and tumble into tier 1 on "people"; all 13 breathe.
- Real post with a highlighter on "2", plus the hand-written real label "1-2B".
- Official ChatGPT and Claude chips dropped and taped on, with squash on the chip backgrounds only.

## Deviations
- "free" is 150, not ~160, so it fits between the tag and the card (as agreed).
- The tag is word-free, with a red reinforcement ring around its hole.
- To keep the 7 f exit inside the zone, the speaker card shrinks into its top-right corner instead of translating out of the frame.
- The card returns with the runtime entrance through a second card element (same clip, trimmed). One card can't be visible from frame 0 and also use the runtime's delayed entrance.
- Tag swing amplitudes are damped (+1.6° on the left) so the 142 px tag stays inside x ≥ 60.
- The speaker card is at y 304 instead of v04's 300 (4 px) to keep the 20% camera punch inside y ≥ 285.
- Logo chips sit right of tiers 1–2 (y 1054–1258), under the "1-2B" note.
- Lower zone has only the funnel outline until 20% lands at about 1.0 s.

## QA
- 208 frames (ffprobe). `slots.py check --motion`: checks passed, motion: no dead holds.
- Bounds: diff against a background-only render on all 208 frames gives x 61–955, y 287–1476, with 0 frames out of zone.
