---
name: checklist-update
description: Update aircraft checklists via the EFIS Editor JSON workflow. Use when the user wants to add, remove, or modify checklist items.
argument-hint: [checklist name and change description]
user-invocable: true
---

# Checklist Update

The user wants to modify an aircraft checklist.

## Input

$ARGUMENTS

## Context

N720AK checklists are managed through a specific sync workflow:

**Canonical source**: https://rdamazio.github.io/efis-editor/checklists#N720AK

**Files in repo:**
- `N720AK.json` — Checklist data exported from EFIS Editor
- `sections/04-emergency.md` — GENERATED from JSON (emergency procedures)
- `sections/04b-abnormal.md` — GENERATED from JSON (abnormal procedures)
- `sections/05-normal.md` — GENERATED from JSON (normal procedures)

**IMPORTANT**: Sections 04, 04b, and 05 are GENERATED — never edit them directly.

## Steps

1. **Read `N720AK.json`** to understand current checklist structure
2. **Identify which checklist** the user wants to change (emergency, abnormal, or normal)
3. **Make the change in `N720AK.json`** — add, remove, or modify checklist items
4. **Regenerate the markdown** by running:
   ```bash
   python3 json_to_markdown.py N720AK.json
   ```
5. **Verify the output** — read the regenerated markdown to confirm it looks right
6. **Remind the user** about the full sync workflow:
   - Upload the updated JSON back to EFIS Editor (manual step)
   - Export to Dynon (.txt) for the Skyview HDX
   - Export to ForeFlight (.fmd) for the EFB
   - The POH HTML/PDF will update automatically on next build

## Checklist Item Format in JSON

Refer to the existing `N720AK.json` for the exact schema. Items typically have:
- Title/name
- Type (challenge-response, note, caution, warning)
- Steps with expected responses
