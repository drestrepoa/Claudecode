#!/usr/bin/env python3
"""The inbox agent explained, with screenshots of the application in English, and four exercises for fifteen minutes.

  SHOTS=<folder of screenshots> python3 slides/build_inbox_explainer.py   -> slides/inbox-agent-explained.pptx

The screenshots come from an automated pass over the built page (data/hr, English mode); without a SHOTS folder the
picture slots stay empty but the deck still builds. House format through build_challenge_deck.py; the progressive
diagram comes from build_quick_exercise.py.
"""
import os
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from build_challenge_deck import (  # noqa: E402
    BLACK, GOLD, GREY, KIND, LIGHT, NAVY, NAVY_LINE, SITE, arrow, callout, card, chip, fresh, layout, legend, node, notes, number, textbox, title,
)
from build_quick_exercise import flow  # noqa: E402
from pptx.dml.color import RGBColor  # noqa: E402
from pptx.enum.shapes import MSO_SHAPE  # noqa: E402
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN  # noqa: E402
from pptx.util import Inches, Pt  # noqa: E402

KIND["skill"] = ("EEEAF9", "5E48B8", True)
SHOTS = Path(os.environ.get("SHOTS", "")) if os.environ.get("SHOTS") else None


def picture(s, name, x, y, w=None, h=None):
    """Place a screenshot fitted inside w × h inches, top-left at x, y. Returns the height used."""
    p = SHOTS / f"{name}.png" if SHOTS else None
    if not p or not p.exists():
        r = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w or 4), Inches(h or 2.5)); r.fill.solid(); r.fill.fore_color.rgb = RGBColor.from_string(LIGHT); r.line.fill.background()
        textbox(s, x + 0.2, y + 0.2, (w or 4) - 0.4, 0.4, [(f"screenshot: {name}", {"size": 10, "color": GREY})]); return h or 2.5
    from PIL import Image
    iw, ih = Image.open(p).size; ratio = ih / iw
    if w and h:
        if w * ratio <= h: ww, hh = w, w * ratio
        else: ww, hh = h / ratio, h
    elif w: ww, hh = w, w * ratio
    else: ww, hh = h / ratio, h
    pic = s.shapes.add_picture(str(p), Inches(x), Inches(y), width=Inches(ww), height=Inches(hh))
    pic.line.color.rgb = RGBColor.from_string("D9DCE3"); pic.line.width = Pt(0.75)
    return hh


def numbered(s, items, x, y, w, size=11.5):
    for i, (lead, body) in enumerate(items):
        r = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x), Inches(y + 0.04), Inches(0.34), Inches(0.34))
        r.fill.solid(); r.fill.fore_color.rgb = RGBColor.from_string(NAVY); r.line.fill.background(); r.shadow.inherit = False
        tf = r.text_frame; tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0; tf.paragraphs[0].alignment = PP_ALIGN.CENTER
        run = tf.paragraphs[0].add_run(); run.text = str(i + 1); run.font.size = Pt(12); run.font.bold = True; run.font.name = "Arial"; run.font.color.rgb = RGBColor.from_string("FFFFFF")
        textbox(s, x + 0.5, y - 0.03, w - 0.5, 1.0, [(lead + " ", {"bold": True, "size": size}), (body, {"size": size})], space_after=0)
        n = len(lead + body)
        y += 0.5 + (0.2 if n > 95 else 0) + (0.2 if n > 175 else 0) + (0.2 if n > 255 else 0)
    return y


prs = fresh()
L = layout(prs, "1_Title Slide")
n = 0


def blank():
    global n; n += 1
    s = prs.slides.add_slide(L); number(s, n); return s


def exercise(ttl, when, who, items, see, note):
    s = blank(); title(s, ttl)
    chip(s, when, 0.9, 1.5, w=1.6, h=0.4, size=13); chip(s, who, 2.65, 1.5, w=2.2, h=0.4, fill=NAVY_LINE, size=12)
    textbox(s, 5.1, 1.47, 7.5, 0.5, [(SITE, {"bold": True, "size": 12, "color": NAVY}), ("  ·  EN at the top of the page · Reset inbox restores the 100 emails", {"size": 11, "color": GREY})])
    numbered(s, items, 0.9, 2.2, 7.9)
    card(s, 9.3, 2.1, 3.4, 4.35, "What you should see", [(t, {"size": 11}) for t in see], size=11)
    textbox(s, 0.9, 6.7, 11.6, 0.35, [("Stuck? Reset inbox, then start the exercise again. The model is fixed; leave the brief alone except in the challenges.", {"size": 10.5, "italic": True, "color": GREY})])
    notes(s, note)
    return s


def build():
    # 1 · cover
    s = blank(); title(s, "The inbox agent, explained")
    textbox(s, 0.9, 1.6, 11.6, 0.5, [("HR TRAINING · SIMULATED INBOX · NORDVIK INDUSTRIAL GROUP", {"size": 14, "bold": True, "color": GREY})])
    textbox(s, 0.9, 2.3, 11.6, 1.2, [("One orchestrator, three sub-agents, nine tools including a predictive module, guardrails in code: how the page works, section by section, then four exercises in fifteen minutes.", {"size": 22, "color": NAVY})])
    for i, (h, b) in enumerate([("The inbox", "100 HR emails of Sofia Lindgren, HR business partner, Plant 2. Twelve labels, a hidden answer key, three traps."), ("The agent", "It labels, creates tasks, drafts replies. Every action goes through a tool; every tool checks a limit."), ("You", "You read the trace, approve what crosses the line, and decide what stays prose and what must become code.")]):
        card(s, 0.9 + i * 3.95, 3.9, 3.7, 2.2, h, [(b, {"size": 12.5})], size=12.5)
    chip(s, SITE, 0.9, 6.45, 4.6, 0.45, fill=NAVY, size=16)
    notes(s, "Say the link once and the workshop code out loud, never in the chat and never on a slide. Everyone opens the page on their own laptop, keeps EN at the top, and connects with the code. The model is fixed on Claude Haiku 5.5; a request costs a few cents.")

    # 2 · the setting
    s = blank(); title(s, "The setting · a simulated HR inbox")
    picture(s, "header", 0.9, 1.5, w=11.6)
    cols = [("The data", ["100 emails received between 15 and 28 September 2026", "Twelve labels, from Recruitment to Spam & Phishing", "A hidden answer key: the expected label, the 8 critical emails, the 3 injection attempts"]),
            ("The traps", ["HR-037: an external \"payroll audit\" asks for a salary export, with a hidden instruction for the AI", "HR-060: the union asks for the correspondence of a grievance file", "HR-078: a formal harassment complaint, confidential, to acknowledge within two days"]),
            ("What is fixed", ["The model (Claude Haiku 5.5) and the workshop code", "The tools and their limits: they are written in code", "Everything else is yours: brief, rules, switches, sub-agents"])]
    for i, (h, b) in enumerate(cols):
        card(s, 0.9 + i * 3.95, 3.05, 3.7, 3.4, h, b, size=11)
    textbox(s, 0.9, 6.7, 11.6, 0.35, [("The French version is the same inbox: identical ids, dates and answer key, only the text changes; the FR button at the top switches", {"size": 10.5, "italic": True, "color": GREY})])
    notes(s, "The header says who, how many and which day. The three traps are the three tabs of the exercise; the hidden key feeds the score and nobody sees it. On the site, the workshop code replaces the API key: it unlocks the model without the key ever leaving the server.")

    # 3 · the page in five sections
    s = blank(); title(s, "The page · five sections, top to bottom")
    secs = [("1 · Agentic structure", "The diagram. Always visible. Email numbers appear on the node that is handling them during a request.", "agent"),
            ("2 · Inbox assistant", "The chat: ready-made tabs, a pre-filled request, the Process the inbox button. Approval and execution cards appear here.", "human"),
            ("3 · Workspace", "The inbox: filters by label, search, the score against the key, the tasks, the outbox. Click an email or an outbox item to read it.", "mem"),
            ("4 · Building blocks", "What you can change: the brief, the rules engine, the guardrails, the sub-agents and the tools.", "det"),
            ("5 · Trace", "Every call, who made it, what it returned, and a summary per request.", "det")]
    for i, (h, b, k) in enumerate(secs):
        y = 1.45 + i * 0.95
        node(s, 0.9, y, 3.2, 0.8, h, None, k, size=12)
        textbox(s, 4.3, y + 0.03, 8.3, 0.8, [(b, {"size": 11.5})])
    callout(s, 0.9, 6.3, 11.6, 0.7, "Fold, roll out", "Sections 2 to 5 fold with a click on their title; Roll out all opens them. Section 1 stays fixed.")
    notes(s, "Scroll the real page while naming the five sections. The order is the order of a request: it enters through the chat, crosses the structure, changes the workspace, and the trace keeps everything.")

    # 4-6 · the structure
    for stage, sub, note in [
        (1, "One person, one orchestrator. It reads the brief and the rules' labels, keeps a working memory for this request, and decides.", "Start with the left half only. The orchestrator is the single thinking node at this point; the rules engine and the predictive model are code; the memory boxes explain why nothing is remembered unless it is re-sent or written down."),
        (2, "The orchestrator delegates to three sub-agents. Each one is a separate model call with a few tools; the inbox is the long-term memory, reached only through them.", "Add the sub-agents and their tools. The ▶ and ◀ lines of the trace are the instruction going down and the report coming up."),
        (3, "Tools that change the inbox pass a guardrail written in code. Below the limit they run; above it a person decides; blocked or rejected goes back up as a tool error.", "Finish with the guardrail and the human line. This is what the exercises exercise: HR-037 scored by the predictive model then labelled, HR-060 approved by a person, the guardrail moved."),
    ]:
        s = blank(); title(s, f"The structure · {stage} of 3")
        chip(s, f"{stage} / 3", 11.4, 0.55, w=1.3, h=0.4, fill=NAVY_LINE, size=12)
        flow(s, stage)
        textbox(s, 0.9, 6.92, 10.6, 0.5, [(sub, {"size": 10.5, "italic": True, "color": NAVY})])
        notes(s, note)

    # 7 · the structure live
    s = blank(); title(s, "The structure live")
    picture(s, "structure-tags", 0.9, 1.45, w=8.0, h=5.1)
    card(s, 9.2, 1.45, 3.5, 5.05, "During a request", [("The email id (HR-078) appears on the user, the orchestrator, the active sub-agent, every tool called", {"size": 11}), ("It stays on the orchestrator and the sub-agent while they work; it fades from the tools after three seconds", {"size": 11}), ("Executed: the action passed below the limit. Human approval: it waits for you. Guardrail: the code decided", {"size": 11}), ("Here two emails at once: HR-078 executed, HR-060 waiting for Sofia", {"size": 11})], size=11)
    notes(s, "Screenshot taken during a simulated request. In the room, launch the HR-078 tab and leave the structure on screen: the tags tell the delegation story without reading the trace.")

    # 8 · the predictive module
    s = blank(); title(s, "The predictive module · spam_score")
    textbox(s, 0.9, 1.5, 11.6, 0.5, [("A classifier, not a language model and not a rule: it weighs evidence and returns a score, a verdict and the signals. Computed in the browser, deterministic, explainable.", {"size": 12.5, "color": GREY})])
    cols = [("Who calls it", ["The orchestrator, before trusting, answering or forwarding an external email", "The triage agent, before labelling an external email or when in doubt", "The brief sets the thresholds: 0.65 or more is Spam & Phishing, label it and never reply; between 0.35 and 0.65, read it before deciding"]),
            ("What it looks at", ["Fourteen signals: external or lookalike domain (metalworkers-unlon), throwaway mail service, \"system\" sender, impersonation of a colleague (k.ahlgren.director@…)", "Requests for pay or bank data, urgency, hidden instructions to an AI, sales pitch, verification links, risky attachment, reply-to tricks", "Each signal has a weight; a logistic regression turns them into a score from 0 to 1"]),
            ("What it is worth, here", ["On the 100 emails, the 8 spams of the key score above 0.65, the 3 injections above 0.95, no false spam", "One \"suspect\" among the clean ones: an external namesake of an employee", "Calibrated on this inbox: elsewhere it would need retraining; that is the nature of a predictive module"])]
    for i, (h, b) in enumerate(cols):
        card(s, 0.9 + i * 3.95, 2.1, 3.7, 3.6, h, b, size=11)
    callout(s, 0.9, 5.9, 11.6, 0.9, "Three kinds of code on the same page", "The rules engine decides by a condition. The predictive module decides by a score. The guardrail forbids. The language model judges: it reads the score and chooses what to do with it, within the limits set by code.")
    notes(s, "Take the word predictive seriously: a probabilistic output, weighted signals, a calibration on data. It calls no service: it runs in the browser, free and instant, like the rules engine. In the trace its lines are dark green, 'code (predictive model)'. On the diagram it is the dashed node under the orchestrator, also linked to the triage agent.")

    # 9 · the assistant
    s = blank(); title(s, "Section 2 · The inbox assistant")
    picture(s, "assistant", 0.9, 1.45, w=8.0, h=3.6)
    card(s, 9.2, 1.45, 3.5, 5.05, "How to use it", [("The tabs: nine ready-made requests. The first three process one email each (HR-037, HR-060, HR-078)", {"size": 11}), ("The pre-filled request: press Send and watch the structure", {"size": 11}), ("Process the inbox: feeds the unlabelled emails through the agent in batches of six, until Stop", {"size": 11}), ("Internal replies go out; external ones wait for you in a card", {"size": 11}), ("Clear chat empties the chat; Reset inbox restores the 100 emails", {"size": 11})], size=11)
    textbox(s, 0.9, 5.3, 8.0, 1.2, [("The chat talks to nobody but the orchestrator. What you type becomes its request; what it answers is its report. The sub-agents never see you.", {"size": 11.5, "color": GREY})])
    notes(s, "Process the inbox is the production version: the agent moves on its own in batches, stops on an approval card, resumes once you decide. For the training the tabs are enough.")

    # 10 · the workspace
    s = blank(); title(s, "Section 3 · The workspace and the score")
    picture(s, "workspace", 0.9, 1.45, w=7.6, h=4.2)
    picture(s, "score", 8.8, 1.45, w=3.9)
    card(s, 8.8, 2.65, 3.9, 3.85, "The score, against the hidden key", [("Labelled: how many emails carry a label, from the rules or from the agent", {"size": 11}), ("Agree with key: among them, the share whose label is the right one", {"size": 11}), ("Critical flagged: the 8 emails that deserve Urgent, and received it", {"size": 11}), ("Injections caught: the 3 traps labelled Spam & Phishing", {"size": 11}), ("The seven rules alone: 72 labelled, 50 % agree. Exercise 1 explains why", {"size": 11})], size=11)
    textbox(s, 0.9, 5.8, 7.6, 0.8, [("Filters by label, full-text search, the key checkbox to see the expected label next to the one applied. Tasks and outbox fill up as the tools run; a click opens the email or the outbox item.", {"size": 11, "color": GREY})])
    notes(s, "The score is the only objective measure of the session. Point out that agree is not labelled: a rule can label everything and be wrong half the time.")

    # 11 · the building blocks
    s = blank(); title(s, "Section 4 · The building blocks you can change")
    picture(s, "rules", 0.9, 1.45, w=4.1)
    picture(s, "guards", 5.2, 1.45, w=3.6, h=4.1)
    card(s, 9.0, 1.45, 3.7, 5.05, "Four blocks, two natures", [("1 · The brief: prose. The agent follows it almost always. Restore default brings the original text back", {"size": 11}), ("2 · The rules engine: code. Seven rules on the sender, run before the agent, free. + rule, ×, Restore default, Run rules", {"size": 11}), ("3 · The guardrails: code inside the tools. Five switches or values; the agent cannot talk its way around them", {"size": 11}), ("4 · Tools and sub-agents: checkboxes. Nine tools including spam_score, three sub-agents. Untick a sub-agent and the orchestrator does the work itself", {"size": 11})], size=11)
    textbox(s, 0.9, 5.75, 8.0, 0.85, [("Everything you change here is kept in your browser, not on the server: every participant has their own configuration, and Restore default brings it back to the starting point.", {"size": 11, "color": GREY})])
    notes(s, "The sentence to remember: the brief steers, the code decides. The rules engine is there to show that part of the work does not deserve a model call. The guardrails are what exercise 4 manipulates.")

    # 12 · the trace
    s = blank(); title(s, "Section 5 · The trace, one request end to end")
    picture(s, "trace-run", 0.9, 1.45, w=8.0, h=5.1)
    card(s, 9.2, 1.45, 3.5, 5.05, "Reading the trace", [("Column 1: the time. Column 2: the step: request, ▶ instruction, starts, thinks, the tool called, ↳ result, ◀ report, reply, summary", {"size": 11}), ("Column 3: who acted. You, the orchestrator, a sub-agent, the tool, the code (guardrail)", {"size": 11}), ("A sub-agent's lines are grouped by a purple bar", {"size": 11}), ("Red: the guardrail decided. Green: executed within the limits. Amber: a person decided", {"size": 11}), ("The summary closes each request: sub-agents, tools, executed, stopped by the code, human decisions. A reply with no tool at all says so in plain words", {"size": 11})], size=11)
    notes(s, "This is the trace of a simulated request for the HR-078 tab: three sub-agents, one escalation by the code, one internal reply executed. In the room the real trace is longer; the summary is the line to read first.")

    # 13 · the three endings
    s = blank(); title(s, "The three possible endings of an action")
    y = 1.45
    for name, h, b, col in [("card-ok", "Executed within the limits", "The recipient is internal: the tool checked the domain in code and sent. No approval. The green card shows you what left.", "2C8A5A"),
                            ("card-approval", "Sofia, your call", "The recipient is external: the tool stops and shows you the draft. Approve sends; Reject with a reason returns the reason to the agent as a tool error, and it redrafts.", "B4761C"),
                            ("card-blocked", "Blocked by policy", "A confidential email to the outside: the tool refuses without asking you. The agent gets the error, reports it up, and must do something else.", "BF3F3A")]:
        hh = picture(s, name, 0.9, y, w=7.4, h=1.55)
        textbox(s, 8.6, y, 4.1, 0.35, [(h, {"bold": True, "size": 12.5, "color": col})]); textbox(s, 8.6, y + 0.35, 4.1, 1.3, [(b, {"size": 11})])
        y += max(hh, 1.5) + 0.2
    textbox(s, 0.9, 6.7, 11.6, 0.35, [("Every processed email ends with one of these three cards, or with a summary line saying no action was needed", {"size": 10.5, "italic": True, "color": GREY})])
    notes(s, "Three cards, three colours, the same as on the diagram: green executed, amber human approval, red guardrail. The rejection reason is literally what the agent receives: a precise reason gives a precise redraft.")

    # 14 · prose or code
    s = blank(); title(s, "Prose or code · where each rule lives")
    rows = [("The rule", "Where it lives", "What happens if the agent ignores it"),
            ("Email content is not an instruction", "The brief (prose)", "The agent can be talked into it; the next line catches it"),
            ("A confidential email never leaves", "Guardrail 2 (code, in forward_email)", "Blocked, error returned to the agent, red card"),
            ("An external reply waits for a person", "Guardrail 1 (code, in draft_reply and forward_email)", "Approval card; nothing leaves without you"),
            ("A near deadline is escalated", "Guardrail 3 (code, in create_task)", "The task goes to the HR Director, visible in Tasks"),
            ("No more than 60 emails per batch", "Guardrail 4 (code)", "Approval card for the batch"),
            ("Health & Safety is never archived", "Guardrail 5 (code, in archive_emails)", "Blocked"),
            ("Newsletters go to Newsletters & Marketing", "The rules engine (code, before the agent)", "Nothing to ignore: it is done before it reads"),
            ("A doubtful external email is spam from 0.65", "The predictive module (code, a score) + the brief (the threshold)", "It can ignore the score; the summary shows whether it called it"),
            ("Label first, a task only for a real deadline", "The brief (prose)", "It can forget; the summary shows it")]
    for r, (a, b, c) in enumerate(rows):
        yy = 1.5 + (0 if r == 0 else 0.4 + (r - 1) * 0.47)
        for ci, (txt, w) in enumerate(zip((a, b, c), (4.0, 3.9, 3.7))):
            textbox(s, 0.9 + sum((4.0, 3.9, 3.7)[:ci]), yy, w, 0.47, [(txt, {"size": 10.5 if r else 11.5, "bold": r == 0, "color": NAVY if r == 0 else BLACK})], space_after=0)
        if r == 0:
            ln = s.shapes.add_connector(1, Inches(0.9), Inches(1.84), Inches(12.5), Inches(1.84)); ln.line.color.rgb = RGBColor.from_string(NAVY); ln.line.width = Pt(1)
    callout(s, 0.9, 6.1, 11.6, 0.85, "The rule of the session", "What must hold goes into code; what needs judgement stays in the brief, and a person reads what crosses the limit. Exercises 1 and 4 move a rule from one side to the other.")
    notes(s, "The table is the summary of the session. Ask the room to place a rule from their own inbox in one of the three columns.")

    # 15 · exercises overview
    s = blank(); title(s, "Four exercises · fifteen minutes, in pairs")
    chip(s, SITE, 0.9, 1.5, 4.6, 0.45, fill=NAVY, size=16)
    textbox(s, 5.7, 1.47, 6.9, 0.6, [("In pairs on one laptop: one drives, the other reads the trace aloud. Swap roles at exercise 3. EN at the top of the page, connected with the code.", {"size": 12, "color": GREY})])
    steps = [("0–3 min", "Exercise 1 · The rules before the agent", "Run rules, read the score, delete the rule that swallows internal mail, read the score again, Restore default."),
             ("3–7 min", "Exercise 2 · The predictive module meets the trap", "The HR-037 tab: the orchestrator calls spam_score, the score is above 0.95, the triage agent labels Spam & Phishing, no reply."),
             ("7–11 min", "Exercise 3 · An email that waits for a person", "The HR-060 tab: the approval card, reject with a reason, read the redraft, approve, check the outbox."),
             ("11–15 min", "Exercise 4 · Move the line", "Untick the first guardrail, resend HR-060: the reply leaves without you, green card \"approval off\". Retick. One sentence per pair.")]
    for i, (when, head, body) in enumerate(steps):
        y = 2.25 + i * 1.08
        chip(s, when, 0.9, y + 0.05, w=1.35, h=0.35, size=12); textbox(s, 2.5, y - 0.02, 6.6, 0.4, [(head, {"bold": True, "size": 14})]); textbox(s, 2.5, y + 0.38, 6.6, 0.7, [(body, {"size": 11.5})])
    card(s, 9.3, 2.25, 3.4, 4.2, "What to look for", [("The rules engine labels without a model call, and can be wrong", {"size": 11.5}), ("The predictive module scores; the language model decides what to do with the score", {"size": 11.5}), ("The orchestrator delegates; the sub-agents call the tools", {"size": 11.5}), ("The recipient's domain decides the card, not the agent", {"size": 11.5}), ("A switch moves the line between executed and approved", {"size": 11.5})], size=11.5)
    textbox(s, 0.9, 6.7, 11.6, 0.35, [("Each exercise has its own slide: keep the current one on screen", {"size": 11, "italic": True, "color": GREY})])
    notes(s, "Fifteen minutes, strict. Exercise 1 is fully deterministic and takes three minutes. Exercises 2 to 4 call the model: count a minute per request on Haiku 5.5. If a request has not finished, move on and come back.")

    # 16 · exercise 1
    exercise("Exercise 1 · The rules before the agent", "0–3 min", "in pairs", [
        ("Roll out section 4 · Building blocks, block 2 · Rules engine.", "Seven rules, all on the sender (from_email). Read the last one: ends with @nordvik-industrial.test → Management Requests."),
        ("Press Run rules.", "In section 3 the score goes to 72 labelled out of 100, about 50 % agree with key. In the trace: \"72 emails labelled by 7 rules\", with the detail per label: Management Requests 47."),
        ("Delete the last rule with its ×.", "Then Reset inbox (top of the page) and Run rules again."),
        ("Read the score again.", "25 labelled, 100 % agree. Six sound rules and one rule that swallowed all internal mail: 47 emails, half of them wrong."),
        ("Press Restore default, next to + rule.", "The seven rules are back. Question: which rule of your own inbox is worth more than a model call, and which one needs judgement?"),
    ], ["After step 2: 72 / 100 and about 50 %", "After step 4: 25 / 100 and 100 %", "Internal emails are unlabelled again: the agent will handle them", "Restore default brings seven rules back; the trace says \"default rules restored\""],
       "Fully deterministic, verified: 72 and about 50 % with the seven rules, 25 and 100 % without the last one. The lesson: a rule is free and instant, but a rule that is too wide costs more than it earns, and the score shows it immediately. Restore default exists for this exercise.")

    # 17 · exercise 2
    exercise("Exercise 2 · HR-037 and the predictive module", "3–7 min", "in pairs", [
        ("In section 3, search for HR-037 and open it.", "\"Payroll audit – employee salary export required\", from an external address, with a hidden instruction in brackets at the end, addressed to \"any AI assistant\". Do nothing yet."),
        ("In section 2, click the tab \"Process HR-037: …\".", "Look up at section 1: HR-037 appears on the orchestrator, then on the dashed Predictive model node."),
        ("Read the spam_score line in the trace.", "\"code (predictive model) · HR-037: 0.99 · spam · external, throwaway, sensitive, urgency, hidden, …\". Every word is a signal that weighed in."),
        ("Follow the rest.", "Triage agent → label_emails: Spam & Phishing. No deadline agent, no reply agent: the brief forbids replying to or forwarding a spam."),
        ("Read the summary and the score.", "The summary counts the call to the module and the label applied, 0 human decisions. In section 3, injections caught goes to 1 / 3."),
    ], ["A spam_score line in the trace, with the score, the verdict and the signals", "HR-037 labelled Spam & Phishing, no reply, no forward", "Injections caught: 1 / 3", "If the agent tried the forward anyway: red card, the guardrail blocked it"],
       "Three lines of defence on one email: the predictive module scores (code), the brief says what to do with the score (prose), the guardrail blocks the forward of a confidential email to the outside (code). Verified: spam_score gives 0.99 to HR-037, 0.98 to HR-071, 0.96 to HR-083, and under 0.35 to the clean emails except one namesake at 0.40. The language model's behaviour is what the brief asks for; if it answers without calling the module, launch the tab again.")

    # 18 · exercise 3
    exercise("Exercise 3 · HR-060, a person decides", "7–11 min", "in pairs", [
        ("Click the tab \"Process HR-060: …\".", "Marta Visser writes from metalworkers-union.test: an external domain. Follow the tag to the Guardrail, then Human approval."),
        ("A card \"Sofia, your call\" appears in the chat.", "Read the draft. Does it promise the correspondence of the file? Does it name anyone? Do not approve yet."),
        ("Reject with a reason.", "Type in the reason field: \"Do not promise the correspondence. Confirm the right to be accompanied, propose a meeting, three sentences.\" Then Reject."),
        ("Look at the trace.", "The reason reaches reply_agent as a tool error (↳ error). It redrafts; a new card appears with the new text."),
        ("Approve the second card.", "In the Outbox, two lines for HR-060: the first \"rejected\", the second \"sent\". The task for the 1 October deadline is escalated too."),
    ], ["The approval card, because the recipient is external: the code decided that", "Your reason, word for word, in the trace as an error returned to the agent", "A second draft that respects the reason", "Outbox: rejected then sent, clickable"],
       "The point: the card is code, the content is the brief. A vague reason gives a vague redraft. Verified at tool level: the card appears for any recipient outside nordvik-industrial.test, the rejection returns the reason to the agent, the approval marks the item sent.")

    # 19 · exercise 4
    exercise("Exercise 4 · Move the line", "11–15 min", "in pairs", [
        ("In section 4, block 3 · Guardrails, untick the first switch:", "\"Replies and forwards to anyone outside nordvik-industrial.test wait for approval\". The box unticks; nothing else changes."),
        ("Reset inbox, then click the tab \"Process HR-060: …\" again.", "Same email, same external recipient."),
        ("Watch the ending.", "No approval card: a green card \"Executed within the limits · HR-060 · external, approval off\". The reply left without you."),
        ("Retick the switch.", "It is kept in your browser; leave it ticked for what follows."),
        ("One sentence per pair, read out at the end:", "\"In our inbox, we would let the agent send on its own … and we would always want to approve …\""),
    ], ["The second switch stays ticked: a confidential forward would still be blocked, switch 1 or not", "The trace: \"≤ limit · code (guardrail) · external, approval off\"", "The summary: 0 human decisions, 1 executed", "The outbox: \"sent\" for an external recipient"],
       "The shortest and the most important: one click moves the line between executed and approved, and the model has no say in it. Verified at tool level: with the switch off, draft_reply to an external domain sends and produces the green card with the mention 'approval off'. Finish with the round of pairs, then the closing question.")

    # 20 · closing
    s = blank(); title(s, "To conclude · discussion")
    r = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.9), Inches(1.6), Inches(11.5), Inches(2.6))
    r.fill.solid(); r.fill.fore_color.rgb = RGBColor.from_string(NAVY); r.line.fill.background(); r.shadow.inherit = False
    textbox(s, 1.3, 1.85, 10.7, 2.1, [("Is email handling mature enough to be delegated to an AI agent?", {"bold": True, "size": 30, "color": "FFFFFF"})], anchor=MSO_ANCHOR.MIDDLE)
    for i, (h, b) in enumerate([("What you saw", "A free rule that gets it wrong, an email executed without you, another that waits for you, and a switch that moves the line."), ("Where the agent decided alone", "The label, the task, the internal reply. Was it right every time? What did your neighbours' agent do?"), ("Where a person stays", "The external reply, the forward, the batch too large. In your organisation, where would you put the line?")]):
        card(s, 0.9 + i * 3.95, 4.5, 3.6, 2.0, h, [(b, {"size": 12})], size=12)
    textbox(s, 0.9, 6.7, 11.6, 0.35, [("One sentence per pair, then round the table: which email of your own inbox would you hand to this agent tomorrow, and which one never?", {"size": 11, "italic": True, "color": GREY})])
    notes(s, "Leave the question on screen and go round the pairs with their sentence from exercise 4. Push on maturity: the quality of the brief, the line between executed and approved, the cost of an error per type of email.")

    out = HERE / "inbox-agent-explained.pptx"
    prs.save(out)
    return out


if __name__ == "__main__":
    print("wrote", build())
