/* adnaan-reel shared runtime — paper.js (v3)
   One paused GSAP timeline, seek-safe and deterministic (HyperFrames). The world, speaker cards, kinetic
   words, exits, floats and the tactile primitives are driven from data attributes; the scene's bespoke
   hero object is added by the scene script on the returned timeline.

   Lasseter's principles are the defaults here, not options:
     timing          — weight-based durations (pop 5 f, small 10 f, card 16 f, exit 6–8 f, exits faster than entrances)
     slow in/out     — eased everything; linear only for continuous mechanical motion (grid drift, marching dots)
     anticipation    — hero/pop words and cards dip 2–3 f the other way before the main move
     follow-through  — overshoot then settle (3-key), parts lag the whole (card → sheen → words), siblings stagger 2–4 f
     arcs            — Paper.arc / cursorTo / coinIn bend the path by easing x and y differently
     squash/stretch  — Paper.squash on shapes only (coins, pills, pucks), never type or logos
     staging         — Paper.recede dims/blurs what is not the focal point; one focal point at a time
     secondary action— grid drift, camera push, floats, breathing glow: holds are never dead
     exaggeration    — Paper.punch / Paper.shake on the scene's one hero beat
     solid drawing   — one light direction (shadows down-right), contact shadows, shared perspective
     appeal          — the primitives are simple shapes with generous spacing; one accent

   Usage (scene script):
     const P = await Paper.init();            // fonts asserted, lines laid out, world + cards + words + exits wired
     const { tl, D, F, $, $$ } = P;           // add the bespoke hero object on tl, then nothing else — Paper registers tl
*/
window.Paper = (() => {
  const FPS = 30;
  const F = 1 / FPS;
  const $ = (s, r = document) => (typeof s === "string" ? r.querySelector(s) : s);
  const $$ = (s, r = document) => (typeof s === "string" ? Array.from(r.querySelectorAll(s)) : Array.isArray(s) ? s : [s]);
  const num = (v, d) => (v === undefined || v === null || v === "" ? d : parseFloat(v));
  const FONTS = ['900 100px "Inter Tight"', '800 100px "Inter Tight"', '700 100px "Inter Tight"', '500 40px "Inter"', '600 40px "Inter"'];

  // strength presets (references/animation-principles.md): subtle is the house default
  const STRENGTH = {
    subtle: { antic: 0.95, anticF: 3, over: 1.06, back: 1.6, settle: 0.3, rot: 1.5 },
    playful: { antic: 0.9, anticF: 4, over: 1.1, back: 2.2, settle: 0.4, rot: 3 },
  };
  let S = STRENGTH.subtle;
  let tl, D;

  // ------------------------------------------------------------------ fonts
  async function fonts(extra = []) {
    const specs = FONTS.concat(extra);
    await Promise.all(specs.map((f) => document.fonts.load(f)));
    await document.fonts.ready;
    for (const f of specs) if (!document.fonts.check(f)) throw new Error("brand font missing: " + f);
  }

  // ------------------------------------------------------------------ type layout
  // .line[data-x|data-right][data-base][data-size][data-fit]: placed by baseline, measured once (deterministic).
  function layoutLines(root = document) {
    // --type-scale (brand.css, default 1): a whole-reel nudge of kinetic type size without re-laying scenes
    const K = parseFloat(getComputedStyle(document.documentElement).getPropertyValue("--type-scale")) || 1;
    for (const line of $$(".line", root)) {
      if (line.dataset.size) line.style.fontSize = line.dataset.size * K + "px";
      else if (K !== 1 && !line.dataset.scaled) line.style.fontSize = parseFloat(getComputedStyle(line).fontSize) * K + "px";
      line.dataset.scaled = "1";
      if (!line.querySelector(".bl")) {
        const bl = document.createElement("span");
        bl.className = "bl";
        line.insertBefore(bl, line.firstChild);
      }
      line.style.top = "0px";
      line.style.left = "0px";
      const fit = num(line.dataset.fit, 0);
      if (fit) {
        // shrink until the line fits the width (incl. overshoot headroom) — hero floor 170 px
        let fs = parseFloat(getComputedStyle(line).fontSize);
        while (line.offsetWidth * S.over > fit && fs > 64) {
          fs -= 2;
          line.style.fontSize = fs + "px";
        }
      }
      const bl = line.querySelector(".bl");
      const base = num(line.dataset.base, 0);
      line.style.top = base - bl.offsetTop + "px";
      if (line.dataset.right !== undefined) line.style.left = num(line.dataset.right, 960) - line.offsetWidth + "px";
      else if (line.dataset.cx !== undefined) line.style.left = num(line.dataset.cx, 510) - line.offsetWidth / 2 + "px";
      else line.style.left = num(line.dataset.x, 76) + "px";
    }
  }

  // ------------------------------------------------------------------ world (secondary action, always on)
  function world() {
    if ($("#grid")) tl.fromTo("#grid", { x: 0, y: 0 }, { x: -20, y: -12, duration: D, ease: "none" }, 0);
    const cam = $("#cam");
    if (cam) {
      const push = num(cam.dataset.push, 1.006);
      tl.fromTo(cam, { scale: 1, transformOrigin: cam.dataset.origin || "510px 880px" }, { scale: push, duration: D, ease: "none" }, 0);
    }
  }

  // ------------------------------------------------------------------ speaker (v6: the three-mode system)
  // Mode A  <div class="spk split" [data-h="960"] [data-face-at="0.5"] [data-at="t"]>  HE edge to edge in the TOP part of the
  //         frame (no border, radius, shadow, tilt or float); the grid + kinetic words + doodles own the bottom part.
  // Mode B  no .spk at all — the doodles, kinetic type and cards own the whole canvas.
  // Mode C  <div class="spk full">  HE fills the frame (1–2 s emphasis), or
  //         <div class="spk cutout" [data-w="900"] [data-x] [data-drop="0"] [data-at]> + a transparent assets/speaker_cut.webm
  //         (hyperframes remove-background) anchored on the bottom edge in front of a big article/screenshot card.
  // Cards (legacy, use sparingly — 0–2 per reel when presence helps and the graphic needs most of the frame):
  // <div class="spk portrait|secondary|small" data-x data-y data-w data-h data-face="0.43" [data-at="t"] [data-ry="-5"] [data-rx="3"]>
  //   <div class="spk-card"><div class="spk-vid"><video class="clip" …></video></div><div class="spk-sheen"></div></div></div>
  const SPK = {
    full: { w: 1080, h: 1920, at: 0.43, ry: 0, rx: 0, radius: 0 },   // HE fills the frame (no card): hook, verdicts, CTA
    split: { w: 1080, h: 960, at: 0.5, ry: 0, rx: 0, radius: 0 },    // Mode A: top half, face centred in it
    cutout: { w: 900, h: 1600, at: 0, ry: 0, rx: 0, radius: 0 },     // Mode C cutout: bottom-anchored, no background
    portrait: { w: 740, h: 810, at: 0.4, ry: -5, rx: 3, radius: 34 },
    secondary: { w: 620, h: 432, at: 0.5, ry: -6, rx: 4, radius: 30 },
    small: { w: 440, h: 306, at: 0.5, ry: -7, rx: 4, radius: 30 },
  };
  function splitTop(h, faceAt, face) {      // video top so the face centre sits at faceAt of a 1080-wide band of height h
    return Math.min(0, Math.max(h - 1920, Math.round(faceAt * h - face * 1920)));
  }
  function speakerCards() {
    for (const spk of $$(".spk")) {
      const kind = ["full", "split", "cutout", "portrait", "secondary", "small"].find((k) => spk.classList.contains(k)) || "portrait";
      const p = SPK[kind];
      const w = num(spk.dataset.w, p.w), h = num(spk.dataset.h, p.h);
      const x = num(spk.dataset.x, kind === "full" ? 0 : (1080 - w) / 2), y = num(spk.dataset.y, kind === "full" ? 0 : 630);
      if (kind === "split") {
        // Mode A: edge to edge, flat — the top part of the frame IS the footage; slow push for life, no float
        const face = num(spk.dataset.face, num(document.body.dataset.face, 0.43));
        Object.assign(spk.style, { left: "0px", top: "0px", width: "1080px", height: h + "px" });
        const vid = $("video", spk);
        Object.assign(vid.style, { width: "1080px", height: "1920px", top: splitTop(h, num(spk.dataset.faceAt, p.at), face) + "px" });
        gsap.set(vid, { transformOrigin: "50% 30%" });
        const at = num(spk.dataset.at, 0);
        if (at > 0) splitIn(spk, at);
        tl.fromTo(vid, { scale: 1.0 }, { scale: num(spk.dataset.push, 1.02), duration: D, ease: "none" }, 0);
        continue;
      }
      if (kind === "cutout") {
        // Mode C cutout: transparent footage standing on the bottom edge (the frame edge hides the cut-off torso)
        const ch = Math.round((w * 1920) / 1080);
        const cx = num(spk.dataset.x, (1080 - w) / 2), cy = 1920 - ch + num(spk.dataset.drop, 0);
        Object.assign(spk.style, { left: cx + "px", top: cy + "px", width: w + "px", height: ch + "px" });
        const vid = $("video", spk);
        Object.assign(vid.style, { width: w + "px", height: ch + "px", top: "0px" });
        gsap.set(spk, { transformOrigin: "50% 100%" });
        const at = num(spk.dataset.at, 0);
        if (at > 0) {
          tl.set(spk, { opacity: 0, y: 160 }, 0);
          tl.to(spk, { opacity: 1, duration: 0.12, ease: "power1.out" }, at - 0.45);
          tl.to(spk, { y: -8, duration: 0.36, ease: "power3.out" }, at - 0.45);
          tl.to(spk, { y: 0, duration: 0.24, ease: "back.out(1.6)" }, at - 0.09);
        }
        tl.fromTo(vid, { scale: 1.0 }, { scale: 1.015, duration: D, ease: "none", transformOrigin: "50% 100%" }, 0);
        continue;
      }
      if (kind === "full") {
        // full-screen speaker: the source is already 1080x1920 — no crop, no tilt, no edge; only a slow push for life
        Object.assign(spk.style, { left: "0px", top: "0px", width: "1080px", height: "1920px" });
        const vid = $("video", spk);
        Object.assign(vid.style, { width: "1080px", height: "1920px", top: "0px" });
        gsap.set(vid, { transformOrigin: "50% 40%" });
        const at = num(spk.dataset.at, 0);
        if (at > 0) {
          tl.set(spk, { opacity: 0 }, 0);
          tl.fromTo(spk, { opacity: 0, scale: 1.06 }, { opacity: 1, scale: 1, duration: 0.4, ease: "power3.out" }, at - 0.3);
        }
        tl.fromTo(vid, { scale: 1.0 }, { scale: num(spk.dataset.push, 1.03), duration: D, ease: "none" }, 0);
        continue;
      }
      Object.assign(spk.style, { left: x + "px", top: y + "px", width: w + "px", height: h + "px" });
      const card = $(".spk-card", spk), vid = $("video", spk);
      const sheen = $(".spk-sheen", spk);
      // crop: source 1080x1920 scaled to the card width; the face centre (fraction of source height,
      // from SHARED.md project specifics) sits at `at` of the card height — whole head in, never cropped
      const vh = Math.round((w * 1920) / 1080);
      const face = num(spk.dataset.face, num(document.body.dataset.face, 0.43));
      const faceAt = num(spk.dataset.faceAt, p.at);
      let top = Math.round(faceAt * h - face * vh);
      top = Math.min(0, Math.max(h - vh, top));
      Object.assign(vid.style, { width: w + "px", height: vh + "px", top: top + "px" });
      const ry = num(spk.dataset.ry, p.ry), rx = num(spk.dataset.rx, p.rx);
      gsap.set(card, { transformPerspective: 1600, transformOrigin: "50% 50%" });
      const at = num(spk.dataset.at, 0);
      if (at <= 0) {
        // on screen from frame 0, ~90 % settled; finishes its 3D settle by 0.32 s (follow-through, parts lag)
        tl.fromTo(card, { y: -10, scale: 0.97, rotationX: rx + 5, rotationY: ry - 5 },
          { y: 0, scale: 1, rotationX: rx, rotationY: ry, duration: 0.32, ease: "back.out(1.6)", immediateRender: true }, 0);
        tl.to(card, { rotationY: ry + 1.5, rotationX: rx - 0.8, duration: D - 0.32, ease: "sine.inOut" }, 0.32);
        sheenSweep(sheen, 0.0);
      } else {
        // enters later: anticipation (the card is below, slightly behind), arc in, overshoot, settle; sheen lags 3 f
        const s = at - 0.42;
        tl.set(card, { opacity: 0, y: 140, x: 40, scale: 0.9, rotationY: ry - 14, rotationX: rx + 10 }, 0);
        tl.to(card, { opacity: 1, duration: 0.12, ease: "power1.out" }, s);
        tl.to(card, { x: 0, duration: 0.42, ease: "power3.out" }, s);
        tl.to(card, { y: -10, scale: 1.02, duration: 0.3, ease: "power3.out" }, s);
        tl.to(card, { y: 0, scale: 1, rotationY: ry, rotationX: rx, duration: 0.3, ease: "back.out(1.6)" }, s + 0.3);
        tl.to(card, { rotationY: ry + 1.5, rotationX: rx - 0.8, duration: Math.max(0.3, D - at - 0.2), ease: "sine.inOut" }, at + 0.2);
        sheenSweep(sheen, at - 0.1);
      }
      // video push (secondary action, origin at the eyes)
      gsap.set(vid, { transformOrigin: "50% 22%" });
      tl.fromTo(vid, { scale: 1.04 }, { scale: 1, duration: 0.4, ease: "power3.out" }, Math.max(0, at));
      tl.to(vid, { scale: 1.012, duration: Math.max(0.3, D - at - 0.4), ease: "none" }, Math.max(0, at) + 0.4);
      floatY(spk, num(spk.dataset.float, 4), 1.1);
    }
  }
  function sheenSweep(el, t) {
    if (!el) return;
    tl.fromTo(el, { opacity: 0 }, { opacity: 1, duration: 0.1, ease: "power1.out" }, Math.max(0, t));
    tl.fromTo(el, { backgroundPosition: "100% 0" }, { backgroundPosition: "0% 0", duration: 0.7, ease: "power2.inOut", immediateRender: false }, Math.max(0, t));
    tl.to(el, { opacity: 0, duration: 0.25, ease: "power1.in" }, Math.max(0, t) + 0.5);
  }
  function floatY(el, px, period = 1.1) {
    if (!px) return;
    const reps = Math.max(1, Math.floor(D / period));
    tl.fromTo(el, { y: 0 }, { y: -px, duration: period, ease: "sine.inOut", yoyo: true, repeat: reps }, 0);
  }

  // ------------------------------------------------------------------ kinetic words
  // .w[data-t] lands its CONTACT frame on the word time. Kinds: data-hero (overshoot + settle, with anticipation),
  // data-pop (quick pop), data-accent (soft back.out rise), default (rise + unblur). data-rise, data-peak, data-origin.
  function words() {
    for (const w of $$(".w[data-t]")) {
      const t = num(w.dataset.t, 0);
      const rise = num(w.dataset.rise, w.dataset.hero ? 100 : w.dataset.pop ? 84 : 56);
      if (w.dataset.hero !== undefined) {
        const peak = num(w.dataset.peak, S.over);
        const s = Math.max(0, t - 0.2);
        gsap.set(w, { transformOrigin: w.dataset.origin || "50% 80%" });
        // anticipation: the word is already faintly there and sinks 2 f before it rises (only when there is time)
        if (s >= S.anticF * F) {
          tl.fromTo(w, { opacity: 0, y: rise * 0.9, scale: 0.6, filter: "blur(10px)" },
            { opacity: 0.001, y: rise, scale: 0.55, duration: S.anticF * F, ease: "power2.in" }, s - S.anticF * F);
        }
        tl.fromTo(w, { opacity: 0, y: rise, scale: 0.55, rotation: -7, filter: "blur(10px)" },
          { opacity: 1, y: -8, scale: peak, rotation: S.rot, filter: "blur(0px)", duration: 0.2, ease: "power3.out", immediateRender: false }, s);
        tl.to(w, { y: 0, scale: 1, rotation: 0, duration: S.settle, ease: `back.out(${S.back})` }, s + 0.2);
      } else if (w.dataset.pop !== undefined) {
        const s = Math.max(0, t - 0.16);
        gsap.set(w, { transformOrigin: w.dataset.origin || "50% 85%" });
        tl.fromTo(w, { opacity: 0, y: rise, scale: 0.72, rotation: -5, filter: "blur(8px)" },
          { opacity: 1, y: -5, scale: 1.05, rotation: 1, filter: "blur(0px)", duration: 0.16, ease: "power3.out" }, s);
        tl.to(w, { y: 0, scale: 1, rotation: 0, duration: 0.28, ease: "back.out(1.5)" }, s + 0.16);
      } else if (w.dataset.accent !== undefined) {
        const s = Math.max(0, t - 0.16);
        gsap.set(w, { transformOrigin: "50% 85%" });
        // blur on its own non-overshooting ease: back.out would drive it negative (invalid CSS → stays blurred)
        tl.fromTo(w, { opacity: 0, y: rise, scale: 0.78, rotation: -1.5 },
          { opacity: 1, y: 0, scale: 1, rotation: 0, duration: 0.46, ease: "back.out(2.2)" }, s);
        tl.fromTo(w, { filter: "blur(8px)" }, { filter: "blur(0px)", duration: 0.3, ease: "power3.out", immediateRender: false }, s);
      } else {
        const s = Math.max(0, t - 0.13);
        tl.fromTo(w, { opacity: 0, y: rise, filter: "blur(6px)" },
          { opacity: 1, y: 0, filter: "blur(0px)", duration: 0.36, ease: "power3.out" }, s);
      }
      if (w.dataset.strike !== undefined) strike(w, num(w.dataset.strike, t + 0.3));
    }
    // ornaments: hand-drawn accent underline under [data-underline="t"] words
    for (const w of $$("[data-underline]")) underline(w, num(w.dataset.underline, num(w.dataset.t, 0) + 0.1));
  }

  // ------------------------------------------------------------------ exits, floats, punches, pulses (data-driven)
  function exits() {
    for (const el of $$("[data-exit]")) exitUp(el, num(el.dataset.exit, 0) + num(el.dataset.exitLag, 0) * F, num(el.dataset.exitDy, -60));
    for (const el of $$("[data-float]")) if (!el.classList.contains("spk")) floatY(el, num(el.dataset.float, 4), num(el.dataset.floatPeriod, 1.3));
    for (const el of $$("[data-punch]")) punch(num(el.dataset.punch, 0), { origin: el.dataset.origin });
    for (const el of $$("[data-pulse]")) pulse(el, num(el.dataset.pulse, 0));
    for (const el of $$("[data-breathe]")) breathe(el, num(el.dataset.breathe, 1.02));
  }
  // exits are faster than entrances (6 f) and blur up out of the way
  function exitUp(sel, t, dy = -60) {
    return tl.to(sel, { y: dy, opacity: 0, filter: "blur(8px)", duration: 6 * F, ease: "power2.in" }, t);
  }
  function exitDown(sel, t, dy = 40) {
    return tl.to(sel, { y: dy, opacity: 0, filter: "blur(6px)", duration: 6 * F, ease: "power2.in" }, t);
  }
  // exaggeration: a 0.4 % camera punch on the hero beat, or a 4 f shake on impact
  function punch(t, { scale = 1.004, origin = "510px 1000px", dur = 0.4 } = {}) {
    const el = $("#punch") || $("#cam");
    if (!el) return;
    tl.fromTo(el, { scale: 1, transformOrigin: origin }, { scale, duration: dur, ease: "power2.out", immediateRender: false }, t);
    tl.to(el, { scale: 1, duration: dur * 1.5, ease: "sine.inOut" }, t + dur);
  }
  function shake(t, px = 3) {
    const el = $("#punch") || $("#cam");
    if (!el) return;
    tl.to(el, { x: px, y: -px * 0.6, duration: F, ease: "none" }, t)
      .to(el, { x: -px * 0.8, y: px * 0.4, duration: F, ease: "none" }, t + F)
      .to(el, { x: px * 0.4, y: 0, duration: F, ease: "none" }, t + 2 * F)
      .to(el, { x: 0, y: 0, duration: F, ease: "none" }, t + 3 * F);
  }
  function pulse(el, t, amt = 1.04) {
    tl.to(el, { scale: amt, duration: 0.14, ease: "power2.out" }, t).to(el, { scale: 1, duration: 0.3, ease: "back.out(1.6)" }, t + 0.14);
  }
  function breathe(el, amt = 1.02, period = 1.6) {
    const reps = Math.max(1, Math.floor(D / period));
    tl.fromTo(el, { scale: 1 }, { scale: amt, duration: period, ease: "sine.inOut", yoyo: true, repeat: reps }, 0);
  }

  // ------------------------------------------------------------------ generic object moves (Lasseter recipes)
  // enter: anticipation dip → rise with overshoot → settle; children lag 2–4 f when `stagger` is set
  function enter(sel, t, { rise = 60, scaleFrom = 0.9, dur = 16 * F, stagger = 3 * F, rot = 0, antic = true } = {}) {
    const els = $$(sel);
    els.forEach((el, i) => {
      const s = t + i * stagger;
      gsap.set(el, { transformOrigin: el.dataset.origin || "50% 70%" });
      if (antic && s >= 3 * F) {
        tl.fromTo(el, { opacity: 0, y: rise * 0.85, scale: scaleFrom * 1.03 }, { opacity: 0.001, y: rise, scale: scaleFrom, duration: 3 * F, ease: "power2.in" }, s - 3 * F);
      }
      tl.fromTo(el, { opacity: 0, y: rise, scale: scaleFrom, rotation: -rot, filter: "blur(6px)" },
        { opacity: 1, y: -rise * 0.08, scale: 1 + (S.over - 1) * 0.6, rotation: rot * 0.3, filter: "blur(0px)", duration: dur * 0.6, ease: "power3.out", immediateRender: false }, s);
      tl.to(el, { y: 0, scale: 1, rotation: 0, duration: dur * 0.7, ease: `back.out(${S.back})` }, s + dur * 0.6);
    });
  }
  // pop: shapes/icons — 3-key anticipation → overshoot → settle (contact frame on t)
  function pop(sel, t, { peak = 1.08, from = 0.4 } = {}) {
    const el = $(sel);
    gsap.set(el, { transformOrigin: el.dataset.origin || "50% 60%" });
    tl.fromTo(el, { opacity: 0, scale: from, rotation: -8 }, { opacity: 1, scale: peak, rotation: 2, duration: 5 * F, ease: "power3.out" }, t - 5 * F);
    tl.to(el, { scale: 1, rotation: 0, duration: 8 * F, ease: "back.out(1.8)" }, t);
  }
  // arc: move from (fromX, fromY) to its resting place on a curve (x and y eased differently), tilting into travel
  function arc(sel, t, { fromX = 0, fromY = 300, dur = 16 * F, tilt = -6, ease = "power3.out" } = {}) {
    const el = $(sel);
    tl.fromTo(el, { x: fromX }, { x: 0, duration: dur, ease }, t);
    tl.fromTo(el, { y: fromY }, { y: 0, duration: dur, ease: "power1.out" }, t);
    tl.fromTo(el, { rotation: tilt }, { rotation: 0, duration: dur * 1.15, ease: "back.out(1.4)" }, t);
  }
  // squash & stretch on contact (shapes only — never type or logos); volume-preserving
  function squash(sel, t, amt = 0.1) {
    const el = $(sel);
    gsap.set(el, { transformOrigin: el.dataset.origin || "50% 100%" });
    tl.to(el, { scaleX: 1 - amt * 0.6, scaleY: 1 + amt * 0.6, duration: 3 * F, ease: "power2.in" }, t - 4 * F)
      .to(el, { scaleX: 1 + amt, scaleY: 1 - amt, duration: 2 * F, ease: "power2.out" }, t)
      .to(el, { scaleX: 1, scaleY: 1, duration: 8 * F, ease: "back.out(2)" }, t + 2 * F);
  }
  // staging: what is not the focal point recedes (dim + blur + 97 %); restore brings it back
  function recede(sel, t, { opacity = 0.5, blur = 5, scale = 0.97, dur = 0.3 } = {}) {
    return tl.to(sel, { opacity, filter: `blur(${blur}px)`, scale, duration: dur, ease: "power2.inOut" }, t);
  }
  function restore(sel, t, dur = 0.3) {
    return tl.to(sel, { opacity: 1, filter: "blur(0px)", scale: 1, duration: dur, ease: "power2.out" }, t);
  }
  // growFull: a speaker card grows into the full frame on a word (anticipation dip, then the frame fills; radius,
  // tilt and accent edge dissolve). Use on a verdict / hero line; the words that follow sit at the bottom with .kin.
  function growFull(sel, t, { dur = 0.6 } = {}) {
    const spk = $(sel), card = $(".spk-card", spk), vid = $("video", spk);
    const w0 = parseFloat(spk.style.width), h0 = parseFloat(spk.style.height);
    tl.to(card, { scale: 0.985, duration: 3 * F, ease: "power2.in" }, t - 3 * F);
    tl.to(card, { scale: 1, rotationX: 0, rotationY: 0, borderRadius: 0, boxShadow: "0 0 0 0 rgba(0,0,0,0)", duration: dur, ease: "power3.inOut" }, t);
    tl.to(spk, { left: 0, top: 0, width: 1080, height: 1920, duration: dur, ease: "power3.inOut" }, t);
    tl.to(vid, { width: 1080, height: 1920, top: 0, duration: dur, ease: "power3.inOut" }, t);
    tl.to(spk, { y: 0, duration: 0.01 }, t);        // cancel the float so the frame sits flush
    return t + dur;
  }
  // ---- Mode switches (v6). The footage band slides like a shutter: anticipation, then a fast eased move; exits
  // faster than entrances. Use them to change mode INSIDE a scene (A ↔ B, C → A) on a sentence boundary.
  // splitIn: Mode B → A — the top band drops in from above the frame.
  function splitIn(sel, t, { dur = 0.42 } = {}) {
    const spk = $(sel), h = parseFloat(spk.style.height) || 960;
    tl.set(spk, { y: -h - 20 }, 0);
    tl.to(spk, { y: 12, duration: dur * 0.75, ease: "power3.out" }, t - dur);
    tl.to(spk, { y: 0, duration: dur * 0.25, ease: "power2.out" }, t - dur * 0.25);
    return t;
  }
  // splitOut: Mode A → B — a 3-frame dip down, then the band shoots up out of the frame.
  function splitOut(sel, t, { dur = 0.3 } = {}) {
    const spk = $(sel), h = parseFloat(spk.style.height) || 960;
    tl.to(spk, { y: 10, duration: 3 * F, ease: "power2.out" }, t - 3 * F);
    tl.to(spk, { y: -h - 30, duration: dur, ease: "power3.in" }, t);
    return t + dur;
  }
  // fullToSplit: Mode C → A — the full-screen footage shrinks to the top band (face slides to the band centre).
  function fullToSplit(sel, t, { h = 960, faceAt = 0.5, dur = 0.5 } = {}) {
    const spk = $(sel), vid = $("video", spk);
    const face = num(spk.dataset.face, num(document.body.dataset.face, 0.43));
    tl.to(spk, { height: h, duration: dur, ease: "power3.inOut" }, t);
    tl.to(vid, { top: splitTop(h, faceAt, face), duration: dur, ease: "power3.inOut" }, t);
    return t + dur;
  }
  // splitToFull: Mode A → C — the band grows to the whole frame on a hero line.
  function splitToFull(sel, t, { dur = 0.5 } = {}) {
    const spk = $(sel), vid = $("video", spk);
    tl.to(spk, { height: 1920, duration: dur, ease: "power3.inOut" }, t);
    tl.to(vid, { top: 0, duration: dur, ease: "power3.inOut" }, t);
    return t + dur;
  }
  // hold-and-move: a settled element glides to a new spot (used when the header compacts to make room)
  function moveTo(sel, t, { x = 0, y = 0, scale = 1, dur = 0.5 } = {}) {
    tl.to(sel, { x, duration: dur, ease: "power2.inOut" }, t);
    tl.to(sel, { y, duration: dur, ease: "power3.inOut" }, t);
    if (scale !== 1) tl.to(sel, { scale, duration: dur, ease: "power2.inOut" }, t);
  }

  // ------------------------------------------------------------------ ornaments
  // strike-through drawn left→right on t (the ::after bar scales with --sx)
  function strike(w, t) {
    w.classList.add("strike");
    w.style.setProperty("--sx", 0);
    if (!document.getElementById("strike-style")) {
      const st = document.createElement("style");
      st.id = "strike-style";
      st.textContent = ".strike::after{transform:scaleX(var(--sx,0))}";
      document.head.appendChild(st);
    }
    const proxy = { v: 0 };
    tl.to(proxy, { v: 1, duration: 0.22, ease: "power2.inOut", onUpdate: () => w.style.setProperty("--sx", proxy.v) }, t);
  }
  // hand-drawn accent underline under a word: an svg path drawn on 0.26 s before/after the word lands
  function underline(w, t, { width = 12, dur = 0.26 } = {}) {
    const line = w.closest(".line");
    const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    svg.setAttribute("class", "ul");
    svg.setAttribute("width", "1080"); svg.setAttribute("height", "1920"); svg.setAttribute("viewBox", "0 0 1080 1920");
    const ux0 = line.offsetLeft + w.offsetLeft + 10, ux1 = line.offsetLeft + w.offsetLeft + w.offsetWidth - 14;
    const uy = num(line.dataset.base, 0) + Math.round(parseFloat(getComputedStyle(line).fontSize) * 0.1);
    const L = ux1 - ux0;
    const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
    path.setAttribute("d", `M ${ux0} ${uy + 4} C ${ux0 + L * 0.22} ${uy - 3}, ${ux0 + L * 0.45} ${uy + 6}, ${ux0 + L * 0.66} ${uy + 1} S ${ux1 - 30} ${uy - 6}, ${ux1} ${uy - 2}`);
    path.setAttribute("fill", "none"); path.setAttribute("stroke", "var(--brand-primary)");
    path.setAttribute("stroke-width", width); path.setAttribute("stroke-linecap", "round");
    svg.appendChild(path);
    (line.parentElement).appendChild(svg);
    const len = path.getTotalLength();
    path.style.strokeDasharray = `${len} ${len}`;
    if (t <= 0) { path.style.strokeDashoffset = 0; return; }
    tl.set(path, { opacity: 0 }, 0);               // a round cap at offset=len would show as a dot before t
    tl.set(path, { opacity: 1 }, t);
    tl.fromTo(path, { strokeDashoffset: len }, { strokeDashoffset: 0, duration: dur, ease: "power2.out" }, t);
  }

  // ------------------------------------------------------------------ primitives
  // coins: <div class="coin" data-n="03" data-x data-y> → body + 4 ticks + accent face + contact shadow
  function buildCoins() {
    for (const c of $$(".coin")) {
      if (c.dataset.built) continue;
      c.dataset.built = "1";
      c.style.left = num(c.dataset.x, 0) + "px"; c.style.top = num(c.dataset.y, 0) + "px";
      const n = c.dataset.n || "01";
      c.innerHTML = `<div class="coin-shadow"></div><div class="coin-body">${n}
        <i class="tick" style="left:44px;top:6px;width:4px;height:8px"></i><i class="tick" style="left:44px;bottom:6px;width:4px;height:8px"></i>
        <i class="tick" style="top:44px;left:6px;width:8px;height:4px"></i><i class="tick" style="top:44px;right:6px;width:8px;height:4px"></i></div>
        <div class="coin-active">${n}</div>`;
    }
  }
  // coin rolls in on an arc, squashes on contact, settles
  function coinIn(sel, t, { fromX = -240, fromY = -120, dur = 0.5 } = {}) {
    const c = $(sel);
    tl.set(c, { opacity: 1 }, Math.max(0, t - dur));
    const body = $(".coin-body", c), sh = $(".coin-shadow", c);
    tl.fromTo(c, { x: fromX }, { x: 0, duration: dur, ease: "power2.out" }, t - dur);
    tl.fromTo(c, { y: fromY }, { y: 0, duration: dur, ease: "power1.in" }, t - dur);
    tl.fromTo(body, { rotation: -200 }, { rotation: 0, duration: dur * 1.1, ease: "power3.out" }, t - dur);
    tl.fromTo(sh, { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: dur, ease: "power2.out" }, t - dur);
    squash(body, t, 0.12);
  }
  // active coin: flips grey → accent on its word with a ring flash (exaggeration on the hero beat)
  function coinActive(sel, t) {
    const c = $(sel), a = $(".coin-active", c);
    gsap.set(a, { transformOrigin: "50% 50%" });
    tl.fromTo(a, { opacity: 0, scale: 0.6, rotation: -30 }, { opacity: 1, scale: 1.08, rotation: 0, duration: 5 * F, ease: "power3.out" }, t - 2 * F);
    tl.to(a, { scale: 1, duration: 8 * F, ease: "back.out(2)" }, t + 3 * F);
    tl.fromTo(a, { boxShadow: "0 18px 30px rgba(60,50,40,.22), 0 0 0 0 rgba(46,156,203,.6)" },
      { boxShadow: "0 18px 30px rgba(60,50,40,.22), 0 0 0 22px rgba(46,156,203,0)", duration: 0.5, ease: "power2.out" }, t);
  }
  // pills drop in from above like notifications: anticipation lift, overshoot, squash on landing, 3 f stagger
  function pillIn(sel, t, { stagger = 3 * F, fromY = -70 } = {}) {
    $$(sel).forEach((el, i) => {
      const s = t + i * stagger;
      gsap.set(el, { transformOrigin: "50% 100%" });
      tl.fromTo(el, { opacity: 0, y: fromY, scale: 0.92, filter: "blur(6px)" },
        { opacity: 1, y: 6, scale: 1.02, filter: "blur(0px)", duration: 8 * F, ease: "power3.out" }, s);
      tl.to(el, { y: 0, scale: 1, duration: 9 * F, ease: "back.out(1.8)" }, s + 8 * F);
      squash(el, s + 8 * F, 0.05);
    });
  }
  // browser / ui / terminal cards: heavy things — 16 f, small tilt into travel, sheen lags 3 f
  function cardIn(sel, t, { fromY = 90, rot = -3, dur = 16 * F, ry = 0 } = {}) {
    const el = $(sel);
    gsap.set(el, { transformPerspective: 1400, transformOrigin: "50% 60%" });
    tl.fromTo(el, { opacity: 0, y: fromY, scale: 0.94, rotation: rot, rotationY: ry - 8 },
      { opacity: 1, y: -6, scale: 1.01, rotation: rot * 0.2, rotationY: ry, duration: dur * 0.6, ease: "power3.out" }, t);
    tl.to(el, { y: 0, scale: 1, rotation: 0, duration: dur * 0.7, ease: `back.out(${S.back})` }, t + dur * 0.6);
    const sheen = $(".sheen", el);
    if (sheen) sheenSweep(sheen, t + 3 * F);
  }
  // slow internal scroll of a captured page (continuous mechanical motion → linear is right)
  function scrollPage(sel, t, dur, px) {
    return tl.fromTo(sel, { y: 0 }, { y: -px, duration: dur, ease: "none" }, t);
  }
  // puck: <div class="puck" data-x data-y [data-scale]> built here; feed() = glow + bob on receiving something
  function buildPucks() {
    for (const p of $$(".puck")) {
      if (p.dataset.built) continue;
      p.dataset.built = "1";
      p.style.left = num(p.dataset.x, 0) + "px"; p.style.top = num(p.dataset.y, 0) + "px";
      p.innerHTML = `<div class="puck-shadow"></div><div class="puck-glow"></div><div class="puck-ring"></div>
        <div class="puck-disc"><div class="puck-visor"><div class="eye l"></div><div class="eye r"></div></div></div>`;
      if (p.dataset.scale) gsap.set(p, { scale: num(p.dataset.scale, 1), transformOrigin: "50% 50%" });
    }
  }
  function puckFeed(sel, t) {
    const p = $(sel), g = $(".puck-glow", p), r = $(".puck-ring", p), d = $(".puck-disc", p);
    tl.fromTo(g, { opacity: 0, scale: 0.7 }, { opacity: 1, scale: 1, duration: 0.2, ease: "power2.out" }, t);
    tl.to(g, { opacity: 0, duration: 0.6, ease: "power2.in" }, t + 0.3);
    tl.fromTo(r, { opacity: 0, scale: 0.9 }, { opacity: 1, scale: 1, duration: 4 * F, ease: "power2.out" }, t);
    tl.to(r, { opacity: 0, scale: 1.12, duration: 0.4, ease: "power2.out" }, t + 4 * F);
    squash(d, t, 0.08);
    for (const e of $$(".eye", p)) tl.fromTo(e, { scaleY: 1 }, { scaleY: 0.15, duration: 2 * F, yoyo: true, repeat: 1, ease: "power1.inOut" }, t + 0.25);
  }
  // dotted path: draw on with a mask (the dots themselves cannot dash-offset), then march continuously
  function drawPath(sel, t, dur = 0.5) {
    const path = $(sel), svg = path.ownerSVGElement;
    const ns = "http://www.w3.org/2000/svg";
    let defs = svg.querySelector("defs") || svg.insertBefore(document.createElementNS(ns, "defs"), svg.firstChild);
    const id = "m" + Math.abs(hash(path.getAttribute("d") || "")) + "_" + $$("mask", defs).length;
    const mask = document.createElementNS(ns, "mask");
    mask.setAttribute("id", id); mask.setAttribute("maskUnits", "userSpaceOnUse");
    mask.setAttribute("x", "0"); mask.setAttribute("y", "0"); mask.setAttribute("width", "1080"); mask.setAttribute("height", "1920");
    const m = document.createElementNS(ns, "path");
    m.setAttribute("d", path.getAttribute("d")); m.setAttribute("fill", "none"); m.setAttribute("stroke", "#fff");
    m.setAttribute("stroke-width", "24"); m.setAttribute("stroke-linecap", "round");
    mask.appendChild(m); defs.appendChild(mask);
    path.setAttribute("mask", `url(#${id})`);
    const L = m.getTotalLength();
    m.style.strokeDasharray = `${L} ${L}`;
    tl.set(path, { opacity: 0 }, 0);               // hidden until it starts drawing (no stray cap dot)
    tl.set(path, { opacity: 1 }, t);
    tl.fromTo(m, { strokeDashoffset: L }, { strokeDashoffset: 0, duration: dur, ease: "power1.inOut" }, t);
    return L;
  }
  function marchPath(sel, t, dur, speed = 140) {
    return tl.fromTo(sel, { strokeDashoffset: 0 }, { strokeDashoffset: -speed * (dur / 1), duration: dur, ease: "none" }, t);
  }
  // ride: an element travels along a path (needs MotionPathPlugin — the starter loads it)
  function ride(sel, pathSel, t, dur, { align = true, start = 0, end = 1 } = {}) {
    if (!window.MotionPathPlugin) throw new Error("ride() needs MotionPathPlugin (see the starter's <script> tags)");
    gsap.registerPlugin(MotionPathPlugin);
    return tl.to(sel, { motionPath: { path: pathSel, align: align ? pathSel : false, alignOrigin: [0.5, 0.5], autoRotate: false, start, end },
      duration: dur, ease: "power2.inOut" }, t);
  }
  // cursor: built once; moves on arcs; clicks with a scale dip (anticipation) and a back.out release
  function buildCursor() {
    for (const c of $$(".cursor")) {
      if (c.dataset.built) continue;
      c.dataset.built = "1";
      c.innerHTML = `<svg viewBox="-4 -4 60 84"><path d="M2,2 L2,62 L16.5,48.5 L27,72 L38.5,67 L28,44 L48,44 Z" fill="#FBFAF8" stroke="#141414" stroke-width="3.5" stroke-linejoin="round"/></svg>`;
      gsap.set($("svg", c), { transformOrigin: "8px 8px" });
    }
  }
  function cursorTo(sel, t, x, y, { dur = 0.34, show = true } = {}) {
    const c = $(sel);
    if (show) tl.to(c, { opacity: 1, duration: 0.12, ease: "power1.out" }, t);
    tl.to(c, { x, duration: dur, ease: "power2.inOut" }, t);
    tl.to(c, { y, duration: dur, ease: "power3.out" }, t);
  }
  function cursorClick(sel, t) {
    const s = $("svg", $(sel));
    tl.to(s, { scale: 0.8, duration: 3 * F, ease: "power2.in" }, t - 3 * F);
    tl.to(s, { scale: 1, duration: 0.18, ease: "back.out(2.5)" }, t);
  }
  function cursorOut(sel, t) {
    tl.to(sel, { opacity: 0, x: "+=120", y: "+=140", duration: 0.24, ease: "power2.in" }, t);
  }
  // typing into a terminal: <span class="cmd"><span class="pr">$ </span><span class="ch">n</span>…</span>
  function typeIn(sel, t, cps = 28) {
    const chars = $$(".ch", $(sel));
    chars.forEach((ch, i) => tl.set(ch, { opacity: 1 }, t + i / cps));
    return t + chars.length / cps;
  }
  function hash(s) { let h = 0; for (let i = 0; i < s.length; i++) h = (h * 31 + s.charCodeAt(i)) | 0; return h; }

  // ------------------------------------------------------------------ init
  async function init({ strength, extraFonts = [] } = {}) {
    const root = $("#root");
    D = parseFloat(root.dataset.duration);
    S = STRENGTH[strength || root.dataset.strength || "subtle"] || STRENGTH.subtle;
    await fonts(extraFonts);
    // every timed video must be exactly the scene length (the renderer rounds data-duration up)
    for (const v of $$("video.clip")) if (!v.dataset.duration) v.dataset.duration = root.dataset.duration;
    layoutLines();
    buildCoins(); buildPucks(); buildCursor();
    tl = gsap.timeline({ paused: true });
    world();
    speakerCards();
    words();
    exits();
    window.__timelines = window.__timelines || {};
    window.__timelines.main = tl;
    return {
      tl, D, F, $, $$, S,
      enter, pop, arc, squash, recede, restore, moveTo, growFull, splitIn, splitOut, fullToSplit, splitToFull, exitUp, exitDown, punch, shake, pulse, breathe, floatY,
      coinIn, coinActive, pillIn, cardIn, scrollPage, puckFeed, drawPath, marchPath, ride,
      cursorTo, cursorClick, cursorOut, typeIn, sheenSweep, underline, layoutLines,
    };
  }
  return { init, F, FPS };
})();
