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
2026-09-22 and is sending the LA pulley assembly and a shear screw
replacement kit — see the repair procedure below.
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


#### The repair — LA pulley assembly + shear screw kit

Dynon's disposition (2026-09-22): they are sending the **linear actuator pulley
assembly** and a **shear screw replacement kit**, not a replacement servo. So
**S/N 50220 stays in the airplane**, and this is a field repair rather than a
swap — no SkyView Network reconfiguration, since it is the same device on the
bus.

Two Dynon documents govern it:

| Document | P/N | Rev | Covers |
|---|---|---|---|
| [Actuator Component Removal and Replacement Instructions](https://drive.google.com/file/d/1hkn3ZSZ0kA-6VMMo36JMxOC2y0EBwMue/view) | 101156-001 | B, 2019-08-07 | Removing and refitting the LA pulley |
| [Servo Shear Screw Replacement Kit Installation Guide](https://drive.google.com/file/d/1MKjDThXXtjv1IXXn5uSAirbLZfcWBGYj/view) | 103000-000 | C, 2025-02-18 | Replacing the shear screw (kit P/N **102991-000**) |

> ⚠ **The two documents disagree on castle nut torque.** 101156-001 Rev B says
> *"DO NOT EXCEED 4.5 in-lb (72 in-oz)"*; 103000-000 Rev C says *"beyond
> **4 in-lbs.** of torque may prevent the capstan from separating from the servo
> output shaft if the controls become jammed."* **Use 4 in-lb** — it is the
> lower figure and the newer document (2025 vs 2019). Over-torquing defeats the
> shear screw's entire purpose, so err low.

**Tools:** needle-nose pliers, torque driver reading to 4 in-lb, 1/2" SAE
socket, side cutters, 5/64" hex wrench (supplied in the kit).

**Consumables:** cotter pin **MS24665-210** — *"cotter pins should never be
reused."* Castle nut is **AN310-5**. The kit supplies its own cotter pin, shear
screw, 5/64" hex wrench and a red Loctite 271 capsule.

**Stack order, output shaft outward:** pulley → **nylon washer** → **wavy
washer** → castle nut (AN310-5) → new cotter pin. Finger-tighten the nut, then
torque only until a slot lines up with the cotter pin hole. Servo rotation must
be smooth afterwards, with no movement between the actuating component and the
attachment disc.

**On the shear screw.** 101156-001 is explicit that for a plain pulley change
the screw stays put: *"DO NOT REMOVE the socket head safety shear screw... The
autopilot safety shear screw should NEVER be removed or adjusted during this
procedure."* The pulley has a hole that fits over the screw head. The kit is
therefore a contingency for a screw found broken or damaged on teardown.
<!-- TODO: confirm with Dynon whether they intend the shear screw to be
replaced as part of this repair, or only if it is found damaged. -->

If the screw does need replacing (103000-000 Rev C):

- The attachment disc has **three** threaded holes, so a servo accepts **at
  most two** field shear-screw replacements before it must go back to Dynon.
  <!-- TODO: record how many of S/N 50220's three holes are already used -->
- The broken screw's threaded shaft stays in the disc. **Check it for burrs**
  and file smooth. **If that shaft is loose and rotating in the threads it must
  come out** — *"If the loose shear screw shaft vibrates out of the servo
  attachment disc, it may jam the flight controls."* If it will not come out,
  the servo goes back to Dynon.
- **Only a Dynon shear screw.** Any other fastener *"will void the servo's
  warranty and can cause the aircraft to be unsafe for flight."*
- Light strip of red Loctite 271 on one side of the lower half of the threads;
  fit into an **unused** hole; 5/64" hex, **hand strength only**, head **fully
  seated** against the disc. Under-seating or over-tightening both cause
  premature failure.
- **Cure: 15 minutes before refitting the pulley, and a minimum of one hour
  before flight.**

**Finally, recalibrate.** 103000-000 Rev C closes with *"Perform servo
calibration procedure provided in the appropriate installation manual."* On
SkyView that is `SETUP > HARDWARE CALIBRATION > AP SERVO CALIBRATION >
CALIBRATION`. Autopilot status will not return to the top bar until it
completes. Follow with a flight test and fine-tune per the
[tuning guide](https://drive.google.com/file/d/1EsYWdLyHYih_TPhDTpNbwdXyRhECW5kl/view).

**Check the new pulley before fitting it** — crosshatch weave, plastic-like
smooth finish, under a loupe. The bulletin covers only *some* servos by receipt
date, and it is worth thirty seconds to confirm the replacement is not itself
the affected design.

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

- [Actuator Component Removal and Replacement Instructions (101156-001, Rev B)](https://drive.google.com/file/d/1hkn3ZSZ0kA-6VMMo36JMxOC2y0EBwMue/view) — removing and refitting the LA pulley; castle nut AN310-5, cotter pin MS24665-210.
- [Servo Shear Screw Replacement Kit Installation Guide (103000-000, Rev C)](https://drive.google.com/file/d/1MKjDThXXtjv1IXXn5uSAirbLZfcWBGYj/view) — kit P/N 102991-000; three disc holes, two field replacements maximum.
- [Dynon TSB 080219 — SV42T Servo Pulley (2019-08-02)](https://drive.google.com/file/d/1DdcqVG1yfhzCUwwgrU_Hi_uofDWzlLMx/view) — the pulley cracking bulletin; N720AK's pitch servo is affected.
- [Dynon SkyView Autopilot In-Flight Tuning Guide (Rev F)](https://drive.google.com/file/d/1EsYWdLyHYih_TPhDTpNbwdXyRhECW5kl/view)
- [Dynon SkyView System Installation Guide (Rev AX)](https://drive.google.com/file/d/1n78cJB2_7Fj_dKWa3pZ48iWXHp_xgzVq/view)
- [Dynon AP Roll Servo for RV-10 Right Wing (Doc 101046-003, Rev H)](https://drive.google.com/file/d/1cMuioRntHVxvx_9T4MZJNQehKsGSFT4j/view) — Kit P/Ns: 100870-001 Right Roll Bracket, 100872-001 Right Support Bracket, 100966-008 Aluminum Pushrod 3.0", 100836-000 Large Male Rod End. Hardware: AN3H-3A, AN3H-10A, AN3H-17A, AN970-3, AN365-1032A.
- [Dynon AP Pitch Servo for RV-10 Linear Actuator (Doc 101046-007, Rev E)](https://drive.google.com/file/d/1X12fxjfgxR3uQbcHKydyKK7tb5qta-Yg/view) — Kit P/Ns: 100973-002, 100836-000, 100982-001.
- [Dynon AP Yaw Tiller Arm/Bow Kit for RV-10/14 (Doc 102710-000, Rev A)](https://drive.google.com/file/d/15AFIPQ6ojmhK8ppL7KS-saivPqSvHEjH/view) — Kit P/Ns: 102701-000, 102702-000, 100904-001, 100905-000, 101877-000.
