# Order sheet — 2026 annual electrical

Companion to `electrical-mods-2026-annual.md`. **That plan is the source of
truth for *why*** — part choices, the breaker-vs-fuse partition and the rejected
alternatives are all argued there. This page is just the transaction.

Prices verified against live product pages **2026-09-22/23**. They drift.

---

## Resolve these before placing the order

Most of these closed on 2026-09-23. Two remain.

- [ ] **Does one of the two bayonet positions point along the fuselage?** This
      is a two-minute look at the installed connector, and it decides the whole
      question — see the connector note below. `SA-1010R` **does not swivel**
      (Sam, 2026-09-23).
- [ ] **Confirm the FastOn tab size on the SA-303.** The block takes FastOns
      (Sam, 2026-09-23); 1/4" is the near-universal ATC/ATO blade-block size and
      is what is ordered below, but it has not been measured. Verify before
      crimping 25 of them.

**Resolved:**

- ~~Klixon dash-variant~~ — SteinAir's Klixon line runs **1, 2, 3, 4, 5, 10, 15
  and 20 A** (Sam, 2026-09-23). Both values this job needs are stocked. Worth a
  one-line confirm on the sub-series when ordering if the panel is mixed.
- ~~BNC or TNC~~ — **BNC at both ends, confirmed** (Sam, 2026-09-23). Not the
  threaded kind. TNC alternatives dropped from this sheet.
- ~~SA-303 terminals~~ — **FastOns**, now on the order.
- ~~What the 18 AWG is for~~ — the **three new breaker feed runs** from the
  essential bus bar: `AUDIO` (Phase 2), `XPDR` (Phase 3) and `AP PANEL`
  (Phase 4). All three are specified 18 AWG in the plan.

**Not ordered yet, pending Phase 0:**

- **2N7000 MOSFET** — only if Monkworkz says MZ-30 pin 2 cannot sink the lamp. Measure pin 2 polarity first: units before 2011-06-12 are inverted.
- **LED series resistor value** — the assortment below covers it either way.
- **Three ladder resistors** — only if Phase 0 picks the resistor-ladder route for the GP inputs.

---

## SteinAir — ORDERED 2026-09-23

> The 90° BNC `SA-1010R` was **not** ordered; it is coming from Aircraft Spruce
> as the Amphenol instead. Everything else below was placed.

| ☐ | Item | SKU | Qty | Unit | Ext. |
|---|---|---|---|---|---|
| ☐ | Klixon 7277 breaker, 5 A — `AUDIO` | `7277-5` | 1 | $29.50 | $29.50 |
| ☐ | Klixon 7277 breaker, 3 A — `XPDR` | `7277-3` | 1 | $29.50 | $29.50 |
| ☐ | Klixon 7277 breaker, 3 A — `AP PANEL` | `7277-3` | 1 | $29.50 | $29.50 |
| ☐ | Fuse block, 10 circuit, ATO/ATC | `SA-303` | 1 | $26.00 | $26.00 |
| ☐ | Fuse, 1 A black (5 pk) — `AV MSTR COIL` | `SA-201` | 1 | $2.00 | $2.00 |
| ☐ | Fuse, 3 A violet (5 pk) | `SA-203` | 1 | $2.00 | $2.00 |
| ☐ | Fuse, 5 A tan (5 pk) | `SA-205` | 1 | $2.00 | $2.00 |
| ☐ | Tefzel 22 AWG **Wht/Red** — AV MSTR coil feed | `AWG22W/R` | 10 | $0.55 | $5.50 |
| ☐ | Tefzel 22 AWG **Wht/Grn** — IDENT contact | `AWG22W/G` | 10 | $0.55 | $5.50 |
| ☐ | Tefzel 22 AWG **Wht/Yel** — yaw-damper contact | `AWG22W/Y` | 10 | $0.55 | $5.50 |
| ☐ | Tefzel 20 AWG — 15 ft | `AWG20x` | 15 | $0.60 | $9.00 |
| ☐ | Tefzel 16 AWG white — 10 ft, **fuse block feed** | `AWG16W` | 10 | $0.95 | $9.50 |
| ☐ | RG-400 coax, M17/128 — 26 ft | `RG-400` | 26 | $8.95 | $232.70 |
| ☐ | BNC male crimp, straight | `SA-1010M` | 1 | $6.75 | $6.75 |
| ☐ | FastOn QD receptacle, red, 22-18 AWG, 1/4" | `SA-001` | 25 | $0.42 | $10.50 |

**Subtotal: $405.45** as placed (was $454.95 with the 90° included).

Breaker mounting hardware (7/16-32 and 6-32) is **included** with SteinAir's
7277s — do not add the NUTPACK.

> **The 90° at the antenna — resolve the azimuth before ordering.**
>
> **The geometry** (Sam, 2026-09-23): the RG-400 comes up and lays along the top
> of the fuselage, and a 90° turns it up into the BNC on the underside of the
> top-mounted antenna. The swivel currently fitted is there to **relieve
> azimuth strain** — to let the elbow point along the fuselage rather than
> forcing the cable around to meet it.
>
> **Why a fixed elbow may not do.** A BNC jack has two bayonet pins 180° apart,
> so a plug mates in **two positions only**, 180° apart, and which two is set by
> how the antenna is clocked in the skin. You cannot re-clock the antenna. If
> neither position lands fore-and-aft, the cable is twisted to reach — and
> RG-400 at 0.195" double-braid has a bend radius around an inch, so that strain
> lands at the ferrule, where the strain relief should be working.
>
> **The test, before spending anything:** look at the connector on the aircraft
> now. If it is sitting at or near one of the two natural bayonet positions, a
> fixed elbow drops straight in. If it is clocked roughly 90° away from both,
> rotation is doing real work and a fixed elbow will fight the cable.
>
> **A service loop may settle it for nothing.** The cable lays along the top of
> the fuselage, so if there is room for a gentle 6–8" curve before it settles
> into the run, that absorbs an azimuth mismatch with no strain at the
> connector. Cheapest fix available, and worth eyeballing first.
>
> **There is no "swivel right-angle BNC" product category.** Three searches
> across Amphenol, L-com, Milestek, Pasternack and RF Industries turned up
> nothing sold as one. What is on the aircraft is most likely an ordinary
> right-angle crimp plug whose body happens to rotate on the cable — a property
> of the design that nobody documents either way. So the only way to know
> whether a given part rotates is to ask the vendor holding it.
>
> **Price finding.** The industry-standard right-angle BNC for RG-400 is the
> **Amphenol 112526**, at Aircraft Spruce as **11-17167 for $8.60** — against
> **$49.50** for SteinAir's `SA-1010R`. Same function, **$40.90 apart**. The
> trade is that the Amphenol solders the centre conductor and crimps the ferrule,
> where the SteinAir part is all-crimp. All-crimp is quicker and avoids heat near
> the dielectric; a soldered centre pin is a perfectly good joint done properly.
> **Unless the all-crimp matters to you, take the Amphenol and put the $40 into
> the cable.**

> **FastOn sizing.** `SA-001` (red, 22-18 AWG) covers every wire in this job —
> 18, 20 and 22 AWG all fall inside its range. If any heavier feeds turn up,
> blue 16-14 AWG 1/4" is `SA-002` at $0.45. Other tab sizes, in case the SA-303
> measures differently: 3/16" red `SA-049` $0.55, .110 red `SA-052` $0.35.
> SteinAir also sells a 440-piece terminal kit, `SA-000-1`, at $150 if a full
> restock is wanted rather than 25 of one part.

## Aircraft Spruce — FINAL

| ☐ | Item | SKU | Qty | Unit | Ext. |
|---|---|---|---|---|---|
| ☐ | C&K SPDT momentary — yaw damper button | `11-04471` | 1 | $15.90 | $15.90 |
| ☐ | BNC male right-angle crimp plug, RG-400 — Amphenol 112526 | `11-17167` | 1 | $8.60 | $8.60 |
| ☐ | Bus bar MS25226-10A-4 — 4 holes, 2 5/8", 1/16" thick | `11-04676` | 1 | $5.65 | $5.65 |
| ☐ | Tefzel 14 AWG white — 10 ft, feed for the new bus bar | `11-14514` | 10 | $1.67 | $16.70 |
| ☐ | Flat washer AN960-6 — spans the bar's oversize holes | `AN960-6` | 10 | ~$0.10 | ~$1.00 |
| ☐ | PIDG ring tongue, 16-14 AWG, **#6** stud | `11-18375` | 5 | $0.35 | $1.75 |
| ☐ | PIDG ring tongue, 16-14 AWG, **#10** stud | `11-18373` | 5 | $0.33 | $1.65 |
| ☐ | Tefzel 18 AWG white — 25 ft, breaker feeds *(only if SteinAir lacked it)* | `11-14518` | 25 | $0.95 | $23.75 |

**Subtotal: $75.00**, or **$51.25** if SteinAir supplied the 18 AWG white.

> The AN960-6 price is an estimate — Spruce shows it only in the cart. It is a
> commodity washer and will be around a dime; the line will not move the total.

### Why the washers and ring terminals

Three gaps that only appeared once the bus bar was chosen:

- **The bar's holes are .225", the Klixon terminals are 6-32 (0.138").** The
  screw head cannot span that, so each of the three breaker studs wants a
  washer under it. **AN960-6 is 0.375" OD against a 0.225" hole** — ample.
- **The 14 AWG feed needs a ring terminal**, and nothing on the SteinAir order
  covers it: those were red 22-18 AWG FastOns for the SA-303 fuse block, the
  wrong size and the wrong type. 14 AWG wants **blue 16-14 AWG** rings.
- **Both stud sizes are stocked** because it depends where the feed lands. The
  bar's fourth hole at .225" suits a **#10** screw directly; landing on a
  breaker's own 6-32 stud instead wants the **#6**. At ~35¢ each, carry both
  and decide at the bench.

### The bus bar — take the pre-drilled one

**The existing essential bus bar is full** (Sam, 2026-09-23), so the three new
breakers need their own bar, located elsewhere and fed from the essential bus.

**`11-04676`, MS25226-10A-4** — four .225" holes at ~3/4" centres, 2 5/8" long,
**1/16" thick**, cadmium-plated copper, **$5.65**. Four positions covers three
breakers plus the feed, and 3/4" is the standard Klixon spacing.

> **Do not buy the raw copper bar** (`11-40890-1`, $8.50/ft, 0.125" thick).
> It is more expensive *and* more work: reviewers report the copper is "so hard
> that it is tough to drill... even with a drill press", and at 0.125" **the
> screws supplied with the Klixon breakers are too short** — one builder stacked
> three washers to take up the length. The MS25226 at 1/16" matches the
> thickness the supplied 6-32 hardware expects.
>
> The .225" holes are considerably larger than a 6-32 screw. That is normal for
> MS25226 breaker bars, but plan on washers and check the fit.

**14 AWG for the feed**, not 16. The bar carries the sum of the three breakers
— 5 A `AUDIO` + 3 A `XPDR` + 3 A `AP PANEL` = **11 A** worst case. 14 AWG is
the conservative, correct size for a sub-bus feed at that rating; 16 AWG is
marginal once bundled.

## Digi-Key, Mouser or any parts drawer

| ☐ | Item | Qty | Note |
|---|---|---|---|
| ☐ | **10 kΩ resistor, 1/4 W or 1/2 W** | 2–3 | MZ-30 amps pull-down, EMS pin 31 to ground |

**Needed to run the test, not just the fix.** Step 2 of the MZ-30 diagnosis is
bridging pin 31 to ground through 10 kΩ to confirm the float — so one is wanted
before any decision is made. Pennies, and any assortment covers it.

> An earlier revision of this sheet said nothing on this job was a Digi-Key
> order. That was true at the time: the OnSpeed indexer turned out to be an
> M5Stack rather than an LED, which removed the series resistor. **The MZ-30
> float diagnosis put a resistor back on the list** for a different reason.
>
> If the M5Stack ends up fed by a 12 V → 5 V DC-DC rather than USB, that
> converter joins this list — size it once the draw is measured.

## Still needed: bussing the three new breakers

**Not on either order, and not previously in the plan.** The plan assumed three
separate 18 AWG runs from the essential bus bar to each new breaker. Ganging
them on a bar instead is standard panel practice and almost certainly better —
one feed instead of three, and three fewer terminals at the essential bus.

**Look before buying.** How are the *existing* essential-bus breakers bussed?

| What you find | What to do |
|---|---|
| An existing bar with spare positions | Land the three new breakers on it. Buy nothing. |
| An existing bar, full | Extend it, or add a second bar and jumper across. |
| Each breaker individually wired | Match the existing convention, or gang the new three and feed the bar once. |

If a bar is needed: **SteinAir `BB-237`, copper bar stock, 12" × 0.5" × 0.063",
$5.95** — "used for ganging switches and circuit breakers together." Cut to
length and drill for the 7277's 6-32 studs at the panel's breaker spacing.
Current capacity is a non-issue: that cross-section carries far more than the
11 A worst case (5 A `AUDIO` + 3 A `XPDR` + 3 A `AP PANEL`, and realistically
nearer 3–4 A).

Pre-drilled alternatives, if the spacing happens to suit: `BB-231` ten #8
screws $19.00, `BB-235` four #10 studs $19.10.

> **If you gang them, the wire changes.** One feed to the bar rather than three
> runs, so less 18 AWG — but that single feed carries the sum. Size it for the
> realistic 3–4 A and 16 AWG is ample; size it to the breaker total of 11 A and
> it wants 14 AWG. Decide which convention this panel already follows.

## Deferred: sharing the COM antenna with the handheld

**The idea is sound.** A handheld's rubber duck inside an aluminium fuselage is
badly compromised; on the real COM antenna it actually works. That is precisely
the total-electrical-failure case this whole plan keeps circling — panel dark,
handheld is the radio — so it fits the thinking rather than bolting something on.

**The real cost is a manual switch in the primary COM 1 antenna path.** Left in
the handheld position, COM 1 is *silently* dead: nothing indicates it, and the
discovery is nobody answering. That argues for a switch whose position is
unmistakable at a glance and a line in the pre-flight flow, not just a knob
behind the panel.

**Not on this order, for four reasons:**

1. **The product is not pinned down.** Searches did not locate an "Icom antenna
   switch box" in Spruce's current catalogue, and the one candidate that
   surfaced (a Comtronics switcher box) 404s. Buying the wrong switch is worse
   than waiting a week.
2. **The parts list depends on the switch.** Connector type (BNC or UHF) and
   port count decide how many extra Amphenol BNCs and how much RG-400 the
   jumpers need — plausibly four more connectors and a few feet.
3. **It is undesigned.** Where the switch mounts, whether it is reachable in
   flight, and what the handheld end presents on the panel are Phase-0-shaped
   questions, not order-sheet ones. Unplugging behind the panel is not an
   option in flight, which is exactly why a panel-mounted switch is the form
   people end up with.
4. **It belongs with the COM antenna work**, which is live in other branches,
   not with this electrical order. Nothing here waits on it.

> ⚠ **Do not cut the 26 ft of RG-400 until this is decided.** If the run
> terminates at a switch rather than at the GTN, the length and the number of
> connectors both change. The cable is ordered; leave it on the spool.

## Worth adding while the order is open

None of this is required for the job. Priced so the decision is quick.

| Item | SKU | Price | Why |
|---|---|---|---|
| Fuse, 10 A red (5 pk) | `SA-210` | $2.00 | Spares for the aircraft kit. ATC is standard, so they serve anything. |
| Fuse, 15 A blue (5 pk) | `SA-215` | $2.00 | Same. |
| LED-indicating fuses, 3 A / 5 A (5 pk) | `SA-203L` / `SA-205L` | $4.70 ea | They light when blown. The block lives behind the panel where a dead fuse is invisible — $2.70 over a plain pack. |
| Heat Shrink Kit | `HSKIT` | $30.00 | Only if stock is low. |

**Coax tooling**, only if not already owned — stripper `SAT-COAX` $62.00, crimp
die `SAT-031` $17.00, ratcheting crimper frame $35.00, flush cutters $9.75.

**Labelling for Phase 8.** SteinAir sells heat-shrink label cartridges
(`EC-HS3` 3.5 mm, `EC-HS5` 5 mm, `EC-HS11` 11 mm, $15.00 each) but they need
their **`EC-PRINTER` Industrial Label Maker Kit at $199.00**. That is a real
purchase, not an add-on — skip it if there is already a labeller in the shop.

## Check stock before ordering

- Ring terminals, FastOns, adhesive-lined heat shrink — SteinAir carries rings at $0.40–0.45 if needed
- Wire labels or markers for the new breakers and fuse positions
- **Coax tooling**, if not already owned: stripper `SAT-COAX` $62.00, crimp die `SAT-031` $17.00, ratcheting crimper frame $35.00, flush cutters $9.75. Both BNCs above use the same crimper as a standard BNC.

## Consider

SteinAir sells **LED-indicating fuses** (`SA-203L`, `SA-205L`, $4.70/5 pk) that
light when blown. For a block that lives behind the panel where you cannot see
it, that is worth the $2.70 difference.
