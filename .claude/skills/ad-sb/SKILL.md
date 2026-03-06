---
name: ad-sb
description: Track Airworthiness Directive and Service Bulletin compliance for N720AK. Use when logging compliance, checking what's due, or reviewing new ADs/SBs.
argument-hint: [AD/SB number or "check due" or "review new"]
user-invocable: true
---

# AD/SB Compliance Tracking

Track compliance with Airworthiness Directives, Service Bulletins, and Service Instructions.

## Input

$ARGUMENTS

## Steps

### Logging compliance:

1. **Read `ad-sb-compliance.tsv`** at:
   `~/Library/CloudStorage/GoogleDrive-sritchie09@gmail.com/My Drive/N720AK/Private/Maintenance/`

2. **Extract or ask for**:
   - **Doc Type**: AD, SB, SI, Safety Alert
   - **Number**: e.g., AD 2015-10-09, Van's SB-00007
   - **Source**: FAA, Van's Aircraft, Lycoming, Hartzell, EFII, Garmin, Dynon, Artex
   - **Subject**: Brief description
   - **Applies to N720AK?**: Yes / No / Partial
   - **Status**: Complied / Not Yet / N/A / Deferred
   - **Compliance Date**: When complied
   - **Compliance Method**: What was done (one-time or recurring)
   - **Next Due**: For recurring items — hours or calendar date
   - **Logbook Reference**: Which log file and approximate date of the maintenance entry
   - **Notes**: Rationale for deferral, partial applicability details, etc.

3. **Append a row** to `ad-sb-compliance.tsv`

4. **Also create a maintenance log entry** in the appropriate log file if actual work was performed

### Checking what's due:

1. Read `ad-sb-compliance.tsv`
2. Filter for recurring items with a Next Due date/hours
3. Compare against current tach/hobbs (ask if not known)
4. Report what's due, coming due, or overdue

### Reviewing new ADs/SBs:

Help the user evaluate applicability. Key sources for N720AK:

- **FAA ADs**: Check for Lycoming IO-540, any installed certified components (GTN 650, Artex ELT 345)
- **Van's SBs**: vansaircraft.com/service-information-and-revisions/ (filter by RV-10). Advisory for E-AB but strongly recommended.
- **Lycoming SBs/SIs**: Advisory for experimentals, best practice to follow
- **EFII bulletins**: For System32 EFI/ignition system
- **Propeller manufacturer**: Check for applicable SBs

For each new AD/SB, determine:
1. Does it apply to N720AK's specific configuration?
2. Is it one-time or recurring?
3. What's the compliance deadline (if AD)?
4. What work is required?
5. Add to tracking spreadsheet with appropriate status
