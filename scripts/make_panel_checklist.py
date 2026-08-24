#!/usr/bin/env python3
"""Derive the terse in-panel checklist variant from N720AK.json.

The full checklist (N720AK.json) carries amplifying detail as ITEM_PLAINTEXT
and ITEM_NOTE rows — great in the printed/ForeFlight version, noise on the
Dynon's narrow checklist window. This script strips those item types and
writes N720AK-panel.json. Upload BOTH files to the EFIS Editor: export
ForeFlight (.fmd) from the full file, Dynon (.txt) from the panel file.

Never hand-edit N720AK-panel.json — it is always regenerated.

Kept:    ITEM_CHALLENGE_RESPONSE, ITEM_TITLE, ITEM_WARNING, ITEM_CAUTION, ITEM_SPACE
Dropped: ITEM_PLAINTEXT, ITEM_NOTE
Exception: checklists whose group is "Memory Items" keep everything (the
memory card is prose by design).
"""
import json, sys, copy

DROP = {"ITEM_PLAINTEXT", "ITEM_NOTE"}

def main():
    src = json.load(open("N720AK.json"))
    out = copy.deepcopy(src)
    dropped = 0

    def walk(node, keep_all=False):
        nonlocal dropped
        if isinstance(node, dict):
            title = node.get("title", "")
            keep = keep_all or title == "Memory Items"
            if "items" in node and not keep:
                before = len(node["items"])
                node["items"] = [i for i in node["items"] if i.get("type") not in DROP]
                dropped += before - len(node["items"])
            for k in ("groups", "checklists"):
                for c in node.get(k, []):
                    walk(c, keep)

    walk(out)
    meta = out.get("metadata") or out.get("aircraftInfo")
    json.dump(out, open("N720AK-panel.json", "w"), indent=2, ensure_ascii=False)
    print(f"N720AK-panel.json written; dropped {dropped} detail items")

if __name__ == "__main__":
    main()
