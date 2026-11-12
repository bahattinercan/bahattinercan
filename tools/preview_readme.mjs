// README'yi push etmeden yerelde GitHub gorunumuyle render eder, yatay tasma
// ve sayfa yuksekligini CDP uzerinden olcer.
//
// Kullanim: node tools/preview_readme.mjs [README.md] [390,1280]
// Gereksinim: npx (marked) + Chrome. Bagimlilik kurmaz, gecici dosyada calisir.

import { spawn, execSync } from "node:child_process";
import { readFileSync, writeFileSync, mkdtempSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, resolve, dirname, basename } from "node:path";

const [, , mdArg = "README.md", widthArg = "390,1280"] = process.argv;
const MD = resolve(mdArg);
const WIDTHS = widthArg.split(",").map(Number);
const PORT = 9333;
const CHROME = "C:/Program Files/Google/Chrome/Application/chrome.exe";

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

// GitHub'in markdown govdesine yaklasan minimal stil: genislik, font, tablo.
const CSS = `
:root { color-scheme: dark; }
* { box-sizing: border-box; }
body {
  margin: 0; background: #0d1117; color: #e6edf3;
  font: 16px/1.5 -apple-system, BlinkMacSystemFont, "Segoe UI", Noto Sans, Helvetica, Arial, sans-serif;
  word-wrap: break-word;
}
.markdown-body { max-width: 1012px; margin: 0 auto; padding: 40px 24px 80px; }
.markdown-body h1, .markdown-body h2, .markdown-body h3 {
  font-weight: 600; line-height: 1.25; margin: 24px 0 16px;
  padding-bottom: .3em; border-bottom: 1px solid #30363d;
}
.markdown-body h2 { font-size: 1.5em; }
.markdown-body h3 { font-size: 1.25em; border-bottom: 0; padding-bottom: 0; margin: 16px 0 8px; }
.markdown-body h1 { border-bottom: 0; }
.markdown-body p { margin: 0 0 16px; }
.markdown-body a { color: #4493f8; text-decoration: none; }
.markdown-body a:hover { text-decoration: underline; }
.markdown-body img { max-width: 100%; height: auto; border: 0; }
.markdown-body table { border-collapse: collapse; margin: 0 0 16px; }
.markdown-body table td { padding: 4px; border: 0; vertical-align: top; }
.markdown-body code {
  background: rgba(110,118,129,.4); border-radius: 6px; padding: .2em .4em;
  font: 85% ui-monospace, SFMono-Regular, Menlo, monospace;
}
.markdown-body sub { font-size: .75em; color: #8b949e; }
.markdown-body [align=center] { text-align: center; }
.markdown-body div[align=center] > a > img { margin: 2px 4px 2px 0; }
`;

function chromeRunning() {
  try {
    execSync(`curl -s --max-time 2 http://127.0.0.1:${PORT}/json/version`, { stdio: "ignore" });
    return true;
  } catch {
    return false;
  }
}

async function startChrome() {
  if (chromeRunning()) return null;
  const proc = spawn(
    CHROME,
    [`--remote-debugging-port=${PORT}`, `--user-data-dir=${join(tmpdir(), "pi-readme-cdp")}`, "--headless=new", "--disable-gpu", "--hide-scrollbars", "about:blank"],
    { stdio: "ignore", detached: false }
  );
  for (let i = 0; i < 40; i++) {
    await sleep(250);
    if (chromeRunning()) return proc;
  }
  throw new Error("Chrome CDP baslatilamadi");
}

function rpc(ws, id, method, params) {
  return new Promise((res) => {
    const on = (ev) => {
      const msg = JSON.parse(ev.data);
      if (msg.id === id) {
        ws.removeEventListener("message", on);
        res(msg.result);
      }
    };
    ws.addEventListener("message", on);
    ws.send(JSON.stringify({ id, method, params }));
  });
}

async function main() {
  const out = mkdtempSync(join(tmpdir(), "readme-preview-"));
  const body = execSync(`npx -y marked -i "${MD}"`, { encoding: "utf8", maxBuffer: 32 * 1024 * 1024 });
  const htmlPath = join(out, basename(MD, ".md") + ".html");
  writeFileSync(
    htmlPath,
    `<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><base href="file:///${dirname(MD).replace(/\\/g, "/")}/">
     <style>${CSS}</style><article class="markdown-body">${body}</article>`,
    "utf8"
  );

  const proc = await startChrome();
  const targets = await (await fetch(`http://127.0.0.1:${PORT}/json/list`)).json();
  const page = targets.find((t) => t.type === "page");
  const ws = new WebSocket(page.webSocketDebuggerUrl);
  await new Promise((r) => (ws.onopen = r));

  let id = 1;
  await rpc(ws, id++, "Page.enable", {});
  const reports = [];
  for (const width of WIDTHS) {
    await rpc(ws, id++, "Emulation.setDeviceMetricsOverride", {
      width, height: 900, deviceScaleFactor: 2, mobile: width < 600,
    });
    await rpc(ws, id++, "Page.navigate", { url: `file:///${htmlPath.replace(/\\/g, "/")}` });
    await sleep(1200);
    const r = await rpc(ws, id++, "Runtime.evaluate", {
      expression: `(() => {
        const doc = document.documentElement;
        const wide = [];
        document.querySelectorAll('table, img, pre').forEach((el) => {
          const b = el.getBoundingClientRect();
          if (b.width > window.innerWidth + 1) wide.push({ tag: el.tagName, w: Math.round(b.width) });
        });
        return {
          width: window.innerWidth,
          scrollWidth: doc.scrollWidth,
          overflowPx: doc.scrollWidth - window.innerWidth,
          pageHeight: doc.scrollHeight,
          screens: +(doc.scrollHeight / window.innerHeight).toFixed(1),
          imageCount: document.images.length,
          brokenImages: [...document.images].filter((i) => i.currentSrc && i.naturalWidth === 0).map((i) => i.src.slice(-60)),
          overflowing: wide.slice(0, 6),
        };
      })()`,
      returnByValue: true,
    });
    reports.push(r.result.value);

    const shot = await rpc(ws, id++, "Page.captureScreenshot", { format: "png", captureBeyondViewport: true });
    const png = join(out, `readme-${width}.png`);
    writeFileSync(png, Buffer.from(shot.data, "base64"));
    reports[reports.length - 1].screenshot = png;
  }

  console.log(JSON.stringify({ markdown: MD, preview: htmlPath, reports }, null, 2));
  ws.close();
  proc?.kill();
  process.exit(0);
}

main().catch((e) => {
  console.error("HATA:", e.message);
  process.exit(1);
});
