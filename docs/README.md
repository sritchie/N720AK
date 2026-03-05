# Reference Documents

Manufacturer PDFs, manuals, schematics, and configs live on **Google Drive**, not in git. This keeps the repo small and lets us share public links from the website.

## Google Drive Structure

All reference files are in `My Drive/N720AK/` on Google Drive:

| Folder | Sharing | Content |
|--------|---------|---------|
| `Public/Manuals/{ATA}/` | Anyone with link | Manufacturer manuals by ATA chapter |
| `Public/Schematics/` | Anyone with link | Wiring diagrams, system schematics |
| `Public/Configs/` | Anyone with link | Dynon sensor/user configs, OnSpeed calibrations |
| `Public/Performance/` | Anyone with link | ADSB reports, airspeed data, prop balance |
| `Public/Weight-Balance/` | Anyone with link | W&B worksheets |
| `Private/` | Owner only | Invoices, insurance, keys, registration |
| `Archive/` | Owner only | Van's construction drawings, brochures, reference POHs |

## Linking from System Pages

System pages in `sections/sys-*.md` link to Google Drive using shareable URLs:

```markdown
## References
- [EFII System32 Installation Manual (Rev 9-13)](https://drive.google.com/file/d/{FILE_ID}/view)
```

## URL Registry

See [gdrive-links.md](gdrive-links.md) for a mapping of all public files to their Google Drive URLs.

## What Goes in `docs/`

Only small custom diagrams or pinouts created specifically for sys-*.md pages. No manufacturer PDFs.
