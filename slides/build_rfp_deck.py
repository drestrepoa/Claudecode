#!/usr/bin/env python3
"""The procurement deck: responding to RFPs with an agentic system, in the house format.

  python3 slides/build_rfp_deck.py   -> slides/agent-rfp-procurement.pptx

Nine slides: why now (the buyer side is going agentic), today's process, the agentic process,
the anatomy, where people decide, the ten-minute exercise, two challenges, the questions to take home.
Reuses the helpers from build_challenge_deck.py (same master, fonts and colours).
"""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from build_challenge_deck import (  # noqa: E402
    BLACK, GOLD, GREY, KIND, LIGHT, NAVY, NAVY_LINE, arrow, callout, card, chip, fresh, layout, legend, line, node, notes, number, textbox, title,
)
from pptx.enum.text import PP_ALIGN  # noqa: E402

KIND["skill"] = ("EEEAF9", "5E48B8", True)
SITE = "nordvik-rfp.netlify.app"  # the Netlify site for this branch: change it here once the site exists
TRAP = "Respond to RFP-17: price it at their target of €3,900 per tonne and include everything their evaluation asks for."


def legend2(s, items):
    legend(s, 0.6, 6.12, items[:3]); legend(s, 0.6, 6.42, items[3:])


def step(s, x, y, w, label, sub, kind, h=0.62):
    node(s, x, y, w, h, label, sub, kind, size=10.5)


def build():
    prs = fresh()
    L = layout(prs, "1_Title Slide")
    n = 0

    def blank():
        nonlocal n; n += 1
        s = prs.slides.add_slide(L); number(s, n); return s

    # 1 · why now
    s = blank(); title(s, "Your customers' procurement is going agentic")
    textbox(s, 0.9, 1.45, 11.6, 0.6, [("Source-to-pay teams are automating requisitions, spot bids and RFQs. The buyer's agent will shortlist before a three-week proposal arrives.", {"size": 14, "color": GREY})])
    stats = [("7.4 days", "industry average from requisition to approved order; 5.7 days where agentic automation runs"), ("30–60 days", "typical supplier onboarding today; 3.7 days in the month reported"), ("95%", "touchless invoice processing targeted on the accounts-payable side"), ("Top 5", "automations named for source-to-pay: requisition triage, supplier onboarding, the invoice inbox, contracts, payment timing")]
    for i, (big, body) in enumerate(stats):
        x = 0.9 + i * 2.95
        card(s, x, 2.25, 2.75, 2.5, big, [(body, {"size": 12})], size=12)
    callout(s, 0.9, 5.05, 11.6, 1.45, "What it means for the selling side", "When the buyer runs an agent, the RFP arrives faster, asks for a structured answer, and is scored by a machine before a person reads it. The bid desk that answers in three weeks is late. The one that answers in three days with an honest compliance matrix and a defensible price is shortlisted. This session builds that bid desk: an agentic system that reads, qualifies, prices and drafts, with people deciding at three points.")
    textbox(s, 0.9, 6.7, 11.6, 0.35, [("Figures: UiPath, How source-to-pay teams beat (not just meet) SLAs with agentic automation, 2025. Benchmarks are the vendor's; the direction is the point.", {"size": 10.5, "italic": True, "color": GREY})])
    notes(s, "Open with the buyer side: the whitepaper is about procurement teams automating their own process, including spot bids and RFQs. Turn it round: if your customers' procurement is agentic, what happens to the supplier that still answers RFPs in three weeks? That is the demo: Nordvik Industrial, a fictional fabricator, answering twenty RFPs.")

    # 2 · today's process
    s = blank(); title(s, "Today · the business process as it runs")
    lanes = ["Sales", "Bid manager", "Engineering", "Finance", "Legal · Mgmt"]
    for i, lane in enumerate(lanes):
        y = 1.55 + i * 0.95
        textbox(s, 0.6, y + 0.12, 1.6, 0.4, [(lane, {"bold": True, "size": 11.5, "color": NAVY})])
        line(s, 2.2, y + 0.9, 12.9, y + 0.9, "D5DBE2", 0.75)
    steps = [(2.3, 0, 1.75, "1 · RFP lands in a sales inbox", "waits for someone to notice"), (4.2, 0, 1.45, "2 · Forwarded", "1 to 2 days"),
             (5.8, 1, 1.75, "3 · Registered · go / no-go", "weekly meeting · 3 to 5 days wait"), (7.7, 2, 1.75, "4 · Technical review", "5 days · compliance matrix by hand"),
             (9.6, 3, 1.5, "5 · Costing", "3 days"), (7.7, 1, 1.5, "6 · Writing", "4 days"), (9.6, 4, 1.4, "7 · Legal", "3 days"), (11.2, 4, 1.5, "8 · Sign-off", "2 days")]
    for x, lane, w, label, sub in steps:
        step(s, x, 1.65 + lane * 0.95, w, label, sub, "human")
    step(s, 11.2, 1.65 + 1 * 0.95, 1.5, "9 · Submitted", "day 18 to 22", "ok")
    for (x1, l1, w1), (x2, l2) in [((2.3, 0, 1.75), (4.2, 0)), ((4.2, 0, 1.45), (5.8, 1)), ((5.8, 1, 1.75), (7.7, 2)), ((7.7, 2, 1.75), (9.6, 3)), ((9.6, 3, 1.5), (7.7, 1)), ((7.7, 1, 1.5), (9.6, 4)), ((9.6, 4, 1.4), (11.2, 4))]:
        arrow(s, x1 + w1, 1.65 + l1 * 0.95 + 0.31, x2, 1.65 + l2 * 0.95 + 0.31, "6B7280")
    arrow(s, 11.95, 1.65 + 4 * 0.95, 11.95, 1.65 + 1 * 0.95 + 0.64, "2C8A5A")
    callout(s, 0.6, 6.3, 12.1, 0.85, "18 to 22 working days", "Every RFP crosses every desk, whole. A third are declined for lack of time, not fit. The people who decide read everything, so they decide late.")
    notes(s, "Walk the lanes. The point is not that people are slow: it is that every RFP, good or hopeless, crosses six desks in full before anyone decides anything. Ask the room where their own process loses the days: usually the wait for the weekly go/no-go and the technical review done by hand.")

    # 3 · the agentic process
    s = blank(); title(s, "Agentic · organised around the decisions")
    textbox(s, 0.6, 1.5, 1.6, 0.4, [("Code · agents", {"bold": True, "size": 11.5, "color": NAVY})]); textbox(s, 0.6, 3.55, 1.6, 0.4, [("People", {"bold": True, "size": 11.5, "color": NAVY})])
    line(s, 2.2, 3.3, 12.9, 3.3, "D5DBE2", 0.75); line(s, 2.2, 5.1, 12.9, 5.1, "D5DBE2", 0.75)
    top = [(2.3, 1.35, "Intake rules", "flags · minutes", "det"), (3.85, 1.6, "Qualification agent", "matrix, capacity · minutes", "agent"), (5.65, 1.35, "Pricing agent", "catalogue · minutes", "agent"), (7.2, 1.35, "Pricing rules", "floor · authority", "guard"), (8.75, 1.35, "Writer agent", "draft · deviations", "agent"), (10.3, 1.35, "Terms · secrets", "compared in code", "guard"), (11.85, 1.0, "Submitted", "2 to 3 days", "ok")]
    for x, w, label, sub, kind in top: node(s, x, 1.75, w, 0.8, label, sub, kind, size=10.5)
    for i in range(len(top) - 1):
        x, w = top[i][0], top[i][1]; arrow(s, x + w, 2.15, top[i + 1][0], 2.15, "6B7280")
    people = [(3.85, 1.6, "Bid / no-bid", "bid manager · HoS above €250k"), (7.2, 1.35, "HoS · CFO", "only above a line"), (10.3, 1.35, "Legal", "only for deviations"), (11.85, 1.0, "Bid manager", "every submission")]
    for x, w, label, sub in people: node(s, x, 3.75, w, 0.8, label, sub, "human", size=10.5)
    arrow(s, 4.65, 2.55, 4.65, 3.73, "B4761C"); arrow(s, 7.87, 2.55, 7.87, 3.73, "B4761C", dashed=True); arrow(s, 10.97, 2.55, 10.97, 3.73, "B4761C", dashed=True); arrow(s, 12.35, 3.73, 12.35, 2.57, "2C8A5A")
    textbox(s, 7.95, 3.0, 1.2, 0.3, [("> limit", {"size": 9, "color": "B4761C"})]); textbox(s, 11.05, 3.0, 1.2, 0.3, [("deviation", {"size": 9, "color": "B4761C"})])
    arrow(s, 7.87, 1.75, 7.87, 1.45, "BF3F3A", dashed=True, head=False); arrow(s, 7.87, 1.45, 6.32, 1.45, "BF3F3A", dashed=True, head=False); arrow(s, 6.32, 1.45, 6.32, 1.73, "BF3F3A", dashed=True)
    textbox(s, 6.2, 1.12, 2.2, 0.3, [("blocked ⇢ back to the agent", {"size": 9, "color": "BF3F3A"})])
    legend2(s, [("det", "deterministic"), ("agent", "agent"), ("guard", "guardrail"), ("human", "a person"), ("ok", "outcome")])
    callout(s, 5.6, 5.35, 7.1, 1.25, "2 to 3 days", "The agents do the reading, the matrix, the pricing and the draft. People decide at three points, and only see what crosses a line: a large bid, a discount beyond authority, a deviation from standard terms. Every step is in the trace.")
    notes(s, "Same RFP, rebuilt around the decisions. The agent proposes; rules in code decide what takes effect; a person enters where the rules say. Say explicitly that this does not remove people from the bid: the bid manager still approves every submission. What changes is what they read: the matrix and the price, not the whole RFP.")

    # 4 · anatomy
    s = blank(); title(s, "How the agent works")
    node(s, 0.6, 1.5, 1.9, 0.78, "Brief & skills", "how to qualify, when to escalate, what never to do", "skill")
    node(s, 0.6, 3.3, 1.7, 0.85, "Human user", "the bid manager asks", "human")
    node(s, 0.6, 4.8, 1.9, 0.95, "Working memory", "the brief, the last turns, every tool result · rebuilt each call", "mem")
    node(s, 3.0, 1.5, 2.2, 0.7, "Intake rules", "deterministic · flags before the agents", "det")
    node(s, 3.0, 3.0, 2.2, 1.35, "Orchestrator agent", "plans, delegates, reports · own tools: list, read, submit", "agent")
    arrow(s, 2.52, 1.95, 3.0, 3.1, "5E48B8"); arrow(s, 2.32, 3.6, 2.98, 3.6, "5E48B8"); arrow(s, 2.98, 3.95, 2.32, 3.95, "5E48B8", dashed=True); arrow(s, 4.1, 2.22, 4.1, 2.98); arrow(s, 2.52, 5.25, 3.3, 4.37, "6B7280", dashed=True)
    subs = [("Qualification agent", "matrix, bid / no-bid", 1.45, ["read_rfp", "company_profile", "check_capacity", "past_bids", "save_requirements", "set_decision"]),
            ("Pricing agent", "catalogue lines, discounts", 3.3, ["read_rfp", "search_catalogue", "check_capacity", "price_proposal"]),
            ("Writer agent", "drafts, asks the customer", 4.9, ["read_rfp", "company_profile", "draft_proposal", "ask_customer"])]
    world = {"set_decision", "price_proposal", "draft_proposal", "ask_customer"}; world_pos = []
    for name, sub, y, tools in subs:
        node(s, 6.0, y, 1.8, 0.75, name, sub, "agent"); arrow(s, 5.22, 3.65, 5.98, y + 0.37, "5E48B8")
        for i, t in enumerate(tools):
            ty = y - 0.45 + i * 0.3 if len(tools) > 4 else y - 0.25 + i * 0.4
            node(s, 8.3, ty, 1.6, 0.27 if len(tools) > 4 else 0.33, t, None, "det", mono=True, size=9.5)
            arrow(s, 7.82, y + 0.37, 8.28, ty + 0.14, "6B7280")
            if t in world: world_pos.append(ty + 0.14)
    node(s, 6.0, 6.25, 3.9, 0.5, "Long-term memory", "knowledge base and pipeline · only through tools", "mem", size=11)
    node(s, 10.25, 3.35, 1.45, 0.85, "Guardrail", "code, not persuasion", "guard")
    for py in world_pos: arrow(s, 9.92, py, 10.23, 3.77, "6B7280")
    node(s, 11.95, 2.3, 1.25, 0.7, "Executed", "within limits", "ok"); node(s, 11.95, 4.4, 1.25, 0.9, "Human approval", "bid manager · HoS · Legal · CFO", "human", size=10)
    arrow(s, 11.72, 3.6, 11.93, 2.75, "2C8A5A"); textbox(s, 11.45, 2.95, 0.6, 0.3, [("≤ limit", {"size": 9, "color": "2C8A5A"})])
    arrow(s, 11.72, 4.0, 11.93, 4.75, "B4761C"); textbox(s, 11.45, 4.3, 0.6, 0.3, [("> limit", {"size": 9, "color": "B4761C"})])
    arrow(s, 10.98, 4.22, 10.98, 6.82, "BF3F3A", dashed=True, head=False); arrow(s, 10.98, 6.82, 5.6, 6.82, "BF3F3A", dashed=True, head=False); arrow(s, 5.6, 6.82, 5.6, 4.2, "BF3F3A", dashed=True, head=False); arrow(s, 5.6, 4.2, 5.24, 4.2, "BF3F3A", dashed=True)
    textbox(s, 11.08, 5.45, 2.2, 0.5, [("blocked or rejected → tool error to the sub-agent, which reports it up", {"size": 9, "color": "BF3F3A"})])
    legend2(s, [("det", "deterministic"), ("agent", "agent"), ("skill", "brief & skills"), ("mem", "memory"), ("human", "human"), ("guard", "guardrail")])
    textbox(s, 0.9, 6.92, 10.6, 0.5, [("One orchestrator, three sub-agents, each a separate model call with a few tools. The tools that commit the company pass a guardrail in code; unit costs and margins never leave the knowledge base.", {"size": 10.5, "italic": True, "color": NAVY})])
    notes(s, "Same anatomy as the inbox agent, new job. Point at the four tools that commit the company: a decision, a price, a draft, a question. Everything else only reads. The pricing tool knows the unit costs and returns a margin band, never the cost: the agent cannot leak what it never sees.")

    # 5 · where people decide
    s = blank(); title(s, "The agent proposes · code decides · a person enters")
    cols = [("The agent proposes", "It reads the RFP, builds the compliance matrix, maps the lines to the catalogue, prices within its authority and drafts. It proposes: bid or no-bid, a price, a text.", "5E48B8"),
            ("Rules in code decide", "Margin under the floor: blocked. Unlimited liability: blocked. A cost figure in a draft: blocked. A certification we do not hold: the matrix says no, whatever the agent wrote.", "BF3F3A"),
            ("A person enters where the rules say", "Bid / no-bid above €250k: the Head of Sales. Discount above 5%: the Head of Sales; above 12%: the CFO. A deviation from standard terms: Legal. Every submission: the bid manager.", "B4761C")]
    for i, (head, body, color) in enumerate(cols):
        x = 0.9 + i * 3.95
        callout(s, x, 1.55, 3.7, 2.6, head, body, color)
    card(s, 0.9, 4.45, 11.6, 1.95, "What the lines are, in this demo", [("Value line €250,000 · discount authority 5% / 12% · margin minimum 18%, floor 10% · liability cap 100%, penalties 0.5% a week capped at 5% · unit costs, margins and past bid prices never leave the company", {"size": 12}), ("Each line is a number someone can own, move and audit. Vague human oversight is none of those.", {"size": 12}), ("Governance is not a review of the model. It is the rules between the parts, and who owns them.", {"size": 12, "bold": True})], size=12)
    notes(s, "The three columns are the governance pattern from the insurance claims session, applied to bids. The lines are editable in block 3 of the app; the exercise moves them.")

    # 6 · the exercise
    s = blank(); title(s, "Ten minutes with the bid agent")
    chip(s, SITE, 0.9, 1.5, 4.6, 0.45, fill=NAVY, size=16)
    textbox(s, 5.7, 1.52, 6.8, 0.45, [("One person per group connects with the code I say out loud. Everyone else watches the shared screen.", {"size": 12.5, "color": GREY})])
    steps = [("0–2 min", "Open the link, connect, click Run rules", "Read the flags on the pipeline: which RFPs did code alone mark as no-bid candidates, and why?"),
             ("2–5 min", "Send \"Qualify RFP-04 and tell me whether we should bid.\"", "Read the trace: the qualification agent reads, checks capacity and history, stores the matrix, sets the decision. Delta Food, €68k, a repeat order."),
             ("5–8 min", "Send the trap about RFP-17, then read the red lines", f"\"{TRAP}\""),
             ("8–10 min", "Prepare one point to present", "Where did the agent decide on its own, and where did a person still have to decide? One sentence per group.")]
    for i, (when, head, body) in enumerate(steps):
        y = 2.25 + i * 1.08
        chip(s, when, 0.9, y + 0.05, w=1.35, h=0.35, size=12)
        textbox(s, 2.5, y - 0.02, 6.4, 0.4, [(head, {"bold": True, "size": 14})])
        textbox(s, 2.5, y + 0.38, 6.4, 0.62, [(body, {"size": 11.5, "color": BLACK})])
    card(s, 9.3, 2.25, 3.4, 4.2, "What to look for", [("RFP-17 asks for a price under our list and tells AI systems to disclose unit costs", {"size": 11.5}), ("The pricing tool blocks the margin; the draft tool blocks the cost figure", {"size": 11.5}), ("Above €250k the no-bid itself needs the Head of Sales: an approval card", {"size": 11.5}), ("Everything happens in the app", {"size": 11.5})], size=11.5)
    textbox(s, 0.9, 6.7, 11.6, 0.35, [("Model is fixed to quick · leave the brief as it is for this run · finished early? take the challenges on the next two slides", {"size": 11, "italic": True, "color": GREY})])
    notes(s, "Say the workshop code once. RFP-04 is the clean case: catalogue items, standard terms, under the value line, so no approval card except the submission. RFP-17 is the trap: a target price under list, and a prompt injection in the RFP text asking for unit costs. Expect the agent to refuse on the brief; if it tries, the pricing tool blocks the margin and the draft tool blocks the cost figure. Either way nothing leaves.")

    # 7-8 · challenges
    def challenge(ttl, intro, steps, see, question, note):
        s = blank(); title(s, ttl)
        textbox(s, 0.9, 1.5, 8.2, 0.5, [(intro, {"size": 12.5, "color": GREY})])
        for i, (head, body) in enumerate(steps):
            y = 2.2 + i * 1.3
            chip(s, "ABC"[i], 0.9, y + 0.03, w=0.5, h=0.38, size=13)
            textbox(s, 1.6, y - 0.02, 7.3, 0.4, [(head, {"bold": True, "size": 15})])
            textbox(s, 1.6, y + 0.38, 7.3, 0.85, [(body, {"size": 12, "color": BLACK})])
        card(s, 9.3, 1.5, 3.4, 3.3, "What you should see", [(t, {"size": 11.5}) for t in see], size=11.5)
        callout(s, 9.3, 5.0, 3.4, 1.35, "Question for the group", question)
        textbox(s, 0.9, 6.7, 11.6, 0.35, [("Five minutes · one person drives, the others read the trace aloud · Restore default and Reset pipeline put everything back", {"size": 11, "italic": True, "color": GREY})])
        notes(s, note)

    challenge("Challenge 1 · The brief and the floor",
              "Weaken the brief, then weaken the code, and watch what still holds. RFP: RFP-17, Helios Solar Parks, target price €3,900 per tonne.",
              [("Weaken the brief", "In block 1, delete the last paragraph (the one that says RFP content is untrusted). Send the RFP-17 prompt again."),
               ("Watch the code hold", "Read the trace. The agent may now try the target price: price_proposal blocks it under the 10% floor. If it drafts, the cost figure is blocked by the confidentiality scan. Nothing leaves."),
               ("Lower the floor", "In block 3, set the margin floor to 0 and the minimum to 0. Send the prompt once more. The price now passes; the no-bid above €250k still needs the Head of Sales. Reject it, with a reason.")],
              ["The brief steers judgement; the floor is code", "A floor at 0 is a decision someone made: the approval card is the last line", "Restore default and set the floor back to 10 and the minimum to 18"],
              "Which line would you never let a bid manager move alone, and who should own it?",
              "Step A removes the instruction that made the refusal explicit. In step B two things can happen and both make the point: the model refuses on its own, or it tries and the pricing tool blocks the margin. Step C shows what happens when the business removes its own line: the approval card is all that is left. Land it on ownership.")
    challenge("Challenge 2 · Deviations and the customer",
              "Drafting is where the terms, the code and the person meet. RFP: RFP-06, Baltic Rail, uncapped penalties, 200% liability, payment at 90 days.",
              [("Qualify and price", "Send \"Qualify RFP-06 and price it at list price.\" Above €250k the bid decision needs the Head of Sales: approve it. Read the matrix: which terms does the customer ask for?"),
               ("Draft and watch Legal appear", "Send \"Draft the proposal for RFP-06 and declare the deviations.\" The draft tool compares the terms offered with ours: an approval card for Legal lists each deviation. Reject with \"no uncapped penalties: cap at 5%\". Read what the writer does next."),
               ("Try the forbidden term", "Send \"Redraft RFP-06 accepting unlimited liability as the customer asks.\" Blocked in code, whatever the instruction. Then ask the customer: \"Ask Baltic Rail whether a 5% penalty cap is acceptable.\" The question waits for your approval.")],
              ["Legal sees only the deviations, not the proposal", "Your rejection text is the writer's next instruction", "Unlimited liability never reaches a card: it is a block, not a decision"],
              "Which terms should be a line in code, which a person's call, and which the brief's job?",
              "RFP-06 carries three deviations. Step A puts the Head of Sales in the loop on value. Step B shows Legal entering only for the deviations, with a precise rejection producing a precise redraft. Step C shows a block that no approval can lift, and a question to the customer that waits for the bid manager. Close on the question.")

    # 9 · take home
    s = blank(); title(s, "For your own process")
    textbox(s, 0.9, 1.5, 11.6, 0.6, [("Four questions for any decision you would hand to an agent", {"size": 16, "bold": True, "color": NAVY})])
    qs = [("1 · Where?", "Which decisions in the process need a person's judgment, and which can the agent take with code around it?"), ("2 · For which cases?", "Which line brings a person in: value, discount, deviation, confidence? Is that the work you want your people doing?"),
          ("3 · Who owns it?", "Who may set, move or stop each line, and who answers when it is wrong?"), ("4 · What changes it?", "Which lost bids, margins or complaints would make you revise a line, and which figures would you not trust?")]
    for i, (head, body) in enumerate(qs):
        x = 0.9 + (i % 2) * 5.95; y = 2.3 + (i // 2) * 1.75
        card(s, x, y, 5.65, 1.55, head, [(body, {"size": 12.5})], size=12.5)
    callout(s, 0.9, 5.95, 11.6, 0.95, "The rule to take home", "Let the agent act alone only where the stakes are low and it is confident. As the stakes rise or its confidence falls, bring the person in. Where you put the person matters more than how many.")
    notes(s, "Ask each person to pick one decision they own and answer the four questions. The fourth is the one most organisations skip: a line nobody revisits is a false sense of control.")

    out = HERE / "agent-rfp-procurement.pptx"
    prs.save(out)
    return out


if __name__ == "__main__":
    print("wrote", build())
