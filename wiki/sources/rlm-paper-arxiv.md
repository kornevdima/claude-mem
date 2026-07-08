---
type: source
title: "Recursive Language Models (arXiv 2512.24601)"
source_type: paper
author: "Alex L. Zhang, Tim Kraska, Omar Khattab (MIT CSAIL)"
date_published: 2025-12-31
url: "https://arxiv.org/abs/2512.24601"
created: 2026-06-28
updated: 2026-06-28
confidence: high
tags:
  - source
  - rlm
  - long-context
  - inference
status: current
related:
  - "[[Recursive Language Models]]"
  - "[[Context Rot]]"
  - "[[Alex L. Zhang]]"
  - "[[Research Recursive Language Models]]"
key_claims:
  - "RLM = inference paradigm: treats long prompts as an external environment the LLM examines, decomposes, and recursively calls itself over"
  - "Processes inputs up to two orders of magnitude beyond the model context window (10M+ tokens tested)"
  - "Median +26% over GPT-5 (compaction), +130% over CodeAct-with-sub-calls, +13% over Claude Code across four long-context tasks, at comparable cost"
  - "RLM-Qwen3-8B: +28.3% average over base Qwen3-8B, approaching vanilla GPT-5 on three long-context tasks"
  - "Submitted 2025-12-31; revised 2026-05-11"
---

# Source: Recursive Language Models (arXiv 2512.24601)

**Authors**: Alex L. Zhang, Tim Kraska, Omar Khattab (MIT CSAIL)
**URL**: https://arxiv.org/abs/2512.24601

## Summary

The primary paper. Defines RLMs as "a general inference paradigm that treats long prompts as part of an external environment and allows the LLM to programmatically examine, decompose, and recursively call itself over snippets of the prompt." The key move: do not put the long context in the model's window; store it in a REPL environment and let the model write code to inspect it and spawn sub-LM calls.

## Key claims

- Scales to inputs "up to two orders of magnitude beyond model context windows" (10M+ tokens tested).
- Quantitative gains over frontier baselines at comparable cost: +26% median vs GPT-5 compaction, +130% vs CodeAct with sub-calls, +13% vs Claude Code.
- Small-model result: RLM-Qwen3-8B gains +28.3% average over base, approaching vanilla GPT-5 on three tasks.

## Confidence

High as a primary source for the method. Benchmark percentages are author-reported; treat as **medium** until independently verified. Partially corroborated by the reproduction study [[rlm-reproduction-overthink]].

## Connections

- [[Recursive Language Models]] — concept page
- [[Context Rot]] — the problem RLM sidesteps
- [[rlm-blog-zhang]] — the informal primary writeup
- [[rlm-github-repo]] — the implementation
