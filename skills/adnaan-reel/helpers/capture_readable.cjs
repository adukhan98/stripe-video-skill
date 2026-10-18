// capture.py --readable (v5, reel-06): a page/post captured so its TEXT IS READABLE in a 1080x1920 reel.
// Light colour scheme, a NARROW phone viewport at 3x (≈ 45 px text once the 900 px-wide capture is shown at ~0.9),
// fixed bars / dialogs / login walls removed, then the main element (selector, else <article>, else <main>, else body)
// is screenshotted, and every requested phrase is located: its line boxes (in capture px) plus the line boxes of the
// whole element, so capture.py can cut a strip of N lines around each phrase and give the highlight box inside it.
// usage: node capture_readable.cjs <chrome> <url> <out.png> <cssWidth> <selector|""> <phrasesJSON>
const puppeteer = require("puppeteer-core");
const fs = require("fs");
const [chrome, url, out, w, selector, phrasesJSON] = process.argv.slice(2);
const W = +w, DSF = 3, phrases = JSON.parse(phrasesJSON || "[]");
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
(async () => {
  const b = await puppeteer.launch({ executablePath: chrome, headless: "new", args: ["--hide-scrollbars", "--no-first-run"] });
  try {
    const p = await b.newPage();
    await p.setUserAgent("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36");
    await p.emulateMediaFeatures([{ name: "prefers-color-scheme", value: "light" }]);
    await p.setViewport({ width: W, height: 4400, deviceScaleFactor: DSF });
    await p.goto(url, { waitUntil: "networkidle2", timeout: 60000 }).catch(() => {});
    await sleep(4000);
    await p.evaluate(() => {
      for (const el of document.querySelectorAll('[data-testid="BottomBar"], [role="dialog"], #layers')) el.remove();
      const kill = /onetrust|cookie|consent|gdpr|cmp-|truste|osano|didomi|usercentrics/i;
      document.querySelectorAll("body *").forEach((e) => {
        const s = getComputedStyle(e), id = (e.id || "") + " " + (typeof e.className === "string" ? e.className : "");
        if (kill.test(id) || s.position === "fixed" || s.position === "sticky") e.style.display = "none";
        else if (s.opacity === "0" && e.textContent.trim().length) { e.style.opacity = 1; e.style.transform = "none"; }
      });
    });
    await sleep(800);
    const info = await p.evaluate((selector, phrases, DSF) => {
      const root = (selector && document.querySelector(selector)) || document.querySelector("article") || document.querySelector("main") || document.body;
      root.setAttribute("data-capture-root", "1");
      const A = root.getBoundingClientRect();
      const nodes = []; let acc = "";
      const tw = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
      for (let n; (n = tw.nextNode()); ) { nodes.push([n, acc.length]); acc += n.textContent; }
      const loc = (i) => { for (let k = nodes.length - 1; k >= 0; k--) if (nodes[k][1] <= i) return [nodes[k][0], i - nodes[k][1]]; };
      const rel = (q) => [q.left - A.left, q.top - A.top, q.width, q.height].map((v) => Math.round(v * DSF));
      // every rendered text line of the element (merged by top) → lets the cutter snap strips to whole lines
      const lines = [];
      for (const [n] of nodes) {
        if (!n.textContent.trim()) continue;
        const r = document.createRange(); r.selectNodeContents(n);
        for (const q of r.getClientRects()) {
          if (q.width < 2) continue;
          const v = rel(q), hit = lines.find((l) => Math.abs(l[1] - v[1]) < 6 * DSF);
          if (hit) { const x1 = Math.max(hit[0] + hit[2], v[0] + v[2]); hit[0] = Math.min(hit[0], v[0]); hit[2] = x1 - hit[0]; hit[3] = Math.max(hit[3], v[3]); }
          else lines.push(v);
        }
      }
      lines.sort((a, b) => a[1] - b[1]);
      const found = {};
      for (const ph of phrases) {
        const i = acc.indexOf(ph);
        if (i < 0) { found[ph] = null; continue; }
        const r = document.createRange(); r.setStart(...loc(i)); r.setEnd(...loc(i + ph.length));
        found[ph] = [...r.getClientRects()].filter((q) => q.width > 2).map(rel);
      }
      return { size: [Math.round(A.width * DSF), Math.round(A.height * DSF)], lines, found,
               rect: [A.left + scrollX, A.top + scrollY, A.width, A.height] };
    }, selector, phrases, DSF);
    // v6.1: capture in TILES. One element screenshot taller than Chrome's ~16k device-px texture limit silently repeats
    // the top of the page (reel-07: a 39k px article came back as the same few screens over and over). capture.py
    // stitches the tiles back into <out> and refuses identical neighbours.
    const [rx, ry, rw, rh] = info.rect, TILE = 1200;   // CSS px per tile (3600 device px at 3x)
    info.tiles = [];
    for (let k = 0, y = 0; y < rh; k++, y += TILE) {
      const f = out.replace(/\.png$/, `.tile${String(k).padStart(3, "0")}.png`);
      await p.screenshot({ path: f, clip: { x: rx, y: ry + y, width: rw, height: Math.min(TILE, rh - y) }, captureBeyondViewport: true });
      info.tiles.push(f);
    }
    fs.writeFileSync(out.replace(/\.png$/, ".layout.json"), JSON.stringify(info));
  } finally { await b.close(); }
})().catch((e) => { console.error(e.message); process.exit(1); });
