"""Review sheet per scene: frame 0, 25 %, 50 %, 75 % and the last frame, with the speaker-card zone outlined in red.
Look at every sheet as scenes land (frame 0 not empty, no bare-paper frame, card zone clear, words readable, brand
colours only) and send fixes to the scene's agent.

    python helpers/review.py --edit-dir E s08_twelve s09_hundred     → E/verify/review/<id>.jpg
"""
import argparse
import json
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw

CARD = (1574, 614, 1886, 1012)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("ids", nargs="+")
    ap.add_argument("--edit-dir", type=Path, required=True)
    a = ap.parse_args()
    edit = a.edit_dir.resolve()
    out = edit / "verify" / "review"
    out.mkdir(parents=True, exist_ok=True)
    for sid in a.ids:
        d = edit / "animations" / sid
        r = next((p for p in (d / "render.mp4", d / "render.mov") if p.exists()), None)
        if not r:
            print(sid, "no render")
            continue
        n = int(json.loads((d / "slot.json").read_text())["frames"])
        tiles = []
        for f in (0, n // 4, n // 2, 3 * n // 4, n - 1):
            png = out / f"_{sid}_{f}.png"
            subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", str(r), "-vf", f"select=eq(n\\,{f})",
                            "-frames:v", "1", str(png)], check=True)
            im = Image.open(png).convert("RGB")
            ImageDraw.Draw(im).rectangle(CARD, outline=(255, 0, 0), width=4)
            ImageDraw.Draw(im).text((20, 20), f"{sid}  f{f}", fill=(255, 0, 0))
            tiles.append(im.resize((640, 360)))
            png.unlink()
        sheet = Image.new("RGB", (640 * 3, 360 * 2), (40, 40, 40))
        for i, t in enumerate(tiles):
            sheet.paste(t, ((i % 3) * 640, (i // 3) * 360))
        sheet.save(out / f"{sid}.jpg", quality=88)
        print(out / f"{sid}.jpg")


if __name__ == "__main__":
    main()
