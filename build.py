#!/usr/bin/env python3
"""Splice data/emails.json into src/inbox-agent.src.html and write inbox-agent.html."""
import json
import os
import sys
from pathlib import Path

root = Path(__file__).parent
# Which inbox to embed: `python3 build.py` (law firm, data/emails.json) or `python3 build.py hr` / DATASET=hr (data/hr/emails.json)
DATASETS = {"law": root / "data" / "emails.json", "hr": root / "data" / "hr" / "emails.json"}
choice = (sys.argv[1] if len(sys.argv) > 1 else os.environ.get("DATASET", "law")).lower()
src_json = DATASETS.get(choice) or Path(choice)
data = json.loads(src_json.read_text())
fr_json = src_json.with_name(src_json.stem + ".fr.json")
embed = data
if fr_json.exists():  # a French twin of the data rides along, and it must mirror the English set exactly
    fr = json.loads(fr_json.read_text())
    problems = [k for k in ("today", "firm", "firm_domain") if data.get(k) != fr.get(k)]
    for k in ("labels", "default_rules", "suggestions", "emails"):
        if len(data.get(k, [])) != len(fr.get(k, [])): problems.append(f"{k}: {len(data.get(k, []))} en vs {len(fr.get(k, []))} fr")
    if sorted(data.get("examples", {})) != sorted(fr.get("examples", {})): problems.append("examples keys")
    for a, b in zip(data["emails"], fr["emails"]):
        for k in ("id", "date", "from_email", "privileged", "deadline", "read", "importance"):
            if a.get(k) != b.get(k): problems.append(f"{a['id']}.{k}: {a.get(k)!r} vs {b.get(k)!r}")
        if data["labels"].index(a["expected"]) != fr["labels"].index(b["expected"]): problems.append(f"{a['id']}.expected")
    if problems: raise SystemExit("EN/FR datasets differ: " + "; ".join(problems[:10]))
    embed = {"en": data, "fr": fr}
payload = json.dumps(embed, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
src = (root / "src" / "inbox-agent.src.html").read_text()
assert "__INBOX_DATA__" in src
out = src.replace("__INBOX_DATA__", payload).replace("__TITLE__", (data.get("firm", "Inbox") + " Inbox Agent").replace("&", "&amp;"))
(root / "inbox-agent.html").write_text(out)
(root / "site").mkdir(exist_ok=True)
cut = out.index("</style>") + len("</style>")
head, body = out[:cut], out[cut:]
(root / "site" / "index.html").write_text(
    "<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
    + head + "\n</head>\n<body>" + body + "\n</body>\n</html>\n")
print(f"wrote inbox-agent.html and site/index.html from {src_json.relative_to(root)} ({len(out) // 1024} KB, {len(data['emails'])} emails, {data.get('firm')})")
