# Plan: N720AK COM1 Diagnostic

Companion to `plans/vor-antenna-diagnostic.md`. Read that first — the
measurement discipline carries over. What does **not** carry over is the
safety model, because a COM antenna is fed by a transmitter.

## The symptom

COM1 receives badly — "almost unusable." Established by an A/B in the
airplane: both radios powered and tuned, COM2 receiving normally, COM1
getting nothing.

Two facts shape the whole approach:

- **It is recurring, not new.** It has happened before. Whatever is wrong is
  intermittent, so a test that passes once proves very little, and a fix that
  works today needs to be durable rather than a reseat.
- **A COM1 coax barrel was disconnected and reconnected** during the nav
  antenna work on 2026-09-16, immediately before this episode.

Connectors are the running theme on this airframe. The nav antenna improved
after its coax was reseated at the GTN during the same session. Weight that
accordingly: a marginal BNC that gets better or worse when disturbed fits
every observation on both radios.

## Safety — the part that differs from the nav work

**COM transmits at roughly 10 W.** That is +40 dBm into the feedline.

- **Never** have the SDR or the NanoVNA connected to an antenna that is then
  transmitted into. It destroys an RTL-SDR front end instantly and can take
  out the VNA's bridge.
- Physically **disconnect and stow** test gear before any transmit test.
  Not "set aside" — disconnected.
- Brief anyone in or near the cockpit. One absent-minded push-to-talk ends
  the session and the dongle.
- The nav plan's "don't key a COM" note was a footnote. Here it is the
  central constraint.

---

# Phase 0 — Establish what is actually connected to what

Do not measure anything until this is settled. Getting it wrong invalidates
everything downstream.

1. **Which radio is "COM1"** — the GTN 650's com, or the Dynon SV-COM-425?
2. **Which antenna does it feed?** `sections/sys-23-communications.md`
   records COM1 on a Comant **CI-121** on top of the fuselage and COM2 on a
   **CI-122** under the right wing. Trace the coax and confirm. The repo may
   be wrong, and this is the kind of detail that gets recorded once during a
   build and never checked.
3. **Where was the barrel that got disturbed?** Behind the panel at the radio
   end, or out at the wing root? The nav work was happening at the GTN, which
   makes the radio end more likely, but confirm rather than assume.
4. **Is it actually reconnected and seated?** BNC connectors feel mated
   before they lock. Twist to the detent and tug.

Record the answers in `sections/sys-23-communications.md` — if the existing
mapping is wrong, that is a finding in itself and the next person deserves
the corrected version.

---

# Phase 1 — The swap test, then DC

## 1.1 Swap the two coax at the radio end

**Do this first.** It is free, takes two minutes, and it is the single most
decisive test available.

Connect COM1's radio to COM2's antenna feedline and vice versa, then listen
on both.

| Result | Conclusion |
|---|---|
| Fault **follows the cable** — COM1's radio now works, COM2's doesn't | Antenna or feedline. Continue to Phase 2. |
| Fault **stays with the radio** — COM1's radio still bad on the good antenna | The radio. Everything downstream is moot. |
| Both work fine after the swap | You just reseated two connectors. **This is the intermittent fault.** Go to Phase 1.2 and find which joint. |

That third outcome is the likely one given the history, and it is the most
important to recognize rather than celebrate. "It works now" after
disturbing connectors is a reproduction of the fault, not a repair.

## 1.2 Multimeter, every connector in the run

Coax disconnected at **both** ends. Zero the leads first — short the probes,
note the reading, subtract it from everything below. On this airplane the
leads read a few tenths of an ohm and that matters at these levels.

| Probes | Expect | A failure means |
|---|---|---|
| Centre ↔ shield | open | A short — crushed coax or a shorted connector |
| Centre end-to-end | < 1 Ω | Open: broken centre conductor or an unseated pin |
| Shield end-to-end | < 1 Ω | Open: broken braid or a bad crimp |
| Shield ↔ airframe at the antenna end | < 1 Ω | The whip's flange bonds to the skin; high means a mounting problem |

A Comant whip is a base-fed monopole, so **centre-to-shield reads open** at
DC. Note the actual value rather than just "open" — a few hundred kΩ is
different from infinite and worth recording.

**Wiggle everything while watching.** A steady bad reading is a fault. A
reading that jumps when you flex a connector is *this* fault. Spend real
time here: work along the run, flex the cable near each backshell, and
watch for the needle moving. Intermittents are found by provocation, not by
a single clean reading.

Known-good reference on this airplane: the CI-122's shield reads **0.1–0.3 Ω**
to airframe. That is what a proper flange bond looks like on this meter.

---

# Phase 2 — NanoVNA

**On a COM antenna the VNA is the primary instrument**, which is the opposite
of the nav case. A transmitting antenna's match determines how much power
actually radiates, so SWR is genuinely diagnostic here rather than the
near-useless screening tool it was on the Archer.

## 2.1 Sweep

Calibrate over the sweep range first, with the BNC adapter fitted, then:

```bash
uv run --with pyserial python3 scripts/vna_capture.py --band com \
    --out ~/vna/$(date +%F)-com1.s1p --note "COM1 at the radio end"

uv run --with numpy --with matplotlib python3 scripts/vna_analyze.py \
    --bands com ~/vna/$(date +%F)-com1.s1p
```

| Frequency | Healthy Comant whip |
|---|---|
| 118–137 MHz | SWR under 2:1 across the band |
| ~127 MHz | typically 1.1–1.5 |

## 2.2 A/B against COM2 — the strongest measurement available

You have two com antennas on the same airframe, same coax type, same
environment. Sweep both and overlay them:

```bash
uv run --with pyserial python3 scripts/vna_capture.py --band com \
    --out ~/vna/$(date +%F)-com2.s1p --note "COM2 at the radio end"

uv run --with numpy --with matplotlib python3 scripts/vna_analyze.py \
    --bands com ~/vna/$(date +%F)-com1.s1p ~/vna/$(date +%F)-com2.s1p
```

A same-airplane control beats an absolute number. If COM2 sweeps clean and
COM1 doesn't, that is close to conclusive.

## 2.3 Wiggle while sweeping

Put the VNA in continuous sweep and flex each connector and the cable near
the backshells while watching the trace. On an intermittent this finds the
joint faster than any static measurement.

## 2.4 Distance to fault, and cable loss

Time domain: Display → Transform, velocity factor **0.695** for RG-400. Each
connector shows as a bump; a large one tells you which panel to pull.

Then the unambiguous test — disconnect both ends, jumper the far end, measure
**S21** through the run. About 20 ft of RG-400 should lose roughly **0.8 dB at
127 MHz**. Several decibels means the cable or a connector is eating your
signal and you are done looking.

---

# Phase 3 — Quantify "barely working" with the SDR

Receive only. Puts a number in decibels on what is currently a subjective
complaint, and gives a baseline to prove the fix against.

Gain must be recalibrated for this location and this antenna — the nav work
established that the right gain moves substantially between a hangar and a
desk, and between antennas:

```bash
uv run python3 scripts/rf_survey.py --gain-sweep --band com \
    --point coax --outdir ~/rf-survey/gain-com
uv run --with numpy --with matplotlib python3 scripts/rf_analyze.py \
    --gain-check ~/rf-survey/gain-com
```

Then measure carrier-to-noise on a strong steady signal — a nearby ATIS or
AWOS is ideal because it transmits continuously:

```bash
uv run python3 scripts/rf_survey.py --config com1 --carrier <ATIS_MHZ> \
    --point coax --gain <FROM_ABOVE> --duration 30 \
    --outdir ~/rf-survey/$(date +%F)-com-ab
```

Repeat with `--config com2` on the other feedline, and `--config reference`
on the telescopic antenna. Three numbers, same station, minutes apart.

A few dB between COM1 and COM2 is normal — different antennas, different
locations on the airframe. **Twenty dB down is your answer.**

---

# Phase 4 — Transmit

**All test gear disconnected and stowed before anything is keyed.**

## 4.1 The easy version, and usually enough

A real radio check. Ground, tower, or another aircraft at a known distance,
on COM1 and then COM2, back to back. Or park the FTA-850 handheld some
distance away and listen to yourself on both radios.

Qualitative, but a transmitter that is genuinely broken is not subtle.

## 4.2 The quantitative version — read the numbers before setting this up

If you want it in decibels, the SDR can measure your own transmission. The
hazard is real, so here is the arithmetic rather than a rule of thumb.

At 10 W (+40 dBm) and 127 MHz, with roughly omnidirectional antennas at both
ends:

| Distance | Received power | Verdict |
|---|---|---|
| 50 m | −8.5 dBm | **Too hot. Do not.** |
| 100 m | −14.5 dBm | Marginal even at minimum gain |
| **200 m** | **−20.5 dBm** | Workable at gain 0.0 |
| 400 m | −26.5 dBm | Comfortable |

Rules for this test:

- **200 m minimum**, further is better.
- **`--gain 0.0`.** Not low. Zero.
- Transmissions of **2–3 seconds**, no more.
- A 20 dB inline attenuator, if you have one, buys margin for free.
- The SDR is on its **own telescopic antenna**, never the aircraft's.

Then transmit on COM1 and COM2 in turn on the same frequency and compare
received level. That is a direct radiated-power comparison, and the
difference is the number that matters.

---

# Phase 5 — Fix

Whatever is found, the fix has to survive vibration and heat cycling, because
this fault has already come and gone more than once.

- **A marginal BNC** gets replaced, not reseated. Re-terminate with a proper
  crimp, confirm the centre pin seats to its detent, and check the braid
  termination. An RV builder on VAF cut a centre conductor slightly short, the
  pin failed to latch, and it made intermittent contact that passed every
  static test.
- **Secure every barrel** so it cannot swing. Adhesive-lined heat shrink over
  the body, plus a cushioned clamp anchoring it. Tape unwraps and goes gummy;
  an unsecured connector chafes through whatever you put on it.
- **Keep COM and NAV barrels apart.** They were found in contact at the right
  wing root on 2026-09-16 and were separated and secured the same day. Closed,
  and unrelated to COM 1 — that run does not pass through the wing root.
- Re-measure after the fix, against the Phase 3 numbers, and fly it before
  calling it closed.

---

## Running this interactively

The nav survey worked well driven turn by turn: the agent issues one step,
the owner sets switches or moves probes and reports back, the agent runs the
capture and interprets before naming the next step. Keep that pattern.

Two things that mattered in practice:

- **Say what changes and what must not move.** Most of the measurement error
  available here comes from something shifting between captures.
- **Interpret each result before moving on.** The nav survey's most useful
  moment came from noticing mid-run that a spur was uncorrelated with the
  switches, which redirected everything that followed.

## Files

- This plan: `plans/com-antenna-diagnostic.md`
- Nav companion: `plans/vor-antenna-diagnostic.md`
- Capture and analysis: `scripts/rf_survey.py`, `scripts/rf_analyze.py`,
  `scripts/vna_capture.py`, `scripts/vna_analyze.py`
- Antennas and wiring: `sections/sys-23-communications.md`
- Radios: `sections/sys-42-avionics.md`
