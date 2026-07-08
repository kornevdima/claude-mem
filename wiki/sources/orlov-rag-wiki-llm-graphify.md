---
type: source
title: "Orlov — AI Agent Memory: from RAG to Karpathy's Wiki LLM to Graphify"
source_type: video-transcript
url: https://youtu.be/kQWSOAaw7BQ
channel: "Орлов (Orlov)"
published: 2026-06-27
ingested: 2026-07-03
language: uk
raw: ".raw/yt-orlov-ai-agent-memory-wiki-llm.md"
reliability: "auto-generated transcript; names, dates, and numbers are low-confidence"
created: 2026-07-03
updated: 2026-07-03
tags:
  - source
  - transcript
  - rag
  - llm-wiki
  - graphify
status: current
related:
  - "[[LLM Wiki Pattern]]"
  - "[[Wiki vs RAG]]"
  - "[[graphify-integration]]"
  - "[[Andrej Karpathy]]"
  - "[[Orlov]]"
  - "[[Contextual Retrieval]]"
  - "[[sources/_index]]"
---

# Orlov — AI Agent Memory: from RAG to Wiki LLM to Graphify

Ukrainian-language YouTube explainer (channel [[Orlov]], 2026-06-27) that narrates the evolution of agent memory as **three waves**: RAG (vector databases) → [[Andrej Karpathy]]'s Wiki LLM pattern → Graphify (code/knowledge graphs). Includes two live demos: building a Wiki LLM vault in Obsidian with Antigravity + Gemini 3.1 Pro, and running graphify on the author's own project.

> [!warning] Transcript quality
> The source is an auto-generated Ukrainian transcript. Proper names, star counts, and dates are garbled in places (e.g. graphify's author rendered as "Saffish Hamsy", "72 000 GitHub stars"). Treat all specific figures below as the speaker's claims, not verified facts.

---

## Wave 1 — RAG

- Motivation: knowledge cutoff → hallucination; small contexts can be pasted inline, but at 10M–100M tokens of corpus you need retrieval.
- Standard pipeline described: clean/digitize sources → split into chunks → embed → vector DB; query is embedded and matched to semantically nearby vectors (car ≈ automobile example).
- **Chunk best practice**: a chunk is not a word or syllable fragment — it ranges from ~10 to ~500 tokens, and the *ideal chunk is a single self-contained assertion / concrete fact*.
- Stated weaknesses of RAG: the system never learns or improves (every query starts from scratch over raw chunks), it has no understanding of relations between entities (only semantic proximity), and contradictions between sources are silently ignored.
- Verdict: fine for e-commerce-style assistants, not for accumulating knowledge.

## Wave 2 — Karpathy's Wiki LLM

- Attributed to [[Andrej Karpathy]], proposed on **April 4** (2026); the speaker calls it the "second wave" (his own framing, no official status).
- Described as a plain-text instruction set telling an agent how to manage the information it can access; the key differentiator over RAG is that it **captures links between facts, objects, sources, and conclusions**, not just text.
- Demo: clip YouTube videos and web articles (marathon-training example) into an Obsidian vault via the web clipper; ask the agent (Antigravity + Gemini 3.1 Pro) to "make a skill for Wiki LLM per Karpathy's system"; the generated skill splits data into **raw inputs / wiki markdown / system files (index.md, log.md)** — the same three-layer shape as [[LLM Wiki Pattern]].
- index.md is presented as the file every coding agent (Antigravity, Claude, Codex) leans on — the indexation of all files and links.
- **Incremental ingest** highlighted: adding one new source re-analyzes only the new file and updates indexes/concepts, "saving many tokens on large projects."
- Demo detail: the generated wiki normalized all sources into one language (Ukrainian) regardless of source language.
- Speaker judges it more capable than NotebookLM because of controllability.
- RAG vs Wiki LLM summary given: raw chunks re-searched every time vs structured markdown searched directly; no relations vs wikilinks; contradictions ignored vs tracked and worked through; vector DB required vs none.

## Wave 3 — Graphify

- Framed as "currently the best existing system," conceptually **between RAG and Wiki LLM**: like Wiki LLM it builds a graph over all data in a folder; like RAG it divides information semantically — but into **JSON node files connected by graph edges**, not chunks.
- Claimed input coverage: text, code, video, audio, PDF, images — "everything."
- Install/run flow shown: install Python via brew → install graphify → install graphify as a per-project skill → run `graphify`.
- **Three-step pipeline** as described: (1) code + text files processed by bundled Python scripts, *no LLM needed*; (2) video/audio — needs an AI key or the host model; (3) documents/PDF/images. Build takes 5–30 min depending on file count.
- Output: `graphify-out/` with a main graph JSON plus per-node JSON files, and an HTML visualization of connected nodes.
- Payoff claim: when asked to change site text, the agent "doesn't analyze the whole file system — it finds the node directly and fixes it."
- **Scale caveat**: near-useless for small projects (~10–20 files); real savings start at thousands of files, where token savings are "50x, or as they write, even 70x."
- Speaker's timeline musing: RAG appeared "in '21", ~5 years to Wiki LLM; expects the next wave sooner.

---

## Claims needing verification

> [!contradiction] Unverified biography claim about Karpathy
> The transcript says Karpathy "has now joined Anthropic." No existing wiki page or known source corroborates this; [[Andrej Karpathy]] records him as ex-OpenAI/ex-Tesla, later independent. Flagged on the entity page; auto-transcript, low confidence.

- RAG "appeared in 2021" — the RAG paper (Lewis et al.) is 2020; minor.
- graphify author name and "72 000 stars" — garbled; our own [[graphify-integration]] work is the more reliable record of what graphify actually is and does.
- "50–70x token savings" — vendor/marketing figure; compare with the measured cost table in [[graphify-integration]].

## What this source adds to the wiki

1. The **three-waves narrative** (RAG → Wiki LLM → graph) as a popular-audience mental model — now noted in [[Wiki vs RAG]].
2. The **ideal-chunk-is-an-assertion** heuristic — added to [[Contextual Retrieval]].
3. Independent evidence the [[LLM Wiki Pattern]] is spreading beyond the Claude ecosystem (Antigravity/Gemini implementation, non-dev personal use cases like training diaries).
4. External claims about graphify's multi-modal inputs and scale threshold — noted in [[graphify-integration]].
