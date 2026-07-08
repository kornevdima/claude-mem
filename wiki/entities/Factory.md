---
type: entity
entity_type: organization
title: "Factory"
created: 2026-07-03
updated: 2026-07-03
tags:
  - entity
  - organization
  - multi-agent
  - coding-agents
status: current
related:
  - "[[Luke Alvoeiro]]"
  - "[[Multi-Agent Communication Taxonomy]]"
  - "[[Validation Contract]]"
sources:
  - "[[yt-alvoeiro-multi-agent-architecture]]"
---

# Factory

AI dev-tools company whose stated mission is "to bring autonomy to the entire software development life cycle." [[Luke Alvoeiro]] leads its core agent harness. Its agents are called **droids** (product entry point: "Open Droid, try running /missions").

## Missions

Factory's long-running multi-agent delivery system ([[yt-alvoeiro-multi-agent-architecture]]):

- Three roles: **orchestrator** (planning + [[Validation Contract]]), **workers** (clean-context implementation, commit via Git), **validators** (scrutiny + user-testing, adversarial, fresh context).
- Composes four primitives of the [[Multi-Agent Communication Taxonomy]]: delegation, creator-verifier, broadcast, negotiation.
- Serial feature execution with parallelized read-only operations; [[Structured Handoff]]s between agents; progress blocked on unresolved handoff issues.
- Orchestration logic lives in ~700 lines of prompts/skills, not a state machine ("bitter-lesson-proofing"); model-agnostic with per-role model selection ("droid whispering").
- Longest production mission: 16 days. Enterprise uses: overnight prototypes, internal tools, large refactors/migrations, ML research, codebase modernization.
- **Mission control**: dedicated async UI showing progress, budget burn, active worker status, and handoff summaries.

## Connections

- [[Luke Alvoeiro]] — harness lead, talk speaker
- [[Validation Contract]], [[Structured Handoff]] — the system's two load-bearing artifacts
