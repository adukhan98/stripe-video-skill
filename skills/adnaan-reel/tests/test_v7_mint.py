"""v7 "mint" look (reel-08 restyle, 2026-10-17): runtime, starters, look-aware prepare, init-brand --look, icons,
and the frame-exact cut-speaker seek."""
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL / "helpers"))
import fetch  # noqa: E402
import scenes  # noqa: E402
import slots  # noqa: E402

V7_STARTERS = ("talk", "talk_depth", "visual", "chain", "card")


class Runtime(unittest.TestCase):
    def test_v7_runtime_files(self):
        css = (SKILL / "templates" / "runtime" / "v7.css").read_text()
        for cls in (".g7", ".w7", ".v7-vig", ".v7-disc", ".v7-gl", ".v7-link", ".v7-ring", ".spk.matte", ".v7-world",
                    ".v7-zone", ".v7-hl", "--vignette-strong", "--disc-shadow"):
            self.assertIn(cls, css)
        js = (SKILL / "templates" / "runtime" / "v7.js").read_text()
        for api in ("board", "icon", "disc", "discIn", "chain", "chainDraw", "chainEnd", "faceRect", "shrink", "grow",
                    "placed", "cam", "pose", "zoneMask"):
            self.assertRegex(js, rf"\b{api}\b")
        self.assertNotIn("Math.random", js)                       # seek-safe / deterministic
        self.assertIn("v7.css", slots.RUNTIME_FILES)
        self.assertIn("v7.js", slots.RUNTIME_FILES)

    @unittest.skipUnless(shutil.which("node"), "node not installed")
    def test_v7_js_parses_and_exports(self):
        code = ("const vm=require('vm');const ctx={window:{}};vm.runInNewContext(require('fs').readFileSync(process.argv[1],"
                "'utf8'),ctx);console.log(typeof ctx.window.V7.init)")
        out = subprocess.run(["node", "-e", code, str(SKILL / "templates" / "runtime" / "v7.js")], capture_output=True, text=True)
        self.assertEqual(out.stdout.strip(), "function", out.stderr)

    def test_install_runtime_copies_v7(self):
        with tempfile.TemporaryDirectory() as tmp:
            hf = Path(tmp) / "hf"
            hf.mkdir()
            slots.install_runtime(hf)
            self.assertTrue((hf / "v7.js").exists() and (hf / "v7.css").exists())


class Starters(unittest.TestCase):
    def test_v7_starters(self):
        for t in V7_STARTERS:
            html = (SKILL / "templates" / "scenes" / f"{t}.html").read_text()
            self.assertTrue(html.startswith("<!doctype html>"), t)
            for need in ('href="paper.css"', 'src="paper.js"', 'href="v7.css"', 'src="v7.js"', "window.__timelines",
                         "Paper.init(", "V7.init(P)", '@font-face { font-family: "Inter Tight"'):
                self.assertIn(need, html, f"{t}: {need}")
            for banned in ("marker.js", "Marker.init", "Caveat"):     # v7: no hand-drawn layer
                self.assertNotIn(banned, html, f"{t}: {banned}")
            self.assertNotRegex(html, r"#E5484D|\bred\b", t)

    def test_depth_starter_layers_and_matte_type(self):
        html = (SKILL / "templates" / "scenes" / "talk_depth.html").read_text()
        a, b, c = html.index('id="spk"'), html.index('class="v7-behind"'), html.index('src="assets/speaker_cut.webm"')
        self.assertLess(a, b)
        self.assertLess(b, c)                                     # footage → behind → matte
        self.assertIn('class="spk full matte"', html)
        self.assertIn("talk_depth", scenes.MATTE_TYPES)
        for t in ("talk", "talk_depth", "chain", "card"):
            self.assertIn(t, scenes.NON_PAPER_TYPES)              # flashcheck expects his footage there

    def test_write_starter_presets_duration(self):
        with tempfile.TemporaryDirectory() as tmp:
            hf = Path(tmp) / "hf"
            hf.mkdir()
            for t in V7_STARTERS:
                self.assertTrue(slots.write_starter(hf, t, f"s_{t}", 99.5 / 30, force=True))
                html = (hf / "index.html").read_text()
                self.assertEqual(set(re.findall(r'data-duration="([0-9.]+)"', html)), {"3.3167"}, t)


class LookAwarePrepare(unittest.TestCase):
    def _meta(self, look, stype):
        return {"id": "x", "start": 0, "duration": 2, "frames": 60, "fps": "30", "canvas": [1080, 1920],
                "zone": [60, 285, 960, 1480], "type": stype, "bespoke": False, "brief": "b", "look": look}

    def test_task_md_sections(self):
        mint = slots.scene_task_md(self._meta("mint", "talk"), Path("/tmp/x"), Path("/tmp"))
        self.assertIn('v7 "MINT" look', mint)
        self.assertNotIn("## Marker layer", mint)
        self.assertIn("NON-PAPER", mint)
        paper = slots.scene_task_md(self._meta("paper", "hook"), Path("/tmp/x"), Path("/tmp"))
        self.assertIn("## Marker layer", paper)
        self.assertNotIn('v7 "MINT" look', paper)
        self.assertIn("{double}", paper)                          # the marker section's braces survived the f-string

    def test_types(self):
        self.assertEqual(set(slots.V7_TYPES), set(V7_STARTERS))
        for t in ("visual", "chain", "card", "talk_depth"):
            self.assertIn(t, slots.BESPOKE_TYPES)


class InitBrand(unittest.TestCase):
    def test_mint_is_the_default_look(self):
        with tempfile.TemporaryDirectory() as tmp:
            e = Path(tmp) / "edit"
            subprocess.run(["uv", "run", "--project", str(SKILL), str(SKILL / "helpers" / "scenes.py"), "init-brand",
                            "--edit-dir", str(e)], check=True, capture_output=True)
            brand = json.loads((e / "brand" / "brand.json").read_text())
            self.assertEqual(brand["look"], "mint")
            self.assertEqual(brand["colors"]["primary"]["hex"].upper(), scenes.MINT_LOOK[0])
            css = (e / "brand" / "brand.css").read_text()
            self.assertIn("--vignette-strong", css)
            self.assertIn("--peach", css)
            self.assertIn('v7 — the MINT look', (e / "animations" / "SHARED.md").read_text())

    def test_paper_look_keeps_red(self):
        with tempfile.TemporaryDirectory() as tmp:
            e = Path(tmp) / "edit"
            subprocess.run(["uv", "run", "--project", str(SKILL), str(SKILL / "helpers" / "scenes.py"), "init-brand",
                            "--edit-dir", str(e), "--look", "paper"], check=True, capture_output=True)
            brand = json.loads((e / "brand" / "brand.json").read_text())
            self.assertEqual(brand["look"], "paper")
            self.assertEqual(brand["colors"]["primary"]["hex"].upper(), "#E5484D")
            self.assertNotIn("--vignette-strong", (e / "brand" / "brand.css").read_text())
            self.assertIn("legacy PAPER look", (e / "animations" / "SHARED.md").read_text())


class Icons(unittest.TestCase):
    def test_icon_rights(self):
        self.assertIn("open-source", fetch.LOG_RIGHTS)
        self.assertIn("open-source", fetch.USABLE)
        self.assertIn("@phosphor-icons/core@2.1.1", fetch.PHOSPHOR)


class FrameExactSeek(unittest.TestCase):
    def test_seek_ts_math(self):
        self.assertGreater(scenes.seek_ts(41.333), 1240 / 30)      # the reel-08 case: 41.333 means frame 1240
        self.assertLess(scenes.seek_ts(41.333), 1241 / 30)
        self.assertGreater(scenes.seek_ts(10.667), 320 / 30)

    @unittest.skipUnless(shutil.which("ffmpeg"), "ffmpeg not installed")
    def test_cut_lands_on_the_scene_frame(self):
        import numpy as np
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "src.mp4"
            subprocess.run(["ffmpeg", "-v", "error", "-f", "lavfi", "-i", "testsrc2=size=96x96:rate=30", "-t", "3",
                            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-g", "1", str(src)], check=True)

            def frame(args):
                raw = subprocess.run(["ffmpeg", "-v", "error", *args, "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "gray", "-"],
                                     capture_output=True, check=True).stdout
                return np.frombuffer(raw, np.uint8).astype(float)

            start = 1.3333                                          # = frame 40, written as slots.json would round it
            want = frame(["-i", str(src), "-vf", "select=eq(n\\,40)"])
            prev = frame(["-i", str(src), "-vf", "select=eq(n\\,39)"])
            got = frame(["-ss", f"{scenes.seek_ts(round(start, 3)):.4f}", "-i", str(src)])
            self.assertLess(abs(got - want).mean(), abs(got - prev).mean())


if __name__ == "__main__":
    unittest.main()
