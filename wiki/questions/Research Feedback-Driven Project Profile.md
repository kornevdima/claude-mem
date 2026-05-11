---
type: synthesis
title: "Research: Feedback-Driven Project Profile"
created: 2026-05-09
updated: 2026-05-09
tags:
  - research
  - synthesis
  - project-profile
  - feedback-loop
status: developing
related:
  - "[[Project Profile]]"
  - "[[Feedback Loop for Project Profile]]"
  - "[[Rule Generation from Chat]]"
  - "[[Generator-Evaluator Pattern]]"
  - "[[Research Pre-computed Context for Coding Agents]]"
  - "[[cursor-generate-rules]]"
  - "[[aider-conventions]]"
  - "[[reflexion-paper]]"
  - "[[anthropic-harness-design]]"
sources:
  - "[[cursor-generate-rules]]"
  - "[[aider-conventions]]"
  - "[[reflexion-paper]]"
  - "[[anthropic-harness-design]]"
---

# Research: Feedback-Driven Project Profile

Round-2 research run on **2026-05-09**. Scope: how should a `/project-profile` skill capture engineer feedback and update AGENTS.md or related files? Builds on the prior synthesis at [[Research Pre-computed Context for Coding Agents]].

## Overview

Two production patterns exist for "engineer feedback becomes rule": Cursor's `/Generate Cursor Rules` (manual + retrospective + agent participation) and Aider's CONVENTIONS.md (strictly manual, no feedback loop). The academic foundation is Reflexion (Shinn et al., 2023), which formalizes verbal-feedback Actor/Evaluator/Self-Reflection. Anthropic's harness-design article confirms in production that **separating generator from evaluator is "a strong lever"** against the leniency bias of self-evaluation. Pruning, conflict resolution, and overfitting are unsolved in published systems — we design those ourselves.

## Key Findings

### Production patterns

1. **Cursor's `/Generate Cursor Rules`** (v0.49, April 2025) is the closest reference implementation. Manual + retrospective trigger; output is a `.mdc` file in `.cursor/rules/`; same format as hand-written rules; best practice "1 concept per rule, under 50-80 lines, be specific." (Source: [[cursor-generate-rules]])
2. **Aider's CONVENTIONS.md** is the null-hypothesis baseline. Strictly human-authored, no auto-update, no feedback loop. Sidesteps every drift / bias / trust problem by removing the loop entirely. (Source: [[aider-conventions]])

### Academic foundation

3. **Reflexion (Shinn et al., 2023)** is the canonical verbal-reinforcement paper. Three-component Actor / Evaluator / Self-Reflection architecture. Verbal feedback (textual) accumulates in episodic memory across trials. Validated 91% pass@1 on HumanEval vs 80% GPT-4 baseline. (Source: [[reflexion-paper]])

### Production trust-boundary

4. **Generator-Evaluator separation is "a strong lever"** against self-grading leniency, per Anthropic's harness-design article. Self-evaluation is biased; the same agent grading itself is unreliable. (Source: [[anthropic-harness-design]])
5. **Multi-agent decomposition** (planner / generator / evaluator) is recommended for long-running agent applications. (Source: [[anthropic-harness-design]])

### What's NOT solved by literature

6. **Pruning / monotonic growth.** No published system retires stale rules automatically. Cursor implicitly limits via "1 concept per file, 50-80 lines" but doesn't prune.
7. **Conflict resolution between rules.** Not addressed.
8. **Overfitting from one-shot feedback.** A rule derived from one chat may overgeneralize. No published mitigation beyond "use manual retrospective trigger."
9. **Confirmation-bias loop.** Same-agent participation in writing rules about its own behavior shows leniency. Mitigation is the generator-evaluator split.
10. **Self-modification trust boundary.** Most production systems use "human gate" (PR review of rule files); no autonomous mode is well-tested.

## Key Entities

- **Cursor (Anysphere)** — shipped the closest existing feature (Generate Cursor Rules)
- **Aider (Paul Gauthier)** — chose the conservative no-feedback-loop alternative
- **Noah Shinn et al.** — Reflexion paper authors; canonical academic reference
- **Anthropic** — production guidance on generator-evaluator separation

## Key Concepts

- [[Rule Generation from Chat]] — the pattern of converting validated chat behavior to persistent rules
- [[Generator-Evaluator Pattern]] — the trust-boundary architecture
- [[Feedback Loop for Project Profile]] — the design synthesis applying both to claude-mem's planned skill

## Contradictions

- **Cursor (auto-edit-allowed) vs Aider (strict-human-authored).** Both are validated production approaches with different trade-offs. The right answer depends on the team's tolerance for rule churn vs. friction. **Resolution**: hybrid — use Cursor's pattern for the proposal step, Aider's strict-human-authorship for the commit step (i.e., agent drafts, human always approves).
- **Reflexion's "automatic verbal feedback" vs Anthropic's "agents have leniency self-grading."** Reflexion uses self-reflection within the agent; Anthropic warns against self-grading. **Resolution**: Reflexion's Self-Reflection role can be a separate model from the Actor, addressing the leniency bias. They're consistent if you implement Reflexion with role-separation.

## Open Questions

These didn't get answered and shape the design space:

1. **Pruning UX.** When and how often do engineers actually run a `/prune-rules` skill? If never, pruning has to be triggered by some signal (rule count > N, or rule age > X months).
2. **Evaluator quality.** A weak evaluator passes bad rules; a strict one rejects everything. What's the right calibration? Probably needs to be configurable.
3. **Multi-author conflict surfacing.** What's the UX when Engineer A writes a rule that contradicts Engineer B's? PR-review-style? Slack notification? Just record both and let humans sort it out?
4. **Cross-skill consistency.** If `/project-profile` writes AGENTS.md and the wiki layer also describes conventions, how do they stay in sync without duplication?
5. **Rule discoverability.** How does an engineer know what rules are already captured before they trigger `/capture-rule` and propose a duplicate?
6. **AGENTS.md vs separate rule files.** Cursor splits rules into many small `.mdc` files. AGENTS.md spec is monolithic. Hybrid: rules go to small files, AGENTS.md links to them.
7. **Token budget for the evaluator.** It needs to read all existing rules to detect conflict, which scales with rule count. At what point does the evaluator pass become expensive?
8. **Failure handling.** What happens when the evaluator agent itself errors or times out? Fall back to human-only review?

## Implications for `/project-profile` Design

Recorded in detail at [[Feedback Loop for Project Profile]]. Summary:

1. **Trigger**: manual + retrospective. Command name like `/capture-rule`. Engineer-initiated only.
2. **Architecture**: three roles — Generator (skill), Evaluator (separate subagent), Human gate (engineer reviews diff).
3. **Output format**: one rule per file, capped at 80 lines, scoped explicitly. Filed under `.agents/rules/` or equivalent.
4. **Pruning**: separate `/prune-rules` skill, never automatic, always engineer-confirmed.
5. **Conflict handling**: evaluator detects, surfaces both rules to engineer, engineer decides.
6. **Trust boundary**: human gate is mandatory; nothing writes without engineer accept.
7. **No background capture, no continuous monitoring** — copies Cursor's lesson that engineer judgment beats agent judgment for "is this rule worth saving."

## Sources

- [[cursor-generate-rules]] — Cursor v0.49 changelog, April 2025 (high confidence, primary)
- [[aider-conventions]] — Aider docs (high confidence, primary)
- [[reflexion-paper]] — Shinn et al., 2023 (high confidence, foundational academic)
- [[anthropic-harness-design]] — Anthropic Engineering, 2026 (high confidence, vendor authority)

## Research Metadata

- Round: 1
- Searches: 4
- Fetches: 5 (1 redirect failure, partially recovered from search summary)
- Sources cited: 4 primary
- Pages created this session: 8 (4 sources, 3 concepts, 1 synthesis)
- Date: 2026-05-09
- Builds on: [[Research Pre-computed Context for Coding Agents]]
