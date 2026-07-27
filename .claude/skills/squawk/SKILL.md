---
name: squawk
description: Log an aircraft discrepancy (squawk) for N720AK. Use when the user reports something wrong, broken, or needing attention on the aircraft.
argument-hint: [description of the problem]
user-invocable: true
---

# Squawk Entry

The user is reporting an aircraft discrepancy. Log it in the squawk tracker.

## Input

$ARGUMENTS

## Steps

1. **Read `squawks.tsv`** at:
   `~/Library/CloudStorage/GoogleDrive-sritchie09@gmail.com/My Drive/N720AK/Private/Maintenance/squawks.tsv`

2. **Check for related existing squawks** — is this a duplicate or related to an open item?

3. **Extract or ask for these fields**:
   - **Date Reported**: Default to today
   - **Reported By**: Default to Sam Ritchie
   - **Tach/Hobbs**: Current readings if known
   - **Priority**: Suggest based on severity:
     - `Grounding` — aircraft not airworthy until fixed
     - `Before Next Flight` — must resolve before flying
     - `Soon` — fix within next few flights
     - `Routine` — next maintenance opportunity
     - `Monitor` — watch and reassess
   - **Category**: Engine, Airframe, Propeller, Avionics, Electrical, Fuel
   - **Discrepancy**: Clear description of what's wrong
   - **Status**: Default to "Open"

4. **Append a new TSV row** to squawks.tsv

5. **Suggest next steps** based on the category and severity:
   - Grounding items: "This grounds the aircraft. What's your plan to address it?"
   - Engine items: Check if related to known issues in sys-28-fuel-system.md or sys-71-engine.md
   - Electrical items: Check sys-24-electrical.md for relevant system info
   - Suggest relevant sys-*.md pages that might have troubleshooting info

6. **If the user is CLEARING a squawk** (reporting a fix), update the existing row:
   - Set Status to "Cleared"
   - Fill in Corrective Action, Cleared By, Date Cleared
   - Also create a maintenance log entry via the maintenance-log workflow

## Conventions

- Squawks are for **long-lived discrepancies only** — not items about to be addressed, and never pending/future work (that's tracked in Linear).
- No external references in squawk entries — references belong in sys-* pages.
