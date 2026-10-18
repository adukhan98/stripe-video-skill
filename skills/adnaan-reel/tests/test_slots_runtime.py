"""The shared runtime + scene starters: install, starter duration preset, words.html generation."""
import re
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "helpers"))
import slots  # noqa: E402

SKILL = Path(__file__).resolve().parents[1]


class RuntimeFiles(unittest.TestCase):
    def test_runtime_and_starters_exist(self):
        self.assertTrue((SKILL / "templates" / "runtime" / "paper.js").exists())
        self.assertTrue((SKILL / "templates" / "runtime" / "paper.css").exists())
        mode_b = ("chapter_page", "explainer", "mechanism", "blank")      # v6: no speaker on the canvas
        for t in ("hook", "chapter_page", "explainer", "mechanism", "opinion", "wrapup", "cta", "demo", "fullscreen", "blank",
                  "cutout"):
            html = (SKILL / "templates" / "scenes" / f"{t}.html").read_text()
            self.assertTrue(html.startswith("<!doctype html>"), t)
            self.assertIn('href="paper.css"', html, t)
            self.assertIn('src="paper.js"', html, t)
            self.assertIn("window.__timelines", html, t)           # hyperframes lint looks for it statically
            self.assertIn("Paper.init(", html, t)
            self.assertIn('href="marker.css"', html, t)            # v5: the hand-drawn layer is house runtime
            self.assertIn('src="marker.js"', html, t)
            self.assertIn("Marker.init(P)", html, t)
            self.assertIn('"Caveat"', html, t)                     # its font asserted before render
            self.assertIn('data-composition-id="main"', html, t)
            if t in mode_b:
                code = re.sub(r"<!--.*?-->", "", html, flags=re.S)
                self.assertNotRegex(code, r'<div[^>]*class="spk ', t)   # v6 Mode B: no floating corner card by default
            else:
                self.assertRegex(html, r'<video id="[a-z]+" class="clip"', t)  # media needs an id or it renders frozen
        for t in ("hook", "opinion", "wrapup", "cta"):                       # v6 Mode A starters
            self.assertIn('class="spk split"', (SKILL / "templates" / "scenes" / f"{t}.html").read_text(), t)
        self.assertIn('class="spk cutout"', (SKILL / "templates" / "scenes" / "cutout.html").read_text())
        self.assertIn("speaker_cut.webm", (SKILL / "templates" / "scenes" / "cutout.html").read_text())

    def test_three_mode_runtime_and_v6_kit(self):
        js = (SKILL / "templates" / "runtime" / "paper.js").read_text()
        for fn in ('kind === "split"', 'kind === "cutout"', "function splitIn", "function splitOut",
                   "function fullToSplit", "function splitToFull"):
            self.assertIn(fn, js)
        css = (SKILL / "templates" / "runtime" / "paper.css").read_text()
        self.assertIn(".spk.split", css)
        self.assertIn(".spk.cutout", css)
        for tag in ("stamp", "thud", "clunk", "paper", "whoosh", "pop"):
            self.assertTrue((SKILL / "assets" / "sfx" / f"v6_{tag}.wav").exists(), tag)

    def test_marker_runtime(self):
        js = (SKILL / "templates" / "runtime" / "marker.js").read_text()
        for fn in ("function circle", "function underline", "function arrow", "function hatch", "function highlight",
                   "function note", "function tape", "function funnel", "BOIL"):
            self.assertIn(fn, js)
        self.assertTrue((SKILL / "assets" / "fonts" / "Caveat-Variable.ttf").exists())
        for k in (1, 2, 3):
            self.assertTrue((SKILL / "assets" / "sfx" / f"scribble{k}.wav").exists())

    def test_runtime_applies_principles(self):
        js = (SKILL / "templates" / "runtime" / "paper.js").read_text()
        for fn in ("function squash", "function recede", "function arc", "function punch", "function shake",
                   "function exitUp", "function breathe", "function coinIn", "function drawPath", "function cursorClick"):
            self.assertIn(fn, js)
        self.assertIn("anticF", js)              # anticipation frames before hero moves
        self.assertIn("back.out", js)            # overshoot + settle


class Prepare(unittest.TestCase):
    def test_install_runtime_and_starter(self):
        with tempfile.TemporaryDirectory() as tmp:
            hf = Path(tmp) / "hf"
            hf.mkdir()
            slots.install_runtime(hf)
            self.assertTrue((hf / "paper.js").exists() and (hf / "paper.css").exists())
            self.assertTrue((hf / "marker.js").exists() and (hf / "marker.css").exists())
            self.assertTrue((hf / "fonts" / "Caveat-Variable.ttf").exists())
            self.assertTrue((hf / "fonts" / "InterTight-Variable.ttf").exists())
            self.assertTrue(slots.write_starter(hf, "chapter_page", "v04_taste", 166.5 / 30))
            html = (hf / "index.html").read_text()
            self.assertEqual(set(re.findall(r'data-duration="([0-9.]+)"', html)), {"5.5500"})
            self.assertIn("<title>v04_taste</title>", html)
            # an agent-edited scene is never overwritten (index newer than the sentinel)
            import os, time
            os.utime(hf / "index.html", (time.time() + 5, time.time() + 5))
            self.assertFalse(slots.write_starter(hf, "hook", "v04_taste", 1.0))
            self.assertTrue(slots.write_starter(hf, "hook", "v04_taste", 1.0, force=True))

    def test_words_html(self):
        words = [{"start": 10.0, "text": "is"}, {"start": 10.4, "text": "it"}, {"start": 11.2, "text": "A&B"},
                 {"start": 20.0, "text": "later"}]
        out = slots.words_html(words, 10.0, 4.0)
        self.assertIn('<span class="w gap-s" data-t="0.00">is</span>', out)
        self.assertIn('data-t="1.20">A&amp;B</span>', out)
        self.assertNotIn("later", out)


class Beats(unittest.TestCase):
    def test_scribble_beats_and_legacy_marker_beats(self):
        import json
        import scenes
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            (d / "beats.json").write_text(json.dumps([{"t": 1.0, "sfx": "impact"},
                                                      {"t": 0.5, "sfx": "scribble", "dur": 0.3}]))
            b = scenes.load_beats(d, 3.0)
            self.assertEqual([x["sfx"] for x in b], ["scribble", "impact"])
            self.assertIn("scribble", scenes.BEAT_GAIN_DB)
            (d / "beats.json").unlink()
            (d / "marker_beats.json").write_text(json.dumps([{"t": 0.2, "dur": 0.4}]))
            b = scenes.load_beats(d, 3.0)
            self.assertEqual(b[0]["sfx"], "scribble")
            self.assertEqual(b[0]["dur"], 0.4)


if __name__ == "__main__":
    unittest.main()
