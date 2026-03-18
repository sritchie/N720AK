#!/usr/bin/env python3
"""Build printable maintenance logbook PDFs from TSV records.

Reads TSV maintenance logs from Google Drive, generates Typst source files,
and compiles them to professional PDF logbooks for printing and binding.

Usage:
  uv run python3 scripts/build_logbooks.py --all
  uv run python3 scripts/build_logbooks.py --type engine
  uv run python3 scripts/build_logbooks.py --type airframe --type avionics

Output:
  output/logbooks/N720AK-{type}-log-{timestamp}.pdf
  Also copies to GDrive: N720AK/Private/Maintenance/logbooks/
"""

import argparse
import csv
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from textwrap import dedent

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

GDRIVE_MAINT = os.path.expanduser(
    "~/Library/CloudStorage/GoogleDrive-sritchie09@gmail.com/"
    "My Drive/N720AK/Private/Maintenance"
)

REPO_ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_PATH = REPO_ROOT / "templates" / "logbook.typ"
OUTPUT_DIR = REPO_ROOT / "output" / "logbooks"

AIRCRAFT = {
    "type": "RV-10",
    "n_number": "N720AK",
    "serial": "41649",
    "builder": "Samuel E. Ritchie",
}

LOGBOOK_CONFIGS = {
    "airframe": {
        "tsv_file": "airframe-log.tsv",
        "title": "Airframe",
        "data_page": dedent("""\
            #text(size: 14pt, weight: "bold")[Airframe Data]
            #v(0.3in)

            #table(
              columns: (1.8in, 1fr),
              stroke: 0.4pt + rgb("#ddd"),
              inset: 6pt,
              table.cell(fill: rgb("#f0f0f0"))[Aircraft Type], [Van's RV-10],
              table.cell(fill: rgb("#f0f0f0"))[N-Number], [N720AK],
              table.cell(fill: rgb("#f0f0f0"))[Serial Number], [41649],
              table.cell(fill: rgb("#f0f0f0"))[Builder], [Samuel E. Ritchie],
              table.cell(fill: rgb("#f0f0f0"))[Airworthiness Certificate], [Special — Experimental, Amateur Built],
              table.cell(fill: rgb("#f0f0f0"))[Certificate Date], [November 19, 2025],
              table.cell(fill: rgb("#f0f0f0"))[DAR], [Robert P. Husted, \\#554433181],
              table.cell(fill: rgb("#f0f0f0"))[Empty Weight], [1,643 lb],
              table.cell(fill: rgb("#f0f0f0"))[Empty Weight CG], [106.96 in aft of datum],
              table.cell(fill: rgb("#f0f0f0"))[Max Gross Weight], [2,700 lb],
            )

            #v(0.3in)
            #text(size: 10pt, weight: "bold")[Condition Inspection Requirements]
            #v(0.1in)
            #text(size: 9pt)[
              Per Operating Limitations item 10: No person may operate this aircraft unless within the preceding 12 calendar months it has had a condition inspection performed per the scope and detail of Part 43, Appendix D, and was found to be in a condition for safe operation.

              The inspections must be recorded in the aircraft maintenance records showing the following or a similarly worded statement: "I certify that this aircraft has been inspected on \\[date\\] per the \\[insert either: scope and detail of Part 43, Appendix D; or manufacturer's inspection procedures\\] and was found to be in a condition for safe operation."
            ]
        """),
    },
    "engine": {
        "tsv_file": "engine-log.tsv",
        "title": "Engine",
        "data_page": dedent("""\
            #text(size: 14pt, weight: "bold")[Engine Data]
            #v(0.3in)

            #table(
              columns: (1.8in, 1fr),
              stroke: 0.4pt + rgb("#ddd"),
              inset: 6pt,
              table.cell(fill: rgb("#f0f0f0"))[Engine Model], [Lycoming YIO-540-D4A5],
              table.cell(fill: rgb("#f0f0f0"))[Serial Number], [EL-36315-48E],
              table.cell(fill: rgb("#f0f0f0"))[Part Number], [YENPL-RT10474],
              table.cell(fill: rgb("#f0f0f0"))[Work Order], [AR608690],
              table.cell(fill: rgb("#f0f0f0"))[Manufacture Date], [July 6, 2015],
              table.cell(fill: rgb("#f0f0f0"))[Horsepower], [260 HP],
              table.cell(fill: rgb("#f0f0f0"))[Installed], [November 18, 2025],
              table.cell(fill: rgb("#f0f0f0"))[Crankcase Match], [K2463],
              table.cell(fill: rgb("#f0f0f0"))[Crankshaft Serial], [V537968878],
            )

            #v(0.2in)
            #text(size: 10pt, weight: "bold")[Factory Accessories (as shipped — most removed for EFII installation)]
            #v(0.1in)
            #text(size: 8pt)[
              #table(
                columns: (1.2in, 1in, 0.8in, 1in),
                stroke: 0.3pt + rgb("#ddd"),
                inset: 4pt,
                table.cell(fill: rgb("#e8e8e8"))[Part], table.cell(fill: rgb("#e8e8e8"))[P/N], table.cell(fill: rgb("#e8e8e8"))[Mfr], table.cell(fill: rgb("#e8e8e8"))[S/N],
                [Starter], [31B23592], [SKY-TEC], [FN-1615110],
                [Fuel Pump], [62B26931], [Lycoming], [RC26150971109],
              )
            ]

            #v(0.2in)
            #text(size: 10pt, weight: "bold")[Current Ignition / Fuel Injection]
            #v(0.1in)
            #text(size: 9pt)[
              ProTek Performance EFII System32-6R — dual electronic ignition and fuel injection with dual ECU. Installed November 18, 2025, replacing factory injector, magnetos, ignition harness, spark plugs, and engine-driven fuel pump.
            ]
        """),
    },
    "propeller": {
        "tsv_file": "propeller-log.tsv",
        "title": "Propeller",
        "data_page": dedent("""\
            #text(size: 14pt, weight: "bold")[Propeller Data]
            #v(0.3in)

            #table(
              columns: (1.8in, 1fr),
              stroke: 0.4pt + rgb("#ddd"),
              inset: 6pt,
              table.cell(fill: rgb("#f0f0f0"))[Propeller Model], [Whirlwind WWA RV-10 Series],
              table.cell(fill: rgb("#f0f0f0"))[Hub Serial Number], [RV10-366],
              table.cell(fill: rgb("#f0f0f0"))[Blade Serial Numbers], [RV10-443 and RV10-444],
              table.cell(fill: rgb("#f0f0f0"))[Manufacture Date], [October 12, 2017],
              table.cell(fill: rgb("#f0f0f0"))[Installed], [November 18, 2025],
              table.cell(fill: rgb("#f0f0f0"))[Diameter], [80 inches],
              table.cell(fill: rgb("#f0f0f0"))[Weight], [44 lbs],
              table.cell(fill: rgb("#f0f0f0"))[Pitch Range], [High: 35.1° / Low: 12.8°],
              table.cell(fill: rgb("#f0f0f0"))[RPM Max], [2700],
              table.cell(fill: rgb("#f0f0f0"))[Flange Bolt Torque], [65 ft-lbs (dry), 1/2" hardware],
              table.cell(fill: rgb("#f0f0f0"))[Colors], [Black (DBC9700) / White tips (DBC2185)],
            )

            #v(0.2in)
            #text(size: 10pt, weight: "bold")[Governor]
            #v(0.1in)
            #text(size: 9pt)[
              Aero Technologies (Jihostroj) PCU5000X constant-speed governor. Experimental version of the Jihostroj PCU5000. Pumps 30–35% more oil than comparable governors.
            ]

            #v(0.2in)
            #text(size: 10pt, weight: "bold")[Inspection Requirements]
            #v(0.1in)
            #text(size: 9pt)[
              Propeller inspection required at 650 hours or 5 years from first engine start (November 18, 2025), whichever comes first. Due by November 18, 2030 or 650 hours. Annual visual inspection required. Propeller must be returned to Whirlwind Aviation for overhaul.

              Avoid continuous operation between 2050–2300 RPM and 2600–2700 RPM (4-cylinder engines only; per Whirlwind confirmation 12/12/2025, this restriction does not apply to 6-cylinder engines with the RV-10 propeller).
            ]
        """),
    },
    "avionics": {
        "tsv_file": "avionics-log.tsv",
        "title": "Avionics",
        "data_page": dedent("""\
            #text(size: 14pt, weight: "bold")[Avionics Inventory]
            #v(0.2in)

            #text(size: 8pt)[
              #table(
                columns: (1.6in, 1.2in, 0.8in, 1.2in),
                stroke: 0.3pt + rgb("#ddd"),
                inset: 4pt,
                table.cell(fill: rgb("#e8e8e8"))[Component], table.cell(fill: rgb("#e8e8e8"))[Model], table.cell(fill: rgb("#e8e8e8"))[S/N], table.cell(fill: rgb("#e8e8e8"))[Location],
                [PFD (Pilot)], [SV-HDX-1100], [11668], [Panel, pilot],
                [PFD (Copilot)], [SV-HDX-1100], [11672], [Panel, copilot],
                [MFD (Center)], [SV-HDX-800], [10980], [Panel, center],
                [ADAHRS Primary], [SV-ADAHRS-200], [8375], [Tailcone],
                [ADAHRS Secondary], [SV-ADAHRS-201], [4928], [Tailcone],
                [Engine Monitor], [SV-EMS-220], [6468], [Subpanel, pilot],
                [ADS-B In/Out], [SV-ADSB-472], [13201], [Tailcone],
                [Transponder], [SV-XPNDR-261], [4015], [—],
                [AP Panel], [SV-AP-PANEL/V], [4101], [Panel, center],
                [Knob Panel], [SV-KNOB-PANEL/V], [8500], [Panel, center],
                [Com Panel], [SV-COM-PANEL/V], [3090], [Panel, center],
                [Com Radio], [SV-COM-C25/V], [2494], [Subpanel],
                [ARINC Module], [SV-ARINC-429], [2360], [Subpanel],
                [GPS Module], [SV-GPS-250], [1016], [—],
                [Electrical], [SV-VPX-290], [7645], [—],
                [VP-X Sport], [VP-X-SPORT], [2076], [—],
                [Yaw Servo], [SV-42], [11273], [Tailcone],
                [Pitch Servo], [SV-42T], [50220], [Tailcone],
                [Nav/GPS/Com], [GTN 650], [1Z8021616], [Panel, center],
                [Audio Panel], [GMA 245], [3YL000434], [—],
                [ELT], [Artex ELT 345], [267-02567], [Empennage],
                [CO Detector], [452-101-012], [112081], [Panel, copilot],
                [Ignition/FI], [EFII System32-6R], [—], [Subpanel, copilot],
                [Bus Manager], [EFII System32], [—], [Subpanel, center],
                [AOA], [OnSpeed V4P], [dev], [Subpanel, pilot],
                [Backup Alt], [Monkworkz MZ-30], [—], [Engine vac pad],
              )
            ]

            #v(0.2in)
            #text(size: 10pt, weight: "bold")[Transponder / Altimeter / Static Biennial]
            #v(0.1in)
            #text(size: 9pt)[
              Last check: December 10, 2025 by Front Range Transponder Svc (CRS F42R379Y). Mode A/C and S. Next due December 31, 2027.
            ]

            #v(0.1in)
            #text(size: 10pt, weight: "bold")[ELT Beacon Registration]
            #v(0.1in)
            #text(size: 9pt)[
              Hex code: 2DC88 5940E FFBFF. Registration expires November 18, 2027.
            ]
        """),
    },
}


# ---------------------------------------------------------------------------
# TSV Parsing
# ---------------------------------------------------------------------------

def read_tsv(filepath: str) -> list[dict]:
    """Read a TSV maintenance log and return list of entry dicts."""
    entries = []

    def get(row, key):
        val = row.get(key)
        return val.strip() if val else ""

    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            # Skip empty rows
            if not get(row, "Date"):
                continue
            entries.append({
                "date": get(row, "Date"),
                "tach": get(row, "Tach"),
                "hobbs": get(row, "Hobbs"),
                "work_type": get(row, "Work Type"),
                "description": get(row, "Description"),
                "parts": get(row, "Parts Used"),
                "performed_by": shorten_performer(get(row, "Performed By")),
                "reference": get(row, "Reference"),
                "notes": get(row, "Notes"),
                "next_due_hrs": get(row, "Next Due (hrs)"),
                "next_due_date": get(row, "Next Due (date)"),
            })
    # Sort chronologically
    entries.sort(key=lambda e: e["date"])
    return entries


def shorten_performer(name: str) -> str:
    """Shorten 'Sam Ritchie (Repairman 5256450)' to 'S. Ritchie (Rep. 5256450)'."""
    name = name.replace("Sam Ritchie (Repairman ", "S. Ritchie (Rep. ")
    name = name.replace("Sam Ritchie (Pilot ", "S. Ritchie (Pilot ")
    return name


# ---------------------------------------------------------------------------
# Typst Generation
# ---------------------------------------------------------------------------

def escape_typst(s: str) -> str:
    """Escape special characters for Typst string literals."""
    s = s.replace("\\", "\\\\")
    s = s.replace('"', '\\"')
    s = s.replace("#", "\\#")
    s = s.replace("$", "\\$")
    s = s.replace("@", "\\@")
    s = s.replace("<", "\\<")
    s = s.replace(">", "\\>")
    return s


def generate_typst(logbook_type: str, entries: list[dict], timestamp: str) -> str:
    """Generate a complete Typst source file for a logbook."""
    config = LOGBOOK_CONFIGS[logbook_type]

    # Build the entries array for Typst
    entry_lines = []
    for e in entries:
        # Build the "next due" string from hours and/or date
        next_due_parts = []
        if e["next_due_hrs"]:
            next_due_parts.append(f"{e['next_due_hrs']} hrs")
        if e["next_due_date"]:
            next_due_parts.append(e["next_due_date"])
        next_due = " / ".join(next_due_parts)

        entry_lines.append(
            f'    (date: "{escape_typst(e["date"])}", '
            f'tach: "{escape_typst(e["tach"])}", '
            f'hobbs: "{escape_typst(e["hobbs"])}", '
            f'work_type: "{escape_typst(e["work_type"])}", '
            f'description: "{escape_typst(e["description"])}", '
            f'parts: "{escape_typst(e["parts"])}", '
            f'performed_by: "{escape_typst(e["performed_by"])}", '
            f'notes: "{escape_typst(e["notes"])}", '
            f'next_due: "{escape_typst(next_due)}"),'
        )

    entries_str = "\n".join(entry_lines)

    # Date range for informational purposes
    if entries:
        date_range = f"{entries[0]['date']} through {entries[-1]['date']}"
    else:
        date_range = "No entries"

    return f"""\
#import "/templates/logbook.typ": logbook

#logbook(
  aircraft-type: "{AIRCRAFT['type']}",
  n-number: "{AIRCRAFT['n_number']}",
  serial-number: "{AIRCRAFT['serial']}",
  builder: "{AIRCRAFT['builder']}",
  logbook-type: "{config['title']}",
  generated-date: "{timestamp}",
  data-page-content: [
{config['data_page']}
  ],
  entries: (
{entries_str}
  ),
)
"""


# ---------------------------------------------------------------------------
# Build Pipeline
# ---------------------------------------------------------------------------

def build_logbook(logbook_type: str, timestamp: str, output_dir: Path) -> Path | None:
    """Build a single logbook PDF. Returns the output path or None on failure."""
    config = LOGBOOK_CONFIGS[logbook_type]
    tsv_path = os.path.join(GDRIVE_MAINT, config["tsv_file"])

    if not os.path.exists(tsv_path):
        print(f"  WARNING: {tsv_path} not found, skipping {logbook_type}")
        return None

    entries = read_tsv(tsv_path)
    print(f"  {config['title']}: {len(entries)} entries from {config['tsv_file']}")

    # Generate Typst source
    typst_src = generate_typst(logbook_type, entries, timestamp)

    # Write to temp file
    output_dir.mkdir(parents=True, exist_ok=True)
    typst_file = output_dir / f"N720AK-{logbook_type}-log.typ"
    pdf_file = output_dir / f"N720AK-{logbook_type}-log-{timestamp.replace(' ', '_').replace(':', '')}.pdf"

    typst_file.write_text(typst_src, encoding="utf-8")

    # Compile with typst (--root allows importing templates from repo root)
    result = subprocess.run(
        ["typst", "compile", "--root", str(REPO_ROOT), str(typst_file), str(pdf_file)],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print(f"  ERROR compiling {logbook_type}:")
        print(result.stderr)
        return None

    # Clean up .typ source
    typst_file.unlink()

    print(f"  -> {pdf_file.name}")
    return pdf_file


def copy_to_gdrive(pdf_path: Path) -> None:
    """Copy a generated PDF to GDrive for backup."""
    gdrive_logbooks = os.path.join(GDRIVE_MAINT, "logbooks")
    os.makedirs(gdrive_logbooks, exist_ok=True)
    dest = os.path.join(gdrive_logbooks, pdf_path.name)
    shutil.copy2(str(pdf_path), dest)
    print(f"  -> GDrive: Maintenance/logbooks/{pdf_path.name}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Build printable maintenance logbook PDFs from TSV records."
    )
    parser.add_argument(
        "--type", "-t",
        action="append",
        choices=list(LOGBOOK_CONFIGS.keys()),
        help="Logbook type(s) to build (can specify multiple). Default: all.",
    )
    parser.add_argument(
        "--all", "-a",
        action="store_true",
        help="Build all logbook types.",
    )
    parser.add_argument(
        "--output-dir", "-o",
        type=Path,
        default=OUTPUT_DIR,
        help=f"Output directory (default: {OUTPUT_DIR})",
    )
    parser.add_argument(
        "--no-gdrive",
        action="store_true",
        help="Don't copy PDFs to Google Drive.",
    )
    parser.add_argument(
        "--open",
        action="store_true",
        help="Open generated PDFs after building.",
    )

    args = parser.parse_args()

    if args.all or args.type is None:
        types = list(LOGBOOK_CONFIGS.keys())
    else:
        types = args.type

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    print(f"Building {len(types)} logbook(s) — {timestamp}")
    print()

    pdfs = []
    for lt in types:
        pdf = build_logbook(lt, timestamp, args.output_dir)
        if pdf:
            pdfs.append(pdf)
            if not args.no_gdrive:
                copy_to_gdrive(pdf)
        print()

    if pdfs:
        print(f"Done! {len(pdfs)} PDF(s) generated in {args.output_dir}/")
        print()
        print("Printing recommendations:")
        print("  - US Letter, landscape, double-sided")
        print("  - 24lb or 32lb paper for durability")
        print("  - 3-hole punch for binder, or comb/saddle-stitch binding")
        if args.open:
            for pdf in pdfs:
                subprocess.run(["open", str(pdf)])
    else:
        print("No PDFs generated.")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)
