---
type: meta
title: "Operation Log"
updated: 2026-05-09
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
