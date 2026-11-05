#!/usr/bin/env python3
"""Fail if core/ uses I/O, clocks, global RNG, or floating point outside prediction.

Enforces hard rules 1 and 6. Test folders are skipped: tests may read golden files.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

SOURCE_SUFFIXES = {".h", ".hpp", ".cc", ".cpp"}

# Comments and string literals are removed first, so prose cannot trigger a failure.
STRIP = re.compile(
    r"""//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\\n])*"|'(?:\\.|[^'\\\n])*'""",
    re.DOTALL,
)
INCLUDE = re.compile(r"^\s*#\s*include\s*[<\"]([^>\"]+)[>\"]", re.MULTILINE)

BANNED_HEADERS = {
    "chrono", "ctime", "time.h", "random", "cstdlib", "stdlib.h",
    "fstream", "iostream", "cstdio", "stdio.h", "filesystem",
    "thread", "mutex", "future", "atomic",
}

BANNED_CODE = {
    r"\brand\s*\(": "global RNG",
    r"\bsrand\s*\(": "global RNG",
    r"\brandom_device\b": "global RNG",
    r"\bgetenv\s*\(": "environment access",
    r"\bsystem_clock\b|\bsteady_clock\b|\bhigh_resolution_clock\b": "clock",
    r"\btime\s*\(\s*(nullptr|NULL|0)?\s*\)": "clock",
}

FLOATING_POINT = re.compile(r"\b(float|double)\b")
FLOATS_ALLOWED_IN = "prediction"


def check_file(path: Path, core_root: Path) -> list[str]:
    raw = path.read_text(encoding="utf-8")
    errors: list[str] = []

    # Includes first: stripping would erase the quoted form.
    for header in INCLUDE.findall(raw):
        if header in BANNED_HEADERS:
            errors.append(f"{path}: includes <{header}>")

    code = STRIP.sub(" ", raw)
    for pattern, kind in BANNED_CODE.items():
        if re.search(pattern, code):
            errors.append(f"{path}: {kind} ({pattern})")

    module = path.relative_to(core_root).parts[0]
    if module != FLOATS_ALLOWED_IN and FLOATING_POINT.search(code):
        errors.append(f"{path}: float or double outside core/{FLOATS_ALLOWED_IN} (Rule 1)")

    return errors


def check_tree(core_root: Path) -> list[str]:
    errors: list[str] = []
    for path in sorted(core_root.rglob("*")):
        if path.suffix in SOURCE_SUFFIXES and "tests" not in path.parts:
            errors.extend(check_file(path, core_root))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("core_root", type=Path)
    args = parser.parse_args()

    if not args.core_root.is_dir():
        print(f"not a directory: {args.core_root}", file=sys.stderr)
        return 2

    errors = check_tree(args.core_root)
    for error in errors:
        print(f"purity violation: {error}", file=sys.stderr)
    if not errors:
        print("core purity ok")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
