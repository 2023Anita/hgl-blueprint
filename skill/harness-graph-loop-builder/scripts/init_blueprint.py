#!/usr/bin/env python3
"""Create a review-phase HGL Blueprint scaffold without approving it."""

from __future__ import annotations

import argparse
from pathlib import Path

from hgl_core import SCHEMA_VERSION, SLUG_RE, write_json


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    value.add_argument("goal", help="One-sentence observable goal")
    value.add_argument("--name", required=True, help="Human-facing system name")
    value.add_argument("--slug", required=True, help="lowercase-hyphen slug")
    value.add_argument("--owner", required=True, help="Responsible human or role")
    value.add_argument("--root", required=True, type=Path, help="Project root")
    return value


def main() -> int:
    args = parser().parse_args()
    if not SLUG_RE.fullmatch(args.slug):
        raise SystemExit("--slug must contain lowercase letters, digits, and hyphens")
    destination = args.root.resolve() / ".hgl" / args.slug / "blueprint.json"
    if destination.exists():
        raise SystemExit(f"refusing to overwrite existing Blueprint: {destination}")
    blueprint = {
        "schema_version": SCHEMA_VERSION,
        "identity": {
            "name": args.name,
            "slug": args.slug,
            "owner": args.owner,
            "description": args.goal,
        },
        "lifecycle": {
            "phase": "review",
            "approval": {
                "status": "pending",
                "approved_by": "",
                "decision_ref": "",
            },
        },
        "harness": {
            "provider": "provider-neutral",
            "tools": [
                {
                    "id": "replace-with-tool",
                    "purpose": "Replace with the minimum capability required",
                }
            ],
            "permissions": {
                "allowed": ["read scoped project inputs"],
                "approval_required": ["external side effects"],
                "denied": ["secret exfiltration"],
            },
            "budgets": {
                "max_nodes": 8,
                "max_iterations_per_loop": 3,
                "max_runtime_seconds": 900,
                "max_result_chars": 4000,
            },
            "state": {
                "root": ".hgl-state",
                "persist_events": True,
                "resumable": True,
            },
        },
        "graph": {
            "entrypoints": ["replace-with-node"],
            "nodes": [
                {
                    "id": "replace-with-node",
                    "purpose": "Replace with one bounded unit of work",
                    "dependencies": [],
                    "result_schema": {
                        "type": "object",
                        "required": ["status", "evidence"],
                    },
                    "loop": {
                        "gather": "Declare minimum inputs",
                        "act": "Declare candidate-producing action",
                        "verify": "Declare independent check",
                        "max_attempts": 2,
                        "on_failure": "block",
                    },
                }
            ],
        },
        "verification": {
            "criteria": [
                {
                    "id": "AC-01",
                    "outcome": "Replace with an observable outcome",
                    "verifier": "Replace with a deterministic check or human gate",
                    "evidence": "Replace with an evidence path or read-back",
                    "owner": args.owner,
                    "blocking": True,
                }
            ]
        },
        "outputs": {
            "targets": ["codex", "python", "docs"],
            "root": "generated",
        },
        "provenance": {"sources": []},
    }
    write_json(destination, blueprint)
    print(destination)
    print("status: REVIEW — edit and validate; human approval is still required")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

