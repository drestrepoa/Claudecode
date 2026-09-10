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
(root / "site").mkdir(exist_ok=True)
cut = out.index("</style>") + len("</style>")
head, body = out[:cut], out[cut:]
(root / "site" / "index.html").write_text(
    "<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
    + head + "\n</head>\n<body>" + body + "\n</body>\n</html>\n")
print(f"wrote inbox-agent.html and site/index.html ({len(out) // 1024} KB, {len(data['emails'])} emails)")
