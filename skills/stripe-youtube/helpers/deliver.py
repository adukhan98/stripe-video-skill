"""The YouTube upload kit: closed captions, chapter timestamps, thumbnail stills.

    python helpers/deliver.py srt      --edit-dir E       # → E/deliver/captions.srt (upload as CC; nothing is burned in)
    python helpers/deliver.py chapters --edit-dir E       # → E/deliver/chapters.txt (paste into the description)
    python helpers/deliver.py stills   --edit-dir E <video> [t …]  # → E/deliver/thumb_*.png (full-res frames for the thumbnail)

Captions come from the CORRECTED transcript (transcripts/<EDL source key>.json, names fixed, cut words deleted), mapped
through timeline.json onto the cut. Sentence case as spoken, ≤ 2 lines × 42 characters, ≤ 6 s per cue, a new cue at
every sentence end or pause ≥ 0.6 s. Chapters come from layout.json "chapters": [{"start": out s, "title": "…"}];
YouTube needs the first at 0:00, at least 3, each at least 10 s long — this checks all three.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

MAX_LINE, MAX_LINES, MAX_DUR, PAUSE = 42, 2, 6.0, 0.6


def ts(t: float) -> str:
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def out_words(edit: Path) -> list[dict]:
    edl = json.loads((edit / "edl.json").read_text())
    tl = json.loads((edit / "timeline.json").read_text())
    cache: dict[str, list] = {}
    words = []
    for seg in tl["segments"]:
        key = seg["source"]
        if key not in cache:
            p = edit / "transcripts" / f"{key}.json"
            if not p.exists():
                sys.exit(f"no corrected transcript {p} (copy the raw one, fix names, delete cut words — SKILL.md step 6)")
            cache[key] = [w for w in json.loads(p.read_text())["words"] if w.get("type", "word") == "word"]
        for w in cache[key]:
            mid = (w["start"] + w["end"]) / 2
            if seg["start"] <= mid < seg["end"]:
                a = seg["out_start"] + max(0.0, w["start"] - seg["start"])
                b = seg["out_start"] + min(seg["out_duration"], w["end"] - seg["start"])
                words.append({"text": w["text"].strip(), "start": a, "end": max(b, a + 0.05)})
    if not edl.get("ranges"):
        sys.exit("empty EDL")
    return sorted(words, key=lambda w: w["start"])


def wrap(text: str) -> list[str]:
    lines, cur = [], ""
    for word in text.split():
        if cur and len(cur) + 1 + len(word) > MAX_LINE:
            lines.append(cur)
            cur = word
        else:
            cur = f"{cur} {word}".strip()
    return lines + ([cur] if cur else [])


def cues(words: list[dict]) -> list[tuple[float, float, str]]:
    out, cur = [], []

    def flush():
        if cur:
            out.append((cur[0]["start"], cur[-1]["end"], " ".join(w["text"] for w in cur)))
            cur.clear()

    for i, w in enumerate(words):
        if cur:
            gap = w["start"] - cur[-1]["end"]
            text = " ".join(x["text"] for x in cur + [w])
            if gap >= PAUSE or w["end"] - cur[0]["start"] > MAX_DUR or len(wrap(text)) > MAX_LINES:
                flush()
        cur.append(w)
        if w["text"][-1:] in ".?!":
            flush()
    flush()
    # no overlaps, no flicker: each cue ends before the next starts, and lasts at least 0.8 s when there is room
    res = []
    for i, (a, b, t) in enumerate(out):
        nxt = out[i + 1][0] if i + 1 < len(out) else b + 2
        res.append((a, min(max(b, a + 0.8), nxt - 0.04), t))
    return res


def srt(edit: Path) -> None:
    cs = cues(out_words(edit))
    d = edit / "deliver"
    d.mkdir(exist_ok=True)
    lines = []
    for i, (a, b, t) in enumerate(cs, 1):
        lines += [str(i), f"{ts(a)} --> {ts(b)}", *wrap(t), ""]
    (d / "captions.srt").write_text("\n".join(lines))
    print(f"→ {d / 'captions.srt'} ({len(cs)} cues)")


def clock(t: float) -> str:
    t = int(t)
    h, r = divmod(t, 3600)
    m, s = divmod(r, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def chapters(edit: Path) -> None:
    layout = json.loads((edit / "layout.json").read_text())
    ch = [{**c, "start": c.get("start", c.get("t", 0.0))} for c in layout.get("chapters") or []]  # "t" or "start"
    ch = sorted(ch, key=lambda c: c["start"])
    total = json.loads((edit / "timeline.json").read_text())["total"]
    problems = []
    if not ch or ch[0]["start"] > 0.5:
        problems.append("the first chapter must start at 0:00")
    if len(ch) < 3:
        problems.append(f"YouTube needs at least 3 chapters ({len(ch)} given)")
    for i, c in enumerate(ch):
        end = ch[i + 1]["start"] if i + 1 < len(ch) else total
        if end - c["start"] < 10:
            problems.append(f"'{c['title']}' is {end - c['start']:.1f}s — chapters must be ≥ 10 s")
    d = edit / "deliver"
    d.mkdir(exist_ok=True)
    text = "\n".join(f"{clock(0 if i == 0 else c['start'])} {c['title']}" for i, c in enumerate(ch))
    (d / "chapters.txt").write_text(text + "\n")
    print(text)
    print(f"→ {d / 'chapters.txt'}")
    for p in problems:
        print("  ! " + p)


def stills(edit: Path, video: Path, times: list[float]) -> None:
    d = edit / "deliver"
    d.mkdir(exist_ok=True)
    for t in times:
        out = d / f"thumb_{t:07.2f}.png"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", str(t), "-i", str(video), "-frames:v", "1", str(out)], check=True)
        print("→", out)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["srt", "chapters", "stills"])
    ap.add_argument("args", nargs="*")
    ap.add_argument("--edit-dir", required=True, type=Path)
    a = ap.parse_intermixed_args()
    edit = a.edit_dir.resolve()
    if a.cmd == "srt":
        srt(edit)
    elif a.cmd == "chapters":
        chapters(edit)
    else:
        stills(edit, Path(a.args[0]), [float(x) for x in a.args[1:]] or [5.0])


if __name__ == "__main__":
    main()
