/* chores.js — shared geometry of the chore pile (s04_chores + s05_chores2). Byte-identical in both hf/ folders.
   A bottom-anchored stack of white cards (slate icon disc + his word), world px. s05 opens on s04's exact end state. */
window.Chores = (() => {
  const CX = 560, CW = 620, Y0 = 900, OVER = 14;
  const CARDS = [
    { label: "pause", icon: "scissors", h: 116, rot: -1.6, dx: 0 },
    { label: "captions", icon: "closed-captioning", h: 116, rot: 1.8, dx: 14 },
    { label: "logo", icon: "image", h: 116, rot: -1.2, dx: -12 },
    { label: "screenshot", icon: "images", h: 116, rot: 2.0, dx: 10 },
    { label: "music", icon: "music-notes", h: 116, rot: -1.8, dx: -8 },
    { label: "drop it under my voice", icon: "waveform", h: 210, rot: 1.4, dx: 12, wave: true },
    { label: "export", icon: "export", h: 116, rot: -1.0, dx: -6 },
  ];
  CARDS.forEach((c, i) => { c.y = i === 0 ? Y0 : CARDS[i - 1].y - ((CARDS[i - 1].h + c.h) / 2 - OVER); });
  // camera at the end of s04 (looking at world cx, cy; scale s)
  const CAM_END4 = { cx: 900, cy: 534, s: 1 };

  const css = document.createElement("style");
  css.textContent = `
    .stack { position: absolute; left: 0; top: 0; width: 0; height: 0; }
    .tray { position: absolute; left: ${CX - 360}px; top: ${Y0 + 58}px; width: 720px; height: 24px; border-radius: 12px;
      background: color-mix(in srgb, var(--ink) 11%, transparent); }
    .chore { width: ${CW}px; }
    .chore .lbl { position: absolute; left: 132px; top: 50%; transform: translateY(-50%); font: 800 54px/1 "Inter Tight", sans-serif;
      letter-spacing: -.03em; color: var(--ink); white-space: nowrap; }
    .chore .v7-disc .ac { position: absolute; inset: 0; border-radius: 50%; background: var(--brand-primary); opacity: 0; }
    .chore .v7-disc .v7-gl { position: relative; }
    .chore.wave .lbl { left: 150px; top: 20px; transform: none; font-size: 44px; line-height: .98; }
    .chore .wv { position: absolute; left: 150px; top: 120px; }
    .chore .wv rect { fill: var(--brand-deep); }
    .chore .ub { position: absolute; left: 150px; top: 176px; width: 440px; height: 14px; border-radius: 7px; background: var(--brand-primary); transform-origin: 0 50%; }`;
  document.head.appendChild(css);

  function wave(card) {
    const NS = "http://www.w3.org/2000/svg";
    const svg = document.createElementNS(NS, "svg");
    svg.setAttribute("class", "wv"); svg.setAttribute("width", 440); svg.setAttribute("height", 44); svg.setAttribute("viewBox", "0 0 440 44");
    for (let k = 0; k < 26; k++) {
      const h = 8 + 34 * Math.abs(Math.sin(k * 0.62 + 0.4) * Math.cos(k * 0.23)) ;
      const r = document.createElementNS(NS, "rect");
      r.setAttribute("x", k * 17 + 1); r.setAttribute("width", 10); r.setAttribute("rx", 5);
      r.setAttribute("y", 22 - h / 2); r.setAttribute("height", h);
      svg.appendChild(r);
    }
    card.appendChild(svg);
    const ub = document.createElement("div"); ub.className = "ub"; card.appendChild(ub);
  }

  // one card in its FINAL resting state (hidden if opts.hidden); returns the element
  function card(V, stack, i, { cur = false, hidden = false } = {}) {
    const c = CARDS[i];
    const el = document.createElement("div");
    el.className = "v7-card chore" + (c.wave ? " wave" : ""); el.id = (stack.id || "st") + "_c" + i;
    Object.assign(el.style, { left: CX + c.dx - CW / 2 + "px", top: c.y - c.h / 2 + "px", height: c.h + "px", zIndex: i + 1 });
    const l = document.createElement("div"); l.className = "lbl"; l.innerHTML = c.label.replace("drop it ", "drop it<br>"); el.appendChild(l);
    if (c.wave) wave(el);
    stack.appendChild(el);
    const d = V.disc(el, { x: 76, y: c.h / 2, d: 84, icon: c.icon });
    const ac = document.createElement("i"); ac.className = "ac"; d.insertBefore(ac, d.firstChild);
    gsap.set(el, { rotation: c.rot, opacity: hidden ? 0 : 1, transformOrigin: "50% 100%" });
    gsap.set(ac, { opacity: cur ? 1 : 0 });
    return el;
  }
  function stack(V, parent, id, n, cur = n - 1) {
    const s = document.createElement("div"); s.className = "stack"; s.id = id;
    const t = document.createElement("div"); t.className = "tray"; s.appendChild(t);
    document.querySelector(parent).appendChild(s);
    gsap.set(s, { transformOrigin: CX + "px 560px" });
    for (let i = 0; i < n; i++) card(V, s, i, { cur: i === cur });
    return s;
  }
  // a card lands at time t (flight starts 7 f before): anticipation, overshoot, squash; its disc turns accent, the last one slate
  function land(B, V, s, i, t, { hard = false } = {}) {
    const { tl, F } = B;
    const el = card(V, s, i, { hidden: true });
    const c = CARDS[i], d = el.querySelector(".v7-disc"), ac = d.querySelector(".ac");
    const prev = s.querySelector("#" + s.id + "_c" + (i - 1) + " .ac");
    tl.fromTo(el, { y: -(hard ? 420 : 340), rotation: c.rot - 9, opacity: 0, scaleX: 1, scaleY: 1, transformOrigin: "50% 100%" },
      { y: 7, rotation: c.rot + 1.2, opacity: 1, duration: 7 * F, ease: "power3.in", immediateRender: true }, t - 7 * F);
    tl.to(el, { y: 0, rotation: c.rot, scaleX: hard ? 1.045 : 1.025, scaleY: hard ? 0.93 : 0.965, duration: 3 * F, ease: "power2.out" }, t);
    tl.to(el, { scaleX: 1, scaleY: 1, duration: 9 * F, ease: "back.out(2.4)" }, t + 3 * F);
    // the pile feels it: every card below dips a few px and settles
    s.querySelectorAll(".chore").forEach((o) => {
      if (o === el || +o.style.zIndex > i) return;
      tl.to(o, { y: hard ? 6 : 4, duration: 3 * F, ease: "power2.out" }, t);
      tl.to(o, { y: 0, duration: 9 * F, ease: "back.out(2)" }, t + 3 * F);
    });
    V.discIn(d, t + 4 * F);
    tl.to(ac, { opacity: 1, duration: 5 * F, ease: "power2.out" }, t + 2 * F);
    if (prev) tl.to(prev, { opacity: 0, duration: 6 * F, ease: "power2.out" }, t);
    return el;
  }
  // s05 opens with the paper grid exactly where s04 left it (grid drift in board.js is -64*(D/12) px over D)
  function gridContinue(B, prevD) {
    const a = -64 * (prevD / 12), b = -32 * (prevD / 12);
    B.tl.fromTo("#grid", { x: a, y: b }, { x: a - 64 * (B.D / 12), y: b - 32 * (B.D / 12), duration: B.D, ease: "none" }, 0);
  }
  return { CARDS, CX, CW, Y0, CAM_END4, stack, card, land, gridContinue };
})();
