# Execution Plan — `product-management-layer` Skill

**Repo:** `kornevdima/claude-mem`, branch `adlc`
**Execution environment:** Claude Code, local (IntelliJ terminal)
**Governing workflows:** `ai-agent-builder` (modes/gates/git discipline) + `skill-creator` (draft → eval → iterate → package)
**Relationship to skill family:** New "Gate 0" governance layer above `shift-left-engineering-advisor`; bidirectional handoff contracts with `shift-left-engineering-advisor` and `solutioning-software-engineer`.

**Candidate capability scope (v1 narrowing decided at Gate 1, task P1.4):**
1. Use-case intake & approval registry (use case × tool × status × expiry)
2. Vendor/tool lifecycle governance (viability, exit plan, re-review triggers)
3. Per-use-case compliance scoping
4. Buy-vs-build evaluation with TCO artifact
5. Asset/resource tracking (shelfware detection) + portfolio STATUS reporting

---

## Phase 0 — Repo Context & Session Setup

**Entry criteria:** local clone available; Claude Code session opened at repo root.

| # | Task | Command / Artifact |
|---|------|--------------------|
| P0.1 | Checkout & sync branch | `git checkout adlc && git pull` |
| P0.2 | Read project context | Read `CLAUDE.md` (structure, conventions, known issues) |
| P0.3 | Git hygiene per ai-agent-builder | `git status --short`, `git stash list`, `git diff --stat` — commit or resolve anything dirty **before** new work; ask owner about stashes, never drop silently |
| P0.4 | Inventory existing ADLC structure | `tree -L 2` — list existing skills, `docs/`, `evals/` conventions; record deltas from ai-agent-builder standard layout |
| P0.5 | Confirm target locations | Skill source dir (`product-management-layer/`), `docs/adr/` numbering, evals location (`product-management-layer/evals/`) |
| P0.6 | Create feature branch | `git checkout -b feat/pm-layer-skill` |
| P0.7 | Verify tooling | `python -m scripts.package_skill --help` available (skill-creator scripts), `claude -p` works (needed for Phase 5 description optimization), PlantUML MCP renders |

**Exit criteria:** clean tree on feature branch; conventions confirmed; any deviation from standard layout recorded in `CLAUDE.md` update draft.

---

## Phase 1 — Gate 1: Functional Requirements for the Skill (MANAGE mode)

**Entry criteria:** Phase 0 complete. **Rule:** one gate per exchange; artifact presented; owner approval required before Phase 2.

| # | Task | Notes |
|---|------|-------|
| P1.1 | Draft FR document `docs/pm-layer/functional-requirements.md` | FR-1 Use-case intake & registry; FR-2 Vendor lifecycle (viability scoring, exit assessment, re-review triggers on acquisition/sunset/new use case); FR-3 Per-use-case compliance scoping (class + data policy flags); FR-4 Buy-vs-build evaluation (options table, TCO, time-to-value); FR-5 Asset tracking & shelfware detection; FR-6 Portfolio STATUS reporting; FR-7 Handoff contracts (up: shift-left escalates vendor/tool questions here; down: approved intake feeds shift-left Gate 1); FR-8 Decision log maintenance |
| P1.2 | Acceptance criteria per FR | Testable — these become eval assertions in Phase 5 (traceability: FR → eval case ID) |
| P1.3 | Security/compliance requirements separate from NFRs | Per shift-left convention (SRs are first-class) |
| P1.4 | **v1 scope decision checkpoint** | Owner narrows or confirms FR-1..FR-8 for v1; deferred FRs go to Next Steps Registry |
| P1.5 | Initialize Feature Registry + Next Steps Registry tables | In the FR doc |
| P1.6 | Anti-Magic pass | Any "automatically re-reviews" behavior gets explicit infrastructure/trigger requirements |
| P1.7 | Commit | `docs: add pm-layer FRs (gate 1)` |

**Exit criteria:** owner answers "Does this look right?" affirmatively; registries initialized.

---

## Phase 2 — Gate 2: Domain Model (ARCHITECT mode)

**Entry criteria:** Gate 1 approved.

| # | Task | Notes |
|---|------|-------|
| P2.1 | Define entities | `UseCase` (id, name, riskClass, dataPolicy), `Tool/Vendor` (viabilityScore, lifecycleStatus, exitPlanRef), `ApprovalEntry` (useCase × tool, legalStatus, expiry, reviewer), `ComplianceClass`, `BuyVsBuildEvaluation` (options, TCO, decision, ADR ref), `ReviewTrigger` (type: acquisition/sunset/newUseCase/expiry), `AssetRecord` (subscription, owner, utilization, approvalRef), `DecisionLogEntry` |
| P2.2 | Relationships + cardinality | e.g., UseCase 1..N ApprovalEntry; Tool 1..N ReviewTrigger |
| P2.3 | Business rules | ApprovalEntry never transfers between tools; ReviewTrigger of type acquisition/sunset invalidates dependent ApprovalEntries; AssetRecord without ApprovalEntry ⇒ shelfware flag |
| P2.4 | Field ownership | Owner input vs skill-generated vs external-source |
| P2.5 | PlantUML **class diagram first** → `docs/pm-layer/domain-model.md` + `.puml` alongside | House style: `!theme plain`, `#FEFEFE` bg, `#2B579A` accents |
| P2.6 | Commit | `docs: pm-layer domain model (gate 2)` |

**Exit criteria:** owner approval. Storage format (markdown tables in artifacts vs JSON registry file) is **not** decided here — that is Gate 3.

---

## Phase 3 — Gate 3: Skill Architecture (ARCHITECT mode)

**Entry criteria:** Gate 2 approved.

| # | Task | Notes |
|---|------|-------|
| P3.1 | Options & trade-offs table | A: standalone skill (recommended); B: extend shift-left with Gate 0; C: plugin bundling family (end-state). Decision recorded in Phase 4 ADR |
| P3.2 | Mode design | `INTAKE`, `VENDOR-REVIEW`, `BUY-VS-BUILD`, `COMPLIANCE-SCOPE`, `REGISTRY-STATUS`; On-Init questions mirroring shift-left style |
| P3.3 | Artifact templates → `references/reference.md` | Approval-registry table, vendor viability scorecard, TCO comparison, compliance classification sheet, decision-log format; SKILL.md body stays <500 lines via progressive disclosure |
| P3.4 | Handoff contracts | "Governance Escalation" section (down: hand approved intake to shift-left Gate 1 with trace IDs; sideways: evidence questions to solutioning-software-engineer). **Separate workstream flag:** adding the upward escalation into `shift-left-engineering-advisor` is a modification of an existing skill ⇒ its own skill-creator cycle (see Phase 5b) |
| P3.5 | Trigger vocabulary design | PM layer owns: vendor, tool approval, buy vs build, subscription, budget, compliance class, shelfware. Must be disjoint from shift-left's: requirements, FR, ADR, spec, architecture, build. Cross-trigger eval cases derive from this table |
| P3.6 | Registry persistence decision | Where ApprovalEntry/AssetRecord state lives between sessions (project doc vs JSON in repo) — maps domain model to storage |
| P3.7 | Component + sequence PlantUML diagrams | Skill family layering; INTAKE→approval→handoff sequence |
| P3.8 | Commit | `docs: pm-layer skill architecture (gate 3)` |

**Exit criteria:** owner approval of architecture, mode list, trigger vocabulary, storage choice.

---

## Phase 4 — Gate 4: ADR

| # | Task | Notes |
|---|------|-------|
| P4.1 | `docs/adr/ADR-NNN-standalone-pm-layer-skill.md` (Nygard format, full prose) | Context (skill family, this retrospective as motivating case), Decision (option from P3.1), Alternatives considered, Consequences (trigger-collision risk, maintenance of two skills, plugin path), FR references |
| P4.2 | Commit | `docs: ADR-NNN pm-layer skill decision (gate 4)` |

**Exit criteria:** ADR approved. Implementation may start.

---

## Phase 5 — BUILD via skill-creator Workflow

**Entry criteria:** Gates 1–4 approved. All edits in a writable copy: `/tmp/product-management-layer/`, synced to repo at the end.

### 5a. Draft

| # | Task | Notes |
|---|------|-------|
| P5.1 | Write SKILL.md frontmatter | Name `product-management-layer`; **pushy description** listing trigger phrases: "should we use vendor X", "buy vs build", "is this tool approved", "we're paying for X and not using it", "compliance class for this use case", "vendor is shutting down / acquired" |
| P5.2 | Write SKILL.md body | On Init, mode routing, core rules (one gate per exchange, [TBD] tagging, trace IDs), Governance Escalation, response style — consistent with shift-left conventions; B2-plain-English rule inherited |
| P5.3 | Write `references/reference.md` | All artifact templates from P3.3 |

### 5b. Companion change (separate mini-cycle)

| # | Task | Notes |
|---|------|-------|
| P5.4 | Patch `shift-left-engineering-advisor` | Add upward "Governance Escalation" pointer. Full skill-creator treatment: copy, edit, eval that its existing triggering did not regress, package, re-install |

### 5c. Evals

| # | Eval case | Asserts (trace to FR) |
|---|-----------|------------------------|
| E1 | Embrace.ai sunset scenario (this retrospective, golden case) | Re-review trigger fired; approval marked non-transferable; migration checklist produced (FR-2) |
| E2 | "Why not our own rules" + owned Arize subscription | TCO options table with ≥3 options incl. already-paid asset; recommendation + owner decision requested (FR-4, FR-5) |
| E3 | Unused subscription in inventory | Shelfware flagged with renewal action (FR-5) |
| E4 | Two use cases, one tool | Separate compliance classes per use case; approval scoped per pair (FR-1, FR-3) |
| E5 | Cross-trigger negative: "write an ADR for the auth service" | PM layer does NOT trigger (P3.5) |
| E6 | Cross-trigger negative: "should we buy tool X" inside shift-left session | Shift-left escalates UP, does not run buy-vs-build itself (FR-7, P5.4) |
| E7 | Handoff positive: approved intake | Output explicitly directs to shift-left Gate 1 with trace IDs (FR-7) |
| E8 | STATUS mode | Portfolio report: approvals near expiry, open triggers, shelfware (FR-6) |

| # | Task | Notes |
|---|------|-------|
| P5.5 | Encode E1–E8 in `evals/` (benchmark.json + fixtures) | Embrace case data lives here as fixtures — **never** in SKILL.md |
| P5.6 | Run test prompts with skill loaded (subagents in Claude Code) | Baselines optional |
| P5.7 | **Generate eval viewer BEFORE self-assessing** | `eval-viewer/generate_review.py` — owner reviews first |
| P5.8 | Iterate: revise → rerun → review | Repeat until owner satisfied |
| P5.9 | Description optimization (only after content is stable) | `python -m scripts.run_loop --eval-set trigger-eval.json --skill-path /tmp/product-management-layer --model <current> --max-iterations 5 --verbose`; apply `best_description` (test-score selected) |

**Exit criteria:** E1–E8 pass; owner sign-off on qualitative review; optimized description applied.

---

## Phase 6 — Package, Install, Sync

| # | Task | Notes |
|---|------|-------|
| P6.1 | `python -m scripts.package_skill /tmp/product-management-layer` → `.skill`; install | Same for patched shift-left skill (P5.4) — preserve its original name |
| P6.2 | Sync `/tmp` copy back to repo source on `feat/pm-layer-skill` | Installed version == repo version |
| P6.3 | Update `CLAUDE.md` | New skill location, registry storage location, family layering note |
| P6.4 | Update Feature Registry (FR statuses → implemented) and Next Steps Registry (deferred FRs, plugin packaging as candidate) | |
| P6.5 | Quality gates checklist | PlantUML renders; JSON parses; no secrets; docs updated; conventional commits |
| P6.6 | Merge | PR `feat/pm-layer-skill` → `adlc`; smoke-test E1 + E5 post-install |

**Exit criteria:** merged; installed skill verified in a fresh session.

---

## Risks / RAID

| Type | Item | Mitigation |
|------|------|------------|
| Risk | Trigger collision with shift-left skill | Disjoint vocabulary (P3.5) + negative evals E5/E6 + P5.9 optimization |
| Risk | Scope creep (5 capabilities in v1) | P1.4 checkpoint; deferred FRs to Next Steps Registry |
| Risk | Shift-left patch regresses its own triggering | P5.4 mini eval cycle before install |
| Risk | SKILL.md exceeds 500 lines | Templates in references/ from the start |
| Issue | Registry state persistence undecided | Resolved at P3.6, blocks P5.3 |
| Dependency | `claude -p` + skill-creator scripts available locally | Verified at P0.7 |
| Assumption | adlc branch layout matches ai-agent-builder convention | Verified/recorded at P0.4–P0.5 |

## Definition of Done

FRs approved and traced to passing evals E1–E8 · Gates 1–4 artifacts in `docs/` · ADR merged · skill packaged, installed, repo-synced · shift-left companion patch installed without trigger regression · CLAUDE.md + registries updated · negative-trigger cases pass.
