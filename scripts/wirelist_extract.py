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
    ("J1", "2"):  [("ANNUNCIATOR - FAULT ANN", None, "the drawing shows a Red and a Yel line leaving this pin; only the Red is captured")],
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
                     "drawing says SV-ADSB-470; this handbook records an SV-ADSB-472 - one of them is wrong")],
    ("J10", "8"):  [("MH CNTRL HEAD J1-1", None, "matches O2 sheet: control head DB25-1 from VP-X J10-8"),
                    ("CO DETECT J1-1", "Red",
                     "CO Guardian - sys-42 records it as removed (RMA 11096), so this branch may be dead")],
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
    ("PILOT", "3"):  ("COM/NAV RELAY COILS (85)", "AV MSTR output. Drives both GTN power relays - see ESS bus"),
    ("PILOT", "4"):  ("ESS BUS SERVOS breaker", "A/P MSTR input"),
    ("PILOT", "5"):  ("A/P SERVO POWER", "A/P MSTR output"),
    ("PILOT", "9"):  ("AG", "switch-panel ground"),
    ("PILOT", "10"): ("ANNUNCIATOR", "Yel line toward the annunciator test circuit"),
    ("COPILOT", "1"):  ("AG", "switch-panel ground"),
    ("COPILOT", "4"):  ("AG", "switch-panel ground"),
    ("COPILOT", "5"):  ("ANNUNCIATOR", "Yel line toward the annunciator test circuit"),
    ("COPILOT", "6"):  ("AG", "switch-panel ground"),
    ("COPILOT", "7"):  ("ESS BUS PNL LTS breaker", "panel/dimmer power"),
    ("COPILOT", "8"):  ("PANEL LED STRIP - PLUS", ""),
    ("COPILOT", "9"):  ("LEFT MAP LT", "WHITE"),
    ("COPILOT", "10"): ("LEFT MAP LT", "RED"),
    ("COPILOT", "11"): ("RIGHT MAP LT", "WHITE"),
    ("COPILOT", "12"): ("RIGHT MAP LT", "RED"),
    ("COPILOT", "13"): ("MH OXYGEN CONTROL HEAD", "switch dimmer; matches O2 sheet DB25-21 Yel/Grn"),
}
DB15_REVIEW = {("PILOT", "3"), ("PILOT", "4"), ("PILOT", "10"), ("COPILOT", "5"), ("COPILOT", "7")}

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
    ("PNL LTS", "5", "COPILOT SW PANEL", "", "Red", "long run up to the copilot panel; exact DB15 pin to confirm", True),
    ("SERVOS", "5", "A/P MSTR", "20", "Red", "long run up to the pilot panel A/P MSTR switch", True),
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
     "manufacturer-supplied harness", True),
    ("BUS MANAGER", "top harness", "START CONTACTOR 2", "coil", "16", "Red", "",
     "manufacturer-supplied harness", True),
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
    # (lamp, colour, pin, to_ref, wire colour, note, review)
    ("ECU PWR PRI", "GRN", "2", "AG", "Blk", "lit by power on the anode", False),
    ("ECU PWR SEC", "GRN", "2", "AG", "Blk", "lit by power on the anode", False),
    ("FUEL PUMP 1", "GRN", "2", "AG", "Blk", "lit by power on the anode", False),
    ("FUEL PUMP 2", "AMB", "2", "AG", "Blk", "lit by power on the anode", False),
    ("ECU FAULT PRI", "RED", "2", "ECU CHECK ENG PRI", "Yel",
     "cathode to the ECU: the ECU lights this lamp by pulling the line low", False),
    ("ECU FAULT SEC", "RED", "2", "ECU CHECK ENG SEC", "Yel",
     "cathode to the ECU: the ECU lights this lamp by pulling the line low", False),
    ("ECU PWR PRI", "GRN", "1", "ESS BUS ECU PRI (second leg)", "Wht/Red",
     "anode supply; also feeds lamp-test diode D5", True),
    ("ECU PWR SEC", "GRN", "1", "ESS BUS ECU SEC (second leg)", "Ora",
     "anode supply; also feeds lamp-test diode D6", True),
    ("FUEL PUMP 1", "GRN", "1", "ESS BUS PUMP 1 (second leg)", "Wht",
     "anode supply; also feeds lamp-test diode D7", True),
    ("FUEL PUMP 2", "AMB", "1", "ESS BUS PUMP 2 (second leg)", "Wht/Ora",
     "anode supply; also feeds lamp-test diode D8", True),
    ("ECU FAULT PRI", "RED", "1", "VP-X J1-2 (FAULT ANN)", "Red",
     "both FAULT lamp anodes share one supply line", True),
    ("ECU FAULT SEC", "RED", "1", "VP-X J1-2 (FAULT ANN)", "Red",
     "both FAULT lamp anodes share one supply line", True),
]


def extract_power_lighting(pdf):
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
                    add(**base, to_ref=dest, color=cov or g["color"], notes=note,
                        review=("second line not captured" if (conn, pin) == ("J1", "2") else ""))

    # ---- DB15 pins that don't go to a VP-X input ----
    for side, pins in db15.items():
        for pin, (c, gauge) in sorted(pins.items(), key=lambda kv: int(kv[0])):
            if c in SWITCH_BY_COLOR and len(color_to_db15.get(c, [])) == 1:
                continue        # already emitted from the VP-X side
            dest = DB15_DEST.get((side, pin))
            if not dest:
                add(from_ref=f"{side}-SW-PANEL DB15", from_pin=pin, color=c,
                    review="harness-side destination not recorded")
                continue
            add(from_ref=f"{side}-SW-PANEL DB15", from_pin=pin, to_ref=dest[0], color=c,
                awg=gauge, notes=dest[1],
                review=("traced by eye on a long run; confirm" if (side, pin) in DB15_REVIEW else ""))

    # ---- essential bus ----
    for brk, amps, dest, awg, colour, note, rev in ESS_BUS:
        add(from_ref="ESS BUS", from_pin=brk, to_ref=dest, color=colour, awg=awg,
            protection=f"{amps}A", notes=note,
            review=("long run traced by eye; confirm" if rev else ""))

    # ---- Bus Manager, batteries, starter ----
    for fr, fp, to, tp, awg, colour, prot, note, rev in BUS_MGR:
        add(from_ref=fr, from_pin=fp, to_ref=to, to_pin=tp, awg=awg, color=colour,
            protection=prot, notes=note,
            review=("two lines run close here; confirm which coil each feeds" if rev else ""))

    # ---- annunciator ----
    for lamp, lc, pin, to, colour, note, rev in ANNUNCIATOR:
        add(from_ref=f"ANN {lamp} ({lc})", from_pin=pin, to_ref=to, color=colour, notes=note,
            review=("anode supply crosses several lines; confirm the source" if rev else ""))
    add(from_ref="ANNUNCIATOR TEST NETWORK", notes=(
            "diode-OR lamp test: ANN LT TEST pushbutton on Yel drives D1-D4 to every lamp "
            "anode; D9/D10 pull the two FAULT lamp cathodes low. All diodes 1N4001."),
        review="network not broken out wire by wire")

    # ---- regions not yet parsed ----
    add(from_ref="PILOT AND COPILOT SWITCH-PANEL INTERNALS (switch-to-DB15 side)",
        review="region not yet extracted")
    return rows


EXTRACTORS = {"O2": ("MH_Oxygen.pdf", extract_mh_oxygen),
              "PWR": ("Power__Lighting.pdf", extract_power_lighting)}


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
