# Avionics & Wiring

> ATA Chapter 42 — N720AK Systems Reference

## Overview

This section covers N720AK's avionics stack as an integrated system — how everything is wired together, the panel layout, connector types, and the data flow between components. Individual avionics boxes are documented in their own system pages; this page covers the interconnections.

## Avionics Stack

| System | Component | Notes |
|--------|-----------|-------|
| Audio Panel | Garmin GMA 245 | Bluetooth, 4-place intercom, S/N 3YL000434 |
| Nav/GPS/Com | Garmin GTN 650 | Certified IFR, single Bob Archer nav antenna, S/N 1Z8021616 |
| EFIS | Dynon Skyview HDX | Primary flight display |
| Autopilot | Dynon 3-axis | Roll, pitch, yaw damper servos |
| AP Panel | Dynon | Autopilot control panel |
| Com Panel | Dynon | Com frequency control |
| Knob Panels | Dynon | <!-- TODO: what knob panels? --> |
| CO Detector | CO Guardian 452-101-012 | Guardian Avionics | **Not currently wired in.** S/N 112081. See [CO Guardian](#co-guardian-452) below |
| Transponder | <!-- TODO --> | ADS-B Out |
| ELT | Artex ELT 345 | 406 MHz |
| Bus Manager | flyEFII System32 | See [Electrical Power](./sys-24-electrical.md) |
| Power Distribution | VPX Sport | See [Electrical Power](./sys-24-electrical.md) |
| Instrument Panel | [Aerosport 310](https://drive.google.com/file/d/1XEkeFnaRrYsqUShLOq1EERuG9CNP62BV/view) | Aerosport Products | Carbon fiber |
| Overhead Console | [Aerosport Carbon](https://drive.google.com/file/d/1aat78Dnjsbh3dJIaiVSpEzNr9fb0-NqJ/view) | Aerosport Products | Houses GPS antennas, AeroVents (4), map lights |
| Map Lights (x2) | MAPLIGHT-R-24 | SteinAir | Red/white switchable LED, 24V, 15mA, dimmable |

### CO Guardian 452

**Model**: 452-101-012 (Certified Remote Mount CO Detector for Dynon Systems)
**S/N**: 112081
**Status**: Not currently installed. The unit was replaced under RMA 11096 (Dec 2025). The Dynon EMS pin it previously occupied (pin 31, brown/blue wire) is now used by the Monkworkz MZ-30 generator proportional current output.

**Wiring for future reinstallation**:
- The brown/blue wire for the CO Guardian's EFIS connection is tied up near the Dynon EMS connector
- Audio warning line runs from the CO detector location to the GMA 245 Music input (currently disconnected, difficult to reach behind panel)
- Dynon sensor definition file: [CO Guardian Sensor Config (RevC)](https://drive.google.com/file/d/1Xkl4iw0zSDyENs1FRKbf_wncMTQaPB9u/view) — already filed in GDrive Configs/Dynon
- Circuit breaker: 7277-2-2 (2A, 14/28 VDC Avionics)
- RS-232 interface available (optional)

**References**:
- [CO Guardian 452 Installation Drawings (Rev G)](https://drive.google.com/file/d/1ynvn6eUuAsSj5bIYoHiptycL0zvR_6YZ/view)

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

### Known Wiring Notes

**Serial 4 (Dynon ↔ GTN 650)**: The blue and green wires are intentionally flipped on this serial connection. This swap was done during installation — the TX/RX lines needed to be crossed for proper communication between the Dynon SkyView and GTN 650 on serial port 4.

**Disconnected audio warning line**: The old CO audio warning line runs from the former CO detector location to the GMA 245 Music input. This line is currently disconnected. It is difficult to reach — runs behind the panel.

**Disconnected serial 4 line**: A serial 4 cable was cut — it leads from one of the GTN 650's serial outputs to the Dynon's serial 4 port. Both connections are a major pain to reach and worth documenting on an updated schematic.

## Wiring

<!-- TODO: Connector types used (D-sub, Molex, etc.) -->
<!-- TODO: Wire labeling scheme -->
<!-- TODO: Harness routing overview -->
<!-- TODO: Firewall passthrough details -->

## Inspection & Maintenance

<!-- TODO: Connector inspection and cleaning -->
<!-- TODO: Wire chafe inspection points -->
<!-- TODO: Antenna inspections -->

### Connector References

- **Delphi connectors**: [VAF thread — which Delphi connectors for RV-10](https://vansairforce.net/community/showthread.php?t=142169)
- **Metri-Pack connectors**: [VAF thread — Metri-Pack connectors for engine sensor harness](https://vansairforce.net/community/showthread.php?t=125549)

### EMS Wiring

The Dynon SkyView Installation Guide page 7-7 shows the EMS wiring diagram for engine sensor connections.

## References

- [Power & Lighting Schematic](https://drive.google.com/file/d/1hXrVusmeaCbz3MywPmLUjcQ1TfPFVOE9/view)
- [SkyView Interconnect Schematic](https://drive.google.com/file/d/12A0_Y_iNQHOCiC1JO2z4mCb5z9XO-COs/view)
- [VPX Pro/Sport Load Planning Worksheet](https://drive.google.com/file/d/1uy9UFDHQYeuw0kTXVAed_0YB3Jd1rMf1/view)
- [Dynon SkyView Third-Party Device Connection (Rev E)](https://drive.google.com/file/d/1oxEsay5amF7m1MqrphiiwM65MX3KoH7I/view)
- [CO Guardian 452 Installation Drawings (Rev G)](https://drive.google.com/file/d/1ynvn6eUuAsSj5bIYoHiptycL0zvR_6YZ/view)
- [CO Guardian Sensor Config (RevC)](https://drive.google.com/file/d/1Xkl4iw0zSDyENs1FRKbf_wncMTQaPB9u/view) — Dynon sensor definition file
- [Aerosport 310 Panel Installation](https://drive.google.com/file/d/1XEkeFnaRrYsqUShLOq1EERuG9CNP62BV/view)
- [Aerosport Overhead Console Installation](https://drive.google.com/file/d/1aat78Dnjsbh3dJIaiVSpEzNr9fb0-NqJ/view)
- [Aerosport Switch Hole Dimensions](https://drive.google.com/file/d/1HmPeGt9jzB_QAWJ-khXQDT_Y__GTGZ2U/view)
- [Aerosport Switch Wiring Diagram](https://drive.google.com/file/d/1a5IdEYA0HwpPrvTgOwI8GaTtZSjuGCYF/view)
