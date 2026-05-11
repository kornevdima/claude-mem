---
type: source
title: "Retrieval-Augmented Code Generation Survey (Tao et al., 2025)"
source_type: peer-reviewed-survey
author: "Yicheng Tao, Yao Qin, Yepang Liu"
date_published: 2025
url: "https://arxiv.org/html/2510.04905v1"
created: 2026-05-09
updated: 2026-05-09
confidence: high
tags:
  - source
  - survey
  - rag
  - code-generation
  - repository-level
status: current
related:
  - "[[Context Engineering for Coding Agents]]"
  - "[[Repo Map]]"
  - "[[Research Pre-computed Context for Coding Agents]]"
key_claims:
  - "RACG splits into non-graph (lexical/semantic) and graph-based (AST/call/dependency) approaches"
  - "Graph-based excels at cross-file reasoning and global consistency"
  - "Vector-based offers ease of deployment but lacks structural awareness"
  - "Iterative agentic retrieval outperforms one-shot for repo-scale tasks"
  - "RAG is NOT universally superior; effectiveness is context-dependent"
---

# Source: Retrieval-Augmented Code Generation Survey

**Authors**: Yicheng Tao, Yao Qin, Yepang Liu
**Published**: 2025
**URL**: https://arxiv.org/html/2510.04905v1

## Summary

Comprehensive survey of retrieval-augmented code generation (RACG) at the repository level. Useful here as the **landscape map**: tells us which families of approach exist and which trade-offs they make.

## Two-part taxonomy

**Non-graph-based RAG**: lexical/semantic similarity over chunks, no explicit graph construction. Sub-types:
- Retrieval strategy optimization (better embeddings, hybrid search)
- Retrieval content construction (chunking strategies)
- Static analysis integration (dataflow, type info)

**Graph-based RAG**: explicit code-structure graphs (ASTs, call graphs, dependency graphs). Nodes = code entities, edges = relationships (calls, inheritance, imports).

> "Non-graph-based and graph-based RAG approaches represent two complementary and increasingly interconnected research directions."

## Best-method-per-task findings

- **Uncommon APIs**: retrieval "substantially improves code generation accuracy" (Chen et al., cited in survey).
- **General**: "BM25 retrieval and Sequential Integration Fusion strike an appealing balance of simplicity and effectiveness" (Yang et al., cited).
- **Universal verdict**: "RAG is not universally superior" — effectiveness is context-dependent.

## Repository-level context types identified as critical

- Cross-file dependencies and global semantic consistency
- Structural information (class hierarchies, type definitions)
- API signatures and documentation
- Project-wide naming conventions
- Module / package relationships

This is the literature's answer to the user's design question: *what's worth pre-computing*. Note that "naming conventions" is on the list — supports the project-profile concept.

## Graph-based vs vector-based trade-off

| Dimension | Graph-based | Vector-based |
|---|---|---|
| Cross-file reasoning | Strong | Weak |
| Global consistency | Strong | Weak |
| Preprocessing cost | High | Low |
| Maintenance | Complex | Simple |
| Deployment ease | Hard | Easy |
| Heterogeneous repos | Struggles | Generalizes |

> "While graph-based methods offer high fidelity and structural awareness, they also introduce challenges...especially when applied to large-scale, heterogeneous repositories."

## Agentic / iterative vs one-shot

The survey identifies a "level" progression:
- Level 0: traditional non-agent retrieval (one-shot)
- Level 1: partial agent (some iteration)
- Level 2: fully autonomous agent frameworks (multi-step retrieval, reflection, tool use)

RepoCoder (cited) introduced iterative retrieval — "retrieved context is progressively refined over multiple rounds." This is now standard for repo-scale tasks.

## What this contributes to project-profile design

- **Both layers needed**: claude-mem's `wiki/` (vector-similar narrative) + `graphify/` (graph) maps cleanly onto the survey's taxonomy. The hybrid is the right answer.
- The "naming conventions" being explicitly listed as a critical context type validates the project-profile concept.
- Iterative retrieval beats one-shot — argues for the `wiki-query` skill's tiered (quick/standard/deep) modes.
- "Effectiveness is context-dependent" — no universal recipe. The skill should let the user dial intensity.

## Limits

- Survey, not original measurement. Numbers are second-hand.
- Coverage of agentic-retrieval is shallower than non-agent.

## Connections

- [[Context Engineering for Coding Agents]]
- [[Repo Map]]
- [[Research Pre-computed Context for Coding Agents]]
- [[graphify-integration]] — claude-mem's graph-based layer
