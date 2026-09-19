# Engine — Mechanical

> ATA Chapter 71 — N720AK Systems Reference

## Overview

N720AK is powered by a **Lycoming IO-540** series engine, fuel-injected and normally aspirated, rated at 260 HP at 2700 RPM. This page covers the mechanical aspects of the engine — oil system, cooling, baffling, exhaust, and mounts. For the electronic engine management (ignition and fuel injection), see [EFII System32](./sys-73-efii.md).

## Components

| Component | Part Number | Supplier | Notes |
|-----------|-------------|----------|-------|
| Engine | [YIO-540-D4A5](https://drive.google.com/file/d/17j1PZGpcXN6gP7nDkUjgf3N6mP3sHwLI/view) | Lycoming | S/N EL-36315-48E, 260 HP at 2700 RPM |
| Engine mount | <!-- TODO --> | <!-- TODO --> | Steel tube |
| Oil drain plug | [Magnetic Oil Drain Super Plug](https://www.aircraftspruce.com/catalog/hapages/superplub05-12373.php) | Aircraft Spruce (05-12373) | 1/2" NPT, Alnico magnet (1-1/32" long), CAD plated, safety wire drilled. Experimental — verify sump/pickup clearance before install |
| Oil quick drain | P5000 | Saf-Air | Quick drain valve on engine oil sump |
| Oil filter | <!-- TODO --> | <!-- TODO --> | <!-- TODO --> |
| Oil cooler | <!-- TODO --> | <!-- TODO --> | <!-- TODO --> |
| Oil separator | ASA | Antisplat Aero | Installed with install kit — [manual](https://drive.google.com/file/d/1rjRygbzXgBNityTIXKS4SQdpd77tuhWP/view), [installation guide](https://drive.google.com/file/d/1NkfPKDnFfFsIQvHDnso-gt4cVNGTY-EB/view) |
| Crankcase vacuum valve | Complete kit | Antisplat Aero | Crankcase vacuum system — [manual](https://drive.google.com/file/d/1rjRygbzXgBNityTIXKS4SQdpd77tuhWP/view) |
| Valve covers | Billet | SDS/Lycoming | O-ring #160 Viton 75 duro, torque 75–85 in-lbs — [specs](https://drive.google.com/file/d/1fxoCymURDKGM_IgYJJXaPjBpLPWcRwWW/view) |
| Filtered air box | FAB-540 | Van's Aircraft | VFR only, 1/4-20 mounts tab-locked or safety wired — [installation guide](https://drive.google.com/file/d/1wrHayG8FZioF6GTLJ1P4RvtxQxPMfhZ7/view). Modified alt air door — see [Alt Air Door](#alt-air-door) below |
| Engine mount covers | <!-- TODO --> | Aerosport Products | Carbon fiber covers, installed |
| Preheat — engine | [Reiff XP](https://www.reiffpreheat.com/product.htm) | Reiff Preheat Systems | Cylinder band heaters on all 6 cylinders |
| Preheat — oil sump | Reiff HotStrip | Reiff Preheat Systems | Oil sump heater; plug is inside the oil door |
| Spark plug adapters | SPA-6 | flyEFII | 18mm→14mm thread adapters, naval brass, 6 installed. Allows automotive spark plugs with EFII ignition |
| Spark plugs | <!-- TODO: confirm exact NGK model --> | NGK | Automotive 14mm plugs in EFII SPA-6 adapters |

**Engine:** Lycoming YIO-540-D4A5, S/N EL-36315-48E, firing order 1-4-5-2-3-6, spark plug gap 0.016"–0.022".

<!-- TODO: Time since new, time since overhaul -->

## How It Works

### Oil System

Oil separator evacuation tube: check every oil change or 50 hrs for coking/buildup. Hose: 3/4" (6-cyl). Pop-off valve 0.5 PSI. Oil return #4 AN. See [Anti-Splat installation guide](https://drive.google.com/file/d/1NkfPKDnFfFsIQvHDnso-gt4cVNGTY-EB/view).

<!-- TODO: Oil type and capacity -->
<!-- TODO: Oil cooler location and routing -->
<!-- TODO: Oil filter location -->
<!-- TODO: Oil temperature and pressure normal ranges -->

### Cooling

<!-- TODO: Baffling description -->
<!-- TODO: CHT management — what's normal, what's too hot -->
<!-- TODO: Any baffling modifications or improvements? -->

### Exhaust

Ball joint hardware: AN3 bolt, AN960C10 washer, MS21042-3 nut (3 places). Springs face forward toward prop. Install nut with 2–3 threads showing; do not bottom spring on bolt. See [Goldberg ball joint diagram](https://drive.google.com/file/d/1exjRBHG0Y3DB3LnLpRSHmjOAufc6BeaS/view).

Exhaust hanging kit: cable assembly, anti-sway assembly, support strap bends (30° up LH, 20° down RH). See [exhaust hanging kit sketch](https://drive.google.com/file/d/1mBQ22gVyqttqpm6rcNZUiJZYJOeXri_9/view).

<!-- TODO: Exhaust system description -->
<!-- TODO: Heat muff for cabin heat -->
<!-- TODO: EGT probe locations -->

### Alt Air Door

N720AK uses a modified alternate air door on the FAB-540 filtered air box, based on [this design](https://buildingrv10.blogspot.com/2014/09/filtered-air-box-alt-air-door-redo.html). Unlike the stock Van's design (which only allows opening), this modification uses an aluminum sliding gate mechanism actuated by cable from inside the cabin, allowing the pilot to both **open and close** the alternate air door in flight.

### Preheat System

N720AK has a **Reiff XP** preheat system with cylinder band heaters on all 6 cylinders, plus a **Reiff HotStrip** oil sump heater. The power plug is located inside the oil access door.

### Engine Mount

Steel tube engine mount.
<!-- TODO: Mount type, manufacturer -->
<!-- TODO: Lord mount locations and part numbers -->
<!-- TODO: Inspection criteria -->

## Inspection & Maintenance

<!-- TODO: Oil change interval and procedure -->
<!-- TODO: Compression check procedure and recent results -->
<!-- TODO: Spark plug (if any traditional ones) inspection -->

### Lycoming SB 634 — Cylinder Retirement

Lycoming Mandatory Service Bulletin 634 (October 2018) requires retirement of certain parallel valve cylinder and head assemblies shipped between Sep 2013 and Apr 2015, due to compression loss from head casting leakage. N720AK cylinder serial numbers were checked against Table 1 — **none are listed, aircraft is not affected**.

### Airworthiness Directives and this engine

**No FAA Airworthiness Directive reaches this engine, and the reason is not that
the airframe is experimental.** Lycoming Form 2784 states that non-certified
engines are *"not type certificated in accordance with Title 14, Part 33"* and
*"not made under a Federal Aviation Administration production limitation record."*
A Part 39 AD attaches to a type-certificated product, and a **Y**IO-540-D4A5 is
not one — which is why it shipped on a Certificate of Conformance (Form 2700)
rather than an 8130-3, and why every Lycoming AD model list reads `IO-540-D4A5`
and never `YIO-540-D4A5`.

Do not over-generalize this. Per **AC 39-7D**, an AD written against a
type-certificated engine, propeller or appliance *does* reach that item when it
is installed in an amateur-built aircraft. This aircraft's operating limitations
(8130-7, 27 conditions) never mention ADs either way. So each installed item is
judged on its own certification status, not the airframe's.

**Mandatory Service Bulletins are a separate question, and they do bite.**
Lycoming writes bulletins against ship dates and serial numbers regardless of
certification status — MSB 632B's Table 1 contains 119 experimental `EL-`
serials, proving the point. One currently applies:

| Bulletin | Applies | Trigger |
|---|---|---|
| **MSB 630B** — connecting rod bushing inspection | **YES**, by ship date (window 2009-01-30 → 2021-09-09; this engine shipped 2015-07-06) | **At every cylinder removal**, before reinstalling. Not calendar or hour driven. |

The parallel AD (2026-04-11) would additionally require a repetitive
bronze-particulate check of the filter and screens at **every oil change**. That
requirement exists only in the AD and does not bind this engine — but it is
cheap and aimed squarely at the failure mode, so it is worth doing voluntarily.

Full determinations, including the negative ones, live in
`ad-sb-compliance.tsv` in GDrive `Private/Maintenance/`.

### Billet Valve Covers

Replacement O-rings for billet covers: COTS Viton O-ring #160, 75 durometer. Torque: 75–85 in-lbs. Lubricate O-ring and groove before install. See [SDS billet valve cover specs](https://drive.google.com/file/d/1fxoCymURDKGM_IgYJJXaPjBpLPWcRwWW/view).

<!-- TODO: Engine mount inspection points -->
<!-- TODO: Baffling inspection -->

### Lycoming Accessory Case Oil System

Reference: [VAF thread — Lycoming accessory case oil schematic by Dan H](https://vansairforce.net/threads/lycoming-accessory-case-oil-schematic.45548/)

## References

- [Oil Separator / Vacuum System](https://drive.google.com/file/d/1rjRygbzXgBNityTIXKS4SQdpd77tuhWP/view)
- [Anti-Splat Aero Oil Separator Installation Guide](https://drive.google.com/file/d/1NkfPKDnFfFsIQvHDnso-gt4cVNGTY-EB/view) — evacuation tube check interval, hose sizing, pop-off valve spec
- [Lycoming IO-540 Operator's Manual (60297-10)](https://drive.google.com/file/d/17j1PZGpcXN6gP7nDkUjgf3N6mP3sHwLI/view)
- [Goldberg Exhaust Ball Joint Diagram (2014)](https://drive.google.com/file/d/1exjRBHG0Y3DB3LnLpRSHmjOAufc6BeaS/view) — AN3/AN960C10/MS21042-3 hardware, spring orientation
- [Exhaust Hanging Kit Sketch](https://drive.google.com/file/d/1mBQ22gVyqttqpm6rcNZUiJZYJOeXri_9/view) — cable assembly, anti-sway, support strap bend angles
- [SDS/Lycoming Billet Valve Cover Specs](https://drive.google.com/file/d/1fxoCymURDKGM_IgYJJXaPjBpLPWcRwWW/view) — O-ring #160 Viton, torque 75–85 in-lbs
- [Van's FAB-540 Filtered Air Box Installation](https://drive.google.com/file/d/1wrHayG8FZioF6GTLJ1P4RvtxQxPMfhZ7/view) — VFR only, carb heat door VA-130-H
- [MilSpec 4000 Series Cowling Fasteners Installation](https://drive.google.com/file/d/1VDGxhOahlBffD9VvPlNwQtvttik_Vqoc/view) — Diamondhead quarter-turn, TSO-C-148, spacing 3.5–4.25"
- [Skybolt VLoc Diamondhead Cowling Installation (Rev 22)](https://drive.google.com/file/d/1I4oNZoDTvq9ZZDrlb65K6z9avPsKbJcM/view) — SK-OSG1-8 high shear grommet
