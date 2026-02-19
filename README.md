# N720AK RV-10 Pilot's Operating Handbook

Pilot's Operating Handbook for **N720AK**, a Van's RV-10 experimental aircraft. Follows [GAMA Specification No. 1](https://gama.aero/documents/gama-specification-1-specification-for-pilots-operating-handbook-version-2-0/) format.

Outputs:
- **PDF** (`output/poh.pdf`) — single combined document via Pandoc + Typst
- **HTML** (`output/html/`) — browsable site via mdBook, deployed to [n720ak.com](https://n720ak.com)

## Prerequisites

```bash
# macOS
brew install pandoc typst mdbook
```

## Build

```bash
./build.sh pdf     # Build PDF
./build.sh html    # Build HTML site
./build.sh serve   # Start mdBook dev server with live reload
./build.sh all     # Build both PDF and HTML
```

## Checklist Synchronization

Canonical checklist source: https://rdamazio.github.io/efis-editor/checklists#N720AK

1. Edit checklists at the EFIS Editor URL
2. Export JSON and save as `N720AK.json`
3. Run `python3 json_to_markdown.py N720AK.json` to generate `04-emergency.md`, `04b-abnormal.md`, `05-normal.md`
4. Export from EFIS Editor to Dynon (.txt) and ForeFlight (.fmd) as needed

Sections 4, 4b, and 5 are **generated** — edit the JSON, not the markdown directly.

## Directory Structure

```
rv10/
├── metadata.yaml          # PDF title, author, revision
├── template.typ           # Typst template for PDF styling
├── book.toml              # mdBook configuration
├── build.sh               # Build script (pdf/html/serve/all)
├── json_to_markdown.py    # Converts checklist JSON to markdown
├── N720AK.json            # Canonical checklist (from EFIS Editor)
├── sections/
│   ├── SUMMARY.md         # mdBook table of contents
│   ├── 00-introduction.md
│   ├── 01-general.md
│   ├── 02-limitations.md
│   ├── 03-engine-info.md
│   ├── 04-emergency.md    # Generated from JSON
│   ├── 04b-abnormal.md   # Generated from JSON
│   ├── 05-normal.md       # Generated from JSON
│   ├── 06-performance.md
│   ├── 07-weight-balance.md
│   ├── 08-systems.md
│   └── 09-servicing.md
├── images/
└── output/
    ├── poh.pdf            # Generated PDF
    └── html/              # Generated HTML site
```

## Customization

### Aircraft Details
Edit `metadata.yaml`:
```yaml
title: "Pilot's Operating Handbook"
aircraft-type: "RV-10"
n-number: "N720AK"
revision: "1.0"
builder: "Sam Ritchie"
serial: "41649"
```

### Styling
Edit `template.typ` to customize page headers/footers, fonts, table styling, and section formatting.

### Adding Images
Place images in `images/` and reference as `![Alt](images/file.png)`.

### Page Breaks
Insert `\pagebreak` where needed in section markdown files.
