#!/usr/bin/env python3
"""Migrate N720AK reference files from Dropbox to Google Drive.

Copies and renames files from ~/Dropbox/N720AK/ to the Google Drive sync folder,
organizing them into Public/Private/Archive structure with kebab-case naming.

Usage: uv run python3 scripts/migrate_dropbox_to_gdrive.py [--dry-run]
"""

import shutil
import sys
from pathlib import Path

DROPBOX = Path.home() / "Dropbox" / "N720AK"
GDRIVE = (
    Path.home()
    / "Library"
    / "CloudStorage"
    / "GoogleDrive-sritchie09@gmail.com"
    / "My Drive"
    / "N720AK"
)

# (source relative to DROPBOX, dest relative to GDRIVE)
MANUAL_MAPPINGS = [
    # 22-Autopilot
    (
        "Manuals/SkyView_Autopilot_In-Flight_Tuning_Guide-Rev_F.pdf",
        "Public/Manuals/22-Autopilot/dynon-skyview-autopilot-tuning-guide-rev-f.pdf",
    ),
    (
        "Manuals/SkyView_System_Installation_Guide-Rev_AV.pdf",
        "Public/Manuals/22-Autopilot/dynon-skyview-system-install-guide-rev-av.pdf",
    ),
    # 23-Communications
    (
        "Manuals/GMA245.pdf",
        "Public/Manuals/23-Communications/garmin-gma245-pilots-guide.pdf",
    ),
    (
        "Manuals/GTN650_pilots_guide.pdf",
        "Public/Manuals/23-Communications/garmin-gtn650-pilots-guide.pdf",
    ),
    (
        "Manuals/ELT 345 Manual_Y1-03-0282R.pdf",
        "Public/Manuals/23-Communications/artex-elt345-manual.pdf",
    ),
    # 24-Electrical
    (
        "Manuals/vp-x-installation-and-operating-manual_rev-g3.pdf",
        "Public/Manuals/24-Electrical/vpx-sport-install-operating-manual-rev-g3.pdf",
    ),
    (
        "Manuals/Bus-Manager-Installation-Instructions-1-6-20.pdf",
        "Public/Manuals/24-Electrical/efii-bus-manager-install-instructions.pdf",
    ),
    # 28-Fuel-System
    (
        "Manuals/EFII_Installation_Manual_rev9-13.pdf",
        "Public/Manuals/28-Fuel-System/efii-system32-installation-manual-rev-9-13.pdf",
    ),
    (
        "Manuals/EFII_system32_installation.pdf",
        "Public/Manuals/28-Fuel-System/efii-system32-installation-manual-rev-6-19.pdf",
    ),
    # Note: System32-Installation-Manual-rev-6-19.pdf is a duplicate of above — skip
    (
        "Manuals/System32 Operating Procedures, 12-20.pdf",
        "Public/Manuals/28-Fuel-System/efii-system32-operating-procedures-12-20.pdf",
    ),
    (
        "Manuals/System32 Fuel Flow and RPM config, rev 10-19.pdf",
        "Public/Manuals/28-Fuel-System/efii-system32-fuel-flow-rpm-config-rev-10-19.pdf",
    ),
    (
        "Manuals/System32 Initial Tuning - Constant Speed Prop - rev 6-20.pdf",
        "Public/Manuals/28-Fuel-System/efii-system32-initial-tuning-csp-rev-6-20.pdf",
    ),
    (
        "Manuals/System32 Upgrade Installation Manual.docx",
        "Public/Manuals/28-Fuel-System/efii-system32-upgrade-installation-manual.docx",
    ),
    # 34-Navigation
    (
        "Manuals/Dynon_SkyView_HDX_Pilots_Users_Guide-Rev_Q.pdf",
        "Public/Manuals/34-Navigation/dynon-skyview-hdx-pilots-guide-rev-q.pdf",
    ),
    (
        "Manuals/SkyView_HDX_Pilots_Users_Guide-Rev_R.pdf",
        "Public/Manuals/34-Navigation/dynon-skyview-hdx-pilots-guide-rev-r.pdf",
    ),
    (
        "Manuals/SkyView_Customizing_the_EMS_Gauges.pdf",
        "Public/Manuals/34-Navigation/dynon-skyview-ems-gauge-customization.pdf",
    ),
    (
        "Manuals/Skyview_Third_Party_Device_Connection_and_Configuration_Reference-Rev_E.pdf",
        "Public/Manuals/34-Navigation/dynon-skyview-third-party-device-connection-rev-e.pdf",
    ),
    (
        "Manuals/TLAR Pilot Guide v7.80.pdf",
        "Public/Manuals/34-Navigation/tlar-pilot-guide-v7.80.pdf",
    ),
    # 35-Oxygen
    (
        "Manuals/eds4ip_oxygen.pdf",
        "Public/Manuals/35-Oxygen/mountain-high-eds4ip-manual.pdf",
    ),
    # 71-Engine
    (
        "Manuals/Separator-vacuum-sys.pdf",
        "Public/Manuals/71-Engine/separator-vacuum-sys.pdf",
    ),
    # Misc
    (
        "Manuals/RV-10-Gust-Lock.pdf",
        "Public/Manuals/Misc/rv10-gust-lock-instructions.pdf",
    ),
]

SCHEMATIC_MAPPINGS = [
    ("Schematics/MH_Oxygen.pdf", "Public/Schematics/mountain-high-oxygen-schematic.pdf"),
    ("Schematics/Power__Lighting.pdf", "Public/Schematics/power-and-lighting-schematic.pdf"),
    ("Schematics/SV_Interconnect.pdf", "Public/Schematics/skyview-interconnect-schematic.pdf"),
    ("Schematics/VP-X_Pro-Sport_LPW.xls", "Public/Schematics/vpx-pro-sport-lpw.xls"),
]

PERFORMANCE_MAPPINGS = [
    (
        "ADSBPerformanceReport01282026.pdf",
        "Public/Performance/adsb-performance-report-2026-01-28.pdf",
    ),
    (
        "N720AK Airspeed Data Collection 2_4_26.pdf",
        "Public/Performance/n720ak-airspeed-data-2026-02-04.pdf",
    ),
    (
        "N720AK Airspeed Data Collection 2_4_26.xlsx",
        "Public/Performance/n720ak-airspeed-data-2026-02-04.xlsx",
    ),
    ("prop_balance_02_2026.htm", "Public/Performance/prop-balance-2026-02.htm"),
    ("prop_balance_12_2025.htm", "Public/Performance/prop-balance-2025-12.htm"),
]

PRIVATE_MAPPINGS = [
    ("GallagherCoverage.pdf", "Private/Insurance/gallagher-coverage.pdf"),
    ("engine_registration.pdf", "Private/Registration/engine-registration.pdf"),
    ("repairman.pdf", "Private/Registration/repairman-certificate.pdf"),
]

ARCHIVE_SINGLE = [
    ("RVator27Years.pdf", "Archive/RVator-27-Years.pdf"),
]

# Directories to copy recursively (source dir, dest dir)
DIR_COPIES = [
    # OnSpeed schematics
    ("Schematics/OnSpeed", "Public/Schematics/OnSpeed"),
    # Configs
    ("Dynon Configs", "Public/Configs/Dynon"),
    ("OnSpeed Cals", "Public/Configs/OnSpeed"),
    # W&B
    ("W&B", "Public/Weight-Balance"),
    # Private dirs
    ("Invoices", "Private/Invoices/misc"),
    ("Transition Training", "Private/Transition-Training"),
    ("Vans Forms", "Private/Vans-Forms"),
    # Archive dirs
    ("Plans/Construction Drawings", "Archive/Construction-Drawings"),
    ("Plans/Brochures", "Archive/Brochures"),
    ("POH : Checklist Examples", "Archive/POH-Examples"),
]


def copy_file(src: Path, dst: Path, dry_run: bool) -> bool:
    """Copy a single file, creating parent dirs. Returns True if copied."""
    if not src.exists():
        print(f"  SKIP (not found): {src}")
        return False
    if dst.exists():
        print(f"  SKIP (exists):    {dst.name}")
        return False
    if dry_run:
        print(f"  WOULD COPY: {src.name} -> {dst}")
        return True
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    print(f"  COPIED: {src.name} -> {dst.relative_to(GDRIVE)}")
    return True


def copy_dir_contents(src_dir: Path, dst_dir: Path, dry_run: bool) -> int:
    """Copy all files from src_dir to dst_dir. Returns count of files copied."""
    if not src_dir.exists():
        print(f"  SKIP (dir not found): {src_dir}")
        return 0
    count = 0
    for f in sorted(src_dir.iterdir()):
        if f.name.startswith(".") or f.name == "Icon\r":
            continue
        if f.is_file():
            count += copy_file(f, dst_dir / f.name, dry_run)
        elif f.is_dir():
            count += copy_dir_contents(f, dst_dir / f.name, dry_run)
    return count


def main():
    dry_run = "--dry-run" in sys.argv

    if not DROPBOX.exists():
        print(f"ERROR: Dropbox source not found: {DROPBOX}")
        sys.exit(1)
    if not GDRIVE.parent.exists():
        print(f"ERROR: Google Drive not found: {GDRIVE.parent}")
        sys.exit(1)

    GDRIVE.mkdir(exist_ok=True)

    if dry_run:
        print("=== DRY RUN — no files will be copied ===\n")

    total = 0

    print("--- Manuals ---")
    for src_rel, dst_rel in MANUAL_MAPPINGS:
        total += copy_file(DROPBOX / src_rel, GDRIVE / dst_rel, dry_run)

    print("\n--- Schematics ---")
    for src_rel, dst_rel in SCHEMATIC_MAPPINGS:
        total += copy_file(DROPBOX / src_rel, GDRIVE / dst_rel, dry_run)

    print("\n--- Performance ---")
    for src_rel, dst_rel in PERFORMANCE_MAPPINGS:
        total += copy_file(DROPBOX / src_rel, GDRIVE / dst_rel, dry_run)

    print("\n--- Private (single files) ---")
    for src_rel, dst_rel in PRIVATE_MAPPINGS:
        total += copy_file(DROPBOX / src_rel, GDRIVE / dst_rel, dry_run)

    print("\n--- Archive (single files) ---")
    for src_rel, dst_rel in ARCHIVE_SINGLE:
        total += copy_file(DROPBOX / src_rel, GDRIVE / dst_rel, dry_run)

    print("\n--- Directory copies ---")
    for src_rel, dst_rel in DIR_COPIES:
        src_dir = DROPBOX / src_rel
        dst_dir = GDRIVE / dst_rel
        print(f"  [{src_rel}] -> [{dst_rel}]")
        total += copy_dir_contents(src_dir, dst_dir, dry_run)

    action = "would copy" if dry_run else "copied"
    print(f"\nDone! {total} files {action}.")


if __name__ == "__main__":
    main()
