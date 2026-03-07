#!/bin/bash
# One-time extraction of text from Van's RV-10 construction plan PDFs.
# Plans are static (won't change), so this only needs to run once.
# Usage: bash scripts/extract_plans_text.sh

DRAWINGS="/Users/sritchie/Library/CloudStorage/GoogleDrive-sritchie09@gmail.com/My Drive/N720AK/Archive/Construction-Drawings"
OUTPUT="docs/plans-text"
mkdir -p "$OUTPUT"

echo "=== Extracting core plans and FF kits ==="
for f in "$DRAWINGS"/*_10.pdf; do
  base=$(basename "$f" .pdf)
  echo "  $base"
  pdftotext -layout "$f" "$OUTPUT/${base}.txt" 2>/dev/null
done

echo "=== Extracting flowchart ==="
pdftotext -layout "$DRAWINGS/10 DWG 1-3 3-View, Cutaway, Flowchart.pdf" \
  "$OUTPUT/flowchart.txt" 2>/dev/null

echo "=== Extracting Optional Parts drawings ==="
for f in "$DRAWINGS/Optional Parts Drawings/"*.pdf; do
  # Extract OP number from filename (e.g., "OP-36 RV-10 Wingtip Lighting.pdf" -> "OP-36")
  base=$(basename "$f" .pdf)
  op=$(echo "$base" | grep -oE '^OP-[0-9]+[A-Z]?')
  if [ -n "$op" ]; then
    echo "  $op"
    pdftotext -layout "$f" "$OUTPUT/${op}.txt" 2>/dev/null
  fi
done

echo "=== Extracting manual sections ==="
for f in "$DRAWINGS"/Manual\ Section\ *.pdf; do
  num=$(basename "$f" .pdf | grep -oE '[0-9]+')
  echo "  manual-section-${num}"
  pdftotext -layout "$f" "$OUTPUT/manual-section-${num}.txt" 2>/dev/null
done

pdftotext -layout "$DRAWINGS/RV-10 Manual - Main.pdf" "$OUTPUT/manual-main.txt" 2>/dev/null
pdftotext -layout "$DRAWINGS/RV-10 Manual - Design Philosophy.pdf" "$OUTPUT/manual-design-philosophy.txt" 2>/dev/null
pdftotext -layout "$DRAWINGS/RV-10 Manual - Section 4.pdf" "$OUTPUT/manual-section-4-parts-index.txt" 2>/dev/null
pdftotext -layout "$DRAWINGS/RV-10 Manual - Table of Contents.pdf" "$OUTPUT/manual-toc.txt" 2>/dev/null
pdftotext -layout "$DRAWINGS/RV-10 Manual - Title Page.pdf" "$OUTPUT/manual-title.txt" 2>/dev/null
pdftotext -layout "$DRAWINGS/Plans Warning Cover Page.pdf" "$OUTPUT/plans-warning.txt" 2>/dev/null
echo "  manual sections done"

# Remove empty files (drawing-only PDFs with no text layer)
echo "=== Removing empty files (drawing-only PDFs) ==="
find "$OUTPUT" -name "*.txt" -size 0 -print -delete

echo "=== Done ==="
echo "Files in $OUTPUT/:"
ls -1 "$OUTPUT/" | wc -l
echo "total files"
