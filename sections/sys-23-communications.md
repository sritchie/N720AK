# Communications

> ATA Chapter 23 — N720AK Systems Reference

## Overview

N720AK's communications stack includes the **Garmin GMA 245** audio panel, **Dynon Com Panel**, and intercom system. The audio panel provides Bluetooth connectivity for phone calls and music.

## Components

| Component | Part Number | Supplier | Notes |
|-----------|-------------|----------|-------|
| Audio panel | [GMA 245](https://drive.google.com/file/d/1e8kQ9axjUSXKm6KyOz8QHKcjZ_O7Li0g/view) | Garmin | Bluetooth, IntelliVox |
| Com radio | [GTN 650](https://drive.google.com/file/d/1sfoTlZ5wrmtwO3mMsBR-yLXfv64Wy9II/view) Com | Garmin | Integrated in GTN 650 |
| Com radio 2 | [SV-COM-425](https://drive.google.com/file/d/1UfjDYUc6NpaRH4Fd9VGXTsmC3CkCvkWE/view) | Dynon | A complete second com radio, not just a control head: the SV-COM-425 kit is an SV-COM-C25 panel head plus a remote SV-COM-T25 transceiver. The antenna BNC is on the **T25**. <!-- TODO: where is the T25 mounted? Needed before any radio-end coax work on COM 2. --> |
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

#### Feedline Mapping

Confirmed at the airplane **2026-09-22**, during the COM 1 receive
investigation:

| | COM 1 | COM 2 |
|---|---|---|
| Radio | Garmin **GTN 650** com | Dynon **SV-COM** (T25 transceiver) |
| Audio panel input | GMA 245 COM 1 | GMA 245 COM 2 |
| Antenna | **CI-121**, top of fuselage | **CI-122**, bottom of right wing |
| Radio-end connector | Back of the GTN tray, **outboard side** | At the T25 |

The radio assignment comes from the SteinAir interconnect drawing (GTN P1003 →
GMA 245 COM 1) and is corroborated by the VPX circuit labelled "COM 2
(SV-COM)" in [Electrical Power](sys-24-electrical.md). The antenna assignment
was previously an unsourced build-record entry; it is now confirmed by
direction — the coax leaving the GTN's com BNC runs **up and aft toward the
cabin top**, not outboard toward the wing root.

Two consequences that matter for diagnostics:

- **COM 1's feedline never passes through the wing root.** The NAV and COM
  barrels found in contact at the right wing root on 2026-09-16 are therefore
  the **nav** and **COM 2** feedlines, not COM 1. They were separated and
  secured the same day — that item is closed, and it is unrelated to the COM 1
  fault.
- **There is not enough slack at the radio end to swap the two com
  feedlines**, so a direct COM 1 ↔ COM 2 A/B swap is not available as a
  diagnostic on this airframe. Substituting a test antenna at the radio, or
  sweeping the feedline from the radio end, replaces it.


### NAV Antenna

- **Bob Archer** (Sportcraft) — single wingtip nav antenna feeding the GTN 650.
  VOR, localizer and glideslope all come off this one antenna; the GTN's
  glideslope diplexer is internal, so no external splitter is fitted.
- Mounted in the **right** wingtip. The coax reaches the panel through an inline
  BNC at the right wing root — see
  [wing root connectors](sys-24-electrical.md#wing-root-connectors-cpc).
<!-- TODO: Bob Archer model number (SA-001 or VOR Model 1), exact position in the tip, coax routing -->

**Grounding caveat specific to N720AK.** Archer's design grounds the antenna's
base strip by clamping it between the wingtip and the wing skin under the
nutplate screws. N720AK's wingtips are on
[piano hinges](sys-52-doors-airframe.md#wingtip-attachment), so that path does
not exist here. Anodized hinge stock is a poor RF conductor, and two RV-10
owners with hinge-mounted tips traced a wagging needle and a dead antenna to
exactly this, both fixed with a strap from the base leg to the outboard rib.
**Verify the base leg reads under 1 Ω to the rib** whenever the tip is off.

**Known-good reference numbers** for a stock Archer, from owners who measured:
SWR under 2:1 across 108–118 MHz, and 4:1 to 6:1 at glideslope frequencies.
The poor glideslope match is normal — Archer never designed for 330 MHz, and a
GTN 650 works through it.

**Diagnostics**: `plans/vor-antenna-diagnostic.md` covers the RF interference
survey, VNA measurement, and the antenna rebuild dimensions.

### COM 1 Receive Fault — 2026-09-22

COM 1 (GTN 650 → CI-121) receives so poorly as to be unusable: a strong
transmitter on the field will not break squelch. Recurring, not new. Measured
at the airplane on 2026-09-22 with the coax broken at the **GTN tray barrel**
(back of the tray, outboard side).

**Observations**

| Test | Result |
|---|---|
| COM 1 on aircraft antenna | Very high noise floor; noise drops when a station keys, so AGC is capturing; squelch barely twitches |
| COM 1 antenna disconnected | All static, no reception — only marginally worse than connected |
| COM 1 on telescopic whip at the same BNC | **Good.** Low noise floor, squelch breaks cleanly, close to COM 2 |
| Electrical loads switched off one at a time, down to bus minimum | No change in noise floor |
| Barrel flexed and worked while listening | No change |
| Coax shield → airframe, at the GTN end | **0.1–0.2 Ω** (leads 0.1 Ω) = 0.0–0.1 Ω actual |
| Centre → shield | **Not measured** |

**Interpretation.** This is signal loss, not noise ingress. The static is the
receiver's own noise under an AGC running wide open for want of signal; that
the chain is only marginally better than a disconnected antenna puts the loss
somewhere around 15–25 dB.

**Eliminated:** the GTN's receiver (works on a whip at the same connector) and
any onboard noise source (loads have no effect).

**Read the shield measurement carefully.** 0.0–0.1 Ω from the coax braid to
airframe proves there is a good conductive path to ground, but *not* that the
path runs through the CI-121's flange — a shield can pick up a bond anywhere
along its run. It therefore does **not** establish that the coax is still
connected at the antenna.

### NanoVNA sweep, 2026-09-22

Swept from the GTN tray barrel looking outward, 100–160 MHz, 401 points.
Uncalibrated screening sweep — adequate for this verdict, since calibration
error at VHF is worth a few tenths of SWR and cannot manufacture the result
below.

| Frequency | SWR |
|---|---|
| 100 MHz | 21.4 |
| 120 MHz | 18.1 |
| 127 MHz | 17.6 |
| 140 MHz | 17.6 |
| 160 MHz | 15.3 |

**No resonance anywhere across 60 MHz of sweep.** A healthy CI-121 shows a
minimum of 1.1–1.5 somewhere in 118–137. Mean |Γ| 0.894 — 80% of power
reflected. The smooth monotonic slope is cable loss rising with frequency
attenuating the return, which is the signature of **total reflection at the
end of a lossy line**: an open circuit.

**The open is not at the panel-end barrel.** A fault at the measurement port
would read near-infinite SWR with no frequency slope. The observed ~1 dB
return loss implies roughly 0.5 dB one-way cable loss to the fault — at
RG-400's ~2.6 dB/100 ft, on the order of **15–20 ft of cable**, which is about
the run length from the panel to the top of the fuselage. This is consistent
with flexing the panel-end barrel having had no effect.

### The antenna is good — the feedline is the fault

The CI-121 was found **properly connected** at its base, with no visible
corrosion or damage. Swept directly at the antenna base connector with the
coax removed, same instrument and same state minutes after the feedline
sweep:

| Sweep | Mean SWR | Resonance | Verdict |
|---|---|---|---|
| **CI-121 alone**, at the antenna base | **1.5** | 1.3 at **132.1 MHz** | Healthy |
| Antenna + feedline, from the GTN tray | 17.8 | none | Open |

Spot values for the antenna alone: 118 = 1.8, 122.8 = 1.6, 127 = 1.6,
132 = 1.3, 136.975 = 1.5.

**Keep 1.3 at 132.1 MHz as the known-good reference for this CI-121.** It is
a directly measured baseline for future comparison.

**Conclusion:** the antenna is healthy and the **coax run between the GTN
tray barrel and the CI-121 base is open**. The centre conductor path is
broken somewhere in the cable or in one of its two end connectors. The
barrel disturbed on 2026-09-16 is not implicated — flexing it changed
nothing, and the measured loss to the fault puts it well away from the
panel end.

### Locating the break — DC and TDR

**Loop continuity.** With the coax free at both ends, centre shorted to shield
at the CI-121 end, the GTN end read **open**. The run is broken; the antenna
is not in the circuit at all.

**Time-domain reflectometry.** Swept 1–900 MHz from each end in turn with the
far end open, transformed with velocity factor 0.695 for RG-400
(`scripts/vna_tdr.py`, 0.116 m resolution):

| Swept from | Distance to the open |
|---|---|
| GTN panel end | **2.67 m — 8.77 ft** |
| CI-121 antenna end | **5.15 m — 16.90 ft** |
| **Total run length** | **7.82 m — 25.67 ft** |

Two independent measurements from opposite ends, each showing a single
dominant reflection, summing to a coherent run length. Neither end connector
shows anything beyond the normal adapter reflection at 0.16 m, and nothing
appears between the port and the break on either sweep — the cable is clean
up to the fault from both directions.

**The break is mid-run, roughly 8.8 ft of cable from the GTN tray**, not at
either termination. Wide-band sweeps are what make this measurable: at the
COM band's 60 MHz span the resolution is 5.7 ft, useless here; at 1–900 MHz
it is 4.6 in.

**Measured from the coax connector's own face** rather than the VNA
reference plane (subtracting the 0.16 m adapter reflection seen on every
sweep): the break is **8.25 ft** from the GTN end and **16.37 ft** from the
antenna end, in a run of about **24.6 ft**. Use 8.2–8.3 ft when tracing with
a tape.

**Confidence.** Four sweeps from the panel end — three at 1–900 MHz and one at
1–1500 MHz — span 8.75–8.77 ft, a spread of a quarter inch. The 1500 MHz
sweep is the meaningful check rather than the repeats: different bandwidth,
different window, 2.7 in resolution instead of 4.6, and the feature does not
move. Velocity-factor error is not a threat either — sweeping VF from 0.66 to
0.72 moves the answer only from 8.33 to 9.09 ft, and RG-400 is solid PTFE at
0.695.

At 2.7 in resolution the fault is still a **single feature**, which points to
one discrete injury — a connector or a sharp local damage — rather than a
degraded length of cable.

**Total COM 1 coax length is ~24.6 ft** — not previously recorded.

<!-- TODO: physical location of the break at 8.8 ft; cause; repair. -->
<!-- TODO: COM 1 coax routing from the panel to the CI-121 — undocumented. -->


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

### ELT Remote Switch

N720AK has a **panel-mounted ELT remote switch** (part of the Artex ELT 345
installation). It allows manual activation from the cockpit, so the beacon can
be turned on *before* an off-airport landing instead of depending on the
crash-activated g-switch.

This matters more than it looks: ELTs transmit after a crash only about half the
time — some fail to activate, but more are separated from their antennas or
buried. Activating while still airborne also gets the signal out from altitude.

<!-- TODO: Switch positions and cockpit annunciation (ON / RESET / armed indication); location on the panel -->

### The ELT Is GPS-Aided — Wiring

**Confirmed from the SteinAir SkyView interconnect** (`SV_Interconnect.pdf`, read
off the drawing, 2026-09-14):

| From | To | Wire |
|---|---|---|
| GTN 650 **P1003 pin 6 — GPS RS-232 Out 3** | **ELT DB15 pin 9 — Serial GPS Data In** | Wht |

So the 406 MHz burst carries a GPS position rather than relying on Doppler
resolution alone. That is worth more than it sounds: in the Embry-Riddle data
cited by PilotWorkshops, mean search duration was **11.8 hours** for a 406 ELT
without GPS aiding against **two hours** with it.

Rest of the ELT DB15, same drawing:

| Pin | Function | Wire |
|---|---|---|
| 3 | 2-Wire Remote Switch | Wht/Blu |
| 9 | Serial GPS Data In | Wht |
| 14 | External On | Wht/Ora |
| 7 | Ground | — |
| 5, 12 | G-Switch Loop | — |
| 8 | Buzzer Power Out | → cabin buzzer |

The remote switch head wires to pins 3 and 14 (Wht/Blu and Wht/Ora).

**Consequence for the position feed:** the GPS data comes from the *GTN*, not from
the ELT's own receiver, so it is only as good as the GTN's power and lock. In a
total electrical failure the ELT still transmits on its internal battery, but
without a live feed the position reverts to whatever it last had. One more reason
the forced-landing checklists activate it **early**, while the panel is still up.

<!-- TODO: Confirm the GTN's RS-232 Out 3 format setting matches what the ELT 345 expects (Artex wants NMEA 0183 / aviation format — verify in the GTN serial-port config page, not just the wiring). -->

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
- [Bob Archer — Wing Tip vs More Common Types of VOR Antennas](http://www.aeroelectric.com/Reference_Docs/Antenna/Bob_Archer/VOR%20Antennas.pdf)
- [AeroElectric Connection Fig. 13-12 — wingtip VOR antenna drawing](https://vansairforce.net/attachments/screenshot-2026-04-11-at-7-24-31%E2%80%AFpm-png.114848/) (dimensions transcribed in `plans/vor-antenna-diagnostic.md`)
- [Archer glideslope add-on — dimensioned PDF](https://vansairforce.net/attachments/archer_gs_mod-pdf.114327/) and [Onshape CAD](https://cad.onshape.com/documents/cbff8ca0fee54b2b954db6af/w/f5ebbd2c43a1e3515aac7cb1/e/1e61d8094a13d9be680380f5)
- [Bob Archer Antenna Installation Instructions](https://drive.google.com/file/d/1tpQ1PFsuzGcuJrZAru651fHs_7vxFHb9/view)
- [Garmin GA 35 Installation Instructions (Rev F)](https://static.garmin.com/pumac/190-00848-00_f.pdf)
- [Garmin GA 35 Product Page](https://www.garmin.com/en-US/p/6573/)
- [Dynon SV-GPS-250/A Product Page](https://dynonavionics.com/gps-receiver-module.php)
- [Dynon SkyView System Installation Guide](https://www.dynonavionics.com/includes/guides/skyview/SkyView_System_Installation_Guide-Rev_AT.pdf)
- [ACR Artex 110-773 Whip Antenna](https://www.acrartex.com/products/110-773-whip-antenna-dual-band/)
- [Artex ELT 345 Manual](https://www.acrartex.com/wp-content/uploads/downloads/1861/ELT_345_Manual_Y1-03-0282P.pdf)
