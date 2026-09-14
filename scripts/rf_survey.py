#!/usr/bin/env python3
"""RF noise survey capture driver for the N720AK nav antenna (RTL-SDR).

Drives `rtl_power` through a fixed, repeatable protocol so that noise-floor
measurements taken under different aircraft lighting configurations can be
compared to each other. The whole point is the DIFFERENCE between runs, so
every knob that affects the measurement (gain, bin width, integration,
duration, antenna attachment point) is locked and recorded alongside the data.

Analysis lives in scripts/rf_analyze.py. Workflow: plans/vor-antenna-diagnostic.md

SAFETY — read before connecting anything:
  * NEVER key a COM radio while the SDR is attached to any aircraft antenna.
    A few watts into an RTL-SDR front end destroys it instantly.
  * Keep the bias tee OFF. The Nooelec v5 defaults off; do not enable it.
  * Disconnect the nav coax from the GTN 650 before attaching it to the SDR.

Usage:
  # 0. Confirm the dongle is alive and list valid gain values
  uv run python3 scripts/rf_survey.py --check

  # 1. Full guided light-configuration protocol on the aircraft nav coax
  uv run python3 scripts/rf_survey.py --protocol --point coax \
      --outdir ~/rf-survey/2026-09-14-coax

  # 2. Same protocol with the SDR on its own antenna beside the wingtip
  uv run python3 scripts/rf_survey.py --protocol --point near \
      --outdir ~/rf-survey/2026-09-14-wingtip

  # 3. One-off capture of a single configuration
  uv run python3 scripts/rf_survey.py --config nav --band nav --outdir ~/rf-survey/spot

  # 4. Carrier-to-noise on a specific station (narrow window around the carrier)
  uv run python3 scripts/rf_survey.py --protocol --carrier 113.8 \
      --outdir ~/rf-survey/2026-09-14-rlg
"""

import argparse
import json
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Band presets.  (start_hz, stop_hz, bin_hz)
# ---------------------------------------------------------------------------
# "nav" deliberately starts at 105 MHz so the top of the FM broadcast band is
# visible.  Strong local FM is the classic way an RTL-SDR's front end gets
# overloaded, and it shows up as a raised floor across the whole VOR band.  If
# the analysis flags FM pressure, drop --gain and re-run.

BANDS = {
    "nav":  (105e6, 120e6, 10e3),   # VOR/LOC 108.00-117.95 plus shoulders
    "gs":   (325e6, 340e6, 10e3),   # glideslope 328.6-335.4 plus shoulders
    "com":  (118e6, 137e6, 10e3),   # COM band, for comparison
    "wide": (100e6, 350e6, 100e3),  # broadband comb hunt, coarse
}

PROTECTED = {
    "nav":  (108.0e6, 117.95e6),
    "gs":   (328.6e6, 335.4e6),
    "com":  (118.0e6, 136.975e6),
    "wide": (108.0e6, 335.4e6),
}

# ---------------------------------------------------------------------------
# The light-configuration protocol.
# ---------------------------------------------------------------------------
# Order matters: baseline first, then one switch added at a time so a jump can
# be attributed to a single system, then a repeat baseline at the end.  The
# repeat baseline is not optional -- it is the only evidence that ambient
# conditions held still for the duration of the survey.

SEQUENCES = {
    # Engine OFF. Lighting only -- the first suspect, and the cheapest to test.
    "lights": [
        ("off1",    "ALL LIGHTS OFF.  Master ON, avionics ON, GTN powered."),
        ("nav",     "NAV / position lights ON.  Everything else still off."),
        ("strobe",  "NAV + STROBE ON."),
        ("wigwag",  "NAV + STROBE + WIG-WAG ON."),
        ("landing", "LANDING lights ON steady.  Nav, strobe, wig-wag OFF."),
        ("all",     "EVERYTHING ON — nav, strobe, wig-wag, landing, taxi."),
        ("off2",    "ALL LIGHTS OFF again.  Drift check — do not skip."),
    ],
    # Engine OFF. Everything else electrical that runs without the engine.
    # The EFII fuel pumps and pitot heat are the big switching loads here.
    "systems": [
        ("off1",     "Master ON, avionics ON.  Lights off, pumps off, "
                     "pitot heat off.  Baseline."),
        ("pump1",    "Fuel PUMP 1 running.  Listen for the whir."),
        ("pump2",    "Fuel PUMP 2 running (PMP 2).  Pump 1 off."),
        ("pitot",    "PITOT HEAT ON.  Pumps off.  (Watch the probe — "
                     "do not leave it on long on the ground.)"),
        ("avionics", "Dynon, GTN, transponder and ADS-B all powered and "
                     "transmitting normally.  Pitot heat off."),
        ("servos",   "Run PITCH and ROLL TRIM continuously, back and forth, "
                     "for the whole capture."),
        ("off2",     "Back to baseline — everything off again.  Drift check."),
    ],
    # ENGINE RUNNING at a fixed RPM.  The only way to test ignition, the
    # alternator and the MZ-30, because none of them do anything with the
    # engine stopped.  Read the Phase 1C safety notes before running this.
    "engine": [
        ("idle1",    "Engine at 1200 RPM.  IGN 1 and IGN 2 both ON.  All "
                     "lights OFF.  Baseline — let RPM and CHT settle first."),
        ("ign1only", "IGN 2 OFF.  Running on IGN 1 alone."),
        ("ign2only", "IGN 1 OFF, IGN 2 back ON.  Running on IGN 2 alone."),
        ("altoff",   "Both IGN ON.  ALT FLD OFF — the MZ-30 picks up the bus."),
        ("mzoff",    "ALT FLD back ON.  MZ-30 enable switch OFF."),
        ("englights","Everything restored, then ALL LIGHTS ON."),
        ("idle2",    "Lights off, same RPM as idle1.  Drift check."),
    ],
}

PROTOCOL = SEQUENCES["lights"]


def die(msg):
    print(f"\nerror: {msg}", file=sys.stderr)
    sys.exit(1)


def check_device():
    """Verify rtl_power exists and a dongle responds; print valid gains."""
    for tool in ("rtl_power", "rtl_test"):
        if not shutil.which(tool):
            die(f"{tool} not found. Install with: brew install librtlsdr")

    print("Probing dongle with rtl_test ...\n")
    try:
        proc = subprocess.run(["rtl_test", "-t"], capture_output=True,
                              text=True, timeout=25)
    except subprocess.TimeoutExpired:
        die("rtl_test hung. Unplug the dongle, replug, and retry.")

    out = (proc.stdout or "") + (proc.stderr or "")
    print(out.strip())

    if "No supported devices found" in out:
        die("No RTL-SDR found. Check the USB connection.")
    if "usb_claim_interface error" in out:
        die("Device busy — another SDR program holds it. Quit it and retry.")

    print("\nDongle looks alive. Pick a --gain from the supported list above "
          "(40.2 is a reasonable default; drop it if FM overload is flagged).")


def band_for(args):
    """Resolve the requested band to (name, lo, hi, step, protected_range)."""
    if args.carrier:
        f = float(args.carrier) * 1e6
        # +/-100 kHz window at 500 Hz bins: carrier peak plus local floor.
        return ("carrier", f - 100e3, f + 100e3, 500.0, (f - 2e3, f + 2e3))
    name = args.band
    lo, hi, step = BANDS[name]
    return (name, lo, hi, step, PROTECTED[name])


def run_capture(cfg, band, outdir, args):
    """Run one rtl_power capture. Returns the path written."""
    name, lo, hi, step, protected = band
    stamp = datetime.now().strftime("%Y%m%dT%H%M%S")
    stem = f"{stamp}_{cfg}_{name}"
    csv_path = outdir / f"{stem}.csv"

    cmd = [
        "rtl_power",
        "-f", f"{lo:.0f}:{hi:.0f}:{step:.0f}",
        "-i", str(args.integration),
        "-e", str(args.duration),
        "-g", str(args.gain),
        "-p", str(args.ppm),
        "-d", str(args.device),
        str(csv_path),
    ]

    print(f"  capturing {name} band, {args.duration}s ... ", end="", flush=True)
    t0 = time.time()
    proc = subprocess.run(cmd, capture_output=True, text=True)
    elapsed = time.time() - t0

    if proc.returncode != 0 or not csv_path.exists():
        print("FAILED")
        die(f"rtl_power failed:\n{proc.stderr.strip()}")

    nrows = sum(1 for _ in csv_path.open())
    print(f"done ({elapsed:.0f}s, {nrows} rows)")

    meta = {
        "config": cfg,
        "band": name,
        "start_hz": lo,
        "stop_hz": hi,
        "bin_hz": step,
        "protected_hz": list(protected),
        "gain_db": args.gain,
        "ppm": args.ppm,
        "integration_s": args.integration,
        "duration_s": args.duration,
        "attach_point": args.point,
        "station": args.carrier,
        "note": args.note,
        "captured_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "command": " ".join(cmd),
    }
    csv_path.with_suffix(".json").write_text(json.dumps(meta, indent=2))
    return csv_path


def main():
    p = argparse.ArgumentParser(
        description="RTL-SDR noise survey driver for the N720AK nav antenna.",
        formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--check", action="store_true",
                   help="probe the dongle, print supported gains, and exit")
    p.add_argument("--protocol", action="store_true",
                   help="run a full guided configuration sequence")
    p.add_argument("--sequence", default="lights", choices=sorted(SEQUENCES),
                   help="which guided sequence: lights (engine off), systems "
                        "(engine off, pumps/pitot/avionics/servos), or engine "
                        "(ENGINE RUNNING — ignition, alternator, MZ-30)")
    p.add_argument("--config", help="label for a single one-off capture")
    p.add_argument("--band", default="nav", choices=sorted(BANDS),
                   help="band preset (default: nav)")
    p.add_argument("--carrier", metavar="MHZ",
                   help="narrow capture centred on a station, e.g. 113.8")
    p.add_argument("--both-bands", action="store_true",
                   help="capture nav and gs bands at every protocol step")
    p.add_argument("--outdir", default="./rf-survey",
                   help="directory for CSV + JSON output")
    p.add_argument("--point", default="coax", choices=["coax", "near", "ref"],
                   help="where the SDR is attached: aircraft coax, near-field "
                        "probe at the wingtip, or a reference antenna")
    p.add_argument("--gain", type=float, default=32.8,
                   help="FIXED tuner gain in dB (default 32.8, chosen by "
                        "--gain-sweep against Front Range FM). Never use AGC "
                        "— it destroys run-to-run comparability.")
    p.add_argument("--gain-sweep", action="store_true",
                   help="capture the same band at several gains so "
                        "rf_analyze.py --gain-check can pick the best one for "
                        "this location. Do this once per site.")
    p.add_argument("--ppm", type=int, default=0, help="frequency correction ppm")
    p.add_argument("--device", type=int, default=0, help="rtl device index")
    p.add_argument("--integration", type=int, default=3,
                   help="seconds per sweep (default 3)")
    p.add_argument("--duration", type=int, default=45,
                   help="seconds per configuration (default 45)")
    p.add_argument("--note", default="", help="free-text note stored in metadata")
    args = p.parse_args()

    if args.check:
        check_device()
        return

    if not args.protocol and not args.config and not args.gain_sweep:
        die("pick one of --check, --gain-sweep, --protocol, or --config NAME")

    if not shutil.which("rtl_power"):
        die("rtl_power not found. Install with: brew install librtlsdr")

    outdir = Path(args.outdir).expanduser()
    outdir.mkdir(parents=True, exist_ok=True)

    bands = [band_for(args)]
    if args.both_bands and not args.carrier:
        bands = [("nav", *BANDS["nav"], PROTECTED["nav"]),
                 ("gs", *BANDS["gs"], PROTECTED["gs"])]

    print("=" * 72)
    print("  N720AK nav antenna RF survey")
    print("=" * 72)
    print(f"  output      {outdir}")
    print(f"  attach      {args.point}")
    print(f"  gain        {args.gain} dB (fixed)")
    print(f"  sequence    {args.sequence if args.protocol else 'one-off'}")
    print(f"  bands       {', '.join(b[0] for b in bands)}")
    print(f"  per config  {args.duration}s x {len(bands)} band(s)")
    print()
    print("  SAFETY: do NOT key a COM radio while the SDR is on an aircraft")
    print("          antenna. Bias tee must be OFF.")
    if args.protocol and args.sequence == "engine":
        print()
        print("  ENGINE-RUNNING SEQUENCE:")
        print("    * Chocks in, brakes set, prop area clear, fire guard aware.")
        print("    * NEVER switch both IGN 1 and IGN 2 off together.")
        print("    * NEVER pull an essential-bus breaker — those ARE the")
        print("      engine on this airplane (ignition, injection, pumps).")
        print("    * Hold the SAME RPM for every configuration or the runs")
        print("      are not comparable.")
        print("    * Second person on the switches; you watch the engine.")
    print("=" * 72)
    print()

    if args.gain_sweep:
        gains = [40.2, 36.4, 32.8, 28.0, 25.4, 19.7]
        print(f"Gain sweep: {len(gains)} captures, antenna must not move.\n")
        for g in gains:
            args.gain = g
            for band in bands:
                run_capture(f"g{g}", band, outdir, args)
        print("=" * 72)
        print("Pick the gain with:")
        print(f"  uv run --with numpy --with matplotlib python3 "
              f"scripts/rf_analyze.py --gain-check {outdir}")
        print("=" * 72)
        return

    if not args.protocol:
        run_all = [(args.config, f"one-off capture: {args.config}")]
    else:
        run_all = SEQUENCES[args.sequence]
        mins = len(run_all) * len(bands) * args.duration / 60
        print(f"{len(run_all)} configurations, roughly {mins:.0f} minutes of "
              f"capture plus your switch time.\n")

    for cfg, instruction in run_all:
        print("-" * 72)
        print(f"[{cfg}]  {instruction}")
        if args.protocol:
            try:
                input("      Set the switches, then press Enter to capture ")
            except (EOFError, KeyboardInterrupt):
                print("\naborted")
                sys.exit(1)
        for band in bands:
            run_capture(cfg, band, outdir, args)
        print()

    print("=" * 72)
    print("Capture complete. Analyze with:")
    print(f"  uv run --with numpy --with matplotlib python3 "
          f"scripts/rf_analyze.py {outdir}")
    print("=" * 72)


if __name__ == "__main__":
    main()
