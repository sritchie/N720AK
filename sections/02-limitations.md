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
| Minimum Grade | 100LL, or automotive gasoline per the limitations below |

### Automotive Fuel (Mogas) Limitations

Lycoming SI 1070AB approves the IO-540-D series for automotive gasoline
(ASTM D4814, 93 AKI). With the EFII System32, all fuel downstream of the
pumps is at 45 PSI — vapor can form only in the suction lines from tank to
pump, so these limits control fuel **volatility** and **temperature**, the
actual vapor-lock variables. Full rationale: [sys-28 Fuel System](sys-28-fuel-system.md).

- **Octane**: 93 AKI premium for unrestricted use (SI 1070AB). 91 AKI premium
  only when blended with at least one-third 100LL, or at or below 75% power.
  Never regular or midgrade (Colorado regular is 85 AKI).
- **Ethanol**: E0 preferred. E10 permitted for fuel burned within ~30 days;
  sump carefully for phase separation after cold soaks. E15/E85 prohibited.
- **Season (the controlling limit)**: unrestricted use only with summer-blend
  fuel (retail June 1 – September 15). Fuel bought outside that window is
  presumed winter blend (RVP up to 15 psi): do not fly it straight when fuel
  temperature may exceed 60 °F at takeoff — blend ≥50% 100LL or use 100LL.
- **Heat soak**: no takeoff on mogas with heat-soaked fuel (estimated above
  ~85 °F after sun or prolonged ground running) unless fuel pressure is
  stable at 45 ± 1 PSI during a full-power runup. Fuel temperature, not OAT,
  is the variable.
- **Altitude**: no density-altitude ceiling. Above 12,500 ft pressure
  altitude on mogas, monitor fuel pressure; on any fluctuation, switch
  tanks and descend.
- **Mixing**: 100LL and mogas mix freely in any ratio. For high terrain with
  limited landing options, keep the takeoff/landing tank 100LL-rich.
- **Oil**: with mogas, oil must contain Lycoming additive LW-16702 or
  equivalent (Aeroshell 15W-50, Phillips Victory AW). Run a tank of 100LL
  roughly every 75 hours, and 100LL only for 25 hours after cylinder work.

## Placards

| Location | Placard |
|----------|---------|
| In view from entrance | EXPERIMENTAL |
| In view of occupants | PASSENGER WARNING: THIS AIRCRAFT IS AMATEUR BUILT AND DOES NOT COMPLY WITH FEDERAL SAFETY REGULATIONS FOR STANDARD AIRCRAFT. |
| At each fuel filler | 100LL / MOGAS 93 AKI (see POH), 30 Gal. |
