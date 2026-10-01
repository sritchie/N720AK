#!/usr/bin/env python3
"""
Extract a structured wire list from the SteinAir schematic PDFs.

The SteinAir drawings are vector PDFs: every pin number, wire colour and
connector label is real text with a position on the page. That makes building
the wire list a parsing job rather than a transcription job.

Output is a TSV per drawing in `wiring/`, which is the source of truth the
KiCad schematics are generated from (see `plans/kicad-schematics.md`). The
output is a DRAFT for review -- rows the parser is unsure about carry a
`review` flag with the reason.

  uv run --with pymupdf python3 scripts/wirelist_extract.py --dump  <pdf>
  uv run --with pymupdf python3 scripts/wirelist_extract.py --sheet O2

`--dump` prints the de-duplicated word layout, which is how you work out a new
drawing's column positions before writing an extractor for it.
"""

import argparse
import csv
import collections
import sys
from pathlib import Path

DROPBOX = Path.home() / "Dropbox" / "N720AK" / "Schematics"
REPO = Path(__file__).resolve().parent.parent

COLUMNS = ["sheet", "net", "from_ref", "from_pin", "to_ref", "to_pin",
           "color", "awg", "notes", "review"]


def load_words(pdf):
    """De-duplicated (x, y, text). These drawings stamp text several times."""
    import pymupdf
    page = pymupdf.open(pdf)[0]
    seen, out = set(), []
    for x0, y0, _x1, _y1, t, *_ in page.get_text("words"):
        key = (round(x0, 1), round(y0, 1), t)
        if key in seen:
            continue
        seen.add(key)
        out.append((x0, y0, t))
    return out


def rows_by_y(words, gap=6.0):
    """Group words into visual rows by clustering on y.

    Fixed-width bucketing splits a row whose label sits a few points above its
    data -- which is how the VP-X J10-8 destination was lost on first pass.
    Cluster on the gap between successive y values instead.
    """
    out, cur, last = {}, [], None
    for x, y, t in sorted(words, key=lambda w: (w[1], w[0])):
        if last is not None and y - last > gap:
            out[cur[0][0]] = sorted((xx, tt) for _, xx, tt in cur)
            cur = []
        cur.append((y, x, t))
        last = y
    if cur:
        out[cur[0][0]] = sorted((xx, tt) for _, xx, tt in cur)
    return out


def col(row, lo, hi):
    """The single token in a row whose x falls in [lo, hi), else None."""
    hits = [t for x, t in row if lo <= x < hi]
    return hits[0] if len(hits) == 1 else (hits[0] if hits else None)


# ---------------------------------------------------------------------------
# MH Oxygen  --  Mountain High control head (DB25) to five distribution heads
# ---------------------------------------------------------------------------

def extract_mh_oxygen(pdf):
    words = load_words(pdf)
    rows = rows_by_y(words)

    # Each DB9 group is introduced by a "DB9" label; its name appears a little
    # below. Walk the page top-down and remember which group we are inside.
    groups = []            # (y_of_DB9_label, name)
    for y, row in rows.items():
        if any(t == "DB9" for _x, t in row):
            groups.append([y, None])
        for x, t in row:
            if x > 495 and groups and groups[-1][1] is None and t.startswith("#"):
                rest = [tt for xx, tt in row if xx > 495]
                groups[-1][1] = " ".join(rest).replace("# ", "#")
            elif x > 495 and t == "REGULATOR" and groups and groups[-1][1] is None:
                groups[-1][1] = "REGULATOR"

    def group_for(y):
        name = None
        for gy, gname in groups:
            if gy <= y:
                name = gname
        return name or "UNKNOWN"

    REF = {"#1 - PILOT": "O2-HEAD-1-PILOT", "#2 COPILOT": "O2-HEAD-2-COPILOT",
           "#3 PASS 1": "O2-HEAD-3-PASS1", "#4 PASS 2": "O2-HEAD-4-PASS2",
           "REGULATOR": "O2-REGULATOR"}

    out = []
    for y, row in rows.items():
        left_pin   = col(row, 125, 140)
        left_col   = col(row, 160, 200)
        right_col  = col(row, 425, 450)
        right_pin  = col(row, 472, 495)
        off_left   = [t for x, t in row if x < 120]
        off_right  = [t for x, t in row if 210 < x < 400]

        # a wire landing on one of the DB9 distribution heads
        if right_pin and right_pin.isdigit() and right_col:
            gname = group_for(y)
            review = ""
            notes = ""
            from_ref = "O2-CTRL-HEAD" if left_pin else ""
            from_pin = left_pin or ""
            if not left_pin:
                # Resolved by reading the rendered drawing; the text layer alone
                # cannot express a junction dot or a shield drain.
                key = (REF.get(gname, gname), right_pin)
                if right_pin == "1" and (right_col or "") == "Grn":
                    from_ref, from_pin = "O2-CABLE-SHIELD", "drain"
                    notes = ("cable shield drain. The shield runs back to the "
                             "control head end and bonds to case ground (CG).")
                elif key == ("O2-REGULATOR", "9"):
                    from_ref, from_pin = "O2-CTRL-HEAD", "19"
                    notes = ("junction dot on the DB9-2 wire: regulator pins 2 "
                             "and 9 are both fed from DB25-19.")
                elif key == ("O2-REGULATOR", "6"):
                    from_ref, from_pin = "O2-CTRL-HEAD", "2"
                    notes = ("junction dot at DB25-2: shared with "
                             "O2-HEAD-4-PASS2 pin 2.")
                else:
                    review = ("no DB25 pin on this row and no known resolution "
                              "- confirm against the drawing")
            out.append(dict(
                sheet="O2", net="",
                from_ref=from_ref, from_pin=from_pin,
                to_ref=REF.get(gname, gname), to_pin=right_pin,
                color=right_col or left_col or "", awg="",
                notes=notes, review=review))
            continue

        # a wire leaving the drawing (arrow to a named destination)
        if left_pin and left_pin.isdigit() and (off_left or off_right):
            dest = " ".join(off_right) if off_right else " ".join(
                t for t in off_left if t not in ("Red", "Blk", "Wht"))
            colour = left_col or next(
                (t for t in off_left if t in ("Red", "Blk", "Wht")), "")
            out.append(dict(
                sheet="O2", net="",
                from_ref="O2-CTRL-HEAD", from_pin=left_pin,
                to_ref=dest.strip(), to_pin="",
                color=colour, awg="",
                notes="off-drawing reference", review=""))
    return out


EXTRACTORS = {"O2": ("MH_Oxygen.pdf", extract_mh_oxygen)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dump", metavar="PDF", help="print the word layout and exit")
    ap.add_argument("--sheet", choices=sorted(EXTRACTORS), help="extract one sheet")
    ap.add_argument("--out", help="output TSV (default wiring/<sheet>.tsv)")
    a = ap.parse_args()

    if a.dump:
        for y, row in rows_by_y(load_words(a.dump)).items():
            print(f"y~{y:7.0f}: " + " | ".join(f"{t}@{x:.0f}" for x, t in row))
        return 0

    if not a.sheet:
        ap.error("give --sheet or --dump")

    name, fn = EXTRACTORS[a.sheet]
    pdf = DROPBOX / name
    if not pdf.exists():
        print(f"error: {pdf} not found", file=sys.stderr)
        return 1
    rows = fn(pdf)
    out = Path(a.out) if a.out else REPO / "wiring" / f"{a.sheet}.tsv"
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS, delimiter="\t")
        w.writeheader()
        w.writerows(rows)
    flagged = sum(1 for r in rows if r["review"])
    print(f"{out}: {len(rows)} wires, {flagged} flagged for review")
    return 0


if __name__ == "__main__":
    sys.exit(main())
