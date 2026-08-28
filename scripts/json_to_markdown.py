#!/usr/bin/env python3
"""Regenerate POH sections 04 / 04b / 05 from the EFIS-editor checklist JSON.

Usage: python3 scripts/json_to_markdown.py N720AK.json

The markdown style here reproduces the previously committed sections exactly;
validate any style change with:  git diff sections/04*.md sections/05-normal.md
"""
import json
import re
import sys
from pathlib import Path

FILES = [
    ("sections/04-emergency.md", "Emergency Procedures", True,
     ["Engine Failures", "Forced Landings", "Fires",
      "Electrical / Engine Malfunctions", "Icing / Static",
      "Inadvertent IMC / Upset"]),
    ("sections/04b-abnormal.md", "Abnormal Procedures", False, ["Abnormal"]),
    ("sections/05-normal.md", "Normal Procedures", True,
     ["Memory Items", "Preflight", "In Flight", "Postflight",
      "Non-Standard Takeoff and Landing"]),
]

DERIVED = "> These procedures are derived from the efis-editor checklist file."
DERIVED2 = "> Update the source JSON and regenerate to modify."

# Items bolded inside their full checklist because they are memory items
# (mirrors the Memory Items group). Keyed by checklist title -> prompts.
BOLD = {
    "Engine Failure Immediately After Takeoff": ["Pitch", "Landing Spot"],
    "Engine Failure In Flight": ["Airspeed", "NRST Button", "Best Field"],
    "Engine Failure On Approach": ["Airspeed", "Best Surface"],
    "Engine Fire In Flight": ["Fuel Selector", "Key Switch"],
    "Electrical Fire / Smoke In Cockpit": ["Key Switch", "Master Switch", "Vents / Cabin Air"],
    "Bus Manager Failure / Switch to Endurance Bus": ["Emergency Power Switch"],
    "Runaway Trim": ["Avionics Master"],
    "Upset Recovery — Power / Push / Roll": ["Power", "Push", "Roll"],
}


def render_checklist(c, memory_style):
    out = [f"\n### {c['title']}\n\n"]
    bold_prompts = BOLD.get(c["title"], [])
    attached = False  # previous rendered item was a list item (CR or its detail)
    for it in c["items"]:
        t = it["type"]
        prompt = it.get("prompt", "")
        exp = it.get("expectation", "")
        indent = it.get("indent", 0)
        if t == "ITEM_CHALLENGE_RESPONSE":
            if memory_style or prompt in bold_prompts:
                out.append(f"\n**{prompt}** ... **{exp}**\n\n")
                attached = False
            else:
                out.append(f"- {prompt} ... **{exp}**\n")
                attached = True
        elif t == "ITEM_TITLE":
            out.append(f"\n#### {prompt}\n\n")
            attached = False
        elif t == "ITEM_PLAINTEXT":
            if indent and attached:
                out.append(f"  \n    *{prompt}*\n")
            elif indent:
                out.append(f"\n  *{prompt}*\n\n")
            else:
                out.append(f"\n*{prompt}*\n\n")
        elif t == "ITEM_NOTE":
            out.append(f"\n> *Note: {prompt}*\n\n")
            attached = False
        elif t == "ITEM_WARNING":
            out.append(f"\n> ⚠️ **WARNING:** {prompt}\n\n")
            attached = False
        elif t == "ITEM_CAUTION":
            out.append(f"\n> ⚠️ **CAUTION:** {prompt}\n\n")
            attached = False
    return "".join(out)


def render_file(data, title, two_line_note, group_titles):
    groups = {g["title"]: g for g in data["groups"]}
    out = [f"# {title}\n\n{DERIVED}\n"]
    if two_line_note:
        out.append(f"{DERIVED2}\n")
    for gt in group_titles:
        out.append(f"\n## {gt}\n")
        for c in groups[gt]["checklists"]:
            out.append(render_checklist(c, memory_style=(gt == "Memory Items")))
    text = "".join(out)
    text = re.sub(r"\n{4,}", "\n\n\n", text)  # never more than 2 blank lines
    return text.rstrip("\n") + "\n"


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else "N720AK.json"
    data = json.load(open(src))
    for path, title, two_line, gts in FILES:
        Path(path).write_text(render_file(data, title, two_line, gts))
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
