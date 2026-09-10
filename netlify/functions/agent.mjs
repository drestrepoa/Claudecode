// Netlify Function: the room's shared door to Claude.
//
// The page posts { tier, system, messages, tools } here with an `x-workshop-code`
// header. The function checks the code, picks the model for the tier, calls the
// Messages API with the site's ANTHROPIC_API_KEY, and streams the raw events back
// as JSON lines. The page runs the tool loop; this function never sees the inbox.
//
// Environment variables (Site settings → Environment variables):
//   ANTHROPIC_API_KEY   required
//   WORKSHOP_CODE       recommended; if unset, anyone with the URL can spend the key
//   DEFAULT_TIER        optional: quick | default | complex (default: "default")
//   ANTHROPIC_WORKSPACE_ID  only if the key is an organisation-level key that Anthropic says
//                       "is not scoped to a workspace"; the wrkspc_... id from the console

import Anthropic from "@anthropic-ai/sdk";

const MODELS = { quick: "claude-haiku-4-5", default: "claude-sonnet-5", complex: "claude-opus-5" };
const json = (obj, status = 200) => new Response(JSON.stringify(obj), { status, headers: { "content-type": "application/json" } });

export default async (req) => {
  if (req.method !== "POST") return json({ error: "POST only" }, 405);
  const code = process.env.WORKSHOP_CODE || "";
  if (code && req.headers.get("x-workshop-code") !== code) return json({ error: "wrong workshop code" }, 401);
  if (!process.env.ANTHROPIC_API_KEY) return json({ error: "ANTHROPIC_API_KEY is not set on this site" }, 500);

  let body;
  try { body = await req.json(); } catch (e) { return json({ error: "body must be JSON" }, 400); }
  if (!Array.isArray(body.messages) || !body.messages.length) return json({ error: "messages required" }, 400);

  const tier = MODELS[body.tier] ? body.tier : (MODELS[process.env.DEFAULT_TIER] ? process.env.DEFAULT_TIER : "default");
  const model = MODELS[tier];
  const params = {
    model,
    max_tokens: 4000,
    system: String(body.system || "").slice(0, 20000),
    messages: body.messages,
    tools: Array.isArray(body.tools) ? body.tools.slice(0, 16) : [],
    // Cache the stable prefix (tools, brief, earlier turns): later rounds of the same request re-read it
    // at a tenth of the price, and cached tokens do not count toward the input-tokens-per-minute limit.
    cache_control: { type: "ephemeral" },
  };
  if (tier !== "quick") params.output_config = { effort: "medium" }; // Haiku 4.5 does not take effort

  const client = new Anthropic(process.env.ANTHROPIC_WORKSPACE_ID ? { defaultHeaders: { "anthropic-workspace-id": process.env.ANTHROPIC_WORKSPACE_ID } } : {});
  try {
    // Wait for the API to accept the request (bad key, bad model, rate limit surface here as JSON errors),
    // then hand the page the raw stream events as JSON lines; the page rebuilds the message from them.
    const { data: stream } = await client.messages.stream(params, { signal: req.signal }).withResponse();
    return new Response(stream.toReadableStream(), {
      status: 200,
      headers: { "content-type": "application/x-ndjson", "cache-control": "no-cache", "x-model": model },
    });
  } catch (e) {
    const status = e?.status === 429 ? 429 : 502;
    const why = e?.status === 401 ? "the site's ANTHROPIC_API_KEY was rejected by Anthropic" : (e?.error?.error?.message || e?.message || "upstream error");
    return json({ error: why }, status);
  }
};

export const config = { path: "/api/agent" };
