#!/usr/bin/env python3
"""Run dependency-free repository validation."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skill" / "harness-graph-loop-builder"


def run(command: list[str]) -> bool:
    print("$", " ".join(command))
    result = subprocess.run(command, cwd=ROOT, check=False)
    return result.returncode == 0


def validate_i18n() -> bool:
    required = {"en", "zh", "ja", "ko"}
    translation_root = ROOT / "docs" / "i18n"
    loaded = {
        path.stem: json.loads(path.read_text(encoding="utf-8"))
        for path in translation_root.glob("*.json")
    }
    if set(loaded) != required:
        print(f"i18n FAIL: expected {sorted(required)}, got {sorted(loaded)}")
        return False
    baseline = set(loaded["en"])
    valid = True
    for language, values in sorted(loaded.items()):
        if set(values) != baseline:
            print(
                f"i18n FAIL: {language} key mismatch "
                f"missing={sorted(baseline-set(values))} "
                f"extra={sorted(set(values)-baseline)}"
            )
            valid = False
    print("i18n PASS" if valid else "i18n FAIL")
    return valid


def validate_skill_structure() -> bool:
    skill_file = SKILL / "SKILL.md"
    metadata_file = SKILL / "agents" / "openai.yaml"
    required = [
        skill_file,
        metadata_file,
        SKILL / "scripts" / "validate_blueprint.py",
        SKILL / "references" / "blueprint.schema.json",
    ]
    missing = [str(path.relative_to(ROOT)) for path in required if not path.is_file()]
    if missing:
        print("skill FAIL: missing " + ", ".join(missing))
        return False
    text = skill_file.read_text(encoding="utf-8")
    valid = (
        text.startswith("---\n")
        and "\nname: harness-graph-loop-builder\n" in text
        and "\ndescription: " in text
        and "\n---\n" in text[4:]
    )
    metadata = metadata_file.read_text(encoding="utf-8")
    valid = valid and "$harness-graph-loop-builder" in metadata
    print("skill PASS" if valid else "skill FAIL: invalid metadata")
    return valid


def main() -> int:
    checks = [
        validate_skill_structure(),
        run(
            [
                sys.executable,
                str(SKILL / "scripts" / "validate_blueprint.py"),
                str(ROOT / "examples" / "code-repair" / "blueprint.json"),
            ]
        ),
        run(
            [
                sys.executable,
                "-m",
                "unittest",
                "discover",
                "-s",
                "tests",
                "-v",
            ]
        ),
        validate_i18n(),
    ]
    if all(checks):
        print("REPOSITORY PASS")
        return 0
    print("REPOSITORY FAIL")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
