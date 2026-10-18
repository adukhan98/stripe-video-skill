/* v7yt.js — the v7 "MINT" primitives (adnaan-reel house look) on the stripe-youtube board runtime (16:9). Default look.
   Load after board.js (do NOT load marker.js — this look has no hand-drawn layer). Styles: v7yt.css. Seek-safe: every move
   is a tween on B.tl, no randomness.

     const B = await Board.init();  const V = V7Y.init(B);  const { tl, D, F } = B;
     V.icon(name)                                   → '<i class="v7-gl" …>' (white Phosphor FILL glyph, hf/assets/icons/<name>.svg)
     V.disc(parent, {x, y, d = 150, icon, mint, cls, tag, id})  → disc element centred on (x, y) (charcoal | mint = current)
     V.discIn(el, t, {peak = 1.12})                 pop with anticipation + overshoot; the glyph lands 2 f later
     V.mintTo(el, t) / V.charcoalTo(el, t)          a disc becomes / stops being the current item (colour cross-fade + tiny punch)
     V.chain(parent, {points, icons, d, mint = [], tags, w = 1920, h = 1080})   → ch {wrap, link, len, cum, discs, glyphs, points}
     V.chainDraw(ch, t0, {gap = 0.12, first = 0.09, skip = []})  connector draws 1→N; each disc pops as the line reaches it
     V.chainEnd(ch)                                 fully drawn (open a scene on a previous scene's end state)
     V.line(parent, pts, t, {dur = .35, width = 6, color, curve = false, ease}) → path; a clean stroke draws itself on
     V.ringRect(parent, x, y, w, h, t, {r = 24, width = 6, color, dur = .35})   clean rounded-rect ring that draws on (the
                                                    v7 replacement for a marker loop; mint by default)
     V.ringCircle(parent, cx, cy, rad, t, {...})    the same as a circle
     V.bar(parent, x, y, w, t, {color, h = 12, dur = .28})       clean solid underline bar under a hero word (grows from the left)
     V.hl(parent, [x, y, w, h], t, {dur = .3})      mint highlighter behind a phrase on a real page (multiply, deep-mint edge)
     V.check(parent, cx, cy, t, {size = 64, disc = true})        clean check in a mint disc (cross: V.cross, charcoal disc)
     V.cam(t, cx, cy, s, {dur = .9})                camera on #cam looking at world point (cx, cy) at scale s — x and y on different
                                                    eases (an arc), never linear. B.camSet(cx, cy, s) for the frame-0 pose.
   V.init adds the mint ring around his card (opaque scenes) — keep the card zone x 1574–1886, y 614–1012 clear. */
window.V7Y = (() => {
  const NS = "http://www.w3.org/2000/svg";
  const $ = (s) => (typeof s === "string" ? document.querySelector(s) : s);

  function init(B) {
    const { tl, F, W, H } = B;
    const root = $("#root");
    if (document.body.dataset.bg !== "transparent" && !document.body.hasAttribute("data-nocard") && !$(".v7-cardring")) {
      const r = document.createElement("div"); r.className = "v7-cardring"; root.appendChild(r);
    }

    const icon = (name) => `<i class="v7-gl" style="--ic:url('assets/icons/${name}.svg')"></i>`;

    function disc(parent, { x, y, d = 150, icon: ic, mint = false, cls = "", tag, id } = {}) {
      const el = document.createElement("div");
      el.className = "v7-disc" + (mint ? " mint" : "") + (cls ? " " + cls : "");
      if (id) el.id = id;
      Object.assign(el.style, { left: x + "px", top: y + "px" });
      el.style.setProperty("--d", d + "px");
      el.innerHTML = (ic ? icon(ic) : "") + (tag !== undefined ? `<span class="v7-tag">${tag}</span>` : "");
      $(parent).appendChild(el);
      return el;
    }

    function discIn(el, t, { peak = 1.12 } = {}) {
      el = $(el);
      tl.fromTo(el, { scale: 0, opacity: 0 }, { scale: 0.92, opacity: 1, duration: 2 * F, ease: "power1.out" }, t - 2 * F);
      tl.to(el, { scale: peak, duration: 5 * F, ease: "power3.out" }, t);
      tl.to(el, { scale: 1, duration: 7 * F, ease: "power2.inOut" }, t + 5 * F);
      const g = el.querySelector(".v7-gl");
      if (g) {
        tl.fromTo(g, { scale: 0.3, opacity: 0 }, { scale: 1.15, opacity: 1, duration: 5 * F, ease: "power3.out" }, t + 2 * F);
        tl.to(g, { scale: 1, duration: 6 * F, ease: "power2.inOut" }, t + 7 * F);
      }
    }

    function mintTo(el, t) {
      el = $(el);
      tl.to(el, { backgroundColor: getComputedStyle(document.documentElement).getPropertyValue("--brand-primary").trim(), duration: 6 * F, ease: "power2.out" }, t);
      tl.to(el, { scale: 1.08, duration: 4 * F, ease: "power2.out" }, t);
      tl.to(el, { scale: 1, duration: 8 * F, ease: "power2.inOut" }, t + 4 * F);
    }
    function charcoalTo(el, t) { tl.to($(el), { backgroundColor: getComputedStyle(document.documentElement).getPropertyValue("--brand-deep").trim(), duration: 6 * F, ease: "power2.out" }, t); }

    function svgLayer(parent, cls, w = W, h = H) {
      const svg = document.createElementNS(NS, "svg");
      svg.setAttribute("class", cls); svg.setAttribute("width", w); svg.setAttribute("height", h);
      svg.setAttribute("viewBox", `0 0 ${w} ${h}`);
      $(parent).appendChild(svg);
      return svg;
    }

    function chain(parent, { points, icons = [], d = 150, mint = [], tags = [], w = W, h = H } = {}) {
      const wrap = document.createElement("div"); wrap.className = "v7-chain"; $(parent).appendChild(wrap);
      const svg = svgLayer(wrap, "v7-link", w, h);
      const link = document.createElementNS(NS, "path");
      link.setAttribute("d", "M " + points.map((p) => p.join(" ")).join(" L "));
      svg.appendChild(link);
      const cum = [0];
      for (let i = 1; i < points.length; i++) cum.push(cum[i - 1] + Math.hypot(points[i][0] - points[i - 1][0], points[i][1] - points[i - 1][1]));
      const len = cum[cum.length - 1];
      const discs = points.map(([x, y], i) => disc(wrap, { x, y, d, icon: icons[i], mint: mint.includes(i), tag: tags[i] }));
      const glyphs = discs.map((el) => el.querySelector(".v7-gl"));
      gsap.set(link, { strokeDasharray: `${len} ${3 * len}`, strokeDashoffset: len });
      return { wrap, svg, link, len, cum, discs, glyphs, points, d };
    }

    function chainDraw(ch, t0, { gap = 0.12, first = 0.09, skip = [] } = {}) {
      const arr = [t0];
      for (let k = 1; k < ch.points.length; k++) arr.push(t0 + first + (k - 1) * gap);
      for (let k = 1; k < ch.points.length; k++) {
        tl.fromTo(ch.link, { strokeDashoffset: ch.len - ch.cum[k - 1] }, { strokeDashoffset: ch.len - ch.cum[k],
          duration: Math.max(F, arr[k] - arr[k - 1]), ease: k === 1 ? "power2.in" : "none", immediateRender: false }, arr[k - 1]);
      }
      ch.discs.forEach((el, k) => { if (!skip.includes(k)) discIn(el, arr[k] + 2 * F); });
      return arr[arr.length - 1] + 0.3;
    }

    function chainEnd(ch) {
      gsap.set(ch.link, { strokeDashoffset: 0 });
      gsap.set(ch.discs, { scale: 1, opacity: 1 });
      gsap.set(ch.glyphs.filter(Boolean), { scale: 1, opacity: 1 });
    }

    function drawOn(path, t, dur, ease = "power2.inOut") {
      const len = path.getTotalLength();
      gsap.set(path, { strokeDasharray: `${len} ${len + 10}`, strokeDashoffset: len });
      tl.fromTo(path, { strokeDashoffset: len }, { strokeDashoffset: 0, duration: dur, ease, immediateRender: true }, t);
      return path;
    }

    function stroke(parent, tag, attrs, { width = 6, color = "var(--brand-primary)" } = {}) {
      const svg = svgLayer(parent, "v7-stroke");
      const p = document.createElementNS(NS, tag);
      for (const [k, v] of Object.entries(attrs)) p.setAttribute(k, v);
      p.style.stroke = color; p.style.strokeWidth = width;
      svg.appendChild(p);
      return p;
    }

    function line(parent, pts, t, { dur = 0.35, width = 6, color = "var(--brand-deep)", curve = false, ease } = {}) {
      let d = "M " + pts[0].join(" ");
      if (curve && pts.length === 3) d += ` Q ${pts[1].join(" ")} ${pts[2].join(" ")}`;
      else d += " L " + pts.slice(1).map((p) => p.join(" ")).join(" L ");
      return drawOn(stroke(parent, "path", { d }, { width, color }), t, dur, ease);
    }

    function ringRect(parent, x, y, w, h, t, { r = 24, width = 6, color = "var(--brand-primary)", dur = 0.35 } = {}) {
      const d = `M ${x + r} ${y} H ${x + w - r} A ${r} ${r} 0 0 1 ${x + w} ${y + r} V ${y + h - r} A ${r} ${r} 0 0 1 ${x + w - r} ${y + h}` +
        ` H ${x + r} A ${r} ${r} 0 0 1 ${x} ${y + h - r} V ${y + r} A ${r} ${r} 0 0 1 ${x + r} ${y} Z`;
      return drawOn(stroke(parent, "path", { d }, { width, color }), t, dur);
    }

    function ringCircle(parent, cx, cy, rad, t, { width = 6, color = "var(--brand-primary)", dur = 0.35 } = {}) {
      const d = `M ${cx} ${cy - rad} A ${rad} ${rad} 0 1 1 ${cx - 0.01} ${cy - rad} Z`;
      return drawOn(stroke(parent, "path", { d }, { width, color }), t, dur);
    }

    function bar(parent, x, y, w, t, { color = "var(--brand-primary)", h = 12, dur = 0.28 } = {}) {
      const el = document.createElement("div"); el.className = "v7-bar";
      Object.assign(el.style, { left: x + "px", top: y + "px", width: w + "px", height: h + "px", background: color });
      $(parent).appendChild(el);
      tl.fromTo(el, { scaleX: 0 }, { scaleX: 1, duration: dur, ease: "power3.out", immediateRender: true }, t);
      return el;
    }

    function hl(parent, [x, y, w, h], t, { dur = 0.3 } = {}) {
      const el = document.createElement("div"); el.className = "v7-hl";
      Object.assign(el.style, { left: x + "px", top: y + "px", width: w + "px", height: h + "px" });
      $(parent).appendChild(el);
      tl.fromTo(el, { scaleX: 0 }, { scaleX: 1, duration: dur, ease: "power2.out", immediateRender: true }, t);
      return el;
    }

    function mark(parent, cx, cy, t, { size = 64, disc: withDisc = true, kind = "check" } = {}) {
      const p = $(parent);
      let host = p, ox = cx - size / 2, oy = cy - size / 2;
      if (withDisc) {
        host = disc(p, { x: cx, y: cy, d: size, mint: kind === "check" });
        discIn(host, t);
        ox = 0; oy = 0;
      }
      const s = size, k = s / 64;
      const pts = kind === "check" ? [[ox + 18 * k, oy + 33 * k], [ox + 28 * k, oy + 43 * k], [ox + 46 * k, oy + 22 * k]]
        : [[ox + 21 * k, oy + 21 * k], [ox + 43 * k, oy + 43 * k]];
      const svgParent = withDisc ? host : p;
      const svg = svgLayer(svgParent, "v7-stroke", withDisc ? s : W, withDisc ? s : H);
      const mk = (pp) => {
        const path = document.createElementNS(NS, "path");
        path.setAttribute("d", "M " + pp.map((q) => q.join(" ")).join(" L "));
        path.style.stroke = withDisc ? "#fff" : "var(--brand-primary-dark)"; path.style.strokeWidth = Math.max(5, 7 * k);
        svg.appendChild(path);
        return path;
      };
      drawOn(mk(pts), t + 4 * F, 0.22, "power2.out");
      if (kind === "cross") drawOn(mk([[ox + 43 * k, oy + 21 * k], [ox + 21 * k, oy + 43 * k]]), t + 9 * F, 0.18, "power2.out");
      return host;
    }
    const check = (parent, cx, cy, t, o = {}) => mark(parent, cx, cy, t, { ...o, kind: "check" });
    const cross = (parent, cx, cy, t, o = {}) => mark(parent, cx, cy, t, { ...o, kind: "cross" });

    const camT = (cx, cy, s) => ({ x: W / 2 - cx * s, y: H / 2 - cy * s, scale: s });
    function cam(t, cx, cy, s, { dur = 0.9 } = {}) {
      const p = camT(cx, cy, s);
      tl.to("#cam", { x: p.x, duration: dur, ease: "power2.inOut" }, t);
      tl.to("#cam", { y: p.y, duration: dur, ease: "power3.inOut" }, t);
      tl.to("#cam", { scale: p.scale, duration: dur, ease: "power3.inOut" }, t);
    }

    return { icon, disc, discIn, mintTo, charcoalTo, chain, chainDraw, chainEnd, line, ringRect, ringCircle, bar, hl, check, cross, cam };
  }
  return { init };
})();
