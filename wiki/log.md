---
type: meta
title: "Operation Log"
updated: 2026-07-04
tags:
  - meta
  - log
status: evergreen
related:
  - "[[index]]"
  - "[[hot]]"
  - "[[overview]]"
  - "[[sources/_index]]"
---

# Operation Log

Navigation: [[index]] | [[hot]] | [[overview]]

Append-only. New entries go at the TOP. Never edit past entries.

Entry format: `## [YYYY-MM-DD] operation | Title`

Parse recent entries: `grep "^## \[" wiki/log.md | head -10`

---

## [2026-07-08] fix | DEFECT-001 closed: /project-profile now augments an existing AGENTS.md
- `skills/project-profile/SKILL.md` Step 5 branches: no existing file → template as before; existing `AGENTS.md` → **augment path** (split into `##` sections, refresh the seven skill-owned sections, `Conventions`/`Code Generations` as a deduped union, preserve every foreign section verbatim in order).
- Step 1 reframed to "back up and augment" (default cancel); Step 7 backs up to `AGENTS.md.bak` (`.bak.N` if taken) before writing; Step 8 logs an augment variant; hard rule 6 added ("never drop a section you don't own"); modes table + known-limitations note updated.
- [[Project Profile Skill Suite]] → Known Defects: DEFECT-001 marked **Fixed** with the approach; the ⚠️ on the first-run flow flipped to ✅. Dedicated `--refresh` (section-level diff) still deferred; the data-loss regression is closed.

---

## [2026-07-08] defect | DEFECT-001: /project-profile first-run overwrites existing AGENTS.md
- Filed in [[Project Profile Skill Suite]] under "Known Defects" (this vault has no `defects/` folder).
- Discovered during a `/project-profile` first-run on a brownfield service repo whose existing `AGENTS.md` carried `wiki/` + ADLC topology sections; on "back up and proceed" the first-run replaced them with mechanical-only output.
- The design spec says "augment rather than replace" (first-run flow, step 1) and Step 1 even passes `existing_agents_md` to the scanner, but composition writes from a fixed template and never merges the existing content back in — so unrecognized sections are dropped.
- Severity: High (data loss). Workaround: manual merge from the `.bak` file. Fix direction: diff/merge into the existing file, preserving unknown sections until `--refresh` mode lands.

---

## [2026-07-04] review | ADLC field review captured: [[ADLC Field Review Findings]]
- Reviewed a production two-wiki ADLC setup end-to-end (genericized — no project names): flow-trace over both wiki logs + ~24 feature plans, duplication analysis (a/b/c classification), per-repo usage ledgers. Two parallel Explore workers (~240K subagent output); main context got only the condensed reports.
- Headline findings filed: the pipeline ships but **inverted** (code-first, BA registered after prod; unregistered local IDs the failure mode); the handoff seam leaks (zero requirement-ID references in plans, re-derivation of context the plan should carry — the `architecture-subagent` template enforces exactly what the manual substitute skipped); records must be pages not prose (verdicts were narrative-only; two "not implemented" pages contradicted shipped reality — the plan-rot trap live); duplication ~6–8% by volume / 25–30% hard in the shared layer (single-source formulas + decision rationale); efficiency operator-set (48–66% delegation on pipelined features vs 4% on a main-thread marathon; harness bounds variance, operator sets the mean).
- Same session (not wiki-filed, in project repos): harness alignment applied to three service repos — reviewer agents added where missing, verifiers now write record pages, coverage ledgers, tier-2/3 dispatcher rules, `.gitattributes` union merge, mission-control seeded in the ADLC vault, `index.json` + `usage.md` generated.

---

## [2026-07-04] impl | Token-usage rollup: meta/usage.md generated at wrap-up
- Operator asked to keep an eye on token consumption and what drives it. New `skills/wrap-up/scripts/usage_report.py` (zero-dep): parses the host's Claude Code transcripts (`~/.claude/projects/<slug>/`), dedupes streamed usage by `requestId`, filters `<synthetic>` placeholder entries, attributes subagent runs via their `.meta.json` sidecars, and writes `wiki/meta/usage.md` — cumulative session ledger (rows survive transcript GC) + top-consumer / per-model / per-subagent-type tables.
- Wired: `wrap-up` step 7 refreshes it alongside `index.json`; `mission-control.md` documents it as the third derived meta page (host-local: each teammate regenerates from their own transcripts; going stale on non-Claude-Code hosts is expected, not drift).
- Dogfooded on this vault: 10 sessions, ~1.3M output / ~5.2M cache-write / ~294M cache-read tokens; top consumer = the May bootstrap session (466K output), subagent fan-out peaked at 63% of output in the 2026-07-03 ingest session.

---

## [2026-07-04] wrap-up | Completed interrupted sync for the two post-commit increments
- Trigger: operator "check latest changes; last wrap-up might not have finished". Finding confirmed: the pm-layer-evals and RLM-follow-ups increments were built and logged but never synced — [[hot]] still listed both as "remaining planned".
- Reconciled: [[hot]] rewritten (uncommitted-state flagged), [[overview]] last-activity + shipped/planned lists updated, [[RLM-Optimized Wiki Querying]] flipped `developing` → `implemented` (index.json item marked built — the plan-rot rule), `wiki/index.json` regenerated post-edits.
- Left for the human: commit the two increments on `adlc`; optional E1 golden-case run on the default model.

---

## [2026-07-04] impl | pm-layer evals E1–E8 encoded (fixtures + runnable runner)
- The eval matrix from [[Product Management Layer Skill]] is now runnable: `skills/product-management-layer/evals/` — `cases/E1..E8.md` (Prompt + Must match / Must not match regexes per case), `fixtures/governance/` (coherent portfolio: 2 approved pairs, underused Arize sub, ungoverned zero-utilization FlowMetrics, empty trigger log; `{{PLUS_45D}}`-style dates substituted at run time so near-expiry never goes stale), `run-evals.sh` (throwaway workspace per case, one `claude -p` turn, grades transcript + registry diff), README.
- Mechanics verified with a stub model (pass path, fail path, must-not path, `--grade-only`, comment filtering). Real smoke runs: **E5 PASS** on haiku (no Gate 0 artifacts in an ADR request — the negative trigger holds). **E1 FAIL on haiku** — a genuine catch, not a runner bug: haiku fired the sunset trigger but skipped `under-review` and the never-transfer invariant. Golden-case verdict on the default model recorded separately below if run.
- Grading design note: negative assertions grade against transcript + registry **diff** (not raw registry) so fixture text can't false-trip them; E6's escalation regex tightened after the stub exposed "governance" matching diff file paths.

---

## [2026-07-04] impl | RLM follow-ups: index.json locator + sub-answer caching
- Closed the Phase 12 open items from [[RLM-Optimized Wiki Querying]]. New `skills/wiki-query/scripts/build_index_json.py` (zero-dep, flat-YAML-subset parser): generates `wiki/index.json` — a machine-readable locator mirror (path, type, status, tags, ADLC trace IDs per page; `--services` includes code wikis). Verified on this vault: 83 pages. Locator, not content: trust it to find, never to answer.
- `wiki-query` large-vault mode: Locate step now checks the `questions/` answer cache first, uses `jq` over `index.json` when present; new step 5 files each recursion sub-answer to `questions/` with a `scope:` frontmatter line (future queries grep-hit it and skip the recursion); new cache-staleness guardrail (cited page newer than cache → re-derive).
- Wired freshness: `wrap-up` step 7 regenerates `index.json` when present; `wiki-lint` check 8a (SKILL) + check 14 (subagent) flag a stale `generated` stamp and stale cached sub-answers.

---

## [2026-07-04] wrap-up | Session end sync + commit (tier 3 + graphify grounding)
- Trigger: operator "wrap up and commit". Scope: this vault only (plugin repo; no `services/` checkouts).
- Rollups reconciled: [[overview]] last-activity line covers both increments; planned list already trimmed to pm-layer evals + RLM→wiki-query. [[index]] unchanged (no new wiki pages — the session's output is harness files + `references/mission-control.md`). [[hot]] rewritten.
- Committed on `adlc` in one commit: metrics seam / mission-control (1 new reference + 7 wired files) + graphify grounding for workers (6 agent/reference files) + wiki bookkeeping.
- Follow-ups for the human: **redeploy `agents/*.md` snapshots to service repos** (now carrying graphify grounding; one repo lacks feature-reviewer); run `/graphify-ingest` once in service repos without a graph; seed `meta/mission-control.md` + `meta/ba-activity.md` in existing ADLC vaults; `.gitattributes` two-liner in existing project vaults; `plugin.json` 0.3.0→0.4.0. Queued: pm-layer evals E1–E8, RLM→wiki-query.

---

## [2026-07-04] impl | Workers ground in the graphify layer (pre-redeploy)
- Before redeploying agent snapshots to service repos: ADLC workers now leverage graphify data where a service carries it. New **Code graph grounding** section in `technical-planning.md`: graph for *finding* (connections, callers, blast radius — zero LLM cost), code for *asserting*; on disagreement the code wins and the worker reports staleness; freshness is the dispatcher's job (`/graphify-update` post-verify pre-commit, in the dispatch packet when present); `wrap-up` step 3 refreshes graphs of changed repos.
- Bash-capable workers got a self-contained CLI step (pinned-python `python -m graphify query --budget 1500`): `feature-builder` (orient step 2 — definition sites / callers / community before survey), `feature-reviewer` (step 3 blast-radius check — callers outside the diff, the missed-call-site bug class), `feature-tester` (step 2 — routes/components the scenarios exercise + neighboring specs to extend).
- Bash-less workers use the readable layer (`wiki/code/_COMMUNITY_*.md`, `GRAPH_REPORT.md`): `architecture-subagent` (new step 2 — module map / god nodes / seams before grep-grounding) and `doc-writer` (step 3 — locate routes fast, confirm in source).
- All agent steps are self-contained (no plugin-relative paths) so the snapshots work standalone in service repos. `feature-verifier` deliberately untouched (runtime verification; the graph adds nothing there).
- Uncommitted, same session as the tier 3 metrics seam below.

---

## [2026-07-04] impl | Harness tier 3: metrics seam / mission-control
- Built the last planned harness item: **`references/mission-control.md`** (new) specifies two derived pages in an ADLC vault's `meta/` — `mission-control.md` (operator's async board: in-flight table with stages, release readiness against the literal bar, defect-route table, milestone status, open human gates; dispatcher updates a row at every stage transition) and `ba-activity.md` (cost rollup from `produced_by` / `feature` / `effort_estimate` frontmatter, grep-first, refreshed at wrap-up; "Not counted" line is the seam's own health check). Both derived — records always win, same principle as the coverage ledger. Optional Obsidian Base for humans.
- Wired in: `technical-planning.md` new dispatcher rule (board row per stage transition); `wrap-up` step 6 reconciles both pages; `wiki-lint-subagent` check 13 (missing `produced_by`, board rows contradicting records, board staleness); `team-sync.md` merge rule (regenerate-don't-merge, like hot.md); `modes.md` + `ba-suite-pipeline.md` metrics-seam stubs upgraded from "(build later)" to pointers; `wiki/SKILL.md` scaffolds both pages for ADLC and refreshes the ledger in the initial-pass integrate step.
- Origin: mission-control operator UX from [[yt-alvoeiro-multi-agent-architecture]] ("budget/progress visibility" gap); the rollup target from the ADLC operating model ("deliverables produced vs BA/QA/PM time replaced").
- Not committed (operator gates commits). Still queued: pm-layer evals E1–E8, RLM→wiki-query; human follow-ups unchanged (agent redeploy to service repos, `.gitattributes` in project vaults, `plugin.json` bump).

---

## [2026-07-04] wrap-up | Session end sync + commit
- Trigger: operator "commit this and wrap up". Scope: this vault only (plugin repo; no `services/` checkouts).
- Rollups reconciled: [[overview]] last-activity line and "Planned / not yet built" updated (tier 2–3 backlog → only metrics seam / mission-control remains planned). [[hot]] rewritten for the tier 2 session; [[index]] unchanged (no new pages this session — all edits were harness files).
- Committed on `adlc` in one commit: 8 harness files (tier 2 + ingest video/language), `.gitattributes` (merge=union), `git-setup.md` scaffold addition, wiki bookkeeping (hot / log / overview).
- Follow-ups for the human: redeploy `agents/*.md` to service repos (stale snapshots; one lacks feature-reviewer); add the two-line `.gitattributes` to existing project vaults by hand; `plugin.json` 0.3.0→0.4.0 bump; queued work — metrics seam / mission-control, pm-layer evals E1–E8, RLM→wiki-query.

---

## [2026-07-04] impl | Harness tier 2 + wiki-ingest tier 3 (video + language)
- Implemented the tier 2 backlog from [[hot]]: **grilling gate** before Gate 1 approval + **milestone holistic verification** (cross-feature journeys, fresh-target re-verify, unscoped suite) + **verifier-FAILs→backlog** dispatcher rule (`conditional — fix pending`; ENV_MISMATCH / NEEDS_SIGN_IN = operational, not defects) in `references/technical-planning.md`.
- **Vertical-slice rule** in `references/ba/ba-user-story-factory.md`: Step 2.5 tracer-bullet check (horizontal layer-stories fail; Technical Enabler needs justification), DAG quality bar on the dependency map, new quality gate.
- **Assertion-coverage ledger**: `feature-tester` step 7 maintains `coverage/_index.md` (one row per contract scenario; derived — contract + spec win) + report field; documented in `references/concerns/qa.md`.
- `wiki-lint-subagent`: 2 new checks — FAIL records / bug pages without a backlog item (critical), coverage-ledger drift. `wrap-up` step 4 now reconciles the defect route (bugs page + backlog item per FAIL).
- Tier 3 partial: `wiki-ingest` gained a **Video / YouTube ingestion** path (yt-dlp subs-only capture, VTT cleaning, proper-noun caveat) and a **Canonical Language** rule (wiki pages in vault language; `.raw/` never translated; `source_language:` frontmatter).
- Closed wrap-up follow-up #2: `wiki/log.md merge=union` — `.gitattributes` created in this repo, and `references/git-setup.md` now scaffolds it into every new vault (scaffold step 8 reads that doc). Other existing project vaults still need the two-line file added by hand.
- Remaining backlog: metrics seam / mission-control (tier 3), pm-layer evals E1–E8, RLM→wiki-query, redeploy stale agent copies to service repos.

---

## [2026-07-03] wrap-up | Session end sync
- Trigger: operator "wrap up". Scope: this vault only (plugin repo; no `services/` checkouts). Tree was clean — all session work already in 3 commits on `adlc` (harness hardening `bc511a3`, team-sync `0278002`, 5-talk ingest `59449d5`).
- Rollup reconciliation (per the new wrap-up step 6): rewrote [[overview]] — it still described the April demo-seed vault ("26 pages, seed content") while the vault is the claude-mem design wiki at 80 pages; also removed two dead canvas links. Fixed [[index]] header metric (ambiguous "Sources ingested: 9" → "Source pages: 23"); bumped log frontmatter date.
- Follow-ups for the human: redeploy updated `agents/*.md` to service repos (stale `.claude/agents/` snapshots); add `log.md merge=union` `.gitattributes` to project vaults; tier 2–3 harness backlog in [[hot]]; pm-layer evals E1–E8 still not encoded.

---

## [2026-07-03] impl | Harness hardening (audit-driven + tier 1) + team-sync protocol
- Audited the ADLC harness against two production vaults' decision/verification trails (2 Explore agents). Failure clusters: tester env-precondition assumptions, verifier env-dependent PASSes + stubbed-integration "VERIFIED" + dev-artifact false reds, planner doc-first claims falsified against code, log.md bloat (~7k lines), false completion claims.
- Applied fixes across `agents/feature-{builder,tester,reviewer,verifier}.md`, `agents/{architecture,ba-suite}-subagent.md`, `agents/wiki-lint-subagent.md`, `skills/wrap-up/`, `references/{technical-planning,shift-left/_index}.md`: target fingerprint + ENV_MISMATCH, "Not exercised" stub list, restart-once protocol, records-as-pages, preconditions-are-code, honest tag flips, code-grounding `[UNVERIFIED — from docs]`, dispatcher re-verify + readiness bar.
- Tier 1 (from the 5-talk cross-check): Evidence (commands + exit codes) + "Left undone" fields on all 7 worker reports with a dispatcher blocking rule; `tools:` allowlists on all 7 workers; push-standards-to-reviewer; review loop capped at 3 rounds; plan-doc archival step in wrap-up. Model split encoded: Sonnet workers draft, dispatcher (session model) orchestrates + re-verifies.
- New: `references/team-sync.md` — multi-role / multi-wiki state sharing (git as state bus, role → concern ownership, pull-first / wrap-up-last, `log.md merge=union`, hot.md regenerate-don't-merge, machine-local `services/` symlinks, status fields as the shared state machine). Linked from modes.md + [[Wiki Sharing Patterns]].
- Improvement backlog (tiers 2–3) recorded in [[hot]]: verifier-failures→backlog, milestone holistic verify, grilling gate, vertical-slice rule, YouTube capture path in wiki-ingest, assertion-coverage ledger, metrics seam.

---

## [2026-07-03] ingest | Full Walkthrough: Workflow for AI Coding (Pocock, AI Engineer)
- Source: `.raw/yt-pocock-ai-coding-workflow.md` → [[yt-pocock-ai-coding-workflow]]. Created: [[Grilling Session]], [[Ralph Wiggum Loop]], [[Vertical Slices for Agent Tasks]], [[Deep Modules]], [[Matt Pocock]]. Updated: [[Context Rot]] (smart/dumb zone, ~100K marker, clear-over-compact), [[Context Engineering for Coding Agents]] (push-vs-pull standards, fresh-context review, model tiering, doc rot as anti-context), [[AGENTS.md]] (near-empty always-on file, pull-first counterpoint), [[Compounding Knowledge]] (contradiction callout: doc rot vs compounding — plans rot, as-built knowledge compounds), [[index]], sub-indexes. Key insight: the human's leverage is at alignment (grilling) and QA; implementation becomes an AFK loop over a vertical-slice issue DAG, and the repo's feedback-loop quality — not the model — is the ceiling on agent output.

---

## [2026-07-03] ingest | The Multi-Agent Architecture That Actually Ships (Alvoeiro, AI Engineer)
- Source: `.raw/yt-alvoeiro-multi-agent-architecture.md` → [[yt-alvoeiro-multi-agent-architecture]]. Created: [[Multi-Agent Communication Taxonomy]], [[Validation Contract]], [[Structured Handoff]], [[Factory]], [[Luke Alvoeiro]]. Updated: [[Generator-Evaluator Pattern]] (missions production case, cross-provider evaluators), [[Context Engineering for Coding Agents]] (clean-context workers, serial execution), [[index]], sub-indexes. Key insight: multi-day autonomous delivery works when correctness is defined before code (validation contract), state travels via structured handoffs with exit-code evidence, validators never see the code, and features run serially with only read-only ops parallelized.

---

## [2026-07-03] ingest | AI Agent Memory: from RAG to Wiki LLM to Graphify (Orlov, YouTube)
- Source: `.raw/yt-orlov-ai-agent-memory-wiki-llm.md` → [[orlov-rag-wiki-llm-graphify]]. Created: [[Orlov]]. Updated: [[Andrej Karpathy]] (vibe-coding coinage + flagged unverified "joined Anthropic" claim), [[Wiki vs RAG]] (three-waves framing), [[graphify-integration]] (external claims: video/audio inputs, 50–70x savings claim, small-project caveat), [[Contextual Retrieval]] (chunk-as-assertion heuristic), [[LLM Wiki Pattern]] (adoption beyond Claude stack), [[index]], sub-indexes. Key insight: the wiki pattern is being independently reproduced on non-Claude stacks (Antigravity + Gemini) and pitched to lay audiences as the successor to RAG, with graphs as the third wave.

---

## [2026-07-03] ingest | The Future Is Domain-Specific Agents (Schroeder, AI Engineer)
- Source: `.raw/yt-schroeder-domain-specific-agents.md` → [[yt-schroeder-domain-specific-agents]]. Created: [[Domain-Specific Agents]], [[Justin Schroeder]], [[StandardAgents]]. Updated: [[Context Engineering for Coding Agents]] (composition-over-inheritance section), [[Context Rot]] (DSA as architectural fix), [[index]], all three sub-indexes. Key insight: composition of small complete agents (own prompt/tools/history under a coordinator) beats inflating one agent's context — claimed >80% token efficiency, small-model viability, capability limits by construction; prediction: 2027 = year of multi-agent orchestration.

---

## [2026-07-03] ingest | After the AI Hype — What's Real, and What's Next (Campbell, NDC 2026)
- Source: `.raw/yt-campbell-after-ai-hype.md` → [[campbell-after-ai-hype]]. Updated: [[Generator-Evaluator Pattern]] (GPT-5 LLM-judge failure case), [[Product Management Layer Skill]] (vendor-volatility evidence), [[index]], [[sources/_index]]. Key insight: the first real LLM product impact was the agentic issue→PR→argue→accept loop — but same-model evaluation rubber-stamps garbage and half the 2025 agentic tools are already gone.

---

## [2026-07-03] eval | Product Management Layer skill — 4/4 pass + 5 fixes
- Role-played E1 (Embrace.ai sunset, golden), E2 (buy-vs-build + owned Arize asset), E5 (negative: ADR request), E6 (cross-trigger: buy inside shift-left escalates up) against the actual skill files via a subagent. Verdict: **PASS 4/4** — disjoint-vocabulary contract + non-transferability + buy-vs-build option set enforced as hard rules on both sides.
- Applied 5 minor fixes: (1) retroactive intake when a sunset/acquisition trigger hits an in-use *ungoverned* tool (was a silent no-op — the real E1 edge); (2) reworded §2 "automatically" to name the VENDOR-REVIEW gate (Anti-Magic self-conflict); (3) spelled out "open a NEW ApprovalEntry for the replacement" in the migration checklist; (4) added rationalization trigger phrases ("why are we still paying for X", "do we still need X", "consolidate our tools"); (5) clarified a mode's linked parts = one gate.

---

## [2026-07-03] impl | Product Management Layer skill shipped
- Built `skills/product-management-layer/` the claude-mem way (not the plan's absent skill-creator toolchain): `SKILL.md` (135 lines, pushy description w/ trigger phrases; On Init, 5 modes INTAKE/VENDOR-REVIEW/BUY-VS-BUILD/COMPLIANCE-SCOPE/REGISTRY-STATUS, domain invariants, ID scheme, handoffs) + `references/reference.md` (10 artifact templates). Auto-discovered via the plugin manifest — no plugin.json edit.
- Registry persistence (plan P3.6) resolved: Markdown under `wiki/governance/` when a vault exists, else `docs/governance/`; decision-log append-only.
- Handoffs wired: down (approved intake → shift-left Gate 1 packet w/ trace IDs), up (shift-left escalates here), sideways (evidence → solutioning). Vocabulary kept disjoint.
- [[Product Management Layer Skill]] flipped planned → implemented; README Skills table updated. NOT done: encoded E1–E8 eval harness, PlantUML diagrams, formal Gates 1–4 docs (documented as next steps).

---

## [2026-07-03] patch | shift-left advisor — Gate 0 governance escalation
- Companion change for [[Product Management Layer Skill]]: added a "Governance Escalation (Gate 0, up)" section to the bundled `shift-left-engineering-advisor.md` so vendor/tool/buy-vs-build/subscription/compliance/shelfware questions route **up** to the planned pm-layer skill (satisfies eval E6), keeping vocabularies disjoint; documented the down-handoff (approved intake → Gate 1 with trace IDs).
- Also fixed a dead `reference.md` link (dropped when shift-left was bundled) → `_index.md` + `technical-planning.md`; added a 5th ADLC override note in the bundle `_index.md`.
- Repo reality: shift-left is a bundled method doc read by `architecture-subagent`, not a standalone installable skill — no package/install/eval cycle (the plan's Phase 5b tooling is absent here); frontmatter `description` is vestigial, so no trigger regression.

---

## [2026-07-03] plan | Product Management Layer Skill (Gate 0 governance)
- Filed [[Product Management Layer Skill]]: new planned skill layering **above** [[shift-left-engineering-advisor]] — use-case intake/approval registry, vendor lifecycle + re-review triggers, buy-vs-build TCO, per-use-case compliance scoping, shelfware detection, portfolio STATUS. Bidirectional handoff (up: shift-left escalates vendor/tool Qs here; down: approved intake → shift-left Gate 1).
- Raw governing plan saved immutable at [[pm-layer-execution-plan]] (`.raw/`): 6 phases, Gates 1–4, 8 FRs, 8 evals (E1 golden = Embrace.ai sunset), built via ai-agent-builder + skill-creator.
- Main risk: trigger collision with shift-left → disjoint vocabulary + negative evals E5/E6 + description optimization. Companion shift-left patch is its own skill-creator mini-cycle.
- Index count 60 → 61.

---

## [2026-06-28] impl | Graphify Relative Paths (Phase 13 done)
- Implemented per [[Graphify Relative Paths]]: `to_rel()` helper in merge.py / update.py / regenerate.py rewrites node `source_file` to project-root-relative before graph.json is written. update.py prune compares relative (auto-migrates old absolute graphs). Subagent + ingest SKILL docs updated. Query skills unchanged (print stored relative paths).
- Verified: py_compile OK on all three scripts; to_rel unit-tested. Deterministic Python relativization chosen over LLM path math in the subagent.

---

## [2026-06-28] plan | Graphify Relative Paths (multi-member portability)
- Filed [[Graphify Relative Paths]]: committed graphify artifacts (graph.json source_file, GRAPH_REPORT.md, wiki/code/*) store machine-absolute paths that break for teammates at other checkout paths.
- Plan: post-merge relativization to project-root-relative source_file; subagent records relative; query skills resolve to absolute only when reading. Tracked as roadmap Phase 13.
- Already fine: runtime TARGET=$(cd&&pwd), gitignored .graphify_python, chunks.py/detect.py relative file lists.

---

## [2026-06-28] autoresearch | Recursive Language Models
- Rounds: 2 | Searches: 3 | Sources fetched: 4
- Pages created: [[Recursive Language Models]], [[Context Rot]], [[RLM-Optimized Wiki Querying]], [[Alex L. Zhang]], [[rlm-paper-arxiv]], [[rlm-blog-zhang]], [[rlm-github-repo]], [[rlm-reproduction-overthink]]
- Synthesis: [[Research Recursive Language Models]]
- Key finding: RLM stores long context in a REPL the model greps/chunks/recurses over (depth=1), sidestepping context rot; maps onto a bash-capable ADLC agent for grep-first + bounded-recursion wiki-query.
- Application: design filed at [[RLM-Optimized Wiki Querying]] — evolve wiki-query, do not rebuild; reinforce greppable frontmatter, per-folder _index, short pages, stable cross-wiki IDs.

---

## [2026-05-09] design | Project Profile Skill Suite (end-to-end)
- Type: design synthesis (no research; resolves open questions from prior two passes)
- Pages created: [[Project Profile Skill Suite]]
- Scope: 5 skills (`/project-profile`, `/capture-rule`, `/list-rules`, `/prune-rules`, `/resolve-rule-conflicts`) + 3 subagents (`mechanical-scanner`, `rule-generator`, `rule-evaluator`) + 1 hook (SessionStart)
- File layout decided: `AGENTS.md` (root) + `.agents/rules/*.md` (one per rule, <80 lines) + `.agents/rules/_index.md` (cheap conflict detection)
- Implementation sequence proposed: (1) /project-profile first-run, (2) /list-rules + index writer, (3) /capture-rule + 2 subagents, (4) status mode, (5) /prune-rules, (6) /resolve-conflicts, (7) integration
- Key constraint: SessionStart is the only automation; everything else is explicit user trigger
- Empirical caveats baked in (from [[evaluating-agents-md-eth]]): cut repository overviews from template, mechanical scanner focuses on commands not prose, generator biases toward concrete directives

## [2026-05-09] autoresearch | Feedback-Driven Project Profile (Round 2)
- Round: 1 (focused, smaller scope than the prior pass)
- Searches: 4 (Cursor /Generate Cursor Rules, Aider conventions, Reflexion, agent feedback UX)
- Fetches: 5 (Cursor docs redirect failed; recovered partial via search summaries + changelog 0-49 + Aider conventions docs + Reflexion abstract + Anthropic harness-design)
- Pages created: [[cursor-generate-rules]], [[aider-conventions]], [[reflexion-paper]], [[anthropic-harness-design]], [[Rule Generation from Chat]], [[Generator-Evaluator Pattern]], [[Feedback Loop for Project Profile]]
- Synthesis: [[Research Feedback-Driven Project Profile]]
- Key finding: Cursor's /Generate Cursor Rules (v0.49, April 2025) is the closest reference implementation. Manual + retrospective trigger; one concept per file under 80 lines; same format as hand-written. Aider takes the opposite approach (strict human authorship). Reflexion paper (2023) is the academic foundation: Actor/Evaluator/Self-Reflection. Anthropic explicitly recommends generator-evaluator separation as "a strong lever" against self-grading leniency.
- Design synthesis: three-role architecture (Generator skill, separate Evaluator subagent, Human gate); manual /capture-rule trigger; one rule per file with 80-line cap; separate /prune-rules skill; nothing writes without engineer accept.
- Total pages: 8 (4 sources, 3 concepts, 1 synthesis), within budget.
- Trigger: continuation of /project-profile design discussion; addresses open question 5 (tribal-knowledge UX) from prior research

## [2026-05-09] autoresearch | Pre-computed Context for Coding Agents
- Rounds: 2 (Round 1: 6 parallel searches + 5 deep fetches; Round 2: 2 search + 2 fetch gap-fill)
- Sources fetched: 7 primary URLs (agents.md spec, ETH Zurich AGENTbench paper, Aider repo-map blog, 2 Anthropic blogs, RACG survey, plus llms.txt + Cody/Continue searches)
- Pages created: [[agents-md-spec]], [[evaluating-agents-md-eth]], [[aider-repo-map]], [[anthropic-context-engineering]], [[anthropic-contextual-retrieval]], [[racg-survey-2025]], [[Context Engineering for Coding Agents]], [[AGENTS.md]], [[Repo Map]], [[Contextual Retrieval]], [[Project Profile]], [[ETH Zurich AGENTbench Team]], [[Aider]]
- Synthesis: [[Research Pre-computed Context for Coding Agents]]
- Key finding: ETH Zurich AGENTbench (Feb 2026) shows LLM-generated context files DEGRADE agent performance by 2-3%; even human-written ones give only +4% with +20-23% inference cost. Auto-summarization is net-negative; hand-curated tribal knowledge + AGENTS.md-compatible format + on-demand structural retrieval is the right pattern.
- Total pages: 14 created (within 15-page program limit)
- Trigger: design discussion about a `/project-profile` skill for brownfield repos

## [2026-04-26] session | Graphify Integration (v0.1.0 → v0.2.0)
- Type: multi-hour build session
- Location: [[2026-04-26-graphify-integration-session]]
- Built: `graphify-ingest` + `graphify-update` skills, `graphify-extract` subagent, `/graphify-ingest` + `/graphify-update` commands, `bin/setup-graphify.sh`
- Extended: `wiki-query` (graph routing), `wiki-lint` (9 graph-layer checks via `scripts/lint_graph.py`), `wiki-ingest` (parallel batch dispatch)
- Removed: `_templates/`, `.windsurf/`
- Test target: `~/esg/esg-website` (Next.js, 169 code files) — full E2E validated
- Key concept pages: [[graphify-integration]], [[maintenance-triggers]]
- Key lessons: labels.json poisoning is not self-healing; Jaccard 0.6 threshold preserves cluster identity across small touches; AST-ID hints fix the edge-drop issue; graphifyy excludes Python 3.14
- Plugin manifest: bumped to v0.2.0 with new keywords

## [2026-04-08] save | claude-obsidian v1.4 Release Session
- Type: session
- Location: wiki/meta/claude-obsidian-v1.4-release-session.md
- From: full release cycle covering v1.1 (URL/vision/delta tracking, 3 new skills), v1.4.0 (audit response, multi-agent compat, Bases dashboard, em dash scrub, security history rewrite), and v1.4.1 (plugin install command hotfix)
- Key lessons: plugin install is 2-step (marketplace add then install), allowed-tools is not valid frontmatter, Bases uses filters/views/formulas not Dataview syntax, hook context does not survive compaction, git filter-repo needs 2 passes for full scrub

## [2026-04-08] ingest | Claude + Obsidian Ecosystem Research
- Type: research ingest
- Source: `.raw/claude-obsidian-ecosystem-research.md`
- Queries: 6 parallel web searches + 12 repo deep-reads
- Pages created: [[claude-obsidian-ecosystem]], [[cherry-picks]], [[claude-obsidian-ecosystem-research]], [[Ar9av-obsidian-wiki]], [[Nexus-claudesidian-mcp]], [[ballred-obsidian-claude-pkm]], [[rvk7895-llm-knowledge-bases]], [[kepano-obsidian-skills]], [[Claudian-YishenTu]]
- Key finding: 16+ active Claude+Obsidian projects; 13 cherry-pick features identified for v1.3.0+
- Top gap confirmed: no delta tracking, no URL ingestion, no auto-commit

## [2026-04-07] session | Full Audit, System Setup & Plugin Installation
- Type: session
- Location: wiki/meta/full-audit-and-system-setup-session.md
- From: 12-area repo audit, 3 fixes, plugin installed to local system, folder renamed

## [2026-04-07] session | claude-obsidian v1.2.0 Release Session
- Type: session
- Location: wiki/meta/claude-obsidian-v1.2.0-release-session.md
- From: full build session — v1.2.0 plan execution, cosmic-brain→claude-obsidian rename, legal/security audit, branded GIFs, PDF install guide, dual GitHub repos


- Source: `.raw/` (first ingest)
- Pages updated: [[index]], [[log]], [[hot]], [[overview]]
- Key insight: The wiki pattern turns ephemeral AI chat into compounding knowledge — one user dropped token usage by 95%.

## [2026-04-07] setup | Vault initialized

- Plugin: claude-obsidian v1.1.0
- Structure: seed files + first ingest complete
- Skills: wiki, wiki-ingest, wiki-query, wiki-lint, save, autoresearch
