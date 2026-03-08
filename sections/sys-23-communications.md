# Communications

> ATA Chapter 23 — N720AK Systems Reference

## Overview

N720AK's communications stack includes the **Garmin GMA 245** audio panel, **Dynon Com Panel**, and intercom system. The audio panel provides Bluetooth connectivity for phone calls and music.

## Components

| Component | Part Number | Supplier | Notes |
|-----------|-------------|----------|-------|
| Audio panel | GMA 245 | Garmin | Bluetooth, IntelliVox |
| Com radio | GTN 650 Com | Garmin | Integrated in GTN 650 |
| Dynon Com panel | <!-- TODO --> | Dynon | Com frequency control |
| Nav antenna | Bob Archer | <!-- TODO --> | Single nav antenna for GTN 650 |
| Com antenna 1 | CI-121 | Comant | Top of fuselage |
| Com antenna 2 | CI-122 | Comant | Bottom of right wing |
| Intercom | GMA 245 internal | Garmin | 4-place |

## How It Works

<!-- TODO: Audio routing — how does the GMA 245 manage audio between GTN 650, Dynon, intercom, Bluetooth? -->
<!-- TODO: Headset setup — what jacks, what types (GA vs helicopter), any adapters? -->
<!-- TODO: Squelch and IntelliVox setup -->

## Antennas

### COM Antennas

| Spec | CI-121 (top of fuselage) | CI-122 (bottom of right wing) |
|------|--------------------------|-------------------------------|
| Frequency | 118–137 MHz | 118–137 MHz |
| VSWR | 2.5:1 max | 3.0:1 |
| Polarization | Vertical | Vertical |
| Pattern | Omnidirectional | Omnidirectional |
| Impedance | 50 Ω | 50 Ω |
| Power | 50 W | 50 W |
| Weight | 0.5 lb max | 0.5 lb max |
| Height | 18.50 in max | 8.75 in max |
| Material | Cast housing / fiberglass whip | Cast housing / stainless whip |
| Connector | BNC female | BNC |
| FAA TSO | C37d, C38d | C37d, C38d |
| Gasket | B12607-3 cork neoprene | C12607-3 cork neoprene |

The CI-121 is a straight vertical whip (standard Cessna-style). The CI-122 is a bent configuration designed for underside mounting.

All antenna coax is RG-400. See [wing root connectors](sys-24-electrical.md#wing-root-connectors-cpc) for the right wing COM antenna coax routing through the wing root CPC.

### NAV Antenna

- **Bob Archer** — single nav antenna for GTN 650
<!-- TODO: Bob Archer model number, location, coax routing -->

### Transponder & ADS-B Antennas

See also [Navigation & Instruments](sys-34-navigation.md).

| Spec | 104-12 Transponder | 104-17 ADS-B |
|------|-------------------|--------------|
| Frequency | 1030–1090 MHz | 978 MHz |
| VSWR | 1.2:1 @ 1090 MHz, <2:1 @ 1030 MHz | — |
| Length | 3-1/8″ (79.4 mm) | 3-3/8″ (85.7 mm) |
| Weight | 0.053 lb | 0.053 lb |
| Connector | BNC female | BNC male |
| Mounting | O-ring sealed bulkhead feed-through | O-ring sealed bulkhead feed-through |
| Source | [SteinAir](https://www.steinair.com/product/transponder-monopole-antenna/) | [SteinAir](https://www.steinair.com/product/ads-b-monopole-antenna/) |

Both are non-TSO monopole antennas fed by 50 Ω RG-400 coax, with omnidirectional vertically-polarized radiation patterns.

## Wiring

<!-- TODO: Audio wiring overview — GMA 245 to GTN 650, to Dynon, to headset jacks -->
<!-- TODO: Antenna coax routing details -->

## Inspection & Maintenance

<!-- TODO: Antenna condition check, connector inspection, headset jack cleaning -->

## References

- [Garmin GMA 245 Pilot's Guide](https://drive.google.com/file/d/1e8kQ9axjUSXKm6KyOz8QHKcjZ_O7Li0g/view)
- [Garmin GTN 650 Pilot's Guide](https://drive.google.com/file/d/1sfoTlZ5wrmtwO3mMsBR-yLXfv64Wy9II/view)
- [Artex ELT 345 Manual](https://drive.google.com/file/d/1OXIHSMY2lg3rjRosWWdaETwle8ACyBID/view)
- [Comant CI-121 Datasheet](https://drive.google.com/file/d/1KGBLLrU7Iy-crf-HF9dJbJl_PzbOfsHo/view)
- [Comant CI-122 Datasheet](https://drive.google.com/file/d/1P0qMaKxGBthdWucwykEZOPH_o9H4uJYB/view)
- [Dynon SV-COM-425 Customer Drawing](https://drive.google.com/file/d/1UfjDYUc6NpaRH4Fd9VGXTsmC3CkCvkWE/view)
- [Bob Archer — Antennas for Aircraft](https://drive.google.com/file/d/1b2w_VkXSzQI-bU9lCF0idzxq1E5rLWBG/view)
- [Bob Archer Antenna Installation Instructions](https://drive.google.com/file/d/1tpQ1PFsuzGcuJrZAru651fHs_7vxFHb9/view)
