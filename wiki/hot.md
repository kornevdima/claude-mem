---
type: meta
title: "Hot Cache"
updated: 2026-07-08T00:00:00
tags:
  - meta
  - hot-cache
status: evergreen
related:
  - "[[index]]"
  - "[[log]]"
  - "[[Project Profile Skill Suite]]"
  - "[[Product Management Layer Skill]]"
  - "[[RLM-Optimized Wiki Querying]]"
---

# Recent Context

Navigation: [[index]] | [[log]]

## Last Updated

**2026-07-08 (DEFECT-001 fixed)**: Closed **DEFECT-001** in `skills/project-profile/SKILL.md`. Step 5 now branches — with an existing `AGENTS.md` it takes an **augment path**: split into `##` sections, refresh the seven skill-owned sections (mechanical from the fresh scan; `Conventions`/`Code Generations` as a deduped union), and preserve every foreign section verbatim in order. Step 1 → "back up and augment" (default cancel); Step 7 backs up to `AGENTS.md.bak` before writing; hard rule 6 added. [[Project Profile Skill Suite]] → Known Defects marked **Fixed**; ⚠️ on the first-run flow flipped to ✅. Uncommitted.

**2026-07-08 (defect registered)**: Filed **DEFECT-001** (High / data loss) against `/project-profile` in [[Project Profile Skill Suite]] → "Known Defects": first-run overwrites an existing `AGENTS.md` with mechanical-only output instead of augmenting it. Design says "augment rather than replace" and Step 1 passes `existing_agents_md` to the scanner, but composition writes from a fixed template and drops the existing content. (Now fixed — see above.)

**2026-07-04 (post-wrap-up increments, committed)**: After the tier-3 commit (`8ba3856`), the session continued with two more increments — pm-layer evals E1–E8 (`3a740df`) and the RLM → wiki-query follow-ups (`9e9b02f`). Both synced (wrap-up completion, `2e56b07`) and committed on `adlc`; plugin bumped to 0.6.0 (`8cfc840`).

## Key Recent Facts

- **DEFECT-001 fixed ([[Project Profile Skill Suite]] → Known Defects):** `/project-profile` first-run on an existing `AGENTS.md` now augments instead of replacing — backs up to `.bak`, refreshes skill-owned sections, preserves foreign sections verbatim. Was High (data loss); root cause was a fixed-template composition that ignored the `existing_agents_md` it read. Dedicated `--refresh` (section-level diff) still deferred.
- **pm-layer evals E1–E8 encoded (committed):** `skills/product-management-layer/evals/` — golden cases + `fixtures/governance/` + `run-evals.sh` (grades transcript + registry diff). Smoke: E5 PASS / E1 FAIL on haiku (discriminates by model strength, as designed).
- **RLM follow-ups closed ([[RLM-Optimized Wiki Querying]] `implemented`):** `build_index_json.py` generates `wiki/index.json` (locator, not content); `wiki-query` large-vault mode is cache-first + `jq`-over-index.json + sub-answer caching; freshness wired into `wrap-up` step 7 and `wiki-lint`.
- **Token-usage rollup:** `skills/wrap-up/scripts/usage_report.py` → `wiki/meta/usage.md` (cumulative ledger + per-model/subagent tables), refreshed at wrap-up step 7. Also committed same day: tiers 2–3 (metrics seam / mission-control + graphify grounding).

- **ADLC field review filed ([[ADLC Field Review Findings]], new):** production two-wiki setup reviewed end-to-end. Grounded in evidence: code-first inversion (BA as catch-up; unregistered local IDs = the failure mode), handoff-seam costs (zero FR-ID traceability in ~24 plans, re-derivation), records-as-pages (narrative verdicts + two stale "not implemented" pages = plan-rot live), duplication ~6–8% volume / 25–30% of the shared layer, efficiency operator-set (48–66% delegation on pipelined features vs 4% on marathons). Harness alignment applied to three service repos in the same session (reviewer agents, verification records, ledgers, mission-control seed — in those repos, uncommitted for owner review).

## Recent Changes

- Fixed: **DEFECT-001** — `skills/project-profile/SKILL.md` Steps 1/5/7/8 + hard rule 6 (augment an existing `AGENTS.md`, back up, preserve foreign sections); [[Project Profile Skill Suite]] marked Fixed; `fix` log entry at top of [[log]].
- Registered: **DEFECT-001** — added "Known Defects" section to [[Project Profile Skill Suite]] + inline flag on the first-run flow; `defect` log entry in [[log]].
- Created: `skills/product-management-layer/evals/` (cases, fixtures, runner, README), `skills/wiki-query/scripts/build_index_json.py`, `wiki/index.json`.
- Edited: `skills/wiki-query/SKILL.md` (cache-first locate, index.json, sub-answer caching), `skills/wrap-up/SKILL.md` (step 7 regen), `skills/wiki-lint/SKILL.md` + `agents/wiki-lint-subagent.md` (staleness checks), [[Product Management Layer Skill]] (evals build note), [[RLM-Optimized Wiki Querying]] (status → implemented).
- Logged: [[log]] entries `impl | pm-layer evals E1–E8 encoded` and `impl | RLM follow-ups: index.json locator + sub-answer caching`, plus the wrap-up completion, the usage-rollup impl, and `review | ADLC field review captured`.
- Created: [[ADLC Field Review Findings]] (concepts/), indexed in [[index]] + concepts index.

## Active Threads

- **DEFECT-001 fixed** — `/project-profile` composition now merges into (not replaces) an existing `AGENTS.md`. Follow-on: the dedicated `--refresh` mode (section-level diff, tribal untouched) is still deferred. Fix is uncommitted.
- **All committed** — next: redeploy `agents/*.md` snapshots to service repos (carrying graphify grounding; one repo lacks feature-reviewer entirely); `/graphify-ingest` once in graph-less service repos.
- Other human follow-ups: `.gitattributes` two-liner in existing project vaults; seed the two `meta/` pages in existing ADLC vaults. (Plugin version bump: done, 0.6.0.)
- Optional: run the pm-layer golden case (E1) on the default model and record the verdict in [[log]].
