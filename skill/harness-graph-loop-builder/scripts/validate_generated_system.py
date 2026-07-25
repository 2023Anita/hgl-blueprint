#!/usr/bin/env python3
"""Validate the structure and approval binding of a generated HGL system."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from hgl_core import load_blueprint, validate_blueprint


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("system_root", type=Path)
    args = parser.parse_args()
    root = args.system_root.resolve()
    errors: list[str] = []
    for relative in (
        "blueprint.json",
        "BLUEPRINT.md",
        "build-manifest.json",
    ):
        if not (root / relative).is_file():
            errors.append(f"missing {relative}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        print("FAIL: generated system is incomplete")
        return 1
    blueprint = load_blueprint(root / "blueprint.json")
    result = validate_blueprint(blueprint)
    errors.extend(result.errors)
    manifest = json.loads(
        (root / "build-manifest.json").read_text(encoding="utf-8")
    )
    if manifest.get("blueprint_slug") != blueprint["identity"]["slug"]:
        errors.append("build-manifest Blueprint slug mismatch")
    if manifest.get("approval") != blueprint["lifecycle"]["approval"]:
        errors.append("build-manifest approval does not match Blueprint")
    target_files = {
        "codex": "codex/AGENTS.md",
        "python": "python/runtime.py",
        "docs": "docs/system.md",
    }
    for target in blueprint["outputs"]["targets"]:
        expected = target_files[target]
        if not (root / expected).is_file():
            errors.append(f"target {target!r} missing {expected}")
    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        print("FAIL: generated system is invalid")
        return 1
    print("PASS: generated system is structurally valid")
    print("NOTE: domain acceptance criteria still require real evidence")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

