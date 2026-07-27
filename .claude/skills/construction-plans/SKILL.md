---
name: construction-plans
description: Search the Van's RV-10 construction plans for parts, hardware, and build details. Use for construction drawings, Van's part numbers, or how-is-it-built questions about N720AK.
---

# Construction Plans Search

Van's RV-10 construction plans (121 PDFs) are indexed for search in `docs/`.

**Index file**: `docs/construction-plans-index.md` — section directory, topic cross-reference
**Extracted text**: `docs/plans-text/*.txt` — one file per PDF, visually transcribed from drawings
**Source PDFs**: `~/Library/CloudStorage/GoogleDrive-sritchie09@gmail.com/My Drive/N720AK/Archive/Construction-Drawings/`

## Search workflow

0. For part number lookups, search `docs/plans-text/manual-section-4-parts-index.txt` first — it has every Van's part number with nomenclature, material, and sub-kit
1. For operational specs (V-speeds, control surface limits, flap range), search `sections/` POH files first — these are NOT in construction plans
2. Grep `docs/construction-plans-index.md` for topic keywords — the Topic Cross-Reference maps topics to section numbers, and ⚠️ marks N720AK build deviations
3. Grep `docs/plans-text/` for part numbers (AN, MS, F-xxxx) or detailed terms
4. Read the specific PDF page visually if a drawing/figure is needed (use `Read` with `pages` parameter)
5. **Search VansAirForce.net** — the VAF forums are an invaluable resource for RV-10 construction questions. Many build questions (especially ambiguous plan details, "what are these holes for", fitment issues, and builder tips) have been discussed and answered there. Always consider searching VAF when the plans alone don't give a clear answer.

## Important notes

- `pdftotext` does NOT extract text from these PDFs — the `.txt` files were created by visually transcribing each page. All 54 core sections have `=== PAGE N ===` markers.
- Construction plans show **assembly**, not disassembly. For removal questions, the answer is typically "reverse of installation."
- **N720AK deviates from stock plans** in 25+ areas (see Build Deviations table in the index). Always check deviations before answering — the plans show what Van's designed, not necessarily what's installed.
- AN fastener numbers in the plans cross-reference to modern MS/NAS numbers used by retailers — see `sections/sys-00-workshop.md` "AN/MS/NAS Fastener Cross-Reference" section for the full mapping (AN509→MS24694, AN426→MS20426, AN365→MS21044, etc.).
