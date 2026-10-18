/* stripe-youtube runtime — board.js
   One paused GSAP timeline, seek-safe and deterministic (HyperFrames). The 16:9 board world, kinetic words, the
   tactile primitives and the camera; the hand-drawn layer is marker.js (Marker.init(B)). Never edit per scene.

   Lasseter's principles are defaults, not options (adnaan-reel references/animation-principles.md):
     anticipation (2–3 f dip before a pop) · overshoot + settle (3-key) · exits ~40 % faster than entrances ·
     siblings stagger 2–4 f · arcs on coins · squash only on shapes, never type or logos · one focal point
     (B.recede objects, never words) · secondary action (grid drift, floats) so a hold is never dead.

   Usage (scene script):
     const B = await Board.init();                 // fonts asserted, words + data-in elements wired, grid drifts
     const M = Marker.init(B);                     // loops, underlines, arrows, highlighter, notes (marker.js header)
     const { tl, D, F } = B;                       // add the bespoke object on tl; Board registered tl already

   Auto-wired from markup:
     <span class="w" data-t="1.20" [data-hero] [data-out="4.0"]>word</span>   pops in ON its spoken word (start ~0.15 s early)
     <div data-in="pop|up|down|left|right|grow|fade" data-at="0.5" [data-out="5"] [data-dist="60"] [data-rot="-2"]>
   Primitives (all take scene seconds):
     B.in(el, at, {type, dist, dur, rot}) · B.out(el, at, {dur, to}) · B.coinIn(el, at) · B.pageIn(el, at, {rot})
     B.flow([tile, arrow, tile, …], at, {gap}) · B.countTo(el, at, from, to, dur, fmt) · B.punch(el, at)
     B.recede(el, at, {opacity, blur, scale}) · B.float(el, {amp, period}) · B.camSet(cx, cy, s) · B.camera(at, cx, cy, s, dur)
*/
window.Board = (() => {
  const FPS = 30, F = 1 / FPS, W = 1920, H = 1080;
  const $ = (s, r = document) => (typeof s === "string" ? r.querySelector(s) : s);
  const $$ = (s, r = document) => (typeof s === "string" ? Array.from(r.querySelectorAll(s)) : Array.isArray(s) ? s.flatMap((x) => (typeof x === "string" ? Array.from(r.querySelectorAll(x)) : [x])) : [s]);
  const num = (v, d) => (v === undefined || v === null || v === "" ? d : parseFloat(v));
  const FONTS = ['900 100px "Inter Tight"', '800 100px "Inter Tight"', '700 100px "Inter Tight"', '600 40px "Inter"', '500 40px "Geist Mono"'];
  let tl, D;

  async function fonts(extra = []) {
    const specs = FONTS.concat(extra);
    await Promise.all(specs.map((f) => document.fonts.load(f)));
    await document.fonts.ready;
    for (const f of specs) if (!document.fonts.check(f)) throw new Error("font missing: " + f);
  }

  // ---------------------------------------------------------------- entrances / exits
  const FROM = {
    up: (d) => ({ y: d }), down: (d) => ({ y: -d }), left: (d) => ({ x: -d }), right: (d) => ({ x: d }),
    pop: () => ({ scale: 0.86 }), grow: () => ({ scaleX: 0 }), fade: () => ({}),
  };
  // Every entrance is a fromTo whose FROM state renders immediately (immediateRender, as in adnaan-reel paper.js).
  // Hiding with zero-length steps at position 0 left the first frames empty when HyperFrames seeks.
  function inn(sel, at, { type = "up", dist = 60, dur = 16 * F, rot = 0, over = 1.04 } = {}) {
    for (const [i, el] of $$(sel).entries()) {
      const t = at + i * 3 * F;
      const from = { opacity: 0, rotation: rot ? rot * 2.2 : 0, ...(FROM[type] ? FROM[type](dist) : FROM.up(dist)) };
      if (type === "grow") el.style.transformOrigin = el.style.transformOrigin || "0 50%";
      if (type === "pop") {
        tl.fromTo(el, from, { opacity: 1, scale: over + 0.04, rotation: rot, duration: dur * 0.5, ease: "power3.out" }, t);
        tl.to(el, { scale: 1, duration: dur * 0.5, ease: "power2.inOut" }, t + dur * 0.5);
      } else if (type === "grow") {
        tl.fromTo(el, from, { opacity: 1, scaleX: 1, duration: dur, ease: "power3.out" }, t);
      } else if (type === "fade") {
        tl.fromTo(el, from, { opacity: 1, duration: dur * 0.6, ease: "power1.out" }, t);
      } else {   // up / down / left / right: travel with a small overshoot, then settle
        const o = { opacity: 1, x: 0, y: 0, rotation: rot, duration: dur * 0.72, ease: "power3.out" };
        if (from.y) o.y = -Math.sign(from.y) * Math.min(10, Math.abs(from.y) * 0.08);
        if (from.x) o.x = -Math.sign(from.x) * Math.min(10, Math.abs(from.x) * 0.08);
        tl.fromTo(el, from, o, t);
        tl.to(el, { x: 0, y: 0, duration: dur * 0.4, ease: "power2.inOut" }, t + dur * 0.72);
      }
    }
  }
  function out(sel, at, { dur = 7 * F, to = "up" } = {}) {
    const d = to === "up" ? { y: -24 } : to === "down" ? { y: 24 } : to === "left" ? { x: -40 } : to === "right" ? { x: 40 } : {};
    tl.to($$(sel), { opacity: 0, ...d, duration: dur, ease: "power2.in", stagger: F, immediateRender: false }, at);
  }

  // kinetic word: rise + pop to 1.03 (hero 1.08), settle — scale overshoots briefly, position never does
  function word(el, at, hero) {
    const peak = hero ? 1.08 : 1.03;
    tl.fromTo(el, { opacity: 0, y: 22, scale: 0.94 }, { opacity: 1, y: 0, scale: peak, duration: 5 * F, ease: "power3.out" }, at);
    tl.to(el, { scale: 1, duration: 6 * F, ease: "power2.inOut" }, at + 5 * F);
  }

  // ---------------------------------------------------------------- primitives
  function coinIn(sel, at) {
    const el = $(sel);
    tl.fromTo(el, { opacity: 0, x: -140 }, { opacity: 1, x: 0, duration: 14 * F, ease: "power2.out" }, at);   // arc: x and y eased differently
    tl.fromTo(el, { y: -60 }, { y: 0, duration: 14 * F, ease: "back.out(1.6)" }, at);
    tl.fromTo(el, { rotation: -200, scale: 0.8 }, { rotation: 0, scale: 1, duration: 14 * F, ease: "power3.out" }, at);
    tl.to(el, { scaleX: 1.12, scaleY: 0.88, duration: 3 * F, ease: "power1.out" }, at + 13 * F);   // squash on contact
    tl.to(el, { scaleX: 1, scaleY: 1, duration: 6 * F, ease: "power2.out" }, at + 16 * F);
  }
  function pageIn(sel, at, { rot = -1.5, dist = 140 } = {}) {
    const el = $(sel);
    tl.fromTo(el, { opacity: 0, y: dist, rotation: rot * 3 }, { opacity: 1, y: -8, rotation: rot * 0.6, duration: 14 * F, ease: "power3.out" }, at);
    tl.to(el, { y: 0, rotation: rot, duration: 8 * F, ease: "power2.inOut" }, at + 14 * F);
  }
  // a flow of tiles and arrowlines: tile pops, its arrow grows, the next tile pops as the arrow lands
  function flow(items, at, { gap = 0.35 } = {}) {
    let t = at;
    for (const el of (Array.isArray(items) ? items : [items]).flatMap((x) => $$(x))) {
      if (el.classList.contains("arrowline")) { inn(el, t - gap * 0.45, { type: "grow", dur: 9 * F }); continue; }
      inn(el, t, { type: "pop" });
      t += gap;
    }
  }
  function countTo(sel, at, from, to, dur = 0.8, fmt = (v) => Math.round(v).toLocaleString("en-US")) {
    const el = $(sel), o = { v: from };
    el.textContent = fmt(from);
    tl.to(o, { v: to, duration: dur, ease: "power2.out", onUpdate: () => (el.textContent = fmt(o.v)) }, at);
  }
  function punch(sel, at, peak = 1.06) {
    tl.to($(sel), { scale: peak, duration: 4 * F, ease: "power2.out" }, at);
    tl.to($(sel), { scale: 1, duration: 8 * F, ease: "power2.inOut" }, at + 4 * F);
  }
  function recede(sel, at, { opacity = 0.45, blur = 3, scale = 0.98 } = {}) {
    tl.to($$(sel), { opacity, scale, filter: `blur(${blur}px)`, duration: 10 * F, ease: "power2.out" }, at);
  }
  function float(sel, { amp = 4, period = 3.2, phase = 0 } = {}) {
    for (const [i, el] of $$(sel).entries()) {
      const n = Math.max(1, Math.floor(D / period));
      tl.to(el, { y: `+=${amp}`, duration: period / 2, ease: "sine.inOut", yoyo: true, repeat: n * 2 - 1 }, phase + i * 0.4);
    }
  }
  // camera over the whole board (#cam): look at (cx, cy) at scale s
  const camT = (cx, cy, s) => ({ x: W / 2 - cx * s, y: H / 2 - cy * s, scale: s });
  function camSet(cx, cy, s) { gsap.set("#cam", camT(cx, cy, s)); }   // immediate: the start of every later camera move
  function camera(at, cx, cy, s, dur = 0.9, ease = "power3.inOut") { tl.to("#cam", { ...camT(cx, cy, s), duration: dur, ease }, at); }

  // ---------------------------------------------------------------- init
  async function init({ extraFonts = [] } = {}) {
    await fonts(['700 60px "Caveat"', ...extraFonts]);
    const root = $("#root");
    D = parseFloat(root.dataset.duration);
    if (!document.body.dataset.theme) document.body.dataset.theme = "light";
    if (!$("#card-zone")) { const z = document.createElement("div"); z.id = "card-zone"; root.appendChild(z); }
    gsap.set("#cam", { transformOrigin: "0 0" });
    tl = gsap.timeline({ paused: true });
    window.__timelines = window.__timelines || {};
    window.__timelines.main = tl;
    // secondary action: the grid drifts the whole scene (linear = mechanical motion, allowed)
    if ($("#grid")) tl.fromTo("#grid", { x: 0, y: 0 }, { x: -64 * (D / 12), y: -32 * (D / 12), duration: D, ease: "none" }, 0);
    for (const el of $$(".w[data-t]")) {
      word(el, num(el.dataset.t, 0), el.hasAttribute("data-hero"));
      if (el.dataset.out) out(el, num(el.dataset.out));
    }
    for (const el of $$("[data-in]")) {
      inn(el, num(el.dataset.at, 0), { type: el.dataset.in, dist: num(el.dataset.dist, 60), rot: num(el.dataset.rot, 0) });
      if (el.dataset.out) out(el, num(el.dataset.out));
    }
    tl.set({}, {}, D);   // the timeline is exactly the scene length
    const B = { tl, D, F, FPS, W, H, $, $$, theme: document.body.dataset.theme,
      in: inn, out, word, coinIn, pageIn, flow, countTo, punch, recede, float, camSet, camera };
    return B;
  }
  return { init, F, FPS, W, H };
})();
