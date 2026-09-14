#!/usr/bin/env python3
"""Capture a sweep from a NanoVNA over USB serial and save it as Touchstone.

The NanoVNA exposes a text console on its USB CDC serial port. This drives that
console directly, so a sweep lands in a .s1p file that can be read, plotted and
compared instead of photographed off the screen.

Calibrate on the instrument itself BEFORE capturing (see the plan). This tool
reads whatever the active calibration produces; it does not calibrate for you.

Usage:
  # find the NanoVNA's serial port
  uv run --with pyserial python3 scripts/vna_capture.py --list

  # sweep the nav band and save Touchstone
  uv run --with pyserial python3 scripts/vna_capture.py \
      --start 100e6 --stop 350e6 --points 401 \
      --out ~/vna/2026-09-14-antenna-at-radio.s1p \
      --note "wingtip on, measured at the GTN end of the coax"

  # band presets
  uv run --with pyserial python3 scripts/vna_capture.py --band nav --out nav.s1p
  uv run --with pyserial python3 scripts/vna_capture.py --band both --out full.s1p

Analysis: scripts/vna_analyze.py.  Workflow: plans/vor-antenna-diagnostic.md
"""

import argparse
import glob
import sys
import time
from datetime import datetime
from pathlib import Path

PROMPT = b"ch> "

BANDS = {
    "nav":  (100e6, 130e6),     # VOR/LOC with shoulders
    "gs":   (300e6, 360e6),     # glideslope with shoulders
    "both": (100e6, 350e6),     # one sweep covering everything
    "wide": (1e6, 900e6),       # survey sweep
}


def die(msg):
    print(f"\nerror: {msg}", file=sys.stderr)
    sys.exit(1)


def candidate_ports():
    """Serial ports a NanoVNA is likely to appear on."""
    pats = ["/dev/cu.usbmodem*", "/dev/tty.usbmodem*",
            "/dev/cu.usbserial*", "/dev/ttyACM*", "/dev/ttyUSB*"]
    out = []
    for p in pats:
        out += sorted(glob.glob(p))
    return out


# ---------------------------------------------------------------------------
# Console response parsing.  Pure functions so they can be tested without
# hardware attached.
# ---------------------------------------------------------------------------

def strip_echo(text, command):
    """Drop the echoed command and the trailing prompt from a response."""
    lines = [l.strip() for l in text.replace("\r", "\n").split("\n")]
    lines = [l for l in lines if l and l != "ch>" and l != command.strip()]
    return lines


def parse_frequencies(text):
    """`frequencies` returns one integer Hz per line."""
    out = []
    for line in strip_echo(text, "frequencies"):
        try:
            out.append(float(line.split()[0]))
        except (ValueError, IndexError):
            continue
    return out


def parse_data(text, command="data 0"):
    """`data 0` returns 'real imag' pairs, one complex sample per line."""
    out = []
    for line in strip_echo(text, command):
        parts = line.split()
        if len(parts) < 2:
            continue
        try:
            out.append((float(parts[0]), float(parts[1])))
        except ValueError:
            continue
    return out


def write_touchstone(path, freqs, s11, note="", meta=None):
    """Write a 1-port Touchstone file in real/imaginary form."""
    path = Path(path).expanduser()
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        f"! NanoVNA capture — N720AK nav antenna",
        f"! captured {datetime.now().isoformat(timespec='seconds')}",
    ]
    if note:
        lines.append(f"! note: {note}")
    for k, v in (meta or {}).items():
        lines.append(f"! {k}: {v}")
    lines.append("# Hz S RI R 50")
    for f, (re, im) in zip(freqs, s11):
        lines.append(f"{f:.0f} {re:.9f} {im:.9f}")
    path.write_text("\n".join(lines) + "\n")
    return path


# ---------------------------------------------------------------------------
# Instrument I/O
# ---------------------------------------------------------------------------

class NanoVNA:
    def __init__(self, port, timeout=12):
        try:
            import serial
        except ImportError:
            die("pyserial not installed. Run with: uv run --with pyserial ...")
        self.ser = serial.Serial(port, 115200, timeout=timeout)
        time.sleep(0.25)
        self.ser.reset_input_buffer()

    def cmd(self, command, settle=0.0):
        """Send a command and read until the console prompt returns."""
        self.ser.reset_input_buffer()
        self.ser.write((command + "\r").encode())
        self.ser.flush()
        if settle:
            time.sleep(settle)
        buf = b""
        deadline = time.time() + self.ser.timeout
        while time.time() < deadline:
            chunk = self.ser.read(4096)
            if chunk:
                buf += chunk
                if buf.rstrip().endswith(b"ch>") or buf.endswith(PROMPT):
                    break
            elif buf:
                break
        return buf.decode(errors="replace")

    def close(self):
        try:
            self.ser.close()
        except Exception:
            pass


def main():
    ap = argparse.ArgumentParser(
        description="Capture a NanoVNA sweep to a Touchstone .s1p file")
    ap.add_argument("--list", action="store_true",
                    help="list candidate serial ports and exit")
    ap.add_argument("--port", help="serial port (default: autodetect)")
    ap.add_argument("--band", choices=sorted(BANDS),
                    help="frequency preset instead of --start/--stop")
    ap.add_argument("--start", type=float, help="sweep start in Hz")
    ap.add_argument("--stop", type=float, help="sweep stop in Hz")
    ap.add_argument("--points", type=int, default=401, help="sweep points")
    ap.add_argument("--out", help="output .s1p path")
    ap.add_argument("--note", default="", help="note recorded in the file header")
    ap.add_argument("--settle", type=float, default=2.0,
                    help="seconds to let the sweep complete (default 2)")
    args = ap.parse_args()

    ports = candidate_ports()
    if args.list:
        if not ports:
            print("No candidate serial ports found.")
            print("Plug the NanoVNA in, power it on, and check the USB cable —")
            print("charge-only cables are the usual culprit; it must carry data.")
        else:
            print("Candidate ports (the NanoVNA is usually a usbmodem device):")
            for p in ports:
                print(f"  {p}")
        return

    if not args.out:
        die("--out is required")
    if args.band:
        start, stop = BANDS[args.band]
    elif args.start and args.stop:
        start, stop = args.start, args.stop
    else:
        die("give --band, or both --start and --stop")

    port = args.port
    if not port:
        modem = [p for p in ports if "usbmodem" in p]
        if not modem:
            die("no usbmodem port found. Run --list, then pass --port explicitly.")
        port = modem[0]
        print(f"using {port}")

    vna = NanoVNA(port)
    try:
        vna.cmd("pause")
        vna.cmd(f"sweep {start:.0f} {stop:.0f} {args.points}")
        time.sleep(args.settle)
        vna.cmd("resume")
        time.sleep(args.settle)
        vna.cmd("pause")

        freq_txt = vna.cmd("frequencies")
        data_txt = vna.cmd("data 0")
        vna.cmd("resume")
    finally:
        vna.close()

    freqs = parse_frequencies(freq_txt)
    s11 = parse_data(data_txt, "data 0")

    if not freqs or not s11:
        die("no data returned. Is the NanoVNA on its main screen and not in a "
            "menu? Try --port explicitly and re-run.")
    if len(freqs) != len(s11):
        n = min(len(freqs), len(s11))
        print(f"warning: {len(freqs)} frequencies vs {len(s11)} samples — "
              f"truncating to {n}")
        freqs, s11 = freqs[:n], s11[:n]

    path = write_touchstone(args.out, freqs, s11, args.note,
                            {"points": len(freqs),
                             "start_hz": f"{freqs[0]:.0f}",
                             "stop_hz": f"{freqs[-1]:.0f}"})
    print(f"wrote {path}  ({len(freqs)} points, "
          f"{freqs[0] / 1e6:.1f}–{freqs[-1] / 1e6:.1f} MHz)")
    print(f"\nAnalyze with:\n  uv run --with numpy --with matplotlib python3 "
          f"scripts/vna_analyze.py {path}")


if __name__ == "__main__":
    main()
