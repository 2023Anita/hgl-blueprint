<div align="center">
  <img src="docs/assets/hero.svg" alt="HGL Blueprint" width="100%">
</div>

<p align="center">
  <a href="README.md">English</a> ·
  <a href="README.zh-CN.md">简体中文</a> ·
  <a href="README.ja.md">日本語</a> ·
  <a href="README.ko.md">한국어</a>
</p>

<p align="center">
  <strong>Design the system before the system runs.</strong><br>
  A specification-first Skill that turns a need into a bounded, reviewable
  Harness–Graph–Loop Blueprint—and generates an implementation only after
  explicit human approval.
</p>

<p align="center">
  <a href="https://2023anita.github.io/hgl-blueprint/">Live site</a> ·
  <a href="#five-minute-start">Five-minute start</a> ·
  <a href="#worked-example">Worked example</a> ·
  <a href="#safety-model">Safety model</a>
</p>

## The short answer

**Yes: this repository can be reused to design a different system from your
own requirements.** It is not a one-click “spawn many agents” template. It is a
design compiler with a deliberate review boundary:

```text
need → assess complexity → draft blueprint → validate → human approval
     → generate targets → domain verification → evidence-backed handoff
```

The reusable unit is `blueprint.json`. It describes the goal, boundaries,
permissions, nodes, edges, local feedback loops, budgets, evidence, recovery,
and stop conditions without locking the design to one runtime.

<img src="docs/assets/hgl-blueprint-illustrations/01-intent-to-blueprint.png" alt="A small traveler sorts an unclear need into a reviewable blueprint while the build toolbox stays closed">

## The problem it solves

Agent systems often make important decisions while already acting:

- scope expands implicitly;
- every worker receives too much context or permission;
- transcripts become the integration format;
- retries continue without a finite budget;
- “looks good” replaces evidence;
- a failed run cannot be resumed cleanly.

HGL Blueprint moves those decisions into a machine-validatable artifact that a
human can inspect, reject, or approve before generation begins.

## The three layers

| Layer | Responsibility | Typical questions |
|---|---|---|
| **Harness** | Controls the operating environment | Which tools and permissions exist? What are the budgets, evidence store, cancellation and recovery rules? |
| **Graph** | Expresses real dependencies | Which bounded units exist? What must happen first? Where are fan-out, fan-in, failure routes and independent review? |
| **Loop** | Improves one bounded unit | What feedback changes the next attempt? What is persisted? When must the unit stop? |

<img src="docs/assets/hgl-blueprint-illustrations/02-harness-graph-loop.png" alt="A small traveler tends a protected room, connected worktables, and a local feedback checklist">

The project always chooses the smallest justified shape:

- **direct workflow** for one bounded pass;
- **Loop** only when feedback can improve the next attempt;
- **Graph** only when units have real dependencies, parallelism, or independent review;
- **Harness** when tools, permissions, context, state, budgets, recovery, and auditability matter.

## What this repository generates

One approved, provider-neutral `blueprint.json` can generate:

- **Codex target** — project instructions plus a callable operator Skill;
- **Python target** — a dependency-free reference runtime and manifest;
- **Docs target** — human-readable architecture, operational and acceptance contracts.

The generator does **not** claim to deliver a finished domain product. It
creates the controlled operating skeleton. Generated systems still require
domain-specific implementation and verification.

## What it is not

- not a replacement for domain expertise;
- not a guarantee that a workflow is correct because it has many agents;
- not permission to commit, push, deploy, publish, delete, or spend money;
- not an autonomous approval mechanism;
- not a universal runtime adapter—v1 is Codex-first with a Python reference.

## Five-minute start

### 1. Install the Skill

Clone the repository, then link the Skill into your Codex skills directory:

```bash
git clone https://github.com/2023Anita/hgl-blueprint.git
mkdir -p "$HOME/.codex/skills"
ln -s "$(pwd)/hgl-blueprint/skill/harness-graph-loop-builder" \
  "$HOME/.codex/skills/harness-graph-loop-builder"
```

Restart or refresh Codex after installation. If you prefer not to use a
symbolic link, copy the Skill directory instead.

### 2. Ask for a Blueprint

```text
Use $harness-graph-loop-builder to design a reviewable HGL Blueprint for
turning my weekly research notes into an evidence-linked literature brief.
Do not build until I approve.
```

The Skill should first ask only for missing decisions that materially affect
the architecture, then produce a review package rather than an executing
system.

### 3. Validate the draft

```bash
python3 skill/harness-graph-loop-builder/scripts/validate_blueprint.py \
  path/to/blueprint.json
```

### 4. Review the approval gate

Check at least:

- goal and explicit non-goals;
- input and output contracts;
- tools, permissions, and external side effects;
- node responsibilities and graph edges;
- retry, no-progress, cost, and time budgets;
- verifier/evidence mapping;
- recovery and stop conditions.

<img src="docs/assets/hgl-blueprint-illustrations/03-human-approval-gate.png" alt="A small traveler waits at a human approval gate before any building begins">

### 5. Approve, then generate

Approval must be explicit and external to the Blueprint. Material changes after
approval return the design to review. The generator fails closed while approval
is pending.

## Worked example

The included [`examples/code-repair/blueprint.json`](examples/code-repair/blueprint.json)
models one reproducible repository defect:

1. gather only the reproduction, relevant code, and constraints;
2. diagnose the smallest plausible cause;
3. implement a bounded repair;
4. run named verifiers;
5. perform independent review;
6. return compact Result Envelopes and durable Evidence Records.

Validate it:

```bash
python3 skill/harness-graph-loop-builder/scripts/validate_blueprint.py \
  examples/code-repair/blueprint.json
```

Try generation in a temporary output directory:

```bash
python3 skill/harness-graph-loop-builder/scripts/build_system.py \
  examples/code-repair/blueprint.json \
  --target codex \
  --output /tmp/hgl-code-repair
```

The checked-in example is intentionally in review state, so build remains
blocked until a human approval record is supplied.

## Blueprint anatomy

```json
{
  "intent": {
    "goal": "Produce a verified result",
    "non_goals": ["Unapproved publication"]
  },
  "harness": {
    "permissions": {},
    "budgets": {},
    "evidence": {},
    "recovery": {}
  },
  "graph": {
    "nodes": [],
    "edges": []
  },
  "approval": {
    "status": "pending"
  }
}
```

The full contract lives in
[`blueprint.schema.json`](skill/harness-graph-loop-builder/references/blueprint.schema.json).
Design rationale is recorded in [`docs/adr`](docs/adr).

## Result and evidence contract

Workers keep heavy source material local to their bounded task. They return a
size-limited Result Envelope: status, concise result, evidence references,
remaining risks, and a suggested next route—not an entire transcript.

Every blocking acceptance criterion names:

1. a **Verifier** that performs the check; and
2. an **Evidence Record** that persists what happened.

<img src="docs/assets/hgl-blueprint-illustrations/04-evidence-handoff.png" alt="A small traveler carries only a compact result and evidence record to a durable handoff tray">

## Where it can be used

The same principles can shape:

- repository defect repair and migration workflows;
- literature review, data analysis, and manuscript preparation;
- medical teaching content with expert review gates;
- content research, drafting, fact-checking, and publication packaging;
- compliance, audit, and evidence-collection pipelines;
- dataset curation and quality-control systems;
- product discovery, specification, implementation, and release checks.

Use a direct workflow when the work is simple. HGL is valuable only when
boundaries, dependencies, iterative verification, or recoverability are real.

## Safety model

- **Fail closed:** missing approval or evidence is not success.
- **Least privilege:** each phase receives only the capabilities it needs.
- **No self-approval:** the generated system cannot approve its own design.
- **Finite work:** retries, no-progress, time, and cost have explicit limits.
- **Material-change review:** changed permissions, scope, graph, budgets, or
  acceptance rules invalidate prior approval.
- **External effects remain gated:** commit, push, deploy, publish, delete,
  purchase, and similar actions require their own authorization.
- **Durable handoff:** a fresh operator can resume from artifacts instead of
  reconstructing chat history.

## Repository map

```text
hgl-blueprint/
├── skill/harness-graph-loop-builder/   # installable design-and-build Skill
├── examples/code-repair/               # complete review-state example
├── tests/                              # contract and approval-gate tests
├── scripts/verify_repo.py              # one-command repository verification
├── docs/                               # multilingual GitHub Pages site + ADRs
└── README.*.md                         # English, Chinese, Japanese, Korean
```

## Verify the repository

```bash
python3 scripts/verify_repo.py
```

This checks Skill structure, Blueprint schema and graph invariants, the approval
gate, generated targets, unit tests, and four-language key parity.

## Status and roadmap

**v1 foundation:** installable Skill, contract validators, approval-gated
generator, Codex/Python/docs targets, tested example, multilingual site.

Near-term work should remain evidence-led: more contract fixtures, stronger
failure-path tests, and additional runtime adapters only after each adapter has
an implementation and contract tests.

## Provenance

HGL Blueprint is an independent project inspired by
[Archive228/loop-graph-harness](https://github.com/Archive228/loop-graph-harness),
a compact teaching demonstration of Loop, Graph, and Harness composition.
See [NOTICE](NOTICE) for attribution and implementation boundaries.

MIT License.
