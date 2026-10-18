"""Creator-reel layouts: media split overlays, full_pip face circle, alternate zooms, --sheet."""

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SKILL = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SKILL / "helpers"))

import render  # noqa: E402

TIMELINE = {"fps": "30/1", "segments": [
    {"out_start": 0.0, "out_duration": 2.0},
    {"out_start": 2.0, "out_duration": 1.5},
    {"out_start": 3.5, "out_duration": 2.5},
    {"out_start": 6.0, "out_duration": 2.0},
]}


class PanelDetectionTests(unittest.TestCase):
    C = [(1080, 1920)]

    def test_alpha_canvas_sized_is_panel(self):
        self.assertTrue(render.overlay_is_panel(".mov", "yuva444p12le", (1080, 1920), self.C))
        self.assertTrue(render.overlay_is_panel(".png", "rgba", (1080, 1920), self.C))
        self.assertTrue(render.overlay_is_panel(".webm", "yuv420p", (1080, 1920), self.C))  # VP9 alpha probes as yuv

    def test_media_is_not_panel(self):
        self.assertFalse(render.overlay_is_panel(".mp4", "yuv420p", (1920, 1080), self.C))
        self.assertFalse(render.overlay_is_panel(".mp4", "yuv420p", (1080, 1920), self.C))
        self.assertFalse(render.overlay_is_panel(".png", "rgb24", (1080, 1920), self.C))
        self.assertFalse(render.overlay_is_panel(".mov", "yuva444p", (1280, 720), self.C))

    def test_unprobeable_keeps_legacy(self):
        self.assertTrue(render.overlay_is_panel(".mp4", None, None, self.C))


class MediaFitTests(unittest.TestCase):
    def test_cover_focus(self):
        f = render.media_fit_chain("cover", 1080, 960, 0.5, 0.2)
        self.assertIn("force_original_aspect_ratio=increase", f)
        self.assertIn("crop=1080:960:(iw-1080)*0.500:(ih-960)*0.200", f)

    def test_contain_pad_default(self):
        f = render.media_fit_chain("contain", 1080, 960)
        self.assertIn("pad=1080:960", f)
        self.assertIn("color=0x0E0E10", f)


class AlternateZoomTests(unittest.TestCase):
    def test_default_zooms_odd_segments_from_one(self):
        z = render.alternate_zooms(TIMELINE, [], 1.15, 0.5, 0.36, True)
        self.assertEqual([(a["start"], a["end"]) for a in z], [(0.0, 2.0), (3.5, 6.0)])
        self.assertEqual(z[0]["scale"], 1.15)
        self.assertEqual((z[0]["x"], z[0]["y"]), (0.5, 0.36))

    def test_start_wide_flips_phase(self):
        z = render.alternate_zooms(TIMELINE, [], 1.15, 0.5, 0.36, True, start="wide")
        self.assertEqual([(a["start"], a["end"]) for a in z], [(2.0, 3.5), (6.0, 8.0)])

    def test_overlay_windows_are_skipped(self):
        ovs = [{"layout": "split", "start_in_output": 4.0, "duration": 1.0},
               {"layout": "full_pip", "start_in_output": 0.0, "duration": 2.5},
               {"start_in_output": 3.5, "duration": 2.5}]            # plain overlay: not skipped
        z = render.alternate_zooms(TIMELINE, ovs, 1.15, 0.5, 0.36, True)
        self.assertEqual([(a["start"], a["end"]) for a in z], [(3.5, 4.0), (5.0, 6.0)])
        z = render.alternate_zooms(TIMELINE, ovs, 1.15, 0.5, 0.36, False)
        self.assertEqual(len(z), 2)

    def test_resolve_zooms_object_and_list(self):
        self.assertEqual(render.resolve_zooms({"zooms": [{"start": 1, "end": 2}]}, TIMELINE),
                         [{"start": 1, "end": 2}])
        z = render.resolve_zooms({"zooms": {"mode": "alternate", "scale": 1.2}}, TIMELINE)
        self.assertEqual([a["scale"] for a in z], [1.2, 1.2])
        with self.assertRaises(SystemExit):
            render.resolve_zooms({"zooms": {"mode": "random"}}, TIMELINE)

    def test_end_hold_extends_last_zoom(self):
        edl = {"zooms": {"mode": "alternate", "start": "wide"}, "end_hold": 1.2}
        z = render.resolve_zooms(edl, TIMELINE)          # wide: last segment (6.0-8.0) is zoomed
        self.assertEqual([(a["start"], a["end"]) for a in z], [(2.0, 3.5), (6.0, 9.2)])
        edl = {"zooms": {"mode": "alternate"}, "end_hold": 1.2}
        z = render.resolve_zooms(edl, TIMELINE)          # zoomed: last segment is wide, untouched
        self.assertEqual([(a["start"], a["end"]) for a in z], [(0.0, 2.0), (3.5, 6.0)])


class PipGeometryTests(unittest.TestCase):
    def test_default_in_safe_zone(self):
        g = render.pip_geometry({"layout": "full_pip"}, {}, (1080, 1920))
        x0, y0, x1, y1 = render.get_platform("vertical")["safe"]
        self.assertEqual(g["size"], 340)
        self.assertEqual((g["x"], g["y"]), (x1 - 340 - 24, y0 + 24))
        self.assertEqual(g["crop_y"], 1920 * 0.2)

    def test_platform_face_crop_and_overrides(self):
        g = render.pip_geometry({"layout": "full_pip"}, {"platform": "tiktok", "face_crop_y": 500}, (1080, 1920))
        self.assertEqual((g["x"], g["y"], g["crop_y"]), (940 - 340 - 24, 160 + 24, 500))
        g = render.pip_geometry({"layout": "full_pip", "pip": {"size": 300, "crop_y": 420, "x": 10, "y": 20}},
                                {"face_crop_y": 500}, (1080, 1920))
        self.assertEqual((g["size"], g["x"], g["y"], g["crop_y"]), (300, 10, 20, 420))
        self.assertIsNone(render.pip_geometry({"layout": "full_pip", "pip": False}, {}, (1080, 1920)))

    def test_size_scales_with_canvas(self):
        self.assertEqual(render.pip_geometry({"layout": "full_pip"}, {}, (720, 1280))["size"], 227)


class CompositeLayoutGraphTests(unittest.TestCase):
    def test_media_split_and_full_pip_graph(self):
        with tempfile.TemporaryDirectory() as d:
            edit = Path(d)
            for f in ("base.mp4", "demo.mp4", "shot.png", "panel.mov"):
                (edit / f).write_text("x")
            (edit / "timeline.json").write_text(json.dumps(TIMELINE))
            edl = {
                "face_crop_y": 450,
                "overlays": [
                    {"file": "demo.mp4", "start_in_output": 1.0, "duration": 2.0, "layout": "split",
                     "focus_y": 0.0, "loop": True, "trim_start": 0.5},
                    {"file": "shot.png", "start_in_output": 3.5, "duration": 1.0, "layout": "split"},
                    {"file": "demo.mp4", "start_in_output": 5.0, "duration": 2.0, "layout": "full_pip"},
                    {"file": "panel.mov", "start_in_output": 7.0, "duration": 1.0, "layout": "split", "crop_y": 300},
                ],
                "zooms": {"mode": "alternate"},
            }
            # draft base: 720x1280 on a 1080x1920 canvas
            dims = {"base.mp4": (720, 1280), "demo.mp4": (1920, 1080), "shot.png": (1200, 800),
                    "panel.mov": (1080, 1920)}
            pix = {"demo.mp4": "yuv420p", "shot.png": "rgb24", "panel.mov": "yuva444p12le"}
            with patch.object(render, "probe_dims", side_effect=lambda p: dims.get(Path(p).name)), \
                    patch.object(render, "probe_pix_fmt", side_effect=lambda p: pix.get(Path(p).name)), \
                    patch.object(render, "probe_duration", return_value=8.0):
                inputs, graph, v, a, dur = render.build_composite(
                    edit / "base.mp4", edl, edit, None, None, (1080, 1920))
            gen = json.loads((edit / "_zooms_generated.json").read_text())
            mask_exists = (edit / "_work" / "pip_mask_226.png").exists()
        # media split: video cover into the top half, image contain with the default pad
        self.assertIn("crop=720:640:(iw-720)*0.500:(ih-640)*0.000", graph)
        self.assertIn("pad=720:640:(ow-iw)/2:(oh-ih)/2:color=0x0E0E10", graph)
        # loop + trim_start on the input, trimmed in the graph
        i = inputs.index("-stream_loop")
        self.assertEqual(inputs[i:i + 4], ["-stream_loop", "-1", "-ss", "0.500"])
        self.assertIn("trim=duration=2.000", graph)
        # speaker swap: media uses the whole window, panel keeps the 0.15 inset and its own crop_y
        self.assertIn("crop=720:640:0:300", graph)            # face_crop_y 450 * 2/3
        self.assertIn("between(t,1.000,3.000)", graph)
        self.assertIn("crop=720:640:0:200", graph)            # panel crop_y 300 * 2/3
        self.assertIn("between(t,7.150,7.850)", graph)
        # full_pip: full-canvas cover + circle via alphamerge, in the scaled safe zone
        self.assertIn("crop=720:1280:(iw-720)*0.500:(ih-1280)*0.500", graph)
        self.assertIn("alphamerge", graph)
        self.assertIn("split=2[vrgbm][pipsrc2]", graph)
        self.assertIn("overlay=x=384:y=206", graph)           # (940-340-24, 285+24) * 2/3
        self.assertTrue(mask_exists)
        # alternate zooms skip every media window
        self.assertEqual([(z["start"], z["end"]) for z in gen], [(0.0, 1.0), (4.5, 5.0)])
        # order: zoom → split → RGB → overlays → BT.709
        order = [graph.index(s) for s in ("crop=626:1112", "crop=720:640:0:300", "format=gbrp[vrgb]",
                                          "alphamerge", "out_color_matrix=bt709")]
        self.assertEqual(order, sorted(order))
        self.assertEqual(dur, 8.0)


@unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "ffmpeg not installed")
class CreatorReelSmokeTest(unittest.TestCase):
    def test_draft_render(self):
        with tempfile.TemporaryDirectory(dir="/private/tmp") as d:
            edit = Path(d)

            def ff(*args):
                subprocess.run(["ffmpeg", "-y", "-v", "error", *args], check=True)

            ff("-f", "lavfi", "-i", "testsrc=size=1080x1920:rate=30:duration=3",
               "-f", "lavfi", "-i", "sine=frequency=440:duration=3:sample_rate=48000",
               "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest",
               str(edit / "talk.mp4"))
            ff("-f", "lavfi", "-i", "testsrc2=size=640x360:rate=30:duration=2",
               "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p", str(edit / "demo.mp4"))
            ff("-f", "lavfi", "-i", "sine=frequency=1200:duration=0.3:sample_rate=48000", str(edit / "hit.wav"))
            edl = {
                "sources": {"talk": str(edit / "talk.mp4")},
                "output": {"width": 1080, "height": 1920, "fps": 30},
                "ranges": [{"source": "talk", "start": 0, "end": 1},
                           {"source": "talk", "start": 1, "end": 2, "sfx": str(edit / "hit.wav")},
                           {"source": "talk", "start": 2, "end": 3}],
                "overlays": [
                    {"file": "demo.mp4", "start_in_output": 0.2, "duration": 0.9, "layout": "split"},
                    {"file": "demo.mp4", "start_in_output": 1.8, "duration": 1.0, "layout": "full_pip",
                     "loop": True, "trim_start": 1.5, "sfx": "./hit.wav"},
                ],
                "zooms": {"mode": "alternate", "scale": 1.15},
            }
            (edit / "edl.json").write_text(json.dumps(edl))
            out = edit / "out.mp4"
            proc = subprocess.run([sys.executable, str(SKILL / "helpers" / "render.py"), str(edit / "edl.json"),
                                   "-o", str(out), "--draft", "--sheet"], capture_output=True, text=True)
            self.assertEqual(proc.returncode, 0, proc.stdout[-2000:] + proc.stderr[-2000:])
            self.assertTrue(out.exists())
            self.assertAlmostEqual(render.probe_duration(out), 3.0, delta=0.2)
            self.assertTrue((edit / "out_sheet.jpg").exists())
            self.assertTrue((edit / "_zooms_generated.json").exists())
            self.assertIn("alphamerge", (edit / "_composite_graph.txt").read_text())


if __name__ == "__main__":
    unittest.main()
