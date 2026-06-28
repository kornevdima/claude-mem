---
type: meta
title: "Hot Cache"
updated: 2026-06-28
tags:
  - meta
  - hot-cache
status: evergreen
related:
  - "[[index]]"
  - "[[log]]"
  - "[[Research Recursive Language Models]]"
  - "[[RLM-Optimized Wiki Querying]]"
  - "[[Recursive Language Models]]"
---

# Recent Context

Navigation: [[index]] | [[log]]

## Last Updated

**2026-06-28 (autoresearch: Recursive Language Models)**: Filed 9 pages on RLMs (Zhang, Kraska, Khattab, MIT CSAIL; arXiv 2512.24601). Synthesis at [[Research Recursive Language Models]]; application design at [[RLM-Optimized Wiki Querying]].

## Key Recent Facts

- **RLM** = inference strategy: long context lives in a REPL as a variable; the model gets only the query, then greps/chunks/prints it and recursively calls sub-LMs (`rlm_query`, depth=1). Sidesteps [[Context Rot]]; scales to 10M+ tokens. (Source: [[rlm-blog-zhang]], [[rlm-paper-arxiv]])
- Reported +26% vs GPT-5 compaction / +130% vs CodeAct-sub-calls / +13% vs Claude Code at comparable cost (medium confidence; [[rlm-reproduction-overthink]] confirms direction, warns on over-recursion/latency).
- **Application to claude-mem**: the ADLC agent has bash over `wiki/`, which is the RLM precondition (vault = environment, bash = REPL). Evolve `wiki-query` to **grep-first + bounded recursion** (peek hot.md, rg matches, recurse per large area via sub-agents, synthesize). Do not rebuild structure; reinforce greppable frontmatter, `_index.md`, short pages, stable IDs.

## Recent Changes

- Created: the 9 RLM pages (4 sources, 1 entity, 3 concepts, 1 synthesis). See [[log]].
- Index/log updated; total pages 51 -> 60.

## Active Threads

- **RLM -> wiki-query**: design filed; not yet implemented. Open: ship as `wiki-query` evolution vs a large-vault mode flag; whether `wiki/index.json` is needed at scale; sub-answer caching to `questions/`.
- **ADLC mode (Phase 11, in code not this wiki)**: shipped this session in `skills/wiki/references/` + `agents/` + `skills/wrap-up/` + hooks + `permissions.md` + `mcp-setup.md` + `technical-planning.md`. Two workers: `ba-suite-subagent`, `architecture-subagent`. Uncommitted on `main`. Tracked in the roadmap memory (Phase 11).
