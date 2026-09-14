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

1. **Performance profiles.** The `Unreliable Airspeed` checklist is only useful
   if it can say "set this power, this pitch, this configuration." The book's
   worksheet (p. 79) is exactly that table and N720AK does not have one. The
   numbers have to come from flight data or from Sam — **they must not be
   invented.** The proposed checklist therefore points at a table rather than
   containing one, and building that table is a separate task (a good use of the
   `flight-data-analysis` skill against existing Dynon logs).
2. **REACT's "E".** The book's version of the Engine-gauges check (p. 21) singles
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

---

## Resolved: the ELT switch exists

Sam confirmed a panel ELT remote switch (2026-09-14). `Emergency Landing Without
Engine Power` and `Ditching` now activate it right after the 7700 squawk, and
both `08-systems.md` and `sys-23-communications.md` record the switch — it was
absent from the panel inventory, which is why the question had to be asked.

The reason it goes early and high rather than at touchdown: a crash g-switch
fires only about half the time (p. 116) — some beacons fail to activate, but
more are separated from their antennas, buried or burned. Squawk plus ELT is
about four seconds (p. 117). N720AK's ADS-B Out is transmitting GPS position
independently, which helps, but it stops at impact and the ELT does not.

Added with it: a note to turn the ELT **off** and notify ATC or the AFRCC after
walking away from a landing. An un-cancelled 406 alert launches a search.

Still open: **is the ELT 345 fed a GPS position?** The Embry-Riddle data in the
book (p. 117) puts the mean search at **11.8 hours** for a 406 ELT without GPS
aiding and **two hours** with it. If it is not wired for position, that is worth
fixing. Logged as a TODO in `sys-23-communications.md`.

---

## UNRESOLVED — a life-safety conflict between two sources Sam already owns

**Five in-flight checklists say `Doors ... UNLATCH PRIOR TO TOUCHDOWN`:** Engine
Failure Immediately After Takeoff, Engine Failure On Approach, Emergency Landing
Without Engine Power, Precautionary Landing With Engine Power, and Ditching.

The two authorities disagree, and they disagree *specifically about gull-wing
doors*:

| Source | Says |
|---|---|
| **Stowell**, *Emergency Maneuver Training*, pp. 174–175, 186 | Unlatch before an off-airport touchdown — a deformed fuselage can jam a latched door over your only exit. If there is time for exactly **one** set-up item, make it this one. Wedge the gap so it cannot relatch. |
| **PilotWorkshops**, *Emergency Strategies* v1.1, p. 117 | "Unlatching the cabin doors prior to touchdown makes them less likely to jam shut. However, some POHs have guidance otherwise. **Gull-wing doors and some canopies are better left shut.** … the forces are substantial." |

**The checklists currently follow Stowell, and I did not change them.** Stowell
gives a mechanism (jamming) and PilotWorkshops gives none — it asserts the
gull-wing exception in one clause with no reasoning and no citation. Flipping
five emergency checklists on an unreasoned sentence would be worse than leaving
them. But it is not nothing either: an RV-10 door hinges forward at the top and
opens *upward*, so the failure modes an unlatched one can produce (departing in
the flare, or standing open across the egress path after a rollover) are not the
failure modes Stowell is reasoning about with a conventional side door.

**This needs an answer from a source that knows the RV-10 specifically** — Van's,
the type club, or an RV-10 accident review. Until then the checklists stay as
they are, and this note exists so the next pass does not silently adopt either
side.

---

## The turnback: TLAR and ONSPEED, not an altitude number

I first read `Turnback Procedure`'s *"Below 200 ft AGL, turnback is
non-recoverable"* as a gap — the book gives a method for deriving a briefed
altitude (measure at altitude with perfect form, add 50 %, gate above that;
~800 ft → 1200 AGL for a 172) and N720AK had no such number. I proposed deriving
one.

**Sam's call: no. TLAR, flown at ONSPEED.** A fixed altitude gate "just won't
really work," and the FlyONSPEED engine-out material is the reason:

> maintain ONSPEED and fly the airplane to the crash

ONSPEED holds **best sustained turn rate and smallest sustained turn radius**,
and the AoA that does it is the *same* AoA regardless of weight, density altitude
or G. An altitude number is a proxy that is valid at one weight, one wind, one
lateral offset and one runway — which is exactly the set of things that are
different on every takeoff. FlyONSPEED declines to give a decision altitude at
all: it is "airplane dependent" and "can only be determined by practice."

So the checklist was already the right shape — `Pitch … ONSPEED IMMEDIATELY`,
and `above turnback altitude / per TLAR` in Engine Failure Immediately After
Takeoff. Two things were added rather than a number:

1. **200 ft is a floor, not a gate**, with the reason ONSPEED is what makes a
   TLAR call workable. Under stress a lone "non-recoverable below 200" reads as
   permission above it.
2. **FlyONSPEED's fallback, which was missing**: *if there is any doubt about the
   energy to reach the runway, turn into the wind and slow to ONSPEED* — framed
   as the maneuver rather than as giving up on the good one.

The book's derive-a-number method still earns its cards, because it is right for
the airplanes Sam rents and for the commercial ride. It is just not how this
airplane is flown.

Source: [FlyONSPEED, Using AOA for Emergency
Maneuvering](https://www.flyonspeed.org/using-aoa-for-em-engine-out).

One thing worth noting for a later pass: FlyONSPEED calls for **"lift" flaps**
(takeoff setting, else half or less) during the turn-back, and N720AK's checklist
does not mention flaps in the turn at all. At ONSPEED with 16° the airplane is
below the 90 KIAS flap inhibit, so they are available there — unlike the clean
95 KIAS best-glide case elsewhere in this document. Not changed here; it wants
Sam's judgement and probably a flight.
