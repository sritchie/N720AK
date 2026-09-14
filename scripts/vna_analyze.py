#!/usr/bin/env python3
"""Analyze NanoVNA Touchstone (.s1p) sweeps of the N720AK nav antenna.

Reports SWR, impedance and resonance across the VOR/LOC and glideslope bands,
and overlays multiple sweeps so a change can be seen rather than remembered.

Reference numbers for a STOCK Bob Archer wingtip antenna, from owners who
measured theirs:

    108-118 MHz   SWR < 2:1      Archer's own specification
    328.6-335.4   SWR 4:1 to 6:1 NORMAL. Archer never designed for 330 MHz
                                 and a GTN 650 works through it. Do not
                                 "fix" this unless reception says otherwise.

After the glideslope add-on, owners measured 1.1:1 to 1.5:1 at 333 MHz with
no penalty at 113 MHz.

Usage:
  uv run --with numpy --with matplotlib python3 scripts/vna_analyze.py sweep.s1p
  uv run --with numpy --with matplotlib python3 scripts/vna_analyze.py before.s1p after.s1p
"""

import argparse
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK_2 = "#52514e"
GRID = "#dedbd4"
SERIES = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100",
          "#e87ba4", "#008300", "#4a3aa7", "#e34948"]

BANDS = [("VOR / LOC", 108.0e6, 117.95e6, 2.0),
         ("Glideslope", 328.6e6, 335.4e6, 6.0)]
SPOTS = [108.0e6, 113.0e6, 117.95e6, 328.6e6, 332.0e6, 335.4e6]


def read_s1p(path):
    """Read a 1-port Touchstone file. Returns (freqs_hz, gamma, comments)."""
    path = Path(path).expanduser()
    if not path.exists():
        sys.exit(f"error: {path} not found")

    mult = {"HZ": 1.0, "KHZ": 1e3, "MHZ": 1e6, "GHZ": 1e9}
    unit, fmt, z0 = 1.0, "RI", 50.0
    freqs, gamma, comments = [], [], []

    for raw in path.read_text().splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("!"):
            comments.append(line.lstrip("! ").rstrip())
            continue
        if line.startswith("#"):
            tok = line[1:].upper().split()
            for i, t in enumerate(tok):
                if t in mult:
                    unit = mult[t]
                elif t in ("RI", "MA", "DB"):
                    fmt = t
                elif t == "R" and i + 1 < len(tok):
                    try:
                        z0 = float(tok[i + 1])
                    except ValueError:
                        pass
            continue
        line = line.split("!")[0]
        parts = line.split()
        if len(parts) < 3:
            continue
        try:
            f, a, b = float(parts[0]), float(parts[1]), float(parts[2])
        except ValueError:
            continue
        if fmt == "RI":
            g = complex(a, b)
        elif fmt == "MA":
            g = a * np.exp(1j * np.deg2rad(b))
        else:  # DB
            g = 10 ** (a / 20.0) * np.exp(1j * np.deg2rad(b))
        freqs.append(f * unit)
        gamma.append(g)

    if not freqs:
        sys.exit(f"error: no data points in {path}")
    return np.array(freqs), np.array(gamma), comments, z0


def swr(gamma):
    m = np.clip(np.abs(gamma), 0, 0.999999)
    return (1 + m) / (1 - m)


def impedance(gamma, z0=50.0):
    return z0 * (1 + gamma) / (1 - gamma)


def at(freqs, values, target):
    """Value at the sample nearest a target frequency, or None if out of range."""
    if target < freqs.min() or target > freqs.max():
        return None
    return float(values[int(np.argmin(np.abs(freqs - target)))])


def summarize(name, freqs, gamma, z0):
    s = swr(gamma)
    z = impedance(gamma, z0)
    print(f"\n  {name}")
    print(f"    {freqs.min() / 1e6:.1f}–{freqs.max() / 1e6:.1f} MHz, "
          f"{len(freqs)} points, Z0 {z0:.0f} Ω")

    rows = []
    for label, lo, hi, limit in BANDS:
        m = (freqs >= lo) & (freqs <= hi)
        if m.sum() < 2:
            print(f"    {label}: not covered by this sweep")
            continue
        band_s = s[m]
        band_f = freqs[m]
        res_i = int(np.argmin(band_s))
        mean_s, worst_s = float(np.mean(band_s)), float(np.max(band_s))
        zc = at(freqs, np.abs(z), (lo + hi) / 2)
        if label == "Glideslope":
            # A stock Archer measures 4:1-6:1 here and a GTN 650 works through
            # it. Only call it a fault well outside that range.
            if mean_s <= 2.0:
                verdict = "excellent — looks modified for glideslope"
            elif mean_s <= 7.0:
                verdict = "normal for a stock Archer"
            else:
                verdict = "HIGH even for a stock Archer"
        else:
            verdict = "ok" if mean_s <= limit else "HIGH"
        print(f"    {label:<11} mean SWR {mean_s:4.1f}  worst {worst_s:4.1f}  "
              f"min {band_s[res_i]:4.1f} at {band_f[res_i] / 1e6:7.2f} MHz  "
              f"|Z| {zc:5.0f} Ω   {verdict}")
        rows.append((label, mean_s, worst_s, band_f[res_i], verdict))

    spot = [(f, at(freqs, s, f)) for f in SPOTS]
    spot = [(f, v) for f, v in spot if v is not None]
    if spot:
        print("    spot SWR: " + "  ".join(
            f"{f / 1e6:.6g}={v:.1f}" for f, v in spot))
    return rows


def plot(sweeps, outpath):
    fig, axes = plt.subplots(1, len(BANDS), figsize=(11, 4.2),
                             facecolor=SURFACE)
    if len(BANDS) == 1:
        axes = [axes]

    for ax, (label, lo, hi, limit) in zip(axes, BANDS):
        ax.set_facecolor(SURFACE)
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
        for side in ("left", "bottom"):
            ax.spines[side].set_color(GRID)
        ax.tick_params(colors=INK_2, labelsize=8, length=3)
        ax.grid(True, color=GRID, linewidth=0.6, alpha=0.8)
        ax.set_axisbelow(True)

        pad = (hi - lo) * 0.8
        span = (lo - pad, hi + pad)
        ax.axvspan(lo / 1e6, hi / 1e6, color=GRID, alpha=0.5, zorder=0)
        ax.axhline(limit, color="#e34948", linewidth=1, linestyle="--", zorder=2)
        ax.annotate(f"{limit:.0f}:1", (span[0] / 1e6, limit),
                    textcoords="offset points", xytext=(2, 3),
                    fontsize=8, color="#e34948")

        any_data = False
        for i, (name, f, g, _) in enumerate(sweeps):
            m = (f >= span[0]) & (f <= span[1])
            if m.sum() < 2:
                continue
            any_data = True
            ax.plot(f[m] / 1e6, np.clip(swr(g)[m], 1, 10),
                    color=SERIES[i % len(SERIES)], linewidth=1.6,
                    label=name, zorder=3)

        ax.set_xlim(span[0] / 1e6, span[1] / 1e6)
        ax.set_ylim(1, 10)
        ax.set_xlabel("MHz", fontsize=9, color=INK_2)
        ax.set_title(label, fontsize=10, color=INK, loc="left", pad=8)
        if not any_data:
            ax.annotate("not covered by these sweeps", (0.5, 0.5),
                        xycoords="axes fraction", ha="center",
                        fontsize=9, color=INK_2)
    axes[0].set_ylabel("SWR", fontsize=9, color=INK_2)

    if len(sweeps) > 1:
        handles, labels = axes[0].get_legend_handles_labels()
        if handles:
            leg = fig.legend(handles, labels, frameon=False, fontsize=8,
                             ncol=min(len(labels), 4), loc="lower center",
                             bbox_to_anchor=(0.5, -0.02))
            for t in leg.get_texts():
                t.set_color(INK_2)
        fig.tight_layout(rect=(0, 0.07, 1, 1))
    else:
        fig.tight_layout()
    fig.savefig(outpath, dpi=150, facecolor=SURFACE)
    plt.close(fig)


def main():
    ap = argparse.ArgumentParser(description="Analyze NanoVNA .s1p sweeps")
    ap.add_argument("files", nargs="+", help="Touchstone .s1p files")
    ap.add_argument("--out", default=None, help="output PNG path")
    args = ap.parse_args()

    sweeps = []
    print("=" * 72)
    print("  NanoVNA sweep analysis — N720AK nav antenna")
    print("=" * 72)
    for path in args.files:
        f, g, comments, z0 = read_s1p(path)
        name = Path(path).stem
        note = next((c for c in comments if c.startswith("note:")), None)
        summarize(name + (f"  [{note[5:].strip()}]" if note else ""), f, g, z0)
        sweeps.append((name, f, g, z0))

    out = Path(args.out).expanduser() if args.out else \
        Path(args.files[0]).expanduser().with_suffix(".png")
    plot(sweeps, out)
    print(f"\n  Figure: {out}\n")


if __name__ == "__main__":
    main()
