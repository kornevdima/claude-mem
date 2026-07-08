---
type: concept
title: "Graphify Integration"
complexity: intermediate
domain: claude-mem
created: 2026-04-26
updated: 2026-07-03
tags:
  - concept
  - graphify
  - architecture
  - design-decision
status: developing
related:
  - "[[hot]]"
  - "[[maintenance-triggers]]"
  - "[[LLM Wiki Pattern]]"
---

# Graphify Integration

How claude-mem layers a structural code graph on top of the narrative wiki, and why we built it the way we did.

---

## The split: structural vs narrative

Two layers, two data shapes, one vault.

| Layer | What it captures | Owned by | Updates how |
|---|---|---|---|
| **Structural** | What the code *is* — modules, calls, types, communities, AST edges | graphify | Manual `/graphify-update` after each feature |
| **Narrative** | What the code *means* — decisions, rationale, trade-offs, history | claude-mem wiki | `/save`, `wiki-ingest`, manual edit |

**Rule**: if a fact is derivable from the AST, it lives in the graph. If it's a reason a human chose something, it lives in the wiki.

---

## Why we picked Option C (coexist + glue)

When integrating graphify, three options were on the table:

- **A** — Coexist as peers, both plugins installed independently
- **B** — Wrap graphify as a backend, claude-mem skills proxy the calls
- **C** — Recommend graphify alongside, write only the glue (one-line wiki-query update + scaffold prompts + lint cross-checks)

**We chose C.** Reasoning:

1. graphify is mature and ships its own polished Claude Code integration — wrapping adds maintenance burden for marginal benefit
2. The real value-add for claude-mem is the **knowledge synthesis layer on top** — hot cache, lint, domain folders, multi-mode vaults
3. Decoupling lets either side evolve independently
4. The glue (wiki-query routing, wiki-lint graph checks, wiki/code/ summaries) is small and high-leverage

What we ended up building is a refined Option C with two custom skills (`graphify-ingest`, `graphify-update`) that orchestrate graphify rather than wrap it.

---

## File layout (canonical)

```
project-root/
├── src/                          ← code (untouched by claude-mem)
├── graphify-out/                 ← graphify-owned, committed
│   ├── graph.json                ← queryable NetworkX graph
│   ├── labels.json               ← cluster_id → human label (committed!)
│   ├── GRAPH_REPORT.md           ← god nodes, surprises, suggested questions
│   ├── graph.html                ← interactive viz (committed)
│   ├── cache/                    ← per-file SHA256 (speeds re-runs)
│   └── memory/                   ← Q&A feedback loop
└── wiki/                         ← claude-mem-owned
    ├── index.md, hot.md, log.md
    ├── code/                     ← graphify-derived summaries (regenerated)
    │   ├── _index.md
    │   ├── _COMMUNITY_NN_<slug>.md
    │   └── graph.canvas
    ├── decisions/                ← human ADRs (the WHY)
    ├── concepts/                 ← domain knowledge
    └── sources/                  ← ingested external docs
```

---

## Jaccard label preservation

The hardest design problem: cluster IDs aren't stable across Louvain re-runs, but we want labels to survive incremental updates.

**Algorithm** (in `skills/graphify-update/scripts/update.py`):

1. Before merge: snapshot old communities (cluster_id → set of node_ids) from existing `graph.json`
2. Re-cluster the merged graph → new communities with new IDs
3. For each NEW cluster with ≥3 members: compute Jaccard similarity (member set overlap) against every OLD labeled cluster
4. If best match Jaccard ≥ **0.6**: inherit the old label
5. Otherwise: flag as "needs Claude labeling," sample 18 member labels for context

**Threshold tuned on a real run**: 0.7 was too strict (a single touched file dropped a clearly-same cluster from 0.74 to 0.64); 0.6 captures legitimate continuity while flagging genuine splits.

**Important**: only labeled clusters (≥3 members in the OLD graph) count as inheritance candidates. Singletons matching singletons would inherit junk placeholder labels.

---

## Edge-drop fix via AST ID hints

Discovered in our first Path B test: 604 edges were silently dropped at merge because semantic subagents invented ID names that didn't match what the AST extractor produced (e.g., agent guessed `submit_to_hubspot` for the symbol, AST had `hubspot_submittohubspot`).

**Fix**: `chunks.py` pre-extracts AST nodes and includes the per-file AST IDs in each subagent's prompt. The agent is instructed to use those exact IDs when creating edges to known symbols. Edge drop is still nonzero (~25% on Next.js) but much better than starting at zero.

---

## labels.json poisoning gotcha

`graphify-out/labels.json` and `graphify-out/graph.json` MUST come from the same run. If something writes one without the other (manual edit, partial test run, copy from older state), `update.py` will faithfully PRESERVE the wrong labels via Jaccard inheritance — every subsequent update locks in the mismatch.

**Symptom**: `wiki-lint` reports `FAIL` "title is X but labels.json[N] = Y" on `_COMMUNITY_NN_*.md` pages.

**Fix**: re-run `/graphify-ingest` to recompute labels from scratch. Don't try to repair labels.json by hand.

This is documented in [[maintenance-triggers]] (§negative triggers) and `skills/wiki-lint/scripts/lint_graph.py` checks for it explicitly.

---

## Subagent dispatch pattern

`graphify-extract-subagent` (defined in `agents/graphify-extract-subagent.md`) is dispatched by both `/graphify-ingest` (8–10 chunks for first build) and `/graphify-update` (1–2 chunks for changed docs only).

**Pattern**: all Agent tool calls in a single message → run concurrently. `model: "sonnet"` for cost. Each subagent writes JSON to `graphify-out/.graphify_chunk_NN.json` (file existing on disk = success signal). Worker prompt is centralized in the agent file, not duplicated in skills.

---

## Cost reality

Tested on a 169-file Next.js codebase (esg-website):

| Operation | Cost | Time |
|---|---|---|
| `/graphify-ingest` (Path B, no images) | ~$2 | ~2 min |
| `/graphify-ingest --include-images` (118 images) | ~$8–20 | ~5 min |
| `/graphify-update` after touching 1 code file | $0 | ~10 sec |
| `/graphify-update` after editing 3 docs | ~$0.30 | ~30 sec |

---

## External claims about graphify (third-party)

From [[orlov-rag-wiki-llm-graphify]] (2026-06, auto-transcript — figures are the speaker's claims, not verified):

- Positions graphify as the "third wave" of agent memory, between RAG and the [[LLM Wiki Pattern]]: mechanical decomposition like RAG, explicit relations like a wiki, stored as JSON nodes + edges.
- Claims input coverage beyond ours: **video and audio files** as graph inputs (step 2 of its pipeline, requires an AI key). Our `graphify-ingest` covers code, docs, and images only.
- Confirms our layering: step 1 (code + text) runs on bundled Python scripts with **no LLM cost** — matches our $0 code-only update row above.
- Claims token savings of "50x, even 70x" on projects with thousands of files. Marketing-grade number; our measured costs are in the table above.
- Scale caveat worth adopting: graphify adds little on projects of ~10–20 files; the payoff starts at large file counts. Our skills don't currently gate or advise on this.
- Author name and star count in the transcript are garbled — do not cite them.

---

## What's still incomplete

- **Hooks not wired** for auto-update on session end. By design — user said they prefer manual control via `/graphify-update`.
- **No incremental cluster-aware regeneration**: every run rewrites all `wiki/code/_COMMUNITY_*.md` even if only one cluster changed. Acceptable for current scale.
- **Path B image extraction is expensive**: each image is its own subagent (graphify default). Skip unless visual concepts genuinely matter for the codebase.
