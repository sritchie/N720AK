# Reference Documents

Manufacturer PDFs, install guides, and reference materials organized by ATA chapter number.

## Directory Structure

| Directory | ATA Chapter | Content |
|-----------|-------------|---------|
| `22-autopilot/` | ATA 22 | Dynon AP install guide, servo manuals |
| `23-communications/` | ATA 23 | GMA 245 pilot guide, antenna specs |
| `24-electrical/` | ATA 24 | VPX Sport manual, EarthX specs, System32 bus docs |
| `27-flight-controls/` | ATA 27 | Tosten grip docs |
| `28-fuel-system/` | ATA 28 | Aeromotive regulator specs, Walbro pump docs, Andair valve |
| `33-lighting/` | ATA 33 | AeroLEDs install guides |
| `34-navigation/` | ATA 34 | Dynon Skyview guides, GTN 650 manual, OnSpeed docs |
| `35-oxygen/` | ATA 35 | Mountain High EDS-4iP manual |
| `42-avionics/` | ATA 42 | Wiring diagrams, connector pinouts |
| `61-brakes/` | ATA 61 | Brake caliper docs, wheel specs |
| `71-engine/` | ATA 71 | Lycoming operator's manual, overhaul manual |
| `73-efii/` | ATA 73 | EFII System32 manual, tuning guides, wiring docs |
| `84-propeller/` | ATA 84 | Prop manual, governor docs |
| `misc/` | — | Anything that doesn't fit a specific chapter |

## Naming Convention

Use descriptive filenames, not generic names:

- `dynon-skyview-install-guide-rev15.pdf` (good)
- `manual.pdf` (bad)
- `aeromotive-13109-regulator-datasheet.pdf` (good)
- `datasheet.pdf` (bad)

## Linking from System Pages

System pages in `sections/sys-*.md` link to docs using relative paths:

```markdown
## References
- [Dynon Skyview Installation Guide](../docs/34-navigation/dynon-skyview-install-guide.pdf)
```
