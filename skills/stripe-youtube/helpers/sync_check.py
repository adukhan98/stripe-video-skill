"""Lip-sync check: does the voice still sit on the picture at every cut?

Why (IMG_2533, 2026-10-17): the cut's per-range AAC clips were concatenated with `-c copy`; each kept ~17 ms of encoder
priming, so the voice slipped later at every join — 0.2 s by 0:40, > 1.5 s by 4:00 — while the picture stayed right.
He caught it, not the self-check. render.py now builds the voice in one sample-accurate pass, but run this on every
base and every final anyway.

  base  — per segment of timeline.json: the base's PICTURE (64x36 grey frames) and VOICE (10 ms envelope) are each matched
          against source/cam.mov at the segment's source time; AV = picture offset − voice offset. Drift shows up as AV
          growing segment by segment.
  final — the final's audio against base.mp4's voice in 8 s windows (music and SFX are on top, so only the lag is read).

    python helpers/sync_check.py --edit-dir E                 # base.mp4 vs source (picture + voice)
    python helpers/sync_check.py --edit-dir E --final final.mp4   # + final audio vs base voice
Exit code 1 when a reliable segment is off by more than --tol (default 0.08 s, ~2.5 frames).
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np

FPS = 30
FW, FH = 64, 36


def audio_env(video: Path, tmp: Path) -> np.ndarray:
    raw = tmp / (video.stem + ".f32")
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", str(video), "-map", "0:a:0", "-ac", "1", "-ar", "8000",
                    "-f", "f32le", str(raw)], check=True)
    x = np.fromfile(raw, np.float32)
    n = len(x) // 80
    return np.abs(x[:n * 80]).reshape(n, 80).mean(1)          # 10 ms envelope


def frames(video: Path, tmp: Path, resample: bool) -> np.ndarray:
    raw = tmp / (video.stem + ".gray")
    vf = (f"fps={FPS}," if resample else "") + f"scale={FW}:{FH},format=gray"
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", str(video), "-vf", vf, "-f", "rawvideo", str(raw)], check=True)
    return np.fromfile(raw, np.uint8).reshape(-1, FW * FH).astype(np.float32)


def best_lag(seg: np.ndarray, ref: np.ndarray, at: int, span: int) -> tuple[int, float]:
    best = (0, -1.0)
    if seg.std() == 0:
        return best
    for lag in range(-span, span + 1):
        j = at + lag
        if j < 0 or j + len(seg) > len(ref):
            continue
        c = float(np.corrcoef(seg, ref[j:j + len(seg)])[0, 1])
        if c > best[1]:
            best = (lag, c)
    return best


def check_base(edit: Path, tmp: Path, tol: float) -> bool:
    segs = json.loads((edit / "timeline.json").read_text())["segments"]
    src, base = edit / "source" / "cam.mov", edit / "base.mp4"
    print("reading frames and audio (the source is decoded once; a 20-min 4K take takes a few minutes)…")
    sa, ba = audio_env(src, tmp), audio_env(base, tmp)
    sv, bv = frames(src, tmp, True), frames(base, tmp, False)
    ok, worst = True, 0.0
    for k, s in enumerate(segs):
        d = s["out_duration"]
        if d < 1.2:
            continue
        o = s["out_start"] + d / 2 - 0.3
        fb, n = int(round(o * FPS)), 18
        fs = int(round((s["start"] + o - s["out_start"]) * FPS))
        errs = [(float(np.mean((sv[fs + L:fs + L + n] - bv[fb:fb + n]) ** 2)), L) for L in range(-45, 46)
                if 0 <= fs + L and fs + L + n <= len(sv) and fb + n <= len(bv)]
        vlag = min(errs)[1] / FPS if errs else 0.0
        ib, w = int(round((s["out_start"] + 0.1) * 100)), int((d - 0.2) * 100)
        lag, r = best_lag(ba[ib:ib + w], sa, int(round((s["start"] + 0.1) * 100)), 150)
        av = vlag - lag / 100
        reliable = r >= 0.6
        flag = reliable and abs(av) > tol
        ok &= not flag
        if reliable:
            worst = max(worst, abs(av))
        if flag or k % 10 == 0:
            print(f"  seg {k:3d} @ {s['out_start']:7.2f}s  picture {vlag:+.3f}s  voice {lag / 100:+.2f}s (r {r:.2f})  AV {av:+.2f}s"
                  + ("  ← OUT OF SYNC" if flag else ""))
    print(f"base: worst reliable AV offset {worst:.3f} s → {'OK' if ok else 'OUT OF SYNC'}")
    return ok


def check_final(edit: Path, final: Path, tmp: Path, tol: float) -> bool:
    va, fa = audio_env(edit / "base.mp4", tmp), audio_env(final, tmp)
    ok, w = True, 800
    for i in range(500, min(len(va), len(fa)) - w - 200, 3000):         # every 30 s
        lag, r = best_lag(va[i:i + w], fa, i, 200)
        flag = r >= 0.5 and abs(lag) / 100 > tol
        ok &= not flag
        print(f"  final @ {i / 100:6.1f}s  lag {lag * 10:+5d} ms (r {r:.2f})" + ("  ← OFF" if flag else ""))
    print(f"final vs base voice → {'OK' if ok else 'OFF'}")
    return ok


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--edit-dir", required=True, type=Path)
    ap.add_argument("--final", type=Path, help="also check this composite's audio against base.mp4's voice")
    ap.add_argument("--skip-base", action="store_true")
    ap.add_argument("--tol", type=float, default=0.08)
    a = ap.parse_args()
    edit = a.edit_dir.resolve()
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        ok = True if a.skip_base else check_base(edit, tmp, a.tol)
        if a.final:
            final = a.final if a.final.is_absolute() else edit / a.final
            ok &= check_final(edit, final, tmp, a.tol)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
