"""Read a Cap recording project (.cap) and lay its tracks on one clock.

A Cap project keeps every track separate (recording-meta.json):
    content/segments/segment-N/display.mp4    the screen (often 24 fps, e.g. 1600x1000)
    content/segments/segment-N/camera.mp4     the webcam (e.g. 1280x720 @ 30)
    content/segments/segment-N/audio-input.ogg  the mic
    content/segments/segment-N/cursor.json    {"clicks": [{time_ms, down, cursor_id}], "moves": [{time_ms, x, y}]} (x, y 0–1)
and project-config.json holds what he did in Cap's editor: timeline.segments (the parts he KEPT) and
timeline.zoomSegments (zooms he placed). Both are his intent — the cut starts from his trims, his zooms win.

Usage:
    python helpers/cap.py find                                   # recent Cap projects, newest first
    python helpers/cap.py info <project.cap>
    python helpers/cap.py ingest <project.cap> --edit-dir E      # → E/source/{cam.mov, screen.mp4, cap.json}

ingest writes:
    cam.mov     camera + mic (PCM), CFR 30 fps — the EDL source "CAM" (transcribe, cut and the speaker card come from it)
    screen.mp4  the screen at its native size, CFR 30 fps, on the SAME clock (cut with the same ranges by compose.py)
    cap.json    {"screen": [w, h], "duration", "clicks": [{t, x, y}], "moves": [{t, x, y}], "trims": [[a, b]],
                 "zooms": [{start, end, amount, mode, x?, y?}]}   — all times in seconds on the ingested clock
Multi-segment recordings (pause/resume) are concatenated in order; their times are offset accordingly.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

CAP_DIR = Path.home() / "Library" / "Application Support" / "so.cap.desktop" / "recordings"
FPS = 30


def run(cmd: list[str]) -> None:
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"command failed: {' '.join(cmd[:6])} …\n{r.stderr[-1200:]}")


def probe(path: Path) -> dict:
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=codec_type,width,height,r_frame_rate",
                        "-of", "json", str(path)], capture_output=True, text=True)
    return json.loads(r.stdout or "{}")


def duration(path: Path) -> float:
    return float(probe(path).get("format", {}).get("duration", 0) or 0)


def load(project: Path) -> tuple[dict, dict]:
    meta = json.loads((project / "recording-meta.json").read_text())
    cfg_p = project / "project-config.json"
    cfg = json.loads(cfg_p.read_text()) if cfg_p.exists() else {}
    return meta, cfg


def segments(project: Path, meta: dict) -> list[dict]:
    out, offset = [], 0.0
    for i, s in enumerate(meta.get("segments") or []):
        disp = project / s["display"]["path"]
        cam = project / s["camera"]["path"] if s.get("camera") else None
        mic = project / s["mic"]["path"] if s.get("mic") else None
        cur = project / s["cursor"] if s.get("cursor") else None
        d = duration(disp)
        out.append({"i": i, "display": disp, "camera": cam if cam and cam.exists() else None,
                    "mic": mic if mic and mic.exists() else None, "cursor": cur if cur and cur.exists() else None,
                    "offset": offset, "duration": d,
                    "lag_cam": float((s.get("camera") or {}).get("start_time", 0) or 0) - float(s["display"].get("start_time", 0) or 0),
                    "lag_mic": float((s.get("mic") or {}).get("start_time", 0) or 0) - float(s["display"].get("start_time", 0) or 0)})
        offset += d
    return out


def cursor_events(segs: list[dict]) -> tuple[list[dict], list[dict]]:
    clicks, moves = [], []
    for s in segs:
        if not s["cursor"]:
            continue
        d = json.loads(s["cursor"].read_text())
        mv = sorted(d.get("moves") or [], key=lambda m: m["time_ms"])
        for m in mv:
            moves.append({"t": round(s["offset"] + m["time_ms"] / 1000, 3), "x": m["x"], "y": m["y"]})
        for c in d.get("clicks") or []:
            if not c.get("down"):
                continue
            t = c["time_ms"] / 1000
            prior = [m for m in mv if m["time_ms"] / 1000 <= t] or mv[:1]
            if not prior:
                continue
            p = prior[-1]
            clicks.append({"t": round(s["offset"] + t, 3), "x": p["x"], "y": p["y"]})
    return clicks, moves


def info(project: Path) -> dict:
    meta, cfg = load(project)
    segs = segments(project, meta)
    clicks, moves = cursor_events(segs)
    tl = cfg.get("timeline") or {}
    first = segs[0]
    pd = probe(first["display"]).get("streams", [{}])[0]
    return {
        "project": str(project), "name": meta.get("pretty_name"),
        "segments": len(segs), "duration": round(sum(s["duration"] for s in segs), 3),
        "screen": [pd.get("width"), pd.get("height")], "screen_fps": pd.get("r_frame_rate"),
        "camera": all(s["camera"] for s in segs), "mic": all(s["mic"] for s in segs),
        "clicks": len(clicks), "moves": len(moves),
        "trims": [[round(x["start"], 3), round(x["end"], 3)] for x in tl.get("segments") or []],
        "zooms": [{k: z.get(k) for k in ("start", "end", "amount", "mode")} for z in tl.get("zoomSegments") or []],
        "cap_camera_layout": (cfg.get("camera") or {}).get("position"),
    }


def ingest(project: Path, edit: Path) -> None:
    meta, cfg = load(project)
    segs = segments(project, meta)
    if not all(s["camera"] for s in segs):
        sys.exit("this Cap project has no camera track — record with the camera on (the card and talk beats need it)")
    src = edit / "source"
    src.mkdir(parents=True, exist_ok=True)
    tmp = src / "_parts"
    tmp.mkdir(exist_ok=True)
    cam_parts, scr_parts = [], []
    for s in segs:
        cp, sp = tmp / f"cam_{s['i']}.mp4", tmp / f"screen_{s['i']}.mp4"
        d = f"{s['duration']:.3f}"
        # camera + mic → CFR 30, 48 kHz; tracks shifted by their start_time lag against the display (usually ~0)
        cmd = ["ffmpeg", "-y", "-v", "error"]
        cmd += (["-itsoffset", f"{s['lag_cam']:.4f}"] if abs(s["lag_cam"]) > 0.005 else []) + ["-i", str(s["camera"])]
        if s["mic"]:
            cmd += (["-itsoffset", f"{s['lag_mic']:.4f}"] if abs(s["lag_mic"]) > 0.005 else []) + ["-i", str(s["mic"])]
        else:
            cmd += ["-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo"]
        cmd += ["-map", "0:v:0", "-map", "1:a:0", "-t", d, "-vf", f"fps={FPS},format=yuv420p",
                "-c:v", "libx264", "-crf", "14", "-preset", "medium", "-g", "30",
                "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2", str(cp).replace(".mp4", ".mov")]
        cp = Path(str(cp).replace(".mp4", ".mov"))
        run(cmd)
        # screen → CFR 30 (duplicates frames from 24 fps), crisp for UI text
        run(["ffmpeg", "-y", "-v", "error", "-i", str(s["display"]), "-t", d, "-vf", f"fps={FPS},format=yuv420p",
             "-c:v", "libx264", "-crf", "12", "-preset", "medium", "-tune", "stillimage", "-g", "30", "-an", str(sp)])
        cam_parts.append(cp)
        scr_parts.append(sp)
    for parts, out in ((cam_parts, src / "cam.mov"), (scr_parts, src / "screen.mp4")):
        if len(parts) == 1:
            parts[0].replace(out)
        else:
            lst = tmp / f"{out.stem}.txt"
            lst.write_text("".join(f"file '{p}'\n" for p in parts))
            run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(out)])
    clicks, moves = cursor_events(segs)
    tl = cfg.get("timeline") or {}
    pd = probe(segs[0]["display"]).get("streams", [{}])[0]
    zooms = []
    for z in tl.get("zoomSegments") or []:
        item = {"start": round(z["start"], 3), "end": round(z["end"], 3), "amount": z.get("amount", 1.5), "mode": z.get("mode", "auto")}
        if isinstance(z.get("mode"), dict) and "manual" in z["mode"]:   # Cap manual zoom: {"manual": {"x":…, "y":…}}
            item.update(mode="manual", x=z["mode"]["manual"].get("x"), y=z["mode"]["manual"].get("y"))
        zooms.append(item)
    data = {"project": str(project), "screen": [pd.get("width"), pd.get("height")],
            "duration": round(sum(s["duration"] for s in segs), 3),
            "clicks": clicks, "moves": moves,
            "trims": [[round(x["start"], 3), round(x["end"], 3)] for x in tl.get("segments") or []],
            "zooms": zooms}
    (src / "cap.json").write_text(json.dumps(data, indent=1))
    for p in tmp.iterdir():
        p.unlink()
    tmp.rmdir()
    print(f"cam    → {src / 'cam.mov'}  ({duration(src / 'cam.mov'):.2f}s)")
    print(f"screen → {src / 'screen.mp4'}  ({duration(src / 'screen.mp4'):.2f}s, {data['screen'][0]}x{data['screen'][1]})")
    print(f"cap    → {src / 'cap.json'}  ({len(clicks)} clicks, {len(moves)} moves, {len(data['trims'])} Cap trims, {len(zooms)} Cap zooms)")


def find() -> None:
    projects = sorted(CAP_DIR.glob("*.cap"), key=lambda p: p.stat().st_mtime, reverse=True)
    for p in projects[:15]:
        try:
            i = info(p)
            print(f"{i['duration']:7.1f}s  cam={'y' if i['camera'] else 'n'} clicks={i['clicks']:3d}  {p}")
        except Exception as e:  # half-written or failed recordings
            print(f"   ?     {p}  ({type(e).__name__})")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["find", "info", "ingest"])
    ap.add_argument("project", nargs="?", type=Path)
    ap.add_argument("--edit-dir", type=Path)
    a = ap.parse_args()
    if a.cmd == "find":
        find()
    elif a.cmd == "info":
        print(json.dumps(info(a.project), indent=1))
    else:
        if not a.edit_dir:
            sys.exit("--edit-dir required")
        ingest(a.project, a.edit_dir.resolve())


if __name__ == "__main__":
    main()
