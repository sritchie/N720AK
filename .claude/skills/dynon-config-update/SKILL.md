---
name: dynon-config-update
description: File new Dynon config downloads, diff against previous versions, update GDrive links and documentation
---

# Dynon Config Update

Use when the user says they've downloaded new configs, pulled configs from a Dynon display, or needs to file Dynon .sfg/.dfg files.

## File Naming Convention

`YYYY-MM-DD-N720AK-SN{serial}-{version}-{TYPE}.{ext}`

- SN10980 = HDX800 (pilot side)
- SN11668 = HDX1100 (copilot side)
- SN11672 = third display (model/position unconfirmed — appeared in the 2026-07-27 SkyView 17.5 upgrade's settings_archive backups)
- `.sfg` = SENSOR_CONFIG (sensor definitions, transfer functions, min/max)
- `.dfg` = USER_CONFIG (display ranges, color bands, alarms, widget layout)

**Contact alarm text indicators**: controlled by `range_name` fields in USER_CONFIG.dfg. Setting `range_name=` (empty string) removes the text overlay while keeping the color indicator — e.g. LDOOR/RDOOR have empty range names (no text), while PHEAT has `range1_name=ON` and `range2_name=OFF` (shows text).

## Workflow

### 1. Identify Downloads

Find the new config files (typically in `~/Downloads/`). Confirm serial number and firmware version from the filename.

### 2. Diff Against Previous

Compare the new .sfg and .dfg against the most recent versions in GDrive:

```
~/Library/CloudStorage/GoogleDrive-sritchie09@gmail.com/My Drive/N720AK/Public/Configs/Dynon/
```

Use `diff` to identify what changed. Report changes to the user — especially any sensor definition changes (min_val, max_val, transfer functions, new sensors).

### 3. Copy to GDrive

Copy both files to the GDrive Dynon config folder (source of truth):

```bash
cp ~/Downloads/YYYY-MM-DD-*.sfg ~/Downloads/YYYY-MM-DD-*.dfg \
  ~/Library/CloudStorage/GoogleDrive-sritchie09@gmail.com/My\ Drive/N720AK/Public/Configs/Dynon/
```

### 4. Extract GDrive File IDs

Wait for GDrive to sync, then extract file IDs:

```bash
xattr -p com.google.drivefs.item-id#S "/path/to/file"
```

URL format: `https://drive.google.com/file/d/{ID}/view`

If IDs aren't available yet, add "pending GDrive sync" rows and remind the user to update later.

### 5. Update `docs/gdrive-links.md`

Add new rows to the **Configs → Dynon** table with the date, description (include serial/display name), and GDrive link.

### 6. Update Memory

Update `reference_dynon_sensor_config.md` in the claude-home memory system:
- Change "Latest as of" date
- Document any sensor definition changes

### 7. Document Sensor Changes

If sensor definitions changed in the .sfg:
- Update `sections/sys-42-avionics.md` (EMS Sensors table, MAP Blanking section)
- Update `CLAUDE.md` if MAP or fuel pressure sensor details changed
- Update `.claude/skills/flight-data-analysis/SKILL.md` if blanking thresholds changed

### 8. Log in avionics-log.tsv

Add entry to `~/Library/CloudStorage/GoogleDrive-sritchie09@gmail.com/My Drive/N720AK/Private/Maintenance/avionics-log.tsv` for any sensor definition modifications. Format: tab-separated, date in YYYY-MM-DD, performed by "Sam Ritchie (Repairman 5256450)".

### 9. Remind User

If sensor definitions were modified in the .sfg, remind the user:
- **The updated .sfg must be loaded back onto the Dynon display** via USB to take effect
- Only the display matching the serial number needs the update
- The .dfg (display config) is separate and may also need to be loaded if changed
