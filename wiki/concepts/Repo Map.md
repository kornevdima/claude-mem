---
type: concept
title: "Repo Map"
complexity: intermediate
domain: ai-agents
aliases:
  - "Repository Map"
  - "Aider Repo Map"
  - "Repository Mapping"
created: 2026-05-09
updated: 2026-05-09
tags:
  - concept
  - repo-map
  - tree-sitter
  - codebase-understanding
status: current
related:
  - "[[Context Engineering for Coding Agents]]"
  - "[[Aider]]"
  - "[[graphify-integration]]"
  - "[[aider-repo-map]]"
sources:
  - "[[aider-repo-map]]"
  - "[[racg-survey-2025]]"
---

# Repo Map

A compressed, structural representation of a codebase that gives a coding agent enough scaffolding to know what exists and how it connects without including any full implementations. Originated by [[Aider]] in 2023, now copied across the ecosystem (Source: [[aider-repo-map]]).

## The Core Idea

Sending whole files to the agent is wasteful: most of the bytes are implementations the agent doesn't need to *understand*, only to *fetch when relevant*. The repo map is the inverse: signatures and key identifiers, ranked by importance, fitting in a small token budget.

## How it's built (Aider's reference design)

1. **AST extraction** — parse every source file with tree-sitter (130+ languages supported). Pull out function/class/method definitions and their references.
2. **Dependency graph** — files are nodes, edges connect files that reference each other's symbols.
3. **PageRank** — rank nodes by importance (most-referenced wins). The ranking is **personalized** by what files are currently in the working chat context, so the same repo renders different maps depending on the task.
4. **Budget-fit** — select the top-ranked symbols that fit the token budget (`--map-tokens`, default **1,024 tokens**).

## What's in it vs what's left out

Included:
- Function and method signatures
- Class definitions
- Type declarations
- Top-level variables (when referenced)
- The few critical lines per definition

Excluded:
- Function bodies
- Imports
- Comments
- Boilerplate
- Anything not in the top-ranked subset

## Why 1K tokens

Default 1K is small on purpose. The map's job is **scaffolding for the agent's next read**, not a self-contained codebase summary. Bigger competes with the actual task prompt and trips the same diminishing-returns problem [[anthropic-context-engineering]] warns about.

## When it helps and when it doesn't

From the broader literature ([[racg-survey-2025]]):

- **Helps**: tasks that span multiple files, require global naming consistency, or need cross-module reasoning.
- **Less useful**: small isolated edits where one file holds all the relevant context.
- **Trade-off**: graph-based approaches "excel at capturing architectural and dependency relationships, making it particularly suited for tasks involving global consistency or cross-file reasoning" but introduce "challenges in preprocessing, graph maintenance, and computational overhead."

No published quantitative benchmarks confirm specific success-rate lifts (the original Aider blog reports only qualitative improvement).

## Variants in the ecosystem

- **Aider** — the canonical implementation, tree-sitter + PageRank.
- **claude-mem `graphify`** — produces a richer graph (entities, edges, hyperedges, communities) that subsumes repo-map data and adds semantic clustering. See [[graphify-integration]].
- **Sourcegraph Cody** — uses SCIP code graph as a backend for context retrieval; closer to "queryable repo map" than static artifact. (Source: search results, sourcegraph.com)
- **RepoMapper** — open-source extraction of Aider's logic into a standalone tool / MCP server.

## What this contributes to project-profile design

- The 1K-token default is a strong empirical prior on size for "structural" context.
- PageRank-on-dependency-graph is the right algorithm; graphify already produces the graph.
- The "personalized by chat context" trick says the artifact should be **on-demand and parameterized**, not a frozen snapshot.
- Repo map answers structural questions; AGENTS.md answers convention questions. Project profile likely needs both.

## Connections

- [[aider-repo-map]] — primary source
- [[Aider]] — entity
- [[graphify-integration]] — claude-mem's structural layer (richer than vanilla repo-map)
- [[Context Engineering for Coding Agents]]
- [[Project Profile]]
