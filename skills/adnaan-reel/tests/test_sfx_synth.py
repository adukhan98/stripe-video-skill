import importlib.util
import sys
import tempfile
import unittest
import wave
from pathlib import Path

import numpy as np

HELPERS = Path(__file__).parents[1] / "helpers"
SFX_DIR = Path(__file__).parents[1] / "assets" / "sfx"
sys.path.insert(0, str(HELPERS))
SPEC = importlib.util.spec_from_file_location("video_edit_sfx_synth", HELPERS / "sfx_synth.py")
sfx = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(sfx)

NAMES = ["whoosh", "chime", "ticks", "ping", "subdrop", "flick"]
ELEVEN = ["pop", "tick", "impact", "riser", "whoosh", "ping", "ding"]   # v4 house kit (ElevenLabs, not synthesized)


def synth_path(name):
    """The synthesized checked-in file: whoosh/ping moved to assets/sfx/synth/ when the ElevenLabs kit took their names."""
    return SFX_DIR / "synth" / f"{name}.wav" if name in sfx.PROTECTED else SFX_DIR / f"{name}.wav"


def read(path):
    with wave.open(str(path), "rb") as w:
        params = (w.getframerate(), w.getnchannels(), w.getsampwidth())
        pcm = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2").reshape(-1, w.getnchannels())
    return params, pcm.astype(np.float64) / 32768


class CheckedInKitTests(unittest.TestCase):
    def test_every_file_exists_48k_stereo_16bit(self):
        for name in NAMES:
            with self.subTest(name=name):
                params, _ = read(synth_path(name))
                self.assertEqual(params, (48000, 2, 2))

    def test_peaks_and_durations(self):
        for name in NAMES:
            with self.subTest(name=name):
                _, x = read(synth_path(name))
                self.assertLessEqual(np.abs(x).max(), 0.95)
                self.assertGreater(np.abs(x).max(), 0.3)
                self.assertTrue(0.05 <= len(x) / 48000 <= 3.0)

    def test_checked_in_files_match_generator(self):
        with tempfile.TemporaryDirectory() as tmp:
            sfx.generate(Path(tmp))
            for name in NAMES:
                with self.subTest(name=name):
                    # +-1 LSB: other BLAS/FFT builds may round a sample differently.
                    _, fresh = read(Path(tmp) / f"{name}.wav")
                    _, kit = read(synth_path(name))
                    self.assertEqual(fresh.shape, kit.shape)
                    self.assertLessEqual(np.abs(fresh - kit).max(), 1.5 / 32768)


class ElevenLabsKitTests(unittest.TestCase):
    def test_house_kit_present_48k_stereo_normalised(self):
        for name in ELEVEN:
            with self.subTest(name=name):
                params, x = read(SFX_DIR / f"{name}.wav")
                self.assertEqual(params, (48000, 2, 2))
                self.assertTrue(0.7 <= np.abs(x).max() <= 0.95)      # peak-normalised to about -1 dBFS
                self.assertTrue(0.2 <= len(x) / 48000 <= 1.5)

    def test_beat_tags_map_to_kit_files(self):
        spec = importlib.util.spec_from_file_location("scenes_mod", HELPERS / "scenes.py")
        scenes = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(scenes)
        self.assertEqual(set(scenes.BEAT_GAIN_DB) - {"scribble"}, set(ELEVEN))
        for name in scenes.BEAT_GAIN_DB:
            if name == "scribble":          # v5 felt-tip: three variants, rotated per stroke
                for f in scenes.SCRIBBLE_FILES:
                    self.assertTrue((SFX_DIR / f).exists(), f)
                continue
            self.assertTrue((SFX_DIR / f"{name}.wav").exists(), name)


class GeneratorTests(unittest.TestCase):
    def test_deterministic_same_bytes_twice(self):
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
            sfx.generate(Path(a))
            sfx.generate(Path(b), list(reversed(NAMES)))      # order must not matter
            for name in NAMES:
                with self.subTest(name=name):
                    self.assertEqual((Path(a) / f"{name}.wav").read_bytes(),
                                     (Path(b) / f"{name}.wav").read_bytes())

    def test_attack_table_matches_peaks(self):
        self.assertEqual(set(sfx.ATTACK_S), set(NAMES))
        self.assertEqual(sfx.ATTACK_S["whoosh"], 0.25)
        for name in NAMES:
            with self.subTest(name=name):
                self.assertAlmostEqual(sfx.peak_time(sfx.synth(name)), sfx.ATTACK_S[name], delta=0.01)

    def test_channels_identical(self):
        _, x = read(synth_path("ping"))
        self.assertTrue(np.array_equal(x[:, 0], x[:, 1]))


if __name__ == "__main__":
    unittest.main()
