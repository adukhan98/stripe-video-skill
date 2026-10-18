import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "helpers"))
import compose  # noqa: E402
import deliver  # noqa: E402


def data(layout=None, scenes=None, total=300):
    return {"total": total, "layout": layout or {}, "scenes": {"scenes": scenes or []},
            "tl": {"segments": [{"start": 10.0, "end": 15.0, "out_start": 0.0, "out_duration": 5.0},
                                {"start": 20.0, "end": 25.0, "out_start": 5.0, "out_duration": 5.0}]}}


def test_every_frame_in_exactly_one_window_scene_wins():
    d = data({"windows": [{"start": 1, "end": 8, "layout": "screen"}]},
             [{"id": "s1", "type": "map", "start": 3, "duration": 2}, {"id": "o1", "type": "callout_overlay", "start": 2, "duration": 1}])
    ws = compose.windows(d)
    assert ws[0]["f0"] == 0 and ws[-1]["f1"] == 300
    assert all(a["f1"] == b["f0"] for a, b in zip(ws, ws[1:]))
    assert [(w["layout"], w["ref"]) for w in ws] == [("talk", None), ("screen", 0), ("scene", "s1"), ("screen", 0), ("talk", None)]
    assert ws[2]["f0"] == 90 and ws[2]["f1"] == 150


def test_out_to_src_maps_through_the_cut():
    d = data()
    assert abs(compose.out_to_src(d["tl"], 2.0) - 12.0) < 1e-9
    assert abs(compose.out_to_src(d["tl"], 6.5) - 21.5) < 1e-9


def test_caption_cues_split_on_sentences_pauses_and_length():
    words = [{"text": w, "start": i * 0.3, "end": i * 0.3 + 0.25} for i, w in enumerate("This is one. And here is".split())]
    words.append({"text": "another.", "start": 5.0, "end": 5.4})
    cs = deliver.cues(words)
    assert [c[2] for c in cs] == ["This is one.", "And here is", "another."]
    assert all(a < b for a, b, _ in cs) and all(cs[i][1] < cs[i + 1][0] for i in range(len(cs) - 1))
    long = [{"text": "word", "start": i * 0.2, "end": i * 0.2 + 0.15} for i in range(60)]
    for a, b, t in deliver.cues(long):
        assert len(deliver.wrap(t)) <= deliver.MAX_LINES and b - a <= deliver.MAX_DUR + 0.8


def test_srt_and_chapters_end_to_end(tmp_path):
    (tmp_path / "transcripts").mkdir()
    (tmp_path / "edl.json").write_text(json.dumps({"ranges": [{"source": "CAM", "start": 10, "end": 15}]}))
    (tmp_path / "timeline.json").write_text(json.dumps({"total": 40.0, "segments": [{"source": "CAM", "start": 10.0, "end": 15.0, "out_start": 0.0, "out_duration": 5.0}]}))
    (tmp_path / "transcripts" / "CAM.json").write_text(json.dumps({"words": [
        {"text": "cut", "start": 2.0, "end": 2.3, "type": "word"},
        {"text": "Hello", "start": 10.5, "end": 10.9, "type": "word"}, {"text": "world.", "start": 11.0, "end": 11.4, "type": "word"}]}))
    deliver.srt(tmp_path)
    s = (tmp_path / "deliver" / "captions.srt").read_text()
    assert "Hello world." in s and "cut" not in s and "00:00:00,500 -->" in s
    (tmp_path / "layout.json").write_text(json.dumps({"chapters": [{"start": 0, "title": "Intro"}, {"start": 12, "title": "One"}, {"start": 25, "title": "Two"}]}))
    deliver.chapters(tmp_path)
    assert (tmp_path / "deliver" / "chapters.txt").read_text().splitlines() == ["0:00 Intro", "0:12 One", "0:25 Two"]
