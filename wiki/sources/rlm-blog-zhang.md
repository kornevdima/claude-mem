---
type: source
title: "Recursive Language Models (blog, Alex L. Zhang)"
source_type: research-blog
author: "Alex L. Zhang"
date_published: 2025-10
url: "https://alexzhang13.github.io/blog/2025/rlm/"
created: 2026-06-28
updated: 2026-06-28
confidence: high
tags:
  - source
  - rlm
  - long-context
status: current
related:
  - "[[Recursive Language Models]]"
  - "[[rlm-paper-arxiv]]"
  - "[[Research Recursive Language Models]]"
key_claims:
  - "Root LM receives only the query; context is pre-loaded as a variable in a Python REPL the LM views by printing"
  - "The LM interacts by emitting code blocks; finishes with FINAL(answer) or FINAL_VAR(variable_name)"
  - "Strategies: peek (first ~2000 chars), grep (regex/keyword, not semantic), partition+map, summarize"
  - "Recursion is depth=1 today (root LM calls an LM, not a full RLM); the LM decides when to recurse"
  - "OOLONG 132k tokens: RLM(GPT-5-mini) beats GPT-5 by 34 points at roughly the same API cost; REPL-without-recursion ablation loses ~10%"
  - "BrowseComp-Plus: RLM(GPT-5) perfect at 1000 docs (non-recursive ablation 90%); queries take seconds to minutes (blocking, no prefix caching)"
---

# Source: Recursive Language Models (blog, Alex L. Zhang)

**Author**: Alex L. Zhang
**URL**: https://alexzhang13.github.io/blog/2025/rlm/

## Summary

The informal primary writeup (October 2025) that introduced RLMs before the paper. Best source for the concrete mechanics.

## Mechanics

- The root LM gets the **query only**. The long context `C` is a variable in a Python/IPython REPL. The model can only "see" the context by printing slices of it.
- It acts by emitting **code blocks** (CodeAct style, not JSON tool-calls), then reads the REPL output. It terminates with `FINAL(answer)` or `FINAL_VAR(var)`.
- It can call a recursive LM "as if it were a function in code": `rlm_query(sub_query, context_chunk)` / `rlm_query_batched(...)`, each returning an isolated environment's output.

## Strategies the model uses

- **Peek**: grab the first ~2000 chars to orient.
- **Grep**: regex/keyword to narrow the search space (lexical, not semantic retrieval).
- **Partition + map**: split the context, ask recursive LMs to label/answer each piece, combine.
- **Summarize**: condense subsets for the root LM's decision.

## Cost / latency

- OOLONG (132k tokens): +34 points over GPT-5 at roughly equal API cost.
- BrowseComp-Plus (1000 docs): perfect; cost scales reasonably with context length.
- Latency: queries run "a few seconds to several minutes" because sub-calls are **blocking** and there is **no prefix caching**.

## Limitations stated

No asynchrony; no strong guarantees on total cost/runtime; counting/numeric tasks degrade at large contexts; long-output tasks need many recursive calls and get slow. RLM **sidesteps** context rot rather than solving it architecturally.

## Connections

- [[Recursive Language Models]] | [[rlm-paper-arxiv]] | [[rlm-github-repo]] | [[Context Rot]]
