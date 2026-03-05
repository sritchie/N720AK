# EFII System32

> ATA Chapter 73 — N720AK Systems Reference

## Overview

The **EFII System32** provides complete electronic engine management for N720AK — both fuel injection and ignition. This is a fundamentally different architecture from traditional magneto/mechanical fuel injection systems. The System32 replaces the mechanical fuel servo, magnetos, and mixture cable with ECU-controlled port fuel injection and electronic ignition.

## Components

| Component | Part Number | Supplier | Notes |
|-----------|-------------|----------|-------|
| ECU (x2) | System32 | flyEFII | Dual redundant |
| Coil packs | <!-- TODO --> | <!-- TODO --> | One per cylinder |
| Fuel injectors (x6) | <!-- TODO --> | <!-- TODO --> | Port injection |
| Fuel pumps (x2) | Walbro GSL391 | Walbro/EFII | See [Fuel System](./sys-28-fuel-system.md) |
| Throttle body | <!-- TODO --> | <!-- TODO --> | <!-- TODO --> |
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
