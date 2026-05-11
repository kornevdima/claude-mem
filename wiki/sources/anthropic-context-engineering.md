---
type: source
title: "Effective Context Engineering for AI Agents (Anthropic)"
source_type: vendor-engineering-blog
author: "Anthropic Engineering"
date_published: 2025
url: "https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents"
created: 2026-05-09
updated: 2026-05-09
confidence: high
tags:
  - source
  - anthropic
  - context-engineering
  - claude-code
status: current
related:
  - "[[Context Engineering for Coding Agents]]"
  - "[[Research Pre-computed Context for Coding Agents]]"
  - "[[anthropic-contextual-retrieval]]"
key_claims:
  - "Context engineering = curating optimal tokens during inference, broader than prompt engineering"
  - "Goal: smallest possible set of high-signal tokens that maximize desired outcome"
  - "Claude Code uses HYBRID: CLAUDE.md upfront + glob/grep for just-in-time retrieval"
  - "Recommended techniques for long-horizon tasks: compaction, structured note-taking, sub-agents"
  - "Tools should have minimal overlap and unambiguous names"
---

# Source: Effective Context Engineering for AI Agents (Anthropic)

**Author**: Anthropic Engineering
**URL**: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents

## Summary

Anthropic's published guidance on how to design what goes into an agent's context window. This is the canonical statement of how Claude Code itself handles context, useful as both reference and authority for claude-mem design choices.

## Definition Anthropic uses

> "Context engineering is the set of strategies for curating and maintaining the optimal set of tokens (information) during LLM inference."

Distinguished from prompt engineering: prompt engineering is about *writing* effective instructions; context engineering is about *managing* the entire context state across multiple inference turns — system instructions, tools, external data, message history.

## Core principles

- **"Informative, yet tight."** Treat context as a finite resource with diminishing returns.
- **"Smallest possible set of high-signal tokens that maximize the likelihood of some desired outcome."**
- Calibrate system prompts to the right "altitude" — specific enough to guide, flexible enough to be heuristic rather than brittle hardcoded logic.
- Curate a **minimal viable set of tools**. Avoid bloated tool sets where "a human engineer can't definitively say which tool should be used."
- Use **diverse, canonical examples** rather than exhaustive edge cases.

## How Claude Code itself works

> "Claude Code is an agent that employs a hybrid model where CLAUDE.md files are naively dropped into context up front, while primitives like glob and grep allow it to navigate its environment and retrieve files just-in-time."

The just-in-time half "effectively bypasses the issues of stale indexing and complex syntax trees" — i.e., it's a deliberate response to the problems repo-map and indexed-RAG approaches have.

Analogy Anthropic draws: human cognition. Humans don't memorize whole corpuses; they use external indexing systems (filesystems, inboxes, bookmarks) and retrieve on demand.

## Long-horizon task techniques

1. **Compaction** — summarize conversation contents before context limits, preserving architectural decisions and unresolved bugs while discarding redundant outputs. Claude Code does this by compressing history then continuing with compressed context plus the **5 most recently accessed files**.
2. **Structured note-taking** — agents maintain persistent notes (e.g., `NOTES.md` or todo list) outside the context window, retrieving them later. Anthropic released a "memory tool" in public beta.
3. **Sub-agent architectures** — specialized sub-agents handle focused tasks and return condensed summaries (typically 1,000-2,000 tokens) to a coordinator. Maintains a clean main context while enabling deep exploration.

## Tool design recommendations

Tools should be:
- "Self-contained, robust to error, and extremely clear" about intended use.
- "Minimal overlap in functionality."
- Use "descriptive, unambiguous" input parameters.

Plus a tactic: **tool result clearing** — once a tool result is deep in history, agents don't need the raw output; clearing it is "one of the safest lightest forms of compaction."

## Quantitative claims

The article makes **no explicit quantitative claims** about token savings or success-rate lifts. This is principled guidance, not a benchmark report. (Pair with [[anthropic-contextual-retrieval]] for the numbers.)

## What this changes in design

- The **hybrid model is endorsed**: a static, dropped-in artifact (CLAUDE.md / AGENTS.md / project profile) plus on-demand retrieval primitives. Don't try to put everything upfront; don't make everything JIT.
- The **5-most-recently-accessed-files** heuristic from compaction is a strong implementation pattern for any persistent agent context.
- The **sub-agent pattern with 1-2K token returns** matches claude-mem's existing graphify-extract / wiki-ingest design.
- The **minimal-tools** principle argues against the Two-Slash-Commands-Not-A-Smart-Router pattern claude-mem already uses.

## Connections

- [[Context Engineering for Coding Agents]] — concept page generalizing
- [[anthropic-contextual-retrieval]] — companion source on the retrieval side
- [[graphify-integration]] — claude-mem's sub-agent pattern matches the recommendation
