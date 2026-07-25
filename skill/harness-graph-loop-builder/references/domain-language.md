# Domain language

Use these terms consistently in generated artifacts.

**Blueprint**:  
The provider-neutral, human-reviewable contract describing one proposed system.
_Avoid_: plan, prompt, workflow draft

**Harness Contract**:  
The runtime policy governing tools, permissions, context, budgets, state, evidence, and execution boundaries.
_Avoid_: wrapper, miscellaneous infrastructure

**Graph Plan**:  
The dependency and routing model connecting bounded nodes through typed results.
_Avoid_: agent swarm, arbitrary orchestration

**Loop Contract**:  
The gather, act, verify, repair, persist, and stop contract for one bounded node.
_Avoid_: retry prompt, endless cycle

**Node**:  
One bounded unit in the Graph Plan with declared dependencies, input, output, Loop Contract, and permissions inherited from the Harness Contract.
_Avoid_: agent, worker, step when the distinction matters

**Result Envelope**:  
The size-bounded, schema-valid result a Node may return to downstream nodes.
_Avoid_: summary, full transcript

**Verifier**:  
An identified check that compares evidence with one acceptance criterion and returns PASS, FAIL, or BLOCKED.
_Avoid_: reflection, confidence

**Evidence Record**:  
A durable pointer to the observation supporting a verifier result.
_Avoid_: claim, model memory

**Approval Gate**:  
A human decision required before a specified design or external side effect may proceed.
_Avoid_: confirmation hint

**Provider Adapter**:  
A boundary implementation that translates the Blueprint contract into one agent runtime without changing its meaning.
_Avoid_: core runtime

**Generated System**:  
Artifacts produced from one exact approved Blueprint.
_Avoid_: framework when referring to a single generated instance

