---
type: synthesis
title: "Research: Pre-computed Context for Coding Agents"
created: 2026-05-09
updated: 2026-05-09
tags:
  - research
  - synthesis
  - agent-context
  - project-profile
status: developing
related:
  - "[[Context Engineering for Coding Agents]]"
  - "[[AGENTS.md]]"
  - "[[Repo Map]]"
  - "[[Contextual Retrieval]]"
  - "[[Project Profile]]"
  - "[[ETH Zurich AGENTbench Team]]"
  - "[[Aider]]"
  - "[[agents-md-spec]]"
  - "[[evaluating-agents-md-eth]]"
  - "[[aider-repo-map]]"
  - "[[anthropic-context-engineering]]"
  - "[[anthropic-contextual-retrieval]]"
  - "[[racg-survey-2025]]"
sources:
  - "[[agents-md-spec]]"
  - "[[evaluating-agents-md-eth]]"
  - "[[aider-repo-map]]"
  - "[[anthropic-context-engineering]]"
  - "[[anthropic-contextual-retrieval]]"
  - "[[racg-survey-2025]]"
---

# Research: Pre-computed Context for Coding Agents

Two-pass research run on **2026-05-09** to inform the design of a `/project-profile` skill for the claude-mem plugin. Pass A: empirical findings on what context types improve agentic-coding task success. Pass B: emerging conventions and standards (AGENTS.md, llms.txt, CLAUDE.md, .cursorrules, Aider's repo-map).

## Overview

The research question driving this pass: **what should a project pre-compute about itself to save tokens during coding tasks AND produce code that fits the host project's conventions?**

Key finding that reshapes the obvious answer: the only rigorous empirical evaluation (ETH Zurich AGENTbench, Feb 2026) shows that LLM-generated context files **degrade** agent performance by 2-3%, while even human-written ones give only +4% with significant cost overhead. Naive auto-summarization is the wrong move. The right move is hand-curated tribal knowledge plus an AGENTS.md-compatible format plus on-demand structural retrieval.

## Key Findings

### Empirical (Pass A)

1. **LLM-generated context files are net-negative**: -2% to -3% task success on AGENTbench, -0.5% on SWE-bench Lite. They duplicate README and waste tokens. (Source: [[evaluating-agents-md-eth]])
2. **Human-written context files give only +4% task success**, with +20-23% inference cost and +3-4 extra steps per task. The win is real but small. (Source: [[evaluating-agents-md-eth]])
3. **Repository overviews don't help.** The most-included AGENTS.md section provides no measurable benefit. Cut it. (Source: [[evaluating-agents-md-eth]])
4. **Specific actionable directives outperform descriptive prose.** When a tool/command is named in AGENTS.md, the agent uses it 1.6× more often. (Source: [[evaluating-agents-md-eth]])
5. **Anthropic's principle**: "smallest possible set of high-signal tokens that maximize the likelihood of some desired outcome." (Source: [[anthropic-context-engineering]])
6. **Hybrid model is the consensus**: small upfront artifact (CLAUDE.md / AGENTS.md) + on-demand retrieval via glob/grep. (Source: [[anthropic-context-engineering]])
7. **Contextual Retrieval cuts top-20 retrieval failure by 35-67%** (with reranking). One-time preprocessing cost ~$1.02 per million tokens. (Source: [[anthropic-contextual-retrieval]])
8. **Below 200K tokens of corpus, skip RAG entirely** — drop the whole thing into prompt + use prompt caching. Most projects' load-bearing context fits this bound. (Source: [[anthropic-contextual-retrieval]])
9. **Cross-file dependencies, structural information (class hierarchies, types), API signatures, and naming conventions** are explicitly identified as critical context types for repo-level work. (Source: [[racg-survey-2025]])
10. **Iterative agentic retrieval beats one-shot** for repo-scale tasks. (Source: [[racg-survey-2025]])

### Conventional (Pass B)

11. **AGENTS.md is the cross-vendor standard.** 60K+ projects, 20+ tools (Codex, Cursor, Copilot, Aider, Devin, Jules, etc.), Linux Foundation governance since August 2025. (Source: [[agents-md-spec]])
12. **llms.txt is a different standard for a different problem** — it's for AI/LLM web crawlers reading public docs sites, not for in-repo agent context. ~10% adoption, mostly documentation hosts. Adopted by Anthropic, Stripe, Cursor docs. Not the same use case. (Source: search results 2026-05-09)
13. **Aider's repo-map (tree-sitter + PageRank, 1K-token budget) is the canonical structural-summary pattern.** Reproduced in RepoMapper, Sourcegraph Cody (via SCIP), and others. (Source: [[aider-repo-map]])
14. **Sourcegraph Cody scales context retrieval to 300K+ repos** using SCIP code graph + keyword + semantic search. Continue.dev has known scalability issues with full-file indexing. (Source: search results 2026-05-09)
15. **Tool-specific files (CLAUDE.md, .cursorrules, copilot-instructions.md) are not going away** but are converging toward "AGENTS.md as cross-tool source of truth + tool-specific files only for tool-specific features." (Source: agentrulegen comparison)

## Key Entities

- [[ETH Zurich AGENTbench Team]] — Gloaguen, Mündler, Müller, Raychev, Vechev — produced the only rigorous empirical evaluation of AGENTS.md
- [[Aider]] — originated the tree-sitter + PageRank repo-map pattern
- **Anthropic** — published context-engineering principles, contextual retrieval technique, and the hybrid model that Claude Code itself uses
- **Agentic AI Foundation (Linux Foundation)** — stewards the AGENTS.md spec
- **Sourcegraph** — Cody pioneered scalable RAG for codebases (300K+ repo support)

## Key Concepts

- [[Context Engineering for Coding Agents]] — the umbrella discipline
- [[AGENTS.md]] — the cross-vendor convention
- [[Repo Map]] — the structural-summary pattern
- [[Contextual Retrieval]] — the retrieval technique with the strongest published numbers
- [[Project Profile]] — claude-mem's design synthesizing the above

## Contradictions

- **Aider blog vs AGENTbench paper on the value of structural summaries.** Aider's design assumes repo-map gives meaningful task improvement. AGENTbench's evaluation of context files (which include structural summaries when present) finds at most +4%, often negative. **Resolution**: the Aider blog reports only qualitative improvement; AGENTbench tests AGENTS.md specifically, not isolated repo-map. Both can be true if structural summaries help by *enabling targeted retrieval* (Aider's actual usage pattern) rather than by being read top-to-bottom (AGENTbench's setup).
- **Survey ([[racg-survey-2025]]) emphasizes graph-based retrieval for cross-file reasoning.** AGENTbench shows the *upfront* artifacts are mostly neutral. **Resolution**: not actually contradictory — the survey is about retrieval-on-demand, AGENTbench is about pre-loaded context. They argue for the same thing: hybrid.
- **llms.txt vs AGENTS.md naming confusion.** Some sources discuss them as if competing. They aren't — different audiences (web crawlers vs in-repo agents), different content. (Source: 2026-05-09 search and llms.txt adoption guides)

## Open Questions

These didn't get answered by the literature and remain design questions for the project-profile skill:

1. **Brownfield "current generation" tagging.** A 5-year codebase has multiple generations of code. None of the literature addresses how to mark which generation is "current style" so the agent copies from the right examples. Likely needs explicit user annotation (glob patterns or tags).
2. **Layered AGENTS.md.** AGENTbench tested only single-file AGENTS.md. The spec allows nested files. No empirical data on whether nested helps or hurts.
3. **Refresh cadence.** Conventions drift. No published guidance on how often to regenerate / re-curate AGENTS.md, only that drift is a real problem.
4. **Verification UX.** When a skill says "I detected pattern X in your codebase," how does the human review and correct before saving? No standard pattern exists; this is design-original.
5. **The "tribal knowledge" UX problem.** The only consistent positive in AGENTbench is human-curated tribal content. How does a skill prompt humans for this without burning patience? Open.
6. **Quantitative effect of repo-map specifically.** Aider doesn't publish numbers. AGENTbench bundles repo-map with everything else. Worth measuring directly if claude-mem's `/project-profile` ships.
7. **AGENTS.md re-reading mid-task.** GPT-5.1-mini was observed reading AGENTS.md repeatedly despite already having it in context. Token waste worth flagging in design.
8. **How prompt caching changes the math.** AGENTbench cost numbers are without prompt caching. If a project profile is the SAME across many tasks, prompt-cached AGENTS.md has near-zero marginal cost — which would change the +4%/+20%-cost trade-off significantly.

## Implications for `/project-profile` Design

Recorded in detail at [[Project Profile]]. Summary:

1. **Output format = AGENTS.md** (cross-tool), not a claude-mem-specific format.
2. **Don't auto-generate the bulk of the content** — the literature says it'll degrade performance. Skill should generate only the mechanically-extractable parts (build/test commands, linter configs).
3. **Tribal knowledge sections come from a structured user interview**, not auto-extraction.
4. **Repo-map (tree-sitter + PageRank, ~1K tokens) is a separate, on-demand artifact**, not part of AGENTS.md. claude-mem's `graphify` already produces the underlying graph.
5. **Skip RAG, use prompt caching** — claude-mem's wiki scale fits Anthropic's "<200K tokens, just include it" recommendation.
6. **Cap upfront context at ~4K tokens** total (AGENTS.md + repo-map summary + hot cache). Beyond that, AGENTbench data shows costs ramping without benefits.
7. **Refresh model**: mechanical sections auto-refresh on commit hook; tribal sections require human re-interview.
8. **Hybrid pattern**: upfront for what's stable and high-signal; on-demand (glob/grep/graphify queries) for everything else.

## Sources

- [[agents-md-spec]] — Agentic AI Foundation, August 2025 (high confidence, primary spec)
- [[evaluating-agents-md-eth]] — Gloaguen et al., ETH Zurich, 2026-02-12 (high confidence, only rigorous evaluation)
- [[aider-repo-map]] — Paul Gauthier, Aider, 2023-10-22 (high confidence, canonical reference)
- [[anthropic-context-engineering]] — Anthropic Engineering, 2025 (high confidence, vendor authority)
- [[anthropic-contextual-retrieval]] — Anthropic, 2024-09 (high confidence, strongest published retrieval numbers)
- [[racg-survey-2025]] — Tao, Qin, Liu, 2025 (high confidence, comprehensive landscape survey)

## Research Metadata

- Rounds: 2 (Round 1: 6 parallel searches + 5 deep fetches; Round 2: 2 search + 2 fetch gap-fill)
- Total searches: 8
- Total fetches: 7
- Sources cited: 6 primary
- Pages created this session: 14 (6 sources, 5 concepts, 2 entities, 1 synthesis)
- Date: 2026-05-09
