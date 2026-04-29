# Additional Engine Information

## Key Engine Data

| Parameter | Value |
|-----------|-------|
| Manufacturer | Lycoming |
| Model | YIO-540-D4A5 |
| Serial Number | EL-36315-48E |
| Type | 6-cylinder, horizontally opposed, fuel-injected, normally aspirated, air-cooled, direct drive |
| Rated Horsepower | 260 HP @ 2,700 RPM |
| Bore × Stroke | 5.125" × 4.375" |
| Displacement | 541.5 cu in |
| Compression Ratio | 9:1 |
| Firing Order | 1-4-5-2-3-6 |
| Spark Plug Gap | 0.016" – 0.022" |
| TBO (Lycoming recommended) | 2,000 hours |
| Installed | 2025-11-18 (new from Lycoming) |
| Hours at Installation | 0.0 |

## Engine Management System

The engine is managed by the **EFII System32**, which replaces the stock Bendix fuel servo, magnetos, mixture cable, and engine-driven fuel pump with:

- **Dual ECUs** — independent fuel and ignition control. Either ECU can run the engine.
- **Port fuel injection** — six EFII PMI injectors (one per cylinder).
- **Electronic ignition** — coil packs, automotive NGK plugs in EFII SPA-6 18 → 14 mm adapters.
- **Dual electric fuel pumps** — Walbro GSL391 ×2, Bus Manager auto-cutover at 22 PSI Borla output absolute.
- **Borla 203133 MAP-referenced fuel pressure regulator** — 45 PSI injector differential setpoint (DIFF mode on Dynon).

Pilot controls reduce to: throttle, propeller, **Fuel Trim knob** (±50% authority on the System32 controller — replaces the mixture lever). Fuel mixture, ignition timing, accelerator-pump enrichment, and warm-up enrichment are all handled automatically by the ECU based on MAP, RPM, and temperature inputs.

For complete System32 reference see [sys-73-efii.md](./sys-73-efii.md). For the mechanical engine reference see [sys-71-engine.md](./sys-71-engine.md). For the fuel system see [sys-28-fuel-system.md](./sys-28-fuel-system.md).

## Operating Limits Reference

See Section 2 for the authoritative table. Quick reference:

| Parameter | Limit |
|-----------|-------|
| Max RPM | 2,700 |
| Max CHT (red line) | 420 °F |
| Yellow CHT band | 400 – 420 °F (target < 400 °F) |
| Max Oil Temp | 245 °F |
| Oil Pressure (Idle Min) | 25 PSI |
| Oil Pressure (Normal) | 60 – 90 PSI |
| Fuel Pressure DIFF Setpoint | 45 PSI |

## Power Settings (Reference)

| Phase | Throttle | Prop RPM | Fuel Trim |
|-------|----------|---------:|-----------|
| Takeoff | Full | 2,700 | 0% |
| Initial Climb (to 1,000 AGL) | Full | 2,700 | 0% (richen if CHT > 400) |
| Cruise Climb | Full | 2,500 | 0% |
| Cruise (default) | As desired | 2,400 | 0% |
| Descent | As desired | 2,400 | 0% |
| Approach / Landing | Idle | Full forward | 0% |

## Cooling

CHT management on this airframe (Lycoming IO-540 with EFII System32 in an RV-10 cowl) is the primary high-power-climb concern. Per Section 2, target CHT is < 400 °F at all power settings. **Do not exceed 420 °F.** If CHT approaches 400 in climb:

1. Enrich Fuel Trim (+10% CW on the System32 controller).
2. Reduce climb angle (lower the nose, accept a higher airspeed and a lower vertical rate).

CHT alarms are configured in the Dynon EMS sensor config (`.dfg`). See [sys-71-engine.md — Cooling](./sys-71-engine.md#cooling) and the EMS sensor config in `Public/Configs/Dynon/`.
