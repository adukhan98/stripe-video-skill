"""Inserts: clips that carry their OWN audio (a before/after of a reel, a product demo) spliced into the composite.

compose.py lays scenes under his voice; it cannot pause the voice for a clip with its own sound. So an insert is built
as a 16:9 board clip (brand paper + 64 px grid + vignette, the clip in a white phone frame or a window, one label he
says or the beat table approved) and spliced into final_raw.mp4 at a frame where he has stopped speaking. Everything
after the splice moves later by the insert's length, so the SRT and chapters are shifted the same way.

    python helpers/inserts.py clip   --edit-dir E --src reel.mp4 --label before [--accent] [--dur 8.5] [--frame phone|window]
    python helpers/inserts.py splice --edit-dir E final_raw.mp4 final.mp4 --at 7449:inserts/board_before.mp4 --at 7771:…
    python helpers/inserts.py shift  --edit-dir E --at 7449:8.5 --at 7771:8.5      # deliver/captions.srt + chapters.txt

Pick each splice frame from the word times (transcripts/CAM.json mapped through timeline.json): after the last word of
the line that introduces the clip, and — if a talk caption is on screen — just before the next phrase's caption fades
in (else the old caption shows for a few frames after the clip). Check frames on both sides of every splice.
"""
import argparse
import json
import math
import re
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

SKILL = Path(__file__).resolve().parent.parent
FONT = SKILL / "assets" / "fonts" / "InterTight-Variable.ttf"
FPS = 30
W, H = 1920, 1080


def hexrgb(h, a=255):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) + (a,)


def brand_colors(edit: Path) -> dict:
    p = edit / "brand" / "brand.json"
    if not p.exists():
        p = SKILL / "brand" / "stripe.json"
    return {k: v["hex"] for k, v in json.loads(p.read_text())["colors"].items()}


def plate(edit: Path, label: str, accent: bool, box: tuple, rad: int, bezel: int) -> Path:
    C = brand_colors(edit)
    im = Image.new("RGBA", (W, H), hexrgb(C["background"]))
    grid = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(grid)
    for x in range(0, W, 64):
        gd.rectangle([x, 0, x + 1, H], fill=hexrgb(C["deep"], 13))
    for y in range(0, H, 64):
        gd.rectangle([0, y, W, y + 1], fill=hexrgb(C["deep"], 13))
    im = Image.alpha_composite(im, grid)
    vig = Image.new("L", (W // 8, H // 8))  # transparent to 34 %, deep at .30 in the corners (brand.css --vignette-strong)
    px = vig.load()
    for y in range(H // 8):
        for x in range(W // 8):
            r = math.hypot((x * 8 - W / 2) / (W / 2), (y * 8 - H * .42) / (H / 2)) / math.sqrt(2)
            px[x, y] = int(255 * .30 * max(0, (r - .34) / .66) ** 1.3)
    im = Image.composite(Image.new("RGBA", (W, H), hexrgb(C["deep"])), im, vig.resize((W, H), Image.BILINEAR))
    x, y, w, h = box
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([x - bezel, y - bezel + 26, x + w + bezel, y + h + bezel + 26], rad + bezel,
                                         fill=hexrgb(C["deep"], 70))
    im = Image.alpha_composite(im, sh.filter(ImageFilter.GaussianBlur(28)))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([x - bezel, y - bezel, x + w + bezel, y + h + bezel], rad + bezel, fill=hexrgb(C["card"]))
    if label:
        f = ImageFont.truetype(str(FONT), 168)
        f.set_variation_by_axes([900])
        d.text((x + w + bezel + 120, H // 2), label + ".", font=f, fill=hexrgb(C["primary"] if accent else C["deep"]), anchor="lm")
    out = edit / "inserts" / f"plate_{label or 'clip'}.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    im.convert("RGB").save(out)
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], rad, fill=255)
    m.save(edit / "inserts" / "clip_mask.png")
    return out


def clip(edit: Path, src: Path, label: str, accent: bool, dur: float, frame: str, out: Path | None) -> Path:
    box, rad, bezel = ((560, 108, 486, 864), 54, 14) if frame == "phone" else ((150, 170, 1180, 664), 24, 10)
    p = plate(edit, label, accent, box, rad, bezel)
    x, y, w, h = box
    out = out or edit / "inserts" / f"board_{label or src.stem}.mp4"
    n = int(round(dur * FPS))
    fc = (f"[1:v]fps={FPS},scale={w}:{h}:force_original_aspect_ratio=increase:flags=lanczos,crop={w}:{h},format=rgba[r];"
          f"[2:v]format=gray[m];[r][m]alphamerge[rm];[0:v][rm]overlay={x}:{y}:format=auto,format=yuv420p,trim=end_frame={n}[v];"
          f"[1:a]atrim=0:{dur},aresample=48000,afade=t=in:d=0.03,afade=t=out:st={dur - 0.03}:d=0.03[a]")
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-loop", "1", "-framerate", str(FPS), "-i", str(p),
                    "-i", str(src), "-loop", "1", "-i", str(edit / "inserts" / "clip_mask.png"), "-filter_complex", fc,
                    "-map", "[v]", "-map", "[a]", "-t", str(dur), "-c:v", "libx264", "-crf", "16", "-c:a", "aac",
                    "-b:a", "256k", "-ar", "48000", str(out)], check=True)
    print("→", out)
    return out


def probe_frames(p: Path) -> int:
    return int(subprocess.run(["ffprobe", "-v", "error", "-count_packets", "-select_streams", "v:0", "-show_entries",
                               "stream=nb_read_packets", "-of", "csv=p=0", str(p)], capture_output=True, text=True).stdout)


def splice(edit: Path, src: Path, out: Path, at: list[tuple[int, Path]]) -> None:
    at = sorted(at)
    edges = [0] + [f for f, _ in at] + [probe_frames(src)]
    inputs, fc, parts = ["-i", str(src)], [], []
    for _, c in at:
        inputs += ["-i", str(c if c.is_absolute() else edit / c)]
    for k in range(len(edges) - 1):
        a, b = edges[k], edges[k + 1]
        t0, t1 = a / FPS, b / FPS
        fc.append(f"[0:v]trim=start_frame={a}:end_frame={b},setpts=PTS-STARTPTS[v{k}];"
                  f"[0:a]atrim={t0}:{t1},asetpts=PTS-STARTPTS,afade=t=in:d=0.03,afade=t=out:st={t1 - t0 - 0.03}:d=0.03[a{k}]")
        parts.append(f"[v{k}][a{k}]")
        if k < len(at):  # trim each insert to its exact frame length: AAC padding would push everything after ~12 ms late
            n = probe_frames(Path(inputs[2 * (k + 1) + 1]))
            fc.append(f"[{k + 1}:v]trim=end_frame={n},setpts=PTS-STARTPTS[iv{k}];"
                      f"[{k + 1}:a]atrim=0:{n / FPS},asetpts=PTS-STARTPTS[ia{k}]")
            parts.append(f"[iv{k}][ia{k}]")
    fc.append("".join(parts) + f"concat=n={len(parts)}:v=1:a=1[v][ac];[ac]alimiter=limit=0.84:level=false:attack=1:release=50[a]")
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(fc), "-map", "[v]",
                    "-map", "[a]", "-c:v", "libx264", "-crf", "17", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "256k",
                    "-ar", "48000", "-movflags", "+faststart", str(out)], check=True)
    print(f"→ {out}: {probe_frames(out)} frames; inserts at {[round(f / FPS, 3) for f, _ in at]}")
    print("  check: loudness (ebur128), audio vs base after each splice, frames on both sides of every splice")


def shift(edit: Path, at: list[tuple[int, float]]) -> None:
    S = [(f / FPS, d) for f, d in sorted(at)]
    sh = lambda t: t + sum(d for s, d in S if t >= s - 1e-6)
    parse = lambda s: (lambda h, m, r: int(h) * 3600 + int(m) * 60 + float(r.replace(",", ".")))(*s.split(":"))

    def fmt(t):
        ms = round(t * 1000)
        h, ms = divmod(ms, 3600000)
        m, ms = divmod(ms, 60000)
        s, ms = divmod(ms, 1000)
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
    srt = edit / "deliver" / "captions.srt"
    txt = srt.read_text()
    for a, b in re.findall(r"(\S+) --> (\S+)", txt):
        if any(parse(a) < s < parse(b) for s, _ in S):
            print(f"  ! cue {a} → {b} spans a splice")
    srt.write_text(re.sub(r"(\S+) --> (\S+)", lambda m: f"{fmt(sh(parse(m.group(1))))} --> "
                          f"{fmt(sh(parse(m.group(1))) + parse(m.group(2)) - parse(m.group(1)))}", txt))
    lay = json.loads((edit / "layout.json").read_text())
    ch = sorted(lay.get("chapters") or [], key=lambda c: c.get("start", c.get("t", 0)))
    clock = lambda t: f"{int(t) // 60}:{int(t) % 60:02d}"
    lines = [f"{clock(0 if i == 0 else sh(c.get('start', c.get('t', 0))))} {c['title']}" for i, c in enumerate(ch)]
    (edit / "deliver" / "chapters.txt").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    print(f"→ {srt} and chapters.txt shifted")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["clip", "splice", "shift"])
    ap.add_argument("files", nargs="*", type=Path)
    ap.add_argument("--edit-dir", type=Path, required=True)
    ap.add_argument("--src", type=Path)
    ap.add_argument("--label", default="")
    ap.add_argument("--accent", action="store_true", help="label in the brand accent (e.g. 'after')")
    ap.add_argument("--dur", type=float, default=8.5)
    ap.add_argument("--frame", choices=["phone", "window"], default="phone")
    ap.add_argument("-o", type=Path)
    ap.add_argument("--at", action="append", default=[], help="FRAME:clip.mp4 (splice) or FRAME:seconds (shift)")
    a = ap.parse_intermixed_args()
    edit = a.edit_dir.resolve()
    if a.cmd == "clip":
        clip(edit, a.src, a.label, a.accent, a.dur, a.frame, a.o)
    elif a.cmd == "splice":
        splice(edit, a.files[0], a.files[1], [(int(x.split(":")[0]), Path(x.split(":", 1)[1])) for x in a.at])
    else:
        shift(edit, [(int(x.split(":")[0]), float(x.split(":")[1])) for x in a.at])


if __name__ == "__main__":
    main()
