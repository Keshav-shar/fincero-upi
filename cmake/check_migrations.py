#!/usr/bin/env python3
"""Fail if a migration breaks the rules for db/migrations.

- Forward-only: dbmate requires a `-- migrate:down` directive, so it stays empty.
- Rule 2: no single migration may touch both the inr and cero schemas, which rules out
  cross-schema foreign keys, views and functions.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

DOWN = re.compile(r"^--\s*migrate:down\b.*$", re.MULTILINE)
COMMENT = re.compile(r"--[^\n]*|/\*.*?\*/", re.DOTALL)


def check_text(name: str, text: str) -> list[str]:
    errors: list[str] = []

    match = DOWN.search(text)
    if match is None:
        errors.append(f"{name}: missing -- migrate:down directive")
    elif COMMENT.sub("", text[match.end():]).strip():
        errors.append(f"{name}: down section must be empty (migrations are forward-only)")

    body = COMMENT.sub(" ", text).lower()
    if re.search(r"\binr\.", body) and re.search(r"\bcero\.", body):
        errors.append(f"{name}: touches both inr and cero schemas (Rule 2)")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("migrations_dir", type=Path)
    args = parser.parse_args()

    errors: list[str] = []
    for path in sorted(args.migrations_dir.glob("*.sql")):
        errors.extend(check_text(path.name, path.read_text(encoding="utf-8")))

    for error in errors:
        print(f"migration violation: {error}", file=sys.stderr)
    if not errors:
        print("migrations ok")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
