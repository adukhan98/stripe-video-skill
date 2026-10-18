import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HELPERS = Path(__file__).parents[1] / "helpers"
sys.path.insert(0, str(HELPERS))


def load(name):
    spec = importlib.util.spec_from_file_location(f"video_edit_{name}", HELPERS / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


storyboard = load("storyboard")
slots = load("slots")
fetch = load("fetch")
HAS_FFMPEG = shutil.which("ffmpeg") is not None


class StoryboardTests(unittest.TestCase):
    def test_timecodes_mix_source_and_duration_beats(self):
        beats = [{"id": "B1", "start": 1.0, "end": 3.5}, {"id": "B2", "duration": 4}, {"id": "B3", "start": 10, "end": 11}]
        self.assertEqual(storyboard.timecodes(beats), [(0.0, 2.5), (2.5, 6.5), (6.5, 7.5)])

    def test_build_writes_board_and_reports_todo(self):
        with tempfile.TemporaryDirectory() as tmp:
            edit = Path(tmp)
            sb = {"title": "T", "version": 2, "format": {"width": 1080, "height": 1920},
                  "target_duration": 10,
                  "beats": [{"id": "B1", "duration": 3, "visual": "graphic", "description": "Collage",
                             "assets": [{"what": "launch film", "status": "find", "rights": "commentary"}]},
                            {"id": "B2", "duration": 2, "visual": "text", "feedback": "make it shorter"}]}
            (edit / "storyboard.json").write_text(json.dumps(sb))
            res = storyboard.build(edit, edit / "storyboard.json")
            self.assertAlmostEqual(res["total"], 5.0)
            self.assertEqual([bid for bid, _ in res["todo"]], ["B1"])
            self.assertEqual(res["missing"], ["B1", "B2"])
            page = (edit / "storyboard" / "storyboard.html").read_text()
            self.assertIn("make it shorter", page)
            self.assertIn("commentary", page)
            self.assertTrue((edit / "storyboard" / "storyboard_v2.html").exists())
            self.assertTrue((edit / "storyboard" / "storyboard.jpg").exists())


class DeadHoldTests(unittest.TestCase):
    def test_detects_still_visible_run(self):
        fps = 10
        visible = [0.0] * 3 + [0.1] * 20
        change = [1.0] * 8 + [0.0] * 15
        self.assertEqual(slots.dead_holds(visible, change, fps), [(0.8, 2.3)])

    def test_moving_or_invisible_is_not_a_hold(self):
        fps = 10
        self.assertEqual(slots.dead_holds([0.1] * 30, [0.05] * 30, fps), [])
        self.assertEqual(slots.dead_holds([0.0] * 30, [0.0] * 30, fps), [])

    @unittest.skipUnless(HAS_FFMPEG, "ffmpeg not installed")
    def test_profile_on_real_alpha_render(self):
        import numpy as np
        fps, w, h = 30, 216, 384
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "r.mov"
            enc = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgba",
                                    "-s", f"{w}x{h}", "-r", str(fps), "-i", "-", "-c:v", "prores_ks",
                                    "-profile:v", "4444", "-pix_fmt", "yuva444p10le", str(out)],
                                   stdin=subprocess.PIPE)
            for i in range(90):                       # box slides in for 0.5 s, then sits still 2.5 s
                f = np.zeros((h, w, 4), dtype=np.uint8)
                x = 20 + min(i, 15) * 6
                f[150:230, x:x + 60] = (255, 255, 255, 255)
                enc.stdin.write(f.tobytes())
            enc.stdin.close()
            enc.wait()
            visible, change = slots.motion_profile(slots.read_frames(out, width=w), fps)
            holds = slots.dead_holds(visible, change, fps)
            self.assertEqual(len(holds), 1)
            self.assertLess(abs(holds[0][0] - 1.0), 0.1)   # still from 0.5 s, judged over a 0.5 s window


class FindRankingTests(unittest.TestCase):
    def test_official_then_verified_then_rest(self):
        res = [{"uploader": "Random Reuploads", "verified": False},
               {"uploader": "Tech News Daily", "verified": True},
               {"uploader": "OpenAI", "verified": True}]
        ranked = fetch.rank_official(res, "openai")
        self.assertEqual([r["uploader"] for r in ranked], ["OpenAI", "Tech News Daily", "Random Reuploads"])
        self.assertTrue(ranked[0]["official"])

    def test_rights(self):
        self.assertEqual(fetch.item_rights("cc-by", False, "commentary"), "cc-by")
        self.assertEqual(fetch.item_rights("other", True, "commentary"), "commentary")
        self.assertEqual(fetch.item_rights("other", True), "user-provided")
        self.assertEqual(fetch.item_rights("other", False), "other")

    def test_logged_commentary_shows_in_credits(self):
        with tempfile.TemporaryDirectory() as tmp:
            edit = Path(tmp)
            shot = edit / "post.png"
            shot.write_bytes(b"\x89PNG")
            fetch.log_file(shot, edit, url="https://x.com/openai/status/1", uploader="OpenAI", rights="commentary")
            text = fetch.write_credits(edit).read_text()
            self.assertIn("Commentary clips", text)
            self.assertNotIn("Needs a rights check", text)


if __name__ == "__main__":
    unittest.main()
