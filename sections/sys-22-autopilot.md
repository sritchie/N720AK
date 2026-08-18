# Autopilot

> ATA Chapter 22 — N720AK Systems Reference

## Overview

N720AK uses the **Dynon 3-axis autopilot** integrated with the Skyview HDX EFIS. The system provides roll (aileron), pitch (elevator), and yaw damper servo control. The autopilot is controlled via the Dynon autopilot panel on the instrument panel and can be disconnected instantly via the red button on the Tosten CS Military stick grip.

## Components

| Component | Part Number | Supplier | Notes |
|-----------|-------------|----------|-------|
| Roll servo | <!-- TODO --> | Dynon | Aileron axis — [tuning guide](https://drive.google.com/file/d/1EsYWdLyHYih_TPhDTpNbwdXyRhECW5kl/view) |
| Pitch servo | <!-- TODO --> | Dynon | Elevator axis |
| Yaw damper | <!-- TODO --> | Dynon | Yaw axis |
| AP control panel | <!-- TODO --> | Dynon | Panel-mounted — [install guide](https://drive.google.com/file/d/1n78cJB2_7Fj_dKWa3pZ48iWXHp_xgzVq/view) |
| AP disconnect | — | Tosten grip | Red button on both sticks |

## How It Works

<!-- TODO: Describe AP modes available (HDG, NAV, ALT, VS, VNAV, approach), coupling with GTN 650, GPSS steering -->

### Known Quirk: Silent TRK Reversion on Localizer Signal Loss

Community-reported on SkyView HDX + GTN installations: a temporary localizer
signal loss while coupled drops the autopilot from NAV to **TRK mode with no
alert**, and it does **not** recapture when the signal returns — NAV must be
re-armed manually. If the top bar shows TRK on a coupled localizer, guidance
has been lost. <!-- TODO: Verify this behavior in VMC on N720AK. -->

### Control Wheel Steering (CWS)

The Dynon autopilot supports **Control Wheel Steering** mode. Press and hold the autopilot disconnect button on the stick grip to temporarily override the autopilot, manually fly the aircraft to a new attitude/heading, then release the button. The autopilot will hold the new state. This allows quick course corrections without fully disconnecting and re-engaging the autopilot.

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

- [Dynon SkyView Autopilot In-Flight Tuning Guide (Rev F)](https://drive.google.com/file/d/1EsYWdLyHYih_TPhDTpNbwdXyRhECW5kl/view)
- [Dynon SkyView System Installation Guide (Rev AX)](https://drive.google.com/file/d/1n78cJB2_7Fj_dKWa3pZ48iWXHp_xgzVq/view)
- [Dynon AP Roll Servo for RV-10 Right Wing (Doc 101046-003, Rev H)](https://drive.google.com/file/d/1cMuioRntHVxvx_9T4MZJNQehKsGSFT4j/view) — Kit P/Ns: 100870-001 Right Roll Bracket, 100872-001 Right Support Bracket, 100966-008 Aluminum Pushrod 3.0", 100836-000 Large Male Rod End. Hardware: AN3H-3A, AN3H-10A, AN3H-17A, AN970-3, AN365-1032A.
- [Dynon AP Pitch Servo for RV-10 Linear Actuator (Doc 101046-007, Rev E)](https://drive.google.com/file/d/1X12fxjfgxR3uQbcHKydyKK7tb5qta-Yg/view) — Kit P/Ns: 100973-002, 100836-000, 100982-001.
- [Dynon AP Yaw Tiller Arm/Bow Kit for RV-10/14 (Doc 102710-000, Rev A)](https://drive.google.com/file/d/15AFIPQ6ojmhK8ppL7KS-saivPqSvHEjH/view) — Kit P/Ns: 102701-000, 102702-000, 100904-001, 100905-000, 101877-000.
