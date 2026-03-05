# N720AK RV-10 Pilot's Operating Handbook

This repository contains the Pilot's Operating Handbook (POH) for **N720AK**, a Van's RV-10 experimental aircraft. The POH follows [GAMA Specification No. 1](https://gama.aero/documents/gama-specification-1-specification-for-pilots-operating-handbook-version-2-0/) format.

## Repository Purpose

1. **POH Source Files**: Markdown files in `sections/` that compile to PDF and HTML
2. **Checklist Sync**: `N720AK.json` synced from the EFIS Editor for Dynon/ForeFlight export
3. **Weight & Balance**: Exportable W&B data for sharing with other pilots
4. **GitHub Pages**: Auto-deploys HTML version on push to main (target: n720ak.com)

## Checklist Synchronization

**Canonical checklist source**: https://rdamazio.github.io/efis-editor/checklists#N720AK

The workflow:
1. Edit checklists at the EFIS Editor URL above
2. Export JSON and save as `N720AK.json` in this repo
3. Run `python3 json_to_markdown.py N720AK.json` to generate `04-emergency.md`, `04b-abnormal.md`, `05-normal.md`
4. Export from EFIS Editor to Dynon (.txt) and ForeFlight (.fmd) as needed
5. Commit and push - GitHub Pages deploys automatically

This keeps checklists synchronized across:
- Dynon Skyview HDX (in-cockpit EFIS)
- ForeFlight (EFB)
- POH PDF (paper backup)
- POH HTML (web reference)

## Build Commands

```bash
# Build PDF (requires pandoc + typst)
./build.sh pdf

# Build HTML site (requires mdbook)
./build.sh html

# Start dev server with live reload
./build.sh serve

# Build both PDF and HTML
./build.sh all
```

### Prerequisites

```bash
# macOS
brew install pandoc typst mdbook

# Or install individually:
# Pandoc: https://pandoc.org/installing.html
# Typst: https://github.com/typst/typst/releases
# mdBook: https://rust-lang.github.io/mdBook/guide/installation.html
```

## Directory Structure

```
rv10/
├── CLAUDE.md              # This file
├── README.md              # Build instructions
├── book.toml              # mdBook configuration
├── metadata.yaml          # PDF title, author, revision
├── template.typ           # Typst template for PDF styling
├── build.sh               # Build script (pdf/html/serve)
├── json_to_markdown.py    # Converts checklist JSON to markdown
├── N720AK.json            # Canonical checklist (from EFIS Editor)
├── sections/
│   ├── SUMMARY.md         # mdBook table of contents
│   ├── 00-introduction.md
│   ├── 01-general.md      # General info, specs, dimensions
│   ├── 02-limitations.md  # Operating limits, V-speeds, placards
│   ├── 03-engine-info.md  # Engine performance charts
│   ├── 04-emergency.md    # [GENERATED] Emergency procedures
│   ├── 04b-abnormal.md    # [GENERATED] Abnormal procedures
│   ├── 05-normal.md       # [GENERATED] Normal procedures
│   ├── 06-performance.md  # Performance charts
│   ├── 07-weight-balance.md
│   ├── 08-systems.md      # Aircraft systems descriptions
│   ├── 09-servicing.md    # Handling, servicing, maintenance
│   ├── sys-22-autopilot.md      # Systems Reference: Dynon 3-axis AP
│   ├── sys-23-communications.md # Systems Reference: GMA 245, audio, intercom
│   ├── sys-24-electrical.md     # Systems Reference: buses, VPX, batteries
│   ├── sys-27-flight-controls.md # Systems Reference: stick grip, trim, flaps
│   ├── sys-28-fuel-system.md    # Systems Reference: complete fuel system
│   ├── sys-33-lighting.md       # Systems Reference: AeroLEDs, wingtip lights
│   ├── sys-34-navigation.md     # Systems Reference: Dynon, GTN 650, pitot-static
│   ├── sys-34-onspeed.md        # Systems Reference: OnSpeed AoA system
│   ├── sys-35-oxygen.md         # Systems Reference: Mountain High O2
│   ├── sys-42-avionics.md       # Systems Reference: wiring, panel, interconnects
│   ├── sys-61-brakes.md         # Systems Reference: brakes, wheels, tires
│   ├── sys-71-engine.md         # Systems Reference: Lycoming mechanical
│   ├── sys-73-efii.md           # Systems Reference: EFII System32 EFI/ignition
│   └── sys-84-propeller.md      # Systems Reference: prop and governor
├── docs/                  # Manufacturer PDFs organized by ATA chapter
│   ├── README.md          # Naming convention and organization
│   ├── 22-autopilot/      # Dynon AP install guide, servo manuals
│   ├── 23-communications/ # GMA 245 pilot guide, antenna specs
│   ├── 24-electrical/     # VPX Sport manual, EarthX specs
│   ├── 27-flight-controls/ # Tosten grip docs
│   ├── 28-fuel-system/    # Aeromotive regulator, Walbro pump docs
│   ├── 33-lighting/       # AeroLEDs install guides
│   ├── 34-navigation/     # Dynon Skyview, GTN 650, OnSpeed docs
│   ├── 35-oxygen/         # Mountain High EDS-4iP manual
│   ├── 42-avionics/       # Wiring diagrams, connector pinouts
│   ├── 61-brakes/         # Brake caliper docs, wheel specs
│   ├── 71-engine/         # Lycoming operator's manual
│   ├── 73-efii/           # EFII System32 manual, tuning guides
│   ├── 84-propeller/      # Prop manual, governor docs
│   └── misc/              # Anything that doesn't fit
├── images/                # Aircraft photos, diagrams
├── maintenance/
│   └── fuel-system/
│       └── flight-logs/   # Archived analysis results
├── scripts/               # Analysis scripts (regulator diagnostic, etc.)
├── plans/                 # Maintenance and diagnostic plans
└── output/
    ├── poh.pdf            # Generated PDF
    └── html/              # Generated HTML site
```

## POH Sections (GAMA Spec No. 1)

| Section | File | Content |
|---------|------|---------|
| 1 | `01-general.md` | Aircraft description, dimensions, specifications |
| 2 | `02-limitations.md` | V-speeds, engine limits, weight/CG limits, placards |
| 3 | `03-engine-info.md` | Engine performance charts |
| 4 | `04-emergency.md` | Emergency procedures (generated from JSON) |
| 4b | `04b-abnormal.md` | Abnormal procedures (generated from JSON) |
| 5 | `05-normal.md` | Normal procedures (generated from JSON) |
| 6 | `06-performance.md` | Takeoff, climb, cruise, landing performance |
| 7 | `07-weight-balance.md` | Empty weight, CG envelope, loading |
| 8 | `08-systems.md` | All aircraft systems descriptions |
| 9 | `09-servicing.md` | Ground handling, servicing, maintenance |

## Aircraft Configuration - N720AK

### Avionics

| System | Component | Notes |
|--------|-----------|-------|
| Audio Panel | Garmin GMA245 | |
| Nav/GPS | Garmin GTN 650 | Certified IFR, single nav antenna (Bob Archer) |
| EFIS | Dynon Skyview HDX | Primary flight display |
| Autopilot | Dynon 3-axis | Roll servo, pitch servo, yaw damper |
| Panels | Dynon | Comm panel, autopilot panel, knob panels |
| ELT | Artex ELT 345 | 406 MHz |

### Power Management

| System | Component | Notes |
|--------|-----------|-------|
| Bus Manager | flyEFII System32 | Controls full system vs emergency endurance bus |
| Electronic Breakers | VPX Sport | Power distribution and protection |
| Battery 1 | EarthX ETX900 | |
| Battery 2 | EarthX ETX900 | |
| Alternator | 60 amp | Single alternator |

**Emergency Endurance Bus**: The System32 Bus Manager automatically switches to the endurance bus if a battery fails, shedding non-essential loads to preserve power for critical systems.

### Engine

| System | Component | Notes |
|--------|-----------|-------|
| Ignition | EFII System32 | Full electronic ignition |
| Fuel Injection | EFII System32 | Electronic fuel injection |
| Fuel Pumps | Primary + Backup | Pressurize fuel line with return to each tank |

### Oxygen

| System | Component | Notes |
|--------|-----------|-------|
| O2 System | Mountain High EDS-4iP | Pulse on demand |
| Mode Switch | Panel mounted | Toggles pulse-on-demand ↔ constant flow |

### Flight Controls

| System | Component | Notes |
|--------|-----------|-------|
| Stick Grip | Tosten CS Military | Document button layout with photo |
| Co-pilot Trim | Panel switch | Enable/disable co-pilot trim |

### Pitot-Static

| System | Component | Notes |
|--------|-----------|-------|
| Pitot Tube | Dynon heated | Includes AoA probe |
| Alternate Static | Panel valve | Top left of panel |

### Other Systems

| System | Component | Notes |
|--------|-----------|-------|
| Door Lock | Cam mechanism | Locking mechanism |
| Brake Fluid | Royco 782 | MIL-PRF-83282 hydraulic fluid |
| Wing Lights | AeroSun VX | LED position/strobe in wingtips |
| Nav Antenna | Bob Archer | For GTN 650 |
| Wingtips | Piano hinge mod | Removable for maintenance |

## What Goes Where: POH vs Systems Reference

### POH (Sections 00-09) — PDF + HTML

Information a **pilot** needs for **normal operation**. This is the GAMA Spec No. 1 content that compiles to both PDF and HTML.

**Section 8 - Systems Description:** How each system works (operational description), panel switch locations, stick grip layout, emergency bus behavior.

**Section 9 - Handling, Servicing:** Brake fluid type, tire pressures, oil specs, fuel specs, preflight items, service intervals.

### Systems Reference (sys-*.md) — HTML Only

Comprehensive technical reference for **how the airplane is built and how everything works**. This is NOT just maintenance — it's the complete "how is my airplane built" reference. Includes:

- Part numbers, suppliers, data sheets
- Wiring/plumbing details, AN fittings, routing
- Tuning notes, calibration data
- Diagnostic procedures and flight data analysis
- Lessons learned, installation quirks
- Photos with captions

**Key constraint:** Systems Reference pages use `sys-XX-` prefix (ATA chapter numbers). The PDF build in `build.sh` explicitly lists sections 00-09, so sys-* files are automatically excluded. No build changes needed.

Each system page links to manufacturer PDFs stored in `docs/XX-*/` and to scripts/plans via GitHub URLs (since those directories aren't served by mdBook).

### Reference Documents (docs/)

Manufacturer PDFs, install guides, and reference materials organized by ATA chapter number in `docs/`. Use descriptive filenames (e.g., `dynon-skyview-install-guide-rev15.pdf`, not `manual.pdf`). System pages link to these with relative paths like `../docs/34-navigation/filename.pdf`.

### Analysis Scripts

```
scripts/
└── regulator_diagnostic.py    # Fuel pressure regulator diagnostic
                               # Auto-detects Dynon/Garmin CSV format
                               # Computes: delta σ, MAP slope, FF slope, residual σ
                               # Generates 4-panel diagnostic plot
                               # Supports altitude correction (--alt-correct)
                               # and correction fraction scan (--alt-scan)
```

Run with: `uv run --with numpy --with matplotlib python3 scripts/regulator_diagnostic.py /path/to/log.csv`

### Plans

```
plans/
└── regulator-diagnostic.md    # Workflow for analyzing regulator health
                               # Includes baseline targets, how to run, what to look for
```

### Key Fuel System Findings (as of 2026-03)

- N720AK's Aeromotive regulator has consistent MAP slope of **−0.30 PSI/inHg** (should be ~0)
- Variable sticking/hunting: residual σ ranges from 0.18 to 1.25 PSI across flights
- Reference baseline (N88810, same regulator): σ = 0.08 PSI, slope = −0.01 — essentially perfect
- Dynon fuel pressure sensor appears to be baro-compensated (altitude correction fraction ≈ 0)
- Garmin fuel pressure sensor is standard gauge (needs altitude correction, fraction = 1.0)
- Full details: `sections/sys-28-fuel-system.md`

## Weight & Balance for ForeFlight

To share W&B with other pilots, create a ForeFlight-compatible aircraft profile export that includes:
- Empty weight and CG
- Fuel tank arm(s)
- Seat arm locations
- Baggage arm locations
- CG envelope limits

This allows guest pilots to do accurate W&B in ForeFlight before flying N720AK.

## Deployment

On push to `main`, GitHub Actions:
1. Builds HTML with mdBook
2. Deploys to GitHub Pages

Target domain: **n720ak.com** (configure in GitHub Pages settings)

## Systems Reference TODOs

The Systems Reference pages (`sections/sys-*.md`) contain `<!-- TODO -->` markers and structured TODO checklists at the bottom of each file. These represent information that needs to come from the owner (part numbers, photos, procedures, measurements, supplier info, etc.).

**When the user asks about TODOs, or asks to work on a system page, or says something like "let's fill in some details":**

1. Read the TODO section at the bottom of the relevant `sys-*.md` file
2. **Interview the user** — pick 3-5 related TODOs and ask about them using AskUserQuestion or conversationally. Group related questions (e.g., all filter-related items together, all fuel line items together).
3. After getting answers, update the system page immediately — fill in the TODO markers with real data
4. Then pick the next batch and continue

**Do not** dump the entire TODO list at the user. Work through it in focused batches, organized by topic. The user is a pilot/builder and knows this aircraft — they just need to be prompted for specific details.

**When the user provides photos**, save them to `images/` and reference them from the system page.

**When the user provides PDFs**, save them to the appropriate `docs/XX-*/` directory and add a link from the system page's References section.

## Editing Tips

- Use `<!-- placeholders -->` for missing data
- Tables use Pandoc pipe syntax
- Insert `\pagebreak` for PDF page breaks
- Images go in `images/` and reference as `![Alt](images/file.png)`
- Sections 4, 4b, 5 are **generated** - edit the JSON, not the markdown
