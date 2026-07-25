---
name: harness-graph-loop-builder
description: Design, review, generate, and validate specification-first Harness-Graph-Loop systems from a user's goal. Use when a user wants to turn a repeatable or high-consequence task into a bounded agent workflow with isolated node contexts, typed results, explicit permissions, durable state, independent verification, approval gates, and Codex or Python output. Default to design-only; never build or run the generated system until the user explicitly approves its Blueprint.
---

# HGL Blueprint

Turn a goal into a reviewable Harness-Graph-Loop system without letting implementation outrun consent.

## Non-negotiable sequence

`intake -> blueprint -> validate -> human approval -> build -> validate -> handoff`

Do not combine design and build. A plausible design is not approval. A generated scaffold is not a verified system.

## Choose the smallest justified shape

- Use a direct workflow when one bounded pass and one verification step are enough.
- Use one Loop when feedback can improve the next attempt.
- Add a Graph only when multiple bounded units have real dependencies, parallelism, or independent review.
- Add the full Harness contract when tools, permissions, context isolation, budgets, recovery, or auditability matter.

Prefer the smallest shape that satisfies the goal. Do not add agents, nodes, or adapters for visual complexity.

## Mode 1: design

Default to `design` for every new request.

1. Resolve facts from the environment instead of asking the user.
2. Ask one decision question at a time when an answer changes scope, risk, ownership, or acceptance.
3. Define canonical terms using [domain-language.md](references/domain-language.md).
4. Create a Blueprint matching [blueprint-contract.md](references/blueprint-contract.md) and [blueprint.schema.json](references/blueprint.schema.json).
5. Map each required outcome to independent evidence using [verification-policy.md](references/verification-policy.md).
6. Apply least privilege and action-time approval using [safety-and-permissions.md](references/safety-and-permissions.md).
7. Select only implemented targets using [provider-adapters.md](references/provider-adapters.md).
8. Run:

```bash
python3 scripts/validate_blueprint.py "<path-to-blueprint.json>"
```

9. Present the validated Blueprint, trade-offs, non-goals, and unresolved risks.
10. Stop and wait for explicit approval.

The Blueprint remains `lifecycle.phase: review` and `approval.status: pending` until the user approves that exact design.

## Mode 2: build

Enter `build` only after explicit approval.

1. Record the approving human or role and a short decision reference:

```bash
python3 scripts/approve_blueprint.py "<path-to-blueprint.json>" \
  --approved-by "<human-or-role>" \
  --decision-ref "<approval-reference>"
```

2. Re-run validation.
3. Generate the approved targets:

```bash
python3 scripts/build_system.py "<path-to-blueprint.json>" \
  --output-root "<new-empty-directory>"
```

4. Implement domain-specific actions only inside the generated contracts. Do not broaden tools, permissions, nodes, or outputs while building.
5. Run:

```bash
python3 scripts/validate_generated_system.py "<generated-system-directory>"
```

6. Execute every domain verifier declared by the Blueprint.
7. Report `PASS`, `FAIL`, or `BLOCKED` with evidence. Never infer completion from generation alone.

## Mode 3: validate

Use `validate` to inspect a Blueprint or generated system without changing it.

- Validate schema and graph invariants.
- Confirm all required criteria have non-circular verifiers.
- Confirm every node has bounded retries and a typed output.
- Confirm permission classes do not overlap.
- Confirm approval-sensitive actions remain gated.
- Confirm generated files remain inside the declared output root.

## Mode 4: improve

Use `improve` only from observed failures or repeated friction.

- Preserve the original evidence.
- Classify the failure before proposing a change.
- Produce a reviewable improvement proposal.
- Do not silently modify this Skill, durable project instructions, permissions, memory, or production configuration.

## Required architecture

### Harness

Own runtime policy: tools, permissions, isolation, budgets, state, events, cancellation, secrets, and provider adapters.

### Graph

Own wiring: nodes, dependencies, typed edges, entry points, fan-out/fan-in, routing, partial-failure policy, and independent review.

### Loop

Own one bounded unit: gather, act, verify, repair or retry, persist, and stop.

The Graph does not grant permissions. A Loop does not redefine global completion. Provider adapters do not change the Blueprint contract.

## Completion rule

Completion requires:

- an approved Blueprint;
- generated artifacts for every selected target;
- successful structural validation;
- passing required domain verifiers with evidence;
- no unresolved approval gate;
- a resumable handoff.

Budget exhaustion, rejection, failure, and blocked are valid terminal results. Report them truthfully.

