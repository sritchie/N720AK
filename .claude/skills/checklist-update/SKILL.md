---
name: checklist-update
description: Use when the user wants to add, remove, or modify aircraft checklist items, regenerate the Dynon or ForeFlight checklist exports, or asks about the EFIS editor / checklist pipeline.
---

# Checklist Update (local EFIS pipeline)

**Canonical source: `N720AK.json` in this repo.** The rdamazio EFIS-editor
website is no longer in the loop — all exports are generated locally by
scripts ported from its source (verified byte-identical against a real site
export, 2026-08-19).

## Files

| File | Role |
|---|---|
| `N720AK.json` | Source of truth — full checklist, EFIS-editor JSON schema |
| `N720AK-panel.json` | GENERATED terse variant — never hand-edit |
| `sections/04*.md`, `05-normal.md` | GENERATED POH sections — never hand-edit |
| `scripts/make_panel_checklist.py` | Strips ITEM_PLAINTEXT/ITEM_NOTE detail (keeps Memory Items intact) |
| `scripts/export_dynon_checklist.py` | JSON → Dynon .txt (31-col default; `--variant 40/none`) |
| `scripts/export_foreflight_checklist.py` | JSON → ForeFlight .fmd (AES; needs `uv run --with cryptography`); `--decrypt` reads an .fmd back |
| `json_to_markdown.py` (repo root) | JSON → POH markdown sections |

## Workflow

1. Edit `N720AK.json` (item types: ITEM_CHALLENGE_RESPONSE with prompt/
   expectation; ITEM_PLAINTEXT/ITEM_NOTE for detail that only ForeFlight
   should show; ITEM_TITLE for `** headers **`; ITEM_WARNING/CAUTION;
   ITEM_SPACE. Optional per-item: `indent`, `centered`.)
2. `python3 scripts/make_panel_checklist.py`
3. `python3 scripts/export_dynon_checklist.py N720AK-panel.json checklist.txt`
   — the terse in-panel version. Dynon loads only a file named
   **`checklist.txt`** from USB root: SETUP MENU > SYSTEM SOFTWARE > LOAD FILES.
4. `uv run --with cryptography python3 scripts/export_foreflight_checklist.py N720AK.json N720AK.fmd`
   — the detailed version. Import into ForeFlight (open the .fmd on the iPad).
5. `python3 json_to_markdown.py N720AK.json` then `./build.sh` — POH.
6. Send the user the generated checklist.txt / N720AK.fmd; commit JSON +
   regenerated markdown + panel JSON via branch + PR per repo git workflow.

## Visual editing fallback

The web app still works for visual editing, run locally so there is no
dependency on the hosted site: `git clone https://github.com/rdamazio/efis-editor
&& cd efis-editor && npm ci && npm start` — then import/export `N720AK.json`.
If its export format ever changes, re-verify the Python exporters against a
fresh export (diff modulo the Last-updated date line).

## Gotchas

- The Dynon display keeps whatever was last loaded — check the export footer
  ("LAST UPDATED ...") to see which version the panel is actually running.
- Detail rows belong in the JSON as ITEM_PLAINTEXT/ITEM_NOTE so the panel
  filter can strip them; never encode detail inside an expectation string.
- Memory Items are prose by design — the panel filter preserves them fully.
