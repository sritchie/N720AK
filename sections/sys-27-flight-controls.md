# Flight Controls

> ATA Chapter 27 — N720AK Systems Reference

## Overview

N720AK has dual controls (pilot and co-pilot) with push-pull tube actuation for ailerons and elevator, cable actuation for rudder. The stick grips are **Tosten CS Military** with multiple programmable buttons. Electric trim is provided for pitch and roll axes.

## Components

| Component | Part Number | Supplier | Notes |
|-----------|-------------|----------|-------|
| Stick grip (x2) | [CS Military (MS)](https://tostenmanufacturing.com/product/military-style-grip-ms/) | Tosten Manufacturing | Pilot and co-pilot |
| Pitch trim servo | <!-- TODO --> | <!-- TODO --> | Elevator trim tab |
| Roll trim servo | <!-- TODO --> | <!-- TODO --> | In wing |
| Flap actuator | PHA-09P | PH Aviation Services | 12V, 4A, 150 lb, 5" stroke |
| Co-pilot trim switch | — | — | Panel-mounted enable/disable |
| Throttle quadrant | [Quad Arm Rest](https://drive.google.com/file/d/1_vrHLLGZNJYQtTfJmIRkMZ_g-e_2D7c-/view) | Aerosport Products | Custom: throttle + prop only (no mixture — EFII) |
| Throttle cable | 176-VTT-2.25-89.5 | California Push-Pull | |
| Prop cable | 176-VTT-2.25-64.5 | California Push-Pull | |

## How It Works

### Stick Grip Button Layout

<!-- TODO: Add stick grip photo with button callouts -->

| Button | Function |
|--------|----------|
| Trigger | Push-to-talk (PTT) |
| Index finger button | COM1/COM2 switch (wired to GTN 650) |
| Thumb button | Autopilot disconnect |
| Hat switch | Aileron (roll) and pitch trim |
| Top right button | COM1 standby/active swap |
| Small flush black button (front, below PTT) | Not wired / unused |

### Trim Systems

- **Pitch Trim**: Electric servo-actuated trim tab on elevator, controlled by hat switch on stick grip
- **Roll Trim**: Electric servo in wing, controlled by hat switch on stick grip
- **Yaw Trim**: None installed

### Elevator Trim Tab Setting

N720AK's elevator trim tabs were set using Bill DeRouchey's method (via [myrv10.com trimming tips](https://www.myrv10.com/tips/trimming/index.html)) instead of the stock Van's procedure. The stock instructions to set both trim tabs at 35° down creates an asymmetry problem where one tab fails to rise to trail position while the other overshoots, causing tail twisting forces.

The corrected method:
1. Move the trim servo to full nose-up position
2. Set the starboard (right) trim tab trailing edge to 3" below the elevator trailing edge
3. Run the starboard trim tab to trail position
4. Set the port (left) trim tab to trail position

The key requirement is that both trim tabs reach the neutral/trailing position at the same time, and that neither tab goes up while the other goes down.

### Co-Pilot Trim Enable

A panel switch enables or disables trim authority from the co-pilot stick grip. When disabled, the co-pilot's trim hat has no effect. This prevents inadvertent trim inputs from passengers.

### Flaps

Electric flap motor with position indicator on EFIS. Controlled by:
- Panel-mounted flap switch
- Stick grip switch (both sticks)

Flap positions range from reflex (-3°) to full (40°).

## Inspection & Maintenance

### Control Stick Slop Fix

The RV-10 control stick bases can develop play between the brass bushing and the welded cylinder of the stick base. On N720AK, the **pilot side only** had noticeable slop (co-pilot was fine). The fix was a single **AN960-6** washer (sized for AN6 bolt) placed around the brass bushing so it sits against the welded cylinder. No delrin bushing replacement was needed — the original brass bushings were retained, and the single washer was sufficient to eliminate the play.

<!-- TODO: Control surface travel measurements, bellcrank inspection, push-pull tube rod end checks -->
<!-- TODO: Trim servo inspection -->
<!-- TODO: Flap motor and limit switch check -->

### Quadrant Cable Boots

Replacement cable boots for the throttle/mixture/prop quadrant: see [VAF thread on Q-43 boots](https://vansairforce.net/threads/the-quadrant-cable-boots-e-g-q-43.228223/).

## Photos

<!-- TODO: Stick grip button layout photo -->
<!-- TODO: Trim servo locations -->

## References

- [Ray Allen trim system installation instructions](http://www.aeroelectric.com/Installation_Data/Ray-Allen/Trim%20Sys%20General.pdf)
- [Tosten CS Military Wiring Diagram](https://drive.google.com/file/d/1B6rsaPuWOP-TiiiwlmuQLgSspJDqMclw/view)
- [Tosten CS Military Stick Assembly Drawing (Rev A, P/N 3-12-02)](https://drive.google.com/file/d/1N4iyJ68f3y31-2DaqXpZnqNncsPK0zsS/view) — Drill 3/16 dia hole, use 10-32 socket head cap and lock nut.
- [PH Aviation PHA-09P Flap Actuator Installation](https://drive.google.com/file/d/1qQL7wGVN-vjMoh4NBLxsvACVc99HgZmU/view) — 12 VDC, 4A full load, 150 lb capacity, 5" stroke, 0.4 in/sec, internal limit switches, built-in potentiometer. Mount: AN5-23 bolt. Compatible with Garmin GAD 27 positioning.
- [Aerosport Throttle Quadrant Installation](https://drive.google.com/file/d/1AEMHdlwCex34L_dxx_a_mmb6Uz_51j8r/view)
- [Aerosport RV-10 Cable Lengths for Quad Arm Rest](https://drive.google.com/file/d/1M2_ZCTfNf7b1JNINIGPUvsU3JesMsHgJ/view)
- [Tosten Military Style Grip (MS) product page](https://tostenmanufacturing.com/product/military-style-grip-ms/)
- Throttle/prop cables: [California Push-Pull](https://push-pull.com/) — PN 176-VTT-2.25-89.5 (throttle), PN 176-VTT-2.25-64.5 (prop)
