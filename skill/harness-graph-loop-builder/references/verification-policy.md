# Verification policy

## Evidence ladder

Prefer:

1. schema, type, parser, or invariant check;
2. unit, integration, or end-to-end behavior test;
3. build, lint, or static analysis;
4. external state read-back;
5. visual inspection;
6. rubric-based human review;
7. model self-review.

Self-review may discover problems but cannot be the only required completion gate.

## Criterion contract

Every required criterion declares:

- stable `id`;
- observable `outcome`;
- named `verifier`;
- expected `evidence`;
- responsible `owner`;
- whether it blocks completion.

## Independence test

A verifier is insufficient when it:

- shares the producer's hidden reasoning;
- checks only formatting while the goal is behavioral;
- accepts success from a command without reading resulting state;
- can pass after a required node failed;
- treats missing evidence as success.

Return `BLOCKED`, not `PASS`, when required evidence cannot be observed.

## Generated-system gate

Structural validation proves only that the system is well formed. Domain completion additionally requires every blocking criterion to pass against real evidence.

