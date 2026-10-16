// GitHub profil sayfasini verilen genislikte acar ve yatay tasma olup
// olmadigini CDP uzerinden olcer. Tahmin degil, gercek olcum.
//
// Kullanim: node tools/measure_overflow.mjs <url> <genislik> [beklemeMs]

const [, , url, widthArg, waitArg] = process.argv;
const width = Number(widthArg || 390);
const waitMs = Number(waitArg || 9000);
const PORT = 9333;

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function cdpTargets() {
  const res = await fetch(`http://127.0.0.1:${PORT}/json/list`);
  return res.json();
}

function rpc(ws, id, method, params) {
  return new Promise((resolve) => {
    const onMsg = (ev) => {
      const msg = JSON.parse(ev.data);
      if (msg.id === id) {
        ws.removeEventListener("message", onMsg);
        resolve(msg.result);
      }
    };
    ws.addEventListener("message", onMsg);
    ws.send(JSON.stringify({ id, method, params }));
  });
}

async function evaluate(ws, expr, id) {
  const r = await rpc(ws, id, "Runtime.evaluate", {
    expression: expr,
    returnByValue: true,
    awaitPromise: false,
  });
  return r?.result?.value;
}

const targets = await cdpTargets();
const page = targets.find((t) => t.type === "page" && t.webSocketDebuggerUrl);
if (!page) {
  console.error("HATA: sayfa hedefi bulunamadi");
  process.exit(1);
}

// Sekmeyi istenen genislige ayarla (Emulation ile, pencere boyutundan bagimsiz)
const ws = new WebSocket(page.webSocketDebuggerUrl);
await new Promise((r) => (ws.onopen = r));

let id = 1;
await rpc(ws, id++, "Page.enable", {});
await rpc(ws, id++, "Emulation.setDeviceMetricsOverride", {
  width,
  height: 900,
  deviceScaleFactor: 1,
  mobile: width < 600,
});
await rpc(ws, id++, "Page.navigate", { url });
await sleep(waitMs);

const report = await evaluate(
  ws,
  `(() => {
     const doc = document.documentElement;
     const body = document.body;
     const overflow = Math.max(doc.scrollWidth, body.scrollWidth) - window.innerWidth;
     const wide = [];
     document.querySelectorAll('table, img, pre, code').forEach((el) => {
       const r = el.getBoundingClientRect();
       if (r.width > window.innerWidth + 1) {
         wide.push({
           tag: el.tagName.toLowerCase(),
           cls: (el.className || '').toString().slice(0, 40),
           w: Math.round(r.width),
           text: (el.textContent || '').trim().slice(0, 40),
         });
       }
     });
     const md = document.querySelector('.markdown-body');
     return {
       innerWidth: window.innerWidth,
       scrollWidth: Math.max(doc.scrollWidth, body.scrollWidth),
       overflowPx: overflow,
       markdownOverflow: md ? md.scrollWidth - md.clientWidth : null,
       overflowing: wide.slice(0, 8),
       counting: wide.length,
     };
   })()`,
  id++
);

console.log(JSON.stringify(report, null, 2));
ws.close();
process.exit(0);
