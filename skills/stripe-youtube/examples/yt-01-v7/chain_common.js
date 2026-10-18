/* chain_common.js — THE 11-HABIT DISC CHAIN, shared by all 14 chain scenes (m00_teaser, m01–m11_push, m12/m13_recap).
   Owner: m00_teaser. Geometry, icons, labels and poses = animations/CHAIN_SHARED.md. COPY this file verbatim into your
   hf/ (never edit the copy) so every scene matches to the pixel.

   Load after board.js + v7yt.js:        <script src="chain_common.js"></script>
   Build inside the async init, BEFORE any other tween touches the chain:
     const B = await Board.init();  const V = V7Y.init(B);  const { tl, F } = B;
     const C = buildChain(V, B, { current, done, labels, state, shown, parent });

   OPTIONS (habit numbers are 1-based, 1..11)
     current  0          the habit whose disc is MINT at frame 0 (0 = none, all charcoal)
     done     []         habits that carry the small mint CHECK disc at frame 0 (top-left of the disc, already drawn)
     labels   []         habits whose label + "HABIT n OF 11" kicker are shown at frame 0 (end state, no animation)
     state    "end"      "end"   = connector fully drawn, every disc + glyph shown (open on a previous scene's end state)
                         "fresh" = connector undrawn, every disc hidden except `shown` — then call C.draw(t0) to draw it on
     shown    []         fresh only: habits already visible at frame 0 (C.draw skips their pop)
     parent   "#punch"   world layer (inside #cam): the chain, labels and checks all live here and travel with the camera

   RETURNS C
     C.ch                the V.chain object {wrap, svg, link, len, cum, discs[11], glyphs[11], points, d}
     C.disc(n)           disc element of habit n             C.pt(n) → [x, y] world centre of habit n
     C.draw(t0, o)       fresh: V.chainDraw(C.ch, t0, {skip: shown, gap, first}) — connector draws 1→11, each disc pops as
                         the line reaches it; returns the time the last pop settles
     C.mintTo(n, t)      habit n becomes current (V.mintTo)  C.charcoalTo(n, t) — stops being current (V.charcoalTo)
     C.label(n, t)       label + kicker of habit n: t given → they land at t (kicker 3 f after the label); t omitted →
                         static end state. Returns {label, kicker}. Idempotent per n (built once, reused).
     C.labelOut(n, t)    label + kicker exit in 6 f (faster than the entrance)
     C.check(n, t)       mint check disc of habit n: t given → V.check pops + draws it at t; t omitted → static end state
     C.pose(k)           camera pose [cx, cy, s]: k = "whole" → [1146, 640, 0.85]; k = n → FOCUS n [x+267, y+92, 1.2]
     C.camSet(k)         B.camSet(...C.pose(k))              C.camTo(t, k, {dur = 1.0}) — V.cam(t, ...C.pose(k), {dur})
   window.CHAIN = {PTS, ICONS, LABELS, D, WHOLE, FOCUS_S} for anything bespoke.

   EXACTNESS / SEEK-SAFETY: everything a scene opens on is set synchronously with gsap.set / inline styles at build time
   (no tween at a negative or zero time, no randomness), so frame 0 is exact and later tweens record it as their start.
   Everything animated goes on B.tl (fromTo with immediateRender where an element must be hidden before its time).
   The static check is the exact DOM/geometry V.check ends on (48 px mint disc, white 5.25 px stroke).
   Label: Inter Tight 800, 70 px world (84 px on screen at 1.2), left x-75; ABOVE the disc (top y-165) or, for habits 5, 6, 7, 9,
   BELOW it (top y+147). Kicker: Inter 600, 28 px world, letter-spacing .12em, uppercase, muted, left x-73, 42 px above the label. Number tags (.v7-tag) sit on each disc's top-right edge. */
(function () {
  const PTS = [[300, 300], [660, 300], [1020, 300], [1380, 300], [1380, 640], [1020, 640], [660, 640], [300, 640], [300, 980], [660, 980], [1020, 980]];
  const ICONS = ["pencil-simple-line", "question", "lightbulb-filament", "chalkboard-teacher", "exam", "shield-check",
    "presentation-chart", "book-open-text", "list-checks", "rocket-launch", "mountains"];
  const LABELS = ["Try it yourself first", "Make AI ask you questions", "Ask for the why", "Explain it back", "Quiz yourself",
    "The delegation check", "Make AI show you things", "Actually read what it writes", "Give your agent rules",
    "Keep up with the new tools", "Be more ambitious"];
  const D = 150, WHOLE = [1146, 640, 0.85], FOCUS_S = 1.2, MINT = "#7CC49E";
  const CHECK = { size: 48, dx: -55, dy: -55 };
  // v2 (lead, 2026-10-17): labels sit on EMPTY paper between the rows, left-aligned with the disc, never in the disc row
  // (in-row they ran over the neighbouring discs). ABOVE the disc, except where a turn connector enters from above or the
  // text would cross one: 5, 6, 7, 9 go BELOW. Above: kicker top y-207, label top y-165. Below: kicker y+105, label y+147.
  const BELOW = [5, 6, 7, 9];
  window.CHAIN = { PTS, ICONS, LABELS, D, WHOLE, FOCUS_S, BELOW };

  function css() {
    if (document.getElementById("chain-common-css")) return;
    const st = document.createElement("style");
    st.id = "chain-common-css";
    st.textContent =
      ".ch-label { font-family: 'Inter Tight', sans-serif; font-weight: 800; font-size: 70px; color: var(--ink); }\n" +
      ".ch-kicker { position: absolute; white-space: nowrap; font-family: 'Inter', sans-serif; font-weight: 600; font-size: 28px;" +
      " line-height: 1; letter-spacing: .12em; text-transform: uppercase; color: var(--muted); }\n" +
      ".ch-check .v7-stroke path { fill: none; stroke-linecap: round; stroke-linejoin: round; }";
    document.head.appendChild(st);
  }

  window.buildChain = function buildChain(V, B, { current = 0, done = [], labels = [], state = "end", shown = [], parent = "#punch" } = {}) {
    css();
    const P = typeof parent === "string" ? document.querySelector(parent) : parent;
    const { tl, F } = B;
    const NS = "http://www.w3.org/2000/svg";
    const ch = V.chain(P, { points: PTS, icons: ICONS, d: D, tags: PTS.map((_, i) => i + 1) });
    const idx = (n) => n - 1;

    if (state === "end") V.chainEnd(ch);
    else {   // fresh: connector undrawn (V.chain default), discs hidden except `shown`
      ch.discs.forEach((el, i) => {
        if (shown.includes(i + 1)) return;
        gsap.set(el, { scale: 0, opacity: 0 });
        if (ch.glyphs[i]) gsap.set(ch.glyphs[i], { scale: 0.3, opacity: 0 });
      });
    }
    if (current) gsap.set(ch.discs[idx(current)], { backgroundColor: MINT });

    const labelEls = {}, checkEls = {};
    function label(n, t) {
      if (!labelEls[n]) {
        const [x, y] = PTS[idx(n)];
        const below = BELOW.includes(n);
        const kicker = document.createElement("div");
        kicker.className = "ch-kicker";
        Object.assign(kicker.style, { left: x - 73 + "px", top: y + (below ? 105 : -207) + "px" });
        kicker.textContent = `Habit ${n} of 11`;
        const lab = document.createElement("div");
        lab.className = "k ch-label";
        Object.assign(lab.style, { left: x - 75 + "px", top: y + (below ? 147 : -165) + "px" });
        lab.textContent = LABELS[idx(n)];
        P.appendChild(kicker); P.appendChild(lab);
        labelEls[n] = { label: lab, kicker };
      }
      const L = labelEls[n];
      if (t !== undefined && t !== null) {
        B.in(L.label, t, { type: "left", dist: 50 });
        B.in(L.kicker, t + 3 * F, { type: "fade" });
      }
      return L;
    }
    function labelOut(n, t) {
      const L = label(n);
      tl.to([L.kicker, L.label], { opacity: 0, x: 24, duration: 6 * F, ease: "power2.in", stagger: F, immediateRender: false }, t);
    }
    function check(n, t) {
      const [x, y] = PTS[idx(n)], cx = x + CHECK.dx, cy = y + CHECK.dy;
      if (t !== undefined && t !== null) { checkEls[n] = V.check(P, cx, cy, t, { size: CHECK.size }); return checkEls[n]; }
      // static end state of V.check (same disc, same svg geometry, stroke fully drawn)
      const s = CHECK.size, k = s / 64;
      const host = V.disc(P, { x: cx, y: cy, d: s, mint: true, cls: "ch-check" });
      const svg = document.createElementNS(NS, "svg");
      svg.setAttribute("class", "v7-stroke"); svg.setAttribute("width", s); svg.setAttribute("height", s);
      svg.setAttribute("viewBox", `0 0 ${s} ${s}`);
      const path = document.createElementNS(NS, "path");
      path.setAttribute("d", "M " + [[18 * k, 33 * k], [28 * k, 43 * k], [46 * k, 22 * k]].map((q) => q.join(" ")).join(" L "));
      path.style.stroke = "#fff"; path.style.strokeWidth = Math.max(5, 7 * k);
      svg.appendChild(path); host.appendChild(svg);
      checkEls[n] = host;
      return host;
    }

    for (const n of done) check(n);
    for (const n of labels) label(n);

    const pose = (k) => (k === "whole" ? WHOLE.slice() : [PTS[idx(k)][0] + 267, PTS[idx(k)][1] + 92, FOCUS_S]);
    return {
      ch, labelEls, checkEls, pose,
      disc: (n) => ch.discs[idx(n)],
      pt: (n) => PTS[idx(n)].slice(),
      draw: (t0, o = {}) => V.chainDraw(ch, t0, { ...o, skip: (o.skip || []).concat(shown.map(idx)) }),
      mintTo: (n, t) => V.mintTo(ch.discs[idx(n)], t),
      charcoalTo: (n, t) => V.charcoalTo(ch.discs[idx(n)], t),
      label, labelOut, check,
      camSet: (k) => B.camSet(...pose(k)),
      camTo: (t, k, { dur = 1.0 } = {}) => V.cam(t, ...pose(k), { dur }),
    };
  };
})();
