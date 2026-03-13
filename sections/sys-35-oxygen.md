# Oxygen

> ATA Chapter 35 — N720AK Systems Reference

## Overview

N720AK is equipped with the **Mountain High EDS-4iP** pulse-demand oxygen system. A panel-mounted mode switch toggles between pulse-on-demand and constant flow modes.

## Components

| Component | Part Number | Supplier | Notes |
|-----------|-------------|----------|-------|
| O2 system | [EDS-4iP](https://drive.google.com/file/d/1jyxfl9qch7xVHHYem4MqP5z7yCiDlXEi/view) | Mountain High | Pulse on demand |
| Mode switch | <!-- TODO --> | <!-- TODO --> | Panel mounted |
| O2 bottle | S/N 602-100814 | Mountain High | 6×18, 2216 PSI rating |
| Cannulas | <!-- TODO --> | <!-- TODO --> | <!-- TODO: how many ports? --> |

## How It Works

### Operating Modes

A panel switch selects between:

- **Pulse Mode**: Oxygen delivered in pulses synchronized with inhalation. This is normal operation and conserves oxygen significantly compared to constant flow.
- **Constant Flow**: Continuous oxygen flow. Use at high altitude or if pulse mode is insufficient (e.g., nasal congestion, very high breathing rate).

This switch also serves as the system on/off — there is no separate emergency oxygen switch. In an emergency, switch to constant flow.

<!-- TODO: At what altitude does the EDS-4iP auto-activate? -->
<!-- TODO: How does the system detect inhalation? -->
<!-- TODO: Flow rate at various altitudes -->
<!-- TODO: Bottle duration estimates at typical cruise altitudes -->

## Inspection & Maintenance

### Service History

- **2026-01-12**: O2 cylinder (S/N 602-100814) hydro requalification — passed. Operator: Rod Morton, United Fire. (Invoice in Private/Invoices/)
- **2026-01-16**: Mountain High IPR-0157 regulator overhaul — replaced O-rings, seat seals, valve/reg springs, new E-bypass switch per ECO 2022-001, exhaust-port filter replaced with less-restrictive part (09025-0023-43) per MHTSB-2022-01. Valve test passed at 500/1500/2300 PSI. Cylinder torqued to 60 ft-lbs. (Invoice in Private/Invoices/)

<!-- TODO: Bottle hydro test schedule (next due ~2031 based on 2026-01-12 requalification) -->
<!-- TODO: How to check remaining O2 -->
<!-- TODO: Cannula replacement schedule -->
<!-- TODO: System leak check procedure -->

### Service Bulletin Compliance

- **MHTSB-2022-01** (Emergency Bypass Control Switch Upgrade): Complied 2026-01-16 during IPR overhaul. Exhaust-port filter at EBC switch Port C replaced with less-restrictive part (old: "05"/"F05"/"MB-05", new: "43"/"S43"/"MBS-43", P/N 09025-0023-43). Issue: excessive restriction prevented EBC control line from purging in OFF position, causing oxygen to continue flowing.
- **MHTSB-2022-01A** (Customer Advisory): Companion letter noting that in some cases the IPR regulator return spring may also need adjustment. N720AK's IPR was fully overhauled at the same time, addressing this concern.

## References

- [Mountain High EDS-4iP Manual](https://drive.google.com/file/d/1jyxfl9qch7xVHHYem4MqP5z7yCiDlXEi/view)
- [Mountain High Oxygen System Schematic](https://drive.google.com/file/d/1otK6zi20DjUBk0ewwCl77eq1ITZm7oin/view)
- [MHTSB-2022-01 — EBC Switch Exhaust-Port Filter Upgrade](https://www.mhoxygen.com/2016/download/833/blt-pulse-demand/27082/mhtsb-2022-01a0-apcr0-0152-00.pdf)
- [MHTSB-2022-01A — Customer Advisory Letter](https://www.mhoxygen.com/2016/download/833/blt-pulse-demand/27084/mhtsb-2022-01a1-apcr0-0152-00.pdf)
