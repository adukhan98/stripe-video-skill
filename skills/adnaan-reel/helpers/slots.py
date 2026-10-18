"""Graphic slots: set up the folders parallel sub-agents build in, then QA their renders.

  prepare  for every slot in <edit>/animations/slots.json create <edit>/animations/<id>/:
             TASK.md    what to build: exact window, canvas, layout zone, brief, paths
             slot.json  the same, machine-readable (check reads it)
             words.txt  words spoken during the slot, seconds from slot start
             refs/      3 frames of the cut underneath (start / middle / end)
             brand.css + fonts/ + logos/   (brand_kit.py install)
             hf/paper.css + hf/paper.js    the shared runtime (templates/runtime) — world, cards, words, primitives
             hf/marker.css + hf/marker.js  the hand-drawn marker layer (v5) — strokes that draw on and boil, highlighter, notes
             hf/index.html                 the starter for the slot's "type" (templates/scenes/<type>.html), duration preset
             words.html                    every spoken word as a ready <span class="w" data-t> (paste, then size/place)
           and <edit>/animations/SLOT_BRIEF.md (shared rules) if missing.
           Prints one sub-agent prompt per slot (template scenes can go to a smaller model; "bespoke": true = strong model).
  check    composite a slot render over the cut at its window with the safe zone (red)
           and caption band (yellow) drawn, write <slot>/check_sheet.jpg, and verify
           size, fps, duration, alpha, transparent first/last frame and safe-zone spill.
           --motion also writes <slot>/motion_strip.jpg (every 2nd frame through the
           entrance, each --at landing and the exit — read it to see anticipation,
           overshoot and settle) and warns about dead holds (≥ 1 s of visible graphic
           with nothing moving: add secondary action).

slots.json:
  [{"id": "v01_hook", "start": 0.0, "duration": 4.433, "layout": "scene", "type": "hook", "bespoke": false,
    "brief": "...", "assets": ["captures/rea_repo.png"], "sfx": "chime"}]
  layouts: scene (adnaan-reel) | full | top | lower_third | split | corner
  types (scene starters) — v7 mint look (house default): talk | talk_depth | visual | chain | card
                          legacy paper look: hook | chapter_page | explainer | mechanism | opinion | wrapup | cta | fullscreen | demo | blank | cutout

Usage:
    python helpers/slots.py prepare --edit-dir <edit> [--platform reels]
    python helpers/slots.py check <edit>/animations/s1_hook
    python helpers/slots.py check <edit>/animations/s1_hook --motion --at 0.9,2.6
    python helpers/slots.py check <render.mov> --start 12.5 --edit-dir <edit> [--layout split]
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import shutil
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from captions import output_words  # noqa: E402
from platforms import get_platform, platform_for_canvas, scaled  # noqa: E402

SKILL_DIR = Path(__file__).resolve().parent.parent
RUNTIME_DIR = SKILL_DIR / "templates" / "runtime"
STARTERS_DIR = SKILL_DIR / "templates" / "scenes"
LAYOUTS = ("scene", "full", "top", "lower_third", "split", "corner")
RUNTIME_FONTS = ("InterTight-Variable.ttf", "Inter-Variable.ttf", "GeistMono-Medium.ttf", "Caveat-Variable.ttf")
RUNTIME_FILES = ("paper.css", "paper.js", "marker.css", "marker.js", "v7.css", "v7.js")   # v5 marker layer (paper look) + v7 mint layer
ALPHA_PIX = ("yuva", "gbra", "rgba", "bgra", "argb", "abgr", "ya")


def layout_zone(layout: str, plat: dict) -> tuple[int, int, int, int]:
    """Where a slot's content may go, inside the platform safe zone."""
    w, h = plat["canvas"]
    x0, y0, x1, y1 = plat["safe"]
    b0, _ = plat["caption_band"]
    if layout == "top":
        return x0, y0, x1, y0 + int((y1 - y0) * 0.30)
    if layout == "lower_third":
        return x0, max(y0, b0 - int(h * 0.17)), x1, b0 - int(h * 0.01)
    if layout == "split":
        return x0, y0, x1, h // 2 - 30
    if layout == "corner":
        return x1 - int(w * 0.22), y0, x1, y0 + int(h * 0.09)
    return x0, y0, x1, y1


LAYOUT_NOTES = {
    "scene": "FULL-SCREEN OPAQUE SCENE (adnaan-reel): paint the grey-paper background edge to edge on EVERY frame, "
             "first and last included — scenes butt against each other with hard cuts and replace the footage "
             "entirely (the speaker appears only as the embedded hf/assets/speaker.mp4). All content inside the zone; "
             "measure your own bounds across all frames (the check cannot, because the scene is opaque).",
    "full": "Full-screen graphic. Background fills may run edge to edge; text and marks stay in the zone. "
            "Keep the caption band visually quiet (plain background only) while captions show.",
    "top": "Top card. Content only in the zone so the speaker's face stays visible below it.",
    "lower_third": "Name/title strap above the caption band. Animate in, hold, animate out.",
    "split": "Opaque panel covering the TOP HALF (y 0 to H/2, edge to edge); content in the zone. The "
             "compositor moves the speaker into the bottom half and captions sit on the seam — keep the "
             "bottom 30 px of the panel free of content.",
    "corner": "Small mark (logo bug, badge, counter) in the top-right corner of the safe zone.",
}


def find_base(edit_dir: Path) -> Path | None:
    for name in ("base.mp4", "base_preview.mp4", "base_draft.mp4"):
        if (edit_dir / name).exists():
            return edit_dir / name
    return None


def probe(path: Path) -> dict:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=codec_name,pix_fmt,width,height,avg_frame_rate:format=duration",
         "-of", "json", str(path)],
        capture_output=True, text=True,
    )
    try:
        data = json.loads(out.stdout)
        s = data["streams"][0]
        num, den = (s.get("avg_frame_rate") or "0/1").split("/")
        return {
            "codec": s.get("codec_name"), "pix_fmt": s.get("pix_fmt"),
            "width": int(s["width"]), "height": int(s["height"]),
            "fps": float(num) / float(den or 1) if float(den or 1) else 0.0,
            "duration": float(data.get("format", {}).get("duration") or 0),
        }
    except (KeyError, IndexError, ValueError, json.JSONDecodeError):
        return {}


# -------- prepare ----------------------------------------------------------------


def cmd_prepare(args: argparse.Namespace) -> None:
    edit_dir = args.edit_dir.resolve()
    anim = edit_dir / "animations"
    slots_path = args.slots or (anim / "slots.json")
    if not slots_path.exists():
        sys.exit(f"no {slots_path} — write the slot list first (see this file's docstring)")
    slots = json.loads(slots_path.read_text())
    edl = json.loads((edit_dir / "edl.json").read_text())
    base = args.base or find_base(edit_dir)
    if base is None:
        sys.exit("no base.mp4 — run render.py <edl> -o <edit>/base.mp4 --base-only first")
    bp = probe(base)
    out = edl.get("output") or {}
    cw, ch = (int(out["width"]), int(out["height"])) if out.get("width") else (bp["width"], bp["height"])
    tl = edit_dir / "timeline.json"
    fps = json.loads(tl.read_text()).get("fps", "30") if tl.exists() else "30"
    fps_f = eval_fps(fps)
    platform = args.platform
    brand_json = edit_dir / "brand" / "brand.json"
    if platform is None and brand_json.exists():
        platform = json.loads(brand_json.read_text()).get("platform")
    plat = scaled(get_platform(platform or platform_for_canvas(cw, ch)), cw, ch)
    words = output_words(edl, edit_dir)
    look = json.loads(brand_json.read_text()).get("look", "paper") if brand_json.exists() else "paper"

    brief_path = anim / "SLOT_BRIEF.md"
    anim.mkdir(parents=True, exist_ok=True)
    if not brief_path.exists():
        tmpl = (SKILL_DIR / "templates" / "SLOT_BRIEF.md").read_text()
        brief_path.write_text(tmpl.replace("{{EDIT_DIR}}", str(edit_dir)).replace("{{SKILL_DIR}}", str(SKILL_DIR)))

    prompts = []
    for s in slots:
        sid, start, dur = s["id"], float(s["start"]), float(s["duration"])
        layout = s.get("layout", "full")
        if layout not in LAYOUTS:
            sys.exit(f"slot {sid}: unknown layout '{layout}' (use {', '.join(LAYOUTS)})")
        d = anim / sid
        (d / "refs").mkdir(parents=True, exist_ok=True)
        zone = layout_zone(layout, plat)
        # frames from the frame-snapped window (what scenes.py edl uses), not round(dur * fps):
        # a 5.55 s slot starting at 35.15 s needs 167 frames, round(166.5) gives 166 → a 1-frame gap
        frames = round((start + dur) * fps_f) - round(start * fps_f)

        lines = [f"{w['start'] - start:7.2f}  {w['text']}" for w in words
                 if start - 0.3 <= w["start"] <= start + dur + 0.3]
        (d / "words.txt").write_text(
            "# seconds from slot start → word (approximate: land reveals ~0.15 s before the listed time)\n"
            + "\n".join(lines) + "\n")

        for name, t in (("start", start + 0.05), ("mid", start + dur / 2), ("end", start + dur - 0.05)):
            subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{max(0, t):.3f}", "-i", str(base),
                            "-frames:v", "1", "-vf", "scale=trunc(iw/4)*2:-2",
                            str(d / "refs" / f"{name}.jpg")], check=False)

        hf_ok = scaffold_hyperframes(d, cw, ch, (frames - 0.5) / fps_f)
        if (edit_dir / "brand" / "brand.css").exists():
            subprocess.run([sys.executable, str(SKILL_DIR / "helpers" / "brand_kit.py"), "install", str(d / "hf"),
                            "--edit-dir", str(edit_dir)], check=False, stdout=subprocess.DEVNULL)
        stype = s.get("type")
        if layout == "scene" and hf_ok:
            install_runtime(d / "hf")
            if look == "mint":
                stype = stype or ("talk" if s is slots[0] or s is slots[-1] else "visual")
                if stype in PAPER_ONLY_TYPES:
                    print(f"  WARNING {sid}: '{stype}' is a legacy paper-look starter (split band + marker); "
                          f"v7 starters: {', '.join(V7_TYPES)}")
            else:
                stype = stype or ("hook" if s is slots[0] else "cta" if s is slots[-1] else "blank")
            write_starter(d / "hf", stype, sid, (frames - 0.5) / fps_f)
            (d / "words.html").write_text(words_html(words, start, dur))

        meta = {"id": sid, "start": start, "duration": dur, "frames": frames, "fps": fps, "canvas": [cw, ch],
                "layout": layout, "type": stype, "bespoke": bool(s.get("bespoke", stype in BESPOKE_TYPES)),
                "zone": list(zone), "safe": list(plat["safe"]),
                "caption_band": list(plat["caption_band"]), "platform": plat["label"],
                "base": str(base), "crop_y": s.get("crop_y"), "brief": s.get("brief", ""), "scaffolded": hf_ok,
                "look": look}
        (d / "slot.json").write_text(json.dumps(meta, indent=2))
        (d / "TASK.md").write_text(task_md(meta, d, edit_dir))
        model = "strong model (bespoke hero object)" if meta["bespoke"] else "smaller model is fine (template scene)"
        prompts.append(f"[{model}] Build graphic slot {sid}. Read {brief_path} and then {d / 'TASK.md'}. "
                       f"Work only inside {d}. Do not ask questions.")
        print(f"  {sid:20s} {start:7.2f}s +{dur:5.2f}s  {layout:11s} {stype or '-':13s} zone x {zone[0]}-{zone[2]}, "
              f"y {zone[1]}-{zone[3]}  ({len(lines)} words)")

    print(f"\nprepared {len(slots)} slot(s) in {anim}. Spawn one sub-agent per slot, all in ONE message:")
    for p in prompts:
        print(f"  - {p}")


BESPOKE_TYPES = ("explainer", "mechanism", "blank", "visual", "chain", "card", "talk_depth")   # hero object has to be invented
V7_TYPES = ("talk", "talk_depth", "visual", "chain", "card")
PAPER_ONLY_TYPES = ("hook", "opinion", "wrapup", "cta", "chapter_page", "explainer", "mechanism")   # split band / marker starters


def install_runtime(hf: Path) -> None:
    """Copy the shared runtime (paper + marker layer) and its fonts into a slot's hf/ (idempotent; re-run to restyle)."""
    for name in RUNTIME_FILES:
        shutil.copy2(RUNTIME_DIR / name, hf / name)
    (hf / "fonts").mkdir(exist_ok=True)
    for f in RUNTIME_FONTS:
        src = SKILL_DIR / "assets" / "fonts" / f
        if src.exists() and not (hf / "fonts" / f).exists():
            shutil.copy2(src, hf / "fonts" / f)


def starter_path(stype: str) -> Path:
    p = STARTERS_DIR / f"{stype}.html"
    if not p.exists():
        sys.exit(f"unknown scene type {stype!r}; starters: {', '.join(sorted(x.stem for x in STARTERS_DIR.glob('*.html')))}")
    return p


def write_starter(hf: Path, stype: str, sid: str, duration: float, force: bool = False) -> bool:
    """hf/index.html ← templates/scenes/<type>.html with every data-duration preset to the exact frame count.
    A sentinel hf/.starter records the type; if index.html was edited after it (an agent authored the scene),
    it is left alone unless force."""
    index, sentinel = hf / "index.html", hf / ".starter"
    if index.exists() and sentinel.exists() and index.stat().st_mtime > sentinel.stat().st_mtime + 1 and not force:
        return False
    html = starter_path(stype).read_text()
    html = re.sub(r'data-duration="[0-9.]+"', f'data-duration="{duration:.4f}"', html)
    html = re.sub(r"<title>.*?</title>", f"<title>{sid}</title>", html, count=1)
    index.write_text(html)
    sentinel.write_text(stype + "\n")
    return True


def words_html(words: list[dict], start: float, dur: float) -> str:
    """Every spoken word of the slot as a ready kinetic span (contact time preset). The agent pastes these into
    .line blocks, then only chooses size/position/kind (data-hero / data-pop / data-accent) and colour."""
    out = ["<!-- words.html: paste into .line blocks in hf/index.html; keep data-t, add data-hero/data-pop/data-accent,",
           "     .ocean (accent) on 1-2 key words per phrase; omit fillers only; never paraphrase. Times = word start, slot seconds. -->"]
    for w in words:
        if start - 0.3 <= w["start"] <= start + dur + 0.3:
            t = w["start"] - start
            txt = w["text"].replace("&", "&amp;").replace("<", "&lt;")
            if t < -0.02 or t > dur:
                out.append(f'<!-- {"before" if t < 0 else "after"} this scene ({t:+.2f} s): {txt} — belongs to the neighbour -->')
            else:
                out.append(f'<span class="w gap-s" data-t="{t:.2f}">{txt}</span>')
    return "\n".join(out) + "\n"


RESOLUTION_PRESETS = {(1080, 1920): "portrait", (1920, 1080): "landscape", (1080, 1080): "square",
                      (2160, 3840): "portrait-4k", (3840, 2160): "landscape-4k", (2160, 2160): "square-4k"}


def count_frames(p: Path) -> int | None:
    r = subprocess.run(["ffprobe", "-v", "error", "-count_packets", "-select_streams", "v:0",
                        "-show_entries", "stream=nb_read_packets", "-of", "csv=p=0", str(p)],
                       capture_output=True, text=True)
    try:
        return int(r.stdout.strip())
    except ValueError:
        return None


def scaffold_hyperframes(slot_dir: Path, width: int, height: int, duration: float) -> bool:
    """`hyperframes init hf` inside the slot (init refuses non-empty folders, so the project
    lives in hf/), pre-set to the canvas, the slot duration and a transparent background."""
    hf = slot_dir / "hf"
    if (hf / "index.html").exists():
        return True
    cmd = ["npx", "--yes", "hyperframes", "init", "hf", "--example", "blank", "--non-interactive"]
    if (width, height) in RESOLUTION_PRESETS:
        cmd += ["--resolution", RESOLUTION_PRESETS[(width, height)]]
    try:
        subprocess.run(cmd, cwd=slot_dir, env={**os.environ, "HYPERFRAMES_SKIP_SKILLS": "1"},
                       capture_output=True, text=True, timeout=300)
    except (OSError, subprocess.TimeoutExpired):
        return False
    index = hf / "index.html"
    if not index.exists():
        return False
    html = index.read_text()
    # the renderer rounds the frame count up, so (frames - 0.5) / fps yields exactly `frames`
    html = re.sub(r'data-duration="[0-9.]+"', f'data-duration="{duration:.4f}"', html)
    html = re.sub(r'data-width="\d+"', f'data-width="{width}"', html)
    html = re.sub(r'data-height="\d+"', f'data-height="{height}"', html)
    html = re.sub(r'content="width=\d+, height=\d+"', f'content="width={width}, height={height}"', html)
    html = re.sub(r"width: \d+px;(\s*)height: \d+px;", f"width: {width}px;\\1height: {height}px;", html, count=1)
    html = html.replace("background: #0a0a0a;", "background: transparent;")
    index.write_text(html)
    return True


def eval_fps(fps: str) -> float:
    if "/" in str(fps):
        a, b = str(fps).split("/")
        return float(a) / float(b)
    return float(fps)


def task_md(m: dict, d: Path, edit_dir: Path) -> str:
    x0, y0, x1, y1 = m["zone"]
    sx0, sy0, sx1, sy1 = m["safe"]
    b0, b1 = m["caption_band"]
    w, h = m["canvas"]
    if m["layout"] == "scene":
        return scene_task_md(m, d, edit_dir)
    return f"""# Graphic slot `{m['id']}`

Build ONE transparent overlay animation. Nothing else.

| | |
|---|---|
| Output | `{d / 'render.mov'}` — HyperFrames `--format mov` (ProRes 4444 with alpha) |
| Canvas | {w}x{h} @ {m['fps']} fps |
| Duration | EXACTLY {m['frames']} frames (window {m['duration']:.3f} s; data-duration is preset so the renderer outputs {m['frames']} — keep it; `slots.py check` fails on any other count) |
| Window in the final video | {m['start']:.3f} – {m['start'] + m['duration']:.3f} s |
| Layout | **{m['layout']}** — content inside **x {x0}–{x1}, y {y0}–{y1}** |
| Safe zone ({m['platform']}) | x {sx0}–{sx1}, y {sy0}–{sy1}; caption band y {b0}–{b1} |

{LAYOUT_NOTES[m['layout']]}

## Brief

{m['brief'] or '(see the editor notes)'}

## Inputs (all in this folder)

- `words.txt` — what is said during the slot, seconds from slot start. Land reveals on the words.
- `refs/start.jpg`, `refs/mid.jpg`, `refs/end.jpg` — the footage underneath (half scale).
- `hf/` — the HyperFrames project: {"already scaffolded at this canvas and duration with a transparent background" if m.get("scaffolded") else "NOT scaffolded yet — run: cd " + str(d) + " && HYPERFRAMES_SKIP_SKILLS=1 npx --yes hyperframes init hf --example blank --non-interactive, then set the canvas, duration and transparent background"}.
  The brand kit is in `hf/brand.css`, `hf/fonts/`, `hf/logos/`. Binding rules: `{edit_dir / 'brand' / 'DESIGN.md'}`.

## Deliver

1. Author `hf/index.html`, then render from `hf/`:
   `npx --yes hyperframes lint . && npx --yes hyperframes render . --format mov -o ../render.mov`
2. QA: `uv run --project {SKILL_DIR} {SKILL_DIR / 'helpers' / 'slots.py'} check {d}` → read `check_sheet.jpg` and fix until clean.
3. `NOTES.md`: what it shows and its timeline in slot seconds.
"""


V7_TASK_SECTION = """## v7 "MINT" look (this project — read hf/v7.js + hf/v7.css headers; SHARED.md's v7 section is binding)

- **No red, no hand-drawn marker layer, no Caveat.** marker.js is installed for legacy scenes only — don't load it. A line
  that draws itself (connector, underline bar, magnifier rim) is a clean vector stroke: even width, round caps, no wobble.
- **Two modes.** TALK = him full-screen (`.spk.full`); our kinetic captions in charcoal with the soft light glow (`.g7`), mint
  hero words (`.ocean`, hero sizes ≥ 170 only); usually captions only, occasionally ONE icon disc, no pills. VISUAL = the
  board (`V.board()` strong vignette), a world layer the camera travels across (`V.cam`, `V.pose`, `.v7-zone`), icon discs,
  flat vector props, real pages as big readable cards with the mint highlighter (`.v7-hl`).
- **Signature shrink** (`V.shrink` / `V.grow` / `V.placed`): his footage → a chain disc `{x, y, d}` or the small card
  `{x, y, w, h}` (LEFT side only). **Disc chain** (`V.chain`, `V.chainDraw`, `V.chainEnd`): the reel's map — geometry in
  SHARED.md; a scene that follows a chain scene opens on its exact end state (`scenes.py seam` checks it).
- **Icon discs** (`V.disc`, `V.discIn`): white Phosphor fill glyph from `hf/assets/<name>.svg` (fetch with `fetch.py icon`),
  charcoal = default, mint = the current item; pop with anticipation + overshoot, glyph 2 f later.
- **Palette**: mint `--brand-primary`, deep mint `--brand-primary-dark`, charcoal `--brand-deep`, ink `--brand-text`,
  `--mint-soft`, `--mint-panel`, `--peach` = DATA ONLY (charts, result bars, rolling numbers). Hero objects are flat vector
  illustrations (flat fills + soft shadows) with the same personality in motion.
- **Depth** (`talk_depth`): footage → `.v7-behind` → his matte (`assets/speaker_cut.webm`, identical data-push) → words.

"""


def scene_task_md(m: dict, d: Path, edit_dir: Path) -> str:
    x0, y0, x1, y1 = m["zone"]
    w, h = m["canvas"]
    stype = m.get("type") or "blank"
    starter = STARTERS_DIR / f"{stype}.html"
    mint = m.get("look") == "mint"
    marker_section = f"""## Marker layer (hf/marker.js — read its header; the starter already inits `const M = Marker.init(P)`)

The house look since v5 (reel-06): a red felt-tip marker annotates every scene, strokes draw on ON their word and then
boil on fours. `M.circle / circleEl / circleRect` (loops — only around isolated big words, numbers, objects),
`M.underline / underlineEl {{double}}`, `M.arrow`, `M.cross / check / strikeEl`, `M.hatch(poly)`, `M.highlight(card, rect)`
(highlighter BEHIND text in a real page/post — never a loop across lines), `M.note(text, x, y, at, {{size ≥ 60}})` (Caveat,
ink or default dark accent), `M.tape`, `M.funnel` (recurring diagram pattern), `M.line(points)` for any doodle you invent
(crown, clock, globe, padlock, sun, stick people, price tag, magnifier…), `M.erase`. Pass `{{parent}}` to draw on a card's
own svg so the drawing rides the card. Stroke width 8–14 px.

"""
    look_section = V7_TASK_SECTION if mint else marker_section
    return f"""# Scene `{m['id']}` — type **{stype}** ({"bespoke hero object: invent it" if m.get("bespoke") else "template scene: fill the starter"})

Build ONE full-screen opaque scene of an adnaan-reel. Nothing else. Work only inside this folder.

| | |
|---|---|
| Output | `{d / 'render.mov'}` — HyperFrames `--format mov` |
| Canvas | {w}x{h} @ {m['fps']} fps |
| Duration | **EXACTLY {m['frames']} frames** (window {m['duration']:.3f} s). `data-duration` is preset on the root AND the speaker video — keep both. `slots.py check` fails on any other count. |
| Window in the final video | {m['start']:.3f} – {m['start'] + m['duration']:.3f} s |
| Content zone | x {x0}–{x1}, y {y0}–{y1} (measure your bounds on every frame, incl. overshoot and the camera push) |

## Brief

{m['brief'] or '(see SHARED.md project specifics)'}
{"" if stype not in ("fullscreen", "demo", "talk", "talk_depth") else chr(10) + "This scene is planned as NON-PAPER (he / the recording fills the frame); flashcheck expects it. Keep it minimal: words low, at most ONE object if the brief names it."}

## What is already done for you

- `hf/index.html` is the **{stype} starter** (`{starter}`): world, speaker MODE (v6: A split / B canvas / C full or
  cutout — see SHARED.md / style.md "v6"), kinetic words, exits and one
  bespoke object, already wired to the shared runtime `hf/paper.js` + `hf/paper.css`. Keep the runtime untouched —
  it IS the house style. You change the copy, positions, sizes, timings and the hero object.
- `words.html` — every spoken word as `<span class="w" data-t="…">` with its contact time. Paste them into
  `.line` blocks; add `data-hero` / `data-pop` / `data-accent`, `.ocean` (= the accent class; red by default) on 1–2 key words per phrase,
  `data-size` / `data-x` / `data-right` / `data-base` on the line, `data-exit="t"` to clear a phrase.
  On-screen words = these words only (fix ASR spellings of names; omit fillers; never paraphrase).
- `hf/assets/speaker.mp4` — his take, already cut to this window (muted). Face centre is set once on
  `<body data-face>` (from SHARED.md "Project specifics"); the runtime crops the split band / cards so the whole head is in.
  Cutout scenes also get `hf/assets/speaker_cut.webm` (background removed) — use it as the cutout's video src.
- `hf/assets/` — captured pages / media named in the brief (after `scenes.py cut-speaker`).
- `refs/*.jpg` — the footage under this window. `slot.json` — this table, machine-readable.

## Runtime API (hf/paper.js — read its header; everything applies Lasseter's principles by default)

`const P = await Paper.init(); const {{ tl, D, F, $, $$ }} = P;` then on `tl`:
`P.enter(sel, t)`, `P.pop(sel, t)`, `P.arc(sel, t, {{fromX, fromY}})`, `P.squash(sel, t)` (shapes only),
`P.recede(sel, t)` / `P.restore(sel, t)` (staging), `P.moveTo(sel, t, {{x, y, scale}})`, `P.exitUp/exitDown(sel, t)`,
`P.punch(t)` / `P.shake(t)` (one hero beat), `P.pulse(el, t)`, `P.breathe(el)`, `P.floatY(el, px)`,
`P.coinIn/coinActive`, `P.pillIn`, `P.cardIn`, `P.scrollPage`, `P.puckFeed`, `P.drawPath/marchPath/ride`,
`P.cursorTo/cursorClick/cursorOut`, `P.typeIn`, `P.underline(wordEl, t)`,
**v6 mode switches**: `P.splitIn(sel, t)` (B→A), `P.splitOut(sel, t)` (A→B), `P.fullToSplit(sel, t, {{h}})` (C→A), `P.splitToFull(sel, t)` (A→C).
Data attributes: `.spk.split[data-h data-face-at data-at]` (Mode A), `.spk.full`, `.spk.cutout[data-w data-x data-drop data-at]` (Mode C),
`.spk.portrait|secondary|small[data-x data-y data-w data-h data-at]` (rare: 0–2 per reel), `.coin[data-n data-x data-y]`,
`.puck[data-x data-y]`, `.cursor`, `.pill`, `.chip`, `.uicard[.deep]`, `.browser > .chrome/.viewport/.page`, `.term`,
`[data-float] [data-breathe] [data-pulse] [data-punch] [data-exit data-exit-lag] [data-underline] [data-strike]`.

{look_section}## Readability (binding — the reviewer fails a scene on any of these)

- Every pixel (type incl. descenders + overshoot, cards incl. rotated corners, logos, notes, marker strokes) inside
  the content zone on every frame, incl. the camera push — measured, not eyeballed.
- Real pages/posts: readable strips (≥ 0.85 scale, ~40–45 px text), one strip at a time; emphasise with `M.highlight`.
- No semi-transparent text: a word is fully readable or gone (exit it in 6 f). Stage focus by receding OBJECTS, never words.
- Handwriting ≥ 60 px in ink / dark accent (never grey). Kinetic hero ≥ 170 authored, nothing under 64.
- Nothing crosses text or the face; words over his clothing sit on solid paper (strip/panel), not on dark fabric.
- Logos, doodles and chips big enough to read on a phone (logo in a chip ≥ 56 px).
- **IG safe zones (v6)**: nothing right of x 900 below y 1200 (Like/Comment/Share icons); in Mode A the content band is
  y 1000–1480. Guidelines (content-dependent): about two focal elements at a time, ~35–50 % of the grid left empty.

## Deliver

1. **Key poses first** (`NOTES.md`): frame, what is on screen, which word it lands on. Then author `hf/index.html`.{chr(10) + "   **This scene opens the reel — frame 0 is the THUMBNAIL**: only finished, true content on it (text hook readable, no transient" + chr(10) + "   numbers: odometers/split-flaps/counters start blank or on their real value, nothing mid-entrance). Check frame-00 of your snapshot." if (stype == "hook" or float(m.get("start", 1)) == 0) else ""}
2. **Snapshot before you render** (seconds): `cd hf && npx --yes hyperframes lint . && npx --yes hyperframes snapshot . --at <your landings>`
   Look at the PNGs: collisions, cropped face, small type, empty lower zone. Fix, snapshot again. Render only when the stills are right:
   `npx --yes hyperframes render . --format mov -o ../render.mov`
3. **QA**: `uv run --project {SKILL_DIR} {SKILL_DIR / 'helpers' / 'slots.py'} check {d} --motion --at <landings>`
   then `ffprobe -count_packets` = {m['frames']} frames; measure bounds (diff against a background-only render).
   Open `check_sheet.jpg` + `motion_strip.jpg`. Fix and re-render until genuinely good.
4. **Principles checklist** (answer each in NOTES.md — Lasseter, `{SKILL_DIR / 'references' / 'animation-principles.md'}`):
   contact frames on words · anticipation before the hero moves · overshoot + settle · parts lag the whole (2–4 f) ·
   long moves on arcs · squash/stretch on shapes only · one focal point (recede the rest) · secondary action, no dead hold ≥ 1 s ·
   one exaggerated hero beat · exits faster than entrances · one light direction / contact shadows · nothing reads as a static slide.
   Plus the readability list above (zone measured, strips ≥ 0.85, no ghosted text, notes ≥ 60 px, nothing over face/text).
5. **Richness (house level, tempered by the v6 two-element guideline)**: list in NOTES.md the hero object + the 1–3 secondary micro-animations
   (`{SKILL_DIR / 'references' / 'motion-ideas.md'}`) and the word each lands on{" — this is a fullscreen/TALK beat: expressive type + at most one small object (v7: one icon disc, no pills)" if stype in ("fullscreen", "demo", "talk", "talk_depth") else ""}.
6. **`beats.json`** in this folder: `[{{"t": 2.80, "sfx": "thud", "role": "structural", "what": "…"}}]` — v6, the 30 % rule:
   list your contact frames, but only tag the 0–2 that deserve a sound with a `"role"`: `"hook"` (only in the reel's first
   4 s: `stamp`/`clunk`) or `"structural"` (point 1/2/3 → `thud`, a mode switch → `whoosh`, a page/screenshot sliding in →
   `paper`, a list/CTA landing → `pop`). Untagged beats stay silent. No `scribble` beats, no dings/ticks/risers.
   Scratch work → `{d / 'qa'}/`.
7. **Stop every background process/monitor you started**, then **reply** with: render path, check line, frame count,
   measured bounds, key timings, what is new, deviations from the brief.
"""


# -------- check ----------------------------------------------------------------


def cmd_check(args: argparse.Namespace) -> None:
    target = args.target.resolve()
    if target.is_dir():
        meta = json.loads((target / "slot.json").read_text())
        render = next((target / n for n in ("render.mov", "render.webm", "render.mp4") if (target / n).exists()), None)
        if render is None:
            sys.exit(f"no render.mov in {target}")
        slot_dir = target
    else:
        if args.start is None or args.edit_dir is None:
            sys.exit("checking a bare file needs --start and --edit-dir")
        render, slot_dir = target, target.parent
        edit_dir = args.edit_dir.resolve()
        base = find_base(edit_dir)
        bp = probe(base)
        plat = scaled(get_platform(args.platform or platform_for_canvas(bp["width"], bp["height"])), bp["width"], bp["height"])
        meta = {"start": args.start, "duration": None, "layout": args.layout or "full", "base": str(base),
                "canvas": [bp["width"], bp["height"]], "safe": list(plat["safe"]),
                "caption_band": list(plat["caption_band"]), "crop_y": args.crop_y, "fps": None}

    info = probe(render)
    problems: list[str] = []
    w, h = meta["canvas"]
    print(f"{render.name}: {info.get('codec')} {info.get('pix_fmt')} {info.get('width')}x{info.get('height')} "
          f"@ {info.get('fps', 0):.3f} fps, {info.get('duration', 0):.3f} s")
    if (info.get("width"), info.get("height")) != (w, h):
        problems.append(f"size {info.get('width')}x{info.get('height')} ≠ canvas {w}x{h}")
    pix = info.get("pix_fmt") or ""
    if not pix.startswith(ALPHA_PIX) and render.suffix != ".mp4":
        problems.append(f"no alpha channel (pix_fmt {info.get('pix_fmt')}) — render with --format mov")
    if meta.get("fps") and abs(info.get("fps", 0) - eval_fps(meta["fps"])) > 0.01:
        problems.append(f"fps {info.get('fps'):.3f} ≠ {meta['fps']}")
    if meta.get("duration") and abs(info.get("duration", 0) - meta["duration"]) > 1.5 / max(1, info.get("fps", 30)):
        problems.append(f"duration {info.get('duration'):.3f} s ≠ {meta['duration']:.3f} s")
    if meta.get("frames"):
        n = count_frames(render)
        if n is not None and n != meta["frames"]:
            problems.append(f"{n} frames ≠ {meta['frames']} — the scene must be EXACTLY {meta['frames']} frames "
                            f"(set data-duration to {(meta['frames'] - 0.5) / eval_fps(meta['fps']):.4f})")

    dur = meta.get("duration") or info.get("duration") or 1.0
    with tempfile.TemporaryDirectory() as tmp:
        first, last = Path(tmp) / "first.png", Path(tmp) / "last.png"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(render), "-frames:v", "1",
                        "-pix_fmt", "rgba", str(first)], check=False)
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-sseof", "-0.2", "-i", str(render), "-update", "1",
                        "-pix_fmt", "rgba", str(last)], check=False)
        from PIL import Image
        for label, p in (("first", first), ("last", last)):
            if meta["layout"] == "scene":
                break  # opaque scenes cut hard into each other: no transparent first/last frame
            if p.exists():
                with Image.open(p) as im:
                    amax = im.getchannel("A").getextrema()[1] if im.mode == "RGBA" else 255
                if amax > 8:
                    problems.append(f"{label} frame is not fully transparent (max alpha {amax})")

        # safe-zone spill: any visible pixel outside the zone (full/split may paint background to the edges)
        spill = 0
        if meta["layout"] not in ("full", "split", "scene"):
            sx0, sy0, sx1, sy1 = meta["safe"]
            for k in range(6):
                t = dur * (k + 0.5) / 6
                fp = Path(tmp) / f"s{k}.png"
                subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.3f}", "-i", str(render),
                                "-frames:v", "1", "-pix_fmt", "rgba", str(fp)], check=False)
                if fp.exists():
                    with Image.open(fp) as im:
                        a = im.getchannel("A")
                        inside = a.crop((sx0, sy0, sx1, sy1)).histogram()
                        total = a.histogram()
                        visible_total = sum(total[17:])
                        visible_inside = sum(inside[17:])
                        spill = max(spill, visible_total - visible_inside)
            if spill > 200:
                problems.append(f"{spill} visible pixels outside the safe zone")

        # contact sheet over the real footage
        sx0, sy0, sx1, sy1 = meta["safe"]
        b0, b1 = meta["caption_band"]
        base = Path(meta["base"])
        bp = probe(base)
        s = bp["width"] / w
        base_chain = "[0:v]null[bb]"
        if meta["layout"] == "split":
            half = bp["height"] // 2
            cy = int(round((meta.get("crop_y") or h * 0.2) * s))
            base_chain = f"[0:v]split[a][b];[b]crop={bp['width']}:{half}:0:{cy}[c];[a][c]overlay=0:{half}[bb]"
        n = 8
        fps = info.get("fps") or 30
        sel = "+".join(f"eq(n,{int((i + 0.5) * dur / n * fps)})" for i in range(n))
        sheet = slot_dir / "check_sheet.jpg"
        graph = (f"{base_chain};[1:v]format=yuva444p10le,scale={bp['width']}:{bp['height']}[o];"
                 f"[bb][o]overlay=0:0:format=auto,"
                 f"drawbox=x={int(sx0 * s)}:y={int(sy0 * s)}:w={int((sx1 - sx0) * s)}:h={int((sy1 - sy0) * s)}:color=red@0.9:t=3,"
                 f"drawbox=x=0:y={int(b0 * s)}:w={bp['width']}:h={int((b1 - b0) * s)}:color=yellow@0.5:t=3,"
                 f"select='{sel}',scale=360:-2,tile=4x2")
        proc = subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{meta['start']:.3f}", "-t", f"{dur:.3f}",
                               "-i", str(base), "-i", str(render), "-filter_complex", graph,
                               "-frames:v", "1", "-update", "1", str(sheet)], capture_output=True, text=True)
        if proc.returncode != 0:
            problems.append(f"contact sheet failed: {proc.stderr.strip()[-300:]}")
        else:
            print(f"contact sheet → {sheet}  (red: safe zone, yellow: caption band) — open it and look")

    if args.motion:
        motion_check(render, slot_dir, info.get("fps") or 30, [float(t) for t in (args.at or "").split(",") if t.strip()])

    if problems:
        for p in problems:
            print(f"  PROBLEM: {p}")
        sys.exit(1)
    if meta["layout"] == "scene":
        print("  checks passed: size, fps, duration, alpha channel (opaque scene: first/last-frame and spill checks skipped — measure bounds yourself)")
    else:
        print("  checks passed: size, fps, duration, alpha, transparent first/last frame, safe zone")


# -------- motion ------------------------------------------------------------------


def read_frames(render: Path, width: int = 540):
    """Yield RGBA frames (numpy, half-ish scale) one at a time."""
    import numpy as np
    info = probe(render)
    w = width
    h = int(round(info["height"] * w / info["width"] / 2)) * 2
    proc = subprocess.Popen(["ffmpeg", "-v", "error", "-i", str(render), "-vf", f"scale={w}:{h}",
                             "-pix_fmt", "rgba", "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
    size = w * h * 4
    try:
        while True:
            buf = proc.stdout.read(size)
            if len(buf) < size:
                break
            yield np.frombuffer(buf, dtype=np.uint8).reshape(h, w, 4)
    finally:
        proc.stdout.close()
        proc.wait()


def motion_profile(frames, fps: float, window_s: float = 0.5) -> tuple[list[float], list[float]]:
    """Per frame: visible fraction of the canvas, and the fraction of visible pixels that differ from
    the frame `window_s` earlier. Comparing across a window (not frame to frame) lets a slow push-in
    of a few percent count as motion."""
    import numpy as np
    k = max(1, int(round(window_s * fps)))
    ring: list = []
    visible, change = [], []
    for f in frames:
        a = f[..., 3]
        vis = a > 16
        nvis = int(vis.sum())
        visible.append(nvis / a.size)
        if len(ring) == k:
            prev = ring.pop(0)
            prem = f[..., :3].astype(np.int16) * a[..., None] // 255
            pprem = prev[..., :3].astype(np.int16) * prev[..., 3:4] // 255
            diff = (np.abs(prem - pprem).max(axis=-1) > 6) | (np.abs(a.astype(np.int16) - prev[..., 3]) > 6)
            change.append(float(diff.sum()) / max(1, nvis))
        else:
            change.append(1.0)          # can't judge the first window: treat as moving
        ring.append(f)
    return visible, change


def dead_holds(visible: list[float], change: list[float], fps: float, min_hold_s: float = 1.0,
               min_visible: float = 0.003, still: float = 0.002) -> list[tuple[float, float]]:
    """Windows (seconds) where a graphic is on screen and nothing in it moves for ≥ min_hold_s."""
    out, run = [], None
    for i, (v, c) in enumerate(zip(visible, change)):
        if v >= min_visible and c < still:
            run = i if run is None else run
        else:
            if run is not None and (i - run) / fps >= min_hold_s:
                out.append((run / fps, i / fps))
            run = None
    if run is not None and (len(visible) - run) / fps >= min_hold_s:
        out.append((run / fps, len(visible) / fps))
    return out


def motion_check(render: Path, slot_dir: Path, fps: float, at: list[float]) -> None:
    import numpy as np
    from PIL import Image, ImageDraw
    frames = list(read_frames(render))
    if not frames:
        print("  motion: could not decode frames")
        return
    visible, change = motion_profile(frames, fps)
    n = len(frames)
    first = next((i for i, v in enumerate(visible) if v > 0.0005), 0)
    last = max((i for i, v in enumerate(visible) if v > 0.0005), default=n - 1)
    rows = [("entrance", list(range(first, min(n, first + 32), 2)))]
    for t in at:
        c = int(round(t * fps))
        rows.append((f"@{t:g}s", [i for i in range(c - 8, c + 10, 2) if 0 <= i < n]))
    rows.append(("exit", list(range(max(0, last - 16), last + 1, 2))))

    tw = 135
    th = int(frames[0].shape[0] * tw / frames[0].shape[1])
    cols = max(len(r[1]) for r in rows)
    sheet = Image.new("RGB", (90 + cols * (tw + 4), len(rows) * (th + 22)), (30, 30, 34))
    d = ImageDraw.Draw(sheet)
    checker = np.indices((th, tw)).sum(axis=0) // 8 % 2
    bg = np.where(checker[..., None] == 1, 70, 52).astype(np.uint8).repeat(3, axis=-1)
    for r, (label, idx) in enumerate(rows):
        y = r * (th + 22)
        d.text((6, y + th // 2), label, fill=(220, 220, 220))
        for c, i in enumerate(idx):
            im = Image.fromarray(frames[i]).resize((tw, th))
            base = Image.fromarray(bg)
            base.paste(im, (0, 0), im)
            sheet.paste(base, (90 + c * (tw + 4), y))
            d.text((90 + c * (tw + 4) + 3, y + th + 4), f"f{i} {i / fps:.2f}s", fill=(170, 170, 170))
    out = slot_dir / "motion_strip.jpg"
    sheet.save(out, quality=85)
    print(f"motion strip → {out}  (rows: {', '.join(r[0] for r in rows)}) — look for anticipation, "
          f"overshoot and settle, and overlap between parts")
    holds = dead_holds(visible, change, fps)
    for a, b in holds:
        print(f"  WARN: dead hold {a:.2f}–{b:.2f} s — nothing moves; add secondary action "
              f"(slow push-in 100→103%, drift, pulse, breathing glow)")
    if not holds:
        print("  motion: no dead holds")


def main() -> None:
    ap = argparse.ArgumentParser(description="Prepare and QA graphic slots")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("prepare")
    p.add_argument("--edit-dir", type=Path, required=True)
    p.add_argument("--slots", type=Path, default=None, help="Default: <edit>/animations/slots.json")
    p.add_argument("--base", type=Path, default=None, help="Default: <edit>/base.mp4")
    p.add_argument("--platform", default=None, help="Safe-zone preset (default: brand.json platform, else from canvas)")
    p.set_defaults(fn=cmd_prepare)
    c = sub.add_parser("check")
    c.add_argument("target", type=Path, help="Slot folder (or a render file with --start)")
    c.add_argument("--start", type=float, default=None)
    c.add_argument("--edit-dir", type=Path, default=None)
    c.add_argument("--layout", choices=LAYOUTS, default=None)
    c.add_argument("--crop-y", type=int, default=None)
    c.add_argument("--platform", default=None)
    c.add_argument("--motion", action="store_true", help="Write motion_strip.jpg and flag dead holds")
    c.add_argument("--at", default=None, help="Landing times in slot seconds for the strip, e.g. 0.9,2.6")
    c.set_defaults(fn=cmd_check)
    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
