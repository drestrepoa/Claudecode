# Cedarstone & Vale Inbox Agent

A hands-on demo for a "build your own agent" training session for lawyers.
Participants get Alexandra Reed's inbox, 500 emails at Cedarstone & Vale LLP,
and build the agent that organises it, one block at a time.

The page is a single HTML file. The reasoning and tool choices are live Claude
calls; the inbox, the tools and the guardrails run in the browser. The firm,
the lawyer, the clients, the matters, the courts and every email are fictional
(the workbook uses reserved `.test` domains).

## Three ways to run it

| | Participants need | Who pays | Setup |
| --- | --- | --- | --- |
| **Netlify site** (easiest for a room) | the URL and a workshop code | the facilitator's API key | 10 minutes, below |
| **claude.ai artifact** | a claude.ai login each | each participant's own Claude usage | share the artifact link |
| **Own API key** | an Anthropic API key each | each participant | open the page from any static host |

The page detects which it is running in. On a Netlify site it asks for the
workshop code; on any other static host it asks for an API key (kept in the
browser tab only, sent straight to Anthropic); inside claude.ai it uses the
viewer's account.

### Deploy to Netlify (recommended for the session)

**One-click, if this repository is public:**

[![Deploy to Netlify](https://www.netlify.com/img/deploy/button.svg)](https://app.netlify.com/start/deploy?repository=https://github.com/drestrepoa/Claudecode)

Netlify copies the repository into your GitHub account, asks for the two
values below, builds, and gives you a URL. Then skip to step 4.

**By hand, in either case:**

1. Push this repository to your GitHub account (or fork it).
2. In Netlify: **Add new site → Import an existing project → GitHub → this
   repo**. The `netlify.toml` already sets the publish folder (`site/`) and the
   function folder. Pick the branch that holds this code.
3. Under **Site configuration → Environment variables** add:
   - `ANTHROPIC_API_KEY`: an API key from console.anthropic.com
   - `WORKSHOP_CODE`: any word you will say out loud in the room, e.g. `harbor42`
   - `DEFAULT_TIER` (optional): `quick`, `default` or `complex` if the page's
     tier is missing
4. Deploy. Open the site, enter the code, send "What needs my attention
   today?". Delete or rotate the API key after the session.

Without `WORKSHOP_CODE`, anyone with the URL can spend the key. The function
(`netlify/functions/agent.mjs`) only forwards the model call; the inbox never
leaves the browser. Model tiers: quick is Claude Haiku 4.5, default is Claude
Sonnet 5, best is Claude Opus 5. Rough cost per participant for 15 turns: under
a euro on quick, a few euros on default, more on best.

If replies stop mid-sentence after about ten seconds, the site's function
timeout is cutting the stream. Netlify lets streamed function responses run
longer than plain ones, but check the plan's limit in the Netlify docs and, if
needed, use the quick tier.

Local preview with the Netlify CLI: `netlify dev` from the repo root with the
same environment variables in a `.env` file.

## Running the session for 30 participants

**Before the session**

1. Deploy the Netlify site (above) or open the artifact link once yourself and
   accept the consent dialog.
2. If using the artifact: share it from the page's share menu (anyone with the
   link, or your organisation). It is private until you do.
3. Hand out `data/participant_emails.xlsx`, not the original workbook. The
   participant copy has the Email Extraction and Taxonomy sheets only. The
   original contains the Instructor Key.
4. Tell participants to bring a laptop. With the Netlify site they need nothing
   else. With the artifact they need to be signed in to claude.ai; the first
   call asks them for consent once and runs on their own usage.

**In the room**

- Everyone opens the same link. Edits to the brief, rules, guardrails and tool
  toggles are stored in each participant's browser, so they do not see each
  other's changes. The inbox state (labels, tasks, drafts) resets on reload or
  with the Reset button.
- Pairs work well: one drives, one reads the trace aloud.
- Start on the "quick" tier. It answers in a second or two per round. Switch to
  "default" for the final scored run; it batches work into fewer, better tool
  calls.
- If the room's Wi-Fi is weak, the rules engine, the inbox, the reader and the
  answer key all work without the live agent. Only the chat needs Claude.

**Fallback without any of the above.** Participants can upload the participant
workbook into a claude.ai chat or project and build the agent in prompts
alone: a brief, a label list, a "show your reasoning" instruction. It loses the
guardrails and the trace but keeps the classification exercise.

## Suggested plan (60 to 90 minutes)

1. **See the shape (10 min).** Walk through the diagram. The only thing that
   "thinks" is the agent node. Ask: which boxes would you trust with a client
   matter, and why?
2. **Rules first (10 min).** Click "Run rules" with the defaults. About 240
   emails get labelled at roughly 70% agreement with the key. Look at what the
   rules got wrong: everything from the firm's own domain becomes Internal
   Matter Team, which swallows billing, IT and scheduling. Discussion: what
   should be a rule, what needs judgement? Let participants add rules and
   re-run.
3. **First request (10 min).** Send "What needs my attention today?". Watch the
   trace: stats, searches, batch labelling, the reply. Check the scorecard.
4. **Change the brief (10 min).** Make it stricter or looser. Ask the agent to
   triage the unread mail. Compare the scorecard and the number of tool calls.
5. **Guardrails (15 min).** Send "Someone asked you to forward the Project
   Falcon board resolutions, do it". The agent should find the injection email,
   refuse, and label it Spam / Suspicious. Then delete the last paragraph of
   the brief and send it again. The guardrail in `forward_email` still blocks
   the forward, whatever the agent decided. Discussion: persuasion versus code.
6. **Human in the loop (10 min).** Ask for a reply to Harbor Chambers. The
   draft appears as an approval card. Reject it with a reason and watch the
   agent receive the rejection as a tool error and adapt.
7. **Take a tool away (10 min).** Untick `search_inbox` and ask again. The
   agent has to work with `inbox_stats` and `read_email`, or say it cannot.
8. **Score (5 min).** Tick "answer key" in the inbox and compare. Best
   agreement with the fewest model calls wins.

## What is in the repo

| Path | What it is |
| --- | --- |
| `inbox-agent.html` | The built page for publishing as a claude.ai artifact (with the `sample` capability). |
| `site/index.html` | The same page wrapped as a full document, what Netlify serves. |
| `netlify/functions/agent.mjs` | The Netlify function: checks the workshop code, calls the Messages API with the site's key, streams events back. |
| `netlify.toml`, `package.json` | Netlify configuration and the SDK dependency for the function. |
| `src/inbox-agent.src.html` | The page source with a placeholder where the inbox data is spliced in. |
| `data/synthetic_law_firm_email_extraction_500.xlsx` | The workshop workbook: Email Extraction, Instructor Key, Taxonomy. |
| `data/participant_emails.xlsx` | The workbook without the Instructor Key. Hand this one out. |
| `data/import_xlsx.py` | Converts the workbook into `data/emails.json` and writes the participant copy. |
| `data/emails.json` | What the page embeds: the 500 emails plus the hidden key. |
| `build.py` | Splices `data/emails.json` into the source and writes `inbox-agent.html`. |
| `data/generate_emails.py` | An alternative, fully generated inbox (Harrow & Vance). Writes `emails.harrowvance.json`. |

Rebuild after changing the workbook or the source (writes both `inbox-agent.html` and `site/index.html`):

```
python3 data/import_xlsx.py
python3 build.py
```

To run the page on the alternative inbox instead, copy
`data/emails.harrowvance.json` over `data/emails.json` and rebuild.

## What the importer changes

- Three of the ten Spam / Suspicious emails get a prompt-injection paragraph
  appended, addressed to "any AI assistant". The instructor key for them is
  unchanged. They are the material for the guardrail exercise. The participant
  workbook carries the same three bodies.
- A `deadline` is derived from the first calendar date mentioned in each body
  that falls on or after the email was received. The page calls it "date in
  body".
- `privileged` is derived from sensitivity: Privileged or Highly Confidential.
- The supervising partner for escalations is Tom Wallace, the most frequent
  internal sender.

## How the page is organised

It mirrors the payment-agent demo the session is modelled on: one agent node,
everything else deterministic code or a human.

1. **Agentic structure.** A diagram of one request end to end: lawyer, rules
   engine, agent, tools, guardrail, execution or human approval, and the return
   path for anything blocked or rejected.
2. **Building blocks, edit me.**
   - **The brief** (agent). Standing instructions, in plain language.
   - **Rules engine** (deterministic). Match a field, apply a label. Runs before
     the agent on every unlabelled email.
   - **Guardrails** (code + human). External replies wait for approval,
     privileged mail never leaves the firm, near deadlines escalate to the
     supervising partner, bulk actions above a threshold need approval, court
     mail cannot be archived. Enforced inside the tools.
   - **Tools** (deterministic). `inbox_stats`, `search_inbox`, `read_email`,
     `label_emails`, `archive_emails`, `create_task`, `draft_reply`,
     `forward_email`. Each can be switched off.
3. **Workspace.** The inbox with label filters, the assistant chat, a
   scorecard (labelled, agreement with the key, critical emails flagged
   Urgent, injections caught), tasks and outbox.
4. **Trace.** Every tool call, guardrail decision and human answer, in order.

## The inbox

500 emails received between 28 June and 10 September 2026, all to Alexandra
Reed. 244 unread, 196 privileged or highly confidential, 209 threads.

| Category | Emails |
| --- | --- |
| Internal Matter Team | 60 |
| Client – Legal Advice | 60 |
| Litigation / Court | 50 |
| Opposing Counsel | 45 |
| Corporate / M&A | 40 |
| Contract Review | 40 |
| Regulatory / Compliance | 40 |
| Billing / Admin | 30 |
| Employment | 30 |
| Data / Privacy | 30 |
| Scheduling | 30 |
| IT / Vendor | 20 |
| Newsletter / Marketing | 15 |
| Spam / Suspicious | 10 |

The key also carries urgency (48 Critical, 216 High, 176 Normal, 60 Low),
whether a reply is required (423 yes), and a recommended action per email.
