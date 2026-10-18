// capture.py's browser path: a real Chrome (not "HeadlessChrome") so bot walls (Akamai etc.) serve the page,
// scroll the whole page so scroll-reveal content renders, strip cookie/consent banners and fixed overlays,
// force still-hidden text visible, then screenshot the top <height> CSS px at 2x.
// usage: node capture_page.cjs <chrome> <url> <out.png> <width> <height> <waitMs>
const puppeteer = require("puppeteer-core");
const [chrome, url, out, w, h, wait] = process.argv.slice(2);
const W = +w, H = +h, WAIT = +wait;
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
(async () => {
  const b = await puppeteer.launch({ executablePath: chrome, headless: "new", args: ["--hide-scrollbars", "--no-first-run"] });
  try {
    const p = await b.newPage();
    await p.setUserAgent("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36");
    await p.setViewport({ width: W, height: 960, deviceScaleFactor: 2 });
    await p.goto(url, { waitUntil: "networkidle2", timeout: 60000 }).catch(() => {});
    await sleep(Math.min(WAIT, 4000));
    for (let y = 0; y < H + 2400; y += 400) { await p.evaluate((y) => window.scrollTo(0, y), y); await sleep(220); }
    await p.evaluate(() => window.scrollTo(0, 0));
    await sleep(1500);
    await p.evaluate(() => {
      const kill = /onetrust|cookie|consent|gdpr|cmp-|truste|osano|didomi|usercentrics/i;
      document.querySelectorAll("body *").forEach((e) => {
        const s = getComputedStyle(e), id = (e.id || "") + " " + (e.className && e.className.baseVal === undefined ? e.className : "");
        if (kill.test(id) && (s.position === "fixed" || s.position === "sticky" || s.zIndex > 100)) e.remove();
        else if (s.position === "fixed" && e.getBoundingClientRect().top > 200) e.remove();   // chat bubbles, bottom bars
      });
      document.querySelectorAll("body *").forEach((e) => {
        const s = getComputedStyle(e);
        if (s.opacity === "0" && e.textContent.trim().length) { e.style.opacity = 1; e.style.transform = "none"; }
      });
      document.documentElement.style.overflow = "auto"; document.body.style.overflow = "auto";
    });
    await sleep(800);
    await p.screenshot({ path: out, clip: { x: 0, y: 0, width: W, height: H }, captureBeyondViewport: true });
  } finally { await b.close(); }
})().catch((e) => { console.error(e.message); process.exit(1); });
