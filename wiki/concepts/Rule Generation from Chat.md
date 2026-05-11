---
type: concept
title: "Rule Generation from Chat"
complexity: intermediate
domain: ai-agents
aliases:
  - "Chat-Derived Rules"
  - "Conversational Rule Capture"
created: 2026-05-09
updated: 2026-05-09
tags:
  - concept
  - rule-generation
  - feedback-driven
  - context-engineering
status: developing
related:
  - "[[Feedback Loop for Project Profile]]"
  - "[[AGENTS.md]]"
  - "[[Generator-Evaluator Pattern]]"
  - "[[cursor-generate-rules]]"
sources:
  - "[[cursor-generate-rules]]"
  - "[[aider-conventions]]"
  - "[[reflexion-paper]]"
---

# Rule Generation from Chat

The pattern of converting a productive chat session — including human corrections of agent output — into a persistent, version-controlled rule that future agent runs read. Pioneered in the coding-agent ecosystem by Cursor's `/Generate Cursor Rules` (v0.49, April 2025) (Source: [[cursor-generate-rules]]).

## The Pattern in One Sentence

After a chat where the user corrects the agent's behavior into something they're happy with, a command crystallizes that conversation into a rule file that future agent invocations will read upfront.

## Why it works

- **Context is intact.** The rule is written while the example that motivated it is still in the conversation, with all surrounding context.
- **Validation is implicit.** The user only triggers the command when they're satisfied — so the captured behavior is already validated.
- **Persistent and shareable.** The output is a versioned file, so it survives sessions, teams, and tool changes.
- **Concrete > abstract.** Rules derived from real chats are about real situations the team actually encountered, not hypothetical conventions.

## Reference implementation: Cursor's design

From [[cursor-generate-rules]]:

- Command: `/Generate Cursor Rules`
- Trigger: manual, retrospective (after the chat, not during).
- Output: `.mdc` file in `.cursor/rules/`, same format as hand-written rules.
- Best-practice constraints:
  - **One concept per rule** — many small files, not one giant one.
  - **Under 50-80 lines** per rule.
  - **Be specific** — vague rules get ignored.

## Contrast: Aider's conservative approach

[[aider-conventions]] takes the opposite stance. CONVENTIONS.md is **strictly human-authored**. Aider never writes to it. The reasoning is implicit: by removing the feedback loop entirely, you sidestep every drift, bias, and trust-boundary problem.

Both designs are valid. The trade-off:

| | Cursor approach | Aider approach |
|---|---|---|
| Friction to add a rule | Low (one command after chat) | Higher (manual edit) |
| Risk of bad rule sneaking in | Higher (agent participates in writing) | Lower (human writes everything) |
| Rule volume over time | Grows fast | Grows slowly |
| Trust model | Agent + human shared authorship | Strict separation |

## Academic foundation: Reflexion

[[reflexion-paper]] formalizes the underlying architecture: an Actor produces output, an Evaluator scores it, a Self-Reflection model converts that score into verbal feedback that becomes durable text the next-run Actor reads. Cursor's rule generation is essentially Reflexion applied at the project level rather than the task level.

## Open design problems

These are not solved by either Cursor's docs or the academic literature:

1. **Pruning.** Rules accumulate. Nothing in published systems retires a rule that's no longer useful.
2. **Conflict resolution.** Two rules can disagree (especially in multi-author teams). No system handles this gracefully.
3. **Overfitting from one-shot feedback.** A rule derived from one chat may overgeneralize.
4. **Confirmation-bias loop.** When the agent participates in writing rules about its own behavior, it tends toward leniency (per [[anthropic-harness-design]]).
5. **Trust boundary.** What signs off a generated rule before it lands in the file? Human review? Auto-commit?

## Design implications for `/project-profile`

- **Manual + retrospective trigger** beats automatic / continuous. The user knows when a rule is worth crystallizing; the agent doesn't.
- **One concept per file, with a length cap** is the simple solution to monotonic growth — replace "AGENTS.md grows forever" with "many small rule files, each one PR-reviewable."
- **Generator-Evaluator separation** ([[Generator-Evaluator Pattern]]) is the trust-boundary tool. The skill that proposes the rule should not be the agent that uses it.
- **Pruning has to be a deliberate operation**, not implicit. Add a `/prune-rules` or equivalent.

## Connections

- [[cursor-generate-rules]] — primary reference implementation
- [[aider-conventions]] — null-hypothesis baseline
- [[reflexion-paper]] — academic foundation
- [[Generator-Evaluator Pattern]] — trust-boundary pattern
- [[Feedback Loop for Project Profile]] — design synthesis
- [[Project Profile]] — broader skill design this feeds into
