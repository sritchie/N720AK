# General

## Introduction

The RV-10 is a four-place, single-engine experimental aircraft powered by a Lycoming YIO-540-D4A5 six-cylinder reciprocating engine driving a Whirlwind constant-speed propeller. The aircraft is primarily constructed of alclad aluminum using flush rivets to the maximum extent possible. N720AK is operated under FAA Experimental Amateur-Built rules.

For aircraft systems descriptions see Section 8. For systems-reference detail beyond what is needed for normal operation, see the `sys-*.md` pages.

## Exterior Dimensions

| Dimension | Value |
|-----------|-------|
| Wing Span | 32' 9" |
| Length | 25' |
| Height | 8' 8" |
| Wing Area | 147 sq. ft. |
| Wing Airfoil | Custom (coordinates in `docs/rv10-airfoil-coordinates.txt`) |

## General Specifications

| Specification | Value |
|---------------|-------|
| Wing Span | 32' 9" |
| Length | 25' |
| Wing Area | 147 sq. ft. |
| Empty Weight (2025-11-18) | 1,643 lbs |
| Gross Weight | 2,700 lbs |
| Useful Load | 1,057 lbs |
| Wing Loading (Gross) | 18.4 lbs/sq. ft. |
| Power Loading (Gross) | 10.4 lbs/HP |
| Engine | Lycoming YIO-540-D4A5, 260 HP @ 2,700 RPM |
| Propeller | Whirlwind WWA-RV10, 2-blade, 80" constant-speed |
| Fuel Capacity | 60 U.S. gal (59 usable) |
| Baggage Capacity | 150 lbs |

## Performance Specifications

Van's published numbers for the RV-10 with a 260 HP engine. Cruise figures at 8,000 ft. Speeds are KTAS unless noted.

| Performance | Light (2,200 lbs) | Gross (2,700 lbs) |
|-------------|------------------:|------------------:|
| Top Speed | 183 KTAS | 181 KTAS |
| Cruise (75%) | 175 KTAS | 171 KTAS |
| Cruise (55%) | 156 KTAS | 153 KTAS |
| Stall Speed | 50 KIAS | 55 KIAS |
| Rate of Climb | 1,950 fpm | 1,450 fpm |
| Ceiling | 24,000 ft | 20,000 ft |
| Takeoff Distance | 360 ft | 500 ft |
| Landing Distance | 525 ft | 650 ft |
| Range (75%) | — | 717 NM |
| Range (55%) | — | 869 NM |

> N720AK-specific test stalls: V~S0~ 48 / V~S~ 56 / V~S1~ 61 KIAS at ~2,190 lb test weight (see Section 2).

## Engine

| Parameter | Value |
|-----------|-------|
| Manufacturer | Lycoming |
| Model | YIO-540-D4A5 |
| Serial Number | EL-36315-48E |
| Rated Horsepower | 260 HP |
| Rated Speed | 2,700 RPM |
| Type | 6-cylinder, horizontally opposed, fuel-injected, normally aspirated, air-cooled, direct drive |
| Firing Order | 1-4-5-2-3-6 |
| Bore | 5.125" |
| Stroke | 4.375" |
| Displacement | 541.5 cu in |
| Compression Ratio | 9:1 (N720AK as configured for EFII System32) |
| Spark Plug Gap | 0.016" – 0.022" |

Fuel injection and ignition are managed by the **EFII System32** electronic engine management system (dual ECU); see [sys-73-efii.md](./sys-73-efii.md). The mechanical engine reference is in [sys-71-engine.md](./sys-71-engine.md).

## Propeller

| Parameter | Value |
|-----------|-------|
| Manufacturer | Whirlwind Aviation, 1 Propeller Place, Piqua OH 45356 |
| Model | WWA-RV10 |
| Type | Constant-speed |
| Blades | 2 |
| Length | 80" |
| Weight | 44 lbs |
| Hub Serial Number | RV10-366 |
| Blade Serial Numbers | RV10-443, RV10-444 |
| Date of Manufacture | 2017-10-12 |
| Low Pitch | 12.8° |
| High Pitch | 35.1° |
| Governor | Aero Technologies (Jihostroj) PCU5000X |

## Fuel

| Parameter | Value |
|-----------|-------|
| Fuel Capacity (Total) | 60 U.S. gallons (30 per tank) |
| Usable Fuel | 59 U.S. gallons (29.5 per tank) |
| Minimum Grade | 100LL or premium unleaded 91 octane mogas (see [EFII fuel notes](sys-73-efii.md)) |
| Fuel Pressure (DIFF setpoint) | 45 PSI (Borla regulator, 2026-03-17) |

## Oil

| Parameter | Value |
|-----------|-------|
| Capacity | 12 quarts max, 8 quarts min for operation |
| Recommended Quantity | 9 quarts for extended flight |
| Viscosity (All Temps) | SAE 15W-50 or SAE 20W-50 |

## Maximum Weights

| Weight | Value |
|--------|-------|
| Maximum Takeoff Weight | 2,700 lbs |
| Maximum Landing Weight | 2,700 lbs |
| Maximum Baggage Weight | 150 lbs |
| Empty Weight (current, 2025-11-18) | 1,643 lbs |
| Useful Load | 1,057 lbs |

## Specific Loadings

| Loading | Value |
|---------|-------|
| Wing Loading (at gross) | 18.4 lbs/sq. ft. |
| Power Loading (at gross) | 10.4 lbs/HP |

## Symbols, Abbreviations and Terminology

### Airspeed Terminology

| Symbol | Definition |
|--------|------------|
| KIAS | Knots Indicated Airspeed |
| KCAS | Knots Calibrated Airspeed |
| KTAS | Knots True Airspeed |
| V~S0~ | Stall speed in landing configuration (flaps down) |
| V~S1~ | Stall speed in clean configuration (flaps up) |
| V~X~ | Best angle of climb speed |
| V~Y~ | Best rate of climb speed |
| V~G~ | Best glide speed |
| V~FE~ | Maximum flap extended speed |
| V~NO~ | Maximum structural cruising speed |
| V~A~ | Design maneuvering speed |
| V~NE~ | Never exceed speed (TAS, not IAS) |

### Engine Terminology

| Abbreviation | Definition |
|--------------|------------|
| RPM | Revolutions Per Minute |
| MP | Manifold Pressure |
| CHT | Cylinder Head Temperature |
| EGT | Exhaust Gas Temperature |
| FF | Fuel Flow |
| GPH | Gallons Per Hour |
| PSI | Pounds Per Square Inch |
| ECU | Engine Control Unit (EFII System32) |
| EFII | Electronic Fuel Injection and Ignition |

### Navigation and Avionics

| Abbreviation | Definition |
|--------------|------------|
| EFIS | Electronic Flight Instrument System |
| PFD | Primary Flight Display |
| MFD | Multi-Function Display |
| AHRS | Attitude and Heading Reference System |
| GPS | Global Positioning System |
| VOR | VHF Omnidirectional Range |
| ILS | Instrument Landing System |
| ADS-B | Automatic Dependent Surveillance-Broadcast |
| AoA | Angle of Attack |
| NRST | Nearest (Dynon button — direct-to-nearest with AP engaged) |

### Electrical

| Abbreviation | Definition |
|--------------|------------|
| VDC | Volts Direct Current |
| VPX | Vertical Power Sport (electronic circuit breaker system) |
| MZ-30 | Monkworkz MZ-30 generator (Battery 2 charging source) |

### Weight and Balance

| Abbreviation | Definition |
|--------------|------------|
| CG | Center of Gravity |
| MAC | Mean Aerodynamic Chord |
| ARM | Horizontal distance from datum to item CG |
| MOMENT | Weight multiplied by arm |

### General

| Abbreviation | Definition |
|--------------|------------|
| POH | Pilot's Operating Handbook |
| SM | Statute Miles |
| NM | Nautical Miles |
| ISA | International Standard Atmosphere |
| MSL | Mean Sea Level |
| AGL | Above Ground Level |
| OAT | Outside Air Temperature |
