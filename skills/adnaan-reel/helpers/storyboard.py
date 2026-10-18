"""Storyboard: the whole video, beat by beat, approved by the user BEFORE anything is built.

Reads <edit>/storyboard.json and writes
  <edit>/storyboard/storyboard.html      the board to review (self-contained, open it in a browser)
  <edit>/storyboard/storyboard_vN.html   a copy per version, so earlier rounds stay comparable
  <edit>/storyboard/storyboard.jpg       the same board as one image (for the Read tool / chat)
  <edit>/storyboard/frames/<beat>.jpg    the thumbnail of each beat
and prints a summary: running time vs target, assets still to find, beats without a picture.

storyboard.json:
  {
    "title": "Why every lab wants one agent", "version": 1,
    "format": {"width": 1080, "height": 1920, "fps": 30},
    "style": "creator",                   # brand | creator | mixed  (video-edit preset; adnaan-reel uses its own scene grammar)
    "target_duration": 45,
    "sources": {"A": "/abs/IMG_2298.MOV"},   # paths absolute or relative to storyboard.json
    "beats": [
      {"id": "B01", "section": "HOOK",
       "source": "A", "start": 1.54, "end": 4.20,      # the spoken line under this beat (source seconds)
       "vo": "If you're wondering why Muse is all over your Instagram…",
       "visual": "media",                   # a-roll | graphic | clip | broll | screenshot | media | split | text
       "layout": "split",                   # full | top | split | full_pip | lower_third | corner | none
       "media": "raw/instagram_scroll.mp4", # split / full_pip: the recording or screenshot shown
       "description": "Screen recording of the Instagram feed on top, speaker below, 'Muse' ads circled.",
       "motion": "Hard cut into the split; circle draws on 'Muse' with 3-frame anticipation.",
       "audio": "whoosh on the layout change; bed starts",
       "assets": [{"what": "Muse launch film", "status": "find", "rights": "commentary",
                   "source": "https://…"}],      # status: have | find | need (from the user) | make
       "frame": {"source": "A", "t": 2.0},  # or "frame": "path/to/style_frame.png"; omit → text card
       "feedback": ""}                       # the user's notes on this beat, kept across versions
    ]
  }
A beat with no source/start/end gives its length as "duration" (seconds).
A split / full_pip beat with "media" (an image, or a video at "media_t" seconds) and no "frame" uses
that media as its thumbnail.

Usage:
    python helpers/storyboard.py --edit-dir <edit> [--storyboard <edit>/storyboard.json]
"""

from __future__ import annotations

import argparse
import base64
import html
import json
import subprocess
import sys
import textwrap
from pathlib import Path

VISUAL_COLOURS = {
    "a-roll": "#6B7280", "graphic": "#7C3AED", "clip": "#DC2626", "broll": "#059669",
    "screenshot": "#2563EB", "split": "#D97706", "text": "#DB2777", "media": "#0891B2",
}
STYLES = ("brand", "creator", "mixed")
LAYOUTS = ("full", "top", "split", "full_pip", "lower_third", "corner", "none")
STATUS_COLOURS = {"have": "#059669", "make": "#2563EB", "find": "#D97706", "need": "#DC2626"}
SHEET_FONT = "/System/Library/Fonts/Helvetica.ttc"


def beat_duration(b: dict) -> float:
    if b.get("start") is not None and b.get("end") is not None:
        return max(0.0, float(b["end"]) - float(b["start"]))
    return float(b.get("duration") or 0.0)


def timecodes(beats: list[dict]) -> list[tuple[float, float]]:
    """Estimated output-timeline window of each beat (beats play back to back)."""
    out, t = [], 0.0
    for b in beats:
        d = beat_duration(b)
        out.append((t, t + d))
        t += d
    return out


def fmt_tc(t: float) -> str:
    return f"{int(t // 60)}:{t % 60:04.1f}"


def resolve(path: str, base: Path) -> Path:
    p = Path(path).expanduser()
    return p if p.is_absolute() else (base / p)


def extract_frame(src: Path, t: float, out: Path, w: int, h: int, focus_x: float = 0.5) -> bool:
    """One frame at t, cropped to the output aspect around focus_x, 360 px wide."""
    tw = 360
    th = int(round(tw * h / w / 2)) * 2
    vf = (f"crop='min(iw,ih*{w}/{h})':'min(ih,iw*{h}/{w})':"
          f"'(iw-min(iw,ih*{w}/{h}))*{focus_x}':'(ih-min(ih,iw*{h}/{w}))/2',scale={tw}:{th}")
    proc = subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{max(0.0, t):.3f}", "-i", str(src),
                           "-frames:v", "1", "-vf", vf, str(out)], capture_output=True, text=True)
    return proc.returncode == 0 and out.exists()


def beat_frame(b: dict, sb: dict, base: Path, frames_dir: Path) -> Path | None:
    fmt = sb.get("format") or {}
    w, h = int(fmt.get("width") or 1080), int(fmt.get("height") or 1920)
    spec = b.get("frame")
    if isinstance(spec, str):
        p = resolve(spec, base)
        return p if p.exists() else None
    if spec is None and b.get("media"):
        media = resolve(b["media"], base)
        if not media.exists():
            return None
        if media.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp"):
            return media
        out = frames_dir / f"{b['id']}.jpg"
        return out if extract_frame(media, float(b.get("media_t", 0)), out, w, h) else None
    if isinstance(spec, dict) and spec.get("source"):
        src_key, t = spec["source"], float(spec.get("t", 0))
    elif spec is None and b.get("source") and b.get("visual", "a-roll") in ("a-roll", "split") \
            and b.get("start") is not None:
        src_key, t = b["source"], (float(b["start"]) + float(b.get("end") or b["start"])) / 2
    else:
        return None
    src = (sb.get("sources") or {}).get(src_key)
    if not src:
        return None
    out = frames_dir / f"{b['id']}.jpg"
    ok = extract_frame(resolve(src, base), t, out, w, h, float((spec or {}).get("focus_x", 0.5))
                       if isinstance(spec, dict) else 0.5)
    return out if ok else None


def data_uri(p: Path) -> str:
    mime = "image/png" if p.suffix.lower() == ".png" else "image/jpeg"
    return f"data:{mime};base64,{base64.b64encode(p.read_bytes()).decode()}"


# -------- html ----------------------------------------------------------------------


def render_html(sb: dict, beats: list[dict], tcs: list[tuple[float, float]], frames: dict[str, Path | None]) -> str:
    fmt = sb.get("format") or {}
    w, h = int(fmt.get("width") or 1080), int(fmt.get("height") or 1920)
    total = tcs[-1][1] if tcs else 0.0
    e = html.escape
    cards = []
    for b, (t0, t1) in zip(beats, tcs):
        vis = b.get("visual", "a-roll")
        img = frames.get(b["id"])
        pic = (f'<img src="{data_uri(img)}" alt="">' if img else
               f'<div class="ph"><span>{e(vis.upper())}</span><p>{e(b.get("description", ""))}</p></div>')
        assets = "".join(
            f'<li><b style="background:{STATUS_COLOURS.get(a.get("status", "have"), "#6B7280")}">'
            f'{e(a.get("status", "have"))}</b> {e(a.get("what", ""))}'
            + (f' <i>({e(a["rights"])})</i>' if a.get("rights") else "") + "</li>"
            for a in b.get("assets") or [])
        rows = [("VO", b.get("vo")), ("Picture", b.get("description")), ("Media", b.get("media")),
                ("Motion", b.get("motion")), ("Sound", b.get("audio"))]
        body = "".join(f'<dt>{k}</dt><dd>{e(v)}</dd>' for k, v in rows if v)
        fb = f'<div class="fb">Your note: {e(b["feedback"])}</div>' if b.get("feedback") else ""
        cards.append(f"""<article>
  <div class="frame" style="aspect-ratio:{w}/{h}">{pic}</div>
  <header><span class="id">{e(b['id'])}</span><span class="sec">{e(b.get('section', ''))}</span>
    <span class="tc">{fmt_tc(t0)}–{fmt_tc(t1)} · {t1 - t0:.1f}s</span></header>
  <div class="tags"><span style="background:{VISUAL_COLOURS.get(vis, '#6B7280')}">{e(vis)}</span>
    {f'<span class="ghost">{e(b["layout"])}</span>' if b.get('layout') and b['layout'] != 'none' else ''}</div>
  <dl>{body}</dl>{f'<ul>{assets}</ul>' if assets else ''}{fb}
</article>""")
    target = sb.get("target_duration")
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(sb.get('title', 'Storyboard'))}</title>
<style>
:root{{--bg:#F6F5F1;--card:#FFFFFF;--ink:#16161A;--mute:#6B6B72;--line:#E4E2DC}}
@media (prefers-color-scheme:dark){{:root{{--bg:#141416;--card:#1D1D21;--ink:#F2F1ED;--mute:#9A9AA2;--line:#2E2E34}}}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);
font:14px/1.45 -apple-system,BlinkMacSystemFont,"Inter",sans-serif;padding:24px 16px}}
h1{{font-size:22px;margin:0 0 4px}}.meta{{color:var(--mute);margin-bottom:20px}}
main{{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:16px}}
article{{background:var(--card);border:1px solid var(--line);border-radius:12px;overflow:hidden}}
.frame{{background:#000;width:100%;max-height:420px;display:flex;align-items:center;justify-content:center;overflow:hidden}}
.frame img{{width:100%;height:100%;object-fit:cover;display:block}}
.ph{{color:#fff;padding:16px;text-align:center}}.ph span{{font-weight:700;letter-spacing:.08em;font-size:12px;opacity:.7}}
.ph p{{margin:8px 0 0;font-size:13px}}
header{{display:flex;gap:8px;align-items:baseline;padding:10px 12px 0}}.id{{font-weight:700}}
.sec{{color:var(--mute);font-size:12px;text-transform:uppercase;letter-spacing:.06em}}
.tc{{margin-left:auto;color:var(--mute);font-variant-numeric:tabular-nums;font-size:12px}}
.tags{{padding:6px 12px 0;display:flex;gap:6px}}.tags span{{color:#fff;border-radius:99px;padding:1px 8px;font-size:11px}}
.tags .ghost{{background:transparent;color:var(--mute);border:1px solid var(--line)}}
dl{{margin:8px 12px;display:grid;grid-template-columns:auto 1fr;gap:4px 10px}}
dt{{color:var(--mute);font-size:12px}}dd{{margin:0}}
ul{{list-style:none;margin:0 12px 10px;padding:0}}li{{font-size:12px;margin:3px 0}}
li b{{color:#fff;border-radius:4px;padding:0 5px;font-weight:600;margin-right:4px}}
.fb{{margin:0 12px 12px;padding:6px 8px;border-left:3px solid #D97706;font-size:12px;color:var(--mute)}}
</style></head><body>
<h1>{e(sb.get('title', 'Storyboard'))} <span style="color:var(--mute);font-weight:400">v{e(str(sb.get('version', 1)))}</span></h1>
<div class="meta">{w}×{h} · style: {e(sb.get('style', 'brand'))} · {len(beats)} beats · ~{total:.1f}s
{f' (target {target}s)' if target else ''}{(' · ' + e(sb['notes'])) if sb.get('notes') else ''}</div>
<main>{''.join(cards)}</main>
</body></html>
"""


# -------- contact sheet ----------------------------------------------------------------


def render_sheet(sb: dict, beats: list[dict], tcs: list[tuple[float, float]], frames: dict[str, Path | None],
                 out: Path) -> Path | None:
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        return None
    fmt = sb.get("format") or {}
    w, h = int(fmt.get("width") or 1080), int(fmt.get("height") or 1920)
    cw = 300
    ih = min(int(cw * h / w), 420)
    text_h = 230
    cols = min(5, max(1, len(beats)))
    rows = (len(beats) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (cw + 16) + 16, rows * (ih + text_h + 16) + 16), (246, 245, 241))
    d = ImageDraw.Draw(sheet)
    try:
        f_b = ImageFont.truetype(SHEET_FONT, 18)
        f_s = ImageFont.truetype(SHEET_FONT, 14)
    except OSError:
        f_b = f_s = ImageFont.load_default()
    for i, (b, (t0, t1)) in enumerate(zip(beats, tcs)):
        x = 16 + (i % cols) * (cw + 16)
        y = 16 + (i // cols) * (ih + text_h + 16)
        d.rectangle((x, y, x + cw, y + ih + text_h), fill=(255, 255, 255), outline=(228, 226, 220))
        img = frames.get(b["id"])
        if img:
            with Image.open(img) as im:
                im = im.convert("RGB")
                scale = max(cw / im.width, ih / im.height)
                im = im.resize((int(im.width * scale) + 1, int(im.height * scale) + 1))
                left, top = (im.width - cw) // 2, (im.height - ih) // 2
                sheet.paste(im.crop((left, top, left + cw, top + ih)), (x, y))
        else:
            d.rectangle((x, y, x + cw, y + ih), fill=(22, 22, 26))
            vis = b.get("visual", "graphic").upper()
            d.text((x + 12, y + 12), vis, fill=(200, 200, 200), font=f_b)
            yy = y + 44
            for line in textwrap.wrap(b.get("description", ""), 34)[:12]:
                d.text((x + 12, yy), line, fill=(235, 235, 235), font=f_s)
                yy += 19
        colour = VISUAL_COLOURS.get(b.get("visual", "a-roll"), "#6B7280")
        d.rectangle((x, y + ih, x + cw, y + ih + 6), fill=colour)
        ty = y + ih + 12
        d.text((x + 10, ty), f"{b['id']}  {b.get('section', '')}", fill=(22, 22, 26), font=f_b)
        d.text((x + cw - 110, ty + 3), f"{fmt_tc(t0)} · {t1 - t0:.1f}s", fill=(107, 107, 114), font=f_s)
        ty += 26
        for label, val, n in (("VO", b.get("vo"), 3), ("", b.get("description") if img else None, 3),
                              ("Motion", b.get("motion"), 2), ("Sound", b.get("audio"), 1)):
            if not val:
                continue
            for j, line in enumerate(textwrap.wrap((f"{label}: " if label else "") + val, 38)[:n]):
                d.text((x + 10, ty), line, fill=(60, 60, 66), font=f_s)
                ty += 18
            ty += 3
        todo = [a for a in b.get("assets") or [] if a.get("status") in ("find", "need")]
        if todo:
            d.text((x + 10, y + ih + text_h - 22), f"needs: {', '.join(a.get('what', '') for a in todo)}"[:44],
                   fill=(217, 119, 6), font=f_s)
    sheet.save(out, quality=88)
    return out


# -------- main ---------------------------------------------------------------------------


def build(edit_dir: Path, sb_path: Path) -> dict:
    sb = json.loads(sb_path.read_text())
    beats = sb.get("beats") or []
    if not beats:
        sys.exit(f"{sb_path} has no beats")
    ids = [b.get("id") for b in beats]
    if None in ids or len(set(ids)) != len(ids):
        sys.exit("every beat needs a unique id")
    if sb.get("style") and sb["style"] not in STYLES:
        print(f"  WARNING: style {sb['style']!r} is not one of {' | '.join(STYLES)}")
    bad = [b["id"] for b in beats if b.get("layout") and b["layout"] not in LAYOUTS]
    if bad:
        print(f"  WARNING: unknown layout on {', '.join(bad)} (expected {' | '.join(LAYOUTS)})")
    out_dir = edit_dir / "storyboard"
    frames_dir = out_dir / "frames"
    frames_dir.mkdir(parents=True, exist_ok=True)
    base = sb_path.parent
    tcs = timecodes(beats)
    frames = {b["id"]: beat_frame(b, sb, base, frames_dir) for b in beats}

    page = render_html(sb, beats, tcs, frames)
    (out_dir / "storyboard.html").write_text(page)
    (out_dir / f"storyboard_v{sb.get('version', 1)}.html").write_text(page)
    sheet = render_sheet(sb, beats, tcs, frames, out_dir / "storyboard.jpg")

    total = tcs[-1][1]
    target = sb.get("target_duration")
    todo = [(b["id"], a) for b in beats for a in b.get("assets") or [] if a.get("status") in ("find", "need")]
    print(f"storyboard v{sb.get('version', 1)}: {len(beats)} beats, ~{total:.1f}s"
          + (f" (target {target}s, {total - float(target):+.1f}s)" if target else ""))
    mix: dict[str, int] = {}
    for b in beats:
        mix[b.get("visual", "a-roll")] = mix.get(b.get("visual", "a-roll"), 0) + 1
    print("  mix: " + ", ".join(f"{k} {v}" for k, v in sorted(mix.items(), key=lambda kv: -kv[1])))
    for (b, (t0, t1)) in zip(beats, tcs):
        print(f"  {b['id']:5s} {fmt_tc(t0):>6s} {t1 - t0:4.1f}s  {b.get('visual', 'a-roll'):10s} "
              f"{(b.get('description') or b.get('vo') or '')[:70]}")
    long_static = [b["id"] for b, (t0, t1) in zip(beats, tcs)
                   if b.get("visual", "a-roll") == "a-roll" and b.get("layout", "none") == "none"
                   and t1 - t0 > 8]
    if long_static:
        print(f"  WARNING: a-roll beats over 8 s with nothing changing: {', '.join(long_static)}")
    if todo:
        print("  assets to source: " + "; ".join(f"{bid} {a.get('what')} ({a.get('status')})" for bid, a in todo))
    missing = [b["id"] for b in beats if frames[b["id"]] is None]
    if missing:
        print(f"  text cards (no picture yet): {', '.join(missing)}")
    print(f"  → {out_dir / 'storyboard.html'}" + (f"\n  → {sheet}" if sheet else ""))
    return {"total": total, "todo": todo, "missing": missing}


def main() -> None:
    ap = argparse.ArgumentParser(description="Build the storyboard board from storyboard.json")
    ap.add_argument("--edit-dir", type=Path, required=True)
    ap.add_argument("--storyboard", type=Path, default=None, help="Default: <edit>/storyboard.json")
    args = ap.parse_args()
    edit_dir = args.edit_dir.resolve()
    build(edit_dir, (args.storyboard or edit_dir / "storyboard.json").resolve())


if __name__ == "__main__":
    main()
