"""SFX sugar: "sfx" on ranges / overlays / zooms expands into one-shot audio[] items."""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "helpers"))

import render  # noqa: E402

TIMELINE = {"fps": "30/1", "segments": [
    {"out_start": 0.0, "out_duration": 2.0},
    {"out_start": 2.0, "out_duration": 1.5},
    {"out_start": 3.5, "out_duration": 2.5},
]}
RANGES = [{"source": "a", "start": 0, "end": 2}, {"source": "a", "start": 5, "end": 6.5},
          {"source": "a", "start": 9, "end": 11.5}]


class ExpandSfxTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name)
        self.sfx = self.dir / "sfx"
        self.sfx.mkdir()
        for name in ("whoosh", "pop", "click"):
            (self.sfx / f"{name}.wav").write_bytes(b"RIFF")

    def tearDown(self):
        self._tmp.cleanup()

    def expand(self, edl):
        return render.expand_sfx(edl, TIMELINE, edit_dir=self.dir, sfx_dir=self.sfx)

    def test_range_fires_at_measured_offset_with_attack(self):
        edl = {"ranges": [RANGES[0], {**RANGES[1], "sfx": "whoosh"}, {**RANGES[2], "sfx": "pop"}]}
        items = self.expand(edl)
        self.assertEqual([(Path(a["file"]).name, a["start_in_output"]) for a in items],
                         [("whoosh.wav", 1.75), ("pop.wav", 3.5)])
        self.assertTrue(all(a["gain_db"] == -10 for a in items))
        self.assertEqual(render.ATTACK_S["whoosh"], 0.25)

    def test_attack_never_goes_negative(self):
        items = self.expand({"ranges": [{**RANGES[0], "sfx": "whoosh"}]})
        self.assertEqual(items[0]["start_in_output"], 0.0)

    def test_overlay_list_none_and_gain_precedence(self):
        edl = {"ranges": RANGES, "sfx_gain_db": -14, "overlays": [
            {"file": "x.mp4", "start_in_output": 4.0, "duration": 1, "sfx": ["whoosh", "click"],
             "sfx_gain_db": -6},
            {"file": "y.mp4", "start_in_output": 5.0, "duration": 1, "sfx": "pop"},
            {"file": "z.mp4", "start_in_output": 6.0, "duration": 1, "sfx": "none"},
        ]}
        items = self.expand(edl)
        self.assertEqual([(a["sfx"], a["start_in_output"], a["gain_db"]) for a in items],
                         [("whoosh", 3.75, -6.0), ("click", 4.0, -6.0), ("pop", 5.0, -14.0)])

    def test_zoom_list_and_alternate_zooms(self):
        items = self.expand({"ranges": RANGES, "zooms": [{"start": 1.0, "end": 2.0, "sfx": "click"}]})
        self.assertEqual([(a["sfx"], a["start_in_output"]) for a in items], [("click", 1.0)])
        items = self.expand({"ranges": RANGES, "zooms": {"mode": "alternate", "sfx": "pop"}})
        self.assertEqual([(a["sfx"], a["start_in_output"]) for a in items], [("pop", 0.0), ("pop", 3.5)])
        items = self.expand({"ranges": RANGES, "zooms": {"mode": "alternate", "start": "wide", "sfx": "pop"}})
        self.assertEqual([(a["sfx"], a["start_in_output"]) for a in items], [("pop", 2.0)])

    def test_path_values_resolve_against_edl_dir(self):
        (self.dir / "my").mkdir()
        edl = {"ranges": [RANGES[0], {**RANGES[1], "sfx": "my/whoosh.wav"}, {**RANGES[2], "sfx": "boom.mp3"}]}
        items = self.expand(edl)
        self.assertEqual(items[0]["file"], str((self.dir / "my" / "whoosh.wav").resolve()))
        self.assertEqual(items[0]["start_in_output"], 1.75)   # attack keyed by the file stem
        self.assertEqual(items[1]["file"], str((self.dir / "boom.mp3").resolve()))

    def test_missing_named_sfx_explains_synth(self):
        with self.assertRaises(SystemExit) as cm:
            self.expand({"ranges": [{**RANGES[0], "sfx": "riser"}]})
        self.assertIn("sfx_synth.py assets/sfx", str(cm.exception))

    def test_ranges_without_timeline_use_nominal_durations(self):
        edl = {"ranges": [RANGES[0], {**RANGES[1], "sfx": "pop"}]}
        items = render.expand_sfx(edl, {}, edit_dir=self.dir, sfx_dir=self.sfx)
        self.assertEqual(items[0]["start_in_output"], 2.0)

    def test_default_sfx_dir_is_skill_assets(self):
        self.assertEqual(render.SFX_DIR, Path(render.__file__).resolve().parent.parent / "assets" / "sfx")

    def test_has_sfx(self):
        self.assertFalse(render.has_sfx({"ranges": [{"sfx": "none"}]}))
        self.assertTrue(render.has_sfx({"zooms": {"mode": "alternate", "sfx": "pop"}}))


if __name__ == "__main__":
    unittest.main()
