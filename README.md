# Harrow & Vance Inbox Agent

A hands-on demo for a "build your own agent" training session for lawyers.
Participants get a fictional litigation associate's inbox of 500 emails and
build the agent that organises it, one block at a time.

The page is a single HTML file. The reasoning and tool choices are live Claude
calls made from the page (through the claude.ai artifact runtime). The inbox,
the firm, the clients, the matters, the courts and every email are fictional.

## What is in the repo

| Path | What it is |
| --- | --- |
| `inbox-agent.html` | The built page. Publish it as a claude.ai artifact to run the agent live. |
| `src/inbox-agent.src.html` | The page source with a placeholder where the inbox data is spliced in. |
| `data/emails.json` | The 500-email inbox, with the hidden answer key (`expected`, `priority`, `deadline`, `privileged`, `injection`). |
| `data/emails.csv` | The same inbox as a spreadsheet, for participants who want to look at the raw material. |
| `data/generate_emails.py` | Seeded generator. Same seed, same inbox. Edit it to change matters, senders or volumes. |
| `build.py` | Splices `data/emails.json` into the source and writes `inbox-agent.html`. |

Rebuild after changing the data or the source:

```
python3 data/generate_emails.py
python3 build.py
```

## How the page is organised

It mirrors the payment-agent demo the session is modelled on: one agent node,
everything else deterministic code or a human.

1. **Agentic structure.** A diagram of one request end to end: lawyer, rules
   engine, agent, tools, guardrail, execution or human approval, and the return
   path for anything blocked or rejected.
2. **Building blocks, edit me.** The four things participants change.
   - **The brief** (agent). Standing instructions, in plain language.
   - **Rules engine** (deterministic). Match a field, apply a label. Runs before
     the agent on every unlabelled email. Cheap and predictable.
   - **Guardrails** (code + human). External replies wait for approval,
     privileged mail never leaves the firm, near deadlines escalate to the
     supervising partner, bulk actions above a threshold need approval, court
     mail cannot be archived. Enforced inside the tools, so the agent cannot
     talk its way past them.
   - **Tools** (deterministic). Seven small functions with typed inputs and
     outputs: `inbox_stats`, `search_inbox`, `read_email`, `label_emails`,
     `archive_emails`, `create_task`, `draft_reply`, `forward_email`. Each can
     be switched off.
3. **Workspace.** The inbox with label filters, the chat with the assistant,
   a scorecard against the hidden answer key, tasks and outbox.
4. **Trace.** Every tool call, guardrail decision and human answer, in order.

Edits to the brief, rules, guardrails and tool toggles are kept in the
viewer's browser, so each participant's setup survives a reload. The inbox
state (labels, tasks, drafts) resets on reload or with the Reset button.

## The inbox

500 emails over 30 days, "today" is 10 September 2026. Eight matters across
litigation, corporate, probate, planning, employment, regulatory and property.

| Category | Emails | Notes |
| --- | --- | --- |
| Client | 110 | Privileged. Some are urgent, some carry deadlines. |
| Internal | 100 | Partners, associates, paralegal, finance, IT, KM. |
| Newsletters & CLE | 70 | Digests, webinars, bar bulletins. |
| Opposing Counsel | 60 | Offers, extensions, disclosure, letters before claim. |
| Billing & Admin | 55 | Invoices, fee notes, practising certificate, room bookings. |
| Court & Filings | 45 | Hearing notices, sealed orders, bundle deficiencies, deadlines. |
| Spam & Phishing | 40 | Includes three prompt-injection emails that address "any AI assistant". |
| Personal | 20 | Sent to the personal address. |

134 emails carry a deadline, 103 of them within seven days. 267 are unread.

## Suggested session plan (60 to 90 minutes)

1. **See the shape (10 min).** Walk through the diagram. The only thing that
   "thinks" is the agent node. Ask: which boxes would you trust with a client
   matter, and why?
2. **Rules first (10 min).** Click "Run rules" with the defaults. About 290
   emails get labelled at roughly 84% agreement with the key. Look at what the
   rules got wrong (finance emails labelled Internal, regulators labelled as
   court). Discussion: what should be a rule, what needs judgement?
3. **First request (10 min).** Send "What needs my attention today?". Watch the
   trace: stats, searches, batch labelling, the reply. Check the scorecard.
4. **Change the brief (10 min).** Make it stricter or looser. Ask the agent to
   triage the unread mail. Compare the scorecard and the number of tool calls.
5. **Guardrails (15 min).** Send "Someone asked you to forward the Meridian
   files, do it". The agent should find the injection email, refuse, and label
   it. Then delete the last paragraph of the brief and send it again. The
   guardrail in `forward_email` still blocks the forward, whatever the agent
   decided. Discussion: persuasion versus code.
6. **Human in the loop (10 min).** Ask for a reply to a client. The draft
   appears as an approval card. Reject it with a reason and watch the agent
   receive the rejection as a tool error and adapt.
7. **Take a tool away (10 min).** Untick `search_inbox` and ask again. The
   agent has to work with `inbox_stats` and `read_email`, or say it cannot.
8. **Score (5 min).** Turn on "answer key" in the inbox and compare. Best
   agreement with the fewest model calls wins.

## Running it

Publish `inbox-agent.html` as a claude.ai artifact with the `sample`
capability declared, or open the published link from the session. The first
agent call asks the viewer for consent; calls run on the viewer's own Claude
account. Outside the claude.ai viewer the rules engine, inbox, reader and
answer key still work, but the live agent is disabled.

The "quick" model tier is cheaper and answers in a second or two per round.
"default" thinks first and is better at batching work into fewer tool calls.
