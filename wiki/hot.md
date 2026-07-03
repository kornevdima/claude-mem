---
type: meta
title: "Hot Cache"
updated: 2026-07-03T00:00:00
tags:
  - meta
  - hot-cache
status: evergreen
related:
  - "[[index]]"
  - "[[log]]"
  - "[[Product Management Layer Skill]]"
  - "[[shift-left-engineering-advisor]]"
  - "[[Project Profile Skill Suite]]"
---

# Recent Context

Navigation: [[index]] | [[log]]

## Last Updated

**2026-07-03 (impl: Product Management Layer skill)**: Shipped the Gate 0 governance skill at `skills/product-management-layer/` and patched the shift-left advisor to escalate up to it. Design page: [[Product Management Layer Skill]] (now status: implemented).

## Key Recent Facts

- **`product-management-layer`** is a shipped, user-facing claude-mem skill (auto-discovered from `skills/*/SKILL.md`). It governs *which tools/vendors are approved* before engineering; shift-left governs Gates 1–4.
- **Built the claude-mem way, not the plan's way.** The plan assumed `skill-creator` / `package_skill` / `docs/adr` / `evals/` tooling that **doesn't exist here**. So: a `SKILL.md` (pushy description, 5 modes) + `references/reference.md` (10 artifact templates). No plugin.json edit needed.
- **5 modes:** INTAKE · VENDOR-REVIEW · BUY-VS-BUILD · COMPLIANCE-SCOPE · REGISTRY-STATUS. Registries persist as Markdown under `wiki/governance/` (or `docs/governance/`); decision-log append-only.
- **Domain invariants:** ApprovalEntry scoped to (use case × tool), never transfers; acquisition/sunset triggers invalidate dependent approvals + spawn a migration checklist; asset with no approval ⇒ shelfware.
- **Handoffs:** down = approved intake → shift-left Gate 1 (packet w/ trace IDs); up = shift-left escalates governance Qs here; sideways = evidence → solutioning. Vocabulary disjoint (satisfies eval E6).

## Recent Changes

- Created: `skills/product-management-layer/SKILL.md` + `references/reference.md`.
- Patched: `skills/wiki/references/shift-left/` (Gate 0 escalation + dead-link fix), README Skills table.
- Updated: [[Product Management Layer Skill]] (planned→implemented), [[index]], [[log]] (impl entry), [[hot]].
- Committed: 2 commits (shift-left patch; wiki plan filing). Skill impl + wiki updates still uncommitted.

## Active Threads

- **pm-layer evals**: E1–E8 (E1 golden = Embrace.ai sunset; E5/E6 negative triggers) are **documented but not encoded/run**. Next step if wanted.
- **`plugin.json`**: pre-existing version bump 0.3.0→0.4.0, still uncommitted (user-managed).
- **RLM → wiki-query**: design filed ([[RLM-Optimized Wiki Querying]]), not implemented.
