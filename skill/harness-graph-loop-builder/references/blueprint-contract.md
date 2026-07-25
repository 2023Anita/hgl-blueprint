# Blueprint contract

`blueprint.json` is the authoritative, provider-neutral design artifact.

## Required areas

1. `identity` — stable name, slug, owner, and purpose.
2. `lifecycle` — current phase plus an explicit human approval record.
3. `harness` — provider, tools, permission classes, budgets, and durable state.
4. `graph` — entry points and nodes with dependency edges.
5. `verification` — observable acceptance criteria and evidence.
6. `outputs` — implemented build targets and a relative output root.
7. `provenance` — source materials and design lineage without secrets.

## Node contract

Each node declares:

- a unique `id`;
- a single purpose;
- dependency node IDs;
- a JSON-shaped `result_schema`;
- a bounded Loop Contract;
- a partial-failure policy.

The result is a Result Envelope, not a transcript. It must fit inside `max_result_chars`.

## Loop contract

Each Loop Contract defines:

- `gather`: the minimum context required;
- `act`: the candidate-producing action;
- `verify`: the check that can reject it;
- `max_attempts`: a finite positive limit;
- `on_failure`: `repair`, `block`, or `fail`.

## Approval invariant

`lifecycle.phase` may become `approved` or `built` only when:

- `approval.status` is `approved`;
- `approved_by` is non-empty;
- `decision_ref` identifies the human decision.

Any material Blueprint change after approval returns the design to `review`.

## Build targets

Version 1 implements:

- `codex` — Codex-native instructions and Skill scaffold;
- `python` — dependency-free reference runtime and manifest;
- `docs` — human-readable system documentation.

Do not claim support for other providers until an adapter and its tests exist.

