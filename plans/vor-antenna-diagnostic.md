# Plan: N720AK VOR/LOC/GS Antenna Diagnostic and Rebuild

## Why

Symptoms as of 2026-09-13:

- Nav audio is mostly **static with a faint ident**, even when the GTN 650 decodes
  the identifier. That is a working receiver operating with no signal margin.
- **2026-09-08**: VOR check passed at 14 DME from Kremmling (RLG 113.8), 1° bearing
  error, station identified aurally. Logged per 91.171.
- **2026-09-13**: Kremmling ducking in and out of ident and twitching on a 10 DME
  arc where reception should be solid. Steamboat unreceivable close in.
  Wig-wag was ON for this flight, which is not the usual configuration.

A one-degree bearing error the week before rules out a mistuned antenna as the
*primary* fault. Tuning does not drift in five days. What changes day to day is a
marginal connection, or a noise source that got switched on.

Two candidate mechanisms, and they are not mutually exclusive:

1. **Lossy RF path** — corroded or mis-crimped connector, or a poor antenna
   ground. N720AK's wingtips are on **piano hinges**, so Bob Archer's designed
   ground path (nutplate screws clamping the base strip to the wing) does not
   exist here. Anodized hinge stock is a poor RF conductor. Two RV-10 owners on
   VAF had exactly this: one had a wagging needle, one had no signal at all, and
   both were fixed with a ground strap from the antenna base leg to the outboard
   rib.
2. **LED lighting noise** — the Archer sits inches from a Pulsar NSP/660 (5 A
   pulsed strobe) and an AeroSun VX with wig-wag. One VAF owner with a GTN 650
   and an Archer measured his lighting raising the nav noise floor enough to flag
   the CDI at any meaningful range, with steady noise from position lights and
   cyclic noise from strobes and wig-wag. None of it showed on COM.
3. **Onboard electrical noise other than lights** — N720AK is an unusually
   electrically noisy airframe by design. The EFII System32 runs electronic
   ignition with a coil pack per cylinder, two Walbro fuel pumps, port injectors
   switching on millisecond current peaks, a 60 A alternator and an MZ-30
   generator. Switching supplies and coil discharge are broadband emitters.
   Unsuppressed plug wires in particular radiate hard across VHF.

Phase 1 separates all three. Do not cut aluminum before it does.

**Why NAV and not COM.** A nav receiver runs far more gain than a COM receiver
and the Archer sits roughly ten times closer to the wingtip lights than the belly
COM whip — about a hundred times the coupled power. "The radios sound fine" is
not evidence that the nav band is clean, and the one VAF owner who measured both
found exactly this asymmetry.

## What each instrument actually answers

They are not interchangeable, and it matters:

| Instrument | Measures | Answers |
|---|---|---|
| **RTL-SDR** (Nooelec v5) | received power vs frequency | Is something *emitting* noise into the nav band? How strong is a real station? |
| **NanoVNA-H4** | S11/S21, impedance, SWR, TDR | Is the antenna resonant in band? Where is the reflection in the coax? What is the cable loss? |
| **Multimeter** | DC continuity | Is a connector shorted or open? Is the antenna base bonded? |

The NanoVNA is a **vector network analyzer, not a spectrum analyzer**. It cannot
see ambient noise — it only measures what it transmits and gets back. The SDR
cannot measure impedance. Phase 1 is SDR work; Phase 2 is VNA work.

*(If the "spectrum analyzer" you bought is a tinySA rather than the NanoVNA, it
adds one genuinely useful trick: a near-field probe sniff to localize an emitter
to a specific box. Say so and I'll fold it into Phase 1.)*

## Safety — non-negotiable

- **Never key a COM radio while the SDR or VNA is on an aircraft antenna.**
  A few watts destroys an RTL-SDR front end and a NanoVNA bridge instantly.
  COM 2 lives under the same wing. Pull the COM breakers or brief anyone in the
  cockpit before starting.
- **Bias tee OFF.** The Nooelec v5 defaults off. Do not enable it.
- **Disconnect the nav coax from the GTN** before attaching it to test gear.
- Engine off, prop area clear, for all ground testing.

## Shopping list

| Item | Why |
|---|---|
| BNC female → SMA male adapter (×2) | Aircraft coax plug onto the SDR and the VNA |
| BNC calibration kit (open / short / 50 Ω load) | Calibrate the VNA at the plane where the aircraft plug mates |
| BNC male → BNC male jumper, ~1 ft | S21 cable-loss measurement |
| FM band-stop filter (88–108 MHz), optional | Only if Phase 1 flags front-end overload |

---

# Phase 0 — Set up the instruments

Done once. The gain calibration at the end must be repeated at the airport.

## 0.1 The SDR — already working

`librtlsdr` is installed on this Mac, and macOS needs no driver for the NESDR
SMArt v5. Plug it in and confirm:

```bash
uv run python3 scripts/rf_survey.py --check
```

Expect `Found 1 device(s): Nooelec, NESDR SMArt v5` and a list of 29 supported
gain values. The `PLL not locked!` and `No E4000 tuner found, aborting` lines at
the end are normal — `rtl_test -t` is probing for a tuner this dongle does not
have. They are not errors.

**Do not enable the bias tee.** It defaults off and would push DC into whatever
is connected.

## 0.2 Which antenna

The bundle ships three masts. For this job:

| Antenna | Use |
|---|---|
| **Telescopic** (the car-aerial one) | **Everything here.** It is the only one that reaches a quarter wave at VOR frequencies. |
| Long whip with a coil in the middle | Loaded for a different band. Not for 108–118 MHz. |
| Short whip | UHF. Not useful here. |

Set the telescopic to a quarter wavelength for the band you are sweeping:

| Band | Quarter wave |
|---|---|
| 113 MHz (VOR/LOC) | **26 in / 66 cm** |
| 332 MHz (glideslope) | **9 in / 23 cm** |

The magnetic base wants a metal ground plane under it. On the airplane, the wing
skin is ideal — that is also the most repeatable place to put it. On a desk it
has essentially no counterpoise, so desk readings are for checking the equipment,
not the airplane.

For the near-field wingtip survey, hold it **horizontal**, matching the
polarization of the nav signals you care about.

## 0.3 Calibrate the gain for your location

**This is location-specific and worth three minutes.** Auto gain is never used —
it destroys comparability — so the gain is a fixed number that has to be right.
Too high and strong local FM compresses the tuner's front end and lifts the
apparent noise floor. Too low and the dongle's own noise drowns out what you came
to measure.

Without moving the antenna:

```bash
uv run python3 scripts/rf_survey.py --gain-sweep --band nav \
    --point ref --duration 24 --outdir ~/rf-survey/gain-$(date +%F)

uv run --with numpy --with matplotlib python3 scripts/rf_analyze.py \
    --gain-check ~/rf-survey/gain-$(date +%F)
```

It captures the same band at six gains and reports how the measured noise floor
tracks the gain change:

- **Floor falls more than the gain reduction** → the higher gain was compressing.
- **Floor falls less** → the dongle's own noise is taking over.
- The best gain is the **highest one still tracking linearly**.

A bench run on 2026-09-14 at a desk in Boulder measured this:

| Gain | Floor | FM pressure | Reading |
|---|---|---|---|
| 40.2 | −25.1 | 19.8 dB | mildly compressing |
| 32.8 | −33.1 | 15.9 dB | **linear — use this** |
| 25.4 | −36.9 | 13.6 dB | internal noise dominating |
| 19.7 | −41.1 | 10.9 dB | internal noise dominating |

`32.8` is the script default as a result. **Re-run this at the airport**: the FM
environment there is different, and so is the antenna once it sits on the wing.

## 0.4 How small a change can you believe?

Two identical back-to-back captures on the bench, nothing changed between them,
differed by **0.8 dB**. That is the repeatability floor of the method at 30
seconds per capture. It is why the interpretation table treats anything under
1 dB as noise, and why every sequence repeats its baseline at the end.

## 0.5 The NanoVNA

macOS needs no driver — the NanoVNA appears as a USB CDC serial device. Plug it
in, power it on, and:

```bash
uv run --with pyserial python3 scripts/vna_capture.py --list
```

Look for a `/dev/cu.usbmodem*` entry. If nothing appears, the usual cause is a
**charge-only USB cable**; it has to carry data.

### Calibrate — and calibrate at the right plane

Calibration is only valid for the sweep range it was taken over, and only at the
physical point where the standards were attached. Both matter:

1. Screw the **SMA-to-BNC-female adapter onto the VNA** and leave it there. That
   adapter is now part of the instrument, and the aircraft plug mates to it.
2. Set the sweep range **first**: STIMULUS → START 100 MHz, STOP 350 MHz.
3. CAL → RESET, then CAL → CALIBRATE.
4. Attach each **BNC** standard to the adapter in turn: OPEN, SHORT, LOAD.
5. DONE, then SAVE to a slot.
6. **Verify**: with the 50 Ω load attached, SWR should read ≈ 1.0 flat across the
   sweep. If it does not, the calibration did not take — redo it.

Calibrating at the SMA port and then adding the adapter puts the reference plane
in the wrong place and quietly biases every reading.

### Capture a sweep to a file

Photographs of the screen are much worse than data. The H4 speaks a text console
over that serial port, so sweeps can land in Touchstone files:

```bash
uv run --with pyserial python3 scripts/vna_capture.py --band both \
    --out ~/vna/$(date +%F)-antenna-at-radio.s1p \
    --note "wingtip on, measured at the GTN end of the coax"

uv run --with numpy --with matplotlib python3 scripts/vna_analyze.py \
    ~/vna/$(date +%F)-antenna-at-radio.s1p
```

That prints mean and worst SWR per band, the resonant frequency, and |Z|, and
plots the two bands side by side. Give me the `.s1p` files and I can compare
sweeps directly — before and after a fix, or against the stock-Archer reference.

For live tuning while trimming aluminium, watching the VNA's own screen is
fine — capture a file at each step so the progression is recorded.

## 0.6 Adapters you still need

Nothing in either box mates to an aircraft BNC. See the shopping list above.

# Phase 1 — Interference and signal survey (SDR)

**Goal:** a number, in dB, for how much each lighting system raises the noise
floor in the VOR/LOC and glideslope bands. Ground test, engine off.

## 1.0 Bench check (do this at home, before the hangar)

```bash
cd ~/code/rv10
uv run python3 scripts/rf_survey.py --check
```

Confirms the dongle enumerates and prints the supported gain steps. Pick one and
use the **same value for every run** — auto gain makes runs incomparable and is
the single easiest way to waste an afternoon.

## 1.1 Survey A — on the aircraft nav coax

This is the money measurement: it sees exactly what the GTN sees, both radiated
and conducted noise.

1. Pull the airplane out where it has line of sight to a VOR or a localizer.
   Inside a metal hangar nothing works and the test is meaningless.
2. Disconnect the nav coax at the GTN 650. Adapt it onto the SDR.
3. Master ON, avionics ON. Engine off.

```bash
uv run python3 scripts/rf_survey.py --protocol --both-bands \
    --point coax --gain 32.8 \
    --outdir ~/rf-survey/$(date +%F)-coax \
    --note "KBDU ramp, engine off, nav coax at GTN end"
```

The script walks you through seven configurations and prompts before each:

| Step | Switches |
|---|---|
| `off1` | all lights off — the baseline |
| `nav` | position lights only |
| `strobe` | position + strobe |
| `wigwag` | position + strobe + wig-wag |
| `landing` | landing lights steady, everything else off |
| `all` | everything on |
| `off2` | all off again — the drift check |

`off2` is not optional. It is the only evidence that ambient conditions held
still, and the analysis refuses to trust small deltas without it.

Roughly 11 minutes of capture plus switch time.

## 1.2 Survey B — near-field at the wingtip

Same protocol, SDR on its own telescopic antenna held a foot from the right
wingtip, horizontal. This sees radiated noise only, so comparing A against B
says whether noise is arriving through the air or up the coax — which decides
whether the fix is wire routing or shielding and grounding.

```bash
uv run python3 scripts/rf_survey.py --protocol --both-bands \
    --point near --gain 32.8 \
    --outdir ~/rf-survey/$(date +%F)-wingtip
```

## 1.3 Survey C — other electrical systems, engine off

Same protocol machinery, different switches. These are the loads that run
without the engine turning.

```bash
uv run python3 scripts/rf_survey.py --protocol --sequence systems \
    --both-bands --point coax --gain 32.8 \
    --outdir ~/rf-survey/$(date +%F)-systems
```

| Step | Switches |
|---|---|
| `off1` | master + avionics only — baseline |
| `pump1` | fuel pump 1 running |
| `pump2` | fuel pump 2 running (PMP 2) |
| `pitot` | pitot heat on — the biggest switched load on the airplane |
| `avionics` | Dynon, GTN, transponder, ADS-B all live |
| `servos` | run pitch and roll trim continuously through the capture |
| `off2` | drift check |

Pitot heat is worth real attention. It is a large switched load whose wiring runs
the length of the same wing as the antenna, and the left-wing Molex for it routes
through the wing root alongside the nav coax.

## 1.4 Survey D — engine running

The only way to test ignition, the alternator and the MZ-30, because none of them
do anything with the engine stopped. This is the survey that addresses the
ignition theory directly.

### Safety, specific to this run

- Chocks in, brakes set, prop area clear, fire guard aware, second person on the
  switches while you watch the engine.
- **Never switch IGN 1 and IGN 2 off at the same time.** One at a time only.
- **Never pull an essential-bus breaker as part of this test.** On N720AK those
  breakers *are* the engine — ignition, injection and fuel pumps. This is the
  inverse of a conventional airplane and it is the one habit that could hurt you
  here.
- **Hold the same RPM for every configuration.** 1200 is a reasonable choice.
  Different RPM means different noise and the runs stop being comparable.
- Let RPM and temperatures settle before the baseline capture.

```bash
uv run python3 scripts/rf_survey.py --protocol --sequence engine \
    --both-bands --point coax --gain 32.8 \
    --outdir ~/rf-survey/$(date +%F)-engine \
    --note "1200 RPM held throughout"
```

| Step | Configuration |
|---|---|
| `idle1` | 1200 RPM, both ignitions on, lights off — baseline |
| `ign1only` | IGN 2 off, running on IGN 1 alone |
| `ign2only` | IGN 1 off, IGN 2 back on |
| `altoff` | ALT FLD off — the MZ-30 picks up the bus |
| `mzoff` | ALT FLD back on, MZ-30 enable off |
| `englights` | everything restored, then all lights on |
| `idle2` | back to baseline RPM, lights off — drift check |

The analysis uses `idle1` as the baseline automatically.

### Reading the ignition result

The comparison that matters is the two single-ignition runs against each other
and against the both-on baseline:

- **Floor drops noticeably with one ignition off** → that channel's coils or plug
  wires are the emitter. If one channel is much worse than the other, you have
  localized it to specific hardware, which is the best possible outcome.
- **Both single-ignition runs match the baseline** → ignition is not your source.
- **Both single runs are quieter than both-on by a similar amount** → both
  channels contribute; the fix is suppression, not one bad part.

### RPM sweep — the confirming test

If ignition looks guilty, capture the baseline configuration at 1000, 1500 and
2000 RPM:

```bash
for rpm in 1000 1500 2000; do
  uv run python3 scripts/rf_survey.py --config rpm$rpm --band nav \
      --point coax --gain 32.8 --outdir ~/rf-survey/$(date +%F)-rpm
done
```

Noise that scales with RPM is firing-rate correlated and therefore ignition.
Noise that is flat with RPM but present only when the engine runs is the
alternator or the generator. This distinction is worth the extra five minutes
because the two have completely different fixes.

## 1.5 Signal strength on a real station

Pick the strongest VOR receivable on the ramp from the GTN's NRST VOR page and
**write down which one** so later runs compare. Kremmling (RLG 113.8) is the
known reference from the 91.171 check if it reaches the ground at Boulder;
otherwise a localizer at a nearby field is a stronger, continuous alternative.

```bash
uv run python3 scripts/rf_survey.py --protocol --carrier 113.8 \
    --point coax --gain 32.8 --duration 30 \
    --outdir ~/rf-survey/$(date +%F)-rlg
```

This reports carrier-to-noise per lighting configuration. C/N is the number that
actually predicts whether the receiver holds lock, and it is immune to gain drift.

## 1.6 Hand it to me

```bash
uv run --with numpy --with matplotlib python3 scripts/rf_analyze.py \
    ~/rf-survey/$(date +%F)-coax \
    ~/rf-survey/$(date +%F)-wingtip \
    ~/rf-survey/$(date +%F)-systems \
    ~/rf-survey/$(date +%F)-engine
```

Tell me the directory and I'll run this, read the plots, and interpret. Output is
a delta table, a summary bar chart, per-configuration delta spectra, and a
`report.md`.

## How to read the result

| Mean rise in band | Reading |
|---|---|
| < 1 dB | measurement noise, ignore |
| 1–3 dB | real but minor |
| 3–6 dB | meaningful; a marginal antenna will show it in flight |
| 6–10 dB | serious; expect a flagged CDI at moderate range |
| > 10 dB | severe; this is the primary fault |

The analysis also separates **steady** from **pulsed** noise. Position lights
raise the median. Strobes and wig-wag raise the peak far more than the median, so
they show a large "pulsed" column. That distinction matches what the one VAF
owner with the same symptom reported, and it points at different fixes.

Two failure modes the script flags on its own:

- **FM overload** — strong Boulder FM stations compressing the tuner and lifting
  the whole floor. Re-run at `--gain 25.4` or add the band-stop filter. This is an
  artifact of the SDR, not a fault in the airplane.
- **Baseline drift** — `off1` and `off2` disagree by more than 1.5 dB, meaning
  conditions changed mid-survey and small deltas are untrustworthy.

## Decision gate

- **Lights raise the floor ≥ 3 dB** → lighting is a real contributor. Fix list in
  Phase 5: ground the lights at the wing root rather than the wingtip, shielded
  three-conductor wire, aluminium backing plate behind the Pulsar, light wires off
  the antenna elements.
- **Ignition raises the floor ≥ 3 dB** → suppression work in Phase 5.4: plug
  wires, boots, resistor plugs, coil pack grounding, routing away from the wing.
- **The alternator or MZ-30 raises the floor** → regulator or field-wire noise;
  a capacitor across the field and better bonding are the usual fixes.
- **Nothing electrical changes anything** → the problem is the RF path or the
  receiver. Phase 2 becomes primary.
- Expect **more than one**. The VAF case that started this had three faults at
  once: a painted-over ground, reversed lugs, and a failing radio.

---

# Phase 2 — RF path integrity (VNA + multimeter)

Runs independently of Phase 1. Do it the same day, wingtip off.

## 2.1 Multimeter first — it is free and finds hard faults

With the coax disconnected at **both** ends:

| Measurement | Expected | A failure means |
|---|---|---|
| Centre ↔ shield at the GTN end | **open** | Near 0 Ω = crushed coax or a shorted connector |
| Centre end-to-end | < 1 Ω | Open = broken centre conductor |
| Shield end-to-end | < 1 Ω | Open = broken braid or bad crimp |
| Antenna base leg ↔ wing rib | < 1 Ω | **The piano-hinge suspect.** High or varying = the fault |

The Archer's gamma-match capacitor DC-isolates the feed from the grounded
radiator, so centre-to-shield at the antenna reads open on a healthy install.
A near-zero reading is a fault, not a feature.

The last row is the highest-prior single fault on this airplane. Wiggle the
hinge while measuring — a reading that moves is a reading that fails in flight.

## 2.2 VNA sweep from the radio end

Calibrate **open / short / load at the BNC plane** where the aircraft plug mates,
not at the SMA port. Sweep 100–350 MHz.

| Frequency | Healthy | Note |
|---|---|---|
| 108–118 MHz | SWR < 2:1 | Archer's own spec |
| 328.6–335.4 MHz | SWR 4:1 to 6:1 | **Normal for a stock Archer.** Bob never designed for GS. A GTN 650 works fine with this. |

Do not chase the glideslope number in Phase 2. A measured 5:1 at 330 MHz is the
expected stock behaviour, not evidence of a fault.

## 2.3 Distance to fault

NanoVNA-H4: Display → Transform → Low Pass Impulse. Set velocity factor
**0.695** for RG-400. Each connector shows as a small bump. A large bump tells
you which floor panel to pull:

- A reflection at the wing-root distance → the inline BNC at the root
- A reflection at the far end → the antenna feed
- A reflection near zero → the connector in your hand

## 2.4 Cable loss, the unambiguous test

Disconnect both ends, jumper the antenna end, measure **S21** through the run.

| Frequency | ~20 ft RG-400 should read |
|---|---|
| 113 MHz | ≈ 0.7 dB |
| 330 MHz | ≈ 1.2 dB |

Several dB means the cable or a connector is eating the signal, and that is your
answer. This is the test that would have caught the VAF case where a new BNC
crimp had a short inside it that passed VOR and localizer but killed glideslope.

## 2.5 Hand it to me

Capture each measurement with `scripts/vna_capture.py` rather than photographing
the screen, then hand me the `.s1p` files:

```bash
uv run --with pyserial python3 scripts/vna_capture.py --band both \
    --out ~/vna/$(date +%F)-<what-this-is>.s1p --note "..."
```

`scripts/vna_analyze.py` takes several files at once and overlays them, which is
how you see a fix working rather than remembering that it felt better.

---

# Phase 3 — Is the antenna actually deaf?

Only meaningful after Phase 1 establishes a noise baseline.

**Simple version, uses gear you have.** Same station, back to back, lights off:
measure C/N on the aircraft antenna, then on the SDR's own dipole held at the
wingtip, horizontal.

```bash
uv run python3 scripts/rf_survey.py --config aircraft --carrier 113.8 \
    --point coax --outdir ~/rf-survey/$(date +%F)-ab
uv run python3 scripts/rf_survey.py --config reference --carrier 113.8 \
    --point ref  --outdir ~/rf-survey/$(date +%F)-ab
```

A few dB apart is normal — the dipole is a fair antenna and the Archer is not
optimally placed. **Twenty dB down says the aircraft path is eating the signal**
and sends you back to Phase 2.

**Rigorous version.** NanoVNA S21 over the air: CH0 to a reference antenna a few
metres away, CH1 to the aircraft coax, sweep the nav band. Then repeat with a
known dipole in the wingtip position. The difference is antenna gain, measured
properly. Dynamic range is adequate below 300 MHz at short range.

---

# Phase 4 — Flight validation

Before touching anything, fly the protocol so there is a before picture:

1. Pick a station at **moderate** range where signal is not overwhelming. The
   10 DME Kremmling arc is a known-bad data point and a good repeat.
2. Lights off. Note ident clarity, CDI steadiness, and **which** identifier field
   is showing — the one **above** the frequency is decoded from received Morse;
   the one **below** comes from GPS and the database and appears with no signal
   at all.
3. Add NAV, then STROBE, then wig-wag, 30 seconds each. Note what changes and when.
4. Repeat after each fix.

Ignore anything observed directly overhead a VOR. That is the cone of confusion
and it misbehaves on every airplane.

---

# Phase 5 — Fix and rebuild

Ordered cheapest-and-most-likely first. Re-measure after each step; stop when the
airplane is good.

## 5.1 Ground the antenna properly

The single highest-prior fix. Either bond the base leg to the outboard rib with a
short strap and two screws, or mount the antenna on a piece of 0.063 aluminium
angle screwed to the rib so the wingtip slides off over it. Do **not** rely on the
piano hinge. Carl Froehlich's caution applies: this wants a couple of clean
screws, not a rib sanded to bare metal — the antenna needs a counterpoise, not a
battery ground.

## 5.2 Lighting fixes (if Surveys A/B justify them)

- Ground the lights at the **wing root or firewall**, never at the wingtip.
  N720AK currently grounds the Pulsar via its mounting screw *and* carries a
  shield ground — that is two paths, which is the ground-loop pattern owners kept
  finding. Confirm what is actually connected when the tip is off.
- Three-conductor shielded 18 AWG in the wing, third conductor as a real ground
  rather than the shield.
- Aluminium backing plate behind the Pulsar, bonded through its mounting screws.
- Light wires off the antenna elements entirely, routed along the end rib.
- AeroLEDs support has a track record of helping directly with this.

## 5.3 Ignition and charging suppression (if Survey D justifies it)

Only if the engine-running survey points here. In rough order of effort:

- **Plug wires and boots.** Unsuppressed wires on an electronic ignition radiate
  broadband across VHF. Confirm resistor plugs are installed and that wires,
  terminals and boots are sound — already an annual item in the EFII inspection
  schedule. Route them as far from the wing leading edge as the installation
  allows.
- **Coil pack grounding.** Terminal corrosion and loose mounts are on the 50-hour
  list for a reason; a coil pack grounding through a marginal bolted joint is an
  antenna.
- **Keep Hall crank sensor cables clear of plug wires.** EFII's own guidance is a
  minimum of one inch and never tie-wrapped together. That rule exists to protect
  the ECU, but the same coupling is what puts ignition noise on other wiring.
- **Alternator field.** A capacitor across the field lead and clean bonding of
  the alternator and regulator cases are the standard fixes for charging-system
  whine.

## 5.4 Tidy the feed

Short pigtails, coax leaving the lugs at 90° to the elements, secured so it cannot
flop, bend radius no tighter than 2 inches. Braid lug to the base structure,
centre lug to the small gamma stub only.

## 5.5 Build a better antenna — last, not first

Only after the above, and only if measurements justify it. Base drawing is
**AeroElectric Connection Figure 13-12**, 0.025 aluminium throughout:

| Part | Dimension |
|---|---|
| Angled leg, rib to elbow | 1.5 × 11.7 in |
| Long arm, elbow aft | 1.5 × 16.5 in |
| Triangle side | 5.0 in, 60° corners |
| Gamma stub (aft triangle leg) | 0.8 × 6.2 in |
| Gap in that leg | 0.31 in |
| Capacitor plate | 0.8 × 2.5 in |
| Dielectric | 0.032 × 0.8 × 3.25 in bakelite |
| Hardware | 4-40 brass feed lugs, two 10-32 nylon screws |

Two proven improvements on top of it:

- **Extend to fill the tip.** Lengthen the angled leg toward the outboard edge
  and shorten the aft leg by the same amount, gamma triangle unchanged. Owners
  doing this report VOR at 90–100 nm.
- **Glideslope stub.** A 6 mm wide strip, 17.1 cm from the centreline of the
  pickup strip, replacing the small cable hookup plate. Measured 8.7:1 → 1.5:1
  at 333.5 MHz with no penalty at 113 MHz. Only worth it if Phase 2 shows the
  glideslope is actually marginal — a GTN 650 generally does not need it.

**Tuning procedure** (needs the VNA, cutting is one-way):

1. Build the arm an inch or two long.
2. Analyzer at the feed point. Find the SWR minimum.
3. Trim the tail of the long arm to move resonance up to ~110 MHz.
4. Adjust the gamma capacitor — loosening the nylon screws reduces capacitance.
   Watch which direction lowers SWR, then trim the plate accordingly. Iterative,
   takes minutes.
5. Trim overall length for minimum SWR at ~113 MHz.
6. Verify with the wingtip on and the real coax back to the radio.

---

## Where I plug in

| You | Me |
|---|---|
| Run `rf_survey.py`, give me the directory | Run the analysis, read the plots, tell you which system is guilty and by how many dB |
| Multimeter readings, read aloud or typed | Compare against expected, say which is out |
| `.s1p` files off the NanoVNA SD card | Plot, overlay the bands, compare to stock-Archer reference |
| Flight notes from the Phase 4 protocol | Correlate with the ground data |
| Photos of the wingtip with the tip off | Check routing and grounding against the install rules |

## Files

- SDR capture driver: `scripts/rf_survey.py`
- SDR analysis: `scripts/rf_analyze.py`
- NanoVNA capture: `scripts/vna_capture.py`
- NanoVNA analysis: `scripts/vna_analyze.py`
- This plan: `plans/vor-antenna-diagnostic.md`
- Antenna reference and links: `sections/sys-23-communications.md`
- Lighting wiring: `sections/sys-33-lighting.md`
- Ignition and fuel injection: `sections/sys-73-efii.md`
- Buses, alternator, MZ-30: `sections/sys-24-electrical.md`
