#!/usr/bin/env python3
"""adnaan-reel scene pipeline: brand init, scene planning, speaker clips, scene EDL, safe previews, flash scan.

Every beat of an adnaan-reel is a full-screen opaque HyperFrames scene (slot layout "scene") laid back to
back over the locked cut. This helper does the mechanical parts around the slot agents:

  init-brand   copy the bundled fonts, write brand.json with an accent preset, copy style.md to
               animations/SHARED.md, run brand_kit.py build
  words        print every cut segment with its output start and words — pick scene boundaries here
  cut-speaker  per scene: cut base.mp4 to the scene window → hf/assets/speaker.mp4 (muted; the last
               scene is padded with a freeze for end_hold) and copy the scene's "assets" (--only ids: just those —
               e.g. after a mid-build cut fix that changed one scene's length)
  edl          write the scene EDL from edl.json + animations/slots.json + the renders: frame-snapped,
               12 ms pre-roll, each scene holds 0.1 s under the next (render.py's overlay sync otherwise
               leaks ONE raw footage frame at every boundary), last scene held to the end, no captions;
               every scene's animations/<id>/beats.json becomes timed audio[] cues from the house SFX kit
               ("scribble" beats = marker strokes: felt-tip variants rotated and trimmed to each stroke's dur)
  preview      one scene with its voice → verify/<id>_preview.mp4 (never touches base.mp4/timeline.json)
  flashcheck   scan a render for frames where raw footage shows instead of the paper world (with --edit-dir the
               windows of "fullscreen" / "demo" / v7 talk·talk_depth·chain·card scenes are expected and not counted)
  seam         continuity check: scene A's last frame beside scene B's first (a recurring drawing must not jump)
  runtime      re-install the shared runtime (paper.css/js + marker.css/js) into every scene's hf/
  rerender     re-render every scene in parallel (after a runtime/brand change — a whole-reel restyle in minutes),
               then verify each render's frame count against slot.json

Usage:
  scenes.py init-brand --edit-dir E [--look mint|paper] (mint = v7 house default) [--accent red|ocean|cobalt|terracotta|lilac|mustard|blush|olive|mint|#hex] (red = house default since v5) [--type grotesk|editorial] [--frame still.jpg]
  scenes.py words --edit-dir E [--edl edl.json]
  scenes.py cut-speaker --edit-dir E [--only v07_hookup]
  scenes.py edl --edit-dir E [--edl edl.json] [-o edl_scenes.json]
  scenes.py preview v03_genius --edit-dir E
  scenes.py flashcheck E/final.mp4
  scenes.py seam v04_funnel v05_free --edit-dir E
  scenes.py runtime --edit-dir E
  scenes.py rerender --edit-dir E [--jobs 4] [--only v03_inside,v07_adobe]
"""
from __future__ import annotations

import argparse
import colorsys
import json
import shutil
import subprocess
import sys
from pathlib import Path

HELPERS = Path(__file__).resolve().parent
SKILL_DIR = HELPERS.parent
sys.path.insert(0, str(HELPERS))

# accent presets: (primary, primary_dark, deep) — see assets/style/accent_options.jpg
ACCENTS = {
    "ocean": ("#2E9CCB", "#1F7EA8", "#0D2731"),
    "cobalt": ("#3D63F2", "#2A4AD0", "#0E1A3F"),
    "terracotta": ("#D9622B", "#B54C1C", "#2B1710"),
    "lilac": ("#8B7CF6", "#6F5FE0", "#211A3F"),
    "mustard": ("#D9A21B", "#B98712", "#262016"),
    "blush": ("#E0708F", "#C55574", "#3A1220"),
    "olive": ("#8FA83A", "#738A28", "#1E2412"),
    "red": ("#E5484D", "#C7353A", "#1A1A1A"),
    "mint": ("#74C69D", "#4FA77C", "#13261E"),
}
# v7 "mint" look (house default since reel-08, 2026-10-17): mint words/discs, deep mint small accents, charcoal ink discs.
MINT_LOOK = ("#7CC49E", "#2F8A63", "#2B2B2B")
MINT_TOKENS = """
/* ---- v7 "mint" look (init-brand --look mint) — v7.css / v7.js read these ---- */
:root {
  --brand-text: #232323;           /* charcoal ink for words */
  --mint-soft: #CFEAD9;            /* highlighter fill / soft panels */
  --mint-panel: #8FCBA8;           /* full-bleed mint panel (1–2 per reel) */
  --peach: #F2A07B;                /* DATA ONLY: charts, result bars, rolling numbers */
  --disc-shadow: 0 22px 36px -10px rgba(30, 30, 30, .38), 0 6px 12px -4px rgba(30, 30, 30, .22);
  --vignette-strong: radial-gradient(ellipse at 50% 42%, transparent 30%, rgba(60, 55, 50, .42) 100%);
}
"""
PAPER_CORNER_RGB = (207, 201, 196)   # 40x40 patch at (20,20) of a scene frame: paper under the vignette
FPS = 30
TYPE_SCALE = 0.94   # house kinetic-type size since v4 (reel-05: "a tiny bit smaller"); paper.js reads --type-scale
# beats.json tags → assets/sfx/<tag>.wav (ElevenLabs house kit) and their default gain under the voice
# v5: −3 dB vs v4 (reel-06 carried ~230 kit cues + marker strokes and needed it); scribble = felt-tip on paper (3 variants)
BEAT_GAIN_DB = {"pop": -22, "tick": -28, "impact": -18, "riser": -20, "whoosh": -22, "ping": -22, "ding": -19, "scribble": -27}
# v6 (reel-07, his SOP "the 30 % rule"): a LOW & WARM kit (assets/sfx/v6_<tag>.wav, ElevenLabs, low-passed at 5 kHz)
# and SPARSE cues — 1–2 punchy "hook" sounds in 0–4 s, then only "structural" beats (point 1/2/3, a mode switch,
# a screenshot/article sliding in). Gains put SFX ~16 dB under a voice that peaks near −2 dBFS (target −16…−22).
V6_GAIN_DB = {"stamp": -15, "thud": -15, "clunk": -16, "pop": -16, "paper": -18, "whoosh": -18}
V6_FROM_LEGACY = {"impact": "thud", "pop": "pop", "whoosh": "whoosh"}   # old tags an agent may still use
HOOK_WINDOW_S, HOOK_MAX = 4.0, 2
MATTE_TYPES = ("cutout", "talk_depth")   # scene types that get speaker_cut.webm (his background removed)
SCRIBBLE_FILES = ("scribble1.wav", "scribble2.wav", "scribble3.wav")   # rotated; trimmed to the stroke's "dur"
BEAT_LEAD = {"riser": 0.45}   # riser.wav peaks ~0.45 s in: a riser beat names the HIT time, the cue starts earlier


def _hex(rgb: tuple[float, float, float]) -> str:
    return "#" + "".join(f"{max(0, min(255, round(c * 255))):02X}" for c in rgb)


def accent_from_hex(h: str) -> tuple[str, str, str]:
    h = h.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    hh, ll, ss = colorsys.rgb_to_hls(r, g, b)
    dark = colorsys.hls_to_rgb(hh, max(0, ll * 0.8), ss)
    deep = colorsys.hls_to_rgb(hh, 0.12, min(1, ss * 0.6))
    return "#" + h.upper(), _hex(dark), _hex(deep)


def run(cmd: list[str], **kw) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, check=True, **kw)


def probe_duration(p: Path) -> float:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                         capture_output=True, text=True).stdout.strip()
    return float(out or 0)


def frame_count(p: Path) -> int:
    out = subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries",
                          "stream=nb_read_frames", "-of", "csv=p=0", str(p)], capture_output=True, text=True).stdout
    return int(out.strip().split(",")[0])


def seek_ts(start: float, fps: int = FPS) -> float:
    """Input -ss that lands exactly on the frame a scene starts on: the frame's own timestamp + 0.5 ms (ffmpeg returns the
    frame covering the -ss instant, so a start rounded DOWN — 41.3333 → 41.333 — gave the previous frame)."""
    return round(start * fps) / fps + 0.0005


def load_slots(edit_dir: Path) -> list[dict]:
    p = edit_dir / "animations" / "slots.json"
    if not p.exists():
        sys.exit(f"missing {p}")
    return json.loads(p.read_text())


# ---------------------------------------------------------------- init-brand
def cmd_init_brand(a: argparse.Namespace) -> None:
    e = a.edit_dir.resolve()
    fonts = e / "brand" / "fonts"
    fonts.mkdir(parents=True, exist_ok=True)
    # grotesk (default, v2): Inter Tight + Inter + Geist Mono; editorial (v1): Newsreader + Fraunces + Geist
    font_src = SKILL_DIR / "assets" / "fonts" / ("editorial" if a.type == "editorial" else "")
    for f in font_src.glob("*.ttf"):
        shutil.copy(f, fonts / f.name)
    acc = (a.accent or ("mint-look" if a.look == "mint" else "red")).lower()
    if acc == "mint-look":
        primary, dark, deep = MINT_LOOK
        name = "Mint"
    elif acc.startswith("#"):
        primary, dark, deep = accent_from_hex(acc)
        name = acc.upper()
    elif acc in ACCENTS:
        primary, dark, deep = ACCENTS[acc]
        name = acc.capitalize()
    else:
        sys.exit(f"unknown accent {a.accent!r}; presets: {', '.join(ACCENTS)} or #hex")
    tmpl = "brand_ocean_editorial.json" if a.type == "editorial" else "brand_ocean.json"
    brand = json.loads((SKILL_DIR / "templates" / tmpl).read_text())
    brand["name"] = f"adnaan-reel — {name} {a.type}"
    brand["look"] = a.look
    brand["colors"]["primary"].update(hex=primary, name=name)
    brand["colors"]["primary_dark"].update(hex=dark, name=f"{name} dark")
    brand["colors"]["deep"].update(hex=deep, name=f"{name} deep")
    (e / "brand" / "brand.json").write_text(json.dumps(brand, indent=2))
    anim = e / "animations"
    anim.mkdir(exist_ok=True)
    shared = anim / "SHARED.md"
    style = (SKILL_DIR / "references" / "style.md").read_text()
    if a.type == "editorial":
        style += ("\n\n## THIS PROJECT: editorial type variant\n\nUse Newsreader 600 + Fraunces 700 italic accent "
                  "+ Geist labels (reel-03 look) instead of Inter Tight/Inter; everything else in this file applies.\n")
    if a.look == "paper":
        style += ("\n\n## THIS PROJECT: the legacy PAPER look (init-brand --look paper)\n\nIgnore the v7 \"mint\" section at the "
                  "top: this reel uses the v6 red paper + hand-drawn marker look described below it (split band, marker layer, Caveat).\n")
    if a.look == "paper" and acc != "red":
        style = style.replace("| Token | Default (Red) | Role |", f"| Token | Default (Red) — THIS PROJECT: {name} {primary} / {dark} / {deep} | Role |")
    shared.write_text(style + "\n\n## Project specifics (edit per project)\n\n- Accent: "
                      f"{name} {primary} (dark {dark}, deep {deep}).\n- List / coins: (e.g. 5 items, coins 01–05) \n"
                      "- Speaker face position in the source: (e.g. face centre ~45% of frame height)\n")
    print(f"brand.json ({a.look} look, {name} {primary}/{dark}/{deep}), fonts → {fonts}, SHARED.md → {shared}")
    cmd = ["uv", "run", "--project", str(SKILL_DIR), str(HELPERS / "brand_kit.py"), "build", "--edit-dir", str(e),
           "--platform", a.platform]
    if a.frame:
        cmd += ["--frame", str(a.frame)]
    run(cmd)
    css = e / "brand" / "brand.css"
    if css.exists() and "--type-scale" not in css.read_text():
        with css.open("a") as f:
            f.write(f"\n:root {{ --type-scale: {a.type_scale}; }} /* kinetic type size (paper.js); nudge per reel */\n")
        print(f"brand.css: --type-scale {a.type_scale}")
    if a.look == "mint" and css.exists() and "--vignette-strong" not in css.read_text():
        with css.open("a") as f:
            f.write(MINT_TOKENS)
        print("brand.css: v7 mint tokens")


# ---------------------------------------------------------------- words
def cmd_words(a: argparse.Namespace) -> None:
    from captions import output_words
    e = a.edit_dir.resolve()
    edl = json.loads((e / a.edl).read_text())
    tl = json.loads((e / "timeline.json").read_text())
    words = output_words(edl, e)
    segs = tl["segments"]
    for i, s in enumerate(segs):
        o0 = s["out_start"]
        o1 = segs[i + 1]["out_start"] if i + 1 < len(segs) else tl["total"]
        ws = [w for w in words if o0 - 0.02 <= w["start"] < o1 - 0.02]
        line = " ".join(f"{w['text']}@{w['start']:.2f}" for w in ws)
        print(f"[{i:02d}] out {o0:7.3f}–{o1:7.3f} (frame {round(o0 * FPS):5d})  {line}")
    print(f"total {tl['total']:.3f} s; end_hold {edl.get('end_hold', 0)} s → reel {tl['total'] + float(edl.get('end_hold', 0)):.3f} s")


# ---------------------------------------------------------------- cut-speaker
def cmd_cut_speaker(a: argparse.Namespace) -> None:
    e = a.edit_dir.resolve()
    base = e / "base.mp4"
    if not base.exists():
        sys.exit("render the base first: render.py edl.json -o edit/base.mp4 --base-only")
    base_d = probe_duration(base)
    only = set(a.only.split(",")) if a.only else None
    for s in load_slots(e):
        if s.get("layout") != "scene" or (only and s["id"] not in only):
            continue
        assets = e / "animations" / s["id"] / "hf" / "assets"
        if not (e / "animations" / s["id"] / "hf" / "index.html").exists():
            sys.exit(f"{s['id']}: run slots.py prepare first (hf/ must be scaffolded before assets/ exists)")
        assets.mkdir(parents=True, exist_ok=True)
        st, du = float(s["start"]), float(s["duration"])
        out = assets / "speaker.mp4"
        tail = st + du - base_d
        vf = ["-vf", f"tpad=stop_mode=clone:stop_duration={tail + 0.2:.3f}"] if tail > 0.01 else []
        # frame-exact seek (reel-08 bug): -ss f"{st:.3f}" rounds a start like 41.3333 DOWN to 41.333, and ffmpeg then
        # returns the frame covering that instant — one frame early (the previous take's last frame on the scene's
        # frame 0, 1-frame lip lag). Seek to the frame's own timestamp + 0.5 ms instead.
        ss = seek_ts(st)
        run(["ffmpeg", "-v", "error", "-y", "-ss", f"{ss:.4f}", "-i", str(base), "-an", *vf, "-t", f"{du:.3f}",
             "-c:v", "libx264", "-crf", "14", "-pix_fmt", "yuv420p", str(out)])
        copied = []
        if s.get("type") in MATTE_TYPES or s.get("cutout") or s.get("depth"):
            # v6 Mode C cutout / v7 depth ("behind me"): the same window with his background removed (VP9 alpha)
            run(["npx", "--yes", "hyperframes", "remove-background", str(out), "-o", str(assets / "speaker_cut.webm"),
                 "--quality", "best"])
            copied.append("speaker_cut.webm (matte)")
        for p in s.get("assets", []):
            src = (e / p) if not Path(p).is_absolute() else Path(p)
            if not src.exists():
                sys.exit(f"{s['id']}: asset not found {src}")
            shutil.copy(src, assets / src.name)
            copied.append(src.name)
        print(f"{s['id']:16s} speaker {probe_duration(out):6.3f}s (scene {du:.3f}{', +freeze' if tail > 0.01 else ''})  {copied}")


# ---------------------------------------------------------------- edl
def load_beats(scene_dir: Path, dur: float) -> list[dict]:
    """animations/<id>/beats.json: [{"t": 2.80, "sfx": "impact", "gain_db": -15 (optional), "what": "..."}] —
    scene-local seconds of the visual contact frame, tag from BEAT_GAIN_DB (written by the scene agent).
    A "scribble" beat (one marker stroke) also carries "dur" (stroke length, s); a legacy marker_beats.json
    ([{"t", "dur"}], reel-06) is read as scribble beats."""
    p = scene_dir / "beats.json"
    if not p.exists() and not (scene_dir / "marker_beats.json").exists():
        return []
    beats = json.loads(p.read_text()) if p.exists() else []
    mp = scene_dir / "marker_beats.json"
    if mp.exists() and not any(b.get("sfx") == "scribble" for b in beats):
        beats += [{"t": b["t"], "sfx": "scribble", "dur": b.get("dur", 0.3), "what": b.get("what", "")}
                  for b in json.loads(mp.read_text())]
    for b in beats:
        if b.get("sfx") not in BEAT_GAIN_DB and b.get("sfx") not in V6_GAIN_DB:
            sys.exit(f"{p}: unknown sfx {b.get('sfx')!r} (use {', '.join(V6_GAIN_DB)}; legacy: {', '.join(BEAT_GAIN_DB)})")
        if not 0 <= float(b["t"]) <= dur + 0.05:
            sys.exit(f"{p}: beat t={b['t']} outside the scene (0–{dur:.2f} s)")
    return sorted(beats, key=lambda b: float(b["t"]))


def cmd_edl(a: argparse.Namespace) -> None:
    e = a.edit_dir.resolve()
    src = json.loads((e / a.edl).read_text())
    out = {k: src[k] for k in ("version", "sources", "output", "mirror", "grade", "ranges", "end_hold") if k in src}
    out["ranges"] = [dict(r) for r in src["ranges"]]
    for r in out["ranges"]:
        r.pop("sfx", None)
    if out["ranges"] and a.hook_sfx and a.hook_sfx != "none":
        out["ranges"][0]["sfx"] = a.hook_sfx
    out["sfx_gain_db"] = a.sfx_gain_db
    sop = a.sfx_policy == "sop"
    if sop:
        out["sfx_lowpass_hz"] = 5000
    n_hook, dropped = 0, 0
    scenes = [s for s in load_slots(e) if s.get("layout") == "scene"]
    ovs, audio = [], []
    prev_end = 0
    n_scribble = 0
    for i, s in enumerate(scenes):
        render = e / "animations" / s["id"] / "render.mov"
        if not render.exists():
            sys.exit(f"{s['id']}: no render.mov yet")
        n = frame_count(render)
        f0 = round(float(s["start"]) * FPS)
        if f0 != prev_end and i > 0:
            print(f"  WARNING {s['id']}: starts at frame {f0}, previous scene ends at frame {prev_end} "
                  f"({'gap' if f0 > prev_end else 'overlap'} of {abs(f0 - prev_end)} f)")
        prev_end = f0 + n
        pre = 0.012 if i > 0 else 0.0
        o = {"file": f"animations/{s['id']}/render.mov", "start_in_output": round(f0 / FPS - pre, 5),
             "duration": round(n / FPS + pre, 5)}
        if i < len(scenes) - 1:
            o["hold"] = 0.1
        else:
            o["duration"] = round(o["duration"] + 0.15, 5)
            o["hold"] = True
        beats = load_beats(e / "animations" / s["id"], n / FPS)
        if s.get("sfx") and not beats:      # legacy one-shot per scene; beats.json supersedes it
            o["sfx"] = s["sfx"]
        last_scribble = -1.0
        for b in beats:
            if sop:
                # the 30 % rule: only hook (≤ 2 in the first 4 s) and structural beats make a sound, from the v6 kit
                t_out = f0 / FPS + float(b["t"])
                role = b.get("role")
                tag = b["sfx"] if b["sfx"] in V6_GAIN_DB else V6_FROM_LEGACY.get(b["sfx"])
                keep = tag and (role == "structural" or (role == "hook" and t_out < HOOK_WINDOW_S and n_hook < HOOK_MAX))
                if not keep:
                    dropped += 1
                    continue
                n_hook += role == "hook"
                audio.append({"file": str(SKILL_DIR / "assets" / "sfx" / f"v6_{tag}.wav"),
                              "start_in_output": round(max(0.0, t_out - 0.02), 3),
                              "gain_db": float(b.get("gain_db", V6_GAIN_DB[tag]) + a.beat_gain_offset),
                              "sfx": tag, "role": role, "scene": s["id"], "what": b.get("what", "")})
                continue
            if b["sfx"] == "scribble":
                # felt-tip stroke: rotate the 3 variants, trim to the stroke's length, never two within 0.1 s
                if float(b["t"]) - last_scribble < 0.1:
                    continue
                last_scribble = float(b["t"])
                dur = max(0.12, min(float(b.get("dur", 0.3)), 1.0, n / FPS - float(b["t"])))
                audio.append({"file": str(SKILL_DIR / "assets" / "sfx" / SCRIBBLE_FILES[n_scribble % 3]),
                              "start_in_output": round(max(0.0, f0 / FPS + float(b["t"]) - 0.01), 3),
                              "duration": round(dur + 0.05, 3), "fade_out": 0.08,
                              "gain_db": float(b.get("gain_db", BEAT_GAIN_DB["scribble"]) + a.beat_gain_offset),
                              "sfx": "scribble", "scene": s["id"]})
                n_scribble += 1
                continue
            audio.append({"file": str(SKILL_DIR / "assets" / "sfx" / f"{b['sfx']}.wav"),
                          "start_in_output": round(max(0.0, f0 / FPS + b["t"] - BEAT_LEAD.get(b["sfx"], 0) - 0.02), 3),
                          "gain_db": float(b.get("gain_db", BEAT_GAIN_DB[b["sfx"]]) + a.beat_gain_offset),
                          "sfx": b["sfx"], "scene": s["id"]})
        ovs.append(o)
        print(f"{s['id']:16s} frames {f0:5d}–{f0 + n:5d}  sfx {s.get('sfx') or '-'}  beats {len(beats)}")
    out["overlays"] = ovs
    reel = float(json.loads((e / "timeline.json").read_text())["total"]) + float(src.get("end_hold", 0))
    if sop:
        print(f"  sfx policy sop: {len(audio)} cues kept (hook ≤ {HOOK_MAX} in 0–{HOOK_WINDOW_S:g} s + structural), "
              f"{dropped} beats left silent")
        if len(audio) > max(14, round(reel / 5)):
            print(f"  WARNING: {len(audio)} cues for {reel:.0f} s — the SOP wants roughly one per structural moment")
    if a.music:
        # music bed: ducked under the voice (render.py sidechain), +lift dB over the last 3 s for the CTA energy lift
        mp = Path(a.music).expanduser()
        if not mp.is_absolute():
            mp = (e / mp).resolve()
        if not mp.exists():
            sys.exit(f"music not found: {mp}")
        bed = mp.with_name(mp.stem + "_lift.wav")
        t0 = max(0.0, reel - 3.0)
        g = 10 ** (a.music_lift / 20) - 1
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(mp), "-af",
                        f"volume='if(lt(t,{t0:.3f}),1,if(lt(t,{t0 + 0.5:.3f}),1+{g:.4f}*(t-{t0:.3f})/0.5,{1 + g:.4f}))':eval=frame",
                        "-ar", "48000", str(bed)], check=True)
        audio.append({"file": str(bed), "start_in_output": 0, "duck": True, "gain_db": a.music_gain,
                      "fade_in": 0.4, "fade_out": 2.0})
        print(f"  music bed {mp.name}: {a.music_gain:+g} dB, ducked under speech, +{a.music_lift:g} dB from {t0:.2f} s")
    if audio:
        out["audio"] = audio
        if not sop:
            print(f"  {len(audio)} beat cues from beats.json (house SFX kit; --beat-gain-offset {a.beat_gain_offset:+g} dB)")
    if abs(prev_end / FPS - reel) > 1.5 / FPS:
        print(f"  WARNING: scenes end at {prev_end / FPS:.3f} s but the reel is {reel:.3f} s")
    if a.captions and "captions" in src:
        out["captions"] = src["captions"]
    (e / a.output).write_text(json.dumps(out, indent=1))
    print(f"→ {e / a.output}  ({len(ovs)} scenes; render with: render.py {a.output} -o final.mp4 --reuse-base)")


# ---------------------------------------------------------------- preview
def cmd_preview(a: argparse.Namespace) -> None:
    e = a.edit_dir.resolve()
    s = next((x for x in load_slots(e) if x["id"] == a.slot), None)
    if not s:
        sys.exit(f"no slot {a.slot}")
    render = e / "animations" / s["id"] / "render.mov"
    out = e / "verify" / f"{s['id']}_preview.mp4"
    out.parent.mkdir(exist_ok=True)
    run(["ffmpeg", "-v", "error", "-y", "-i", str(render), "-ss", f"{float(s['start']):.3f}", "-t", f"{float(s['duration']):.3f}",
         "-i", str(e / "base.mp4"), "-map", "0:v", "-map", "1:a?", "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "192k", "-shortest", str(out)])
    print(f"→ {out}")


# ---------------------------------------------------------------- runtime / rerender
def cmd_runtime(a: argparse.Namespace) -> None:
    from slots import install_runtime
    e = a.edit_dir.resolve()
    n = 0
    for s in load_slots(e):
        hf = e / "animations" / s["id"] / "hf"
        if s.get("layout") == "scene" and hf.is_dir():
            install_runtime(hf)
            n += 1
    print(f"runtime installed into {n} scene(s) — now: scenes.py rerender --edit-dir {e}")


def cmd_rerender(a: argparse.Namespace) -> None:
    import concurrent.futures as cf
    e = a.edit_dir.resolve()
    only = set(a.only.split(",")) if a.only else None
    scenes = [s for s in load_slots(e) if s.get("layout") == "scene" and (only is None or s["id"] in only)]

    def one(s: dict) -> tuple[str, str]:
        d = e / "animations" / s["id"]
        r = subprocess.run(["npx", "--yes", "hyperframes", "render", ".", "--format", "mov", "-o", "../render.mov"],
                           cwd=d / "hf", capture_output=True, text=True)
        if r.returncode != 0:
            return s["id"], "FAILED: " + (r.stderr or r.stdout).strip()[-300:]
        want = json.loads((d / "slot.json").read_text()).get("frames") if (d / "slot.json").exists() else None
        got = frame_count(d / "render.mov")
        return s["id"], f"{got} frames" + ("" if want in (None, got) else f"  MISMATCH (slot.json says {want})")

    with cf.ThreadPoolExecutor(max_workers=a.jobs) as ex:
        for sid, msg in ex.map(one, scenes):
            print(f"{sid:16s} {msg}")
    print(f"rendered {len(scenes)} scene(s) → next: scenes.py edl --edit-dir {e}")


# ---------------------------------------------------------------- flashcheck
NON_PAPER_TYPES = ("fullscreen", "demo", "talk", "talk_depth", "chain", "card")   # windows that legitimately show his footage (v7: Talk beats + the shrink scenes)


def allowed_windows(edit_dir: Path, fps: int = FPS) -> list[tuple[int, int, str]]:
    """Frame ranges (inclusive, with a 3-frame tolerance at each end) of scenes planned as non-paper."""
    out = []
    for s in load_slots(edit_dir):
        if s.get("layout") == "scene" and s.get("type") in NON_PAPER_TYPES:
            f0 = round(float(s["start"]) * fps)
            f1 = round((float(s["start"]) + float(s["duration"])) * fps)
            out.append((max(0, f0 - 3), f1 + 3, s["id"]))
    return out


def gray_frames(video: Path, w: int = 36, h: int = 64) -> list[bytes]:
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(video), "-vf", f"scale={w}:{h},format=gray",
                          "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
    n = len(raw) // (w * h)
    return [raw[i * w * h:(i + 1) * w * h] for i in range(n)]


def cmd_flashcheck(a: argparse.Namespace) -> None:
    """Two detectors. With --edit-dir (and base.mp4): a frame that is near-identical to base.mp4 at the same time IS
    the raw cut showing through (mean abs diff < --raw-mad on a 36x64 grey thumbnail; paper scenes score 25–90,
    fullscreen scenes ~20 because of the strip + push, a leak ~0–2). This is the reliable test — reel-05's ceiling
    was paper-coloured, so the corner test alone was blind. Without --edit-dir: the old corner-colour test (paper,
    or paper uniformly darkened by a scene's own vignette/spotlight)."""
    windows = allowed_windows(a.edit_dir.resolve()) if a.edit_dir else []
    base = a.edit_dir.resolve() / "base.mp4" if a.edit_dir else None
    if base and base.exists():
        out_f, base_f = gray_frames(a.video), gray_frames(base)
        n = len(out_f)
        m = min(n, len(base_f))
        bad = [i for i in range(m) if sum(abs(x - y) for x, y in zip(out_f[i], base_f[i])) / len(out_f[i]) < a.raw_mad]
        how = f"raw-match vs base.mp4 (mad < {a.raw_mad:g})"
    else:
        rgb = tuple(int(x) for x in a.rgb.split(","))
        raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(a.video), "-vf", "crop=40:40:20:20,scale=1:1,format=rgb24",
                              "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
        n = len(raw) // 3

        def is_paper(px: tuple[int, int, int]) -> bool:
            if all(abs(px[k] - rgb[k]) <= a.tol for k in range(3)):
                return True
            kk = sum(px) / sum(rgb)     # paper under a scene's own spotlight/vignette: same colour, uniformly darker
            return 0.6 <= kk <= 1.0 and all(abs(px[k] - rgb[k] * kk) <= 10 for k in range(3))

        bad = [i for i in range(n) if not is_paper(tuple(raw[i * 3:i * 3 + 3]))]
        how = "corner colour (pass --edit-dir for the reliable raw-match test)"
    expected = [i for i in bad if any(f0 <= i <= f1 for f0, f1, _ in windows)]
    bad = [i for i in bad if i not in expected]
    if windows:
        print(f"planned non-paper scenes: " + ", ".join(f"{sid} f{f0}–{f1}" for f0, f1, sid in windows)
              + f" ({len(expected)} raw-looking frames there, as expected)")
    print(f"{a.video}: {n} frames, {len(bad)} unexpected raw-footage frames [{how}]" + (f": {bad[:40]}" if bad else " — clean"))
    if bad and not a.allow:
        sys.exit(1)


def cmd_seam(a: argparse.Namespace) -> None:
    """Continuity check for a recurring drawing (v5): scene A's LAST frame beside scene B's FIRST frame, plus their
    mean difference. Two scenes that share an object (the reel-06 funnel) must cut without a jump."""
    e = a.edit_dir.resolve()
    ra, rb = (e / "animations" / x / "render.mov" for x in (a.a, a.b))
    for r in (ra, rb):
        if not r.exists():
            sys.exit(f"no render: {r}")
    out = e / "verify" / f"seam_{a.a}__{a.b}.jpg"
    out.parent.mkdir(exist_ok=True)
    run(["ffmpeg", "-y", "-v", "error", "-sseof", "-0.04", "-i", str(ra), "-i", str(rb), "-filter_complex",
         "[0:v]trim=end_frame=1,scale=540:-1,format=rgb24[a];[1:v]trim=end_frame=1,scale=540:-1,format=rgb24[b];[a][b]hstack",
         "-frames:v", "1", str(out)])
    from PIL import Image, ImageChops, ImageStat
    im = Image.open(out)
    w = im.width // 2
    diff = ImageStat.Stat(ImageChops.difference(im.crop((0, 0, w, im.height)), im.crop((w, 0, 2 * w, im.height)))).mean
    print(f"{out}  mean diff {sum(diff) / 3:.1f} (0 = identical; the shared drawing should line up, scene-specific words may differ)")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("init-brand"); p.add_argument("--edit-dir", type=Path, required=True)
    p.add_argument("--look", choices=["mint", "paper"], default="mint",
                   help="mint = v7 house look (default since reel-08); paper = legacy v6 red paper + marker")
    p.add_argument("--accent", default=None, help="paper look: preset or #hex (default red); mint look: leave unset")
    p.add_argument("--type", choices=["grotesk", "editorial"], default="grotesk")
    p.add_argument("--frame", type=Path); p.add_argument("--platform", default="reels")
    p.add_argument("--type-scale", type=float, default=TYPE_SCALE, help="kinetic type size multiplier (house 0.94)")
    p.set_defaults(fn=cmd_init_brand)
    p = sub.add_parser("words"); p.add_argument("--edit-dir", type=Path, required=True); p.add_argument("--edl", default="edl.json")
    p.set_defaults(fn=cmd_words)
    p = sub.add_parser("cut-speaker"); p.add_argument("--edit-dir", type=Path, required=True)
    p.add_argument("--only", default=None, help="comma-separated scene ids"); p.set_defaults(fn=cmd_cut_speaker)
    p = sub.add_parser("edl"); p.add_argument("--edit-dir", type=Path, required=True); p.add_argument("--edl", default="edl.json")
    p.add_argument("-o", "--output", default="edl_scenes.json")
    p.add_argument("--hook-sfx", default="none", help="legacy synth on the first range (v5: subdrop); v6 default none")
    p.add_argument("--sfx-gain-db", type=float, default=-13); p.add_argument("--captions", action="store_true")
    p.add_argument("--beat-gain-offset", type=float, default=0.0, help="shift every beats.json cue (dB), e.g. -3 if busy")
    p.add_argument("--sfx-policy", choices=["sop", "all"], default="sop",
                   help="sop (v6): only hook (≤2 in 0–4 s) + structural beats, low & warm v6 kit, 5 kHz low-pass; "
                        "all: every beat from the v5 kit (legacy)")
    p.add_argument("--music", default=None, help="music bed (e.g. music/take1.mp3): ducked under speech + CTA lift")
    p.add_argument("--music-gain", type=float, default=-19, help="bed gain before ducking (≈ −22…−26 dB under speech)")
    p.add_argument("--music-lift", type=float, default=2.5, help="dB added over the final 3 s (CTA energy lift)")
    p.set_defaults(fn=cmd_edl)
    p = sub.add_parser("preview"); p.add_argument("slot"); p.add_argument("--edit-dir", type=Path, required=True)
    p.set_defaults(fn=cmd_preview)
    p = sub.add_parser("flashcheck"); p.add_argument("video", type=Path)
    p.add_argument("--edit-dir", type=Path, default=None, help="read slots.json: fullscreen/demo scene windows are expected non-paper")
    p.add_argument("--rgb", default=",".join(map(str, PAPER_CORNER_RGB))); p.add_argument("--tol", type=int, default=25)
    p.add_argument("--raw-mad", type=float, default=4.0, help="raw-match threshold (mean abs grey diff vs base.mp4)")
    p.add_argument("--allow", action="store_true", help="report only (e.g. a reel with a full-bleed demo scene)")
    p.set_defaults(fn=cmd_flashcheck)
    p = sub.add_parser("seam"); p.add_argument("a"); p.add_argument("b"); p.add_argument("--edit-dir", type=Path, required=True)
    p.set_defaults(fn=cmd_seam)
    p = sub.add_parser("runtime"); p.add_argument("--edit-dir", type=Path, required=True); p.set_defaults(fn=cmd_runtime)
    p = sub.add_parser("rerender"); p.add_argument("--edit-dir", type=Path, required=True)
    p.add_argument("--jobs", type=int, default=4); p.add_argument("--only", default=None); p.set_defaults(fn=cmd_rerender)
    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
