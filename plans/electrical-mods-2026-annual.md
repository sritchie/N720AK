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
| 6–20 | spare | — | cavity plugs |

Five of twenty positions used. The spare capacity is the point: the next
modification should not need a new fuse holder.

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
- [ ] **Read the AP servo part numbers off their labels** while the panel is
      open. Dynon **TSB 080219** (linear-actuator pulley cracking) says "comply
      before further flight" and covers SV42T P/N 101008-003 / 101058-003 plus
      any SV32/SV42 retrofitted with the linear actuator. N720AK's pitch servo
      *is* the RV-10 linear-actuator install. Inspect the pulley for a crack
      from the centre through the shear-screw bore. This closes a live
      airworthiness item and `sys-22-autopilot.md` has both P/Ns as TODO.
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

- [ ] Add a **1 A blade fuse** on the new essential-bus fuse block, labelled
      `AV MSTR COIL`.
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

Priced at **Aircraft Spruce, 2026-09-22**, verified against live product pages.
Prices change; treat as an estimate.

### Breakers — the three pullable ones (Phase 2, 3, 4)

Klixon **7277 series**, the standard push-pull aviation breaker. All in stock.

| Item | Part No. | Spruce No. | Qty | Unit | Ext. |
|---|---|---|---|---|---|
| `AUDIO` breaker, 5 A | 7277-2-5 | 7277-2-5 | 1 | $31.60 | $31.60 |
| `XPDR` breaker, 3 A | 7277-2-3 | 7277-2-3 | 1 | $29.95 | $29.95 |
| `AP PANEL` breaker, 3 A | 7277-2-3 | 7277-2-3 | 1 | $29.95 | $29.95 |

> **Check the dash number in Phase 0 before ordering.** Spruce stocks three
> variants at very different prices: **7277-2-x ≈ $30**, 7277-5-x ≈ $47,
> 7277-1-x ≈ $57. The `-2-` is the common single-pole. Match whatever is
> already in the panel rather than assuming.
>
> 2 A is also available (7277-2-2, $29.95) if you would rather size XPDR or
> AP PANEL down.

### Fuse panel — the answer to "a bank of fuses behind the panel"

**SteinAir's own SPT rear-terminal mini-fuse panel.** Rear terminals means the
wiring leaves the back, which is what makes it tidy behind a panel, and being
Stein's line it matches how this panel was built.

| Item | Part No. | Spruce No. | Qty | Unit | Ext. |
|---|---|---|---|---|---|
| SPT rear-terminal mini fuse panel (20 pos.) | SPT20FB | 11-13348 | 1 | $65.85 | $65.85 |
| SPT mounting bracket pair | SPT2FMB | 11-13352 | 1 | $20.95 | $20.95 |
| Terminal kit, 22-20 AWG (red) | SPT22-20FT | 11-13353 | 1 | $9.95 | $9.95 |
| Terminal kit, 18-16 AWG (purple) | SPT18-16FT | 11-13354 | 1 | $9.95 | $9.95 |
| Terminal removal tool | — | 11-13358 | 1 | $16.85 | $16.85 |
| Cavity plugs (unused positions) | — | 11-13357 | 1 | $3.45 | $3.45 |
| 2 A fuses (gray) | SPT2AMP | 11-13359 | 1 pk | $4.75 | $4.75 |
| 5 A fuses (tan) | SPT5AMP | 11-13360 | 1 pk | $4.95 | $4.95 |

> **These are MINI (ATM) fuses, not ATC/ATO** — smaller, which is the point
> behind a panel. Spruce's smallest in this line is **2 A**; there is no 1 A.
> That is fine for both planned circuits: the AV MSTR coil draws ~300 mA and
> the indexer less, and what the fuse protects is the **22 AWG wire**, not the
> load. If you want 1 A specifically, generic 1 A ATM fuses are easy to source
> elsewhere.
>
> A 10-fuse + 5-relay variant exists (SPT10F5R, 11-13351, $62.75) if you would
> rather have relay sockets than twenty fuse positions. With five circuits now
> planned, ten would still leave room — but the twenty-position panel is only
> $3 more, so take the spare capacity.
>
> **Buy fuses to match.** The block carries five circuits, not two, and the
> OnSpeed box and the front USBs arrive with ratings already chosen — read what
> their existing inline fuses are rated at rather than guessing.

### Wire — MIL-W-22759/16 Tefzel, sold by the foot

| Gauge | Part No. | Spruce No. | Qty | Unit | Ext. |
|---|---|---|---|---|---|
| 18 AWG white (breaker feeds) | M22759/16-18-9 | 11-14518 | 25 ft | $0.95 | $23.75 |
| 20 AWG white | M22759/16-20-9 | 11-14520 | 15 ft | $0.85 | $12.75 |
| 22 AWG white (coil feed, contact inputs) | M22759/16-22-9 | 11-14522 | 25 ft | $0.70 | $17.50 |

Colored stock exists (18 AWG red 11-01597, green 11-07798, white/black
11-15601) if you want to code the new runs.

### Switch

| Item | Part No. | Spruce No. | Qty | Unit | Ext. |
|---|---|---|---|---|---|
| Yaw-damper button — C&K SPDT momentary | TP11SHZQE | 11-04471 | 1 | $15.90 | $15.90 |

A TE MPS103FPC (11-18894, $44.95) is the nicer option if you want it to match
a specific panel style.

**Aircraft Spruce subtotal ≈ $298.** Note their **free shipping kicks in at
$350** — worth adding the terminals and heat-shrink you are low on rather than
paying freight.

### Not priced here

Stopped browsing at this point to control cost. These two are commodity parts
and only need a spec, not a shopping trip:

- **LED series resistor** — 1/2 W through-hole, value set by Phase 0. Buy a
  small assortment (470 Ω and 1 kΩ) from Digi-Key or Mouser; it is a few
  dollars either way.
- **Schottky diode**, only if Phase 3 goes the diode-OR route — ≥5 A, ≥40 V,
  low forward drop, stud or TO-220. The forward drop comes straight off bus
  voltage at the transponder, so prefer a genuine Schottky over a general
  rectifier.
- **Ring terminals, FastOns, adhesive-lined heat shrink** — you almost
  certainly have these; check stock before ordering.
