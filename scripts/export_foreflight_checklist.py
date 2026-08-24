#!/usr/bin/env python3
"""Export a ForeFlight checklist .fmd from an EFIS-editor JSON file.

Python port of the efis-editor ForeFlightWriter (github.com/rdamazio/efis-editor).
The .fmd container is AES-128-CBC (fixed key published in that repo, random IV
prepended, PKCS#7 padding) over pretty-printed JSON.

Usage:
  uv run --with cryptography python3 scripts/export_foreflight_checklist.py N720AK.json N720AK.fmd
  ... --decrypt file.fmd            # print the JSON payload of an existing .fmd
"""
import argparse
import json
import os
import sys
import uuid

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.padding import PKCS7

KEY = b"81e06e41a93f3848"
PREFIXES = {"ITEM_PLAINTEXT": "", "ITEM_NOTE": "NOTE: ", "ITEM_CAUTION": "CAUTION: ", "ITEM_WARNING": "WARNING: "}
TITLE_LIKE = {"ITEM_TITLE", "ITEM_CHALLENGE_RESPONSE"}
NOTE_INDENT = 1


def oid():
    return uuid.uuid4().hex


def should_merge(item, last):
    li, ii = last.get("indent", 0), item.get("indent", 0)
    lt = last.get("type")
    return (lt in TITLE_LIKE and li < ii) or (lt in PREFIXES and li <= ii and li >= NOTE_INDENT)


def items_to_ff(items):
    acc = []  # [ff_dict, efis_item] pairs
    for it in items:
        typ = it.get("type", "ITEM_CHALLENGE_RESPONSE")
        ff = {"objectId": oid(), "title": it.get("prompt", ""), "detail": it.get("expectation", "").upper()}
        acc.append([ff, it])
        if typ == "ITEM_CHALLENGE_RESPONSE":
            pass
        elif typ == "ITEM_CHALLENGE":
            ff.pop("detail")
        elif typ == "ITEM_TITLE":
            ff["type"] = "comment"
            ff.pop("detail")
        elif typ in PREFIXES:
            text = PREFIXES[typ] + it.get("prompt", "")
            if len(acc) >= 2 and should_merge(it, acc[-2][1]):
                last_ff = acc[-2][0]
                if last_ff.get("type") != "comment":
                    last_ff["note"] = (last_ff["note"] + "\n" + text) if last_ff.get("note") else text
                else:
                    last_ff["detail"] = (last_ff["detail"] + "\n" + text) if last_ff.get("detail") else text
                acc.pop()
                continue
            ff["type"] = "comment"
            ff.pop("title")
            ff["detail"] = text
        elif typ == "ITEM_SPACE":
            ff["type"] = "comment"
            ff.pop("title")
            ff.pop("detail")
        else:
            raise ValueError(f"unknown item type {typ}")
    # reorder keys: objectId, type, title, detail, note (proto field order)
    out = []
    for ff, _ in acc:
        o = {"objectId": ff["objectId"]}
        for k in ("type", "title", "detail", "note"):
            if k in ff:
                o[k] = ff[k]
        out.append(o)
    return out


def convert(data):
    md = data.get("metadata", {})
    return {
        "type": "checklist",
        "payload": {
            "objectId": oid(),
            "schemaVersion": "1.0",
            "metadata": {
                "name": md.get("name", ""),
                "detail": md.get("makeAndModel", ""),
                "tailNumber": md.get("aircraftInfo", "").upper(),
            },
            "groups": [
                {
                    "objectId": oid(),
                    "groupType": cat,
                    "items": [
                        {
                            "objectId": oid(),
                            "title": g.get("title", ""),
                            "items": [
                                {"objectId": oid(), "title": c.get("title", ""), "items": items_to_ff(c.get("items", []))}
                                for c in g.get("checklists", [])
                            ],
                        }
                        for g in data.get("groups", [])
                        if g.get("category", "normal") == cat
                    ],
                }
                for cat in ("normal", "abnormal", "emergency")
            ],
        },
    }


def encrypt(text: str) -> bytes:
    iv = os.urandom(16)
    padder = PKCS7(128).padder()
    padded = padder.update(text.encode()) + padder.finalize()
    enc = Cipher(algorithms.AES(KEY), modes.CBC(iv)).encryptor()
    return iv + enc.update(padded) + enc.finalize()


def decrypt(blob: bytes) -> str:
    dec = Cipher(algorithms.AES(KEY), modes.CBC(blob[:16])).decryptor()
    padded = dec.update(blob[16:]) + dec.finalize()
    unpadder = PKCS7(128).unpadder()
    return (unpadder.update(padded) + unpadder.finalize()).decode()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("input"); ap.add_argument("output", nargs="?")
    ap.add_argument("--decrypt", action="store_true", help="input is a .fmd; print its JSON payload")
    args = ap.parse_args()
    if args.decrypt:
        print(decrypt(open(args.input, "rb").read()))
        return
    data = json.load(open(args.input, encoding="utf-8"))
    payload = json.dumps(convert(data), indent=2, ensure_ascii=False)
    out = args.output or "checklist.fmd"
    with open(out, "wb") as f:
        f.write(encrypt(payload))
    print(f"{out}: {len(payload)} bytes JSON, encrypted")


if __name__ == "__main__":
    main()
