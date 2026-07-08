---
type: concept
title: "Domain-Specific Agents"
complexity: intermediate
domain: ai-agents
aliases:
  - "DSA"
  - "Composition over Inheritance for Agents"
created: 2026-07-03
updated: 2026-07-03
confidence: medium
tags:
  - concept
  - agents
  - multi-agent
  - context-engineering
status: developing
related:
  - "[[Context Engineering for Coding Agents]]"
  - "[[Context Rot]]"
  - "[[Generator-Evaluator Pattern]]"
  - "[[Recursive Language Models]]"
sources:
  - "[[yt-schroeder-domain-specific-agents]]"
---

# Domain-Specific Agents

Small, *complete* agents scoped to one domain — own system prompt written for that domain, own minimal precise toolset, own message history, own agentic loop — composed under a coordinator agent that talks to them in plain English. Framed by [[Justin Schroeder]] as **composition over inheritance** applied to agents. (Source: [[yt-schroeder-domain-specific-agents]])

## Inheritance vs Composition

The default agent stack — model → system prompt → tools → skills → MCP → messages — is almost all *context*. Adding skills and MCP servers to one large general-purpose agent is **inheritance**: bolting attributes onto one object. It works, until it doesn't: 5 skills fine, 100 or 1,000 skills produce diminishing-to-negative returns (this is [[Context Rot]] restated in OO vocabulary).

**Composition** instead: a Figma agent that knows only Figma, a Gmail agent that knows only Gmail, each a full agent, coordinated from above. The coordinator passes only the ask ("get that last email from Debbie") — the sub-agent's total context is its system prompt + tools + that one message.

## Claimed properties

| Property | Claim (unverified vendor numbers) |
|---|---|
| Token efficiency | regularly >80% per task vs. one large agent |
| Small-model viability | narrow task + minimal context lets ~137x-cheaper models execute faithfully; non-LLM models (diffusion, image) usable as tools |
| Security | capability limits by construction — the agent *can only* do pre-approved things, vs. permission-bypassing on omnipotent coding agents |
| Scaling | each agent is its own execution environment: parallelizable, cloud-schedulable, no co-location |

## Ideal agent anatomy (Schroeder's sketch)

- **Tools, three kinds**: *functions* (execute code), *prompts* (sub-prompts calling another model — e.g. an image model under a text model), and *full agents* (recursive sub-agents as tools).
- **Hooks**: inject artificial messages/tool-calls into history (e.g. current time) or fire side effects.
- **Agent rules**: turn/step budgets, per-tool-call validation requirements, stop conditions.
- **Primitives baked in**: a sandboxed file system and sandboxed code execution per agent.

## Relation to existing wiki concepts

- [[Context Engineering for Coding Agents]] already documents sub-agent architectures returning 1-2K-token summaries; DSA generalizes that from an *economy* measure to the *primary architecture*.
- [[Recursive Language Models]] reach the same destination from the inference side: keep the working context tiny, push bulk out-of-context. DSA does it by agent decomposition; RLM by REPL recursion.
- [[Generator-Evaluator Pattern]] is a two-agent special case of composition (trust boundary rather than domain boundary).

## Implications for claude-mem

The ADLC harness already composes domain-scoped workers (feature-builder/tester/reviewer/verifier, ba-suite-subagent, architecture-subagent, doc-writer) under a dispatching main thread — the pattern is validated, not new here. Gaps the talk highlights (candidate improvements, tracked in the [[yt-schroeder-domain-specific-agents]] ingest report): per-agent small-model tiering beyond a flat `model: sonnet`, minimal per-agent tool allowlists instead of "All tools", explicit agent rules (turn/step budgets, stop conditions), per-step telemetry, and recursive sub-agent depth.

> [!note] Verification status
> The efficiency (>80%), cost (137x), and 2026 token-price-reversal (+29% IQ-adjusted) figures are single-source claims from a stealth vendor building this product. Treat as directional until independently sourced.
