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

- **1 A ATC fuse** for `AV MSTR COIL` — SteinAir's listed low end is 3 A. Commodity part, source anywhere.
- **2N7000 MOSFET** — only if Monkworkz says MZ-30 pin 2 cannot sink the lamp. Measure pin 2 polarity first: units before 2011-06-12 are inverted.
- **LED series resistor value** — the assortment below covers it either way.
- **Three ladder resistors** — only if Phase 0 picks the resistor-ladder route for the GP inputs.

---

## SteinAir

| ☐ | Item | SKU | Qty | Unit | Ext. |
|---|---|---|---|---|---|
| ☐ | Klixon 7277 breaker, 5 A — `AUDIO` | `7277-5` | 1 | $29.50 | $29.50 |
| ☐ | Klixon 7277 breaker, 3 A — `XPDR` | `7277-3` | 1 | $29.50 | $29.50 |
| ☐ | Klixon 7277 breaker, 3 A — `AP PANEL` | `7277-3` | 1 | $29.50 | $29.50 |
| ☐ | Fuse block, 10 circuit, ATO/ATC | `SA-303` | 1 | $26.00 | $26.00 |
| ☐ | Fuse, 3 A violet (5 pk) | `SA-203` | 1 | $2.00 | $2.00 |
| ☐ | Fuse, 5 A tan (5 pk) | `SA-205` | 1 | $2.00 | $2.00 |
| ☐ | Tefzel 22 AWG white striped — 25 ft | `AWG22W/x` | 25 | $0.55 | $13.75 |
| ☐ | Tefzel 20 AWG — 15 ft | `AWG20x` | 15 | $0.60 | $9.00 |
| ☐ | RG-400 coax, M17/128 — 26 ft | `RG-400` | 26 | $8.95 | $232.70 |
| ☐ | BNC male crimp, straight | `SA-1010M` | 1 | $6.75 | $6.75 |
| ☐ | BNC male crimp, 90° — **does not swivel** | `SA-1010R` | 1 | $49.50 | $49.50 |
| ☐ | FastOn QD receptacle, red, 22-18 AWG, 1/4" | `SA-001` | 25 | $0.42 | $10.50 |

**Subtotal: $440.70**

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

## Aircraft Spruce

| ☐ | Item | SKU | Qty | Unit | Ext. |
|---|---|---|---|---|---|
| ☐ | C&K SPDT momentary — yaw damper button | `11-04471 / TP11SHZQE` | 1 | $15.90 | $15.90 |
| ☐ | Tefzel 18 AWG white — 25 ft, the three breaker feeds *(only if SteinAir lacks it)* | `11-14518` | 25 | $0.95 | $23.75 |
| ☐ | BNC male right-angle crimp plug, RG-400 — Amphenol 112526 *(alternative to `SA-1010R`, saves $40.90)* | `11-17167` | 1 | $8.60 | $8.60 |

**Subtotal: $39.65**, or **$48.25** taking the Amphenol — which drops SteinAir's
by $49.50, so **$40.90 net saving**.

## Digi-Key or Mouser

| ☐ | Item | SKU | Qty | Unit | Ext. |
|---|---|---|---|---|---|
| ☐ | LED series resistor assortment, 470 Ω + 1 kΩ, 1/2 W | — | 1 | ~$2.00 | ~$2.00 |

**Subtotal ≈ $2.00.** This is the only genuinely Digi-Key line on the whole job.

---

## Total ≈ $482.35

**≈ $193.40 without the coax and its fittings.**

Drops to **≈ $441.45** taking the Amphenol 112526 right-angle from Spruce
instead of SteinAir's `SA-1010R`.

> **Before committing $232 to RG-400:** The Wireman, Pasternack and RF
> Industries were **not** checked and typically run $3–5/ft for genuine
> mil-spec. That is plausibly $100+ off on 26 ft. SteinAir at $8.95/ft is the
> best *verified* mil-spec price — it is the only listing that names
> MIL-DTL-17-128B outright — but it has not been shopped against the RF houses.

## Check stock before ordering

- Ring terminals, FastOns, adhesive-lined heat shrink — SteinAir carries rings at $0.40–0.45 if needed
- Wire labels or markers for the new breakers and fuse positions
- **Coax tooling**, if not already owned: stripper `SAT-COAX` $62.00, crimp die `SAT-031` $17.00, ratcheting crimper frame $35.00, flush cutters $9.75. Both BNCs above use the same crimper as a standard BNC.

## Consider

SteinAir sells **LED-indicating fuses** (`SA-203L`, `SA-205L`, $4.70/5 pk) that
light when blown. For a block that lives behind the panel where you cannot see
it, that is worth the $2.70 difference.
