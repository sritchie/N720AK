# Avionics & Wiring

> ATA Chapter 42 — N720AK Systems Reference

## Overview

This section covers N720AK's avionics stack as an integrated system — how everything is wired together, the panel layout, connector types, and the data flow between components. Individual avionics boxes are documented in their own system pages; this page covers the interconnections.

## Avionics Stack

| System | Component | Notes |
|--------|-----------|-------|
| Audio Panel | Garmin GMA 245 | Bluetooth, 4-place intercom |
| Nav/GPS/Com | Garmin GTN 650 | Certified IFR, single Bob Archer nav antenna |
| EFIS | Dynon Skyview HDX | Primary flight display |
| Autopilot | Dynon 3-axis | Roll, pitch, yaw damper servos |
| AP Panel | Dynon | Autopilot control panel |
| Com Panel | Dynon | Com frequency control |
| Knob Panels | Dynon | <!-- TODO: what knob panels? --> |
| Transponder | <!-- TODO --> | ADS-B Out |
| ELT | Artex ELT 345 | 406 MHz |
| Bus Manager | flyEFII System32 | See [Electrical Power](./sys-24-electrical.md) |
| Power Distribution | VPX Sport | See [Electrical Power](./sys-24-electrical.md) |

## Panel Layout

<!-- TODO: Panel photo with callouts -->
<!-- TODO: Panel dimensions and cutout locations -->

## Data Flow

<!-- TODO: How do the avionics talk to each other?
  - GTN 650 ↔ Dynon Skyview: serial? ARINC 429?
  - Dynon ↔ autopilot servos: proprietary bus?
  - GMA 245 audio routing
  - ADS-B data path
  - GPS position sharing
-->

## Wiring

<!-- TODO: Connector types used (D-sub, Molex, etc.) -->
<!-- TODO: Wire labeling scheme -->
<!-- TODO: Harness routing overview -->
<!-- TODO: Firewall passthrough details -->

## Inspection & Maintenance

<!-- TODO: Connector inspection and cleaning -->
<!-- TODO: Wire chafe inspection points -->
<!-- TODO: Antenna inspections -->

## References

- [Power & Lighting Schematic](https://drive.google.com/file/d/1hXrVusmeaCbz3MywPmLUjcQ1TfPFVOE9/view)
- [SkyView Interconnect Schematic](https://drive.google.com/file/d/12A0_Y_iNQHOCiC1JO2z4mCb5z9XO-COs/view)
- [VPX Pro/Sport Load Planning Worksheet](https://drive.google.com/file/d/1uy9UFDHQYeuw0kTXVAed_0YB3Jd1rMf1/view)
- [Dynon SkyView Third-Party Device Connection (Rev E)](https://drive.google.com/file/d/1oxEsay5amF7m1MqrphiiwM65MX3KoH7I/view)
