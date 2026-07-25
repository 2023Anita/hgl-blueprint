#!/usr/bin/env python3
"""Validate an HGL Blueprint and report errors without modifying it."""

from __future__ import annotations

import argparse
from pathlib import Path

from hgl_core import load_blueprint, validate_blueprint


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("blueprint", type=Path)
    args = parser.parse_args()
    try:
        blueprint = load_blueprint(args.blueprint)
    except (OSError, ValueError) as exc:
        print(f"FAIL: {exc}")
        return 1
    result = validate_blueprint(blueprint)
    for warning in result.warnings:
        print(f"WARN: {warning}")
    for error in result.errors:
        print(f"ERROR: {error}")
    print("PASS: Blueprint is structurally valid" if result.valid else "FAIL: Blueprint is invalid")
    return 0 if result.valid else 1


if __name__ == "__main__":
    raise SystemExit(main())

