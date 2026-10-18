import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

HELPERS = Path(__file__).parents[1] / "helpers"
sys.path.insert(0, str(HELPERS))
SPEC = importlib.util.spec_from_file_location("video_edit_captions", HELPERS / "captions.py")
captions = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(captions)


def w(text, start, end):
    return {"type": "word", "text": text, "start": start, "end": end}


class ColorAndTimeTests(unittest.TestCase):
    def test_hex_to_ass(self):
        self.assertEqual(captions.ass_color("#4DA8FF"), "&H00FFA84D")
        self.assertEqual(captions.ass_color("#fff"), "&H00FFFFFF")
        self.assertEqual(captions.ass_color("#000000", 0.6), "&H99000000")
        self.assertEqual(captions.ass_inline_color("#0071F3"), "&HF37100&")

    def test_css_alpha_is_opacity(self):
        self.assertEqual(captions.ass_color("#FF000080"), "&H7F0000FF")

    def test_rejects_garbage(self):
        with self.assertRaises(ValueError):
            captions.ass_color("blue")

    def test_ass_time(self):
        self.assertEqual(captions.ass_time(0), "0:00:00.00")
        self.assertEqual(captions.ass_time(83.456), "0:01:23.46")
        self.assertEqual(captions.ass_time(3725.0), "1:02:05.00")


class ChunkTests(unittest.TestCase):
    def test_max_chars_breaks_before_overflow(self):
        words = [w("Distribution", 0, 0.5), w("matters", 0.52, 0.8), w("more", 0.82, 1.0)]
        chunks = captions.chunk_words(words, words_per_cue=3, max_words=3, max_chars=18)
        self.assertEqual([" ".join(x["text"] for x in c) for c in chunks], ["Distribution", "matters more"])

    def test_defaults_match_render_legacy(self):
        words = [w("a", 0, 0.1), w("b", 0.11, 0.2), w("c", 0.21, 0.3)]
        self.assertEqual(len(captions.chunk_words(words)), 1)   # 3-word cap, too fast for 2


class TransformTests(unittest.TestCase):
    def style(self, **kw):
        return captions.resolve_style(kw)

    def test_fixes_keep_punctuation(self):
        self.assertEqual(captions.transform_word("Mehta,", self.style(fixes={"Mehta": "Meta"}, strip_punct=False)), "Meta,")

    def test_censor(self):
        self.assertEqual(captions.transform_word("shits", self.style(censor=["shits"])), "s***s")

    def test_strip_and_case(self):
        st = self.style(case="upper")
        self.assertEqual(captions.transform_word("wasted.", st), "WASTED")
        self.assertEqual(captions.transform_word("why?", st), "WHY?")
        self.assertEqual(captions.transform_word("3.5", st), "3.5")

    def test_braces_cannot_inject_tags(self):
        self.assertNotIn("{", captions.transform_word("{\\b1}x", self.style()))


class OutputTimelineTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.edit = Path(self.tmp.name)
        (self.edit / "transcripts").mkdir()
        (self.edit / "transcripts" / "A.json").write_text(json.dumps({"words": [
            w("one", 1.0, 1.3), w("two", 1.4, 1.7), w("three", 5.0, 5.4)]}))
        self.edl = {"sources": {"A": "A.mp4"}, "ranges": [
            {"source": "A", "start": 0.9, "end": 1.8}, {"source": "A", "start": 4.9, "end": 5.6}]}

    def tearDown(self):
        self.tmp.cleanup()

    def test_nominal_offsets(self):
        words = captions.output_words(self.edl, self.edit)
        self.assertEqual([x["text"] for x in words], ["one", "two", "three"])
        self.assertAlmostEqual(words[2]["start"], 0.9 + 0.1, places=3)

    def test_measured_timeline_wins(self):
        (self.edit / "timeline.json").write_text(json.dumps({"segments": [
            {"source": "A", "start": 0.9, "end": 1.8, "out_start": 0.0},
            {"source": "A", "start": 4.9, "end": 5.6, "out_start": 0.9333}]}))
        words = captions.output_words(self.edl, self.edit)
        self.assertAlmostEqual(words[2]["start"], 0.9333 + 0.1, places=3)

    def test_stale_timeline_ignored(self):
        (self.edit / "timeline.json").write_text(json.dumps({"segments": [
            {"source": "A", "start": 0.0, "end": 1.0, "out_start": 0.0}]}))
        self.assertEqual(captions.segment_offsets(self.edl, self.edit), [0.0, 0.9])

    def test_word_cut_by_padding_gets_no_caption(self):
        edl = {"sources": {"A": "A.mp4"}, "ranges": [{"source": "A", "start": 1.25, "end": 1.8}]}
        self.assertEqual([x["text"] for x in captions.output_words(edl, self.edit)], ["two"])


class WriteAssTests(unittest.TestCase):
    def test_highlight_events_and_windows(self):
        chunks = [[w("hello", 0.0, 0.4), w("world", 0.45, 0.9)]]
        style = captions.resolve_style({"highlight": "#FF0000", "windows": [{"start": 0.3, "end": 2, "y": 1000}]})
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / "c.ass"
            captions.write_ass(chunks, style, 1080, 1920, out)
            text = out.read_text()
        self.assertIn("PlayResX: 1080", text)
        events = [l for l in text.splitlines() if l.startswith("Dialogue:")]
        self.assertEqual(len(events), 3)             # word 1 split by the window, then word 2
        self.assertIn("\\pos(540,1360)", events[0])   # vertical default caption line
        self.assertIn("\\pos(540,1000)", events[1])
        self.assertIn("\\c&H0000FF&}world", events[2])
        self.assertIn("\\fscx108", events[0])
        self.assertNotIn("\\fscx108", events[1])

    def test_split_overlays_move_captions_to_seam(self):
        edl = {"overlays": [{"layout": "split", "start_in_output": 5, "duration": 3}]}
        self.assertEqual(captions.split_windows(edl, 1920, []), [{"start": 5.0, "end": 8.0, "y": 1037}])
        self.assertEqual(captions.split_windows(edl, 1920, [{"start": 4, "end": 9, "y": 900}]), [])


class FilterQuoteTests(unittest.TestCase):
    def test_paths_with_spaces_and_colons(self):
        q = captions.ff_quote("/Users/x/Application Support/a:b.ass")
        self.assertEqual(q, "'/Users/x/Application Support/a\\:b.ass'")


class RichCaptionTests(unittest.TestCase):
    """reveal / active_pop / emphasis / soft_shadow (opt-in viral styles)."""

    def chunk(self):
        return [[w("we've", 0.0, 0.3), w("got", 0.3, 0.5), w("$15", 0.5, 0.9)]]

    def test_reveal_hides_later_words_and_pops_active(self):
        style = captions.resolve_style({"reveal": True, "active_pop": 12})
        ev = captions.build_events(self.chunk(), style)
        self.assertEqual(len(ev), 3)
        first = ev[0][2]
        self.assertIn("\\alpha&HFF&", first)                  # later words hidden (space kept)
        self.assertIn("\\fscx112\\fscy112\\t(0,110", first)  # active word pops back to 100

    def test_emphasis_dict_and_time_windows(self):
        style = captions.resolve_style({"emphasis": {"$15": "#4CC9F0"}})
        last = captions.build_events(self.chunk(), style)[-1][2]
        self.assertIn(captions.ass_inline_color("#4CC9F0"), last)
        self.assertIn("\\fscx112", last)
        windowed = captions.resolve_style({"emphasis": [{"word": "$15", "color": "#FF6B6B", "start": 10}]})
        self.assertIsNone(captions.emphasis_color("$15", 0.5, windowed))
        self.assertEqual(captions.emphasis_color("$15.", 12.0, windowed), "#FF6B6B")

    def test_soft_shadow_writes_blurred_layer_under_text(self):
        style = captions.resolve_style({"soft_shadow": True, "font": "Inter ExtraBold"})
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "c.ass"
            captions.write_ass(self.chunk(), style, 1080, 1920, out)
            txt = out.read_text()
        self.assertIn("Style: Shadow,Inter ExtraBold", txt)
        dl = [l for l in txt.splitlines() if l.startswith("Dialogue:")]
        self.assertTrue(any(",Shadow," in l and "\\blur12" in l for l in dl))
        self.assertTrue(any(l.startswith("Dialogue: 1,") and ",Cap," in l for l in dl))
        cap_style = next(l for l in txt.splitlines() if l.startswith("Style: Cap,"))
        self.assertIn(",1,0,0,5,", cap_style)  # BorderStyle 1, outline 0, shadow 0

    def test_plain_highlight_unchanged(self):
        style = captions.resolve_style({})
        ev = captions.build_events(self.chunk(), style)
        self.assertNotIn("alpha", ev[0][2])



class DigitEmphasisTests(unittest.TestCase):
    def test_detection(self):
        for word in ("#1", "5", "10x", "$50", "2026", "90%", "3.5,"):
            self.assertTrue(captions.is_numeric_word(word), word)
        for word in ("hello", "x", "ten", ""):
            self.assertFalse(captions.is_numeric_word(word), word)

    def test_color_falls_back_to_highlight_and_explicit_wins(self):
        st = captions.resolve_style({"emphasis_digits": True, "highlight": "#112233"})
        self.assertEqual(captions.emphasis_color("10x", 0, st), "#112233")
        self.assertIsNone(captions.emphasis_color("hello", 0, st))
        st = captions.resolve_style({"emphasis_digits": True, "emphasis_color": "#3CE07A",
                                     "emphasis": {"$50": "#FF0000"}})
        self.assertEqual(captions.emphasis_color("$50", 0, st), "#FF0000")
        self.assertEqual(captions.emphasis_color("2026", 0, st), "#3CE07A")
        st = captions.resolve_style({"emphasis_digits": True, "emphasis": [{"word": "$50", "color": "#FF0000", "start": 5}]})
        self.assertEqual(captions.emphasis_color("$50", 0, st), st["highlight"])   # outside window: digit rule
        self.assertIsNone(captions.emphasis_color("$50", 0, captions.resolve_style({})))

    def chunk(self):
        return [[w("made", 0.0, 0.3), w("$50", 0.3, 0.6), w("today", 0.6, 0.9)]]

    def test_each_mode(self):
        green = captions.ass_inline_color("#3CE07A")
        white = captions.ass_inline_color("#FFFFFF")
        for mode in ("highlight", "plain", "box"):
            st = captions.resolve_style({"mode": mode, "emphasis_digits": True, "emphasis_color": "#3CE07A",
                                         "emphasis_scale": 120})
            ev = captions.build_events(self.chunk(), st)
            self.assertTrue(ev, mode)
            for _, _, text, _ in ev:
                self.assertIn(f"\\c{green}\\fscx120\\fscy120}}$50", text, mode)
                self.assertNotIn(f"\\c{green}\\fscx120\\fscy120}}made", text, mode)
            if mode != "highlight":
                self.assertIn(f"{{\\c{white}\\fscx100\\fscy100}}made", ev[0][2])

    def test_off_by_default_plain_text_unchanged(self):
        ev = captions.build_events(self.chunk(), captions.resolve_style({"mode": "plain"}))
        self.assertEqual(ev[0][2], "made $50 today")


class PresetTests(unittest.TestCase):
    def test_creator_values(self):
        st = captions.resolve_style({"preset": "creator"})
        self.assertEqual(st["font"], "Montserrat ExtraBold")
        self.assertEqual((st["mode"], st["case"], st["pop"]), ("plain", "upper", "in"))
        self.assertTrue(st["emphasis_digits"])
        self.assertEqual(st["emphasis_scale"], 100)
        self.assertIsNone(st["fonts_dir"])

    def test_precedence(self):
        # defaults < preset < brand < EDL < CLI
        brand = {"color": "#EEEEEE", "font": "Brand Sans"}
        edl = {"preset": "creator", "case": "natural"}
        cli = {"font": "Cli Font", "pop": None}
        st = captions.resolve_style(brand, edl, cli)
        self.assertEqual(st["font"], "Cli Font")          # CLI over brand over preset
        self.assertEqual(st["color"], "#EEEEEE")          # brand over preset
        self.assertEqual(st["case"], "natural")           # EDL over preset
        self.assertEqual(st["pop"], "in")                 # preset over defaults; None does not override
        self.assertEqual(st["preset"], "creator")
        self.assertEqual(captions.resolve_style({"preset": "creator"}, {"mode": "box"})["mode"], "box")

    def test_unknown_preset(self):
        with self.assertRaises(ValueError):
            captions.resolve_style({"preset": "nope"})

    def test_outline_ratio(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / "c.ass"
            captions.write_ass([[w("hi", 0, 0.5)]], captions.resolve_style({"preset": "creator", "size": 100}),
                               1080, 1920, out)
            cap = next(l for l in out.read_text().splitlines() if l.startswith("Style: Cap,"))
        self.assertTrue(cap.startswith("Style: Cap,Montserrat ExtraBold,100,"))
        self.assertIn(",1,11.0,", cap)


class PopTests(unittest.TestCase):
    def events(self, chunks, **kw):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / "c.ass"
            captions.write_ass(chunks, captions.resolve_style(kw), 1080, 1920, out)
            return [l for l in out.read_text().splitlines() if l.startswith("Dialogue:")]

    def test_kinds(self):
        self.assertEqual(captions.pop_kind({"pop": True}), "out")
        self.assertEqual(captions.pop_kind({"pop": "out"}), "out")
        self.assertEqual(captions.pop_kind({"pop": "IN"}), "in")
        self.assertIsNone(captions.pop_kind({"pop": False}))
        with self.assertRaises(ValueError):
            captions.pop_kind({"pop": "sideways"})

    def test_tags(self):
        self.assertEqual(captions.POP_TAG, r"{\fscx108\fscy108\t(0,90,\fscx100\fscy100)}")
        self.assertEqual(captions.POP_IN_TAG, r"{\fscx86\fscy86\t(0,67,\fscx95\fscy95)\t(67,100,\fscx100\fscy100)}")

    def test_whole_line_pop(self):
        ch = [[w("hello", 0.0, 0.4), w("world", 0.45, 0.9)]]
        ev = self.events(ch, mode="plain", pop="in")
        self.assertIn("}" + captions.POP_IN_TAG + "hello world", ev[0])
        ev = self.events(ch, mode="plain", pop="out")
        self.assertIn(captions.POP_TAG + "hello world", ev[0])
        ev = self.events(ch, mode="plain", pop=False)
        self.assertNotIn("\\fscx", ev[0])

    def test_rich_pop_is_per_segment_on_cue_start_only(self):
        ch = [[w("we", 0.0, 0.3), w("got", 0.3, 0.5), w("$15", 0.5, 0.9)]]
        ev = self.events(ch, mode="highlight", pop="in", emphasis={"$15": "#4CC9F0"})
        self.assertEqual(len(ev), 3)
        self.assertNotIn("\\fad", ev[0])
        # every word segment animates; the emphasis word scales in to its own 112%
        self.assertEqual(ev[0].count("\\t(67,100,"), 3)
        self.assertIn("\\fscx96\\fscy96\\t(0,67,\\fscx106\\fscy106)\\t(67,100,\\fscx112\\fscy112)}$15", ev[0])
        self.assertNotIn("\\t(", ev[1])                    # later word events are static
        self.assertIn("\\fscx112\\fscy112}$15", ev[1])
        ev = self.events(ch, mode="highlight", pop="out", emphasis={"$15": "#4CC9F0"})
        self.assertEqual(ev[0].count("\\t(0,90,"), 3)

    def test_rich_pop_with_window_split_only_animates_first_piece(self):
        ch = [[w("10x", 0.0, 0.8), w("growth", 0.8, 1.2)]]
        ev = self.events(ch, mode="plain", pop="in", emphasis_digits=True,
                         windows=[{"start": 0.4, "end": 5, "y": 900}])
        self.assertEqual(len(ev), 2)
        self.assertIn("\\t(0,67,", ev[0])
        self.assertNotIn("\\t(", ev[1])


class CreatorEndToEndTests(unittest.TestCase):
    def test_build_captions_with_fake_transcript(self):
        with tempfile.TemporaryDirectory(dir="/private/tmp") as d:
            edit = Path(d)
            (edit / "transcripts").mkdir()
            (edit / "transcripts" / "A.json").write_text(json.dumps({"words": [
                w("We", 0.0, 0.2), w("hit", 0.25, 0.5), w("$50", 0.55, 0.9), w("in", 1.0, 1.1),
                w("2026.", 1.15, 1.6), w("hello", 2.2, 2.6), w("world", 2.65, 3.0)]}))
            edl = {"sources": {"A": "A.mp4"}, "ranges": [{"source": "A", "start": 0.0, "end": 3.2}],
                   "captions": {"preset": "creator"}}
            out = edit / "captions.ass"
            info = captions.build_captions(edl, edit, out, canvas=(1080, 1920))
            txt = out.read_text()
        self.assertEqual(info["style"]["mode"], "plain")
        self.assertIn("Style: Cap,Montserrat ExtraBold,88,", txt)
        dl = [l for l in txt.splitlines() if l.startswith("Dialogue:")]
        self.assertEqual(len(dl), info["cues"])
        green = captions.ass_inline_color("#3CE07A")
        self.assertTrue(any(f"\\c{green}\\fscx86\\fscy86\\t(0,67,\\fscx95\\fscy95)\\t(67,100,\\fscx100\\fscy100)}}$50" in l
                            for l in dl))
        self.assertTrue(any(f"\\c{green}" in l and "}2026" in l for l in dl))
        self.assertTrue(any(l.endswith(captions.POP_IN_TAG + "HELLO WORLD") for l in dl))
        self.assertFalse(any("hello" in l for l in dl))


if __name__ == "__main__":
    unittest.main()
