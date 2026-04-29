# Handling, Servicing and Maintenance

## General

The airplane should be moved using a tow bar which connects to the nose wheel.
The airplane may be pushed or pulled from the inboard portions of the prop
blades. **Do not push on the spinner!**

## Ground Handling

The airplane has three tie-down rings:

- One on each wing (near outboard bellcrank access panel)
- One on the tail

The tie-down rings are removable and may be kept inside the baggage compartment.

### Jacking

The airplane can be jacked from:

- Tie-down ring locations
- Main spar just outboard of fuselage (protect with padded boards)

## Engine Air Filter

| Specification | Value |
|---------------|-------|
| Filter Type | Van's FAB-540 filtered air box (VFR only) |
| Modified Alt Air Door | Aluminum sliding gate, cable-actuated from cabin (open/close) |
| Service | Inspect and clean filter per FAB-540 installation guide |

> Detailed reference: [sys-71-engine.md — Alt Air Door](./sys-71-engine.md#alt-air-door)

## Brake Service

| Specification | Value |
|---------------|-------|
| Brake Fluid | Royco 782 (MIL-PRF-83282) |
| Brake Type | Hydraulic disc |
| Brake Linings | <!-- TODO: Add part number --> |

**Warning**: Use only MIL-PRF-83282 specification hydraulic fluid. Do not
substitute automotive brake fluid.

## Landing Gear Service

| Item | Specification |
|------|---------------|
| Main Tire Pressure | <!-- TODO --> PSI |
| Nose Tire Pressure | <!-- TODO --> PSI |
| Main Tire Size | <!-- TODO --> |
| Nose Tire Size | <!-- TODO --> |

### Wheel Bearings

Repack main wheel bearings with Aeroshell #5 grease at annual condition
inspection.

## Propeller Service

The propeller must be lubricated at intervals not to exceed 100 hours or
12 calendar months, whichever occurs first.

| Specification | Value |
|---------------|-------|
| Grease Type | <!-- TODO: Verify grease spec --> |
| Interval | 100 hours / 12 months |

**Note**: If annual operation is significantly less than 100 hours, or if
operated in high humidity or salty air conditions, reduce calendar interval
to six months.

## Oil System Service

| Item | Specification |
|------|---------------|
| Oil Type | SAE 15W-50 or 20W-50 (multi-grade aviation) |
| Sump Capacity (max) | 12 quarts |
| Minimum for Operation | 8 quarts |
| Recommended Quantity | 9 quarts (extended flight) |
| Oil Drain Plug | Aircraft Spruce 05-12373 magnetic super plug, 1/2" NPT |
| Oil Quick Drain | Saf-Air P5000 |
| Oil Separator | Antisplat Aero ASA |
| Change Interval | 50 hours / 4 calendar months (Lycoming SB 480), whichever first |

### Oil Change Procedure

1. Change oil and filter every 50 hours / 4 months (whichever first).
2. Remove and inspect oil suction screen for metal.
3. Cut filter and inspect for metal.
4. Replace crush washers as required.
5. Refill with 9 quarts (8 minimum for operation; do not exceed 12).
6. Run engine briefly and check for leaks.

### 50-Hour Companion Tasks

Perform these at every oil change:

**Spark plugs**: Remove, clean, inspect electrodes, re-gap, rotate top↔bottom.

**Oil analysis**: Take sample for Blackstone Labs before draining old oil.

**Anti-Splat oil separator evacuation tube**: Inspect where the evacuation tube enters the exhaust pipe. Remove any carbon coking or buildup that could block crankcase blowby flow. The evacuation tube is saddle-mounted to the exhaust pipe with two stainless steel clamps — look up into the tube entry point and scrape/clean any deposits. If excessive buildup is found, shorten the inspection interval. The safety bypass (0.5 PSI pop-off valve) provides a backup path if the tube blocks, but does not eliminate the need for inspection. See [Anti-Splat installation guide](https://drive.google.com/file/d/1NkfPKDnFfFsIQvHDnso-gt4cVNGTY-EB/view).

**PLX O2 sensor health**: Check sensor health percentage on the DM-6 gauge (requires firmware V2.0+). Replace the wideband sensor if health drops below 50%. Also check reaction time — below 150ms is excellent, above 251ms indicates a degraded sensor. 100LL avgas poisons the sensor faster than mogas; expect 300-500 hours of life on avgas. See [PLX Gen4 sensor diagnostics](https://drive.google.com/file/d/1Lx1w9HNoKxVuSiyQLt7mKklyZbjxm5Bn/view).

## Fuel System Service

### Fuel Strainer

Drain fuel strainer:

- Before first flight of day
- After each refueling
- Check for water and sediment

### Fuel Tank Sumps

Drain each tank sump and check for water/contamination:

- Before first flight of day
- After refueling

## Generator Service

### Monkworkz MZ-30

| Item | Specification |
|------|---------------|
| Type | Permanent-magnet generator |
| Mount | Engine vacuum pad (1.3:1 crankshaft ratio) |
| Output | ~14.4 VDC, 30A max |
| RPM Limit | 3572 crankshaft RPM |
| Regulator | MZ Regulator (mounted on engine mount) |

The MZ-30 requires no brushes or field winding — maintenance is minimal.

**Condition inspection items:**

- Inspect generator mount bolts and silicon/fiberglass gasket
- Check 12 AWG phase wires from generator to regulator for chafe, routing
  clear of exhaust, and no tension from engine movement
- Check regulator mounting on engine mount
- Inspect Pico-Lock connectors (input and output) for security — add
  maintenance loops if missing
- Verify cooling ducts (3/4" corrugated nylon) are intact and connected
  to both generator and regulator
- Check regulator blink code LED (4 flashes/sec = enabled and normal)
- Verify shear coupling is intact: generator should NOT rotate freely.
  If it does, the shear coupling has split — contact Monkworkz for replacement.
- Keep ferrous metal shavings away from generator exterior (permanent magnets)

**Operational check:**

With engine running and enable switch on, Battery 2 voltage should show a
charging indication. The BOSCH relay (0332019155) should be energized
(audible click when enable switch is toggled with ignition on).

**Do not open the regulator box** — adhesive inside dampens vibration,
and opening risks tearing components off the circuit board.

**Fuses**: Input and output fuses are internal to the regulator. If either
blows, the regulator likely needs service. Fuses can be tested with an
ohmmeter (should show near-zero resistance). Contact Monkworkz for
replacement.

## Battery Service

| Battery | Location | Type | Charging Source |
|---------|----------|------|-----------------|
| Battery 1 | Tailcone / baggage-area junction (right side) | EarthX ETX900 | Hartzell 60 A primary alternator |
| Battery 2 | Tailcone / baggage-area junction (right side) | EarthX ETX900 | Monkworkz MZ-30 generator |

The two charging systems are fully isolated. **Do not charge with non-LiFePO4 chargers** — EarthX batteries have an internal BMS and require lithium-specific charging.

**Approved chargers (filed in shop):**

- OptiMate Lithium 4s 5A (TM-291) — 5A maintainer
- OptiMate TM-275 v2 — 9.5A charger / maintainer / 13.6V power supply (TUNE mode for avionics work without battery drain)

**Charger sleep behavior:** OptiMate units enter sleep once fully charged and check voltage hourly. If a continuous parasitic load is present (panel powered for configuration), the maintainer may not detect drain and the battery can deplete. Use TM-275 TUNE mode (continuous 13.6 V) for any avionics work session that requires panel power.

> Detailed reference: [sys-24-electrical.md — EarthX Battery & Chargers](./sys-24-electrical.md#earthx-battery--chargers)

## Lubrication Schedule

| Item | Lubricant | Interval |
|------|-----------|----------|
| Wheel Bearings | Aeroshell #5 | Annual |
| Control Hinges | LPS-2 or equivalent | As needed |
| Nose Wheel Steering | <!-- TODO --> | Annual |
| Propeller | <!-- See propeller section --> | 100 hrs/12 mo |

## Tire Replacement

| Tire | Size | Ply |
|------|------|-----|
| Main | <!-- TODO --> | |
| Nose | <!-- TODO --> | |

## Oxygen System Service

Mountain High EDS-4iP system:

- Refill oxygen per Mountain High procedures
- Inspect cannulas and tubing
- Verify pulse delivery operation

## Dynon Maintenance Log — Scheduled Items

The following items are configured in the Dynon SkyView maintenance log
(SETUP MENU > SYSTEM SETUP > AIRCRAFT INFORMATION > MAINTENANCE LOG).
The MAINT LOG page is accessible via MENU > MAINT LOG. Past-due items
show in red at startup.

### Tach-Based Items

| Slot | Name | Basis | Interval | Notes |
|------|------|-------|----------|-------|
| 1 | OIL CHANGE | TACH | 50 hrs | Oil + filter change, spark plug clean/rotate/re-gap, oil analysis sample (Blackstone). Also: inspect Anti-Splat evacuation tube for coking, check PLX O2 sensor health on DM-6. Also due every 4 calendar months (Lycoming SB 480), whichever comes first. Reset to current tach + 50. |
| 2 | PROP | TACH | 650 hrs | Whirlwind WWA-RV10 inspection. Reset to current tach + 650. |

### Date-Based Items

| Slot | Name | Basis | Current Due | Interval | Notes |
|------|------|-------|-------------|----------|-------|
| 3 | COND INSPECT | DATE | 2026-11-18 | 12 months | Annual condition inspection per 14 CFR 91.409(b). |
| 4 | ELT | DATE | 2026-11-18 | 12 months | ELT inspection per 14 CFR 91.207. Artex ELT 345 S/N 267-02567. |
| 5 | XPDR STATIC | DATE | 2027-12-31 | 24 months | Transponder + pitot-static + altimeter per 14 CFR 91.411/91.413. Front Range Transponder Svc, Broomfield. |
| 6 | MEDICAL | DATE | 2030-10-28 | Per class | Pilot medical certificate expiration. |
| 7 | CO GUARDIAN | DATE | 2031-01-08 | 5-7 years | Guardian Avionics 452-101-012 S/N 112081 overhaul. Installed 2026-01-08. |
| 8 | O2 CYLINDER | DATE | 2031-05-31 | End of life | Mountain High CFFC-048 S/N 602-100814. Hydro test passed 2026-01-15. Cylinder end of life 2031-05-31. |
| 9 | ELT BATTERY | DATE | 2032-11-30 | Per mfr | Artex P/N 8322, S/N 1024675-018 Rev F. Installed 2025-12-08. |
| 10 | *(empty)* | | | | |

### Not in Dynon — Track Separately

| Item | Interval | Notes |
|------|----------|-------|
| Fire extinguishers | 12 months | H3R Aviation A344T (Halon 1211, 1.25 lb). Two installed: right rear passenger seat, co-pilot tunnel side. Inspect gauge (green), weight, and condition at condition inspection. |
| Compression check | 100 hrs (break-in) | Differential compression test. More frequent during break-in, then at each condition inspection. |
| Oil analysis | 50 hrs | Blackstone Labs sample at each oil change. Not yet started — first sample due at first oil change. |
| Oil separator (Anti-Splat) | 50 hrs | Inspect evacuation tube where it enters exhaust pipe — remove coking/buildup. Coincides with oil change. If excessive buildup, shorten interval. See [installation guide](https://drive.google.com/file/d/1NkfPKDnFfFsIQvHDnso-gt4cVNGTY-EB/view). |
| O2 sensor health (PLX SM-AFR) | 50 hrs | Check sensor health % on DM-6 gauge (V2.0+). Replace if <50%. Reaction time: <150ms excellent, >251ms poor. 100LL poisons sensor faster — expect 300-500 hrs life on avgas. See [Gen4 diagnostics](https://drive.google.com/file/d/1Lx1w9HNoKxVuSiyQLt7mKklyZbjxm5Bn/view). |
| ELT registration | 2 years | NOAA SARSAT, expires 2027-11-18. Portal: beaconregistration.noaa.gov |

## Pitot Heat Check

Verify pitot heat operation before flight into potential icing conditions:

1. Turn on PITOT HEAT switch
2. Verify pitot tube warms (carefully touch)
3. Monitor current draw on VPX display
