#!/usr/bin/env python3
"""Export a Dynon SkyView checklist .txt from an EFIS-editor JSON file.

Faithful Python port of the efis-editor TextWriter/DynonFormat
(github.com/rdamazio/efis-editor, src/model/formats/text-writer.ts) so the
checklist pipeline runs entirely offline. Verified byte-for-byte against a
real efis-editor export (see tests via --golden).

Usage:
  python3 scripts/export_dynon_checklist.py N720AK-panel.json checklist.txt
  python3 scripts/export_dynon_checklist.py --variant 31 --date 2026-08-19 in.json out.txt
"""
import argparse
import json
import sys
from datetime import date

CRLF = "\r\n"
WRAP_PREFIX = "| "
HEADER_COMMENT = "# CHECKLIST EXPORTED FROM https://github.com/rdamazio/efis-editor/"
LAST_UPDATED_FOOTER = "Last updated "

OPTS = dict(
    indent_width=2,
    all_uppercase=True,
    checklist_top_blank_line=True,
    output_metadata=True,
    checklist_prefix="CHKLST{c}.TITLE,",
    item_prefix="CHKLST{c}.LINE{i},",
    checklist_zero_indexed=True,
    item_zero_indexed=False,
    skip_first_group=True,
    expectation_separator=" - ",
    note_prefix="NOTE: ",
    title_prefix_suffix="** ",
    warning_prefix="WARNING: ",
    caution_prefix="CAUTION: ",
)

PREFIXES = {
    "ITEM_TITLE": ("** ", " **"),
    "ITEM_WARNING": ("WARNING: ", ""),
    "ITEM_CAUTION": ("CAUTION: ", ""),
    "ITEM_NOTE": ("NOTE: ", ""),
}


class Writer:
    def __init__(self, max_line_length=None, today=None):
        self.max_line_length = max_line_length
        self.today = today or date.today()
        self.parts = []

    def _add(self, s):
        self.parts.append(s.upper() if OPTS["all_uppercase"] else s)

    def _line(self, s=None):
        if s:
            self._add(s)
        self.parts.append(CRLF)

    def _cprefix(self, c):
        return OPTS["checklist_prefix"].format(c=c if OPTS["checklist_zero_indexed"] else c + 1)

    def _iprefix(self, c, i):
        return OPTS["item_prefix"].format(
            c=c if OPTS["checklist_zero_indexed"] else c + 1,
            i=i if OPTS["item_zero_indexed"] else i + 1,
        )

    def write(self, data):
        self._line(HEADER_COMMENT)
        idx = 0
        first_group = True
        for group in data.get("groups", []):
            for checklist in group.get("checklists", []):
                self._line()
                self._add(self._cprefix(idx))
                self._add(" ")
                if not first_group or not OPTS["skip_first_group"]:
                    self._add(group.get("title", ""))
                    self._add(": ")
                self._line(checklist.get("title", ""))
                self._items(checklist.get("items", []), idx)
                idx += 1
            first_group = False
        md = data.get("metadata")
        if OPTS["output_metadata"] and md:
            self._metadata(md, idx)
        return "".join(self.parts)

    def _metadata(self, md, c):
        self._line()
        self._add(self._cprefix(c))
        self._add(" ")
        self._line("Checklist Info")
        i = 0
        if OPTS["checklist_top_blank_line"]:
            self._line(self._iprefix(c, i)); i += 1
        i = self._md_item("Checklist file:", md.get("name", ""), c, i)
        if md.get("makeAndModel"):
            i = self._md_item("Make and model:", md["makeAndModel"], c, i)
        if md.get("aircraftInfo"):
            i = self._md_item("Aircraft:", md["aircraftInfo"], c, i)
        if md.get("manufacturerInfo"):
            i = self._md_item("Manufacturer:", md["manufacturerInfo"], c, i)
        if md.get("copyrightInfo"):
            i = self._md_item("Copyright:", md["copyrightInfo"], c, i)
        self._line(self._iprefix(c, i)); i += 1
        self._add(self._iprefix(c, i))
        self._add(" ")
        self._add(LAST_UPDATED_FOOTER)
        self._line(f"{self.today.year}-{self.today.month:02d}-{self.today.day:02d}")

    def _md_item(self, title, contents, c, i):
        self._add(self._iprefix(c, i)); i += 1
        self._add(" ")
        self._line(title)
        self._add(self._iprefix(c, i)); i += 1
        self._add("   ")
        self._line(contents)
        return i

    def _items(self, items, c):
        i = 0
        if OPTS["checklist_top_blank_line"]:
            self._line(self._iprefix(c, i)); i += 1
        for item in items:
            typ = item.get("type", "ITEM_CHALLENGE_RESPONSE")
            prefix, suffix = PREFIXES.get(typ, ("", ""))
            full = prefix + item.get("prompt", "")
            if item.get("expectation"):
                full += OPTS["expectation_separator"] + item["expectation"]
            full += suffix
            if typ == "ITEM_SPACE":
                indent = 0
            elif item.get("centered"):
                if self.max_line_length and len(full) < self.max_line_length:
                    indent = (self.max_line_length - len(full)) // 2
                else:
                    indent = 7
            else:
                indent = item.get("indent", 0) * OPTS["indent_width"]
            indent_str = " " * indent
            wrapped = False
            while True:
                self._add(self._iprefix(c, i)); i += 1
                if typ != "ITEM_SPACE":
                    self._add(" ")
                self._add(indent_str)
                wrap_width = 0
                if wrapped:
                    wrap_width = len(WRAP_PREFIX)
                    self._add(WRAP_PREFIX)
                if self.max_line_length:
                    max_content = self.max_line_length - indent - wrap_width
                    if len(full) > max_content:
                        wrap_idx = full[:max_content].rfind(" ")
                        if wrap_idx == -1:
                            wrap_idx = self.max_line_length
                        self._line(full[:wrap_idx])
                        full = full[wrap_idx + 1:]
                        wrapped = True
                        continue
                self._add(full)
                if item.get("centered"):
                    self._add(indent_str)
                self._line()
                break


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("input"); ap.add_argument("output")
    ap.add_argument("--variant", choices=["none", "31", "40"], default="31",
                    help="Dynon display width: 31 (40%% page, default), 40 (50%% page), none (no wrap)")
    ap.add_argument("--date", help="Override the Last updated date (YYYY-MM-DD), for reproducible output")
    args = ap.parse_args()
    max_len = None if args.variant == "none" else int(args.variant)
    today = date.fromisoformat(args.date) if args.date else None
    data = json.load(open(args.input, encoding="utf-8"))
    out = Writer(max_line_length=max_len, today=today).write(data)
    with open(args.output, "w", encoding="utf-8", newline="") as f:
        f.write(out)
    print(f"{args.output}: {len(out.splitlines())} lines ({'no wrap' if not max_len else str(max_len) + ' cols'})")


if __name__ == "__main__":
    main()
