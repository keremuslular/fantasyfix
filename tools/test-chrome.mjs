// Loads ESPN Fantasy in headless Chrome, with or without the extension, and reports
// whether calls to ESPN's stats API succeed. Usage: node tools/test-chrome.mjs [--with-extension]
import { spawn } from "node:child_process";
import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";

const CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const withExt = process.argv.includes("--with-extension");
const ext = resolve(import.meta.dirname, "../extension");
const profile = mkdtempSync(join(tmpdir(), "ff-chrome-"));
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

// Talk to Chrome over the DevTools pipe (fd 3 = to Chrome, fd 4 = from Chrome).
const chrome = spawn(CHROME, [
  "--headless=new", "--no-first-run", "--no-default-browser-check",
  `--user-data-dir=${profile}`, "--remote-debugging-pipe", "--enable-unsafe-extension-debugging",
], { stdio: ["ignore", "ignore", "ignore", "pipe", "pipe"] });

let id = 0;
let buffer = "";
const pending = new Map();
chrome.stdio[4].on("data", (chunk) => {
  buffer += chunk.toString();
  let i;
  while ((i = buffer.indexOf("\0")) >= 0) {
    const msg = JSON.parse(buffer.slice(0, i));
    buffer = buffer.slice(i + 1);
    if (msg.id && pending.has(msg.id)) { pending.get(msg.id)(msg); pending.delete(msg.id); }
  }
});
const send = (method, params = {}, sessionId) => new Promise((r) => {
  const n = ++id;
  pending.set(n, r);
  chrome.stdio[3].write(JSON.stringify({ id: n, method, params, ...(sessionId && { sessionId }) }) + "\0");
});

try {
  if (withExt) {
    const res = await send("Extensions.loadUnpacked", { path: ext });
    if (res.error) throw new Error("Could not load extension: " + res.error.message);
    console.log("extension loaded:", res.result.id);
  }
  const { result: { targetId } } = await send("Target.createTarget", { url: "about:blank" });
  const { result: { sessionId } } = await send("Target.attachToTarget", { targetId, flatten: true });
  await send("Page.navigate", { url: "https://fantasy.espn.com/basketball/players/projections" }, sessionId);
  await sleep(9000);

  const res = await send("Runtime.evaluate", {
    awaitPromise: true, returnByValue: true, expression: `(async () => {
      const entries = performance.getEntriesByType('resource')
        .filter(e => /site(\\.web)?\\.api\\.espn\\.com/.test(e.name))
        .map(e => e.responseStatus + ' ' + new URL(e.name).host + new URL(e.name).pathname);
      let direct;
      try {
        const r = await fetch('https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard');
        direct = r.status + ' via ' + new URL(r.url).host + ', ' + (await r.json()).events?.length + ' games';
      } catch (e) { direct = 'FAILED: ' + e.message; }
      return { entries: [...new Set(entries)], direct };
    })()`,
  }, sessionId);
  const result = res.result.result.value;

  console.log(withExt ? "== WITH extension" : "== WITHOUT extension");
  console.log("fetch(site.api.espn.com scoreboard) from page:", result.direct);
  console.log("stats API requests the page made:");
  for (const e of result.entries) console.log("  " + e);
} finally {
  chrome.kill();
  await sleep(500);
  rmSync(profile, { recursive: true, force: true });
}
