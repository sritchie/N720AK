---
name: sys-reference
description: Look up or update a Systems Reference page (sys-*.md). Use when the user asks about a specific aircraft system, wants to add details, or says "let's work on" a system page.
argument-hint: [system name or ATA chapter number]
user-invocable: true
---

# Systems Reference Lookup/Update

The user wants to look up or update information about an aircraft system.

## Input

$ARGUMENTS

## System Page Mapping

| ATA | File | System |
|-----|------|--------|
| 00 | sys-00-workshop.md | Workshop tools, supplies, equipment |
| 22 | sys-22-autopilot.md | Dynon 3-axis autopilot |
| 23 | sys-23-communications.md | GMA 245, audio, intercom |
| 24 | sys-24-electrical.md | Buses, VPX, batteries |
| 27 | sys-27-flight-controls.md | Stick grip, trim, flaps |
| 28 | sys-28-fuel-system.md | Complete fuel system |
| 33 | sys-33-lighting.md | AeroLEDs, wingtip lights |
| 34 | sys-34-navigation.md | Dynon, GTN 650, pitot-static |
| 34 | sys-34-onspeed.md | OnSpeed AoA system |
| 35 | sys-35-oxygen.md | Mountain High O2 |
| 42 | sys-42-avionics.md | Wiring, panel, interconnects |
| 61 | sys-61-brakes.md | Brakes, wheels, tires |
| 71 | sys-71-engine.md | Lycoming IO-540 mechanical |
| 73 | sys-73-efii.md | EFII System32 EFI/ignition |
| 84 | sys-84-propeller.md | Prop and governor |

## Steps

### If looking up information:
1. Read the relevant sys-*.md file
2. Provide the requested information
3. If the info isn't there yet (marked with `<!-- TODO -->`), tell the user it's a known gap and offer to fill it in

### If updating/adding information:
1. Read the sys-*.md file to understand existing structure
2. Read the TODO section at the bottom of the file
3. **Interview the user** in batches of 3-5 related TODOs — don't dump the whole list
4. Update the page with real data as answers come in
5. When the user provides:
   - **Photos**: Save to `images/` and reference from the page
   - **PDFs**: Save to GDrive `Public/Manuals/{ATA}/`, get shareable URL, add to `docs/gdrive-links.md`, link from References section
   - **Part numbers, specs, procedures**: Add directly to the page

### Style guidelines:
- Technical but readable
- Tables for specs and part numbers
- Subsections with clear headings
- Link to GDrive for manufacturer docs (never embed large PDFs)
- Use `<!-- TODO: description -->` for items still missing
