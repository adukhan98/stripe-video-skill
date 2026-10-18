/* chain_common.js — THE 9-STAGE PIPELINE CHAIN, shared by all 10 chain scenes of this video (m01_stages … m10_render).
   Owner: m01_stages. Geometry = animations/m01_stages/hf/CHAIN_SHARED.md. COPY this file byte-identical into every
   m01…m10 hf/ (never edit a copy) so every scene matches to the pixel and each push opens on the previous push's end state.

   Load after board.js + v7yt.js (+ brand.css in the head):   <script src="chain_common.js"></script>
     const B = await Board.init();  const V = V7Y.init(B);
     const C = buildChain(V, B, { current, labels, heading, state, shown });

   OPTIONS (stage numbers 1-based, 1..9)
     current  0 | n | [n…]  discs that are ACCENT at frame 0 (class .mint → var(--brand-primary)); 0 = all slate
     labels   [] | "all"    stages whose label is shown at frame 0 (static end state)
     heading  false         the "Nine stages" heading shown at frame 0 (m01's end state; m02 takes it out)
     state    "end"         "end" = connector drawn, every disc shown · "fresh" = connector undrawn, discs hidden except `shown`
     shown    []            fresh only: stages visible at frame 0

   RETURNS C
     C.ch / C.disc(n) / C.pt(n) / C.glyph(n)
     C.draw(t0, {gap, first})   fresh: connector draws 1→9, each disc pops as the line reaches it (V.chainDraw)
     C.accentTo(n, t) / C.slateTo(n, t)   colour cross-fade between the TOKENS (--brand-primary / --brand-deep, read
                                from the computed style: never a typed hex) + the small punch on accent
     C.label(n, t, {type, dist, dur})  label of stage n: t → lands at t (B.in), no t → static. Idempotent per n.
     C.labelOut(n|[n…], t)      exit in 6 f (faster than entrances)
     C.heading(t1, t2)          heading: no args → static; else "Nine" lands at t1, "stages" at t2. C.headingOut(t)
     C.pose(k)                  "whole" | n (FOCUS n) | "final" (m10: the chain + the render disc) → [cx, cy, s]
     C.travel(segs, LAST)       the camera as ONE pure function of time (seek-safe, applied by a clock on B.tl).
                                segs = [[t0, dur, fromPose, toPose, {lift, zout, dip}] …], consecutive. Frame 0 = segs[0]
                                from-pose; after the last segment the camera rests EXACTLY on its to-pose (holds until LAST).
                                x power2.inOut, y + scale power3.inOut (different eases = an arc); lift = world px the path
                                bows upward mid-move; zout = breath of zoom-out mid-move (negative = a push-in breath; from = to gives a pure breath); dip = anticipation pull-back
                                (log-scale) in the 0.12 s before t0. Returns camPose(t).
   window.CHAIN = {PTS, ICONS, LABELS, D, WHOLE, FINAL, FOCUS_S, FOCUS_X, FOCUS_Y, FOCUS_Y0, RENDER_PT} */
(function () {
  const PTS = [[300, 815], [600, 617], [900, 500], [1200, 497], [1500, 575], [1800, 653], [2100, 650], [2400, 533], [2700, 335]];
  const ICONS = ["microphone", "scissors", "palette", "images", "clipboard-text", "code", "speaker-high", "film-strip", "check-circle"];
  const LABELS = ["Transcribe", "Cut", "Brand", "Assets", "Plan", "Build", "Sound", "Assemble", "Check"];
  const D = 150;
  const WHOLE = [1530, 575, 2 / 3];               // all 9 discs: screen x 140…1740 (200 px apart), labels 34 px on screen
  const FOCUS_S = 1.25, FOCUS_X = 700, FOCUS_Y = { 3: 320, 4: 320 }, FOCUS_Y0 = 430;
  // FOCUS n: disc n at screen (700, 430) — (700, 320) for 3 and 4, so disc n+3 (screen x 1825) stays ABOVE the speaker-card
  // box (x 1574–1886, y 614–1012); label 64 px on screen
  const RENDER_PT = [3000, 250];                  // m10's render disc, one step past Check on the line
  const FINAL = [1683.75, 575, 1600 / 2700];      // m10 end: disc 1 at screen x 140, render disc at x 1740
  const LABEL_PX = 51, LABEL_DY = 93;             // label: 51 px world (34 px at WHOLE), top = disc centre + 93
  const HEAD = [{ txt: "Nine", x: 255, y: -55, px: 225, accent: true }, { txt: "stages", x: 390, y: 155, px: 165 }];
  window.CHAIN = { PTS, ICONS, LABELS, D, WHOLE, FINAL, FOCUS_S, FOCUS_X, FOCUS_Y, FOCUS_Y0, RENDER_PT };

  function css() {
    if (document.getElementById("chain-common-css")) return;
    const st = document.createElement("style");
    st.id = "chain-common-css";
    st.textContent =
      ".ch-label { position: absolute; white-space: nowrap; font-family: 'Inter Tight', sans-serif; font-weight: 800;" +
      " font-size: " + LABEL_PX + "px; line-height: 1; letter-spacing: -.02em; color: var(--ink); }\n" +
      ".ch-head { position: absolute; white-space: nowrap; font-family: 'Inter Tight', sans-serif; font-weight: 900;" +
      " line-height: 1; letter-spacing: -.045em; color: var(--ink); }";
    document.head.appendChild(st);
  }
  const tok = (name) => getComputedStyle(document.body).getPropertyValue(name).trim();

  window.buildChain = function buildChain(V, B, { current = 0, labels = [], heading = false, state = "end", shown = [], parent = "#punch" } = {}) {
    css();
    const P = typeof parent === "string" ? document.querySelector(parent) : parent;
    const { tl, F } = B;
    const ACC = tok("--brand-primary"), SLATE = tok("--brand-deep");
    const ch = V.chain(P, { points: PTS, icons: ICONS, d: D, tags: PTS.map((_, i) => i + 1), w: 3400, h: 1300 });
    const idx = (n) => n - 1;

    if (state === "end") V.chainEnd(ch);
    else ch.discs.forEach((el, i) => {
      if (shown.includes(i + 1)) return;
      gsap.set(el, { scale: 0, opacity: 0 });
      if (ch.glyphs[i]) gsap.set(ch.glyphs[i], { scale: 0.3, opacity: 0 });
    });
    [].concat(current).filter(Boolean).forEach((n) => ch.discs[idx(n)].classList.add("mint"));

    const labelEls = {};
    function label(n, t, { type = "up", dist = 30, dur = 16 / 30 } = {}) {
      if (!labelEls[n]) {
        const [x, y] = PTS[idx(n)];
        const el = document.createElement("div");
        el.className = "ch-label";
        Object.assign(el.style, { left: x + "px", top: y + LABEL_DY + "px" });
        el.textContent = LABELS[idx(n)];
        P.appendChild(el);
        gsap.set(el, { xPercent: -50 });
        labelEls[n] = el;
      }
      if (t !== undefined && t !== null) B.in(labelEls[n], t, { type, dist, dur });
      return labelEls[n];
    }
    function labelOut(ns, t) {
      const els = [].concat(ns).map((n) => label(n));
      tl.to(els, { opacity: 0, y: 14, duration: 6 * F, ease: "power2.in", stagger: F, immediateRender: false }, t);
    }

    let headEls = null;
    function headBuild() {
      if (headEls) return headEls;
      headEls = HEAD.map((h) => {
        const el = document.createElement("div");
        el.className = "ch-head" + (h.accent ? " mint" : "");
        Object.assign(el.style, { left: h.x + "px", top: h.y + "px", fontSize: h.px + "px" });
        el.textContent = h.txt;
        P.appendChild(el);
        return el;
      });
      return headEls;
    }
    function headingIn(t1, t2) {
      const [a, b] = headBuild();
      if (t1 !== undefined) { B.word(a, t1, true); B.word(b, t2 === undefined ? t1 + 4 * F : t2, false); }
    }
    function headingOut(t) {
      tl.to(headBuild(), { opacity: 0, y: -30, duration: 7 * F, ease: "power2.in", stagger: 2 * F, immediateRender: false }, t);
    }

    if (labels === "all") PTS.forEach((_, i) => label(i + 1));
    else labels.forEach((n) => label(n));
    if (heading) headBuild();

    function accentTo(n, t) {
      const el = ch.discs[idx(n)];
      tl.to(el, { backgroundColor: ACC, duration: 6 * F, ease: "power2.out" }, t);
      tl.to(el, { scale: 1.1, duration: 4 * F, ease: "power2.out" }, t);
      tl.to(el, { scale: 1, duration: 8 * F, ease: "power2.inOut" }, t + 4 * F);
    }
    function slateTo(n, t) { tl.to(ch.discs[idx(n)], { backgroundColor: SLATE, duration: 6 * F, ease: "power2.out" }, t); }

    const pose = (k) => (k === "whole" ? WHOLE.slice() : k === "final" ? FINAL.slice()
      : [PTS[idx(k)][0] + (960 - FOCUS_X) / FOCUS_S, PTS[idx(k)][1] + (540 - (FOCUS_Y[k] || FOCUS_Y0)) / FOCUS_S, FOCUS_S]);

    function travel(segs, LAST) {
      const E = (n) => gsap.parseEase(n);
      const e2 = E("power2.inOut"), e3 = E("power3.inOut");
      const cl = (v) => Math.max(0, Math.min(1, v));
      const P0 = typeof segs[0][2] === "object" ? segs[0][2] : pose(segs[0][2]);
      const S = segs.map(([t0, dur, a, b, o = {}]) => [t0, dur, Array.isArray(a) ? a : pose(a), Array.isArray(b) ? b : pose(b), o]);
      function camPose(t) {
        let cur = P0.slice();
        for (const [t0, dur, A, Bp, o] of S) {
          if (t < t0) {                                          // before this segment: rest on its start (+ anticipation)
            const dip = o.dip || 0, w = Math.min(0.12, t0), u = w > 0 ? cl((t - (t0 - w)) / w) : 0;   // never dips frame 0
            if (dip && u > 0) return [A[0], A[1], A[2] * Math.exp(-dip * Math.sin(Math.PI * u * 0.5))];
            return A.slice();
          }
          if (t >= t0 + dur) { cur = Bp.slice(); continue; }
          const u = cl((t - t0) / dur), px = e2(u), py = e3(u), bell = Math.sin(Math.PI * px);
          const dip = t0 > 0 ? o.dip || 0 : 0;
          const la = Math.log(A[2]) - dip * (1 - py), lb = Math.log(Bp[2]);
          return [A[0] + (Bp[0] - A[0]) * px, A[1] + (Bp[1] - A[1]) * py - (o.lift || 0) * bell,
            Math.exp(la + (lb - la) * py) * (1 - (o.zout || 0) * bell)];
        }
        return cur;
      }
      const apply = (t) => B.camSet(...camPose(t));
      apply(0);
      const clock = { t: 0 };
      tl.fromTo(clock, { t: 0 }, { t: B.D, duration: B.D, ease: "none", onUpdate: () => apply(Math.min(clock.t, LAST === undefined ? B.D : LAST)) }, 0);
      return camPose;
    }

    return {
      ch, labelEls, pose, travel, label, labelOut, accentTo, slateTo,
      heading: headingIn, headingOut, headEls: () => headBuild(),
      disc: (n) => ch.discs[idx(n)],
      glyph: (n) => ch.glyphs[idx(n)],
      pt: (n) => PTS[idx(n)].slice(),
      draw: (t0, o = {}) => V.chainDraw(ch, t0, { ...o, skip: (o.skip || []).concat(shown.map(idx)) }),
      camSet: (k) => B.camSet(...pose(k)),
    };
  };
})();
