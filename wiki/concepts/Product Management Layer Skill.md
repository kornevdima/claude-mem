---
type: concept
title: "Product Management Layer Skill"
complexity: advanced
domain: claude-mem
aliases:
  - "product-management-layer"
  - "pm-layer skill"
  - "Gate 0 governance skill"
created: 2026-07-03
updated: 2026-07-03
tags:
  - concept
  - design
  - skill-design
  - implementation-plan
  - governance
  - shift-left
  - implemented
status: implemented
related:
  - "[[Project Profile Skill Suite]]"
  - "[[shift-left-engineering-advisor]]"
  - "[[SDLC Wiki Concerns]]"
  - "[[Spec-Kit and claude-mem]]"
  - "[[maintenance-triggers]]"
  - "[[Generator-Evaluator Pattern]]"
sources:
  - "[[pm-layer-execution-plan]]"
  - "[[campbell-after-ai-hype]]"
---

# Product Management Layer Skill

Design + execution plan for `product-management-layer`, a new **"Gate 0" governance skill** that sits **above** [[shift-left-engineering-advisor]] in the claude-mem skill family. It answers the questions that come *before* engineering starts: is this tool approved, should we buy or build, is the vendor viable, what compliance class applies, are we paying for shelfware. Once a use case is governed and approved, it hands off *down* into shift-left's Gate 1.

Status: **implemented** (2026-07-03) — shipped as a real claude-mem skill at `skills/product-management-layer/` (`SKILL.md` + `references/reference.md`), auto-discovered via the plugin manifest. The shift-left companion patch (upward Governance Escalation) is in place. Source of record for the original governing plan: [[pm-layer-execution-plan]] (raw, immutable).

> **Build note — plan vs repo.** The execution plan assumed the `anthropic-skills` / `ai-agent-builder` / `skill-creator` toolchain (`scripts.package_skill`, `docs/adr/`, `evals/`, `eval-viewer`). That tooling does **not** exist in claude-mem, so the skill was built the **claude-mem way**: a user-facing `SKILL.md` with a pushy description + a `references/reference.md` of artifact templates (progressive disclosure, body < 500 lines). Registries persist as Markdown under a `governance/` area (`wiki/governance/` when a vault exists, else `docs/governance/`). Formal Gates 1–4 docs and PlantUML diagrams were **not** produced. **Update 2026-07-04:** the E1–E8 eval harness IS now encoded — `skills/product-management-layer/evals/` (per-case prompt + regex assertions, date-substituted fixture registry, `run-evals.sh` driving one `claude -p` turn per case and grading transcript + registry diff). Smoke evidence: E5 passes on haiku; E1 fails on haiku (skips `under-review` + never-transfer) — the golden case discriminates by model strength, which is exactly what it is for.

## Where it sits in the skill family

```
product-management-layer   ← Gate 0: governance (NEW)
        │  approved intake ↓         ↑ vendor/tool escalation
shift-left-engineering-advisor  ← Gates 1–4: requirements → ADR
        │                           ↕ evidence questions
solutioning-software-engineer   ← implementation solutioning
```

- **Down-handoff:** an approved use-case intake feeds shift-left **Gate 1** with trace IDs.
- **Up-escalation:** when a vendor / tool / buy-vs-build question surfaces *inside* a shift-left session, shift-left escalates **up** here rather than answering it itself (requires the companion patch, below).
- **Sideways:** evidence questions go to `solutioning-software-engineer`.

This layering complements the [[Project Profile Skill Suite]] (which governs *how code is written*) — the PM layer governs *which tools and vendors are allowed in the first place*.

## v1 capability scope

Narrowed / confirmed at Gate 1 (task P1.4). Five capabilities, eight FRs:

| Capability | FR | What it does |
|---|---|---|
| Use-case intake & approval registry | FR-1 | registry of use case × tool × status × expiry |
| Vendor / tool lifecycle governance | FR-2 | viability scoring, exit assessment, re-review triggers (acquisition / sunset / new use case) |
| Per-use-case compliance scoping | FR-3 | compliance class + data-policy flags, scoped per (use case × tool) |
| Buy-vs-build evaluation | FR-4 | options table, TCO, time-to-value |
| Asset / resource tracking | FR-5 | shelfware detection (paid-for, unused) |
| Portfolio STATUS reporting | FR-6 | approvals near expiry, open triggers, shelfware |
| Handoff contracts | FR-7 | up: shift-left escalates here; down: approved intake → shift-left Gate 1 |
| Decision log | FR-8 | maintained across sessions |

Security / compliance requirements are first-class (separate from NFRs), per shift-left convention. Deferred FRs go to a **Next Steps Registry**.

## Modes

`INTAKE` · `VENDOR-REVIEW` · `BUY-VS-BUILD` · `COMPLIANCE-SCOPE` · `REGISTRY-STATUS`. On-Init questions mirror the shift-left style; core rules inherited: one gate per exchange, `[TBD]` tagging, trace IDs, B2-plain-English.

## Domain model (Gate 2)

Entities: `UseCase` (id, name, riskClass, dataPolicy) · `Tool/Vendor` (viabilityScore, lifecycleStatus, exitPlanRef) · `ApprovalEntry` (useCase × tool, legalStatus, expiry, reviewer) · `ComplianceClass` · `BuyVsBuildEvaluation` (options, TCO, decision, ADR ref) · `ReviewTrigger` (acquisition / sunset / newUseCase / expiry) · `AssetRecord` (subscription, owner, utilization, approvalRef) · `DecisionLogEntry`.

Key business rules:
- An **ApprovalEntry never transfers between tools** — approval is scoped to a (use case × tool) pair.
- A `ReviewTrigger` of type **acquisition / sunset invalidates** dependent ApprovalEntries.
- An **AssetRecord without an ApprovalEntry ⇒ shelfware flag**.

## Trigger vocabulary (collision avoidance)

The PM layer **owns**: vendor, tool approval, buy vs build, subscription, budget, compliance class, shelfware. It must stay **disjoint** from shift-left's: requirements, FR, ADR, spec, architecture, build. This split is the main risk mitigation — negative evals E5/E6 and a description-optimization pass (P5.9) enforce it.

## Eval matrix

Traceability: every FR maps to at least one eval case; the golden case is the **Embrace.ai sunset** retrospective that motivated the skill.

| # | Case | Asserts |
|---|---|---|
| E1 | Embrace.ai sunset (golden) | re-review trigger fired; approval non-transferable; migration checklist (FR-2) |
| E2 | "why not our own rules" + owned Arize sub | TCO options ≥3 incl. paid asset; recommendation + owner decision (FR-4/5) |
| E3 | unused subscription | shelfware flagged w/ renewal action (FR-5) |
| E4 | two use cases, one tool | separate compliance classes; approval per pair (FR-1/3) |
| E5 | negative: "write an ADR for auth" | PM layer does **not** trigger |
| E6 | negative: "should we buy X" inside shift-left | shift-left escalates **up**, doesn't run buy-vs-build (FR-7) |
| E7 | approved intake | output directs to shift-left Gate 1 w/ trace IDs (FR-7) |
| E8 | STATUS mode | portfolio report: expiries, open triggers, shelfware (FR-6) |

Embrace case data lives as **eval fixtures**, never in SKILL.md.

**Encoded 2026-07-04** at `skills/product-management-layer/evals/` (cases + fixtures + runner + README). Fixture dates are placeholders substituted relative to the run date, so E8's near-expiry window never goes stale.

## Execution phases

Gated per `ai-agent-builder` — one gate per exchange, owner approval before advancing:

- **P0 — Setup:** sync `adlc`, git hygiene, feature branch `feat/pm-layer-skill`, verify skill-creator tooling + `claude -p` + PlantUML MCP.
- **P1 — Gate 1 FRs** → `docs/pm-layer/functional-requirements.md`, acceptance criteria, v1 scope checkpoint, registries, Anti-Magic pass.
- **P2 — Gate 2 Domain model** → `docs/pm-layer/domain-model.md` + PlantUML class diagram first.
- **P3 — Gate 3 Architecture** → options table (standalone skill recommended), modes, templates in `references/`, handoff contracts, trigger vocab, registry persistence, component + sequence diagrams.
- **P4 — Gate 4 ADR** → `docs/adr/ADR-NNN-standalone-pm-layer-skill.md` (Nygard).
- **P5 — Build (skill-creator):** SKILL.md draft, `references/reference.md` templates, **companion patch to shift-left** (5b, its own mini eval cycle), encode E1–E8, eval-viewer review before self-assessing, iterate, then description optimization.
- **P6 — Package / install / sync:** package both skills, sync `/tmp` copy back to repo, update `CLAUDE.md` + registries, quality gates, PR → `adlc`, smoke-test E1 + E5.

## Key risks

- **Trigger collision with shift-left** → disjoint vocabulary + negative evals E5/E6 + description optimization.
- **Scope creep (5 capabilities in v1)** → P1.4 checkpoint; deferred FRs to Next Steps Registry.
- **Shift-left patch regresses its own triggering** → the companion patch (P5.4) is a **separate skill-creator cycle** with its own regression eval before install.
- **SKILL.md > 500 lines** → artifact templates in `references/` from the start.
- **Registry persistence undecided** → resolved at Gate 3 (P3.6); blocks the templates (P5.3).

## Definition of done

FRs approved and traced to passing evals E1–E8 · Gates 1–4 artifacts in `docs/` · ADR merged · skill packaged, installed, repo-synced · shift-left companion patch installed without trigger regression · `CLAUDE.md` + registries updated · negative-trigger cases pass.

## External evidence

- [[campbell-after-ai-hype]] (NDC 2026 keynote) independently corroborates the vendor-lifecycle premise: of the 2025 agentic-tool proliferation, "half these products already have disappeared" — incumbents gut startups by hiring away staff rather than acquiring them; no AI vendor is profitable in this line of business; and vendor promises repeat unchanged month over month ("fill the pipeline with noise"). Supports the acquisition/sunset re-review triggers, the viability check in VENDOR-REVIEW, and the practice of dating vendor claims in the decision log.

## Connections

- [[pm-layer-execution-plan]] — the raw, immutable governing plan this page synthesizes
- [[shift-left-engineering-advisor]] — the Gate 1–4 skill this layers above (bidirectional handoff)
- [[Project Profile Skill Suite]] — sibling governance suite (governs how code is written)
- [[SDLC Wiki Concerns]] — the base-mode + opt-in-concern pattern this fits into
- [[Spec-Kit and claude-mem]] — related spec-first / BA-without-code-access positioning
- [[Generator-Evaluator Pattern]] — the eval-before-self-assess discipline (P5.7) applied here
- [[maintenance-triggers]] — where a shipped pm-layer skill would register its cadence
