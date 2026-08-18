# Operating Limitations

## General

This section provides the operating limitations, instrument markings, color
coding and basic placards necessary for the safe operation of the airplane
and its systems.

## Airspeed Limitations

| Type | Description | Value |
|------|-------------|-------|
| V~S0~ | Stall, Flaps Down (33°, ~2,190 lb) | 48 KIAS |
| V~S~ | Stall, Flaps 16° (~2,190 lb) | 56 KIAS |
| V~S1~ | Stall, Flaps Up (~2,190 lb) | 61 KIAS |
| V~G~ | Best Glide (prop full coarse) | 95 KIAS |
| V~X~ | Best Angle of Climb | 80 KIAS |
| V~Y~ | Best Rate of Climb | 95 KIAS |
| V~FE~ | Maximum Flap Extended — half flaps | 95 KIAS |
| V~FE~ | Maximum Flap Extended — full flaps | 87 KIAS |
| V~NO~ | Maximum Structural Cruising | 158 KIAS |
| V~A~ | Design Maneuvering (at max gross) | 125 KIAS |
| V~NE~ | Never Exceed | **200 KTAS** |

> **V~NE~ is true airspeed, not indicated.** At altitude, indicated airspeed
> at V~NE~ is lower than 200 KIAS. The Dynon SkyView shows TAS in the wind
> bug area; verify TAS rather than IAS when operating near V~NE~.
>
> **Stall speeds** are at ~2,190 lb test weight. At max gross (2,700 lb)
> add approximately 10%.

## Power Plant Limitations

| Parameter | Limit |
|-----------|-------|
| Engine | Lycoming YIO-540-D4A5 (S/N EL-36315-48E) |
| Maximum Horsepower | 260 HP |
| Maximum Speed | 2,700 RPM |
| Maximum CHT | 500 °F (operate well below; target < 400 °F) |
| Maximum Oil Temperature | 245 °F |
| Oil Pressure (Idle Min) | 25 PSI |
| Oil Pressure (Normal) | 60 – 90 PSI |
| Oil Pressure (Max Cold) | 115 PSI |
| Fuel Pressure Setpoint (DIFF, displayed) | **45 PSI** — injector differential (Borla regulator, 2026-03-17) |
| Fuel Pressure Auto-Cutover Trip | Borla output drops to **22 PSI absolute**; e.g., at 10 inHg MAP the Dynon DIFF reads ~12 PSI |

## Power Plant EFIS Markings

### Tachometer
| Arc | Range |
|-----|-------|
| Green Arc | 500 – 2,700 RPM |
| Red Line (Max) | 2,700 RPM |

### Oil Temperature
| Arc | Range |
|-----|-------|
| Green Arc | 180 – 220 °F |
| Yellow Arc | 220 – 245 °F |
| Red Line (Max) | 245 °F |

### Oil Pressure
| Arc | Range |
|-----|-------|
| Green Arc | 60 – 90 PSI |
| Yellow Arc (Low) | 25 – 60 PSI |
| Yellow Arc (High) | 90 – 115 PSI |
| Red Line (Min, Idle) | 25 PSI |
| Red Line (Max) | 115 PSI |

### Cylinder Head Temperature
| Arc | Range |
|-----|-------|
| Green Arc | < 400 °F |
| Yellow Arc | 400 – 420 °F |
| Red Line (Max) | 420 °F |

> Target CHT at all power settings is **< 400 °F**. **Do not exceed 420 °F.**
> If CHT approaches 400 °F in climb, enrich Fuel Trim (+10 % CW on the
> System32 controller) or reduce climb angle.

## Weight Limits

| Limit | Value |
|-------|-------|
| Maximum Takeoff Weight | 2,700 lbs |
| Maximum Landing Weight | 2,700 lbs |
| Maximum Baggage Weight | 150 lbs |

## Center of Gravity Limits

CG envelope per Van's RV-10 documentation. See Section 7 (Weight & Balance)
for the loading worksheet.

## Flight Maneuver Limitations

**Slips in clean configuration require care.** The RV-10 rudder can
aerodynamically stall during slips with flaps up, resulting in a sudden and
uncommanded snap roll. Slips are most predictable with flaps extended, which
reduces the angle of attack required for a given airspeed and prevents
rudder stall.

**Spins are prohibited.** The RV-10 is not approved for intentional spins,
and Van's has not demonstrated spin recovery for the type. PARE is the
universal procedure if a spin is entered inadvertently — see Section 4.

## Types of Operations

The airplane is approved for the following operations when equipped in
accordance with FAR 91:

- Day VFR
- Night VFR
- Day IFR
- Night IFR
- Non-Icing

## Fuel Limitations

| Parameter | Value |
|-----------|-------|
| Fuel Capacity (Total) | 60 U.S. gallons (30 per tank) |
| Usable Fuel | 59 U.S. gallons (29.5 per tank) |
| Minimum Grade | 100LL or premium unleaded 91 octane mogas (see limitations below) |

### Mogas Limitations (EFII System32)

When using premium unleaded mogas (91 octane minimum):

- **Altitude limit**: Stay below 8,000 ft density altitude (higher vapor pressure than avgas)
- **Temperature limit**: Do not use mogas in OAT above 100 °F
- **High terrain**: Use 100LL when flying over high terrain with limited landing options
- Mogas reaches its vapor point more easily than avgas at altitude and in heat

## Placards

| Location | Placard |
|----------|---------|
| In view from entrance | EXPERIMENTAL |
| In view of occupants | PASSENGER WARNING: THIS AIRCRAFT IS AMATEUR BUILT AND DOES NOT COMPLY WITH FEDERAL SAFETY REGULATIONS FOR STANDARD AIRCRAFT. |
| At each fuel filler | 100LL / 91 MOGAS, 30 Gal. |
