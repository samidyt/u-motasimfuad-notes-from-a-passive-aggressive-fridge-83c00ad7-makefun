#!/usr/bin/env python3
"""Notes From a Passive-Aggressive Fridge — make.fun entry (program/v1).

The harness runs `python3 main.py` (Python 3.13, standard library only, no
network). The program writes one funny passive-aggressive note to
/output/entry.txt. Outside the grader's container, MAKEFUN_OUTPUT_DIR
stands in for /output:

    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py

Gate (from RULES.txt): /output/entry.txt must be UTF-8 text of 1-200
characters, not only whitespace. This program enforces the gate on its
own output and fails loudly instead of handing in a bad entry.

The note is a fixed constant: no randomness, no clock, no environment
input beyond the output directory, so repeated runs are byte-identical.
"""

import os
import sys

# The note. Dry, petty, specific: the fridge counts door openings with its
# own sensor, notes that nothing was ever taken, and keeps a diary about it.
NOTE = "My door sensor counted 14 openings today. Zero snacks taken. I have started a diary, and you are in it."


def validate_note(note: str) -> int:
    """Return the note's character count, or fail loudly if it breaks the gate.

    The gate (RULES.txt) needs /output/entry.txt to be UTF-8 text of 1-200
    characters, not only whitespace; the bounty wants a single line.
    """
    chars = len(note)
    if chars < 1 or chars > 200:
        raise ValueError(f"entry is {chars} chars, gate needs 1-200")
    if not note.strip():
        raise ValueError("entry is only whitespace")
    if "\n" in note or "\r" in note:
        raise ValueError("entry must be a single line")
    return chars


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")

    try:
        chars = validate_note(NOTE)
    except ValueError as exc:
        print(f"invalid entry: {exc}", file=sys.stderr)
        return 1

    os.makedirs(out_dir, exist_ok=True)
    # Write the note exactly as it stands: no trailing newline, so the
    # file holds one line and its byte count matches the char count.
    with open(os.path.join(out_dir, "entry.txt"), "w", encoding="utf-8",
              newline="") as f:
        f.write(NOTE)

    print(f"wrote entry.txt ({chars} chars)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
