---
type: concept
title: "Context Rot"
created: 2026-06-28
updated: 2026-06-28
confidence: high
tags:
  - concept
  - long-context
  - context-engineering
status: current
related:
  - "[[Recursive Language Models]]"
  - "[[Context Engineering for Coding Agents]]"
  - "[[Hot Cache]]"
  - "[[rlm-blog-zhang]]"
---

# Context Rot

Model performance degrades as input context grows, even when the input fits inside the context window. Bigger windows do not fix it; the signal-to-noise ratio falls and the model attends worse over long inputs. (Source: [[rlm-blog-zhang]])

## Why it matters

It is the motivation for [[Recursive Language Models]]: rather than enlarge the window, keep the working context small and process the bulk out-of-context (grep, chunk, recurse). It also justifies claude-mem's existing tight-context habits: the [[Hot Cache]] (~500 words), short pages (under 200-300 lines), and sub-agent returns of 1-2K tokens (see [[Context Engineering for Coding Agents]]).

## Implication for the wiki

A large ADLC vault (hundreds of requirements, stories, tests, plus code wikis) cannot be loaded wholesale into a query's context without rot. The fix is to never load it all: grep first, read only matched slices, recurse per area. See [[RLM-Optimized Wiki Querying]].
