---
type: concept
title: "Feedback Loop for Project Profile"
complexity: advanced
domain: claude-mem
aliases:
  - "/project-profile feedback design"
  - "Project Profile Update Skill"
created: 2026-05-09
updated: 2026-05-09
tags:
  - concept
  - design
  - feedback-loop
  - project-profile
status: developing
related:
  - "[[Project Profile]]"
  - "[[Rule Generation from Chat]]"
  - "[[Generator-Evaluator Pattern]]"
  - "[[AGENTS.md]]"
  - "[[Context Engineering for Coding Agents]]"
  - "[[Research Feedback-Driven Project Profile]]"
sources:
  - "[[cursor-generate-rules]]"
  - "[[aider-conventions]]"
  - "[[reflexion-paper]]"
  - "[[anthropic-harness-design]]"
  - "[[evaluating-agents-md-eth]]"
---

# Feedback Loop for Project Profile

Design synthesis for the feedback half of the planned `/project-profile` skill. Informed by the 2026-05-09 research pass on rule-generation-from-chat and generator-evaluator patterns.

## What we're designing

A skill the engineer runs after a chat to capture validated patterns into the project's AGENTS.md (or related file). The skill must:

- Have a low friction trigger.
- Produce well-formed, scoped, non-conflicting rules.
- Avoid monotonic growth and rule bloat.
- Maintain a trust boundary so nothing lands without human consent.
- Survive multi-author disagreement and convention drift over time.

## Architecture: three roles, one human gate

Apply the [[Generator-Evaluator Pattern]] explicitly:

```
Engineer corrects agent in chat → /capture-rule (or similar trigger)
   │
   ▼
[Generator agent] — drafts proposed rule from chat context
   │  produces: rule text, scope, name, target file
   ▼
[Evaluator agent] — independent check
   │  validates: well-formed? conflicts with existing? generalizable? <80 lines?
   │  produces: pass / fail + critique
   ▼
[Human gate] — reviews rule diff
   │  options: accept / edit / reject
   ▼
File written, committed, present in next session
```

Three roles map to: skill (generator), separate evaluator subagent, the engineer.

## Specific design choices

### Trigger

**Manual + retrospective**, copying Cursor's pattern from [[cursor-generate-rules]].

- Command: `/capture-rule [optional description]`
- Run AFTER the chat, when the engineer is satisfied with the agent's behavior.
- Optional description lets the engineer hint at what the rule should be about.

Why not auto-trigger: the literature confirms the engineer knows when a rule is worth crystallizing; the agent doesn't. Cursor learned this; we copy.

### Output format

**One concept per file**, not "append to one giant AGENTS.md."

- Files go to `.agents/rules/<short-slug>.md` (or the equivalent for whichever format the project uses).
- Or: append to AGENTS.md only if the rule is genuinely a small addition; create a separate file otherwise.
- Hard cap: 80 lines per rule (Cursor's empirical recommendation from [[cursor-generate-rules]]).
- Each rule has a name, a scope (when it applies), the rule body, and an example or counter-example from the chat.

### Generator agent prompt design

The generator should:

1. Read the recent chat history.
2. Read existing AGENTS.md / rules to avoid duplication.
3. Identify the **specific behavior** the engineer corrected toward.
4. Draft a rule that is:
   - Concrete ("use `pytest -k unit`", not "prefer fast tests")
   - Scoped (mention which kind of file / situation it applies to)
   - Includes a positive example or counter-example
   - Under 80 lines
5. Pick a filename / location.

### Evaluator agent prompt design

The evaluator should reject rules that:

- Conflict with an existing rule (read all existing rules to check).
- Restate something already in AGENTS.md or the codebase obviously.
- Are vague or non-actionable.
- Exceed length cap.
- Generalize too far from the chat (the chat was about X; the rule should not claim it applies to Y).
- Restate something the agent could derive from a linter config or test runner.

The evaluator is **a separate Claude invocation** (or sub-agent dispatch). Different prompt, no shared state with the generator. From [[anthropic-harness-design]]: separation is "a strong lever" against self-grading leniency.

### Human gate

The engineer sees a diff:

- Proposed file path.
- Proposed rule body.
- The chat excerpt that motivated it (so they can verify the generalization is fair).
- Evaluator's critique (if any).
- Three options: **Accept**, **Edit**, **Reject**.

If accepted, the file is written. If edited, the engineer's edits are saved. If rejected, nothing is written (no tracking of "this rejection happened" — the engineer is allowed to change their mind without it becoming a meta-rule).

### Pruning

A separate skill: `/prune-rules`. Runs occasionally (manual). For each existing rule:

- When was it created? When was it last "useful" (referenced in a chat)?
- Does it still apply (the codebase still has the file pattern it scopes to)?
- Has it been superseded by a later rule?
- Does it conflict with a rule added later?

Output: a list of rules to consider removing, with reasons. Human accepts / rejects. **Pruning is never automatic.**

This addresses the monotonic-growth problem (open question 1 in the research synthesis), which neither Cursor nor Aider solves explicitly.

### Conflict resolution

When the evaluator detects that a proposed rule conflicts with an existing one:

- Surface both rules to the engineer.
- Engineer decides: reject new, replace old, scope each more narrowly, or merge.

This is the multi-author handling. We don't try to auto-resolve; we surface and ask.

## What we explicitly do NOT do

- **No background / continuous capture.** The Cursor lesson + the engineer's knowledge of when a rule is real make manual triggering correct.
- **No auto-edit of AGENTS.md without human review.** The trust boundary stays at human approval, always.
- **No machine-learning of "which rules are good"** — too easy to introduce confirmation bias.
- **No reading other engineers' chats for rule inference** — privacy, scope, and noise.

## Risks and mitigations recap

| Risk | Mitigation in this design |
|---|---|
| Feedback ratchet (monotonic growth) | One rule per file + length cap + separate `/prune-rules` |
| Overfitting from one-shot feedback | Manual retrospective trigger; engineer only triggers when validated |
| Conflicting feedback (multi-author) | Evaluator detects, surfaces both, engineer decides |
| Confirmation bias loop | Generator and Evaluator are separate agents (different prompts, no shared context) |
| Self-modification trust boundary | Human gate is mandatory; nothing writes without engineer accept |

## Open implementation questions

1. Where do generated rules go: append AGENTS.md, separate rule files, or hybrid? Likely hybrid; needs concrete file-layout decision.
2. How does the evaluator know about all existing rules without reading the whole AGENTS.md every time? (Caching or rule index needed.)
3. What's the UX for the human gate in a CLI like Claude Code? Inline diff + Y/N/E? Open the file in $EDITOR?
4. How do generated rules interact with claude-mem's wiki layer? Cross-link? Independent?

These are next-iteration design problems, not blockers.

## Connections

- [[Project Profile]] — broader skill design this is part of
- [[Rule Generation from Chat]] — pattern this implements
- [[Generator-Evaluator Pattern]] — architecture this uses
- [[AGENTS.md]] — primary output format
- [[Research Feedback-Driven Project Profile]] — the synthesis page from this research pass
