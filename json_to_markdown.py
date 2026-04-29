#!/usr/bin/env python3
"""
Convert efis-editor checklist JSON to Pandoc markdown sections.

The efis-editor JSON format is the source of truth for checklists.
This script generates markdown sections for normal, abnormal, and emergency
procedures that can be included in the POH.

Usage:
    python3 json_to_markdown.py checklist.json

This generates:
    sections/04-emergency.md   (emergency procedures)
    sections/04b-abnormal.md   (abnormal procedures, if any)
    sections/05-normal.md      (normal procedures)
"""

import json
import sys
from pathlib import Path

# Category mappings - supports both integer (protobuf enum) and string values
CATEGORY_NORMAL = {0, "normal", "NORMAL"}
CATEGORY_ABNORMAL = {1, "abnormal", "ABNORMAL"}
CATEGORY_EMERGENCY = {2, "emergency", "EMERGENCY"}


def format_challenge_response(challenge: str, response: str, indent: int = 0) -> str:
    """Format a challenge-response item with dot leaders."""
    prefix = "  " * indent
    if not response:
        return f"{prefix}- {challenge}"

    # Create dot leader effect using a table-like format for better PDF output
    return f"{prefix}- {challenge} {'.' * 3} **{response}**"


def format_item(item: dict, indent: int = 0, prev_was_listy: bool = True) -> str:
    """Format a single checklist item based on its type.

    `prev_was_listy` tells us whether the previous emitted line was part of an
    open list (so an indented continuation line is OK) vs. a paragraph break
    (so 4-space indentation would be misread as a fenced code block by Pandoc).
    """
    item_type = item.get("type", "ITEM_CHALLENGE_RESPONSE")
    prefix = "  " * indent
    centered = item.get("centered", False)

    if item_type == "ITEM_SPACE":
        return ""

    if item_type == "ITEM_TITLE":
        # The protobuf schema stores the heading text in `prompt`, not `title`.
        # Render as an h4 heading so it stands above the bulleted/bold items
        # that follow. (Checklist title is h3.)
        prompt = item.get("prompt", "").strip()
        if not prompt:
            return ""
        return f"\n{prefix}#### {prompt}\n"

    if item_type == "ITEM_NOTE":
        prompt = item.get("prompt", "")
        return f"\n{prefix}> *Note: {prompt}*\n"

    if item_type == "ITEM_WARNING":
        prompt = item.get("prompt", "")
        return f"\n{prefix}> ⚠️ **WARNING:** {prompt}\n"

    if item_type == "ITEM_CAUTION":
        prompt = item.get("prompt", "")
        return f"\n{prefix}> **CAUTION:** {prompt}\n"

    if item_type == "ITEM_PLAINTEXT":
        prompt = item.get("prompt", "")
        if centered:
            return f"\n{prefix}*{prompt}*\n"
        # When the previous line wasn't a list bullet (e.g., it was a TITLE,
        # WARNING, or centered item rendered as its own paragraph), 4-space
        # indentation here makes Pandoc treat the line as a code block. Emit
        # an italicized paragraph instead so the hint reads as ordinary prose.
        if not prev_was_listy:
            return f"\n{prefix}*{prompt}*\n"
        # Indented continuation under a list bullet. A hard line break
        # (two trailing spaces) plus italics keeps the hint attached to the
        # bullet without indenting 4 spaces — which would be misread as a
        # code block by CommonMark/Pandoc.
        return f"  \n{prefix}  *{prompt}*"

    if item_type == "ITEM_CHALLENGE_RESPONSE":
        prompt = item.get("prompt", "")
        expectation = item.get("expectation", "")

        if centered:
            # Memory item: bold prompt + bold expectation, no list bullet, no
            # dot leaders. Convention: bold-line == memory item.
            if expectation:
                return f"\n**{prompt}** ... **{expectation}**\n"
            return f"\n**{prompt}**\n"

        return format_challenge_response(prompt, expectation, indent)

    # Default fallback
    prompt = item.get("prompt", "")
    return f"{prefix}- {prompt}"


def _is_listy(item_type: str, centered: bool) -> bool:
    """Did this item produce an open list bullet?"""
    if centered:
        return False
    if item_type in ("ITEM_TITLE", "ITEM_NOTE", "ITEM_WARNING", "ITEM_CAUTION", "ITEM_SPACE"):
        return False
    # PLAINTEXT only continues a list if the previous bullet was itself a list
    # item; we approximate by saying PLAINTEXT inherits prior listy-ness.
    if item_type == "ITEM_PLAINTEXT":
        return None  # signal: do not change prev_listy
    return True  # ITEM_CHALLENGE / ITEM_CHALLENGE_RESPONSE


def format_checklist(checklist: dict) -> str:
    """Format a single checklist (e.g., 'Preflight Inspection')."""
    lines = []
    title = checklist.get("title", "Untitled")

    lines.append(f"### {title}")
    lines.append("")

    prev_listy = False
    for item in checklist.get("items", []):
        indent = item.get("indent", 0)
        item_type = item.get("type", "ITEM_CHALLENGE_RESPONSE")
        centered = item.get("centered", False)
        formatted = format_item(item, indent, prev_was_listy=prev_listy)
        if formatted:
            lines.append(formatted)
        # Update listy-ness for the next iteration.
        listy = _is_listy(item_type, centered)
        if listy is not None:
            prev_listy = listy

    lines.append("")
    return "\n".join(lines)


def format_group(group: dict) -> str:
    """Format a checklist group (e.g., 'Preflight' containing multiple checklists)."""
    lines = []
    title = group.get("title", "Untitled Group")

    lines.append(f"## {title}")
    lines.append("")

    for checklist in group.get("checklists", []):
        lines.append(format_checklist(checklist))

    return "\n".join(lines)


def get_aircraft_info(data: dict) -> dict:
    """Extract aircraft metadata from the JSON."""
    metadata = data.get("metadata", {})
    return {
        "name": metadata.get("name", ""),
        "make_model": metadata.get("makeAndModel", ""),
        "aircraft_info": metadata.get("aircraftInfo", ""),
    }


def convert_json_to_markdown(json_path: str) -> dict[str, str]:
    """
    Convert checklist JSON to markdown sections.

    Returns dict with:
        - 'normal': normal procedures markdown
        - 'abnormal': abnormal procedures markdown (if any)
        - 'emergency': emergency procedures markdown (if any)
        - 'aircraft_info': metadata about the aircraft
    """
    with open(json_path, 'r') as f:
        data = json.load(f)

    normal_groups = []
    abnormal_groups = []
    emergency_groups = []

    for group in data.get("groups", []):
        category = group.get("category", 0)

        if category in CATEGORY_EMERGENCY:
            emergency_groups.append(group)
        elif category in CATEGORY_ABNORMAL:
            abnormal_groups.append(group)
        else:
            normal_groups.append(group)

    results = {
        "aircraft_info": get_aircraft_info(data)
    }

    # Emergency procedures
    if emergency_groups:
        lines = ["# Emergency Procedures", ""]
        lines.append("> These procedures are derived from the efis-editor checklist file.")
        lines.append("> Update the source JSON and regenerate to modify.")
        lines.append("")
        for group in emergency_groups:
            lines.append(format_group(group))
        results["emergency"] = "\n".join(lines)

    # Abnormal procedures
    if abnormal_groups:
        lines = ["# Abnormal Procedures", ""]
        lines.append("> These procedures are derived from the efis-editor checklist file.")
        lines.append("")
        for group in abnormal_groups:
            lines.append(format_group(group))
        results["abnormal"] = "\n".join(lines)

    # Normal procedures
    if normal_groups:
        lines = ["# Normal Procedures", ""]
        lines.append("> These procedures are derived from the efis-editor checklist file.")
        lines.append("> Update the source JSON and regenerate to modify.")
        lines.append("")
        for group in normal_groups:
            lines.append(format_group(group))
        results["normal"] = "\n".join(lines)

    return results


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 json_to_markdown.py <checklist.json>")
        print()
        print("Converts efis-editor JSON checklists to POH markdown sections.")
        print()
        print("Output files:")
        print("  sections/04-emergency.md   - Emergency procedures")
        print("  sections/04b-abnormal.md   - Abnormal procedures (if any)")
        print("  sections/05-normal.md      - Normal procedures")
        sys.exit(1)

    json_path = sys.argv[1]

    if not Path(json_path).exists():
        print(f"Error: File not found: {json_path}")
        sys.exit(1)

    # Ensure sections directory exists
    sections_dir = Path("sections")
    sections_dir.mkdir(exist_ok=True)

    print(f"Reading: {json_path}")
    results = convert_json_to_markdown(json_path)

    # Show aircraft info
    info = results["aircraft_info"]
    if info["name"]:
        print(f"Aircraft: {info['name']}")
    if info["make_model"]:
        print(f"Make/Model: {info['make_model']}")

    # Write emergency procedures
    if "emergency" in results:
        output_path = sections_dir / "04-emergency.md"
        with open(output_path, 'w') as f:
            f.write(results["emergency"])
        print(f"Wrote: {output_path}")

    # Write abnormal procedures
    if "abnormal" in results:
        output_path = sections_dir / "04b-abnormal.md"
        with open(output_path, 'w') as f:
            f.write(results["abnormal"])
        print(f"Wrote: {output_path}")

    # Write normal procedures
    if "normal" in results:
        output_path = sections_dir / "05-normal.md"
        with open(output_path, 'w') as f:
            f.write(results["normal"])
        print(f"Wrote: {output_path}")

    print()
    print("Done! Run ./build.sh to generate the PDF.")


if __name__ == "__main__":
    main()
