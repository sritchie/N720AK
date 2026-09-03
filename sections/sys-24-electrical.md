# Electrical Power

> ATA Chapter 24 — N720AK Systems Reference

## Overview

N720AK's electrical system uses a dual-bus architecture managed by the **flyEFII System32 Bus Manager**. Power distribution and electronic circuit breaker protection are provided by the **Vertical Power VPX Sport**. Two **EarthX ETX900** lithium batteries provide redundant power with fully isolated charging systems: a **60-amp primary alternator** charges Battery 1, and a **Monkworkz MZ-30 generator** charges Battery 2.

## Components

| Component | Part Number | Supplier | Notes |
|-----------|-------------|----------|-------|
| Bus Manager | System32 | flyEFII | Controls essential vs main bus — [manual](https://drive.google.com/file/d/15OSKV66Y01w9-h93sxs9tNDaLjTv4gw_/view) |
| Power distribution | VPX Sport | Vertical Power | Electronic breakers — [manual (Rev G4)](https://drive.google.com/file/d/1fx7BQxzuy7GF-xIyuE83zK8BoZ-B0Vz2/view) |
| Battery 1 | [ETX900](https://drive.google.com/file/d/1ZESKGgF3pW5eckKshcZ608nd0RrMmGhE/view) | EarthX | Charged by primary alternator |
| Battery 2 | [ETX900](https://drive.google.com/file/d/1ZESKGgF3pW5eckKshcZ608nd0RrMmGhE/view) | EarthX | Charged by Monkworkz generator |
| Primary Alternator | [AL 12-E160/V](https://drive.google.com/file/d/1ohXkwRfkTZLX-q9fKeWIxboXz9dUrY12/view) (P/N 99-9900) | Hartzell | 60A. Belt: 13355 Dayco / 7355L Gates V-belt |
| Generator | [MZ-30](https://monkworkz.com/product/mz-30/) | Monkworkz | Mounted on engine vacuum pad |
| MZ Regulator | (included with MZ-30) | Monkworkz | Mounted on engine mount |
| Generator relay | BOSCH 0332019155 | Bosch | NO relay, 30A, 12V, internal diode |
| Master switch | <!-- TODO --> | <!-- TODO --> | Keyed |

## How It Works

### Bus Architecture

- **Essential (Endurance) Bus**: Powers critical engine systems — ignition, fuel injection, fuel pumps. Managed by System32 Bus Manager. **Protected by conventional physical circuit breakers, one per item** — these are *not* VPX channels.
- **Main Bus**: Powers avionics and other aircraft systems via VPX Sport electronic breakers.

> **The only physical breakers in this airplane are on the essential bus bar.** Most feed the things that keep the engine running — that is the inverse of a conventional airplane, where the pullable breakers are avionics and the engine needs no electrical power at all. Anyone reaching for a breaker panel out of habit may be reaching for ignition, fuel injection, and the fuel pumps. Brief this before engine start. See `sections/sys-73-efii.md` for why the engine stops without them.

#### Essential Bus Bar Breakers

Per the SteinAir power & lighting schematic (verified 2026-08):

| Breaker | Amps | Feeds |
|---------|------|-------|
| ALT FLD | 5 | Alternator field (via panel switch) |
| ECU PRI | 5 | Primary ECU (via IGN 1 toggle) |
| ECU SEC | 5 | Secondary ECU (via IGN 2 toggle) |
| PUMP 1 | 10 | Fuel pump 1 |
| PUMP 2 | 10 | Fuel pump 2 |
| IGN PWR | 15 | Ignition coils |
| PFD | 5 | SV-HDX1100 PFD1 (D37-1/20) |
| COM 1 | 10 | GTN 650 com board (P1003-30/43/44, via COM relay) |
| NAV 1 | 7.5 | GTN 650 GPS/main + VLOC boards (P1001-19/20, P1004-51/52, via NAV relay) |
| PNL LTS | 5 | Panel lighting |
| SERVOS | — | Autopilot servos |

**COM 1 / NAV 1 split**: pulling COM 1 kills only the GTN's com transceiver (stuck-mic response — screen, GPS, and VLOC keep running). Pulling NAV 1 kills the GTN main and VLOC boards; the com board keeps operating on its last frequency with no display or tuning.

**Known issue (fix planned at annual)**: the GTN's COM/NAV power relays are held closed by the AV MSTR switch from a *main-bus* feed — so any main-bus loss opens them and the GTN goes dark despite its essential-bus breakers being hot. Planned fix: re-source the relay coil feed from the essential bus. The transponder/ADS-B (VPX J10-7) and GMA 245/headset power (VPX J10-4) also die with the main bus; planned fixes are an essential dual-feed and a dedicated essential breaker respectively.

### Display Backup Power — Deliberately Not Installed

Dynon's **SV-BAT-320 backup batteries are not part of this system**, by choice. With the System32 Bus Manager arbitrating two independent EarthX ETX900 batteries on fully isolated charging systems, bus current stays stable through a single charging-source or battery failure, so the per-display backup batteries solve a problem this architecture does not have. This matches what RV builders running the Bus Manager with dual batteries have generally concluded.

Consequence worth knowing: there is no display-level power reserve. Display availability depends entirely on the bus, which is what the dual-battery and dual-charging architecture exists to protect.

### How the Bus Manager Actually Works

Verified against Bus Manager Drawing 5/5A (2026-08). Three facts define the architecture:

1. **The key drives the Main Bus Relay** (the only control of the main bus) and, cascaded from it, the Essential Bus Relay. The IGN 1 / IGN 2 panel toggles — not the key — are the ECU enables, sitting between the ECU breakers and the ECUs.
2. **The essential bus is continuously diode-OR fed from both batteries.** There is no switching logic — the essential bus passively draws from whichever battery node is higher, and when the nodes are close (alternator ~14.3 V, MZ-30 ~14.2 V) both sources share load through their diodes. This is normal and by design. Diode paths drop ~0.5–0.7 V below battery voltage under load. Charge isolation is separate and intact: the alternator cannot charge Battery 2 and the generator cannot charge Battery 1.
3. **The EMERGENCY POWER switch is a hard jumper** from the both-battery diode node directly to the essential bus output, bypassing the key, both relays, and all Bus Manager logic. It exists for Bus-Manager-internal failure; flipping it in normal flight changes nothing observable (it arms a parallel path). The Bus Manager does *not* automatically shed loads — the "automatic" protection is purely the passive diode-OR.

**In-flight main-bus shed maneuver**: E-PWR ON → *verify essential bus voltage* → KEY OFF. The engine keeps running (ECUs fed from the essential bus through the IGN toggles), the main bus and everything on the VPX goes dark, and both charging sources keep working. **Order is critical** — key-off with E-PWR off (or failed) stops the engine. Note the interaction with the engine-fire procedure: "Key OFF" only stops the engine while E-PWR is off. Main-bus loss also kills flaps, electric trim (AP panel), and pitot heat; the AP servos are essential-fed and the autopilot remains flyable from PFD1 minus auto-trim.

**Endurance bus radio behavior**: The GTN 650 is COM1. If power goes out on the GMA 245, it hard-connects COM1 from the GTN 650 directly to the headphones. This ensures radio communication is maintained even if the audio panel loses power on the endurance bus.

### VPX Sport

The VPX Sport provides:
- Electronic circuit breaker protection for **main bus loads** — these channels have no physical breakers to pull or reset; they are reset from the EFIS. (The endurance bus is separate and *does* use physical breakers — see Bus Architecture above.)
- Load monitoring and display on EFIS
- Automatic load shedding if needed
- Programmable power channels

<!-- TODO: VPX channel assignments — what's on each channel? -->
<!-- TODO: How are the buses connected? What's the bus tie arrangement? -->
<!-- TODO: Alternator field control — how does it work? -->

### Fuses (Non-VPX)

Discrete fuses outside the VPX electronic breaker system, located above the essential bus bar behind the pilot PFD:

| Circuit | Fuse | Location |
|---------|------|----------|
| Front USB-C charger | 5A | Above essential bus bar, behind pilot PFD |
| OnSpeed AOA | 1A | Labeled fuse holder, above essential bus bar |
| SwitcheOn 2/15A | 15A (Littelfuse 0456015.DR, 456 series, 125V, 10.1 × 3.05 mm SMD) | Soldered on SwitcheOn board — requires desoldering to replace |

### Monkworkz MZ-30 Generator

Installed 2026-03-09. The MZ-30 is a permanent-magnet generator driven off the engine's vacuum pump pad, providing independent charging for Battery 2. Manual version 4, dated 2024-10-22.

#### Specifications

| Parameter | Value |
|-----------|-------|
| Output voltage | ~14.4 VDC (configurable: 14.6 or 14.2 VDC) |
| Max current | 30 amps (at ≥1800 RPM tach speed) |
| Current at idle | 15 amps (at 900–1000 RPM tach speed) |
| RPM limit | 3572 crankshaft RPM (4600 generator RPM) |
| Vacuum pad ratio | 1.3:1 (Lycoming) |
| Generator weight | 2 lbs 1 oz |
| Regulator weight | 8.2 oz |
| Combined weight | ~2.6 lbs |
| Environmental | Tested to 115°F ambient |

**Voltage selection**: Ships configured for 14.6 VDC. For lithium batteries (EarthX), the lower 14.2 VDC setting is recommended per Monkworkz Feb 2026 guidance. To select 14.2V, disconnect pin 1 (VSEL) on the input side Pico-Lock connector. Voltage is set at startup and cannot be changed while running.

**N720AK is confirmed on the 14.2 V setting** — flight data (2026-06 and 2026-08 logs) shows the Battery 2 node regulating at 14.20 V against the alternator's 14.30 V. This is exactly Monkworkz's recommended standby-generator geometry (primary slightly above the MZ).

#### Standby Behavior — Read This Before Toggling the Enable Switch In Flight

Per the manual (v4, Operation, p. 21), the regulator produces output only when **the attached bus voltage is below 13.7 V** (in addition to RPM/temperature limits). Consequences observed in flight (2026-08-31):

- **Toggling enable OFF then ON in flight does not bring the generator back** while the alternator is healthy — Battery 2's surface charge holds the node above 13.7 V, so the regulator sits in standby, possibly for the rest of the flight. It re-engages on its own after landing as the node sags. This is designed standby-generator behavior, not a fault.
- **The functional test of the MZ-30 is turning the alternator field OFF** (briefly): the bus sags, the MZ engages within seconds, ALT back on. Toggling the MZ's own switch proves nothing.
- **Load sharing is normal**: with the nodes 0.1 V apart, cruise logs show the MZ contributing ~6 A (peaks ~18 A) alongside the alternator's ~23 A through the essential-bus diode-OR. This is supply-sharing into the essential bus, not a charge-isolation failure.

#### Architecture

The two battery charging systems are **fully isolated**:

| System | Charges | Source |
|--------|---------|--------|
| Primary alternator (60A) | Battery 1 | Belt-driven |
| Monkworkz MZ-30 | Battery 2 | Engine vacuum pad |

The bus manager's internal screw that previously allowed the primary alternator to cross-charge Battery 2 has been removed. Each battery has a dedicated charging source.

#### Generator → Battery 2 Wiring

The generator output connects to the Battery 2 stud inside the bus manager (Drawing 5A, bus manager installation guide page 13). A **BOSCH 0332019155 normally-open relay** (30A, 12V, internal diode) sits between the generator output and Battery 2 to prevent parasitic draw when the engine is off.

**Relay coil power**: Essential bus + generator enable switch. This design means:

- Turning off the ignition key de-energizes the essential bus, opening the relay and disconnecting the generator from Battery 2 — regardless of enable switch position
- The enable switch provides pilot control to disable the generator in flight
- The generator cannot turn itself on (unlike the Monkworkz reference diagram which powers the relay from the generator output)

**Note**: The manual recommends connecting to the switched side of the master contactor to avoid parasitic draw from the regulator's ~30mA diagnostic blink code circuit. The BOSCH relay achieves the same purpose.

#### MZ Regulator Connections

The MZ regulator is mounted on the engine mount with the following connections:

**Generator side** (3-phase, #6 screw terminals, 12 AWG):
- Terminal 7 (~1), Terminal 8 (~2), Terminal 9 (~3) → MZ Generator (phases can be connected in any order)

**Input Molex Pico-Lock** (pre-wired, 22-24 AWG):
- Pin 1: Voltage_Select (connected = 14.6V, disconnected = 14.2V)
- Pin 5: GEN_Thermistor → Generator thermistor (required — system will not produce output without it)
- Pin 6: GND

**Output Molex Pico-Lock** (22-24 AWG):
- Pin 1: Enable → Pilot enable switch (pin 1 to switch center, pin 6 to switch N.O.)
- Pin 2: Output_Active — pulls to ground when regulator is active and maintaining ≥14V (works with Dynon/Garmin EFIS contact inputs). **Orange/brown wire, currently coiled up and unused near the Monkworkz enable switch.**
- Pin 3: +i_Shunt (internal fuse used as shunt, 1.1 mΩ nominal)
- Pin 4: −i_Shunt
- Pin 5: Proportional_Current → Dynon EMS pin 31 (0–~2.7V = 0–30A, brown/blue wire)
- Pin 6: GND

**Power output** (#6 screw terminals, 10 AWG Tefzel):
- Terminal 17: Output_Power_Positive → BOSCH relay → Battery 2 stud (bus manager)
- Terminal 18: Output_Power_Ground (to clean metal airframe ground, no paint/corrosion)

**Caution**: The Pico-Lock connectors are delicate — add ~0.5" maintenance loops in the connector wires, secured to nearby 12/10 AWG wires with a small pre-load toward the connector to prevent unseating.

#### Cooling

Both generator and regulator require cooling via 3/4" holes in the engine baffling with corrugated nylon tubing routed from the baffling. The duct material is a force fit into the generator, regulator, and baffling holes. RTV can improve the seal.

<!-- TODO: Confirm cooling ducts are installed and routed for both generator and regulator -->

#### Generator Enable Switch

Panel-mounted next to the primary alternator field switch. Controls the relay coil circuit (essential bus → enable switch → relay coil → ground).

The enable switch wiring connects pin 1 (Enable) to the switch center post and pin 6 (GND) to the switch's normally-open terminal, grounded at the regulator end (not at the panel — grounding at the panel can cause ground loops and erratic behavior per manual section 2.1).

#### Startup Behavior

After engine start, when RPM exceeds ~1200, the MZ-30 performs an internal self-test (2–4 seconds). If all checks pass, it begins providing output voltage. The enable switch can be set ON as part of the pre-start checklist or activated at idle.

#### Protection Features

- **Overvoltage Protection (OVP)**: Shuts down output in <1 second if overvoltage detected. If OVP triggers 3 times in one flight, system shuts down for the remainder of that flight. If this occurs across 3 separate flights (9 total OVP events), the regulator requires service/replacement from Monkworkz.
- **Thermal protection**: Two-stage — first reduces to half current limit, then full shutdown if temperature continues rising. Recovers automatically when temperature drops below recovery threshold.
- **Current limiting**: Electronic current limiting at 30A. Output fuse is internally replaceable by a repair shop only.
- **Shear coupling**: Located between input spline and motor shaft. Breaks if vacuum drive torque is exceeded — contact Monkworkz for replacement if generator rotates freely.

#### Regulator Blink Codes

The regulator has a diagnostic LED on the output side:

| Flashes/sec | Meaning |
|-------------|---------|
| 1 | Thermistor disconnected (check connection, should read ~100kΩ) |
| 2 | Overvoltage lockout (9 total OVP events across 3 flights — return to Monkworkz) |
| 3 | Disabled (enable pin not grounded — enable switch is off) |
| 4 | Enabled (enable pin grounded — enable switch is on, normal operation) |
| 5 | Thermistor shorted or over-temperature |

The Output Active pin (pin 2) also provides status: it "flashes" on an 8-second cycle (4s ground, 4s open) if the generator is overheating, providing an in-cockpit indication.

#### Dynon EMS Monitoring

The MZ-30's proportional current output (pin 5, 0–~2.7V = 0–30A) is wired to Dynon EMS pin 31. This pin previously carried the **CO Guardian PPM signal** to the Dynon EMS — only the *EMS display* was removed when the wire was repurposed. The CO Guardian unit remains installed in the cabin and still provides an audible alarm above 50 PPM. The alarm is not currently wired into the GMA 245 audio panel, so it sounds in the cabin but is not heard through the headsets.

<!-- TODO: Configure Dynon sensor definition for generator amps — see https://vansairforce.net/threads/monkworkz-wiring-for-amps-readout.224156/post-1912075 -->
<!-- TODO: Wire CO Guardian audible alarm into the GMA 245 audio panel so it's heard through the headsets -->
<!-- TODO: Consider an alternative path for CO PPM display on the EFIS (standalone CO monitor or additional EMS module) -->
<!-- TODO: Wire Output Active (pin 2, orange/brown wire coiled near the enable switch) to a Dynon contact input for GEN ACTIVE/STANDBY annunciation. EMS pins are full — use a SkyView DISPLAY D37 contact input instead (pins 28/27/14/15 = Contacts 1-4 on each display harness, unused per the interconnect schematic). Pin 2 pulls to ground when the regulator is producing (post-June-2022 units), which matches Dynon contact-input expectations. -->

#### References

- [Monkworkz MZ-30 product page](https://monkworkz.com/product/mz-30/)
- [MZ-30 Installation and Operation Manual V4 (2024-10-22)](https://drive.google.com/file/d/1gYvTgAvxHc0wkgVv_7ftHDwXXgPplmXw/view)
- [VAF: Monkworkz Wiring for Amps Readout](https://vansairforce.net/threads/monkworkz-wiring-for-amps-readout.224156/post-1912075)
- Bus Manager Installation Guide, Drawing 5A (page 13)

## Wiring

> **KiCad migration**: All connector pinouts and wiring data below should eventually be ported to proper KiCad schematics. The text tables here are transcribed from build notes and serve as the interim reference.

### Wiring Stations (Station-by-Station Topology)

Complete wiring map of the aircraft, from tail to firewall.

#### Rear Tailcone

- ELT
- SunTail (rear position/strobe)
- Elevator trim servo

#### Tailcone / Baggage Area Junction (RIGHT)

- Elevator autopilot servo
- ADSB
- Net hub
- Battery 1 positive (large gauge)
- Battery 2 positive (large gauge)
- Main battery negative (large gauge)

#### Tailcone / Baggage Area Junction (LEFT)

- Alt static line from panel
- EFIS hub connection
- Starter solenoid 1 drive
- Starter solenoid 2 drive
- Starter annunciator wire
- Emergency air override (yellow and red lines)
- O₂ supply and pressure lines (blue and red)
- Oxygen wiring harness
- Pitot air hose (blue)
- AoA hose (green)

#### Passenger Area (LEFT)

- O₂ lines (blue and red)
- Left passenger O₂ harness
- Left door ajar sensor
- Power wire for left door ajar servos

#### Passenger Area (RIGHT)

- O₂ lines (blue and red)
- Right passenger O₂ harness
- Right door ajar sensor
- Power wire for right door ajar servos

#### Left → Center Tunnel

- Flap position sensor harness
- Flap motor wires

#### Wing Connection Area (LEFT)

- Pitot heat power and ground (14 AWG)
- Heated pitot status wire
- Fuel level sensor left
- AoA air hose (green)
- Pitot air hose (blue)
- 2× shielded 3-wire bundles for left lights
- Green sync wire for left lights
- 5-wire trim bundle for left roll trim

#### Wing Connection Area (RIGHT)

- AP splice for red, black, yellow — 3-way (rear, connector, front)
- AP bundle extension from connector
- 2× shielded 3-wire bundles for right lights
- Green sync wire for right lights
- Right wing COM antenna coax from panel (inline connector)
- Right wing NAV antenna coax from panel (inline connector)

#### Gear Support Mount (LEFT) — Under-Seat Terminal Blocks

- EMS ground for trim servo sensors
- Pitch trim motor power and ground
- Roll trim motor power and ground
- Roll trim position sensor
- Pitch trim position sensor
- Trim bundle from left wing
- 5V (red/white) EMS power for trim servo sensors

#### Gear Support Mount (RIGHT) — Under-Seat Terminal Blocks

- Green sync wire for lights
- Wig-wag power
- Nav power
- Strobe power
- Taxi power
- Landing power
- Tail light bundle from rear
- 16 AWG ground wire for lights
- AP servo black, red, yellow spliced together
- 2× 3-wire light bundles + green sync crossing to left wing root
- 2× 3-wire light bundles + green sync from right wing root

#### Forward Center Tunnel

- 2× red power wires for fuel pumps
- Ground wire for fuel pumps (1 wire spliced to 2)

#### Control Sticks (LEFT and RIGHT)

- Main bundle from SteinAir panel harness
- COM flip sensor wire

#### Pilot Knee Side (LEFT)

- O₂ pilot wiring harness
- O₂ lines (blue and red)

#### Copilot Knee Side (RIGHT)

- O₂ copilot wiring harness
- O₂ lines (blue and red)

#### Left Firewall Penetration — Engine Sensors

- CHT wires × 6
- EGT wires × 6
- Fuel pressure ground and data
- Oil pressure ground and data
- Oil temp ground and data
- Spliced 5V wire (red/white) for fuel pressure, oil pressure, oil temp sensors

#### Right Firewall Penetration — EFII / Power

- 60A fuse → bus manager
- Ammeter shunt wires
- Spark plug wires for EFII
- Ignition coil wires (71 and 88)
- Pressure sensor wires
- All remaining EFII outputs

### Terminal Blocks Under Seats

Two terminal blocks located under the front seats distribute wiring between the wing roots, center tunnel, and panel.

#### Left Terminal Block

| Position | Function |
|----------|----------|
| 1 | EMS ground, trim servos |
| 2 | EMS power, trim servos |
| 3 | Roll trim position |
| 4 | Pitch trim position |
| 5 | Roll trim motor 1 L |
| 6 | Roll trim motor 1 R |
| 7 | Pitch trim motor 2 L |
| 8 | Pitch trim motor 2 R |

#### Right Terminal Block

| Position | Function |
|----------|----------|
| 1 | Ground (house, L side) |
| 2 | Ground (R side, empty) |
| 3 | Sync wire for AeroSun VX (green, one from R, one from L) |
| 4 | Taxi power |
| 5 | Wig-wag power |
| 6 | Landing power |
| 7 | Sync wire for Pulsar/SunTail |
| 8 | Strobe power |
| 9 | Nav power |

### Wing Root Connectors (CPC)

CPC barrel connectors (series 1, 17–18 pin) at each wing root carry all wing wiring.

<!-- TODO: CPC connector manufacturer part numbers (shell, pins, strain relief, heat shrink boots) -->
<!-- TODO: CPC pin type and gauge rating (16 AWG? 20 AWG?) -->
<!-- TODO: CPC crimp tool used -->
<!-- TODO: Mating connector orientation — keying/polarization -->

#### Right Wing Root Exit

| Pin | Function | Wire Color |
|-----|----------|------------|
| 1 | AeroSun VX | Orange |
| 2 | AeroSun VX | Blue |
| 3 | AeroSun VX | White |
| 4 | AeroSun VX shield | Black |
| 5 | Pulsar | Orange |
| 6 | Pulsar | Blue |
| 7 | Pulsar | White |
| 8 | AeroSun VX sync | Green |
| 9 | Autopilot servo | Red |
| 10 | Autopilot servo | Black |
| 11 | Autopilot servo | Yellow |
| 12 | Pulsar shield | Black |
| 13 | Autopilot servo | Green |
| 14 | Autopilot servo | Blue |
| 15 | Autopilot servo | White/green |
| 16 | Autopilot servo | White/blue |
| 17 | Fuel level sensor | — |

#### Left Wing Root Exit

| Pin | Function | Wire Color |
|-----|----------|------------|
| 1 | AeroSun VX | Orange |
| 2 | AeroSun VX shield | Black |
| 3 | Pulsar | Orange |
| 4 | AeroSun VX | Blue |
| 5 | Pulsar | Blue |
| 6 | Pulsar | White |
| 7 | Pulsar shield | Black |
| 8 | AeroSun VX | White |
| 9 | AeroSun VX sync | Green |
| 10 | Trim | Orange |
| 11 | Trim | Blue |
| 12 | Trim | Green |
| 13 | Trim | White |
| 14 | Trim | White |
| 15 | Pitot heater | Red |
| 16 | Pitot heater | Black |
| 17 | Fuel level sensor | — |
| 18 | Pitot heater status | Brown/blue |

### Autopilot Servo Wiring (Wing)

Wire color mapping between the wing harness and the Dynon roll/pitch servo connector.

| Harness Color | Servo Color | Function |
|---------------|-------------|----------|
| Red | Red | Power |
| Black | Black | Ground |
| Orange | Green | — |
| Blue | Blue | — |
| Yellow | Yellow | — |
| White | White/green | — |
| White/black | White/blue | — |

### Dynon EMS-220 Connector (37-Pin)

Complete pinout for the SV-EMS-220 engine monitoring module. Updated 2026-03-04.

#### Through Firewall

| Pin | Function | Wire Color |
|-----|----------|------------|
| 3 | Ground (oil pressure) | Black |
| 5 | Ground (oil temp) | Black |
| 6 | Oil pressure sensor | White/yellow |
| 7 | Oil temp sensor | White/brown |
| 8 | Fuel pressure sensor | Brown |
| 16 | Ground (fuel pressure) | Black (twisted) |

#### Across Panel

| Pin | Function | Wire Color |
|-----|----------|------------|
| 1 | Main battery voltage | Red |
| 2 | Secondary battery voltage | Yellow/green |
| 12 | Door ajar right | Yellow (untwisted) |
| 13 | Ground (fuel flow) | Black (twisted) |
| 14 | Fuel flow | Yellow (twisted) |
| 15 | 12V power for fuel flow interface | Red (twisted) |
| 17 | Ground (MAP sensor) | Black |
| 21 | Fuel level right | Orange/blue |
| 24 | Ammeter shunt + | Orange/green (twisted) |
| 25 | Ammeter shunt − | Orange/violet (twisted) |
| 26 | MAP sensor input | Green/red |
| 34 | Low voltage RPM input left | Blue (twisted) |
| 35 | Low voltage RPM input right | Green (twisted) |

#### Down Left (Under Panel)

| Pin | Function | Wire Color |
|-----|----------|------------|
| 4 | Elevator trim position | Violet/blue |
| 9 | Heated pitot status | Brown/blue |
| 10 | Roll trim position | Brown/yellow |
| 11 | Door ajar left | Orange (twisted) |
| 20 | Fuel level left | Orange/brown |
| 22 | Battery fault 1 | Violet/yellow |
| 23 | Battery fault 2 | Violet/green |
| 30 | Ground (roll trim, elevator trim) | Black |

#### Shared Power

| Pin | Function | Wire Color |
|-----|----------|------------|
| 18 | 5V power (shared: fuel flow sensor, elevator trim, roll trim, fuel pressure, oil pressure, oil temp, MAP sensor) | White/red |

#### Unused Pins

| Pin | Dynon Function | Notes |
|-----|----------------|-------|
| 19 | Fuel flow return (type F) | Not used |
| 27 | General thermocouple 1+ | Not used |
| 28 | General thermocouple 1− | Not used |
| 29 | Warning light output | Not used |
| 31 | Monkworkz MZ-30 proportional current (was CO Guardian PPM input) | Brown/blue — 0–2.7V proportional to 0–30A generator output. Sensor definition not yet configured in Dynon. **CO Guardian unit itself is still installed in the cabin and provides an audible alarm above 50 PPM**; only the Dynon EMS PPM display was removed. The audible alarm is currently not wired into the audio panel — it sounds in the cabin but is not heard through the headsets. |
| 32 | RPM input left (high voltage) | Not used (using pin 34 low voltage) |
| 33 | RPM input right (high voltage) | Not used (using pin 35 low voltage) |
| 36 | General thermocouple 2+ | Not used |
| 37 | General thermocouple 2− | Not used |

### Panel Mounting Fasteners

Screw/bolt specs for every panel-mounted component. Useful reference for panel removal and reinstallation.

| Component | Fastener | Qty | Notes |
|-----------|----------|-----|-------|
| Dynon SkyView HDX | AN525-832R14 or R16 | 2 | Shunt mounting |
| EMS-220 | MS35207-10R7 | 4 | |
| GTN 650 | — | — | <!-- TODO: verify --> |
| GMA 245 | — | — | <!-- TODO: verify --> |
| COM-425 | AN515-8R7 | 4 | |
| VPX Sport | AN515-8R7 or 8R8 | 6 | |
| ECU (EFII) | AN4-16 or AN4-17 | 4 | Into nutplates |
| ECU/VPX mounting rails | AN3-3A | 7 | |
| Ethernet hub | AN525-832R7 | 4 | |
| Dynon transponder | AN525-832R7 | 3 | |
| Bus manager (wall) | MS35207-10R6 | 4 | |
| Bus manager (internal) | MS35207-10R10 | 4 | Plus nuts and washers |
| SkyView network hub | AN515-6R12 | 4 | |
| ADS-B mount | AN515-6R7 | 4 | |
| Fans | MS24694-S19-8R22 | 8 | Plus washers, nuts for #8 |
| Ignition coil Adel clamps | AN3-5 or AN3-6 | 2 | Plus long standoff bolt AN3-21/22 |
| Fuel valve (Andair) | AN3-5 | 4 | Plus AN3-10L × 4, washers × 4, nuts |
| Starter contactors | AN4-4A or AN4-5A | — | Plus 960-416 washers |
| ASA oil separator | AN4-5 length | — | 2× AN4 washers, nutplate |
| Automotive fuel valve | AN3-3A or AN3-4A | — | Plus 2× AN960-10 washers |
| Alt fuse block | AN509-10R11 or 10R12 | — | |
| Firewall penetrations | AN515-6R4 | — | |
| COM/wing antennae | AN509-8R8 or 8R9 | 8 | Nutplates |
| POS-12 sensor | NAS1352-04-4P | — | 1/4″ and 3/8″, plus 2× AN365-440 |
| AHRS | MS35214-40 (brass) | — | Brass nyloc nuts, brass washers |
| Grounding block | 5/16″ bolt | 1 | Plus washer and nyloc |
| MAP sensors | AN3-11A | — | All MAP sensors |

### Connector Inventory

Summary of all connector types used in N720AK wiring (all installed).

<!-- TODO: Add manufacturer part numbers for all CPC connectors (series 1 and 2), including shell, pins, boots, and strain relief -->
<!-- TODO: Add CPC series 2 bulkhead mount part numbers for autopilot servos -->

| Type | Quantity | Location | Purpose |
|------|----------|----------|---------|
| CPC series 1, 17–18 pin | 2 | Wing roots (L/R) | Wing exit barrels |
| CPC series 1, 9 pin | 2 | Wingtips (L/R) | Wingtip light connections |
| CPC series 2 | 2 | Autopilot servos | Bulkhead mount |
| DSUB 9-pin female | 8 | Various | 5× O₂ connectors, PFD→hub, AHRS fork, ADSB-472 |
| DSUB 11-pin HD | 2 pairs (M/F) | Under seats | Stick grips (22 AWG) |
| DSUB 15-pin female | 1 | Tailcone rear | Solder pins |
| Molex Micro-Fit 6-pin | 1 | Panel | Fuel air monitor |
| Molex Micro-Fit 3-pin | 1 | Panel | Pitot heat controller (22 AWG status, 14 AWG power) |
| Molex 5-pin (11-4) | 1 | Tailcone rear | Tail light connection |
| Molex 2-pin (OAT probe) | — | — | P/N 43645-0200, pins P/N 43030-0007 |
| 1-pin blade connector | 2 | Tailcone front | Battery status wires |
| 2-pin connectors | 3 | Panel area | LED strip, 2× fans |

<!-- TODO: Bus diagram — essential bus, main bus, VPX channels, battery connections -->
<!-- TODO: Wire gauges for main power runs -->
<!-- TODO: Grounding scheme -->

## Inspection & Maintenance

### EarthX Battery & Chargers

#### Chargers

| Charger | Model | Use |
|---------|-------|-----|
| [OptiMate Lithium 4s 5A](https://optimate1.com/product/optimate-lithium-4s-5a/) | TM-291 | 5A charger/maintainer for LiFePO4 (3–100 Ah). 10-step charging, BMS wake-up mode. 100–240V AC input. |
| [OptiMate TM-275 v2](https://earthxbatteries.com/product/tm-275-13-2v-10-amp-lithium-lifep04-battery-charger-maintainer-power-supply/) | TM-275 v2 | 9.5A charger/maintainer/power supply for LiFePO4 (2.5–120 Ah). Doubles as 8A @ 13.6V bench power supply (TUNE mode) for avionics configuration without battery drain. |

#### Charger Behavior Notes

The OptiMate chargers enter sleep/maintenance mode once the battery is fully charged, checking voltage roughly once per hour. **Important**: If a continuous parasitic load is present (e.g. panel powered on for configuration), the charger may not detect the drain during its sleep intervals and the battery can discharge. This caused a drain-to-zero event during initial setup. The TM-275's TUNE mode (continuous 13.6V power supply) avoids this problem. (Per EarthX Engineering, Dillon Hinners, 2026-01-13.)
### Hartzell Alternator Maintenance

Per the [AL 12-E160/V installation manual](https://drive.google.com/file/d/1ohXkwRfkTZLX-q9fKeWIxboXz9dUrY12/view): battery terminal torque 50 in-lb, safety wire .032. Annual: check bearings. 5yr/1000hr: inspect brushes (replace if <0.250" from holder case edge). 5A enable CB, 60A main breaker.

<!-- TODO: Battery maintenance — EarthX specific procedures, voltage checks, balancing -->
<!-- TODO: Alternator belt inspection, tension -->
<!-- TODO: VPX diagnostics — how to read the log, what to look for -->

## References

- [VPX Sport Installation & Operating Manual (Rev G4)](https://drive.google.com/file/d/1fx7BQxzuy7GF-xIyuE83zK8BoZ-B0Vz2/view)
- [VPX Sport Installation & Operating Manual (Rev G3)](https://drive.google.com/file/d/1hQrYbSkh8DvIVArft79wGad22Tb3wq02/view) — previous revision
- [VPX Getting Started Guide (Rev A)](https://drive.google.com/file/d/1qcHnGA1dfkLlPURjJJ1jw2lAcXntpvlV/view)
- [EFII Bus Manager Installation Instructions](https://drive.google.com/file/d/15OSKV66Y01w9-h93sxs9tNDaLjTv4gw_/view)
- [EarthX ETX900 Installation & Maintenance Manual](https://drive.google.com/file/d/1ZESKGgF3pW5eckKshcZ608nd0RrMmGhE/view)
- [Hartzell AL 12-E160/V Alternator Installation Manual (P/N 99-9900)](https://drive.google.com/file/d/1ohXkwRfkTZLX-q9fKeWIxboXz9dUrY12/view)
- [Power & Lighting Schematic](https://drive.google.com/file/d/1hXrVusmeaCbz3MywPmLUjcQ1TfPFVOE9/view)
- [VPX Pro/Sport Load Planning Worksheet](https://drive.google.com/file/d/1uy9UFDHQYeuw0kTXVAed_0YB3Jd1rMf1/view)
