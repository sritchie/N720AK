---
name: flight-data-analysis
description: Analyze Dynon SkyView or Garmin GDU 460 flight data CSVs. Fuel pressure stability, MAP correlation, sensor diagnostics, pump performance comparison, engine trending.
argument-hint: [path to CSV file(s) and what to analyze]
user-invocable: true
---

# Flight Data Analysis

Analyze flight data from Dynon SkyView or Garmin GDU 460 CSV logs.

## Input

$ARGUMENTS

## Context

Read `CLAUDE.md` sections on:
- "Dynon Fuel Pressure: DIFF vs Gauge Modes"
- "Dynon MAP Sensor Details"
- "Flight Data CSV Formats"
- "Key Fuel System Findings"

These contain critical details about how N720AK's sensors work, the DIFF computation, known thresholds, and current pump/regulator configuration.

## Step 1: Identify the Data

1. Determine the file format:
   - **Dynon**: First row is column headers, `Session Time` is the first column, `Manifold Pressure (inHg)` present
   - **Garmin**: First row starts with `#airframe_info`, column headers on row 2, data starts row 4, uses `Manifold Press (inch Hg)`
   - **EFII**: TBD — Sam has these logs but format not yet characterized

2. Find flight segments by RPM transitions (RPM > 500 = engine on)

3. Report: number of flights, duration of each, date/time range, altitude range

## Step 2: Load and Parse

Use `uv run --with numpy --with matplotlib python3` for all analysis. Key helper:

```python
def safe_float(row, col):
    val = row.get(col, '') or ''
    try: return float(val.strip())
    except: return None

def p_atm_inhg(alt_ft):
    """Standard atmosphere pressure in inHg from pressure altitude."""
    return 29.92 * (1 - alt_ft / 145442.0) ** 5.25588
```

### Computing Injector Differential

The quantity we always care about is **injector differential = P_fuel_absolute - MAP_absolute** (in PSI). How to get it depends on the data source:

**Dynon DIFF mode** (current N720AK setup, post 2026-02):
- `Fuel Pressure (PSI)` column IS the injector differential — use directly
- No conversion needed

**Dynon gauge mode** (old N720AK data, pre 2026-02):
- `Fuel Pressure (PSI)` = gauge = P_fuel - P_atm
- `inj_diff = gauge_FP + (P_atm_inHg - MAP_inHg) * 0.49115`
- P_atm from pressure altitude via standard atmosphere

**Garmin** (always gauge):
- `Fuel Press (PSI)` = gauge = P_fuel - P_atm
- Same formula: `inj_diff = gauge_FP + (P_atm_inHg - MAP_inHg) * 0.49115`

**How to tell DIFF vs gauge mode**: On the ground before engine start, if FP = ~35 PSI and MAP = ambient (~24-25 inHg at KBDU), it's DIFF mode (because diff = absolute_FP - MAP ≈ 35). If FP = ~35 PSI and that equals what you'd expect for gauge (pumps on, no flow), it could be either — check once the engine starts. At ground idle (MAP ~11), DIFF mode reads ~35 PSI while gauge mode reads ~29 PSI.

## Step 3: Core Analysis — Fuel Pressure vs MAP

This is the PRIMARY diagnostic. Always produce this analysis:

1. **Scatter plot**: Injector differential vs MAP (inHg) for all samples with RPM > 1500
2. **Linear regression**: slope (PSI/inHg) and r²
3. **Binned averages**: Mean + std dev of injector diff for each integer MAP value
4. **Cruise stats**: Average, std dev, and range of injector diff for MAP 18-24 inHg

**Interpretation**:
- A perfect regulator/pump combo produces a flat horizontal line at 35 PSI
- Negative slope = pump can't maintain pressure as fuel demand increases with power
- slope > -0.05: excellent (Walbro 392 territory)
- slope -0.05 to -0.15: acceptable (Walbro 391 territory)
- slope < -0.20: pump struggling (Walbro 393 territory)

## Step 4: Time Series

Plot MAP and injector differential vs flight time on a dual-axis chart.

Look for:
- **Blank/missing data**: In Dynon data, empty strings mean the sensor went invalid (NOT zero). Mark these visually (orange bands). If MAP blanks, check if it's near 3.05 inHg (the min_val=1.5 PSI threshold on sensor 100434-000).
- **Transients**: Rapid FP drops during power changes — may explain pump cutover events
- **Steady-state sag**: Does FP settle at a lower value during extended cruise?

## Step 5: Additional Analysis (as requested)

- **CHT/EGT analysis**: Spread, trends, leaning state
- **Fuel burn**: Total fuel flow integration, GPH averages by phase
- **Pump switchover detection** (Garmin only): Check `Fl Pmp 1 Amps`, `Fl Pmp 2 Amps`, `FUEL PP 2 ON (discrete)`
- **Multi-flight comparison**: Overlay binned FP-vs-MAP curves from different flights/configurations
- **Before/after comparison**: Compare old vs new regulator, old vs new pumps, etc.

## Step 6: Generate Graphs

Always use `uv run --with matplotlib --with numpy python3` and save to `/tmp/` then copy to `~/Downloads/` and `open` them.

Standard graph set:
1. **Time series** (dual panel: MAP top, FP bottom, shared x-axis)
2. **Scatter** (injector diff vs MAP with trend line and r²)
3. **Binned comparison** (error bars, multiple datasets if comparing)

## Step 7: Report

Provide a concise summary with:
- Flight date, duration, altitude range
- Cruise injector differential: average, std dev
- MAP slope and r²
- Any anomalies (blanking events, transients, pump switchovers)
- Comparison to baseline if applicable

## Existing Script

There is also `scripts/regulator_diagnostic.py` which automates much of this. Run it with:

```bash
cd ~/code/rv10
uv run --with numpy --with matplotlib python3 scripts/regulator_diagnostic.py /path/to/log.csv
```

For Garmin data add `--alt-correct`. For multi-flight: pass multiple CSV paths. For altitude correction scan: `--alt-scan`.

The script auto-detects Dynon vs Garmin format.

## Reference Data

- **N88810 (Garmin, Walbro 392)**: `~/Downloads/log_20260308_*.csv` — the gold standard baseline
- **N720AK old regulator (Walbro 393)**: `~/Downloads/2011-01-01-N720AK-*.csv`
- **N720AK new regulator (Walbro 391)**: `~/Downloads/2026-03-16-N720AK-*.csv`
