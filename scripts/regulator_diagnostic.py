#!/usr/bin/env python3
"""Fuel pressure regulator diagnostic — analyze injector differential pressure.

Reads a Dynon SkyView or Garmin GDU 460 CSV flight log and produces:
  1. Console summary of regulator health metrics
  2. 4-panel diagnostic plot (PNG)
  3. Optional altitude correction analysis

Usage:
  # Dynon SkyView log
  uv run --with numpy --with matplotlib python3 regulator_diagnostic.py /path/to/dynon_log.csv

  # Garmin GDU 460 log
  uv run --with numpy --with matplotlib python3 regulator_diagnostic.py /path/to/garmin_log.csv --format garmin

  # With altitude correction (for gauge sensors without baro compensation)
  uv run --with numpy --with matplotlib python3 regulator_diagnostic.py /path/to/log.csv --alt-correct

  # Scan for optimal altitude correction fraction
  uv run --with numpy --with matplotlib python3 regulator_diagnostic.py /path/to/log.csv --alt-scan

  # Compare two flights
  uv run --with numpy --with matplotlib python3 regulator_diagnostic.py flight1.csv flight2.csv

See maintenance/fuel-system/README.md for theory and interpretation.
"""

import csv
import sys
import argparse
import numpy as np
from pathlib import Path


# ---------------------------------------------------------------------------
# Standard atmosphere
# ---------------------------------------------------------------------------

def atm_psi(alt_ft):
    """Standard atmosphere pressure in PSI from pressure altitude in feet."""
    return 14.696 * (1 - 6.8756e-6 * np.asarray(alt_ft, dtype=float)) ** 5.2559


# ---------------------------------------------------------------------------
# Data loaders
# ---------------------------------------------------------------------------

def load_dynon(filepath):
    """Load a Dynon SkyView USER_LOG_DATA CSV.

    Returns dict with arrays: time_min, map_inhg, fuel_psi, fuel_flow, alt_ft
    """
    with open(filepath) as f:
        reader = csv.reader(f)
        header = next(reader)

        # Build column index from header names
        idx = {}
        for i, name in enumerate(header):
            n = name.strip()
            if n == "Session Time":
                idx["time"] = i
            elif n == "Manifold Pressure (inHg)":
                idx["map"] = i
            elif n == "Fuel Pressure (PSI)":
                idx["fpres"] = i
            elif n == "Total Fuel Flow (gal/hr)":
                idx["fflow"] = i
            elif n == "Pressure Altitude (ft)":
                idx["alt"] = i

        if "map" not in idx or "fpres" not in idx:
            # Fall back to known column positions
            idx.setdefault("time", 0)
            idx.setdefault("map", 60)
            idx.setdefault("fpres", 64)
            idx.setdefault("fflow", 63)
            idx.setdefault("alt", 19)

        times, maps, fps, ffs, alts = [], [], [], [], []
        for row in reader:
            try:
                t = float(row[idx["time"]].strip())
                m = row[idx["map"]].strip()
                fp = row[idx["fpres"]].strip()
                ff = row[idx["fflow"]].strip() if "fflow" in idx else ""
                alt = row[idx["alt"]].strip() if "alt" in idx else ""
                if not m or not fp:
                    continue
                times.append(t / 60.0)
                maps.append(float(m))
                fps.append(float(fp))
                ffs.append(float(ff) if ff else np.nan)
                alts.append(float(alt) if alt else np.nan)
            except (ValueError, IndexError):
                continue

    return {
        "time_min": np.array(times),
        "map_inhg": np.array(maps),
        "fuel_psi": np.array(fps),
        "fuel_flow": np.array(ffs),
        "alt_ft": np.array(alts),
        "format": "dynon",
    }


def load_garmin(filepath):
    """Load a Garmin GDU 460 CSV log.

    Handles: 3-row header (airframe info, full names, short names),
    duplicate timestamps (averages them), datetime parsing.

    Returns dict with arrays: time_min, map_inhg, fuel_psi, fuel_flow, alt_ft
    """
    from datetime import datetime
    from collections import OrderedDict

    times_raw, fps_raw, maps_raw, alts_raw, ffs_raw = [], [], [], [], []

    with open(filepath) as f:
        reader = csv.reader(f)
        next(reader)  # airframe info
        full_header = next(reader)
        short_header = next(reader)

        col = {}
        for i, name in enumerate(short_header):
            n = name.strip()
            if n == "E1 MAP":
                col["map"] = i
            elif n == "E1 FPres":
                col["fpres"] = i
            elif n == "Lcl Time":
                col["time"] = i
            elif n == "Lcl Date":
                col["date"] = i
            elif n == "AltP":
                col["alt"] = i
            elif n == "AltInd" and "alt" not in col:
                col["alt"] = i
            elif n == "E1 FFlow":
                col["fflow"] = i

        for row in reader:
            try:
                d = row[col["date"]].strip()
                t = row[col["time"]].strip()
                m = row[col["map"]].strip()
                fp = row[col["fpres"]].strip()
                a = row[col["alt"]].strip() if "alt" in col else ""
                ff = row[col["fflow"]].strip() if "fflow" in col else ""
                if not m or not fp or not t or not d:
                    continue
                times_raw.append(datetime.strptime(f"{d} {t}", "%Y-%m-%d %H:%M:%S"))
                maps_raw.append(float(m))
                fps_raw.append(float(fp))
                alts_raw.append(float(a) if a else np.nan)
                ffs_raw.append(float(ff) if ff else np.nan)
            except (ValueError, IndexError):
                continue

    # Average duplicate timestamps
    grouped = OrderedDict()
    for t, fp, mi, a, ff in zip(times_raw, fps_raw, maps_raw, alts_raw, ffs_raw):
        if t not in grouped:
            grouped[t] = ([], [], [], [])
        grouped[t][0].append(fp)
        grouped[t][1].append(mi)
        grouped[t][2].append(a)
        grouped[t][3].append(ff)

    times_dt = list(grouped.keys())
    fps = np.array([np.mean(v[0]) for v in grouped.values()])
    maps = np.array([np.mean(v[1]) for v in grouped.values()])
    alts = np.array([np.nanmean(v[2]) for v in grouped.values()])
    ffs = np.array([np.nanmean(v[3]) for v in grouped.values()])

    t0 = times_dt[0]
    time_min = np.array([(t - t0).total_seconds() / 60.0 for t in times_dt])

    return {
        "time_min": time_min,
        "map_inhg": maps,
        "fuel_psi": fps,
        "fuel_flow": ffs,
        "alt_ft": alts,
        "format": "garmin",
    }


def detect_format(filepath):
    """Auto-detect whether a CSV is Dynon or Garmin format."""
    with open(filepath) as f:
        first_line = f.readline()
        if "airframe_info" in first_line.lower() or "Lcl Date" in f.readline() + f.readline():
            return "garmin"
    # Check for Dynon header
    with open(filepath) as f:
        header = f.readline()
        if "Session Time" in header or "Manifold Pressure" in header:
            return "dynon"
    # Check for Garmin short header names
    with open(filepath) as f:
        for i, line in enumerate(f):
            if i > 3:
                break
            if "E1 MAP" in line or "E1 FPres" in line:
                return "garmin"
    return "dynon"  # default


def load_file(filepath, fmt=None):
    """Load a flight log CSV, auto-detecting format if not specified."""
    if fmt is None:
        fmt = detect_format(filepath)
    if fmt == "garmin":
        return load_garmin(filepath)
    else:
        return load_dynon(filepath)


# ---------------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------------

def analyze(data, label="Flight", alt_correct=False, quiet=False):
    """Run the full regulator diagnostic on a loaded dataset.

    Returns a dict of computed metrics.
    """
    t = data["time_min"]
    maps = data["map_inhg"]
    fps = data["fuel_psi"]
    ffs = data["fuel_flow"]
    alts = data["alt_ft"]

    map_psi = maps * 0.49115
    delta = fps - map_psi

    if alt_correct:
        atm = atm_psi(alts)
        delta = delta + atm

    # Filters
    engine_on = (maps > 15) & (fps > 5) & (t > 5)

    dt = np.diff(t * 60)
    dm = np.diff(maps)
    dmap_dt = np.zeros(len(maps))
    dmap_dt[1:] = dm / np.maximum(dt, 0.5)
    steady = engine_on & (np.abs(dmap_dt) < 0.05)

    results = {
        "label": label,
        "alt_correct": alt_correct,
        "n_total": len(t),
        "n_engine_on": int(np.sum(engine_on)),
        "n_steady": int(np.sum(steady)),
    }

    if np.sum(engine_on) < 10:
        if not quiet:
            print(f"\n=== {label} ===")
            print(f"  Insufficient engine-on data ({np.sum(engine_on)} samples)")
        return results

    results.update({
        "flight_time_range": (float(t[engine_on].min()), float(t[engine_on].max())),
        "alt_range": (float(np.nanmin(alts[engine_on])), float(np.nanmax(alts[engine_on]))),
        "map_range": (float(maps[engine_on].min()), float(maps[engine_on].max())),
        "fp_range": (float(fps[engine_on].min()), float(fps[engine_on].max())),
        "ff_range": (float(np.nanmin(ffs[engine_on])), float(np.nanmax(ffs[engine_on]))),
        "delta_mean": float(np.mean(delta[engine_on])),
        "delta_std": float(np.std(delta[engine_on])),
        "delta_range": (float(delta[engine_on].min()), float(delta[engine_on].max())),
    })

    # Startup fuel pressure
    startup = (fps > 30) & (t < 15)
    if np.sum(startup) > 0:
        results["startup_fp"] = float(np.mean(fps[startup]))

    if np.sum(steady) > 10:
        c_map = np.polyfit(maps[steady], delta[steady], 1)
        resid = delta[steady] - np.polyval(c_map, maps[steady])

        ff_valid = steady & ~np.isnan(ffs) & (ffs > 1)
        ff_slope = np.nan
        if np.sum(ff_valid) > 10:
            c_ff = np.polyfit(ffs[ff_valid], delta[ff_valid], 1)
            ff_slope = float(c_ff[0])

        results.update({
            "map_slope": float(c_map[0]),
            "map_intercept": float(c_map[1]),
            "ff_slope": ff_slope,
            "residual_std": float(np.std(resid)),
        })

        # Bin analysis
        bins = {}
        for lo, hi in [(15, 19), (19, 22), (22, 26)]:
            mask = steady & (maps >= lo) & (maps < hi)
            if np.sum(mask) > 5:
                bins[f"{lo}-{hi}"] = {
                    "n": int(np.sum(mask)),
                    "mean": float(np.mean(delta[mask])),
                    "std": float(np.std(delta[mask])),
                }
        results["bins"] = bins

    # Store arrays for plotting
    results["_arrays"] = {
        "time": t, "maps": maps, "fps": fps, "ffs": ffs, "alts": alts,
        "delta": delta, "map_psi": map_psi,
        "engine_on": engine_on, "steady": steady, "dmap_dt": dmap_dt,
    }

    if not quiet:
        print_results(results)

    return results


def print_results(r):
    """Print analysis results to console."""
    print(f"\n{'=' * 60}")
    print(f"{r['label']}")
    if r.get("alt_correct"):
        print(f"  (altitude-corrected)")
    print(f"{'=' * 60}")
    print(f"  Samples: {r['n_total']} total, {r['n_engine_on']} engine-on, {r['n_steady']} steady")

    if "flight_time_range" not in r:
        print("  Insufficient data")
        return

    t0, t1 = r["flight_time_range"]
    print(f"  Flight time: {t0:.0f} – {t1:.0f} min ({t1 - t0:.0f} min duration)")
    print(f"  Altitude: {r['alt_range'][0]:.0f} – {r['alt_range'][1]:.0f} ft")
    print(f"  MAP: {r['map_range'][0]:.1f} – {r['map_range'][1]:.1f} inHg")
    print(f"  Fuel pressure: {r['fp_range'][0]:.1f} – {r['fp_range'][1]:.1f} PSI (gauge)")
    print(f"  Fuel flow: {r['ff_range'][0]:.1f} – {r['ff_range'][1]:.1f} gal/hr")

    if "startup_fp" in r:
        print(f"  Startup fuel pressure: {r['startup_fp']:.1f} PSI")

    print(f"\n  Delta (fuel PSI − MAP PSI):")
    print(f"    Mean:  {r['delta_mean']:.2f} PSI")
    print(f"    σ:     {r['delta_std']:.2f} PSI")
    print(f"    Range: {r['delta_range'][0]:.2f} – {r['delta_range'][1]:.2f} PSI")

    if "map_slope" in r:
        print(f"\n  Steady-state regression:")
        print(f"    MAP slope:      {r['map_slope']:.3f} PSI/inHg  (ideal: 0)")
        print(f"    FF slope:       {r['ff_slope']:.3f} PSI/(gal/hr)  (ideal: 0)")
        print(f"    Residual σ:     {r['residual_std']:.2f} PSI  (ideal: < 0.1)")

    if "bins" in r:
        print(f"\n  By MAP bin (steady-state):")
        for name, b in r["bins"].items():
            print(f"    MAP {name} inHg: n={b['n']}, mean={b['mean']:.2f}, σ={b['std']:.2f}")


def altitude_scan(data, label="Flight"):
    """Scan altitude correction fractions to determine sensor behavior."""
    t = data["time_min"]
    maps = data["map_inhg"]
    fps = data["fuel_psi"]
    alts = data["alt_ft"]

    map_psi = maps * 0.49115
    engine_on = (maps > 15) & (fps > 5) & (t > 5)
    dt = np.diff(t * 60)
    dm = np.diff(maps)
    dmap_dt = np.zeros(len(maps))
    dmap_dt[1:] = dm / np.maximum(dt, 0.5)
    steady = engine_on & (np.abs(dmap_dt) < 0.05) & ~np.isnan(alts)

    atm = atm_psi(alts)

    print(f"\n=== Altitude Correction Scan — {label} ===")
    print(f"{'Fraction':>10s} {'Resid σ':>10s} {'Alt slope':>16s}")

    best_frac = 0
    best_sigma = 999

    for frac in np.arange(0, 1.05, 0.05):
        delta = fps - map_psi + frac * atm
        c = np.polyfit(maps[steady], delta[steady], 1)
        resid = delta[steady] - np.polyval(c, maps[steady])
        sigma = float(np.std(resid))

        alt_c = np.polyfit(alts[steady], resid, 1)

        print(f"{frac:10.2f} {sigma:10.3f} {alt_c[0] * 1000:+12.3f} PSI/kft")

        if sigma < best_sigma:
            best_sigma = sigma
            best_frac = frac

    print(f"\n  Best fraction: {best_frac:.2f}")
    print(f"  1.0 = standard gauge sensor (needs full correction)")
    print(f"  0.0 = sensor already compensated (no correction needed)")
    return best_frac


# ---------------------------------------------------------------------------
# Plotting
# ---------------------------------------------------------------------------

def plot_diagnostic(results, outpath=None):
    """Generate the 4-panel diagnostic plot."""
    import matplotlib.pyplot as plt

    a = results["_arrays"]
    t = a["time"]
    maps = a["maps"]
    delta = a["delta"]
    ffs = a["ffs"]
    alts = a["alts"]
    engine_on = a["engine_on"]
    steady = a["steady"]
    dmap_dt = a["dmap_dt"]
    transient = engine_on & ~steady

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    label = results["label"]
    corr_note = " (altitude-corrected)" if results.get("alt_correct") else ""
    fig.suptitle(f"Regulator Diagnostic — {label}{corr_note}", fontsize=14, fontweight="bold")

    # Panel 1: Delta vs MAP
    ax = axes[0, 0]
    ax.scatter(maps[transient], delta[transient], s=5, alpha=0.15, color="plum",
               label="Transient", zorder=1)
    ax.scatter(maps[steady], delta[steady], s=5, alpha=0.4, color="darkviolet",
               label="Steady", zorder=2)
    if "map_slope" in results:
        c = [results["map_slope"], results["map_intercept"]]
        x = np.linspace(maps[steady].min(), maps[steady].max(), 100)
        ax.plot(x, np.polyval(c, x), color="orange", linewidth=2,
                label=f"Slope: {c[0]:.2f} PSI/inHg", zorder=3)
    ax.set_xlabel("MAP (inHg)")
    ax.set_ylabel("Delta (PSI)")
    ax.set_title("Delta vs MAP")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    # Panel 2: Delta vs Fuel Flow
    ax = axes[0, 1]
    ff_trans = transient & ~np.isnan(ffs) & (ffs > 1)
    ff_steady = steady & ~np.isnan(ffs) & (ffs > 1)
    ax.scatter(ffs[ff_trans], delta[ff_trans], s=5, alpha=0.15, color="lightgreen",
               label="Transient", zorder=1)
    ax.scatter(ffs[ff_steady], delta[ff_steady], s=5, alpha=0.4, color="forestgreen",
               label="Steady", zorder=2)
    if not np.isnan(results.get("ff_slope", np.nan)) and np.sum(ff_steady) > 10:
        c_ff = np.polyfit(ffs[ff_steady], delta[ff_steady], 1)
        x = np.linspace(ffs[ff_steady].min(), ffs[ff_steady].max(), 100)
        ax.plot(x, np.polyval(c_ff, x), color="orange", linewidth=2,
                label=f"Slope: {c_ff[0]:.2f} PSI/(gal/hr)", zorder=3)
    ax.set_xlabel("Fuel Flow (gal/hr)")
    ax.set_ylabel("Delta (PSI)")
    ax.set_title("Delta vs Fuel Flow")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    # Panel 3: Delta vs Time with altitude
    ax = axes[1, 0]
    dmap_abs = np.abs(dmap_dt)
    sc = ax.scatter(t[engine_on], delta[engine_on], c=dmap_abs[engine_on],
                    cmap="RdYlBu_r", s=5, alpha=0.6, vmin=0, vmax=0.3)
    ax.set_xlabel("Session Time (min)")
    ax.set_ylabel("Delta (PSI)")
    ax.set_title("Delta vs Time (colored by |dMAP/dt|)")
    ax.grid(True, alpha=0.3)
    plt.colorbar(sc, ax=ax, label="|dMAP/dt| (inHg/s)")
    ax2 = ax.twinx()
    ax2.plot(t[engine_on], alts[engine_on], '-', color="gray", alpha=0.3, linewidth=0.8)
    ax2.set_ylabel("Altitude (ft)", color="gray", fontsize=8)
    ax2.tick_params(axis='y', labelcolor='gray', labelsize=7)

    # Panel 4: Histogram
    ax = axes[1, 1]
    d_s = delta[steady]
    ax.hist(d_s, bins=50, color="mediumpurple", edgecolor="darkviolet", alpha=0.8)
    m = np.mean(d_s)
    s = np.std(d_s)
    ax.axvline(m, color="orange", linewidth=2, linestyle="--",
               label=f"Mean = {m:.2f} PSI")
    ax.axvline(m - s, color="orange", linewidth=1, linestyle=":")
    ax.axvline(m + s, color="orange", linewidth=1, linestyle=":",
               label=f"σ = {s:.2f} PSI")
    ax.set_xlabel("Delta (PSI)")
    ax.set_ylabel("Count")
    ax.set_title("Delta Histogram (steady-state)")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()

    if outpath is None:
        outpath = Path(args.files[0]).stem + "_regulator_diagnostic.png"
    plt.savefig(outpath, dpi=150, bbox_inches="tight")
    print(f"\nSaved plot to {outpath}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    global args
    parser = argparse.ArgumentParser(
        description="Fuel pressure regulator diagnostic analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("files", nargs="+", help="CSV flight log file(s)")
    parser.add_argument("--format", choices=["dynon", "garmin", "auto"], default="auto",
                        help="Log file format (default: auto-detect)")
    parser.add_argument("--alt-correct", action="store_true",
                        help="Apply altitude correction to delta")
    parser.add_argument("--alt-scan", action="store_true",
                        help="Scan altitude correction fractions")
    parser.add_argument("--plot", action="store_true", default=True,
                        help="Generate diagnostic plot (default: yes)")
    parser.add_argument("--no-plot", action="store_false", dest="plot",
                        help="Skip plot generation")
    parser.add_argument("-o", "--output", help="Output plot filename")

    args = parser.parse_args()

    fmt = None if args.format == "auto" else args.format

    for filepath in args.files:
        p = Path(filepath)
        label = p.stem

        # Shorten common Dynon filenames
        if "N720AK" in label:
            # Extract date if present
            parts = label.split("-")
            if len(parts) >= 3 and parts[0].isdigit():
                date = "-".join(parts[:3])
                label = f"N720AK — {date}"
            else:
                label = f"N720AK — {label}"

        data = load_file(filepath, fmt)
        print(f"Loaded {filepath} ({data['format']} format, {len(data['time_min'])} samples)")

        if args.alt_scan:
            altitude_scan(data, label)

        results = analyze(data, label=label, alt_correct=args.alt_correct)

        if args.plot and "_arrays" in results:
            out = args.output or str(p.with_suffix("").with_name(p.stem + "_regulator_diagnostic.png"))
            plot_diagnostic(results, outpath=out)


if __name__ == "__main__":
    main()
