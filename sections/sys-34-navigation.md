# Navigation & Instruments

> ATA Chapter 34 — N720AK Systems Reference

## Overview

N720AK's navigation and instrument suite is built around the **Dynon Skyview HDX** EFIS as the primary flight display, with the **Garmin GTN 650** providing certified IFR GPS/Nav/Com capability. The pitot-static system uses a **Dynon heated pitot** with integrated AoA probe.

## Components

| Component | Part Number | Supplier | Notes |
|-----------|-------------|----------|-------|
| EFIS | [Skyview HDX](https://drive.google.com/file/d/1KruWV-_DQwM96mKAEYfoYNYzVmE1Yptf/view) | Dynon | Primary flight display |
| GPS/Nav/Com | [GTN 650](https://drive.google.com/file/d/1sfoTlZ5wrmtwO3mMsBR-yLXfv64Wy9II/view) | Garmin | Certified IFR, S/N 1Z8021616 |
| Transponder | SV-XPNDR-261 | Dynon | ADS-B Out, S/N 04015 |
| ADS-B Receiver | SV-ADSB-472 (P/N 102985-000) | Dynon | **Dual-band** 978 MHz UAT + 1090 MHz ES. Traffic & weather, S/N 13201. Tailcone. Traded in from SV-ADSB-470 S/N 3111 (Dynon inv. 61735, RMA 28912, 2019-04-02). |
| ELT | [ELT 345](https://drive.google.com/file/d/1OXIHSMY2lg3rjRosWWdaETwle8ACyBID/view) | Artex | 406 MHz |
| Pitot tube | <!-- TODO --> | Dynon | Heated, with AoA |
| Static ports | <!-- TODO --> | <!-- TODO --> | Two ports, aft fuselage |
| Alternate static valve | <!-- TODO --> | <!-- TODO --> | Upper left panel |
| Transponder antenna | 104-12 | SteinAir | Monopole, 1030–1090 MHz, BNC |
| ADS-B antenna | 104-17 | SteinAir | Monopole, 978 MHz, BNC. Warranty-replaced 2026-01-19 (SteinAir inv. 59853). Cut for 978 but serves the 472's 1090 MHz reception as well — this is SteinAir's specified part for the dual-band unit. |

## How It Works

### Dynon Skyview HDX

The Skyview HDX provides:
- Primary Flight Display (PFD) — attitude, airspeed, altitude, heading, VSI
- Multi-Function Display (MFD) — moving map with terrain
- Engine monitoring — all EGT, CHT, oil, fuel flow, fuel pressure
- Traffic display (ADS-B In, dual-band — see below)
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
| SV-ADSB-472 ADS-B Receiver (dual-band) | 13201 |
| SV-ADAHRS-200 (Primary) | 8375 |
| SV-ADAHRS-201 (Secondary) | 4928 |
| SV-AP-PANEL/V Autopilot Panel | 4101 |
| SV42T Autopilot Servo | 50220 |
| Heated AOA/Pitot Probe | 8438 |
| SV-KNOB-PANEL/V Knob Panel | 8500 |
| SV-COM-C25/V Com Radio | 3090 |

### GPS Position Sources — Who Draws the Map

**As of the 2026-08-19 config (SkyView 17.6), the Dynon SV-GPS is POS 1** —
promoted from POS 2, making it the primary position source for the moving map
and synthetic vision at its native 5 Hz, per Dynon's recommended arrangement.
The GTN 650 (via SV-ARINC-429 + Aviation-format serial) remains GPS 1, the
fallback position source at 1 Hz.

Flight-log evidence supports the switch. With the GTN as position source
(July 2026 logs, ~13 flights), the logged position stream showed ~9–14 kt
median discrepancy between position-implied and reported ground speed with
occasional 2–3 s position freezes — consistent with jumpy synthetic-vision
rendering — and the log's GPS Fix Quality / satellite-count columns were
unpopulated in flight (the Aviation-format feed does not carry them). With the
SV-GPS as POS 1 (2026-08-19/20 logs), every in-flight sample showed SBAS-grade
fix quality (2), 12 satellites, sub-knot median position jitter, zero
teleports, and immediate fix at startup. Check the live source under SETUP
MENU > LOCAL DISPLAY SETUP > GPS FIX STATUS.

### ADS-B — What You Transmit vs. What You Receive

Two different boxes on two different links. The distinction determines what traffic you actually see and what you file.

| Direction | Box | Link | What it does |
|---|---|---|---|
| **Out** | SV-XPNDR-261 Mode S transponder | **1090 MHz** extended squitter | The §91.227 compliance item. Broadcasts position, velocity and ident. Confirmed by PAPR 2026-01-28: Link Version 2, no exceptions. |
| **In** | SV-ADSB-472 receiver | **978 MHz UAT** | FIS-B weather (US only) and TIS-B/ADS-R traffic relayed from ground stations |
| **In** | SV-ADSB-472 receiver | **1090 MHz ES** | Direct air-to-air traffic from any 1090ES-equipped aircraft, worldwide, **independent of ground station coverage** |

The dual-band receive is the part that matters in practice: on the 978 link alone, traffic only appears where a ground station is rebroadcasting it. The 1090 side sees 1090ES-equipped aircraft directly — which is the difference between having a traffic picture in the mountains west of Boulder and not having one.

Note the asymmetry: **ADS-B Out is 1090-only, ADS-B In is dual-band.** That combination has no clean ICAO surveillance code for the receive side; see the filing note below.

### ADS-B and Mode S Filing Data

| Item | Value | Source |
|---|---|---|
| ICAO 24-bit address | **A9A396** | Derived from the N-number; confirmed broadcast on PAPR 2026-01-28 |
| ADS-B version | **2** (RTCA DO-260B) | PAPR "Link Version 2" |
| ICAO Field 10b | **E** (Mode S, ident, altitude, extended squitter) + **B2** (1090 Out and In) | — |
| ICAO Field 18 | `SUR/260B` · `CODE/A9A396` | — |
| PBN | `B2C2D2O2S1S2` — RNAV 5/2/1 and basic RNP 1 by GNSS, plus RNP APCH with and without vertical | [Garmin PBN capabilities doc 190-02223-00](https://drive.google.com/file/d/15BXBBOPkEBEeaJ18dpvYFTO7NoIxOkUx/view) |

With no AFMS (experimental), the PBN declaration rests on Garmin's published PBN
capabilities document plus the TSO-C146c install; AC 90-100A allows Part 91
operators to self-qualify. Oceanic codes (A1, L1) require dual GPS plus an LOA —
not filed. RNP AR (T1/T2) is beyond the GTN 650's hardware — never filed.

**Remarks are mandatory, not optional.** Airworthiness certificate limitation 7: *"When filing a flight plan, the experimental nature of this aircraft must be listed in the remarks section."* File `RMK/EXPERIMENTAL`.

<!-- TODO: Confirm the SV-XPNDR-261's configured ADS-B In capability bits report dual-band (they should, given the 472) so ground stations deliver the right services. -->

**Nearest Airport Emergency**: Holding the NEAREST button on the Dynon activates the autopilot to fly directly to the nearest airport matching the current filter settings and automatically tunes the radio to that airport's frequency. See the Dynon HDX Pilot's Guide for filter configuration and exact behavior.

<!-- TODO: Screen configuration — how many screens? What's displayed on each? -->
<!-- TODO: AHRS location and mounting -->

### Garmin GTN 650

The GTN 650 provides:
- IFR-certified GPS approaches (LPV, LNAV/VNAV, LNAV)
- VOR/ILS capability via single Bob Archer nav antenna
- Com radio
- Flight plan management

**SD Card Formatting**: The GTN 650 SD card must be formatted using the [SD Card Formatter](https://www.sdcard.org/downloads/formatter/) utility. Formatting with macOS Disk Utility or Windows (including Parallels) does NOT work. ([VAF thread](https://vansairforce.net/threads/wifi-sd-card-on-g3x.222784/#post-1732873))

### Garmin GTN 650 Database Update

1. On a **Windows** machine, open [Garmin Aviation Database Manager](https://fly.garmin.com/fly-garmin/support/softwareUpdates.htm) and download the current navigation database
2. Write the database to an SD card formatted with the [SD Card Formatter](https://www.sdcard.org/downloads/formatter/) utility (do NOT use macOS Disk Utility or Windows format)
3. Insert the SD card into the GTN 650
4. Power on — the unit should prompt to load the database on startup
5. If the database shows as a "future" database and does not load automatically, **hold down the right knob click button during startup** to force-load the database
<!-- TODO: GTN 650 to Dynon data interface — what data flows between them? -->

### Pitot-Static System

| Component | Location |
|-----------|----------|
| Pitot tube | Under left wing |
| Static ports | Two ports on aft fuselage sides |
| Alternate static valve | Upper left panel |

The pitot tube incorporates a second orifice angled to measure differential pressure for Angle of Attack (AoA) display on the EFIS. Pitot heat is activated by the PITOT HEAT switch.

### The Pitot/AoA Probe Is the Single Point of Failure

**The redundancy is in the computers, not in the probe.** Static is well covered; pitot and AoA are not covered at all.

| Data | Source and redundancy | Caught by the ADAHRS cross-check? |
|------|----------------------|-----------------------------------|
| Magnetic heading | **Dual** — magnetometer inside each ADAHRS | Yes |
| Altitude / VSI | **Good** — two fuselage static ports plumbed together, plus the alternate static valve. One blocked port still leaves the other. | Partially |
| Attitude (pitch/roll) | Dual MEMS sensors, **but the solution consumes airspeed**, and airspeed is common to both units. GPS is the declared fallback. | **No** — a shared-source failure |
| **Airspeed** | **None** — one pitot port on one probe | **No** |
| **AoA — Dynon *and* OnSpeed** | **None** — same probe, same ports | **No** |

The Dynon AoA/Pitot probe carries **pitot and AoA ports only, no static port** — static comes from the two aft-fuselage ports independently. So the exposure is precisely the pitot/AoA probe under the left wing, and altitude and VSI survive its loss.

Three consequences worth understanding:

1. **A pitot blockage produces agreeing wrong data.** Both SV-ADAHRS units breathe through the same probe, so a blocked or iced pitot gives them identical bad airspeed. They agree, so no `ADAHRS CROSS CHK ERROR` is raised. The cross-check protects against a *unit* failing, not against a *shared source* being wrong — which is the more likely failure.

2. **AoA is not a backup for unreliable airspeed, and stall warning goes with it.** OnSpeed uses the Dynon probe rather than independent sensors, so a pitot blockage takes airspeed, Dynon AoA, and OnSpeed simultaneously. Dynon stall warning is AoA-derived, so it goes too.

3. **The attitude solution itself depends on airspeed.** The SkyView installation guide is explicit: *"SkyView's attitude calculation requires airspeed from pitot and static. A GPS source can be used as a backup if the pitot and/or static source fails, but should not be the primary source."* So dual ADAHRS does **not** make attitude immune to a probe blockage — what protects attitude is **GPS**, not the second ADAHRS.

What remains after a pitot blockage: **attitude on GPS backup, altitude and VSI on the independent static system, pitch attitude, power setting, and GPS groundspeed** — with no low-speed protection.

Dynon's own guidance assumes shared air lines: the install guide says to *"consider 'teeing' off of existing lines."* Each module does have its own 1/8" NPT AoA/pitot/static ports, so a genuinely independent second air source is physically possible with a second probe — but Dynon neither describes nor recommends it, and a single pitot is the norm across certified light IFR aircraft.

<!-- TODO: Unreliable-airspeed pitch/power reference table from the bootstrap performance data, and a matching Section 4 checklist (Section 4 is generated from N720AK.json — must be added in the EFIS Editor, not the markdown). -->
<!-- TODO: Confirm how the GPS fallback for the attitude solution is configured and whether it annunciates when it engages. -->
<!-- TODO: Confirm whether both SV-ADAHRS units tee off shared pitot/AoA lines or have separate runs from the probe. Either way the probe is common. -->

> Cross-reference: [OnSpeed AoA](./sys-34-onspeed.md) for the shared-probe detail.

Static blockage is the mitigated case: use the alternate static valve. Pitot blockage has no mitigation but pitot heat and preflight discipline.

<!-- TODO: Unreliable-airspeed pitch/power reference table from the bootstrap performance data, and a matching Section 4 checklist (Section 4 is generated from N720AK.json — must be added in the EFIS Editor, not the markdown). -->
<!-- TODO: Confirm whether both SV-ADAHRS units tee off shared pitot/static/AoA lines or have separate runs from the probe. Either way the probe is common. -->

> Cross-reference: [OnSpeed AoA](./sys-34-onspeed.md) for the shared-probe detail.

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

- [Dynon SkyView HDX Pilot's Guide (Rev T)](https://drive.google.com/file/d/1KruWV-_DQwM96mKAEYfoYNYzVmE1Yptf/view) — SkyView 17.6
- [Dynon SkyView HDX Pilot's Guide (Rev Q)](https://drive.google.com/file/d/1gFLcAkuGtnSpceF6xH8AqwYPzSBzoXUG/view)
- [Dynon SkyView EMS Gauge Customization](https://drive.google.com/file/d/1brCO7Om9oDE73qAHHyzJ-TubZGQNGlDb/view)
- [Dynon SkyView Third-Party Device Connection (Rev E)](https://drive.google.com/file/d/1oxEsay5amF7m1MqrphiiwM65MX3KoH7I/view)
- [TLAR Pilot Guide (v7.80)](https://drive.google.com/file/d/1h-OZnxujNiw7GhTnug2ZU91aJiHWozVy/view)
- [Pitot/Static/AOA Air Kit Installation Guide (Rev 04)](https://drive.google.com/file/d/1lbSCO4jr1xFV5EOb0bN8WuqpEOZiVWfn/view) — Quick-disconnect plumbing kit. Variants: A=SkyView ADAHRS, B=EFIS+backups, C=Steam. Tubing: 25' green (pitot), 32' white (static), 23' blue (AOA), all 1/4".
- [Gretz Aero Pitot Tube Mounting Bracket Installation](https://drive.google.com/file/d/14BIicSMrexJGP9uup3Vh63ahOQn89jS5/view) — Left wing bottom, outboard of main spar inspection plate.
- [Dynon AOA/Pitot Probe Installation Guide (Rev C)](https://drive.google.com/file/d/1BmMD7326HdTBKZCkVp0f_06mPmGQvID8/view) — P/N 100141-000 (unheated), P/N 100667-000 (heated). Doc 100740-001.
