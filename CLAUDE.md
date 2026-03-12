# N720AK RV-10 Pilot's Operating Handbook

This repository contains the Pilot's Operating Handbook (POH) for **N720AK**, a Van's RV-10 experimental aircraft. The POH follows [GAMA Specification No. 1](https://gama.aero/documents/gama-specification-1-specification-for-pilots-operating-handbook-version-2-0/) format.

## Repository Purpose

1. **POH Source Files**: Markdown files in `sections/` that compile to PDF and HTML
2. **Checklist Sync**: `N720AK.json` synced from the EFIS Editor for Dynon/ForeFlight export
3. **Weight & Balance**: Exportable W&B data for sharing with other pilots
4. **GitHub Pages**: Auto-deploys HTML version on push to main (target: n720ak.com)

## Linear (Task Manager)

Linear is used **only as a task manager** for pending work items. It is NOT a content store. Key rules:

- **Never store attachments or content in Linear** — all documents, PDFs, invoices, photos, and reference material go in Google Drive or the git repo
- **Never link to Linear issue URLs** from sys-*.md pages, GDrive files, or anywhere in the repo — Linear is not accessible to other users
- **Never reference Linear issue identifiers** (e.g., "Source: Linear RV-XXX") in archived content — once content is migrated out, all Linear provenance must be removed
- **Linear upload URLs expire** — JWT-signed `uploads.linear.app` URLs are valid for ~5 minutes. Never store these as permanent references.
- When closing an issue, the content should already be in its permanent home (GDrive or repo) before marking Done

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
├── docs/                  # Small custom diagrams only (no manufacturer PDFs)
│   ├── README.md          # Documents Google Drive approach
│   └── gdrive-links.md   # URL registry: files → Google Drive shareable links
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

Each system page links to manufacturer PDFs on Google Drive via shareable URLs (see `docs/gdrive-links.md` for the URL registry).

### Reference Documents — Google Drive

Manufacturer PDFs, manuals, schematics, and configs live on **Google Drive** (not in git). The `Public/` folder is shared read-only; sys-*.md pages link to these via stable Google Drive URLs. Claude reads files locally from the synced folder.

**Local sync path**: `~/Library/CloudStorage/GoogleDrive-sritchie09@gmail.com/My Drive/N720AK/`

| GDrive Folder | Sharing | Content |
|---------------|---------|---------|
| `Public/Manuals/{ATA}/` | Anyone with link | Manufacturer manuals by ATA chapter |
| `Public/Schematics/` | Anyone with link | Wiring diagrams, system schematics |
| `Public/Configs/` | Anyone with link | Dynon sensor/user configs, OnSpeed calibrations |
| `Public/Performance/` | Anyone with link | ADSB reports, airspeed data, prop balance |
| `Public/Weight-Balance/` | Anyone with link | W&B worksheets |
| `Private/` | Owner only | Invoices, insurance, keys, registration |
| `Private/Maintenance/` | Owner only | Digital maintenance logs (TSV), oil analysis |
| `Archive/` | Owner only | Van's construction drawings, brochures, reference POHs |

The `docs/` directory in git contains only `README.md`, `gdrive-links.md` (URL registry), and any small custom diagrams created for sys-*.md pages. No manufacturer PDFs in git.

**Getting Google Drive URLs for new files**: On macOS with Google Drive for Desktop, the file ID is stored in extended attributes. To get a shareable URL:
```bash
xattr -p com.google.drivefs.item-id#S "/path/to/file"
# Returns: 1abc123...
# URL: https://drive.google.com/file/d/1abc123.../view
```
After adding a file to `Public/`, extract the file ID with `xattr`, add it to `docs/gdrive-links.md`, and link from the relevant sys-*.md page.

### Analysis Scripts

Always use `uv` to run Python scripts (handles dependencies automatically).

```
scripts/
├── regulator_diagnostic.py        # Fuel pressure regulator diagnostic
│                                  # Auto-detects Dynon/Garmin CSV format
│                                  # Computes: delta σ, MAP slope, FF slope, residual σ
│                                  # Generates 4-panel diagnostic plot
│                                  # Supports altitude correction (--alt-correct)
│                                  # and correction fraction scan (--alt-scan)
└── migrate_dropbox_to_gdrive.py   # One-time migration: Dropbox → Google Drive
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

## Git Workflow

**Never commit directly to main.** Always create a branch, open a PR, and squash merge.

**Branch awareness**: At the start of each session, check `git branch --show-current` and `git log --oneline main..HEAD`. If you're on a feature branch with commits ahead of main, that branch was likely already merged — verify with `gh pr list --state merged --head <branch>`. If merged, switch to main and pull before starting new work. If not merged, you can stack additional commits on the existing branch.

After making edits to POH sections, sys-* pages, or any repo files, always:
1. Create a descriptive branch name
2. Commit with an imperative-mood message
3. Push and open a PR with a summary
4. Squash merge the PR

When merging PRs, **always use squash merge** via `gh pr merge`:

```bash
gh pr merge <number> --squash \
  --subject "<PR title>" \
  --body "<PR description body>"
```

The squash commit title should be the PR title, and the body should be the PR description. This keeps `main` history clean with one commit per PR.

**Do not leave unstaged changes.** Every editing session should end with a clean working tree.

## Systems Reference TODOs

The Systems Reference pages (`sections/sys-*.md`) contain `<!-- TODO -->` markers and structured TODO checklists at the bottom of each file. These represent information that needs to come from the owner (part numbers, photos, procedures, measurements, supplier info, etc.).

**When the user asks about TODOs, or asks to work on a system page, or says something like "let's fill in some details":**

1. Read the TODO section at the bottom of the relevant `sys-*.md` file
2. **Interview the user** — pick 3-5 related TODOs and ask about them using AskUserQuestion or conversationally. Group related questions (e.g., all filter-related items together, all fuel line items together).
3. After getting answers, update the system page immediately — fill in the TODO markers with real data
4. Then pick the next batch and continue

**Do not** dump the entire TODO list at the user. Work through it in focused batches, organized by topic. The user is a pilot/builder and knows this aircraft — they just need to be prompted for specific details.

**When the user provides photos**, save them to `images/` and reference them from the system page.

**When the user provides PDFs**, save them to the appropriate Google Drive `Public/Manuals/{ATA}/` folder, get the shareable URL, add it to `docs/gdrive-links.md`, and link from the system page's References section.

## Maintenance Logs (Digital)

N720AK maintains digital maintenance logs as TSV files in Google Drive, synced locally. These supplement (not replace) the paper logbooks — paper is still needed for condition inspection sign-offs and regulatory signatures.

**Local path**: `~/Library/CloudStorage/GoogleDrive-sritchie09@gmail.com/My Drive/N720AK/Private/Maintenance/`

### Log Files

| File | Purpose |
|------|---------|
| `engine-log.tsv` | Engine work: oil changes, filters, plugs, compression, accessories |
| `airframe-log.tsv` | Airframe: condition inspections, structural, gear, controls |
| `propeller-log.tsv` | Prop and governor: torque, balancing, seal/grease |
| `avionics-log.tsv` | Avionics: software/database updates, wiring, antenna work |
| `squawks.tsv` | Discrepancy tracking: open items through resolution |
| `recurring-items.tsv` | Recurring task schedule with intervals and last-done dates |
| `ad-sb-compliance.tsv` | AD, SB, Service Bulletin compliance tracking |
| `oil-analysis.tsv` | Blackstone Labs oil analysis results (wear metal trends) |

### How to Add Maintenance Log Entries

When the user reports maintenance work (verbally, by dictation, or in chat), Claude should:

1. **Determine the correct log** — engine, airframe, propeller, or avionics
2. **Read the current log file** to see existing entries and the TSV structure
3. **Ask for missing fields** if the user didn't provide them. Key fields to prompt for:
   - Date (default: today)
   - Tach and/or Hobbs reading
   - What was done (description)
   - Parts used (part numbers if known)
   - Who did the work
4. **Append a new row** to the appropriate TSV file using the Edit tool
5. **Update `recurring-items.tsv`** if the work satisfies a recurring item (update Last Done Date and Last Done Tach/Hobbs)
6. **Proactively suggest** related items that might be due soon (e.g., "Since you changed the oil, did you also send a sample to Blackstone?")

### Maintenance Log Conventions

- **Performed By**: Always `Sam Ritchie (Repairman 5256450)` unless otherwise specified
- **No external references** in log entries — no URLs, no "see VAF post", no manual page citations. References belong in sys-* pages only.
- **No pending/future work** in logs or squawks — Sam tracks upcoming work in Linear. Only document completed work.
- **Squawks** are for long-lived discrepancies only, not for items about to be addressed.
- Log entries should be factual, past-tense descriptions of work performed.

### How to Add Squawks

When the user reports a problem or discrepancy:

1. **Read `squawks.tsv`** to check for existing related squawks
2. **Add a new row** with: date, reporter, tach/hobbs, priority, category (Engine/Airframe/Prop/Avionics), description, status=Open
3. **Suggest a priority level** based on the description:
   - `Grounding` — aircraft not airworthy
   - `Before Next Flight` — must fix before flying
   - `Soon` — fix within next few flights
   - `Routine` — next maintenance opportunity
   - `Monitor` — watch and reassess

### What to Prompt the User About

When the user mentions maintenance work, proactively ask about related items:

**Oil change?** Ask about:
- Oil analysis sample sent? (→ oil-analysis.tsv when results come back)
- Filter cut and inspected? Any metal?
- Sump screen checked?
- Oil quantity and brand used?

**Condition inspection?** Ask about:
- Who signed it off? (Repairman cert or A&P name/cert number)
- Compression results for each cylinder?
- Any squawks found? (→ squawks.tsv)
- Transponder/pitot-static due? (check recurring-items.tsv)

**Engine work?** Ask about:
- Was the engine run up afterward?
- Any leaks observed?
- Torque values if applicable?

**Avionics update?** Ask about:
- Which software version? (from → to)
- Any settings that changed?
- Did the update require a config reload?

### Work Type Values

Use consistent values: `Maintenance`, `Inspection`, `Repair`, `Modification`, `Overhaul`

### Category Values (for squawks)

Use: `Engine`, `Airframe`, `Propeller`, `Avionics`, `Electrical`, `Fuel`

### Recurring Items Reference

Key intervals for N720AK:

| Item | Interval | Notes |
|------|----------|-------|
| Oil & filter change | 50 hrs / 4 months | Lycoming recommendation |
| Oil analysis | Every oil change | Blackstone Labs |
| Spark plug service | 100 hrs | Clean, gap, inspect, rotate |
| Compression check | Condition inspection | Differential method, all cylinders |
| Condition inspection | 12 calendar months | Signed by Repairman Cert holder or A&P |
| Transponder check (91.413) | 24 calendar months | Required |
| Pitot-static test (91.411) | 24 calendar months | Required for IFR |
| ELT battery | Per manufacturer | Artex ELT 345 |
| NOAA beacon registration | 24 months | Beacon ID: 2DC885940EFFBFF |
| Nav database updates | 28-day cycle | Dynon + GTN 650 |

### AD/SB Compliance

Track compliance with:
- **FAA Airworthiness Directives** — mandatory for certified components (Lycoming engine, propeller, GTN 650, Artex ELT)
- **Van's Service Bulletins** — advisory for E-AB, but strongly recommended. Check: vansaircraft.com/service-information-and-revisions/
- **Lycoming Service Bulletins/Instructions** — advisory for experimentals, best practice to follow
- **EFII Service Bulletins** — for System32 EFI/ignition

When adding AD/SB entries, record: document type, number, source, subject, applicability, compliance status, date, method, and next due if recurring.

## Construction Plans Index

Van's RV-10 construction plans (121 PDFs) are indexed for search in `docs/`.

**Index file**: `docs/construction-plans-index.md` — section directory, topic cross-reference
**Extracted text**: `docs/plans-text/*.txt` — one file per PDF, visually transcribed from drawings
**Source PDFs**: `~/Library/CloudStorage/GoogleDrive-sritchie09@gmail.com/My Drive/N720AK/Archive/Construction-Drawings/`

**Search workflow** when user asks about construction plans, parts, or hardware:
0. For part number lookups, search `docs/plans-text/manual-section-4-parts-index.txt` first — it has every Van's part number with nomenclature, material, and sub-kit
1. For operational specs (V-speeds, control surface limits, flap range), search `sections/` POH files first — these are NOT in construction plans
2. Grep `docs/construction-plans-index.md` for topic keywords — the Topic Cross-Reference maps topics to section numbers, and ⚠️ marks N720AK build deviations
3. Grep `docs/plans-text/` for part numbers (AN, MS, F-xxxx) or detailed terms
4. Read the specific PDF page visually if a drawing/figure is needed (use `Read` with `pages` parameter)
5. **Search VansAirForce.net** — the VAF forums are an invaluable resource for RV-10 construction questions. Many build questions (especially ambiguous plan details, "what are these holes for", fitment issues, and builder tips) have been discussed and answered there. Always consider searching VAF when the plans alone don't give a clear answer.

**Important notes**:
- `pdftotext` does NOT extract text from these PDFs — the `.txt` files were created by visually transcribing each page. All 54 core sections have `=== PAGE N ===` markers.
- Construction plans show **assembly**, not disassembly. For removal questions, the answer is typically "reverse of installation."
- **N720AK deviates from stock plans** in 25+ areas (see Build Deviations table in the index). Always check deviations before answering — the plans show what Van's designed, not necessarily what's installed.
- AN fastener numbers in the plans cross-reference to modern MS/NAS numbers used by retailers — see `sections/sys-00-workshop.md` "AN/MS/NAS Fastener Cross-Reference" section for the full mapping (AN509→MS24694, AN426→MS20426, AN365→MS21044, etc.).

## Editing Tips

- Use `<!-- placeholders -->` for missing data
- Tables use Pandoc pipe syntax
- Insert `\pagebreak` for PDF page breaks
- Images go in `images/` and reference as `![Alt](images/file.png)`
- Sections 4, 4b, 5 are **generated** - edit the JSON, not the markdown
