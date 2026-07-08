---
type: concept
title: "Structured Handoff"
complexity: beginner
domain: ai-agents
aliases:
  - "Agent Handoff"
  - "Handoff Summary"
created: 2026-07-03
updated: 2026-07-03
tags:
  - concept
  - multi-agent
  - context-engineering
  - handoff
status: current
related:
  - "[[Context Engineering for Coding Agents]]"
  - "[[Validation Contract]]"
  - "[[Multi-Agent Communication Taxonomy]]"
sources:
  - "[[yt-alvoeiro-multi-agent-architecture]]"
  - "[[anthropic-harness-design]]"
---

# Structured Handoff

A mandatory, schema-shaped report an agent produces when finishing a unit of work, so the next agent (or the orchestrator) inherits state without inheriting context. Two independent production sources now converge on it: [[anthropic-harness-design]] ("context resets combined with a structured handoff that carries the previous agent's state") and [[Factory]]'s missions ([[yt-alvoeiro-multi-agent-architecture]]).

## Why

Long-running systems can't rely on agents "remembering what happened" — context degrades, and fresh-context workers are deliberately spun up with no baggage. Coherence must therefore live in written artifacts, "not by hoping that agents remember what happened but by forcing them to write it down."

## The missions handoff schema

When a worker finishes a feature, it fills out:

- **What was completed**
- **What was left undone**
- **Commands run** during the agent loop, **with their exit codes**
- **Issues discovered**
- **Procedure compliance** — did it abide by the procedures the orchestrator defined for this worker?

The orchestrator reviews handoffs at milestone boundaries (the negotiation step of the [[Multi-Agent Communication Taxonomy]]): corrective work gets scoped as follow-up features, and — key enforcement detail — **progress is blocked while handoff issues are unaddressed**. This is how a 16-day mission "pulls itself back on track" (self-heals).

## Relation to claude-mem ADLC

ADLC workers (feature-builder, feature-tester, feature-verifier, ba-suite/architecture subagents) each return "a short structured report," and this vault's own wiki-ingest subagents return a fixed summary block. Missing relative to missions: the **commands-run + exit-codes** field (verifiable evidence vs. self-description), the explicit **left-undone** field, the **procedure-compliance** attestation, and the **progress-blocking** rule when a handoff reports unresolved issues.

## Connections

- [[Context Engineering for Coding Agents]] — handoffs are the "structured note-taking" pattern applied at agent boundaries
- [[Validation Contract]] — handoffs report against it; validators check it
- [[anthropic-harness-design]] — independent confirmation of reset-plus-handoff over compaction
- [[yt-alvoeiro-multi-agent-architecture]] — the richest published field schema
