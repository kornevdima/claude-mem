---
type: concept
title: "Context Rot"
created: 2026-06-28
updated: 2026-07-03
confidence: high
tags:
  - concept
  - long-context
  - context-engineering
status: current
related:
  - "[[Recursive Language Models]]"
  - "[[Context Engineering for Coding Agents]]"
  - "[[Domain-Specific Agents]]"
  - "[[Hot Cache]]"
  - "[[rlm-blog-zhang]]"
  - "[[yt-pocock-ai-coding-workflow]]"
---

# Context Rot

Model performance degrades as input context grows, even when the input fits inside the context window. Bigger windows do not fix it; the signal-to-noise ratio falls and the model attends worse over long inputs. (Source: [[rlm-blog-zhang]])

## Why it matters

It is the motivation for [[Recursive Language Models]]: rather than enlarge the window, keep the working context small and process the bulk out-of-context (grep, chunk, recurse). It also justifies claude-mem's existing tight-context habits: the [[Hot Cache]] (~500 words), short pages (under 200-300 lines), and sub-agent returns of 1-2K tokens (see [[Context Engineering for Coding Agents]]).

It is also the architectural motivation for [[Domain-Specific Agents]]: stacking skills/MCP onto one agent ("inheritance") hits diminishing-to-negative returns, so composition of small agents with minimal per-agent context is the structural fix. (Source: [[yt-schroeder-domain-specific-agents]])

## Practitioner framing: smart zone / dumb zone

[[Matt Pocock]] (crediting Dex Horthy of HumanLayer) teaches the same phenomenon as a **smart zone / dumb zone**: attention relationships scale quadratically with tokens ("adding a token is like adding a team to a football league"), and around **~100K tokens** the model gets measurably dumber — regardless of a 200K or 1M window. His operational rules: size every task to fit the smart zone; keep the always-loaded layer (system prompt, CLAUDE.md) tiny; show a token-count status line in every session; prefer **clearing context over compaction** (compaction accumulates "sediment"; clearing returns to a deterministic base state); and run automated code review in a *fresh* context, because reviewing at the end of an implementation session means reviewing in the dumb zone. 1M-token windows "ship more dumb zone" — useful for retrieval, not coding. (Source: [[yt-pocock-ai-coding-workflow]])

## Implication for the wiki

A large ADLC vault (hundreds of requirements, stories, tests, plus code wikis) cannot be loaded wholesale into a query's context without rot. The fix is to never load it all: grep first, read only matched slices, recurse per area. See [[RLM-Optimized Wiki Querying]].
