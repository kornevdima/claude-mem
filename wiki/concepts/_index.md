---
type: meta
title: "Concepts Index"
updated: 2026-07-03
tags:
  - meta
  - index
  - concept
domain: knowledge-management
status: evergreen
related:
  - "[[index]]"
  - "[[Hot Cache]]"
  - "[[LLM Wiki Pattern]]"
  - "[[Compounding Knowledge]]"
---

# Concepts Index

Navigation: [[index]] | [[entities/_index|Entities]] | [[sources/_index|Sources]]

All concept pages — ideas, patterns, and frameworks extracted from sources.

---

## Knowledge Management

- [[LLM Wiki Pattern]] — the core architecture for persistent, compounding knowledge bases
- [[Hot Cache]] — ~500-word session context file, updated after every ingest
- [[Compounding Knowledge]] — why the wiki grows more valuable over time, unlike RAG

---

## AI Agents

- [[Domain-Specific Agents]] — composition over inheritance for agents: small complete agents under a coordinator, minimal per-agent context (Source: [[yt-schroeder-domain-specific-agents]])
- [[Multi-Agent Communication Taxonomy]] — five primitives: delegation, creator-verifier, direct communication, negotiation, broadcast (Source: [[yt-alvoeiro-multi-agent-architecture]])
- [[Validation Contract]] — correctness defined at planning time, before code; assertion coverage accounted across features; validated behaviorally (Source: [[yt-alvoeiro-multi-agent-architecture]])
- [[Structured Handoff]] — schema-shaped worker report (done / undone / commands + exit codes / issues / procedure compliance) that lets clean-context agents inherit state (Sources: [[yt-alvoeiro-multi-agent-architecture]], [[anthropic-harness-design]])

---

## Agent Workflow

- [[ADLC Field Review Findings]] — production two-wiki ADLC review: code-first inversion, handoff-seam costs (zero traceability, re-derivation), records-as-pages, duplication rates (~6–8% volume / 25–30% of the shared layer), delegation share as the efficiency lever (Source: field review, 2026-07-04)
- [[Grilling Session]] — alignment-first interview (one question at a time + recommended answer) until a shared design concept exists; precedes any plan/PRD (Source: [[yt-pocock-ai-coding-workflow]])
- [[Ralph Wiggum Loop]] — AFK implementation loop: fresh context per iteration over an issue backlog, sentinel-terminated, sandboxed; Sandcastle for the parallel version (Source: [[yt-pocock-ai-coding-workflow]])
- [[Vertical Slices for Agent Tasks]] — tracer-bullet issue decomposition; Kanban DAG of independently grabbable, all-layer slices enables parallel agents (Source: [[yt-pocock-ai-coding-workflow]])
- [[Deep Modules]] — Ousterhout's small-interface/big-functionality modules as agent enablement: feedback-loop quality is the ceiling on agent output (Source: [[yt-pocock-ai-coding-workflow]])

---

## Add new concepts here as they are extracted from sources.
