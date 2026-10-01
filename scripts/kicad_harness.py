#!/usr/bin/env python3
"""
Generate a KiCad 10 schematic sheet from a wire-list TSV, then prove it.

The wire list (`wiring/<SHEET>.tsv`) is the source of truth; this produces a
drawing *of* it. Each connector becomes a generated symbol carrying only the
pins the harness uses. Destinations that leave the sheet become global labels,
named the way Vern Little's drawings name them. Every wire gets its own
vertical routing channel, so no two wires can meet except where the wire list
says they do.

Then it closes the loop: exports the netlist with kicad-cli and diffs it,
node set by node set, against the wire list it was generated from. A sheet is
only correct if that diff is clean.

  uv run python3 scripts/kicad_harness.py O2            # build + verify
  uv run python3 scripts/kicad_harness.py O2 --render   # also write a PNG

Format notes learned from flyonspeed/OnSpeed-Gen3-hardware (kicad/gen/):
  * target `(version 20251024)` -- KiCad 10
  * every symbol used must be embedded in `lib_symbols` keyed by its FULL
    lib_id, or KiCad cannot resolve pins and the netlist comes out empty
  * keep everything on the 1.27 mm grid so pin ends land on grid

Two choices that are deliberate, not cosmetic:
  * Wire colour is drawn as plain text, never as a net label. In KiCad two
    labels with the same text join their nets, so labelling two different
    wires `Wht` would silently short them.
  * The drawing carries no connectivity the wire list doesn't. If something
    looks wrong here, fix the wire list (or its extractor), not the sheet.
"""

import argparse
import collections
import csv
import os
import re
import subprocess
import sys
import tempfile
import uuid
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
KCLI = "/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli"
LIB = "n720ak"
GRID = 1.27
PITCH = 2.54          # pin spacing
PIN_LEN = 2.54
BODY_W = 15.24


NS = uuid.UUID("5b2f6c1e-7a0d-4c3e-9f1a-720a720a720a")
_uid = {"key": "", "n": 0}


def U():
    """Deterministic UUIDs. A generated file that drew fresh random UUIDs on
    every run would show every line changed in git each time it was
    regenerated, burying the real differences."""
    _uid["n"] += 1
    return str(uuid.uuid5(NS, f'{_uid["key"]}:{_uid["n"]}'))


def reset_uids(key):
    _uid["key"], _uid["n"] = key, 0


ROOT_UUID = str(uuid.uuid5(NS, "n720ak-root"))


def sheet_block_uuid(sheet):
    return str(uuid.uuid5(NS, f"sheet-block:{sheet}"))


def g(v):
    """Snap to the 1.27 mm grid."""
    return round(round(v / GRID) * GRID, 2)


def esc(s):
    return s.replace("\\", "\\\\").replace('"', '\\"')


def pin_no(pin):
    """KiCad rewrites spaces in pin numbers; avoid them up front."""
    return pin.replace(" ", "_")


def unescape(s):
    """Undo KiCad's netlist escaping of label names."""
    for a, b in (("{slash}", "/"), ("{dblquote}", '"'), ("{backslash}", "\\"), ("{colon}", ":")):
        s = s.replace(a, b)
    return s


def sym_id(name):
    return re.sub(r"[^A-Za-z0-9_.+-]", "_", name)


# ---------------------------------------------------------------------------
# Reading the wire list
# ---------------------------------------------------------------------------

def load_rows(sheet):
    """The AS-BUILT wire list: the drawing's extraction with every recorded
    change in wiring/changes.tsv applied (see scripts/wirelist_changes.py).
    The drawings show the airplane as it is, not as it was in 2017."""
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import wirelist_changes
    rows = wirelist_changes.as_built(sheet)
    # rows still under review, and region placeholders, are not drawn
    return [r for r in rows if not r["review"] and r["from_ref"] and r["to_ref"]], None


def endpoints(r):
    a = ("pin", r["from_ref"], r["from_pin"]) if r["from_pin"] else ("label", r["from_ref"], "")
    b = ("pin", r["to_ref"], r["to_pin"]) if r["to_pin"] else ("label", r["to_ref"], "")
    return a, b


# ---------------------------------------------------------------------------
# Symbols
# ---------------------------------------------------------------------------

def connector_symbol(name, pins, side, ys=None):
    """A box with one pin per entry in `pins`, on the `side` facing the wires.

    By default pins sit at uniform pitch. Pass `ys` (sheet-relative offsets,
    y-down, one per pin) to place pins at chosen heights instead -- which is
    how a connector's rows are lined up with the pins they feed, so that its
    wires run straight across the sheet the way the source drawing reads.
    """
    n = len(pins)
    if ys is None:
        ys = [PITCH * (k + 1) for k in range(n)]
    lo, hi = min(ys) - PITCH, max(ys) + PITCH
    h = hi - lo
    mid = (lo + hi) / 2
    sid = sym_id(name)
    px = (BODY_W / 2 + PIN_LEN) * (1 if side == "R" else -1)
    ang = 180 if side == "R" else 0
    top = g(h / 2)
    out = [f'(symbol "{LIB}:{sid}"',
           '\t(exclude_from_sim no) (in_bom yes) (on_board yes)',
           f'\t(property "Reference" "J" (at 0 {g(top + 2.54)} 0) (effects (font (size 1.27 1.27))))',
           f'\t(property "Value" "{esc(name)}" (at 0 {g(-top - 2.54)} 0) (effects (font (size 1.27 1.27))))',
           '\t(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))',
           '\t(property "Datasheet" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))',
           f'\t(symbol "{sid}_0_1"',
           f'\t\t(rectangle (start {-BODY_W / 2} {top}) (end {BODY_W / 2} {-top})',
           '\t\t\t(stroke (width 0.254) (type default)) (fill (type background))))',
           f'\t(symbol "{sid}_1_1"']
    pos = {}
    for (pin, label), yy in zip(pins, ys):
        y = g(mid - yy)                     # library space is y-up, centred on the body
        pos[pin] = (px, y)
        out.append(f'\t\t(pin passive line (at {px} {y} {ang}) (length {PIN_LEN})'
                   f' (name "{esc(label)}" (effects (font (size 1.0 1.0))))'
                   f' (number "{esc(pin_no(pin))}" (effects (font (size 1.0 1.0)))))')
    out.append('\t)')
    out.append(')')
    return "\n".join(out), pos, h, mid


# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------

def build(sheet, rows, title, layout="aligned", index=1):
    reset_uids(f"{sheet}:{layout}")
    # which connectors, which pins, and which side of the page
    pins = collections.OrderedDict()
    left_votes = collections.Counter()
    pin_name = {}
    for r in rows:
        for (kind, ref, pin), is_from in zip(endpoints(r), (True, False)):
            if kind != "pin":
                continue
            pins.setdefault(ref, [])
            if pin not in pins[ref]:
                pins[ref].append(pin)
            left_votes[ref] += 1 if is_from else -1
            if is_from and r.get("net"):
                pin_name.setdefault((ref, pin), r["net"])
    flags_on = collections.Counter()
    for r in rows:
        a, b = endpoints(r)
        if (a[0] == "pin") != (b[0] == "pin"):
            p = a if a[0] == "pin" else b
            flags_on[(p[1], p[2])] += 1
    left = [c for c in pins if left_votes[c] > 0]
    right = [c for c in pins if left_votes[c] <= 0]

    libs, inst, wires, labels, texts = [], [], [], [], []
    root = U()
    world = {}                    # (ref, pin) -> (x, y) connection point
    refdes = {}

    def emit(c, x, yc, body, pos, h):
        libs.append(body)
        rd = f"J{index}{len(refdes) + 1:02d}"     # unique across the whole project
        refdes[c] = rd
        inst.append(
            f'\t(symbol (lib_id "{LIB}:{sym_id(c)}") (at {x} {yc} 0) (unit 1)\n'
            f'\t\t(in_bom yes) (on_board yes) (dnp no) (uuid "{U()}")\n'
            f'\t\t(property "Reference" "{rd}" (at {x} {g(yc - h / 2 - 2.54)} 0) '
            f'(effects (font (size 1.27 1.27))))\n'
            f'\t\t(property "Value" "{esc(c)}" (at {x} {g(yc + h / 2 + 2.54)} 0) '
            f'(effects (font (size 1.27 1.27))))\n'
            f'\t\t(instances (project "n720ak"\n'
            f'\t\t\t(path "/{root}" (reference "{rd}") (unit 1))\n'
            f'\t\t\t(path "/{ROOT_UUID}/{sheet_block_uuid(sheet)}" (reference "{rd}") (unit 1)))))')
        for p, (px, py) in pos.items():
            world[(c, p)] = (g(x + px), g(yc - py))     # library is y-up, sheet is y-down

    def place_stacked(cols, x, side, y0):
        y = y0
        for c in cols:
            plist = [(p, pin_name.get((c, p), "")) for p in pins[c]]
            # A pin carrying several off-sheet flags reserves a spare row per
            # extra flag, so each flag gets its own line instead of overprinting.
            ys, row = [], 1
            for p, _ in plist:
                ys.append(PITCH * row)
                row += max(1, flags_on[(c, p)])
            body, pos, h, _mid = connector_symbol(c, plist, side, ys)
            yc = g(y + h / 2)
            emit(c, x, yc, body, pos, h)
            y = g(yc + h / 2 + 7.62)
        return y

    def place_aligned(c, x, side, y0):
        """Put each pin at the height of the pin it feeds on the other column."""
        partner = {}
        for r in rows:
            a, b = endpoints(r)
            for me, other in ((a, b), (b, a)):
                if me[0] == "pin" and me[1] == c and other[0] == "pin" and (other[1], other[2]) in world:
                    partner.setdefault(me[2], world[(other[1], other[2])][1])
        wanted = sorted(((partner.get(p), k, p) for k, p in enumerate(pins[c])),
                        key=lambda t: (t[0] is None, t[0] if t[0] is not None else 0, t[1]))
        taken, ys = [], {}
        for want, k, p in wanted:
            if want is None:
                continue
            y = want
            while any(abs(y - u) < PITCH - 0.01 for u in taken):
                y = g(y + PITCH)
            taken.append(y); ys[p] = y
        # pins with no partner (off-sheet labels): fill gaps in their original order
        free = [p for p in pins[c] if p not in ys]
        cursor = g(min(taken) - PITCH) if taken else y0
        for p in free:
            # prefer the gap just after the previous pin in drawing order
            k = pins[c].index(p)
            prev = [ys[q] for q in pins[c][:k] if q in ys]
            y = g(prev[-1] + PITCH) if prev else cursor
            while any(abs(y - u) < PITCH - 0.01 for u in taken):
                y = g(y + PITCH)
            taken.append(y); ys[p] = y
        order = sorted(pins[c], key=lambda p: ys[p])
        top = min(ys.values())
        plist = [(p, pin_name.get((c, p), "")) for p in order]
        body, pos, h, mid = connector_symbol(c, plist, side, [ys[p] - top + PITCH for p in order])
        yc = g(top - PITCH + h / 2)
        emit(c, x, yc, body, pos, h)
        return g(yc + h / 2 + 7.62)

    XL = 50.8
    lane_start = g(XL + BODY_W / 2 + PIN_LEN + 45.72)
    n_lanes = sum(1 for r in rows if r["from_pin"] and r["to_pin"])
    # The right column must clear the last routing lane, or lanes run through
    # its pins and fuse nets. Leave room for right-side label flags too.
    XR = g(lane_start + n_lanes * 2.54 + 45.72 + BODY_W)
    if layout == "aligned":
        # one connector on the left: line its rows up with the pins they feed
        place_stacked(right, XR, "L", 40.64)
        y = 40.64
        for c in left:
            y = place_aligned(c, XL, "R", y)
    else:
        # Stacked, with the right column offset by half a pitch so that no two
        # pins anywhere on the sheet share a y. With every wire in its own
        # vertical lane, two wires can then only meet where they share a pin --
        # accidental contact is impossible rather than merely unlikely.
        place_stacked(left, XL, "R", 40.64)
        place_stacked(right, XR, "L", g(40.64 + GRID))

    # one vertical channel per wire, between the two columns
    lane = [lane_start]

    def next_lane():
        x = lane[0]
        lane[0] = g(x + 2.54)
        return x

    def seg(a, b):
        if a != b:
            wires.append(f'\t(wire (pts (xy {a[0]} {a[1]}) (xy {b[0]} {b[1]})) '
                         f'(stroke (width 0) (type default)) (uuid "{U()}"))')

    def glabel(name, x, y, rot, justify):
        labels.append(f'\t(global_label "{esc(name)}" (shape bidirectional) (at {x} {y} {rot})\n'
                      f'\t\t(effects (font (size 1.27 1.27)) (justify {justify})) (uuid "{U()}"))')

    def note(s, x, y):
        texts.append(f'\t(text "{esc(s)}" (at {x} {y} 0) '
                     f'(effects (font (size 1.0 1.0)) (justify left bottom)) (uuid "{U()}"))')

    n_flags = collections.Counter()
    # Rows with a named destination at BOTH ends (a bus bar feeding a device
    # that is not drawn as a connector) have no pin to hang off. Draw each as
    # two global labels joined by a short wire, below the connectors.
    loose_y = [g(max([p[1] for p in world.values()] or [40.64]) + 15.24)]
    for r in rows:
        a, b = endpoints(r)
        if a[0] == "label" and b[0] == "label":
            y = loose_y[0]
            loose_y[0] = g(y + 5.08)
            x0, x1 = g(XL + 20.32), g(XL + 60.96)
            seg((x0, y), (x1, y))
            glabel(a[1], x0, y, 180, "right")
            glabel(b[1], x1, y, 0, "left")
            tag = " ".join(v for v in (r["color"], (r["awg"] + " AWG") if r["awg"] else "",
                                       r["protection"]) if v)
            if tag:
                note(tag, g(x0 + 2.54), g(y - 0.6))
    for r in rows:
        a, b = endpoints(r)
        if a[0] == "label" and b[0] == "label":
            continue
        tag = " ".join(t for t in (r["color"], (r["awg"] + " AWG") if r["awg"] else "") if t)
        if a[0] == "pin" and b[0] == "pin":
            pa, pb = world[(a[1], a[2])], world[(b[1], b[2])]
            if pa[0] > pb[0]:
                pa, pb = pb, pa
            if pa[1] == pb[1]:
                seg(pa, pb)
            else:
                cx = next_lane()
                seg(pa, (cx, pa[1])); seg((cx, pa[1]), (cx, pb[1])); seg((cx, pb[1]), pb)
            if tag:
                note(tag, g(pa[0] + 2.54), g(pa[1] - 0.6))
        else:
            pin_end, lab = (a, b) if a[0] == "pin" else (b, a)
            px, py = world[(pin_end[1], pin_end[2])]
            on_left = pin_end[1] in left
            d = 1 if on_left else -1
            stub = g(px + d * 10.16)
            k = n_flags[(pin_end[1], pin_end[2])]
            n_flags[(pin_end[1], pin_end[2])] += 1
            if k == 0:
                seg((px, py), (stub, py))
                ly = py
            else:
                # A second or third flag on the same pin branches off the first
                # stub into the spare row reserved beneath the pin.
                tap = g(px + d * 5.08)
                ly = g(py + k * PITCH)            # into the row reserved below
                seg((tap, py), (tap, ly))
                seg((tap, ly), (stub, ly))
            glabel(lab[1], stub, ly, 0 if on_left else 180, "left" if on_left else "right")
            if tag and k == 0:
                note(tag, g(min(px, stub) + 1.27), g(py - 0.6))

    # Junction dots wherever three or more wire ends meet, or a wire ends on
    # another wire's run. KiCad connects a T without one, but a reader
    # shouldn't have to infer it.
    pts = []
    for w in wires:
        m = re.findall(r"\(xy ([\d.-]+) ([\d.-]+)\)", w)
        pts.append(((float(m[0][0]), float(m[0][1])), (float(m[1][0]), float(m[1][1]))))
    ends = collections.Counter(p for s in pts for p in s)
    pinpts = set(world.values())
    dots = set()
    for p, n in ends.items():
        hits = n + sum(1 for a, b in pts if p not in (a, b) and
                       ((a[1] == b[1] == p[1] and min(a[0], b[0]) < p[0] < max(a[0], b[0])) or
                        (a[0] == b[0] == p[0] and min(a[1], b[1]) < p[1] < max(a[1], b[1]))))
        if hits >= 3 or (hits >= 2 and p not in pinpts and n == 1):
            dots.add(p)
    junctions = [f'\t(junction (at {x} {y}) (diameter 0) (color 0 0 0 0) (uuid "{U()}"))'
                 for x, y in sorted(dots)]

    ys = [p[1] for p in world.values()] + [loose_y[0]]
    W = max(420, int(XR + BODY_W + 60))
    H = max(297, int(max(ys) + 60))
    paper = '"A3"' if (W, H) == (420, 297) else f'"User" {W} {H}'

    text = (
        '(kicad_sch\n\t(version 20251024)\n\t(generator "n720ak_kicad_harness")\n'
        '\t(generator_version "10.0")\n'
        f'\t(uuid "{root}")\n\t(paper {paper})\n'
        f'\t(title_block (title "{esc(title)}") (company "N720AK -- Van\'s RV-10") '
        f'(comment 1 "Generated from wiring/{sheet}.tsv -- edit the wire list, not this sheet"))\n'
        '\t(lib_symbols\n' + "\n".join("\t\t" + ln for b in libs for ln in b.splitlines()) + '\n\t)\n'
        + "\n".join(inst + wires + junctions + labels + texts) +
        '\n\t(sheet_instances (path "/" (page "1")))\n)\n')
    return text, refdes


# ---------------------------------------------------------------------------
# Verification: the generated netlist must match the wire list exactly
# ---------------------------------------------------------------------------

def expected_nets(rows):
    """Connected groups implied by the wire list, as frozensets of nodes."""
    parent = {}

    def f(a):
        parent.setdefault(a, a)
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    for r in rows:
        a, b = endpoints(r)
        parent[f(a)] = f(b)
    groups = collections.defaultdict(set)
    for n in list(parent):
        groups[f(n)].add(n)
    out = set()
    for g_ in groups.values():
        out.add(frozenset((k, ref, pin) if k == "pin" else ("label", ref, "") for k, ref, pin in g_))
    return out


def actual_nets(netfile, refdes, rows):
    """Connected groups in the exported netlist, translated back to wire-list names."""
    back = {v: k for k, v in refdes.items()}
    unpin = {}
    for r in rows:
        for ref, pin in ((r["from_ref"], r["from_pin"]), (r["to_ref"], r["to_pin"])):
            if pin:
                unpin[(ref, pin_no(pin))] = pin
    s = open(netfile).read()
    out = set()
    for m in re.finditer(r'\(net\s*\(code "\d+"\)\s*\(name "([^"]*)"\)(.*?)\n\t\t\)', s, re.S):
        name, body = m.group(1), m.group(2)
        nodes = set()
        for nm in re.finditer(r'\(ref "([^"]+)"\)\s*\(pin "([^"]+)"\)', body):
            ref = back.get(nm.group(1), nm.group(1))
            nodes.add(("pin", ref, unpin.get((ref, nm.group(2)), nm.group(2))))
        lab = unescape(name.lstrip("/"))
        if not lab.startswith("Net-") and not lab.startswith("unconnected"):
            nodes.add(("label", lab, ""))
        if nodes:
            out.add(frozenset(nodes))
    return out


def verify(sch, rows, refdes, quiet=False):
    with tempfile.TemporaryDirectory() as td:
        net = os.path.join(td, "out.net")
        r = subprocess.run([KCLI, "sch", "export", "netlist", "--format", "kicadsexpr", "-o", net, str(sch)],
                           capture_output=True, text=True)
        if r.returncode != 0:
            print("netlist export FAILED:", r.stderr or r.stdout)
            return False
        exp, act = expected_nets(rows), actual_nets(net, refdes, rows)
    pins_only = lambda nets: {frozenset(n for n in s if n[0] == "pin") for s in nets} - {frozenset()}
    missing, extra = pins_only(exp) - pins_only(act), pins_only(act) - pins_only(exp)
    # A net with several off-sheet labels is named by only one of them in the
    # netlist, so labels are checked separately: every expected label must name
    # the KiCad net that holds its pins.
    act_name = {frozenset(n for n in s if n[0] == "pin"): {n[1] for n in s if n[0] == "label"} for s in act}
    bad_labels = []
    for s in exp:
        pins = frozenset(n for n in s if n[0] == "pin")
        want = {n[1] for n in s if n[0] == "label"}
        if want and pins in act_name and not (want & act_name[pins]):
            bad_labels.append((sorted(want), sorted(act_name[pins])))
    if quiet:
        return not missing and not extra and not bad_labels
    print(f"  wire list : {len(exp)} nets")
    print(f"  KiCad     : {len(act)} nets")
    if not missing and not extra and not bad_labels:
        print("  CLEAN -- the drawing's connectivity matches the wire list exactly")
        return True
    for w, got in bad_labels:
        print("  label mismatch: expected one of", w, "got", got)
    for m in sorted(missing, key=str):
        print("  missing from drawing:", sorted(m))
    for e in sorted(extra, key=str):
        print("  extra in drawing    :", sorted(e))
    return False


TITLES = {"O2": "Mountain High Oxygen", "PWR": "Power & Lighting", "SV": "SkyView Interconnect",
          "EMS": "Engine Monitoring", "ONSPEED": "OnSpeed AoA"}
ORDER = ["PWR", "SV", "O2", "ONSPEED", "EMS"]


def write_project(sheets):
    """Root sheet plus a minimal project file, tying the sheets into one
    hierarchical KiCad project. Global labels with the same name on different
    sheets join -- which is how an off-sheet flag like `AG` means the same net
    everywhere, the way Vern's SHEET/NET references do."""
    d = REPO / "kicad" / "n720ak"
    blocks = []
    for k, s in enumerate(sheets):
        x, y = 30 + (k % 4) * 90, 40 + (k // 4) * 60
        blocks.append(
            f'\t(sheet (at {x} {y}) (size 70 35) (fields_autoplaced yes)\n'
            f'\t\t(stroke (width 0.1524) (type solid)) (fill (color 0 0 0 0.0000))\n'
            f'\t\t(uuid "{sheet_block_uuid(s)}")\n'
            f'\t\t(property "Sheetname" "{esc(TITLES.get(s, s))}" (at {x} {y - 1} 0)\n'
            f'\t\t\t(effects (font (size 1.27 1.27)) (justify left bottom)))\n'
            f'\t\t(property "Sheetfile" "{s}.kicad_sch" (at {x} {y + 36} 0)\n'
            f'\t\t\t(effects (font (size 1.27 1.27)) (justify left top)))\n'
            f'\t\t(instances (project "n720ak" (path "/{ROOT_UUID}" (page "{k + 2}")))))')
    (d / "n720ak.kicad_sch").write_text(
        '(kicad_sch\n\t(version 20251024)\n\t(generator "n720ak_kicad_harness")\n'
        '\t(generator_version "10.0")\n'
        f'\t(uuid "{ROOT_UUID}")\n\t(paper "A3")\n'
        '\t(title_block (title "N720AK Wiring") (company "N720AK -- Van\'s RV-10") '
        '(comment 1 "Generated from wiring/*.tsv -- edit the wire lists, not these sheets"))\n'
        '\t(lib_symbols)\n' + "\n".join(blocks) +
        '\n\t(sheet_instances (path "/" (page "1")))\n)\n')
    (d / "n720ak.kicad_pro").write_text(
        '{\n  "meta": {"filename": "n720ak.kicad_pro", "version": 3},\n'
        '  "schematic": {"legacy_lib_dir": "", "legacy_lib_list": []},\n'
        '  "sheets": [' + ", ".join(f'["{sheet_block_uuid(s)}", "{TITLES.get(s, s)}"]' for s in sheets) +
        ']\n}\n')
    return d / "n720ak.kicad_sch"


def make_sheet(sheet, index, render):
    rows, _src = load_rows(sheet)
    out = REPO / "kicad" / "n720ak" / f"{sheet}.kicad_sch"
    out.parent.mkdir(parents=True, exist_ok=True)
    # Prefer rows lined up across the sheet; keep it only if it verifies.
    for layout in ("aligned", "stacked"):
        text, refdes = build(sheet, rows, TITLES.get(sheet, sheet), layout, index)
        out.write_text(text)
        if verify(out, rows, refdes, quiet=True):
            break
    print(f"{out.relative_to(REPO)}: {len(refdes)} connectors, {len(rows)} wires, layout={layout}")
    ok = verify(out, rows, refdes)
    r = subprocess.run([KCLI, "sch", "erc", "--severity-error", "-o", "/dev/stdout", str(out)],
                       capture_output=True, text=True)
    errs = re.search(r"\*\* ERC messages: (\d+)", r.stdout)
    print(f"  ERC errors: {errs.group(1) if errs else '?'}")
    if render:
        pdf = out.with_suffix(".pdf")
        subprocess.run([KCLI, "sch", "export", "pdf", "-o", str(pdf), str(out)], capture_output=True)
        print(f"  rendered {pdf.relative_to(REPO)}")
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("sheets", nargs="*", help="sheets to build (default: all)")
    ap.add_argument("--render", action="store_true")
    a = ap.parse_args()
    sheets = a.sheets or ORDER
    ok = True
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import wirelist_changes
    try:
        wirelist_changes.main.__wrapped__ if False else None
        for s in ORDER:
            wirelist_changes.as_built(s)          # fail fast on a stale change
    except wirelist_changes.ChangeError as e:
        print("error:", e)
        return 1
    built = [s for s in sheets if load_rows(s)[0]]
    for s in sheets:
        if s not in built:
            print(f"{s}: nothing drawable yet (every row is flagged for review) - skipped")
    sheets = built
    for s in sheets:
        ok &= make_sheet(s, ORDER.index(s) + 1 if s in ORDER else 9, a.render)
    if not a.sheets:
        root = write_project([s for s in ORDER if s in sheets])
        with tempfile.TemporaryDirectory() as td:
            net = os.path.join(td, "all.net")
            r = subprocess.run([KCLI, "sch", "export", "netlist", "--format", "kicadsexpr", "-o", net, str(root)],
                               capture_output=True, text=True)
            s = open(net).read() if os.path.exists(net) else ""
        comps = len(re.findall(r"\(comp\s*\n?\s*\(ref ", s))
        nets = len(re.findall(r"\(net\s*\n?\s*\(code ", s))
        warn = (r.stderr or r.stdout).strip()
        print(f"\nproject {root.relative_to(REPO)}: {comps} connectors, {nets} nets across "
              f"{len(sheets)} sheets" + (f"  [kicad-cli: {warn}]" if warn else ""))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
