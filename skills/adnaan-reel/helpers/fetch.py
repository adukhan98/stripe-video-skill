"""Download video/audio assets with yt-dlp — the only way this skill downloads media.

Every download lands in <edit>/downloads/, is recorded in downloads/manifest.json
with its source URL, uploader and licence, and is cached: asking for the same
URL (and section) twice returns the file already on disk.

  url      download one link (footage the user owns, licensed stock, a reference
           video, a music bed with --audio-only). --section grabs just a slice.
  search   find b-roll on YouTube. Creative Commons only by default: results are
           filtered with YouTube's CC filter, then every candidate's licence is
           verified from its metadata. Writes a numbered thumbnail contact sheet.
  find     find the REAL clip of something the speaker talks about (a launch film,
           a keynote moment, a news clip). Any licence; official channels rank
           first (--official "OpenAI" + YouTube's verified badge). Download the
           pick with `url --rights commentary --section a-b`.
  log      record a media file that did not come through yt-dlp (a screenshot, a
           `hyperframes capture` plate, an official logo) so credits.md covers it.
  credits  write <edit>/credits.md for third-party media the EDL actually uses.

Rights classes: cc-by / cc0 (usable), user-provided (the user's own link or file),
commentary (a third-party clip the user approved at the check-in for commentary use:
short, framed, on-screen source label), cc-restricted / other / unknown (flagged).

yt-dlp resolution: $VIDEO_EDIT_YTDLP, else a system yt-dlp >= 2025.11.12, else
`uvx --from "yt-dlp[default]@latest" yt-dlp` (no install needed when uv exists).
YouTube needs a JavaScript runtime since late 2025: Deno is used when present,
otherwise Node >= 22 is enabled automatically.

Usage:
    python helpers/fetch.py url <URL> --edit-dir <edit> [--purpose broll] [--section 1:05-1:20]
    python helpers/fetch.py url <URL> --edit-dir <edit> --audio-only --purpose music
    python helpers/fetch.py search "city skyline night drone" --edit-dir <edit> [--n 8] [--max-duration 300]
    python helpers/fetch.py find "openai dots launch film" --official OpenAI --edit-dir <edit>
    python helpers/fetch.py url <URL> --edit-dir <edit> --rights commentary --section 0:12-0:18
    python helpers/fetch.py log <file> --edit-dir <edit> --url <source page> --rights commentary --purpose screenshot
    python helpers/fetch.py tweet https://x.com/<user>/status/<id> --edit-dir <edit> --check "phrase he shows"
    python helpers/fetch.py credits --edit-dir <edit> [--edl <edit>/edl.json]
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import quote_plus

MIN_YTDLP = (2025, 11, 12)
CC_FILTER = "EgIwAQ%3D%3D"   # YouTube search filter: Creative Commons
USABLE = {"cc-by", "cc-by-sa", "cc0", "user-provided", "commentary", "official", "open-source"}
RIGHTS = ("user-provided", "commentary")
LOG_RIGHTS = RIGHTS + ("cc-by", "cc-by-sa", "cc0", "official", "open-source")   # official: a brand's own logo, shown unaltered; open-source: MIT icon sets


# -------- yt-dlp resolution ---------------------------------------------------


def parse_version(text: str) -> tuple[int, ...]:
    nums = re.findall(r"\d+", text.strip().splitlines()[0] if text.strip() else "")
    return tuple(int(n) for n in nums[:4]) if nums else (0,)


def _version_of(cmd: list[str]) -> tuple[int, ...]:
    try:
        out = subprocess.run(cmd + ["--version"], capture_output=True, text=True, timeout=180)
        return parse_version(out.stdout) if out.returncode == 0 else (0,)
    except (OSError, subprocess.TimeoutExpired):
        return (0,)


def resolve_ytdlp() -> tuple[list[str], tuple[int, ...], str]:
    """(command, version, origin)."""
    env = os.environ.get("VIDEO_EDIT_YTDLP")
    if env:
        cmd = shlex.split(env)
        return cmd, _version_of(cmd), "env"
    system = shutil.which("yt-dlp")
    sys_version = _version_of([system]) if system else (0,)
    if system and sys_version >= MIN_YTDLP:
        return [system], sys_version, "system"
    uvx = shutil.which("uvx")
    if uvx:
        cmd = [uvx, "--from", "yt-dlp[default]@latest", "yt-dlp"]
        v = _version_of(cmd)
        if v >= MIN_YTDLP:
            if system:
                print(f"note: system yt-dlp {'.'.join(map(str, sys_version))} is too old for YouTube; "
                      f"using uvx yt-dlp {'.'.join(map(str, v))}. Upgrade with: brew upgrade yt-dlp",
                      file=sys.stderr)
            return cmd, v, "uvx"
    if system:
        print(f"WARNING: yt-dlp {'.'.join(map(str, sys_version))} is older than 2025.11.12 — YouTube "
              f"downloads will likely fail. Upgrade: brew upgrade yt-dlp  (or pip install -U 'yt-dlp[default]')",
              file=sys.stderr)
        return [system], sys_version, "system-outdated"
    sys.exit("yt-dlp not found. Install it (macOS: brew install yt-dlp deno; anywhere: "
             "pip install -U 'yt-dlp[default]'), or install uv so it can run via uvx.")


def _node_major() -> int:
    node = shutil.which("node")
    if not node:
        return 0
    try:
        out = subprocess.run([node, "--version"], capture_output=True, text=True, timeout=10).stdout
        return int(re.findall(r"\d+", out)[0])
    except (OSError, IndexError, ValueError, subprocess.TimeoutExpired):
        return 0


def runtime_flags(version: tuple[int, ...], origin: str) -> list[str]:
    """JS runtime flags for YouTube's challenges (only on yt-dlp versions that know them)."""
    if version < MIN_YTDLP:
        return []
    flags: list[str] = []
    if not shutil.which("deno") and _node_major() >= 22:
        flags += ["--js-runtimes", "node"]
    if origin in ("system", "env"):
        # Homebrew and distro builds do not bundle the challenge solver scripts; allow
        # yt-dlp to fetch them from its own GitHub repo when it needs them.
        flags += ["--remote-components", "ejs:github"]
    return flags


class YtDlp:
    def __init__(self) -> None:
        self.cmd, self.version, self.origin = resolve_ytdlp()
        self.flags = runtime_flags(self.version, self.origin)

    def run(self, args: list[str], timeout: int = 3600) -> subprocess.CompletedProcess:
        return subprocess.run(self.cmd + self.flags + args, capture_output=True, text=True, timeout=timeout)

    def json(self, args: list[str], timeout: int = 300) -> dict:
        proc = self.run(args, timeout=timeout)
        if proc.returncode != 0:
            raise RuntimeError(_explain(proc.stderr))
        return json.loads(proc.stdout)


def _explain(stderr: str) -> str:
    tail = "\n".join(l for l in stderr.strip().splitlines()[-6:])
    hints = []
    if "Sign in to confirm" in stderr or "not a bot" in stderr:
        hints.append("YouTube wants a signed-in session. Only if the user explicitly agrees, retry with "
                     "VIDEO_EDIT_YTDLP='yt-dlp --cookies-from-browser chrome' (reads their browser cookies).")
    if "Requested format is not available" in stderr:
        hints.append("Try --max-height 720, or update yt-dlp.")
    if "HTTP Error 403" in stderr or "nsig" in stderr or "challenge" in stderr.lower():
        hints.append("Usually an outdated yt-dlp or a missing JS runtime: brew upgrade yt-dlp && brew install deno.")
    if "Private video" in stderr or "members-only" in stderr:
        hints.append("The video is private/members-only — ask the user for the file instead.")
    return tail + ("\n  hint: " + "\n  hint: ".join(hints) if hints else "")


# -------- licence ---------------------------------------------------------------


def classify_license(info: dict) -> str:
    """cc-by | cc0 | cc-restricted (NC/ND: not for commercial or edited use) | other | unknown."""
    lic = (info.get("license") or "").strip().lower()
    if not lic:
        return "unknown"
    if "creative commons" in lic or lic.startswith(("cc", "by")):
        if "zero" in lic or "cc0" in lic or "public domain" in lic:
            return "cc0"
        if re.search(r"\b(nc|nd)\b|non-?commercial|no-?deriv", lic):
            return "cc-restricted"
        return "cc-by"
    if "public domain" in lic:
        return "cc0"
    return "other"


# -------- manifest ----------------------------------------------------------------


def downloads_dir(edit_dir: Path) -> Path:
    d = edit_dir / "downloads"
    d.mkdir(parents=True, exist_ok=True)
    return d


def load_manifest(edit_dir: Path) -> dict:
    p = downloads_dir(edit_dir) / "manifest.json"
    if p.exists():
        return json.loads(p.read_text())
    return {"items": []}


def save_manifest(edit_dir: Path, manifest: dict) -> None:
    (downloads_dir(edit_dir) / "manifest.json").write_text(json.dumps(manifest, indent=2))


def slugify(text: str, n: int = 40) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", (text or "").lower()).strip("-")
    return (s[:n].rstrip("-") or "media")


def parse_section(spec: str) -> tuple[float, float]:
    """'1:05-1:20' / '65-80' / '00:01:05.5-00:01:20' → seconds."""
    def secs(t: str) -> float:
        parts = [float(p) for p in t.strip().split(":")]
        v = 0.0
        for p in parts:
            v = v * 60 + p
        return v
    a, b = spec.split("-", 1)
    start, end = secs(a), secs(b)
    if end <= start:
        raise ValueError(f"section end must be after start: {spec}")
    return start, end


def probe(path: Path) -> dict:
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries",
             "format=duration:stream=codec_type,width,height,avg_frame_rate", "-of", "json", str(path)],
            capture_output=True, text=True, check=True,
        )
        data = json.loads(out.stdout)
    except (subprocess.CalledProcessError, json.JSONDecodeError, OSError):
        return {}
    v = next((s for s in data.get("streams", []) if s.get("codec_type") == "video"), {})
    return {
        "duration": round(float(data.get("format", {}).get("duration", 0) or 0), 3),
        "width": v.get("width"), "height": v.get("height"), "fps": v.get("avg_frame_rate"),
        "has_audio": any(s.get("codec_type") == "audio" for s in data.get("streams", [])),
    }


# -------- url ---------------------------------------------------------------------


def download(
    url: str,
    edit_dir: Path,
    purpose: str = "broll",
    section: str | None = None,
    audio_only: bool = False,
    max_height: int = 1080,
    name: str | None = None,
    user_provided: bool = True,
    ytdlp: YtDlp | None = None,
    rights: str | None = None,
) -> dict:
    y = ytdlp or YtDlp()
    info = y.json(["--dump-single-json", "--no-playlist", "--skip-download", url])
    vid = str(info.get("id") or slugify(url))
    sec = parse_section(section) if section else None
    manifest = load_manifest(edit_dir)
    key = {"extractor": info.get("extractor_key"), "id": vid,
           "section": list(sec) if sec else None, "audio_only": audio_only}
    for item in manifest["items"]:
        if all(item.get(k) == v for k, v in key.items()) and Path(item["file"]).exists():
            print(f"cached: {item['file']}")
            return item

    base = f"{slugify(name or info.get('title') or vid)}-{vid}"
    if sec:
        base += f"_{sec[0]:g}-{sec[1]:g}"
    out_tmpl = str(downloads_dir(edit_dir) / f"{base}.%(ext)s")
    args = ["--no-playlist", "--no-overwrites", "-o", out_tmpl, "--print", "after_move:filepath"]
    if audio_only:
        args += ["-f", "ba/b", "-x"]
    else:
        args += ["-f", "bv*+ba/b", "-S", f"res:{max_height},+codec:avc:m4a", "--merge-output-format", "mp4"]
    if sec:
        args += ["--download-sections", f"*{sec[0]:.2f}-{sec[1]:.2f}", "--force-keyframes-at-cuts"]
    print(f"downloading {url}" + (f" [{section}]" if section else "") + f" via yt-dlp {'.'.join(map(str, y.version))} ({y.origin})")
    proc = y.run(args + [url])
    if proc.returncode != 0:
        raise RuntimeError(_explain(proc.stderr))
    lines = [l for l in proc.stdout.strip().splitlines() if l.strip()]
    if not lines or not Path(lines[-1]).exists():
        raise RuntimeError(f"yt-dlp finished but no file was reported\n{_explain(proc.stderr)}")
    path = Path(lines[-1]).resolve()

    licence = classify_license(info)
    item = {
        **key,
        "url": info.get("webpage_url") or url,
        "title": info.get("title"),
        "uploader": info.get("uploader") or info.get("channel"),
        "uploader_url": info.get("uploader_url") or info.get("channel_url"),
        "license": info.get("license"),
        "license_class": licence,
        "rights": item_rights(licence, user_provided, rights),
        "purpose": purpose,
        "file": str(path),
        "downloaded_at": dt.datetime.now().isoformat(timespec="seconds"),
        **probe(path),
    }
    manifest["items"].append(item)
    save_manifest(edit_dir, manifest)
    print(f"saved: {path}")
    dims = f" {item['width']}x{item['height']}" if item.get("width") else ""
    print(f"  {item.get('duration')}s{dims}  licence: {item['license'] or 'none listed'} → {item['rights']}")
    if item["rights"] == "cc-restricted":
        print("  WARNING: NonCommercial/NoDerivatives licence — not usable in a brand/commercial edit.")
    elif item["rights"] == "user-provided":
        print("  note: not Creative Commons. Use it only if the user owns it or holds the rights.")
    elif item["rights"] == "commentary":
        print("  note: commentary clip — keep it short (2–6 s), framed, muted or ducked, with an on-screen "
              f"source label ('{item.get('uploader') or 'source'}').")
    return item


def item_rights(licence: str, user_provided: bool, rights: str | None = None) -> str:
    """CC licences always win; otherwise an explicit rights class, else user-provided / the raw licence."""
    if licence in ("cc-by", "cc0"):
        return licence
    if rights:
        return rights
    return "user-provided" if user_provided else licence


# -------- search ------------------------------------------------------------------


def search(
    query: str,
    edit_dir: Path,
    n: int = 8,
    cc_only: bool = True,
    max_duration: float | None = None,
    min_height: int = 720,
    official: str | None = None,
) -> list[dict]:
    y = YtDlp()
    url = f"https://www.youtube.com/results?search_query={quote_plus(query)}"
    if cc_only:
        url += f"&sp={CC_FILTER}"
    data = y.json(["--flat-playlist", "--dump-single-json", "--playlist-end", str(n * 3), url])
    entries = [e for e in data.get("entries") or [] if e.get("id")]
    if max_duration:
        entries = [e for e in entries if (e.get("duration") or 0) <= max_duration]

    def verify(e: dict) -> dict | None:
        try:
            info = y.json(["--dump-single-json", "--no-playlist", "--skip-download",
                           f"https://www.youtube.com/watch?v={e['id']}"], timeout=180)
        except Exception:
            return None
        height = max((f.get("height") or 0) for f in info.get("formats") or [{}])
        return {
            "id": e["id"], "url": info.get("webpage_url"), "title": info.get("title"),
            "uploader": info.get("uploader") or info.get("channel"), "duration": info.get("duration"),
            "height": height, "license": info.get("license"), "license_class": classify_license(info),
            "verified": bool(info.get("channel_is_verified")), "views": info.get("view_count"),
            "thumbnail": info.get("thumbnail") or ((e.get("thumbnails") or [{}])[-1].get("url")),
        }

    with ThreadPoolExecutor(max_workers=4) as pool:
        results = [r for r in pool.map(verify, entries[: n * 2]) if r]
    if cc_only:
        results = [r for r in results if r["license_class"] in ("cc-by", "cc0")]
    results = [r for r in results if (r["height"] or 0) >= min_height]
    if not cc_only:
        results = rank_official(results, official)
    results = results[:n]

    sdir = downloads_dir(edit_dir) / "search"
    sdir.mkdir(parents=True, exist_ok=True)
    slug = slugify(query, 32)
    (sdir / f"{slug}.json").write_text(json.dumps({"query": query, "cc_only": cc_only, "results": results}, indent=2))
    sheet = contact_sheet(results, sdir / f"{slug}.jpg")

    print(f"{len(results)} result(s) for '{query}'" + (" (Creative Commons, licence verified)" if cc_only
          else " (any licence — official channels first)"))
    for i, r in enumerate(results, 1):
        mark = " ✓official" if r.get("official") else (" ✓verified" if r.get("verified") else "")
        print(f"  [{i}] {r['duration'] or '?':>5}s {r['height']}p  {r['license_class']:6s}  {r['uploader'] or '?'}{mark} — "
              f"{(r['title'] or '')[:60]}\n       {r['url']}")
    if sheet:
        print(f"  thumbnails: {sheet}")
    if cc_only:
        print("Pick with the thumbnails + titles, then: fetch.py url <URL> --purpose broll --section a-b --found-by-search")
    else:
        print("Pick with the thumbnails + titles (prefer ✓official), find the exact seconds with timeline_view.py, then:\n"
              "  fetch.py url <URL> --purpose reference --rights commentary --section a-b")
    return results


def rank_official(results: list[dict], official: str | None) -> list[dict]:
    """Official uploads first: the named owner's channel, then verified channels, then the rest
    (stable within each group, so YouTube's relevance order survives)."""
    want = re.sub(r"[^a-z0-9]", "", (official or "").lower())
    for r in results:
        who = re.sub(r"[^a-z0-9]", "", (r.get("uploader") or "").lower())
        r["official"] = bool(want) and (want in who or (bool(who) and who in want))
    return sorted(results, key=lambda r: (not r["official"], not r.get("verified")))


def contact_sheet(results: list[dict], out: Path) -> Path | None:
    if not results:
        return None
    try:
        import io
        import requests
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        return None
    tw, th, cols = 384, 216, 4
    rows = (len(results) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tw, rows * (th + 30)), (20, 20, 24))
    d = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 20)
    except OSError:
        font = ImageFont.load_default()
    for i, r in enumerate(results):
        x, yy = (i % cols) * tw, (i // cols) * (th + 30)
        try:
            img = Image.open(io.BytesIO(requests.get(r["thumbnail"], timeout=20).content)).convert("RGB")
            img = img.resize((tw, th))
            sheet.paste(img, (x, yy))
        except Exception:
            pass
        d.rectangle((x, yy, x + 44, yy + 30), fill=(0, 0, 0))
        d.text((x + 8, yy + 4), str(i + 1), fill=(255, 255, 255), font=font)
        tag = "* " if r.get("official") else ""
        d.text((x + 6, yy + th + 4), f"{tag}{r['duration'] or '?'}s {r['height']}p  {(r['title'] or '')[:26]}",
               fill=(220, 220, 220), font=font)
    sheet.save(out, quality=85)
    return out


# -------- credits -----------------------------------------------------------------


def used_files(edl_path: Path) -> set[str]:
    edl = json.loads(edl_path.read_text())
    base = edl_path.parent
    files = set()
    for p in list((edl.get("sources") or {}).values()) + [o.get("file") for o in edl.get("overlays") or []] \
            + [a.get("file") for a in edl.get("audio") or []]:
        if p:
            q = Path(p)
            files.add(str((q if q.is_absolute() else (base / q)).resolve()))
    return files


def write_credits(edit_dir: Path, edl_path: Path | None = None) -> Path:
    items = load_manifest(edit_dir)["items"]
    if edl_path and edl_path.exists():
        used = used_files(edl_path)
        # scene assets (captures, strips, logos) are copied into animations/<id>/hf/assets — count those too (reel-06:
        # filtering by edl.json alone listed 0 items)
        in_scenes = {p.name for p in edit_dir.glob("animations/*/hf/assets/*")}
        items = [i for i in items if str(Path(i["file"]).resolve()) in used
                 or (Path(i["file"]).name in in_scenes and Path(i["file"]).exists())]
        seen: set[str] = set()
        items = [i for i in items if not (Path(i["file"]).name in seen or seen.add(Path(i["file"]).name))]
    lines = ["# Credits", "", "Third-party media in this edit (from downloads/manifest.json).", ""]
    for i in items:
        who = i.get("uploader") or "unknown"
        lic = i.get("license") or ("provided by the client" if i.get("rights") == "user-provided" else "no licence listed")
        lines.append(f"- \"{i.get('title')}\" by {who} — {i.get('url')} — {lic} [{i.get('purpose')}]")
    commentary = [i for i in items if i.get("rights") == "commentary"]
    if commentary:
        lines += ["", "## Commentary clips (third-party, used for commentary — each needs its on-screen source label)", ""]
        lines += [f"- {i.get('title')} — {i.get('uploader') or 'unknown'} — {i.get('url')}" for i in commentary]
    flagged = [i for i in items if i.get("rights") not in USABLE]
    if flagged:
        lines += ["", "## Needs a rights check before publishing", ""]
        lines += [f"- {i.get('title')} — {i.get('url')} ({i.get('rights')})" for i in flagged]
    out = edit_dir / "credits.md"
    out.write_text("\n".join(lines) + "\n")
    print(f"credits → {out} ({len(items)} item(s){', ' + str(len(flagged)) + ' flagged' if flagged else ''})")
    return out


# -------- log ---------------------------------------------------------------------


def log_file(path: Path, edit_dir: Path, url: str | None = None, title: str | None = None,
             uploader: str | None = None, rights: str = "user-provided", purpose: str = "screenshot",
             license: str | None = None) -> dict:
    """Record a file that did not come through yt-dlp (screenshot, capture plate, logo) in the manifest."""
    path = path.resolve()
    if not path.exists():
        raise FileNotFoundError(path)
    manifest = load_manifest(edit_dir)
    manifest["items"] = [i for i in manifest["items"] if Path(i["file"]).resolve() != path]
    item = {"extractor": "local", "id": slugify(path.stem), "section": None, "audio_only": False,
            "url": url, "title": title or path.stem, "uploader": uploader, "license": license,
            "license_class": "unknown", "rights": rights, "purpose": purpose, "file": str(path),
            "downloaded_at": dt.datetime.now().isoformat(timespec="seconds"), **probe(path)}
    manifest["items"].append(item)
    save_manifest(edit_dir, manifest)
    print(f"logged: {path} ({rights}, {purpose})")
    return item


# -------- logo ------------------------------------------------------------------


LOGO_UA = {"User-Agent": "adnaan-reel/1.0 (https://github.com/adukhan98/adnaan-reel) asset fetch; python-requests"}


def _get(url: str, timeout: int = 15, tries: int = 3):
    """GET with a UA and small backoff (Commons/Wikipedia answer 429/503 under bursts). None on failure."""
    import time
    import requests
    for i in range(tries):
        try:
            r = requests.get(url, headers=LOGO_UA, timeout=timeout, allow_redirects=True)
        except requests.RequestException:
            r = None
        if r is not None and r.ok and r.content:
            return r
        if r is not None and r.status_code == 404:
            return None
        time.sleep(1.5 * (i + 1))
    return None


def _icon_links(html: str, base: str) -> list[tuple[int, str]]:
    """(size, absolute url) for <link rel=icon|apple-touch-icon …> tags, biggest first; svg counts as 1024."""
    from urllib.parse import urljoin
    out = []
    for tag in re.findall(r"<link[^>]+>", html, flags=re.I):
        rel = re.search(r'rel=["\']([^"\']+)', tag, flags=re.I)
        href = re.search(r'href=["\']([^"\']+)', tag, flags=re.I)
        if not rel or not href or not re.search(r"icon", rel.group(1), flags=re.I):
            continue
        sizes = re.search(r'sizes=["\'](\d+)x', tag, flags=re.I)
        url = urljoin(base, href.group(1))
        size = 1024 if url.lower().split("?")[0].endswith(".svg") else int(sizes.group(1)) if sizes else (180 if "apple" in rel.group(1).lower() else 32)
        out.append((size, url))
    return sorted(out, reverse=True)


def app_store_icon(name: str, country: str = "us") -> tuple[str, str] | None:
    """(1024 px icon url, seller) for an app whose App Store name matches `name` (exact, case-insensitive,
    or starts with it). The iTunes search API is free and keyless. None when no close match."""
    from urllib.parse import quote
    for entity in ("software", "macSoftware"):
        r = _get(f"https://itunes.apple.com/search?term={quote(name)}&entity={entity}&country={country}&limit=8")
        if r is None:
            continue
        try:
            results = r.json().get("results", [])
        except ValueError:
            continue
        want = name.strip().lower()
        for item in results:
            track = (item.get("trackName") or "").strip().lower()
            base = re.split(r"[:\-–—(]", track)[0].strip()
            if track == want or base == want or track.startswith(want + " "):
                art = item.get("artworkUrl512") or item.get("artworkUrl100") or ""
                if art:
                    return re.sub(r"\d+x\d+bb", "1024x1024bb", art), item.get("sellerName") or "?"
    return None


def fetch_logo(name: str, edit_dir: Path, domain: str | None = None, github: str | None = None,
               simple: str | None = None, min_size: int = 96, app: bool = True) -> Path:
    """Official logo for a named tool/company → <edit>/logos/<slug>.<ext>, logged (rights: official, purpose: logo).
    Order: GitHub org avatar (--github) → the site's own icon links (--domain: apple-touch-icon / svg icon)
    → Simple Icons (official brand SVGs, brand colour) → error (ask for the press-kit file)."""
    out_dir = edit_dir / "logos"
    out_dir.mkdir(parents=True, exist_ok=True)
    slug = slugify(name)
    tried = []
    candidates: list[tuple[str, str, str]] = []   # (url, ext, source-label)
    if github:
        candidates.append((f"https://github.com/{github}.png?size=512", "png", f"GitHub avatar of {github}"))
    if app:
        hit = app_store_icon(name)
        if hit:
            candidates.append((hit[0], "png", f"App Store icon (seller: {hit[1]}) — verify the seller is the real maker"))
    if domain:
        home = domain if domain.startswith("http") else f"https://{domain}"
        r = _get(home)
        if r is not None:
            for size, url in _icon_links(r.text, r.url):
                if size >= min_size:
                    candidates.append((url, "svg" if url.lower().split("?")[0].endswith(".svg") else "png", f"{domain} site icon {size}px"))
            candidates.append((home.rstrip("/") + "/apple-touch-icon.png", "png", f"{domain}/apple-touch-icon.png"))
    candidates.append((f"https://cdn.simpleicons.org/{simple or slug}", "svg", f"Simple Icons '{simple or slug}' (official brand SVG, monochrome)"))
    # last resorts: the brand's GitHub org avatar under its own name, then Google's favicon service for the domain
    if not github:
        candidates.append((f"https://github.com/{slug}.png?size=512", "png", f"GitHub avatar of '{slug}' (verify it is the brand's own org)"))
    if domain:
        d = re.sub(r"^https?://", "", domain).split("/")[0]
        candidates.append((f"https://www.google.com/s2/favicons?domain={d}&sz=256", "png", f"Google favicon service for {d} (the site's own icon)"))
    for url, ext, label in candidates:
        r = _get(url)
        tried.append(label)
        if r is None or len(r.content) < 80:
            continue
        ctype = r.headers.get("content-type", "")
        if ext == "png" and "svg" in ctype:
            ext = "svg"
        if ext == "png" and not ("image" in ctype or r.content[:4] == b"\x89PNG"):
            continue
        if ext == "svg" and b"<svg" not in r.content[:4000]:
            continue
        path = out_dir / f"{slug}.{ext}"
        path.write_bytes(r.content)
        if ext == "png":
            try:
                from PIL import Image
                with Image.open(path) as im:
                    if min(im.size) < min_size:
                        path.unlink()
                        continue
            except Exception:
                pass
        log_file(path, edit_dir, url=url, title=f"{name} logo", uploader=name, rights="official", purpose="logo",
                 license="trademark of its owner — shown unaltered to identify the product")
        print(f"logo: {name} → {path}  ({label})")
        return path
    sys.exit(f"no official logo found for {name!r} (tried: {'; '.join(tried)}). Ask for the press-kit file and "
             f"`fetch.py log <file> --purpose logo --rights official`, or pass --domain / --github / --simple.")


def cmd_logo(args: argparse.Namespace) -> None:
    fetch_logo(args.name, args.edit_dir.resolve(), domain=args.domain, github=args.github, simple=args.simple,
               min_size=args.min_size, app=not args.no_app)


# -------- icon (v7) ----------------------------------------------------------------

PHOSPHOR = "https://unpkg.com/@phosphor-icons/core@2.1.1/assets/{weight}/{name}{suffix}.svg"


def cmd_icon(args: argparse.Namespace) -> None:
    """Phosphor glyphs (MIT) for the v7 icon discs → <edit>/icons/<name>.svg (fill weight by default; logged).
    List them in a slot's "assets" as "icons/<name>.svg"; scenes use them via V.icon(name) / V.disc({icon: name})."""
    import requests
    edit_dir = args.edit_dir.resolve()
    out = edit_dir / "icons"
    out.mkdir(parents=True, exist_ok=True)
    suffix = "" if args.weight == "regular" else f"-{args.weight}"
    bad = []
    for name in args.names:
        url = PHOSPHOR.format(weight=args.weight, name=name, suffix=suffix)
        r = requests.get(url, timeout=30)
        if r.status_code != 200 or b"<svg" not in r.content[:200]:
            bad.append(name)
            continue
        path = out / f"{name}.svg"
        path.write_bytes(r.content)
        log_file(path, edit_dir, url=url, title=f"Phosphor icon: {name}", uploader="Phosphor Icons",
                 rights="open-source", purpose="icon", license="MIT")
        print(f"icon: {name} → {path}")
    if bad:
        sys.exit(f"not in Phosphor ({args.weight}): {', '.join(bad)} — browse https://phosphoricons.com for the exact name")


# -------- photo -----------------------------------------------------------------


COMMONS_API = "https://commons.wikimedia.org/w/api.php"


def wikipedia_lead_image(title: str) -> dict | None:
    """Wikipedia's lead image for a page (REST summary API). Returns {url, width, height, page, title} or None."""
    from urllib.parse import quote
    r = _get(f"https://en.wikipedia.org/api/rest_v1/page/summary/{quote(title.replace(' ', '_'))}")
    if r is None:
        return None
    try:
        j = r.json()
    except ValueError:
        return None
    img = j.get("originalimage") or j.get("thumbnail")
    if not img or j.get("type") == "disambiguation":
        return None
    return {"url": img["source"], "width": img.get("width", 0), "height": img.get("height", 0),
            "page": j.get("content_urls", {}).get("desktop", {}).get("page"), "title": j.get("title")}


def commons_search(query: str, n: int = 5, width: int = 1600) -> list[dict]:
    """Wikimedia Commons file search → [{title, url, width, height, license, artist, credit, page}] (biggest files first)."""
    from urllib.parse import quote
    r = _get(f"{COMMONS_API}?action=query&list=search&srnamespace=6&srlimit={n * 2}&format=json&srsearch={quote(query)}")
    if r is None:
        return []
    try:
        hits = [h["title"] for h in r.json()["query"]["search"]]
    except (ValueError, KeyError):
        return []
    hits = [h for h in hits if h.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))][: n * 2]
    if not hits:
        return []
    titles = "|".join(quote(h) for h in hits)
    r = _get(f"{COMMONS_API}?action=query&prop=imageinfo&iiprop=url|size|extmetadata&iiurlwidth={width}&format=json&titles={titles}")
    if r is None:
        return []
    out = []
    try:
        pages = r.json()["query"]["pages"].values()
    except (ValueError, KeyError):
        return []
    for pg in pages:
        ii = (pg.get("imageinfo") or [{}])[0]
        if not ii.get("url"):
            continue
        meta = ii.get("extmetadata") or {}
        get = lambda k: re.sub(r"<[^>]+>", "", (meta.get(k) or {}).get("value", "")).strip()
        url = ii.get("thumburl") or ii["url"]
        if ii["url"].lower().endswith(".webp"):
            w = min(width, ii.get("width", width))
            url = ii["url"].replace("/commons/", "/commons/thumb/") + f"/{w}px-{ii['url'].rsplit('/', 1)[-1]}.png"
        out.append({"title": pg.get("title"), "url": url, "orig": ii["url"], "width": ii.get("width", 0),
                    "height": ii.get("height", 0), "license": get("LicenseShortName") or "unknown",
                    "artist": get("Artist"), "credit": get("Credit"), "page": ii.get("descriptionurl")})
    # rank: files whose title names the thing first (a search for a person returns their papers' figures too), then size
    toks = [t for t in re.findall(r"[a-z0-9]+", query.lower()) if len(t) > 2]
    score = lambda x: sum(1 for t in toks if t in (x["title"] or "").lower())
    out.sort(key=lambda x: (-score(x), -(x["width"] * x["height"])))
    return out[:n]


def commons_filename(url: str) -> str:
    """Original Commons file name from an upload.wikimedia.org URL (handles /thumb/…/<name>/<N>px-<name> and ?query)."""
    from urllib.parse import unquote
    path = url.split("?")[0]
    parts = path.split("/")
    if "/thumb/" in path and len(parts) >= 2:
        return unquote(parts[-2])
    return unquote(parts[-1])


def commons_file_info(title: str) -> dict | None:
    """Licence / artist / file page for one Commons file title (File:…)."""
    from urllib.parse import quote
    r = _get(f"{COMMONS_API}?action=query&prop=imageinfo&iiprop=url|extmetadata&format=json&titles={quote(title)}")
    if r is None:
        return None
    try:
        pg = next(iter(r.json()["query"]["pages"].values()))
        ii = (pg.get("imageinfo") or [{}])[0]
    except (ValueError, KeyError, StopIteration):
        return None
    meta = ii.get("extmetadata") or {}
    get = lambda k: re.sub(r"<[^>]+>", "", (meta.get(k) or {}).get("value", "")).strip()
    return {"license": get("LicenseShortName"), "artist": get("Artist") or get("Credit"), "page": ii.get("descriptionurl")}


def fetch_photo(query: str, edit_dir: Path, min_width: int = 800, n: int = 1) -> list[Path]:
    """Real photo(s) of a person/thing → <edit>/photos/<slug>[-k].<ext>, logged with the licence for credits.
    Wikipedia's lead image first (people, landmarks), then Wikimedia Commons search. Never AI, never watermarked
    (Commons rejects those), minimum width enforced. Look at the file before using it: right person, right era."""
    out_dir = edit_dir / "photos"
    out_dir.mkdir(parents=True, exist_ok=True)
    slug = slugify(query)
    saved: list[Path] = []
    cands: list[dict] = []
    lead = wikipedia_lead_image(query)
    if lead and lead["width"] >= min_width:
        # resolve the lead image's licence/author from its Commons file page (the summary API has none)
        info = commons_file_info("File:" + commons_filename(lead["url"]))
        cands.append({**lead, "license": (info or {}).get("license") or "see Commons file page",
                      "artist": (info or {}).get("artist", ""), "credit": "Wikipedia lead image",
                      "page": (info or {}).get("page") or lead.get("page"), "title": lead["title"]})
    cands += [c for c in commons_search(query, n=max(n, 3)) if c["width"] >= min_width]
    for c in cands:
        if len(saved) >= n:
            break
        r = _get(c["url"], timeout=30)
        if (r is None or len(r.content) < 5000) and c.get("orig"):
            r = _get(c["orig"], timeout=60)
        if r is None or len(r.content) < 5000:
            continue
        src_ext = (c["url"].split("?")[0].rsplit(".", 1)[-1] or "jpg").lower()
        ext = "png" if src_ext in ("png", "webp", "svg") else "jpg"
        path = out_dir / (f"{slug}.{ext}" if not saved else f"{slug}-{len(saved) + 1}.{ext}")
        if src_ext == "webp":      # HyperFrames/Chrome read webp, but keep the kit uniform: convert to png
            try:
                from PIL import Image
                import io
                Image.open(io.BytesIO(r.content)).convert("RGBA").save(path)
            except Exception:
                path.write_bytes(r.content)
        else:
            path.write_bytes(r.content)
        lic = c.get("license") or "unknown"
        log_file(path, edit_dir, url=c.get("page") or c["url"], title=f"{query} — {c.get('title') or 'photo'}",
                 uploader=c.get("artist") or c.get("credit") or "Wikimedia Commons",
                 rights="cc-by-sa" if "BY-SA" in lic.upper() else "cc-by" if "BY" in lic.upper() else "cc0" if ("CC0" in lic.upper() or "PUBLIC DOMAIN" in lic.upper()) else "commentary",
                 purpose="photo", license=lic)
        print(f"photo: {query} → {path}  ({c['width']}x{c['height']}, {lic}, {c.get('artist') or c.get('credit') or ''})")
        saved.append(path)
    if not saved and min_width > 400:
        print(f"WARNING: nothing ≥ {min_width} px for {query!r}; taking the best smaller file — check it reads at phone size, "
              f"or ask him for a press photo")
        return fetch_photo(query, edit_dir, min_width=400, n=n)
    if not saved:
        sys.exit(f"no usable photo for {query!r} (Wikipedia lead image / Commons search). "
                 f"Try another spelling or ask him for a press photo.")
    return saved


def cmd_photo(args: argparse.Namespace) -> None:
    fetch_photo(args.query, args.edit_dir.resolve(), min_width=args.min_width, n=args.n)


# -------- tweet (post text + attached media without login) ----------------------


TWEET_SYNDICATION = "https://cdn.syndication.twimg.com/tweet-result?id={id}&token=a"
TWEET_EMBED = "https://platform.twitter.com/embed/Tweet.html?id={id}&hideThread=true&theme=light"


def tweet_id(url_or_id: str) -> str:
    """'https://x.com/user/status/123?s=20' or 'twitter.com/.../123' or '123' → '123'."""
    m = re.search(r"/status(?:es)?/(\d+)", url_or_id)
    if m:
        return m.group(1)
    if re.fullmatch(r"\d+", url_or_id.strip()):
        return url_or_id.strip()
    raise ValueError(f"not a post URL or id: {url_or_id}")


def tweet_info(url_or_id: str) -> dict | None:
    """Author, date, full text and attached media of a public post — no login, no API key (the syndication
    endpoint that powers embeds). From b-roll-finder's notes; verified 2026-10-17. None when the post is gone,
    protected or the endpoint changed."""
    tid = tweet_id(url_or_id)
    r = _get(TWEET_SYNDICATION.format(id=tid), timeout=20)
    if r is None:
        return None
    try:
        d = r.json()
    except ValueError:
        return None
    if not isinstance(d, dict) or not d.get("text") and not d.get("user"):
        return None
    user = d.get("user") or {}
    media: list[dict] = []
    for m in d.get("mediaDetails") or []:
        kind = m.get("type", "photo")
        if kind == "photo":
            media.append({"type": "photo", "url": m.get("media_url_https"), "w": (m.get("original_info") or {}).get("width"),
                          "h": (m.get("original_info") or {}).get("height")})
        else:   # video / animated_gif: the highest-bitrate mp4 variant
            vs = [v for v in (m.get("video_info") or {}).get("variants", []) if (v.get("content_type") == "video/mp4")]
            vs.sort(key=lambda v: v.get("bitrate") or 0, reverse=True)
            media.append({"type": kind, "url": vs[0]["url"] if vs else None, "poster": m.get("media_url_https")})
    if not media:
        media = [{"type": "photo", "url": p.get("url"), "w": p.get("width"), "h": p.get("height")} for p in d.get("photos") or []]
    article = (d.get("article") or {})
    q = d.get("quoted_tweet") or {}
    return {"id": tid, "url": f"https://x.com/{user.get('screen_name', 'i')}/status/{tid}",
            "author": user.get("name"), "handle": user.get("screen_name"), "created_at": d.get("created_at"),
            "text": d.get("text") or "", "likes": d.get("favorite_count"), "media": [m for m in media if m.get("url")],
            # a long post ("note tweet") comes back cut at ~280 chars; the embed cuts it too — only the x.com page is full
            "truncated": bool(d.get("note_tweet")),
            "article_url": next((u.get("expanded_url") for u in (d.get("entities") or {}).get("urls", [])
                                 if "/i/article/" in (u.get("expanded_url") or "")), None) if article or d.get("entities") else None,
            "quoted": {"handle": (q.get("user") or {}).get("screen_name"), "text": q.get("text")} if q else None,
            "embed_url": TWEET_EMBED.format(id=tid)}


def fetch_tweet(url_or_id: str, edit_dir: Path, check: str | None = None) -> dict | None:
    """Verify a quoted phrase against the post's real text and save every attached image/video at full size into
    <edit>/posts/<id>/ (logged, rights=commentary). Prints what to capture for the readable strip. The page
    capture itself stays `capture.py --readable` on the x.com URL (fuller than the embed, which truncates long
    posts with "Show more"); the embed URL printed here is the fallback when x.com shows a login wall."""
    info = tweet_info(url_or_id)
    if info is None:
        print(f"no public data for {url_or_id} — deleted, protected, or the syndication endpoint changed; "
              f"capture the page in Claude in Chrome or ask him for a screenshot")
        return None
    print(f"@{info['handle']} ({info['author']}) · {info['created_at']} · {info['likes']} likes\n{info['text']}\n")
    if info["truncated"]:
        print("(long post: only the first ~280 chars come back here; the x.com capture has the full text)\n")
    if info.get("article_url"):
        print(f"(an X Article — the body lives at {info['article_url']}; capture that page for the readable strip)\n")
    if info.get("quoted"):
        print(f"(quotes @{info['quoted']['handle']}: {(info['quoted']['text'] or '')[:120]!r})\n")
    if check:
        norm = lambda t: re.sub(r"\s+", " ", t).strip().lower()
        hit = norm(check) in norm(info["text"])
        if hit:
            print("OK: " + repr(check))
        elif info["truncated"]:
            print("NOT IN PREVIEW: " + repr(check) + " — the post is longer than the preview; confirm it on the captured strip")
        else:
            print("NOT IN POST: " + repr(check) + " — fix the on-screen words or the strip phrase")
        info["check"] = hit
    out_dir = edit_dir / "posts" / info["id"]
    saved: list[Path] = []
    for k, m in enumerate(info["media"], 1):
        r = _get(m["url"] + ("?name=orig" if m["type"] == "photo" and "?" not in m["url"] else ""), timeout=60)
        if r is None or len(r.content) < 2000:
            r = _get(m["url"], timeout=60)
        if r is None or len(r.content) < 2000:
            print(f"  media {k}: download failed ({m['url']})")
            continue
        out_dir.mkdir(parents=True, exist_ok=True)
        ext = "mp4" if m["type"] != "photo" else ((m["url"].split("?")[0].rsplit(".", 1)[-1] or "jpg").lower())
        path = out_dir / f"media-{k}.{ext}"
        path.write_bytes(r.content)
        log_file(path, edit_dir, url=info["url"], title=f"@{info['handle']}: {info['text'][:60]}",
                 uploader=info["author"] or info["handle"], rights="commentary", purpose="post-media")
        size = f"{m.get('w')}x{m.get('h')}" if m.get("w") else m["type"]
        print(f"  media {k}: {path} ({size})")
        saved.append(path)
    if not info["media"]:
        print("  no attached media")
    print(f"\nreadable strip: capture.py {info['url']} --edit-dir {edit_dir} --name post --readable --phrases \"…\"\n"
          f"login wall?    use {info['embed_url']} (truncates long posts — check the strip has the phrase)")
    info["files"] = [str(p) for p in saved]
    (edit_dir / "posts").mkdir(parents=True, exist_ok=True)
    (edit_dir / "posts" / f"{info['id']}.json").write_text(json.dumps(info, indent=2, ensure_ascii=False))
    return info


def cmd_tweet(args: argparse.Namespace) -> None:
    fetch_tweet(args.url, args.edit_dir.resolve(), check=args.check)


# -------- CLI ---------------------------------------------------------------------


def main() -> None:
    ap = argparse.ArgumentParser(description="Download media with yt-dlp (cached, licence-tracked)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    u = sub.add_parser("url", help="Download one link")
    u.add_argument("url")
    u.add_argument("--edit-dir", type=Path, required=True)
    u.add_argument("--purpose", default="broll", help="broll | footage | reference | music | sfx | logo")
    u.add_argument("--section", help="Only this slice, e.g. 1:05-1:20")
    u.add_argument("--audio-only", action="store_true")
    u.add_argument("--max-height", type=int, default=1080)
    u.add_argument("--name", help="Short name for the file")
    u.add_argument("--found-by-search", action="store_true",
                   help="The link came from fetch.py search, not from the user (rights not assumed)")
    u.add_argument("--rights", choices=RIGHTS, default=None,
                   help="commentary = a third-party clip the user approved for commentary use at the check-in")

    s = sub.add_parser("search", help="Find Creative Commons b-roll on YouTube")
    s.add_argument("query")
    s.add_argument("--edit-dir", type=Path, required=True)
    s.add_argument("--n", type=int, default=8)
    s.add_argument("--max-duration", type=float, default=None, help="Skip videos longer than this (s)")
    s.add_argument("--min-height", type=int, default=720)
    s.add_argument("--any-license", action="store_true",
                   help="Include non-CC results (only when the user has said they hold the rights)")

    f = sub.add_parser("find", help="Find the real clip of something (any licence, official channels first)")
    f.add_argument("query")
    f.add_argument("--edit-dir", type=Path, required=True)
    f.add_argument("--official", default=None, help="Owner name to rank first, e.g. 'OpenAI'")
    f.add_argument("--n", type=int, default=8)
    f.add_argument("--max-duration", type=float, default=None)
    f.add_argument("--min-height", type=int, default=720)

    lg = sub.add_parser("log", help="Record a local media file (screenshot, capture, logo) for credits")
    lg.add_argument("file", type=Path)
    lg.add_argument("--edit-dir", type=Path, required=True)
    lg.add_argument("--url", default=None, help="Where it came from")
    lg.add_argument("--title", default=None)
    lg.add_argument("--uploader", default=None, help="Owner shown in credits and the on-screen label")
    lg.add_argument("--rights", choices=LOG_RIGHTS, default="user-provided")
    lg.add_argument("--license", default=None, help="Licence text for credits, e.g. 'CC BY-SA 4.0'")
    lg.add_argument("--purpose", default="screenshot")

    lo = sub.add_parser("logo", help="Fetch the official logo of a named tool/company into <edit>/logos/ (logged)")
    lo.add_argument("name", help="As he says it, e.g. 'Claude Code', 'Adobe', 'Cursor'")
    lo.add_argument("--edit-dir", type=Path, required=True)
    lo.add_argument("--domain", default=None, help="Official site, e.g. cursor.com — its own icon links are tried first")
    lo.add_argument("--github", default=None, help="GitHub org/user whose avatar is the logo, e.g. anthropics")
    lo.add_argument("--simple", default=None, help="Simple Icons slug if it differs from the slugified name")
    lo.add_argument("--min-size", type=int, default=96)
    lo.add_argument("--no-app", action="store_true", help="Skip the App Store icon lookup")
    lo.set_defaults(fn=cmd_logo)

    ic = sub.add_parser("icon", help="Phosphor icon glyphs (MIT) for v7 icon discs → <edit>/icons/<name>.svg (logged)")
    ic.add_argument("names", nargs="+", help="Phosphor names, e.g. microphone eye magnifying-glass folder-open")
    ic.add_argument("--edit-dir", type=Path, required=True)
    ic.add_argument("--weight", default="fill", choices=["fill", "bold", "regular", "duotone"])

    ph = sub.add_parser("photo", help="Real photo of a person/thing from Wikipedia or Wikimedia Commons (licence logged)")
    ph.add_argument("query", help="e.g. 'Andrej Karpathy', 'Golden Gate Bridge'")
    ph.add_argument("--edit-dir", type=Path, required=True)
    ph.add_argument("--min-width", type=int, default=800, help="People photos are often ~1000 px; 800 keeps most")
    ph.add_argument("--n", type=int, default=1, help="How many Commons candidates to save (first is Wikipedia's lead image if any)")

    tw = sub.add_parser("tweet", help="Real text + attached media of a public X post, no login (verify a quote, save images)")
    tw.add_argument("url", help="x.com/twitter.com status URL or the numeric id")
    tw.add_argument("--edit-dir", type=Path, required=True)
    tw.add_argument("--check", default=None, help="phrase he reads/shows — printed OK or NOT IN POST")

    c = sub.add_parser("credits", help="Write credits.md for downloaded media the EDL uses")
    c.add_argument("--edit-dir", type=Path, required=True)
    c.add_argument("--edl", type=Path, default=None)

    args = ap.parse_args()
    edit_dir = args.edit_dir.resolve()
    try:
        if args.cmd == "url":
            download(args.url, edit_dir, purpose=args.purpose, section=args.section,
                     audio_only=args.audio_only, max_height=args.max_height, name=args.name,
                     user_provided=not args.found_by_search, rights=args.rights)
        elif args.cmd == "search":
            search(args.query, edit_dir, n=args.n, cc_only=not args.any_license,
                   max_duration=args.max_duration, min_height=args.min_height)
        elif args.cmd == "find":
            search(args.query, edit_dir, n=args.n, cc_only=False, max_duration=args.max_duration,
                   min_height=args.min_height, official=args.official)
        elif args.cmd == "log":
            log_file(args.file, edit_dir, url=args.url, title=args.title, uploader=args.uploader,
                     rights=args.rights, purpose=args.purpose, license=args.license)
        elif args.cmd == "logo":
            cmd_logo(args)
        elif args.cmd == "photo":
            cmd_photo(args)
        elif args.cmd == "icon":
            cmd_icon(args)
        elif args.cmd == "tweet":
            cmd_tweet(args)
        else:
            write_credits(edit_dir, args.edl.resolve() if args.edl else (edit_dir / "edl.json"))
    except RuntimeError as e:
        sys.exit(f"yt-dlp failed:\n{e}")


if __name__ == "__main__":
    main()
