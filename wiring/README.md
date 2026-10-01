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

`PWR` is not one table but several regions on a 40-inch sheet: the four VP-X
connector tables, both switch-panel DB15s, the essential bus, the Bus Manager
/ battery / starter region, and the annunciator. The VP-X tables are parsed;
the schematic regions are transcribed from the rendered drawing with the text
layer supplying labels and gauges. Every flagged row says why. The one region
not yet broken out is the inside of the two switch panels (switch to DB15).

Still to do: `SV_Interconnect.pdf` (3,181 words), then the systems no drawing
covers — OnSpeed, wing and tailcone.
