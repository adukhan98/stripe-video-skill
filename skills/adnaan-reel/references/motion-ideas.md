# Motion idea bank: how a scene becomes engaging, not just animated

In reel-05 the first pass was correct, but Adnaan asked for "more creative … more engaging" motion. The
creative pass below became the house level: **every paper scene = a hero object + 2–3 secondary
micro-animations from this list (or new ones in the same spirit), each landing on a spoken word**. Everything
here is built from the runtime's primitives (`P.*` + GSAP), brand tokens and soft shapes. No new colours,
outlines or emoji. The finished code is in `examples/reel-05/` (the hero objects, with their `beats.json`).

Rule of thumb: an idea earns its place when it **acts out the sentence**. "Hook up the AI to the systems" is
the puck wiring cables to cards, not a generic glow. If it only decorates, cut it. Stage everything with
`P.recede` so there is one focal point at a time.

## 1. A cursor that does the thing
- Clicks the real button: a press dip, a ripple, and the button state changes. A job card's **Apply**
  (reel-05 v01) and a comment box's **send** (v14).
- Ticks the boxes in rhythm, one click per spoken beat. Each completed row's bar fills with accent (v03).
- Marker-swipes the real stat on a captured page just before the number flies out of it (v09).
- Types the CTA word letter by letter with a caret (`P.typeIn`), then sends it as a bubble that flies into
  the headline (v14).

## 2. Real numbers that move to their real value
- **Odometer:** digits roll vertically and lock left to right on the real value, $100 → 10,000 (v09).
- **Split-flap:** each digit squash-flips and locks, for years and dates, e.g. 2027 (v09).
- **×N counter pill:** ×1 → ×2 → ×3 as each copy lands, for "tripled" or "doubled" (v10).
- **Calendar strip:** N tiles flip down from a top hinge for "six months". No month names, last tile accent (v10).
- **Meter:** an unlabelled pill track fills and snaps full with a glint, for "getting good" (v03).
- Never invent a number: unlabelled charts, gauges and meters only, or the real figure from the source.

## 3. Icons and UI that come alive
- Grid of department/app tiles: after the hero flip, each icon gets its own loop. The gear turns, chart bars
  breathe, the chat bubble types, the truck idles, the coin flips, the shield draws its check, document lines
  write (v05).
- System cards wake up as they connect: database layers stack, a new-mail dot slides into the inbox,
  doc lines write, CRM rows shuffle (v07).
- A network pulse: tiny accent connectors light between neighbouring tiles, travelling out from the centre (v05).
- Building lights: a grid of window lights cascades on inside a "company" frame (v03).
- Notification tower: pills arrive from alternating sides, each with a ripple ring from its dot. Older pills
  step up a slot first, and the stack sways (v10).

## 4. Physics (soft, believable, never slapstick)
- **Lanyard / badge:** the strap lags the pendulum swing, the clip jiggles on impact, a glint sweeps the plastic (v02).
- **Rope cables:** they draw out sagging, snap taut with an elastic wobble, and data packets flow both ways after (v07).
- **Liquid:** a tank with a travelling sine surface that pours in choppy, churns when the drain opens and
  sloshes at the bottom (v11).
- **Page curl:** copies peel off a card with the corner lifting toward camera, then flatten in flight (v10).
- **Shockwave:** a thin accent ellipse expands and fades behind a hero word. Add a paper-white echo ring
  when it sits over dark clothing (v02, v04, v08).
- **Dust burst:** 4–10 soft accent dots fly off a word or object on contact (v01, v02).

## 5. Characters with personality
- **The agent puck:** an antenna that trails and whips, eyes that follow each pulse, a happy ^^ squint and a
  hop when everything connects (v07).
- **Little people:** grey silhouettes try to drop into empty seats and get bounced out (v01). Others flail
  their arms as they drain out of a tank (v11), or hop onto the supply bar, two making it and three bonking
  back down (v12).
- **Strain:** the supply bar dips, trembles upward, sinks back twice, and two sweat-drop shapes fly off (v12).
- **An avatar that wakes:** a placeholder face on a badge pops its eyes open and turns to camera when the
  label stamps on (v02).

## 6. Type that performs (kinetic words stay readable)
- **Per-letter slam:** the letters of "at once" fly in from six directions and land on the same frame (v04).
- **Block drop:** F, D and E drop 2 frames apart as heavy blocks, and the last one is the impact (v08).
- **Stamp-in:** "one" scales 1.45 → 0.95 → 1.0 with a dust burst and a tiny 0.4 % punch (v01).
- **Cascade:** the letters of "hiring" arrive 2–3 frames apart, then run a small wave while held (v01).
- **Echoes:** two faint ink ghosts of "tripled" fan out, drift, then snap back into the word (v10).
- **Thinning:** two letters of "many" flicker down to 50–70 % opacity and stay readable (v08).
- **Sag:** the letters of "out" sag 12 px one by one and bounce back (v11).
- **Collapse:** "forward deployed engineer" slides into its initials with ghost trails, then F/D/E fly into
  one giant FDE (v02).
- **Shimmer:** a per-letter light wave across the hook's accent word every ~1.5 s, and an underline that
  re-draws once with a flourish (v01).
- **Ride:** "faster" rides the tip of the rocketing bar with a ghost trail, then detaches (v12).

## 7. Hero icons that land exactly on their word
- A padlock swings in with its shackle open and **snaps shut on "lock"** (v13).
- A star seal stamps the card corner on "expert" (v13).
- A clock tile ticks three times on "now" (v13).
- A dotted arrow draws under "where this industry" and flies off on "headed" (v13).
- A paper plane leaves his chest on "send you" and lands in the roadmap card (v14).
- A wrench swings in and taps "AI" twice with sparks on "implement" (v11).
- A magnifier that really magnifies: a 1.8× copy of the step under the lens (v06).
- A spotlight vignette tightens on the speaker card for "somebody", with a hand-drawn dotted ellipse and an
  arrow flick pointing at him (v06).

## 8. Hand-drawn (v5 marker layer — reel-06; all on `M.*`, boiling on fours)
- **Loop + double underline + sparkle ticks** on the hook's hero number; a marker arrow ties the text hook to the
  kinetic word that echoes it (v01).
- **Marker over full-screen footage**: a loop round the hero phrase on the paper strip, never over the face (v02);
  a padlock drawn beside the words whose shackle snaps shut on "lock" (v14).
- **A polaroid that develops** (washed-out → full colour) taped onto the paper; a logo chip swinging in like a hung
  sign at the end of a marker arrow (OpenAI → now at → Anthropic, v03).
- **The real post as taped strips** with a highlighter behind the spoken phrase; a stat underlined on the strip then
  flying out of it as a rolling odometer (v03, v05, v07, v10).
- **A diagram that draws itself** (rim, walls, spout — the way a hand would), then fills tier by tier with hatch:
  pencil for the many, red for "you" (v04 → v10).
- **Stick-people characters**: tumble on arcs into the drawing, squash and pile; a few hop down a tier; the crowd
  waves when a pin lands (v04, v05, v07).
- **Doodles that act out the sentence**: a crown on a search bar ("glorified"), a messy zig-zag scrawl across a post
  ("sloppy"), an empty chat bubble that types nothing and gets crossed out ("never interacted"), a price tag swinging
  on a string ("free"), a 3-week calendar struck through in one sweep that collapses into a clock whose hand spins
  two hours ("weeks → hours"), `</>` / doc / sparkle doodles drawing themselves round a portrait card (v06, v04, v05, v08, v09).
- **A magnifier that really magnifies** the drawing under it (a 2× seeded redraw clipped to the lens) (v10).
- **A locked lab door** with light leaking under it and ")))" sound waves for "heard about" (v10).
- **The camera pull-back**: a marker bubble crowded with logo stickers, then a log-scale zoom-out until it is a speck
  on a hand-drawn globe, then three tiny scratches on the surface ("barely scratched the surface") (v11).
- **A hand-drawn chart**: a red curve that bends up to vertical vs a flat ink line, a curly-brace bracket measuring
  the gap that stretches as the curve keeps climbing (v12).
- **A sunrise behind the portrait card**: horizon line, a red hatched sun rising from behind it, rays drawing out one
  by one and slowly rotating ("early", "golden") (v13).

## Sound goes with it
Every contact frame above is a candidate beat in `beats.json`: pop, tick, impact, riser, whoosh, ping or
ding, plus `scribble` (with `dur`) for every marker stroke (see `assets/sfx/README.md`). Use `impact` only for the
1–2 hero beats, ticks for clicks, checks, typing and digits, and `ding` for a payoff.
