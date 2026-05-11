---
type: source
title: "Contextual Retrieval (Anthropic)"
source_type: vendor-engineering-blog
author: "Anthropic"
date_published: 2024-09
url: "https://www.anthropic.com/news/contextual-retrieval"
created: 2026-05-09
updated: 2026-05-09
confidence: high
tags:
  - source
  - anthropic
  - rag
  - retrieval
  - prompt-caching
status: current
related:
  - "[[Contextual Retrieval]]"
  - "[[Context Engineering for Coding Agents]]"
  - "[[Research Pre-computed Context for Coding Agents]]"
key_claims:
  - "Contextual Embeddings cut top-20-chunk retrieval failure 35% (5.7% to 3.7%)"
  - "Contextual Embeddings + Contextual BM25 cut failure 49% (5.7% to 2.9%)"
  - "Adding reranking cuts failure 67% (5.7% to 1.9%)"
  - "Preprocessing cost: $1.02 per million document tokens"
  - "Below 200K tokens: skip RAG entirely, use prompt caching with full doc in context"
---

# Source: Contextual Retrieval (Anthropic)

**Author**: Anthropic
**URL**: https://www.anthropic.com/news/contextual-retrieval

## Summary

Anthropic's published technique for fixing the "lost context when chunking" problem in RAG. Important here for two reasons: (1) the quantitative results are the strongest published numbers on retrieval improvements, (2) the recommendation about *when not to use RAG* is directly relevant to project-profile design.

## The technique

Standard chunking strips context. A chunk reading "The company's revenue grew 3% over the previous quarter" has no anchor: which company, which quarter?

Contextual Retrieval prepends a short LLM-generated explanation to each chunk before embedding/indexing:

> Prompt used: "Please give a short succinct context to situate this chunk within the overall document for the purposes of improving search retrieval of the chunk."

The generated context is **50-100 tokens** per chunk, prepended before both:
- Embedding (Contextual Embeddings)
- BM25 indexing (Contextual BM25)

Both methods retrieve candidates independently, results are fused via rank fusion, top-K passes to the LLM.

## Quantitative results (the table that matters)

| Configuration | Top-20 retrieval failure rate | Reduction vs baseline |
|---|---|---|
| Baseline embeddings + BM25 | 5.7% | — |
| + Contextual Embeddings | 3.7% | **-35%** |
| + Contextual BM25 | 2.9% | **-49%** |
| + Reranking (Cohere/Voyage) | 1.9% | **-67%** |

These are the strongest published numbers on retrieval improvements as of late 2024.

## Cost economics

- One-time preprocessing: **$1.02 per million document tokens** (using Claude Haiku + prompt caching).
- Prompt caching is what makes this affordable — caching the document means generating contexts for many chunks doesn't pay full document-input cost each time.

## When NOT to use it

> "If your knowledge base is smaller than 200,000 tokens (about 500 pages of material), you can just include the entire knowledge base in the prompt that you give the model, with no need for RAG or similar methods. Prompt caching makes this approach significantly faster and more cost-effective."

This is the load-bearing recommendation for our context. Most projects' "important context" (AGENTS.md + key file summaries + decision log) fits well under 200K tokens. **For project-scale knowledge, the right answer may be no-RAG-just-cache, not contextual retrieval.**

## Other empirical guidance

- Embedding models tested: Gemini and Voyage performed best.
- Number of retrieved chunks: 20 outperformed 5 or 10.
- Reranking (Cohere or Voyage) is the cheapest single additional improvement.

## What this changes in design

- For claude-mem's wiki-vault scale (hundreds to a few thousand pages), **prompt caching of the index + hot cache + relevant pages** is empirically more efficient than chunked RAG. The current design is right.
- For graphify's structural data, the graph is the equivalent of "context that situates each symbol." That's exactly the contextual-retrieval insight applied to code.
- The 67% failure-reduction ceiling with full reranking is a useful upper bound. Don't expect retrieval to be much better than that.

## Connections

- [[Contextual Retrieval]] — concept page
- [[anthropic-context-engineering]] — companion principles source
- [[Hot Cache]] — claude-mem's existing design that exploits the "just put it in the prompt" recommendation
