---
type: source
title: "Evaluating AGENTS.md (ETH Zurich)"
source_type: peer-reviewed-paper
author: "Thibaud Gloaguen, Niels Mündler, Mark Müller, Veselin Raychev, Martin Vechev"
affiliation: "ETH Zurich"
date_published: 2026-02-12
url: "https://arxiv.org/html/2602.11988v1"
created: 2026-05-09
updated: 2026-05-09
confidence: high
tags:
  - source
  - paper
  - empirical
  - agents-md
  - benchmark
status: current
related:
  - "[[AGENTS.md]]"
  - "[[Context Engineering for Coding Agents]]"
  - "[[Project Profile]]"
  - "[[Research Pre-computed Context for Coding Agents]]"
key_claims:
  - "Human-written AGENTS.md gives only +4% task success on AGENTbench"
  - "LLM-generated AGENTS.md REDUCES success by 2-3% (worse than no file)"
  - "Context files cost +20-23% inference and 3-4 extra steps regardless of source"
  - "Repository overviews (the most-included section) provide no measurable benefit"
  - "Stronger models do not generate better context files"
---

# Source: Evaluating AGENTS.md — Are Repository-Level Context Files Helpful for Coding Agents?

**Authors**: Thibaud Gloaguen, Niels Mündler, Mark Müller, Veselin Raychev, Martin Vechev (ETH Zurich)
**Published**: 2026-02-12
**License**: CC BY 4.0
**URL**: https://arxiv.org/html/2602.11988v1

## Why this is the most important source in this research pass

This is the **only** primary-source empirical evaluation of repository-level context files for coding agents. It directly tests the central premise of every "project profile" tool. The findings are counterintuitive enough to reshape design decisions.

## Methodology

- Built **AGENTbench**: 138 instances from 12 Python repositories that already have human-written AGENTS.md files.
- Tested four coding agents (Claude Code, Codex, Qwen Code) across three settings:
  1. No context file
  2. LLM-generated context file
  3. Human-written context file (the original developer's AGENTS.md)
- Measured by test-suite pass rate on real GitHub-issue-derived tasks.

## Headline empirical results

| Setting | AGENTbench delta | SWE-bench Lite delta | Cost delta |
|---|---|---|---|
| LLM-generated AGENTS.md | **-2%** (worse) | -0.5% | +20-23% inference, +3-4 steps |
| Human-written AGENTS.md | **+4%** | (small positive) | +19% inference (max), +3-4 steps |

> Both forms of context files **increased** inference cost by 20-23% and required 3-4 additional steps per task, regardless of whether they helped accuracy.

## Surprising findings

1. **Repository overviews don't help.** The most commonly included section provides no measurable benefit. Context files don't reduce the number of steps before the agent first interacts with relevant files.
2. **LLM-generated files merely duplicate README.** When documentation was artificially removed from the repo, LLM-generated AGENTS.md improved performance by +2.7% — confirming that in normal repos, the file just restates what's already discoverable.
3. **Reasoning tokens go up.** Following context files increases reasoning tokens 14-22% for GPT models. The agent has to *think* about the rules.
4. **Stronger models don't write better context.** Throwing more capable models at AGENTS.md generation doesn't fix it.
5. **Agents re-read context they already have.** GPT-5.1 mini was observed reading AGENTS.md repeatedly mid-task despite it being in the prompt.
6. **Specific instructions matter.** When AGENTS.md mentions a specific tool, the agent uses that tool 1.6× more often. So *concrete, actionable* directives beat overviews.

## What this changes in design

- Auto-generation from the repo without curation is **net-negative**. A `/project-profile` skill that just summarizes the codebase will likely degrade agent performance.
- Human curation is the only path to positive ROI, and even that is +4%.
- "Repository overview" sections waste tokens. Cut them.
- Specific actionable directives ("use `ruff check`, not `flake8`") outperform descriptive prose.
- The +20-23% baseline cost of carrying ANY context file means the file has to clear a bar to justify itself.

## Limits / open questions

- Tested only Python repos. C++, JS, Rust, Java may behave differently.
- 138 instances is a modest sample for cross-cutting claims.
- Doesn't test layered/hierarchical AGENTS.md (root + per-subdirectory) — only single-file setups.
- Doesn't test whether *retrieval* of context (only-when-relevant) outperforms upfront drop-in. This is the main design lever the paper leaves open.

## Connections

- [[AGENTS.md]] — the convention this paper evaluates
- [[Project Profile]] — design implications for claude-mem's planned skill
- [[Research Pre-computed Context for Coding Agents]] — synthesis
- [[anthropic-context-engineering]] — related Anthropic guidance on JIT vs upfront
