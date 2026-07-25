#!/usr/bin/env python3
"""Shared validation and rendering primitives for HGL Blueprint.

The module is dependency-free so an installed Skill can use it without package
installation. It validates structural contracts; domain verification remains
the responsibility of the generated system.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "1.0.0"
PHASES = {"draft", "review", "approved", "built"}
APPROVAL_STATES = {"pending", "approved", "rejected"}
TARGETS = {"codex", "python", "docs"}
FAILURE_POLICIES = {"repair", "block", "fail"}
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


@dataclass(frozen=True)
class ValidationResult:
    errors: tuple[str, ...]
    warnings: tuple[str, ...]

    @property
    def valid(self) -> bool:
        return not self.errors


def load_blueprint(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError("blueprint root must be a JSON object")
    return value


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def _expect_mapping(
    value: Any, path: str, errors: list[str]
) -> dict[str, Any]:
    if not isinstance(value, dict):
        errors.append(f"{path}: expected object")
        return {}
    return value


def _expect_list(value: Any, path: str, errors: list[str]) -> list[Any]:
    if not isinstance(value, list):
        errors.append(f"{path}: expected array")
        return []
    return value


def _required_text(
    mapping: dict[str, Any], key: str, path: str, errors: list[str]
) -> str:
    value = mapping.get(key)
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{path}.{key}: required non-empty string")
        return ""
    return value.strip()


def _positive_int(
    mapping: dict[str, Any], key: str, path: str, errors: list[str]
) -> int:
    value = mapping.get(key)
    if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
        errors.append(f"{path}.{key}: required positive integer")
        return 0
    return value


def _validate_acyclic(
    dependencies: dict[str, list[str]], errors: list[str]
) -> None:
    remaining = {node: set(deps) for node, deps in dependencies.items()}
    ready = sorted(node for node, deps in remaining.items() if not deps)
    visited: list[str] = []
    while ready:
        current = ready.pop(0)
        visited.append(current)
        for node, deps in remaining.items():
            if current in deps:
                deps.remove(current)
                if not deps and node not in visited and node not in ready:
                    ready.append(node)
                    ready.sort()
    if len(visited) != len(remaining):
        cyclic = sorted(set(remaining) - set(visited))
        errors.append("graph.nodes: dependency cycle detected among " + ", ".join(cyclic))


def validate_blueprint(blueprint: dict[str, Any]) -> ValidationResult:
    errors: list[str] = []
    warnings: list[str] = []

    expected_root = {
        "schema_version",
        "identity",
        "lifecycle",
        "harness",
        "graph",
        "verification",
        "outputs",
        "provenance",
    }
    missing = sorted(expected_root - set(blueprint))
    extra = sorted(set(blueprint) - expected_root)
    for key in missing:
        errors.append(f"{key}: required top-level field")
    for key in extra:
        errors.append(f"{key}: unsupported top-level field")

    if blueprint.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"schema_version: expected {SCHEMA_VERSION!r}")

    identity = _expect_mapping(blueprint.get("identity"), "identity", errors)
    _required_text(identity, "name", "identity", errors)
    slug = _required_text(identity, "slug", "identity", errors)
    _required_text(identity, "owner", "identity", errors)
    _required_text(identity, "description", "identity", errors)
    if slug and not SLUG_RE.fullmatch(slug):
        errors.append("identity.slug: use lowercase letters, digits, and hyphens")

    lifecycle = _expect_mapping(blueprint.get("lifecycle"), "lifecycle", errors)
    phase = lifecycle.get("phase")
    if phase not in PHASES:
        errors.append(f"lifecycle.phase: expected one of {sorted(PHASES)}")
    approval = _expect_mapping(
        lifecycle.get("approval"), "lifecycle.approval", errors
    )
    approval_status = approval.get("status")
    if approval_status not in APPROVAL_STATES:
        errors.append(
            "lifecycle.approval.status: expected pending, approved, or rejected"
        )
    if phase in {"approved", "built"}:
        if approval_status != "approved":
            errors.append(
                "lifecycle: approved/built phase requires approval.status=approved"
            )
        _required_text(
            approval, "approved_by", "lifecycle.approval", errors
        )
        _required_text(
            approval, "decision_ref", "lifecycle.approval", errors
        )

    harness = _expect_mapping(blueprint.get("harness"), "harness", errors)
    provider = _required_text(harness, "provider", "harness", errors)
    if provider and provider != "provider-neutral":
        errors.append("harness.provider: v1 core must be 'provider-neutral'")

    tools = _expect_list(harness.get("tools"), "harness.tools", errors)
    tool_ids: set[str] = set()
    for index, raw_tool in enumerate(tools):
        path = f"harness.tools[{index}]"
        tool = _expect_mapping(raw_tool, path, errors)
        tool_id = _required_text(tool, "id", path, errors)
        _required_text(tool, "purpose", path, errors)
        if tool_id in tool_ids:
            errors.append(f"{path}.id: duplicate {tool_id!r}")
        tool_ids.add(tool_id)

    permissions = _expect_mapping(
        harness.get("permissions"), "harness.permissions", errors
    )
    permission_sets: dict[str, set[str]] = {}
    for permission_class in ("allowed", "approval_required", "denied"):
        values = _expect_list(
            permissions.get(permission_class),
            f"harness.permissions.{permission_class}",
            errors,
        )
        normalized: set[str] = set()
        for value in values:
            if not isinstance(value, str) or not value.strip():
                errors.append(
                    f"harness.permissions.{permission_class}: values must be strings"
                )
            else:
                normalized.add(value.strip())
        permission_sets[permission_class] = normalized
    classes = tuple(permission_sets)
    for left_index, left in enumerate(classes):
        for right in classes[left_index + 1 :]:
            overlap = sorted(permission_sets[left] & permission_sets[right])
            if overlap:
                errors.append(
                    f"harness.permissions: {left} and {right} overlap: "
                    + ", ".join(overlap)
                )

    budgets = _expect_mapping(harness.get("budgets"), "harness.budgets", errors)
    _positive_int(budgets, "max_nodes", "harness.budgets", errors)
    _positive_int(
        budgets, "max_iterations_per_loop", "harness.budgets", errors
    )
    _positive_int(
        budgets, "max_runtime_seconds", "harness.budgets", errors
    )
    _positive_int(budgets, "max_result_chars", "harness.budgets", errors)

    state = _expect_mapping(harness.get("state"), "harness.state", errors)
    state_root = _required_text(state, "root", "harness.state", errors)
    if state_root and (Path(state_root).is_absolute() or ".." in Path(state_root).parts):
        errors.append("harness.state.root: must be a safe relative path")
    for key in ("persist_events", "resumable"):
        if not isinstance(state.get(key), bool):
            errors.append(f"harness.state.{key}: required boolean")

    graph = _expect_mapping(blueprint.get("graph"), "graph", errors)
    raw_nodes = _expect_list(graph.get("nodes"), "graph.nodes", errors)
    if not raw_nodes:
        errors.append("graph.nodes: at least one node is required")
    node_ids: set[str] = set()
    dependencies: dict[str, list[str]] = {}
    for index, raw_node in enumerate(raw_nodes):
        path = f"graph.nodes[{index}]"
        node = _expect_mapping(raw_node, path, errors)
        node_id = _required_text(node, "id", path, errors)
        _required_text(node, "purpose", path, errors)
        if node_id and not SLUG_RE.fullmatch(node_id):
            errors.append(f"{path}.id: use lowercase letters, digits, and hyphens")
        if node_id in node_ids:
            errors.append(f"{path}.id: duplicate {node_id!r}")
        node_ids.add(node_id)
        deps = _expect_list(node.get("dependencies"), f"{path}.dependencies", errors)
        clean_deps: list[str] = []
        for dep in deps:
            if not isinstance(dep, str) or not dep.strip():
                errors.append(f"{path}.dependencies: values must be node IDs")
            else:
                clean_deps.append(dep.strip())
        dependencies[node_id] = clean_deps
        result_schema = _expect_mapping(
            node.get("result_schema"), f"{path}.result_schema", errors
        )
        if result_schema.get("type") != "object":
            errors.append(f"{path}.result_schema.type: expected 'object'")
        loop = _expect_mapping(node.get("loop"), f"{path}.loop", errors)
        for field in ("gather", "act", "verify"):
            _required_text(loop, field, f"{path}.loop", errors)
        attempts = _positive_int(loop, "max_attempts", f"{path}.loop", errors)
        global_attempts = budgets.get("max_iterations_per_loop")
        if (
            attempts
            and isinstance(global_attempts, int)
            and attempts > global_attempts
        ):
            errors.append(
                f"{path}.loop.max_attempts: exceeds harness budget "
                f"{global_attempts}"
            )
        if loop.get("on_failure") not in FAILURE_POLICIES:
            errors.append(
                f"{path}.loop.on_failure: expected one of "
                f"{sorted(FAILURE_POLICIES)}"
            )
    for node_id, deps in dependencies.items():
        for dep in deps:
            if dep not in node_ids:
                errors.append(
                    f"graph.nodes[{node_id}].dependencies: unknown node {dep!r}"
                )
            if dep == node_id:
                errors.append(
                    f"graph.nodes[{node_id}].dependencies: self dependency"
                )
    if dependencies and all(dep in node_ids for deps in dependencies.values() for dep in deps):
        _validate_acyclic(dependencies, errors)

    entrypoints = _expect_list(graph.get("entrypoints"), "graph.entrypoints", errors)
    if not entrypoints:
        errors.append("graph.entrypoints: at least one entrypoint is required")
    for entrypoint in entrypoints:
        if entrypoint not in node_ids:
            errors.append(f"graph.entrypoints: unknown node {entrypoint!r}")
        elif dependencies.get(entrypoint):
            warnings.append(
                f"graph.entrypoints: {entrypoint!r} has dependencies and will not start first"
            )

    verification = _expect_mapping(
        blueprint.get("verification"), "verification", errors
    )
    criteria = _expect_list(
        verification.get("criteria"), "verification.criteria", errors
    )
    if not criteria:
        errors.append("verification.criteria: at least one criterion is required")
    criterion_ids: set[str] = set()
    for index, raw_criterion in enumerate(criteria):
        path = f"verification.criteria[{index}]"
        criterion = _expect_mapping(raw_criterion, path, errors)
        criterion_id = _required_text(criterion, "id", path, errors)
        for field in ("outcome", "verifier", "evidence", "owner"):
            _required_text(criterion, field, path, errors)
        if not isinstance(criterion.get("blocking"), bool):
            errors.append(f"{path}.blocking: required boolean")
        if criterion_id in criterion_ids:
            errors.append(f"{path}.id: duplicate {criterion_id!r}")
        criterion_ids.add(criterion_id)

    outputs = _expect_mapping(blueprint.get("outputs"), "outputs", errors)
    targets = _expect_list(outputs.get("targets"), "outputs.targets", errors)
    if not targets:
        errors.append("outputs.targets: select at least one target")
    for target in targets:
        if target not in TARGETS:
            errors.append(
                f"outputs.targets: unsupported target {target!r}; "
                f"implemented targets are {sorted(TARGETS)}"
            )
    if len(targets) != len(set(str(target) for target in targets)):
        errors.append("outputs.targets: duplicate target")
    output_root = _required_text(outputs, "root", "outputs", errors)
    if output_root and (
        Path(output_root).is_absolute() or ".." in Path(output_root).parts
    ):
        errors.append("outputs.root: must be a safe relative path")

    provenance = _expect_mapping(
        blueprint.get("provenance"), "provenance", errors
    )
    sources = _expect_list(provenance.get("sources"), "provenance.sources", errors)
    for index, raw_source in enumerate(sources):
        path = f"provenance.sources[{index}]"
        source = _expect_mapping(raw_source, path, errors)
        _required_text(source, "title", path, errors)
        _required_text(source, "location", path, errors)

    if phase in {"draft", "review"} and approval_status == "approved":
        warnings.append(
            "lifecycle: approval is recorded but phase is not approved; "
            "run approve_blueprint.py to align the lifecycle"
        )
    if not any(
        isinstance(item, dict) and item.get("blocking") is True for item in criteria
    ):
        warnings.append("verification.criteria: no blocking criterion is defined")

    return ValidationResult(tuple(errors), tuple(warnings))


def topological_order(blueprint: dict[str, Any]) -> list[str]:
    nodes = blueprint["graph"]["nodes"]
    remaining = {
        node["id"]: set(node.get("dependencies", [])) for node in nodes
    }
    order: list[str] = []
    while remaining:
        ready = sorted(node for node, deps in remaining.items() if not deps)
        if not ready:
            raise ValueError("graph contains a dependency cycle")
        for node in ready:
            order.append(node)
            remaining.pop(node)
        for deps in remaining.values():
            deps.difference_update(ready)
    return order


def blueprint_markdown(blueprint: dict[str, Any]) -> str:
    identity = blueprint["identity"]
    harness = blueprint["harness"]
    graph = blueprint["graph"]
    lines = [
        f"# {identity['name']}",
        "",
        identity["description"],
        "",
        "## Lifecycle",
        "",
        f"- Phase: `{blueprint['lifecycle']['phase']}`",
        f"- Approval: `{blueprint['lifecycle']['approval']['status']}`",
        f"- Owner: {identity['owner']}",
        "",
        "## Harness contract",
        "",
        f"- Provider: `{harness['provider']}`",
        f"- Tools: {', '.join(tool['id'] for tool in harness['tools']) or 'none'}",
        f"- State root: `{harness['state']['root']}`",
        f"- Node budget: {harness['budgets']['max_nodes']}",
        f"- Result limit: {harness['budgets']['max_result_chars']} characters",
        "",
        "## Graph plan",
        "",
    ]
    for node in graph["nodes"]:
        dependencies = ", ".join(node["dependencies"]) or "entry"
        lines.extend(
            [
                f"### `{node['id']}`",
                "",
                node["purpose"],
                "",
                f"- Depends on: {dependencies}",
                f"- Gather: {node['loop']['gather']}",
                f"- Act: {node['loop']['act']}",
                f"- Verify: {node['loop']['verify']}",
                f"- Attempts: {node['loop']['max_attempts']}",
                f"- Failure route: `{node['loop']['on_failure']}`",
                "",
            ]
        )
    lines.extend(["## Acceptance criteria", ""])
    for criterion in blueprint["verification"]["criteria"]:
        required = "blocking" if criterion["blocking"] else "advisory"
        lines.append(
            f"- **{criterion['id']}** ({required}) — {criterion['outcome']}  "
            f"Verifier: {criterion['verifier']}; evidence: {criterion['evidence']}."
        )
    lines.extend(
        [
            "",
            "## Permission envelope",
            "",
            f"- Allowed: {', '.join(harness['permissions']['allowed']) or 'none'}",
            "- Approval required: "
            + (", ".join(harness["permissions"]["approval_required"]) or "none"),
            f"- Denied: {', '.join(harness['permissions']['denied']) or 'none'}",
            "",
            "_Generated from an approved HGL Blueprint. Domain verification is still required._",
            "",
        ]
    )
    return "\n".join(lines)

