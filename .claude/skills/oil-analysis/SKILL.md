---
name: oil-analysis
description: Log oil analysis results from Blackstone Labs. Use when the user has received oil analysis results and wants to record and interpret them.
argument-hint: [lab results or "show trends"]
user-invocable: true
---

# Oil Analysis Entry

The user has oil analysis results to log, or wants to review trends.

## Input

$ARGUMENTS

## Steps

### If logging new results:

1. **Read `oil-analysis.tsv`** at:
   `~/Library/CloudStorage/GoogleDrive-sritchie09@gmail.com/My Drive/N720AK/Private/Maintenance/`

2. **Extract or ask for these fields**:
   - **Date**: When the sample was taken
   - **Tach / Hobbs**: Readings when oil was drained
   - **Hours on Oil**: Hours since last oil change
   - **Lab**: Default "Blackstone Labs"
   - **Wear metals** (ppm): Iron (Fe), Chromium (Cr), Nickel (Ni), Aluminum (Al), Copper (Cu), Lead (Pb), Tin (Sn), Silver (Ag), Silicon (Si), Boron (B)
   - **TBN**: Total Base Number (oil remaining useful life)
   - **Viscosity**: Measured viscosity
   - **Water**: Water content in ppm
   - **Lab Notes**: What Blackstone said
   - **Our Notes**: Any additional observations

3. **Append a row** to `oil-analysis.tsv`

4. **Interpret the results** — flag anything abnormal:

   **Universal action limits for Lycoming IO-540** (approximate, per Blackstone):

   | Metal | Normal (ppm) | Watch | Concern |
   |-------|-------------|-------|---------|
   | Iron (Fe) | < 30 | 30-50 | > 50 |
   | Chromium (Cr) | < 5 | 5-10 | > 10 |
   | Nickel (Ni) | < 2 | 2-5 | > 5 |
   | Aluminum (Al) | < 10 | 10-20 | > 20 |
   | Copper (Cu) | < 15 | 15-30 | > 30 |
   | Lead (Pb) | < 30 | 30-50 | > 50 |
   | Tin (Sn) | < 5 | 5-10 | > 10 |
   | Silver (Ag) | < 1 | 1-2 | > 2 |
   | Silicon (Si) | < 20 | 20-30 | > 30 |

   - Iron: Primarily from cylinder walls, cam, gears
   - Chromium: Piston rings (chrome-plated)
   - Aluminum: Pistons, case halves
   - Copper: Bearings, bushings, oil cooler
   - Lead: Bearing overlay, fuel contamination
   - Silicon: Dirt ingestion (air filter), sealant
   - Silver: Silver-plated bearings (if equipped)

5. **Compare to previous samples** — trend analysis is more important than absolute numbers. Flag:
   - Any metal that doubled from the previous sample
   - Any metal consistently climbing over 3+ samples
   - Sudden appearance of a metal not previously present
   - TBN dropping unusually fast (suggests oil degradation)

6. **Also update `engine-log.tsv`** with a maintenance entry noting the oil analysis was logged.

### If reviewing trends:

1. Read `oil-analysis.tsv` and present a summary table
2. Highlight any concerning trends
3. Note hours between oil changes and whether the interval is consistent
