#!/usr/bin/env python3
"""Build declared v1 targets from an approved HGL Blueprint."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from hgl_core import (
    blueprint_markdown,
    load_blueprint,
    topological_order,
    validate_blueprint,
    write_json,
)


def ensure_empty(destination: Path) -> None:
    if destination.exists() and any(destination.iterdir()):
        raise ValueError(f"output directory is not empty: {destination}")
    destination.mkdir(parents=True, exist_ok=True)


def write_python_target(root: Path, blueprint: dict) -> None:
    target = root / "python"
    target.mkdir(parents=True, exist_ok=True)
    manifest = {
        "schema_version": blueprint["schema_version"],
        "system": blueprint["identity"],
        "order": topological_order(blueprint),
        "nodes": blueprint["graph"]["nodes"],
        "budgets": blueprint["harness"]["budgets"],
        "notice": "Reference runtime only; this is not a security sandbox.",
    }
    write_json(target / "system-manifest.json", manifest)
    runtime = '''#!/usr/bin/env python3
"""Dependency-free HGL reference runtime.

It proves graph ordering and contract loading. Replace node hooks only after
adding domain tests; this file does not claim to sandbox arbitrary code.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=Path(__file__).with_name("system-manifest.json"))
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    print(f"system: {manifest['system']['name']}")
    print("mode: dry-run" if args.dry_run else "mode: contract inspection")
    for index, node_id in enumerate(manifest["order"], start=1):
        print(f"{index:02d}  {node_id}")
    print("No domain actions executed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
'''
    (target / "runtime.py").write_text(runtime, encoding="utf-8")


def write_codex_target(root: Path, blueprint: dict) -> None:
    target = root / "codex"
    skill_root = target / "skills" / f"{blueprint['identity']['slug']}-operator"
    skill_root.mkdir(parents=True, exist_ok=True)
    (target / "AGENTS.md").write_text(
        "# Generated HGL system instructions\n\n"
        "Read `../BLUEPRINT.md` and `../blueprint.json` before acting. "
        "Operate only inside the declared Harness Contract. Do not bypass "
        "approval gates. Treat generated scaffolding as unverified until every "
        "blocking criterion has passing evidence.\n",
        encoding="utf-8",
    )
    nodes = "\n".join(
        f"- `{node_id}`" for node_id in topological_order(blueprint)
    )
    skill_text = f"""---
name: {blueprint['identity']['slug']}-operator
description: Operate the approved {blueprint['identity']['name']} HGL system without changing its Blueprint, permissions, graph, or completion criteria.
---

# {blueprint['identity']['name']} operator

Read the generated `blueprint.json` and `BLUEPRINT.md`.

## Node order

{nodes}

For each node, gather only declared inputs, produce a Result Envelope, run the
declared verifier, persist evidence, and route according to `on_failure`.

Stop before every approval-required action. Completion requires every blocking
criterion to pass with evidence.
"""
    (skill_root / "SKILL.md").write_text(skill_text, encoding="utf-8")


def write_docs_target(root: Path, blueprint: dict) -> None:
    target = root / "docs"
    target.mkdir(parents=True, exist_ok=True)
    (target / "system.md").write_text(
        blueprint_markdown(blueprint), encoding="utf-8"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("blueprint", type=Path)
    parser.add_argument("--output-root", required=True, type=Path)
    args = parser.parse_args()
    blueprint = load_blueprint(args.blueprint)
    result = validate_blueprint(blueprint)
    if not result.valid:
        for error in result.errors:
            print(f"ERROR: {error}")
        print("FAIL: invalid Blueprint")
        return 1
    approval = blueprint["lifecycle"]["approval"]
    if (
        blueprint["lifecycle"]["phase"] != "approved"
        or approval["status"] != "approved"
    ):
        print("FAIL: build requires an explicitly approved Blueprint")
        return 2
    destination = args.output_root.resolve()
    try:
        ensure_empty(destination)
    except ValueError as exc:
        print(f"FAIL: {exc}")
        return 3

    (destination / "blueprint.json").write_text(
        json.dumps(blueprint, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (destination / "BLUEPRINT.md").write_text(
        blueprint_markdown(blueprint), encoding="utf-8"
    )
    targets = blueprint["outputs"]["targets"]
    if "python" in targets:
        write_python_target(destination, blueprint)
    if "codex" in targets:
        write_codex_target(destination, blueprint)
    if "docs" in targets:
        write_docs_target(destination, blueprint)
    build_manifest = {
        "schema_version": blueprint["schema_version"],
        "blueprint_slug": blueprint["identity"]["slug"],
        "targets": targets,
        "approval": approval,
        "structural_status": "generated-not-domain-verified",
    }
    write_json(destination / "build-manifest.json", build_manifest)
    print(f"PASS: generated targets {', '.join(targets)}")
    print("status: GENERATED — domain verification is still required")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

