#!/usr/bin/env python3
"""
Wire lists for the parts of the airplane no SteinAir drawing covers: the
wings, the under-seat terminal blocks, and the EMS-220's 37-pin connector.

The source is the owner's typed build notes as they live in the handbook --
`sections/sys-24-electrical.md` (wing roots, terminal blocks, EMS pinout) and
`sections/sys-33-lighting.md` (wingtip CPCs). The tables are READ, not
retyped, so the wire lists cannot drift from the handbook: edit the handbook
table, re-run the extractor.

What the tables record is a pin's function and wire colour at ONE connector.
Wires are joined across connectors here, and every join says what it rests on:

  * same bundle, same colour at both ends (root and tip CPC)
  * a function named at both ends (TB-R "Taxi power" and VP-X "TAXI LIGHTS
    POWER")
  * a manufacturer's documented colour code matching one for one (the Dynon
    servo pigtail; Ray Allen's trim sensor leads)

A join none of those settles is NOT drawn. It is emitted with `review` set to
the question that would settle it, and every row sharing that question is
grouped into one item on `wiring/INSPECT.md`. A join that is drawn but rests
on something odd in the record carries "Confirm at inspection:" in its notes
and also lands on the checklist.

Labels (destinations with no pin) are global in the KiCad project, so a label
written here with the same text as one on another sheet joins the two nets:
"TAXI LIGHTS POWER" on WING meets VP-X J12-3 on PWR.

  uv run python3 scripts/wirelist_extract.py --sheet WING
  uv run python3 scripts/wirelist_extract.py --sheet EMS
"""

import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SYS24 = REPO / "sections" / "sys-24-electrical.md"
SYS33 = REPO / "sections" / "sys-33-lighting.md"
CONFIRM = "Confirm at inspection:"

# ---------------------------------------------------------------------------
# Reading handbook tables
# ---------------------------------------------------------------------------


def table(path, heading):
    """The first pipe table under `heading` (exact text, e.g. '#### Left Wing
    Root Exit'), as a list of dicts keyed by the header row."""
    lines = Path(path).read_text().splitlines()
    try:
        i = next(n for n, l in enumerate(lines) if l.strip() == heading)
    except StopIteration:
        raise SystemExit(f"{Path(path).name}: heading {heading!r} not found")
    rows, header = [], None
    for l in lines[i + 1:]:
        s = l.strip()
        if s.startswith("#"):
            break
        if not s.startswith("|"):
            if header:
                break
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if header is None:
            header = cells
        elif set(s) <= set("|-: "):
            continue
        else:
            rows.append(dict(zip(header, cells)))
    if not rows:
        raise SystemExit(f"{Path(path).name}: no table under {heading!r}")
    return rows


def by_pin(rows, key="Pin"):
    return {r[key]: r for r in rows}


def colour(c):
    """Handbook colour text -> wire-list colour ('White/green' -> 'Wht/Grn')."""
    c = c.replace("(twisted)", "").replace("(untwisted)", "").strip()
    if c in ("", "—", "-"):
        return ""
    short = {"white": "Wht", "black": "Blk", "red": "Red", "orange": "Ora", "blue": "Blu",
             "green": "Grn", "yellow": "Yel", "brown": "Brn", "violet": "Vio"}
    return "/".join(short[p.strip().lower()] for p in c.split("/"))


def row(sheet, a, ap, b, bp="", color="", notes="", review="", net="", awg=""):
    return dict(sheet=sheet, net=net, from_ref=a, from_pin=ap, to_ref=b, to_pin=bp,
                color=color, awg=awg, protection="", notes=notes, review=review)


# ---------------------------------------------------------------------------
# Questions the record cannot answer. Rows carrying one are not drawn.
# ---------------------------------------------------------------------------

Q_AEROSUN = ("AeroSun bundle: which harness colour (orange, blue, white) carries landing, taxi and "
             "wig-wag? The light's own leads are red = landing, blue = taxi, yellow = wig-wag "
             "(AeroSun Vx manual Rev C); the record names only the harness colours")
Q_PULSAR = ("Pulsar bundle: which harness colour (orange, blue, white) carries position, strobe and "
            "sync? The light's own leads are red = position, yellow = strobe, green = sync "
            "(AeroLEDs Pulsar/SunTail diagram); the record names only the harness colours")
Q_SHIELD = ("Light-bundle shields at the cabin end: where do the AeroSun and Pulsar shield drains "
            "land? TB-R 1 is the recorded light ground, but no record says the shields go there")
Q_PITOT_GND = ("Pitot heat ground (left wing root pin 16, black): where does it land on the cabin "
               "side? Also record the pitot's Molex Micro-Fit 3-pin pinout")
Q_TAIL = ("Tailcone: record the pitch trim servo wiring from TB-L to the tail (the tailcone-rear "
          "DSUB-15 is the likely path; its pinout is not recorded)")
Q_SUNTAIL = ("Tail light: record the tailcone-rear Molex 5-pin pinout and harness colours from "
             "TB-R to the SunTail")

# ---------------------------------------------------------------------------
# WING: both wings, the under-seat terminal blocks, and the tail feeds
# ---------------------------------------------------------------------------

LROOT, RROOT = "LEFT WING ROOT CPC", "RIGHT WING ROOT CPC"
LTIP, RTIP = "LEFT WINGTIP CPC", "RIGHT WINGTIP CPC"
TBL, TBR = "TB-L (under left seat)", "TB-R (under right seat)"

# Cross-sheet labels. Same text on another sheet = same net in the project.
LBL = dict(
    taxi="TAXI LIGHTS POWER", wigwag="WIGWAG POWER", landing="LANDING LIGHTS POWER",
    strobe="STROBE LIGHTS POWER", nav="NAV LIGHTS POWER",            # PWR sheet, VP-X outputs
    pitot_pwr="PITOT HEAT POWER", ap_pwr="A/P SERVO POWER",          # PWR sheet
    pitot_status="PITOT HEAT STATUS", fuel_l="FUEL LEVEL LEFT", fuel_r="FUEL LEVEL RIGHT",
    trim_gnd="TRIM SENSOR GROUND", trim_5v="SENSOR +5V",
    roll_pos="ROLL TRIM POSITION", pitch_pos="PITCH TRIM POSITION",  # EMS sheet
    roll_a="ROLL TRIM MOTOR A", roll_b="ROLL TRIM MOTOR B",
    pitch_a="PITCH TRIM MOTOR A", pitch_b="PITCH TRIM MOTOR B",      # SV sheet, SV-AP-PANEL
    light_gnd="LIGHTS GROUND",
)

# Dynon servo pigtail, SkyView System Installation Guide Table 75.
SERVO = {"Red": "RED (POWER)", "Black": "BLK (GROUND)", "Green": "GRN (NETWORK 1A)",
         "Blue": "BLU (NETWORK 1B)", "Yellow": "YEL (AP DISENGAGE)",
         "White/green": "WHT/GRN (NETWORK 2A)", "White/blue": "WHT/BLU (NETWORK 2B)"}
SERVO_CABIN = {"Red": LBL["ap_pwr"], "Black": "A/P SERVO GROUND", "Yellow": "A/P DISCONNECT (servo yellow)",
               "Green": "SKYVIEW NETWORK DATA 1A", "Blue": "SKYVIEW NETWORK DATA 1B",
               "White/green": "SKYVIEW NETWORK DATA 2A", "White/blue": "SKYVIEW NETWORK DATA 2B"}
SERVO_SRC = ("colours match Dynon's servo pigtail one for one (SkyView System Installation "
             "Guide, Table 75)")

# Ray Allen trim servo, SkyView System Installation Guide Fig. 79: the sensor
# leads are white/orange (+5 V), white/blue (ground), white/green (signal);
# the motor leads are plain white. The wing harness uses the solid colours.
TRIM = {"Orange": ("WHT/ORA (SENSOR +5V)", 2), "Blue": ("WHT/BLU (SENSOR GND)", 1),
        "Green": ("WHT/GRN (SENSOR SIGNAL)", 3)}
TRIM_SRC = ("harness colour matches Ray Allen's sensor lead colour (SkyView System Installation "
            "Guide, Fig. 79: white/orange +5 V, white/blue ground, white/green signal)")


def tip_side(sheet, side, root, root_rows, tip_rows, out):
    """Root CPC (wing side) -> wingtip CPC, joined by bundle and colour."""
    tip = LTIP if side == "LEFT" else RTIP
    tipmap = {}
    for p, r in tip_rows.items():
        fn = r["Function"]
        if fn.startswith("AeroSun VX sync"):
            tipmap[("sync", "Green")] = p
        elif fn.startswith("AeroSun VX"):
            tipmap[("vx", r["Wire Color"])] = p
        elif fn.startswith("Pulsar"):
            tipmap[("pulsar", r["Wire Color"])] = p
        elif fn == "Ground":
            tipmap["ground"] = p
        elif fn == "(unused)":
            continue
        else:
            raise SystemExit(f"sys-33 wingtip pin {p}: unrecognised function {fn!r}")
    for p, r in root_rows.items():
        fn, c = r["Function"], r["Wire Color"]
        if fn == "AeroSun VX sync":
            out.append(row(sheet, root, p, tip, tipmap[("sync", "Green")], "Grn",
                           "AeroSun sync, green at both ends"))
        elif fn in ("AeroSun VX shield", "Pulsar shield"):
            out.append(row(sheet, root, p, tip, tipmap["ground"], "Blk",
                           f"{fn} drain to the tip CPC's only ground pin. Inferred: AeroLEDs uses the "
                           "shield as the light's ground return"))
        elif fn == "AeroSun VX":
            out.append(row(sheet, root, p, tip, tipmap[("vx", c)], colour(c), "AeroSun bundle, same colour at both CPCs"))
        elif fn == "Pulsar":
            out.append(row(sheet, root, p, tip, tipmap[("pulsar", c)], colour(c), "Pulsar bundle, same colour at both CPCs"))
    # tip -> the lights themselves
    vx, pulsar = f"{side} AEROSUN VX", f"{side} PULSAR NS"
    out.append(row(sheet, tip, tipmap[("sync", "Green")], vx, "GRN (SYNC)", "Grn",
                   "AeroSun Vx Rev C: green is the sync line, green to green between the pair"))
    out.append(row(sheet, tip, tipmap["ground"], vx, "BLK (GROUND)", "Blk", "light ground"))
    out.append(row(sheet, tip, tipmap["ground"], pulsar, "BLK (GROUND)", "Blk", "light ground"))
    for c in ("Orange", "Blue", "White"):
        out.append(row(sheet, tip, tipmap[("vx", c)], vx, "", colour(c), review=Q_AEROSUN))
        out.append(row(sheet, tip, tipmap[("pulsar", c)], pulsar, "", colour(c), review=Q_PULSAR))


def extract_wing(_src=None):
    S = "WING"
    out = []
    left = by_pin(table(SYS24, "#### Left Wing Root Exit"))
    right = by_pin(table(SYS24, "#### Right Wing Root Exit"))
    tip = by_pin(table(SYS33, "### Wingtip Connectors (CPC Series 1, 9-Pin)"))
    tbl = by_pin(table(SYS24, "#### Left Terminal Block"), "Position")
    tbr = by_pin(table(SYS24, "#### Right Terminal Block"), "Position")

    def tb_pos(tb, phrase):
        hits = [p for p, r in tb.items() if r["Function"].lower().startswith(phrase.lower())]
        if len(hits) != 1:
            raise SystemExit(f"terminal block: {len(hits)} positions start with {phrase!r}")
        return hits[0]

    # ---- right terminal block: lights ------------------------------------
    for phrase, key in (("Taxi power", "taxi"), ("Wig-wag power", "wigwag"), ("Landing power", "landing"),
                        ("Strobe power", "strobe"), ("Nav power", "nav")):
        out.append(row(S, TBR, tb_pos(tbr, phrase), LBL[key],
                       notes=f"TB-R '{tbr[tb_pos(tbr, phrase)]['Function']}' is the VP-X output PWR names "
                             f"{LBL[key]}; the label joins the two sheets"))
    out.append(row(S, TBR, tb_pos(tbr, "Ground (house"), LBL["light_gnd"],
                   notes="TB-R 1, 'Ground (house, L side)'. The 16 AWG light ground at the right gear mount"))

    # ---- wing roots, cabin side and wing side ----------------------------
    for side, root, rows in (("LEFT", LROOT, left), ("RIGHT", RROOT, right)):
        tip_side(S, side, root, rows, tip, out)
        for p, r in rows.items():
            fn, c = r["Function"], r["Wire Color"]
            if fn == "AeroSun VX sync":
                out.append(row(S, root, p, TBR, tb_pos(tbr, "Sync wire for AeroSun"), "Grn",
                               "TB-R 3 joins the two AeroSun greens, 'one from R, one from L'"))
            elif fn == "AeroSun VX":
                out.append(row(S, root, p, TBR, "", colour(c), review=Q_AEROSUN))
            elif fn == "Pulsar":
                out.append(row(S, root, p, TBR, "", colour(c), review=Q_PULSAR))
            elif fn.endswith("shield"):
                out.append(row(S, root, p, LBL["light_gnd"], "", "Blk", review=Q_SHIELD))
            elif fn == "Fuel level sensor":
                lab = LBL["fuel_l"] if side == "LEFT" else LBL["fuel_r"]
                out.append(row(S, root, p, lab, notes="cabin side, to the EMS fuel level input"))
                out.append(row(S, root, p, f"{side} FUEL LEVEL SENDER", "SIG",
                               notes="wing side, to the tank's sender. Sender ground is not recorded"))
            elif fn == "Pitot heater" and c == "Red":
                out.append(row(S, root, p, LBL["pitot_pwr"], color="Red",
                               notes="cabin side. VP-X J10-6 on PWR, 15 A; the handbook gives the wing run as 14 AWG"))
                out.append(row(S, root, p, "HEATED PITOT", "POWER", "Red",
                               "wing side, through the pitot's Molex Micro-Fit 3-pin (pins not recorded)"))
            elif fn == "Pitot heater" and c == "Black":
                out.append(row(S, root, p, "PITOT HEAT GROUND", "", "Blk", review=Q_PITOT_GND))
                out.append(row(S, root, p, "HEATED PITOT", "GROUND", "Blk",
                               "wing side, through the pitot's Molex Micro-Fit 3-pin (pins not recorded)"))
            elif fn == "Pitot heater status":
                out.append(row(S, root, p, LBL["pitot_status"], color=colour(c),
                               notes="cabin side, to EMS pin 9 (brown/blue at both ends)"))
                out.append(row(S, root, p, "HEATED PITOT", "STATUS", colour(c),
                               "wing side, through the pitot's Molex Micro-Fit 3-pin (pins not recorded)"))
            elif fn == "Trim" and c in TRIM:
                lead, pos_n = TRIM[c]
                pos = tb_pos(tbl, {1: "EMS ground", 2: "EMS power", 3: "Roll trim position"}[pos_n])
                out.append(row(S, root, p, TBL, pos, colour(c),
                               f"cabin side. {TRIM_SRC}; the owner's EMS notes also name orange as the trim +5 V"))
                out.append(row(S, root, p, "ROLL TRIM SERVO", lead, colour(c), f"wing side. {TRIM_SRC}"))
            elif fn == "Trim" and c == "White":
                pass   # the two motor whites, handled as a pair below
            elif fn == "Autopilot servo":
                out.append(row(S, root, p, "ROLL SERVO", SERVO[c], colour(c), f"wing side. {SERVO_SRC}"))
                out.append(row(S, root, p, SERVO_CABIN[c], "", colour(c),
                               (f"cabin side. {SERVO_SRC}. Red, black and yellow are 3-way spliced (front harness, "
                                "pitch servo, wing root) at the right wing connection area"
                                if c in ("Red", "Black", "Yellow") else f"cabin side. {SERVO_SRC}") +
                               (f". {CONFIRM} sys-24's servo colour table maps a wing harness of orange / white / "
                                "white-black onto the servo's green / white-green / white-blue, but the root CPC "
                                "is recorded in the servo's own colours. Which colour set is on which side of "
                                "the root CPC?" if c == "Green" else "")))
            elif fn in ("AeroSun VX shield", "Pulsar shield"):
                pass
            else:
                raise SystemExit(f"sys-24 {side.lower()} wing root pin {p}: unrecognised function {fn!r}")
        if side == "LEFT":
            whites = [p for p, r in rows.items() if r["Function"] == "Trim" and r["Wire Color"] == "White"]
            if len(whites) != 2:
                raise SystemExit(f"left wing root: expected two white trim motor leads, found {whites}")
            for w, phrase in zip(whites, ("Roll trim motor 1 L", "Roll trim motor 1 R")):
                note = ("roll trim motor lead. The two whites are not told apart in the record, so which "
                        "lands on TB-L 5 and which on 6 is unrecorded; swapping them only reverses trim direction")
                out.append(row(S, root, w, TBL, tb_pos(tbl, phrase), "Wht", note))
                out.append(row(S, root, w, "ROLL TRIM SERVO", f"WHT (MOTOR {'A' if phrase.endswith('L') else 'B'})",
                               "Wht", "wing side. " + note))

    # ---- left terminal block: trim, EMS side and SV-AP-PANEL side --------
    for phrase, key, note in (
            ("EMS ground", "trim_gnd", "EMS pin 30, 'Ground (roll trim, elevator trim)'"),
            ("EMS power", "trim_5v", "EMS pin 18, the shared +5 V"),
            ("Roll trim position", "roll_pos", "EMS pin 10"),
            ("Pitch trim position", "pitch_pos", "EMS pin 4")):
        out.append(row(S, TBL, tb_pos(tbl, phrase), LBL[key], notes=f"to {note}; the label joins the EMS sheet"))
    motor_confirm = (f"{CONFIRM} the TB-L labels say 'roll trim motor 1' and 'pitch trim motor 2', but the "
                     "SteinAir drawing and Dynon both put Motor 1 (DB15 7/8) on pitch and Motor 2 (DB15 14/15) "
                     "on roll. Trim works, so the wiring follows function; confirm which SV-AP-PANEL pins land "
                     "on TB-L 5-8 and fix the labels")
    for phrase, key, pin in (("Roll trim motor 1 L", "roll_a", "14"), ("Roll trim motor 1 R", "roll_b", "15"),
                             ("Pitch trim motor 2 L", "pitch_a", "7"), ("Pitch trim motor 2 R", "pitch_b", "8")):
        out.append(row(S, TBL, tb_pos(tbl, phrase), LBL[key], color="Wht",
                       notes=f"SV-AP-PANEL DB-15 pin {pin} via the label. Lead order within the pair is "
                             "unrecorded and only sets direction" + (f". {motor_confirm}" if key == "roll_a" else "")))

    # ---- tail: known to exist, not recorded ------------------------------
    for phrase, lead in (("EMS ground", "WHT/BLU (SENSOR GND)"), ("EMS power", "WHT/ORA (SENSOR +5V)"),
                         ("Pitch trim position", "WHT/GRN (SENSOR SIGNAL)"),
                         ("Pitch trim motor 2 L", "WHT (MOTOR A)"), ("Pitch trim motor 2 R", "WHT (MOTOR B)")):
        out.append(row(S, TBL, tb_pos(tbl, phrase), "PITCH TRIM SERVO", lead, review=Q_TAIL))
    for phrase, lead in (("Nav power", "RED (POSITION)"), ("Strobe power", "YEL (STROBE)"),
                         ("Sync wire for Pulsar", "GRN (SYNC)"), ("Ground (house", "BLK (GROUND)")):
        out.append(row(S, TBR, tb_pos(tbr, phrase), "SUNTAIL", lead, review=Q_SUNTAIL))
    return out


# ---------------------------------------------------------------------------
# EMS: the SV-EMS-220's 37-pin connector
# ---------------------------------------------------------------------------

EMS = "SV-EMS-220 DB37"

# Function text in the handbook -> (destination ref, pin or "" for a label, extra note)
EMS_DEST = [
    (r"^Main battery voltage$", "BATTERY 1 VOLTAGE SENSE", ""),
    (r"^Secondary battery voltage$", "BATTERY 2 VOLTAGE SENSE", ""),
    (r"^Ground \(oil pressure\)$", "OIL PRESSURE SENSOR", "GND"),
    (r"^Ground \(oil temp\)$", "OIL TEMP SENSOR", "GND"),
    (r"^Oil pressure sensor$", "OIL PRESSURE SENSOR", "SIG"),
    (r"^Oil temp sensor$", "OIL TEMP SENSOR", "SIG"),
    (r"^Fuel pressure sensor$", "FUEL PRESSURE SENSOR", "SIG"),
    (r"^Ground \(fuel pressure\)$", "FUEL PRESSURE SENSOR", "GND"),
    (r"^Door ajar right$", "RIGHT DOOR AJAR SWITCH", ""),
    (r"^Door ajar left$", "LEFT DOOR AJAR SWITCH", ""),
    (r"^Ground \(fuel flow\)$", "FUEL FLOW TRANSDUCER", "GND"),
    (r"^Fuel flow$", "FUEL FLOW TRANSDUCER", "SIG"),
    (r"^12V power for fuel flow interface$", "FUEL FLOW TRANSDUCER", "+12V"),
    (r"^Ground \(MAP sensor\)$", "MAP SENSOR", "GND"),
    (r"^MAP sensor input$", "MAP SENSOR", "SIG"),
    (r"^Fuel level right$", LBL["fuel_r"], ""),
    (r"^Fuel level left$", LBL["fuel_l"], ""),
    (r"^Ammeter shunt \+$", "ALTERNATOR AMMETER SHUNT", "+"),
    (r"^Ammeter shunt −$", "ALTERNATOR AMMETER SHUNT", "-"),
    (r"^Low voltage RPM input left$", "RPM LEFT (low-voltage tach)", ""),
    (r"^Low voltage RPM input right$", "RPM RIGHT (low-voltage tach)", ""),
    (r"^Elevator trim position$", LBL["pitch_pos"], ""),
    (r"^Roll trim position$", LBL["roll_pos"], ""),
    (r"^Heated pitot status$", LBL["pitot_status"], ""),
    (r"^Battery fault 1$", "BATTERY 1 FAULT (EarthX BMS)", ""),
    (r"^Battery fault 2$", "BATTERY 2 FAULT (EarthX BMS)", ""),
    (r"^Ground \(roll trim, elevator trim\)$", LBL["trim_gnd"], ""),
]

EMS_NOTES = {
    "BATTERY 1 VOLTAGE SENSE": f"{CONFIRM} where each battery-voltage sense lead is tapped, and that it is fused at the tap",
    "BATTERY 2 VOLTAGE SENSE": f"{CONFIRM} where each battery-voltage sense lead is tapped, and that it is fused at the tap",
    "ALTERNATOR AMMETER SHUNT": (f"{CONFIRM} the owner's build notes call for a 1 A fuse inline on EACH shunt lead "
                                 "(Dynon install guide); confirm both are fitted"),
    "BATTERY 1 FAULT (EarthX BMS)": "through a 1-pin blade connector at the tailcone front",
    "BATTERY 2 FAULT (EarthX BMS)": "through a 1-pin blade connector at the tailcone front",
    "RPM LEFT (low-voltage tach)": "source not recorded in the handbook",
    "RPM RIGHT (low-voltage tach)": "source not recorded in the handbook",
    "LEFT DOOR AJAR SWITCH": "contact input; the switch's other side is not recorded",
    "RIGHT DOOR AJAR SWITCH": "contact input; the switch's other side is not recorded",
}

# The shared +5 V on pin 18, by the device names its handbook row lists.
EMS_5V = {"fuel flow sensor": ("FUEL FLOW TRANSDUCER", "+5V"), "fuel pressure": ("FUEL PRESSURE SENSOR", "+5V"),
          "oil pressure": ("OIL PRESSURE SENSOR", "+5V"), "oil temp": ("OIL TEMP SENSOR", "+5V"),
          "MAP sensor": ("MAP SENSOR", "+5V"), "elevator trim": (LBL["trim_5v"], ""),
          "roll trim": (LBL["trim_5v"], "")}
EMS_5V_NOTES = {
    "OIL TEMP SENSOR": (f"{CONFIRM} Dynon's fluid temperature sender (100409-001) is a single-stud sensor "
                        "grounded through its case: one wire, to the input pin (SkyView install guide, "
                        "fluid temperature section). The records also give it ground pin 5 and the shared "
                        "+5 V. Where do those two leads actually land?"),
    "FUEL FLOW TRANSDUCER": (f"{CONFIRM} Dynon's fuel flow transducer (100403-003) is powered from pin 15 "
                             "alone (SkyView install guide, EMS harness table), yet the record also lists "
                             "fuel flow on the shared +5 V. What does the 5 V lead feed?"),
}


# The handbook groups the pins by where the wire goes from the connector.
ROUTE = {"Through Firewall": "through the firewall", "Across Panel": "across the panel",
         "Down Left (Under Panel)": "down the left side, under the panel", "Shared Power": "shared"}


def extract_ems(_src=None):
    S = "EMS"
    out = []
    pins = {}
    for h in ("#### Through Firewall", "#### Across Panel", "#### Down Left (Under Panel)", "#### Shared Power"):
        for r in table(SYS24, h):
            pins[r["Pin"]] = (ROUTE[h[5:]], r)
    unused = by_pin(table(SYS24, "#### Unused Pins"))
    missing = sorted(set(str(n) for n in range(1, 38)) - set(pins) - set(unused), key=int)
    if missing:
        raise SystemExit(f"sys-24 EMS tables do not account for pins {missing}")

    for p, (where, r) in sorted(pins.items(), key=lambda kv: int(kv[0])):
        fn, c = r["Function"], r["Wire Color"]
        if p == "18":
            m = re.search(r"\(shared: (.*)\)", fn)
            seen = set()
            for name in (s.strip() for s in m.group(1).split(",")):
                ref, pin = EMS_5V[name]
                if (ref, pin) in seen:
                    continue
                seen.add((ref, pin))
                out.append(row(S, EMS, p, ref, pin, colour(c),
                               "shared +5 V; the firewall list records it as one spliced lead"
                               + (f". {EMS_5V_NOTES[ref]}" if ref in EMS_5V_NOTES else "")))
            continue
        hit = [(ref, pin) for pat, ref, pin in EMS_DEST if re.search(pat, fn)]
        if len(hit) != 1:
            raise SystemExit(f"sys-24 EMS pin {p}: function {fn!r} matched {len(hit)} destinations")
        ref, pin = hit[0]
        out.append(row(S, EMS, p, ref, pin, colour(c),
                       f"{fn}, routed {where}" + (f". {EMS_NOTES[ref]}" if ref in EMS_NOTES else "")))

    # Pin 31's handbook row describes the 2026 MZ-30 change, which
    # wiring/changes.tsv records with its history. Insist it still does.
    if "MZ-30" not in unused["31"]["Dynon Function"]:
        raise SystemExit("sys-24 EMS pin 31 no longer mentions the MZ-30; reconcile with wiring/changes.tsv")
    return out
