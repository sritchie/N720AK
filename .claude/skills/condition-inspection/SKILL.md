---
name: condition-inspection
description: Guide the annual condition inspection for N720AK. Walks through Appendix D checklist areas, captures compression results, records squawks, and logs the sign-off.
argument-hint: [start | continue | sign-off]
user-invocable: true
---

# Condition Inspection Workflow

Guide the user through the annual condition inspection per 14 CFR Part 43, Appendix D.

## Input

$ARGUMENTS

## Context

N720AK is an Experimental Amateur-Built (E-AB) Van's RV-10. The condition inspection must:
- Follow the scope and detail of Appendix D to Part 43
- Be signed off by either the Repairman Certificate holder or a licensed A&P
- Be completed within 12 calendar months of the previous one
- Result in either an airworthy finding OR a list of discrepancies

## Steps

### Starting a new inspection:

1. **Check `recurring-items.tsv`** for when the last condition inspection was done
2. **Read `squawks.tsv`** for any open squawks that should be addressed during the inspection
3. **Walk through inspection areas** in batches, asking the user to report findings:

**Batch 1 — Fuselage & Cabin:**
- Fabric/skin condition, corrosion, dents
- Windows, windshield condition
- Seats, belts, harness condition
- Door mechanisms and seals
- Control stick and rudder pedal freedom

**Batch 2 — Engine Compartment:**
- Engine mount condition and bolt torque
- Hoses, lines, fittings — leaks?
- Exhaust system condition
- Baffles and seals
- Wiring condition
- Air filter condition

**Batch 3 — Engine Performance:**
- Compression check (differential, all cylinders)
  - Ask for each cylinder: #1, #2, #3, #4, #5, #6
  - Format: XX/80 (e.g., 76/80)
  - Flag any cylinder below 60/80 or more than 10 below the average
- Oil consumption trend
- Spark plug condition (if being serviced now)

**Batch 4 — Propeller & Governor:**
- Blade condition (nicks, erosion, cracks)
- Hub/bolt torque
- Governor operation and linkage
- Spinner condition

**Batch 5 — Landing Gear & Brakes:**
- Tire condition and pressure
- Brake pad wear
- Brake fluid level (Royco 782)
- Wheel bearings
- Gear leg fairings

**Batch 6 — Wing & Empennage:**
- Skin condition
- Control surface freedom and travel
- Hinges and hinge pins
- Trim tab condition and operation
- Wing tip lights (AeroSun VX)
- Pitot tube and AoA probe

**Batch 7 — Avionics & Electrical:**
- Antenna connections and condition
- VPX operation and settings
- Battery condition (EarthX ETX900 x2)
- Alternator output check
- ELT check (Artex ELT 345)
- Transponder and pitot-static due dates

4. **Log squawks** — for each discrepancy found, add to `squawks.tsv` with appropriate priority
5. **After all areas inspected**, summarize findings

### Sign-off:

1. **Ask who is signing off** — Repairman Certificate holder or A&P (name, certificate number)
2. **Create an airframe log entry** in `airframe-log.tsv`:
   - Work Type: Inspection
   - Description: "Annual condition inspection per 14 CFR Part 43, Appendix D. Aircraft [found/not found] in condition for safe operation. [X] discrepancies noted — see squawk list."
   - Performed By / Approved By with certificate info
3. **Update `recurring-items.tsv`** — set Condition Inspection last done date
4. **Check other recurring items** that are due:
   - Transponder check (91.413) — is it within 24 months?
   - Pitot-static test (91.411) — is it within 24 months?
   - ELT battery — is it due?
   - NOAA beacon registration — check expiration
5. **Remind about paper logbook** — the sign-off MUST go in the paper airframe log with a physical signature. The digital log supplements but does not replace the paper record.
