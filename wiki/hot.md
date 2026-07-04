---
type: meta
title: "Hot Cache"
updated: 2026-07-04T18:30:00
tags:
  - meta
  - hot-cache
status: evergreen
related:
  - "[[index]]"
  - "[[log]]"
  - "[[Product Management Layer Skill]]"
  - "[[RLM-Optimized Wiki Querying]]"
---

# Recent Context

Navigation: [[index]] | [[log]]

## Last Updated

**2026-07-04 (post-wrap-up increments, UNCOMMITTED)**: After the tier-3 commit (`8ba3856`), the session continued with two more increments — pm-layer evals E1–E8 and the RLM → wiki-query follow-ups. Both are logged and now fully synced (this wrap-up completion), but **not yet committed** on `adlc`.

## Key Recent Facts

- **pm-layer evals E1–E8 encoded (runnable):** `skills/product-management-layer/evals/` — `cases/E1..E8.md` (Prompt + Must/Must-not regexes), `fixtures/governance/` (coherent portfolio; `{{PLUS_45D}}`-style dates substituted at run time so near-expiry never goes stale), `run-evals.sh` (throwaway workspace per case, one `claude -p` turn, grades transcript + registry **diff** so fixture text can't false-trip negatives). Smoke: **E5 PASS on haiku** (negative trigger holds); **E1 FAIL on haiku** (skipped `under-review` + never-transfer) — the golden case discriminates by model strength, as designed. `results/` is gitignored.
- **RLM follow-ups closed ([[RLM-Optimized Wiki Querying]] now `implemented`):** new `skills/wiki-query/scripts/build_index_json.py` (zero-dep) generates `wiki/index.json` — a machine-readable locator (path/type/status/tags/trace IDs; `--services` adds code wikis; 83 pages on this vault). Locator, not content: trust it to find, never to answer. `wiki-query` large-vault mode now checks the `questions/` answer cache first, uses `jq` over `index.json` when present, files each recursion sub-answer to `questions/` with `scope:` frontmatter, and re-derives when a cited page is newer than the cache. Freshness wiring: `wrap-up` step 7 regenerates `index.json`; `wiki-lint` check 8a / subagent check 14 flag staleness.
- Committed earlier same day: tier 3 (metrics seam / mission-control + graphify grounding for workers, `8ba3856`) and tier 2 (`91934de`).

## Recent Changes

- Created: `skills/product-management-layer/evals/` (cases, fixtures, runner, README), `skills/wiki-query/scripts/build_index_json.py`, `wiki/index.json`.
- Edited: `skills/wiki-query/SKILL.md` (cache-first locate, index.json, sub-answer caching), `skills/wrap-up/SKILL.md` (step 7 regen), `skills/wiki-lint/SKILL.md` + `agents/wiki-lint-subagent.md` (staleness checks), [[Product Management Layer Skill]] (evals build note), [[RLM-Optimized Wiki Querying]] (status → implemented).
- Logged: [[log]] entries `impl | pm-layer evals E1–E8 encoded` and `impl | RLM follow-ups: index.json locator + sub-answer caching`, plus this wrap-up completion.

## Active Threads

- **Commit pending**: the two increments above are uncommitted on `adlc` — commit is the next human/operator action.
- Redeploy `agents/*.md` snapshots to service repos (carrying graphify grounding; one repo lacks feature-reviewer entirely); `/graphify-ingest` once in graph-less service repos.
- Other human follow-ups: `.gitattributes` two-liner in existing project vaults; seed the two `meta/` pages in existing ADLC vaults; `plugin.json` 0.3.0→0.4.0.
- Optional: run the pm-layer golden case (E1) on the default model and record the verdict in [[log]].
