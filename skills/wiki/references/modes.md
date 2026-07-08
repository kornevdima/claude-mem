# Wiki Modes

claude-mem ships scaffolds aligned with its primary use cases: **Mode B (Repository)** for code projects, **Mode C (Business / Project)** for product documentation, and **Mode ADLC (Agentic Development Life Cycle)** for small teams where AI agents cover the BA / QA / PM roles and humans operate them. B and C can be combined (B+C). ADLC is a separate, additive option (it does not replace B or C); it composes with the `qa` and `ops` concerns and with co-located Mode B code wikis.

> The original LLM Wiki pattern by Andrej Karpathy defined six modes (A: Website, B: Repository, C: Business, D: Personal, E: Research, F: Book / Course). The full historical pattern is preserved at [`.raw/llm-wiki-pattern-spec.md`](../../../.raw/llm-wiki-pattern-spec.md). Modes A, D, E, F are out of scope for the active claude-mem skills but you can still scaffold them by hand from the reference if needed.

---

## Mode B: GitHub / Repository

Use when: "map my codebase", "architecture wiki for my repo", "understand this project"

```
vault/
├── .raw/              # README, git log exports, code dumps, issue exports
├── wiki/
│   ├── modules/       # one note per major module / package / service
│   ├── components/    # reusable UI or functional components
│   ├── decisions/     # Architecture Decision Records (ADRs)
│   ├── dependencies/  # external deps, versions, risk assessment
│   └── flows/         # data flows, request paths, auth flows
├── _meta/
│   ├── index.md
│   └── log.md
└── AGENTS.md
```

Frontmatter for `wiki/modules/` notes:
```yaml
---
type: module           # module | component | decision | dependency | flow
path: "src/auth/"
status: active         # active | deprecated | experimental | planned
language: typescript
purpose: ""
maintainer: ""
last_updated: YYYY-MM-DD
linked_issues: []
depends_on: []
used_by: []
tags: [module]
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

Key wiki pages to create: `[[Architecture Overview]]`, `[[Data Flow]]`, `[[Tech Stack]]`, `[[Dependency Graph]]`, `[[Key Decisions]]`

**Scaffold + content:** Creating the folders is not enough for a useful repo wiki. After vault setup, follow the **`wiki` skill → SCAFFOLD → "Mode B: initial repository pass"** when the vault lives in a codebase: seed `modules/`, `flows/`, `decisions/`, and `dependencies/` from the tree (and keep `domains/entities/concepts/` for ingest-driven notes). That yields the same shape as a manual architecture pass without mislabeling the vault "Mode B" when only generic taxonomy folders exist.

---

## Mode C: Business / Project

Use when: "project wiki", "competitive intelligence", "team knowledge base", "meeting notes", "product documentation"

```
vault/
├── .raw/              # meeting transcripts, Slack exports, docs, emails
├── wiki/
│   ├── stakeholders/  # people, companies, decision-makers
│   ├── decisions/     # key decisions with rationale and date
│   ├── deliverables/  # milestones, outputs, status tracking
│   ├── intel/         # competitor analysis, market research
│   └── comms/         # synthesized meeting notes, key threads
├── _meta/
│   ├── index.md
│   └── log.md
└── AGENTS.md
```

Frontmatter for `wiki/decisions/` notes:
```yaml
---
type: decision         # stakeholder | decision | deliverable | intel | meeting | competitor
status: active         # active | pending | done | blocked | superseded
priority: 3            # 1 (highest) to 5 (lowest)
date: YYYY-MM-DD
owner: ""
due_date: ""
context: ""
tags: [decision]
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

Key wiki pages to create: `[[Project Overview]]`, `[[Stakeholder Map]]`, `[[Decision Log]]`, `[[Competitor Landscape]]`

---

## Mode ADLC: Agentic Development Life Cycle

Use when: a small team runs an **agent-operated delivery lifecycle**. AI agents cover the BA / QA / PM roles, humans operate the agents and hold the gates (scope confirmation, sign-off). Phrases: "agentic delivery wiki", "BA + delivery hub run by agents", "ingest Confluence / Jira / meeting notes into BA deliverables".

ADLC is a **separate, additive** mode. It does not replace Mode B or Mode C. It composes with the `qa` (recommended) and `ops` concerns, and with co-located Mode B code wikis under `services/`.

### Operating model

- **The wiki is canonical.** BA deliverables live here as Markdown with stable IDs. Office files are a generated view, not the source of truth.
- **Multi-wiki topology.** One product / ADLC wiki plus N code wikis (Mode B), linked through `services/` symlinks. Work flows down (impl specs into code wikis) and up (shipped features back into the product wiki).
- **The bundled BA method set is the engine at both ends** (`skills/wiki/references/ba/`, no external plugin). It ingests raw context (Confluence, Jira, meeting notes) into BA deliverables, and exports wiki content to Office formats. See [`ba-suite-pipeline.md`](ba-suite-pipeline.md).
- **Humans operate and gate.** Agents produce; humans confirm scope and sign off. The value is measurable: deliverables produced per feature against the BA / QA / PM time they replace.

### Folder map

```
vault/
├── .raw/                 # Confluence / Jira / meeting-note sources (immutable)
│   └── exports/          # formal Office exports (PlantUML) + HTML tech-doc exports (Mermaid)
├── wiki/
│   ├── requirements/     # registers, RTM, approval packs, change records
│   ├── features/         # feature specs, AS-IS / TO-BE
│   ├── user-stories/     # INVEST backlog + Gherkin
│   ├── gaps/             # gap registers, heatmaps, roadmap
│   ├── stakeholders/     # RACI, power / interest, engagement
│   ├── decisions/        # product / business decisions (not engineering ADRs)
│   ├── deliverables/     # business cases, solution assessments, milestones
│   ├── sprints/          # sprint packs, impediment + retro logs
│   ├── planning/         # BA approach, governance, information mgmt, performance
│   ├── comms/            # circulation memos, synthesis exports, meeting notes
│   ├── sources/          # one summary page per ingested raw source
│   └── meta/             # mission-control board, ba-activity ledger (metrics seam), lint reports
├── services/             # symlinks to code checkouts; each service's code wiki holds its specs (no project-context folder)
└── AGENTS.md
```

Recommended concerns: add `qa` (`test-plans/`, `test-cases/`, `coverage/`, `bugs/`) in almost all cases, since ADLC produces test artifacts. Add `ops` when the product is operated in production.

Frontmatter for `wiki/requirements/` notes (representative; reuse the relevant pattern per folder):
```yaml
---
type: requirement        # requirement | feature | user-story | gap | sprint | ...
req_id: ""               # stable ba-suite ID, never renumber (e.g. FR-001, NFR-001)
status: specified        # specified | implemented | partial | contradicted | approved
moscow: must             # must | should | could | wont
epic: ""
produced_by: ""          # ba-suite skill that authored this (metrics seam)
effort_estimate: ""      # optional, for cost rollups (metrics seam)
feature: ""              # feature / cluster this belongs to (metrics seam)
traces_to: []            # wikilinks to stories / tests / gaps
source: []               # wikilinks to sources/
tags: [requirement]
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

Key wiki pages to create: `[[Project Overview]]`, `[[Requirements Index]]`, `[[Backlog Index]]`, `[[Gap Analysis]]`, `[[Stakeholder Map]]`, `[[Decision Log]]`.

### The pipelines

1. **Ingest** — `ba-suite` converts Confluence / Jira / meeting-note context into BA deliverables (product wiki) with stable IDs and `[[traceability]]` links, and the shift-left `architecture-subagent` refines those into per-service technical specs (in each service's code wiki). This is the "ingest better deliverables" path: structured artifacts, not generic entity / concept extraction. Maps: [`ba-suite-pipeline.md`](ba-suite-pipeline.md) and [`technical-planning.md`](technical-planning.md).
2. **Plan, build, verify** — each service is its own service: its spec lands in the service code wiki, the repo agent builds it, and the feature is verified with the operator's toolset (`docker compose` local run + chrome-devtools MCP e2e + the service's own tests). See [`technical-planning.md`](technical-planning.md).
3. **Sync (session wrap-up)** — when the operator says "end session" or "wrap up", the `wrap-up` skill uses already-loaded context to check git changes across `services/`, inject updates into the code wikis (impl specs, ADRs, plans), reflect shipped features / resolved gaps / new requirements into this wiki, then refresh `hot.md` and append `log.md`. The Stop hook is a backstop nudge.
4. **Export** — reuse `ba-suite`'s Office generation to render wiki content to `.xlsx` / `.docx` under `.raw/exports/`, and push deliverables to the team tracker over MCP (ClickUp or Jira). Formal-export diagrams use PlantUML; living tech docs use Mermaid, HTML-exported to `.raw/exports/`. Mapping + MCP config: [`mcp-setup.md`](mcp-setup.md). Implemented by the `ba-export` skill (+ `ba-export-subagent`); folder + ID conventions are kept export-friendly.

### Sub-agent

The ingest and planning pipelines run through two workers that each cover a whole skill family: `agents/ba-suite-subagent.md` (BA deliverables) and `agents/architecture-subagent.md` (shift-left technical specs). The ADLC pass and the `wrap-up` skill dispatch them one task at a time (parallel where independent) and update `index` / `log` / `hot` after. See [`ba-suite-pipeline.md`](ba-suite-pipeline.md) and [`technical-planning.md`](technical-planning.md).

The per-service **build pipeline** runs five more service-level workers: `agents/feature-builder.md`, `agents/feature-tester.md`, `agents/feature-reviewer.md`, `agents/feature-verifier.md`, `agents/doc-writer.md` (build -> test -> review -> verify -> document; review loops back to builder / tester on changes requested). Export uses `agents/ba-export-subagent.md`. All BA + build + shift-left methods are bundled (`references/ba/`, `references/shift-left/`) — no external plugin.

### Team state sharing

When more than one person (dev, architect, BA / QA, writer) operates agents against the same wiki set, follow [`team-sync.md`](team-sync.md): git as the state bus, role → concern ownership, pull-first / wrap-up-last session protocol, union-merge for `log.md`, regenerate-don't-merge for `hot.md`, machine-local `services/` symlinks.

### Permissions

ADLC is agent-operated: routine project work should run without prompts, destructive operations stay gated. Scaffold `.claude/settings.json` from [`permissions.md`](permissions.md) (`allow` / `ask` / `deny` lists).

### Privacy

ADLC vaults often hold client data. Keep PII (person names, headcount, contract values, staffing) out of the committed wiki: put sensitive context in a gitignored private note (e.g. `proposals/`), and keep role-based RACI / engagement analysis (no named individuals) in the wiki. Anonymize when in doubt.

### Metrics seam

`log.md` records every operation with the skill that ran it; the `produced_by` / `effort_estimate` / `feature` frontmatter fields feed the rollups. Two derived pages in `meta/` consume them: `mission-control.md` (the operator's async delivery board, updated by the dispatcher at stage transitions) and `ba-activity.md` (the cost rollup, refreshed at wrap-up). Formats, update triggers, and the derived-view rule: [`mission-control.md`](mission-control.md). Seed both at scaffold time with empty tables.

---

## Combining Modes (B + C)

Many projects benefit from both layers: a code wiki for engineering and a project wiki for product/business context. When combining:

- Keep folder names distinct. Do not merge `decisions/` between B and C — engineering ADRs (B) and business decisions (C) belong in separate folders so they remain searchable by audience.
- Suggested combined layout: keep all of Mode B's folders (`modules/`, `components/`, `decisions/`, `dependencies/`, `flows/`) and add Mode C's `stakeholders/`, `deliverables/`, `intel/`, `comms/` alongside. Decisions stay split: `wiki/decisions/` (engineering ADRs) and `wiki/business-decisions/` (or `wiki/c-decisions/`).
- The vault `AGENTS.md` should label the mode as `B+C` and list both folder sets under Structure.

A combined vault is the natural fit when developers and a BA share the same repository as their working surface.

---

## Concerns (opt-in folder kits)

A vault's base mode (B / C / B+C) covers the engineering and project layers. **Concerns** are opt-in folder kits that add role-specific artifacts on top of the base — for SDLC teams that include DevOps, QA, security, design, or technical writing alongside the dev / BA work.

The full design rationale is at [[SDLC Wiki Concerns]] in the wiki. Per-concern reference docs (folder map, frontmatter, key pages) live in `references/concerns/<name>.md`.

| Concern | Folders added | Reference doc |
|---|---|---|
| `ops` | `runbooks/`, `incidents/`, `services/`, `observability/` | [`concerns/ops.md`](concerns/ops.md) |
| `qa` | `test-plans/`, `test-cases/`, `bugs/`, `coverage/` | [`concerns/qa.md`](concerns/qa.md) |
| `sec` | `threat-models/`, `compliance/`, `security-decisions/` | [`concerns/sec.md`](concerns/sec.md) |
| `design` | `designs/`, `user-research/` | [`concerns/design.md`](concerns/design.md) |
| `writing` | `user-docs/`, `api-docs/`, `tutorials/` | [`concerns/writing.md`](concerns/writing.md) |

### When to add a concern

| Add | When |
|---|---|
| `ops` | Production deployments, on-call rotation, incident response |
| `qa` | Formal test plans, bug-tracking discipline, regression coverage |
| `sec` | Threat modeling, compliance frameworks (SOC2, ISO, HIPAA), security review process |
| `design` | UX designers on the team, user research practice |
| `writing` | Public/external user-facing docs (API reference, tutorials) |

Skip a concern if the role exists informally (everyone wears a DevOps hat occasionally) but doesn't produce structured artifacts. Concerns are about **artifacts**, not roles.

### Composition examples

| Team shape | Mode | Concerns |
|---|---|---|
| Solo dev | `B` | none |
| Small product team | `B+C` | none |
| Platform / SRE team | `B` | `ops`, `qa` |
| Regulated SaaS | `B+C` | `ops`, `qa`, `sec` |
| Full SDLC org | `B+C` | `ops`, `qa`, `sec`, `design`, `writing` |
| Documentation team | `C` | `writing` |

### Recording in the vault `AGENTS.md`

Add a `Concerns:` line below `Mode:`. Example:

```markdown
Mode: B+C
Concerns: ops, qa, sec
Purpose: Internal billing platform, dev + product + ops + QA + security all use this vault.
```

When a concern's folders exist, the corresponding reference doc applies. The `wiki-ingest` and `wiki-query` skills cross-link new pages into concern folders automatically when matches exist.
