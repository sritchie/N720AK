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
| `PWR` | `Power__Lighting.pdf` | 115 | 18 |
| `SV` | `SV_Interconnect.pdf` | 175 | 19 |

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

Not yet extracted from `SV`: the SkyView network block diagram, the servo DB-9s,
and the two pinout reference tables. Then the systems no drawing covers —
OnSpeed, wing and tailcone.

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
| `O2` | 6 | 30 | 24 | clean, 0 ERC errors |
| `PWR` | 24 | 97 | 59 | clean, 0 ERC errors |
| `SV` | 19 | 156 | 71 | clean, 0 ERC errors |

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

Not yet done: a presentation pass toward Vern's look, and canonical connector
names across sheets — the power sheet calls the right PFD's power pin
`SV-HDX1100 (PFD2) D37-1/20` as a label, while the SkyView sheet draws that
connector as a part. Until those names agree, cross-sheet references are
checked by eye rather than by the netlist. The sheets are correct before they
are pretty, on purpose.
