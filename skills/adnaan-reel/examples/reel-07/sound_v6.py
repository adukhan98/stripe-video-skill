"""reel-07 v6 sound pass: sparse structural SFX (low & warm kit) + music bed with a +2.5 dB CTA lift.

Run AFTER `scenes.py edl` (which rewrites edl_scenes.json with one cue per beats.json entry):
    python3 edit/sound_v6.py
Replaces edl_scenes.json audio[] with 12 hand-placed cues and the music bed, and drops the legacy hook sub-drop.
"""
import json
import subprocess
from pathlib import Path

E = Path(__file__).resolve().parent
starts = {s["id"]: s["start"] for s in json.loads((E / "animations/slots.json").read_text())}
end = max(s["start"] + s["duration"] for s in json.loads((E / "animations/slots.json").read_text()))

# (scene, local time the sound should start, kit file, gain dB, why)
CUES = [
    ("v01_hook", 0.81, "stamp", -15, "hook: 1939 locks"),
    ("v02_board", 0.03, "clunk", -16, "hook: the board starts drawing"),
    ("v03_unsolved", 1.52, "paper", -18, "article strip slides in"),
    ("v04_impossible", 2.52, "whoosh", -18, "mode switch: full screen -> split"),
    ("v05_article", 0.62, "paper", -17, "the real article page slides in"),
    ("v06_three", 1.60, "pop", -16, "the three takeaways appear"),
    ("v07_outcome", 0.15, "thud", -15, "point 1"),
    ("v10_unreasonable", 0.20, "thud", -15, "point 2"),
    ("v13_grade", 0.13, "thud", -15, "point 3"),
    ("v14_test", 2.53, "whoosh", -18, "mode switch: canvas -> split"),
    ("v15_gauge", 1.37, "whoosh", -18, "mode switch: split -> canvas"),
    ("v18_cta", 2.27, "pop", -16, "CTA: lands in your inbox"),
]

# music: take 1, +2.5 dB over the last 3 s (0.5 s ramp) — the CTA energy lift
lift_t0 = end - 3.0
music = E / "music/take1_lift.wav"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(E / "music/take1.mp3"), "-af",
                f"volume='if(lt(t,{lift_t0:.3f}),1,if(lt(t,{lift_t0 + 0.5:.3f}),1+0.334*(t-{lift_t0:.3f})/0.5,1.334))':eval=frame",
                "-ar", "48000", str(music)], check=True)

p = E / "edl_scenes.json"
d = json.loads(p.read_text())
for r in d["ranges"]:
    r.pop("sfx", None)                                 # no legacy synth sub-drop on the hook
audio = [{"file": f"sfx_v6/v6_{kit}.wav", "start_in_output": round(starts[sid] + t, 3), "gain_db": g, "note": why}
         for sid, t, kit, g, why in CUES]
audio.append({"file": "music/take1_lift.wav", "start_in_output": 0, "duck": True, "gain_db": -19,
              "fade_in": 0.4, "fade_out": 2.0})
d["audio"] = audio
p.write_text(json.dumps(d, indent=1))
print(f"{len(CUES)} SFX cues + music bed (lift from {lift_t0:.2f} s) → {p.name}")
for a in audio[:-1]:
    print(f"  {a['start_in_output']:6.2f}  {a['file']:22} {a['gain_db']:>4} dB  {a['note']}")
