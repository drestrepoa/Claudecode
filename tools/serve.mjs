#!/usr/bin/env node
// Run the Inbox Agent locally, without Netlify.
//
//   ANTHROPIC_API_KEY=sk-ant-... WORKSHOP_CODE=room1 node tools/serve.mjs [path/to/index.html] [port]
//
// Serves the built page (default: site/index.html, so check out the branch you want first,
// or run `python3 build.py hr`) and mounts the same function Netlify runs at /api/agent.
// A .env file in the repo root is read if present (KEY=value lines).
import http from "node:http";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const envFile = path.join(root, ".env");
if (fs.existsSync(envFile)) {
  for (const line of fs.readFileSync(envFile, "utf8").split("\n")) {
    const m = line.match(/^\s*([A-Z_]+)\s*=\s*(.*?)\s*$/);
    if (m && !process.env[m[1]]) process.env[m[1]] = m[2].replace(/^["']|["']$/g, "");
  }
}

const page = path.resolve(root, process.argv[2] || "site/index.html");
const port = Number(process.argv[3] || process.env.PORT || 8787);
if (!fs.existsSync(page)) {
  console.error(`page not found: ${page}\nBuild it first: python3 build.py hr   (or check out the branch that has it)`);
  process.exit(1);
}
const { default: agent } = await import(path.join(root, "netlify/functions/agent.mjs"));
const html = fs.readFileSync(page);
const title = (html.toString("utf8").match(/<title>([^<]*)<\/title>/) || [])[1] || "Inbox Agent";

http.createServer(async (req, res) => {
  if (req.url.startsWith("/api/agent")) {
    let body = "";
    for await (const c of req) body += c;
    const r = await agent(new Request("http://localhost" + req.url, { method: req.method, headers: req.headers, body: req.method === "POST" ? body : undefined }));
    res.writeHead(r.status, Object.fromEntries(r.headers));
    if (!r.body) return res.end();
    for await (const chunk of r.body) res.write(chunk);
    return res.end();
  }
  res.writeHead(200, { "content-type": "text/html; charset=utf-8", "cache-control": "no-cache" });
  res.end(html);
}).listen(port, () => {
  const key = process.env.ANTHROPIC_API_KEY ? "set" : "MISSING: set ANTHROPIC_API_KEY";
  const code = process.env.WORKSHOP_CODE ? "set" : "not set: any code accepted";
  console.log(`${title}\n  page:   http://localhost:${port}\n  agent:  /api/agent  (key ${key}, workshop code ${code})`);
});
