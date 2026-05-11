---
type: source
title: "Harness Design for Long-Running Application Development (Anthropic)"
source_type: vendor-engineering-blog
author: "Anthropic Engineering"
date_published: 2026
url: "https://www.anthropic.com/engineering/harness-design-long-running-apps"
created: 2026-05-09
updated: 2026-05-09
confidence: high
tags:
  - source
  - anthropic
  - harness-design
  - generator-evaluator
status: current
related:
  - "[[Generator-Evaluator Pattern]]"
  - "[[Feedback Loop for Project Profile]]"
  - "[[Context Engineering for Coding Agents]]"
key_claims:
  - "Generator-evaluator separation is 'a strong lever' against self-grading leniency"
  - "Agents exhibit leniency when grading their own outputs"
  - "Context resets with structured handoff outperform pure compaction for long runs"
  - "Multi-agent decomposition: planner expands spec, generator works in sprints, evaluator grades"
---

# Source: Harness Design for Long-Running Application Development (Anthropic)

**Author**: Anthropic Engineering
**URL**: https://www.anthropic.com/engineering/harness-design-long-running-apps

## Summary

Anthropic's published lessons on harness design for agents that run for long stretches building applications. Most of the content is about generator-evaluator architectures, context resets, and multi-agent decomposition. Most directly relevant to our design: the **strong recommendation to separate the agent doing the work from the agent judging it**.

## Generator-Evaluator separation

> "Self-evaluation problems: Agents exhibit 'leniency' when grading their own work. Separating generator from evaluator is 'a strong lever' to address poor judgment."

This is the load-bearing finding for our `/project-profile` design. The skill that **proposes** updates to AGENTS.md based on chat feedback should not be the same agent that **uses** AGENTS.md during work. Otherwise you get the leniency bias: the agent rationalizes that its own behavior was correct and writes self-favorable rules.

## Multi-agent pattern

Three roles in Anthropic's recommended pattern:

1. **Planner** — expands a high-level spec into detailed requirements.
2. **Generator** — produces output in sprints (or continuously with newer models).
3. **Evaluator** — tests outputs and provides criteria-based feedback.

This is the same Actor/Evaluator/Self-Reflection split as Reflexion ([[reflexion-paper]]), confirmed in production at Anthropic.

## Context management for long runs

- Compaction alone "proved insufficient for Claude Sonnet 4.5"; Opus 4.6 improved.
- "Context resets — clearing the context window entirely and starting a fresh agent, combined with a structured handoff that carries the previous agent's state — solves context anxiety."
- Structured artifacts carry state between sessions.

The implication for `/project-profile`: AGENTS.md is exactly the kind of "structured artifact carrying state" that survives context resets. The skill should be designed to produce updates that are valuable across many fresh sessions, not just within one.

## Evaluator tuning

- "Evaluator tuning requires several iterations to align with desired standards."

For our design: the evaluator-equivalent (the human reviewing whether feedback should become a rule) doesn't get it right first time. Need an iterative review/edit loop.

## What this contributes

- **Generator-evaluator separation is the trust-boundary pattern.** Direct guidance for our design.
- The **multi-agent decomposition** matches what we'd want: one agent observes the chat, a separate agent (or the human) judges whether to crystallize feedback into a rule.
- **AGENTS.md as durable state** that survives context resets is validated as a useful pattern.

## What's NOT addressed

- Self-modifying context / instructions specifically.
- Trust boundaries for agent autonomy when editing its own rules.
- Mechanisms for systematic human feedback incorporation.
- Rule-accumulation / drift mitigation over time.

These remain unsolved in the literature. We design them.

## Connections

- [[Generator-Evaluator Pattern]] — concept page
- [[Feedback Loop for Project Profile]] — design synthesis
- [[reflexion-paper]] — academic foundation for the same architecture
- [[anthropic-context-engineering]] — companion source
