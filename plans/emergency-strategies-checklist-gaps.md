# Emergency Strategies vs. the N720AK checklists — gap analysis

**Source:** PilotWorkshops, *Emergency Strategies: A Pilot-Friendly Manual* v1.1
(2023). GDrive `Private/Training-Manuals/`. 11 strategies, ~30 worked scenarios.
**Compared against:** `N720AK.json` as of 2026-09-14 — 12 groups, 58 checklists.

The book is a book of *decisions*, not procedures, so most of it does not belong
in a checklist at all. This document records the comparison anyway, because the
places where a decision book and a procedure set disagree are exactly where a
checklist is quietly wrong.

**Headline:** the N720AK set is in better shape than the book's own examples —
it is already EFII-specific, it already uses this book's REACT mnemonic in the
takeoff briefing, and its fire checklists reason about the dual-path electrical
architecture in a way no generic checklist does. Seven real gaps came out of the
comparison, one of which is a **numerical error** in a forced-landing checklist.

---

## The one actual error

**`Forced Landings / Emergency Landing Without Engine Power`** says:

> Wing Flaps ... **AS REQUIRED — 40º RECOMMENDED**

**N720AK has no 40° flap position.** Full flaps are **33°**
(`sys-27-flight-controls.md`: "Flap positions range from reflex (-3°) to full
(33°)"; §2 Limitations lists V~S0~ at 33° and V~FE~ full-flap as 87 KIAS). Every
other checklist in the file says 33° — `Normal Landing`, `Short Field Landing`,
`Precautionary Landing`, and the short-final note inside `Engine Failure
Immediately After Takeoff`. The 40° is a stale number from a generic source, and
it sits in the one checklist where a pilot is most likely to be reading rather
than remembering.

---

## The systemic gap: N720AK's emergency configurations have no flaps, and no
## checklist says so

This is the finding the comparison was worth doing for. Three separate facts
compose into it, and each one is documented in a different file:

1. **Flaps are electric and live on the main bus.** `sys-24-electrical.md`,
   essential-bus walkthrough: "Main-bus loss also kills flaps, electric trim (AP
   panel), and pitot heat."
2. **The flap switch has a 90 KIAS speed inhibit** (`sys-27`, `08-systems.md`).
3. **Best glide is 95 KIAS** (§2 Limitations, V~G~).

So:

- Any checklist that ends with the airplane dark — `Engine Fire In Flight`
  (Key OFF + E-PWR OFF), `Electrical Fire / Smoke In Cockpit` (same), the
  post-shed state of `Bus Manager Failure` — has **committed the pilot to a
  no-flap landing**, and none of the three says it. V~S1~ flaps-up is 61 KIAS
  against 48 KIAS at 33°: a materially faster, longer, flatter arrival that
  wants a different runway choice.
- In *any* power-off glide, **flaps are unavailable at best glide speed**,
  because 95 KIAS is above the 90 KIAS inhibit. "Wing Flaps — AS REQUIRED" is
  not actionable until the airplane is slowed below 90. The book's own scenario
  (p. 24) leans on "an extension of full flaps right at the end to cushion your
  landing"; on N720AK that is a two-step move with a speed gate in front of it.

---

## Strategy-by-strategy

| # | Strategy | N720AK coverage | Verdict |
|---|---|---|---|
| 1 | Power Loss Down Low | `Engine Failure During Takeoff Run`, `…Immediately After Takeoff`, `Turnback Procedure`, REACT in `Before Takeoff` | **Strong.** Better than the book's: the turnback is AoA-referenced (ONSPEED) rather than airspeed-referenced, which is the correct answer to the book's own worry that bank and G move the stall number mid-maneuver. |
| 2 | Power Loss Up High | `Engine Failure In Flight`, `System32 Restore Function` | **Strong.** The book's fuel-air-spark flow maps onto System32 Restore. |
| 3 | Fire | five checklists | **Strong, and more specific than the book.** |
| 4 | Flight Upset | `Upset Recovery — Power/Push/Roll`, `Spin Recovery — PARE` | Adequate. Gap: no *graveyard spiral* item (below). |
| 5 | Flight Control Malfunction | `Runaway Trim`, `Landing Without Elevator Control` | Adequate. See the split-flap note under "deliberate skips". |
| 6 | Non-Powerplant System Failure | `Primary Alternator Failure`, `MZ-30 Generator Failure`, `Bus Manager Failure`, `Static Source Blockage` | **Gap: no pitot/airspeed failure checklist** (below). **Gap: no autopilot-malfunction checklist** (below). |
| 7 | Unplanned Instrument Flight | `180º Turn In Clouds`, `Emergency Descent Through Clouds` | Adequate. |
| 8 | Pilot/Passenger Impairment | `CO Alarm In Flight`, `Oxygen System Failure / Hypoxia` | Adequate. Minor gap: nothing says a medical event should be *declared*. |
| 9 | Dangerous Distraction | `Door Open In Flight` | Adequate. Gap: the post-interruption rule (below). |
| 10 | Landing Complication | `Landing With A Flat Main Tire`, `Go Around` | **Gap: no brake failure checklist** (below). |
| 11 | Unavoidable Crash | `Emergency Landing Without Engine Power`, `Ditching` | Adequate. Open question: ELT activation (below). |

---

## Proposed changes, in priority order

### 1. Fix the 40° flap error → 33°
One-word correction. `Emergency Landing Without Engine Power`.

### 2. New checklist — `Unreliable Airspeed / Pitot Blockage` (Abnormal)
The largest genuine hole. `Static Source Blockage` exists; its twin does not,
and on this airplane the pitot side is by far the worse failure.
`sys-34-navigation.md` §"The Pitot/AoA Probe Is the Single Point of Failure"
establishes why:

- **One probe, no redundancy.** Static is dual (two aft-fuselage ports); pitot
  and AoA are a single probe under the left wing.
- **Both ADAHRS breathe through it, so they agree on the bad data** and raise
  **no `ADAHRS CROSS CHK ERROR`**. The cross-check catches a *unit* failing, not
  a *shared source* being wrong. A pilot trained on the book's "Triangles of
  Agreement" will take two agreeing ADAHRS as confirmation. That is backwards.
- **It takes four things at once**: airspeed, Dynon AoA, OnSpeed audio, and the
  AoA-derived stall warning. N720AK's normal procedures are built on ONSPEED —
  `Normal Takeoff`, `Turnback`, `Go Around`, `Short Field Landing` and the
  memory items all cue off the tone. A pitot blockage removes the airplane's
  primary reference, and nothing currently tells the pilot that.
- **Attitude degrades too.** Per Dynon's install guide, the SkyView attitude
  solution *uses* airspeed and falls back to GPS. So the answer is GPS, not the
  second ADAHRS.
- **The alternate static valve does not help.** It is the wrong system.

### 3. Add the no-flap consequence to the dark-airplane checklists
A single `ITEM_WARNING` on `Engine Fire In Flight`, `Electrical Fire / Smoke In
Cockpit`, and `Bus Manager Failure`, plus a speed-gate note on the forced-landing
checklists. See the systemic gap above.

### 4. New checklist — `Brake Failure` (Non-Standard Takeoff and Landing)
Fully transferable from the book (pp. 112–113) — the gear-retraction half of
that chapter is moot on fixed gear but the brake half is not. N720AK has
independent pilot/co-pilot toe brakes on hydraulic discs, so a *total* loss is
most likely a fluid/line failure rather than a single master cylinder; a
one-side failure is the more likely case and is a directional-control problem on
rollout. Existing coverage is `Landing With A Flat Main Tire`, which is a
different failure.

### 5. New checklist — `Autopilot Malfunction` (Abnormal)
The book's doctrine — **downgrade a level of automation before disengaging** —
is a better fit for N720AK than for its own examples, because Dynon gives an
extra rung the book never mentions: **Control Wheel Steering** (hold the stick
disconnect, fly it, release, the AP holds the new state). And N720AK has a
*documented, specific* instance of the book's scenario:
`sys-22-autopilot.md` §"Known Quirk: Silent TRK Reversion on Localizer Signal
Loss" — a coupled localizer drops NAV → **TRK with no alert**, and does not
recapture when the signal returns. A misbehaving autopilot on this airplane has
a named first suspect.

### 6. Add the post-interruption rule to `Before Takeoff`
Book p. 102: the hidden danger of a distraction is not the distraction, it is
the *oversight it causes later* by breaking a flow. One `ITEM_NOTE`.

### 7. Add a graveyard-spiral cue to `Upset Recovery`
Book p. 55: **"just let go" is not a recovery for a spiral** — releasing back
pressure in a spiral tightens the descent. The existing Power/Push/Roll sequence
is correct for a spiral; what is missing is the *recognition* that this is a
spiral and not a spin, and the warning against the hands-off reflex.

---

## Open questions for Sam

1. **ELT.** `Emergency Landing Without Engine Power` and `Ditching` both squawk
   7700 and call mayday, but neither activates the ELT. N720AK carries an Artex
   ELT 345 (406 MHz) — but the panel-switch inventory in `08-systems.md` does
   not list an ELT remote switch, so I can't tell whether there is one to flip.
   *Is there a remote ELT switch on the panel?* If yes, it is a one-line
   addition to both checklists.
2. **Performance profiles.** The `Unreliable Airspeed` checklist is only useful
   if it can say "set this power, this pitch, this configuration." The book's
   worksheet (p. 79) is exactly that table and N720AK does not have one. The
   numbers have to come from flight data or from Sam — **they must not be
   invented.** The proposed checklist therefore points at a table rather than
   containing one, and building that table is a separate task (a good use of the
   `flight-data-analysis` skill against existing Dynon logs).
3. **REACT's "E".** The book's version of the Engine-gauges check (p. 21) singles
   out **fuel flow** as the most-overlooked abort cue, with a sea-level estimate
   of HP ÷ 11 for engines over 200 HP — about 23–24 GPH for the IO-540. The
   current briefing says only "Engine gauges — GREEN". *Do you want the actual
   observed full-power fuel flow written in as a number?* I did not add one
   because I would be guessing at N720AK's real figure.

---

## Deliberate skips — recorded so the next pass does not re-litigate them

| Book content | Why skipped |
|---|---|
| Split flaps (pp. 66–69) | Single PHA-09P actuator drives both flaps through one weldment. Asymmetric deployment is not a system failure mode on this airframe; it would take a structural pushrod/hinge failure. |
| Landing gear won't extend (pp. 108–111) | Fixed gear. |
| Carb heat / carb ice (pp. 21, 34) | No carburetor — EFII port injection. |
| Mixture-based restart and leaning items | No mixture control. |
| Magneto checks, "bumped the ignition to OFF" (p. 25) | No magnetos. The ECU p-lead check in `Runup` is the analogue and already exists. |
| Airframe parachute (p. 12) | Not installed. |
| Turn It All Off load-shed strategy (p. 75) | **Actively dangerous here.** The book's master-off-then-on trick assumes a magneto engine. On N720AK, key-off stops the engine unless EMERGENCY POWER is on *first*. The existing checklists already have the correct ordering; the point is that the book's version must never be carried over. |
