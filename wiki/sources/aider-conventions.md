---
type: source
title: "Aider Conventions Documentation"
source_type: vendor-documentation
author: "Aider (Paul Gauthier)"
date_published: ongoing
url: "https://aider.chat/docs/usage/conventions.html"
created: 2026-05-09
updated: 2026-05-09
confidence: high
tags:
  - source
  - aider
  - conventions
  - manual
status: current
related:
  - "[[Aider]]"
  - "[[Feedback Loop for Project Profile]]"
key_claims:
  - "Aider supports CONVENTIONS.md as a manual coding-style file"
  - "Loaded via /read CONVENTIONS.md or --read CONVENTIONS.md flag"
  - "No documented mechanism for auto-updating from chat feedback"
  - "Format is unconstrained markdown; no length or structure prescription"
---

# Source: Aider Conventions

**URL**: https://aider.chat/docs/usage/conventions.html
**Vendor**: Aider (Paul Gauthier)

## Summary

Aider's approach to project conventions is **deliberately manual and minimal**. CONVENTIONS.md is just a markdown file you write. Aider reads it. There is no automatic update, no chat-derived rule generation, no feedback loop. Pair this with the fact that Aider also reads AGENTS.md natively, and the picture is: convention files are owned by the human; Aider does not modify them.

## How it works

- Filename: `CONVENTIONS.md` (default; configurable).
- Loaded by:
  - `/read CONVENTIONS.md` in a chat session (marks read-only)
  - `aider --read CONVENTIONS.md` flag at startup
  - Configuration entry in `.aider.conf.yml`
- Format: free-form markdown. Recommended: bullet points like "Prefer httpx over requests", "Use types everywhere possible".

## What Aider does not do

- **No `/generate-conventions` or equivalent** — there's no command to derive conventions from chat history.
- **No auto-update mechanism** — Aider never writes to CONVENTIONS.md.
- **No length / structure guidance** — docs are silent on size limits.
- **No interaction with AGENTS.md documented in this page** — though Aider reads AGENTS.md too, this docs page doesn't address overlap or precedence.

## Implicit design philosophy

Aider's choice is **strict separation of human authorship and agent execution**. The agent reads the conventions; the human writes them. This sidesteps every trust-boundary, drift, and feedback-bias problem by simply not having a feedback loop.

## What this contributes

- A useful **null-hypothesis baseline**: many users get value from a manual file with no feedback loop at all. It's a real option for `/project-profile`.
- The **strict separation pattern** is a worthy default — more conservative than Cursor's auto-edit-rules approach.
- Suggests one valid design: `/project-profile` proposes a draft, human edits, never re-writes without explicit ask.

## Connections

- [[Aider]]
- [[Rule Generation from Chat]]
- [[Feedback Loop for Project Profile]] — design page contrasts this baseline with Cursor's approach
