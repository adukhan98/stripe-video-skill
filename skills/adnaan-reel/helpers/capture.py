#!/usr/bin/env python3
"""Capture a web page as a tall phone-width screenshot for a browser card (adnaan-reel).

Chrome at 540 px wide @2x → a 1080 px wide PNG (default 2600 CSS px tall → 5200 px), which scenes scroll
inside a browser card. Logs the capture (source URL, owner) via fetch.py log so credits.md lists it.

Default path (v4): puppeteer-core (installed once into <skill>/.cache/node) drives Chrome with a normal desktop
user agent, scrolls the whole page so scroll-reveal sections render, removes cookie/consent banners and fixed
overlays, then screenshots — reel-05's Salesforce page (Akamai "Access Denied" for HeadlessChrome) and
claude.com (content faded in on scroll → a black page) both failed with the plain CLI screenshot.
--simple uses the old one-shot `chrome --headless --screenshot` (now with a desktop user agent too).

  capture.py https://github.com/owner/repo --edit-dir edit --name repo --uploader owner
  capture.py https://example.com --edit-dir edit --name site --height 3200 --wait 12000

--readable (v5, reel-06 — he said the first screenshot text was "way too small to read"): light mode, a NARROW
viewport (330 CSS px @3x) so lines wrap short and text lands at ~45 px when shown ≥ 0.85 in a card; the main element
(--selector, else <article>/<main>/body) → captures/<name>.png, and for every --phrases entry a STRIP of whole lines
around it (--context lines above/below) → captures/<name>_<k>.png (white padded, 32/20 px) plus
captures/<name>.strips.json with each strip's file, source y-range and the phrase's highlight box(es) in strip px —
exactly what M.highlight(card, [x,y,w,h]) takes (scale by the card's width / strip width). Header/stats strips that
are not phrases: crop the full capture with the "lines" in <name>.layout.json.

  capture.py https://x.com/karpathy/status/2109361546505966046 --edit-dir edit --name post --readable \
      --phrases "6B people (~75%|1-2B (~20%)|20M people (0.2%)|~5,000 people" --context 1
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

HELPERS = Path(__file__).resolve().parent
CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
    "google-chrome", "chromium", "chromium-browser",
]


def find_chrome() -> str:
    for c in CHROME_CANDIDATES:
        if Path(c).exists() or shutil.which(c):
            return c
    sys.exit("no Chrome/Chromium found — install Google Chrome or use `npx hyperframes capture`")


UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/129.0.0.0 Safari/537.36")
NODE_DIR = HELPERS.parent / ".cache" / "node"
PUPPETEER = "puppeteer-core@24.10.0"


def browser_capture(chrome: str, url: str, out: Path, w: int, h: int, wait: int) -> bool:
    if not shutil.which("node") or not shutil.which("npm"):
        return False
    if not (NODE_DIR / "node_modules" / "puppeteer-core").exists():
        NODE_DIR.mkdir(parents=True, exist_ok=True)
        r = subprocess.run(["npm", "install", "--silent", "--no-audit", "--no-fund", "--prefix", str(NODE_DIR), PUPPETEER],
                           capture_output=True, text=True)
        if r.returncode != 0:
            print(f"  puppeteer-core install failed ({r.stderr.strip()[-200:]}) — falling back to the CLI screenshot")
            return False
    env = dict(**__import__("os").environ, NODE_PATH=str(NODE_DIR / "node_modules"))
    r = subprocess.run(["node", str(HELPERS / "capture_page.cjs"), chrome, url, str(out), str(w), str(h), str(wait)],
                       capture_output=True, text=True, timeout=240, env=env)
    if r.returncode != 0:
        print(f"  browser capture failed: {r.stderr.strip()[-200:]}")
    return out.exists()


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("url")
    ap.add_argument("--edit-dir", type=Path, required=True)
    ap.add_argument("--name", required=True, help="output file stem in edit/captures/")
    ap.add_argument("--height", type=int, default=2600, help="CSS px (output is 2x)")
    ap.add_argument("--width", type=int, default=540, help="CSS px (output is 2x)")
    ap.add_argument("--wait", type=int, default=9000, help="virtual time budget, ms")
    ap.add_argument("--uploader", default="", help="owner shown in credits")
    ap.add_argument("--title", default="")
    ap.add_argument("--no-log", action="store_true")
    ap.add_argument("--simple", action="store_true", help="one-shot CLI screenshot (no scroll / banner removal)")
    ap.add_argument("--readable", action="store_true", help="light, narrow @3x capture + one readable strip per phrase")
    ap.add_argument("--phrases", default="", help="'|'-separated phrases to cut strips around (with --readable)")
    ap.add_argument("--context", type=int, default=1, help="whole lines kept above/below each phrase (with --readable)")
    ap.add_argument("--selector", default="", help="element to capture (with --readable; default article/main/body)")
    ap.add_argument("--narrow", type=int, default=330, help="CSS width for --readable (output ≈ 3x)")
    a = ap.parse_args()
    if a.readable:
        return readable(a)
    out = a.edit_dir.resolve() / "captures" / f"{a.name}.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.unlink(missing_ok=True)
    chrome = find_chrome()
    if a.simple or not browser_capture(chrome, a.url, out, a.width, a.height, a.wait):
        subprocess.run([chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=2",
                        f"--user-agent={UA}", f"--window-size={a.width},{a.height}", f"--virtual-time-budget={a.wait}",
                        f"--screenshot={out}", a.url], capture_output=True, timeout=180)
    if not out.exists():
        sys.exit(f"capture failed: {a.url}")
    print(f"→ {out}")
    if not a.no_log:
        subprocess.run(["uv", "run", "--project", str(HELPERS.parent), str(HELPERS / "fetch.py"), "log", str(out),
                        "--edit-dir", str(a.edit_dir), "--url", a.url, "--title", a.title or a.name,
                        "--uploader", a.uploader or a.url, "--rights", "commentary",
                        "--purpose", "page capture shown in a browser card"], check=False)


def stitch_tiles(tiles: list[Path], out: Path) -> None:
    """capture_readable.cjs writes the page as ≤ 1200-CSS-px tiles (one giant screenshot repeats past Chrome's texture
    limit); stack them into `out`. Two identical, non-blank neighbouring tiles mean the page did not scroll/render under
    the clip — fail loudly instead of cutting strips from a repeated image."""
    import hashlib
    from PIL import Image, ImageStat
    ims = [Image.open(t).convert("RGB") for t in tiles]
    prev = None
    for t, im in zip(tiles, ims):
        h = hashlib.sha1(im.tobytes()).hexdigest()
        flat = max(ImageStat.Stat(im).stddev) < 2.0          # an empty band of page can legitimately repeat
        if h == prev and not flat and im.height > 200:
            sys.exit(f"capture repeated itself at {t.name}: the page did not render under the clip — try --selector or --wait")
        prev = h
    W = max(im.width for im in ims)
    sheet = Image.new("RGB", (W, sum(im.height for im in ims)), "white")
    y = 0
    for im in ims:
        sheet.paste(im, (0, y))
        y += im.height
    sheet.save(out)
    for t in tiles:
        t.unlink(missing_ok=True)


def readable(a: argparse.Namespace) -> None:
    import json
    from PIL import Image
    caps = a.edit_dir.resolve() / "captures"
    caps.mkdir(parents=True, exist_ok=True)
    out = caps / f"{a.name}.png"
    out.unlink(missing_ok=True)
    phrases = [x for x in a.phrases.split("|") if x.strip()]
    if not browser_ready():
        sys.exit("--readable needs node + puppeteer-core (installed on the first plain capture)")
    env = dict(**__import__("os").environ, NODE_PATH=str(NODE_DIR / "node_modules"))
    r = subprocess.run(["node", str(HELPERS / "capture_readable.cjs"), find_chrome(), a.url, str(out), str(a.narrow),
                        a.selector, json.dumps(phrases)], capture_output=True, text=True, timeout=240, env=env)
    lay_p = out.with_suffix(".layout.json")
    if r.returncode != 0 or not lay_p.exists():
        sys.exit(f"readable capture failed: {r.stderr.strip()[-300:]}")
    lay = json.loads(lay_p.read_text())
    if lay.get("tiles"):
        stitch_tiles([Path(t) for t in lay["tiles"]], out)
    if not out.exists():
        sys.exit("readable capture failed: no image written")
    img = Image.open(out).convert("RGB")
    lines, pad_x, pad_y, strips = lay["lines"], 32, 20, []
    for k, ph in enumerate(phrases, 1):
        boxes = lay["found"].get(ph)
        if not boxes:
            print(f"  phrase not found: {ph!r}")
            continue
        merged: list[list[int]] = []          # one box per line (a phrase can span several text nodes)
        for b in sorted(boxes, key=lambda b: (b[1], b[0])):
            m = next((x for x in merged if abs(x[1] - b[1]) < 12), None)
            if m:
                x1 = max(m[0] + m[2], b[0] + b[2]); m[0] = min(m[0], b[0]); m[2] = x1 - m[0]; m[3] = max(m[3], b[3])
            else:
                merged.append(list(b))
        boxes = merged
        y_top, y_bot = min(b[1] for b in boxes), max(b[1] + b[3] for b in boxes)
        idx = [i for i, l in enumerate(lines) if l[1] + l[3] > y_top and l[1] < y_bot] or [0]
        i0, i1 = max(0, idx[0] - a.context), min(len(lines) - 1, idx[-1] + a.context)
        y0 = max(0, lines[i0][1] - 6)
        y1 = min(img.height, lines[i1][1] + lines[i1][3] + 6)
        if i0 > 0:   # never cut into the line above (descenders)
            y0 = max(y0, lines[i0 - 1][1] + lines[i0 - 1][3] + 2)
        if i1 < len(lines) - 1:
            y1 = min(y1, lines[i1 + 1][1] - 2)
        crop = img.crop((0, y0, img.width, y1))
        strip = Image.new("RGB", (crop.width + 2 * pad_x, crop.height + 2 * pad_y), "white")
        strip.paste(crop, (pad_x, pad_y))
        f = caps / f"{a.name}_{k}.png"
        strip.save(f)
        strips.append({"phrase": ph, "file": f.name, "size": list(strip.size), "source_y": [y0, y1],
                       "highlight": [[b[0] + pad_x, b[1] - y0 + pad_y, b[2], b[3]] for b in boxes]})
        print(f"  {f.name}: {strip.size[0]}x{strip.size[1]}  highlight {strips[-1]['highlight']}  ← {ph!r}")
    (caps / f"{a.name}.strips.json").write_text(json.dumps(strips, indent=1))
    print(f"→ {out} ({img.width}x{img.height}) + {len(strips)} strip(s); show strips at ≥ 0.85 scale in a card")
    if not a.no_log:
        for f in [out] + [caps / s_["file"] for s_ in strips]:
            subprocess.run(["uv", "run", "--project", str(HELPERS.parent), str(HELPERS / "fetch.py"), "log", str(f),
                            "--edit-dir", str(a.edit_dir), "--url", a.url, "--title", f"{a.title or a.name} ({f.stem})",
                            "--uploader", a.uploader or a.url, "--rights", "commentary",
                            "--purpose", "readable page strip shown in a card"], check=False, capture_output=True)


def browser_ready() -> bool:
    if not shutil.which("node"):
        return False
    if not (NODE_DIR / "node_modules" / "puppeteer-core").exists():
        NODE_DIR.mkdir(parents=True, exist_ok=True)
        r = subprocess.run(["npm", "install", "--silent", "--no-audit", "--no-fund", "--prefix", str(NODE_DIR), PUPPETEER],
                           capture_output=True, text=True)
        return r.returncode == 0
    return True


if __name__ == "__main__":
    main()
