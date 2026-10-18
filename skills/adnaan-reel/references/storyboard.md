# Storyboard: plan the whole video with the user, then build

> **adnaan-reel:** every beat is an opaque `scene` slot built in the house style — `references/style.md`
> and `references/scenes.md` win over anything below. The transparent-overlay / EDL-layout guidance here is
> inherited from video-edit and applies only to rare extras (e.g. a corner badge over a full-bleed demo).


Nothing gets built until the user approves a storyboard. The storyboard is the edit plan made
visible: every beat of the video in order, with what's said, what's on screen, how it moves, what
it sounds like, and which assets it needs. It is cheap to change; a rendered graphic isn't.

## Inputs (from the earlier steps)
- The packed transcript (`takes_packed.md`) and the pre-scan: the lines that carry the message,
  slips, fillers to cut.
- The **reference pass**: every concrete thing the speaker mentions, such as a product, launch, post,
  company, person, event, number or place. For each, propose the real thing: a clip (`fetch.py
  find`), a screenshot or capture, an official logo, a photo. The user's own assets come first.
  If they said they'll supply something, mark it `need`.
- **Media mapping**: every screen recording, screenshot and site, matched to the moment it is
  spoken (creator reels, video-edit's creator preset (not used in adnaan-reel)).
- Format and style, asked up front (vertical / landscape / both; brand / creator / mixed).

## Writing the beats
One beat per idea, usually one sentence of VO (2–7 s). For each beat:
- **section**: the archetype part (HOOK, POINT 1, PROOF, CTA…).
- **source / start / end**: the spoken line it sits on (source seconds from the transcript), or a
  `duration` for a beat with no speech.
- **vo**: the words, so the user reads the script alongside the pictures.
- **visual**: one of `a-roll`, `graphic`, `clip`, `broll`, `screenshot`, `media`, `split` or `text`.
- **layout**: one of `full`, `top`, `split`, `full_pip`, `lower_third`, `corner` or `none`.
- **media**: for a `split` / `full_pip` beat, the path of the recording or screenshot it shows.
- **description**: what the viewer sees, concretely ("the dots launch film plays in a rounded frame,
  'Source: OpenAI' bottom-left"), not "a cool graphic about agents".
- **motion**: the key poses and the principle doing the work ("card rises on an arc, 3 f
  anticipation; highlighter lands on 'billion'; slow push to the line").
- **audio**: SFX tied to visible events, plus music changes.
- **assets**: each with a status (`have`, `find` = I'll source it, `need` = the user supplies it, or
  `make` = built in a slot) and its rights class.
- **frame**: a thumbnail. A-roll beats pull one from the source automatically. For 2–3 hero
  graphic beats, make a **style frame**: a quick single-frame HyperFrames mock (`npx --yes
  hyperframes snapshot hf --at 1.2`) using the brand kit, so the user sees the look, not just
  a description of it.

Rhythm checks before showing it:
- No neighbouring beats look the same (vary layout and visual type).
- No a-roll stretch longer than ~8 s without a change (the builder warns).
- The hook beat lands its payoff within 2–3 s (creator: ≤ 3 s, and a visual change every ≤ 4 s).
- Graphic count is honest: fewer, better graphics. A board of 14 graphics in 40 s is a warning
  sign.
- Running time is near the target (the builder prints the difference).

## Building and showing it
```bash
uv run --project <skill_dir> <skill_dir>/helpers/storyboard.py --edit-dir <project>/edit
```
It writes `storyboard/storyboard.html` (open it in the browser pane, or give the path),
`storyboard/storyboard.jpg` (attach it in chat), and a versioned copy per round. For a short creator
reel, a compact beat table (time, words, layout, media, sfx) in chat can stand in for the board;
the gate is the same.

The check-in message is the brand board, the caption-style grid and the storyboard, plus:
- the beat list in plain text (id, time, one line each), so the user can reply "B4: use the real
  clip instead"
- the assets list: what you'll find, what you need from them, and which clips will be used as
  commentary (one confirmation covers them)
- the open questions, each with your proposed default

## Iterating
The user replies per beat. Write their words into that beat's `feedback`, change the beat, bump
`version`, and rebuild. Show only what changed ("v2: B3 now a split, B6 cut, B7 new"). Repeat
until they approve.

**The gate:** the user's explicit OK on a version ("approved", "go", "looks good, build it").
Record the approved version in `project.md`. From then on, build exactly that storyboard: the EDL
ranges come from its beats, `slots.json` from its graphic beats (description + motion become the
slot brief), and the reference assets get downloaded. If something has to change during the build
(an asset can't be found, a beat doesn't work in motion), say so when you deliver, or ask if it
changes the story.

Autopilot ("just do it", "no questions"): still write and build the storyboard, since it drives the
build, but don't wait. Attach it to the delivery with the assumptions listed.
