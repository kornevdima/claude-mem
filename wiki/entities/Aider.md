---
type: entity
title: "Aider"
entity_type: project
role: "AI pair-programming CLI; originator of the tree-sitter repo-map pattern"
first_mentioned: "[[Repo Map]]"
created: 2026-05-09
updated: 2026-05-09
tags:
  - entity
  - project
  - coding-agent
  - aider
status: current
related:
  - "[[Repo Map]]"
  - "[[Context Engineering for Coding Agents]]"
  - "[[aider-repo-map]]"
sources:
  - "[[aider-repo-map]]"
---

# Aider

Open-source CLI tool for AI pair-programming with LLMs. Created by Paul Gauthier. Notable in this wiki as the originator of the tree-sitter + PageRank **repo-map** technique — now widely copied across the coding-agent ecosystem.

## Why it matters here

Aider was one of the earliest agentic-coding tools to take "context window economics" seriously. Their 2023 blog post on building a better repo map (Source: [[aider-repo-map]]) is still the canonical reference for compressing a codebase into a small, signature-only structural summary that fits a token budget.

## Key technical contributions

- **Tree-sitter-based AST extraction** for 130+ languages.
- **PageRank over the dependency graph** to rank symbols by importance.
- **Personalized ranking** — the same repo-map renders differently depending on which files are currently in the chat context.
- **Token-budgeted output** (`--map-tokens`, default 1K).
- **Native AGENTS.md support** — Aider reads it like other agents do.

## Influence

The repo-map pattern is now reproduced in:

- **RepoMapper** — standalone reimplementation.
- **MCP servers** wrapping the algorithm for use in other agents.
- **Sourcegraph Cody** — uses similar PageRank ideas on top of SCIP code graphs.
- **claude-mem `graphify`** — same AST + community detection foundation, with richer semantic clustering on top.

## Limitations Paul Gauthier acknowledges

- The map can still be too large for very big repos even with budget capping.
- No published quantitative benchmark of repo-map's specific contribution to task success.
- Tree-sitter language coverage varies in completeness.

## Connections

- [[Repo Map]] — concept page generalizing the pattern
- [[aider-repo-map]] — primary blog post source
- [[graphify-integration]] — claude-mem's richer take on the same idea
