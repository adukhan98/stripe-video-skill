/* adnaan-reel v7 "MINT" runtime — v7.js (loaded after paper.js; styles in v7.css)
   Built from the approved reel-08 style test (examples/reel-08-v7): his face full-screen in TALK beats, a grey board with a
   strong vignette and white-glyph icon discs in VISUAL beats, the camera travelling across a world bigger than the frame,
   and the SIGNATURE SHRINK (his full-screen footage shrinks into a disc or a small card on the board, and grows back).
   Everything is seek-safe: time-driven tweens on P.tl, no randomness.

   const P = await Paper.init(); const V = V7.init(P);
     V.board()                                   strong vignette over the paper (Visual beats)
     V.icon(name)                                → '<i class="v7-gl" …>' (white Phosphor glyph from hf/assets/<name>.svg)
     V.disc(parent, {x, y, d = 180, icon, mint = false, id})          → the disc element (charcoal, or mint = current item)
     V.discIn(el, t, {peak = 1.12})              pop with anticipation + overshoot; the glyph lands 2 f later
     V.chain(parent, {points, icons, d = 180, mint = []})             → ch {svg, link, len, cum, discs, glyphs}
     V.chainDraw(ch, t0, {gap = 2 * F, first = 0.09, skip = []})      connector draws 1→N, each disc pops as the line reaches it
     V.chainEnd(ch)                              the chain fully drawn (open a scene on a previous scene's end state)
     V.faceRect({cx, cy, R})                     his face region in SOURCE px (default from <body data-face>)
     V.shrink(spk, t0, {to, dur = 0.4, board = "#bg", ring = 8})      SIGNATURE: full-screen → target (see below); t0 = the dip
     V.grow(spk, t0, {from, dur = 0.45})         the reverse: target → full screen (payoff). Combine with V.placed (a scene
                                                 that opens shrunk) or with an earlier V.shrink in the same scene
     V.placed(spk, {to, ring = 8})               start a scene already shrunk (= a previous scene's end state)
         to = {x, y, d}                 a circle (a chain disc) centred at (x, y), diameter d
            | {x, y, w, h, r = 34}      the small card: top-left (x, y), size w×h (house: ~360×460, LEFT side only)
     V.cam(sel, t, {x, y, s, dur = 0.55, ease = "power3.inOut"})      move the camera (world layer) — x/y eased apart = an arc
     V.pose(wx, wy, s, sx = 540, sy = 900)        → {x, y, s}: the camera pose that puts world point (wx, wy) at screen (sx, sy)
     V.zoneMask(sel)                             feathered content-zone mask (minus the IG corner) on a travelling layer
*/
window.V7 = (() => {
  const NS = "http://www.w3.org/2000/svg";
  const W = 1080, H = 1920;
  const clamp = (v) => Math.max(0, Math.min(1, v));
  const num = (v, d) => (v === undefined || v === null || v === "" ? d : parseFloat(v));

  function init(P) {
    const { tl, F } = P;
    const $ = (s) => (typeof s === "string" ? document.querySelector(s) : s);
    const E = (n) => gsap.parseEase(n);
    const e2o = E("power2.out"), e3o = E("power3.out"), e2io = E("power2.inOut");

    function board() {
      const bg = $("#bg");
      if (bg && !bg.querySelector(".v7-vig")) {
        const v = document.createElement("div"); v.className = "v7-vig"; bg.appendChild(v);
      }
    }

    const icon = (name) => `<i class="v7-gl" style="--ic:url('assets/${name}.svg')"></i>`;

    function disc(parent, { x, y, d = 180, icon: ic, mint = false, id } = {}) {
      const el = document.createElement("div");
      el.className = "v7-disc" + (mint ? " mint" : "");
      if (id) el.id = id;
      Object.assign(el.style, { left: x + "px", top: y + "px", "--d": d + "px" });
      if (ic) el.innerHTML = icon(ic);
      $(parent).appendChild(el);
      return el;
    }

    function discIn(el, t, { peak = 1.12 } = {}) {
      P.pop(el, t, { peak, from: 0 });
      const g = el.querySelector(".v7-gl");
      if (g) P.pop(g, t + 2 * F, { peak: 1.15, from: 0.3 });
    }

    function chain(parent, { points, icons = [], d = 180, mint = [] } = {}) {
      const wrap = document.createElement("div"); wrap.className = "v7-chain"; $(parent).appendChild(wrap);
      const svg = document.createElementNS(NS, "svg");
      svg.setAttribute("class", "v7-link"); svg.setAttribute("width", W); svg.setAttribute("height", H);
      svg.setAttribute("viewBox", `0 0 ${W} ${H}`);
      const link = document.createElementNS(NS, "path");
      link.setAttribute("d", "M " + points.map((p) => p.join(" ")).join(" L "));
      svg.appendChild(link); wrap.appendChild(svg);
      const cum = [0];
      for (let i = 1; i < points.length; i++) cum.push(cum[i - 1] + Math.hypot(points[i][0] - points[i - 1][0], points[i][1] - points[i - 1][1]));
      const len = cum[cum.length - 1];
      const discs = points.map(([x, y], i) => disc(wrap, { x, y, d, icon: icons[i], mint: mint.includes(i) }));
      const glyphs = discs.map((el) => el.querySelector(".v7-gl"));
      gsap.set(link, { strokeDasharray: `${len} ${3 * len}`, strokeDashoffset: len });
      return { wrap, svg, link, len, cum, discs, glyphs, points, d };
    }

    // the connector leaves disc 1 at t0 (eases out of it), then runs at constant speed; each disc pops as the tip
    // reaches it (gap = time per segment), its glyph 2 f later. skip = disc indices that are already on screen.
    function chainDraw(ch, t0, { gap = 2 * F, first = 0.09, skip = [0] } = {}) {
      const arr = [t0];
      for (let k = 1; k < ch.points.length; k++) arr.push(t0 + first + (k - 1) * gap);
      for (let k = 1; k < ch.points.length; k++) {
        tl.fromTo(ch.link, { strokeDashoffset: ch.len - ch.cum[k - 1] }, { strokeDashoffset: ch.len - ch.cum[k],
          duration: Math.max(F, arr[k] - arr[k - 1]), ease: k === 1 ? "power2.in" : "none", immediateRender: false }, arr[k - 1]);
      }
      ch.discs.forEach((el, k) => {
        if (skip.includes(k)) return;
        gsap.set(el, { scale: 0 });
        discIn(el, arr[k] + 2 * F);
      });
      return arr[arr.length - 1] + 0.3;
    }

    function chainEnd(ch) {
      gsap.set(ch.link, { strokeDashoffset: 0 });
      gsap.set(ch.discs, { scale: 1, opacity: 1 });
      gsap.set(ch.glyphs.filter(Boolean), { scale: 1, opacity: 1 });
    }

    // his face region in the 1080x1920 source: centre a touch above data-face (eyes/nose), radius ~0.35 of the width
    function faceRect({ cx = 540, cy, R = 380 } = {}) {
      const face = num(document.body.dataset.face, 0.43);
      return { cx, cy: cy ?? Math.round((face - 0.017) * H), R };
    }

    // target geometry: what part of the source is shown (inset), at what scale, landing where
    function geometry(to, fr) {
      if (to.d) {                                       // circle on a chain disc
        const s = to.d / 2 / fr.R;
        return { s, x: to.x - fr.cx, y: to.y - fr.cy, ox: fr.cx, oy: fr.cy,
          inset: [fr.cy - fr.R, W - (fr.cx + fr.R), H - (fr.cy + fr.R), fr.cx - fr.R], round: fr.R, w: 2 * fr.R, h: 2 * fr.R };
      }
      // small card: show head + shoulders — source width sw (≈ 1.9 R), height from the card's aspect, face in the upper third
      const sw = Math.min(W, 1.9 * fr.R), s = to.w / sw, sh = to.h / s;
      const top = Math.max(0, Math.min(H - sh, fr.cy - 0.36 * sh)), left = Math.max(0, Math.min(W - sw, fr.cx - sw / 2));
      const ox = left + sw / 2, oy = top + sh / 2;
      return { s, x: to.x + to.w / 2 - ox, y: to.y + to.h / 2 - oy, ox, oy,
        inset: [top, W - (left + sw), H - (top + sh), left], round: (to.r ?? 34) / s, w: sw, h: sh };
    }

    function ringFor(spk, g, ringPx) {
      let svg = spk.querySelector(".v7-ring");
      if (!svg) {
        svg = document.createElementNS(NS, "svg");
        svg.setAttribute("class", "v7-ring"); svg.setAttribute("width", W); svg.setAttribute("height", H);
        svg.setAttribute("viewBox", `0 0 ${W} ${H}`);
        svg.appendChild(document.createElementNS(NS, "rect"));
        spk.appendChild(svg);
      }
      const r = svg.firstChild, w = ringPx / g.s, [it, , , il] = g.inset;
      const half = w / 2 - 1 / g.s;                     // outer edge 1 screen px beyond the clip: no footage fringe
      Object.entries({ x: il + half, y: it + half, width: g.w - 2 * half, height: g.h - 2 * half,
        rx: Math.max(0, g.round - half), "stroke-width": w + 1 / g.s, pathLength: 1 })
        .forEach(([k, v]) => r.setAttribute(k, v));
      gsap.set(r, { strokeDasharray: "1 2", strokeDashoffset: 1 });
      return r;
    }

    // one pure function of progress p (0 = full screen, 1 = at the target) drives the .spk.full element
    function applier(spk, g, boardEl) {
      const vig = boardEl ? boardEl.querySelector(".v7-vig") : null;
      return (p, pop = 1, dx = 0, dy = 0) => {
        const zoom = Math.exp(Math.log(1.0) + (Math.log(g.s) - Math.log(1.0)) * e2o(p));   // log-space: snap that decelerates
        const x = g.x * e3o(p) + dx, y = g.y * e2o(p) + dy;                               // x leads y → an arc
        const c = e3o(clamp(p * 1.1));                                                    // the clip leads the zoom
        const [it, ir, ib, il] = g.inset;
        spk.style.transformOrigin = `${g.ox}px ${g.oy}px`;
        spk.style.transform = `translate(${x}px, ${y}px) scale(${zoom * pop})`;
        spk.style.clipPath = c <= 0 ? "none" : `inset(${it * c}px ${ir * c}px ${ib * c}px ${il * c}px round ${g.round * c}px)`;
        if (vig) vig.style.opacity = c;
      };
    }

    function shrink(spk, t0, { to, dur = 0.4, board: b = "#bg", ring = 8, face } = {}) {
      spk = $(spk); board();
      const g = geometry(to, faceRect(face)), boardEl = $(b), apply = applier(spk, g, boardEl);
      const vig = boardEl && boardEl.querySelector(".v7-vig"); if (vig) vig.style.opacity = 0;
      const dip = t0, start = t0 + 3 * F, land = start + dur, peak = land + 0.07, settle = land + 0.22;
      const clock = { t: 0 };
      const at = (t) => {
        let p = 0, pop = 1, pre = 1;
        if (t >= dip && t < start) pre = 1 + 0.015 * e2o((t - dip) / (start - dip));        // anticipation: a 1.5 % push-in
        if (t >= start) p = clamp((t - start) / dur);
        if (t > land) pop = t < peak ? 1 + 0.06 * e2o((t - land) / (peak - land)) : 1 + 0.06 * (1 - e2io(clamp((t - peak) / (settle - peak))));
        apply(p, pop * (p === 0 ? pre : 1));
      };
      at(0);
      // the clock only runs in this move's window, so a later V.grow on the same .spk can take over
      tl.fromTo(clock, { t: 0 }, { t: settle, duration: settle, ease: "none", onUpdate: () => at(clock.t) }, 0);
      const r = ring ? ringFor(spk, g, ring) : null;
      if (r) tl.to(r, { strokeDashoffset: 0, duration: 0.24, ease: "power2.inOut" }, land - 0.16);
      return { g, land, ring: r };
    }

    function grow(spk, t0, { from, dur = 0.45, board: b = "#bg", ring = 8, face } = {}) {
      spk = $(spk); board();
      const g = geometry(from, faceRect(face)), apply = applier(spk, g, $(b));
      const r = ring ? ringFor(spk, g, ring) : null;
      if (r) gsap.set(r, { strokeDashoffset: 0 });
      const clock = { t: 0 }, start = t0 + 2 * F;
      const at = (t) => {
        const p = t < t0 ? 1 : t < start ? 1 : 1 - clamp((t - start) / dur);
        const pre = t >= t0 && t < start ? 0.94 + 0.06 * (1 - (t - t0) / (start - t0)) : 1;   // anticipation squeeze
        apply(p, pre);
        if (r) r.style.opacity = p > 0.2 ? 1 : p / 0.2;
      };
      tl.fromTo(clock, { t: t0 }, { t: start + dur, duration: start + dur - t0, ease: "none", immediateRender: false,
        onUpdate: () => at(clock.t) }, t0);
      return { g, full: start + dur };
    }

    function placed(spk, { to, ring = 8, board: b = "#bg", face } = {}) {
      spk = $(spk); board();
      const g = geometry(to, faceRect(face)), apply = applier(spk, g, $(b));
      apply(1);
      const r = ring ? ringFor(spk, g, ring) : null;
      if (r) gsap.set(r, { strokeDashoffset: 0 });
      return { g, ring: r };
    }

    function cam(sel, t, { x, y, s, dur = 0.55, ease = "power3.inOut" } = {}) {
      const els = typeof sel === "string" ? Array.from(document.querySelectorAll(sel)) : [].concat(sel);
      gsap.set(els, { transformOrigin: "0px 0px" });
      if (x !== undefined) tl.to(els, { x, duration: dur, ease: ease.replace("power3", "power2") }, t);
      if (y !== undefined) tl.to(els, { y, duration: dur, ease }, t);
      if (s !== undefined) tl.to(els, { scale: s, duration: dur, ease }, t);
    }

    const pose = (wx, wy, s, sx = 540, sy = 900) => ({ x: sx - s * wx, y: sy - s * wy, s });

    function zoneMask(sel) { document.querySelectorAll(typeof sel === "string" ? sel : "").forEach((e) => e.classList.add("v7-view", "v7-zone")); }

    return { board, icon, disc, discIn, chain, chainDraw, chainEnd, faceRect, shrink, grow, placed, cam, pose, zoneMask };
  }

  return { init };
})();
