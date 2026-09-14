#!/usr/bin/env python3
"""Analyze an RTL-SDR noise survey captured by scripts/rf_survey.py.

Answers one question: does turning on an aircraft system raise the noise floor
in the bands the nav receiver cares about, and by how many dB?

Every dB the noise floor rises is a dB of receiver sensitivity lost, so the
delta column is directly a range penalty. Rough reading of the numbers:

    < 1 dB    measurement noise, ignore
    1-3 dB    real but minor
    3-6 dB    meaningful; a marginal antenna system will show it in flight
    6-10 dB   serious; expect flagged CDI at moderate range
    > 10 dB   severe; treat as the primary fault

Usage:
  uv run --with numpy --with matplotlib python3 scripts/rf_analyze.py ~/rf-survey/2026-09-14-coax

  # compare two attachment points side by side
  uv run --with numpy --with matplotlib python3 scripts/rf_analyze.py DIR1 DIR2

  # override which configuration is the reference
  uv run --with numpy --with matplotlib python3 scripts/rf_analyze.py DIR --baseline off1
"""

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# --- palette (validated: see references/palette.md, all six checks pass) ------
SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK_2 = "#52514e"
GRID = "#dedbd4"
SERIES = ["#2a78d6", "#eb6834"]   # slot 1 blue, slot 2 orange
FLAG = "#e34948"                   # slot 8 red, reserved for the threshold line

BAND_LABEL = {"nav": "VOR / LOC 108-118", "gs": "Glideslope 328.6-335.4",
              "com": "COM 118-137", "wide": "100-350 wide",
              "carrier": "carrier window"}

SEVERITY = [(10.0, "SEVERE"), (6.0, "serious"), (3.0, "meaningful"),
            (1.0, "minor"), (-1e9, "negligible")]


def severity(delta_db):
    for threshold, label in SEVERITY:
        if delta_db >= threshold:
            return label
    return "negligible"


# ---------------------------------------------------------------------------
# Loading
# ---------------------------------------------------------------------------

def _safe_float(tok):
    try:
        v = float(tok)
    except ValueError:
        return np.nan
    return v if np.isfinite(v) else np.nan


def load_rtl_power(path):
    """Parse an rtl_power CSV.

    rtl_power emits one row per frequency chunk per sweep:
        date, time, Hz_low, Hz_high, Hz_step, n_samples, bin0, bin1, ...
    A wide range is split across several chunks, and the whole set repeats once
    per sweep. Group by chunk so that chunks with unequal sweep counts still
    aggregate cleanly, then stitch the chunks together in frequency order.

    Returns (freqs_hz, median_db, max_db, n_sweeps).
    """
    chunks = defaultdict(list)
    with open(path) as fh:
        for line in fh:
            parts = [p.strip() for p in line.split(",")]
            if len(parts) < 7:
                continue
            try:
                lo, hi, step = float(parts[2]), float(parts[3]), float(parts[4])
            except ValueError:
                continue
            vals = np.array([_safe_float(t) for t in parts[6:] if t != ""])
            if vals.size == 0:
                continue
            chunks[(lo, hi, step)].append(vals)

    if not chunks:
        raise ValueError(f"no usable rows in {path}")

    freqs, med, mx = [], [], []
    sweeps = []
    for (lo, hi, step) in sorted(chunks):
        stack = chunks[(lo, hi, step)]
        width = min(a.size for a in stack)
        arr = np.vstack([a[:width] for a in stack])
        sweeps.append(arr.shape[0])
        centres = lo + step * (np.arange(width) + 0.5)
        with np.errstate(all="ignore"):
            freqs.append(centres)
            med.append(np.nanmedian(arr, axis=0))
            mx.append(np.nanmax(arr, axis=0))

    f = np.concatenate(freqs)
    order = np.argsort(f)
    return (f[order], np.concatenate(med)[order],
            np.concatenate(mx)[order], int(np.min(sweeps)))


def load_run_dir(d):
    """Load every capture in a directory, keyed by (config, band)."""
    d = Path(d).expanduser()
    if not d.is_dir():
        sys.exit(f"error: {d} is not a directory")

    runs = {}
    for csv_path in sorted(d.glob("*.csv")):
        meta_path = csv_path.with_suffix(".json")
        if not meta_path.exists():
            print(f"  skipping {csv_path.name}: no metadata sidecar")
            continue
        meta = json.loads(meta_path.read_text())
        try:
            f, med, mx, n = load_rtl_power(csv_path)
        except ValueError as e:
            print(f"  skipping {csv_path.name}: {e}")
            continue
        runs[(meta["config"], meta["band"])] = {
            "freq": f, "median": med, "max": mx, "sweeps": n,
            "meta": meta, "path": csv_path,
        }
    if not runs:
        sys.exit(f"error: no usable captures found in {d}")
    return runs


# ---------------------------------------------------------------------------
# Metrics
# ---------------------------------------------------------------------------

def band_mask(freq, lo, hi):
    return (freq >= lo) & (freq <= hi)


def fm_pressure(run):
    """dB by which the FM broadcast tail exceeds the mid-VOR band.

    A large number means strong local FM is compressing the tuner's front end
    and lifting the apparent floor across the whole sweep. The fix is less
    gain or an FM band-stop filter, not more antenna work.
    """
    f, med = run["freq"], run["median"]
    fm = band_mask(f, 105e6, 107.9e6)
    nav = band_mask(f, 112e6, 118e6)
    if fm.sum() < 5 or nav.sum() < 5:
        return None
    return float(np.nanmedian(med[fm]) - np.nanmedian(med[nav]))


def compare(base, run, protected):
    """Delta metrics for one configuration against the baseline."""
    f = base["freq"]
    if run["freq"].shape != f.shape or not np.allclose(run["freq"], f):
        run_med = np.interp(f, run["freq"], run["median"])
        run_max = np.interp(f, run["freq"], run["max"])
    else:
        run_med, run_max = run["median"], run["max"]

    m = band_mask(f, *protected)
    d_med = run_med - base["median"]
    d_max = run_max - base["max"]

    # Pulsed emitters (strobes, wig-wag) lift the peak far more than the
    # median. Steady emitters (position lights) lift both together.
    spread_base = base["max"][m] - base["median"][m]
    spread_run = run_max[m] - run_med[m]

    peak_i = int(np.nanargmax(np.where(m, d_med, -np.inf)))
    return {
        "mean_delta": float(np.nanmean(d_med[m])),
        "peak_delta": float(d_med[peak_i]),
        "peak_freq": float(f[peak_i]),
        "max_delta": float(np.nanmean(d_max[m])),
        "pulse_delta": float(np.nanmean(spread_run) - np.nanmean(spread_base)),
        "freq": f, "delta": d_med, "mask": m,
    }


def carrier_metrics(run):
    """Carrier-to-noise for a narrow capture centred on a station."""
    f, med = run["freq"], run["median"]
    peak_i = int(np.nanargmax(med))
    peak_f, peak_db = float(f[peak_i]), float(med[peak_i])
    skirt = np.abs(f - peak_f) > 10e3
    floor = float(np.nanmedian(med[skirt])) if skirt.sum() > 5 else np.nan
    return {"peak_freq": peak_f, "peak_db": peak_db,
            "floor_db": floor, "cn_db": peak_db - floor}


# ---------------------------------------------------------------------------
# Plots
# ---------------------------------------------------------------------------

def style(ax):
    ax.set_facecolor(SURFACE)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(GRID)
    ax.tick_params(colors=INK_2, labelsize=8, length=3)
    ax.grid(True, color=GRID, linewidth=0.6, alpha=0.8)
    ax.set_axisbelow(True)


def plot_summary(results, configs, bands, outpath, title):
    """Grouped bars: mean in-band noise rise per configuration.

    Configurations stay in capture order, not alphabetical, so the bars read
    in the same sequence the switches were thrown.
    """
    n_band = len(bands)
    x = np.arange(len(configs))
    width = 0.72 / n_band

    fig, ax = plt.subplots(figsize=(1.35 * len(configs) + 3.2, 4.4),
                           facecolor=SURFACE)
    style(ax)

    finite = []
    for bi, band in enumerate(bands):
        vals = [results[c].get(band, {}).get("mean_delta", np.nan)
                for c in configs]
        finite += [v for v in vals if np.isfinite(v)]
        pos = x + (bi - (n_band - 1) / 2) * width
        # edgecolor in the surface colour gives the 2px gap between adjacent
        # fills that keeps touching bars readable
        bars = ax.bar(pos, vals, width * 0.92, color=SERIES[bi % len(SERIES)],
                      edgecolor=SURFACE, linewidth=1.5, zorder=3,
                      label=BAND_LABEL.get(band, band))
        for rect, v in zip(bars, vals):
            if not np.isfinite(v):
                continue
            ax.annotate(f"{v:+.1f}", (rect.get_x() + rect.get_width() / 2, v),
                        textcoords="offset points",
                        xytext=(0, 3 if v >= 0 else -11),
                        ha="center", fontsize=8, color=INK)

    hi = max(finite + [3.5]) if finite else 3.5
    lo = min(finite + [0.0]) if finite else 0.0
    ax.set_ylim(lo * 1.25 if lo < 0 else 0, hi * 1.18)

    ax.axhline(0, color=INK_2, linewidth=1, zorder=4)
    ax.axhline(3, color=FLAG, linewidth=1, linestyle="--", zorder=4)
    ax.annotate("3 dB — meaningful", (-0.45, 3), textcoords="offset points",
                xytext=(0, 4), ha="left", fontsize=8, color=FLAG)

    ax.set_xticks(x)
    ax.set_xticklabels(configs, fontsize=9, color=INK)
    ax.set_ylabel("noise floor rise vs lights-off  (dB)",
                  fontsize=9, color=INK_2)
    ax.set_title(title, fontsize=11, color=INK, loc="left", pad=28)
    if n_band > 1:
        leg = ax.legend(frameon=False, fontsize=8, ncol=n_band,
                        loc="lower left", bbox_to_anchor=(0, 1.0),
                        borderaxespad=0)
        for t in leg.get_texts():
            t.set_color(INK_2)

    fig.tight_layout()
    fig.savefig(outpath, dpi=150, facecolor=SURFACE)
    plt.close(fig)


def plot_spectra(results, configs, band, outpath, title):
    """Small multiples: one delta spectrum per configuration.

    All panels share a y-axis. Independent scales would make a 1 dB drift
    look as dramatic as a 10 dB emitter, which is exactly the wrong reading.
    """
    configs = [c for c in configs if band in results.get(c, {})]
    if not configs:
        return False

    fig, axes = plt.subplots(len(configs), 1, sharex=True, sharey=True,
                             figsize=(9, 1.5 * len(configs) + 1.2),
                             facecolor=SURFACE)
    if len(configs) == 1:
        axes = [axes]

    hi = max(np.nanmax(results[c][band]["delta"]) for c in configs)
    lo = min(np.nanmin(results[c][band]["delta"]) for c in configs)
    span = max(hi - lo, 1.0)
    ylim = (min(lo, 0) - 0.05 * span, hi + 0.30 * span)  # headroom for labels

    for ax, cfg in zip(axes, configs):
        r = results[cfg][band]
        f_mhz = r["freq"] / 1e6
        style(ax)
        ax.set_ylim(*ylim)
        blo, bhi = f_mhz[r["mask"]].min(), f_mhz[r["mask"]].max()
        ax.axvspan(blo, bhi, color=GRID, alpha=0.45, zorder=0)
        ax.axhline(0, color=INK_2, linewidth=0.9, zorder=2)
        ax.plot(f_mhz, r["delta"], color=SERIES[0], linewidth=1.0, zorder=3)
        ax.set_ylabel("dB", fontsize=8, color=INK_2)
        ax.annotate(f"{cfg}   mean {r['mean_delta']:+.1f} dB in band",
                    (0.012, 0.93), xycoords="axes fraction",
                    fontsize=9, color=INK, va="top")

    axes[-1].set_xlabel("frequency (MHz)", fontsize=9, color=INK_2)
    axes[0].set_title(title, fontsize=11, color=INK, loc="left", pad=12)
    fig.tight_layout()
    fig.savefig(outpath, dpi=150, facecolor=SURFACE)
    plt.close(fig)
    return True


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------

def analyze_dir(d, baseline_cfg, outdir):
    print(f"\n{'=' * 72}\n  {d}\n{'=' * 72}")
    runs = load_run_dir(d)

    bands = sorted({b for (_, b) in runs})
    configs = []
    for (c, _) in runs:
        if c not in configs:
            configs.append(c)

    if baseline_cfg not in configs:
        fallback = configs[0]
        print(f"  note: no '{baseline_cfg}' capture here — using first "
              f"captured config '{fallback}' as the baseline")
        baseline_cfg = fallback

    any_meta = next(iter(runs.values()))["meta"]
    lines = [f"## Survey: {Path(d).name}", ""]
    lines.append(f"- Attach point: `{any_meta.get('attach_point')}`")
    lines.append(f"- Fixed gain: {any_meta.get('gain_db')} dB")
    lines.append(f"- {any_meta.get('duration_s')}s per configuration, "
                 f"{any_meta.get('integration_s')}s sweeps")
    if any_meta.get("note"):
        lines.append(f"- Note: {any_meta['note']}")
    lines.append("")

    # --- carrier captures are a different measurement ----------------------
    if "carrier" in bands:
        lines += ["### Carrier-to-noise", "",
                  "| Config | Peak (MHz) | C/N (dB) |", "|---|---|---|"]
        print("\n  Carrier-to-noise")
        for cfg in configs:
            run = runs.get((cfg, "carrier"))
            if not run:
                continue
            cm = carrier_metrics(run)
            lines.append(f"| {cfg} | {cm['peak_freq'] / 1e6:.4f} | "
                         f"{cm['cn_db']:.1f} |")
            print(f"    {cfg:<9} peak {cm['peak_freq'] / 1e6:8.4f} MHz   "
                  f"C/N {cm['cn_db']:5.1f} dB")
        lines.append("")
        bands = [b for b in bands if b != "carrier"]

    # --- front-end sanity --------------------------------------------------
    warnings = []
    base_nav = runs.get((baseline_cfg, "nav"))
    if base_nav is not None:
        fm = fm_pressure(base_nav)
        if fm is not None and fm > 20:
            warnings.append(
                f"FM broadcast sits {fm:.0f} dB above the VOR band in the "
                f"baseline. The tuner is probably compressing — re-run with "
                f"`--gain 25` or add an FM band-stop filter before trusting "
                f"absolute floor numbers.")

    # --- drift check -------------------------------------------------------
    results = defaultdict(dict)
    for band in bands:
        base = runs.get((baseline_cfg, band))
        if base is None:
            warnings.append(f"no `{baseline_cfg}` baseline for the {band} "
                            f"band — deltas skipped")
            continue
        protected = tuple(base["meta"]["protected_hz"])
        for cfg in configs:
            if cfg == baseline_cfg:
                continue
            run = runs.get((cfg, band))
            if run is None:
                continue
            results[cfg][band] = compare(base, run, protected)

    drift_cfg = next((c for c in ("off2", "idle2") if c in results), None)
    if drift_cfg:
        for band in bands:
            if band in results[drift_cfg]:
                drift = results[drift_cfg][band]["mean_delta"]
                if abs(drift) > 1.5:
                    warnings.append(
                        f"Baseline drifted {drift:+.1f} dB in the {band} band "
                        f"between the first and last lights-off capture. "
                        f"Conditions changed during the survey; treat deltas "
                        f"smaller than {abs(drift):.0f} dB as unreliable.")

    # --- summary table -----------------------------------------------------
    lines += ["### Noise floor rise vs lights-off", "",
              "| Config | Band | Mean (dB) | Peak (dB) | At (MHz) | "
              "Pulsed (dB) | Verdict |", "|---|---|---|---|---|---|---|"]
    print(f"\n  {'config':<9} {'band':<5} {'mean':>7} {'peak':>7} "
          f"{'at MHz':>9} {'pulsed':>7}  verdict")
    print("  " + "-" * 62)
    for cfg in configs:
        if cfg == baseline_cfg:
            continue
        for band in bands:
            r = results.get(cfg, {}).get(band)
            if not r:
                continue
            verdict = severity(r["mean_delta"])
            if r["pulse_delta"] > 3:
                verdict += ", pulsed"
            lines.append(
                f"| {cfg} | {band} | {r['mean_delta']:+.1f} | "
                f"{r['peak_delta']:+.1f} | {r['peak_freq'] / 1e6:.3f} | "
                f"{r['pulse_delta']:+.1f} | {verdict} |")
            print(f"  {cfg:<9} {band:<5} {r['mean_delta']:+7.1f} "
                  f"{r['peak_delta']:+7.1f} {r['peak_freq'] / 1e6:9.3f} "
                  f"{r['pulse_delta']:+7.1f}  {verdict}")
    lines.append("")

    if warnings:
        lines += ["### Warnings", ""]
        print("\n  Warnings")
        for w in warnings:
            lines.append(f"- {w}")
            print(f"    ! {w}")
        lines.append("")

    # --- plots -------------------------------------------------------------
    outdir = Path(outdir).expanduser()
    outdir.mkdir(parents=True, exist_ok=True)
    tag = Path(d).name
    written = []

    plotted = [c for c in configs if c != baseline_cfg and results.get(c)]
    if plotted and bands:
        p = outdir / f"{tag}-summary.png"
        plot_summary(results, plotted, bands, p,
                     f"Noise floor rise by lighting configuration — {tag}")
        written.append(p)
        for band in bands:
            p = outdir / f"{tag}-{band}-spectra.png"
            if plot_spectra(results, plotted, band, p,
                            f"{BAND_LABEL.get(band, band)} — change vs "
                            f"lights-off, {tag}"):
                written.append(p)

    if written:
        lines += ["### Figures", ""]
        for p in written:
            lines.append(f"- `{p}`")
        lines.append("")
        print("\n  Figures")
        for p in written:
            print(f"    {p}")

    return lines


def gain_check(d):
    """Pick a tuner gain for this location.

    Sweeps the same band at several gains without moving the antenna and asks
    how the measured noise floor tracks the gain change:

      * floor falls MORE than the gain reduction -> the higher gain was
        compressing, usually from strong local FM broadcast
      * floor falls LESS than the gain reduction -> the dongle's own noise is
        taking over and it is going deaf to what we came to measure

    The best gain is the highest one still tracking linearly.
    """
    runs = load_run_dir(d)
    rows = []
    for (cfg, band), r in runs.items():
        g = float(r["meta"].get("gain_db", float("nan")))
        f, med = r["freq"], r["median"]
        fm = band_mask(f, 105e6, 107.9e6)
        nav = band_mask(f, 112e6, 118e6)
        if nav.sum() < 5:
            continue
        rows.append((g, float(np.nanmedian(med[nav])),
                     float(np.nanmedian(med[fm])) if fm.sum() > 5 else np.nan))
    if len(rows) < 2:
        sys.exit("error: need captures at two or more gains in that directory")

    rows.sort(key=lambda r: -r[0])
    g0, f0, _ = rows[0]
    print("\n  Gain check — is the tuner linear at this location?\n")
    print(f"  {'gain':>6} {'floor':>8} {'FM press':>9} {'expect':>8} "
          f"{'actual':>8} {'error':>8}  reading")
    print("  " + "-" * 66)
    best, best_err = None, None
    for g, floor, fm in rows:
        exp, act = g0 - g, f0 - floor
        err = act - exp
        if abs(err) < 1.0:
            reading = "linear"
        elif err > 0:
            reading = "higher gain was compressing"
        else:
            reading = "internal noise dominating"
        fmp = f"{fm - floor:9.1f}" if np.isfinite(fm) else "        -"
        print(f"  {g:6.1f} {floor:8.1f} {fmp} {exp:8.1f} {act:8.1f} "
              f"{err:+8.1f}  {reading}")
        if abs(err) < 1.0 and (best is None or g > best):
            best, best_err = g, err
    print()
    if best is not None:
        print(f"  -> use --gain {best}  (tracks within {best_err:+.1f} dB of "
              f"linear, and it is the highest gain that does)")
    else:
        print("  -> nothing tracked linearly. Try a wider spread of gains, or "
              "an FM band-stop filter if the FM pressure column is large.")
    print()


def main():
    ap = argparse.ArgumentParser(
        description="Analyze RTL-SDR noise surveys from rf_survey.py")
    ap.add_argument("dirs", nargs="+", help="survey directories to analyze")
    ap.add_argument("--baseline", default="off1",
                    help="configuration used as the reference (default off1)")
    ap.add_argument("--gain-check", action="store_true",
                    help="treat the directory as a gain sweep and recommend a "
                         "tuner gain for this location")
    ap.add_argument("--outdir", default=None,
                    help="where to write figures and the report "
                         "(default: alongside the first survey directory)")
    args = ap.parse_args()

    if args.gain_check:
        for d in args.dirs:
            gain_check(d)
        return

    outdir = Path(args.outdir).expanduser() if args.outdir \
        else Path(args.dirs[0]).expanduser() / "analysis"

    report = ["# N720AK nav antenna RF survey", ""]
    for d in args.dirs:
        report += analyze_dir(d, args.baseline, outdir)

    outdir.mkdir(parents=True, exist_ok=True)
    report_path = outdir / "report.md"
    report_path.write_text("\n".join(report))
    print(f"\n  Report written to {report_path}\n")


if __name__ == "__main__":
    main()
