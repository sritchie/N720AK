# Plan: N720AK Wiring Schematics in KiCad

Goal: **every wire in the airplane captured in a structured, inspectable form**,
from which schematic drawings, connector pin tables and cable schedules are all
generated — so modifications get recorded rather than remembered.

The drawings are the output. The wire list is the thing.

---

## Where we are

Two previous attempts exist. Neither contains a single wire.

| Location | State |
|---|---|
| GDrive `Public/Schematics/kicad_project/` | 5 sheets named for the source PDFs — **all empty**. 0 symbols, 0 wires, 0 labels. Scaffolding only. |
| Dropbox `N720AK/rv10_kicad/` | 1 sheet, 14 symbols, **0 wires**. Parts placed, nothing connected. |

One asset is worth keeping: `libraries/RV10_Connectors.kicad_sym` (97 KB) from the
GDrive attempt. Audit it before reuse, but connector symbols are the tedious part
and someone already did some.

Both are superseded by this plan. Don't try to continue either.

### Source material — better than expected

The SteinAir drawings are **vector PDFs with extractable text and positions**, not
scans:

| PDF | Words | Vector paths |
|---|---|---|
| `SV_Interconnect.pdf` | 3,181 | 2,733 |
| `Power__Lighting.pdf` | 1,142 | 2,542 |
| `MH_Oxygen.pdf` | 198 | 241 |

The text includes pin numbers, wire colours (`Wht/Blu`, `Wht/Ora`, `Grn`, `Blk`),
connector types (`DB-9`), and ground-architecture names (`AVIONICS GROUND POINT`,
`CASE GROUND`, `AG`, `CG`, `BACKSHELL GROUND`).

**This makes extraction a parsing problem rather than a transcription job.** Text
with coordinates, plus path geometry, is enough to associate pin numbers with
connectors and nets with wires semi-automatically. Expect to review and correct
the result, not to type it.

---

## The central idea

A wire list is the source of truth. Everything else is a **view** of it:

```
                      ┌─> KiCad schematic sheets   (drawings)
   wirelist.tsv ──────┼─> connector pin tables     (Vern's CONNECTORS sheet)
   (reviewed,         ├─> cable / harness schedule (Vern's AUDIO CABLES sheet)
    version           ├─> BOM
    controlled)       └─> cross-reference: "what touches the GTN?"
```

Vern's `CONNECTORS.pdf` is the proof of why. It is pure tabular data — pin
designator → net name, spares marked `--`, plus a connector-face diagram. Nobody
should draw that by hand, and nobody should maintain it separately from the
schematic it must agree with. Generate it.

The same argument applies to the question that started this whole project: *"which
antenna does COM 1 feed?"* That is a query against a wire list. It should never
again depend on someone's recollection or on which way a coax appears to leave a
connector.

### Why this ordering matters

The temptation is to open KiCad and start drawing. Resist it. Drawing first means
the connectivity lives only in the drawing, which is exactly the trap the two dead
projects fell into — and it makes every later modification a redraw.

---

## Factoring — adapted from Vern

Vern's 26 drawings (`vx-aviation.com/sprocket/photos/panel_elec/schematics/`) split
into two kinds, and that distinction is the thing worth copying:

- **Subsystem schematics** — `MASTER`, `EFIS`, `EMS`, `AP`, `IGN`, `TRIM`,
  `LIGHTS1/2/3`, `AUDIO1/2/3`. Split by function; split again when one sheet gets
  crowded, rather than shrinking the drawing.
- **Cross-cutting reference sheets** — `TITLE` (index), `CONNECTORS` (pin tables),
  `AUDIO CABLES` (cable schedule). These are generated views.

Proposed N720AK sheet set. Starred sheets are **not captured anywhere today** —
they are the reason this project exists:

| Sheet | Covers |
|---|---|
| `TITLE` | Drawing index, revision history |
| `MASTER` | Battery, contactors, starter, alternator, MZ-30 generator, bus architecture |
| `GROUNDS` | Ground points: avionics ground, case ground, backshell ground, engine ground |
| `VPX` | VP-X Sport distribution and circuit list |
| `BUSMGR` | flyEFII System32 — fuel pumps, ignition feeds |
| `EBUS` | Emergency bus (active project — see `plans/electrical-mods-2026-annual.md`) |
| `EFIS` | SkyView HDX, ADAHRS, SkyView network |
| `EMS` | Engine sensors — the large EMS harness |
| `GTN` | GTN 650 nav/com/GPS, ARINC-429, serial |
| `AUDIO` | GMA 245, intercom, Bluetooth, alert inputs |
| `ANT` | Antennas and coax runs, with lengths |
| `XPDR` | Transponder and ADS-B |
| `AP` | Autopilot servos, 3-axis |
| `IGN` | EFII ignition |
| `FUEL` | Pumps, senders, pressure sensing |
| `LIGHTS` | Nav/strobe/landing/taxi/wig-wag, AeroSun VX, Pulsar |
| `TRIM` | Pitch/roll trim, stick grips |
| `PITOT` | Pitot heat, static, AoA |
| `O2` | MH oxygen |
| `ELT` | Artex 345 and remote |
| `ONSPEED` * | OnSpeed AoA |
| `WING` * | Wing-root CPC pinouts, wing wiring both sides |
| `TAILCONE` * | Tailcone wiring |
| `CONNECTORS` † | Pin tables — **generated** |
| `CABLES` † | Cable/harness schedule — **generated** |

Roughly 25 sheets, comparable to Vern's 26.

---

## Drawing conventions

Taken from Vern's `MASTER.pdf`, which is the clearest statement of what good looks
like for an airplane:

1. **Net name on every wire.** `MASTER-SW`, `ALT-FIELD`, `START-PWR`.
2. **AWG on every wire.** `2AWG`, `20AWG`, `28AWG FUSELINK`.
3. **Off-sheet links written `SHEET/NET`** — `EMS/AMPS+`, `IGN/IGN-PWR`,
   `LIGHTS3/START-SW` — drawn as a flag. Simple, greppable, unambiguous.
4. **Connector-type glyphs with an on-sheet legend** (Vern: diamond = CPC panel
   connector, circle = stick connector).
5. **Distinct ground nets, not one `GND`.** Vern separates `GF` from `GENG`;
   N720AK's drawings already name avionics / case / backshell grounds. Keep them
   distinct — a shared `GND` symbol hides exactly the kind of fault that is hard to
   find later.
6. **Physical-location notes in plain text** — *"Contactor located on right
   instrument panel bulkhead."* These are what make a drawing useful in the hangar.
7. **Manufacturer part numbers on components.**
8. **Title block** on every sheet: aircraft, system, author, date, sheet name.
9. **Detail insets** where a physical pinout helps (Vern's "RELAY BOTTOM VIEW").

And from the OnSpeed `schematic-capture` agent, the rule that most determines
whether a sheet is readable:

> **Label discipline.** Place a label ONLY for (a) power rails and (b) off-sheet
> signals. **Every other net is local: connect it with wires, no label.** Dumping
> auto-generated net names into the drawing is *the* failure mode.

---

## Reusable tooling — `flyonspeed/OnSpeed-Gen3-hardware`

That repo contains a mature "schematics as code" framework, ~10,000 lines of
Python, built for exactly this shape of problem (reconstruct a known-correct design
in KiCad, provably).

**Nine Claude agents** in `.claude/agents/`: `kicad-ops`, `schematic-capture`,
`symbol-librarian`, `netlist-verifier`, `footprint-engineer`, `layout-router`,
`electrical-engineer`, `design-reviewer`, `datasheet-analyst`, `pm-integrator`.
The first four are directly relevant; the PCB-oriented ones are not — **we have no
PCB.** This is schematic capture only.

**The generator** in `kicad/gen/`:

| Module | Does |
|---|---|
| `schgen.py` | Emits `.kicad_sch` S-expressions |
| `wirelib.py` | Wired-layout framework — real wires and junctions |
| `engine.py` | Label-driven sheet generation |
| `render.py` / `render_png.py` | `kicad-cli` → PDF → PNG for visual review |
| `overlap_check.py` | Automated check that symbols don't collide |
| `text_crowd.py` | Automated check that text doesn't sit on parts or wires |
| `diffnet.py` | Netlist diff by node-set |
| `verify_sheet.py` / `verify_all.py` | Per-sheet and whole-design verification |
| `eco001.py` … `eco012.py` | **Each engineering change as a script** |

Two patterns are worth stealing outright:

- **Automated drawing-quality QA.** `overlap_check` and `text_crowd` mechanise the
  rules above. A human reviewing 25 sheets by eye will miss things; a script won't.
- **ECOs as scripts.** Each modification is a committed, reviewable script that
  transforms the design, with an ID. That is precisely *"record our modifications"*
  — the airplane's change history becomes executable and auditable rather than a
  changelog someone hopes is accurate.

### The version problem — decide this first

| Thing | Schematic format |
|---|---|
| OnSpeed generator output | `20251024` (KiCad 10) |
| Existing N720AK project | `20231120` (KiCad 7/8) |
| **KiCad installed on this machine** | **9.0.6** |

The generator emits a format our KiCad cannot open. Options:

1. **Upgrade to KiCad 10.** Simplest; the framework is proven at v10. Recommended.
2. Adapt `schgen.py` to emit v9. Real work, and we'd be maintaining a fork.

Also note `kicad-cli` is **not on `PATH`** — it lives at
`/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli`.

A KiCad MCP server exists (swig backend) and OnSpeed used it, but their
`schematic-capture` agent concluded the MCP backend lagged their KiCad version and
authored text directly instead. **Author text, validate with `kicad-cli`.**

---

## Phases

**Phase 0 — decide.** KiCad 10 upgrade; where the project lives (repo vs GDrive —
see open questions); confirm the sheet list above.

**Phase 1 — extraction.** Parse the three SteinAir PDFs into a draft
`wirelist.tsv`. Columns at minimum: net, from-refdes, from-pin, to-refdes, to-pin,
AWG, colour, sheet, notes. Expect to hand-correct. **This is the deliverable that
matters** — if Phase 1 is right and KiCad never happens, the project still
succeeded.

**Phase 2 — scaffold.** Port `kicad/gen/` into the repo. Project skeleton,
`${KIPRJMOD}`-relative library tables, audit the salvaged connector symbols, prove
`kicad-cli` round-trips. One sheet end to end as a vertical slice — `O2` is the
obvious candidate at 198 words.

**Phase 3 — capture.** Generate sheets from the wire list, one at a time, each
verified by netlist diff against the extracted list and by the overlap/text-crowd
checks. Render and visually inspect every sheet before calling it done.

**Phase 4 — the uncaptured systems.** OnSpeed, wing wiring, tailcone. No source
PDF exists; these come from the aircraft, the sys-* pages, and inspection. Slower,
and the highest-value part of the whole project.

**Phase 5 — generated views.** `CONNECTORS` pin tables, `CABLES` schedule, BOM.
Mechanical once the wire list is trustworthy.

**Phase 6 — ECO process.** Adopt ECOs-as-scripts for modifications going forward.
Backfill recent ones: the emergency-bus work, the MZ-30 generator, the COM 1
feedline.

---

## Open questions

1. **Where does the project live?** The repo gives version control and review,
   which is most of the value. But `build.sh` only compiles sections 00–09 for the
   PDF, so KiCad files would need to sit outside that — and binary-ish schematic
   files in a handbook repo is a judgement call. GDrive gives sharing but no diffs.
   **Recommendation: the repo.** Diffability is the whole point.

2. **Upgrade KiCad to 10?** Recommended, see above.

3. **How much does the wire list need to carry?** Minimum is connectivity. Richer
   options: wire colour, AWG, terminal type, routing path, length, splice
   locations. Richer costs more to populate and more to keep true. Suggest starting
   at net/from/to/AWG/colour/sheet and growing only where a question actually
   demanded it.

4. **RV-801** — the Linear issue naming Vern's style could not be read; no API key
   is configured on this machine.

---

## Reference

- Vern Little's drawings: `vx-aviation.com/sprocket/photos/panel_elec/schematics/`
  (26 sheets; `MASTER.pdf` and `CONNECTORS.pdf` are the two to study)
- OnSpeed framework: `github.com/flyonspeed/OnSpeed-Gen3-hardware`, `kicad/gen/`
  and `.claude/agents/`
- Source PDFs: `~/Dropbox/N720AK/Schematics/`
- Existing connector symbols: GDrive
  `Public/Schematics/kicad_project/libraries/RV10_Connectors.kicad_sym`
