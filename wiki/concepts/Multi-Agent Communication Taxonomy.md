---
type: concept
title: "Multi-Agent Communication Taxonomy"
complexity: intermediate
domain: ai-agents
aliases:
  - "Five Multi-Agent Primitives"
  - "Multi-Agent Frameworks Taxonomy"
created: 2026-07-03
updated: 2026-07-03
tags:
  - concept
  - multi-agent
  - orchestration
  - taxonomy
status: current
related:
  - "[[Generator-Evaluator Pattern]]"
  - "[[Validation Contract]]"
  - "[[Structured Handoff]]"
  - "[[Factory]]"
sources:
  - "[[yt-alvoeiro-multi-agent-architecture]]"
---

# Multi-Agent Communication Taxonomy

A five-primitive taxonomy for multi-agent system design, proposed by [[Luke Alvoeiro]] ([[Factory]]) to cut through the "mess" of competing frameworks and terminology. The claim: every multi-agent architecture is a composition of these five communication patterns, and long-running systems succeed by picking the right subset — not by using all of them.

## The five primitives

| Primitive | Shape | Notes |
|---|---|---|
| **Delegation** | Parent spawns child, gets a response back | Simplest form; sub-agents in coding tools are the most common example. What most people implement first. |
| **Creator-verifier** | One agent builds, a separate agent checks | Separation of concerns: the implementer has "cost bias — wants that code to work." A fresh agent with fresh context finds issues far more reliably. Same reason humans do code review. See [[Generator-Evaluator Pattern]]. |
| **Direct communication** | Agents DM each other, no central coordinator | "Hard to get right — state fragments across conversations without that coordinator and there's no single source of truth." |
| **Negotiation** | Agents communicate over a shared resource (same API, same code region) | Need not be adversarial; best case is net-positive-sum trading (win-win interactions). |
| **Broadcast** | One agent sends information to many | Status updates, new context that applies to everyone, shared constraints. "Less flashy, but critical for maintaining coherence over long-running tasks." |

## How Factory's missions composes them

Missions uses four of the five (skipping direct communication):

- **Delegation** — orchestrator spawns workers; workers spawn research sub-agents.
- **Creator-verifier** — implementation and validation are always separate agents with separate context; validators never see the code before judging.
- **Broadcast** — shared mission state that every agent references.
- **Negotiation** — at milestone boundaries: orchestrator judges handoff summaries and decides on follow-up features or rescoping.

## Mapping to claude-mem ADLC

The claude-mem harness already uses **delegation** (orchestrating session dispatches feature-builder/tester/reviewer/verifier, ba-suite and architecture subagents) and **creator-verifier** (feature-reviewer and feature-verifier have fresh context and never fix, only judge). **Broadcast** exists in weak form as shared wiki state (hot.md, specs). **Negotiation** (milestone-boundary rescoping into follow-up features) is the least developed primitive here — verifier failures log-and-stop rather than trigger scoped corrective work.

## Connections

- [[Generator-Evaluator Pattern]] — creator-verifier is the same trust boundary
- [[Structured Handoff]] — the payload format that makes delegation and negotiation reliable
- [[Validation Contract]] — the shared artifact broadcast defines "done" against
- [[yt-alvoeiro-multi-agent-architecture]] — source
