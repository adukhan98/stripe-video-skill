"""Hear every cut by reading it: transcribe the audio across each join of an EDL.

Word-level timestamps (especially local whisper) are loose by 0.1-0.4 s, so a cut that
removes a filler ("So", "basically", "Great.") can clip the next word or leave half of the
filler behind. For every join this concatenates the last ~1.5 s before the cut with the
first ~1.5 s after it (20 ms fades, like render.py) and transcribes just that snippet —
short clips transcribe reliably. Compare each line with the words you meant to keep.

The transcript alone is not enough: ASR "hears" a word whose soft ending was cut ("works" → still read as
"works" on reel-05 while the final "s" was gone). So every join also gets an ENERGY check on the source audio:
  TAIL  sound continues within 0.25 s after a range end (> floor + 12 dB) and that audio is dropped
        → a soft ending (s, t, k, breathy vowel) is clipped; the line suggests where the energy dies
  HEAD  sound within 0.12 s before a range start → a word onset may be clipped
Read both flags; extend the range end / pull the start earlier and re-probe until both are quiet.

Usage:
    python helpers/verify_cuts.py <edit>/edl.json                  # every join
    python helpers/verify_cuts.py --source clip.MOV --probe 22.3:23.04,23.44:24.6
        # try candidate cut points before writing them into the EDL (repeat --probe)
"""

from __future__ import annotations

import argparse
import array
import json
import math
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from transcribe import find_model, model_download_command  # noqa: E402

CTX = 1.5
BIN = 0.05
SR_E = 16000
TAIL_DB = 12   # soft endings (the "s" of "works") sit only ~12–15 dB over the floor
HEAD_DB = 18


def energy_bins(source: str, audio_track: int = 0) -> tuple[list[float], float]:
    """50 ms RMS bins (dBFS) of the whole source + its noise floor (2nd percentile)."""
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", source, "-map", f"0:a:{audio_track}", "-ac", "1",
                          "-ar", str(SR_E), "-f", "s16le", "-"], capture_output=True, check=True).stdout
    x = array.array("h", raw)
    step = int(SR_E * BIN)
    db = []
    for i in range(0, len(x) - step, step):
        seg = x[i:i + step]
        rms = math.sqrt(sum(v * v for v in seg) / step) / 32768
        db.append(20 * math.log10(max(rms, 1e-6)))
    floor = sorted(db)[len(db) // 50] if db else -60   # 2nd percentile: dense takes leave few true silences
    return db, floor


def edge_flags(db: list[float], floor: float, end: float, next_start: float, start: float) -> str:
    def at(t: float) -> float:
        i = int(t / BIN)
        return db[i] if 0 <= i < len(db) else floor
    out = []
    dropped = min(0.3, max(0.0, next_start - end - 0.08))   # stop short of the next range: its onset is not a tail
    i0 = math.ceil(end / BIN - 1e-6)                       # first whole bin after the cut (skip the decaying one)
    tail = [(i * BIN - end, db[i]) for i in range(i0, int((end + dropped) / BIN) + 1) if 0 <= i < len(db)]
    if tail:
        vals = [v for _, v in tail]
        lo = min(vals[0], floor + 6)
        rerise, sustained = None, 0
        for k, (dt, v) in enumerate(tail):
            if k and v > floor + TAIL_DB and v - min(vals[:k]) >= 6:
                rerise = (dt, v)                            # a NEW sound after a dip: a cut-off sibilant/plosive
            sustained = sustained + 1 if v > floor + TAIL_DB + 6 else 0
            if sustained >= 3 and rerise is None:
                rerise = (dt, v)                            # or the word simply keeps going
        if rerise:
            dies = next((dt for dt, v in tail if dt > rerise[0] and v < floor + 8), rerise[0] + BIN)
            out.append(f"TAIL {rerise[1]:.0f} dB at +{rerise[0]:.2f}s (floor {floor:.0f}) → try end ≈ {end + dies:.2f}")
    head = [at(start - k * BIN) for k in (1, 2)]
    if max(head) > floor + HEAD_DB:
        out.append(f"HEAD {max(head):.0f} dB just before the start → onset may be clipped")
    return ("   ⚠ " + " | ".join(out)) if out else ""


def join_text(source: str, pieces: list[tuple[float, float]], model: Path, audio_track: int = 0) -> str:
    with tempfile.TemporaryDirectory() as tmp:
        wav = Path(tmp) / "j.wav"
        parts, labels = [], []
        for i, (a, b) in enumerate(pieces):
            d = max(0.05, b - a)
            parts.append(f"[0:a:{audio_track}]atrim={a}:{b},asetpts=PTS-STARTPTS,"
                         f"afade=t=in:d=0.02,afade=t=out:st={max(0, d - 0.02):.3f}:d=0.02[a{i}]")
            labels.append(f"[a{i}]")
        fc = ";".join(parts) + ";" + "".join(labels) + f"concat=n={len(pieces)}:v=0:a=1,apad=pad_dur=0.4[o]"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", source, "-filter_complex", fc, "-map", "[o]",
                        "-ac", "1", "-ar", "16000", str(wav)], check=True)
        r = subprocess.run(["whisper-cli", "-m", str(model), "-f", str(wav), "-np", "-nt"],
                           capture_output=True, text=True)
    return " ".join(r.stdout.split())


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("edl", type=Path, nargs="?")
    ap.add_argument("--source", help="source video for --probe")
    ap.add_argument("--probe", action="append", default=[],
                    help="a1:b1,a2:b2[,...] — pieces to join and transcribe (source seconds)")
    ap.add_argument("--context", type=float, default=CTX)
    ap.add_argument("--model", default="medium.en")
    ap.add_argument("--audio-track", type=int, default=0)
    args = ap.parse_args()

    model = find_model(args.model)
    if not model:
        sys.exit(f"whisper model {args.model} not found. {model_download_command(args.model)}")

    if args.probe:
        if not args.source:
            ap.error("--probe needs --source")
        for p in args.probe:
            pieces = [tuple(float(x) for x in seg.split(":")) for seg in p.split(",")]
            print(f"{p:>28}  ->  {join_text(args.source, pieces, model, args.audio_track)}")
        return

    if not args.edl:
        ap.error("edl or --probe required")
    edl = json.loads(args.edl.read_text())
    rs = edl["ranges"]
    track = int(edl.get("audio_track", args.audio_track))
    energy: dict[str, tuple[list[float], float]] = {}
    for i in range(len(rs) - 1):
        a, b = rs[i], rs[i + 1]
        if a["source"] != b["source"]:
            continue
        src = edl["sources"][a["source"]]
        pieces = [(max(float(a["start"]), float(a["end"]) - args.context), float(a["end"])),
                  (float(b["start"]), min(float(b["end"]), float(b["start"]) + args.context))]
        if src not in energy:
            energy[src] = energy_bins(src, track)
        db, floor = energy[src]
        flags = edge_flags(db, floor, float(a["end"]), float(b["start"]), float(b["start"]))
        print(f"[{i:2d}|{i + 1:2d}] {float(a['end']):8.2f} -> {float(b['start']):8.2f}  "
              f"{join_text(src, pieces, model, track)}{flags}")


if __name__ == "__main__":
    main()
