# Communications

> ATA Chapter 23 — N720AK Systems Reference

## Overview

N720AK's communications stack includes the **Garmin GMA 245** audio panel, **Dynon Com Panel**, and intercom system. The audio panel provides Bluetooth connectivity for phone calls and music.

## Components

| Component | Part Number | Supplier | Notes |
|-----------|-------------|----------|-------|
| Audio panel | [GMA 245](https://drive.google.com/file/d/1e8kQ9axjUSXKm6KyOz8QHKcjZ_O7Li0g/view) | Garmin | Bluetooth, IntelliVox |
| Com radio | [GTN 650](https://drive.google.com/file/d/1sfoTlZ5wrmtwO3mMsBR-yLXfv64Wy9II/view) Com | Garmin | Integrated in GTN 650 |
| Dynon Com panel | [SV-COM-425](https://drive.google.com/file/d/1UfjDYUc6NpaRH4Fd9VGXTsmC3CkCvkWE/view) | Dynon | Com frequency control |
| Nav antenna | [Bob Archer](https://drive.google.com/file/d/1tpQ1PFsuzGcuJrZAru651fHs_7vxFHb9/view) | <!-- TODO --> | Single nav antenna for GTN 650 |
| Com antenna 1 | [CI-121](https://drive.google.com/file/d/1KGBLLrU7Iy-crf-HF9dJbJl_PzbOfsHo/view) | Comant | Top of fuselage |
| Com antenna 2 | [CI-122](https://drive.google.com/file/d/1P0qMaKxGBthdWucwykEZOPH_o9H4uJYB/view) | Comant | Bottom of right wing |
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

### GPS Antennas

#### Dynon SV-GPS-250/A

| Parameter | Value |
|-----------|-------|
| Model | [SV-GPS-250/A](https://dynonavionics.com/gps-receiver-module.php) |
| Type | Combined GPS receiver + antenna module |
| WAAS | Yes |
| Update rate | 5 Hz |
| Weight | 6.7 oz |
| Connections | 4 leads to SkyView DB37 via Serial Port 5 |
| Power | 8 VDC from SkyView DB37 pin 29 (GPS POWER OUT) |
| Ground | SkyView DB37 pin 24 (GPS GND) |
| Data TX | GPS gray/violet wire → DB37 pin 11 (Serial 5 RX) |
| Data RX | GPS gray/orange wire → DB37 pin 12 (Serial 5 TX) |
| Baud rate | 38,400 (SV-GPS-250); Serial Port 5 configured as POS 1 |
| Mounting | Overhead console |
| Used by | Dynon SkyView HDX |

#### Garmin GA 35

| Parameter | Value |
|-----------|-------|
| Model | [GA 35](https://www.garmin.com/en-US/p/6573/) |
| Part number | 013-00235-00 |
| Type | Passive GPS/WAAS antenna with built-in LNA |
| Frequency | 1575.42 MHz ±10 MHz (L1 GPS/WAAS) |
| Gain | 27+ dB at +25°C nominal |
| Impedance | 50 Ω |
| Connector | Female TNC |
| Supply current | 60 mA max |
| Weight | 0.47 lbs |
| Dimensions | 4.68 × 3.00 × 0.81 in |
| Mounting | 4x #8-32 oval head SS screws, 12–15 in-lbs torque |
| Certification | TSO-C144.9 |
| Mounting | Overhead console |
| Used by | Garmin GTN 650 |

- [Installation Instructions (Rev F)](https://static.garmin.com/pumac/190-00848-00_f.pdf)

### ELT Antenna

| Parameter | Value |
|-----------|-------|
| Model | [ACR Artex 110-773](https://www.acrartex.com/products/110-773-whip-antenna-dual-band/) (Rev C) |
| Type | Dual-band whip antenna |
| Frequencies | 121.5 MHz and 406.0 MHz |
| Connector | BNC female |
| Speed rating | Fixed-wing up to 200 knots |
| Included with | Artex ELT 345 kit |

<!-- TODO: mounting location (internal cabin?), coax length/routing -->

### Antenna Summary

| Function | Antenna | Location |
|----------|---------|----------|
| COM 1 | Comant CI-121 | Top of fuselage |
| COM 2 | Comant CI-122 | Bottom of right wing |
| NAV | Bob Archer | <!-- TODO --> |
| Transponder | SteinAir 104-12 | <!-- TODO --> |
| ADS-B | SteinAir 104-17 | <!-- TODO --> |
| Dynon GPS | Dynon SV-GPS-250/A | Overhead console |
| GTN 650 GPS | Garmin GA 35 | Overhead console |
| ELT | ACR Artex 110-773 | <!-- TODO --> |

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
- [Garmin GA 35 Installation Instructions (Rev F)](https://static.garmin.com/pumac/190-00848-00_f.pdf)
- [Garmin GA 35 Product Page](https://www.garmin.com/en-US/p/6573/)
- [Dynon SV-GPS-250/A Product Page](https://dynonavionics.com/gps-receiver-module.php)
- [Dynon SkyView System Installation Guide](https://www.dynonavionics.com/includes/guides/skyview/SkyView_System_Installation_Guide-Rev_AT.pdf)
- [ACR Artex 110-773 Whip Antenna](https://www.acrartex.com/products/110-773-whip-antenna-dual-band/)
- [Artex ELT 345 Manual](https://www.acrartex.com/wp-content/uploads/downloads/1861/ELT_345_Manual_Y1-03-0282P.pdf)
