import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import numpy as np

HELPERS = Path(__file__).parents[1] / "helpers"
sys.path.insert(0, str(HELPERS))


def load(name):
    spec = importlib.util.spec_from_file_location(f"video_edit_{name}", HELPERS / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


transcribe = load("transcribe")
render = load("render")


def tok(text, t_dtw, p=0.9):
    return {"text": text, "t_dtw": t_dtw, "p": p}


class WhisperConversionTests(unittest.TestCase):
    def data(self):
        return {"_dtw": True, "transcription": [{"tokens": [
            tok("[_BEG_]", -1), tok(" If", 166), tok(" you", 178), tok("'re", 190),
            tok(" Insta", 250), tok("gram", 262), tok(",", 270),
            tok(" (", 300), tok("up", 302), tok("beat", 305), tok(" music", 310), tok(")", 320),
            tok(" [", 330), tok("BLANK", 331), tok("_AUDIO", 332), tok("]", 333),
            tok(" bet", 400), tok(".", 420),
        ]}]}

    def test_tokens_merge_into_words_with_shift(self):
        env = np.full(600, -70.0)
        env[160:215] = -20     # "If you're"
        env[245:290] = -20     # "Instagram,"
        env[395:430] = -20     # "bet."
        words = transcribe.whisper_to_words(self.data(), env, duration=6.0)
        texts = [(x["text"], x["type"]) for x in words]
        self.assertEqual(texts, [("If", "word"), ("you're", "word"), ("Instagram,", "word"),
                                 ("(upbeat music)", "audio_event"), ("bet.", "word")])
        self.assertAlmostEqual(words[0]["start"], 1.66 - transcribe.DTW_SHIFT_S, places=3)
        # end trimmed to where the energy stops, not stretched to the next word
        self.assertLess(words[2]["end"], 2.95)
        self.assertGreater(words[2]["end"], words[2]["start"])

    def test_scribe_shape_has_spacing(self):
        words = [{"text": "a", "start": 0.0, "end": 0.2, "type": "word"},
                 {"text": "b", "start": 0.8, "end": 1.0, "type": "word"}]
        out = transcribe.to_scribe_shape(words, "en", {"engine": "whisper.cpp"})
        self.assertEqual([x["type"] for x in out["words"]], ["word", "spacing", "word"])
        self.assertAlmostEqual(out["words"][1]["end"] - out["words"][1]["start"], 0.6)

    def test_english_only_model_refuses_other_languages(self):
        with self.assertRaises(RuntimeError):
            transcribe.call_whisper(Path("x.wav"), model="medium.en", language="es")


class MlxEngineTests(unittest.TestCase):
    def test_mlx_words_keep_onsets_and_trim_ends(self):
        env = np.full(600, -70.0)
        env[100:140] = -20     # "Hello,"
        env[300:330] = -20     # "world."
        result = {"language": "en", "segments": [{"words": [
            {"word": " .", "start": 0.0, "end": 0.5, "probability": 0.2},
            {"word": " Hello,", "start": 1.0, "end": 2.9, "probability": 0.9},
            {"word": " (upbeat", "start": 2.0, "end": 2.2, "probability": 0.5},
            {"word": " music)", "start": 2.2, "end": 2.4, "probability": 0.5},
            {"word": " world.", "start": 3.0, "end": 3.3, "probability": 0.8},
        ]}]}
        words = transcribe.mlx_to_words(result, env, duration=6.0)
        self.assertEqual([(w["text"], w["type"]) for w in words],
                         [("Hello,", "word"), ("(upbeat music)", "audio_event"), ("world.", "word")])
        self.assertAlmostEqual(words[0]["start"], 1.0)          # no DTW shift for mlx
        self.assertLess(words[0]["end"], 1.5)                   # trimmed to the energy
        self.assertAlmostEqual(words[0]["confidence"], 0.9)

    def test_auto_order(self):
        with patch.object(transcribe, "find_api_key", return_value="k"), \
             patch.object(transcribe, "mlx_available", return_value=True):
            self.assertEqual(transcribe.resolve_engine("auto"), ("elevenlabs", "k"))
        with patch.object(transcribe, "find_api_key", return_value=None):
            with patch.object(transcribe, "mlx_available", return_value=True):
                self.assertEqual(transcribe.resolve_engine("auto"), ("mlx", None))
            with patch.object(transcribe, "mlx_available", return_value=False):
                self.assertEqual(transcribe.resolve_engine("auto"), ("whisper", None))
                with self.assertRaises(SystemExit):
                    transcribe.resolve_engine("mlx")

    def test_module_does_not_import_mlx(self):
        self.assertNotIn("mlx_whisper", vars(transcribe))


class FitFilterTests(unittest.TestCase):
    def test_crop_focus(self):
        f = render.fit_filter((1080, 1920), "crop", 0.3, 0.5, "#000000")
        self.assertIn("force_original_aspect_ratio=increase", f)
        self.assertIn("crop=1080:1920:(iw-1080)*0.3000:(ih-1920)*0.5000", f)

    def test_pad_colour(self):
        self.assertIn("color=0xFAF9F5", render.fit_filter((1080, 1080), "pad", 0.5, 0.5, "#faf9f5"))

    def test_draft_canvas(self):
        self.assertEqual(render.output_canvas({"output": {"width": 1080, "height": 1920}}, draft=True), (720, 1280))
        self.assertIsNone(render.output_canvas({}))


class CompositeGraphTests(unittest.TestCase):
    def test_graph_order_and_pieces(self):
        with tempfile.TemporaryDirectory() as d:
            edit = Path(d)
            for f in ("base.mp4", "slot.mov", "logo.png", "bed.m4a", "captions.ass"):
                (edit / f).write_text("x")
            (edit / "timeline.json").write_text(json.dumps({"fps": "30/1"}))
            edl = {
                "overlays": [
                    {"file": "slot.mov", "start_in_output": 2.0, "duration": 3.0, "layout": "split", "crop_y": 300},
                    {"file": "logo.png", "start_in_output": 0, "duration": 10, "x": 850, "y": 300, "width": 110, "opacity": 0.9},
                ],
                "zooms": [{"start": 5, "end": 6, "scale": 1.2, "x": 0.5, "y": 0.4}],
                "audio": [{"file": "bed.m4a", "start_in_output": 0, "duck": True, "fade_out": 1.5}],
                "end_hold": 1.0,
            }
            dims = {str(edit / "base.mp4"): (1080, 1920), str(edit / "slot.mov"): (1080, 1920)}
            with patch.object(render, "probe_dims", side_effect=lambda p: dims.get(str(p))), \
                    patch.object(render, "probe_duration", return_value=10.0):
                inputs, graph, v, a, dur = render.build_composite(
                    edit / "base.mp4", edl, edit, edit / "captions.ass", None, (1080, 1920))
        self.assertEqual(dur, 11.0)
        order = [graph.index(s) for s in ("tpad=stop_mode=clone", "crop=900:1600", "crop=1080:960:0:300",
                                           "format=gbrp[vrgb]", "[vo1]", "[vo2]", "ass=filename=",
                                           "out_color_matrix=bt709")]
        self.assertEqual(order, sorted(order), "end hold → zoom → split → RGB → overlays → captions LAST → BT.709")
        self.assertIn("setpts=PTS-STARTPTS+2.000/TB", graph)
        self.assertIn("colorchannelmixer=aa=0.900", graph)
        self.assertIn("sidechaincompress", graph)
        self.assertIn("apad=pad_dur=1.000", graph)
        self.assertIn("-loop", inputs)


if __name__ == "__main__":
    unittest.main()
