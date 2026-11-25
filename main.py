#!/usr/bin/env python3
"""The Best Meal You Ever Had — make.fun entry.

Writes one sentence, at most 200 characters, about the best meal
I ever had, to /output/entry.txt.

Tournament winner (specificity 5 / surprise 5 / freshness 4 = 14):
the nasi goreng on the curb at midnight — named dish, a real place,
a texture, a smell of the street, one specific moment, and an ending
that turns on the white-tablecloth dinners that never measured up.
"""

import argparse
import sys
from pathlib import Path

ENTRY = (
    "A street vendor in Jakarta handed me a plastic bag of nasi goreng "
    "with a fried egg on top, and I ate it on the curb at midnight, "
    "knees up, happier than at any white-tablecloth dinner since."
)

MAX_CHARS = 200


def check(text: str) -> list[str]:
    problems = []
    if not text or not text.strip():
        problems.append("entry is empty or only white space")
    if len(text) > MAX_CHARS:
        problems.append(f"entry is {len(text)} chars, over the {MAX_CHARS} limit")
    if "\n" in text.strip():
        problems.append("entry must be a single sentence, no newlines inside")
    return problems


def self_test() -> int:
    """Write the entry to a temp file and verify the bytes read back."""
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp) / "entry.txt"
        target.write_text(ENTRY, encoding="utf-8")
        back = target.read_text(encoding="utf-8")
        if back != ENTRY:
            print("error: self-test round-trip mismatch", file=sys.stderr)
            return 1
        problems = check(back)
        if problems:
            for problem in problems:
                print(f"error: {problem}", file=sys.stderr)
            return 1
    print(f"self-test ok: {len(ENTRY)} chars, round-trip byte-identical")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Write the best-meal entry.")
    parser.add_argument("--check", action="store_true",
                        help="Validate the entry without writing it.")
    parser.add_argument("--self-test", action="store_true",
                        help="Write to a temp file and verify the bytes read back.")
    parser.add_argument("--out", default="/output/entry.txt",
                        help="Where to write the entry.")
    args = parser.parse_args()

    problems = check(ENTRY)
    if problems:
        for problem in problems:
            print(f"error: {problem}", file=sys.stderr)
        return 1

    if args.self_test:
        return self_test()

    if args.check:
        print(f"ok: {len(ENTRY)} characters, {len(ENTRY.encode())} bytes")
        print("tournament: nasi goreng curb at midnight, 5/5/4 = 14 (winner)")
        print(ENTRY)
        return 0

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(ENTRY, encoding="utf-8")
    read_back = out.read_text(encoding="utf-8")
    assert read_back == ENTRY, "round-trip mismatch"
    print(f"wrote {len(ENTRY)} chars to {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
