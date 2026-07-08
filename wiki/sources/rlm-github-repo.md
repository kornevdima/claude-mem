---
type: source
title: "alexzhang13/rlm (GitHub)"
source_type: code-repo
author: "Alex L. Zhang et al."
date_published: 2025
url: "https://github.com/alexzhang13/rlm"
created: 2026-06-28
updated: 2026-06-28
confidence: high
tags:
  - source
  - rlm
  - implementation
status: current
related:
  - "[[Recursive Language Models]]"
  - "[[RLM-Optimized Wiki Querying]]"
  - "[[Research Recursive Language Models]]"
key_claims:
  - "Drop-in shape: replace llm.completion(prompt, model) with rlm.completion(prompt, model)"
  - "Context offloaded as a REPL variable; recursion via rlm_query() / rlm_query_batched() inside generated code"
  - "REPL backends: LocalREPL (exec), IPythonREPL, DockerREPL; cloud sandboxes Modal / Prime Intellect / Daytona / E2B"
  - "Providers: OpenAI, Anthropic, OpenRouter, Portkey, local via vLLM; Python 3.11+"
  - "RL training harness via prime-rl + verifiers env (training/environments/oolong)"
  - "Adoption: DSPy.RLM, Ax, context-labs/HALO, Symbolica ARC-AGI, Google Cloud ADK"
---

# Source: alexzhang13/rlm (GitHub)

**URL**: https://github.com/alexzhang13/rlm

## Summary

Reference implementation. API mirrors a normal completion call: `rlm.completion(prompt, model)` in place of `llm.completion(...)`. The harness is **CodeAct-style** (the model writes executable code rather than emitting JSON tool calls).

## Architecture notes

- Context is an in-memory **variable** in a REPL; the model reads it only by printing.
- Recursion: `rlm_query()` and `rlm_query_batched()` callable from generated code (depth=1 today).
- REPL backends: `LocalREPL` (same-process `exec`), `IPythonREPL` (optional subprocess isolation), `DockerREPL` (container). Cloud sandboxes: Modal, Prime Intellect, Daytona, E2B.
- Providers: OpenAI, Anthropic, OpenRouter, Portkey, local via vLLM. Python 3.11+.
- Includes an RL training harness (`prime-rl`, `verifiers` env, `training/environments/oolong/`).

## Why it matters for claude-mem

The "context as a REPL variable + the agent greps/chunks/recurses via code" pattern maps directly onto an agent that already has **bash** over a `wiki/` filesystem. See [[RLM-Optimized Wiki Querying]].

## Caveats

Non-isolated REPLs (Local/IPython) are unsafe for adversarial/production input. Prime sandboxes noted as slow (open issue).

## Connections

- [[Recursive Language Models]] | [[rlm-blog-zhang]] | [[RLM-Optimized Wiki Querying]]
