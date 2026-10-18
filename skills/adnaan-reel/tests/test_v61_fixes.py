"""v6.1 fixes from reel-07: highlighter fill, tiled long-page captures, straight-stroke texture, frame-0 rule."""
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image, ImageDraw

SKILL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL / "helpers"))
import capture  # noqa: E402


class MarkerRuntime(unittest.TestCase):
    def test_strokes_never_filled(self):
        js = (SKILL / "templates" / "runtime" / "marker.js").read_text()
        self.assertIn('p.setAttribute("fill", "none")', js)       # highlighter paths live outside svg.mk-layer
        self.assertIn("svg.mk-hl path { fill: none; }", (SKILL / "templates" / "runtime" / "marker.css").read_text())

    def test_texture_filter_region_is_user_space(self):
        js = (SKILL / "templates" / "runtime" / "marker.js").read_text()
        self.assertIn('id="mk-tex" filterUnits="userSpaceOnUse"', js)   # bbox units sliced straight strokes thin


class TiledCapture(unittest.TestCase):
    def _tile(self, d: Path, k: int, text: str, h: int = 400) -> Path:
        im = Image.new("RGB", (300, h), "white")
        ImageDraw.Draw(im).text((10, 10 + 40 * k), text, fill="black")
        p = d / f"page.tile{k:03d}.png"
        im.save(p)
        return p

    def test_stitches_tiles_in_order(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            tiles = [self._tile(d, k, f"tile {k}") for k in range(3)]
            out = d / "page.png"
            capture.stitch_tiles(tiles, out)
            im = Image.open(out)
            self.assertEqual(im.size, (300, 1200))
            self.assertFalse(any(t.exists() for t in tiles))      # tiles cleaned up

    def test_refuses_repeated_tiles(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            a = self._tile(d, 0, "same screen")
            b = d / "page.tile001.png"
            b.write_bytes(a.read_bytes())                          # the Chrome texture-limit failure mode
            with self.assertRaises(SystemExit):
                capture.stitch_tiles([a, b], d / "page.png")

    def test_allows_repeated_blank_tiles(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            tiles = []
            for k in range(2):
                p = d / f"page.tile{k:03d}.png"
                Image.new("RGB", (300, 400), "white").save(p)       # an empty band of page may repeat
                tiles.append(p)
            capture.stitch_tiles(tiles, d / "page.png")
            self.assertTrue((d / "page.png").exists())

    def test_capture_script_tiles(self):
        cjs = (SKILL / "helpers" / "capture_readable.cjs").read_text()
        self.assertIn("captureBeyondViewport: true", cjs)
        self.assertIn("info.tiles", cjs)
        self.assertNotIn("await root.screenshot(", cjs)


class ThumbnailRule(unittest.TestCase):
    def test_frame0_rule_documented(self):
        self.assertIn("Frame 0 is the thumbnail", (SKILL / "references" / "style.md").read_text())
        self.assertIn("FRAME 0 = THE THUMBNAIL", (SKILL / "templates" / "scenes" / "hook.html").read_text())
        self.assertIn("frame 0 is the THUMBNAIL", (SKILL / "helpers" / "slots.py").read_text())


if __name__ == "__main__":
    unittest.main()
