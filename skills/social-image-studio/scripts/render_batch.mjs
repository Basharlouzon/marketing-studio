// render_batch.mjs — proven IAB screenshot batch renderer.
// Usage from a mcp__node_repl__js cell (nodeRepl host provides ZCODE_PLUGIN_ROOT):
//   const m = await import(pathToFileURL("<skill>/social-image-studio/scripts/render_batch.mjs").href);
//   await m.renderBatch({
//     jobs: [ { url: "http://localhost:8734/html/oct-01.html", w: 1080, h: 1350,
//               out: "/abs/path/images/oct-01.png" }, ... ],
//     onProgress: (done, total, lastFile) => {},   // optional
//   });
// Implements: plugin bootstrap, IAB tab recovery, viewport per job, cache-buster,
// 2-attempt retry with 4s backoff, skip-if-exists resume.
import { join } from "node:path";
import { pathToFileURL } from "node:url";
import fs from "node:fs";

export async function renderBatch({ jobs, onProgress }) {
  const browserPluginRoot =
    process.env.ZCODE_PLUGIN_ROOT ?? process.env.CLAUDE_PLUGIN_ROOT;
  if (!browserPluginRoot) throw new Error("Browser plugin root unavailable in this host");
  const browserClientUrl = pathToFileURL(
    join(browserPluginRoot, "scripts", "browser-client.mjs"),
  ).href;
  const { setupBrowserRuntime } = await import(browserClientUrl);
  await setupBrowserRuntime({ globals: globalThis });
  const browser = await agent.browsers.get("iab");

  // Tab recovery: reuse an existing controlled tab, else open one.
  let tab;
  const controlled = await browser.tabs.list();
  const match = controlled.find((t) => (t.url || "").startsWith("http://localhost"));
  if (match) tab = await browser.tabs.get(match.id);
  else {
    const userTabs = await browser.user.openTabs();
    const um = userTabs.find((t) => (t.url || "").startsWith("http://localhost"));
    tab = um ? await browser.user.claimTab(um) : await browser.tabs.new();
  }

  const bust = Date.now();
  let done = 0;
  const fails = [];
  let currentSize = null;
  for (const job of jobs) {
    if (fs.existsSync(job.out)) { done++; continue; }        // resume support
    if (currentSize !== `${job.w}x${job.h}`) {
      await tab.setViewportSize({ width: job.w, height: job.h });
      currentSize = `${job.w}x${job.h}`;
    }
    let ok = false;
    for (let attempt = 0; attempt < 2 && !ok; attempt++) {
      try {
        const sep = job.url.includes("?") ? "&" : "?";
        await tab.goto(`${job.url}${sep}v=${bust}`);
        await tab.playwright.waitForLoadState({ state: "domcontentloaded" });
        await tab.playwright.waitForTimeout(500);
        const png = await tab.screenshot();
        fs.writeFileSync(job.out, png);
        done++; ok = true;
      } catch (e) {
        await new Promise((r) => setTimeout(r, 4000));       // host-load backoff
        if (attempt === 1) fails.push(job.out);
      }
    }
    if (onProgress) onProgress(done, jobs.length, job.out);
  }
  return { done, fails };
}
