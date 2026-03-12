# Navigation & Instruments

> ATA Chapter 34 — N720AK Systems Reference

## Overview

N720AK's navigation and instrument suite is built around the **Dynon Skyview HDX** EFIS as the primary flight display, with the **Garmin GTN 650** providing certified IFR GPS/Nav/Com capability. The pitot-static system uses a **Dynon heated pitot** with integrated AoA probe.

## Components

| Component | Part Number | Supplier | Notes |
|-----------|-------------|----------|-------|
| EFIS | [Skyview HDX](https://drive.google.com/file/d/1Y3jAv6gFAzsHuQtpea_3SMW1-8REZwoi/view) | Dynon | Primary flight display |
| GPS/Nav/Com | [GTN 650](https://drive.google.com/file/d/1sfoTlZ5wrmtwO3mMsBR-yLXfv64Wy9II/view) | Garmin | Certified IFR, S/N 1Z8021616 |
| Transponder | SV-XPNDR-261 | Dynon | ADS-B Out, S/N 04015 |
| ADS-B Receiver | SV-ADSB-470 | Dynon | Traffic & weather, S/N 3111 |
| ELT | [ELT 345](https://drive.google.com/file/d/1OXIHSMY2lg3rjRosWWdaETwle8ACyBID/view) | Artex | 406 MHz |
| Pitot tube | <!-- TODO --> | Dynon | Heated, with AoA |
| Static ports | <!-- TODO --> | <!-- TODO --> | Two ports, aft fuselage |
| Alternate static valve | <!-- TODO --> | <!-- TODO --> | Upper left panel |
| Transponder antenna | 104-12 | SteinAir | Monopole, 1030–1090 MHz, BNC |
| ADS-B antenna | 104-17 | SteinAir | Monopole, 978 MHz, BNC |

## How It Works

### Dynon Skyview HDX

The Skyview HDX provides:
- Primary Flight Display (PFD) — attitude, airspeed, altitude, heading, VSI
- Multi-Function Display (MFD) — moving map with terrain
- Engine monitoring — all EGT, CHT, oil, fuel flow, fuel pressure
- Traffic display (ADS-B In)
- Autopilot interface
- Checklists

**Dynon Equipment Serial Numbers** (registered 2017-05-28):

| Product | Serial Number |
|---------|---------------|
| SV-HDX1100 Display | 11672 |
| SV-HDX1100 Display | 11668 |
| SV-HDX800 Display | 10980 |
| SV-ARINC-429 Module | 2360 |
| SV-EMS-220 Engine Monitoring | 6468 |
| SV-XPNDR-261 Transponder | 04015 |
| SV-ADSB-470 ADS-B Receiver | 3111 |
| SV-ADAHRS-200 (Primary) | 8375 |
| SV-ADAHRS-201 (Secondary) | 4928 |
| SV-AP-PANEL/V Autopilot Panel | 4101 |
| SV42T Autopilot Servo | 50220 |
| Heated AOA/Pitot Probe | 8438 |
| SV-KNOB-PANEL/V Knob Panel | 8500 |
| SV-COM-C25/V Com Radio | 3090 |

<!-- TODO: Screen configuration — how many screens? What's displayed on each? -->
<!-- TODO: AHRS location and mounting -->

### Garmin GTN 650

The GTN 650 provides:
- IFR-certified GPS approaches (LPV, LNAV/VNAV, LNAV)
- VOR/ILS capability via single Bob Archer nav antenna
- Com radio
- Flight plan management

**SD Card Formatting**: The GTN 650 SD card must be formatted using the [SD Card Formatter](https://www.sdcard.org/downloads/formatter/) utility. Formatting with macOS Disk Utility or Windows (including Parallels) does NOT work. ([VAF thread](https://vansairforce.net/threads/wifi-sd-card-on-g3x.222784/#post-1732873))

<!-- TODO: Database update procedure -->
<!-- TODO: GTN 650 to Dynon data interface — what data flows between them? -->

### Pitot-Static System

| Component | Location |
|-----------|----------|
| Pitot tube | Under left wing |
| Static ports | Two ports on aft fuselage sides |
| Alternate static valve | Upper left panel |

The pitot tube incorporates a second orifice angled to measure differential pressure for Angle of Attack (AoA) display on the EFIS. Pitot heat is activated by the PITOT HEAT switch.

## Inspection & Maintenance

### Alternate Static Valve

The alternate static source valve is a toggle on the upper left panel. Reference: [Steinair pitot-static toggle switch](https://www.steinair.com/product/pitot-static-toggle-switch/)

### Right Wing Com Antenna Access

To install or remove the right wing com antenna, the outboard aileron push-pull tube must be removed first.

### 91.411 / 91.413 Inspections

Per 14 CFR 91.411 and 91.413, the altimeter system and transponder must be inspected every 24 calendar months if operating in controlled airspace requiring this equipment (IFR flight, Class B/C airspace).

<!-- TODO: Pitot-static system leak check procedure -->
<!-- TODO: ADS-B compliance check -->
### ELT — Artex ELT 345

- **Beacon ID:** 2DC88 5940E FFBFF
- **Registration:** NOAA SARSAT, registered 2025-11-18, expires **2027-11-18**
- **Frequency:** 406 MHz
- **Registration portal:** [beaconregistration.noaa.gov](http://www.beaconregistration.noaa.gov)
- Registration form PDF saved in GDrive `Private/Registration/ELT_registration_form.pdf`

**Battery:** Artex P/N 8322 (replacement ordered via Aircraft Spruce, order #17716532, 2025-11-12)
<!-- TODO: Database currency requirements -->

## References

- [Dynon SkyView HDX Pilot's Guide (Rev R)](https://drive.google.com/file/d/1Y3jAv6gFAzsHuQtpea_3SMW1-8REZwoi/view)
- [Dynon SkyView HDX Pilot's Guide (Rev Q)](https://drive.google.com/file/d/1gFLcAkuGtnSpceF6xH8AqwYPzSBzoXUG/view)
- [Dynon SkyView EMS Gauge Customization](https://drive.google.com/file/d/1brCO7Om9oDE73qAHHyzJ-TubZGQNGlDb/view)
- [Dynon SkyView Third-Party Device Connection (Rev E)](https://drive.google.com/file/d/1oxEsay5amF7m1MqrphiiwM65MX3KoH7I/view)
- [TLAR Pilot Guide (v7.80)](https://drive.google.com/file/d/1h-OZnxujNiw7GhTnug2ZU91aJiHWozVy/view)
