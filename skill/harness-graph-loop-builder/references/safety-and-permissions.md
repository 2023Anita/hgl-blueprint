# Safety and permissions

## Permission classes

**Allowed**: Read-only inspection, local calculation, tests, and explicitly scoped reversible edits.

**Approval required**: External messages, publication, repository creation, commit, push, deployment, production writes, deletion, bulk rewrite, permission or credential changes, and sensitive-data transmission.

**Denied**: Secret exfiltration, bypassing controls, work outside scope, silent policy weakening, and self-granted permissions.

The three classes must be disjoint.

## Phase envelopes

- `design`: inspect facts and write Blueprint artifacts only;
- `build`: create only approved generated artifacts;
- `validate`: read-only checks and bounded test execution;
- `run`: use task-specific capabilities only;
- `improve`: propose changes without applying durable policy changes.

## Context and result boundaries

- Start nodes with only their declared inputs.
- Do not inherit the parent transcript.
- Return a schema-valid Result Envelope.
- Enforce `max_result_chars`.
- Store evidence outside prompts and return pointers.
- Never persist secret values.

## High-consequence domains

Medical, legal, financial, security, and identity-related workflows require stronger sources, auditability, isolation, and accountable human review. Generated systems assist; they do not replace professional responsibility.

