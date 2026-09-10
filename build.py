#!/usr/bin/env python3
"""Splice data/emails.json into src/inbox-agent.src.html and write inbox-agent.html."""
import json
from pathlib import Path

root = Path(__file__).parent
data = json.loads((root / "data" / "emails.json").read_text())
payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
src = (root / "src" / "inbox-agent.src.html").read_text()
assert "__INBOX_DATA__" in src
out = src.replace("__INBOX_DATA__", payload)
(root / "inbox-agent.html").write_text(out)
print(f"wrote inbox-agent.html ({len(out) // 1024} KB, {len(data['emails'])} emails)")
