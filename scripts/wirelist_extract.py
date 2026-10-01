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
import os
import csv
import collections
import sys
from pathlib import Path

DROPBOX = Path.home() / "Dropbox" / "N720AK" / "Schematics"
REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

COLUMNS = ["sheet", "net", "from_ref", "from_pin", "to_ref", "to_pin",
           "color", "awg", "protection", "notes", "review"]


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
                    from_ref, from_pin = "CG", ""
                    notes = ("cable shield drain. Each cable's shield bonds to "
                             "case ground (CG) at the control head end, so the "
                             "drain is recorded as landing on CG.")
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
                color=right_col or left_col or "", awg="", protection="",
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
                color=colour, awg="", protection="",
                notes="off-drawing reference", review=""))
    return out



# ---------------------------------------------------------------------------
# Power & Lighting  --  SteinAir POWER & LTG, 5/19/2017
#
# Not one table but several regions on a 40" sheet. Parsed here:
#   * the four VP-X Sport connector tables (J1, J2, J10, J12)
#   * the pilot and copilot switch-panel DB15s
#   * the essential bus
# Not yet parsed (flagged as review rows at the end): the Bus Manager /
# battery / starter region and the annunciator panel.
# ---------------------------------------------------------------------------

COLORS = {"Red", "Blk", "Wht", "Yel", "Grn", "Blu", "Ora", "Brn", "Vio",
          "Gray", "Pur"}


def _is_color(t):
    return t.split("/")[0] in COLORS


def _vpx_rows(words, lx, y0, y1):
    """Generic VP-X table rows: pin -> label, breaker, gauge, colour."""
    import re
    sub = [w for w in words if lx - 160 <= w[0] < lx + 620 and y0 + 8 <= w[1] < y1]
    pins = sorted((y, t) for x, y, t in sub if lx + 65 <= x < lx + 100 and t.isdigit())
    out = {}
    for i, (py, pin) in enumerate(pins):
        lo = (pins[i - 1][0] + py) / 2 if i else py - 14
        hi = (py + pins[i + 1][0]) / 2 if i + 1 < len(pins) else py + 14
        win = sorted((w for w in sub if lo <= w[1] < hi), key=lambda w: w[0])
        left = [t for x, y, t in win if x < lx + 60]
        mid = [t for x, y, t in win if lx + 100 <= x < lx + 200]
        brk = next((t for t in left if re.fullmatch(r"\d+(\.\d+)?A-\d+", t)), "")
        if not brk and "EFIS" in left and "5A" in left:
            brk = "EFIS 5A"
        label = " ".join(t for t in left if t != brk and t not in ("EFIS", "5A") or not brk and False)
        out[pin] = dict(label=label,
                        breaker=brk,
                        awg=next((t for t in mid if t.isdigit()), ""),
                        color=next((t for t in mid if _is_color(t)), ""))
    return out


# Destinations, read from the drawing. The text layer holds every label, but on
# these tables a destination often spans several lines or a row feeds two
# boxes, so they are listed explicitly rather than guessed from geometry.
# Each entry: list of (destination, colour override or None, note).
VPX_DEST = {
    ("J1", "1"):  [("DEFROST FAN PWR", None, "")],
    ("J1", "2"):  [("ANN ECU FAULT PRI", None, "lamp anode, pin 1"),
                   ("ANN ECU FAULT SEC", None, "lamp anode, pin 1"),
                   ("ANN LT TEST", "Yel", "lamp-test supply: the test button's first pole")],
    ("J1", "17"): [("FLAP POSITION SENSOR", None, "flap position input; drawing spells it POSTION")],
    ("J1", "18"): [("FLAP POSITION SENSOR", None, "flap position ground")],
    ("J1", "19"): [("FLAP POSITION SENSOR", None, "flap position 2.5 V reference")],
    ("J1", "20"): [("EFIS (ALL) SERIAL 1", None, "VP-X serial TX")],
    ("J1", "22"): [("EFIS (ALL) SERIAL 1", None, "VP-X serial RX")],
    ("J2", "11"): [("STARTER CONTACTOR", None, "start annunciate; optional connection per VP-X Manual 5.7")],
    ("J2", "14"): [("FLAPS SWITCH", None, "flaps UP")],
    ("J2", "15"): [("FLAPS SWITCH", None, "flaps DOWN")],
    ("J12", "1"): [("LANDING LIGHTS POWER", None, "")],
    ("J12", "2"): [("STROBE LIGHTS POWER", None, "")],
    ("J12", "3"): [("TAXI LIGHTS POWER", None, "")],
    ("J12", "4"): [("AG", None, "avionics ground point")],
    ("J12", "5"): [("FLAP MOTOR", None, "")],
    ("J12", "6"): [("FLAP MOTOR", None, "")],
    ("J12", "7"): [("SV-COM D15-8", None, "COM 2 power")],
    ("J12", "8"): [("USB CHARGERS", None, "")],
    ("J12", "9"): [("SV-HDX800 (MFD) D37-1/20", None, ""),
                   ("ETHERNET SWITCH", "Red", "shares the MFD 5 A circuit")],
    ("J12", "10"): [("SV-A/P-PNL D15-9", None, "")],
    ("J12", "12"): [("WIGWAG POWER", None, "")],
    ("J10", "2"):  [("SV-HDX1100 (PFD2) D37-1/20", None, "")],
    ("J10", "3"):  [("CABIN LIGHTS POWER", None, "")],
    ("J10", "4"):  [("GMA245 J2-8/9", None, ""),
                    ("BOSE JACKS Pin 1", "Red", "headset jack power, shares the AUDIO 5 A circuit")],
    ("J10", "5"):  [("NAV LIGHTS POWER", None, "")],
    ("J10", "6"):  [("PITOT HEAT POWER", None, "")],
    ("J10", "7"):  [("SV-XPNDR-261 J1-15", None, ""),
                    ("SV-ADSB-470 J1-1", "Red",
                     "drawing (2017) shows the SV-ADSB-470; it was traded in for the SV-ADSB-472 on "
                     "2019-04-02 (sys-34). A recorded modification the drawing predates")],
    ("J10", "8"):  [("MH CNTRL HEAD J1-1", None, "matches O2 sheet: control head DB25-1 from VP-X J10-8"),
                    ("CO DETECT J1-1", "Red",
                     "CO Guardian, installed and powered. Its audio and EMS data wires were cut (wiring/changes.tsv)")],
    ("J10", "9"):  [("AG", None, "avionics ground point")],
    ("J10", "10"): [("PLX AIR/FUEL MODULE", None, "")],
}

# Spare / undrawn pins, deliberately not emitted as wires.
VPX_SPARE = {("J1", "21"), ("J2", "10"), ("J10", "1"), ("J12", "11")}

# The panel switches, keyed by the wire colour that leaves each one. Every
# switch output colour is unique on this drawing, which is what lets a VP-X
# switch input be traced to its switch without following the line.
SWITCH_BY_COLOR = {
    "Vio": ("PILOT", "AV MSTR"), "Vio/Blu": ("PILOT", "PITOT HEAT"),
    "Vio/Yel": ("PILOT", "NAV LTS"), "Vio/Grn": ("PILOT", "STROBE LTS"),
    "Ora": ("PILOT", "TAXI/LDG"), "Ora/Blk": ("PILOT", "TAXI/LDG"),
    "Ora/Yel": ("PILOT", "WIG-WAG"),
    "Ora/Brn": ("COPILOT", "DEF FAN"), "Brn/Yel": ("COPILOT", "CABIN LTS"),
}


def _db15_pins(words, y_lo, y_hi, x_lo, x_hi):
    """Harness-side colour and gauge on each DB15 pin, matched by x position.

    Two quirks of this drawing: a two-colour label can be broken across lines
    (`Wht/` above `Blk`), and gauge labels are sometimes lower-case (`20 red`).
    Both silently produced the wrong colour on the AV MSTR relay-coil line
    until handled here.
    """
    band = [(x, y, t) for x, y, t in words if y_lo <= y < y_hi and x_lo - 20 <= x < x_hi]
    merged, used = [], set()
    for i, (x, y, t) in enumerate(band):
        if i in used:
            continue
        if t.endswith("/"):
            j = min((k for k, (xx, yy, tt) in enumerate(band)
                     if k != i and abs(xx - x) < 10 and 0 < yy - y < 16),
                    key=lambda k: band[k][1] - y, default=None)
            if j is not None:
                used.add(j)
                t = t + band[j][2]
        merged.append((x, y, t[:1].upper() + t[1:]))
    pins = [(x, t) for x, y, t in words if 612 <= y < 620 and x_lo <= x < x_hi and t.isdigit()]
    cols = [(x, t) for x, y, t in merged if _is_color(t)]
    gauges = [(x, t) for x, y, t in merged if t.isdigit()]
    out = {}
    for px, pin in pins:
        near = sorted(cols, key=lambda c: abs(c[0] - px))
        if near and abs(near[0][0] - px) < 22:
            g = [gt for gx, gt in gauges if 0 < near[0][0] - gx < 20]
            out[pin] = (near[0][1], g[0] if g else "")
    return out


# Harness-side destinations of DB15 pins that do NOT go to a VP-X switch input
# (those are emitted once, from the VP-X side). Read from the drawing.
DB15_DEST = {
    ("PILOT", "1"):  ("AG", "switch-panel ground"),
    ("PILOT", "3"):  ("COM/NAV RELAY COILS (85)", "AV MSTR output. Traced to pin 85 of both the COM and NAV relay coils"),
    ("PILOT", "5"):  ("A/P SERVO POWER", "A/P MSTR output"),
    ("PILOT", "9"):  ("AG", "switch-panel ground"),
    ("PILOT", "10"): ("COPILOT-SW-PANEL DB15", "Switch backlighting: the copilot panel's SWITCHES dimmer output, crossing to light the pilot panel's switches. Traced"),
    ("COPILOT", "1"):  ("AG", "switch-panel ground"),
    ("COPILOT", "4"):  ("AG", "switch-panel ground"),

    ("COPILOT", "6"):  ("AG", "switch-panel ground"),

    ("COPILOT", "8"):  ("PANEL LED STRIP - PLUS", ""),
    ("COPILOT", "9"):  ("LEFT MAP LT", "WHITE"),
    ("COPILOT", "10"): ("LEFT MAP LT", "RED"),
    ("COPILOT", "11"): ("RIGHT MAP LT", "WHITE"),
    ("COPILOT", "12"): ("RIGHT MAP LT", "RED"),
    ("COPILOT", "13"): ("MH OXYGEN CONTROL HEAD", "switch dimmer; matches O2 sheet DB25-21 Yel/Grn"),
}
DB15_REVIEW = set()
# pins whose wire is emitted from the other end (the ESS bus rows)
DB15_FROM_ELSEWHERE = {("PILOT", "4"), ("COPILOT", "5"), ("COPILOT", "7")}

# The essential bus. A schematic, not a table, so transcribed from the text
# layer and checked against the rendered drawing.
#   (breaker, rating A, destination, awg, colour, note, needs_review)
ESS_BUS = [
    ("ALT FLD", "5", "ALTERNATOR FIELD", "20", "Red", "through the ALT FLD panel switch", False),
    ("ECU PRI", "5", "PRIMARY ECU PWR", "18", "Red", "through the IGN 1 panel switch; second leg runs to the ECU PWR PRI annunciator", False),
    ("ECU SEC", "5", "SECONDARY ECU PWR", "18", "Red", "through the IGN 2 panel switch; second leg runs to the ECU PWR SEC annunciator", False),
    ("PUMP 1", "10", "FUEL PUMP 1 PWR", "16", "Red",
     "NOT on the bus bar: fed from the fuel-pump changeover relay contact 87a (NC). Second leg to the FUEL PUMP 1 annunciator", False),
    ("PUMP 2", "10", "FUEL PUMP 2 PWR", "16", "Red",
     "NOT on the bus bar: fed from the fuel-pump changeover relay contact 87 (NO). Second leg to the FUEL PUMP 2 annunciator", False),
    ("IGN PWR", "15", "IGNITION PWR", "", "", "", False),
    ("PFD", "5", "SV-HDX1100 (PFD) D37-1/20", "", "", "", False),
    ("COM 1", "10", "COM RELAY 30", "18", "Red",
     "GTN COM power is relay-switched: COM relay 87 (NO) -> GTN650 P3-30,43,44, 18 Red. Coil 85 on the Wht/Blk AV MSTR line", False),
    ("NAV 1", "7.5", "NAV RELAY 30", "20", "Red",
     "GTN NAV power is relay-switched: NAV relay 87 (NO) -> GTN650 P1-19,20 and P4-51,52, 20 Red. Coil shares the Wht/Blk AV MSTR line", False),
    ("PNL LTS", "5", "COPILOT-SW-PANEL DB15:7", "", "Red",
     "copilot DB15 pin 7; inside the panel it powers all four LED dimmers (switches, panel, map L, map R). Traced", False),
    ("SERVOS", "5", "PILOT-SW-PANEL DB15:4", "20", "Red", "pilot DB15 pin 4, the A/P MSTR switch input. Traced", False),
    ("ECU PRI", "5", "D1:A", "", "Red", "second leg: annunciator ECU PWR PRI, through D1. Traced", False),
    ("ECU SEC", "5", "D2:A", "", "Red", "second leg: annunciator ECU PWR SEC, through D2. Traced", False),
    ("PUMP 1", "10", "D3:A", "", "Red", "second leg: annunciator FUEL PUMP 1, through D3. Traced", False),
    ("PUMP 2", "10", "D4:A", "", "Red", "second leg: annunciator FUEL PUMP 2, through D4. Traced", False),
]


# The Bus Manager / battery / starter region. Transcribed from the rendered
# drawing; the text layer supplies the labels and gauges but not which line
# goes where. Rows marked review are ones where two lines run close enough
# that the reading is less than certain.
#   (from_ref, from_pin, to_ref, to_pin, awg, colour, protection, note, review)
BUS_MGR = [
    ("BATT 1", "-", "AIRFRAME GROUND", "", "4", "", "", "airframe ground bus and engine case", False),
    ("BATT 2", "-", "AIRFRAME GROUND", "", "4", "", "", "airframe ground bus and engine case", False),
    ("BATT 1", "+", "START CONTACTOR 1", "BAT", "4", "", "", "", False),
    ("BATT 2", "+", "START CONTACTOR 2", "BAT", "4", "", "", "", False),
    ("START CONTACTOR 1", "OUT", "STARTER", "", "4", "", "", "", False),
    ("START CONTACTOR 2", "OUT", "STARTER", "", "4", "", "", "", False),
    ("BATT 1", "+", "BUS MANAGER", "Batt1/Alt", "10", "", "", "", False),
    ("BATT 2", "+", "BUS MANAGER", "Batt 2", "10", "", "", "", False),
    ("ALTERNATOR", "B", "ALT CURRENT LIMITER", "", "10", "", "40A", "", False),
    ("ALT CURRENT LIMITER", "", "BUS MANAGER", "Batt1/Alt", "10", "", "40A",
     "alternator output joins the Batt 1 feed at the Bus Manager", False),
    ("ALTERNATOR", "FIELD", "ALT FIELD SWITCH", "", "", "", "",
     "continues on the ESS bus ALT FLD circuit", False),
    ("BUS MANAGER", "Essential Bus Pwr", "ESSENTIAL BUS BAR", "", "10", "", "", "", False),
    ("BUS MANAGER", "Main Bus Pwr", "VP-X SPORT", "", "10", "", "", "VP-X main power feed", False),
    ("BUS MANAGER", "E-Pwr-1", "EMERG POWER SWITCH", "", "10", "", "",
     "E-Pwr-1 and E-Pwr-2 are bridged by the emergency power switch, rated 30 A minimum", False),
    ("BUS MANAGER", "E-Pwr-2", "EMERG POWER SWITCH", "", "10", "", "", "", False),
    ("BUS MANAGER", "GND", "AG", "", "16", "", "", "avionics ground point", False),
    ("BUS MANAGER", "top harness", "START CONTACTOR 1", "coil", "16", "Blk", "",
     "manufacturer-supplied harness. Traced: the Blk wire ends at Start Contactor 1's coil", False),
    ("BUS MANAGER", "top harness", "START CONTACTOR 2", "coil", "16", "Red", "",
     "manufacturer-supplied harness. Traced: the Red wire ends at Start Contactor 2's coil", False),
    ("BUS MANAGER", "top harness", "FUEL PRESS INPUT", "", "", "Pur", "",
     "fuel pressure input to the Bus Manager", False),
    ("BUS MANAGER", "top harness", "FUEL PUMP CHANGEOVER RELAY", "85", "20", "Gray", "",
     "the relay that selects PUMP 1 or PUMP 2 on the ESS bus. This is the Bus Manager's pump auto-cutover", False),
    ("KEYSWITCH", "3", "BUS MANAGER", "left harness", "", "Grn", "", "through a 2-pin connector, pin 2", False),
    ("KEYSWITCH", "1", "BUS MANAGER", "left harness", "", "Blk", "", "through a 2-pin connector, pin 1", False),
    ("ENGINE START", "3", "BUS MANAGER", "left harness", "16", "Red", "", "through a 2-pin connector, pin 2", False),
    ("ENGINE START", "4", "ESSENTIAL BUS BAR", "", "16", "Red", "",
     "through a 2-pin connector, pin 1; long run along the bottom of the sheet", False),
    ("BUS MANAGER", "bottom harness", "FUEL PUMP MODE", "1", "", "Brn", "", "position 1/AUTO", False),
    ("BUS MANAGER", "bottom harness", "FUEL PUMP MODE", "3", "", "Wht", "", "position 2", False),
    ("ESSENTIAL BUS BAR", "", "FUEL PUMP MODE", "2", "20", "", "",
     "switch common. The same 20 ga line also feeds the START BAT SEL common", False),
    ("ESSENTIAL BUS BAR", "", "START BAT SEL", "2", "20", "", "", "switch common, shared with FUEL PUMP MODE", False),
    ("BUS MANAGER", "bottom harness", "START BAT SEL", "1", "", "Grn", "", "position 1", False),
    ("BUS MANAGER", "bottom harness", "START BAT SEL", "3", "", "Red", "", "position 2 (centre position is BOTH)", False),
]


# Annunciator panel: six lamps, each on a 2-pin connector (1 = anode, Red;
# 2 = cathode, Blk), plus a diode-OR lamp-test network (D1-D10, 1N4001).
# Lamp ground and output legs read cleanly. Anode supplies and the test network
# cross many lines and are recorded as review rows rather than guessed.
ANNUNCIATOR = [
    # Traced end to end with scripts/sch_trace.py. Each "power" lamp's anode
    # is diode-ORed: fed from its essential-bus breaker through D1-D4, and
    # from the lamp-test bus through D5-D8. The test button is two-pole: pole
    # 1 connects VP-X J1-2 to the test bus, pole 2 grounds the two FAULT lamp
    # cathodes through D9/D10 (the FAULT lamps' anodes are always fed from
    # VP-X J1-2; the ECU lights them by pulling their cathodes low).
    #   (from_ref, from_pin, to_ref, to_pin, colour, note)
    ("D1", "K", "ANN ECU PWR PRI", "1", "Wht/Red", ""),
    ("D5", "K", "ANN ECU PWR PRI", "1", "Wht/Red", "lamp test"),
    ("D2", "K", "ANN ECU PWR SEC", "1", "Ora", ""),
    ("D6", "K", "ANN ECU PWR SEC", "1", "Ora", "lamp test"),
    ("D3", "K", "ANN FUEL PUMP 1", "1", "Wht", ""),
    ("D7", "K", "ANN FUEL PUMP 1", "1", "Wht", "lamp test"),
    ("D4", "K", "ANN FUEL PUMP 2", "1", "Wht/Ora", ""),
    ("D8", "K", "ANN FUEL PUMP 2", "1", "Wht/Ora", "lamp test"),
    ("ANN LT TEST", "1B", "D5", "A", "Yel", "test bus"),
    ("ANN LT TEST", "1B", "D6", "A", "Yel", "test bus"),
    ("ANN LT TEST", "1B", "D7", "A", "Yel", "test bus"),
    ("ANN LT TEST", "1B", "D8", "A", "Yel", "test bus"),
    ("ANN ECU FAULT PRI", "2", "D9", "A", "Blk", "fault lamp cathode"),
    ("ANN ECU FAULT SEC", "2", "D10", "A", "Wht/Blk", "fault lamp cathode"),
    ("D9", "K", "ANN LT TEST", "2A", "Blk", ""),
    ("D10", "K", "ANN LT TEST", "2A", "Blk", ""),
    ("ANN LT TEST", "2B", "AG", "", "Blk", ""),
    ("ANN ECU FAULT PRI", "2", "ECU CHECK ENG PRI", "", "Yel", "the ECU lights the lamp by pulling this low"),
    ("ANN ECU FAULT SEC", "2", "ECU CHECK ENG SEC", "", "Yel", "the ECU lights the lamp by pulling this low"),
    ("ANN ECU PWR PRI", "2", "AG", "", "Blk", ""),
    ("ANN ECU PWR SEC", "2", "AG", "", "Blk", ""),
    ("ANN FUEL PUMP 1", "2", "AG", "", "Blk", ""),
    ("ANN FUEL PUMP 2", "2", "AG", "", "Blk", ""),
]


# Facts the power sheet's geometry must confirm. The schematic regions of this
# sheet (essential bus, annunciator, Bus Manager) are entered by hand from the
# rendered drawing; these checks run the line tracer over the same drawing and
# fail the extraction if any hand-entered connection is not really there.
# Each point is a wire end or a point on a wire, in PDF coordinates.
POWER_TRACE_CHECKS = [
    ("pilot DB15-3 (AV MSTR) reaches the COM/NAV relay coils", (630, 648), (2076, 1575)),
    ("pilot DB15-4 (A/P MSTR) reaches the ESS SERVOS breaker", (648, 648), (2434, 1818)),
    ("copilot DB15-7 reaches the ESS PNL LTS breaker", (2160, 648), (2434, 1746)),
    ("pilot DB15-10 and copilot DB15-5 are one wire (switch backlighting)", (1170, 648), (2123, 648)),
    ("D1 anode <- ESS ECU PRI breaker", (1283, 1674), (2409, 1188)),
    ("D2 anode <- ESS ECU SEC breaker", (1283, 1692), (2409, 1260)),
    ("D3 anode <- ESS PUMP 1 breaker", (1283, 1710), (2409, 1332)),
    ("D4 anode <- ESS PUMP 2 breaker", (1283, 1728), (2409, 1404)),
    ("ECU PWR PRI anode = D5/D1 cathode node", (900.5, 1440), (1163, 1674)),
    ("ECU PWR SEC anode = D6/D2 cathode node", (981.5, 1440), (1163, 1692)),
    ("FUEL PUMP 1 anode = D7/D3 cathode node", (1224, 1440), (1163, 1710)),
    ("FUEL PUMP 2 anode = D8/D4 cathode node", (1305, 1440), (1163, 1728)),
    ("D1 cathode joins the D5 node", (1255, 1674), (1163, 1674)),
    ("D4 cathode joins the D8 node", (1255, 1728), (1163, 1728)),
    ("ECU FAULT PRI cathode -> D9 anode", (1080.5, 1440), (1107, 1660)),
    ("ECU FAULT SEC cathode -> D10 anode", (1161, 1440), (1125, 1660)),
    ("both ECU FAULT anodes <- VP-X J1-2 (Red)", (1062.5, 1440), (342, 1584)),
    ("ECU FAULT SEC anode on the same feed", (1143.5, 1440), (342, 1584)),
    ("lamp-test bus (D5-D8 anodes) -> test pole 1, one side", (1143, 1731), (1183, 1845)),
    ("VP-X J1-2 (Yel) -> test pole 1, other side", (360, 1602), (1191, 1845)),
    ("D9/D10 cathodes -> test pole 2, one side", (1125, 1710), (1183, 1863)),
    ("Bus Manager Blk 16 ga -> Start Contactor 1 coil", (2040.5, 2250), (2010, 2178)),
    ("Bus Manager Red 16 ga -> Start Contactor 2 coil", (2058.5, 2250), (2112, 2065)),
    ("Bus Manager Pur -> FUEL PRESS INPUT", (2076, 2270), (2196, 2196)),
    ("Bus Manager Gray -> fuel-pump changeover relay coil (85)", (2094, 2270), (2610, 1350)),
    ("test pole 2, other side -> AG", (1200, 1863), (1265, 1874)),
]
POWER_TRACE_APART = [
    # the test button's contacts must be open, and its two poles separate
    ("test pole 1 is open (test bus vs J1-2)", (1143, 1731), (360, 1602)),
    ("test pole 2 is open (fault cathodes vs AG)", (1125, 1710), (1265, 1874)),
    ("test pole 1 and pole 2 are separate", (1143, 1731), (1125, 1710)),
    # a lamp's anode and cathode must not be shorted
    ("ECU PWR PRI anode and cathode are separate", (900.5, 1440), (918.5, 1440)),
    ("the two start contactor coil feeds are separate", (2040.5, 2250), (2058.5, 2250)),
]


def verify_power_trace(pdf):
    import sch_trace
    segs, _rects, dots, _words = sch_trace.load(pdf)
    uf, _ = sch_trace.connectivity(segs, dots)

    def root(pt):
        x, y = pt
        for i, (o, x0, y0, x1, y1) in enumerate(segs):
            if (abs(x0 - x) <= 3 and abs(y0 - y) <= 3) or (abs(x1 - x) <= 3 and abs(y1 - y) <= 3):
                return uf.find(i)
            if o == "H" and abs(y0 - y) <= 1.5 and x0 <= x <= x1:
                return uf.find(i)
            if o == "V" and abs(x0 - x) <= 1.5 and y0 <= y <= y1:
                return uf.find(i)
        return None

    bad = []
    for name, a, b in POWER_TRACE_CHECKS:
        ra, rb = root(a), root(b)
        if ra is None or rb is None or ra != rb:
            bad.append(f"NOT CONNECTED: {name}")
    for name, a, b in POWER_TRACE_APART:
        ra, rb = root(a), root(b)
        if ra is not None and ra == rb:
            bad.append(f"SHORTED: {name}")
    return len(POWER_TRACE_CHECKS) + len(POWER_TRACE_APART), bad


def extract_power_lighting(pdf):
    n, bad = verify_power_trace(pdf)
    if bad:
        raise SystemExit("power sheet: hand-entered wiring disagrees with the drawing:\n  " + "\n  ".join(bad))
    print(f"power sheet: {n} hand-entered connections confirmed against the drawing's geometry")
    words = load_words(pdf)
    rows = []

    def add(**kw):
        r = dict(sheet="PWR", net="", from_ref="", from_pin="", to_ref="", to_pin="",
                 color="", awg="", protection="", notes="", review="")
        r.update(kw)
        rows.append(r)

    # ---- DB15 colours, both panels ----
    db15 = {"PILOT": _db15_pins(words, 660, 696, 500, 1500),
            "COPILOT": _db15_pins(words, 655, 696, 1700, 2760)}
    color_to_db15 = {}
    for side, pins in db15.items():
        for pin, (c, _g) in pins.items():
            color_to_db15.setdefault(c, []).append((side, pin))

    # ---- VP-X tables ----
    for conn, lx, y0, y1 in [("J2", 250, 820, 1480), ("J1", 250, 1513, 1840),
                             ("J12", 250, 1873, 2300), ("J10", 1110, 2144, 2560)]:
        for pin, g in _vpx_rows(words, lx, y0, y1).items():
            if (conn, pin) in VPX_SPARE:
                continue
            base = dict(from_ref=f"VP-X {conn}", from_pin=pin, awg=g["awg"],
                        protection=g["breaker"])
            if conn == "J2" and pin not in ("11", "14", "15"):
                hits = color_to_db15.get(g["color"], [])
                sw = SWITCH_BY_COLOR.get(g["color"])
                if len(hits) == 1 and sw:
                    side, dpin = hits[0]
                    add(**base, to_ref=f"{side}-SW-PANEL DB15", to_pin=dpin, color=g["color"],
                        notes=f"VP-X switch input {pin} <- {sw[1]} switch. Traced by unique wire colour.")
                else:
                    add(**base, color=g["color"],
                        review=f"switch input {pin}: colour {g['color']!r} did not match exactly one DB15 pin")
                continue
            for dest, cov, note in VPX_DEST.get((conn, pin), [(None, None, "")]):
                if dest is None:
                    add(**base, color=g["color"], review="no destination recorded for this pin")
                else:
                    to_pin = {"ANN ECU FAULT PRI": "1", "ANN ECU FAULT SEC": "1", "ANN LT TEST": "1A"}.get(dest, "") \
                        if (conn, pin) == ("J1", "2") else ""
                    add(**base, to_ref=dest, to_pin=to_pin, color=cov or g["color"], notes=note)

    # ---- DB15 pins that don't go to a VP-X input ----
    for side, pins in db15.items():
        for pin, (c, gauge) in sorted(pins.items(), key=lambda kv: int(kv[0])):
            if c in SWITCH_BY_COLOR and len(color_to_db15.get(c, [])) == 1:
                continue        # already emitted from the VP-X side
            if (side, pin) in DB15_FROM_ELSEWHERE:
                continue
            dest = DB15_DEST.get((side, pin))
            if not dest:
                add(from_ref=f"{side}-SW-PANEL DB15", from_pin=pin, color=c,
                    review="harness-side destination not recorded")
                continue
            to_pin = "5" if (side, pin) == ("PILOT", "10") else ""
            add(from_ref=f"{side}-SW-PANEL DB15", from_pin=pin, to_ref=dest[0], to_pin=to_pin, color=c,
                awg=gauge, notes=dest[1],
                review=("traced by eye on a long run; confirm" if (side, pin) in DB15_REVIEW else ""))

    # ---- essential bus ----
    for brk, amps, dest, awg, colour, note, rev in ESS_BUS:
        dest, _, dpin = dest.partition(":")
        add(from_ref="ESS BUS", from_pin=brk, to_ref=dest, to_pin=dpin, color=colour, awg=awg,
            protection=f"{amps}A", notes=note,
            review=("long run traced by eye; confirm" if rev else ""))

    # ---- Bus Manager, batteries, starter ----
    for fr, fp, to, tp, awg, colour, prot, note, rev in BUS_MGR:
        add(from_ref=fr, from_pin=fp, to_ref=to, to_pin=tp, awg=awg, color=colour,
            protection=prot, notes=note,
            review=("two lines run close here; confirm which coil each feeds" if rev else ""))

    # ---- annunciator: lamps, 1N4001 diodes, two-pole lamp-test button ----
    for fr, fp, to, tp, colour, note in ANNUNCIATOR:
        add(from_ref=fr, from_pin=fp, to_ref=to, to_pin=tp, color=colour, notes=note)

    # ---- regions not yet parsed ----
    add(from_ref="PILOT AND COPILOT SWITCH-PANEL INTERNALS (switch-to-DB15 side)",
        review="region not yet extracted")
    return rows


# ---------------------------------------------------------------------------
# SkyView Interconnect  --  SteinAir, 5/17/2017
#
# ~17 connector boxes joined by drawn lines: here the pin names are text but
# the connectivity exists only in the geometry, so this sheet is traced rather
# than read. See scripts/sch_trace.py for the rules.
# ---------------------------------------------------------------------------

# Single-ended SV wires resolved by inspecting the rendered drawing. Keyed by
# (connector, pin). Each value is a list of rows to emit instead.
SV_RESOLVED = {
    ("GTN P1001", "7"): [
        dict(to_ref="R-XPNDR-GPS (1.21 kOhm series resistor)", to_pin="1",
             notes="GPS RS-232 Out 2 to the transponder through an in-line 1.21 kOhm resistor, drawn "
                   "as a zigzag mid-run. A real component in the harness, invisible to pin-to-pin tracing."),
    ],
    ("SV-XPNDR-261 DB-25M", "3"): [
        dict(to_ref="R-XPNDR-GPS (1.21 kOhm series resistor)", to_pin="2",
             notes="GPS In (ADS-B) from the GTN, through the in-line 1.21 kOhm resistor"),
    ],
    ("GMA245 J1", "44"): [
        dict(to_ref="MH OXYGEN CONTROL HEAD", to_pin="DB25-9",
             notes="Alert 4 Audio Hi. Matches the O2 sheet independently: control head DB25-9 -> GMA245 J1-44"),
    ],
    ("GTN P1001", "62"): [dict(to_ref="GTN CONFIG MODULE", to_pin="", notes="Config Mod Data")],
    ("GTN P1001", "65"): [dict(to_ref="GTN CONFIG MODULE", to_pin="", notes="Config Mod Power")],
    ("GTN P1001", "43"): [dict(to_ref="GTN FAN", to_pin="", notes="Fan Ground")],
    ("GTN P1001", "63"): [dict(to_ref="GTN CONFIG MODULE", to_pin="", notes="Config Mod Clock")],
    ("GTN P1001", "64"): [dict(to_ref="GTN CONFIG MODULE", to_pin="", notes="Config Mod Ground")],
    ("GTN P1001", "58"): [dict(to_ref="GTN FAN", to_pin="", notes="Fan Tach In")],
    ("GTN P1001", "59"): [dict(to_ref="GTN FAN", to_pin="", notes="Fan Power")],
    ("ARTEX 345 ELT DB15", "8"): [dict(to_ref="ELT BUZZER", to_pin="", notes="Buzzer Power Out")],
    ("SV-AP-PANEL DB-15", "7"): [dict(to_ref="PITCH TRIM SERVO MOTOR", to_pin="1", notes="Pitch Trim Motor Output 1")],
    ("SV-AP-PANEL DB-15", "8"): [dict(to_ref="PITCH TRIM SERVO MOTOR", to_pin="2", notes="Pitch Trim Motor Output 2")],
    ("SV-AP-PANEL DB-15", "14"): [dict(to_ref="ROLL TRIM SERVO MOTOR", to_pin="1", notes="Roll Trim Motor Output 1")],
    ("SV-AP-PANEL DB-15", "15"): [dict(to_ref="ROLL TRIM SERVO MOTOR", to_pin="2", notes="Roll Trim Motor Output 2")],
    ("GMA245 J2", "20"): [dict(to_ref="GRIPS", to_pin="COM SWAP",
                               notes="COM Swap button on the grips, drawn as an off-sheet arrow")],
}


def _sv_dest_by_name(fn):
    """Destination implied unambiguously by a pin's function name."""
    f = fn.lower()
    who = ("PILOT" if f.startswith("pilot") else "COPILOT" if f.startswith(("copilot", "coplilot"))
           else "PASSENGER" if f.startswith("pass") else None)
    if who and ("phone" in f):
        return f"{who} HEADSET JACK (phones)"
    if who and "mic" in f:
        return f"{who} HEADSET JACK (mic)"
    if who and "trim" in f:
        return f"{who} GRIP"
    if f.strip(" -") in ("ground", "ground in", "gnd"):
        return "GROUND"
    return None


def extract_sv_interconnect(pdf):
    import sch_trace
    nets, boxes, _uf, _segs, _words, _x = sch_trace.trace(pdf)
    func = {}
    for b in boxes:
        for pin, f in b["func"].items():
            func[(b["name"], pin)] = f

    def ref(b):
        # "PFD - LEFT #1 | SV-HDX1100 DB37" -> "SV-HDX1100 (PFD - LEFT #1) DB37"
        if " | " in b:
            sup, core = b.split(" | ", 1)
            head, _, tail = core.partition(" ")
            return f"{head} ({sup}) {tail}".strip()
        return b

    # Name each headset jack by the GMA 245 function on its tip, numbering
    # the passenger jacks (two phone jacks share one set of pins) top to bottom.
    jack_fn = {}
    for _root, nodes, _c in nets:
        gma = [func.get((n["ref"], n["pin"]), "") for n in nodes if n["kind"] == "pin" and "GMA245" in n["ref"]]
        for n in nodes:
            if n["ref"].startswith("JACK@") and n["pin"] == "T" and gma:
                jack_fn[n["ref"]] = gma[0]
    def jack_name(fn):
        f = fn.lower().replace("coplilot", "copilot")
        who = ("COPILOT" if f.startswith("copilot") else "PILOT" if f.startswith("pilot")
               else "PASSENGER" if f.startswith("pass") else "?")
        kind = "PHONE" if "phone" in f else "MIC" if "mic" in f else "?"
        return f"{who} {kind} JACK"
    rename, used = {}, collections.Counter()
    for jref in sorted(jack_fn, key=lambda r: tuple(int(v) for v in r[5:].split(","))[::-1]):
        base = jack_name(jack_fn[jref])
        used[base] += 1
        rename[jref] = base
    dup = {b for b, n in used.items() if n > 1}
    seen = collections.Counter()
    for jref in sorted(rename, key=lambda r: int(r[5:].split(",")[1])):
        if rename[jref] in dup:
            seen[rename[jref]] += 1
            rename[jref] = f"{rename[jref]} {seen[rename[jref]]}"
    for _root, nodes, _c in nets:
        for n in nodes:
            if n["ref"] in rename:
                n["ref"] = rename[n["ref"]]
    # jack contacts with no wire (the passenger mic jacks' rings) are not wires
    nets = [(r, nd, c) for r, nd, c in nets
            if not (len(nd) == 1 and nd[0]["ref"].endswith("JACK") or len(nd) == 1 and " JACK " in nd[0]["ref"])]

    order = {b["name"]: i for i, b in enumerate(sorted(boxes, key=lambda b: (b["x0"], b["y0"])))}
    rows = []
    for _root, nodes, colours in nets:
        pins = sorted((n for n in nodes if n["kind"] == "pin"),
                      key=lambda n: (order.get(n["ref"], 99), int(n["pin"]) if n["pin"].isdigit() else 0))
        others = [n for n in nodes if n["kind"] != "pin"]
        if not pins:
            continue
        hub = pins[0]
        net = func.get((hub["ref"], hub["pin"]), "")
        colour = " + ".join(colours)
        rest = pins[1:] + others
        if (hub["ref"], hub["pin"]) in SV_RESOLVED:
            for extra in SV_RESOLVED[(hub["ref"], hub["pin"])]:
                rows.append(dict(sheet="SV", net=net, from_ref=ref(hub["ref"]), from_pin=hub["pin"],
                                 color=colour, awg="", protection="", review="", **extra))
            continue
        if not rest:
            dest = _sv_dest_by_name(net)
            rows.append(dict(sheet="SV", net=net, from_ref=ref(hub["ref"]), from_pin=hub["pin"],
                             to_ref=dest or "", to_pin="", color=colour, awg="", protection="",
                             notes=(f"{net}. Destination taken from the pin name: jacks, grips "
                                    "and ground symbols are drawn as symbols, not connectors, so "
                                    "the geometry cannot name them" if dest else net),
                             review=("" if dest else
                                     "a wire leaves this pin but its far end was not identified")))
            continue
        for n in rest:
            fn = func.get((n["ref"], n["pin"]), "") if n["kind"] == "pin" else ""
            if n["kind"] == "text" and n["ref"] in ("AG", "CG"):
                n = dict(n, kind="label")      # a ground symbol: AG avionics, CG case
            note = f"{net} -> {fn}" if fn else net
            if len(nodes) > 2:
                note += f"  [{len(nodes)}-way net]"
            rows.append(dict(sheet="SV", net=net, from_ref=ref(hub["ref"]), from_pin=hub["pin"],
                             to_ref=ref(n["ref"]), to_pin=n["pin"], color=colour, awg="",
                             protection="", notes=note.strip(),
                             review=("far end named from nearby text, not a connector; confirm"
                                     if n["kind"] == "text" else "")))
    for region, why in (
        ("SKYVIEW NETWORK", "the network topology (SV-NET-HUB, SV-NET-SPL, ADAHRS, EMS, knob/AP/COM "
                            "panels, ARINC module) is drawn as a block diagram of network cables, not wires"),
        ("ROLL AND PITCH SERVO DB-9s", "servo connectors are drawn with F/M pin columns the box detector "
                                       "does not recognise"),
        ("BOSE JACK / SKYVIEW NETWORK CABLE PINOUTS", "connector reference tables, not wires -- they "
                                                     "belong in the generated CONNECTORS view"),
    ):
        rows.append(dict(sheet="SV", net="", from_ref=region, from_pin="", to_ref="", to_pin="",
                         color="", awg="", protection="", notes=why, review="region not yet extracted"))
    return rows


EXTRACTORS = {"O2": ("MH_Oxygen.pdf", extract_mh_oxygen),
              "PWR": ("Power__Lighting.pdf", extract_power_lighting),
              "SV": ("SV_Interconnect.pdf", extract_sv_interconnect)}


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
