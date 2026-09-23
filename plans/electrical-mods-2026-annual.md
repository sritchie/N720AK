# Electrical modifications — 2026 annual

A task plan to run against, not a design document. The design is in
[`sections/sys-24-electrical.md`](../sections/sys-24-electrical.md); the *why*
behind the emergency-bus work was settled 2026-08-29 and re-confirmed
2026-09-22.

**The goal in one sentence:** make the main-bus-shed state IFR-capable, so a
main-side failure degrades automatically to engine + PFD 1 + GTN + audio +
transponder rather than to engine + PFD 1 alone.

**Load budget.** Essential today is ~14–16 A (engine 10–13, PFD 1 ~3). These
changes add ~3 A, landing at ~19–20 A. The MZ-30 makes 30 A at cruise, so it
carries that indefinitely — but only **15 A at 900–1000 RPM**, which is why the
shed ladder exists and why three of these circuits must be *pullable from the
seat*.

---

## Decisions locked before starting

Two were open on 2026-09-22 and are resolved here. Flip them if you disagree,
but flip them *before* Phase 4.

| Question | Decision | Why |
|---|---|---|
| AP panel on the SERVOS breaker? | **No — its own breaker** | The shed ladder pulls SERVOS to hand-fly and save ~1.5 A; sharing would kill electric trim exactly when hand-flying a long descent. The stick-grip red button already kills the servos instantly. Trim runaway is the failure with no instant kill, so it gets the dedicated breaker. Separate breakers give both kills. |
| Front USB onto the VPX? | **No** | The VPX is entirely main-bus, so a VPX-fed USB dies in the shed state and takes iPad charging with it. Leave it, or move it to an **essential** fuse. |

**No conflict on the buttons.** An earlier draft of this plan claimed IDENT and
the yaw damper had to compete for the single unused stick-grip button, because
it assumed both would land on SkyView *display* contact inputs. **That was
wrong** — see Phase 5. Both functions have their own dedicated, documented
inputs elsewhere, so the grip button goes to IDENT and the yaw damper gets its
own button wherever it fits.

---

## What gets a breaker, and what gets a fuse

**Partition by whether you would ever touch it in flight**, not by size or
importance. A shed-ladder item behind a hidden fuse is useless, because the
ladder only works if you can climb it from the seat.

**Pullable breakers, in the power panel** — the centre console where the
OnSpeed and engine items already live. No panel space up top, and these are
the three you actually pull:

| Breaker | Rating | Why it must be reachable |
|---|---|---|
| `AUDIO` | 5 A | Shed-ladder item, ~1.5 A. The GMA fail-safe still passes GTN COM 1 passively with it pulled. |
| `XPDR` | 3 A | Shed-ladder item, 0.7 A. |
| `AP PANEL` | 3 A | The runaway-trim kill, pulled independently of SERVOS. |

**Fuse block, behind the panel** — never touched in flight, so accessibility
only has to be good enough for the annual:

| Position | Circuit | Phase | Notes |
|---|---|---|---|
| 1 | `AV MSTR COIL` | 1 | ~300 mA, two relay coils |
| 2 | `ONSPEED` | 6 | the box itself, moved off the PFD circuit |
| 3 | `ONSPEED IDXR` | 6 | separate, so a fried LED line cannot take the tone |
| 4 | `USB FWD` | 7 | consolidated from its existing inline fuse |
| 5 | `GEN LED` | 5 | only if the MZ-30 lamp is buffered |
| 6–10 | spare | — | — |

Five of ten positions used, on a **SteinAir SA-303 ATO/ATC block**. The spare
capacity is the point: the next modification should not need a new fuse holder.
Standard ATC fuses, not minis, so spares are available anywhere.

**Neither bucket:** the IDENT button and the yaw-damper button are dry contacts
into dedicated device inputs — the transponder and the yaw servo respectively,
not the fuse block and not a breaker. Just wire and a button. The MZ-30 and CO
discretes need an **EMS general-purpose input**, which is its own problem —
Phase 5.

## Phase 0 — Verify before cutting anything

Nothing here changes the airplane. Do all of it first; two items could change
the plan.

- [ ] **Confirm the GTN root cause with a voltmeter.** EMERGENCY POWER on, key
      off. Expect: **Wht/Blk at the GTN relay coils dead**, while the COM 1 and
      NAV 1 breaker *outputs* are hot. That is the whole diagnosis — if the
      Wht/Blk is live, stop and re-trace before rewiring anything.
- [x] **Pitch servo pulley — Dynon TSB 080219. THE SERVO IS AFFECTED.** It is an
      **SV42T, P/N 101008-003, S/N 50220** (Sam, 2026-09-22), and 101008-003 is
      named in the bulletin's applicability list. The pulley reads as the
      unidirectional "wood-grain" texture, which condemns it whether or not a
      crack is present. Dynon Technical Support contacted 2026-09-22.
- [ ] **Repair the pitch servo — LA pulley assembly + shear screw kit.** Dynon
      is sending both (2026-09-22), so **S/N 50220 stays in the airplane** and no
      SkyView Network reconfiguration is needed. The hazard is *"a risk of
      interfering with the flight controls"*, so pulling the AP breaker is **not**
      a mitigation — this is still before-further-flight.
      **Check the new pulley is the crosshatch design before fitting it.**
      Castle nut **4 in-lb maximum** — the two Dynon documents disagree (4.5 vs
      4 in-lb); use the lower, newer figure, because over-torquing defeats the
      shear screw. New cotter pin **MS24665-210** every time, never reused.
      Stack order: pulley, nylon washer, wavy washer, castle nut AN310-5, cotter
      pin. If the shear screw is replaced, Loctite 271 needs **1 hour before
      flight**. Finish with `SETUP > HARDWARE CALIBRATION > AP SERVO CALIBRATION`
      and a tuning flight.
      Full procedure and part numbers: `sections/sys-22-autopilot.md`.
- [ ] Read the **roll** servo part number off its label to close it out. SV32 and
      SV42 are on the bulletin's *unaffected* list unless retrofitted with the
      Dynon linear actuator, and the roll servo installs per doc 101046-003, the
      capstan/pushrod kit — so it is almost certainly out of scope. Confirm,
      don't assume.
- [ ] **Photograph the SkyView VPX setup page** and record which channels are
      gated by **Switch Input #1**. This is the standing sys-24 TODO, and you
      need it to know what the AV MSTR actually still controls after Phase 1.
- [ ] **Identify the OnSpeed indexer LED** — forward voltage, current, and
      whether it is a bare LED or a pre-resistored 12 V unit. This sets the
      resistor value in Phase 6. A pre-resistored unit needs **no** series
      resistor.
- [ ] Confirm the panel cutout size of the existing essential-bus breakers so
      the three new ones match.
- [ ] **Audit the 13 EMS general-purpose inputs and write down what is on each.**
      They are reportedly full, and that single fact decides Phase 5: whether the
      MZ-30 and CO discretes get a freed pin, a resistor ladder, a second EMS
      module, or nothing. Nobody should be guessing at this by the time the
      panel is open.
- [ ] **Measure MZ-30 output pin 2 with the engine running, before wiring an
      LED to it.** The manual is explicit that behaviour was *reversed* partway
      through production: regulators shipped **before 12 June 2022 show 5 V when
      active and 0 V when inactive**; later units **pull to ground when active**,
      which is what makes them work with EFIS contact inputs. An LED wired for
      the wrong polarity simply never lights. Expect pull-to-ground.
- [ ] **Ask Monkworkz what pin 2 can sink.** The electrical ratings table gives
      only voltages — 0–5 VDC signal, 30 VDC maximum — and publishes **no
      current rating**, because the output is intended for a high-impedance EFIS
      contact input, not a lamp. See Phase 5 for what to do if they do not
      answer.

---

## Phase 1 — The GTN fix (one wire, highest value)

The GTN's COM 1 (10 A) and NAV 1 (7.5 A) breakers are already on the essential
bus. Power passes through two Bosch relays — COM at P1003-30/43/44, NAV at
P1001-19/20 and P4-51/52 — whose coils are held closed by the **AV MSTR** switch
through a **Wht/Blk** wire fed from the *main-bus* switch rail. Main bus dies,
coils drop, relays open, GTN goes dark behind hot breakers.

- [ ] Add a **1 A ATC blade fuse** on the new essential-bus fuse block, labelled
      `AV MSTR COIL`. 1 A is a standard ATC value — one of the reasons the block
      is ATC rather than MINI. <!-- TODO: SteinAir's listed low end is 3 A
      (SA-203); source 1 A ATC elsewhere if they do not stock it. -->
- [ ] Run **22 AWG** Tefzel from that fuse to the AV MSTR pole that feeds the
      Wht/Blk coil wire. Load is ~150 mA per coil, two coils.
- [ ] **Disconnect that pole's existing main-bus feed.** Both halves of this
      matter — adding the essential feed without removing the main feed leaves
      the main bus back-feeding through the switch.
- [ ] Keep this feed **independent of the VPX Switch Input #1 pole**. AV MSTR is
      DPDT doing two separate jobs; only the coil pole moves.
- [ ] **Verify:** EMERGENCY POWER on, key off → GTN powers up and holds.

---

## Phase 2 — Audio to essential (pullable breaker)

GMA 245 and the Bose LEMO jack power currently sit on **VPX J10-4 (channel
5A-9)**, which is main-bus.

- [ ] Install a **5 A pull-able breaker** labelled `AUDIO` in the power panel
      (centre console, where the OnSpeed and engine items live — no panel space
      up top).
- [ ] Feed it from the essential bus bar. **18 AWG** Tefzel.
- [ ] Move GMA 245 power and the Bose LEMO jack feed onto it.
- [ ] Remove the VPX J10-4 assignment so the channel is not left orphaned and
      live.
- [ ] **Do not share COM 1's breaker.** It destroys the GMA fail-safe's
      independence — one fault would kill the audio panel *and* the GTN com it
      fails over to — and it eats COM 1's transmit margin.
- [ ] **Verify:** audio works with AV MSTR **off** (useful for taxi tests), and
      in the shed state. Confirm the GMA fail-safe still passes GTN COM 1
      passively with the AUDIO breaker pulled.

Why audio matters enough to be on the ladder at all: **OnSpeed's AoA tone
reaches the headsets through the GMA.** A dead audio panel means no AoA tone on
an emergency approach.

---

## Phase 3 — Transponder / ADS-B

**VPX J10-7 (channel 5A-10)** feeds **SV-XPNDR-261 J1-15** and **SV-ADSB-470
J1-1**. Main-bus, so it dies in the shed state — which is exactly when being
visible to ATC matters most.

**DECIDED 2026-09-22: Option B, move it outright.** Sam's call — the VPX's
current monitoring is not worth keeping on this circuit, and moving it keeps the
transponder on the shed ladder where its 0.7 A can actually be given up. The
diode-OR alternative is recorded below only so nobody re-opens it.

- [ ] **3 A pull-able breaker** labelled `XPDR`, essential bus, **18 AWG**.
- [ ] Remove the VPX J10-7 assignment.
- [ ] No Schottky needed. *(Rejected Option A was: diode-OR from the essential
      bus into the existing VPX feed — keeps VPX monitoring, costs a diode drop
      off bus voltage, and leaves the circuit unsheddable.)*

Then:
- [ ] **Verify:** shed state → transponder replies and ADS-B Out still reports.
      Re-run a PAPR afterward to confirm nothing changed in the position source
      (the 2026-01-28 report was Link Version 2, no exceptions — that is the
      baseline to match).

---

## Phase 4 — AP panel / trim (pullable breaker)

- [ ] **3 A pull-able breaker** labelled `AP PANEL`, essential bus, **18 AWG**.
- [ ] Move SV-AP-PANEL and the electric trim feed onto it, off the VPX.
- [ ] **Keep it separate from SERVOS** — see the decision table.
- [ ] **Verify:** pulling `AP PANEL` stops a trim runaway while the autopilot
      servos remain available; pulling `SERVOS` stops the servos while electric
      trim remains available. Both must be true.
- [ ] Update the **Runaway Trim** checklist — it currently predates this breaker
      existing.

---

## Phase 5 — Discrete inputs and buttons

> **Correction, 2026-09-22.** An earlier version of this plan routed IDENT, the
> yaw damper and the MZ-30 annunciation to SkyView **display** contact inputs
> (D37 pins 28/27/14/15). **That was wrong.** Those four are not
> general-purpose. Per the SkyView System Installation Guide Rev AX: Contact
> Input **#1 is the External LEVEL button**, **#2 is the External GO AROUND
> button**, and **#3 and #4 "are currently not supported… Do not connect
> anything to these pins currently."** The guide also says not to connect
> anything to unspecified D37 pins at all. Display contacts cannot raise a
> configurable alert, and there are no nine spare inputs.
>
> The good news is that every want below has a *better* home than the one that
> was wrong, and two of them are dedicated inputs built for exactly this.

### IDENT — the transponder's own input (easy, do it)

The SV-XPNDR-261 has a documented **Ident Switch Input on pin 20**: *"the ident
switch input allows the IDENT function to be selected using a remote switch.
The input is active low and will be asserted when the voltage to ground is
pulled below approximately 4 Volts."*

- [ ] Wire the unused small flush stick-grip button (front, below the trigger)
      to **SV-XPNDR-261 pin 20**, other side to ground. **22 AWG.**
- [ ] Momentary, normally open.
- [ ] Verify: press → SkyView's transponder page shows IDENT active.

### Yaw damper — the servo's yellow wire (easy, do it)

Also documented and optional. The yaw servo is engaged automatically with
roll/pitch, but a button gives discrete control.

- [ ] **Single-pole, normally-open momentary** button. One terminal to the **yaw
      damper servo's YELLOW wire**, the other to **ground**.
- [ ] ⚠ **The yaw damper's yellow wire must NOT be connected to the other
      servos' disconnect wires** — unlike roll and pitch. And if the button is
      ever removed, the yellow wire must be left unconnected rather than tied
      to the roll/pitch disconnects.
- [ ] This is a *separate* button from the AP Engage/Disengage button on the
      grip. It can live on the panel; nothing about it is time-critical.

### MZ-30 GEN ACTIVE and the CO detector — the actual problem

Both are discretes that need to **raise an alert**, and on SkyView that means an
**EMS general-purpose input**. The SV-EMS-220/221 has **13 GP inputs**, and a
contact is configured by defining two voltage ranges in sensor setup — 0–2 V
(closed, grounded) and 2–5 V (open). GP inputs are 0–5 V, tolerate 30 V spikes,
and anything sensing above 5 V needs a 10 kΩ series resistor.

**N720AK's 13 GP inputs are full.** That is the whole constraint, and it is why
the CO detector contact had to be disconnected in the first place. Four ways
out, cheapest first:

1. **Audit the 13 and free one.** Do this before spending anything — it is
      entirely possible something on there has been superseded or matters less
      than a CO alarm.
2. **Resistor-ladder multiplex.** A GP input reads a *voltage*, and sensor setup
      lets you define as many ranges as you like — the manual's two-range recipe
      is just the one-contact case. Several contacts, each closing a different
      resistance to ground, give distinct voltages on one pin. The catch is that
      it priority-encodes rather than monitoring independently: simultaneous
      closures read as the lowest resistance. For "any one of these alarms is
      active" that is usually fine, and it costs three resistors.
3. **A second EMS module (SV-EMS-221).** The firmware supports two natively —
      `engine_1_ems_sn_v16` / `engine_2_ems_sn_v16` and two RTIO slots — giving
      13 more GP inputs. It presents as "Engine 2", which is cosmetically odd on
      a single, but it is supported hardware at zero risk.
4. **An emulated EMS node on DSAB.** Genuinely feasible given the wire format is
      already modelled, and genuinely the riskiest: DSAB is multi-master with
      token passing and it carries the ADAHRS, the AP servos and the COM panel.
      Develop against the rig, never the airplane, and give any flying node a
      switch you can physically open.

- [ ] Pick a route, then wire the **MZ-30 Output Active** (orange/brown, pin 2)
      and the **CO detector contact** to GP inputs and configure both as
      contacts with alerts.

## Phase 6 — OnSpeed indexer

The OnSpeed box already runs from the **PFD circuit through a 2 A fuse** (red
wire, pin 1), so it is already essential-fed.

- [ ] **Move the OnSpeed box itself onto the new fuse block** (Sam, 2026-09-22),
      fed from the essential bar rather than from the PFD circuit. Two gains: the
      inline fuse stops being a thing you have to go find, and the AoA tone
      stops depending on the PFD breaker being in. It stays essential-fed either
      way — this only decouples it from the PFD.
- [ ] Give the indexer its **own separate fuse** on the block rather than
      sharing the box's. The AoA **tone** is the primary cue and the indexer
      is secondary — a fried LED line must not be able to take the tone with it.
- [ ] **Fit the series resistor at the value Phase 0 determined.** Note that
      100 Ω on a 12 V line with a ~2 V Vf LED passes about **100 mA**, which is
      high for a single indicator; 20 mA wants roughly 470 Ω–1 kΩ. And a
      pre-resistored 12 V unit needs none at all.
- [ ] **Verify:** indexer tracks the tone, and pulling the indexer fuse leaves
      the tone working.

---

## Phase 7 — Front USBs

The front USBs already have their own little fuse (Sam, 2026-09-22), so this is
consolidation rather than a rework.

- [ ] **Fold the front USBs into the new fuse block**, keeping them fed from the
      essential bus. Same reasoning as the OnSpeed box: one labelled, serviceable
      bank instead of an inline fuse holder somewhere behind the panel.
- [ ] **Not onto the VPX.** That was the original idea and it is the wrong
      direction — the VPX is entirely main-bus, so a VPX-fed USB dies in the shed
      state and takes iPad charging with it, which is exactly when the plates on
      that iPad matter most.

---

## Phase 8 — Close out

This is the part that gets skipped. None of it is optional.

- [ ] **Log entries** — airframe or avionics log as appropriate. Keep them
      short: what was done, part numbers in Parts Used.
- [ ] **`sections/sys-24-electrical.md`** — new breakers in the essential-bus
      table, the AV MSTR known-issue paragraph rewritten as resolved, the VPX
      channel table updated for the channels that moved, and the Switch Input #1
      channel list from Phase 0.
- [ ] **`sections/sys-22-autopilot.md`** — servo part numbers from Phase 0, and
      the new AP PANEL breaker.
- [ ] **`sections/sys-42-avionics.md`** and **POH §8** — the shed state is now
      IFR-capable; say so.
- [ ] **Emergency checklists in `N720AK.json`** — the shed ladder changes
      materially. New order, cheapest first: SERVOS ~1.5 A → PNL LTS 0.5 A →
      AUDIO ~1.5 A → XPDR/ADSB 0.7 A → COM 1 → **NAV 1 last** (it kills the
      whole GTN brain including GPS and screen; a headless com survives on
      COM 1, which is a VFR-only move). Regenerate the exports.
- [ ] **Anki** — the N720AK essential-bus cards state what dies in the shed
      state. That answer changes. Fix them in `cards/src/` and push; run
      `scripts/diff_decks.py` afterward.
- [ ] **`ad-sb-compliance.tsv`** — close Dynon TSB 080219 with what the Phase 0
      inspection found.

---

## What this does not cover

- The **MAP guard** for lean-of-peak operation. Separate project, documented in
  `sections/sys-73-efii.md`.
- **Battery-only endurance.** After these changes the essential load is
  ~19–20 A, so the double-failure reserve on ~31 Ah is roughly 1.5 hours —
  plan on one.

---

## Shopping list

**To actually place the order, use [`order-2026-annual.md`](order-2026-annual.md)** —
a vendor-split checklist with the open questions at the top. This section is the
reasoning behind those choices.

Priced **2026-09-22/23** against live product pages at **SteinAir** and
**Aircraft Spruce**. Prices change; treat as an estimate.

**SteinAir is the primary source.** It came out cheaper on every line that both
carry, it includes breaker mounting hardware that Spruce sells separately, and
it consolidates breakers, wire, fuse block and coax into one order.

### Breakers — the three pullable ones (Phase 2, 3, 4)

Klixon **7277 series**, the standard push-pull aviation breaker.

| Item | SteinAir SKU | Qty | Unit | Ext. |
|---|---|---|---|---|
| `AUDIO` breaker, 5 A | 7277-5 | 1 | $29.50 | $29.50 |
| `XPDR` breaker, 3 A | 7277-3 | 1 | $29.50 | $29.50 |
| `AP PANEL` breaker, 3 A | 7277-3 | 1 | $29.50 | $29.50 |

**Subtotal $88.50.** Spruce is $91.50 for the same three (7277-2-5 $31.60,
7277-2-3 $29.95 ×2) *and* charges separately for the mounting hardware —
SteinAir's listing states 7/16-32 mounting and 6-32 wiring hardware included.
Spruce's equivalent NUTPACK is $8.75.

> **Confirm the dash variant before ordering.** SteinAir lists these by
> amperage only ("7277-5"). Spruce stocks three variants at very different
> prices — **7277-2-x ≈ $30**, 7277-5-x ≈ $47, 7277-1-x ≈ $57 — where `-2-` is
> the common single-pole. Phase 0 says match what is already in the panel; ask
> SteinAir which variant they ship.

**Physical envelope** (SteinAir, for planning the cutouts): 0.570" wide ×
0.940" tall, 2.1" overall length, and the body **protrudes about 1.550" behind
the panel**. Allow more for the wiring behind that.

### Fuse block — standard ATC, not minis

**SteinAir SA-303, 10-circuit, $26.00** — "For ATO & ATC Twin Blade Fuses."

| Item | SteinAir SKU | Qty | Unit | Ext. |
|---|---|---|---|---|
| Fuse block, 10 circuit (ATO/ATC) | SA-303 | 1 | $26.00 | $26.00 |
| Fuse, 3 A violet (5 pk) | SA-203 | 1 | $2.00 | $2.00 |
| Fuse, 5 A tan (5 pk) | SA-205 | 1 | $2.00 | $2.00 |

Five circuits are planned (AV MSTR coil, OnSpeed, OnSpeed indexer, front USB,
GEN LED), so ten positions leaves five spare. The 6-, 8- and 12-circuit
versions are SA-301 $22, SA-302 $24, SA-304 $28 — the spread is small enough
that the extra capacity is worth having.

> **Standard ATC fuses are the point** (Sam, 2026-09-22). They are stocked at
> any auto parts counter, so spares are trivial and nothing exotic has to live
> in the aircraft. SteinAir also sells **LED-indicating** variants (SA-203L,
> SA-205L, $4.70/5 pk) that light when blown — worth considering for a block
> that lives behind the panel where you cannot see it.
>
> Buy fuse ratings to match the actual loads: the AV MSTR coil draws ~300 mA
> and the indexer less, but **the fuse protects the wire, not the load**. The
> OnSpeed box and the front USBs arrive with ratings already chosen — read
> their existing inline fuses rather than guessing.

#### Rejected: the SPT mini fuse panel

An earlier draft of this plan specified the **SPT rear-terminal mini fuse
panel** (Spruce 11-13348, SPT20FB) and justified it as *"SteinAir's own... being
Stein's line it matches how this panel was built."* **That attribution is
wrong.** SteinAir's store returns no results for "SPT" at all, and Spruce lists
the brand simply as SPT with no SteinAir connection. A web search appears to
confirm the SteinAir link, but its cited source is this repository's own PR
#101 — the claim was being quoted back as evidence for itself.

The hardware is real and proven (Spruce's reviews include an RV-4 builder with
23 years of service on one), and its rear terminals and sealed cover are
genuine advantages **in a tight installation**. Two facts rule it out here:

1. **Space behind this panel is not tight** (Sam, 2026-09-22) — there is a
   substantial existing cable bundle the block can be mounted to. The
   compactness premium buys nothing.
2. **It takes MINI (ATM) fuses only**, which means stocking a second fuse size
   purely for this block.

Cost, fully equipped, was **≈ $137** — panel $65.85, bracket $20.95, two
terminal kits $19.90, removal tool $16.85, cavity plugs $3.45, fuses $9.70 —
against **$30** for the SA-303 and two packs of fuses. Revisit only if the
mounting location turns out to be tighter than expected.

### Wire — MIL-W-22759/16 Tefzel, sold by the foot

SteinAir is materially cheaper on the gauges checked:

| Gauge | SteinAir | Spruce | Qty | Ext. (SteinAir) |
|---|---|---|---|---|
| 22 AWG, white striped (coil feed, contact inputs) | $0.55 | $0.70 | 25 ft | $13.75 |
| 20 AWG | $0.60 | $0.85 | 15 ft | $9.00 |
| 18 AWG (breaker feeds) | <!-- TODO: not verified --> | $0.95 | 25 ft | — |

> **18 AWG white was not confirmed at SteinAir** — their search surfaced 14 and
> 16 AWG white and 22 AWG striped, but not 18 AWG plain white. Check when
> ordering; Spruce's 11-14518 at $0.95/ft is the fallback. The 20 AWG figure is
> from their red stock (AWG20R); confirm white is the same price.

### Switch

| Item | Part No. | Spruce No. | Qty | Unit | Ext. |
|---|---|---|---|---|---|
| Yaw-damper button — C&K SPDT momentary | TP11SHZQE | 11-04471 | 1 | $15.90 | $15.90 |

This one **is** a genuine Digi-Key part (DK 67030) if you would rather source it
there, though Digi-Key blocks automated price checks. A TE MPS103FPC (11-18894,
$44.95) is the nicer option if you want it to match a specific panel style.

### Coax — RG400, ~26 ft

For the COM antenna run. **The antenna decisions themselves live with the COM1
diagnostic work, not this plan** — this is cable sourcing only.

| Source | $/ft | 26 ft | Notes |
|---|---|---|---|
| **SteinAir** RG-400 | **$8.95** | **$232.70** | **M17/128-RG400, MIL-DTL-17-128B.** Double silver-plated shield, silver-plated stranded inner, Teflon |
| Digi-Key Marketplace — McGill Microwave | ~$2.26 | ~$59 (8 m) | FEP, double braid, 19/0.0079", 50 Ω. Third-party; **mil-spec not stated on the listing** |
| Digi-Key stocked — Huber+Suhner Enviroflex_400 | ~$7.04 | ~$185 | ⚠ **RADOX jacket, not FEP** — not an M17/128 part |
| Digi-Key stocked — Huber+Suhner RG_400_/U | ~$10.12 | ~$266 | FEP, brown |
| Aircraft Spruce "Certified" (11-09202) | $14.60 | $379.60 | |
| Digi-Key — L-com, Ease Electronics | $23.99–29.99 | $624–780 | |

**SteinAir is the recommendation**: it is the only listing that names the
military specification outright, which is what should be feeding a COM antenna.
Spruce is paying aviation markup for the same thing. The McGill marketplace
cable is a quarter the price and its published specs look correct, but mil-spec
compliance cannot be verified from the listing.

> **Not checked: The Wireman, Pasternack, RF Industries.** All three typically
> land around $3–5/ft for genuine mil-spec RG400, so they are worth a look
> before committing $232 — a saving of well over $100 is plausible.
>
#### Coax connectors

One straight and one right-angle, both BNC crimp, both rated for RG-400 by
SteinAir (Sam, 2026-09-23).

| Item | SKU | Qty | Unit | Ext. |
|---|---|---|---|---|
| BNC male crimp, straight — 3-pc Amphenol, RG400/RG58 | SA-1010M | 1 | $6.75 | $6.75 |
| BNC male crimp, 90° — 3-pc Amphenol, RG400/RG58 | SA-1010R | 1 | $49.50 | $49.50 |

> **"Swivel" is unconfirmed.** Neither SteinAir listing uses the word. SA-1010R
> is described only as a *"3 Piece 90 Degree Right Angle Male BNC Crimp
> Connector for RG-400 & RG-58... Uses the same crimper as standard BNC's."*
> Confirm with SteinAir that it rotates, or compare against the one currently
> installed, before ordering.
>
> Two cheaper right-angle alternatives exist if the one-piece crimp is not what
> is on the aircraft: **SA-1010R-A** ($17.50), a 1-piece adapter that converts a
> straight BNC to right angle, and **SA-1010TR** ($44.75), a right-angle *tray*
> adapter with snap ring.

> **Check BNC vs TNC at both ends before ordering.** SteinAir's own product page
> warns: *"Be sure to look closely at the unit/tray to determine which style you
> need."* BNC is push-and-twist, TNC is threaded. If either end turns out to be
> TNC, the equivalents are SA-1001 (male straight, $5.50) and SA-1000 (female
> crimp, $7.75). BNC female crimp is SA-1010F ($5.75).

**Tooling — only if not already on hand.** The run needs a coax stripper and the
right crimp die. SteinAir: coax stripper **SAT-COAX** $62.00, coax crimp die
**SAT-031** $17.00, ratcheting crimper frame $35.00, flush cutters $9.75. Both
connectors above use the same crimper as a standard BNC.

### Not priced here

- **LED series resistor** — 1/2 W through-hole, value set by Phase 0. A 470 Ω
  and 1 kΩ assortment from Digi-Key or Mouser is a couple of dollars. This is
  the only genuinely Digi-Key line on the whole list.
- **Ring terminals, FastOns, adhesive-lined heat shrink** — you almost
  certainly have these; check stock before ordering. SteinAir carries ring
  terminals at $0.40–0.45 each if not.

> **No Schottky diode is required.** An earlier revision listed one against a
> possible diode-OR on the transponder. Option B is locked — the transponder
> moves to its own 3 A breaker with the VPX channel removed, and **no diode-OR**
> — so that part has been removed from this list.

**Estimated total ≈ $450** including 26 ft of RG400 and both connectors at
SteinAir, or ≈ $160 without the coax and its fittings — and less again if a
cheaper mil-spec RG400 source pans out. Spruce's free shipping starts at $350; check SteinAir's own
shipping terms before splitting the order across both.
