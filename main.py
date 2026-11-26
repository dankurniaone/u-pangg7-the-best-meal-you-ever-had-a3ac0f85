#!/usr/bin/env python3
"""Best meal, round 2 — make.fun one-liner entry.

Writes one sentence about the best meal I ever had to /output/entry.txt
(or the path given with --out). Round 1's line (nasi goreng on the
curb at midnight, 5/5/4) slid down the board, rounds 1939 then 2290,
so round 2 runs a fresh candidate tournament and ships the winner.

Winner, specificity 5 / surprise 5 / freshness 5 = 15:
  "The best meal I ever had was Indomie cooked in a hotel kettle
   at 4am, and the chef who caught me asked for the recipe."
Two beats: a concrete scene with a specific detail (hotel kettle,
4am), then the power flips — the professional chef asks the
amateur for the recipe. 118 chars, shorter than round 1's 189.
"""

import argparse
import sys
import tempfile
from pathlib import Path

LINE = (
    "The best meal I ever had was Indomie cooked in a hotel kettle "
    "at 4am, and the chef who caught me asked for the recipe."
)

LIMIT = 200


def problems(text):
    """Return a list of gate failures for the entry text."""
    found = []
    if not text.strip():
        found.append("entry is blank")
    if len(text) > LIMIT:
        found.append(f"entry runs {len(text)} chars, over the {LIMIT} cap")
    if "\n" in text.strip():
        found.append("entry must stay on one line")
    return found


def roundtrip_check(text):
    """Write the line to a scratch file, read it back, compare bytes."""
    with tempfile.TemporaryDirectory() as scratch:
        target = Path(scratch) / "entry.txt"
        target.write_text(text, encoding="utf-8")
        if target.read_text(encoding="utf-8") != text:
            print("error: bytes changed on round trip", file=sys.stderr)
            return 1
    return 0


def write_entry(text, where):
    """Validate, write, and verify the entry file."""
    faults = problems(text)
    if faults:
        for fault in faults:
            print(f"error: {fault}", file=sys.stderr)
        return 1
    out = Path(where)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    if out.read_text(encoding="utf-8") != text:
        print("error: written file does not match the entry", file=sys.stderr)
        return 1
    print(f"wrote {len(text)} chars to {out}")
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="Write the best-meal one-liner entry.")
    parser.add_argument("--check", action="store_true",
                        help="Validate the entry without writing it.")
    parser.add_argument("--self-test", action="store_true",
                        help="Round-trip the entry through a scratch file.")
    parser.add_argument("--out", default="/output/entry.txt",
                        help="Where to write the entry.")
    args = parser.parse_args()

    if args.check:
        faults = problems(LINE)
        if faults:
            for fault in faults:
                print(f"error: {fault}", file=sys.stderr)
            return 1
        print(f"ok: {len(LINE)} characters, {len(LINE.encode())} bytes")
        print("tournament: Indomie in a hotel kettle, 5/5/5 = 15 (winner)")
        print(LINE)
        return 0

    if args.self_test:
        faults = problems(LINE)
        if faults:
            for fault in faults:
                print(f"error: {fault}", file=sys.stderr)
            return 1
        if roundtrip_check(LINE) != 0:
            return 1
        print(f"self-test ok: {len(LINE)} chars, round-trip byte-identical")
        return 0

    return write_entry(LINE, args.out)


if __name__ == "__main__":
    raise SystemExit(main())
