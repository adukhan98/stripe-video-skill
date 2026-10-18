/* brandcard.js — THE BRAND FILE CARD, one shared object for s17_brandfile, s34_onefile, s35_mine, s36_swap (byte-identical
   copies; edit in s17_brandfile/hf and copy). A flat white file card: header (slate file disc + 'brand.json' + optional
   official logo chip as an <img>), then the REAL json typeset VERBATIM in Geist Mono — the raw file text, line for line,
   never re-serialised (long lines are cropped by the card window and fade out on the right; nothing is invented).
   Beside every hex VALUE a small swatch square is drawn in that file's own hex (the file's data). Colours otherwise come
   from tokens only (brand.css). Seek-safe: every move is a tween on the caller's timeline.

     const txt = await BrandCard.load("assets/brand_stripe.json");          // BEFORE Board.init (raw text)
     const B = await Board.init(); const V = V7Y.init(B);
     const bc = BrandCard.make("#punch", txt, {id, x, y, w, rows = 19, font = 28, title = "brand.json", logo, top = 0});
       bc.el (card) · bc.code (scrolling code block, put V.hl here) · bc.lh (line height) · bc.lines[] · bc.sw[] (swatches)
     BrandCard.box(bc, key, n = 0)      → [x, y, w, h] of the n-th "key" (in bc.code coords) for V.hl(bc.code, box, t)
     BrandCard.lineOf(bc, key, n = 0)   → 0-based line index of that key
     BrandCard.scroll(tl, bc, t, line, {dur = .4})   the window scrolls so `line` (0-based) is the top row
     BrandCard.swatchesIn(tl, bc, t, {gap = 2/30})    the visible swatches pop in, top → bottom
     BrandCard.hexOf(txt, path)          → a value from the parsed file, e.g. hexOf(txt, "colors.primary.hex")       */
window.BrandCard = (() => {
  const F = 1 / 30;
  const esc = (s) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  const HEX = /^"#[0-9A-Fa-f]{6}"$/;

  if (!document.getElementById("bc-style")) {
    const st = document.createElement("style"); st.id = "bc-style";
    st.textContent = `
      .bc { position: absolute; overflow: hidden; border-radius: 28px; background: var(--brand-card); box-shadow: var(--shadow); }
      .bc-head { position: absolute; left: 0; top: 0; right: 0; height: 96px; display: flex; align-items: center; gap: 20px;
        padding: 0 28px; border-bottom: 2px solid color-mix(in srgb, var(--ink) 8%, transparent); }
      .bc-fd { position: relative; width: 60px; height: 60px; margin: 0; flex: none; }
      .bc-title { font: 800 44px/1 "Inter Tight", sans-serif; letter-spacing: -.03em; color: var(--ink); white-space: nowrap; }
      .bc-logo { margin-left: auto; height: 60px; padding: 0 22px; border-radius: 30px; display: flex; align-items: center;
        background: var(--brand-card); box-shadow: inset 0 0 0 2px color-mix(in srgb, var(--ink) 10%, transparent); }
      .bc-logo img { height: 34px; display: block; }
      .bc-win { position: absolute; left: 0; right: 0; overflow: hidden; background: var(--brand-card);
        -webkit-mask-image: linear-gradient(to right, black 84%, transparent 99%), linear-gradient(to bottom, black 90%, transparent 100%);
        -webkit-mask-composite: source-in; mask-image: linear-gradient(to right, black 84%, transparent 99%), linear-gradient(to bottom, black 90%, transparent 100%);
        mask-composite: intersect; }
      .bc-code { position: absolute; left: 0; top: 0; padding-left: 34px; font-family: "Geist Mono", ui-monospace, monospace;
        font-weight: 500; color: var(--ink); white-space: pre; }
      .bc-ln { position: relative; display: block; white-space: pre; }
      .bc-k { color: var(--ink); }
      .bc-s { color: color-mix(in srgb, var(--ink) 58%, var(--brand-card)); }
      .bc-hx { color: var(--ink); }
      .bc-p { color: var(--muted); }
      .bc-sw { display: inline-block; width: .82em; height: .82em; margin: 0 .2em 0 .3em; vertical-align: -.08em; border-radius: 6px;
        box-shadow: inset 0 0 0 2px color-mix(in srgb, var(--ink) 14%, transparent); }`;
    document.head.appendChild(st);
  }

  async function load(url) {
    const r = await fetch(url, { cache: "no-store" });
    if (!r.ok) throw new Error("brandcard: cannot load " + url);
    return await r.text();
  }

  function hexOf(txt, path) { return path.split(".").reduce((o, k) => o[k], JSON.parse(txt)); }

  // tokenise ONE raw line; the concatenated token text is exactly the raw line (verbatim)
  function lineHTML(raw) {
    const re = /("(?:[^"\\]|\\.)*")(\s*:)?|([{}\[\],:])|(\s+)|([^"{}\[\],:\s]+)/g;
    let m, out = "", lastKey = null;
    while ((m = re.exec(raw))) {
      if (m[1] !== undefined && m[2] !== undefined) {          // a key
        lastKey = JSON.parse(m[1]);
        out += `<span class="bc-k" data-key="${esc(lastKey)}">${esc(m[1])}</span><span class="bc-p">${esc(m[2])}</span>`;
      } else if (m[1] !== undefined) {                          // a string value
        if (HEX.test(m[1]) && lastKey !== "name") {
          out += `<span class="bc-hx">${esc(m[1])}</span><span class="bc-sw" style="background:${m[1].slice(1, -1)}"></span>`;
        } else out += `<span class="bc-s">${esc(m[1])}</span>`;
      } else if (m[3] !== undefined) out += `<span class="bc-p">${esc(m[3])}</span>`;
      else if (m[4] !== undefined) out += m[4];
      else out += `<span class="bc-s">${esc(m[5])}</span>`;   // numbers / literals
    }
    return out || " ";
  }

  function make(parent, txt, { id, x = 0, y = 0, w = 1000, rows = 19, font = 28, title = "brand.json", logo, top = 0 } = {}) {
    const lh = Math.round(font * 1.42);
    const winTop = 96 + 18, winH = rows * lh;
    const el = document.createElement("div");
    el.className = "bc"; if (id) el.id = id;
    Object.assign(el.style, { left: x + "px", top: y + "px", width: w + "px", height: winTop + winH + 22 + "px" });
    el.innerHTML =
      `<div class="bc-head"><div class="v7-disc bc-fd" style="--d:60px"><i class="v7-gl" style="--ic:url('assets/icons/file-code.svg')"></i></div>` +
      `<div class="bc-title">${esc(title)}</div>${logo ? `<div class="bc-logo"><img src="${logo}" alt="" /></div>` : ""}</div>` +
      `<div class="bc-win" style="top:${winTop}px;height:${winH}px"><div class="bc-code" style="font-size:${font}px;line-height:${lh}px"></div></div>`;
    const code = el.querySelector(".bc-code");
    const raw = txt.replace(/\r/g, "").replace(/\n$/, "").split("\n");
    code.innerHTML = raw.map((l) => `<div class="bc-ln" style="height:${lh}px">${lineHTML(l)}</div>`).join("");
    (typeof parent === "string" ? document.querySelector(parent) : parent).appendChild(el);
    gsap.set(code, { y: -top * lh });
    return { el, code, lh, rows, lines: Array.from(code.children), sw: Array.from(code.querySelectorAll(".bc-sw")), top, w };
  }

  function keyEl(bc, key, n = 0) {
    const all = Array.from(bc.code.querySelectorAll(".bc-k")).filter((s) => s.dataset.key === key);
    if (!all[n]) throw new Error("brandcard: no key " + key);
    return all[n];
  }
  function lineOf(bc, key, n = 0) { return bc.lines.indexOf(keyEl(bc, key, n).parentNode); }
  function box(bc, key, n = 0) {
    const s = keyEl(bc, key, n), ln = s.parentNode;
    return [s.offsetLeft + 34 - 8, ln.offsetTop + 3, s.offsetWidth + 16, bc.lh - 6];
  }
  function scroll(tl, bc, t, line, { dur = 0.4 } = {}) {
    tl.to(bc.code, { y: -line * bc.lh, duration: dur, ease: "power3.inOut" }, t);
  }
  function swatchesIn(tl, bc, t, { gap = 2 * F, first = 0, last = bc.rows } = {}) {
    let i = 0;
    for (const s of bc.sw) {
      const li = bc.lines.indexOf(s.parentNode) - bc.top;
      if (li < first || li >= last) continue;
      tl.fromTo(s, { scale: 0, opacity: 0 }, { scale: 1.3, opacity: 1, duration: 4 * F, ease: "power3.out" }, t + i * gap);
      tl.to(s, { scale: 1, duration: 6 * F, ease: "power2.inOut" }, t + i * gap + 4 * F);
      i++;
    }
  }
  return { load, make, box, lineOf, scroll, swatchesIn, hexOf };
})();
