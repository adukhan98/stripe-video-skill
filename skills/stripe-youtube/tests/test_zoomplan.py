import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "helpers"))
import zoomplan as zp  # noqa: E402

SCREEN, VIEW = (1600, 1000), (1424, 842)


def test_no_zoom_covers_view():
    cam = zp.Camera([], SCREEN, VIEW)
    x, y, w, h = cam.rect(10)
    assert abs(w / h - VIEW[0] / VIEW[1]) < 1e-6
    assert 0 <= x and 0 <= y and x + w <= SCREEN[0] + 1e-6 and y + h <= SCREEN[1] + 1e-6


def test_fully_in_during_zoom_and_out_after():
    z = [{"start": 5, "end": 8, "x": 1400, "y": 560, "scale": 2.0}]
    cam = zp.Camera(z, SCREEN, VIEW)
    assert abs(cam.state(6)[2] - 2.0) < 1e-9
    assert cam.state(0)[2] == 1.0
    assert abs(cam.state(30)[2] - 1.0) < 1e-9
    # the target point is in view while zoomed (clamped near the edge, never off-screen)
    px, py = cam.point(6.5, 1400, 560)
    assert 0 <= px <= VIEW[0] and 0 <= py <= VIEW[1]


def test_rect_never_leaves_screen():
    z = [{"start": 2, "end": 3, "x": 1599, "y": 999, "scale": 3.0}, {"start": 4, "end": 5, "x": 0, "y": 0, "scale": 2.5}]
    cam = zp.Camera(z, SCREEN, VIEW)
    for i in range(0, 300):
        x, y, w, h = cam.rect(i / 30)
        assert x >= -1e-6 and y >= -1e-6 and x + w <= SCREEN[0] + 1e-6 and y + h <= SCREEN[1] + 1e-6


def test_close_zooms_chain_without_zooming_out():
    z = [{"start": 2, "end": 3, "x": 300, "y": 300, "scale": 2.0}, {"start": 4.2, "end": 5, "x": 1200, "y": 700, "scale": 2.0}]
    cam = zp.Camera(z, SCREEN, VIEW)
    assert min(cam.state(3 + i / 30)[2] for i in range(36)) > 1.9


def test_glide_respects_speed_cap():
    a = zp.Camera([], SCREEN, VIEW)
    g = a._glide((100, 100, 2.0), (1500, 900, 2.0))
    assert g >= zp.MIN_GLIDE
    assert g >= ((1400 ** 2 + 800 ** 2) ** 0.5) / (a.bw / 2.0) / zp.MAX_SPEED - 1e-9


def test_gather_cap_wins_over_clicks_and_manual_wins_over_all():
    cap = {"zooms": [{"start": 10, "end": 12, "amount": 1.5, "mode": "auto"}],
           "clicks": [{"t": 10.5, "x": 0.5, "y": 0.5}, {"t": 30, "x": 0.25, "y": 0.75}, {"t": 31, "x": 0.27, "y": 0.73}],
           "moves": [{"t": 10.0, "x": 0.9, "y": 0.5}]}
    z = zp.gather(cap, SCREEN)
    assert [o["src"] for o in z] == ["cap", "click"]
    assert abs(z[0]["x"] - 1440) < 1e-6           # Cap auto zoom centres on where the cursor was
    assert z[1]["start"] < 30 < 31 < z[1]["end"]   # two close clicks = one zoom
    z2 = zp.gather(cap, SCREEN, manual=[{"start": 29, "end": 33, "x": 800, "y": 500, "scale": 2.2}])
    assert [o["src"] for o in z2] == ["cap", "manual"]
