#!/usr/bin/env python3
"""Record an explicit human approval on one exact Blueprint."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path

from hgl_core import load_blueprint, validate_blueprint, write_json


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("blueprint", type=Path)
    parser.add_argument("--approved-by", required=True)
    parser.add_argument("--decision-ref", required=True)
    args = parser.parse_args()
    blueprint = load_blueprint(args.blueprint)
    result = validate_blueprint(blueprint)
    if not result.valid:
        for error in result.errors:
            print(f"ERROR: {error}")
        print("FAIL: refusing to approve an invalid Blueprint")
        return 1
    lifecycle = blueprint["lifecycle"]
    if lifecycle["approval"]["status"] == "rejected":
        print("FAIL: rejected Blueprint must return to review before approval")
        return 1
    lifecycle["phase"] = "approved"
    lifecycle["approval"] = {
        "status": "approved",
        "approved_by": args.approved_by.strip(),
        "decision_ref": args.decision_ref.strip(),
        "approved_at": datetime.now(timezone.utc).isoformat(),
    }
    if not lifecycle["approval"]["approved_by"] or not lifecycle["approval"]["decision_ref"]:
        print("FAIL: approval identity and decision reference cannot be blank")
        return 1
    write_json(args.blueprint, blueprint)
    print("PASS: Blueprint approved")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

