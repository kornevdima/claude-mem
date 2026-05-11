---
type: entity
title: "ETH Zurich AGENTbench Team"
entity_type: research-group
role: "Academic team; built AGENTbench and ran the 2026 evaluation of AGENTS.md"
first_mentioned: "[[evaluating-agents-md-eth]]"
created: 2026-05-09
updated: 2026-05-09
tags:
  - entity
  - research-group
  - eth-zurich
  - empirical
status: current
related:
  - "[[AGENTS.md]]"
  - "[[evaluating-agents-md-eth]]"
  - "[[Context Engineering for Coding Agents]]"
sources:
  - "[[evaluating-agents-md-eth]]"
---

# ETH Zurich AGENTbench Team

The research group at ETH Zurich (Software Reliability Lab adjacent) that produced AGENTbench and the 2026 paper "Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents?"

## Members

- Thibaud Gloaguen
- Niels Mündler
- Mark Müller
- Veselin Raychev
- Martin Vechev

## Why they matter here

Theirs is the **only** rigorous published empirical evaluation of repository-level context files for coding agents (as of mid-2026). Their findings are the load-bearing evidence behind the design caveats in the [[Project Profile]] concept.

## Headline findings (recap)

- LLM-generated context files: **-2 to -3%** task success (worse than no file).
- Human-written context files: **+4%** task success.
- Both options cost +20-23% inference and +3-4 extra steps regardless.
- Repository overviews specifically provide no measurable benefit.
- Stronger LLMs do not generate better context files.

(Source: [[evaluating-agents-md-eth]])

## What they tested

- **AGENTbench**: 138 instances from 12 Python repositories with developer-written AGENTS.md files.
- **Agents**: Claude Code, Codex, Qwen Code (4 total agents).
- **Conditions**: no context, LLM-generated context, human-written context.
- **Metric**: test-suite pass rate on real GitHub-issue-derived tasks.

## Limits to weight against

- Python only.
- 138 instances is a modest sample.
- Single-file AGENTS.md only (didn't test layered/nested).
- Doesn't test retrieval-on-demand vs upfront.

## Connections

- [[evaluating-agents-md-eth]] — the paper
- [[AGENTS.md]] — the format they evaluated
- [[Project Profile]] — claude-mem design that incorporates their caveats
