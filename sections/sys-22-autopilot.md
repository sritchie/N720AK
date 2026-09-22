# Autopilot

> ATA Chapter 22 — N720AK Systems Reference

## Overview

N720AK uses the **Dynon 3-axis autopilot** integrated with the Skyview HDX EFIS. The system provides roll (aileron), pitch (elevator), and yaw damper servo control. The autopilot is controlled via the Dynon autopilot panel on the instrument panel and can be disconnected instantly via the red button on the Tosten CS Military stick grip.

## Components

| Component | Part Number | Supplier | Notes |
|-----------|-------------|----------|-------|
| Roll servo | <!-- TODO --> | Dynon | Aileron axis — [tuning guide](https://drive.google.com/file/d/1EsYWdLyHYih_TPhDTpNbwdXyRhECW5kl/view) |
| Pitch servo | **SV42T, P/N 101008-003, S/N 50220** | Dynon | Elevator axis, linear actuator (install doc 101046-007 Rev E). **Affected by Dynon TSB 080219 — see below.** |
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

### Dynon TSB 080219 — SV42T servo pulley (AFFECTED, OPEN)

**N720AK's pitch servo is affected.** The pulley reads as the unidirectional
"wood-grain" texture (Sam), which the bulletin defines as an affected pulley
regardless of whether a crack is present. Dynon Technical Support was contacted
2026-09-22 for repair/replacement.
<!-- TODO: inspection date, tach/hobbs, whether a crack was found, and whether
the crack check was performed under load -->

**Why it matters:** *"This can cause poor autopilot performance and presents a
risk of interfering with the flight controls."* This is a flight-controls
hazard, not an autopilot-availability one — disconnecting the autopilot does not
address it, because the linkage stays coupled to the elevator either way. That
is why Dynon's wording is *before further flight*.

**Applicability.** The bulletin (2019-08-02) covers the pulley on the Dynon
linear actuator found on *"Some Dynon Avionics SV42T Autopilot Servos (P/N
101008-003 / 101058-003)"* and on some SV32/SV42 servos retrofitted with the
linear actuator, received after 2011-12-13. This airplane's pitch servo is an
**SV42T, P/N 101008-003, S/N 50220** — the part number is listed, and the
airframe postdates the cutoff by over a decade. The bulletin is *"in effect
indefinitely or until superseded by a future bulletin."*

Dynon's compliance wording: *"Due to the nature of the issue, we recommend
complying with this service bulletin before further flight. However, it is up to
the owner/operator to determine the airworthiness of the aircraft for flight."*

#### Inspection procedure

1. **Crack check** — look for a crack running from the centre of the pulley out
   through the shear-screw bore. *"It may be necessary to engage the autopilot
   on the ground and apply force to the control surface in order to load the
   pulley to make the crack visible."* An unloaded look can miss it. A crack
   alone condemns the pulley.
2. **Texture read, with a magnifier.** Both bulletin figures are loupe shots;
   the distinction is not reliable with the naked eye.

| Pulley surface | Finish | Meaning | Action |
|---|---|---|---|
| **Crosshatch weave** — visible two-axis basket weave | Plastic-like, smooth | Not affected | May remain in service |
| **Unidirectional, wood-like "grain"** | Dull, resembles wood | **Affected** | Remove from service, contact Dynon |

#### If affected — removal

Dynon allows either removal path:

- the **entire servo assembly**, or
- the **linear actuator sub-assembly** alone, per Dynon's *"Servo Arm / Capstan
  Removal and Replacement Instructions."*

Two safety steps apply either way:

- *"ensure that any remaining linkages are secured and do not interfere with
  flight controls."*
- If removing **only** the linear actuator, *"disable the servo circuit
  electrically to prevent misleading autopilot behavior"* — disconnect the servo
  wiring and/or pull its fuse or open its breaker. This touches the SERVOS
  circuit in `plans/electrical-mods-2026-annual.md`.

Contact Dynon Technical Support on **425-402-0433** or
**support@dynonavionics.com**. The bulletin says to contact Dynon, not to ship
the unit blind.

**Roll and yaw servos.** SV32/SV42 are on the bulletin's *unaffected* list
unless retrofitted with the Dynon linear actuator. N720AK's roll servo installs
per doc 101046-003, the capstan/pushrod kit — almost certainly out of scope.
Read the label to close it out.

Compliance is tracked in `ad-sb-compliance.tsv`. Full bulletin:
[Dynon TSB 080219 — SV42T Servo Pulley](https://drive.google.com/file/d/1DdcqVG1yfhzCUwwgrU_Hi_uofDWzlLMx/view).

### Servo Installation

<!-- TODO: Servo locations, mounting details, clutch adjustment, bridle cable routing -->

## Inspection & Maintenance

<!-- TODO: Annual inspection items — servo clutch check, bridle cable condition, control surface travel with AP engaged -->

## References

- [Dynon TSB 080219 — SV42T Servo Pulley (2019-08-02)](https://drive.google.com/file/d/1DdcqVG1yfhzCUwwgrU_Hi_uofDWzlLMx/view) — the pulley cracking bulletin; N720AK's pitch servo is affected.
- [Dynon SkyView Autopilot In-Flight Tuning Guide (Rev F)](https://drive.google.com/file/d/1EsYWdLyHYih_TPhDTpNbwdXyRhECW5kl/view)
- [Dynon SkyView System Installation Guide (Rev AX)](https://drive.google.com/file/d/1n78cJB2_7Fj_dKWa3pZ48iWXHp_xgzVq/view)
- [Dynon AP Roll Servo for RV-10 Right Wing (Doc 101046-003, Rev H)](https://drive.google.com/file/d/1cMuioRntHVxvx_9T4MZJNQehKsGSFT4j/view) — Kit P/Ns: 100870-001 Right Roll Bracket, 100872-001 Right Support Bracket, 100966-008 Aluminum Pushrod 3.0", 100836-000 Large Male Rod End. Hardware: AN3H-3A, AN3H-10A, AN3H-17A, AN970-3, AN365-1032A.
- [Dynon AP Pitch Servo for RV-10 Linear Actuator (Doc 101046-007, Rev E)](https://drive.google.com/file/d/1X12fxjfgxR3uQbcHKydyKK7tb5qta-Yg/view) — Kit P/Ns: 100973-002, 100836-000, 100982-001.
- [Dynon AP Yaw Tiller Arm/Bow Kit for RV-10/14 (Doc 102710-000, Rev A)](https://drive.google.com/file/d/15AFIPQ6ojmhK8ppL7KS-saivPqSvHEjH/view) — Kit P/Ns: 102701-000, 102702-000, 100904-001, 100905-000, 101877-000.
