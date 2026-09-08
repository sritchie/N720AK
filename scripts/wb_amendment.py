"""N720AK weight-and-balance amendment by computation (no re-weigh).

Recomputes empty weight, moment and CG from the 2025-11-18 weighing plus the
equipment changes listed in CHANGES, prints the result, and optionally writes a
one-page amendment sheet:

    uv run --with reportlab python scripts/wb_amendment.py            # print only
    uv run --with reportlab python scripts/wb_amendment.py --pdf out.pdf

Method: AC 43.13-1B, Chapter 10 (weight and balance revision for equipment
changes). Datum is 99.44 in forward of the wing leading edge (POH Section 7).
"""
import sys, datetime

BASE = {"date": "2025-11-18", "weight": 1643.0, "arm": 106.96, "moment": 175730.0}  # 12 qt oil, no fuel
GROSS = 2700.0
DATUM_TO_LE = 99.44
AMEND_DATE = "2026-09-08"
CHANGES = [  # (description, delta_lb, arm_in_aft_of_datum, note)
    ("Monkworkz MZ-30 generator with regulator and BOSCH relay, installed 2026-03-09",
     +2.600, DATUM_TO_LE - 34.0, "34 in forward of the wing leading edge"),
    ("OnSpeed AOA computer, installed after the weighing",
     +0.375, DATUM_TO_LE - 17.0, "17 in forward of the wing leading edge; 6 oz"),
    ("Borla 203133 fuel pressure regulator replacing the Aeromotive unit, 2026-03-17",
     0.0, DATUM_TO_LE - 34.0, "like-for-like replacement, no net change"),
]

def compute():
    w, m = BASE["weight"], BASE["moment"]
    rows = []
    for desc, dw, arm, note in CHANGES:
        dm = dw * arm; w += dw; m += dm
        rows.append((desc, dw, arm, dm, note))
    return rows, w, m, m / w

def main():
    rows, w, m, cg = compute()
    print(f"Base {BASE['date']}: {BASE['weight']:.1f} lb @ {BASE['arm']:.2f} in, moment {BASE['moment']:,.0f}")
    for desc, dw, arm, dm, note in rows:
        print(f"  {dw:+.3f} lb @ {arm:.2f} in = {dm:+.1f} lb-in  {desc}")
    print(f"Amended {AMEND_DATE}: {w:.1f} lb, moment {m:,.0f} lb-in, CG {cg:.2f} in aft of datum; useful load {GROSS - w:.1f} lb")
    if "--pdf" in sys.argv:
        out = sys.argv[sys.argv.index("--pdf") + 1]
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.lib import colors
        ss = getSampleStyleSheet(); doc = SimpleDocTemplate(out, pagesize=letter, leftMargin=54, rightMargin=54, topMargin=54, bottomMargin=54)
        el = [Paragraph("N720AK — Weight and Balance Amendment", ss["Title"]),
              Paragraph(f"Van's RV-10, S/N 41649, experimental amateur-built. Amendment by computation dated {AMEND_DATE}, "
                        f"revising the empty weight and center of gravity established by the {BASE['date']} weighing for equipment "
                        "installed since. No re-weigh. Method per AC 43.13-1B, Chapter 10. Datum 99.44 in forward of the wing leading edge; "
                        "empty weight includes 12 quarts of oil and no fuel.", ss["BodyText"]), Spacer(1, 10)]
        data = [["Item", "Weight (lb)", "Arm (in)", "Moment (lb-in)"],
                [f"Empty weight as weighed {BASE['date']}", f"{BASE['weight']:.1f}", f"{BASE['arm']:.2f}", f"{BASE['moment']:,.0f}"]]
        for desc, dw, arm, dm, note in rows:
            data.append([Paragraph(f"{desc} — {note}", ss["BodyText"]), f"{dw:+.3f}", f"{arm:.2f}", f"{dm:+.1f}"])
        data.append([Paragraph(f"<b>Amended empty weight, {AMEND_DATE}</b>", ss["BodyText"]), f"<b>{w:.1f}</b>", f"<b>{cg:.2f}</b>", f"<b>{m:,.0f}</b>"])
        data[-1] = [data[-1][0]] + [Paragraph(x, ss["BodyText"]) for x in data[-1][1:]]
        t = Table(data, colWidths=[300, 60, 55, 85])
        t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.5, colors.grey), ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                               ("VALIGN", (0, 0), (-1, -1), "TOP"), ("FONTSIZE", (0, 0), (-1, -1), 9)]))
        el += [t, Spacer(1, 12),
               Paragraph(f"Useful load at the 2,700 lb gross weight: <b>{GROSS - w:.1f} lb</b> (was {GROSS - BASE['weight']:.1f}). "
                         "Allowable CG range 107.84 to 116.24 in aft of datum. This sheet supplements the 2025-11-18 weighing record and "
                         "is carried in the aircraft with it; POH Section 7 is revised to match.", ss["BodyText"]), Spacer(1, 30),
               Paragraph("______________________________________&nbsp;&nbsp;&nbsp;&nbsp;Date: " + AMEND_DATE, ss["BodyText"]),
               Paragraph("Sam Ritchie, Repairman Certificate 5256450 (Experimental Aircraft Builder, N720AK)", ss["BodyText"])]
        doc.build(el); print("wrote", out)

if __name__ == "__main__":
    main()
