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

**A conflict to settle:** there is exactly **one** unused stick-grip button (the
small flush button on the front, below the trigger) and two things want it —
IDENT and yaw damper. Recommend **IDENT on the grip**, because ATC says "ident"
and you want it under your thumb, and the yaw damper on a panel button, because
nothing about it is time-critical.

---

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

Two options; pick one.

**Option A — diode-OR dual feed** (keeps VPX monitoring and control):
- [ ] Schottky diode from the essential bus into the XPDR feed, cathode toward
      the load, sized ≥5 A. Note the forward drop comes off bus voltage.
- [ ] Leave the VPX channel in place as the normal-operations path.

**Option B — move it outright** (simpler, loses VPX monitoring):
- [ ] **3 A pull-able breaker** labelled `XPDR`, essential bus, **18 AWG**.
- [ ] Remove the VPX J10-7 assignment.

Either way:
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

## Phase 5 — Contact inputs

EMS pins are full. Use the **SkyView display D37 contact inputs: pins 28, 27,
14, 15 = Contacts 1–4**, unused on every display harness.

**Put anything that must work in the shed state on PFD 1's harness** — a display
contact input only functions when that display is powered, and PFD 1 is the
essential-fed one.

- [ ] **IDENT** — wire the unused small flush stick-grip button (front, below
      the trigger) to a PFD 1 contact input, configured for transponder ident.
      **22 AWG.**
- [ ] **MZ-30 GEN ACTIVE annunciation** — the orange/brown **Output Active**
      wire (regulator pin 2) is coiled unused near the Monkworkz enable switch.
      It pulls to ground when the regulator is producing, which matches Dynon
      contact-input expectations. Wire to another PFD 1 contact input.
- [ ] **Yaw damper** — panel-mount momentary button to a contact input. Not
      time-critical, so a display other than PFD 1 is acceptable if you would
      rather keep PFD 1's inputs for the two above.
- [ ] Configure all three in SkyView setup and **verify each annunciates**.

---

## Phase 6 — OnSpeed indexer

The OnSpeed box already runs from the **PFD circuit through a 2 A fuse** (red
wire, pin 1), so it is already essential-fed.

- [ ] Give the indexer its **own ~1 A fuse** on the new block rather than
      sharing the box's 2 A. The AoA **tone** is the primary cue and the indexer
      is secondary — a fried LED line must not be able to take the tone with it.
- [ ] **Fit the series resistor at the value Phase 0 determined.** Note that
      100 Ω on a 12 V line with a ~2 V Vf LED passes about **100 mA**, which is
      high for a single indicator; 20 mA wants roughly 470 Ω–1 kΩ. And a
      pre-resistored 12 V unit needs none at all.
- [ ] **Verify:** indexer tracks the tone, and pulling the indexer fuse leaves
      the tone working.

---

## Phase 7 — Front USB (optional)

- [ ] If moving it at all, move it to an **essential** fuse, not the VPX, so
      iPad charging survives a main-bus loss. Otherwise leave it alone.

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
