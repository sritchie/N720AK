# System Descriptions

## The Airplane

The RV-10 is a four-place, single-engine, low-wing aircraft with tricycle landing
gear. The airframe is primarily aluminum alloy construction with flush rivets,
except for some steel components including the engine mount, landing gear legs,
control surface bellcranks, and miscellaneous hardware. Wing tips, tail fairings,
cowling, and wheel fairings are fiberglass.

## Engine and Components

The aircraft is powered by a Lycoming IO-540 series engine, fuel injected and
normally aspirated, rated at 260 HP at 2700 RPM.

<!-- TODO: Add specific engine model and serial number -->

### Electronic Engine Management

The EFII System32 provides:

- **Full Electronic Ignition**: Dual redundant ignition with individual coil packs
  for each cylinder
- **Electronic Fuel Injection**: Precise fuel metering with automatic mixture
  optimization
- **Redundant ECUs**: Two independent Engine Control Units; panel switch allows
  manual ECU selection if needed

The System32 controller on the panel provides mixture control through the
electronic fuel injection system.

> **Detailed reference:** [EFII System32 (ATA 73)](./sys-73-efii.md)

### Fuel Pumps

Two electric fuel pumps (primary and backup) pressurize the fuel line to the
engine. The system includes:

- **Automatic Switchover**: If fuel pressure drops below threshold, the System32
  automatically activates the backup pump
- **Manual Selection**: Panel switch (PMP 2) allows manual pump selection
- **Fuel Return**: Excess fuel returns to the originating tank

> **Detailed reference:** [Fuel System (ATA 28)](./sys-28-fuel-system.md)

## Propeller

<!-- TODO: Add propeller details -->

| Parameter | Value |
|-----------|-------|
| Manufacturer | |
| Model | |
| Type | Constant speed |
| Blades | |
| Diameter | |

> **Detailed reference:** [Propeller (ATA 84)](./sys-84-propeller.md)

## Landing Gear

The landing gear is a fixed tricycle configuration with:

- Steerable nose wheel
- Main gear with wheel fairings

| Specification | Value |
|---------------|-------|
| Main Tire Size | |
| Nose Tire Size | |
| Main Tire Pressure | PSI |
| Nose Tire Pressure | PSI |

## Brake System

Hydraulic disc brakes are operated by toe pedals on both pilot and copilot
rudder pedals.

| Specification | Value |
|---------------|-------|
| Brake Fluid | Royco 782 (MIL-PRF-83282) |
| Brake Type | Hydraulic disc |

> **Detailed reference:** [Brakes & Wheels (ATA 61)](./sys-61-brakes.md)

## Flight Control System

Dual controls are fitted. Primary flight controls:

- **Ailerons**: Operated through push-pull tubes
- **Elevator**: Operated through push-pull tubes
- **Rudder**: Cable operated, connected to rudder pedals

### Trim Systems

- **Pitch Trim**: Electric servo-actuated trim tab on elevator, controlled by
  hat switch on stick grip
- **Roll Trim**: Electric servo in wing, controlled by hat switch on stick grip
- **Yaw Trim**: None installed

### Co-Pilot Trim Enable

A panel switch enables or disables trim authority from the co-pilot stick grip.
This allows the pilot to disable co-pilot trim inputs when desired.

### Flaps

Electric flap motor with position indicator on EFIS. Controlled by:

- Panel-mounted flap switch
- Stick grip switch (both sticks)

Flap positions range from reflex (-3°) to full (40°).

> **Detailed reference:** [Flight Controls (ATA 27)](./sys-27-flight-controls.md)

## Fuel System

Fuel is stored in two wing tanks with a selector valve on the center tunnel.

| Parameter | Value |
|-----------|-------|
| Left Tank Capacity | U.S. gallons |
| Right Tank Capacity | U.S. gallons |
| Total Capacity | U.S. gallons |
| Usable Fuel | U.S. gallons |
| Minimum Grade | 100LL |

### Fuel System Components

- **Wing Tanks**: Integral tanks in wing leading edges
- **Fuel Selector**: Three-position valve (LEFT / RIGHT / OFF) on center tunnel
- **Fuel Pumps**: Primary and backup electric pumps (see Engine section)
- **Fuel Return**: Returns to selected tank
- **Fuel Strainer**: Drain before first flight of day

**Note**: The fuel system does not support inverted flight.

> **Detailed reference:** [Fuel System (ATA 28)](./sys-28-fuel-system.md)

## Electrical System

### Power Sources

| Component | Specification |
|-----------|---------------|
| Primary Alternator | 60 amp, 14 volt — charges Battery 1 |
| Generator | Monkworkz MZ-30L — charges Battery 2 |
| Battery 1 | EarthX ETX900 |
| Battery 2 | EarthX ETX900 |

The two charging systems are fully isolated. The primary alternator charges
Battery 1 only, and the Monkworkz generator charges Battery 2 only.

A **Generator Enable** switch on the panel (next to the alternator field switch)
controls the generator. A normally-open relay disconnects the generator from
Battery 2 whenever the ignition key is off, preventing parasitic battery drain.

### Bus Architecture

The electrical system uses a dual-bus architecture managed by the flyEFII
System32 Bus Manager:

- **Essential Bus**: Powers critical engine systems (ignition, fuel injection,
  fuel pumps)
- **Main Bus**: Powers avionics and other aircraft systems via VPX Sport

### Emergency Endurance Bus

If a battery fails or bus voltage drops critically, the System32 Bus Manager
automatically:

1. Disconnects non-essential loads from the main bus
2. Preserves all available power for the essential bus
3. Maintains engine ignition and fuel injection

The **EMERGENCY POWER** switch on the panel manually activates this mode.

### VPX Sport Power Distribution

The Vertical Power VPX Sport provides:

- Electronic circuit breaker protection
- Load monitoring and display on EFIS
- Automatic load shedding if needed
- No physical circuit breakers to reset

> **Detailed reference:** [Electrical Power (ATA 24)](./sys-24-electrical.md)

## Pitot-Static System

### Pitot

| Component | Specification |
|-----------|---------------|
| Pitot Tube | Dynon heated pitot with AoA |
| Location | Under left wing |
| Heating | Activated by PITOT HEAT switch |

The pitot tube incorporates a second orifice angled to measure differential
pressure for Angle of Attack (AoA) display on the EFIS.

### Static

| Component | Specification |
|-----------|---------------|
| Static Ports | Two ports on aft fuselage sides |
| Alternate Static | Valve on upper left panel |

The static system feeds:

- Dynon Skyview HDX AHRS
- Backup instruments (if installed)

## Instrument Panel

### Primary Flight Display

**Dynon Skyview HDX** provides:

- Primary Flight Display (PFD)
- Multi-Function Display (MFD)
- Engine monitoring
- Moving map with terrain
- Traffic display (ADS-B In)
- Autopilot interface

### Navigation and Communication

| Component | Function |
|-----------|----------|
| Garmin GTN 650 | IFR GPS/Nav/Com - certified for IFR approaches |
| Garmin GMA245 | Audio panel with Bluetooth |
| Dynon Com Panel | Com radio control |

> **Detailed reference:** [Navigation & Instruments (ATA 34)](./sys-34-navigation.md) | [Communications (ATA 23)](./sys-23-communications.md)

### Autopilot

**Dynon 3-Axis Autopilot** with:

- Roll servo (aileron)
- Pitch servo (elevator)
- Yaw damper

Controlled via:

- Dynon autopilot panel
- Stick grip disconnect button

> **Detailed reference:** [Autopilot (ATA 22)](./sys-22-autopilot.md)

### Transponder and ELT

| Component | Specification |
|-----------|---------------|
| Transponder | <!-- TODO: Add model --> with ADS-B Out |
| ELT | Artex ELT 345 (406 MHz) |

### Panel Switches

**Left Panel:**

- Pitot Heat
- Landing Light
- Taxi Light
- Nav Lights
- Strobe Lights

**Center Panel:**

- Flap switch
- Alternator field
- Generator enable
- Avionics power
- Emergency power

**EFII System32 Switches:**

- Ignition Select
- ECU Select
- Fuel Pump Mode
- Start Battery Select

**Other:**

- Master switch (keyed)
- O2 mode switch (pulse/constant)
- Co-pilot trim enable

## Control Sticks

Both pilot and co-pilot have Tosten CS Military stick grips with identical
button functions:

<!-- TODO: Add stick grip photo with button callouts -->

| Button | Function |
|--------|----------|
| Trigger | Push-to-talk (PTT) |
| Top hat | Pitch/roll trim |
| <!-- --> | Flap up |
| <!-- --> | Flap down |
| Red button | Autopilot disconnect |
| <!-- --> | <!-- TODO: Document all buttons --> |

> **Detailed reference:** [Flight Controls (ATA 27)](./sys-27-flight-controls.md) | [Avionics & Wiring (ATA 42)](./sys-42-avionics.md)

## Oxygen System

**Mountain High EDS-4iP** pulse-demand oxygen system:

| Parameter | Specification |
|-----------|---------------|
| Type | Electronic pulse-on-demand |
| Bottle Location | <!-- TODO --> |
| Capacity | <!-- TODO --> cubic feet |

### Operating Modes

A panel switch selects between:

- **Pulse Mode**: Oxygen delivered in pulses synchronized with inhalation
  (normal operation, conserves oxygen)
- **Constant Flow**: Continuous oxygen flow (for high altitude or if pulse
  mode is insufficient)

> **Detailed reference:** [Oxygen (ATA 35)](./sys-35-oxygen.md)

## Heating, Ventilation and Defrosting

### Cabin Heat

Heat is provided from a heat muff on the exhaust system. Controlled by
push-pull knob on panel.

### Ventilation

Fresh air is supplied through:

- Eyeball vents under instrument panel (pilot and copilot)
- NACA ducts on fuselage sides

### Defrost

Windshield defrost air from the heating system.

## Cabin Features

### Seating

Four-place seating:

- Front: Pilot and copilot, side-by-side
- Rear: Two passengers

### Restraints

<!-- TODO: Specify harness type -->

## Baggage Area

| Dimension | Value |
|-----------|-------|
| Maximum Weight | 100 lbs |
| Volume | cubic feet |

Access through rear baggage door.

## Exterior Lighting

### Wing Tip Lights

Each wing tip contains:

- **AeroLEDs Pulsar (NSP/660)**: 3-in-1 LED combining position light (red/green),
  strobe, and rear-facing white position light
- **AeroLEDs AeroSun VX**: Landing and taxi light with built-in wig-wag mode

### Tail Light

- **AeroLEDs SunTail**: LED position light (white) and strobe

### Lighting Controls

| Switch | Function |
|--------|----------|
| NAV | Position lights (wing tips and tail) |
| STROBE | Strobe lights (wing tips and tail) |
| LANDING | Landing lights (wing tips) |
| TAXI | Taxi lights |

> **Detailed reference:** [Lighting (ATA 33)](./sys-33-lighting.md)
