/* stripe-youtube runtime — marker.js: the adnaan-reel v5 marker layer, frame size read from the runtime (1920x1080).
   Theme: --marker is the theme's marker colour (ink on light, white on dark); "accent" = the chapter hue.
   (Origin: adnaan-reel marker.js v5, reel-06 "the AI funnel".)
   The HAND-DRAWN layer on top of paper.js: a red felt-tip marker (plus black felt-tip and grey pencil) that annotates
   every scene. Strokes draw on stroke by stroke (dash offset, power2.out = a hand slowing into the end of a stroke),
   then BOIL — they swap between 3 seeded jittered variants every 4 frames, like hand-drawn animation, so a held drawing
   is never dead. Everything is seeded: deterministic and seek-safe (HyperFrames). Never edit per scene.

   Init (every starter already does this):
     const P = await Paper.init({ extraFonts: ['700 60px "Caveat"'] });
     const M = Marker.init(P);                 // full-frame <svg class="mk-layer"> inside #punch (moves with the camera)

   Colours: "marker" (accent, default), "ink" (black felt-tip), "pencil" (grey — fills only, never words), or any CSS colour.
   Coordinates are frame px (P.W x P.H, 1920x1080 here). Times are scene seconds. Contact frame ON the spoken word (start ~0.15 s early).

   M.circle(cx, cy, rx, ry, at, {color, width, dur, turns, tilt, seed})   loose loop, ends overshoot (1.1 turns)
   M.circleEl(el, at, {pad, ...}) / M.circleRect([x,y,w,h], at, …)        loop around an element / a rect
                                                                           (ONLY around isolated big words, numbers, objects —
                                                                            never across lines of text: use highlight)
   M.underline(x0, x1, y, at, {double}) / M.underlineEl(el, at, …)        wobbly underline (double = 2nd pass)
   M.arrow(x0, y0, x1, y1, at, {bend, head})                              curved arrow, head flicks on after the shaft
   M.line(points, at, {...})                                               any rough polyline [[x,y],…] — build doodles from it
   M.cross / M.check(cx, cy, size, at) / M.strikeEl(el, at)               ✗ ✓ and a scribbled strike-through
   M.hatch(poly, at, {color, spacing, angle, width, dur, opacity})        marker hatch fill clipped to a polygon
   M.highlight(cardEl, [x,y,w,h], at)                                      highlighter swipe BEHIND text inside a card (multiply)
                                                                           — how every real page/post phrase is emphasised
   M.note(text, x, y, at, {size, rot, color, cps, parent})                 Caveat handwriting written on left→right (≥ 60 px)
   M.tape(x, y, rot, at)                                                   masking tape pressed onto a card corner
   M.funnel({x, y, w, h, neck, tiers, split, spout, color})                a hand-drawn funnel → {tiers, draw(at), divider(i,at),
                                                                           fill(i,at)} — the pattern for any recurring diagram:
                                                                           fixed geometry + seeds in SHARED.md so every scene
                                                                           redraws the SAME drawing (see references/scenes.md §5)
   M.erase(shape, at, dur)                                                 fade a drawing out (exits faster than entrances)
   Each shape returns { g, paths, end } — tween g (an <g>) like any element; pass {parent} to ride a card's own svg.
   Sound: every audible stroke → a "scribble" beat in beats.json with its "dur" (scenes.py edl mixes the felt-tip kit).
*/
window.Marker = (() => {
  const NS = "http://www.w3.org/2000/svg";
  const COL = { marker: "var(--marker)", ink: "var(--marker-ink)", pencil: "var(--pencil)", accent: "var(--hue-solid)", callout: "var(--callout)", hl: "var(--hl)" };
  const BOIL = 4 / 30; // swap variant every 4 frames ("on fours")

  function rng(seed) {
    let s = (seed >>> 0) || 1;
    return () => { s ^= s << 13; s >>>= 0; s ^= s >> 17; s ^= s << 5; s >>>= 0; return (s % 100000) / 100000; };
  }
  // smooth path through points (Catmull-Rom → cubic Bézier)
  function smooth(pts) {
    if (pts.length < 2) return "";
    let d = `M ${pts[0][0].toFixed(1)} ${pts[0][1].toFixed(1)}`;
    for (let i = 0; i < pts.length - 1; i++) {
      const p0 = pts[i - 1] || pts[i], p1 = pts[i], p2 = pts[i + 1], p3 = pts[i + 2] || p2;
      const c1 = [p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6];
      const c2 = [p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6];
      d += ` C ${c1[0].toFixed(1)} ${c1[1].toFixed(1)}, ${c2[0].toFixed(1)} ${c2[1].toFixed(1)}, ${p2[0].toFixed(1)} ${p2[1].toFixed(1)}`;
    }
    return d;
  }
  // jitter a polyline: resample, push points perpendicular with low-frequency noise
  function roughPts(pts, amp, seed, step = 38) {
    const r = rng(seed);
    const out = [];
    for (let i = 0; i < pts.length - 1; i++) {
      const [x0, y0] = pts[i], [x1, y1] = pts[i + 1];
      const L = Math.hypot(x1 - x0, y1 - y0), n = Math.max(1, Math.round(L / step));
      const nx = -(y1 - y0) / (L || 1), ny = (x1 - x0) / (L || 1);
      for (let k = 0; k < n; k++) {
        const t = k / n, j = (r() - 0.5) * 2 * amp * (i === 0 && k === 0 ? 0.3 : 1);
        out.push([x0 + (x1 - x0) * t + nx * j, y0 + (y1 - y0) * t + ny * j]);
      }
    }
    const last = pts[pts.length - 1];
    out.push([last[0] + (r() - 0.5) * amp * 0.6, last[1] + (r() - 0.5) * amp * 0.6]);
    return out;
  }

  function init(P) {
    const { tl, D, F } = P;
    const W = P.W || 1920, H = P.H || 1080;
    const host = document.querySelector("#punch") || document.querySelector("#root");
    const layer = document.createElementNS(NS, "svg");
    layer.setAttribute("class", "mk-layer");
    layer.setAttribute("viewBox", `0 0 ${W} ${H}`);
    layer.setAttribute("width", W); layer.setAttribute("height", H);
    // felt-tip edge: a tiny static displacement so strokes aren't vector-perfect (fixed seed = deterministic)
    // v6.1: the filter region is the whole frame (+ margin) in user space. With the default objectBoundingBox units the
    // region hugged each stroke's GEOMETRY box (stroke width excluded), so a near-straight line's region was a few px
    // tall and the felt-tip texture sliced a 12 px stroke down to ~8 px (reel-07 agents switched texture off for them).
    layer.innerHTML = `<defs><filter id="mk-tex" filterUnits="userSpaceOnUse" x="-300" y="-300" width="${W + 600}" height="${H + 600}">
      <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="1" seed="7" result="n"/>
      <feDisplacementMap in="SourceGraphic" in2="n" scale="2.6" xChannelSelector="R" yChannelSelector="G"/></filter></defs>`;
    host.appendChild(layer);
    let seedCounter = 1;
    const root = document.querySelector("#root");

    function colorOf(c) { return COL[c] || c || COL.marker; }
    function rectOf(el) {
      const a = root.getBoundingClientRect(), b = el.getBoundingClientRect();
      const k = a.width / W || 1;
      return [(b.left - a.left) / k, (b.top - a.top) / k, b.width / k, b.height / k];
    }

    // core: build a <g> with one path per stroke; each stroke = 3 boil variants (d strings)
    function shape(strokes, at, { color, width = 10, dur = 0.34, gap = 2 * F, boil = true, opacity = 0.96, parent = layer, texture = true, until } = {}) {
      const g = document.createElementNS(NS, "g");
      if (texture && window.MK_TEX !== false) g.setAttribute("filter", "url(#mk-tex)");
      g.style.opacity = opacity;
      parent.appendChild(g);
      const paths = [];
      let t = at;
      const total = strokes.reduce((s, st) => s + (st.w || 1), 0);
      strokes.forEach((st) => {
        const p = document.createElementNS(NS, "path");
        p.setAttribute("d", st.v[0]);
        p.setAttribute("stroke", colorOf(st.color || color));
        p.setAttribute("stroke-width", st.width || width);
        // strokes are never filled — a path inside a card's own svg (M.highlight, {parent}) is outside svg.mk-layer's CSS
        // and would get the default black fill, which reads as a thin dark strike while the swipe draws (reel-07)
        p.setAttribute("fill", "none");
        g.appendChild(p);
        const len = p.getTotalLength() + 2;
        const d = st.dur || dur * ((st.w || 1) / total) * (strokes.length > 1 ? 1.15 : 1);
        p.style.strokeDasharray = `${len} ${len}`;
        if (at <= 0) p.style.strokeDashoffset = 0;
        else {
          tl.set(p, { opacity: 0, strokeDashoffset: len }, 0);
          tl.set(p, { opacity: 1 }, t);
          tl.to(p, { strokeDashoffset: 0, duration: d, ease: st.ease || "power2.out" }, t);
          tl.set(p, { strokeDasharray: "none" }, t + d + F);
        }
        // line boil: variants on fours after the stroke is down
        if (boil && st.v.length > 1) {
          const end = until ?? D;
          let k = 1;
          for (let bt = Math.max(at, 0) + d + 2 * F; bt < end; bt += BOIL, k++) tl.set(p, { attr: { d: st.v[k % st.v.length] } }, bt);
        }
        paths.push(p);
        t += d + gap;
      });
      return { g, paths, end: t };
    }
    const variants = (fn, seed) => [fn(seed), fn(seed + 101), fn(seed + 202)];

    // ---------------------------------------------------------------- primitives
    function line(points, at, o = {}) {
      const seed = o.seed ?? seedCounter++ * 977, amp = o.amp ?? 3.2;
      return shape([{ v: variants((s) => smooth(roughPts(points, amp, s)), seed) }], at, o);
    }
    function circle(cx, cy, rx, ry, at, o = {}) {
      const seed = o.seed ?? seedCounter++ * 977, turns = o.turns ?? 1.12, tilt = ((o.tilt ?? -4) * Math.PI) / 180;
      const start = o.start ?? -2.2; // begin top-left-ish, like a right-handed loop
      const mk = (s) => {
        const r = rng(s), pts = [], n = Math.max(18, Math.round((rx + ry) / 14));
        const wob = [r() * 6, r() * 6, r() * 6];
        for (let i = 0; i <= n * turns; i++) {
          const a = start + (i / n) * Math.PI * 2;
          const k = 1 + 0.035 * Math.sin(a * 2 + wob[0]) + 0.02 * Math.sin(a * 3 + wob[1]) + (i / n) * 0.06; // spirals out a bit
          const x = Math.cos(a) * rx * k, y = Math.sin(a) * ry * k;
          pts.push([cx + x * Math.cos(tilt) - y * Math.sin(tilt) + (r() - 0.5) * 2, cy + x * Math.sin(tilt) + y * Math.cos(tilt) + (r() - 0.5) * 2]);
        }
        return smooth(pts);
      };
      return shape([{ v: variants(mk, seed) }], at, { dur: 0.4, ...o });
    }
    function circleRect([x, y, w, h], at, o = {}) {
      const pad = o.pad ?? 18;
      return circle(x + w / 2, y + h / 2, w / 2 + pad + 6, h / 2 + pad, at, o);
    }
    function circleEl(el, at, o = {}) { return circleRect(rectOf(el), at, o); }
    function underline(x0, x1, y, at, o = {}) {
      const seed = o.seed ?? seedCounter++ * 977;
      const mk = (s) => { const r = rng(s); const L = x1 - x0; return smooth(roughPts([[x0, y + 3], [x0 + L * 0.5, y - 2 + r() * 4], [x1, y - 4]], 2.4, s, 60)); };
      const strokes = [{ v: variants(mk, seed) }];
      if (o.double) {
        const mk2 = (s) => { const L = x1 - x0; return smooth(roughPts([[x1 - L * 0.06, y + 10], [x0 + L * 0.5, y + 16], [x0 + L * 0.12, y + 12]], 2.4, s, 60)); };
        strokes.push({ v: variants(mk2, seed + 7), w: 0.8 });
      }
      return shape(strokes, at, { dur: 0.26, ...o });
    }
    function underlineEl(el, at, o = {}) {
      const [x, y, w, h] = rectOf(el);
      return underline(x + 6, x + w - 6, y + h * (o.k ?? 0.92), at, o);
    }
    function arrow(x0, y0, x1, y1, at, o = {}) {
      const seed = o.seed ?? seedCounter++ * 977, bend = o.bend ?? 0.25, head = o.head ?? 34;
      const mx = (x0 + x1) / 2, my = (y0 + y1) / 2, dx = x1 - x0, dy = y1 - y0;
      const c = [mx - dy * bend, my + dx * bend];
      const curve = [];
      for (let i = 0; i <= 12; i++) { const t = i / 12; curve.push([(1 - t) ** 2 * x0 + 2 * (1 - t) * t * c[0] + t * t * x1, (1 - t) ** 2 * y0 + 2 * (1 - t) * t * c[1] + t * t * y1]); }
      const tx = x1 - curve[10][0], ty = y1 - curve[10][1], tl0 = Math.hypot(tx, ty) || 1, ux = tx / tl0, uy = ty / tl0;
      const h1 = [x1 - ux * head + -uy * head * 0.62, y1 - uy * head + ux * head * 0.62];
      const h2 = [x1 - ux * head - -uy * head * 0.62, y1 - uy * head - ux * head * 0.62];
      return shape([
        { v: variants((s) => smooth(roughPts(curve, 2.2, s, 30)), seed), w: 1 },
        { v: variants((s) => smooth(roughPts([h1, [x1, y1], h2], 1.4, s, 80)), seed + 3), w: 0.35, dur: 0.12, ease: "power3.out" },
      ], at, { dur: 0.36, ...o });
    }
    function cross(cx, cy, size, at, o = {}) {
      const seed = o.seed ?? seedCounter++ * 977, s = size / 2;
      return shape([
        { v: variants((q) => smooth(roughPts([[cx - s, cy - s], [cx + s, cy + s * 1.05]], 3, q, 40)), seed) },
        { v: variants((q) => smooth(roughPts([[cx + s * 0.95, cy - s * 1.05], [cx - s * 1.05, cy + s]], 3, q, 40)), seed + 5) },
      ], at, { dur: 0.24, width: 12, ...o });
    }
    function check(cx, cy, size, at, o = {}) {
      const seed = o.seed ?? seedCounter++ * 977, s = size / 2;
      return shape([{ v: variants((q) => smooth(roughPts([[cx - s, cy], [cx - s * 0.25, cy + s * 0.7], [cx + s, cy - s * 0.9]], 2, q, 30)), seed) }], at, { dur: 0.22, width: 12, ...o });
    }
    function strikeEl(el, at, o = {}) {
      const [x, y, w, h] = rectOf(el), yy = y + h * 0.55;
      return line([[x - 8, yy + 6], [x + w * 0.5, yy - 4], [x + w + 8, yy + 2]], at, { width: 12, dur: 0.22, ...o });
    }
    function hatch(poly, at, o = {}) {
      const seed = o.seed ?? seedCounter++ * 977, spacing = o.spacing ?? 22, ang = ((o.angle ?? -32) * Math.PI) / 180;
      const id = "mkclip" + seed;
      const cp = document.createElementNS(NS, "clipPath");
      cp.setAttribute("id", id);
      const pg = document.createElementNS(NS, "polygon");
      pg.setAttribute("points", poly.map((p) => p.join(",")).join(" "));
      cp.appendChild(pg);
      layer.querySelector("defs").appendChild(cp);
      const g = document.createElementNS(NS, "g");
      g.setAttribute("clip-path", `url(#${id})`);
      (o.parent || layer).appendChild(g);
      const xs = poly.map((p) => p[0]), ys = poly.map((p) => p[1]);
      const minx = Math.min(...xs) - 40, maxx = Math.max(...xs) + 40, miny = Math.min(...ys) - 40, maxy = Math.max(...ys) + 40;
      const diag = Math.hypot(maxx - minx, maxy - miny), cx = (minx + maxx) / 2, cy = (miny + maxy) / 2;
      const n = Math.ceil(diag / spacing), strokes = [];
      const dx = Math.cos(ang), dy = Math.sin(ang), px = -dy, py = dx;
      const hr = rng(seed + 31);
      let off = -n / 2 * spacing;
      for (let i = 0; i <= n; i++) {
        off += spacing * (0.75 + hr() * 0.5);                       // uneven spacing, like a hand
        const wob = (hr() - 0.5) * 0.08, ddx = Math.cos(ang + wob), ddy = Math.sin(ang + wob);
        const bx = cx + px * off, by = cy + py * off;
        const a = [bx - ddx * diag / 2, by - ddy * diag / 2], b = [bx + ddx * diag / 2, by + ddy * diag / 2];
        const z = i % 2 ? [b, a] : [a, b]; // zig-zag like a real hand
        strokes.push({ v: variants((q) => smooth(roughPts(z, 2, q, 90)), seed + i * 13) });
      }
      const res = shape(strokes, at, { width: o.width ?? 13, dur: o.dur ?? 0.45, gap: 0, opacity: o.opacity ?? 0.85, color: o.color, parent: g, texture: true, boil: o.boil ?? false });
      return { ...res, g };
    }
    // highlighter swipe BEHIND text inside a card (multiply, so the words stay crisp and readable).
    // parent = the card element (rect in the card's own px), so it follows the card's rotation/moves exactly.
    function highlight(parent, [x, y, w, h], at, o = {}) {
      const seed = o.seed ?? seedCounter++ * 977;
      const svg = document.createElementNS(NS, "svg");
      svg.setAttribute("class", "mk-hl");
      Object.assign(svg.style, { position: "absolute", left: 0, top: 0, width: "100%", height: "100%", overflow: "visible", pointerEvents: "none", mixBlendMode: "multiply", zIndex: 2 });
      if (getComputedStyle(parent).position === "static") parent.style.position = "relative";
      parent.appendChild(svg);
      const yy = y + h * 0.56, pad = o.pad ?? 8;
      const mk = (s) => smooth(roughPts([[x - pad, yy + 3], [x + w * 0.5, yy - 2], [x + w + pad, yy + 1]], 2, s, 80));
      const res = shape([{ v: variants(mk, seed) }], at, { color: o.color || "var(--hl)", width: h * (o.k ?? 1.05), dur: o.dur ?? 0.3, opacity: o.opacity ?? (o.color ? 0.38 : 0.9), parent: svg, texture: false, boil: false });
      res.paths.forEach((p) => p.setAttribute("stroke-linecap", "butt"));
      return res;
    }
    function note(text, x, y, at, o = {}) {
      const el = document.createElement("div");
      el.className = "mk-note" + (o.color === "ink" ? " ink" : o.color === "pencil" ? " pencil" : "");
      if (o.color && !COL[o.color]) el.style.color = o.color;
      el.textContent = text;
      el.style.left = x + "px"; el.style.top = y + "px"; el.style.fontSize = (o.size ?? 64) + "px";
      el.style.transform = `rotate(${o.rot ?? -4}deg)`;
      (o.parent || host).appendChild(el);
      const cps = o.cps ?? 16, dur = Math.max(0.2, text.length / cps);
      if (at <= 0) return el;
      tl.set(el, { clipPath: "inset(-20% 100% -20% -2%)" }, 0);
      tl.to(el, { clipPath: "inset(-20% -4% -20% -2%)", duration: dur, ease: "none" }, at);
      // writing hand rhythm: tiny bob while writing
      tl.fromTo(el, { y: 2 }, { y: 0, duration: dur, ease: "sine.inOut" }, at);
      return el;
    }
    function tape(x, y, rot, at) {
      const el = document.createElement("div");
      el.className = "mk-tape";
      el.style.left = x + "px"; el.style.top = y + "px";
      host.appendChild(el);
      tl.fromTo(el, { opacity: 0, scale: 1.25, rotation: rot - 6 }, { opacity: 1, scale: 1, rotation: rot, duration: 0.18, ease: "back.out(2)" }, at);
      return el;
    }
    function erase(target, at, dur = 0.2) {
      const el = target.g || target;
      tl.to(el, { opacity: 0, duration: dur, ease: "power2.in" }, at);
    }

    // ---------------------------------------------------------------- the funnel
    // A hand-drawn kitchen funnel seen slightly from above: an elliptical rim, straight-ish tapering walls, a spout.
    // Tiers split the cone top→bottom. widths taper from w (rim) to w*neck (spout top).
    function funnel({ x = 140, y = 520, w = 800, h = 760, neck = 0.14, tiers = 4, split, color = "ink", width = 11, spout = 120 } = {}) {
      const cx = x + w / 2, rimRy = w * 0.085;
      const fr = split || Array.from({ length: tiers + 1 }, (_, i) => i / tiers);
      const halfAt = (f) => (w / 2) * (1 - f * (1 - neck));
      const yAt = (f) => y + f * h;
      const T = [];
      for (let i = 0; i < fr.length - 1; i++) {
        const f0 = fr[i], f1 = fr[i + 1], y0 = yAt(f0), y1 = yAt(f1), h0 = halfAt(f0), h1 = halfAt(f1);
        // front edge of each band is a shallow ellipse arc (perspective)
        const arc = (yy, hw, ry, steps = 10) => Array.from({ length: steps + 1 }, (_, k) => { const a = Math.PI - (k / steps) * Math.PI; return [cx + Math.cos(a) * hw, yy + Math.sin(a) * ry]; });
        const top = arc(y0, h0, i === 0 ? rimRy : rimRy * (h0 / (w / 2)));
        const bot = arc(y1, h1, rimRy * (h1 / (w / 2))).reverse();
        const poly = top.concat(bot);
        T.push({ poly, cx, cy: (y0 + y1) / 2 + rimRy * 0.5, yTop: y0, yBot: y1, xl: cx - h0, xr: cx + h0, wTop: h0 * 2, wBot: h1 * 2, rimRy: rimRy * (h0 / (w / 2)) });
      }
      const sx = halfAt(1), sy = yAt(1);
      const api = {
        tiers: T,
        spout: { x: cx, y: sy + spout },
        // draw the outline: rim ellipse, left wall, right wall, spout — 4 strokes like a hand would
        draw(at, o = {}) {
          const seed = o.seed ?? 4242;
          const rim = (s) => { const r = rng(s), pts = []; for (let i = 0; i <= 30; i++) { const a = -2.6 + (i / 28) * Math.PI * 2; pts.push([cx + Math.cos(a) * (w / 2) * (1 + (r() - 0.5) * 0.012), y + Math.sin(a) * rimRy + (r() - 0.5) * 2.5]); } return smooth(pts); };
          const wallL = (s) => smooth(roughPts([[cx - w / 2, y + 2], [cx - sx, sy], [cx - sx * 0.55, sy + spout]], 2.6, s, 70));
          const wallR = (s) => smooth(roughPts([[cx + w / 2, y + 2], [cx + sx, sy], [cx + sx * 0.55, sy + spout]], 2.6, s, 70));
          const lip = (s) => smooth(roughPts([[cx - sx * 0.55, sy + spout], [cx, sy + spout + 8], [cx + sx * 0.55, sy + spout]], 1.6, s, 30));
          return shape([
            { v: variants(rim, seed), w: 1.4 }, { v: variants(wallL, seed + 1), w: 1 }, { v: variants(wallR, seed + 2), w: 1 }, { v: variants(lip, seed + 3), w: 0.3 },
          ], at, { color, width, dur: o.dur ?? 1.0, ...o });
        },
        // tier divider i (between tier i and i+1): a front arc across the cone
        divider(i, at, o = {}) {
          const t = T[i], hw = t.wBot / 2, ry = rimRy * (hw / (w / 2));
          const pts = Array.from({ length: 11 }, (_, k) => { const a = Math.PI - (k / 10) * Math.PI; return [cx + Math.cos(a) * hw, t.yBot + Math.sin(a) * ry]; });
          return line(pts, at, { color, width: width * 0.8, dur: 0.24, amp: 1.6, ...o });
        },
        fill(i, at, o = {}) { return hatch(T[i].poly, at, { color: "marker", ...o }); },
      };
      return api;
    }

    return { layer, line, circle, circleRect, circleEl, underline, underlineEl, arrow, cross, check, strikeEl, hatch, highlight, note, tape, funnel, erase, rectOf, smooth, roughPts };
  }
  return { init };
})();
