---
type: source
title: "Reflexion: Language Agents with Verbal Reinforcement Learning"
source_type: peer-reviewed-paper
author: "Noah Shinn, Federico Cassano, Edward Berman, Ashwin Gopinath, Karthik Narasimhan, Shunyu Yao"
date_published: 2023
url: "https://arxiv.org/abs/2303.11366"
created: 2026-05-09
updated: 2026-05-09
confidence: high
tags:
  - source
  - paper
  - reflexion
  - self-improvement
  - feedback-loop
status: current
related:
  - "[[Generator-Evaluator Pattern]]"
  - "[[Feedback Loop for Project Profile]]"
  - "[[Context Engineering for Coding Agents]]"
key_claims:
  - "Verbal feedback (textual, not weight updates) drives agent self-improvement"
  - "Three-component architecture: Actor, Evaluator, Self-Reflection"
  - "Reflective text accumulates in episodic memory across trials"
  - "Reflexion achieves 91% pass@1 on HumanEval vs 80% for GPT-4 baseline"
  - "Feedback can be scalar values or free-form language; external or internally simulated"
---

# Source: Reflexion (Shinn et al., 2023)

**Authors**: Noah Shinn, Federico Cassano, Edward Berman, Ashwin Gopinath, Karthik Narasimhan, Shunyu Yao
**Published**: 2023
**URL**: https://arxiv.org/abs/2303.11366

## Summary

The foundational academic paper on "verbal reinforcement" for LLM agents — using natural-language feedback (not weight updates) to improve agent behavior across trials. The three-component Actor / Evaluator / Self-Reflection architecture is the canonical reference for any feedback-driven self-improvement design, including the one we're sketching for `/project-profile`.

## Architecture

Three distinct models / roles:

1. **Actor** — generates text and actions to complete the task.
2. **Evaluator** — scores the Actor's output (binary pass/fail or scalar).
3. **Self-Reflection model** — converts the Evaluator's feedback into verbal reinforcement: a textual summary of what went wrong and how to do better next time.

The Self-Reflection output is stored in an **episodic memory buffer** and prepended to the Actor's context on subsequent trials.

## Why this matters for our design

- The **separation of Actor from Evaluator** is the trust boundary. The agent doing the work is not the agent judging it. Anthropic's harness-design article ([[anthropic-harness-design]]) confirms this — self-evaluation has "leniency" bias.
- The **verbal feedback channel** is the right shape for project-level rule generation: not numeric scores, not weight updates, but explicit textual rules the human (or a separate agent) can read and approve.
- The **episodic memory buffer** maps to AGENTS.md / .cursor/rules/ in our world: durable text that future agent runs read.

## Performance

- HumanEval coding benchmark: **91% pass@1** (vs 80% for GPT-4 baseline at the time of publication).
- Validated across sequential decision-making, coding, and language reasoning.

## What the paper does NOT address (relevant to our design)

The abstract and standard summaries do not detail:

- **Pruning**. How the episodic memory is bounded over time. (Open in the paper; an unsolved practical problem.)
- **Conflict resolution**. What happens when reflections from different trials disagree.
- **Overfitting to single instances**. Whether the agent generalizes the lesson correctly.
- **Failure modes**. When verbal reinforcement makes things worse.

These are the exact gaps we have to design around for `/project-profile`.

## What this contributes

- The Actor / Evaluator / Self-Reflection separation is the architectural pattern to copy.
- "Verbal reinforcement as text the next agent reads" validates the AGENTS.md-as-output approach.
- The unsolved problems in the paper (pruning, conflict, overfitting) are exactly the open questions we still have to design around.

## Connections

- [[Generator-Evaluator Pattern]] — broader design pattern this paper instantiates
- [[Feedback Loop for Project Profile]] — design that applies these ideas
- [[Context Engineering for Coding Agents]]
