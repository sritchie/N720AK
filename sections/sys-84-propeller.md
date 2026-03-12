# Propeller

> ATA Chapter 84 — N720AK Systems Reference

## Overview

N720AK uses a constant-speed propeller. The propeller governor maintains RPM as set by the pilot, adjusting blade pitch to match power demand.

## Components

| Component | Part Number | Supplier | Notes |
|-----------|-------------|----------|-------|
| Propeller | WWA-RV10 | Whirlwind Aviation | 2-blade, 80" constant speed |
| Governor | PCU5000X | Aero Technologies (Jihostroj) | Constant-speed, FAA PMA (experimental) |
| Spinner | Std 13" | Whirlwind Aviation | Included with propeller |

**Propeller details:**
- Manufacturer: Whirlwind Aviation, 1 Propeller Place, Piqua OH 45356
- Date of Manufacture: 2017-10-12
- Hub Serial: RV10-366
- Blade Serials: RV10-443 & RV10-444
- Weight: 44 lbs
- Length: 80"
- High Pitch: 35.1°, Low Pitch: 12.8°
- Colors: Black w/ White Tips (DBC9700 & DBC2185)
- Aircraft config: RV-10 w/ IO-540 & 260 HP
- 5-year maintenance clock starts on first engine run (2025-11-18)

**Governor details:**
- The PCU5000X is the experimental version of the Jihostroj PCU5000
- Manufactured by Jihostroj (Czech Republic), sold in US as Aero Technologies
- Pumps 30-35% more oil than comparable governors
- Compatible with Whirlwind, Hartzell, MT, McCauley propellers
- 3-year warranty from Aero Technologies

## How It Works

The PCU5000X governor maintains a pilot-selected RPM by adjusting propeller blade pitch through engine oil pressure. When the engine tends to overspeed, the governor increases oil pressure to the prop hub, driving blades toward higher pitch (coarser) to add load. When the engine tends to underspeed, oil pressure is reduced and the counterweights/spring drive blades toward lower pitch (finer).

- **Prop control**: Blue lever — full forward = high RPM, full aft = low RPM
- **Takeoff**: Always full forward for maximum RPM
- **Landing**: Full forward (propeller positioned for immediate go-around)

<!-- TODO: RPM range (min/max governor settings) -->
<!-- TODO: Low pitch stop, high pitch stop -->
<!-- TODO: Feathering capability? -->

### Prop Balance

Two DynaVibe prop balance reports on file:
- December 2025 (initial balance)
- February 2026

Reports saved in GDrive `Public/Performance/prop_balance_12_2025.htm` and `prop_balance_02_2026.htm`.

## Inspection & Maintenance

### Governor Maintenance

Per Jihostroj (manufacturer):
- **Overhaul interval**: At engine overhaul time (no separate governor TBO under normal conditions)
- **Routine checks**: Inspect tightness and security of all external screws, nuts, and levers during routine engine maintenance
- **Oil**: Uses engine oil — frequent oil changes extend governor life
- **Post-bearing-failure**: Governor must be disassembled and cleaned following any engine bearing failure

### Troubleshooting Reference

| Symptom | Common Causes |
|---------|---------------|
| Propeller surging | Transfer bearing leakage, dirty oil, control linkage play, excessive friction |
| RPM drift | Internal oil leakage, high oil temperature, governor wear |
| Governor seizure | Oil contamination |
| Drive failure | Engine vibration |

<!-- TODO: Prop inspection — nicks, erosion, leading edge condition -->
<!-- TODO: Torque values for prop bolts -->
<!-- TODO: Prop overhaul/life limit (Whirlwind 5-year maintenance) -->
<!-- TODO: Spinner inspection and attachment -->

## References

- [Jihostroj PCU5000 Operation & Installation Manual (P-ROV-514/01)](https://drive.google.com/file/d/1NKEBQB5P2vPNg61rXFMayjDfw0GWobEx/view) — covers installation, operation, maintenance, troubleshooting, and overhaul
- [PCU5000X Spec Sheet (Aero Technologies)](https://drive.google.com/file/d/1YAwcA1_zx4bJqVcv5skJ-e-F5T8wburt/view)
- [Jihostroj Installation Page](https://www.jihostroj.com/en/installation.html) — additional installation guidance
- [Jihostroj Maintenance Page](https://www.jihostroj.com/en/maintenance.html) — maintenance procedures and troubleshooting
- [Jihostroj Operation Instructions](https://www.jihostroj.com/en/operation-instructions.html) — operating procedures including feathering

<!-- TODO: Scan Whirlwind RV-10 propeller maintenance manual and upload to GDrive -->
