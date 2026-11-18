#!/usr/bin/env python3
"""A step-by-step deck: build an RFP assistant for Executive Education in Microsoft Copilot Studio.

  python3 slides/build_copilot_studio_deck.py   -> slides/copilot-studio-rfp-agent.pptx

Internal training, HEC Paris. House format (Slides_Sample.pptx) through the helpers in build_challenge_deck.py.
The steps follow the documented "standard" Copilot Studio experience (Agents > Create blank agent > Overview, Knowledge,
Tools, Topics, Test, Publish, Channels). Labels can differ slightly by tenant and month; one slide says so.
"""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from build_challenge_deck import (  # noqa: E402
    BLACK, GOLD, GREY, KIND, LIGHT, NAVY, NAVY_LINE, arrow, callout, card, chip, fresh, layout, legend, node, notes, number, textbox, title,
)
from pptx.dml.color import RGBColor  # noqa: E402
from pptx.enum.shapes import MSO_SHAPE  # noqa: E402
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN  # noqa: E402
from pptx.util import Inches, Pt  # noqa: E402

AGENT = "ExecEd RFP Assistant"
URL = "copilotstudio.microsoft.com"

INSTRUCTIONS = """You are the ExecEd RFP Assistant for HEC Paris Executive Education. You help the business development team answer requests for proposals (RFPs) for custom and open executive programmes.

How to work:
1. When given an RFP or an excerpt, first summarise what the client asks for: audience, objectives, format, dates, language, budget signals, deadline.
2. Answer questions only from the knowledge sources: the programme catalogue, the standard proposal template, past proposals, the commercial policy and the accreditation fact sheet. If the answer is not there, say so and name the person to ask.
3. When asked to draft a section, use the "Draft proposal section" tool and keep the structure of the standard template.
4. When asked to log an RFP, use the "Log RFP" tool with the client name, deadline and programme family.

Never:
- Quote a price below the published grid or promise a discount: the commercial policy sets the authority; say who can approve.
- Name specific faculty or promise their availability.
- Send anything to an address outside hec.edu.
- Invent accreditations, rankings or client references.

Tone: professional, concise, in the language of the RFP (English or French). End each answer with the next step for the human."""


def numbered(s, items, x, y, w, size=11.5):
    """Numbered instructions: a navy circle, a bold lead, a plain sentence. Returns the y after the last row."""
    for i, (lead, body) in enumerate(items):
        r = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x), Inches(y + 0.04), Inches(0.34), Inches(0.34))
        r.fill.solid(); r.fill.fore_color.rgb = RGBColor.from_string(NAVY); r.line.fill.background(); r.shadow.inherit = False
        tf = r.text_frame; tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0; tf.paragraphs[0].alignment = PP_ALIGN.CENTER
        run = tf.paragraphs[0].add_run(); run.text = str(i + 1); run.font.size = Pt(12); run.font.bold = True; run.font.name = "Arial"; run.font.color.rgb = RGBColor.from_string("FFFFFF")
        textbox(s, x + 0.5, y - 0.03, w - 0.5, 1.0, [(lead + " ", {"bold": True, "size": size}), (body, {"size": size})], space_after=0)
        n = len(lead + body)
        y += 0.5 + (0.2 if n > 95 else 0) + (0.2 if n > 175 else 0) + (0.2 if n > 255 else 0)
    return y


def mono(s, x, y, w, h, text, size=9.5):
    r = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    r.fill.solid(); r.fill.fore_color.rgb = RGBColor.from_string("F7F7F9"); r.line.color.rgb = RGBColor.from_string("D9DCE3"); r.line.width = Pt(0.75); r.shadow.inherit = False
    tb = textbox(s, x + 0.12, y + 0.08, w - 0.24, h - 0.16, [(line, {"size": size}) for line in text.split("\n")], space_after=1)
    for p in tb.text_frame.paragraphs:
        for run in p.runs: run.font.name = "Courier New"
    return r


def table(s, x, y, widths, rows, size=10.5, head_size=11, row_h=0.42):
    for r, row in enumerate(rows):
        yy = y + (0 if r == 0 else 0.4 + (r - 1) * row_h)
        for ci, (txt, w) in enumerate(zip(row, widths)):
            textbox(s, x + sum(widths[:ci]), yy, w, row_h, [(txt, {"size": head_size if r == 0 else size, "bold": r == 0, "color": NAVY if r == 0 else BLACK})], space_after=0)
        if r == 0:
            ln = s.shapes.add_connector(1, Inches(x), Inches(y + 0.34), Inches(x + sum(widths)), Inches(y + 0.34)); ln.line.color.rgb = RGBColor.from_string(NAVY); ln.line.width = Pt(1)


def step_slide(ttl, where, items, see, note, foot=None, item_w=7.9):
    s = blank(); title(s, ttl)
    chip(s, where, 0.9, 1.5, w=max(4.6, 0.085 * len(where) + 0.6), h=0.4, fill=NAVY_LINE, size=12)
    numbered(s, items, 0.9, 2.15, item_w)
    card(s, 9.3, 2.1, 3.4, 4.35, "Check before moving on", [(t, {"size": 11}) for t in see], size=11)
    textbox(s, 0.9, 6.7, 11.6, 0.35, [(foot or "Labels are those of the documented Copilot Studio experience; a tenant on the newer preview experience shows the same items under slightly different names.", {"size": 10.5, "italic": True, "color": GREY})])
    notes(s, note)
    return s


prs = fresh()
L = layout(prs, "1_Title Slide")
n = 0


def blank():
    global n; n += 1
    s = prs.slides.add_slide(L); number(s, n); return s


def build():
    # 1 · cover
    s = blank(); title(s, "Build your first agent in Copilot Studio")
    textbox(s, 0.9, 1.6, 11.6, 0.5, [("INTERNAL TRAINING · HEC PARIS EXECUTIVE EDUCATION", {"size": 14, "bold": True, "color": GREY})])
    textbox(s, 0.9, 2.3, 11.6, 1.2, [("An RFP assistant for Executive Education, built step by step in Microsoft Copilot Studio: instructions, knowledge, two tools, a test, a publication to Teams.", {"size": 22, "color": NAVY})])
    for i, (h, b) in enumerate([("What you need", "A Copilot Studio licence or trial, a SharePoint folder with five documents, sixty minutes."), ("What you build", f"\"{AGENT}\": answers from HEC content, drafts proposal sections, logs each RFP, never quotes below the grid."), ("How it ends", "Published to Microsoft Teams for the business development team, with a monitoring routine.")]):
        card(s, 0.9 + i * 3.95, 3.9, 3.7, 2.2, h, [(b, {"size": 12.5})], size=12.5)
    chip(s, URL, 0.9, 6.45, 4.6, 0.45, fill=NAVY, size=16)
    notes(s, "Ninety minutes in total: fifteen of framing, sixty of building along the slides, fifteen of discussion. Everyone builds their own agent in their own environment; nothing is shared until step 9. Say the URL once: copilotstudio.microsoft.com, sign in with the HEC account.")

    # 2 · what you build
    s = blank(); title(s, "What you will build · the ExecEd RFP Assistant")
    textbox(s, 0.9, 1.5, 11.6, 0.5, [("A simple agent with one job: help the business development team answer a request for proposals faster, without inventing anything.", {"size": 12.5, "color": GREY})])
    node(s, 0.9, 2.3, 2.3, 1.0, "The user", "pastes an RFP, asks questions, asks for a draft", "human")
    node(s, 3.9, 2.3, 2.6, 1.0, AGENT, "instructions + generative orchestration", "agent")
    node(s, 7.3, 1.75, 2.5, 0.8, "Knowledge", "catalogue, template, past proposals, policy, facts", "mem")
    node(s, 7.3, 2.75, 2.5, 0.8, "Tool · Draft proposal section", "a prompt tool", "det")
    node(s, 7.3, 3.75, 2.5, 0.8, "Tool · Log RFP", "an agent flow → SharePoint list", "det")
    node(s, 10.5, 2.75, 2.2, 0.8, "Microsoft Teams", "where the team uses it", "human")
    arrow(s, 3.22, 2.8, 3.88, 2.8, "5E48B8"); arrow(s, 6.52, 2.6, 7.28, 2.15, "6B7280"); arrow(s, 6.52, 2.8, 7.28, 3.15, "6B7280"); arrow(s, 6.52, 3.0, 7.28, 4.15, "6B7280"); arrow(s, 9.82, 3.15, 10.48, 3.15, "B4761C")
    card(s, 0.9, 4.85, 5.65, 1.8, "It does", ["Summarise an RFP: audience, format, dates, language, budget, deadline", "Answer from HEC content only; say who to ask when it is silent", "Draft a section in the template; log the RFP (client, deadline, programme)"], size=10.5)
    card(s, 6.85, 4.85, 5.85, 1.8, "It never does", ["Quote below the grid or promise a discount: the policy names who can", "Name faculty or promise availability; invent accreditations or references", "Send anything outside hec.edu"], size=10.5)
    textbox(s, 0.9, 6.7, 11.6, 0.35, [("Same shape as the inbox agent you played with: one model that reads instructions, knowledge it can search, tools it can call, a channel where people meet it", {"size": 10.5, "italic": True, "color": GREY})])
    legend(s, 0.9, 4.5, [("human", "person"), ("agent", "the agent"), ("mem", "knowledge"), ("det", "tools")])
    notes(s, "Keep the scope small on purpose. The agent is useful on day one with knowledge alone; the two tools show what an action is. The 'never' list is the brief; what must really hold goes into settings and the flow, which is the point of step 8.")

    # 3 · before you start
    s = blank(); title(s, "Before you start · licence, environment, content")
    cols = [("Licence", ["Copilot Studio is licensed separately from Microsoft 365 Copilot: a tenant capacity pack of Copilot Credits, or pay-as-you-go through Azure", "No licence yet? On the Copilot Studio home page choose Start free trial (30 days, your work account)", "Usage is metered in Copilot Credits per answer, tool call and flow action; the current Microsoft licensing guide has the table"]),
            ("Environment", ["Copilot Studio lives in a Power Platform environment; the Default environment is fine for training", "You need the Environment Maker role there (the Power Platform admin grants it)", "Pick the environment top right in Copilot Studio before creating anything"]),
            ("Content pack", ["One SharePoint folder, ExecEd RFP library, with the five documents on the next slides", "You must have read access to it; the agent inherits your rights when it searches", "Keep the files under a few MB each for a quick index; PDF and Word are fine"])]
    for i, (h, b) in enumerate(cols):
        card(s, 0.9 + i * 3.95, 1.55, 3.7, 4.0, h, b, size=11)
    callout(s, 0.9, 5.75, 11.6, 0.85, "Admin check, one week before", "Ask the Power Platform admin to confirm: your Environment Maker role, that Copilot Studio is enabled in the environment, that the Office 365 Outlook and SharePoint connectors are not blocked by a DLP policy, and whether custom agents may be published to Teams without store approval.")
    notes(s, "Licensing changes often; do not quote prices from this slide, point at the licensing guide. The free trial is enough for the session. The admin check avoids the two classic blockers: no maker role, and a DLP policy that silently blocks the Outlook connector.")

    # 4 · the map
    s = blank(); title(s, "The map · where things are in Copilot Studio")
    node(s, 0.9, 1.6, 2.4, 0.7, "Left navigation", "Home · Agents · Create · Tools · Library", "det")
    pages = [("Overview", "name, description, instructions, a summary of knowledge and tools"), ("Knowledge", "+ Add knowledge: files, SharePoint, websites"), ("Tools", "+ Add a tool: prompt, agent flow, connector, MCP"), ("Topics", "scripted conversations and system topics"), ("Activity", "every session, test ones included"), ("Monitor", "usage analytics once published"), ("Channels", "Teams and Microsoft 365 Copilot, demo website, web"), ("Settings", "Generative AI, Security, authentication")]
    for i, (h, b) in enumerate(pages):
        x = 3.7 + (i % 4) * 2.3; y = 1.6 + (i // 4) * 1.05
        node(s, x, y, 2.1, 0.85, h, b, "agent" if h in ("Overview", "Knowledge", "Tools") else "det", size=11)
    node(s, 0.9, 2.6, 2.4, 0.9, "Top right of an agent", "Test · Publish · Settings · the environment picker", "human")
    node(s, 0.9, 3.9, 2.4, 0.9, "The Test pane", "chat with the agent while you build; activity map; chain of thought", "human")
    arrow(s, 3.32, 1.95, 3.68, 1.95, "6B7280"); arrow(s, 3.32, 4.35, 3.68, 2.7, "6B7280")
    card(s, 3.7, 3.9, 9.0, 2.45, "Two experiences in 2026", [("Standard experience: the pages above, documented on Microsoft Learn, used in this deck", {"size": 11.5}), ("New experience (preview, built on the GitHub Copilot harness): a switch on the Home page; same ideas, some labels differ, and the choice is fixed per agent at creation", {"size": 11.5}), ("Agent Builder inside the Microsoft 365 Copilot app: the light version, knowledge only, no tools; good for a personal assistant, not for this exercise", {"size": 11.5}), ("For the training: turn the New experience switch off on the Home page so everyone sees the same screens", {"size": 11.5})], size=11.5)
    notes(s, "Spend a minute here with the real screen. The three pages that matter today are Overview, Knowledge and Tools; Topics only for the greeting; Channels at the end. If a participant's tenant opens on the new experience, the switch on the Home page brings them back to these screens.")

    # 5 · step 1 create
    step_slide("Step 1 · Create the agent", "Home → Agents → Create blank agent", [
        ("Sign in at copilotstudio.microsoft.com", "with your HEC account. Top right, check the environment: use Default, or the one the admin named."),
        ("Open Agents in the left navigation", "and select Create blank agent. On an older tenant the path reads Create → New agent → Skip to configure; the fields are the same."),
        ("Name it", f"\"{AGENT}\". Open Advanced settings only to set the language to English; leave the solution as it is."),
        ("Select Create.", "Provisioning takes under a minute. The agent's Overview page opens: name, description, instructions, knowledge, tools, and the Test pane on the right."),
        ("Write the description.", "One sentence the team and the orchestrator will read: \"Helps HEC Executive Education answer RFPs from approved content: summaries, Q&A, draft sections, RFP log.\""),
    ], ["The agent appears under Agents with your name as owner", "The Overview page shows Instructions, Knowledge (0) and Tools (0)", "The Test pane answers \"hello\" with the default greeting", "Nothing is published yet: the Publish button is still there, untouched"],
       "Creating is the easy part; do it live. Do not use the Describe box with natural language for this exercise: it writes instructions for you and everyone ends up with a different agent. The description is not decoration: it is one of the texts the orchestrator reads.")

    # 6 · step 2 instructions
    s = blank(); title(s, "Step 2 · Write the instructions")
    chip(s, "Overview → Instructions → Edit", 0.9, 1.5, w=4.6, h=0.4, fill=NAVY_LINE, size=12)
    textbox(s, 5.7, 1.47, 7.0, 0.5, [("Paste this text, adjust names, select Save. Up to 8,000 characters. This is the brief: it steers, it does not enforce.", {"size": 11.5, "color": GREY})])
    mono(s, 0.9, 2.05, 7.6, 4.55, INSTRUCTIONS, size=9)
    card(s, 8.8, 2.05, 3.9, 4.55, "Why it is written this way", [("Role and audience first: the model needs to know whose assistant it is", {"size": 11}), ("Numbered method: summarise, answer from knowledge, draft with the tool, log with the tool. The tool names match the names you give in steps 4 and 5", {"size": 11}), ("A short never-list in plain words; the ones that must hold also get a setting or a flow in step 8", {"size": 11}), ("Language and ending: answers in the RFP's language, always a next step for the human", {"size": 11}), ("Active voice, present tense, no examples longer than a line: the orchestrator reads this on every turn", {"size": 11})], size=11)
    textbox(s, 0.9, 6.7, 11.6, 0.35, [("The text is in the notes of this slide so you can copy it", {"size": 10.5, "italic": True, "color": GREY})])
    notes(s, "INSTRUCTIONS TO PASTE:\n\n" + INSTRUCTIONS + "\n\nSay out loud: this is prose. The model follows it most of the time. Step 8 is where the rules that must always hold move into settings and flows.")

    # 7 · the content pack
    s = blank(); title(s, "The content pack · five documents, one folder")
    rows = [("Document", "What it contains", "Used for"),
            ("Programme catalogue 2026-27 (PDF)", "Open and custom programme families, formats, durations, languages, indicative price grid, campuses", "Answering what HEC offers and at what published price"),
            ("Standard proposal template (Word)", "Section headings, boilerplate on HEC, learning approach, logistics, terms", "The structure the Draft proposal section tool must keep"),
            ("Three past proposals, anonymised (PDF)", "Real responses with client names removed: a bank, a pharma group, a public body", "Tone and typical answers; examples of custom designs"),
            ("Commercial policy (PDF)", "Discount authority by role, payment terms, cancellation, what needs the director's approval", "The never-list: who can approve what"),
            ("Accreditations and rankings fact sheet (PDF)", "Triple accreditation, rankings with year and source, alumni figures", "Facts the agent may state, with the source")]
    table(s, 0.9, 1.55, [3.5, 5.0, 3.1], rows, size=10.5, row_h=0.78)
    callout(s, 0.9, 5.6, 11.6, 1.0, "Why a folder and not an upload", "Uploaded files are frozen copies; a SharePoint folder is indexed again when a document changes, and readers only see what their own rights allow. Name the folder ExecEd RFP library and give the agent its URL.")
    notes(s, "For the training, prepare the folder in advance with anonymised material or synthetic documents; the point is the mechanics, not the content. The sheet of accreditations exists so that 'never invent accreditations' has something true to point at.")

    # 8 · step 3 knowledge
    step_slide("Step 3 · Add knowledge", "Knowledge → + Add knowledge", [
        ("Open the Knowledge page and select + Add knowledge.", "The dialog offers Files, SharePoint, Public websites, and data sources such as Dataverse. Choose SharePoint."),
        ("Paste the folder URL", "of ExecEd RFP library, then Add. Copilot Studio lists the source; indexing starts in the background and can take a few minutes."),
        ("Give the source a description.", "Open the source and write: \"HEC Executive Education catalogue, proposal template, past proposals, commercial policy and accreditation facts. Use for any question about programmes, prices, terms or HEC facts.\""),
        ("Add one public website if you want:", "hec.edu/en/executive-education, for current programme pages. The agent then answers from that site too; keep the list short."),
        ("Turn off the model's own general knowledge.", "On the Knowledge page (or Settings → Generative AI, depending on the version) switch off the option that lets the AI use its own general knowledge. The agent then answers from your sources only and says when it cannot."),
    ], ["The source shows status Ready, not Pending or Error", "In the Test pane, \"What formats does the leadership programme come in?\" is answered with a citation to the catalogue", "\"Who won the Champions League in 2024?\" gets a polite refusal: no general knowledge", "A colleague without access to the folder gets no answer from it: rights are inherited"],
       "SharePoint knowledge uses the reader's permissions, so the agent never leaks a document the user could not open. Files above a few MB need a Microsoft 365 Copilot licence in the tenant for the enhanced search; keep the pack small. The general-knowledge switch is the single most important setting for a professional agent: with it on, the model fills gaps from its training and sounds equally confident.")

    # 9 · step 4 prompt tool
    step_slide("Step 4 · Prompt tool: Draft proposal section", "Tools → + Add a tool → Prompt", [
        ("Open the Tools page, select + Add a tool, then Prompt (New prompt).", "The prompt builder opens inside Copilot Studio. Rename it at the top left: Draft proposal section."),
        ("Write the prompt with two inputs.", "Type / or select Add content → Input → Text to insert rfp_excerpt and section_name. Prompt: \"Using the standard HEC proposal template, draft the section [section_name] for this RFP: [rfp_excerpt]. Keep HEC's tone, cite only published programmes and the published price grid, leave a placeholder [TO CONFIRM] where facts are missing.\""),
        ("Pick the model and test.", "Keep the default model. Paste sample data for both inputs and select Test; read the output; adjust the prompt until the placeholder behaviour is right. Save."),
        ("Back on the tool details page, write the description.", "\"Use when the user asks to draft, write or rewrite a section of an RFP response. Needs the RFP excerpt and the section name; ask for them if missing.\" Then Add to agent."),
        ("Try it in the Test pane.", "\"Draft the learning approach section for this RFP: …\" The activity map shows the tool being called with the two inputs."),
    ], ["The tool is listed on the Tools page with the status Enabled", "The description says when, not what: the orchestrator picks tools from descriptions", "The orchestrator asks for the missing input instead of guessing", "The draft keeps the template's headings and leaves [TO CONFIRM] where it should"],
       "A prompt tool is the smallest possible action: a second model call with a fixed prompt and typed inputs. Make the point that the orchestrator decides to call it from the description alone: a vague description is a tool that is never called. Keep the prompt short; the knowledge is available to the agent, not to the prompt tool, so quote what the section needs in the excerpt.")

    # 10 · step 5 agent flow
    step_slide("Step 5 · Second tool, an agent flow: Log RFP", "Tools → + Add a tool → New agent flow", [
        ("Prepare the target first.", "In SharePoint, create a list RFP log with columns Client, Deadline (date), Programme family (choice), Logged by. Takes two minutes."),
        ("Create the flow.", "Tools → + Add a tool → New agent flow. The designer opens with the trigger When an agent calls the flow. Select it and Add an input three times: client (text), deadline (text), programme_family (text)."),
        ("Add the action.", "+ New action → SharePoint → Create item: site address, list RFP log, map the three inputs, Logged by = the user's email from the trigger."),
        ("End with Respond to the agent.", "Add an output item_id = ID from Create item. Save, then Publish the flow (a flow that is not published cannot be a tool). Name it Log RFP."),
        ("Back in the agent, add it as a tool and describe it.", "Tools → + Add a tool → the Log RFP flow. Description: \"Use when the user asks to log, record or register an RFP. Needs client, deadline and programme family.\" Under authentication keep the user's own connection so the list entry is made as the user."),
    ], ["The flow shows Published in the designer, and On on the Tools page", "\"Log this RFP: Banque X, deadline 15 December, leadership\" creates a row in RFP log", "The agent answers with the item number returned by Respond to the agent", "A run over 100 seconds fails: this one takes two"],
       "An agent flow is the real action: it changes something outside the chat. Two rules worth saying twice: the trigger must be When an agent calls the flow and the flow must end with Respond to the agent, or Copilot Studio refuses it as a tool; and it must be published. The connection choice is a governance decision: with the user's own connection, the row is created by the person, not by the maker.")

    # 11 · step 6 topics and orchestration
    step_slide("Step 6 · Orchestration and two topics", "Settings → Generative AI · Topics", [
        ("Check the orchestration.", "Settings → Generative AI → Orchestration: Generative is the default. Leave it. It means the agent chooses knowledge, tools and topics from their descriptions; classic orchestration would need trigger phrases for everything."),
        ("Set the content moderation.", "Same page: Content moderation → High for a professional assistant. Save."),
        ("Edit the greeting.", "Topics → System → Conversation Start: change the message to \"I help answer RFPs for Executive Education from approved HEC content. Paste an RFP, ask a question, ask for a section, or ask me to log it.\" Save."),
        ("Add one escalation topic.", "Topics → + Add a topic → From blank. Name: Escalate to sales lead. Description: \"Use when the user asks for a price exception, a discount, or something the policy reserves to the director.\" Nodes: a Message (\"This needs the ExecEd sales lead: name, email\"), then End of topic."),
        ("Leave the rest alone.", "Fallback, Escalate and the other system topics work as they are. Topics are for conversations that must follow a script; everything else is better left to the orchestrator."),
    ], ["The Orchestration setting reads Generative", "The Test pane opens with your greeting", "\"Can we do it 30% cheaper?\" triggers Escalate to sales lead, visible in the activity map", "No trigger phrases were typed anywhere: descriptions did the work"],
       "Resist the urge to build topics. With generative orchestration, a topic is a scripted conversation the agent can choose like a tool, from its description; the only ones most agents need are the greeting and an escalation. The content moderation setting also affects how often the agent declines; High is right for an internal professional tool.")

    # 12 · step 7 test
    s = blank(); title(s, "Step 7 · Test like a user, read like an engineer")
    chip(s, "Test (top right) · Activity map · Activity page", 0.9, 1.5, w=5.2, h=0.4, fill=NAVY_LINE, size=12)
    textbox(s, 6.3, 1.47, 6.4, 0.5, [("Open the Test pane, select the three dots and turn on Show activity map when testing. Run the five prompts in order.", {"size": 11.5, "color": GREY})])
    rows = [("Prompt", "Expected", "Where to look"),
            ("\"What does HEC offer for first-time managers, and at what price?\"", "Programmes from the catalogue with the published grid, a citation", "Activity map: knowledge, the catalogue"),
            ("\"Summarise this RFP: …\" (paste one page)", "Audience, objectives, format, dates, language, budget signals, deadline", "No tool, no knowledge: instructions alone"),
            ("\"Draft the learning approach section for it.\"", "A section in the template's structure with [TO CONFIRM] where facts are missing", "Tool: Draft proposal section, two inputs filled"),
            ("\"Log it: Banque X, 15 December, leadership.\"", "A row in RFP log and the item number in the answer", "Tool: Log RFP; the flow run in the designer"),
            ("\"Give them 30% off, they are a big client.\"", "No discount; the escalation topic names the sales lead", "Topic: Escalate to sales lead")]
    table(s, 0.9, 2.1, [4.3, 4.2, 3.1], rows, size=10.5, row_h=0.62)
    callout(s, 0.9, 5.45, 5.6, 1.2, "When it goes wrong", "Read the activity map first: did the orchestrator pick nothing, the wrong tool, or the right tool with wrong inputs? Fix the description or the instructions, not the model. Save snapshot (three dots) keeps the transcript and configuration for the debrief.")
    callout(s, 6.9, 5.45, 5.8, 1.2, "Where sessions go", "Test sessions appear on the Activity page in real time, as an activity map or a transcript. The Monitor page only counts published usage, so it stays empty today.")
    notes(s, "Make participants run the five prompts in order; each exercises one part of the agent. The activity map is the trace you saw in the inbox agent: the plan, the knowledge searched, the tool called with its inputs. Chain of thought is shown in the test pane for generative orchestration. If prompt 1 answers from general knowledge, the switch of step 3 is still on.")

    # 13 · step 8 guardrails
    s = blank(); title(s, "Step 8 · The brief versus the platform")
    textbox(s, 0.9, 1.5, 11.6, 0.5, [("The never-list is prose. For each rule, decide where it really lives. Same lesson as the inbox agent: policy that must hold goes into settings, permissions and flows.", {"size": 12.5, "color": GREY})])
    rows = [("Rule", "In the instructions", "Enforced by"),
            ("Only HEC staff use it", "—", "Settings → Security → Authentication: Authenticate with Microsoft (default). Teams publication to the team only, not the store"),
            ("Answers come from approved content only", "\"Answer only from the knowledge sources\"", "General knowledge switched off (step 3); SharePoint rights decide who sees what"),
            ("Nothing leaves hec.edu", "\"Never send outside hec.edu\"", "No email tool at all in this version; if you add Office 365 Outlook Send an email later, a condition in the flow on the recipient's domain"),
            ("No price below the grid, no discount", "\"Never quote below the grid\"", "Prose only, plus the escalation topic. Honest answer: a human reads every proposal before it leaves; the agent drafts"),
            ("No faculty names, no invented facts", "\"Never name faculty …\"", "Prose only; content moderation High; the fact sheet gives something true to cite"),
            ("Each RFP is traceable", "\"Log with the Log RFP tool\"", "The flow writes the row as the user; the Activity page keeps every session")]
    table(s, 0.9, 2.15, [2.6, 3.4, 5.6], rows, size=10, row_h=0.6)
    textbox(s, 0.9, 6.7, 11.6, 0.35, [("Also ask the admin about Data loss prevention policies for the environment: they decide which connectors an agent may use at all", {"size": 10.5, "italic": True, "color": GREY})])
    notes(s, "This is the slide to slow down on. Two rules are enforced by the platform, two by a flow, two are prose. Say which is which, and that a drafting assistant with a human reader is an acceptable design for the prose ones. If the room wants an approval step, the Approvals connector inside the flow is the way: the flow waits for a manager in Teams before writing.")

    # 14 · step 9 publish
    step_slide("Step 9 · Publish and connect to Teams", "Publish · Channels → Microsoft Teams and Microsoft 365 Copilot", [
        ("Select Publish (top right), then Publish again in the dialog.", "The first publication takes a minute or two. Every later change needs a new Publish; the Test pane always shows the unpublished version."),
        ("Open Channels → Microsoft Teams and Microsoft 365 Copilot.", "Select Add channel. Keep Make agent available in Microsoft 365 Copilot ticked if the team uses Copilot chat; the agent then appears there too."),
        ("Choose how people get it: Availability options.", "Copy link: send it to the BD team, they add the app themselves. Show to my teammates and shared users: it appears in Built for your org after you share it. Show in Teams store: needs admin approval in the Teams admin center (Manage apps)."),
        ("Set the Teams details.", "Icon, short description, developer name HEC Paris Executive Education, privacy and terms links: the standard internal ones."),
        ("Skip the Demo website for this agent.", "It only works with No authentication, and an agent with SharePoint knowledge needs the user signed in. Use the Teams link for stakeholders."),
    ], ["Publish shows the date and time of the last publication", "The Teams channel shows Connected", "A colleague opens the link, adds the app and gets your greeting", "A change in the instructions does not reach Teams until the next Publish"],
       "Publish is a version: what the team uses is the last published state, the Test pane is the draft. For a training, the Copy link path needs no admin; the store path is the right one for a real roll-out, with an admin approving in Manage apps. If the tenant restricts custom agents in Teams, the link still works for people the agent is shared with.")

    # 15 · step 10 monitor
    s = blank(); title(s, "Step 10 · Run it · monitor, improve, govern")
    cols = [("Every week", ["Monitor page: sessions, engagement, resolution rate, the knowledge sources and tools actually used", "Activity page: read five transcripts; where did the agent say \"I cannot find\"? Add the document or fix the description", "Check the RFP log list: rows created, by whom"]),
            ("Every change", ["Edit in the draft, run the five test prompts, then Publish", "Change one thing at a time: an instruction line, a description, a source", "Export the agent as a solution before a big change (Solutions in Power Apps) so you can go back"]),
            ("Every quarter", ["Refresh the catalogue and the policy in the folder: the index follows", "Review who the agent is shared with; remove leavers", "Look at credit consumption with the admin: the Copilot Studio capacity report in the Power Platform admin center"])]
    for i, (h, b) in enumerate(cols):
        card(s, 0.9 + i * 3.95, 1.55, 3.7, 3.7, h, b, size=11)
    callout(s, 0.9, 5.45, 11.6, 1.15, "Ownership", "An agent needs a named owner in the business, not in IT: the person who reads the transcripts and updates the content. Name them on the Overview description. Copilot Studio can be co-owned: Share from the agent's Overview, Co-owner for the backup person.")
    notes(s, "The agent is a product with a maintenance routine, not a project with an end date. The weekly transcript reading is the only step that improves the agent; everything else keeps it alive.")

    # 16 · the exercise
    s = blank(); title(s, "Build it yourself · sixty minutes, in pairs")
    chip(s, URL, 0.9, 1.5, 4.6, 0.45, fill=NAVY, size=16)
    textbox(s, 5.7, 1.47, 6.9, 0.6, [("One agent per pair: one drives, the other reads the slide and checks the boxes. Swap at step 4. The content pack is in the shared folder named on the board.", {"size": 12, "color": GREY})])
    rows = [("Minutes", "Steps", "Done when"),
            ("0–10", "Steps 1 and 2: create, description, paste the instructions", "The greeting answers in the Test pane; the description is on the Overview"),
            ("10–20", "Step 3: the SharePoint folder as knowledge, general knowledge off", "The catalogue question is answered with a citation; the football question is refused"),
            ("20–35", "Step 4: the Draft proposal section prompt tool", "A draft with the template headings and [TO CONFIRM] placeholders"),
            ("35–50", "Step 5: the Log RFP flow and list (skip if no SharePoint rights: note why)", "A row appears in RFP log with the item number in the answer"),
            ("50–60", "Steps 6 and 7: greeting, escalation topic, the five test prompts", "All five prompts behave as the table says; one snapshot saved")]
    table(s, 0.9, 2.2, [1.1, 5.6, 4.9], rows, size=10.5, row_h=0.6)
    callout(s, 0.9, 5.75, 11.6, 0.85, "Publishing is for after the session", "Nobody publishes during the training: a published agent is a product with an owner. The last fifteen minutes are the debrief: which rule in your never-list could you move from prose into a setting or a flow?")
    notes(s, "Sixty minutes is tight; the flow in step 5 is the usual sink. Pairs without rights on the SharePoint site skip it and write down the blocker: that is itself a lesson in governance. Keep the slide of the current step on screen and walk the room.")

    # 17 · what goes wrong
    s = blank(); title(s, "What goes wrong, and the fix")
    rows = [("Symptom", "Cause", "Fix"),
            ("Answers sound right but are not from HEC content", "General knowledge is on", "Knowledge page or Settings → Generative AI: switch it off; retest the football question"),
            ("\"I could not find …\" for a document that is in the folder", "Indexing not finished, wrong URL, or the user has no access to the file", "Wait a few minutes; paste the folder URL, not a file URL; check rights in SharePoint"),
            ("The tool is never called", "Vague description, or the orchestrator cannot see the inputs", "Rewrite the description with \"Use when …\" and the inputs it needs; test with an explicit request"),
            ("The flow cannot be added as a tool", "Wrong trigger, no Respond to the agent, or not published", "Trigger When an agent calls the flow; end with Respond to the agent; Publish"),
            ("Flow error at run time", "Connector blocked by a DLP policy, or run over 100 seconds", "Ask the admin about the policy; simplify the flow"),
            ("Teams shows the old behaviour", "Not re-published", "Publish again; the Test pane is the draft, Teams is the last publication"),
            ("The agent will not install in Teams", "Custom agents restricted by the admin", "Share by link to named users, or ask for store approval in Manage apps"),
            ("Credits run out mid-week", "Each answer, tool call and flow action is metered", "Capacity report in the admin center; pay-as-you-go as a safety net")]
    table(s, 0.9, 1.55, [3.9, 3.6, 4.1], rows, size=10, row_h=0.58)
    notes(s, "Keep this slide for the debrief and for the day after. The first three lines cover most of what happens in a room.")

    # 18 · which tool for which agent
    s = blank(); title(s, "Which builder for which agent")
    rows = [("", "Agent Builder (in Microsoft 365 Copilot)", "Copilot Studio, standard experience", "Copilot Studio, new experience (preview)"),
            ("Who", "Any Microsoft 365 Copilot user", "Makers with a Copilot Studio licence or trial", "Same, opting in on the Home page"),
            ("Knowledge", "SharePoint, files, websites", "Same, plus Dataverse and enterprise data", "Same"),
            ("Tools", "None: answers only", "Prompts, agent flows, connectors, MCP servers, REST APIs", "Same, in a different dialog"),
            ("Guardrails", "Microsoft 365 permissions, DLP", "Authentication, moderation, DLP, flow logic", "Same"),
            ("Publish", "Share with people or the org", "Teams, Microsoft 365 Copilot, web, demo site", "Same channels"),
            ("Use it for", "A personal or team Q&A assistant on documents", "This RFP assistant: knowledge plus two actions", "New agents once the preview is general in your tenant")]
    table(s, 0.9, 1.55, [1.6, 3.3, 3.5, 3.2], rows, size=10.5, row_h=0.6)
    callout(s, 0.9, 5.65, 11.6, 0.95, "Rule of thumb", "If the agent only has to answer from documents for a few people, Agent Builder is enough and costs nothing extra. The moment it must do something, or be governed as a product, it is a Copilot Studio agent.")
    notes(s, "Participants with a Microsoft 365 Copilot licence can rebuild the knowledge part of this agent in Agent Builder in ten minutes; the two tools are what need Copilot Studio.")

    # 19 · sources
    s = blank(); title(s, "Sources and further reading")
    src = [("Microsoft Learn · Copilot Studio documentation", "learn.microsoft.com/microsoft-copilot-studio: Create and delete agents · Add knowledge sources · Add tools to custom agents · Add an agent flow as a tool · Orchestrate agent behavior with generative AI · Configure high-quality instructions · Test your agent · Review agent activity · Publish and deploy your agent · Configure user authentication · Requirements and quotas"),
           ("Microsoft Agent Academy and Copilot Studio labs", "microsoft.github.io/agent-academy and microsoft.github.io/mcs-labs: hands-on courses with the same steps, kept current with the new experience"),
           ("Microsoft Copilot Studio licensing guide", "The current edition from Microsoft: Copilot Credits, capacity packs, pay-as-you-go, what Microsoft 365 Copilot includes"),
           ("Agent Builder in Microsoft 365 Copilot", "learn.microsoft.com/microsoft-365/copilot/extensibility/agent-builder-build-agents"),
           ("This course", "The inbox agent (brief, rules, tools, guardrails, trace) and the payment lab (mandates, verifiers): the same four ideas, in Copilot Studio's vocabulary")]
    for i, (h, b) in enumerate(src):
        y = 1.45 + i * 1.0
        textbox(s, 0.9, y, 11.6, 0.35, [(h, {"bold": True, "size": 12.5})]); textbox(s, 0.9, y + 0.33, 11.6, 0.65, [(b, {"size": 10.5, "color": GREY})])
    textbox(s, 0.9, 6.5, 11.6, 0.5, [("Copilot Studio changes monthly. The steps here follow the documented standard experience as of November 2026; when a label differs on your screen, the Microsoft Learn page of that step is the reference.", {"size": 10.5, "italic": True, "color": GREY})])
    notes(s, "Hand out the Learn links. The licensing guide is the only document to quote on cost.")

    out = HERE / "copilot-studio-rfp-agent.pptx"
    prs.save(out)
    return out


if __name__ == "__main__":
    print("wrote", build())
