# Provider adapters

The Blueprint is provider-neutral. An adapter may translate mechanisms, but may not weaken contracts.

| Blueprint concept | Codex v1 | Python reference v1 |
|---|---|---|
| durable instructions | `AGENTS.md`, generated Skill | manifest and generated docs |
| node execution | bounded task or explicitly authorized subagent | topological dry-run/runtime hook |
| tools | Codex tool calls and local commands | injected Python callables |
| state | project-local JSON and evidence files | JSON state and event records |
| approval | user confirmation before action | approved Blueprint record |
| isolation | workspace/sandbox/permission scope | interface boundary only; not a security sandbox |
| verification | commands, inspections, read-back, human gates | callables and manifest checks |

## Honest capability rule

Do not label the Python reference runtime a sandbox or concurrent scheduler. Do not label a Codex Skill a provider-neutral executable. State precisely which boundary is conceptual and which is technically enforced.

## Future adapters

Claude Code, OpenAI Agents SDK, LangGraph, CrewAI, or other runtimes require their own implementation, contract tests, and documentation before being advertised as supported.

