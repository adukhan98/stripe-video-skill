"""reel-07: hold the last on-camera frame where Adnaan glances down at his notes at a cut edge.

He often looks down while finishing his last word. Cutting there would clip the word, so instead the
video holds the last frame before the glance (end of a range) or the first frame after it (start of a
range) while the audio plays on. Re-run after every `render.py --base-only` (it rewrites base.mp4):

    python3 edit/freeze_lookdowns.py

Source times come from Apple Vision head pitch at 30 fps (edit/verify/lookdown_edges.json).
"""
import json
import math
import subprocess
from pathlib import Path

EDIT = Path(__file__).resolve().parent
FPS = 30
# range index -> source time the head first drops (end of range)
END = {0: 8.443, 1: 13.80, 3: 27.907, 5: 44.597, 6: 63.187, 7: 73.177, 8: 79.463, 9: 84.187,
       15: 125.193, 17: 141.59, 18: 153.53, 19: 157.42}
# range index -> last source time the head is still down (start of range)
START = {12: 100.553, 14: 116.19}


def main() -> None:
    segs = json.loads((EDIT / "timeline.json").read_text())["segments"]
    edl = json.loads((EDIT / "edl.json").read_text())["ranges"]
    filters, report = [], []
    for i, s in enumerate(segs):
        assert abs(s["start"] - edl[i]["start"]) < 1e-3, "timeline.json does not match edl.json — re-render the base"
        f0 = round(s["out_start"] * FPS)
        f1 = round((s["out_start"] + s["out_duration"]) * FPS) - 1          # last frame of this range
        if i in END:
            first = max(f0 + 1, math.floor((s["out_start"] + END[i] - s["start"]) * FPS) - 4)  # eyes drop ~3 frames before the head pitches
            if first <= f1:
                filters.append(f"freezeframes=first={first}:last={f1}:replace={first - 1}")
                report.append(f"range {i:2}: end hold frames {first}-{f1} ({(f1 - first + 1) / FPS:.2f} s)")
        if i in START and START[i] >= s["start"]:
            last = min(f1 - 1, math.ceil((s["out_start"] + START[i] - s["start"]) * FPS) + 4)  # eyes come back ~3 frames after the head
            if last >= f0:
                filters.append(f"freezeframes=first={f0}:last={last}:replace={last + 1}")
                report.append(f"range {i:2}: start hold frames {f0}-{last} ({(last - f0 + 1) / FPS:.2f} s)")
    base = EDIT / "base.mp4"
    raw = EDIT / "base_unfrozen.mp4"
    marker = EDIT / ".frozen"
    fresh = base.exists() and (not marker.exists() or base.stat().st_mtime > marker.stat().st_mtime + 1)
    if fresh:                                 # a new render.py base: keep it untouched and patch a copy
        base.replace(raw)
    tmp = EDIT / "base_frozen_tmp.mp4"
    graph, cur = [], "[0:v]"
    for k, f in enumerate(filters):            # freezeframes takes (main, replacement) inputs
        graph.append(f"{cur}split=2[m{k}][r{k}];[m{k}][r{k}]{f}[v{k}]")
        cur = f"[v{k}]"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(raw), "-filter_complex", ";".join(graph),
                    "-map", cur, "-map", "0:a", "-fps_mode", "passthrough",
                    "-c:v", "libx264", "-preset", "fast", "-crf", "16", "-pix_fmt", "yuv420p",
                    "-c:a", "copy", "-movflags", "+faststart", str(tmp)], check=True)
    tmp.replace(base)
    marker.write_text("base.mp4 = base_unfrozen.mp4 + look-down holds (a newer base.mp4 means a fresh render)\n")
    print("\n".join(report))
    print(f"→ {base} ({len(filters)} holds; untouched render kept as {raw.name})")


if __name__ == "__main__":
    main()
