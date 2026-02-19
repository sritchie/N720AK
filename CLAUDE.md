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
│   └── 09-servicing.md    # Handling, servicing, maintenance
├── images/                # Aircraft photos, diagrams
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

## What Goes in POH vs Maintenance Documentation

### POH (This Repository)

Information a **pilot** needs for **normal operation**:

**Section 8 - Systems Description:**
- How each system works (operational description)
- Normal operating procedures
- Panel switch locations and functions
- Stick grip button layout (with photo)
- What the emergency bus does and when it activates

**Section 9 - Handling, Servicing:**
- Brake fluid type (Royco 782)
- Tire pressures
- Oil type and capacity
- Fuel specifications
- Preflight inspection items
- Service intervals

### Separate Maintenance Manual (Not in POH)

Information for **maintenance and repair**:

- **Wingtip removal procedure** (piano hinge details)
- **AeroSun VX light installation** (wiring, mounting)
- **Bob Archer antenna installation** (location, coax routing)
- Wiring diagrams and harness documentation
- Part numbers and suppliers
- Torque specifications
- Detailed inspection procedures

**Recommendation**: Create a `maintenance/` directory or separate repo for:
- Component installation guides
- Wiring diagrams
- Part numbers and sources

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

## Editing Tips

- Use `<!-- placeholders -->` for missing data
- Tables use Pandoc pipe syntax
- Insert `\pagebreak` for PDF page breaks
- Images go in `images/` and reference as `![Alt](images/file.png)`
- Sections 4, 4b, 5 are **generated** - edit the JSON, not the markdown
