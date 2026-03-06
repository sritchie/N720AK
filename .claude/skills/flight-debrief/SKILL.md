---
name: flight-debrief
description: Post-flight debrief for N720AK. Capture squawks, performance observations, engine notes, and upload flight data to analysis services.
argument-hint: [flight notes or "upload"]
user-invocable: true
---

# Flight Debrief

Capture post-flight observations and route data to the right places.

## Input

$ARGUMENTS

## Steps

### Capturing flight notes:

1. **Ask about the flight** (only what's relevant — don't interrogate):
   - Any squawks or discrepancies? (→ `squawks.tsv`)
   - Engine behavior — temps, pressures, anything unusual?
   - Fuel burn — total gallons, flight time?
   - Weather or performance notes worth recording?

2. **Log any squawks** per the squawk skill workflow

3. **Note any maintenance items** triggered by the flight:
   - Approaching an oil change interval?
   - Anything that needs attention before next flight?

### Uploading flight data:

N720AK records flight data on the Dynon SkyView HDX SD card. The data lives in CSV files.

**To extract data from Dynon:**
1. Remove the SD card from the SkyView HDX
2. Copy the CSV files to the computer
3. The main files are:
   - `C_ENGINE.CSV` — engine monitor data (CHT, EGT, oil temp/pressure, fuel flow, etc.)
   - `C_FLIGHT.CSV` — flight track data (GPS, altitude, airspeed)

**Upload to SavvyAnalysis** (engine health trending):
- Go to https://savvyanalysis.com
- Log in, click "Upload Files"
- Upload `C_ENGINE.CSV` (compress to ZIP if large)
- SavvyAnalysis auto-parses Dynon format
- Review the flight in their analysis tool for CHT/EGT trends

**Upload to FlySto** (full flight analysis + ADSB debrief):
- Go to https://www.flysto.net
- Log in, click upload / import
- Upload the Dynon data log CSV
- FlySto provides: flight track replay, engine data overlay, near-ADSB-traffic analysis, altimeter setting validation
- Note: FlySto may show duplicate flights if you re-upload the full circular log file. Upload only new data or delete duplicates in the FlySto UI.

**Neither service has a public API** — uploads must be done through the browser. Claude cannot automate these uploads, but can:
- Remind you to upload after each flight
- Help interpret SavvyAnalysis results once you share them
- Help analyze Dynon CSV files locally using scripts in `scripts/`

### Local analysis:

If the user provides a Dynon CSV file path, Claude can analyze it directly:
- Fuel pressure analysis: `uv run --with numpy --with matplotlib python3 scripts/regulator_diagnostic.py /path/to/log.csv`
- CHT/EGT spread analysis (can be built on request)
- Fuel burn calculations
