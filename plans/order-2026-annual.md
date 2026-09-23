# Order sheet — 2026 annual electrical

Companion to `electrical-mods-2026-annual.md`. **That plan is the source of
truth for *why*** — part choices, the breaker-vs-fuse partition and the rejected
alternatives are all argued there. This page is just the transaction.

Prices verified against live product pages **2026-09-22/23**. They drift.

---

## Resolve these before placing the order

Five open items. The first three change what you order; the last two are
Phase 0 outputs, so those lines stay off the order until Phase 0 runs.

- [ ] **Which Klixon dash-variant does SteinAir ship?** They list by amperage
      only ("7277-5"). Spruce stocks `-2-` ≈ $30, `-5-` ≈ $47, `-1-` ≈ $57. The
      `-2-` is the common single-pole. **Match what is already in the panel.**
- [ ] **Does SA-1010R actually swivel?** The listing says only *"3 Piece 90
      Degree Right Angle Male BNC Crimp Connector."* Compare against the one on
      the aircraft. Cheaper alternatives if not: **SA-1010R-A** $17.50 (straight
      → 90° adapter), **SA-1010TR** $44.75 (right-angle tray adapter).
- [ ] **BNC or TNC at each end?** SteinAir: *"Be sure to look closely at the
      unit/tray to determine which style you need."* TNC equivalents are
      **SA-1001** $5.50 male straight, **SA-1000** $7.75 female crimp.
- [ ] **Does SteinAir stock 18 AWG white?** Not found in their search. The
      Spruce line below is the fallback — drop it if SteinAir has it.
- [ ] **What terminals does the SA-303 take?** Stud size, or FastOns? Not
      established. Confirm before the bench session, not at it.

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
| ☐ | BNC male crimp, 90° | `SA-1010R` | 1 | $49.50 | $49.50 |

**Subtotal: $430.20**

Breaker mounting hardware (7/16-32 and 6-32) is **included** with SteinAir's
7277s — do not add the NUTPACK.

## Aircraft Spruce

| ☐ | Item | SKU | Qty | Unit | Ext. |
|---|---|---|---|---|---|
| ☐ | C&K SPDT momentary — yaw damper button | `11-04471 / TP11SHZQE` | 1 | $15.90 | $15.90 |
| ☐ | Tefzel 18 AWG white — 25 ft *(only if SteinAir lacks it)* | `11-14518` | 25 | $0.95 | $23.75 |

**Subtotal: $39.65**

## Digi-Key or Mouser

| ☐ | Item | SKU | Qty | Unit | Ext. |
|---|---|---|---|---|---|
| ☐ | LED series resistor assortment, 470 Ω + 1 kΩ, 1/2 W | — | 1 | ~$2.00 | ~$2.00 |

**Subtotal ≈ $2.00.** This is the only genuinely Digi-Key line on the whole job.

---

## Total ≈ $471.85

**≈ $182.90 without the coax and its fittings.**

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
