---
type: concept
title: "Recursive Language Models"
created: 2026-06-28
updated: 2026-06-28
confidence: high
tags:
  - concept
  - rlm
  - long-context
  - inference
status: developing
related:
  - "[[Context Rot]]"
  - "[[RLM-Optimized Wiki Querying]]"
  - "[[Context Engineering for Coding Agents]]"
  - "[[Wiki vs RAG]]"
  - "[[rlm-paper-arxiv]]"
  - "[[rlm-blog-zhang]]"
  - "[[rlm-github-repo]]"
---

# Recursive Language Models (RLM)

An inference strategy: instead of stuffing a long context into the model's window, store it as a variable in a **REPL environment** and give the model only the **query**. The model writes code to peek, grep, chunk, and print the context, and can **recursively call sub-LM instances** over snippets. (Source: [[rlm-paper-arxiv]], [[rlm-blog-zhang]])

## Mechanism

- Root LM sees the query, not the context. Context `C` is a Python REPL variable it can only view by printing slices.
- It acts via **code blocks** (CodeAct, not JSON tool-calls); terminates with `FINAL(answer)` / `FINAL_VAR(var)`.
- Recursion: `rlm_query(sub_query, chunk)` / `rlm_query_batched(...)` run sub-LMs over pieces and return condensed output. Depth is 1 today. The model decides when to recurse.
- Strategies: peek (first chars), grep (lexical), partition+map, summarize.

## Why

Avoids **[[Context Rot]]**: model accuracy falls as context grows, regardless of window size. RLM keeps the root window tiny and processes the bulk out-of-context. Scales to 10M+ tokens (two orders of magnitude beyond the window). (Source: [[rlm-paper-arxiv]])

## Results (author-reported, treat as medium)

- +26% median vs GPT-5 compaction, +130% vs CodeAct-with-sub-calls, +13% vs Claude Code, at comparable cost.
- OOLONG 132k: RLM(GPT-5-mini) +34 points over GPT-5 at ~equal API cost.
- BrowseComp-Plus: perfect at 1000 docs. Partially corroborated by [[rlm-reproduction-overthink]].

## Limitations

Blocking sub-calls, no prefix caching, no hard cost/runtime bound, weak on counting, slow on long-output tasks. Reproduction adds: over-recursion latency, error propagation, superlinear cost in depth, non-termination on ambiguous prompts. Fix: **calibrate** depth. (Source: [[rlm-reproduction-overthink]])

## Relation to claude-mem

The pattern (context as an environment the agent programs over) is exactly what an agent with **bash over `wiki/`** can do. Design: [[RLM-Optimized Wiki Querying]]. Compare [[Wiki vs RAG]] and [[Context Engineering for Coding Agents]] (Anthropic's hybrid JIT-retrieval is a shallow version of the same idea).
