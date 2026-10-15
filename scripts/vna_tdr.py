#!/usr/bin/env python3
"""
Time-domain reflectometry from a NanoVNA s1p sweep.

Locates impedance discontinuities -- open circuits, shorts, bad connectors --
along a coax run by inverse-transforming an S11 frequency sweep.

Distance resolution is set by sweep BANDWIDTH, not by point count:

    resolution = c * VF / (2 * BW)

which is why this wants a wide sweep.  On RG-400 (VF 0.695):

    --band wide  (1-900 MHz)    ~4.6 in    use this to find a break
    --band com   (100-160 MHz)  ~5.7 ft    useless for locating anything

Capture first, then analyze:

  uv run --with pyserial python3 scripts/vna_capture.py --band wide \\
      --out ~/vna/cable.s1p --note "COM1 coax, panel end, far end open"
  uv run --with numpy python3 scripts/vna_tdr.py ~/vna/cable.s1p

Validate the maths against a synthetic break at a known distance:

  uv run --with numpy python3 scripts/vna_tdr.py --self-test
"""

import argparse
import sys

import numpy as np

C = 299_792_458.0
VF_RG400 = 0.695
M_TO_FT = 3.280839895


def die(msg):
    print(f"\nerror: {msg}", file=sys.stderr)
    sys.exit(1)


def load_s1p(path):
    """Read a Touchstone .s1p in real/imag form; returns (freq_hz, gamma)."""
    f, re, im = [], [], []
    fmt = None
    for line in open(path):
        line = line.strip()
        if not line or line.startswith("!"):
            continue
        if line.startswith("#"):
            parts = line.upper().split()
            fmt = "RI" if "RI" in parts else ("MA" if "MA" in parts else None)
            continue
        p = line.split()
        if len(p) < 3:
            continue
        f.append(float(p[0]))
        re.append(float(p[1]))
        im.append(float(p[2]))
    if not f:
        die(f"no data points in {path}")
    f = np.asarray(f)
    a, b = np.asarray(re), np.asarray(im)
    if fmt == "MA":
        g = a * np.exp(1j * np.deg2rad(b))
    else:
        g = a + 1j * b
    return f, g


def tdr(f, gamma, vf=VF_RG400, pad=16):
    """Bandpass-mode TDR.  Returns (distance_m, magnitude) one-way."""
    if len(f) < 8:
        die("need at least 8 frequency points")
    df = np.diff(f)
    if not np.allclose(df, df[0], rtol=1e-3):
        die("frequency points are not uniformly spaced")
    df = float(df[0])
    n = len(f)

    # Hann window: costs about 2x in resolution, buys ~31 dB sidelobe
    # suppression.  Without it a strong reflection smears across the whole
    # trace and buries anything smaller.
    win = np.hanning(n)
    m = n * pad
    h = np.fft.ifft(gamma * win, m)

    dt = 1.0 / (m * df)
    t = np.arange(m) * dt
    dist = C * vf * t / 2.0          # round trip -> one-way distance
    return dist, np.abs(h)


def find_peaks(dist, mag, max_m, floor_frac=0.05, min_sep_m=0.05):
    """Local maxima above a fraction of the largest, nearest first."""
    keep = dist <= max_m
    d, a = dist[keep], mag[keep]
    if len(a) < 3:
        return []
    thr = a.max() * floor_frac
    idx = [i for i in range(1, len(a) - 1)
           if a[i] > thr and a[i] >= a[i - 1] and a[i] > a[i + 1]]
    out = []
    for i in idx:
        if out and d[i] - out[-1][0] < min_sep_m:
            if a[i] > out[-1][1]:
                out[-1] = (d[i], a[i])
            continue
        out.append((d[i], a[i]))
    return out


def report(path, f, g, vf, max_m):
    dist, mag = tdr(f, g, vf)
    bw = f[-1] - f[0]
    res = C * vf / (2 * bw)
    print(f"\n  {path}")
    print(f"    {f[0]/1e6:.3f}-{f[-1]/1e6:.1f} MHz, {len(f)} points, VF {vf}")
    print(f"    resolution {res:.3f} m ({res*M_TO_FT:.2f} ft), "
          f"window {max_m:.0f} m")

    peaks = find_peaks(dist, mag, max_m)
    if not peaks:
        print("    no reflections found")
        return
    big = max(a for _, a in peaks)
    print(f"\n    {'distance':>12} {'':>10}  relative")
    print(f"    {'(m)':>12} {'(ft)':>10}  magnitude")
    for d, a in peaks[:8]:
        bar = "#" * max(1, int(round(20 * a / big)))
        print(f"    {d:12.2f} {d*M_TO_FT:10.2f}  {a/big:6.3f}  {bar}")


def self_test():
    """Synthesize an open at a known distance and check we recover it."""
    print("self-test: synthetic open circuit on RG-400")
    ok = True
    for truth_m in (2.0, 6.0, 15.0):
        f = np.linspace(1e6, 900e6, 401)
        v = C * VF_RG400
        # Round trip of 2*d: gamma = exp(-j 2pi f (2d/v)), |gamma| = 1.
        g = np.exp(-1j * 2 * np.pi * f * (2 * truth_m / v))
        dist, mag = tdr(f, g)
        got = dist[np.argmax(mag)]
        res = C * VF_RG400 / (2 * (f[-1] - f[0]))
        good = abs(got - truth_m) < res
        ok &= good
        print(f"  truth {truth_m:6.2f} m -> found {got:6.2f} m  "
              f"(err {abs(got-truth_m)*100:5.1f} cm, tol {res*100:.1f} cm)  "
              f"{'PASS' if good else 'FAIL'}")
    print("self-test PASSED" if ok else "self-test FAILED")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(
        description="Locate coax faults from a NanoVNA s1p sweep")
    ap.add_argument("files", nargs="*", help="s1p sweeps to analyze")
    ap.add_argument("--vf", type=float, default=VF_RG400,
                    help=f"velocity factor (default {VF_RG400}, RG-400)")
    ap.add_argument("--max", type=float, default=30.0,
                    help="furthest distance to report, metres (default 30)")
    ap.add_argument("--self-test", action="store_true",
                    help="validate against a synthetic open at known distance")
    args = ap.parse_args()

    if args.self_test:
        return self_test()
    if not args.files:
        die("give one or more .s1p files, or --self-test")

    print("=" * 72)
    print("  NanoVNA time-domain reflectometry")
    print("=" * 72)
    for path in args.files:
        f, g = load_s1p(path)
        report(path, f, g, args.vf, args.max)
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
