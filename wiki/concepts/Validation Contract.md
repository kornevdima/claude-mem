---
type: concept
title: "Validation Contract"
complexity: intermediate
domain: ai-agents
aliases:
  - "Verification Contract"
  - "Done Contract"
created: 2026-07-03
updated: 2026-07-03
tags:
  - concept
  - validation
  - multi-agent
  - testing
status: current
related:
  - "[[Generator-Evaluator Pattern]]"
  - "[[Multi-Agent Communication Taxonomy]]"
  - "[[Structured Handoff]]"
sources:
  - "[[yt-alvoeiro-multi-agent-architecture]]"
---

# Validation Contract

A definition of correctness **written during planning, before any code exists**, that an autonomous delivery system validates against for its entire run. Coined (as used here) by [[Factory]]'s missions system; presented by [[Luke Alvoeiro]] as the load-bearing artifact that lets agent runs last days without drifting.

## The problem it solves

The familiar failure mode of coding agents:

> "An agent builds a feature. It writes some tests. The tests pass. There's full coverage. But the tests were shaped by the code, not by what the code was attempting to actually do. Tests written after implementation don't catch bugs. They confirm decisions."

Any system that validates only against post-hoc tests will eventually drift, because the yardstick was manufactured by the thing being measured.

## The mechanism

- Written by the **orchestrator during planning**, alongside features and milestones — before implementation starts.
- Defines correctness **independently of implementation**.
- For a complex project: **hundreds of assertions**.
- Each feature is assigned one or more assertions it must satisfy; **the sum of all features must cover every assertion** (explicit coverage accounting).
- After each milestone, two validator types check against it:
  - **Scrutiny validator** — tests, type check, lint, plus per-feature code-review agents.
  - **User-testing validator** — spawns the live application and exercises it via computer use (forms, buttons, page renders, end-to-end flows). This is where most mission wall-clock time goes.
- Validators have **never seen the code** — validation is adversarial by design ([[Generator-Evaluator Pattern]]).
- Contract + milestone checkpoints also compensate for weaker models: missions "run very successfully even using open-weight models."

## Relation to claude-mem ADLC

The ADLC harness already has **per-feature verification contracts** (feature-verifier reads a contract; feature-tester derives e2e specs from it). What the missions version adds beyond that:

1. **Coverage accounting across the whole plan** — assertions ledgered so no feature ships without its assertions and no assertion is orphaned.
2. **Contract authored strictly before implementation** as a single planning-time artifact spanning all features/milestones.
3. **Milestone-level holistic validation** — the user-testing validator exercises cross-feature flows, not just the feature in isolation.
4. **Unit-test derivation from the contract** — the talk's critique applies to builder-written unit tests authored after the code.

## Connections

- [[Generator-Evaluator Pattern]] — the adversarial-validator side of the same coin
- [[Structured Handoff]] — carries per-feature results back against the contract
- [[Multi-Agent Communication Taxonomy]] — the contract is the broadcast "shared constraint"
- [[yt-alvoeiro-multi-agent-architecture]] — source
