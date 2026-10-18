"""Plan where the view looks while it zooms into a screen recording (idea after The Attention Machine's zoom-camera:
eased glides, chained zooms glide straight into each other, a speed cap so long moves take longer instead of whipping).

Zooms are on the SOURCE clock (the recording's own seconds), so each zoom stays on its moment whatever the cuts.
The plan is computed once from the inputs, so the view at any time depends only on that time — seek-safe.

    zooms = gather(cap, screen=(w, h), manual=[...])           # Cap's own zooms win, then click clusters, then manual
    cam = Camera(zooms, screen=(w, h), view=(vw, vh))
    cam.rect(t)   → (x, y, w, h) of the screen recording that fills the view at source time t (screen px)
    cam.point(t, sx, sy) → where screen point (sx, sy) lands in the view (view px), for callouts

A zoom: {"start", "end", "x", "y" (screen px), "scale"}. The view is fully in from start to end, zooms in before start
and out after end; zooms CHAIN_GAP s apart or closer glide into each other without zooming out.
"""

from __future__ import annotations

import math

MAX_SCALE = 3.0
DEFAULT_SCALE = 1.9
CHAIN_GAP = 2.0          # s: closer zooms glide into each other
MIN_GLIDE = 0.55         # s: the shortest move
MAX_SPEED = 0.75         # view widths per second for the centre of the view
CLICK_GAP = 2.5          # s: clicks closer than this are one zoom
LEAD, TAIL = 0.45, 1.6   # s: a click zoom is fully in this long before the first click and holds this long after the last


def ease(u: float) -> float:
    u = min(1.0, max(0.0, u))
    return u * u * u * (u * (u * 6 - 15) + 10)


def gather(cap: dict, screen: tuple[int, int], manual: list[dict] | None = None) -> list[dict]:
    """Zoom list from Cap's own zoom segments, click clusters and manual zooms (source seconds, screen px)."""
    sw, sh = screen
    moves = cap.get("moves") or []

    def mean_pos(a: float, b: float) -> tuple[float, float]:
        pts = [m for m in moves if a <= m["t"] <= b] or [m for m in moves if m["t"] <= b][-1:]
        if not pts:
            return sw / 2, sh / 2
        return sum(m["x"] for m in pts) / len(pts) * sw, sum(m["y"] for m in pts) / len(pts) * sh

    out: list[dict] = []
    for z in cap.get("zooms") or []:   # his own zooms from Cap's editor
        if z.get("mode") == "manual" and z.get("x") is not None:
            x, y = z["x"] * sw, z["y"] * sh
        else:
            x, y = mean_pos(z["start"] - 0.3, z["end"])
        out.append({"start": z["start"], "end": max(z["end"], z["start"] + 0.8), "x": x, "y": y,
                    "scale": min(MAX_SCALE, max(1.2, float(z.get("amount") or DEFAULT_SCALE))), "src": "cap"})
    clicks = sorted(cap.get("clicks") or [], key=lambda c: c["t"])
    cluster: list[dict] = []
    for c in clicks + [None]:
        if c is not None and (not cluster or c["t"] - cluster[-1]["t"] <= CLICK_GAP):
            cluster.append(c)
            continue
        if cluster:
            a, b = cluster[0]["t"] - LEAD, cluster[-1]["t"] + TAIL
            if not any(o["start"] < b and a < o["end"] for o in out):          # Cap's zooms win
                out.append({"start": a, "end": b, "x": sum(k["x"] for k in cluster) / len(cluster) * sw,
                            "y": sum(k["y"] for k in cluster) / len(cluster) * sh, "scale": DEFAULT_SCALE, "src": "click"})
        cluster = [c] if c is not None else []
    for z in manual or []:
        out = [o for o in out if not (o["start"] < z["end"] and z["start"] < o["end"])]   # manual wins over both
        out.append({**z, "scale": min(MAX_SCALE, z.get("scale", DEFAULT_SCALE)), "src": "manual"})
    return sorted(out, key=lambda z: z["start"])


class Camera:
    def __init__(self, zooms: list[dict], screen: tuple[int, int], view: tuple[int, int]):
        self.sw, self.sh = screen
        va = view[0] / view[1]
        # scale 1 = the screen COVERS the view (cropped on one axis if the aspects differ)
        if self.sw / self.sh > va:
            self.bh, self.bw = self.sh, self.sh * va
        else:
            self.bw, self.bh = self.sw, self.sw / va
        self.view = view
        self.base = (self.sw / 2, self.sh / 2, 1.0)
        self.moves: list[tuple[float, float, tuple, tuple]] = []   # (t0, t1, from_state, to_state)
        self._plan(sorted(zooms, key=lambda z: z["start"]))

    def _clamp(self, s: tuple) -> tuple:
        x, y, k = s
        w, h = self.bw / k, self.bh / k
        return (min(max(x, w / 2), self.sw - w / 2), min(max(y, h / 2), self.sh - h / 2), k)

    def _glide(self, a: tuple, b: tuple) -> float:
        # the centre of the view never moves faster than MAX_SPEED view widths a second (measured at the wider view)
        w = self.bw / min(a[2], b[2])
        d = math.hypot(b[0] - a[0], b[1] - a[1]) / w
        zoom = abs(math.log(b[2] / a[2])) / math.log(2) * 0.45      # ~0.45 s per doubling
        return max(MIN_GLIDE, d / MAX_SPEED, zoom)

    def _plan(self, zooms: list[dict]) -> None:
        state, t_free = self.base, -1e9
        for i, z in enumerate(zooms):
            target = self._clamp((z["x"], z["y"], min(MAX_SCALE, z["scale"])))
            g = self._glide(state, target)
            t0 = max(t_free, z["start"] - g)
            self.moves.append((t0, max(t0 + 0.01, z["start"]), state, target))
            state, t_free = target, z["end"]
            nxt = zooms[i + 1] if i + 1 < len(zooms) else None
            if nxt is None or nxt["start"] - z["end"] > CHAIN_GAP:
                g = self._glide(target, self.base)
                self.moves.append((z["end"], z["end"] + g, target, self.base))
                state, t_free = self.base, z["end"] + g

    def state(self, t: float) -> tuple:
        cur = self.base
        for t0, t1, a, b in self.moves:
            if t < t0:
                return cur
            if t <= t1:
                u = ease((t - t0) / (t1 - t0))
                k = math.exp(math.log(a[2]) + (math.log(b[2]) - math.log(a[2])) * u)   # scale moves in log space
                return self._clamp((a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u, k))
            cur = b
        return cur

    def rect(self, t: float) -> tuple[float, float, float, float]:
        x, y, k = self.state(t)
        w, h = self.bw / k, self.bh / k
        return (x - w / 2, y - h / 2, w, h)

    def point(self, t: float, sx: float, sy: float) -> tuple[float, float]:
        x, y, w, h = self.rect(t)
        return ((sx - x) / w * self.view[0], (sy - y) / h * self.view[1])
