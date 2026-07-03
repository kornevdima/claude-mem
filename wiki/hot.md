---
type: meta
title: "Hot Cache"
updated: 2026-07-03T23:59:00
tags:
  - meta
  - hot-cache
status: evergreen
related:
  - "[[index]]"
  - "[[log]]"
  - "[[Multi-Agent Communication Taxonomy]]"
  - "[[Domain-Specific Agents]]"
  - "[[Grilling Session]]"
---

# Recent Context

Navigation: [[index]] | [[log]]

## Last Updated

**2026-07-03 (harness audit + 5-talk ingest + wrap-up)**: Audited the ADLC harness against two production vaults' decision/verification trails, applied evidence-backed fixes (audit findings + tier 1) across the workers and dispatcher docs, batch-ingested 5 YouTube talks, filed the team-sync protocol, and closed with a wrap-up sync (rollups reconciled).

## Key Recent Facts

- **Production audit findings (two ADLC vaults):** failures cluster by worker — feature-tester specs assumed unseeded environment state (largest class); feature-verifier PASSes were environment-dependent and one "VERIFIED" shipped a bug because the integration was stubbed in e2e; BA/architecture workers authored doc-first claims later falsified against code (12 corrections in one vault); log.md hit ~7,000 lines carrying full records inline.
- **Harness fixes applied (committed, `bc511a3`):** verifier target-fingerprint + `ENV_MISMATCH` + "Not exercised" stub list + restart-once false-red protocol + records-as-pages; tester "preconditions are code, not assumptions" + honest tag flips; reviewer test-self-sufficiency dimension; planner code-grounding (`[UNVERIFIED — from docs]`) + contradiction cross-check; dispatcher rules in `technical-planning.md`; wrap-up rollup reconciliation; 4 new wiki-lint checks.
- **Model split (operator decision):** workers draft on Sonnet (now pinned on architecture- + ba-suite-subagents too); judgment/orchestration/re-verification live at the dispatcher (session model). Don't fix worker quality with model upgrades.
- **5 talks ingested** as sources: [[orlov-rag-wiki-llm-graphify]] (wiki-LLM pattern reproduced on non-Claude stacks), [[yt-schroeder-domain-specific-agents]] (composition of small complete agents), [[yt-alvoeiro-multi-agent-architecture]] (validation contracts, structured handoffs w/ exit codes, serial writers), [[yt-pocock-ai-coding-workflow]] (grilling, vertical slices, AFK loop, doc-rot lifecycle), [[campbell-after-ai-hype]] (same-model evaluation publicly failed; verify outcomes not reasoning).
- New concept pages: [[Multi-Agent Communication Taxonomy]], [[Validation Contract]], [[Structured Handoff]], [[Domain-Specific Agents]], [[Grilling Session]], [[Ralph Wiggum Loop]], [[Vertical Slices for Agent Tasks]], [[Deep Modules]].

## Recent Changes

- Edited: `agents/feature-{verifier,tester,reviewer,builder}.md`, `agents/{architecture,ba-suite}-subagent.md`, `agents/wiki-lint-subagent.md`, `skills/wrap-up/SKILL.md`, `skills/wiki/references/technical-planning.md`, `skills/wiki/references/shift-left/_index.md`.
- Ingested: 5 YouTube transcripts into `.raw/` (yt-dlp auto-subs, cleaned) → 80 wiki pages total; `.raw/.manifest.json` now tracks all 5.
- Created: `skills/wiki/references/team-sync.md` (+ modes.md link, [[Wiki Sharing Patterns]] pointer).
- Committed on `adlc`: harness hardening `bc511a3`; team-sync `0278002`; 5-talk ingest `59449d5`; wrap-up sync (overview rewrite + index metric fix).
- Wrap-up reconcile: [[overview]] rewritten (was still the April demo-seed text at "26 pages"; now describes the design wiki at 80 pages, dead canvas links removed); [[index]] metric disambiguated to "Source pages: 23".

## Active Threads

- **Tier 1 implemented** (evidence + left-undone handoff fields with dispatcher blocking, `tools:` allowlists on all 7 workers, push-standards-to-reviewer, 3-round review cap, plan-doc archival in wrap-up) plus `references/team-sync.md` (multi-role wiki state sharing). **Tier 2–3 backlog remains**: verifier-failures→backlog, milestone-level holistic verification, grilling gate, vertical-slice rule in user-story-factory, YouTube capture path + canonical-language rule in wiki-ingest, assertion-coverage ledger, metrics seam / mission-control.
- **Deployed agent copies are stale**: service repos carry their own `.claude/agents/` snapshots (one lacks feature-reviewer entirely) — redeploy after committing harness fixes.
- **pm-layer evals**: E1–E8 documented but not encoded/run.
- **`plugin.json`**: 0.3.0→0.4.0 bump still uncommitted (user-managed).
- **RLM → wiki-query**: design filed ([[RLM-Optimized Wiki Querying]]), not implemented.
