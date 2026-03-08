# Flight Controls

> ATA Chapter 27 — N720AK Systems Reference

## Overview

N720AK has dual controls (pilot and co-pilot) with push-pull tube actuation for ailerons and elevator, cable actuation for rudder. The stick grips are **Tosten CS Military** with multiple programmable buttons. Electric trim is provided for pitch and roll axes.

## Components

| Component | Part Number | Supplier | Notes |
|-----------|-------------|----------|-------|
| Stick grip (x2) | [CS Military](https://drive.google.com/file/d/1B6rsaPuWOP-TiiiwlmuQLgSspJDqMclw/view) | Tosten | Pilot and co-pilot |
| Pitch trim servo | <!-- TODO --> | <!-- TODO --> | Elevator trim tab |
| Roll trim servo | <!-- TODO --> | <!-- TODO --> | In wing |
| Flap motor | <!-- TODO --> | <!-- TODO --> | Electric |
| Co-pilot trim switch | <!-- TODO --> | <!-- TODO --> | Panel-mounted enable/disable |

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

### Trim Systems

- **Pitch Trim**: Electric servo-actuated trim tab on elevator, controlled by hat switch on stick grip
- **Roll Trim**: Electric servo in wing, controlled by hat switch on stick grip
- **Yaw Trim**: None installed

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
