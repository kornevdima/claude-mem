---
type: concept
title: "Generator-Evaluator Pattern"
complexity: intermediate
domain: ai-agents
aliases:
  - "Actor-Critic"
  - "Generator-Critic"
  - "Two-Agent Pattern"
created: 2026-05-09
updated: 2026-07-03
tags:
  - concept
  - pattern
  - generator-evaluator
  - trust-boundary
status: current
related:
  - "[[Rule Generation from Chat]]"
  - "[[Feedback Loop for Project Profile]]"
  - "[[anthropic-harness-design]]"
  - "[[reflexion-paper]]"
sources:
  - "[[anthropic-harness-design]]"
  - "[[reflexion-paper]]"
  - "[[campbell-after-ai-hype]]"
  - "[[yt-alvoeiro-multi-agent-architecture]]"
---

# Generator-Evaluator Pattern

The architectural pattern of separating the agent that **produces** an output from the agent that **judges** it. Often combined with a third role (planner, self-reflection, or human) that closes the loop. The dominant trust-boundary pattern in agentic systems as of 2026.

## Why it exists

Self-evaluation is biased. From [[anthropic-harness-design]]:

> "Agents exhibit 'leniency' when grading their own work. Separating generator from evaluator is 'a strong lever' to address poor judgment."

Asking the same agent "did you do a good job?" is unreliable because the agent has implicit incentives to validate its own reasoning. Splitting the role into two agents (or one agent and a human) gives independent judgment.

## The pattern

Three roles, often:

1. **Generator** — produces output (code, decision, rule, response).
2. **Evaluator** — scores or critiques the output against criteria.
3. **Reflector / Planner / Human** — closes the loop by deciding what to do with the evaluation (retry, accept, store as lesson).

[[reflexion-paper]] is the canonical academic formulation: Actor / Evaluator / Self-Reflection.

## Variants

- **Two-agent (no human)**: Generator and Evaluator are both LLM agents. Cheap but evaluator may share blind spots.
- **Generator + human evaluator**: Standard PR-review workflow. Highest trust but slowest.
- **Generator + LLM evaluator + human gate**: Hybrid. LLM evaluator filters; human approves final updates. Common in production systems.

## Where it applies in our design

For the planned `/project-profile` skill:

- **Generator role**: the skill that drafts a proposed AGENTS.md rule based on chat feedback.
- **Evaluator role**: a separate agent that judges whether the proposed rule is well-formed, non-conflicting with existing rules, and likely to generalize.
- **Human gate**: the engineer reviews the diff before commit.

This three-step loop avoids the leniency problem and gives a clear trust boundary: nothing lands in `AGENTS.md` without explicit human consent.

## Why not just one agent + human

Theoretically, a single LLM proposing a rule and a human reviewing it would suffice. But:

- The human gets fatigued by mediocre proposals.
- An LLM evaluator pre-filters obvious issues (rule conflicts, vague phrasing, exceeded length) so the human only reviews proposals that have already passed quality bar.
- Cost: an evaluator pass is cheap compared to the human attention it saves.

## Performance evidence

- [[reflexion-paper]] showed +11 percentage points on HumanEval (91% vs 80% GPT-4 baseline) when using verbal-feedback Actor/Evaluator/Self-Reflection vs. baseline.
- [[anthropic-harness-design]] reports the pattern as "a strong lever" without specific numbers.

## Production form: Factory missions (2026)

[[Factory]]'s missions system ([[yt-alvoeiro-multi-agent-architecture]]) is the strongest production case study to date, running the pattern inside autonomous delivery missions of up to 16 days:

- **"Creator-verifier"** is one of five primitives in its [[Multi-Agent Communication Taxonomy]]; the rationale matches Anthropic's leniency finding: the implementer "has cost bias — wants that code to work. A fresh agent with fresh context is way more likely to find issues."
- **Validators never see the code before judging** — "validation is adversarial by design." Two validator types: scrutiny (tests/type/lint + per-feature code-review agents) and user-testing (drives the live app via computer use).
- **Evaluation criteria are fixed before generation**: a [[Validation Contract]] written at planning time, so the evaluator judges against implementation-independent assertions — a direct mitigation for evaluator drift (below).
- **Cross-provider evaluators**: validation "might use a different model provider entirely to make sure that it's not biased by the same training data" — a concrete mitigation for the same-LLM blind-spot failure mode (below).

## Failure modes

- **Evaluator drift**: if the evaluator's criteria themselves are poorly defined or change, it can mis-judge.
- **Same-LLM blind spots**: Generator and Evaluator running on the same base model may share systematic errors. Mitigation: different model families or strong evaluator-specific prompting.
  - **Public failure case** ([[campbell-after-ai-hype]], NDC 2026): GPT-5's literary mode was reportedly trained "by exercising against another GPT, and the fact that the sentences made no sense didn't bother GPT at all — it gave it all green lights. Then humans used it and went, 'Wow, this isn't English.'" A same-family LLM as sole evaluator rubber-stamped nonsense at production scale; grounded evaluation (humans, runtime observation) caught it immediately.
- **Evaluator latency**: adds tokens and time. For interactive use, the evaluator may need to be small/fast.

## Connections

- [[Rule Generation from Chat]] — applies this pattern to convention capture
- [[Feedback Loop for Project Profile]] — design synthesis
- [[anthropic-harness-design]] — Anthropic's recommendation for this pattern
- [[reflexion-paper]] — academic foundation
- [[yt-alvoeiro-multi-agent-architecture]] — Factory missions, production-scale creator-verifier
- [[Validation Contract]] — pre-written criteria the evaluator judges against
