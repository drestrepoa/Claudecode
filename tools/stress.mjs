#!/usr/bin/env node
// Stress test for a deployed Inbox Agent site.
//
//   node tools/stress.mjs https://your-site.netlify.app WORKSHOP_CODE 30 [quick|default|complex]
//
// Sends N requests to /api/agent at the same moment, each a realistic first round of the agent
// (brief + tool definitions + one question), reads every stream to the end, and reports:
//   - HTTP status per request (401 = wrong code, 429 = rate limited, 502 = key or upstream problem)
//   - time to first byte and total time
//   - whether the stream ended cleanly (a missing message_stop means the function was cut off)
// Cost: N model calls on the site's key. On the quick tier that is a few cents per run.

const [site, code, nArg, tierArg] = process.argv.slice(2);
if (!site || !code) { console.error("usage: node tools/stress.mjs <site-url> <workshop-code> [count=30] [tier=quick]"); process.exit(1); }
const N = Math.max(1, Number(nArg) || 30);
const tier = tierArg || "quick";
const url = site.replace(/\/$/, "") + "/api/agent";

const system = "You are the inbox assistant for a test run. Reply in one short sentence and do not call any tool.";
const tools = [{ name: "inbox_stats", description: "Counts for the whole inbox. Do not call it in this test.", input_schema: { type: "object", properties: {} } }];
const body = JSON.stringify({ tier, system, messages: [{ role: "user", content: "Say hello in five words." }], tools });

async function one(i) {
  const t0 = performance.now(); let ttfb = null, status = 0, events = 0, ended = false, chars = 0, err = "";
  try {
    const r = await fetch(url, { method: "POST", headers: { "content-type": "application/json", "x-workshop-code": code }, body });
    status = r.status;
    if (!r.ok) { err = (await r.text()).slice(0, 120); }
    else {
      const reader = r.body.getReader(); const dec = new TextDecoder(); let buf = "";
      while (true) {
        const { value, done } = await reader.read(); if (done) break;
        if (ttfb === null) ttfb = performance.now() - t0;
        buf += dec.decode(value, { stream: true });
        const lines = buf.split("\n"); buf = lines.pop();
        for (const line of lines) { if (!line.trim()) continue; events++; try { const ev = JSON.parse(line); if (ev.type === "message_stop") ended = true; if (ev.type === "content_block_delta" && ev.delta?.text) chars += ev.delta.text.length; if (ev.type === "error") err = JSON.stringify(ev.error).slice(0, 120); } catch (e) {} }
      }
    }
  } catch (e) { err = e.message; }
  return { i, status, ttfb, total: performance.now() - t0, events, ended, chars, err };
}

console.log(`Firing ${N} simultaneous requests at ${url} on tier "${tier}"...`);
const t0 = performance.now();
const results = await Promise.all(Array.from({ length: N }, (_, i) => one(i)));
const wall = (performance.now() - t0) / 1000;

const byStatus = {}; for (const r of results) byStatus[r.status] = (byStatus[r.status] || 0) + 1;
const ok = results.filter((r) => r.status === 200);
const clean = ok.filter((r) => r.ended);
const cut = ok.filter((r) => !r.ended);
const pct = (arr, p) => { if (!arr.length) return null; const s = [...arr].sort((a, b) => a - b); return s[Math.min(s.length - 1, Math.floor(p * s.length))]; };
const fmt = (ms) => ms == null ? "n/a" : (ms / 1000).toFixed(1) + "s";

console.log(`\nDone in ${wall.toFixed(1)}s wall time.`);
console.log("HTTP status counts:", JSON.stringify(byStatus));
console.log(`Streams that ended cleanly: ${clean.length}/${ok.length}` + (cut.length ? `   <-- ${cut.length} cut off before message_stop (function timeout?)` : ""));
console.log(`Time to first byte: median ${fmt(pct(ok.map((r) => r.ttfb), 0.5))}, p90 ${fmt(pct(ok.map((r) => r.ttfb), 0.9))}, max ${fmt(pct(ok.map((r) => r.ttfb), 1))}`);
console.log(`Total time:         median ${fmt(pct(ok.map((r) => r.total), 0.5))}, p90 ${fmt(pct(ok.map((r) => r.total), 0.9))}, max ${fmt(pct(ok.map((r) => r.total), 1))}`);
const errs = results.filter((r) => r.err); if (errs.length) { console.log("\nErrors (first 5):"); for (const r of errs.slice(0, 5)) console.log(`  #${r.i} status ${r.status}: ${r.err}`); }
console.log("\nHow to read it:");
console.log("  401 -> the workshop code does not match WORKSHOP_CODE on the site");
console.log("  429 -> Anthropic rate limit; check https://platform.claude.com/settings/limits and the tier your organisation is on");
console.log("  502 -> the site's API key was rejected or Anthropic returned an error; the message above says which");
console.log("  cut off -> the Netlify function timed out mid-stream; use the quick tier or a plan with a longer function timeout");
