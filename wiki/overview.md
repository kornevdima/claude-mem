---
type: overview
title: "Wiki Overview"
created: 2026-04-07
updated: 2026-07-04
tags:
  - meta
  - overview
status: evergreen
related:
  - "[[index]]"
  - "[[hot]]"
  - "[[log]]"
  - "[[LLM Wiki Pattern]]"
sources:
---

# Wiki Overview

Navigation: [[index]] | [[log]] | [[hot]]

---

## Purpose

This is the **claude-mem design wiki**: the knowledge base behind the claude-mem plugin itself (the repo doubles as plugin source, Obsidian vault, and working repo). It holds the research, design decisions, and audit lessons that shaped the skills in `skills/` and the workers in `agents/` — the [[LLM Wiki Pattern]] applied to its own development.

---

## Current State

- Wiki pages: 80 (32 concepts, 16 entities, 23 sources, plus comparisons / questions / meta)
- Raw sources on disk: 8 (`.raw/`), 5 tracked in `.raw/.manifest.json`
- Last activity: 2026-07-04 — pm-layer evals E1–E8 encoded as runnable fixtures (`skills/product-management-layer/evals/`) and the RLM follow-ups closed (`wiki/index.json` locator + wiki-query sub-answer caching); earlier same day: tier 3 metrics seam / mission-control + graphify grounding for ADLC workers (committed), tier 2 harness backlog (committed)

---

## What lives here

- **Pattern & memory research** — [[LLM Wiki Pattern]], [[Hot Cache]], [[Compounding Knowledge]], [[Context Rot]], [[Recursive Language Models]], [[Contextual Retrieval]], [[Wiki vs RAG]]
- **Harness & agent design** — [[Generator-Evaluator Pattern]], [[Multi-Agent Communication Taxonomy]], [[Validation Contract]], [[Structured Handoff]], [[Domain-Specific Agents]], [[Vertical Slices for Agent Tasks]], [[Grilling Session]]
- **Shipped skill designs** — [[Product Management Layer Skill]] (incl. evals E1–E8), [[Project Profile Skill Suite]], [[graphify-integration]], [[SDLC Wiki Concerns]], [[Wiki Sharing Patterns]] (operational protocol: `skills/wiki/references/team-sync.md`), [[RLM-Optimized Wiki Querying]] (wiki-query large-vault mode + `index.json` locator)

---

## Key Themes

**Knowledge compounds.** Unlike RAG, the wiki pre-compiles synthesis. Cross-references are already there. Contradictions are flagged. Every ingest enriches existing pages rather than adding isolated chunks.

**The hot cache is the force multiplier.** A ~500-word file captures recent context. New sessions start with full context at minimal token cost.

**Plans rot; as-built knowledge compounds.** Point-in-time planning docs get archived as `delivered` once shipped; maintained as-built pages are what future agents trust (rule now enforced by the `wrap-up` skill).

**Every harness rule traces to a real failure.** The 2026-07-03 hardening pass encoded production audit findings — env-dependent PASSes, stubbed-integration "VERIFIED", doc-first claims falsified against code — as worker prompt rules, not folklore.

**Obsidian is the IDE, Claude is the programmer.** The graph view shows what's connected. The human curates sources and asks questions. Claude writes and maintains everything else.
