# N720AK RV-10 Pilot's Operating Handbook

This repository contains the Pilot's Operating Handbook (POH) for **N720AK**, a Van's RV-10 experimental aircraft. The POH follows [GAMA Specification No. 1](https://gama.aero/documents/gama-specification-1-specification-for-pilots-operating-handbook-version-2-0/) format.

## Repository Purpose

1. **POH Source Files**: Markdown files in `sections/` that compile to PDF and HTML
2. **Checklist Sync**: `N720AK.json` synced from the EFIS Editor for Dynon/ForeFlight export
3. **Weight & Balance**: Exportable W&B data for sharing with other pilots
4. **GitHub Pages**: Auto-deploys HTML version on push to main (target: n720ak.com)

## Linear (Task Manager)

Linear is used **only as a task manager** for pending work items. It is NOT a content store. Key rules:

- **Never store attachments or content in Linear** — all documents, PDFs, invoices, photos, and reference material go in Google Drive or the git repo
- **Never link to Linear issue URLs** from sys-*.md pages, GDrive files, or anywhere in the repo — Linear is not accessible to other users
- **Never reference Linear issue identifiers** (e.g., "Source: Linear RV-XXX") in archived content — once content is migrated out, all Linear provenance must be removed
- **Linear upload URLs expire** — JWT-signed `uploads.linear.app` URLs are valid for ~5 minutes. Never store these as permanent references.
- When closing an issue, the content should already be in its permanent home (GDrive or repo) before marking Done

### Linear API

Use the `linear` skill — it has the GraphQL-via-Python mechanics, the RV team ID, and the known close-by-UUID quirk.

## Checklist Synchronization

**Canonical checklist source**: `N720AK.json` in this repo. The EFIS-editor website is out of the loop — Dynon .txt and ForeFlight .fmd exports are generated locally by `scripts/export_dynon_checklist.py` and `scripts/export_foreflight_checklist.py` (ports of the efis-editor writers, golden-tested against a real export). `N720AK-panel.json` is the generated terse in-panel variant.

Sections 04/04b/05 are **generated** from `N720AK.json` — edit the JSON, never the markdown. Use the `checklist-update` skill for the full workflow.

## Build Commands

`./build.sh <pdf|html|serve|all>` — prerequisites in `README.md`, section-to-file mapping in `sections/SUMMARY.md`.

## Web Tools

`sections/tools/` holds static browser tools that mdBook copies verbatim into the site (e.g. `sections/tools/fta850/` → `n720ak.com/tools/fta850/`, the FTA-850 memory-book programmer over Web Serial). Logic lives in plain ES modules with node tests: `node --test tests/*.test.mjs`. Keep the DOM code thin and the protocol/codec code in the tested module.

## Aircraft Configuration - N720AK

The full system inventory and operational descriptions live in `sections/08-systems.md` (pilot-facing) and the `sys-*.md` pages (build/technical reference) — read those rather than expecting a summary here. Servicing specs (fluids, tire pressures, intervals) are in `sections/09-servicing.md`.

## What Goes Where: POH vs Systems Reference

### POH (Sections 00-09) — PDF + HTML

Information a **pilot** needs for **normal operation**. This is the GAMA Spec No. 1 content that compiles to both PDF and HTML.

**Section 8 - Systems Description:** How each system works (operational description), panel switch locations, stick grip layout, emergency bus behavior.

**Section 9 - Handling, Servicing:** Brake fluid type, tire pressures, oil specs, fuel specs, preflight items, service intervals.

### Systems Reference (sys-*.md) — HTML Only

Comprehensive technical reference for **how the airplane is built and how everything works**. This is NOT just maintenance — it's the complete "how is my airplane built" reference. Includes:

- Part numbers, suppliers, data sheets
- Wiring/plumbing details, AN fittings, routing
- Tuning notes, calibration data
- Diagnostic procedures and flight data analysis
- Lessons learned, installation quirks
- Photos with captions

**Key constraint:** Systems Reference pages use `sys-XX-` prefix (ATA chapter numbers). The PDF build in `build.sh` explicitly lists sections 00-09, so sys-* files are automatically excluded. No build changes needed.

Each system page links to manufacturer PDFs on Google Drive via shareable URLs (see `docs/gdrive-links.md` for the URL registry).

### Reference Documents — Google Drive

Manufacturer PDFs, manuals, schematics, and configs live on **Google Drive** (not in git). The `Public/` folder is shared read-only; sys-*.md pages link to these via stable Google Drive URLs. Claude reads files locally from the synced folder.

**Local sync path**: `~/Library/CloudStorage/GoogleDrive-sritchie09@gmail.com/My Drive/N720AK/`

| GDrive Folder | Sharing | Content |
|---------------|---------|---------|
| `Public/Manuals/{ATA}/` | Anyone with link | Manufacturer manuals by ATA chapter |
| `Public/Schematics/` | Anyone with link | Wiring diagrams, system schematics |
| `Public/Configs/` | Anyone with link | Dynon sensor/user configs, OnSpeed calibrations |
| `Public/Performance/` | Anyone with link | ADSB reports, airspeed data, prop balance |
| `Public/Weight-Balance/` | Anyone with link | W&B worksheets |
| `Private/` | Owner only | Invoices, insurance, keys, registration |
| `Private/Maintenance/` | Owner only | Digital maintenance logs (TSV), oil analysis |
| `Archive/` | Owner only | Van's construction drawings, brochures, reference POHs |

The `docs/` directory in git contains only `README.md`, `gdrive-links.md` (URL registry), and any small custom diagrams created for sys-*.md pages. No manufacturer PDFs in git.

**Getting Google Drive URLs for new files**: On macOS with Google Drive for Desktop, the file ID is stored in extended attributes. To get a shareable URL:
```bash
xattr -p com.google.drivefs.item-id#S "/path/to/file"
# Returns: 1abc123...
# URL: https://drive.google.com/file/d/1abc123.../view
```
After adding a file to `Public/`, extract the file ID with `xattr`, add it to `docs/gdrive-links.md`, and link from the relevant sys-*.md page.

### Analysis Scripts

Always use `uv` to run Python scripts (handles dependencies automatically), e.g. `uv run --with numpy --with matplotlib python3 scripts/regulator_diagnostic.py /path/to/log.csv`. Each script's header documents its flags; `plans/` holds the matching analysis workflows.

### Fuel System Quick Facts

- Fuel pressure setpoint: **45 PSI** (Dynon DIFF mode) on the **Borla 203133** regulator (installed 2026-03-17). **>1 PSI variation from 45 under load warrants investigation.**
- Auto-cutover trip (Bus Manager Pump 1 → Pump 2): 22 PSI absolute at the pump-side sense.
- Full system details: `sections/sys-28-fuel-system.md`. Sensor details, DIFF vs gauge math, and CSV formats: `.claude/skills/flight-data-analysis/reference.md` (loaded by the `flight-data-analysis` skill).

## Deployment

Push to `main` auto-deploys the mdBook HTML to GitHub Pages (target domain: **n720ak.com**).

## Git Workflow

**Never commit directly to main.** Always create a branch, open a PR, and squash merge.

**Branch awareness**: At the start of each session, check `git branch --show-current` and `git log --oneline main..HEAD`. If you're on a feature branch with commits ahead of main, that branch was likely already merged — verify with `gh pr list --state merged --head <branch>`. If merged, switch to main and pull before starting new work. If not merged, you can stack additional commits on the existing branch.

**Always start from fresh main.** Every new batch of changes must begin by switching to main, pulling latest, and creating a new branch. Do not make edits on stale branches or on main directly. The workflow is:
1. `git checkout main && git pull`
2. `git checkout -b descriptive-branch-name`
3. Make edits
4. Commit with an imperative-mood message
5. Push and open a PR with a summary
6. Squash merge the PR

When merging PRs, **always use squash merge** via `gh pr merge`:

```bash
gh pr merge <number> --squash \
  --subject "<PR title>" \
  --body "<PR description body>"
```

The squash commit title should be the PR title, and the body should be the PR description. This keeps `main` history clean with one commit per PR.

**Do not leave unstaged changes.** Every editing session should end with a clean working tree.

## Systems Reference TODOs

The `sys-*.md` pages contain `<!-- TODO -->` markers and TODO checklists for owner-supplied details. When the user wants to fill in details or work on a system page, use the `sys-reference` skill — it has the batch-interview workflow (3-5 related TODOs at a time, never the whole list) and the photo/PDF filing rules.

## Maintenance Logs (Digital)

N720AK maintains digital maintenance logs as TSV files in GDrive `Private/Maintenance/`, synced locally. These supplement (not replace) the paper logbooks — paper is still needed for condition inspection sign-offs and regulatory signatures. The maintenance skills know the file inventory and local path.

### Workflows

Use the skills: `maintenance-log` (log entries + proactive follow-up prompts), `squawk` (discrepancies), `oil-analysis` (Blackstone results), `ad-sb` (AD/SB compliance tracking and review), `condition-inspection` (annual inspection). Recurring intervals and last-done dates live in `recurring-items.tsv` — always check it, never assume.

### Maintenance Log Conventions

- **Performed By**: Always `Sam Ritchie (Repairman 5256450)` unless otherwise specified
- **No external references** in log entries — no URLs, no "see VAF post", no manual page citations. References belong in sys-* pages only.
- **No pending/future work** in logs or squawks — Sam tracks upcoming work in Linear. Only document completed work.
- **Squawks** are for long-lived discrepancies only, not for items about to be addressed.
- Log entries should be factual, past-tense descriptions of work performed.
- **Routine database cycles are not logged.** The 28-day Dynon/GTN nav and obstacle database updates get no avionics-log entries — the displays warn on expiry. Log avionics **software/firmware version changes** only.

## Construction Plans

Van's RV-10 construction plans (121 PDFs) are indexed in `docs/construction-plans-index.md`, with visually transcribed text in `docs/plans-text/`. Use the `construction-plans` skill for the search workflow and the N720AK build-deviation caveats.

## Dynon Configs

Dynon SkyView config snapshots (.sfg/.dfg) live in GDrive `Public/Configs/Dynon/`. Use the `dynon-config-update` skill for filing new downloads, diffing, and documentation updates.

## Editing Tips

- Use `<!-- placeholders -->` for missing data
- Tables use Pandoc pipe syntax
- Insert `\pagebreak` for PDF page breaks
- Images go in `images/` and reference as `![Alt](images/file.png)`
- Sections 4, 4b, 5 are **generated** - edit the JSON, not the markdown
