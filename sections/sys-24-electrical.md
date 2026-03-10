# Electrical Power

> ATA Chapter 24 — N720AK Systems Reference

## Overview

N720AK's electrical system uses a dual-bus architecture managed by the **flyEFII System32 Bus Manager**. Power distribution and electronic circuit breaker protection are provided by the **Vertical Power VPX Sport**. Two **EarthX ETX900** lithium batteries provide redundant power with fully isolated charging systems: a **60-amp primary alternator** charges Battery 1, and a **Monkworkz MZ-30 generator** charges Battery 2.

## Components

| Component | Part Number | Supplier | Notes |
|-----------|-------------|----------|-------|
| Bus Manager | System32 | flyEFII | Controls essential vs main bus — [manual](https://drive.google.com/file/d/15OSKV66Y01w9-h93sxs9tNDaLjTv4gw_/view) |
| Power distribution | VPX Sport | Vertical Power | Electronic breakers — [manual](https://drive.google.com/file/d/1hQrYbSkh8DvIVArft79wGad22Tb3wq02/view) |
| Battery 1 | [ETX900](https://drive.google.com/file/d/1ZESKGgF3pW5eckKshcZ608nd0RrMmGhE/view) | EarthX | Charged by primary alternator |
| Battery 2 | [ETX900](https://drive.google.com/file/d/1ZESKGgF3pW5eckKshcZ608nd0RrMmGhE/view) | EarthX | Charged by Monkworkz generator |
| Primary Alternator | <!-- TODO: P/N --> | <!-- TODO --> | 60 amp, 14 volt |
| Generator | [MZ-30](https://monkworkz.com/product/mz-30/) | Monkworkz | Mounted on engine vacuum pad |
| MZ Regulator | (included with MZ-30) | Monkworkz | Mounted on engine mount |
| Generator relay | BOSCH 0332019155 | Bosch | NO relay, 30A, 12V, internal diode |
| Master switch | <!-- TODO --> | <!-- TODO --> | Keyed |

## How It Works

### Bus Architecture

- **Essential Bus**: Powers critical engine systems — ignition, fuel injection, fuel pumps. Managed by System32 Bus Manager.
- **Main Bus**: Powers avionics and other aircraft systems via VPX Sport electronic breakers.

### Emergency Endurance Bus

If a battery fails or bus voltage drops critically, the System32 Bus Manager automatically:

1. Disconnects non-essential loads from the main bus
2. Preserves all available power for the essential bus
3. Maintains engine ignition and fuel injection

The **EMERGENCY POWER** switch on the panel manually activates this mode.

**Endurance bus radio behavior**: The GTN 650 is COM1. If power goes out on the GMA 245, it hard-connects COM1 from the GTN 650 directly to the headphones. This ensures radio communication is maintained even if the audio panel loses power on the endurance bus.

### VPX Sport

The VPX Sport provides:
- Electronic circuit breaker protection (no physical breakers to reset)
- Load monitoring and display on EFIS
- Automatic load shedding if needed
- Programmable power channels

<!-- TODO: VPX channel assignments — what's on each channel? -->
<!-- TODO: How are the buses connected? What's the bus tie arrangement? -->
<!-- TODO: Alternator field control — how does it work? -->

### Monkworkz MZ-30 Generator

Installed 2026-03-09. The MZ-30 is a permanent-magnet generator mounted on the engine's vacuum pad, providing independent charging for Battery 2.

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

#### MZ Regulator Connections

The MZ regulator is mounted on the engine mount with the following connections:

**Generator side** (3-phase, #6 screw terminals, 14 AWG):
- Terminal 7 (~1), Terminal 8 (~2), Terminal 9 (~3) → MZ Generator

**Input Molex** (pre-wired, 22-24 AWG):
- Pin 6: GND
- Pin 5: GEN_Thermistor → Generator thermistor
- Pin 1: Voltage_Select

**Output Molex** (22-24 AWG):
- Pin 1: Enable → Pilot enable switch
- Pin 2: Active_High
- Pin 3: +i_Shunt
- Pin 4: −i_Shunt
- Pin 5: Proportional_Current → Dynon EMS pin 31 (0–2.8V, brown/blue wire)
- Pin 6: GND

**Power output** (#6 screw terminals, 10 AWG):
- Terminal 17: Output_Power_Positive → BOSCH relay → Battery 2 stud (bus manager)
- Terminal 18: Output_Power_Ground

#### Generator Enable Switch

Panel-mounted next to the primary alternator field switch. Controls the relay coil circuit (essential bus → enable switch → relay coil → ground).

#### Dynon EMS Monitoring

The MZ-30's proportional current output (pin 5, 0–2.8V) is wired to Dynon EMS pin 31 (previously CO Guardian). This replaces the CO detector wiring.

<!-- TODO: Configure Dynon sensor definition for generator amps — see https://vansairforce.net/threads/monkworkz-wiring-for-amps-readout.224156/post-1912075 -->
<!-- TODO: Reinstall CO detector on alternate Dynon EMS pin (27, 28, 36, or 37 available) or use standalone CO monitor -->

#### References

- [Monkworkz MZ-30 product page](https://monkworkz.com/product/mz-30/)
- MZ-30 Installation and Operation Manual — <!-- TODO: request updated manual from Bill at Monkworkz (aeroelectric.com version is for older MZ-30L) -->
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
| 31 | Monkworkz MZ-30 proportional current (was CO Guardian) | Brown/blue — 0–2.8V proportional to generator amps. Sensor definition not yet configured in Dynon. |
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

### EarthX Battery & OptiMate Charger Notes

The OptiMate charger enters sleep/maintenance mode once the battery is fully charged, checking voltage roughly once per hour. **Important**: If a continuous parasitic load is present (e.g. panel powered on for configuration), the charger may not detect the drain during its sleep intervals and the battery can discharge. This caused a drain-to-zero event during initial setup. (Per EarthX Engineering, Dillon Hinners, 2026-01-13.)

<!-- TODO: Battery maintenance — EarthX specific procedures, voltage checks, balancing -->
<!-- TODO: Alternator belt inspection, tension -->
<!-- TODO: VPX diagnostics — how to read the log, what to look for -->

## References

- [VPX Sport Installation & Operating Manual (Rev G3)](https://drive.google.com/file/d/1hQrYbSkh8DvIVArft79wGad22Tb3wq02/view)
- [VPX Getting Started Guide (Rev A)](https://drive.google.com/file/d/1qcHnGA1dfkLlPURjJJ1jw2lAcXntpvlV/view)
- [EFII Bus Manager Installation Instructions](https://drive.google.com/file/d/15OSKV66Y01w9-h93sxs9tNDaLjTv4gw_/view)
- [EarthX ETX900 Installation & Maintenance Manual](https://drive.google.com/file/d/1ZESKGgF3pW5eckKshcZ608nd0RrMmGhE/view)
- [Power & Lighting Schematic](https://drive.google.com/file/d/1hXrVusmeaCbz3MywPmLUjcQ1TfPFVOE9/view)
- [VPX Pro/Sport Load Planning Worksheet](https://drive.google.com/file/d/1uy9UFDHQYeuw0kTXVAed_0YB3Jd1rMf1/view)
