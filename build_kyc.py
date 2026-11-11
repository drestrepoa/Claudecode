#!/usr/bin/env python3
"""Splice data/kyc/cases.json into src/kyc-agent.src.html and write kyc-agent.html and site/index.html.

    python3 data/kyc/generate_kyc_cases.py   # regenerate the case queue (optional)
    python3 build_kyc.py                     # build the page

kyc-agent.html is the single-file page (publish it as a claude.ai artifact with the `sample`
capability, or open it from any static host); site/index.html is the same page wrapped as a
full document, which Netlify serves next to netlify/functions/agent.mjs.
"""
import json
from pathlib import Path

root = Path(__file__).parent
src_json = root / "data" / "kyc" / "cases.json"
data = json.loads(src_json.read_text())
payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
src = (root / "src" / "kyc-agent.src.html").read_text()
assert "__KYC_DATA__" in src
out = src.replace("__KYC_DATA__", payload).replace("__TITLE__", (data.get("bank", "KYC") + " KYC Agent").replace("&", "&amp;"))
(root / "kyc-agent.html").write_text(out)
(root / "site").mkdir(exist_ok=True)
cut = out.index("</style>") + len("</style>")
head, body = out[:cut], out[cut:]
(root / "site" / "index.html").write_text(
    "<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
    + head + "\n</head>\n<body>" + body + "\n</body>\n</html>\n")
print(f"wrote kyc-agent.html and site/index.html from {src_json.relative_to(root)} ({len(out) // 1024} KB, {len(data['cases'])} cases, {data.get('bank')})")
