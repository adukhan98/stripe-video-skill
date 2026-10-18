import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "helpers"))
import lookdowns  # noqa: E402
import talkcaps  # noqa: E402


def words(text, gap=0.3):
    return [(w, i * gap, i * gap + 0.25) for i, w in enumerate(text.split())]


def test_phrases_break_at_sentences_and_stay_short():
    ph = talkcaps.phrases_of(words("This is the first point. And then you ask yourself what you would do if the tool was gone tomorrow."))
    assert [w for w, *_ in ph[0]] == ["This", "is", "the", "first", "point."]
    assert all(len(p) <= 7 for p in ph)
    assert all(talkcaps.norm(p[-1][0]) not in {"the", "to", "a"} for p in ph[:-1])


def test_lines_and_hero():
    ph = words("never let the tool think first")
    assert [len(ln) for ln in talkcaps.lines_of(ph)] == [3, 3]
    assert talkcaps.hero_of(ph, set()) == "never"          # longest content word, first on a tie
    assert talkcaps.hero_of(ph, {"first"}) == "first"     # a configured hero wins


def test_schedule_leads_words_spaced_and_lands_before_exit():
    flat = [("a", 0.5, 0.6), ("b", 0.51, 0.6), ("c", 2.9, 3.0)]
    t = talkcaps.schedule(flat, 3.0)
    assert t[0] == 0.4 and all(b - a >= 2 * talkcaps.F - 1e-6 for a, b in zip(t, t[1:]))
    assert t[-1] <= 3.0 - 6 * talkcaps.F - talkcaps.RULE + 1e-6


def test_lookdown_holds_at_start_end_and_whole_range():
    segs = [{"start": 10.0, "end": 14.0, "out_start": 0.0, "out_duration": 4.0},
            {"start": 20.0, "end": 22.0, "out_start": 4.0, "out_duration": 2.0}]
    filters, report = lookdowns.holds(segs, [(9.5, 10.5), (13.5, 14.2), (19.8, 22.5)], pad=0)
    assert filters[0] == "freezeframes=first=0:last=15:replace=16"       # head comes up at 10.5 s → hold to frame 15
    assert filters[1] == "freezeframes=first=105:last=119:replace=104"   # head goes down at 13.5 s
    assert filters[2] == "freezeframes=first=120:last=179:replace=119"   # down the whole range → previous frame
    assert len(report) == 3


def test_down_spans_parses_headpose_report(tmp_path):
    r = tmp_path / "hp.txt"
    r.write_text("t pitch\n# looking down: 1.0-2.5, 7.25-8\n")
    assert lookdowns.down_spans(r) == [(1.0, 2.5), (7.25, 8.0)]
    r.write_text("# looking down: none\n")
    assert lookdowns.down_spans(r) == []
