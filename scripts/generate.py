#!/usr/bin/env python3
"""
Master generator script for the SltyNX GitHub Profile README.
Runs all modular SVG/PNG generators and prints a summary of generated assets.
"""
from __future__ import annotations
import pathlib
import sys

SCRIPT_DIR = pathlib.Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import generate_dotmatrix
import generate_hero
import generate_mobile
import generate_terminal


def main() -> int:
    all_written: dict[str, pathlib.Path] = {}
    all_written.update(generate_hero.generate_all())
    all_written.update(generate_dotmatrix.generate_all())
    all_written.update(generate_terminal.generate_all())
    all_written.update(generate_mobile.generate_all())

    print("SltyNX Profile Asset Generation Complete:")
    print("-" * 50)
    for name in sorted(all_written):
        path = all_written[name]
        print(f"  {name:30s} {path.stat().st_size:>9,} bytes")
    print("-" * 50)
    print(f"Total assets verified: {len(all_written)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
