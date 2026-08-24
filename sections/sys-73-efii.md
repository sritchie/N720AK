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

<!-- TODO: Coil pack inspection -->
<!-- TODO: Injector cleaning schedule -->
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
