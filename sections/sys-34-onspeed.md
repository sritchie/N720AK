# OnSpeed AoA

> ATA Chapter 34 — N720AK Systems Reference

## Overview

The **OnSpeed** system is an audio angle-of-attack (AoA) indicator that provides continuous tone-based feedback on the aircraft's energy state. It uses differential pressure from the pitot-static system to compute AoA and delivers audio tones through the intercom.

**OnSpeed shares the Dynon heated AoA/pitot probe — it has no independent air data source.** So OnSpeed is not a redundant AoA reference. A blocked or iced pitot takes airspeed, Dynon AoA, OnSpeed, and the AoA-derived stall warning at the same time, and because both SV-ADAHRS units breathe through the same probe they will *agree* on the bad data and raise no cross-check error. See [The Pitot/AoA Probe Is the Single Point of Failure](./sys-34-navigation.md#the-pitotaoa-probe-is-the-single-point-of-failure).

The practical upshot: **the tones are a stall-margin aid, not a redundant airspeed system.** In an unreliable-airspeed event they are gone, and the remaining references are pitch attitude, power setting, and GPS groundspeed. Altitude and VSI survive, because static comes from the two aft-fuselage ports rather than the probe.

<!-- TODO: Confirm OnSpeed is installed and operational on N720AK -->

## Components

| Component | Part Number | Supplier | Notes |
|-----------|-------------|----------|-------|
| OnSpeed box | <!-- TODO --> | FlyOnSpeed | Main processor |
| Pressure sensors | Shares the Dynon heated AoA/pitot probe | Dynon | **No independent sensors.** Common-mode failure with airspeed and Dynon AoA. |

## How It Works

OnSpeed converts AoA into a continuous audio cue. As the wing approaches stall, AoA rises and the tone changes to give the pilot a head-out-of-the-cockpit indication of energy state and stall margin. **The tones are the primary reference; the percent indicator on the panel is descriptive after-the-fact information, not directive.**

### Tones — What They Mean

As you slow down (AoA increases), you progress through five regions:

```
 FAST ─────── L/Dmax ────── ONSPEED ────── SLOW ─────── STALL
 (silence)   (low-pitch    (ONSPEED       (high-pitch   (stall warning
              pulsing)      solid tone)     pulsing)      buzz)
```

| Region | Tone | Meaning | Pilot Action |
|--------|------|---------|--------------|
| **Fast** | Silence | Above best-glide. Positive energy margin. | No action. |
| **L/D~MAX~ → ONSPEED** | Low-pitch pulsing (slow → fast) | Decelerating into the approach range. Start of low-pitch tone ≈ V~Y~ / best glide. | Normal deceleration. |
| **ONSPEED** | **Solid 400 Hz tone** | Balanced effective power — V~X~ / V~REF~ / max sustained turn rate. | **Hold this.** |
| **Below ONSPEED** | High-pitch pulsing (slow → fast) | Energy deficit — unsustainable. | **Push**: throttle, nose down, or both. |
| **Stall warning** | High-pitch buzz (20 pps) | At the aerodynamic limit. | **Unload** — reduce AoA immediately. |

### The Push / Pull Decision

The pattern alone tells you the action — no airspeed lookup required:

- **High-pitch pulsing** → push (throttle forward, nose down, or both)
- **ONSPEED solid tone** → hold; you are balanced
- **Low-pitch pulsing** → pull (throttle back, allow pitch to increase)
- **Stall warning buzz** → unload immediately

Logic is the same in level flight, in a turn, climbing, or descending — AoA-based, so the tones automatically account for bank, weight, and load factor.

### Mapping to V-Speeds

For N720AK, the OnSpeed tone progression maps approximately to the published V-speeds:

| Tone | Approximate condition |
|------|------|
| Start of low-pitch tone | V~Y~ / best glide (~95 KIAS clean) |
| ONSPEED solid tone | V~X~ / V~REF~ approach (~80 KIAS clean) |
| Stall warning buzz | Approaching V~S~ for the configuration |

Speeds vary with weight, bank, and configuration — **fly the tone, not the airspeed**.

### Audio Routing

OnSpeed audio is delivered to the headsets via the Dynon PFD audio output, mixed through the GMA 245 audio panel.

### Muted Mode

If the pilot mutes audio:

- All tones go silent **except the stall-warning buzz**, which overrides mute as a safety feature.
- Stall warning in mute fires only if AoA > stall threshold AND IAS > the mute-under-IAS setting (default 25 KIAS).

## Calibration

<!-- TODO: OnSpeed calibration procedure
  - How was it calibrated?
  - What are the current settings?
  - How to re-calibrate after maintenance?
-->

## Wiring

OnSpeed connects to the Dynon PFD for power, data, and audio output.

### OnSpeed Connector Pinout

#### Power / Ground

| Pin | Function | Wire Color |
|-----|----------|------------|
| 1 | 12V power (from PFD, 2A fuse) | Red |
| 4 | Ship ground | Black |

#### Data Inputs

| Pin | Function | Wire Color |
|-----|----------|------------|
| 21 | Flap pot wiper | White |
| 25 | EFIS serial4 TX line | Blue |

#### Button / Lower Console

| Pin | Function | Wire Color |
|-----|----------|------------|
| 5 | Ground (to "−" on button, "C1" on button, volume pot "−/CCW", pilot lo) | Black |
| 2 | Volume pot CW | Red/white |
| 9 | Volume pot wiper | Orange/white |
| 11 | "+" on button | Orange/blue |
| 23 | "NO1" on button | Brown/white |

Control cable wiring (6-conductor, button to OnSpeed box):

| Wire | Color |
|------|-------|
| 1 | Red/white |
| 2 | Orange/white |
| 3 | (none) |
| 4 | Orange/blue |
| 5 | Brown/white |
| 6 | Black |

#### Headset Audio Output

| Pin | Function | Wire Color |
|-----|----------|------------|
| 10 | Pilot audio right | Purple/green |
| 22 | Pilot audio left | Purple/yellow |

## Emergency Maneuvering — Why the Turnback Has No Altitude Number

FlyONSPEED's engine-out guidance is one line: **"maintain ONSPEED and fly the
airplane to the crash."** It holds from the failure through the flare.

The reason it replaces a number rather than supplementing one: ONSPEED is the AoA
that gives **best sustained turn rate and smallest sustained turn radius**, and it
is the *same* AoA at any weight, density altitude or G. A briefed turnback
altitude is a proxy that is only valid at one weight, one wind, one lateral
offset and one runway — which is a different set on every takeoff. FlyONSPEED
declines to publish a decision altitude at all: it is "airplane dependent" and
"can only be determined by practice."

So N720AK's `Turnback Procedure` is TLAR at ONSPEED, and the 200 ft AGL line in
it is a **floor** — where the turn definitely fails, not where it works.

Two details from the same source worth knowing:

- **If there is any doubt about the energy to reach the runway, turn into the
  wind and slow to ONSPEED.** That is the maneuver, not a fallback.
- FlyONSPEED calls for **"lift" flaps** in the turn-back — takeoff setting, else
  half or less. N720AK's checklist does not mention flaps in the turn.
  <!-- TODO: decide whether 16° belongs in the turnback. At ONSPEED with flaps the airplane is below the 90 KIAS flap inhibit, so they are available — unlike the clean 95 KIAS best-glide case. Wants a flight. -->

## Inspection & Maintenance

<!-- TODO: Annual inspection items -->

## References

- [AMX-10A Installation Diagram 1](https://drive.google.com/file/d/13pwiMGAFJFnBhGvPYXi-F6jSHgqcx79H/view)
- [AMX-10A Installation Diagram 2](https://drive.google.com/file/d/1Sw1c2xQJSDzzdc_xtxlVrdaLRYVWg2Jx/view)
- [AMX-10A Installation Diagram 3](https://drive.google.com/file/d/1UFVWUY-fRRcR6ru1VY8mgm_RKLxF4dOI/view)
- [OnSpeed Calibration Configs](https://drive.google.com/drive/folders/1Bt_X_CIPS1z9uNAD2iXAzmN482ym8fyv?usp=sharing) (Public/Configs/OnSpeed/)
- [OnSpeed Documentation](http://dev.flyonspeed.org/latest/) (web-based — installation, calibration, troubleshooting)
- [Using AOA for Emergency Maneuvering](https://www.flyonspeed.org/using-aoa-for-em-engine-out) — the engine-out turn-back doctrine above
