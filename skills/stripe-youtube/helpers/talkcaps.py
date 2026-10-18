"""Full-coverage TALK captions: every full-frame talk window gets kinetic captions for ALL his words.

Adnaan, IMG_2533 (2026-10-17): "for all the ones where I am full screen, add the captions there". This replaces the old
"one sparse accent per 45–90 s" rule: every talk window (compose.py windows with layout "talk") gets one generated
talk_overlay scene (cNN_talk) built from templates/scenes/talk_captions.html — white Inter Tight in a left column, one mint
hero word per phrase, words popping on their spoken times. Board / screen windows get no captions (the SRT covers them).

How the words become captions:
  - words = transcripts/CAM.json mapped through timeline.json (only words inside kept ranges);
  - sentences break at . ? !, at pauses > 0.4 s and before a capitalised sentence start the transcript missed;
  - a sentence longer than 7 words splits at its best sense point (after a comma, before a conjunction, at a breath, never
    right after a weak word like "the" / "to"), recursively; a lone trailing word joins the phrase before it;
  - lines of 2–3 words; one hero per phrase (layout heroes first, else the longest content word of 4+ letters);
  - each phrase fits its own font size (<= 110 px, widest line <= 620 px), centred on captions.y.

layout.json (all optional):
    "captions": {"y": 280,            # centre line of the caption column: a calm area of HIS background (sky, wall)
                 "x": 96,             # left edge of the column (keep it beside his head, never over his face)
                 "heroes": ["good", "habits."],          # words that win the mint hero slot (lower case, as spoken)
                 "fix": [["anything", "left.", "less."]]} # [previous word, word, replacement] for transcript slips

Writes animations/scenes.json (all talk_overlay scenes are replaced; the first run keeps scenes_pre_talkcaps.json),
scaffolds each cNN_talk with board.py prepare and writes its hf/index.html. Re-run after every change to the cut,
transcripts/CAM.json or the opaque scenes; then render: `board.py render --edit-dir E --only c01_talk,c02_talk,…`.

    python helpers/talkcaps.py --edit-dir E [--dry-run]
"""

from __future__ import annotations

import argparse
import html as htmllib
import json
import math
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import board  # noqa: E402
import compose  # noqa: E402

FPS = 30
F = 1 / FPS
TEMPLATE = board.STARTERS / "talk_captions.html"
RULE = 0.35          # the last word lands at least this long before the exit starts
MIN_WINDOW = 15      # frames: a talk window shorter than 0.5 s gets no captions
STOP = set("""a an the and or but so if of to in on at for with from by as is are was were be been being am i you he she
it we they me my your our their this that these those there here then than just really actually very kind like do does did
dont don't can't cant can could would should will its it's i'm im you're youre that's thats what when where who how why
about into out up down over more most some any all not no yes also even still because which while get got going
came come comes makes make looked look looks through gives give keeps keep takes take know think ahead trust
said says want wants thing things something""".split())
SENT_START = {"If", "And", "But", "So", "You", "The", "That's", "This", "It's", "When", "Then"}
CONJ = {"and", "but", "so", "because", "that", "which", "when", "if", "then", "or", "while", "where"}
WEAK = {"a", "an", "the", "to", "of", "for", "and", "but", "so", "in", "on", "at", "with", "my", "your", "is", "are", "i"}


def norm(w: str) -> str:
    return re.sub(r"[^a-z']", "", w.lower())


def load_words(edit: Path, fix: dict) -> list[tuple[str, float, float]]:
    """(word, out_start, out_end) for every transcript word inside a kept range."""
    segs = json.loads((edit / "timeline.json").read_text())["segments"]

    def out(t: float) -> float:
        for s in segs:
            if t < s["start"] - 1e-6:
                return s["out_start"]
            if t <= s["end"] + 1e-6:
                return s["out_start"] + (t - s["start"])
        return segs[-1]["out_start"] + segs[-1]["out_duration"]

    words = [w for w in json.loads((edit / "transcripts" / "CAM.json").read_text())["words"] if w.get("type", "word") == "word"]
    kept = [w for w in words if any(s["start"] - 0.08 <= w["start"] < s["end"] - 0.05 for s in segs)]
    res = [(w["text"], out(w["start"]), out(w["end"])) for w in kept]
    return [(fix.get((res[i - 1][0] if i else "", w), w), a, b) for i, (w, a, b) in enumerate(res)]


def split_sense(ws: list) -> list[list]:
    """a sentence longer than 7 words splits at its best sense point near the middle, recursively"""
    n = len(ws)
    if n <= 7:
        return [ws]
    best, bi = None, None
    for i in range(3, n - 2):
        sc = 3 * (ws[i - 1][0][-1] in ",;:") + 2 * (norm(ws[i][0]) in CONJ) + (ws[i][1] - ws[i - 1][2] > 0.2)
        sc -= 2.5 * (norm(ws[i - 1][0]) in WEAK) + 0.35 * abs(i - n / 2)
        if best is None or sc > best:
            best, bi = sc, i
    return split_sense(ws[:bi]) + split_sense(ws[bi:])


def phrases_of(words: list) -> list[list]:
    sents, cur = [], []
    for w, s, e in words:
        if cur:
            pw, _, pe = cur[-1]
            if pw[-1] in ".?!" or s - pe > 0.4 or (len(cur) >= 2 and w in SENT_START):
                sents.append(cur)
                cur = []
        cur.append((w, s, e))
    if cur:
        sents.append(cur)
    ph = [u for sent in sents for u in split_sense(sent)]
    for k in range(len(ph) - 1, 0, -1):                     # a lone word joins the phrase before it
        if len(ph[k]) == 1 and len(ph[k - 1]) < 7 and ph[k][0][1] - ph[k - 1][-1][2] < 0.6:
            ph[k - 1] += ph.pop(k)
    return ph


def lines_of(ph: list) -> list[list]:
    n = len(ph)
    cut = {1: [1], 2: [2], 3: [3], 4: [2, 2], 5: [3, 2], 6: [3, 3], 7: [3, 2, 2], 8: [3, 3, 2], 9: [3, 3, 3]}.get(
        n, [3] * (n // 3) + ([n % 3] if n % 3 else []))
    out, i = [], 0
    for c in cut:
        out.append(ph[i:i + c])
        i += c
    return out


def hero_of(ph: list, heroes: set) -> str | None:
    for w, *_ in ph:
        if w.lower() in heroes:
            return w
    cands = [w for w, *_ in ph if norm(w) not in STOP and len(norm(w)) >= 4]
    return max(cands, key=lambda w: len(norm(w))) if cands else None


def schedule(flat: list, dur: float) -> list[float]:
    """pop times: 0.1 s before each spoken word, >= 2 frames apart, all landed RULE s before the exit"""
    last = dur - 6 * F - RULE
    t = [max(s - 0.10, 0.10) for _, s, _ in flat]
    for i in range(1, len(t)):
        t[i] = max(t[i], t[i - 1] + 2 * F)
    t[-1] = min(t[-1], last)
    for i in range(len(t) - 2, -1, -1):
        t[i] = min(t[i], t[i + 1] - 2 * F)
    return [round(max(x, 0.03), 2) for x in t]


def page(cid: str, words: list, frames: int, heroes: set, x: int, y: int) -> tuple[str, int, int]:
    dur = frames / FPS
    ph = phrases_of(words)
    flat = [w for p in ph for w in p]
    t = schedule(flat, dur)
    i, blocks, starts = 0, [], []
    for p in ph:
        hero, used, rows = hero_of(p, heroes), False, []
        starts.append(t[i])
        for li, ln in enumerate(lines_of(p)):
            spans = []
            for w, _, _ in ln:
                is_hero = w == hero and not used
                used |= is_hero
                spans.append(f'<span class="kw w7{" mint hero" if is_hero else ""}" data-t="{t[i]:.2f}">{htmllib.escape(w)}</span>')
                i += 1
            rows.append(f'<div class="ln l{li % 2}">' + " ".join(spans) + "</div>")
        blocks.append('        <div class="ph">\n          ' + "\n          ".join(rows) + "\n        </div>")
    out = (TEMPLATE.read_text().replace("{{ID}}", cid).replace("{{DURATION}}", f"{math.floor(dur * 1000 - 1) / 1000:.3f}")
           .replace("{{PHRASES}}", "\n".join(blocks)).replace("{{STARTS}}", json.dumps(starts))
           .replace("{{X}}", str(x)).replace("{{Y}}", str(y)))
    return out, len(ph), len(flat)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--edit-dir", required=True, type=Path)
    ap.add_argument("--dry-run", action="store_true", help="print the windows and phrases, write nothing")
    a = ap.parse_args()
    edit = a.edit_dir.resolve()
    d = compose.load(edit)
    cfg = d["layout"].get("captions") or {}
    fix = {(p, w): r for p, w, r in cfg.get("fix", [])}
    heroes = {h.lower() for h in cfg.get("heroes", [])}
    x, y = int(cfg.get("x", 96)), int(cfg.get("y", 280))
    words = load_words(edit, fix)

    sj = edit / "animations" / "scenes.json"
    doc = d["scenes"] if sj.exists() else {"theme": d["theme"], "look": "v7", "scenes": []}
    bak = edit / "animations" / "scenes_pre_talkcaps.json"
    if sj.exists() and not bak.exists() and not a.dry_run:
        bak.write_text(json.dumps(doc, indent=1))
    dropped = [s["id"] for s in doc["scenes"] if s["type"] == "talk_overlay"]
    keep = [s for s in doc["scenes"] if s["type"] != "talk_overlay"]
    d["scenes"] = {**doc, "scenes": keep}
    new, pages = [], {}
    talk = [w for w in compose.windows(d) if w["layout"] == "talk" and w["f1"] - w["f0"] >= MIN_WINDOW]
    for k, w in enumerate(talk, 1):
        a0, b0 = w["start"], w["end"]
        ws = [(t, s - a0, e - a0) for t, s, e in words if a0 - 0.02 <= s < b0 - 0.15]
        if not ws:
            continue
        cid = f"c{k:02d}_talk"
        frames = w["f1"] - w["f0"]
        pages[cid], nph, nw = page(cid, ws, frames, heroes, x, y)
        new.append({"id": cid, "type": "talk_overlay", "start": round(a0, 4), "duration": round(frames / FPS, 4),
                    "hue": "mint", "assets": [], "generated": "talkcaps",
                    "brief": "Full-coverage talk captions, generated by helpers/talkcaps.py — re-run it instead of editing."})
        print(f"{cid}: {a0:7.2f}–{b0:7.2f} ({frames} f)  {nph} phrases, {nw} words")
        if a.dry_run:
            for p in phrases_of(ws):
                print("      " + " / ".join(" ".join(w for w, *_ in ln) for ln in lines_of(p)))
    if dropped:
        print(f"{'would replace' if a.dry_run else 'replaced'} talk_overlay scenes: {', '.join(dropped)}")
    if a.dry_run:
        return
    doc["scenes"] = sorted(keep + new, key=lambda s: s["start"])
    sj.parent.mkdir(parents=True, exist_ok=True)
    sj.write_text(json.dumps(doc, indent=1))
    if new:
        board.prepare(edit, ",".join(s["id"] for s in new))
        for cid, html in pages.items():
            (edit / "animations" / cid / "hf" / "index.html").write_text(html)
            board.brand.install(edit / "animations" / cid / "hf")  # the page was rewritten: link brand.css again
            (edit / "animations" / cid / "beats.json").write_text("[]\n")
        print(f"→ render: board.py render --edit-dir {edit} --only {','.join(pages)}")


if __name__ == "__main__":
    main()
