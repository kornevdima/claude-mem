---
type: source
title: "Building a Better Repository Map with Tree-sitter (Aider)"
source_type: vendor-engineering-blog
author: "Paul Gauthier (Aider)"
date_published: 2023-10-22
url: "https://aider.chat/2023/10/22/repomap.html"
created: 2026-05-09
updated: 2026-05-09
confidence: high
tags:
  - source
  - aider
  - repo-map
  - tree-sitter
  - codebase-understanding
status: current
related:
  - "[[Repo Map]]"
  - "[[Aider]]"
  - "[[Context Engineering for Coding Agents]]"
  - "[[Research Pre-computed Context for Coding Agents]]"
key_claims:
  - "Aider parses source with tree-sitter into ASTs to extract symbol definitions and references"
  - "Files are ranked with PageRank on the dependency graph; chat context personalizes the ranking"
  - "Map fits a configurable token budget (default 1K tokens)"
  - "Map includes signatures and key identifiers, not full implementations"
  - "Supports 130+ languages via tree-sitter parsers"
---

# Source: Building a Better Repository Map with Tree-sitter (Aider)

**Author**: Paul Gauthier (Aider)
**Published**: 2023-10-22 (still the canonical reference for Aider's design)
**URL**: https://aider.chat/2023/10/22/repomap.html

## Summary

Aider's repo-map is the most-copied technique for giving coding agents a compressed, structural view of an unfamiliar codebase. It addresses the brute-force problem ("send whole files") by extracting only the symbols that are most-referenced and fitting them within a token budget.

## How it works

1. **Tree-sitter parsing**: every source file is parsed into an AST. Tree-sitter has parsers for 130+ languages.
2. **Symbol extraction**: from each AST, pull out function definitions, class definitions, methods, types, top-level variables, plus *references* to those symbols across other files.
3. **Dependency graph**: build a graph where each file is a node, edges connect files that reference each other's symbols.
4. **PageRank**: run NetworkX PageRank over the graph. Ranking is *personalized* based on what files are currently in the chat context — files near the working set get boosted.
5. **Budgeted output**: select the top-ranked symbols that fit within `--map-tokens` (default **1,024 tokens**). Show signatures and key lines, not full bodies.

## What's in the map vs what isn't

**Included**: function/class signatures, method declarations, key variable definitions, the few "critical" lines per definition.

**Excluded**: full implementation bodies, less-referenced internals, comments, imports, boilerplate.

The intuition: GPT needs to know *what exists and how it connects*, not *how it's implemented*. Implementation comes from on-demand file reads.

## Token budget rationale

Default 1K tokens is small on purpose. The goal isn't to fit the codebase; it's to give the agent enough scaffolding to know which files to ask for next. Anything bigger competes with the actual task prompt.

## Reported limitations

- "For large repositories even just the repo map might be too large for GPT's context window." Token-budget capping mitigates but doesn't solve.
- No published quantitative benchmark in this article. Improvement is described qualitatively.

## Why this matters for project-profile design

- Repo-map is the **structural** complement to AGENTS.md's **convention** content. They answer different questions.
- Aider's choice of **1K tokens default** is a strong empirical prior on the right size for this kind of artifact.
- PageRank-on-dependency-graph is the right algorithm for "what matters most" — claude-mem's `graphify` already produces the underlying graph, so the same ranking is one query away.
- The "personalized by chat context" trick is huge: the same repo-map is rendered differently depending on what files are open. This argues for **on-demand, parameterized** generation rather than a single static artifact.

## Evolution from ctags

Aider's older approach used ctags. Switching to tree-sitter gave: full signatures (not just names), better structural fidelity, broader language coverage.

## Connections

- [[Repo Map]] — concept page generalizing this technique
- [[Aider]] — entity page
- [[graphify-integration]] — claude-mem's structural-layer skill, which produces graph data the same shape Aider's PageRank consumes
- [[Project Profile]]
