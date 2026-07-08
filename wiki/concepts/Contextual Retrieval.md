---
type: concept
title: "Contextual Retrieval"
complexity: intermediate
domain: ai-agents
aliases:
  - "Contextual Embeddings"
  - "Contextual BM25"
created: 2026-05-09
updated: 2026-07-03
tags:
  - concept
  - rag
  - retrieval
  - prompt-caching
status: current
related:
  - "[[Context Engineering for Coding Agents]]"
  - "[[Hot Cache]]"
  - "[[anthropic-contextual-retrieval]]"
sources:
  - "[[anthropic-contextual-retrieval]]"
---

# Contextual Retrieval

A RAG technique that prepends LLM-generated explanatory context to each chunk before embedding and indexing, so retrieval works on chunks that carry their own anchoring rather than naked fragments. Published by Anthropic in late 2024 (Source: [[anthropic-contextual-retrieval]]).

## The Problem It Solves

Standard chunking strips context. A chunk reading "The company's revenue grew 3% over the previous quarter" is useless without knowing which company and which quarter — but those facts live in surrounding paragraphs the chunk no longer has access to.

## The Technique

Before embedding/indexing, prepend a short LLM-generated paragraph to each chunk:

> Prompt used: "Please give a short succinct context to situate this chunk within the overall document for the purposes of improving search retrieval of the chunk." (Source: [[anthropic-contextual-retrieval]])

The generated context is **50-100 tokens**. Both retrieval methods get the prepended chunk:

- **Contextual Embeddings** — semantic similarity over the enriched chunk
- **Contextual BM25** — exact-term match over the enriched chunk

Both retrieve candidates independently. Rank fusion merges results. Top-K passes to the model.

## Quantitative results

The strongest published numbers on retrieval improvements:

| Configuration | Top-20 retrieval failure | Reduction |
|---|---|---|
| Baseline (embeddings + BM25) | 5.7% | — |
| + Contextual Embeddings | 3.7% | **-35%** |
| + Contextual BM25 | 2.9% | **-49%** |
| + Reranking (Cohere/Voyage) | 1.9% | **-67%** |

(Source: [[anthropic-contextual-retrieval]])

## Cost economics

- One-time preprocessing: ~**$1.02 per million document tokens** with Claude Haiku + prompt caching.
- Caching the document means generating contexts for many chunks doesn't pay full document-input cost each time. Prompt caching is what makes this affordable.

## When NOT to use it (the load-bearing recommendation)

> "If your knowledge base is smaller than 200,000 tokens (about 500 pages of material), you can just include the entire knowledge base in the prompt that you give the model, with no need for RAG or similar methods. Prompt caching makes this approach significantly faster and more cost-effective." (Source: [[anthropic-contextual-retrieval]])

For most projects' "important context" (AGENTS.md + key file summaries + decision log + index), the answer is **no RAG, just cache the whole thing**.

## Empirical guidance

- Embedding models tested: Gemini and Voyage performed best.
- Number of retrieved chunks: 20 outperformed 5 or 10.
- Reranking is the cheapest single additional improvement.
- Chunk sizing heuristic: chunks range ~10–500 tokens, and the **ideal chunk is a single self-contained assertion / concrete fact** — not an arbitrary text window. A chunk that already states its subject needs less prepended context. (Source: [[orlov-rag-wiki-llm-graphify]])

## Why this matters here

- For claude-mem's wiki vault scale (a few hundred to a few thousand pages), the right answer is **prompt-cached upfront context**, not chunked RAG.
- Hot cache + index already exploits this.
- For graphify's structural data, the graph itself **is** the contextual prefix for each symbol — same insight applied to code.
- The 67% failure-reduction ceiling is a useful upper bound; don't expect retrieval to be much better than that.

## Connections

- [[anthropic-contextual-retrieval]] — primary source
- [[Hot Cache]] — claude-mem's existing application of the "just include it" recommendation
- [[Context Engineering for Coding Agents]]
