#!/usr/bin/env python3
"""
As-drawn plus recorded changes equals as-built.

`wiring/<SHEET>.tsv` is what the 2017 SteinAir drawings say. The airplane has
been modified since. `wiring/changes.tsv` records each modification as a
dated, numbered change; applying them in order gives the wiring as it is in
the airplane today, written to `wiring/as-built/<SHEET>.tsv`. The KiCad sheets
are drawn from the as-built lists.

Actions:

  add         a new wire, ref:pin -> to_ref:to_pin
  remove      the wire between ref:pin and to_ref:to_pin
  disconnect  take ref:pin out of whatever net it is in. Everything else in
              that net stays connected -- wire lists store a net as a star
              from one pin, so deleting that pin's rows would otherwise split
              the rest of the net apart
  rename      replace the text `ref` with `to_ref` in every connector and
              destination name on the sheet (a box swapped for a successor)

A change that matches nothing is an error. That is deliberate: if an extractor
is re-run and a change no longer applies, the build stops instead of silently
drawing the old wiring.

Only changes with status `done` are applied. `planned` changes are recorded
for the plan but do not alter the as-built drawings.

  uv run python3 scripts/wirelist_changes.py            # write every as-built sheet
  uv run python3 scripts/wirelist_changes.py --diff SV  # show what changes did to SV
"""

import argparse
import csv
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
WIRING = REPO / "wiring"
COLUMNS = ["sheet", "net", "from_ref", "from_pin", "to_ref", "to_pin",
           "color", "awg", "protection", "notes", "review"]


class ChangeError(Exception):
    pass


def read(path):
    return list(csv.DictReader(open(path), delimiter="\t"))


def changes():
    p = WIRING / "changes.tsv"
    return read(p) if p.exists() else []


def sheets():
    names = {p.stem for p in WIRING.glob("*.tsv") if p.stem != "changes"}
    names |= {c["sheet"] for c in changes()}
    return sorted(names)


def _node(ref, pin):
    return (ref.strip(), pin.strip())


def _ends(r):
    return _node(r["from_ref"], r["from_pin"]), _node(r["to_ref"], r["to_pin"])


def _tag(r, c):
    r = dict(r)
    note = f'{c["id"]}: {c["notes"]}'.strip().rstrip(":")
    r["notes"] = (r["notes"] + "  |  " if r.get("notes") else "") + note
    return r


def apply(sheet, rows):
    rows = [dict(r) for r in rows]
    for c in changes():
        if c["sheet"] != sheet or c["status"] != "done":
            continue
        act, me = c["action"], _node(c["ref"], c["pin"])
        if act == "add":
            rows.append(_tag(dict(
                sheet=sheet, net=c.get("net", ""), from_ref=c["ref"], from_pin=c["pin"],
                to_ref=c["to_ref"], to_pin=c["to_pin"], color=c["color"], awg=c["awg"],
                protection=c["protection"], notes="", review=c.get("review", "")), c))
        elif act == "remove":
            other = _node(c["to_ref"], c["to_pin"])
            keep = [r for r in rows if set(_ends(r)) != {me, other}]
            if len(keep) == len(rows):
                raise ChangeError(f'{c["id"]}: no wire between {me} and {other} on {sheet}')
            rows = keep
        elif act == "disconnect":
            hit = [r for r in rows if me in _ends(r)]
            if not hit:
                raise ChangeError(f'{c["id"]}: {me} is not on any wire on {sheet}')
            rows = [r for r in rows if me not in _ends(r)]
            others = []
            for r in hit:
                a, b = _ends(r)
                others.append((b if a == me else a, r))
            # re-join the rest of the net to its first remaining member
            hub = others[0][0]
            for node, r in others[1:]:
                nr = dict(r)
                nr["from_ref"], nr["from_pin"] = hub
                nr["to_ref"], nr["to_pin"] = node
                if c.get("net"):
                    nr["net"] = c["net"]
                rows.append(_tag(nr, dict(c, notes=f"re-joined after {me[0]}:{me[1]} was disconnected")))
        elif act == "rename":
            n = 0
            for r in rows:
                for k in ("from_ref", "to_ref"):
                    if c["ref"] in r[k]:
                        r[k] = r[k].replace(c["ref"], c["to_ref"])
                        n += 1
            if not n:
                raise ChangeError(f'{c["id"]}: "{c["ref"]}" does not appear on {sheet}')
        else:
            raise ChangeError(f'{c["id"]}: unknown action {act!r}')
    return rows


def as_built(sheet):
    src = WIRING / f"{sheet}.tsv"
    return apply(sheet, read(src) if src.exists() else [])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--diff", metavar="SHEET")
    a = ap.parse_args()
    if a.diff:
        before = read(WIRING / f"{a.diff}.tsv") if (WIRING / f"{a.diff}.tsv").exists() else []
        after = as_built(a.diff)
        key = lambda r: (r["from_ref"], r["from_pin"], r["to_ref"], r["to_pin"])
        b, f = {key(r) for r in before}, {key(r) for r in after}
        for k in sorted(b - f):
            print("  -", ":".join(k[:2]), "->", ":".join(k[2:]))
        for k in sorted(f - b):
            print("  +", ":".join(k[:2]), "->", ":".join(k[2:]))
        return 0
    out = WIRING / "as-built"
    out.mkdir(exist_ok=True)
    try:
        for s in sheets():
            rows = as_built(s)
            with open(out / f"{s}.tsv", "w", newline="") as fh:
                w = csv.DictWriter(fh, fieldnames=COLUMNS, delimiter="\t", extrasaction="ignore")
                w.writeheader()
                w.writerows(rows)
            n = sum(1 for c in changes() if c["sheet"] == s and c["status"] == "done")
            print(f"wiring/as-built/{s}.tsv: {len(rows)} rows, {n} changes applied")
    except ChangeError as e:
        print("error:", e, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
