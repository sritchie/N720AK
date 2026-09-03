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

### NAV Audio (VOR/ILS Ident)

The GTN 650's nav receiver audio (Morse ident for VOR/LOC identification) reaches the headsets through two gates in series — both must be open:

1. **GTN 650**: press the **small right knob** to activate the Nav window, then **push the Volume knob** to enable nav ident (an "ID" annunciation appears in the Nav window). Turning the Volume knob while the Nav window is active sets nav audio volume, independent of Com volume. (GTN 650 Pilot's Guide §3.5.1.)
2. **GMA 245**: press the **NAV1** key — nav receiver audio is heard only when its green in-key annunciator is lit. (GMA 245 Pilot's Guide p. 15.)

The GTN also auto-decodes the Morse and displays the identifier next to the active nav frequency, but audible identification requires the chain above.

Related GMA 245 behaviors: the **SPKR** key routes selected radios to the cabin speaker (aural alerts always play on the speaker regardless); press-hold **RADIO MUTE** toggles intercom muting while radio (COM/NAV/AUX) audio is active.

<!-- TODO: Audio routing — how does the GMA 245 manage Dynon, intercom, Bluetooth sources? -->
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

### GTN 650 → GMA 245 Audio Connections

Pin assignments traced on the SteinAir SkyView Interconnect schematic (verified visually end-to-end, 2026-08). Both runs are shielded twisted pairs with backshell-grounded shields:

| Signal | GTN 650 | GMA 245 | Wire |
|--------|---------|---------|------|
| NAV audio (VOR/ILS ident) Hi | P1004-16 (VOR/ILS Audio Hi) | J1-17 (NAV 1 Audio Hi) | White |
| NAV audio (VOR/ILS ident) Lo | P1004-17 (VOR/ILS Audio Lo) | J1-18 (NAV 1 Lo) | White/Blue |
| GPS alert audio Hi (approach callouts, GTN tones) | P1001-4 (Audio Out Hi) | J1-31 (Alert 1 Audio Hi) | White |
| GPS alert audio Lo | P1001-23 (Audio Out Lo) | J1-32 (Alert 1 Audio Lo) | White/Blue |

The GMA 245's **NAV 2 input (J1-19/20) is unwired** — the GTN is the only nav receiver. GTN nav audio and GTN alert audio arrive on separate audio panel inputs (NAV1 key vs. always-on alert input).

COM audio routing per the same drawing: GTN 650 com (P1003) is the GMA 245's **COM 1**; the Dynon SV-COM C25 is **COM 2**.

<!-- TODO: Antenna coax routing details -->

## Backup NavCom — Yaesu FTA-850 (handheld)

Carry-aboard backup transceiver (purchased 2026-08). COM 118–136.975 MHz
transmit/receive, plus **VOR and ILS CDI display** on the NAV band
(108–117.975) and a built-in GPS with waypoint/route navigation — so a total
electrical failure still leaves com, a nav needle, and a position source.
Nav functions are supplemental aids only, per Yaesu.

**In the box** (FTA-850L): SBR-39LI 7.2 V 2200 mAh lithium pack (~10 hr
receive-heavy; 5.5 hr fast charge in the cradle), SAD-25 AC charger +
SBH-11 cradle, **SDD-12 cigarette-lighter DC adapter** (12–24 V — runs off
the panel power port), **SCU-42 headset adapter cable** (aviation headset →
radio), SBT-12 alkaline AA tray (do NOT put rechargeables in it — no
protection circuits), SRA-20A antenna, belt clip, USB cable.

### Condensed operating guide

- **121.5 in one action**: press and hold **[121.5]** — four beeps, tuned.
  Works even with the keypad locked. Exit: [COMM], confirm YES.
- **Frequency entry**: five keypad digits (134.35 → 1-3-4-3-5; trailing
  5/0 of 8.33-style channels auto-completes), or the outer DIAL knob.
  [ENT] on the freq field recalls a recently-used list.
- **Volume/squelch**: inner knob = volume; hold SQL to open squelch for
  setting level against noise. Monitor switch un-mutes weak signals.
- **Transmit**: PTT on the left side; speak close to the grille mic (it's
  waterproof-sealed and needs directed voice) — or use the SCU-42 with a
  real headset, which is the plan in the airplane.
- **Memories**: 400 channels in 9 groups. MENU → MEMORY → group → ▲/▼.
  [SAVE] from COMM mode stores the current freq. Bulk-load from a browser
  with the [FTA-850 Memory Book Programmer](tools/fta850/index.html)
  (Chrome/Edge, USB, no driver) or Yaesu's Windows-only YCE46 software —
  preload home/mission channels (KBDU, KBJC, KLMO, Denver App sectors,
  KEGE and mountain AWOS/CTAFs, Flight Service 122.2).
- **VOR**: tune a NAV-band VOR frequency and the CDI screen appears
  automatically — compass rose, deviation needle, TO/FROM, GPS
  speed-over-ground. Set the course: [FUNC] → OBS → enter the radial.
- **ILS**: tune the localizer frequency; LOC and GS needles display
  automatically. Combined with GPS groundspeed this is a genuine
  get-down-through-a-layer backup.
- **Dual watch**: polls a priority channel while listening to another
  (SETUP → COMM Setup sets the priority; FUNC menu toggles it).
- **Weather**: NOAA weather channels via MENU → WX; GPS position readout
  under the GPS menu for the "where am I" call.
- **Battery discipline**: battery-saver sleep cycles are on by default;
  the display battery icon blinks when charge is critical. AA tray rides
  in the flight bag as the deep reserve.

### Carriage doctrine

- Lives **charged and reachable from the pilot seat** — not in the
  baggage area. The whole point is the panel-dark scenario.
- The SCU-42 headset adapter stays WITH the radio; using the internal
  mic/speaker against cabin noise at cruise is marginal.
- Rubber-duck antenna inside an aluminum cabin costs serious range —
  community consensus is roughly a factor of five versus an external
  antenna. Usable for pattern/tower work; for a real IFR lost-com the
  fix is an external antenna jack (BNC to a spare or belly whip) —
  candidate future wiring project.
- Exercised on a recurring schedule (flight-school `sys-handheld-navcom`
  drill): power on, recall a memory, hold [121.5], tune a VOR and set
  the OBS — so the first fumble happens on the ground.

## Inspection & Maintenance

<!-- TODO: Antenna condition check, connector inspection, headset jack cleaning -->

### PC programming (YCE46) and the web programmer

Yaesu's YCE46 (v1.0.0.0, 2021) is a .NET 4.6 WinForms program; its
"driver" is just an INF binding the radio to Windows' stock USB CDC-ACM
serial driver (VID `26AA`, PID `0024`), so macOS and Linux need no driver
at all. The radio must be in CP mode (hold **SQL** while powering on).
The wire protocol is plain ASCII at 115200 8N1: tab-delimited commands
with a one-byte XOR checksum (`#CMDSY` sync, `#CVRRQ` firmware version,
`#CEPSR` status poll, `#CEPRD`/`#CEPWR` 64-byte reads and writes of a
32 KiB memory image), plus MediaTek PMTK sentences for the GPS logger. A
`.dat` file is that raw image; model code `0352` sits at offsets `0x0100`
and `0x7FFE`, the 400 memory-book entries (48 bytes each) start at
`0x3000`, group names at `0x0300`.

The [web programmer](tools/fta850/index.html) in this handbook
reimplements that protocol over Web Serial and edits only the
memory-book areas. Source: `sections/tools/fta850/`; tests run with
`node --test tests/*.test.mjs` against a fake radio. As of 2026-09 the
write path has not yet been tried against the real radio.

## References

- [Yaesu FTA-850 Operating Manual](https://drive.google.com/file/d/17F35mGrab0zRVGJ53-fjDBMTiwleQnHr/view)
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
