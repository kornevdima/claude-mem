---
type: concept
title: "RLM-Optimized Wiki Querying"
created: 2026-06-28
updated: 2026-06-28
confidence: medium
tags:
  - concept
  - design
  - rlm
  - wiki-query
  - adlc
status: developing
related:
  - "[[Recursive Language Models]]"
  - "[[Context Rot]]"
  - "[[rlm-github-repo]]"
  - "[[rlm-reproduction-overthink]]"
  - "[[Research Recursive Language Models]]"
---

# RLM-Optimized Wiki Querying

A design for applying [[Recursive Language Models]] to claude-mem's `wiki-query` skill and `wiki/` structure, so wiki work in **Mode ADLC** scales to large multi-service vaults without [[Context Rot]]. The main ADLC agent already runs a frontier model and can execute bash, which is exactly the RLM precondition: the vault is the environment, bash is the REPL.

## The mapping

| RLM primitive | claude-mem equivalent |
|---|---|
| Context as a REPL variable | the `wiki/` filesystem (and `services/*/wiki/`) |
| `print(context[a:b])` | `rg` / read a specific page or slice |
| grep over context | `rg`/`grep` across `wiki/` (frontmatter + IDs are greppable) |
| `rlm_query(sub_query, chunk)` | dispatch a sub-agent (Explore / wiki-query worker) over a folder or page set; it returns a condensed answer |
| `FINAL(answer)` | synthesize, cite pages, file good answers back to `questions/` |

## Today vs proposed

- **Today** (`wiki-query`): cost-tiered loading. Read `hot.md` -> `index.md` -> a few pages into the root context. Works at < ~50 pages; degrades as the vault grows.
- **Proposed**: keep the tiers as the **peek** step, then switch to **grep-first + bounded recursion**. The root agent greps for matches, reads only matched slices, and for any large/dense area dispatches a sub-agent to read+answer over that subtree, pulling back ~1-2K tokens. The root window stays small; cheaper sub-models do the bulk reading.

## Proposed query loop

1. **Peek**: read `hot.md`; if it answers, stop.
2. **Locate**: `rg` the query terms across `wiki/` (and `services/*/wiki/`), targeting greppable frontmatter (`type`, `status`, `req_id`, `traces_to`) and `_index.md` files. Collect candidate pages, do not read them all.
3. **Read or recurse**: for a handful of small pages, read slices directly. For a large/dense area (e.g. all `requirements/` or one service's specs), dispatch one sub-agent per area with the sub-query; it returns a condensed, cited answer.
4. **Synthesize**: combine sub-answers, cite pages, answer. File valuable answers to `questions/`.

## Guardrails (from the reproduction critique)

- **Bound depth** to 1 (optionally 2 for service code wikis). No unbounded recursion. (Source: [[rlm-reproduction-overthink]])
- **Calibrate**: small vault (< ~50 pages) -> stay with the current tiered load; do not recurse. Recursion earns its keep only on large/dense vaults.
- **Explicit termination**: a query plan with a fixed candidate set, not open-ended exploration.
- **Verify sub-answers**: sub-agents can err; require page citations so the root can spot-check, limiting error propagation.
- **Cost/latency**: sub-calls are blocking. Fan out independent areas in parallel (one message) rather than serially.

## Structure changes to support it

The structure is already grep-friendly; reinforce it rather than rebuild:

- **Greppable frontmatter** on every page (already a convention): keep `type`, `status`, and ADLC IDs (`req_id`, `traces_to`) consistent so `rg` is a reliable locator.
- **Per-folder `_index.md`** (already present): these are the cheap "directory listings" the root reads before recursing.
- **Short pages** (under 200-300 lines, already a rule): chunk-sized so a single read or one sub-call covers a page.
- **Stable IDs** across product wiki and service code wikis: makes cross-wiki grep + traceability work for recursion.
- Optional: a generated `wiki/index.json` (machine-readable mirror of `index.md`) if grep over markdown proves noisy at scale. Defer until needed.

## Why this fits ADLC specifically

ADLC vaults are the large case: product wiki (hundreds of requirements/stories/tests) plus N service code wikis. That is precisely where loading index+pages hits context rot and where grep+recurse pays off. The frontier root model plans and synthesizes; sub-agents (cheaper models) absorb the per-area reading. See [[Research Recursive Language Models]] for the full evaluation.
