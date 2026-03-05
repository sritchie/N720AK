# Electrical Power

> ATA Chapter 24 — N720AK Systems Reference

## Overview

N720AK's electrical system uses a dual-bus architecture managed by the **flyEFII System32 Bus Manager**. Power distribution and electronic circuit breaker protection are provided by the **Vertical Power VPX Sport**. Two **EarthX ETX900** lithium batteries provide redundant power, and a single **60-amp alternator** handles in-flight charging.

## Components

| Component | Part Number | Supplier | Notes |
|-----------|-------------|----------|-------|
| Bus Manager | System32 | flyEFII | Controls essential vs main bus |
| Power distribution | VPX Sport | Vertical Power | Electronic breakers |
| Battery 1 | ETX900 | EarthX | <!-- TODO: location --> |
| Battery 2 | ETX900 | EarthX | <!-- TODO: location --> |
| Alternator | <!-- TODO --> | <!-- TODO --> | 60 amp, 14 volt |
| Master switch | <!-- TODO --> | <!-- TODO --> | Keyed |

## How It Works

### Bus Architecture

- **Essential Bus**: Powers critical engine systems — ignition, fuel injection, fuel pumps. Managed by System32 Bus Manager.
- **Main Bus**: Powers avionics and other aircraft systems via VPX Sport electronic breakers.

### Emergency Endurance Bus

If a battery fails or bus voltage drops critically, the System32 Bus Manager automatically:

1. Disconnects non-essential loads from the main bus
2. Preserves all available power for the essential bus
3. Maintains engine ignition and fuel injection

The **EMERGENCY POWER** switch on the panel manually activates this mode.

### VPX Sport

The VPX Sport provides:
- Electronic circuit breaker protection (no physical breakers to reset)
- Load monitoring and display on EFIS
- Automatic load shedding if needed
- Programmable power channels

<!-- TODO: VPX channel assignments — what's on each channel? -->
<!-- TODO: How are the buses connected? What's the bus tie arrangement? -->
<!-- TODO: Alternator field control — how does it work? -->

## Wiring

<!-- TODO: Bus diagram — essential bus, main bus, VPX channels, battery connections -->
<!-- TODO: Wire gauges for main power runs -->
<!-- TODO: Grounding scheme -->

## Inspection & Maintenance

<!-- TODO: Battery maintenance — EarthX specific procedures, voltage checks, balancing -->
<!-- TODO: Alternator belt inspection, tension -->
<!-- TODO: VPX diagnostics — how to read the log, what to look for -->

## References

<!-- TODO: Links to VPX Sport manual, EarthX specs, System32 bus docs in docs/24-electrical/ -->
