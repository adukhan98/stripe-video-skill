/* tablecard.js — THE BEAT TABLE CARD, shared by s19_table (proof), s20_approve (board) and s38_reveal (overlay).
   Owned by s19_table; copied byte-identical into the other two scenes' hf/. The rows are the REAL chapter-3 rows of
   assets/beat_table.md (columns # · Out · He says · Layout · What happens · SFX; "Real assets" is not shown), typeset
   verbatim; a cell longer than two lines is trimmed with an ellipsis (CSS line clamp), nothing is invented.
   Colours are tokens only (brand.css re-points them to Stripe).

     const tc = TableCard.build(parent, { x, y, id });   // after Board.init (fonts are loaded) — tc.el is a .page card
     tc.W, tc.H                                          // natural size (1760 × 1022), card-local px
     tc.head(name) → [x, y, w, h]                        // header cell rect, card-local   (name: num out says layout what sfx)
     tc.colCenter(name) → x                              // card-local x of a column centre
     tc.rows → [row elements]  tc.headRow  tc.file (the file disc in the title bar)
     TableCard.rowsIn(B, tc, t0, { gap })                // rows drop in one by one (seek-safe fromTo)
     TableCard.hlNow(tc, name)                           // a static accent highlighter on a header (an end state carried over)
*/
window.TableCard = (() => {
  const ROWS = [
    ["13", "107.03–115.07", "\"here's a breakdown… nine stages. Each one is a small tool… writes the file the next one reads.\"", "MAP", "the 9-disc chain draws itself (Transcribe · Cut · Brand · Assets · Plan · Build · Sound · Assemble · Check), a file chip passes disc to disc", "whoosh (chapter)"],
    ["14", "115.07–127.63", "\"First, transcribe. Whisper… every word with a start and end time… the backbone\"", "MAP → BOARD", "push to disc 1, then words on a time ruler, each with a start/end bracket; \"backbone\" = the ruler thickens under everything", "—"],
    ["15", "127.63–141.70", "\"Then the cut… word boundaries… whisper ends words a little early… re-transcribes every join\"", "MAP → PROOF", "push to disc 2; a word strip with a scissors on a boundary; then the real verify_cuts output card, one line ticks OK", "—"],
    ["16", "141.70–150.87", "\"Next, the brand. One JSON file… Nothing is hard coded.\"", "MAP → PROOF", "push to disc 3; the real brand.json card, keys light up as named (colors, fonts, captions, logo)", "—"],
    ["17", "150.87–161.00", "\"the assets… official logo fetched, not redrawn… a real, readable strip\"", "MAP → BOARD", "push to disc 4; logos from this video fall into a tray; a page slides in as a tall strip with a blurple highlighter", "—"],
    ["18", "161.00–175.10", "\"the plan and storyboard… beat table… I approve it or change it… nothing renders before I say yes\"", "MAP → PROOF", "push to disc 5; THIS beat table as a page card, rows scroll, a big approve check lands on \"yes\"", "—"],
    ["19", "175.10–193.77", "\"the build… HyperFrames… HTML, CSS, and GSAP… done by code… one agent per scene, in parallel… one runtime\"", "MAP → CANVAS", "push to disc 6; a scene's real index.html card; then a row of agent discs building scene tiles in parallel, all linked to one runtime disc", "—"],
    ["20", "193.77–205.80", "\"the sound. A music bed… ElevenLabs Music… ducked under my voice… kit… structural beats\"", "MAP → BOARD", "push to disc 7; a voice waveform with the bed ducking beneath; 3 small SFX markers only on the structural ticks", "—"],
    ["21", "205.80–219.43", "\"assemble and then check. Lip sync… Instagram corner… every logo official… every caption readable… then render\"", "MAP → BOARD", "push to discs 8–9; a checklist ticks line by line; \"render\" = the chain completes, all nine discs blurple", "—"],
  ];
  const COLS = [
    ["num", "#", 64], ["out", "Out", 240], ["says", "He says", 512],
    ["layout", "Layout", 180], ["what", "What happens", 542], ["sfx", "SFX", 150],
  ];
  const PAD = 36, TITLE = 96, HEAD = 60, ROWH = 94, FOOT = 20;
  const W = PAD * 2 + COLS.reduce((a, c) => a + c[2], 0);          // 1760
  const H = TITLE + HEAD + ROWS.length * ROWH + FOOT;              // 1022
  const X = {}; { let x = PAD; for (const [k, , w] of COLS) { X[k] = [x, w]; x += w; } }

  const CSS = `
  .tcard { background: var(--brand-card); color: var(--ink); font-family: "Inter", sans-serif; transform-origin: 0 0; }
  .tcard .tc-title { position: absolute; left: ${PAD}px; top: 0; height: ${TITLE}px; display: flex; align-items: center; gap: 22px; }
  .tcard .tc-file { position: relative; width: 58px; height: 58px; flex: none; }
  .tcard .tc-file .v7-disc { left: 29px; top: 29px; }
  .tcard .tc-name { font: 500 26px "Geist Mono", monospace; color: var(--muted); }
  .tcard .tc-h { font: 800 40px "Inter Tight", sans-serif; letter-spacing: -.02em; color: var(--ink); white-space: nowrap; }
  .tcard .tc-row, .tcard .tc-headrow { position: absolute; left: 0; width: ${W}px; }
  .tcard .tc-headrow { top: ${TITLE}px; height: ${HEAD}px; border-top: 2px solid var(--brand-deep); border-bottom: 2px solid var(--brand-deep); box-sizing: border-box; }
  .tcard .tc-row { height: ${ROWH}px; border-bottom: 1px solid color-mix(in srgb, var(--brand-deep) 14%, transparent); box-sizing: border-box; }
  .tcard .tc-c { position: absolute; top: 0; padding: 0 14px; box-sizing: border-box; height: 100%; display: flex; align-items: center; }
  .tcard .tc-c > span { display: -webkit-box; -webkit-box-orient: vertical; -webkit-line-clamp: 2; overflow: hidden;
    font-size: 27px; line-height: 36px; font-weight: 500; }
  .tcard .tc-headrow .tc-c > span { font: 700 27px/36px "Inter", sans-serif; color: var(--ink); position: relative; z-index: 1; }
  .tcard .tc-c.num > span { font-weight: 700; }
  .tcard .tc-c.out > span { font-variant-numeric: tabular-nums; color: var(--muted); white-space: nowrap; }
  .tcard .tc-c.layout > span { font-weight: 700; font-size: 24px; letter-spacing: .04em; }
  .tcard .tc-c.sfx > span { color: var(--muted); }
  .tcard .v7-hl { z-index: 0; }`;

  function style() {
    if (document.getElementById("tablecard-css")) return;
    const s = document.createElement("style"); s.id = "tablecard-css"; s.textContent = CSS; document.head.appendChild(s);
  }
  const esc = (t) => t.replace(/&/g, "&amp;").replace(/</g, "&lt;");
  const cells = (vals) => COLS.map(([k], i) =>
    `<div class="tc-c ${k}" style="left:${X[k][0]}px;width:${X[k][1]}px"><span>${esc(vals[i])}</span></div>`).join("");

  function build(parent, { x = 0, y = 0, id = "table" } = {}) {
    style();
    const el = document.createElement("div");
    el.className = "page tcard"; el.id = id;
    Object.assign(el.style, { left: x + "px", top: y + "px", width: W + "px", height: H + "px" });
    el.innerHTML =
      `<div class="tc-title"><div class="tc-file"><div class="v7-disc" style="--d:58px"><i class="v7-gl" style="--ic:url('assets/icons/file-text.svg')"></i></div></div>` +
      `<span class="tc-name">beat_table.md</span><span class="tc-h">3 · Nine stages (1:47)</span></div>` +
      `<div class="tc-headrow">${cells(COLS.map((c) => c[1]))}</div>` +
      ROWS.map((r, i) => `<div class="tc-row" style="top:${TITLE + HEAD + i * ROWH}px">${cells(r)}</div>`).join("");
    (typeof parent === "string" ? document.querySelector(parent) : parent).appendChild(el);
    return {
      el, W, H, rows: Array.from(el.querySelectorAll(".tc-row")), headRow: el.querySelector(".tc-headrow"),
      file: el.querySelector(".tc-file .v7-disc"),
      head: (k) => [X[k][0] + 4, TITLE + 8, X[k][1] - 8, HEAD - 16],
      headText: (k) => { const s = el.querySelector(`.tc-headrow .tc-c.${k} > span`); return [X[k][0] + 14 - 6, TITLE + 10, s.offsetWidth + 12, HEAD - 20]; },
      colCenter: (k) => X[k][0] + X[k][1] / 2,
    };
  }

  function rowsIn(B, tc, t0, { gap = 0.14 } = {}) {
    tc.rows.forEach((r, i) => {
      B.tl.fromTo(r, { opacity: 0, y: 26 }, { opacity: 1, y: -3, duration: 6 * B.F, ease: "power3.out" }, t0 + i * gap);
      B.tl.to(r, { y: 0, duration: 5 * B.F, ease: "power2.inOut" }, t0 + i * gap + 6 * B.F);
    });
  }

  function hlNow(tc, k) {
    const [x, y, w, h] = tc.headText(k);
    const d = document.createElement("div"); d.className = "v7-hl";
    Object.assign(d.style, { left: x + "px", top: y + "px", width: w + "px", height: h + "px" });
    tc.el.appendChild(d);
    return d;
  }

  return { build, rowsIn, hlNow, W, H, ROWS };
})();
