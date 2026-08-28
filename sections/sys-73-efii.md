# EFII System32

> ATA Chapter 73 — N720AK Systems Reference

## Overview

The **EFII System32** provides complete electronic engine management for N720AK — both fuel injection and ignition. This is a fundamentally different architecture from traditional magneto/mechanical fuel injection systems. The System32 replaces the mechanical fuel servo, magnetos, and mixture cable with ECU-controlled port fuel injection and electronic ignition.

## Components

| Component | Part Number | Supplier | Notes |
|-----------|-------------|----------|-------|
| ECU (x2) | [System32](https://drive.google.com/file/d/1qWy2YjOcxXDmAfCELyb1E6BdgQzikOnG/view) | flyEFII | Dual redundant |
| Coil packs | <!-- TODO --> | <!-- TODO --> | One per cylinder |
| Fuel injectors (x6) | [PMI](https://drive.google.com/file/d/1WlyDR120IPO475xFrKHHQDquhz46yU7E/view) | flyEFII | 7075 aluminum, 60lb std / 80lb race. Install in 1/8NPT primer ports, PTFE pipe dope. 1/4NPT fuel rail T fitting. |
| Fuel pumps (x2) | [FPM-1](https://drive.google.com/file/d/1hgK2kdsIXg9Q8jmsiwSf64GxXn0jg-a9/view) | flyEFII | Dual Walbro GSL393, 400HP each, 5A/pump. AN-6 fittings. See [Fuel System](./sys-28-fuel-system.md) |
| Throttle body adapter | [TBFA-1](https://drive.google.com/file/d/1B5nNYFYOsiy5J6uvdSr07eFms28A3tU-/view) | flyEFII | 3 1/4" snout, silicone coupler to 3" adapter. 5.5" total length (same as Bendix servo). |
| System32 controller | <!-- TODO --> | flyEFII | Panel-mounted display/control |

## How It Works

### Electronic Fuel Injection

The System32 ECU controls fuel delivery through port fuel injectors. It uses sensor inputs (MAP, RPM, temperatures, O2) to calculate injector pulse width. The mixture is automatically optimized — no mixture lever or manual leaning required.

The fuel system is a pressurized loop with MAP-referenced regulation. See [Fuel System](./sys-28-fuel-system.md) for complete fuel plumbing and regulator details.

### Electronic Ignition

Dual redundant ignition with individual coil packs for each cylinder. The System32 provides:
- Variable ignition timing based on RPM, MAP, and temperature
- Redundant ECU operation — either ECU can run the engine independently
- Panel switch for manual ECU selection

### Panel Controls

**EFII System32 Switches:**
- Ignition Select
- ECU Select
- Fuel Pump Mode (PMP 2)
- Start Battery Select

<!-- TODO: What does each switch position do? Detail the modes. -->

**EFII Breakers (VPX channels):**

| Breaker | Rating | Function |
|---------|--------|----------|
| ECU 1 | 5 A | ECU 1 power |
| ECU 2 | 5 A | ECU 2 power |
| Ignition | 15 A | Ignition coil packs |
| Fuel Pump | 10 A | Electric fuel pump |

**Annunciator Lamps:**

| Lamp | Color | Function |
|------|-------|----------|
| ECU 1 | Green | ECU 1 active |
| ECU 2 | Green | ECU 2 active |
| Primary Pump | Green | Primary fuel pump running |
| Secondary Pump | Amber | Backup fuel pump activated |

## Fuel Compatibility

The EFII System32 supports 100LL and automotive gasoline, with or without ethanol; the closed-loop mapping handles both. Because the rail runs at 45 PSI with continuous return, **vapor lock downstream of the pumps is physically impossible** — gasoline vapor pressure cannot approach 45 PSI gauge at any survivable temperature. The residual vapor-lock mechanisms are:

- **The suction segment** (tank pickup → duplex valve → FF-2 pre-filter → pump inlets) carries all the standard mogas physics — this is what the volatility and heat-soak limits in [§2 Limitations](02-limitations.md#automotive-fuel-mogas-limitations) protect.
- **Return-fuel heating**: hot rail fuel returns continuously to the selected tank; in a low tank during extended hot ground operations the heat accumulates (the reason EFII's own manual requires ≥5-gallon header tanks in that architecture). On mogas, avoid long ground ops feeding from a low tank, and switch tanks to spread returned heat.
- **The 22 PSI auto-cutover does not protect against suction-side vapor** — Pump 2 shares the same inlet plumbing and cavitates on the same vapor. Fuel-pressure fluctuation on mogas means: switch tanks (cooler fuel), reduce power, descend — not "the backup pump will save it." Cavitation also erodes pump life even when the engine keeps running.

The former 8,000 ft density-altitude and 100 °F OAT limits traced to a single forum post and had no support in EFII, Lycoming, or auto-fuel-STC sources; they were replaced 2026-08-24 with the volatility/temperature limits in §2. Authoritative basis: [Lycoming SI 1070AB](https://drive.google.com/file/d/1Hy5OGaKptmOYBYyTL0mFpC7cQyOJNudS/view) (IO-540-D approved for ASTM D4814 93 AKI, Vapor Pressure Class A-4, ≤1% oxygenate, LW-16702 additive required) and the Petersen auto-fuel STC certification basis (12,500 ft demonstrated on 110 °F winter-blend fuel in suction-fed aircraft).

## Tuning

<!-- TODO: Current fuel map and timing configuration -->
<!-- TODO: How was the engine tuned? What was the process? -->
<!-- TODO: EGT/CHT targets during tuning -->
<!-- TODO: How to adjust the tune if needed -->

## Wiring

<!-- TODO: ECU wiring overview -->
<!-- TODO: Sensor connections — MAP, RPM, temp sensors, O2 -->
<!-- TODO: Coil pack wiring -->
<!-- TODO: Injector wiring -->

## Diagnostics

<!-- TODO: System32 diagnostic modes -->
<!-- TODO: How to read ECU logs -->
<!-- TODO: Common fault codes and what they mean -->

## Inspection & Maintenance

### Inspection intervals (SDS-derived)

flyEFII publishes no consolidated inspection schedule. The intervals below are
adapted from the [SDS EFI Aviation Maintenance/Inspection Schedule (May
2024)](http://www.sdsefi.com/sb.htm) — a competing aircraft port-injection
system with analogous hardware (brushed fuel pumps, port injectors in the
primer bosses, coil packs, Hall crank sensor) — tightened where later SDS
service bulletins tightened them. Tracked in `recurring-items.tsv`.

| Item | Interval | What to look for |
|---|---|---|
| Coil packs & mounts | Every oil change / 50 hr | Fastener tightness, mount cracks; terminal corrosion (dielectric grease on assembly helps) |
| Injector (PMI) mounts | Every oil change / 50 hr | Wiggle test — tightness in the primer-port bosses |
| Post-pump fuel filter | 50 hr / annual | Blow-through test — if you can't blow through easily, clean or replace. Black debris is pump brush carbon (SDS SB 2025-05-15, seen in as little as 75 hr) |
| Pre-pump filter | 100 hr / annual | Debris; green growth = bacteria, treat fuel with biocide |
| Fuel pump listen test | Before start | Run each pump in turn; a smooth quiet whir is normal. Gravelly or changed tone = no-fly, inspect filters and pumps (SDS SB 2023-06-14) |
| Fuel pumps | Annual | Seepage, leaks, noise; SDS replaces alternating-use pairs at 2,000 hr |
| Throttle body | 100 hr / annual | All fasteners incl. throttle-plate screws; linkage heim joint and arm nut |
| Hall (crank) sensor cables | 100 hr / annual | Chafing; keep ≥1 in from plug wires — never tie-wrap sensor wires to plug wires (SDS SB 2020-01-03: destroyed ECUs) |
| Fuel hoses | 100 hr / annual | Chafing, leaks; SDS replaces at 2,000 hr |
| Sensor leads (IAT/CHT/MAP) & vacuum hoses | 100 hr / annual | Chafing, cracking, connector security |
| Regulator vacuum reference | Annual + any fuel-pressure anomaly | Vacuum-port jam nut can seep on Borla regulators (SDS SB 2021-09-12) — Loctite 243 on threads. A reference leak corrupts the 45 PSI DIFF behavior |
| Spark plugs, wires, boots | Annual | Inspect/replace plugs; check wires, terminals, boots |

New installations: check both fuel filters at 10 hr, again at 50 hr, then per
the schedule.

### Injector cleaning

Neither flyEFII nor SDS publishes a routine injector-cleaning interval. The
post-pump fine filter exists to keep particulates out of the injectors, so the
filter schedule protects them indirectly. Clean **on condition** — the symptom
is an unexplained single-cylinder EGT shift or a fuel-trim drift — by pulling
the PMIs and having them ultrasonically cleaned and flow-matched at an
automotive injector service.

### SDS service bulletins worth borrowing (different vendor, same physics)

- **Starter contactor flyback diodes** (SB 2025-06-16): missing diodes on
  starter solenoids/contactors cause random spark events during cranking and
  on starter release — kickbacks and backfires, i.e. the ignition source for
  an induction fire. <!-- TODO: verify N720AK starter contactor diode -->
- **GAMI G100UL not approved** (SB 2024-12-27): swelling O-rings, fuel leaks,
  paint damage; SDS pump/seal components untested with G100UL — EFII
  components are equally untested. Do not fuel N720AK with G100UL.
- **VP-X electronic breakers + EFI** (SB 2015-01-15): electronic breakers trip
  on millisecond coil/injector current peaks far below nominal draw —
  potential in-flight engine stoppage. N720AK's architecture already
  sidesteps this: ignition, injection, and pumps live on the endurance bus
  behind physical breakers, not the VPX.
- **Thread sealant** (SB 2015-10-20): never RTV on fuel fittings; Permatex
  high-performance thread sealant, sparingly, male threads only.
- **Lithium batteries** (SB 2018-02-08): with lithium batteries (EarthX
  ETX900 ×2 here), SDS recommends aural high/low-voltage warning plus
  over-voltage (crowbar) protection.
  <!-- TODO: document N720AK's over-voltage protection story -->

<!-- TODO: ECU firmware update procedure -->
<!-- TODO: Sensor calibration checks -->

## References

- [EFII System32 Installation Manual (Rev 9-13)](https://drive.google.com/file/d/1qWy2YjOcxXDmAfCELyb1E6BdgQzikOnG/view)
- [EFII System32 Operating Procedures (12-20)](https://drive.google.com/file/d/1DpagY70w5oKBDZ5f50atGQ_gukgIGGgV/view)
- [EFII System32 Fuel Flow & RPM Config (Rev 10-19)](https://drive.google.com/file/d/1u1Z214HEJB2bEiMpFU9ltmSb-CmbR7ft/view)
- [EFII System32 Initial Tuning — CSP (Rev 6-20)](https://drive.google.com/file/d/1P36hbiAgYbXRVSpBjiZAR1q9-bidzpfb/view)
- [EFII Bus Manager Installation Instructions](https://drive.google.com/file/d/15OSKV66Y01w9-h93sxs9tNDaLjTv4gw_/view)
- [Fuel System — Regulator Diagnostics](./sys-28-fuel-system.md#diagnostics) — fuel pressure analysis
- [PLX DM-6 Multi Gauge User Guide](https://drive.google.com/file/d/1VIanTxYZkHM7e7pnBZsoarOo_NcaR9Uk/view)
- [PLX SM-AFR Gen2 User Guide](https://drive.google.com/file/d/1bdoRUOQrCC5lVv3VV0NL7xmZuAf7LRID/view)
- [PLX SM-AFR Gen4 Sensor Health Diagnostics](https://drive.google.com/file/d/1Lx1w9HNoKxVuSiyQLt7mKklyZbjxm5Bn/view) — O2 sensor health: replace if <50%. Reaction time: <150ms excellent, >251ms poor. Requires DM-6 V2.0+.
- [EFII Port Mount Injector (PMI) Installation](https://drive.google.com/file/d/1WlyDR120IPO475xFrKHHQDquhz46yU7E/view)
- [EFII Throttle Body Flange Adapter (TBFA-1)](https://drive.google.com/file/d/1B5nNYFYOsiy5J6uvdSr07eFms28A3tU-/view)
- [EFII Dual Fuel Pump Module (FPM-1)](https://drive.google.com/file/d/1hgK2kdsIXg9Q8jmsiwSf64GxXn0jg-a9/view) — Dual Walbro GSL393, 400HP each, 5A/pump, AN-6 fittings. 10A breaker per pump or 20A shared.
