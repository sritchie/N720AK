# Performance

> Performance figures below are Van's published numbers for the RV-10 with a 260 HP engine, augmented with N720AK-specific test data where available. Treat the published figures as a planning reference; verify against actual aircraft performance over the course of Phase I and ongoing operation.

## V-Speeds (Reference)

See Section 2 for authoritative values. Quick reference:

| Speed | Value |
|-------|-------|
| V~S0~ (flaps 33°, ~2,190 lb test) | 48 KIAS |
| V~S~ (flaps 16°, ~2,190 lb test) | 56 KIAS |
| V~S1~ (flaps up, ~2,190 lb test) | 61 KIAS |
| V~G~ (best glide, prop full coarse) | 95 KIAS |
| V~X~ (best angle of climb) | 80 KIAS |
| V~Y~ (best rate of climb) | 95 KIAS |
| V~FE~ (max flap extended) | 90 KIAS |
| V~A~ (maneuvering, max gross) | 125 KIAS |
| V~NO~ (max structural cruise) | 158 KIAS |
| V~NE~ (never exceed) | 200 KTAS |

## Stall and Approach Speeds

Stall speeds at ~2,190 lb test weight, level flight, idle power. At max gross (2,700 lb), add approximately 10%.

| Configuration | V~S~ | 1.3 × V~S~ (Approach) |
|---------------|----:|---------------------:|
| Flaps Up | 61 KIAS | 79 KIAS |
| Flaps 16° | 56 KIAS | 73 KIAS |
| Flaps 33° (full) | 48 KIAS | 62 KIAS |

Operationally we fly OnSpeed AOA (solid tone) for normal approach and slow tone (drag-it-in) for short field; see [OnSpeed](./sys-34-onspeed.md).

## Takeoff Performance

Van's published figures, sea level, ISA, no wind, paved runway:

| Weight | Ground Roll | 50 ft Obstacle |
|--------|------------:|---------------:|
| 2,200 lb | 360 ft | (TODO) |
| 2,700 lb (gross) | 500 ft | (TODO) |

Apply standard corrections for density altitude, wind, runway slope, and surface (grass adds ~15%).

## Climb Performance

Van's published rate of climb at sea level, ISA, full power:

| Weight | Rate of Climb | Service Ceiling |
|--------|--------------:|----------------:|
| 2,200 lb | 1,950 fpm | 24,000 ft |
| 2,700 lb (gross) | 1,450 fpm | 20,000 ft |

In practice, climb at V~Y~ (95 KIAS) until 1,000 AGL, then transition to cruise climb at 120 KIAS, full throttle, 2,500 RPM. Reduce climb angle or richen Fuel Trim if CHT approaches 400 °F.

## Cruise Performance

Van's published cruise (260 HP, 8,000 ft, ISA):

| Power Setting | Light (2,200 lb) | Gross (2,700 lb) |
|---------------|-----------------:|-----------------:|
| 75% | 175 KTAS | 171 KTAS |
| 55% | 156 KTAS | 153 KTAS |

Operationally we cruise at full throttle / **2,400 RPM** with **Fuel Trim 0%** at altitudes from 6,000 to 12,000 ft. Verify actual TAS, fuel flow, and CHT against the EFIS as the airframe accumulates hours.

## Landing Performance

Van's published figures, sea level, ISA, no wind, paved runway, max braking:

| Weight | Ground Roll | 50 ft Obstacle |
|--------|------------:|---------------:|
| 2,200 lb | 525 ft | (TODO) |
| 2,700 lb (gross) | 650 ft | (TODO) |

For short-field landing, fly the slow tone with power for descent control (drag-it-in technique); see Section 5 → Short Field Landing.

## Range and Endurance

Van's published range at 8,000 ft, no reserves, full 60 gal fuel, gross weight:

| Power | Range | Time |
|-------|------:|-----:|
| 75% | 717 NM | ~4.2 hr |
| 55% | 869 NM | ~5.7 hr |

Plan a **45-minute reserve at cruise burn** for night/IFR (FAR 91.167), 30-minute reserve for day VFR (FAR 91.151), or longer per personal minimums.

## Glide Performance

| Configuration | Glide Speed | Best L/D Ratio |
|---------------|------------|---------------:|
| Clean, prop full coarse | 95 KIAS | (TODO — verify in flight test) |

Engine-out glide distance (rule of thumb): ~1.7 NM per 1,000 ft AGL clean at best glide. Confirm with at-altitude glide tests; record altitude lost per 360° turn at 20°, 30°, 45° bank for use in turnback briefing planning per the EAA Power-Loss-on-Takeoff Working Group methodology.
