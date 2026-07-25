# HGL Blueprint

HGL Blueprint designs provider-neutral Harness-Graph-Loop systems and generates implementation scaffolds only after an explicit human approval.

## Design language

**Blueprint**:  
The provider-neutral, human-reviewable contract for one proposed system.
_Avoid_: prompt, loose plan, workflow draft

**Harness Contract**:  
The runtime boundary for tools, permissions, context, budgets, state, evidence, and execution.
_Avoid_: wrapper, infrastructure bucket

**Graph Plan**:  
The dependency and routing model that connects bounded Nodes through typed results.
_Avoid_: swarm, agent team

**Loop Contract**:  
The gather, act, verify, repair, persist, and stop contract for one Node.
_Avoid_: retry prompt, infinite loop

**Result Envelope**:  
A schema-valid, size-bounded result returned by one Node.
_Avoid_: transcript, raw context

**Generated System**:  
Artifacts produced from one exact approved Blueprint.
_Avoid_: Blueprint when referring to built files

**Provider Adapter**:  
An implementation that translates the Blueprint contract into one runtime without weakening it.
_Avoid_: provider-neutral core

## Governance language

**Approval Gate**:  
A human decision required before an identified design transition or external side effect.
_Avoid_: optional confirmation

**Verifier**:  
An identified check that compares evidence with one acceptance criterion.
_Avoid_: confidence, reflection

**Evidence Record**:  
A durable pointer to the observation supporting PASS, FAIL, or BLOCKED.
_Avoid_: claim, memory

