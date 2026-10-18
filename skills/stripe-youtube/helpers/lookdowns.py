"""Hide the look-downs left inside kept speech: hold an on-camera frame while the voice plays on.

He glances at his notes between lines. The pauses are cut, but the first ~0.1–0.6 s of many lines still show his head
coming back up (IMG_2533: "cut out … times when I'm looking down"). At a range start this holds the first frame after he
looks up, at a range end the last frame before he looks down; a range that is down from start to end holds the previous
range's last frame. Only the picture changes — the voice is copied untouched, so lip sync is unaffected.

Look-down spans come from adnaan-reel's headpose.py (Apple Vision head pitch) over the whole take:
    uv run --project ~/.claude/skills/adnaan-reel python ~/.claude/skills/adnaan-reel/helpers/headpose.py \\
        <edit>/source/cam.mov --start 0 --end <take seconds> > <edit>/headpose_report.txt
(its last line is "# looking down: a-b, c-d, …" in source seconds).

Re-run after every `render.py --base-only` (it rewrites base.mp4). The first run on a fresh render keeps it as
base_unfrozen.mp4 and patches a copy; later runs start from base_unfrozen.mp4 again.
    python helpers/lookdowns.py --edit-dir E [--pad 4]
"""

from __future__ import annotations

import argparse
import json
import math
import subprocess
from pathlib import Path

FPS = 30


def down_spans(report: Path) -> list[tuple[float, float]]:
    line = report.read_text().strip().splitlines()[-1]
    if not line.startswith("# looking down:"):
        raise SystemExit(f"{report}: last line should be '# looking down: …' (headpose.py output)")
    body = line.split(":", 1)[1].strip()
    return [] if body == "none" else [tuple(map(float, s.strip().split("-"))) for s in body.split(",")]


def holds(segs: list[dict], down: list[tuple[float, float]], pad: int) -> tuple[list[str], list[str]]:
    filters, report = [], []
    for i, s in enumerate(segs):
        a, b = s["start"], s["end"]
        f0 = round(s["out_start"] * FPS)
        f1 = round((s["out_start"] + s["out_duration"]) * FPS) - 1
        to_f = lambda t: (s["out_start"] + t - a) * FPS  # noqa: E731
        head = next((d for d in down if d[0] <= a + 0.05 and d[1] > a), None)
        tail = next((d for d in down if d[1] >= b - 0.05 and d[0] < b), None)
        if head and head[1] >= b - 0.05:                      # down for the whole range
            if i > 0:
                filters.append(f"freezeframes=first={f0}:last={f1}:replace={f0 - 1}")
                report.append(f"range {i:3}: WHOLE hold {f0}-{f1} ({(f1 - f0 + 1) / FPS:.2f} s)  src {a:.2f}-{b:.2f}")
            continue
        if head:
            last = min(f1 - 1, math.ceil(to_f(head[1])) + pad)
            if last >= f0:
                filters.append(f"freezeframes=first={f0}:last={last}:replace={last + 1}")
                report.append(f"range {i:3}: start hold {f0}-{last} ({(last - f0 + 1) / FPS:.2f} s)")
        if tail:
            first = max(f0 + 1, math.floor(to_f(tail[0])) - pad)
            if first <= f1:
                filters.append(f"freezeframes=first={first}:last={f1}:replace={first - 1}")
                report.append(f"range {i:3}: end hold {first}-{f1} ({(f1 - first + 1) / FPS:.2f} s)")
    return filters, report


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--edit-dir", required=True, type=Path)
    ap.add_argument("--report", type=Path, help="headpose report (default <edit>/headpose_report.txt)")
    ap.add_argument("--pad", type=int, default=4, help="frames: eyes lead/lag the head pitch by ~3 frames")
    a = ap.parse_args()
    edit = a.edit_dir.resolve()
    segs = json.loads((edit / "timeline.json").read_text())["segments"]
    filters, report = holds(segs, down_spans(a.report or edit / "headpose_report.txt"), a.pad)
    base, raw, marker = edit / "base.mp4", edit / "base_unfrozen.mp4", edit / ".frozen"
    if base.exists() and (not marker.exists() or base.stat().st_mtime > marker.stat().st_mtime + 1):
        base.replace(raw)                     # a fresh render.py base: keep it untouched and patch a copy
    graph, cur = [], "[0:v]"
    for k, f in enumerate(filters):            # freezeframes takes (main, replacement) inputs
        graph.append(f"{cur}split=2[m{k}][r{k}];[m{k}][r{k}]{f}[v{k}]")
        cur = f"[v{k}]"
    tmp = edit / "base_frozen_tmp.mp4"
    if graph:
        script = edit / "verify" / "freeze_graph.txt"
        script.parent.mkdir(exist_ok=True)
        script.write_text(";".join(graph))
        vid = ["-filter_complex_script", str(script), "-map", cur]
    else:
        vid = ["-map", "0:v"]
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", str(raw), *vid, "-map", "0:a", "-fps_mode", "passthrough",
                    "-c:v", "libx264", "-preset", "fast", "-crf", "16", "-pix_fmt", "yuv420p", "-c:a", "copy",
                    "-movflags", "+faststart", str(tmp)], check=True)
    tmp.replace(base)
    marker.write_text("base.mp4 = base_unfrozen.mp4 + look-down holds (a newer base.mp4 means a fresh render)\n")
    print("\n".join(report))
    print(f"→ {base} ({len(filters)} holds; untouched render kept as {raw.name})")


if __name__ == "__main__":
    main()
