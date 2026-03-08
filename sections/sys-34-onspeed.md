# OnSpeed AoA

> ATA Chapter 34 — N720AK Systems Reference

## Overview

The **OnSpeed** system is an audio angle-of-attack (AoA) indicator that provides continuous tone-based feedback on the aircraft's energy state. It uses differential pressure from the pitot-static system to compute AoA and delivers audio tones through the intercom.

<!-- TODO: Confirm OnSpeed is installed and operational on N720AK -->

## Components

| Component | Part Number | Supplier | Notes |
|-----------|-------------|----------|-------|
| OnSpeed box | <!-- TODO --> | FlyOnSpeed | Main processor |
| Pressure sensors | <!-- TODO --> | <!-- TODO --> | <!-- TODO: uses Dynon pitot or separate? --> |

## How It Works

<!-- TODO: How does OnSpeed integrate with N720AK?
  - Does it use the Dynon pitot AoA port or its own probes?
  - Audio routing — through GMA 245 or direct to headsets?
  - Tone scheme — what do the different tones mean?
  - Calibration procedure and current calibration settings
-->

## Calibration

<!-- TODO: OnSpeed calibration procedure
  - How was it calibrated?
  - What are the current settings?
  - How to re-calibrate after maintenance?
-->

## Wiring

OnSpeed connects to the Dynon PFD for power, data, and audio output.

### OnSpeed Connector Pinout

#### Power / Ground

| Pin | Function | Wire Color |
|-----|----------|------------|
| 1 | 12V power (from PFD, 2A fuse) | Red |
| 4 | Ship ground | Black |

#### Data Inputs

| Pin | Function | Wire Color |
|-----|----------|------------|
| 21 | Flap pot wiper | White |
| 25 | EFIS serial4 TX line | Blue |

#### Button / Lower Console

| Pin | Function | Wire Color |
|-----|----------|------------|
| 5 | Ground (to "−" on button, "C1" on button, volume pot "−/CCW", pilot lo) | Black |
| 2 | Volume pot CW | Red/white |
| 9 | Volume pot wiper | Orange/white |
| 11 | "+" on button | Orange/blue |
| 23 | "NO1" on button | Brown/white |

Control cable wiring (6-conductor, button to OnSpeed box):

| Wire | Color |
|------|-------|
| 1 | Red/white |
| 2 | Orange/white |
| 3 | (none) |
| 4 | Orange/blue |
| 5 | Brown/white |
| 6 | Black |

#### Headset Audio Output

| Pin | Function | Wire Color |
|-----|----------|------------|
| 10 | Pilot audio right | Purple/green |
| 22 | Pilot audio left | Purple/yellow |

## Inspection & Maintenance

<!-- TODO: Annual inspection items -->

## References

- [AMX-10A Installation Diagram 1](https://drive.google.com/file/d/13pwiMGAFJFnBhGvPYXi-F6jSHgqcx79H/view)
- [AMX-10A Installation Diagram 2](https://drive.google.com/file/d/1Sw1c2xQJSDzzdc_xtxlVrdaLRYVWg2Jx/view)
- [AMX-10A Installation Diagram 3](https://drive.google.com/file/d/1UFVWUY-fRRcR6ru1VY8mgm_RKLxF4dOI/view)
- [OnSpeed Calibration Configs](https://drive.google.com/drive/folders/1Bt_X_CIPS1z9uNAD2iXAzmN482ym8fyv?usp=sharing) (Public/Configs/OnSpeed/)
