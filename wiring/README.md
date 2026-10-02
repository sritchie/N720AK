# Wire List

**The source of truth for N720AK's wiring.** One TSV per drawing. Schematics,
connector pin tables, cable schedules and the BOM are all generated *from*
these files — see `plans/kicad-schematics.md`.

The drawings are the output. These tables are the thing.

## Columns

| Column | Meaning |
|---|---|
| `sheet` | Which drawing this wire belongs to |
| `net` | Net name. Blank where the source drawing names no net; assigned during review |
| `from_ref` / `from_pin` | Origin connector and pin |
| `to_ref` / `to_pin` | Destination connector and pin. Blank `to_pin` with a plain-text `to_ref` means the wire leaves the drawing |
| `color` | Wire colour as the drawing records it |
| `awg` | Gauge. Blank where the drawing does not state it |
| `protection` | Breaker, fuse or current limiter on the circuit (`10A-4` is a VP-X channel: 10 A, channel 4). Needed for the wire-gauge-vs-protection check |
| `notes` | Anything a reader needs, including how an ambiguous row was resolved |
| `review` | **Non-empty means the parser could not determine this row.** Zero flagged rows is the goal for a finished sheet |

## Generating

```bash
uv run --with pymupdf python3 scripts/wirelist_extract.py --sheet O2
```

Extraction is deterministic and re-runnable, so **corrections belong in the
extractor, not in the TSV** — hand-edits are lost on the next run. That mirrors
how the schematic generator works.

To work out a new drawing's layout before writing an extractor for it:

```bash
uv run --with pymupdf python3 scripts/wirelist_extract.py --dump path/to.pdf
```

## What the text layer cannot tell you

The SteinAir PDFs carry every pin number and wire colour as real positioned
text, which is what makes this tractable. Two things are **drawn, not written**,
and no amount of parsing will recover them:

- **Junction dots** — a tap off an existing wire
- **Shield drains** — the long ovals representing cable shields

Both must be resolved by reading the rendered drawing, and the resolution is
then encoded in the extractor with a note recording that it came from visual
inspection. `O2.tsv` has seven such rows.

## Sheets

| Sheet | Source | Rows | Flagged |
|---|---|---|---|
| `O2` | `MH_Oxygen.pdf` | 30 | 0 |
| `PWR` | `Power__Lighting.pdf` | 128 | 1 |
| `SV` | `SV_Interconnect.pdf` | 190 | 3 |
| `WING` | handbook tables (`sys-24`, `sys-33`) | 111 | 38 |
| `EMS` | handbook table (`sys-24`) | 33 | 0 |
| `ONSPEED` | `changes.tsv` only | — | — |

`PWR` is not one table but several regions on a 40-inch sheet: the four VP-X
connector tables, both switch-panel DB15s, the essential bus, the Bus Manager
/ battery / starter region, and the annunciator. The VP-X tables are parsed;
the schematic regions are transcribed from the rendered drawing with the text
layer supplying labels and gauges. Every flagged row says why. The one region
not yet broken out is the inside of the two switch panels (switch to DB15).

`SV` is traced rather than read: its pin names are text, but which pin connects
to which exists only in the line geometry. `scripts/sch_trace.py` rebuilds the
connectivity from the PDF's vector paths. Its module docstring records the
drawing conventions it relies on, every one of which was found by a wire going
missing or two nets fusing:

- wires **hop** crossings with small arcs, which must be bridged
- **dashed** lines are annotation (the GPS-250 "Builder Connection") and must
  not conduct
- some **box outlines** are drawn as plain lines, and must be removed before
  tracing or every wire landing on them fuses
- each pin number is printed on **both sides** of its row and is one node
- **black** filled circles are junctions; **white** ones are headset-jack
  contacts, read three to a jack as tip, ring and sleeve
- **dashed rectangles** are devices (the grips); a wire ending inside one lands
  on the button whose label sits directly above it
- the drawing leaves sub-point gaps at some corners, so coordinates are snapped
  per axis, and duplicated strokes are removed

Not yet extracted from `SV`: the SkyView network block diagram, the servo DB-9s,
and the two pinout reference tables.

## Sheets no drawing covers

`WING` (both wings, the under-seat terminal blocks, the tail feeds) and `EMS`
(the EMS-220's 37-pin connector) come from the owner's typed build notes as
they live in the handbook: the wing-root, wingtip, terminal-block and EMS
tables in `sections/sys-24-electrical.md` and `sections/sys-33-lighting.md`.
`scripts/wirelist_handbook.py` **reads those tables** rather than retyping
them, so the wire lists cannot drift from the handbook. Change a pin there and
re-extract. A function text the extractor does not recognise stops it, so a
handbook edit can never be silently dropped.

A handbook table records one connector. Joining two connectors is an
inference, and every join says what it rests on: the same bundle and colour
at both ends (root and tip CPC), the same function named at both ends
(TB-R "Taxi power" and the VP-X output PWR calls `TAXI LIGHTS POWER`), or a
manufacturer's colour code matching one for one (Dynon's servo pigtail, Ray
Allen's trim sensor leads). A join none of those settles is not drawn: it is
flagged with the question that would settle it, and every row sharing that
question becomes one item on `INSPECT.md`. That is why `WING` has 38 flagged
rows but they come down to six questions on the checklist. Most are the two light
bundles, whose harness colours nobody wrote down against function.

## KiCad sheets

```bash
uv run python3 scripts/kicad_harness.py --render     # every sheet, plus the project
uv run python3 scripts/kicad_harness.py O2           # one sheet
```

Open `kicad/n720ak/n720ak.kicad_pro` in KiCad 10 for the whole thing.

`scripts/kicad_harness.py` turns a wire list into a KiCad 10 sheet in
`kicad/n720ak/`, then **proves it**: it exports the netlist with `kicad-cli`
and diffs it, node set by node set, against the wire list it came from. A
sheet is only correct if that diff is clean, and the generator will not
silently produce a wrong one.

| Sheet | Connectors | Wires | Nets | Verified |
|---|---|---|---|---|
| `PWR` | 35 | 130 | 70 | clean, 0 ERC errors |
| `SV` | 32 | 188 | 100 | clean, 0 ERC errors |
| `O2` | 6 | 30 | 24 | clean, 0 ERC errors |
| `ONSPEED` | 3 | 13 | 10 | clean, 0 ERC errors |
| `EMS` | 8 | 34 | 29 | clean, 0 ERC errors |
| `WING` | 15 | 73 | 41 | clean, 0 ERC errors |
| project | 99 | | 252 | clean: all sheets together |

Rows still flagged for review are left off the drawings rather than drawn as
guesses.

The `.kicad_sch` files are **generated** — the title block says so. Edit the
wire list or its extractor and regenerate; hand edits in KiCad would be lost
and, worse, would make the drawing disagree with the source of truth.

Layout: a sheet with one connector on the left is drawn with its rows lined
up against the pins they feed, so wires run straight across the way the
SteinAir originals read. Larger sheets are stacked, with the right column
offset half a pitch so that no two pins share a height and every wire has its
own lane — which makes accidental contact between wires impossible rather than
unlikely. The generator tries the first and keeps it only if it verifies.

The sheets are tied into one hierarchical project by a generated root sheet.
Global labels with the same name on different sheets join, which is how an
off-sheet flag means the same net everywhere. UUIDs are deterministic, so
regenerating an unchanged wire list produces a byte-identical file and git
diffs show only real changes.

The project is verified as a whole too: its netlist must equal the union of
every sheet's wire list, which proves each cross-sheet label merges the nets
it should. It is what shows, for example, EMS pin 10 reaching the roll trim
sensor through TB-L 3 and left wing-root pin 12, with three sheets involved.
A connector belongs to one sheet. Others refer to it by label, and drawing
the same connector on two sheets fails the build.

Not yet done: a presentation pass toward Vern's look, and canonical names for
the older cross-sheet references. The power sheet still calls the right PFD's
power pin `SV-HDX1100 (PFD2) D37-1/20` as a label, while the SkyView sheet
draws that connector as a part, so those few references are checked by eye.
The labels the wing and EMS sheets share with each other and with PWR and SV
were chosen to match, and are netlist-checked. The sheets are correct before
they are pretty, on purpose.

## Changes since the drawings

The SteinAir drawings are dated 2017. `changes.tsv` records every modification
since, numbered and dated; `scripts/wirelist_changes.py` applies them to give
`as-built/<SHEET>.tsv`, and the KiCad sheets are drawn from the as-built lists.

| Action | Effect |
|---|---|
| `add` | a new wire |
| `remove` | delete the wire between two pins |
| `disconnect` | take a pin out of its net; the rest of the net stays joined |
| `rename` | a box replaced by its successor, wiring unchanged |

Changes apply in file order, which is date order. The ids are labels only:
C029 (the CO detector's Dec 2025 replacement) sits above C006 because it
happened first.

## Checks

Two kinds of mechanical check keep the wire lists honest:

- **Hand-entered regions are verified against the drawing.** The power sheet's
  schematic regions (essential bus, annunciator, Bus Manager) are entered by
  hand; `POWER_TRACE_CHECKS` in the extractor lists every connection they
  claim, and extraction fails unless the line tracer finds each one in the
  drawing's geometry - plus assertions that switch contacts are open and
  separate wires stay separate. 34 checks today.
- **Every KiCad sheet is verified against its wire list**, node set by node set.

## Condition inspection

`INSPECT.md` is the hangar checklist, generated by `scripts/wirelist_inspect.py`:
every question the drawings and build notes cannot settle, every drawn wire
whose notes say "Confirm at inspection:" (the record gives the connection, but
something about it does not add up), and every change recorded from memory. Extraction work still to do is kept off it - that needs the
drawings, not the airplane.

A change that no longer matches anything stops the build, so re-running an
extractor can never silently put the old wiring back. Only `done` changes are
applied; `planned` ones are recorded but do not alter the drawings.
