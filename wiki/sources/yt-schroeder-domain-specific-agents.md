---
type: source
title: "The Future Is Domain-Specific Agents (Justin Schroeder, AI Engineer)"
source_type: conference-talk-transcript
author: "Justin Schroeder (StandardAgents)"
date_published: 2026-06-29
url: "https://youtu.be/spNAUEgq_A8"
raw_file: ".raw/yt-schroeder-domain-specific-agents.md"
created: 2026-07-03
updated: 2026-07-03
confidence: medium
tags:
  - source
  - youtube
  - agents
  - multi-agent
  - context-engineering
status: current
related:
  - "[[Domain-Specific Agents]]"
  - "[[Justin Schroeder]]"
  - "[[StandardAgents]]"
  - "[[Context Engineering for Coding Agents]]"
  - "[[Context Rot]]"
key_claims:
  - "Skills/MCP/system-prompt layering is inheritance; the alternative is composition — many small full agents under a coordinator, talking in plain English"
  - "Domain-specific agents show over 80% token efficiency per task vs. a general-purpose agent"
  - "Small models (DeepSeek V4 Flash, ~137x cheaper than Fable 5) become viable when each agent's task and context are narrowly scoped"
  - "MCP in practice is a de facto tool-distribution mechanism — only the tools column is broadly supported by clients"
  - "Token costs reversed trend in 2026: up 29% IQ-adjusted, up 76% raw, by mid-year"
  - "Every agent should have a sandboxed file system and sandboxed code execution as built-in primitives"
---

# Source: The Future Is Domain-Specific Agents

**Speaker**: Justin Schroeder ([[StandardAgents]], stealth) — also known for open-source work (Dmux, ArrowJS).
**Venue**: AI Engineer, published 2026-06-29. Auto-transcript; treat exact figures as speaker claims, not verified data.

## Core Argument

Everyone — real-estate agencies, insurance brokers, Fortune 500s — is trying to build custom agents because they want their data integrated into AI. But robust agents are hard (orchestration, provider abstractions, durable execution, validation, stop conditions), so most efforts die at the demo stage. The current fixes (MCP, skills) all work by **inflating the context layer** of one large general-purpose agent: system prompt + tools + skills + MCP + messages. Schroeder names this **inheritance** and argues for the classic alternative: **composition** — see [[Domain-Specific Agents]].

The composed architecture: many tiny, *complete* agents (own system prompt written for one domain, own precise minimal toolset, own message history, own agentic loop), coordinated by a parent agent, communicating in plain English. Analogy: Apollo 11 was not one guy with a ton of tools and documentation; it was teams of narrow experts.

## Key Claims

1. **Agent definition**: "deterministic software that harness the non-deterministic results produced by models in pursuit of some desired objective"; the agent/harness distinction is pedantic — conflate them.
2. **MCP reality check**: on the MCP site's client-support matrix, only the *tools* column is filled all the way down — MCP has become a de facto tool-distribution mechanism, little more yet.
3. **Skills reality check**: skills are markdown documentation; "there's lots of research out there that shows that if you use very many of these, it actually makes your agent substantially worse" (aligns with [[Context Rot]]).
4. **Token efficiency**: domain-specific agents regularly show **>80% token efficiency per task** because a coordinator sends only the ask ("get that last email from Debbie"), not the whole conversation.
5. **Small-model viability**: with narrow tasks + minimal context, a small model (DeepSeek V4 Flash, claimed ~137x cheaper per task than Fable 5) executes faithfully; you can also mix non-language models (image/diffusion) as tools.
6. **Security posture**: everyone is "bypassing permissions left and right" because a big coding agent *can* do anything. Small agents "can only do the things that are already explicitly approved for them to do" — capability limits by construction, not by permission dialog.
7. **Scaling**: each small agent is its own execution environment — parallelizable, cloud-schedulable in thousands of instances, no geographic co-location needed.
8. **Economics**: token cost decline *reversed* in 2026 — +29% IQ-adjusted, +76% raw by mid-year (StandardAgents tracks this). Also: "you can't put Fable in front of a customer" unless LTV is massive — customer-facing AI forces the efficiency question.
9. **Ideal agent anatomy**: model + system prompt + tools (three kinds: **functions**, **prompts** — sub-prompts calling another model, e.g. Nano Banana under GLM 5.2 — and **full agents**) + **hooks** (inject artificial messages, e.g. current time; fire side effects) + **agent rules** (turn/step budgets, validation requirements) + a **sandboxed file system** and **sandboxed code execution** as baked-in primitives.
10. **Recursion**: sub-agents can call sub-agents (coordinator → Salesforce → asset-generator; legal-team → GDPR agent → OSHA agent), each keeping a minimal context window.

## Prediction

Domain-specific agents "don't exist" publicly yet (mid-2026), but 2026 H2 = rapid uptick in domain-specific-agent frameworks (first sighting: Vercel's **Eve**, whose tagline literally says "domain-specific agent"); **2027 = the year of multi-agent orchestration**.

## Relevance to claude-mem

The ADLC harness (feature-builder / tester / reviewer / verifier, ba-suite-subagent, architecture-subagent) already *is* a composition of domain-scoped agents under a coordinator — validating the pattern. The talk's deltas (per-agent model tiering, minimal tool allowlists, agent rules/turn budgets, per-step telemetry) are candidate harness improvements; see [[Domain-Specific Agents]] § Implications for claude-mem.

## Caveats

- Speaker sells this vision (StandardAgents is a stealth company building exactly this); the >80% efficiency and 137x cost figures are unverified vendor claims.
- The "skills make agents worse" research is asserted, not cited.
- The 2026 token-price-reversal claim is from the speaker's own tracking site; needs an independent source before treating as fact.
