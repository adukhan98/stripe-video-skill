"""Assemble the long-form video: talk / screen / scene windows on the cut, the speaker card, overlays, sound.

Long-form is NOT rendered as one HTML composition (10+ min of HyperFrames is hours). The cut (render.py --base-only)
gives base.mp4 = his camera, cut, 1920x1080, with the voice. compose.py lays every output frame into exactly one window:

    talk    base.mp4 full frame                                                     (+ talk_overlay scenes on top)
    screen  board plate + his screen recording, cut with the SAME ranges, zoomed by zoomplan.Camera, in a window card
            + the speaker card                                                     (+ callout_overlay scenes on top)
    scene   a designed moment rendered by board.py (canvas | map | board | proof) + the speaker card

Inputs in <edit>/:
    base.mp4, timeline.json           render.py <edl> --base-only (EDL source = source/cam.mov)
    source/screen.mp4, source/cap.json  cap.py ingest
    layout.json                       {"theme": "light", "card": {"face_x": .5, "face_y": .42, "zoom": .92},
                                       "windows": [{"start": 12.3, "end": 40.0, "layout": "screen",
                                                    "zooms": [{"start": <SOURCE s>, "end": …, "x": <screen px>, "y": …, "scale": 2}]}],
                                       "music": "music/bed.mp3",       — OUTPUT seconds; anything not covered is "talk"
                                       "music_under_voice_db": 5}      — optional, see Sound
    animations/scenes.json + renders  board.py (opaque scenes become "scene" windows; overlays ride on top)

Sound (mix): voice from base.mp4 + structural SFX + the music bed ducked under the voice (sidechaincompress), then
two-pass loudnorm to -14 LUFS. Hang fix (2026-10-17): the bed used to be an endless `-stream_loop -1` input ended by
`-shortest` / `amix duration=first`; on a full-length video ffmpeg 6.0 wrote a complete final_mix.mov and then hung
forever at 0 % CPU (a deadlock that -t on the looped input does not cure). Now there is no -stream_loop: a bed as long
as the picture is a plain input, a shorter one is repeated with the concat demuxer (compose/music_loop.txt), and every
audio input is atrim'd to the picture's length, so the mix ends on its own.

Music level (2026-10-17, IMG_2533): he could not hear a bed at the old fixed -24 dB — he talks almost wall-to-wall, so the
sidechain keeps the bed ducked ~9 dB nearly all the time and it sat ~30 dB under him. He asked for "5 dB under my voice".
Now the bed is levelled automatically: compose measures the voice (integrated LUFS) and the ducked bed, and sets the bed
gain so the DUCKED bed sits `music_under_voice_db` (default 5) under the voice. `music_gain_db` overrides with a fixed gain
(dB relative to the old -24 dB). The bed runs in float, so a large gain does not clip before loudnorm.

Usage:
    python helpers/compose.py plan   --edit-dir E                  # the window table (check it against the beat table)
    python helpers/compose.py where  --edit-dir E <out_t> <sx> <sy> # where a screen point lands in the frame at out_t
    python helpers/compose.py render --edit-dir E -o final.mp4 [--preview] [--only-window N]
    python helpers/compose.py sheet  --edit-dir E <video>          # frames around every window boundary → verify/compose_sheet.jpg
"""

from __future__ import annotations

import argparse
import json
import math
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, str(Path(__file__).resolve().parent))
import zoomplan  # noqa: E402

REEL_HELPERS = Path.home() / ".claude" / "skills" / "adnaan-reel" / "helpers"
REEL_SFX = REEL_HELPERS.parent / "assets" / "sfx"
FPS = 30
W, H = 1920, 1080
CARD = (1600, 640, 260, 346)                # speaker card x, y, w, h — fixed for the whole video (moves only on a cut)
CARD_R, RIM = 24, 6
WIN = (96, 96, 1424, 888)                   # screen window card on the board
BAR = 46
VIEW = (WIN[0], WIN[1] + BAR, WIN[2], WIN[3] - BAR)   # the zoomed screen fills this
THEME = {
    "light": {"bg": (228, 222, 217), "card": (251, 250, 248), "bar": (241, 238, 234), "dot": (216, 211, 205), "grid": "lines"},
    "dark": {"bg": (30, 30, 30), "card": (42, 42, 42), "bar": (42, 42, 42), "dot": (85, 85, 85), "grid": "dots"},
}
TINT = (90, 80, 72)  # light vignette colour; brand_theme() re-points it (and THEME["light"]) to the brand file
OPAQUE = {"canvas", "map", "board", "proof"}
SFX_GAIN = -18.0


def brand_theme(edit: Path) -> None:
    """Plates follow edit/brand/brand.json (paper, card, vignette in the brand's deep colour), like the scenes do."""
    global TINT
    p = edit / "brand" / "brand.json"
    if not p.exists():
        return
    c = {k: v["hex"] for k, v in json.loads(p.read_text())["colors"].items()}
    h = lambda x: tuple(int(x.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))
    THEME["light"].update(bg=h(c["background"]), card=h(c["card"]), bar=h(c["background"]), dot=h(c["muted"]))
    TINT = h(c["deep"])


def sh(cmd: list[str], what: str = "") -> None:
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"ffmpeg failed ({what}):\n{r.stderr[-2000:]}")


def media_duration(p: Path) -> float | None:
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                       capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return None


def frames_of(p: Path) -> int:
    r = subprocess.run(["ffprobe", "-v", "error", "-count_packets", "-select_streams", "v:0", "-show_entries",
                        "stream=nb_read_packets", "-of", "csv=p=0", str(p)], capture_output=True, text=True)
    return int((r.stdout.strip() or "0").split(",")[0])


# ------------------------------------------------------------------ inputs
def load(edit: Path) -> dict:
    tl = json.loads((edit / "timeline.json").read_text())
    lay_p = edit / "layout.json"
    layout = json.loads(lay_p.read_text()) if lay_p.exists() else {}
    sc_p = edit / "animations" / "scenes.json"
    scenes = json.loads(sc_p.read_text()) if sc_p.exists() else {"scenes": []}
    cap_p = edit / "source" / "cap.json"
    cap = json.loads(cap_p.read_text()) if cap_p.exists() else {}
    total = frames_of(edit / "base.mp4")
    return {"tl": tl, "layout": layout, "scenes": scenes, "cap": cap, "total": total,
            "theme": layout.get("theme") or scenes.get("theme") or "light"}


def out_to_src(tl: dict, t: float) -> float:
    segs = tl["segments"]
    for s in segs:
        if t < s["out_start"] + s["out_duration"]:
            return s["start"] + max(0.0, t - s["out_start"])
    last = segs[-1]
    return last["end"]


def windows(d: dict) -> list[dict]:
    """Every output frame in exactly one window: scenes > layout windows > talk."""
    n = d["total"]
    kind: list[tuple] = [("talk", None)] * n
    for i, w in enumerate(d["layout"].get("windows") or []):
        a, b = round(w["start"] * FPS), min(n, round(w["end"] * FPS))
        for f in range(max(0, a), b):
            kind[f] = (w["layout"], i)
    for s in d["scenes"]["scenes"]:
        if s["type"] not in OPAQUE:
            continue
        a = round(s["start"] * FPS)
        b = min(n, a + round(s["duration"] * FPS))
        for f in range(max(0, a), b):
            kind[f] = ("scene", s["id"])
    out, f0 = [], 0
    for f in range(1, n + 1):
        if f == n or kind[f] != kind[f0]:
            k, ref = kind[f0]
            out.append({"i": len(out), "layout": k, "ref": ref, "f0": f0, "f1": f, "start": f0 / FPS, "end": f / FPS})
            f0 = f
    return out


def overlays_in(d: dict, edit: Path, w: dict) -> list[dict]:
    res = []
    for s in d["scenes"]["scenes"]:
        if s["type"] in OPAQUE:
            continue
        a = round(s["start"] * FPS)
        if w["f0"] <= a < w["f1"]:
            p = edit / "animations" / s["id"] / "render.mov"
            if p.exists():
                res.append({**s, "path": p, "offset": (a - w["f0"]) / FPS})
            else:
                print(f"  ! overlay {s['id']} has no render.mov — skipped")
    return res


# ------------------------------------------------------------------ plates (Pillow)
def rounded(size: tuple[int, int], r: int, fill=255) -> Image.Image:
    m = Image.new("L", size, 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, size[0] - 1, size[1] - 1], r, fill=fill)
    return m


def board_bg(theme: str) -> Image.Image:
    t = THEME[theme]
    img = Image.new("RGB", (W, H), t["bg"])
    dr = ImageDraw.Draw(img, "RGBA")
    if t["grid"] == "lines":
        for x in range(0, W, 64):
            dr.line([(x, 0), (x, H)], fill=(20, 20, 20, 13), width=2)
        for y in range(0, H, 64):
            dr.line([(0, y), (W, y)], fill=(20, 20, 20, 13), width=2)
    else:
        for x in range(20, W, 40):
            for y in range(20, H, 40):
                dr.ellipse([x - 1.6, y - 1.6, x + 1.6, y + 1.6], fill=(255, 255, 255, 33))
    # vignette (board.css #vignette)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    rr = np.sqrt(((xx - W * 0.5) / (W * 0.5)) ** 2 + ((yy - H * 0.45) / (H * 0.55)) ** 2) / 1.41
    inner = 0.5 if theme == "light" else 0.55
    k = np.clip((rr - inner) / (1 - inner), 0, 1) * (0.2 if theme == "light" else 0.35)
    tint = np.array(TINT if theme == "light" else (0, 0, 0), np.float32)
    a = np.asarray(img).astype(np.float32)
    a = a * (1 - k[..., None]) + tint * k[..., None]
    return Image.fromarray(a.clip(0, 255).astype(np.uint8))


def shadow(img: Image.Image, box: tuple, r: int, offset=(0, 18), blur=26, alpha=0.30) -> None:
    x, y, w, h = box
    sm = Image.new("L", img.size, 0)
    ImageDraw.Draw(sm).rounded_rectangle([x + 10, y + offset[1], x + w - 10, y + h + offset[1] - 6], r, fill=int(255 * alpha))
    sm = sm.filter(ImageFilter.GaussianBlur(blur))
    img.paste(Image.new("RGBA", img.size, (40, 30, 20, 255)), (0, 0), sm)


def make_plates(edit: Path, theme: str) -> dict:
    brand_theme(edit)
    out = edit / "compose" / "plates"
    out.mkdir(parents=True, exist_ok=True)
    t = THEME[theme]
    # screen plate: board + window card + bar dots (the zoomed screen goes into VIEW)
    plate = board_bg(theme).convert("RGBA")
    shadow(plate, WIN, 24)
    card = Image.new("RGBA", (WIN[2], WIN[3]), t["card"] + (255,))
    ImageDraw.Draw(card).rectangle([0, 0, WIN[2], BAR], fill=t["bar"] + (255,))
    for i in range(3):
        cx = 27 + i * 24
        ImageDraw.Draw(card).ellipse([cx - 7, BAR / 2 - 7, cx + 7, BAR / 2 + 7], fill=t["dot"] + (255,))
    plate.paste(card, (WIN[0], WIN[1]), rounded((WIN[2], WIN[3]), 24))
    plate.convert("RGB").save(out / f"screen_{theme}.png")
    # card frame: shadow + rim, full-frame RGBA (overlay at 0,0); the camera goes inside, masked
    fr = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    x, y, w, h = CARD
    shadow(fr, (x - RIM, y - RIM, w + 2 * RIM, h + 2 * RIM), CARD_R + RIM, alpha=0.42 if theme == "light" else 0.6)
    rim = (255, 255, 255, 255) if theme == "light" else (255, 255, 255, 230)
    rim_w = RIM if theme == "light" else 3
    fr.paste(Image.new("RGBA", (w + 2 * rim_w, h + 2 * rim_w), rim), (x - rim_w, y - rim_w), rounded((w + 2 * rim_w, h + 2 * rim_w), CARD_R + rim_w))
    fr.save(out / f"card_frame_{theme}.png")
    rounded((w, h), CARD_R).save(out / "card_mask.png")
    return {"screen": out / f"screen_{theme}.png", "frame": out / f"card_frame_{theme}.png", "mask": out / "card_mask.png"}


# ------------------------------------------------------------------ screen: cut + zoom
def screen_cut(edit: Path, tl: dict) -> Path:
    """source/screen.mp4 cut with the SAME ranges as base.mp4 (frame counts from timeline.json)."""
    out = edit / "compose" / "screen_cut.mp4"
    key = json.dumps([[s["start"], s["out_duration"]] for s in tl["segments"]])
    stamp = out.with_suffix(".key")
    if out.exists() and stamp.exists() and stamp.read_text() == key:
        return out
    parts, chains = [], []
    for i, s in enumerate(tl["segments"]):
        n = round(s["out_duration"] * FPS)
        chains.append(f"[0:v]trim=start={s['start']:.4f},setpts=PTS-STARTPTS,trim=end_frame={n},setpts=PTS-STARTPTS[v{i}]")
        parts.append(f"[v{i}]")
    fc = ";".join(chains) + ";" + "".join(parts) + f"concat=n={len(parts)}:v=1:a=0,fps={FPS}[v]"
    script = edit / "compose" / "screen_cut.filter"
    script.write_text(fc)
    sh(["ffmpeg", "-y", "-v", "error", "-i", str(edit / "source" / "screen.mp4"), "-filter_complex_script", str(script),
        "-map", "[v]", "-c:v", "libx264", "-crf", "12", "-preset", "medium", "-tune", "stillimage", "-pix_fmt", "yuv420p", str(out)],
       "screen cut")
    stamp.write_text(key)
    return out


def camera_for(d: dict, w: dict) -> zoomplan.Camera:
    cap = d["cap"]
    scr = tuple(cap.get("screen") or (1600, 1000))
    lw = (d["layout"].get("windows") or [])[w["ref"]] if isinstance(w["ref"], int) else {}
    zooms = zoomplan.gather(cap, scr, manual=lw.get("zooms"))
    return zoomplan.Camera(zooms, scr, (VIEW[2], VIEW[3]))


def render_viewport(edit: Path, d: dict, w: dict, cut: Path, out: Path) -> None:
    """Zoomed screen for one window: read frames of the cut screen, crop by the camera (source clock), scale to VIEW."""
    cam = camera_for(d, w)
    sw, sh_ = tuple(d["cap"].get("screen") or (1600, 1000))
    n = w["f1"] - w["f0"]
    vw, vh = VIEW[2], VIEW[3]
    dec = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", f"{w['start']:.4f}", "-i", str(cut), "-frames:v", str(n),
                            "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    enc = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{vw}x{vh}", "-r", str(FPS),
                            "-i", "-", "-c:v", "libx264", "-crf", "14", "-preset", "medium", "-tune", "stillimage",
                            "-pix_fmt", "yuv420p", str(out)], stdin=subprocess.PIPE)
    size = sw * sh_ * 3
    last = None
    for k in range(n):
        buf = dec.stdout.read(size)
        if len(buf) < size:
            buf = last          # hold the last frame if the source ran short
        if buf is None:
            break
        last = buf
        src_t = out_to_src(d["tl"], (w["f0"] + k) / FPS)
        x, y, rw, rh = cam.rect(src_t)
        im = Image.frombuffer("RGB", (sw, sh_), buf, "raw", "RGB", 0, 1)
        im = im.resize((vw, vh), Image.BICUBIC, box=(x, y, x + rw, y + rh))
        enc.stdin.write(im.tobytes())
    enc.stdin.close()
    enc.wait()
    dec.wait()


# ------------------------------------------------------------------ window composite
def card_chain(d: dict, src_label: str, base_idx: int, mask_idx: int, frame_idx: int, n: int) -> list[str]:
    c = d["layout"].get("card") or {}
    fx, fy, z = c.get("face_x", 0.5), c.get("face_y", 0.42), c.get("zoom", 0.92)
    ch = int(H * z) // 2 * 2
    cw = int(ch * CARD[2] / CARD[3]) // 2 * 2
    cx = int(min(max(fx * W - cw / 2, 0), W - cw))
    cy = int(min(max(fy * H - ch * 0.42, 0), H - ch))
    return [f"[{base_idx}:v]setpts=PTS-STARTPTS,crop={cw}:{ch}:{cx}:{cy},scale={CARD[2]}:{CARD[3]}:flags=lanczos,format=rgba[cam]",
            f"[{mask_idx}:v]format=gray,scale={CARD[2]}:{CARD[3]}[m]",
            "[cam][m]alphamerge[camc]",
            f"{src_label}[{frame_idx}:v]overlay=0:0:format=auto[fr]",
            f"[fr][camc]overlay={CARD[0]}:{CARD[1]}:format=auto[withcard]"]


def compose_window(edit: Path, d: dict, w: dict, plates: dict, cut: Path | None, preview: bool) -> Path:
    out = edit / "compose" / "windows" / f"w_{w['i']:03d}.mp4"
    out.parent.mkdir(parents=True, exist_ok=True)
    n = w["f1"] - w["f0"]
    base = edit / "base.mp4"
    ss = f"{w['start']:.4f}"
    ins: list[str] = []
    fc: list[str] = []
    if w["layout"] == "talk":
        ins += ["-ss", ss, "-i", str(base)]
        cur = "[0:v]setpts=PTS-STARTPTS[bg]"
        fc.append(cur)
        label = "[bg]"
        nxt = 1
    elif w["layout"] == "screen":
        vp = edit / "compose" / "windows" / f"vp_{w['i']:03d}.mp4"
        render_viewport(edit, d, w, cut, vp)
        ins += ["-loop", "1", "-framerate", str(FPS), "-i", str(plates["screen"]), "-i", str(vp),
                "-ss", ss, "-i", str(base), "-loop", "1", "-framerate", str(FPS), "-i", str(plates["mask"]),
                "-loop", "1", "-framerate", str(FPS), "-i", str(plates["frame"])]
        fc.append(f"[0:v][1:v]overlay={VIEW[0]}:{VIEW[1]}:eof_action=repeat[scr]")
        fc += card_chain(d, "[scr]", 2, 3, 4, n)
        label = "[withcard]"
        nxt = 5
    else:  # scene
        r = edit / "animations" / w["ref"] / "render.mp4"
        if not r.exists():
            sys.exit(f"scene {w['ref']} has no render.mp4 — board.py render first")
        ins += ["-i", str(r), "-ss", ss, "-i", str(base), "-loop", "1", "-framerate", str(FPS), "-i", str(plates["mask"]),
                "-loop", "1", "-framerate", str(FPS), "-i", str(plates["frame"])]
        fc.append("[0:v]setpts=PTS-STARTPTS,fps=30[sc]")
        fc += card_chain(d, "[sc]", 1, 2, 3, n)
        label = "[withcard]"
        nxt = 4
    for o in overlays_in(d, edit, w):
        ins += ["-i", str(o["path"])]
        fc.append(f"[{nxt}:v]setpts=PTS-STARTPTS+{o['offset']:.4f}/TB[o{nxt}]")
        fc.append(f"{label}[o{nxt}]overlay=0:0:eof_action=pass:format=auto[l{nxt}]")
        label = f"[l{nxt}]"
        nxt += 1
    fc.append(f"{label}format=yuv420p[vout]")
    sh(["ffmpeg", "-y", "-v", "error", *ins, "-filter_complex", ";".join(fc), "-map", "[vout]", "-frames:v", str(n),
        "-r", str(FPS), "-c:v", "libx264", "-crf", "23" if preview else "16", "-preset", "veryfast" if preview else "medium",
        "-pix_fmt", "yuv420p", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", "-an", str(out)],
       f"window {w['i']} ({w['layout']})")
    got = frames_of(out)
    if got != n:
        sys.exit(f"window {w['i']}: {got} frames, expected {n}")
    return out


# ------------------------------------------------------------------ sound
def sfx_cues(d: dict, edit: Path) -> list[tuple[float, Path]]:
    cues = []
    for s in d["scenes"]["scenes"]:
        b = edit / "animations" / s["id"] / "beats.json"
        if not b.exists():
            continue
        for beat in json.loads(b.read_text()):
            if not beat.get("role"):
                continue          # the 30 % rule: only hook / structural beats sound
            f = REEL_SFX / f"v6_{beat.get('tag', 'paper')}.wav"
            if f.exists():
                cues.append((s["start"] + float(beat["t"]) - 0.02, f))
    return cues


DUCK = "sidechaincompress=threshold=0.03:ratio=6:attack=20:release=400"


def lufs_of(cmd: list[str]) -> float:
    """integrated loudness from an ffmpeg run whose filter graph ends in ebur128"""
    r = subprocess.run(["ffmpeg", "-nostdin", "-nostats", "-hide_banner", *cmd, "-f", "null", "-"], capture_output=True, text=True)
    vals = [float(l.split()[1]) for l in r.stderr.splitlines() if l.strip().startswith("I:") and "LUFS" in l]
    if not vals:
        sys.exit(f"loudness measurement failed:\n{r.stderr[-800:]}")
    return vals[-1]


def music_gain(edit: Path, d: dict, bed_in: list[str], dur: str) -> float:
    """dB to add to the bed (on top of -24 dB) so the ducked bed sits music_under_voice_db under the voice"""
    lay = d["layout"]
    if "music_gain_db" in lay:
        return float(lay["music_gain_db"])
    under = float(lay.get("music_under_voice_db", 5))
    base = str(edit / "base.mp4")
    voice = lufs_of(["-i", base, "-filter_complex", f"[0:a]aresample=48000,atrim=end={dur},ebur128[o]", "-map", "[o]"])
    ducked = lufs_of(["-i", base, *bed_in, "-filter_complex",
                      f"[0:a]aresample=48000,atrim=end={dur}[vk];"
                      f"[1:a]aresample=48000,aformat=sample_fmts=fltp,atrim=end={dur},volume=-24dB[m];"
                      f"[m][vk]{DUCK}[dk];[dk]ebur128[o]", "-map", "[o]"])
    gain = max(-20.0, min(40.0, voice - under - ducked))
    print(f"  music: voice {voice:.1f} LUFS, ducked bed {ducked:.1f} → gain {gain:+.1f} dB (bed {under:g} dB under the voice)")
    return gain


def mix(edit: Path, d: dict, picture: Path, out: Path, preview: bool) -> None:
    base = edit / "base.mp4"
    cues = sfx_cues(d, edit)
    music = d["layout"].get("music")
    dur_s = d["total"] / FPS
    dur = f"{dur_s:.6f}"                         # the picture's length: every audio input is cut to it
    ins = ["-i", str(picture), "-i", str(base)]
    fc = [f"[1:a]aresample=48000,atrim=end={dur}[voice]"]
    mixes = ["[vmix]" if music else "[voice]"]
    k = 2
    for t, f in cues:
        ins += ["-i", str(f)]
        ms = max(0, int(t * 1000))
        fc.append(f"[{k}:a]aresample=48000,volume={SFX_GAIN}dB,adelay={ms}|{ms}[s{k}]")
        mixes.append(f"[s{k}]")
        k += 1
    if music:
        # No -stream_loop: with the bed as a looped input (with or without -t) ffmpeg 6.0 wrote a complete
        # final_mix.mov and then hung forever at 0 % CPU (all demuxer threads gone, main thread waiting on a queue).
        # A bed shorter than the picture is repeated with the concat demuxer instead; atrim ends it with the voice.
        bed = edit / music
        bed_s = media_duration(bed)
        if bed_s and bed_s < dur_s:
            lst = edit / "compose" / "music_loop.txt"
            lst.write_text(("file '" + str(bed.resolve()).replace("'", "'\\''") + "'\n") * math.ceil(dur_s / bed_s))
            bed_in = ["-f", "concat", "-safe", "0", "-i", str(lst)]
        else:
            bed_in = ["-i", str(bed)]
        gain = music_gain(edit, d, bed_in, dur)
        ins += bed_in
        fc.append(f"[{k}:a]aresample=48000,aformat=sample_fmts=fltp,atrim=end={dur},volume={-24 + gain:.2f}dB[mus]")
        fc.append("[voice]asplit=2[vmix][vkey]")
        fc.append(f"[mus][vkey]{DUCK}[duck]")
        mixes.append("[duck]")
    fc.append("".join(mixes) + f"amix=inputs={len(mixes)}:normalize=0:duration=first[a]")
    tmp = out.with_name(out.stem + "_mix.mp4")
    sh(["ffmpeg", "-nostdin", "-y", "-v", "error", *ins, "-filter_complex", ";".join(fc), "-map", "0:v:0", "-map", "[a]",
        "-c:v", "copy", "-c:a", "pcm_s16le", "-t", dur, tmp.with_suffix(".mov").as_posix()], "mix")
    tmp = tmp.with_suffix(".mov")
    sys.path.insert(0, str(REEL_HELPERS))
    import render as reel_render  # noqa: E402  (adnaan-reel: two-pass loudnorm → limiter → AAC, -14 LUFS)
    reel_render.apply_loudnorm_two_pass(tmp, out, preview=preview)
    tmp.unlink(missing_ok=True)
    lufs, tp = reel_render.loudness_report(out)
    print(f"  loudness: {lufs} LUFS, true peak {tp} dBTP, {len(cues)} SFX cues{', music bed ducked' if music else ''}")


# ------------------------------------------------------------------ commands
def cmd_plan(edit: Path) -> None:
    d = load(edit)
    for w in windows(d):
        ov = ", ".join(o["id"] for o in overlays_in(d, edit, w))
        print(f"{w['i']:3d}  {w['start']:8.2f} → {w['end']:8.2f}  ({(w['f1'] - w['f0']) / FPS:6.2f}s)  {w['layout']:7s} {w['ref'] or '':18}{('  + ' + ov) if ov else ''}")
    print(f"total {d['total']} frames = {d['total'] / FPS:.2f}s, theme {d['theme']}")


def cmd_render(edit: Path, out: Path, preview: bool, only: int | None) -> None:
    d = load(edit)
    ws = windows(d)
    plates = make_plates(edit, d["theme"])
    cut = screen_cut(edit, d["tl"]) if any(w["layout"] == "screen" for w in ws) else None
    paths = []
    for w in ws:
        if only is not None and w["i"] != only:
            continue
        print(f"  window {w['i']:3d} {w['layout']:6s} {w['start']:7.2f}–{w['end']:7.2f}")
        paths.append(compose_window(edit, d, w, plates, cut, preview))
    if only is not None:
        print("→", paths[0])
        return
    lst = edit / "compose" / "windows.txt"
    lst.write_text("".join(f"file '{p}'\n" for p in paths))
    picture = edit / "compose" / "picture.mp4"
    sh(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(picture)], "concat")
    if frames_of(picture) != d["total"]:
        sys.exit(f"picture has {frames_of(picture)} frames, base has {d['total']}")
    mix(edit, d, picture, out, preview)
    print("→", out)


def cmd_where(edit: Path, t: float, sx: float, sy: float) -> None:
    d = load(edit)
    w = next((w for w in windows(d) if w["start"] <= t < w["end"]), None)
    if not w or w["layout"] != "screen":
        sys.exit(f"{t}s is not in a screen window")
    px, py = camera_for(d, w).point(out_to_src(d["tl"], t), sx, sy)
    print(f"frame px: {VIEW[0] + px:.0f}, {VIEW[1] + py:.0f}   (window {w['i']}, source t {out_to_src(d['tl'], t):.2f}s)")


def cmd_sheet(edit: Path, video: Path) -> None:
    d = load(edit)
    times = []
    for w in windows(d):
        times += [max(0, w["f0"] - 2), w["f0"], w["f0"] + 2, (w["f0"] + w["f1"]) // 2]
    times = sorted(set(t for t in times if t < d["total"]))[:64]
    sel = "+".join(f"eq(n\\,{t})" for t in times)
    out = edit / "verify" / "compose_sheet.jpg"
    out.parent.mkdir(exist_ok=True)
    cols = 6
    sh(["ffmpeg", "-y", "-v", "error", "-i", str(video), "-vf",
        f"select='{sel}',scale=480:-2,drawtext=text='%{{n}}':x=6:y=6:fontsize=18:fontcolor=yellow:box=1:boxcolor=black@0.6,"
        f"tile={cols}x{(len(times) + cols - 1) // cols}:padding=4", "-frames:v", "1", "-fps_mode", "vfr", str(out)], "sheet")
    print("→", out, f"({len(times)} frames: 2 before / on / 2 after each window start + each middle)")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["plan", "render", "where", "sheet"])
    ap.add_argument("args", nargs="*")
    ap.add_argument("--edit-dir", required=True, type=Path)
    ap.add_argument("-o", "--output", type=Path)
    ap.add_argument("--preview", action="store_true")
    ap.add_argument("--only-window", type=int)
    a = ap.parse_intermixed_args()
    edit = a.edit_dir.resolve()
    if a.cmd == "plan":
        cmd_plan(edit)
    elif a.cmd == "render":
        cmd_render(edit, (a.output or edit / "final.mp4").resolve(), a.preview, a.only_window)
    elif a.cmd == "where":
        cmd_where(edit, float(a.args[0]), float(a.args[1]), float(a.args[2]))
    else:
        cmd_sheet(edit, Path(a.args[0]))


if __name__ == "__main__":
    main()
