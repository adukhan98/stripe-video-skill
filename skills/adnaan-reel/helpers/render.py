"""Render a video from an EDL.

Pipeline, in the order that keeps every hard rule:

  1. Per-segment extract (picture only): HDR→SDR tone map → mirror → fit to the
     output canvas (crop / pad / scale) → grade. timeline.json records the measured
     output offset of every segment (captions, slots and compose.py use it).
  2. base.mp4 = lossless -c copy concat of the picture + the voice cut ONCE from the
     sources: each source's audio is decoded to PCM, every segment is taken at sample
     positions from timeline.json (at out_start, exactly out_duration, 30 ms fades;
     silence for sources without audio) and the track is encoded once.
     Sync fix (2026-10-17): the voice used to be cut as one AAC clip per segment and
     joined with the -c copy concat, which kept every clip's ~1024-sample encoder
     priming/padding, so the voice slipped ~15-20 ms later at each join (+1.5 s by
     4:00 on a 122-range edit) while the picture stayed put. Now every segment's
     voice stays within a millisecond of its source, however many joins there are.
  3. One composite filter graph:
       end hold → punch-in zooms → split layouts → overlays (alpha, PTS-shifted
       to their window) → captions LAST
     composited in RGB and converted to BT.709 once, so brand colours in
     captions and graphics land on their exact hex values; and the audio mix:
     dialogue + music beds ducked under speech + one-shot SFX.
  4. Loudness: two-pass loudnorm (-14 LUFS), brick-wall limiter, AAC 320k — keeps
     the true peak under -1 dBTP after encoding — then a measured report.

Usage:
    python helpers/render.py <edl.json> -o final.mp4 --captions
    python helpers/render.py <edl.json> -o preview.mp4 --preview --captions
    python helpers/render.py <edl.json> -o base.mp4 --base-only          # cut only; build graphics against it
    python helpers/render.py <edl.json> -o final.mp4 --captions --reuse-base
    python helpers/render.py <edl.json> -o final.mp4 --build-subtitles   # legacy: uppercase SRT captions
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

try:
    from grade import get_preset, auto_grade_for_clip  # same directory
except Exception:
    def get_preset(name: str) -> str:
        return ""

    def auto_grade_for_clip(video, start=0.0, duration=None, verbose=False):  # type: ignore
        return "eq=contrast=1.03:saturation=0.98", {}

from captions import (  # noqa: E402
    CHUNK_MAX_WORDS, CHUNK_MIN_S, CHUNK_PAUSE_S, CHUNK_WORDS, PUNCT_BREAK,
    ass_filter, build_captions, chunk_words, ff_quote, load_brand_captions,
)
from platforms import get_platform, platform_for_canvas, scaled  # noqa: E402


# -------- Legacy SRT subtitle style (bold-overlay) ---------------------------
#
# Used only for .srt subtitles. Branded captions are ASS files from captions.py.
# MarginV is a platform safe-zone rule, not taste: libass scales the canvas to
# PlayResY=288, so MarginV=90 puts the baseline ~30% up from the bottom — clear of
# the Reels / TikTok / Shorts UI.
SUB_FORCE_STYLE = (
    "FontName=Helvetica,FontSize=18,Bold=1,"
    "PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BackColour=&H00000000,"
    "BorderStyle=1,Outline=2,Shadow=0,"
    "Alignment=2,MarginV=90"
)

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}

# -------- Helpers ------------------------------------------------------------


def run(cmd: list[str], quiet: bool = False) -> None:
    if not quiet:
        print(f"  $ {' '.join(str(c) for c in cmd[:6])}{' …' if len(cmd) > 6 else ''}")
    subprocess.run(cmd, check=True)


def run_ffmpeg(cmd: list[str], what: str) -> None:
    proc = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
    if proc.returncode != 0:
        tail = "\n".join(proc.stderr.strip().splitlines()[-15:])
        sys.exit(f"ffmpeg failed during {what}:\n{tail}")


def resolve_grade_filter(grade_field: str | None) -> str:
    """The EDL's 'grade' field can be a preset name, a raw ffmpeg filter, or 'auto'.

    Returns the filter string to embed into the per-segment -vf chain.
    For 'auto', returns the sentinel "__AUTO__" which is resolved per-segment.
    """
    if not grade_field:
        return ""
    if grade_field == "auto":
        return "__AUTO__"
    # Preset names are short identifiers, filter strings contain '=' or ','.
    if re.fullmatch(r"[a-zA-Z0-9_\-]+", grade_field):
        try:
            return get_preset(grade_field)
        except KeyError:
            print(f"warning: unknown preset '{grade_field}', using as raw filter")
            return grade_field
    return grade_field


def resolve_path(maybe_path: str, base: Path) -> Path:
    """Resolve a path that may be absolute or relative to `base`."""
    p = Path(maybe_path).expanduser()
    if p.is_absolute():
        return p
    return (base / p).resolve()


def resolve_subtitles_path(maybe_path: str, edit_dir: Path) -> Path:
    """Resolve the EDL's subtitles path: relative to the EDL's directory, else the
    current directory (agents often write "edit/master.srt"). A missing file is an
    error: rendering on without it silently ships a video with no captions."""
    candidates = [resolve_path(maybe_path, edit_dir)]
    if not Path(maybe_path).is_absolute():
        candidates.append(Path(maybe_path).resolve())
    for c in candidates:
        if c.exists():
            return c
    tried = ", ".join(str(c) for c in candidates)
    sys.exit(f"subtitles file in EDL not found (tried {tried}). Fix the path or pass --no-subtitles.")


def hex_to_ff(color: str) -> str:
    return "0x" + color.strip().lstrip("#")[:6].upper()


# -------- HDR → SDR tone mapping (HLG / PQ sources) --------------------------
#
# iPhone defaults to HLG HDR in Rec.2020 (and many mirrorless cameras ship PQ).
# Downconverting bit depth without tone-mapping leaves HLG/PQ transfer metadata on
# 8-bit video; players that honour it show it blown out. Detect HDR via
# color_transfer and tone-map to clean Rec.709 SDR.

HDR_TRANSFERS = {"smpte2084", "arib-std-b67"}  # PQ (HDR10) and HLG

TONEMAP_CHAIN = (
    "zscale=t=linear:npl=100,"
    "format=gbrpf32le,"
    "zscale=p=bt709,"
    "tonemap=tonemap=hable:desat=0,"
    "zscale=t=bt709:m=bt709:r=tv,"
    "format=yuv420p"
)

BT709_TAGS = ["-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv"]


def is_hdr_source(video: Path) -> bool:
    """Return True if the source uses a PQ or HLG transfer function."""
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v:0",
             "-show_entries", "stream=color_transfer",
             "-of", "default=noprint_wrappers=1:nokey=1", str(video)],
            capture_output=True, text=True, check=True,
        )
        return out.stdout.strip() in HDR_TRANSFERS
    except subprocess.CalledProcessError:
        return False


def is_portrait_source(video: Path) -> bool:
    """Return True if the displayed video is portrait, including rotation."""
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v:0",
             "-show_entries",
             "stream=width,height:stream_side_data=rotation",
             "-of", "json", str(video)],
            capture_output=True, text=True, check=True,
        )
        streams = json.loads(out.stdout).get("streams") or []
        if not streams:
            return False
        stream = streams[0]
        w, h = int(stream["width"]), int(stream["height"])

        # ffmpeg autorotates display-matrix side data before applying filters.
        # Swap coded dimensions for quarter-turns so the scale axis is selected
        # from the dimensions the filter actually sees. A plain metadata tag is
        # intentionally ignored because it does not guarantee autorotation.
        rotation = 0
        for side_data in stream.get("side_data_list") or []:
            if side_data.get("rotation") is not None:
                rotation = side_data["rotation"]
                break
        if int(round(float(rotation))) % 360 in (90, 270):
            w, h = h, w
        return h > w
    except (
        subprocess.CalledProcessError,
        json.JSONDecodeError,
        OSError,
        OverflowError,
        KeyError,
        TypeError,
        ValueError,
    ):
        return False


def has_audio_stream(video: Path) -> bool:
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "a",
             "-show_entries", "stream=index", "-of", "csv=p=0", str(video)],
            capture_output=True, text=True, check=True,
        )
        return bool(out.stdout.strip())
    except (subprocess.CalledProcessError, OSError):
        return False


def probe_duration(path: Path) -> float | None:
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
            capture_output=True, text=True, check=True,
        )
        return float(out.stdout.strip())
    except (subprocess.CalledProcessError, ValueError, OSError):
        return None


def probe_dims(path: Path) -> tuple[int, int] | None:
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v:0",
             "-show_entries", "stream=width,height", "-of", "csv=p=0:s=x", str(path)],
            capture_output=True, text=True, check=True,
        )
        w, h = out.stdout.strip().split("x")[:2]
        return int(w), int(h)
    except (subprocess.CalledProcessError, ValueError, OSError):
        return None


def parse_fps(value: str) -> str:
    """Validate and canonicalize an ffmpeg frame rate."""
    text = value.strip()
    if len(text) > 32 or not re.fullmatch(
        r"(?:[0-9]+(?:\.[0-9]+)?|[0-9]+/[0-9]+)", text
    ):
        raise argparse.ArgumentTypeError(
            "FPS must be a positive number or rational, e.g. 30 or 30000/1001"
        )
    try:
        rate = Fraction(text)
    except (ValueError, ZeroDivisionError) as exc:
        raise argparse.ArgumentTypeError(
            "FPS must be a positive number or rational, e.g. 30 or 30000/1001"
        ) from exc
    if rate <= 0:
        raise argparse.ArgumentTypeError("FPS must be greater than zero")
    # FFmpeg stores video rates as AVRational (signed 32-bit components).
    # Bounding the reduced fraction keeps every accepted canonical value safe
    # for ffmpeg and makes parse_fps(parse_fps(value)) idempotent.
    max_component = 2_147_483_647
    if rate.numerator > max_component or rate.denominator > max_component:
        raise argparse.ArgumentTypeError("FPS precision or magnitude is too large")
    return f"{rate.numerator}/{rate.denominator}"


def probe_source_fps(video: Path) -> str | None:
    """Return an ffmpeg-ready source rate, preferring the average frame rate.

    ``avg_frame_rate`` represents the observed average and is the better default
    for variable-frame-rate inputs. ``r_frame_rate`` remains a fallback for
    streams where the average is unavailable. Values are normalized to an exact
    rational so rates such as ``30000/1001`` survive without rounding.
    """
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v:0",
             "-show_entries", "stream=avg_frame_rate,r_frame_rate",
             "-of", "json", str(video)],
            capture_output=True, text=True, check=True,
        )
        streams = json.loads(out.stdout).get("streams") or []
        if not streams:
            return None
        for field in ("avg_frame_rate", "r_frame_rate"):
            value = streams[0].get(field)
            if value and value != "0/0":
                try:
                    return parse_fps(value)
                except argparse.ArgumentTypeError:
                    continue
    except (subprocess.CalledProcessError, json.JSONDecodeError, OSError):
        return None
    return None


# -------- Output canvas -------------------------------------------------------


def output_canvas(edl: dict, draft: bool = False) -> tuple[int, int] | None:
    """Explicit output size from the EDL (draft renders at 2/3 size), or None for the
    default: the source scaled to 1920 on its long edge."""
    out = edl.get("output") or {}
    if not (out.get("width") and out.get("height")):
        return None
    w, h = int(out["width"]), int(out["height"])
    if draft:
        w, h = int(round(w * 2 / 3 / 2) * 2), int(round(h * 2 / 3 / 2) * 2)
    return w, h


def fit_filter(canvas: tuple[int, int], fit: str, focus_x: float, focus_y: float, pad_color: str) -> str:
    """Scale the source onto the canvas. crop: fill and trim (focus 0 = keep the
    left/top edge, 0.5 = centre, 1 = keep the right/bottom edge). pad: fit inside
    and letterbox with pad_color. scale: stretch."""
    w, h = canvas
    if fit == "pad":
        return (f"scale={w}:{h}:force_original_aspect_ratio=decrease:flags=lanczos,"
                f"pad={w}:{h}:(ow-iw)/2:(oh-ih)/2:color={hex_to_ff(pad_color)},setsar=1")
    if fit == "scale":
        return f"scale={w}:{h}:flags=lanczos,setsar=1"
    fx = min(1.0, max(0.0, focus_x))
    fy = min(1.0, max(0.0, focus_y))
    return (f"scale={w}:{h}:force_original_aspect_ratio=increase:flags=lanczos,"
            f"crop={w}:{h}:(iw-{w})*{fx:.4f}:(ih-{h})*{fy:.4f},setsar=1")


# -------- Per-segment extraction (Rule 2 + Rule 3) --------------------------


def extract_segment(
    source: Path,
    seg_start: float,
    duration: float,
    grade_filter: str,
    out_path: Path,
    preview: bool = False,
    draft: bool = False,
    rate: str | None = None,
    canvas: tuple[int, int] | None = None,
    fit: str = "crop",
    focus: tuple[float, float] = (0.5, 0.5),
    pad_color: str = "#000000",
    mirror: bool = False,
) -> None:
    """Extract a cut range's picture as its own MP4 (graded, no audio).

    `-ss` before `-i` for fast accurate seeking. Without an explicit canvas the
    source is scaled to 1920 on its long edge (portrait keeps its orientation).
    The dialogue is not cut here: build_voice_track cuts it from the source in
    one sample-accurate pass (per-segment AAC drifts at every join).

    Quality ladder:
      - final (default): libx264 fast CRF 20
      - preview:         libx264 medium CRF 22 (evaluable for QC)
      - draft:           2/3 size, libx264 ultrafast CRF 28 (cut-point check only)
    """
    out_path.parent.mkdir(parents=True, exist_ok=True)

    vf_parts: list[str] = []
    if is_hdr_source(source):
        vf_parts.append(TONEMAP_CHAIN)
    if mirror:
        vf_parts.append("hflip")
    if canvas:
        vf_parts.append(fit_filter(canvas, fit, focus[0], focus[1], pad_color))
    else:
        portrait = is_portrait_source(source)
        if draft:
            vf_parts.append("scale=-2:1280" if portrait else "scale=1280:-2")
        else:
            vf_parts.append("scale=-2:1920" if portrait else "scale=1920:-2")
    if grade_filter:
        vf_parts.append(grade_filter)
    vf = ",".join(vf_parts)

    if draft:
        preset, crf = "ultrafast", "28"
    elif preview:
        preset, crf = "medium", "22"
    else:
        preset, crf = "fast", "20"

    # Frame rate: use the rate the caller resolved once for the whole render
    # (every segment must share it — concat -c copy in Rule 2 requires a uniform
    # frame rate). When called standalone with no rate, preserve this source's
    # own rate; fall back to 24 only if it can't be probed.
    out_rate = rate if rate is not None else (probe_source_fps(source) or "24")

    cmd = [
        "ffmpeg", "-y", "-ss", f"{seg_start:.3f}", "-i", str(source),
        "-t", f"{duration:.3f}",
        "-map", "0:v:0", "-an",
        "-vf", vf,
        "-c:v", "libx264", "-preset", preset, "-crf", crf,
        "-pix_fmt", "yuv420p", "-r", out_rate, *BT709_TAGS,
        "-movflags", "+faststart",
        str(out_path),
    ]
    run_ffmpeg(cmd, f"extract {source.name} {seg_start:.2f}+{duration:.2f}s")


def extract_all_segments(
    edl: dict,
    edit_dir: Path,
    preview: bool,
    draft: bool = False,
    fps: str | None = None,
) -> list[Path]:
    """Extract every EDL range into edit_dir/clips_graded/seg_NN.mp4.
    Returns the ordered list of segment paths.

    If the EDL `grade` is "auto", analyze each segment range with
    `auto_grade_for_clip` and apply a per-segment subtle correction.
    Otherwise, apply the same preset/raw filter to every segment. A range may
    override it with its own "grade" (e.g. "none" for a graphics insert).
    """
    resolved = resolve_grade_filter(edl.get("grade"))
    clips_dir = edit_dir / (
        "clips_draft" if draft else ("clips_preview" if preview else "clips_graded")
    )
    clips_dir.mkdir(parents=True, exist_ok=True)

    ranges = edl["ranges"]
    sources = edl["sources"]
    out_cfg = edl.get("output") or {}
    canvas = output_canvas(edl, draft=draft)

    # Resolve ONE output frame rate for the entire render and apply it to every
    # segment. The lossless concat (Rule 2, `-c copy`) requires all segments to
    # share a frame rate; probing per-segment would diverge for multi-source
    # EDLs that mix rates (e.g. a 30fps and a 60fps source) and break the concat.
    # Explicit --fps wins, then the EDL's output.fps; otherwise the first source's rate.
    if fps is not None:
        out_rate = parse_fps(str(fps))
    elif out_cfg.get("fps"):
        out_rate = parse_fps(str(out_cfg["fps"]))
    elif ranges:
        first_src = resolve_path(sources[ranges[0]["source"]], edit_dir)
        out_rate = probe_source_fps(first_src) or "24"
    else:
        out_rate = "24"

    seg_paths: list[Path] = []
    print(f"extracting {len(ranges)} segment(s) → {clips_dir.name}/  @ {out_rate} fps"
          f"{' (forced)' if fps is not None else ''}"
          + (f"  canvas {canvas[0]}x{canvas[1]} ({out_cfg.get('fit', 'crop')})" if canvas else ""))
    for i, r in enumerate(ranges):
        src_name = r["source"]
        src_path = resolve_path(sources[src_name], edit_dir)
        start = float(r["start"])
        end = float(r["end"])
        duration = end - start
        out_path = clips_dir / f"seg_{i:02d}_{src_name}.mp4"

        grade = resolve_grade_filter(r["grade"]) if "grade" in r else resolved
        if grade == "__AUTO__":
            seg_filter, _stats = auto_grade_for_clip(src_path, start=start, duration=duration, verbose=False)
        else:
            seg_filter = grade

        note = r.get("beat") or r.get("note") or ""
        print(f"  [{i:02d}] {src_name}  {start:7.2f}-{end:7.2f}  ({duration:5.2f}s)  {note}")
        if grade == "__AUTO__":
            print(f"        grade: {seg_filter or '(none)'}")
        extract_segment(
            src_path, start, duration, seg_filter, out_path,
            preview=preview, draft=draft, rate=out_rate,
            canvas=canvas,
            fit=r.get("fit", out_cfg.get("fit", "crop")),
            focus=(float(r.get("focus_x", out_cfg.get("focus_x", 0.5))),
                   float(r.get("focus_y", out_cfg.get("focus_y", 0.5)))),
            pad_color=r.get("pad_color", out_cfg.get("pad_color", "#000000")),
            mirror=bool(r.get("mirror", edl.get("mirror", False))),
        )
        seg_paths.append(out_path)

    write_timeline(edl, edit_dir, seg_paths, out_rate)
    return seg_paths


def base_key(edl: dict, mode: str) -> str:
    """Fingerprint of everything that shapes base.mp4 (for --reuse-base)."""
    keys = ("sources", "ranges", "grade", "output", "mirror", "audio_track")
    blob = json.dumps({k: edl.get(k) for k in keys} | {"mode": mode}, sort_keys=True)
    return hashlib.sha1(blob.encode()).hexdigest()[:16]


def write_timeline(edl: dict, edit_dir: Path, seg_paths: list[Path], rate: str) -> Path:
    """Measured output offset of every segment (each is rounded to whole frames)."""
    segs, t = [], 0.0
    for r, p in zip(edl["ranges"], seg_paths):
        nominal = float(r["end"]) - float(r["start"])
        measured = probe_duration(p) if p.exists() else None
        dur = measured if measured else nominal
        segs.append({"source": r["source"], "start": float(r["start"]), "end": float(r["end"]),
                     "out_start": round(t, 4), "out_duration": round(dur, 4), "file": str(p)})
        t += dur
    out = edit_dir / "timeline.json"
    out.write_text(json.dumps({"fps": rate, "total": round(t, 4), "segments": segs}, indent=2))
    return out


# -------- Lossless concat + sample-accurate voice ---------------------------
#
# The picture is joined with a lossless -c copy concat. The dialogue is NOT: every
# AAC clip carries ~1024 samples of encoder priming plus end padding, and a -c copy
# concat keeps them, so the voice slipped ~15-20 ms later at every join (+1.5 s by
# 4:00 on a 122-range edit). Instead each source's audio is decoded once to PCM, every
# segment is cut at sample positions from timeline.json (placed at out_start, exactly
# out_duration long, 30 ms fades), and the whole track is encoded once.

VOICE_SR = 48000
VOICE_FADE_S = 0.03                               # Rule 3: no pops at the joins
_F32 = 4                                          # bytes per float32 sample


def _probe_start(path: Path, select: str) -> float:
    """start_time of the format (select="") or of one stream (e.g. "a:0"), 0 if unknown."""
    entries = "format=start_time" if not select else "stream=start_time"
    cmd = ["ffprobe", "-v", "error", "-show_entries", entries,
           "-of", "default=noprint_wrappers=1:nokey=1"]
    if select:
        cmd += ["-select_streams", select]
    try:
        out = subprocess.run([*cmd, str(path)], capture_output=True, text=True, check=True)
        return float(out.stdout.split()[0])
    except (subprocess.CalledProcessError, OSError, ValueError, IndexError):
        return 0.0


def build_voice_track(edl: dict, edit_dir: Path, timeline: dict, out_raw: Path) -> int:
    """Write the cut's dialogue as raw f32le stereo 48 kHz into out_raw; return its sample count.

    Segment i covers output samples [round(out_start*SR), round((out_start+out_duration)*SR)),
    so the track is exactly as long as the picture and can never drift. Its samples come from
    source time `start` onward, mapped the way `-ss` maps the picture (relative to the file's
    start_time, corrected for the audio stream's own start_time). Sources without audio, and
    any part of a range past the end of a source's audio, are silence."""
    from array import array

    sources, ranges = edl["sources"], edl["ranges"]
    segs = timeline["segments"]
    tmp = out_raw.parent
    decoded: dict[tuple[str, int], tuple[Path, int, float] | None] = {}

    def source_pcm(name: str, track: int):
        key = (name, track)
        if key not in decoded:
            src = resolve_path(sources[name], edit_dir)
            if not has_audio_stream(src):
                decoded[key] = None
            else:
                raw = tmp / f"_src_{len(decoded)}.f32"
                run_ffmpeg(["ffmpeg", "-nostdin", "-y", "-v", "error", "-i", str(src),
                            "-map", f"0:a:{track}", "-ac", "2", "-ar", str(VOICE_SR),
                            "-f", "f32le", str(raw)], f"decode audio of {src.name}")
                shift = _probe_start(src, "") - _probe_start(src, f"a:{track}")
                decoded[key] = (raw, raw.stat().st_size // (2 * _F32), shift)
        return decoded[key]

    fade_full = int(round(VOICE_FADE_S * VOICE_SR))
    cursor = 0
    with open(out_raw, "wb") as out:
        for r, seg in zip(ranges, segs):
            o = int(round(float(seg["out_start"]) * VOICE_SR))
            e = int(round((float(seg["out_start"]) + float(seg["out_duration"])) * VOICE_SR))
            if o > cursor:                        # never expected (timeline is contiguous)
                out.write(bytes((o - cursor) * 2 * _F32))
                cursor = o
            o = cursor
            n = max(0, e - o)
            buf = array("f", bytes(n * 2 * _F32))
            pcm = source_pcm(r["source"], int(r.get("audio_track", edl.get("audio_track", 0))))
            if pcm is not None and n:
                raw, total, shift = pcm
                a = int(round((float(seg["start"]) + shift) * VOICE_SR))
                lo, hi = max(a, 0), min(a + n, total)
                if hi > lo:
                    with open(raw, "rb") as f:
                        f.seek(lo * 2 * _F32)
                        chunk = array("f")
                        chunk.frombytes(f.read((hi - lo) * 2 * _F32))
                    buf[(lo - a) * 2:(hi - a) * 2] = chunk
                fade = min(fade_full, n // 2)
                for k in range(fade):
                    g = k / fade
                    i0, i1 = 2 * k, 2 * (n - 1 - k)
                    buf[i0] *= g
                    buf[i0 + 1] *= g
                    buf[i1] *= g
                    buf[i1 + 1] *= g
            buf.tofile(out)
            cursor += n
    return cursor


def concat_segments(segment_paths: list[Path], out_path: Path, edit_dir: Path,
                    edl: dict | None = None) -> None:
    """Lossless -c copy concat of the segments' picture, muxed with the sample-accurate voice
    (build_voice_track, from edit_dir/timeline.json) encoded once. Without an EDL the base
    is picture-only."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    work = edit_dir / "_work"
    work.mkdir(parents=True, exist_ok=True)
    concat_list = work / "_concat.txt"
    concat_list.write_text("".join(
        "file '" + str(p.resolve()).replace("'", "'\\''") + "'\n" for p in segment_paths
    ))
    video = work / "_concat_video.mp4"
    print(f"concat → {out_path.name}")
    run_ffmpeg(["ffmpeg", "-nostdin", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_list),
                "-map", "0:v:0", "-c", "copy", str(video)], "concat")
    concat_list.unlink(missing_ok=True)
    if edl is None:
        video.replace(out_path)
        return
    timeline = json.loads((edit_dir / "timeline.json").read_text())
    voice = work / "_voice.f32"
    samples = build_voice_track(edl, edit_dir, timeline, voice)
    print(f"  voice: {len(timeline['segments'])} segment(s) cut from source, {samples / VOICE_SR:.3f}s")
    # The concat starts the picture at the encoder's B-frame delay (one frame), not 0;
    # -itsoffset starts the voice there too, so out_start lines up with the picture.
    v0 = _probe_start(video, "v:0")
    run_ffmpeg(["ffmpeg", "-nostdin", "-y", "-i", str(video),
                "-itsoffset", f"{v0:.6f}", "-f", "f32le", "-ar", str(VOICE_SR), "-ac", "2", "-i", str(voice),
                "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy",
                "-c:a", "aac", "-b:a", "320k", "-ar", str(VOICE_SR),
                "-movflags", "+faststart", str(out_path)], "mux voice")
    for f in (video, voice, *work.glob("_src_*.f32")):
        f.unlink(missing_ok=True)


# -------- Legacy master SRT (Rule 5) ------------------------------------------


def _srt_timestamp(seconds: float) -> str:
    total_ms = int(round(seconds * 1000))
    h, rem = divmod(total_ms, 3600_000)
    m, rem = divmod(rem, 60_000)
    s, ms = divmod(rem, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def _words_in_range(transcript: dict, t_start: float, t_end: float) -> list[dict]:
    out: list[dict] = []
    for w in transcript.get("words", []):
        if w.get("type") != "word":
            continue
        ws = w.get("start")
        we = w.get("end")
        if ws is None or we is None:
            continue
        if we <= t_start or ws >= t_end:
            continue
        out.append(w)
    return out


def build_master_srt(edl: dict, edit_dir: Path, out_path: Path) -> None:
    """Build an output-timeline SRT from per-source transcripts (legacy style).

    - phrase-aware ~2-word chunks (see chunk_words)
    - UPPERCASE text
    - Output times computed as word.start - segment_start + segment_offset
    """
    transcripts_dir = edit_dir / "transcripts"

    entries: list[tuple[float, float, str]] = []
    seg_offset = 0.0

    for r in edl["ranges"]:
        src_name = r["source"]
        seg_start = float(r["start"])
        seg_end = float(r["end"])
        seg_duration = seg_end - seg_start

        tr_path = transcripts_dir / f"{src_name}.json"
        if not tr_path.exists():
            print(f"  no transcript for {src_name}, skipping captions for this segment")
            seg_offset += seg_duration
            continue

        transcript = json.loads(tr_path.read_text())
        words_in_seg = _words_in_range(transcript, seg_start, seg_end)

        for chunk in chunk_words(words_in_seg):
            local_start = max(seg_start, chunk[0].get("start", seg_start))
            local_end = min(seg_end, chunk[-1].get("end", seg_end))
            out_start = max(0.0, local_start - seg_start) + seg_offset
            out_end = max(0.0, local_end - seg_start) + seg_offset
            if out_end <= out_start:
                out_end = out_start + 0.4
            text = " ".join((w.get("text") or "").strip() for w in chunk)
            text = re.sub(r"\s+", " ", text).strip()
            # Strip trailing punctuation for cleaner uppercase look
            text = text.rstrip(",;:")
            text = text.upper()
            entries.append((out_start, out_end, text))

        seg_offset += seg_duration

    entries.sort(key=lambda e: e[0])
    lines: list[str] = []
    for i, (a, b, t) in enumerate(entries, start=1):
        lines.append(str(i))
        lines.append(f"{_srt_timestamp(a)} --> {_srt_timestamp(b)}")
        lines.append(t)
        lines.append("")
    out_path.write_text("\n".join(lines))
    print(f"master SRT → {out_path.name} ({len(entries)} cues)")


# -------- Loudness normalization (social-ready audio) -----------------------


# Social-media standard: -14 LUFS integrated, -1 dBTP peak, LRA 11 LU.
LOUDNORM_I = -14.0
LOUDNORM_TP = -1.0
LOUDNORM_LRA = 11.0
# AAC re-encoding overshoots loudnorm's true-peak target; a sample-peak brick wall
# at -2 dBFS leaves room for it (measured on a shipped reel: -1.3 to -1.6 dBTP).
LIMITER = "alimiter=limit=0.79:attack=1:release=50:level=disabled"
AAC_FINAL = ["-c:a", "aac", "-b:a", "320k", "-aac_coder", "twoloop", "-ar", "48000"]


def measure_loudness(video_path: Path) -> dict[str, str] | None:
    """Run ffmpeg loudnorm first pass and parse the JSON measurement."""
    filter_str = (
        f"loudnorm=I={LOUDNORM_I}:TP={LOUDNORM_TP}:LRA={LOUDNORM_LRA}:print_format=json"
    )
    cmd = [
        "ffmpeg", "-y", "-hide_banner", "-nostats",
        "-i", str(video_path),
        "-af", filter_str,
        "-vn", "-f", "null", "-",
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    stderr = proc.stderr
    start = stderr.rfind("{")
    end = stderr.rfind("}")
    if start == -1 or end == -1 or end <= start:
        return None
    try:
        data = json.loads(stderr[start: end + 1])
    except json.JSONDecodeError:
        return None
    needed = {"input_i", "input_tp", "input_lra", "input_thresh", "target_offset"}
    if not needed.issubset(data.keys()):
        return None
    return data


def apply_loudnorm_two_pass(
    input_path: Path,
    output_path: Path,
    preview: bool = False,
) -> bool:
    """Loudness-normalize input_path into output_path (video stream copied).

    Final: measured two-pass loudnorm → limiter → AAC 320k twoloop.
    Preview/draft: one-pass approximation → limiter → AAC 192k.
    """
    if preview:
        af = f"loudnorm=I={LOUDNORM_I}:TP={LOUDNORM_TP}:LRA={LOUDNORM_LRA},{LIMITER}"
        print(f"  loudnorm (1-pass preview) → {output_path.name}")
        run_ffmpeg(["ffmpeg", "-y", "-hide_banner", "-nostats", "-i", str(input_path),
                    "-map", "0:v:0", "-map", "0:a:0", "-c:v", "copy", "-af", af,
                    "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                    "-movflags", "+faststart", str(output_path)], "loudnorm")
        return True

    print(f"  loudnorm pass 1: measuring {input_path.name}")
    measurement = measure_loudness(input_path)
    if measurement is None:
        print("  loudnorm measurement failed — falling back to 1-pass")
        return apply_loudnorm_two_pass(input_path, output_path, preview=True)

    print(f"    measured: I={measurement['input_i']} LUFS  "
          f"TP={measurement['input_tp']}  LRA={measurement['input_lra']}")
    af = (
        f"loudnorm=I={LOUDNORM_I}:TP={LOUDNORM_TP}:LRA={LOUDNORM_LRA}"
        f":measured_I={measurement['input_i']}"
        f":measured_TP={measurement['input_tp']}"
        f":measured_LRA={measurement['input_lra']}"
        f":measured_thresh={measurement['input_thresh']}"
        f":offset={measurement['target_offset']}"
        f":linear=true,{LIMITER}"
    )
    print(f"  loudnorm pass 2: normalizing → {output_path.name}")
    run_ffmpeg(["ffmpeg", "-y", "-hide_banner", "-nostats", "-i", str(input_path),
                "-map", "0:v:0", "-map", "0:a:0", "-c:v", "copy", "-af", af, *AAC_FINAL,
                "-movflags", "+faststart", str(output_path)], "loudnorm")
    return True


def loudness_report(path: Path) -> tuple[float | None, float | None]:
    """(integrated LUFS, true peak dBTP) of a finished file."""
    proc = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-i", str(path),
         "-filter_complex", "ebur128=peak=true", "-f", "null", "-"],
        capture_output=True, text=True,
    )
    summary = proc.stderr[proc.stderr.rfind("Summary:"):]
    i = re.search(r"I:\s+(-?[\d.]+) LUFS", summary)
    tp = re.search(r"Peak:\s+(-?[\d.]+) dBFS", summary)
    return (float(i.group(1)) if i else None, float(tp.group(1)) if tp else None)


# -------- Creator-reel layouts: media split, full_pip, alternate zooms, SFX ----------

SKILL_DIR = Path(__file__).resolve().parent.parent
SFX_DIR = SKILL_DIR / "assets" / "sfx"
# Seconds from a sound's start to its peak: fire this much early so the peak lands on the cut.
ATTACK_S: dict[str, float] = {"whoosh": 0.25}
SFX_GAIN_DB = -10.0
ALPHA_PIX = ("yuva", "gbra", "rgba", "bgra", "argb", "abgr", "ya")   # same list as slots.py
MEDIA_LAYOUTS = ("split", "full", "full_pip")    # layouts that take the frame away from the speaker
MEDIA_PAD = "#0E0E10"                            # contain-fit letterbox colour
PIP_SIZE = 340                                   # face-circle diameter on a 1080-px short edge
PIP_MARGIN = 24                                  # px inside the platform safe zone
MIN_ZOOM_S = 0.1                                 # generated zoom pieces shorter than this are dropped


def probe_pix_fmt(path: Path) -> str | None:
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v:0",
             "-show_entries", "stream=pix_fmt", "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
            capture_output=True, text=True, check=True,
        )
        return out.stdout.strip() or None
    except (subprocess.CalledProcessError, OSError):
        return None


def overlay_is_panel(ext: str, pix_fmt: str | None, dims: tuple[int, int] | None,
                     canvas_sizes: list[tuple[int, int]]) -> bool:
    """A split overlay is a full-canvas graphic panel (legacy behaviour) when it is canvas-sized
    and has alpha (pix_fmt) or is a .mov/.webm render; anything else is media for the top half.
    Unprobeable files keep the legacy panel behaviour."""
    if dims is None:
        return True
    if tuple(dims) not in {tuple(c) for c in canvas_sizes}:
        return False
    return bool(pix_fmt and pix_fmt.startswith(ALPHA_PIX)) or ext in (".mov", ".webm")


def media_fit_chain(fit: str, tw: int, th: int, focus_x: float = 0.5, focus_y: float = 0.5,
                    pad_color: str = MEDIA_PAD) -> str:
    """Scale media into a tw x th box: cover (fill + crop at focus), contain (fit + pad), stretch."""
    if fit == "stretch":
        return f"scale={tw}:{th}:flags=lanczos,setsar=1"
    if fit == "contain":
        return (f"scale={tw}:{th}:force_original_aspect_ratio=decrease:flags=lanczos,"
                f"pad={tw}:{th}:(ow-iw)/2:(oh-ih)/2:color={hex_to_ff(pad_color)},setsar=1")
    fx = min(1.0, max(0.0, float(focus_x)))
    fy = min(1.0, max(0.0, float(focus_y)))
    return (f"scale={tw}:{th}:force_original_aspect_ratio=increase:flags=lanczos,"
            f"crop={tw}:{th}:(iw-{tw})*{fx:.3f}:(ih-{th})*{fy:.3f},setsar=1")


def _subtract(a: float, b: float, cuts: list[tuple[float, float]]) -> list[tuple[float, float]]:
    pieces = [(a, b)]
    for c0, c1 in sorted(cuts):
        nxt = []
        for p0, p1 in pieces:
            if c1 <= p0 or c0 >= p1:
                nxt.append((p0, p1))
                continue
            if c0 > p0:
                nxt.append((p0, c0))
            if c1 < p1:
                nxt.append((c1, p1))
        pieces = nxt
    return pieces


def alternate_zooms(timeline: dict, overlays: list[dict], scale: float = 1.15, x: float = 0.5,
                    y: float = 0.36, skip_overlays: bool = True, start: str = "zoomed") -> list[dict]:
    """Punch in on every second segment of the measured timeline so consecutive jump cuts
    alternate scale / 1.0. start="zoomed" (default) zooms segments 1, 3, 5 … (counting from 1, so
    the hook is punched in); start="wide" zooms 2, 4, 6 …. With skip_overlays, the windows of
    split / full / full_pip overlays (start_in_output + duration + hold) are cut out of the zooms."""
    if start not in ("zoomed", "wide"):
        raise ValueError(f"alternate zooms start must be 'zoomed' or 'wide', not {start!r}")
    phase = 0 if start == "zoomed" else 1
    segs = (timeline or {}).get("segments") or []
    cuts: list[tuple[float, float]] = []
    if skip_overlays:
        for o in overlays or []:
            if o.get("layout") not in MEDIA_LAYOUTS:
                continue
            t0 = float(o.get("start_in_output", 0))
            d = float(o.get("duration") or 0) + float(o.get("hold") or 0)
            if d > 0:
                cuts.append((t0, t0 + d))
    out: list[dict] = []
    for i, seg in enumerate(segs):
        if i % 2 != phase:
            continue
        a = float(seg["out_start"])
        b = a + float(seg["out_duration"])
        for p0, p1 in _subtract(a, b, cuts):
            if p1 - p0 >= MIN_ZOOM_S:
                out.append({"start": round(p0, 3), "end": round(p1, 3), "scale": float(scale),
                            "x": float(x), "y": float(y), "range": i})
    return out


def resolve_zooms(edl: dict, timeline: dict) -> list[dict]:
    """EDL zooms as a list: the explicit list, or the one generated by {"mode": "alternate", …}."""
    z = edl.get("zooms")
    if not z:
        return []
    if isinstance(z, list):
        return z
    if not isinstance(z, dict):
        sys.exit("EDL 'zooms' must be a list or an object like {\"mode\": \"alternate\"}")
    mode = z.get("mode", "alternate")
    if mode != "alternate":
        sys.exit(f"unknown zooms mode '{mode}' (supported: alternate)")
    if z.get("start", "zoomed") not in ("zoomed", "wide"):
        sys.exit(f"zooms.start must be 'zoomed' or 'wide', not {z.get('start')!r}")
    gen = alternate_zooms(timeline, edl.get("overlays") or [], scale=float(z.get("scale", 1.15)),
                          x=float(z.get("x", 0.5)), y=float(z.get("y", 0.36)),
                          skip_overlays=bool(z.get("skip_overlays", True)),
                          start=str(z.get("start", "zoomed")))
    # end_hold freezes the last frame: if the zoom runs to the end of the last segment, carry it
    # through the hold so the frozen frame does not snap back to 1.0x.
    end_hold = float(edl.get("end_hold") or 0)
    segs = (timeline or {}).get("segments") or []
    if end_hold > 0 and gen and segs:
        last = segs[-1]
        base_end = float(last["out_start"]) + float(last["out_duration"])
        if gen[-1]["range"] == len(segs) - 1 and abs(gen[-1]["end"] - base_end) < 1e-3:
            gen[-1]["end"] = round(gen[-1]["end"] + end_hold, 3)
    for item in gen:
        for k in ("sfx", "sfx_gain_db"):
            if k in z:
                item[k] = z[k]
    return gen


def _sfx_values(val) -> list[str]:
    if not val:
        return []
    names = [val] if isinstance(val, str) else list(val)
    return [str(n) for n in names if n and str(n) != "none"]


def has_sfx(edl: dict) -> bool:
    items = list(edl.get("ranges") or []) + list(edl.get("overlays") or [])
    z = edl.get("zooms")
    items += z if isinstance(z, list) else ([z] if isinstance(z, dict) else [])
    return any(_sfx_values(i.get("sfx")) for i in items)


def expand_sfx(edl: dict, timeline: dict, edit_dir: Path | None = None,
               sfx_dir: Path | None = None) -> list[dict]:
    """`"sfx"` on ranges, overlays and zooms → one-shot `audio[]` items.

    Fires at the item's output start (ranges: measured timeline offset) minus ATTACK_S[name].
    A name resolves to <skill>/assets/sfx/<name>.wav; a value containing "/" or ending in
    .wav/.mp3 is a path relative to the EDL folder. Gain: item sfx_gain_db > EDL sfx_gain_db > -10."""
    sfx_dir = Path(sfx_dir) if sfx_dir else SFX_DIR
    default_gain = float(edl.get("sfx_gain_db", SFX_GAIN_DB))
    segs = (timeline or {}).get("segments") or []
    events: list[tuple[float, dict]] = []
    t = 0.0
    for i, r in enumerate(edl.get("ranges") or []):
        if i < len(segs):
            start, dur = float(segs[i]["out_start"]), float(segs[i]["out_duration"])
        else:
            start, dur = t, float(r["end"]) - float(r["start"])
        t = start + dur
        events.append((start, r))
    for o in edl.get("overlays") or []:
        events.append((float(o.get("start_in_output", 0)), o))
    for z in resolve_zooms(edl, timeline):
        events.append((float(z["start"]), z))

    items: list[dict] = []
    for t0, item in events:
        names = _sfx_values(item.get("sfx"))
        if not names:
            continue
        gain = float(item.get("sfx_gain_db", default_gain))
        for name in names:
            if "/" in name or name.lower().endswith((".wav", ".mp3")):
                path = str(resolve_path(name, edit_dir)) if edit_dir is not None else name
                key = Path(name).stem
            else:
                p = sfx_dir / f"{name}.wav"
                if not p.exists():
                    sys.exit(f"sfx '{name}' not found: {p}\n"
                             f"Synthesize the SFX library first: cd {SKILL_DIR} && "
                             f"uv run python helpers/sfx_synth.py assets/sfx")
                path, key = str(p), name
            items.append({"file": path, "start_in_output": round(max(0.0, t0 - ATTACK_S.get(key, 0.0)), 3),
                          "gain_db": gain, "sfx": name})
    items.sort(key=lambda a: a["start_in_output"])
    return items


def pip_geometry(o: dict, edl: dict, canvas_full: tuple[int, int]) -> dict | None:
    """Face circle for a full_pip overlay, in full-canvas px: size, position, face crop square."""
    pip = o.get("pip", True)
    if pip is False or o.get("layout") != "full_pip":
        return None
    pip = pip if isinstance(pip, dict) else {}
    W, H = canvas_full
    size = int(round(float(pip.get("size", PIP_SIZE * min(W, H) / 1080))))
    name = edl.get("platform") or (edl.get("captions") or {}).get("platform") or platform_for_canvas(W, H)
    x0, y0, x1, y1 = scaled(get_platform(name), W, H)["safe"]
    x = float(pip["x"]) if "x" in pip else x1 - size - PIP_MARGIN
    y = float(pip["y"]) if "y" in pip else y0 + PIP_MARGIN
    crop_size = float(pip.get("crop_size", W * 0.5))
    crop_y = float(pip.get("crop_y", edl.get("face_crop_y", H * 0.2)))
    crop_x = float(pip.get("crop_x", (W - crop_size) / 2))
    return {"size": size, "x": x, "y": y, "crop_size": crop_size, "crop_x": crop_x, "crop_y": crop_y}


def circle_mask(edit_dir: Path, d: int) -> Path:
    """Anti-aliased white-on-black disc, d x d, for alphamerge."""
    from PIL import Image, ImageDraw
    out = edit_dir / "_work" / f"pip_mask_{d}.png"
    if out.exists():
        return out
    out.parent.mkdir(parents=True, exist_ok=True)
    k = 4
    big = Image.new("L", (d * k, d * k), 0)
    ImageDraw.Draw(big).ellipse((0, 0, d * k - 1, d * k - 1), fill=255)
    big.resize((d, d), Image.LANCZOS).save(out)
    return out


def _load_timeline(edit_dir: Path) -> dict:
    p = edit_dir / "timeline.json"
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text())
    except json.JSONDecodeError:
        return {}


# -------- Final compositing (Rule 1 + Rule 4) -------------------------------


def _num(v, scale: float) -> str:
    """Overlay position: numbers are canvas px (scaled for drafts), strings raw ffmpeg expressions."""
    if isinstance(v, (int, float)):
        return str(int(round(v * scale)))
    return str(v)


def build_composite(
    base_path: Path,
    edl: dict,
    edit_dir: Path,
    subtitles_path: Path | None,
    fonts_dir: Path | None,
    canvas_full: tuple[int, int],
) -> tuple[list[str], str, str, str, float]:
    """→ (ffmpeg inputs, filter_complex, video label, audio label, output duration)."""
    bw, bh = probe_dims(base_path) or canvas_full
    base_dur = probe_duration(base_path) or float(edl.get("total_duration_s") or 0)
    s = bw / canvas_full[0]                       # draft renders are smaller than the canvas
    timeline = _load_timeline(edit_dir)
    fps = timeline.get("fps") or "30"
    end_hold = float(edl.get("end_hold") or 0)
    out_dur = base_dur + end_hold

    # resolve every overlay once: file, window, and what a "split" overlay is (panel vs media)
    ovs: list[dict] = []
    for o in edl.get("overlays") or []:
        path = resolve_path(o["file"], edit_dir)
        if not path.exists():
            sys.exit(f"overlay not found: {path}")
        ext = path.suffix.lower()
        layout = o.get("layout")
        mode = None
        if layout == "split":
            dims = probe_dims(path)
            pix = probe_pix_fmt(path) if dims else None
            mode = "panel" if overlay_is_panel(ext, pix, dims, [(bw, bh), tuple(canvas_full)]) else "split_media"
        elif layout in ("full", "full_pip"):
            mode = layout
        ovs.append({"o": o, "path": path, "ext": ext, "mode": mode,
                    "dur": float(o.get("duration") or probe_duration(path) or 0),
                    "hold": float(o.get("hold") or 0)})
    edl_r = {**edl, "overlays": [{**x["o"], "duration": x["dur"]} for x in ovs]}

    zooms = resolve_zooms(edl_r, timeline)
    if isinstance(edl.get("zooms"), dict):
        (edit_dir / "_zooms_generated.json").write_text(json.dumps(zooms, indent=2))
        print(f"alternate zooms ({len(zooms)}) → _zooms_generated.json")
        for z in zooms:
            print(f"    {z['start']:7.3f}-{z['end']:7.3f}  x{z['scale']}  (range {z['range']})")
    audio_items = list(edl.get("audio") or []) + expand_sfx(edl_r, timeline, edit_dir)

    inputs = ["-i", str(base_path)]
    n_in = 1                                      # next ffmpeg input index
    parts: list[str] = []
    v = "[0:v]"

    if end_hold > 0:
        parts.append(f"{v}tpad=stop_mode=clone:stop_duration={end_hold:.3f}[vhold]")
        v = "[vhold]"

    # punch-in zooms: hard cuts to a tighter framing; zooms with the same framing share one crop
    groups: dict[tuple, list[tuple[float, float]]] = {}
    for z in zooms:
        key = (float(z.get("scale", 1.15)), float(z.get("x", 0.5)), float(z.get("y", 0.5)))
        groups.setdefault(key, []).append((float(z["start"]), float(z["end"])))
    for gi, ((zs, zx, zy), wins) in enumerate(groups.items()):
        cw, ch = int(bw / zs) // 2 * 2, int(bh / zs) // 2 * 2
        cx = int(min(max(zx * bw - cw / 2, 0), bw - cw))
        cy = int(min(max(zy * bh - ch / 2, 0), bh - ch))
        en = "+".join(f"between(t,{a:.3f},{b:.3f})" for a, b in wins)
        parts.append(f"{v}split[zm{gi}][zs{gi}];[zs{gi}]crop={cw}:{ch}:{cx}:{cy},"
                     f"scale={bw}:{bh}:flags=lanczos[zz{gi}];[zm{gi}][zz{gi}]overlay=0:0:enable='{en}'[vz{gi}]")
        v = f"[vz{gi}]"

    # split layouts: while a panel / media covers the top half, show the speaker in the bottom half
    split_groups: dict[int, list[str]] = {}
    for x in ovs:
        o = x["o"]
        if o.get("layout") != "split":
            continue
        t0 = float(o["start_in_output"])
        if x["mode"] == "panel":
            dur = float(o.get("duration") or 0)
            inset = float(o.get("swap_inset", 0.15))  # swap only while the panel is fully opaque
        else:
            dur = x["dur"] + x["hold"]                # media cuts in hard: swap for the whole window
            inset = float(o.get("swap_inset", 0.0))
        crop_y = int(round(float(o.get("crop_y", edl.get("face_crop_y", canvas_full[1] * 0.2))) * s))
        split_groups.setdefault(crop_y, []).append(f"between(t,{t0 + inset:.3f},{t0 + dur - inset:.3f})")
    for gi, (crop_y, wins) in enumerate(split_groups.items()):
        half = bh // 2
        crop_y = max(0, min(crop_y, bh - half))
        parts.append(f"{v}split[sm{gi}][sc{gi}];[sc{gi}]crop={bw}:{half}:0:{crop_y}[scc{gi}];"
                     f"[sm{gi}][scc{gi}]overlay=0:{half}:enable='{'+'.join(wins)}'[vs{gi}]")
        v = f"[vs{gi}]"

    # into RGB once: overlays and captions composite in RGB, one BT.709 conversion at the end
    parts.append(f"{v}scale=in_color_matrix=bt709:in_range=tv,format=gbrp[vrgb]")
    v = "[vrgb]"
    pip_geo = {i: g for i, x in enumerate(ovs) if (g := pip_geometry(x["o"], edl, canvas_full))}
    if pip_geo:                                   # speaker copies for the face circles
        parts.append(f"{v}split={len(pip_geo) + 1}[vrgbm]" + "".join(f"[pipsrc{i}]" for i in pip_geo))
        v = "[vrgbm]"

    for idx, x in enumerate(ovs, start=1):
        o, path, ext, mode = x["o"], x["path"], x["ext"], x["mode"]
        t0, dur, hold = float(o["start_in_output"]), x["dur"], x["hold"]
        is_img = ext in IMAGE_EXTS
        media = mode in ("split_media", "full", "full_pip")
        seek = ["-ss", f"{float(o['trim_start']):.3f}"] if o.get("trim_start") and not is_img else []
        loop = ["-stream_loop", "-1"] if o.get("loop") and not is_img else []
        if is_img:
            inputs += ["-loop", "1", "-framerate", str(fps), "-t", f"{dur + hold + 0.1:.3f}", "-i", str(path)]
        elif ext == ".webm":
            inputs += [*loop, *seek, "-c:v", "libvpx-vp9", "-i", str(path)]   # native VP9 decoder drops alpha
        else:
            inputs += [*loop, *seek, "-i", str(path)]
        n = n_in
        n_in += 1
        chain = [f"[{n}:v]format=gbrap"]
        if media:
            tw, th = (bw, bh // 2) if mode == "split_media" else (bw, bh)
            fit = o.get("fit") or ("contain" if is_img else "cover")
            chain.append(media_fit_chain(fit, tw, th, float(o.get("focus_x", 0.5)),
                                         float(o.get("focus_y", 0.5)), o.get("pad_color", MEDIA_PAD)))
        elif is_img or o.get("width") or o.get("height"):
            if o.get("width") or o.get("height"):
                ow = _num(o["width"], s) if o.get("width") else "-1"
                oh = _num(o["height"], s) if o.get("height") else "-1"
                chain.append(f"scale={ow}:{oh}:flags=lanczos")
        else:
            ov_dims = probe_dims(path)
            if ov_dims and ov_dims != (bw, bh):
                fit = o.get("fit", "cover")       # b-roll: fill the frame and trim, never stretch
                if fit == "stretch":
                    chain.append(f"scale={bw}:{bh}:flags=lanczos")
                elif fit == "contain":
                    chain.append(f"scale={bw}:{bh}:force_original_aspect_ratio=decrease:flags=lanczos,"
                                 f"pad={bw}:{bh}:(ow-iw)/2:(oh-ih)/2:color=black@0")
                else:
                    fx, fy = float(o.get("focus_x", 0.5)), float(o.get("focus_y", 0.5))
                    chain.append(f"scale={bw}:{bh}:force_original_aspect_ratio=increase:flags=lanczos,"
                                 f"crop={bw}:{bh}:(iw-{bw})*{fx:.3f}:(ih-{bh})*{fy:.3f}")
        if loop:
            chain.append(f"trim=duration={dur:.3f}")  # the looped input is endless
        if o.get("opacity") is not None and float(o["opacity"]) < 1:
            chain.append(f"colorchannelmixer=aa={float(o['opacity']):.3f}")
        if hold > 0:
            chain.append(f"tpad=stop_mode=clone:stop_duration={hold:.3f}")
        chain.append(f"setpts=PTS-STARTPTS+{t0:.3f}/TB")
        parts.append(",".join(chain) + f"[ov{idx}]")
        ox, oy = (_num(o.get("x", 0), s), _num(o.get("y", 0), s))
        end = t0 + dur + hold
        parts.append(f"{v}[ov{idx}]overlay=x={ox}:y={oy}:eof_action=pass:format=gbrp:"
                     f"enable='between(t,{t0:.3f},{end:.3f})'[vo{idx}]")
        v = f"[vo{idx}]"

        g = pip_geo.get(idx - 1)
        if g:                                     # speaker as a circle over the full-screen media
            d = max(2, int(round(g["size"] * s)) // 2 * 2)
            cs = max(2, min(int(round(g["crop_size"] * s)), bw, bh))
            cx = max(0, min(int(round(g["crop_x"] * s)), bw - cs))
            cy = max(0, min(int(round(g["crop_y"] * s)), bh - cs))
            px = max(0, min(int(round(g["x"] * s)), bw - d))
            py = max(0, min(int(round(g["y"] * s)), bh - d))
            mask = circle_mask(edit_dir, d)
            inputs += ["-loop", "1", "-framerate", str(fps), "-t", f"{end - t0 + 0.1:.3f}", "-i", str(mask)]
            m = n_in
            n_in += 1
            parts.append(f"[{m}:v]format=gray[pm{idx}]")
            parts.append(f"[pipsrc{idx - 1}]trim=start={t0:.3f}:end={end:.3f},setpts=PTS-STARTPTS,"
                         f"crop={cs}:{cs}:{cx}:{cy},scale={d}:{d}:flags=lanczos,format=gbrap[pf{idx}]")
            parts.append(f"[pf{idx}][pm{idx}]alphamerge,setpts=PTS-STARTPTS+{t0:.3f}/TB[pip{idx}]")
            parts.append(f"{v}[pip{idx}]overlay=x={px}:y={py}:eof_action=pass:format=gbrp:"
                         f"enable='between(t,{t0:.3f},{end:.3f})'[vp{idx}]")
            v = f"[vp{idx}]"

    # captions LAST — Rule 1
    if subtitles_path is not None:
        if subtitles_path.suffix.lower() == ".ass":
            parts.append(f"{v}{ass_filter(subtitles_path, fonts_dir)}[vsub]")
        else:
            parts.append(f"{v}subtitles=filename={ff_quote(subtitles_path.resolve())}:"
                         f"force_style='{SUB_FORCE_STYLE}'[vsub]")
        v = "[vsub]"

    parts.append(f"{v}scale=out_color_matrix=bt709:out_range=tv,format=yuv420p[outv]")

    # ---- audio: dialogue (+ hold) + beds ducked under speech + one-shot effects
    dlg = "[0:a]aformat=sample_rates=48000:channel_layouts=stereo"
    if end_hold > 0:
        dlg += f",apad=pad_dur={end_hold:.3f}"
    parts.append(dlg + "[dlg]")
    beds, sfx = [], []
    for k, a in enumerate(audio_items):
        path = resolve_path(a["file"], edit_dir)
        if not path.exists():
            sys.exit(f"audio file not found: {path}")
        inputs += ["-i", str(path)]
        n = n_in
        n_in += 1
        t0 = float(a.get("start_in_output", 0))
        chain = [f"[{n}:a]aformat=sample_rates=48000:channel_layouts=stereo"]
        if a.get("trim_start"):
            chain.append(f"atrim=start={float(a['trim_start']):.3f}")
        chain.append("asetpts=PTS-STARTPTS")
        length = float(a["duration"]) if a.get("duration") else max(0.1, out_dur - t0)
        chain.append(f"atrim=duration={length:.3f}")
        if a.get("fade_in"):
            chain.append(f"afade=t=in:st=0:d={float(a['fade_in']):.3f}")
        if a.get("fade_out"):
            fo = float(a["fade_out"])
            chain.append(f"afade=t=out:st={max(0.0, length - fo):.3f}:d={fo:.3f}")
        if not a.get("duck"):
            # v6: roll the highs off one-shot SFX so they never fight vocal consonants on phone speakers
            lp = float(a.get("lowpass_hz", edl.get("sfx_lowpass_hz", 0)) or 0)
            if lp > 0:
                chain.append(f"lowpass=f={lp:.0f}:poles=2")
        chain.append(f"volume={float(a.get('gain_db', -18 if a.get('duck') else -6)):.2f}dB")
        if t0 > 0:
            chain.append(f"adelay={int(round(t0 * 1000))}:all=1")
        label = f"[au{k}]"
        parts.append(",".join(chain) + label)
        (beds if a.get("duck") else sfx).append(label)

    mix_inputs = []
    if beds:
        if len(beds) > 1:
            parts.append("".join(beds) + f"amix=inputs={len(beds)}:normalize=0:duration=longest[beds]")
            bed = "[beds]"
        else:
            bed = beds[0]
        parts.append("[dlg]asplit[dlgm][dlgk]")
        parts.append(f"{bed}[dlgk]sidechaincompress=threshold=0.02:ratio=8:attack=20:release=350[bedd]")
        mix_inputs = ["[dlgm]", "[bedd]"]
    else:
        mix_inputs = ["[dlg]"]
    mix_inputs += sfx
    if len(mix_inputs) > 1:
        parts.append("".join(mix_inputs) + f"amix=inputs={len(mix_inputs)}:normalize=0:duration=first[aout]")
    else:
        parts.append(f"{mix_inputs[0]}anull[aout]")

    return inputs, ";".join(parts), "[outv]", "[aout]", out_dur


def composite(
    base_path: Path,
    edl: dict,
    edit_dir: Path,
    subtitles_path: Path | None,
    fonts_dir: Path | None,
    canvas_full: tuple[int, int],
    out_path: Path,
    quality: str,
    pcm_audio: bool,
) -> None:
    has_work = any([
        edl.get("overlays"), edl.get("zooms"), edl.get("audio"), has_sfx(edl),
        float(edl.get("end_hold") or 0) > 0, subtitles_path is not None,
    ])
    if not has_work:
        run_ffmpeg(["ffmpeg", "-y", "-i", str(base_path), "-c:v", "copy",
                    *(["-c:a", "pcm_s16le"] if pcm_audio else ["-c:a", "copy"]), str(out_path)], "copy")
        return
    inputs, graph, vlabel, alabel, out_dur = build_composite(
        base_path, edl, edit_dir, subtitles_path, fonts_dir, canvas_full)
    preset, crf = {"draft": ("ultrafast", "28"), "preview": ("medium", "22")}.get(quality, ("slow", "18"))
    fps = (json.loads((edit_dir / "timeline.json").read_text()).get("fps")
           if (edit_dir / "timeline.json").exists() else None)
    cmd = ["ffmpeg", "-y", "-hide_banner", *inputs, "-filter_complex", graph,
           "-map", vlabel, "-map", alabel, "-t", f"{out_dur:.3f}",
           "-c:v", "libx264", "-preset", preset, "-crf", crf, "-profile:v", "high",
           "-pix_fmt", "yuv420p", *BT709_TAGS, *(["-r", fps] if fps else []),
           *(["-c:a", "pcm_s16le"] if pcm_audio else AAC_FINAL),
           *([] if out_path.suffix == ".mkv" else ["-movflags", "+faststart"]),
           str(out_path)]
    n_ov = len(edl.get("overlays") or [])
    zooms = edl.get("zooms") or []
    n_zoom = len(zooms) if isinstance(zooms, list) else zooms.get("mode", "alternate")
    print(f"compositing → {out_path.name}  (overlays {n_ov}, zooms {n_zoom}, "
          f"audio {len(edl.get('audio') or [])}, sfx {'yes' if has_sfx(edl) else 'no'}, "
          f"captions {'yes' if subtitles_path else 'no'})")
    (edit_dir / "_composite_graph.txt").write_text(graph.replace(";", ";\n"))
    run_ffmpeg(cmd, "composite (graph saved to _composite_graph.txt)")


# -------- Contact sheet (--sheet) ------------------------------------------------

SHEET_FONT = "/System/Library/Fonts/Helvetica.ttc"


def sheet_picks(edl: dict, timeline: dict, overlay_durs: list[float] | None = None) -> list[tuple[float, str]]:
    """(time, label) for the midpoint of every range and every overlay window, in time order."""
    picks: list[tuple[float, str]] = []
    ranges = edl.get("ranges") or []
    for i, seg in enumerate((timeline or {}).get("segments") or []):
        r = ranges[i] if i < len(ranges) else {}
        beat = r.get("beat") or ""
        picks.append((float(seg["out_start"]) + float(seg["out_duration"]) / 2,
                      f"range {i + 1}" + (f" · {beat}" if beat else "")))
    for k, o in enumerate(edl.get("overlays") or []):
        d = overlay_durs[k] if overlay_durs else float(o.get("duration") or 0)
        d += float(o.get("hold") or 0)
        picks.append((float(o.get("start_in_output", 0)) + d / 2, o.get("layout") or "overlay"))
    return sorted(picks, key=lambda p: p[0])


def contact_sheet(video: Path, edl: dict, edit_dir: Path, out: Path, cols: int = 6) -> Path | None:
    """Tile one frame per range midpoint and per overlay window, labelled with time and layout."""
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        print("  sheet skipped: Pillow not installed")
        return None
    durs = []
    for o in edl.get("overlays") or []:
        durs.append(float(o.get("duration") or probe_duration(resolve_path(o["file"], edit_dir)) or 0))
    picks = sheet_picks(edl, _load_timeline(edit_dir), durs)
    if not picks:
        return None
    vw, vh = probe_dims(video) or (1080, 1920)
    tw, th = (480, 270) if vw > vh else (270, 480)
    total = probe_duration(video) or max(t for t, _ in picks) + 0.1
    tmp = edit_dir / "_work" / "sheet"
    tmp.mkdir(parents=True, exist_ok=True)
    label_h, gap = 34, 8
    rows = (len(picks) + cols - 1) // cols
    ncols = min(cols, len(picks))
    sheet = Image.new("RGB", (gap + ncols * (tw + gap), gap + rows * (th + label_h + gap)), (18, 18, 20))
    draw = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype(SHEET_FONT, 16)
    except OSError:
        font = ImageFont.load_default()
    for i, (t, label) in enumerate(picks):
        t = min(max(0.0, t), max(0.0, total - 0.05))
        frame = tmp / f"f{i:03d}.jpg"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.3f}", "-i", str(video), "-frames:v", "1",
                        "-vf", f"scale={tw}:{th}:force_original_aspect_ratio=decrease,"
                               f"pad={tw}:{th}:(ow-iw)/2:(oh-ih)/2", "-q:v", "3", str(frame)],
                       capture_output=True)
        x = gap + (i % cols) * (tw + gap)
        y = gap + (i // cols) * (th + label_h + gap)
        if frame.exists():
            with Image.open(frame) as im:
                sheet.paste(im.convert("RGB").resize((tw, th)), (x, y))
            frame.unlink(missing_ok=True)
        draw.text((x + 6, y + th + 8), f"{t:6.2f}s  {label}"[:40], fill=(235, 235, 235), font=font)
    sheet.save(out, quality=88)
    return out


# -------- Main ---------------------------------------------------------------


def full_canvas(edl: dict, base_path: Path) -> tuple[int, int]:
    c = output_canvas(edl, draft=False)
    if c:
        return c
    dims = probe_dims(base_path) or (1920, 1080)
    w, h = dims
    # base rendered in draft mode is 1280 on the long edge; captions/graphics are authored at 1920
    if max(w, h) == 1280:
        return (round(w * 1.5 / 2) * 2, round(h * 1.5 / 2) * 2)
    return dims


def main() -> None:
    ap = argparse.ArgumentParser(description="Render a video from an EDL")
    ap.add_argument("edl", type=Path, help="Path to edl.json")
    ap.add_argument("-o", "--output", type=Path, required=True, help="Output video path")
    ap.add_argument("--preview", action="store_true",
                    help="Preview mode: medium preset, CRF 22 — evaluable for QC, faster than final.")
    ap.add_argument("--draft", action="store_true",
                    help="Draft mode: 2/3 size, ultrafast, CRF 28 — cut-point verification only.")
    ap.add_argument("--base-only", action="store_true",
                    help="Stop after the cut (base.mp4 + timeline.json). Build graphics against this.")
    ap.add_argument("--reuse-base", action="store_true",
                    help="Skip extraction/concat when base and timeline already match this EDL.")
    ap.add_argument("--captions", action="store_true",
                    help="Build branded captions.ass (captions.py) from the measured timeline and burn it in.")
    ap.add_argument("--build-subtitles", action="store_true",
                    help="Legacy: build an uppercase master.srt and burn it in.")
    ap.add_argument("--no-subtitles", action="store_true", help="Skip captions even if the EDL references some.")
    ap.add_argument("--no-loudnorm", action="store_true",
                    help="Skip loudness normalization. Default is on (-14 LUFS, true peak < -1 dBTP).")
    ap.add_argument("--fps", type=parse_fps, default=None,
                    help="Output frame rate. Default: EDL output.fps, else the first source's rate (24 if unknown).")
    ap.add_argument("--sheet", action="store_true",
                    help="After rendering, write <output stem>_sheet.jpg: a frame per range and per overlay window.")
    args = ap.parse_args()

    edl_path = args.edl.resolve()
    if not edl_path.exists():
        sys.exit(f"edl not found: {edl_path}")
    edl = json.loads(edl_path.read_text())
    edit_dir = edl_path.parent
    out_path = args.output.resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    mode = "draft" if args.draft else ("preview" if args.preview else "final")

    # 1-2. cut → base (reused when nothing that shapes it changed)
    base_path = edit_dir / {"draft": "base_draft.mp4", "preview": "base_preview.mp4"}.get(mode, "base.mp4")
    key = base_key(edl, mode) + (f"-{args.fps}" if args.fps else "")
    key_file = edit_dir / f".{base_path.stem}.key"
    if args.reuse_base and base_path.exists() and key_file.exists() and key_file.read_text() == key \
            and (edit_dir / "timeline.json").exists():
        print(f"reusing {base_path.name} (EDL cut unchanged)")
    else:
        segment_paths = extract_all_segments(edl, edit_dir, preview=args.preview, draft=args.draft, fps=args.fps)
        concat_segments(segment_paths, base_path, edit_dir, edl)
        key_file.write_text(key)

    if args.base_only:
        if out_path != base_path.resolve():
            run_ffmpeg(["ffmpeg", "-y", "-i", str(base_path), "-c", "copy", str(out_path)], "copy")
        print(f"\nbase: {out_path}  (timeline: {edit_dir / 'timeline.json'})")
        return

    canvas = full_canvas(edl, base_path)

    # 3. captions: branded ASS (default) or legacy SRT
    subs_path: Path | None = None
    fonts_dir: Path | None = None
    if not args.no_subtitles:
        if args.captions:
            subs_path = edit_dir / "captions.ass"
            info = build_captions(edl, edit_dir, subs_path, canvas=canvas)
            print(f"captions → {subs_path.name} ({info['cues']} cues, font '{info['style']['font']}')")
            if info["style"].get("fonts_dir"):
                fonts_dir = Path(info["style"]["fonts_dir"])
        elif args.build_subtitles:
            subs_path = edit_dir / "master.srt"
            build_master_srt(edl, edit_dir, subs_path)
        elif edl.get("subtitles"):
            subs_path = resolve_subtitles_path(edl["subtitles"], edit_dir)
        if subs_path is not None and subs_path.suffix.lower() == ".ass" and fonts_dir is None:
            caps = load_brand_captions(None, edit_dir)
            fd = (edl.get("captions") or {}).get("fonts_dir") or caps.get("fonts_dir")
            fonts_dir = resolve_path(fd, edit_dir) if fd else None

    # 4. composite (+ loudness)
    if args.no_loudnorm:
        composite(base_path, edl, edit_dir, subs_path, fonts_dir, canvas, out_path, mode, pcm_audio=False)
    else:
        tmp = out_path.with_suffix(".prenorm.mkv")
        composite(base_path, edl, edit_dir, subs_path, fonts_dir, canvas, tmp, mode, pcm_audio=True)
        print("loudness normalization → -14 LUFS, true peak < -1 dBTP")
        apply_loudnorm_two_pass(tmp, out_path, preview=(mode != "final"))
        tmp.unlink(missing_ok=True)

    size_mb = out_path.stat().st_size / (1024 * 1024)
    lufs, tp = loudness_report(out_path)
    dur = probe_duration(out_path)
    print(f"\ndone: {out_path} ({size_mb:.1f} MB, {dur:.2f}s)" if dur else f"\ndone: {out_path} ({size_mb:.1f} MB)")
    if lufs is not None:
        print(f"  loudness: {lufs:.1f} LUFS integrated, true peak {tp:.1f} dBTP")
    if args.sheet:
        sheet = contact_sheet(out_path, edl, edit_dir, out_path.with_name(f"{out_path.stem}_sheet.jpg"))
        print(f"sheet: {sheet}" if sheet else "sheet: nothing to show")


if __name__ == "__main__":
    main()
