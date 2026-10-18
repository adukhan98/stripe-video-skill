# SFX kit

## v6 — the house kit since reel-07 (his SOP: "the 30 % rule", low & warm > high & sharp)

Generated with **ElevenLabs Sound Effects v2** (`eleven_text_to_sound_v2`, prompt influence 0.6–0.75) on Adnaan's
account, low-passed twice at 5 kHz (+ 30 Hz high-pass), leading silence trimmed, peak-normalised to −1 dBFS, 48 kHz stereo.
Spectrum checked per file (energy above 5 kHz ≥ 15 dB under the body). `render.py` low-passes SFX again at 5 kHz
(`sfx_lowpass_hz`, written by `scenes.py edl --sfx-policy sop`).

| file | prompt (abridged) | use | default gain |
|---|---|---|---|
| `v6_stamp.wav` | heavy rubber stamp on a stack of paper, deep tactile thump | the HOOK scroll-stopper (0–4 s) | −15 |
| `v6_clunk.wav` | deep woody mechanical clunk (drawer latch / carriage lever) | 2nd hook sound, a hard structural lock | −16 |
| `v6_thud.wav` | soft felt mallet on a thick wooden table | point 1 / 2 / 3, the main structural beats | −15 |
| `v6_paper.wav` | thick sheet of paper sliding across a desk | a screenshot / article / card sliding in | −18 |
| `v6_whoosh.wav` | soft low breath of air passing | a MODE switch (split ↔ canvas ↔ full) | −18 |
| `v6_pop.wav` | warm muffled rounded pop | a small structural accent (list appears, CTA lands) | −16 |

**The rule (SOP):** sound on ~30 % of what moves, never on every pop. 0:00–0:04: 1–2 punchy tactile sounds with clean
space between them. After that ONLY structural transitions: introducing point 1/2/3, a mode switch, a major
screenshot sliding in, the CTA landing. A 70 s reel lands around 10–14 cues. Avoid: high dings, alarm bells, clock
ticking, typewriter clicks, marker squeaks, rising pitch whistles/synths.

Agents tag the beats that may sound in `beats.json` with `"role": "hook"` or `"role": "structural"` and a v6 tag
(`stamp thud clunk paper whoosh pop`); `scenes.py edl` (default `--sfx-policy sop`) keeps only those (hook ≤ 2 in the
first 4 s), and leaves every other beat silent. Mix targets (relative to a voice peaking near −2 dBFS before loudnorm):
SFX −16…−22 dB, music bed −22…−26 dB under speech (`--music`, ducked, +2.5 dB over the final 3 s).

## v4/v5 kit (legacy — `--sfx-policy all`)

House kit since v4 (reel-05): generated with **ElevenLabs Sound Effects v2** (`eleven_text_to_sound_v2`) through
Adnaan's ElevenLabs account, leading silence trimmed, peak-normalised to −1 dBFS, 48 kHz stereo.

| file | prompt (abridged) | use |
|---|---|---|
| `pop.wav` | soft rounded UI pop | cards/numbers/words landing, objects popping in |
| `tick.wav` | tiny crisp checkbox tick | checks, typing, cursor clicks, digits locking, deals |
| `impact.wav` | deep soft sub-bass thump | THE hero word/beat of a scene (1–2 per scene) |
| `riser.wav` | airy rising whoosh, peak ≈ 0.45 s in | build into a hero beat — cue it ~0.45 s before the hit |
| `whoosh.wav` | quick soft paper swish | cards sliding, objects flying, scene-start moves |
| `ping.wav` | soft glassy notification ping | notifications, pills, rings, "wake up" moments |
| `ding.wav` | two-note success chime | a payoff: ✓, full meter, flag, "it works" |
| `scribble1-3.wav` | felt-tip marker on paper (v5, reel-06; band-passed pink noise with a stroke rhythm, ffmpeg) | every audible marker stroke — a `scribble` beat with `dur`; variants rotate, trimmed to the stroke, −27 dB |

Synthesized legacy sounds (`sfx_synth.py`): `subdrop.wav` (hook range), `chime.wav`, `flick.wav`, `ticks.wav`,
and the old `synth/whoosh.wav`, `synth/ping.wav`.

Scenes declare their beats in `animations/<id>/beats.json`; `scenes.py edl` turns them into `audio[]` cues
with the per-tag default gains in `helpers/scenes.py` (`BEAT_GAIN_DB`, 3 dB lower since v5 — reel-06 carried ~230 kit
cues + ~120 strokes in 82 s).
