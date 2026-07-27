# N720AK Flight Data Reference

Sensor, fuel system, and CSV format details for analyzing N720AK flight data. Migrated from CLAUDE.md 2026-07-27.

## Key Fuel System Findings (as of 2026-04)

- **Setpoint is now 45 PSI** (DIFF mode on Dynon EMS) following the **Borla 203133 regulator** swap on 2026-03-17. The Borla replaced the Aeromotive Compact EFI regulator.
- The Borla holds much better than the Aeromotive on the same Walbro 391 pumps:
  - Aeromotive @ 45 PSI ground run: MAP slope = **−0.295 PSI/inHg** (2.8 PSI idle-to-cruise droop)
  - Borla @ 45 PSI ground run: MAP slope = **−0.089 PSI/inHg** (0.9 PSI droop) — **3× improvement**
  - Reference N88810 Borla + Walbro 392: **−0.014 PSI/inHg** (essentially flat)
- **Sticking with Walbro 391 pumps.** The 392 upgrade is no longer planned — the Borla solved enough of the regulation problem that the pump upgrade isn't worth pursuing now.
- **In-flight health criterion:** fuel pressure should not budge meaningfully from 45 PSI in any flight regime. >1 PSI variation under load warrants investigation.
- Auto-cutover trip point (Bus Manager Pump 1 → Pump 2): **22 PSI Borla output absolute** (the pump-side sense). Because the Dynon displays the injector differential (Borla output − MAP), the on-screen DIFF value at the moment of trip varies with MAP — e.g. at 10 inHg MAP the Dynon would read ~12 PSI DIFF.
- Full details: `sections/sys-28-fuel-system.md`

## Dynon Fuel Pressure: DIFF vs Gauge Modes

N720AK runs the Dynon fuel pressure in **differential (DIFF) mode** as of 2026-02:
- **DIFF mode** (current): Dynon computes `P_fuel_absolute - MAP` = injector differential
  - The raw sensor reads gauge (P_fuel - P_atm)
  - Dynon adds atmospheric back to get absolute, then subtracts MAP
  - This is the quantity that matters for fuel injection — pressure across the injectors
  - **Depends on a valid MAP reading** — if MAP blanks, FP blanks too
- **Gauge mode** (old, pre-2026-02): Dynon logs the raw sensor reading = P_fuel - P_atm
  - To compute injector differential from gauge data: `inj_diff = gauge_FP + (P_atm - MAP) * 0.49115`
  - Where P_atm is from standard atmosphere: `P_atm_inHg = 29.92 * (1 - alt_ft / 145442)^5.25588`
  - On the ground with engine off, gauge FP = diff FP (because MAP = P_atm, so the delta is zero)

**The core diagnostic quantity is always injector differential vs MAP.** A perfect regulator holds flat. Sag = pump can't keep up.

## Dynon MAP Sensor Details

- **Active sensor**: `100434-000 (-0.5)` on pin `C37_P26`
- **Transfer function**: `PSI = 5.7030 * V + 1.1406` (linear)
- **min_val = 1.5 PSI (= 3.05 inHg)** — values below this are blanked
  - Dead short (0V) reads 1.141 PSI = 2.32 inHg
  - Previously 2 PSI (4.07 inHg); lowered 2026-03-17 to prevent blanking at high altitude idle with CS prop
  - Change approved by Don Jones, Dynon Customer Support (Zendesk #186497, 2026-03-16)
- **Config files**: `GDrive: N720AK/Public/Configs/Dynon/`
  - `.sfg` (SENSOR_CONFIG) = sensor definitions, transfer functions, min/max
  - `.dfg` (USER_CONFIG) = display ranges, color bands, alarm settings
  - Active MAP display: `c37_p26` in the `.dfg`, `min_display=0`, `max_display=19.6439` PSI (= 0-40 inHg)

## Flight Data CSV Formats

**Dynon SkyView** (`*USER_LOG_DATA.csv`):
- 4 Hz sample rate, comma-separated, single header row
- Key columns: `Session Time`, `GPS Date & Time`, `Manifold Pressure (inHg)`, `Fuel Pressure (PSI)`, `FUEL PRESSURE (PSI)`, `RPM L`, `Pressure Altitude (ft)`, `Total Fuel Flow (gal/hr)`, `Barometer Setting (inHg)`, CHTs, EGTs
- `Fuel Pressure (PSI)` and `FUEL PRESSURE (PSI)` are identical in current config
- In DIFF mode, both columns contain the computed differential (P_fuel_abs - MAP)
- In gauge mode (old data), both contain raw gauge pressure
- Blank cells (empty string) = sensor reported invalid/out-of-range — NOT zero
- May contain multiple flights; segment by RPM > 0 transitions
- GPS timestamps are UTC; `Session Time` is seconds from power-on

**Garmin GDU 460** (`log_YYYYMMDD_HHMMSS_XXX.csv`):
- 1 Hz sample rate, comma-separated, 3 header rows (info, long names, short names)
- Data starts at row 4
- Key columns: `Manifold Press (inch Hg)`, `Fuel Press (PSI)`, `RPM`, `Pressure Altitude (ft)`, `Fuel Flow (gal/hour)`, `Baro Setting (inch Hg)`
- Fuel pressure is always **gauge** (relative to atmosphere) — must compute injector diff
- Has `Fl Pmp 1 Amps` / `Fl Pmp 2 Amps` columns for pump current monitoring
- Has `FUEL PP 2 ON (discrete)` for pump switchover detection
