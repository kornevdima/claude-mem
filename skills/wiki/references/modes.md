# Wiki Modes

claude-mem ships two scaffolds aligned with its primary use cases: **Mode B (Repository)** for code projects and **Mode C (Business / Project)** for product documentation. They can be combined when a project needs both layers.

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
