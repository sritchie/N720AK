#!/bin/bash
set -e

mkdir -p output

case "${1:-all}" in
  pdf)
    echo "Building PDF..."
    # Exclude SUMMARY.md (mdBook-only) from PDF build
    pandoc metadata.yaml \
      sections/00-introduction.md \
      sections/01-general.md \
      sections/02-limitations.md \
      sections/03-engine-info.md \
      sections/04-emergency.md \
      sections/04b-abnormal.md \
      sections/05-normal.md \
      sections/06-performance.md \
      sections/07-weight-balance.md \
      sections/08-systems.md \
      sections/09-servicing.md \
      --to=typst \
      --template=template.typ \
      --toc \
      --number-sections \
      -o output/poh.pdf
    echo "Done: output/poh.pdf"
    ;;

  html)
    echo "Building HTML site with mdBook..."
    mdbook build
    echo "Done: output/html/index.html"
    ;;

  serve)
    echo "Starting mdBook dev server..."
    mdbook serve --open
    ;;

  checklists)
    echo "Building cabin checklists PDF..."
    python3 json_to_checklist_pdf.py N720AK.json
    typst compile output/checklists.typ output/checklists.pdf
    echo "Done: output/checklists.pdf"
    ;;

  logbooks)
    echo "Building maintenance logbook PDFs..."
    uv run python3 scripts/build_logbooks.py --all --open
    ;;

  all)
    $0 pdf
    $0 html
    $0 checklists
    ;;

  *)
    echo "Usage: ./build.sh [pdf|html|serve|checklists|logbooks|all]"
    echo ""
    echo "  pdf        - Build PDF using Pandoc/Typst"
    echo "  html       - Build static HTML site using mdBook"
    echo "  serve      - Start mdBook dev server with live reload"
    echo "  checklists - Build cabin checklists PDF from N720AK.json"
    echo "  logbooks   - Build printable maintenance logbook PDFs from GDrive TSV records"
    echo "  all        - Build PDF, HTML, and checklists"
    exit 1
    ;;
esac
