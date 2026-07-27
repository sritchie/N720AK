---
name: maintenance-log
description: Log maintenance work on N720AK. Use when the user reports oil changes, inspections, repairs, modifications, or any other maintenance activity.
argument-hint: [description of work done]
user-invocable: true
---

# Maintenance Log Entry

The user is reporting maintenance work on N720AK. Process their input and add it to the appropriate digital maintenance log.

## Input

$ARGUMENTS

## Steps

1. **Determine the correct log file** based on what system was worked on:
   - Engine work (oil, filters, plugs, compression, accessories) → `engine-log.tsv`
   - Airframe work (structure, gear, controls, condition inspection) → `airframe-log.tsv`
   - Propeller/governor work → `propeller-log.tsv`
   - Avionics work (software, databases, wiring, antennas) → `avionics-log.tsv`

2. **Read the target log file** at:
   `~/Library/CloudStorage/GoogleDrive-sritchie09@gmail.com/My Drive/N720AK/Private/Maintenance/`

3. **Extract or ask for these fields** (ask only for what's missing — don't overwhelm):
   - **Date**: Default to today if not specified
   - **Tach/Hobbs**: Current readings — ask if not provided
   - **Total Time**: Airframe total time if known
   - **Work Type**: One of: Maintenance, Inspection, Repair, Modification, Overhaul
   - **Description**: Detailed narrative of what was done
   - **Parts Used**: Part numbers and quantities if applicable
   - **Reference**: AD, SB, or manual reference if applicable
   - **Performed By**: Who did the work (default: Sam Ritchie)
   - **Cost**: If mentioned
   - **Next Due**: Hours or date for next occurrence if this is a recurring item
   - **Notes**: Anything else relevant

4. **Append a new TSV row** to the log file using the Edit tool. Match the existing column order exactly.

5. **Check `recurring-items.tsv`** — if this work satisfies a recurring item, update the "Last Done Date" and "Last Done Tach" / "Last Done Hobbs" columns.

6. **Check `squawks.tsv`** — if this work resolves an open squawk, update its Status to "Cleared", fill in Corrective Action, Cleared By, and Date Cleared.

7. **Proactively suggest related items**:
   - Oil change → "Did you send a sample to Blackstone? Cut the filter?"
   - Spark plugs → "What were the gap measurements? Any fouling?"
   - Compression check → "What were the readings for each cylinder?"
   - Condition inspection → "Who signed it off? Any squawks found?"
   - Any engine work → "Did you do a run-up afterward? Any leaks?"

## Conventions

- **Performed By**: Always `Sam Ritchie (Repairman 5256450)` unless otherwise specified
- **No external references** in log entries — no URLs, no "see VAF post", no manual page citations. References belong in sys-* pages only.
- **No pending/future work** in logs — only completed work. Upcoming work is tracked in Linear.
- Log entries should be factual, past-tense descriptions of work performed.
- **Work Type** values: `Maintenance`, `Inspection`, `Repair`, `Modification`, `Overhaul`
- **Routine database cycles are not logged.** The 28-day Dynon/GTN nav and obstacle database updates get no avionics-log entries — the displays warn on expiry. Log avionics **software/firmware version changes** only.

## Important

- The user may dictate casually — extract structured data from conversational input
- Always confirm the entry before writing (show a summary)
- If multiple systems were worked on, create entries in multiple log files
- Paper logbooks are the legal record — remind the user to update paper logs for anything requiring a signature (condition inspection sign-off)
