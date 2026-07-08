---
type: source
title: "The Multi-Agent Architecture That Actually Ships (Luke Alvoeiro, Factory)"
source_type: conference-talk
author: "Luke Alvoeiro"
venue: "AI Engineer"
date_published: 2026-05-06
url: "https://youtu.be/ow1we5PzK-o"
created: 2026-07-03
updated: 2026-07-03
confidence: medium
tags:
  - source
  - multi-agent
  - factory
  - validation
  - orchestration
status: current
related:
  - "[[Multi-Agent Communication Taxonomy]]"
  - "[[Validation Contract]]"
  - "[[Structured Handoff]]"
  - "[[Generator-Evaluator Pattern]]"
  - "[[Context Engineering for Coding Agents]]"
  - "[[Factory]]"
  - "[[Luke Alvoeiro]]"
key_claims:
  - "The bottleneck in software engineering is human attention, not model intelligence"
  - "Five multi-agent primitives: delegation, creator-verifier, direct communication, negotiation, broadcast"
  - "A validation contract written during planning, before any code, defines correctness independently of implementation"
  - "Tests written after implementation don't catch bugs — they confirm decisions"
  - "Naive parallel workers conflict; serial features with parallelized read-only ops drop error rates dramatically"
  - "Validators never see the code before judging — validation is adversarial by design"
  - "Longest production mission: 16 days; believed capable of 30"
---

# Source: The Multi-Agent Architecture That Actually Ships

**Speaker**: [[Luke Alvoeiro]] (leads core agent harness at [[Factory]]; previously started Goose at Block)
**Venue**: AI Engineer conference, 2026-05-06 | Auto-transcript from `.raw/yt-alvoeiro-multi-agent-architecture.md`

## Summary

Architecture talk on Factory's **missions** system — long-running (hours to 16+ days) autonomous software-delivery runs. Core thesis: the bottleneck is no longer model intelligence but **human attention**; the fix is a structured agent ecosystem where "a human decides what to build and a system figures out how to do so." The talk proposes a five-primitive taxonomy of multi-agent communication, then shows how missions composes four of them into a three-role architecture with contract-driven, adversarial validation.

## The five-primitive taxonomy

See [[Multi-Agent Communication Taxonomy]]: **delegation**, **creator-verifier**, **direct communication**, **negotiation**, **broadcast**. Missions uses all but direct communication (which "is hard to get right — state fragments across conversations without a coordinator").

## The missions architecture

Three roles, communicating through structured handoffs and shared state:

1. **Orchestrator** — planning. Scopes the goal through conversation, produces a plan of features, milestones, and a [[Validation Contract]] (what "done" means, defined before any code).
2. **Workers** — implementation. Each worker gets **clean context** ("no accumulated baggage, no degraded attention"), reads its spec, implements, commits via Git so the next worker inherits a working codebase.
3. **Validators** — verification. Two kinds run after each milestone:
   - **Scrutiny validator**: test suite, type check, lint, plus dedicated code-review agents per completed feature.
   - **User-testing validator**: acts like a QA engineer — spawns the application, drives it via computer use, fills forms, clicks buttons, checks functional flows holistically. Most of a mission's wall-clock time is spent here, waiting on real-world execution rather than generating tokens.

Neither validator has seen the code before. "They're not invested in the implementation — validation is adversarial by design." This is the [[Generator-Evaluator Pattern]] at production scale.

## Validation philosophy

> "Tests written after implementation don't catch bugs. They confirm decisions."

Hence the [[Validation Contract]]: written during planning, hundreds of assertions for a complex project, each feature assigned assertions it must satisfy, and the sum of all features must cover every assertion. Behavior is validated end-to-end, not just statically.

## Self-healing via structured handoffs

Workers don't just report "done" — they fill a [[Structured Handoff]]: what was completed, what was left undone, commands run + exit codes, issues discovered, and whether orchestrator-defined procedures were followed. Errors get caught at milestone boundaries; corrective work is scoped as follow-up features ("validation never succeeds on the first go — we almost always have to create follow-up features"). Progress is **blocked** while handoff issues are unaddressed.

## Execution strategy: serial with targeted parallelism

Naive 10-agent parallelism failed: "agents conflict, step on each other's changes, duplicate work, make inconsistent architectural decisions" — coordination overhead eats the speed gains. Missions runs **features serially** (one worker or validator active at a time) and parallelizes only **read-only operations** (codebase search, API research, code review). "Seems slower on paper, but the error rate drops dramatically, and correctness compounds" over multi-day runs.

## Right model in each role ("droid whispering")

Planning wants slow careful reasoning; implementation wants fast code fluency; validation wants precise instruction following. No single model/provider is best at all three. Validation may deliberately use a **different provider** so it isn't biased by the same training data. Model-agnostic structure also compensates downward: validation contracts + milestone checkpoints let missions succeed even with open-weight models.

## Bitter-lesson-proofing

Almost all orchestration logic lives in **prompts and skills (~700 lines of text)**, not a hard-coded state machine; four sentences can alter execution strategy dramatically. Deterministic logic is a thin bookkeeping layer (running validation, blocking progress on unresolved handoffs). Uses primitives models already know: AGENTS.md, skills. The system is designed to get better with every model release.

## Production numbers (Slack-clone example)

- 60% of time and 60% of tokens on implementation.
- Validation never passes on the first attempt; follow-up features are the norm.
- Final codebase: ~50% of lines are tests; ~90% coverage.
- Heavy prompt caching to offset long-run cost.
- Longest mission: **16 days**; 30 believed feasible.
- Claimed economics: a team of five goes from ~10 concurrent work streams to ~30.

## Operator UX

**Mission control**: a dedicated async view (not chat) showing progress %, budget burned, what the active worker is doing, and handoff/validator summaries — the human plugs in as a project manager.

## Relevance to claude-mem ADLC

The claude-mem ADLC harness (feature-builder/tester/reviewer/verifier + orchestrating session) already implements delegation, creator-verifier separation, per-feature verification contracts, and prompt-defined orchestration. Gaps this talk highlights: assertion-coverage accounting across features, exit-code-bearing structured handoffs with progress blocking, milestone-level holistic validation, automatic follow-up-feature scoping, per-role model assignment, and budget/progress visibility.

## Connections

- [[Multi-Agent Communication Taxonomy]] — the five primitives
- [[Validation Contract]] — the load-bearing artifact
- [[Structured Handoff]] — the connective tissue
- [[Generator-Evaluator Pattern]] — creator-verifier is its production form here
- [[Context Engineering for Coding Agents]] — clean-context workers + serial execution as context strategy
- [[anthropic-harness-design]] — independent convergence on the same three-role split and context-reset-with-handoff pattern
