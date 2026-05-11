---
type: source
title: "Cursor /Generate Cursor Rules (v0.49)"
source_type: vendor-documentation
author: "Cursor (Anysphere)"
date_published: 2025-04-15
url: "https://cursor.com/changelog/0-49"
created: 2026-05-09
updated: 2026-05-09
confidence: high
tags:
  - source
  - cursor
  - rule-generation
  - feedback-driven
status: current
related:
  - "[[Rule Generation from Chat]]"
  - "[[Feedback Loop for Project Profile]]"
key_claims:
  - "Cursor 0.49 (April 15, 2025) shipped /Generate Cursor Rules command"
  - "Feature converts a productive chat into a reusable .mdc rule file"
  - "Generated rules go to .cursor/rules/ and use the same format as hand-written rules"
  - "Best practice: 1 concept per rule, under 50-80 lines, be specific"
  - "Auto-attached rules persist across long conversations (was previously broken)"
---

# Source: Cursor /Generate Cursor Rules (v0.49)

**Published**: 2025-04-15 (Cursor 0.49 changelog)
**URL**: https://cursor.com/changelog/0-49
**Vendor**: Cursor (Anysphere)

## Summary

The closest existing feature in the ecosystem to the design we're building. Lets a developer turn a productive chat — including correction-and-refinement of the agent's outputs — into a persistent, version-controlled rule file. Triggered manually with `/Generate Cursor Rules`.

## How it works

- During or after a chat, run `/Generate Cursor Rules`.
- Cursor extracts the conversation context (especially corrections and patterns the user has established).
- Output: an `.mdc` rule file written to `.cursor/rules/`.
- Same format as hand-written rules (MDC = Markdown + YAML frontmatter for scope/triggers).
- Rules can also be generated from scratch with a description: `/Generate Cursor Rules [description]`.

## Two trigger patterns

1. **After productive chat** — "When you're chatting with Cursor and correcting its code or refining a response, once you feel like 'Yep, that's exactly how we do it,' Cursor will turn that conversation into a reusable .mdc rule, capturing everything it just learned from you." (Source: search result, Atlan engineering blog)
2. **From scratch** — describe the rule you want; the agent drafts it.

## Best practices Cursor recommends

- **1 concept per rule**.
- **Under 50-80 lines** per rule.
- **Be specific** — vague rules get ignored by the agent.

## Trust / persistence improvements in v0.49

- "Auto-attached" rules now persist across long conversations (was previously broken).
- "Agent can now also edit rules reliably" — meaning the agent can modify rule files itself, not just read them.

## What this contributes

- **The trigger pattern is "manual + retrospective"** — not background, not on every turn. The user explicitly says "yes, this is the way we do it" before crystallizing. Mitigates one-shot-feedback overfitting.
- **One concept per file, with explicit length cap** — directly addresses the rule-bloat / monotonic-growth problem. Many small files instead of one giant one. PR-reviewable.
- **Same format as hand-written** — generated rules don't get a special status; they're peers with human-authored ones, both versioned in git.
- **Agent can edit rules** — Cursor explicitly designed for the self-modification loop. They've validated it's worth doing.

## Limits / what's not addressed in the changelog

- No documented pruning mechanism. Rules accumulate.
- No documented conflict-resolution between rules.
- No documented mechanism for retiring stale rules.
- No mention of whether the human reviews the generated rule before it's saved.

## Connections

- [[Rule Generation from Chat]] — concept page generalizing
- [[Feedback Loop for Project Profile]] — design page applying these patterns
- [[AGENTS.md]] — Cursor reads this too; rules are the tool-specific layer above it
