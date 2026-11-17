#!/usr/bin/env python3
"""Teaching notes for the agentic payments deck: every slide's speaker notes, in order, as Markdown and Word.

  python3 slides/extract_payments_notes.py   -> slides/agentic-payments-teaching-notes.md and .docx (needs pandoc for the .docx)
"""
import re, subprocess, shutil
from pathlib import Path
from pptx import Presentation

HERE = Path(__file__).parent
prs = Presentation(HERE / "agentic-payments.pptx")
out = ["# Agentic payments · teaching notes", "",
       "Course: Navigating Disruptive Innovation in Heavily Regulated Markets. Lab: https://agenticpayment.netlify.app/ (no code, no key).", "",
       "Timing: theory about twenty-five minutes, the exercise ten minutes over five slides (overview, then one slide per step), discussion with what is left. One slide, one message; the notes below are what to say, the slide is what they read.", ""]
for n, slide in enumerate(prs.slides, 1):
    texts = [sh.text_frame.text.strip() for sh in slide.shapes if sh.has_text_frame and sh.text_frame.text.strip()]
    title = next((t for t in texts if len(t) < 90), f"Slide {n}")
    notes = slide.notes_slide.notes_text_frame.text.strip() if slide.has_notes_slide else ""
    out += [f"## {n} · {title}", "", notes or "(no notes)", ""]
md = HERE / "agentic-payments-teaching-notes.md"; md.write_text("\n".join(out))
if shutil.which("pandoc"): subprocess.run(["pandoc", str(md), "-o", str(md.with_suffix(".docx"))], check=True)
print("wrote", md, "and", md.with_suffix(".docx"))
