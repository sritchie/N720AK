# Plan: Fuel Pressure Regulator Diagnostic Workflow

## Background

N720AK's Aeromotive MAP-referenced fuel pressure regulator has been diagnosed with two problems:

1. **MAP under-tracking** (slope = −0.30 PSI/inHg) — consistent across all flights
2. **Mechanical sticking/hunting** (residual σ up to 1.25 PSI) — variable, worse on longer flights

A healthy reference (N88810, same regulator/system) shows σ = 0.08 PSI and slope = −0.01 after altitude correction.

## How to Run the Analysis

### Quick single-flight analysis

```bash
cd ~/code/rv10

# Dynon SkyView log (N720AK)
uv run --with numpy --with matplotlib python3 scripts/regulator_diagnostic.py /path/to/dynon_log.csv

# Garmin log (N88810 or similar) — needs altitude correction
uv run --with numpy --with matplotlib python3 scripts/regulator_diagnostic.py /path/to/garmin_log.csv --alt-correct

# Multiple flights at once
uv run --with numpy --with matplotlib python3 scripts/regulator_diagnostic.py flight1.csv flight2.csv
```

### Altitude correction scan

If you're unsure whether a sensor needs altitude correction:

```bash
uv run --with numpy --with matplotlib python3 scripts/regulator_diagnostic.py /path/to/log.csv --alt-scan
```

Look at the output: fraction ≈ 1.0 means the sensor is gauge (apply `--alt-correct`). Fraction ≈ 0.0 means no correction needed.

### What to look for

| Metric | Healthy | N720AK (current) | What it means |
|--------|---------|-------------------|---------------|
| **Delta σ** | < 0.2 PSI | 0.93–1.43 | Overall variation in injector differential |
| **MAP slope** | ~0 | −0.30 | Regulator doesn't track MAP 1:1 |
| **FF slope** | ~0 | −0.17 to −0.42 | Pressure droops under fuel flow load |
| **Residual σ** | < 0.1 | 0.18–1.25 | Sticking/hunting after removing MAP trend |
| **Startup FP** | ~35 PSI | 32–36 | Spring setpoint (should be consistent) |

## After Regulator Repair/Replacement

1. Fly a profile that includes:
   - Ground run (get startup fuel pressure)
   - Climb through at least 2,000 ft altitude change
   - Cruise at constant power for 10+ minutes
   - Descent with power changes
2. Download the Dynon log
3. Run the analysis script
4. Compare against the baseline table in `maintenance/fuel-system/README.md`
5. Target: σ < 0.2 PSI, MAP slope within ±0.02 PSI/inHg

## File Locations

- **Full documentation**: `maintenance/fuel-system/README.md`
- **Analysis script**: `scripts/regulator_diagnostic.py`
- **This plan**: `plans/regulator-diagnostic.md`
- **N88810 reference data**: `~/Downloads/log_20260209_091157_X05.csv`
- **N720AK flight logs**: `~/Downloads/*N720AK*.csv`
