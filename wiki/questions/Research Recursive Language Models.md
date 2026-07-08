---
type: synthesis
title: "Research: Recursive Language Models"
created: 2026-06-28
updated: 2026-06-28
tags:
  - research
  - rlm
  - long-context
  - wiki-query
  - adlc
status: developing
related:
  - "[[Recursive Language Models]]"
  - "[[Context Rot]]"
  - "[[RLM-Optimized Wiki Querying]]"
  - "[[Alex L. Zhang]]"
  - "[[rlm-paper-arxiv]]"
  - "[[rlm-blog-zhang]]"
  - "[[rlm-github-repo]]"
  - "[[rlm-reproduction-overthink]]"
sources:
  - "[[rlm-paper-arxiv]]"
  - "[[rlm-blog-zhang]]"
  - "[[rlm-github-repo]]"
  - "[[rlm-reproduction-overthink]]"
---

# Research: Recursive Language Models

## Overview

Recursive Language Models (RLMs) are an inference strategy from MIT CSAIL (Zhang, Kraska, Khattab; blog Oct 2025, paper Dec 2025). The long context is held in a REPL environment as a variable; the model gets only the query and writes code to peek, grep, chunk, and recursively call sub-LMs over snippets. It sidesteps [[Context Rot]] and scales to 10M+ tokens. (Source: [[rlm-paper-arxiv]], [[rlm-blog-zhang]])

## Key Findings

- The root LM never holds the full context; it views it by printing slices in a Python REPL and acts via code blocks (CodeAct), ending with `FINAL(...)`. (Source: [[rlm-blog-zhang]])
- Recursion is `rlm_query(sub_query, chunk)`, depth=1 today; the model decides when to recurse. Strategies: peek, grep, partition+map, summarize. (Source: [[rlm-blog-zhang]])
- Reported gains at comparable cost: +26% median vs GPT-5 compaction, +130% vs CodeAct-with-sub-calls, +13% vs Claude Code; OOLONG +34 points; BrowseComp-Plus perfect at 1000 docs. Treat as medium pending independent checks. (Source: [[rlm-paper-arxiv]])
- A reproduction confirms the mechanism but flags over-recursion latency, error propagation, superlinear cost in depth, and non-termination on ambiguous prompts. Headline: calibrate depth. (Source: [[rlm-reproduction-overthink]])
- The implementation is a drop-in `rlm.completion(...)` with REPL backends (Local / IPython / Docker / cloud sandboxes) and multi-provider support. (Source: [[rlm-github-repo]])

## Key Entities

- [[Alex L. Zhang]]: lead author (MIT CSAIL). Co-authors Tim Kraska and Omar Khattab (DSPy; ships DSPy.RLM).

## Key Concepts

- [[Recursive Language Models]]: the inference strategy.
- [[Context Rot]]: the long-context degradation RLM avoids.
- [[RLM-Optimized Wiki Querying]]: the claude-mem application design.

## Application to claude-mem (the point of this research)

The main ADLC agent runs a frontier model and has bash, so the vault is the environment and bash is the REPL: an exact RLM precondition. Proposed direction (full design in [[RLM-Optimized Wiki Querying]]):

- **`wiki-query`**: keep the current `hot.md` read as the **peek** step, then switch to **grep-first + bounded recursion**. Grep `wiki/` (and `services/*/wiki/`) on greppable frontmatter and `_index.md` files, read only matched slices, and dispatch a sub-agent per large/dense area (one `rlm_query` per subtree) returning ~1-2K-token cited answers. Synthesize at the root.
- **Structure**: already grep-friendly; reinforce greppable frontmatter, per-folder `_index.md`, short pages, and stable cross-wiki IDs. Optional `wiki/index.json` only if grep gets noisy at scale.
- **ADLC fit**: large multi-service vaults are exactly where loading index+pages hits context rot and where grep+recurse pays off. Frontier root plans/synthesizes; cheaper sub-models read the chunks.
- **Guardrails**: depth 1 (maybe 2 for service wikis), calibrate (skip recursion for small vaults), explicit termination, require citations to limit error propagation, fan out independent areas in parallel.

## Contradictions

- Benchmark magnitude: the paper reports large gains; the reproduction ([[rlm-reproduction-overthink]]) confirms direction but warns the gains erode under over-recursion and tight latency/cost. Net: real but conditional on calibrated depth.

## Open Questions

- Does grep over markdown frontmatter scale, or is a generated `index.json` needed for large ADLC vaults? (Defer until a vault is large enough to test.)
- Where should sub-call results be cached so re-queries are cheap (no prefix caching in RLM)? Candidate: file answers to `questions/` and check there first.
- Depth=2 for service code wikis: worth it, or does it reintroduce error propagation? Needs a real ADLC vault to measure.
- Should this ship as an evolution of `wiki-query`, or a separate `wiki-query` mode flag for large/ADLC vaults? (Design decision pending.)

## Sources

- [[rlm-paper-arxiv]]: Zhang, Kraska, Khattab, 2025-12-31 (arXiv 2512.24601)
- [[rlm-blog-zhang]]: Alex L. Zhang, 2025-10
- [[rlm-github-repo]]: alexzhang13/rlm
- [[rlm-reproduction-overthink]]: reproduction, 2026 (arXiv 2603.02615)
