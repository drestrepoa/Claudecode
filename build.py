#!/usr/bin/env python3
"""Build the single-file pages.

  python3 build.py            law-firm inbox (data/emails.json)        -> inbox-agent.html, site/index.html
  python3 build.py hr         HR inbox (data/hr/emails.json)           -> inbox-agent.html, site/index.html
  python3 build.py rfp        RFP response agent (data/rfp/rfps.json)  -> rfp-agent.html, site/index.html
  python3 build.py payments   Agentic payment lab (no data file)        -> payments-lab.html, site/index.html

The RFP page shares the inbox page's stylesheet: its source is src/rfp-agent.body.html, and the build
prepends the <title> and <style> block of src/inbox-agent.src.html plus a few extra rules.
"""
import json
import os
import sys
from pathlib import Path

root = Path(__file__).parent
DATASETS = {
    "law": {"json": root / "data" / "emails.json", "src": root / "src" / "inbox-agent.src.html", "placeholder": "__INBOX_DATA__", "out": "inbox-agent.html", "title": lambda d: d.get("firm", "Inbox") + " Inbox Agent"},
    "hr": {"json": root / "data" / "hr" / "emails.json", "src": root / "src" / "inbox-agent.src.html", "placeholder": "__INBOX_DATA__", "out": "inbox-agent.html", "title": lambda d: d.get("firm", "Inbox") + " Inbox Agent"},
    "rfp": {"json": root / "data" / "rfp" / "rfps.json", "src": root / "src" / "rfp-agent.body.html", "placeholder": "__RFP_DATA__", "out": "rfp-agent.html", "title": lambda d: d.get("firm", "Bid desk") + " RFP Agent"},
    "payments": {"json": None, "src": root / "src" / "payments-lab.body.html", "placeholder": None, "out": "payments-lab.html", "title": lambda d: "Agentic Payment Lab"},
}
EXTRA_CSS = """
.lab.Billing{color:var(--muted);border-style:dashed}
.lab.Scheduling{color:#fff;background:var(--ok);border-color:var(--ok)}
.lab.Employment{color:var(--det);border-color:var(--det)}
.lab.Corporate{color:#8A4B12;border-color:#C98A45}
.row .when{min-width:60px}
"""
choice = (sys.argv[1] if len(sys.argv) > 1 else os.environ.get("DATASET", "law")).lower()
cfg = DATASETS[choice]
data = json.loads(cfg["json"].read_text()) if cfg["json"] else {}
payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
src = cfg["src"].read_text()
if choice in ("rfp", "payments"):
    head = (root / "src" / "inbox-agent.src.html").read_text()
    head = head[: head.index("</style>")] + EXTRA_CSS + "</style>\n"
    src = head + src
if cfg["placeholder"]:
    assert cfg["placeholder"] in src
    src = src.replace(cfg["placeholder"], payload)
out = src.replace("__TITLE__", cfg["title"](data).replace("&", "&amp;"))
(root / cfg["out"]).write_text(out)
(root / "site").mkdir(exist_ok=True)
cut = out.index("</style>") + len("</style>")
head, body = out[:cut], out[cut:]
(root / "site" / "index.html").write_text(
    "<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
    + head + "\n</head>\n<body>" + body + "\n</body>\n</html>\n")
n = len(data.get("emails") or data.get("rfps") or [])
print(f"wrote {cfg['out']} and site/index.html from {(cfg['json'] or cfg['src']).relative_to(root)} ({len(out) // 1024} KB, {n} records, {data.get('firm', cfg['title'](data))})")
