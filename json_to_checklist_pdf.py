#!/usr/bin/env python3
"""Convert N720AK.json checklist to a Typst document for PDF export.

Reads the EFIS Editor JSON format and generates a Typst file that produces
a laminated cabin checklist PDF matching the efis-editor PDF export style.

Usage:
    python3 json_to_checklist_pdf.py N720AK.json
    # Produces output/checklists.typ, then compile with:
    # typst compile output/checklists.typ output/checklists.pdf
"""

import json
import sys
import os


# Category → color mapping (group banner backgrounds)
# These match the CSS named colors used by jsPDF in the efis-editor
CATEGORY_COLORS = {
    "normal": ("0000FF", "FFFFFF"),     # CSS 'blue', white text
    "abnormal": ("FFA500", "000000"),   # CSS 'orange', black text
    "emergency": ("FF0000", "FFFFFF"),  # CSS 'red', white text
}

# Checklist title bar color (jsPDF-AutoTable default header)
TITLE_BAR_BG = "2980B9"
TITLE_BAR_FG = "FFFFFF"

# Row colors
ROW_EVEN = "F5F5F5"  # light gray
ROW_ODD = "FFFFFF"   # white
NOTE_BG = "F0F0F0"   # slightly darker gray for notes

# Column widths matching the original 3-column table layout
PROMPT_WIDTH = "27%"    # fixed left column for prompts
EXPECT_WIDTH = "18%"    # fixed right column for expectations


def escape_typst(text: str) -> str:
    """Escape special Typst characters in text."""
    if not text:
        return ""
    for ch in ["\\", "#", "$", "@", "<", ">", "_", "*", "`", "~"]:
        text = text.replace(ch, "\\" + ch)
    return text


def generate_cover_page(metadata: dict) -> str:
    """Generate the cover page matching efis-editor layout.

    Title at ~25% down the page, metadata at ~75%.
    """
    name = escape_typst(metadata.get("name", ""))
    model = escape_typst(metadata.get("makeAndModel", ""))
    aircraft = escape_typst(metadata.get("aircraftInfo", ""))

    return f"""// Cover page
#page(margin: 7%, footer: none)[
  #v(1fr)

  #align(center)[
    #text(size: 30pt, weight: "bold")[Checklists]
  ]

  #v(4fr)

  #align(center)[
    #text(size: 12pt, weight: "bold")[Aircraft:]
    #v(2pt)
    #text(size: 20pt, weight: "bold")[{aircraft}]

    #v(0.8cm)

    #text(size: 12pt, weight: "bold")[Aircraft make/model:]
    #v(2pt)
    #text(size: 20pt, weight: "bold")[{model}]
  ]

  #v(2fr)

  #align(center)[
    #text(size: 8pt, fill: rgb("666666"))[Generated from N720AK.json]
  ]
]
"""


def generate_group_header(title: str, category: str) -> str:
    """Generate a full-bleed group header banner.

    Uses place() to draw edge-to-edge, ignoring page margins.
    The banner is offset by negative margins to reach the page edges.
    """
    bg, fg = CATEGORY_COLORS.get(category, CATEGORY_COLORS["normal"])

    # Full-bleed: we need to break out of the margin.
    # Page margin is 7% = ~0.595in on letter (8.5in).
    # We use a block with negative outset to extend to page edges.
    return f"""
// Group: {title}
#block(
  width: 100% + 2 * 7%,
  inset: (x: 7%, y: 20pt),
  outset: (x: 7%),
  fill: rgb("{bg}"),
  above: 0pt,
  below: 12pt,
)[
  #align(center)[
    #text(size: 20pt, weight: "bold", fill: rgb("{fg}"))[{escape_typst(title)}]
  ]
]
"""


def generate_checklist(checklist: dict, category: str, is_first: bool) -> str:
    """Generate a single checklist with title bar and items."""
    title = checklist["title"]
    items = checklist.get("items", [])

    lines = []

    # Page break hint: if not the first checklist in a group,
    # add a conditional page break (prefer starting on fresh page
    # if less than 40% of the page remains)
    if not is_first:
        # v(1fr, weak: true) won't add space, but pagebreak with
        # weak:true only breaks if near the bottom. We use a
        # block with breakable:false containing a spacer to hint.
        lines.append("""
#block(breakable: false)[
  #v(8pt)
]""")

    # Checklist title bar
    lines.append(f"""
#block(
  width: 100%,
  fill: rgb("{TITLE_BAR_BG}"),
  inset: (x: 8pt, y: 8pt),
  radius: 2pt,
  above: 12pt,
  below: 0pt,
)[
  #align(center)[
    #text(size: 14pt, fill: rgb("{TITLE_BAR_FG}"))[{escape_typst(title)}]
  ]
]
""")

    # Build rows
    row_idx = 0
    for item in items:
        item_type = item.get("type", "ITEM_CHALLENGE_RESPONSE")
        prompt = item.get("prompt", "")
        expectation = item.get("expectation", "")

        if item_type == "ITEM_SPACE":
            lines.append("#v(6pt)")
            continue

        if item_type == "ITEM_TITLE":
            lines.append(f"""#block(
  width: 100%,
  inset: (x: 8pt, y: 5pt),
  fill: rgb("{ROW_ODD}"),
  above: 0pt,
  below: 0pt,
)[
  #text(weight: "bold", size: 10pt)[{escape_typst(prompt)}]
]""")
            row_idx = 0
            continue

        if item_type in ("ITEM_PLAINTEXT", "ITEM_NOTE"):
            lines.append(f"""#block(
  width: 100%,
  inset: (x: 20pt, y: 4pt),
  fill: rgb("{NOTE_BG}"),
  above: 0pt,
  below: 0pt,
)[
  #text(size: 9pt)[{escape_typst(prompt)}]
]""")
            continue

        if item_type == "ITEM_CHALLENGE_RESPONSE":
            bg_color = ROW_EVEN if row_idx % 2 == 0 else ROW_ODD
            row_idx += 1

            if expectation:
                lines.append(f"""#block(
  width: 100%,
  fill: rgb("{bg_color}"),
  inset: (x: 8pt, y: 5pt),
  above: 0pt,
  below: 0pt,
)[
  #grid(
    columns: ({PROMPT_WIDTH}, 1fr, {EXPECT_WIDTH}),
    column-gutter: 0pt,
    [#text(size: 10pt)[{escape_typst(prompt)}]],
    [#align(left)[#box(width: 100%, repeat[.#h(2.5pt)])]],
    [#text(size: 10pt)[{escape_typst(expectation)}]],
  )
]""")
            else:
                lines.append(f"""#block(
  width: 100%,
  fill: rgb("{bg_color}"),
  inset: (x: 8pt, y: 5pt),
  above: 0pt,
  below: 0pt,
)[
  #text(size: 10pt)[{escape_typst(prompt)}]
]""")

    return "\n".join(lines)


def generate_typst(data: dict) -> str:
    """Generate the complete Typst document."""
    metadata = data.get("metadata", {})
    groups = data.get("groups", [])

    parts = []

    # Document setup
    parts.append("""#set document(
  title: "N720AK Checklists",
  author: "N720AK",
)

#set page(
  paper: "us-letter",
  margin: 7%,
  footer: context {
    let current = counter(page).get().first()
    let total = counter(page).final().first()
    align(center)[
      #text(size: 8pt, fill: rgb("666666"))[Page #current of #total]
    ]
  },
)

#set text(font: ("Roboto", "Helvetica", "Arial"), size: 10pt)
#set par(leading: 0.5em)
""")

    # Cover page
    parts.append(generate_cover_page(metadata))

    for group in groups:
        title = group.get("title", "")
        category = group.get("category", "normal")
        checklists = group.get("checklists", [])

        # Group header banner
        parts.append(generate_group_header(title, category))

        # Each checklist in the group
        for i, checklist in enumerate(checklists):
            parts.append(generate_checklist(checklist, category, is_first=(i == 0)))

        # Page break after each group
        parts.append("\n#pagebreak()\n")

    return "\n".join(parts)


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 json_to_checklist_pdf.py <checklist.json>")
        sys.exit(1)

    input_file = sys.argv[1]
    with open(input_file) as f:
        data = json.load(f)

    typst_content = generate_typst(data)

    os.makedirs("output", exist_ok=True)
    output_file = "output/checklists.typ"
    with open(output_file, "w") as f:
        f.write(typst_content)

    print(f"Generated {output_file}")
    print(f"Compile with: typst compile {output_file} output/checklists.pdf")


if __name__ == "__main__":
    main()
