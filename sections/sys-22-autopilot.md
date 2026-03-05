# Autopilot

> ATA Chapter 22 — N720AK Systems Reference

## Overview

N720AK uses the **Dynon 3-axis autopilot** integrated with the Skyview HDX EFIS. The system provides roll (aileron), pitch (elevator), and yaw damper servo control. The autopilot is controlled via the Dynon autopilot panel on the instrument panel and can be disconnected instantly via the red button on the Tosten CS Military stick grip.

## Components

| Component | Part Number | Supplier | Notes |
|-----------|-------------|----------|-------|
| Roll servo | <!-- TODO --> | Dynon | Aileron axis |
| Pitch servo | <!-- TODO --> | Dynon | Elevator axis |
| Yaw damper | <!-- TODO --> | Dynon | Yaw axis |
| AP control panel | <!-- TODO --> | Dynon | Panel-mounted |
| AP disconnect | — | Tosten grip | Red button on both sticks |

## How It Works

<!-- TODO: Describe AP modes available (HDG, NAV, ALT, VS, VNAV, approach), coupling with GTN 650, GPSS steering -->

### Disconnect Logic

The autopilot disconnects when:
- The red disconnect button on either stick grip is pressed
- Manual force is applied to the controls (servo clutch slip)
- <!-- TODO: Other disconnect triggers? EFIS failure? Bus failure? -->

### Servo Installation

<!-- TODO: Servo locations, mounting details, clutch adjustment, bridle cable routing -->

## Inspection & Maintenance

<!-- TODO: Annual inspection items — servo clutch check, bridle cable condition, control surface travel with AP engaged -->

## References

<!-- TODO: Links to Dynon Skyview AP install guide, servo manuals in docs/22-autopilot/ -->
