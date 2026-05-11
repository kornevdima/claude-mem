---
type: concept
title: "SDLC Wiki Concerns"
created: 2026-05-09
updated: 2026-05-09
tags:
  - architecture
  - modes
  - sdlc
status: evergreen
related:
  - "[[Project Profile]]"
  - "[[Context Engineering for Coding Agents]]"
sources:
  - "[[sdlc-team-documentation-research]]"
---

# SDLC Wiki Concerns

claude-mem started with two scaffolds: **Mode B (Repository)** for developers and **Mode C (Business / Project)** for business analysts. Real engineering organizations have more roles than that: DevOps / SRE, QA / QC, security, designers, technical writers, product managers. This page captures the design pattern claude-mem adopts to serve them: **a base mode plus opt-in concerns**.

## Why not "one mode per role"?

Three findings from the research drove the decision:

1. **Real teams aren't single-role.** A repo gets touched by dev, ops, QA, security, and product simultaneously. Forcing a vault to pick "DevOps mode" or "QA mode" misrepresents the cross-functional reality.
2. **Each role has canonical artifact types**, but those artifacts coexist with engineering ADRs, business decisions, etc. They are additive, not competitive. (Source: [[sdlc-team-documentation-research]].)
3. **Spotify Backstage's "docs-like-code" pattern** (one component = one repo = one doc site, with metadata in YAML) is the modern reference. claude-mem's vault-co-located-with-repo design already fits this. The natural extension is letting one vault host multiple role-specific document classes side by side.

The 6-mode Karpathy pattern (preserved at `.raw/llm-wiki-pattern-spec.md`) was role-agnostic. SDLC roles need a different axis.

## The "concerns" pattern

A vault has:

- **One base mode**: `B`, `C`, or `B+C`. Defines the core scaffold (modules / flows / decisions for B; stakeholders / decisions / deliverables for C).
- **Zero or more concerns**: opt-in folder groups that add role-specific artifacts on top of the base.

Concerns supported by claude-mem (one reference doc each in `skills/wiki/references/concerns/`):

| Concern | Folders added | Role |
|---|---|---|
| `ops` | `runbooks/`, `incidents/`, `services/`, `observability/` | DevOps / SRE |
| `qa` | `test-plans/`, `test-cases/`, `bugs/`, `coverage/` | QA / QC / Test engineers |
| `sec` | `threat-models/`, `compliance/`, `security-decisions/` | Security |
| `design` | `designs/`, `user-research/` | UX designers |
| `writing` | `user-docs/`, `api-docs/`, `tutorials/` | Technical writers |

Each concern document gives folder structure, frontmatter shape, and key wiki pages to create.

## Composition examples

| Team shape | Mode | Concerns |
|---|---|---|
| Solo dev | `B` | none |
| Small product team | `B+C` | none |
| Platform / SRE team | `B` | `ops`, `qa` |
| Regulated SaaS | `B+C` | `ops`, `qa`, `sec` |
| Full SDLC org | `B+C` | `ops`, `qa`, `sec`, `design`, `writing` |
| Documentation team | `C` | `writing` |

## SCAFFOLD flow impact

The `wiki` skill's SCAFFOLD operation gains one question:

1. (existing) "Code project (B), product docs (C), or both (B+C)?"
2. (new) "Which concerns apply? Pick any of: ops, qa, sec, design, writing — or 'none'."
3. (existing) "In one sentence, what is this vault for?"

The vault `AGENTS.md` records both `Mode:` and `Concerns:` so other agents reading it know what folders are meaningful in this vault.

## Why this isn't persona presets

A neighboring design option was named presets ("Solo dev", "Platform team", "Full SDLC team") that bundle preset combinations of base + concerns. We rejected this in favor of pure composition: presets become a feature creep surface (every team thinks their preset should ship), they go stale as teams evolve, and the concerns model is already small enough that picking from a checklist isn't friction. The team-shape table above can serve as informal guidance without baking presets into the skill.

## What this leaves out

- **Roles vs. concerns**. A "concern" is a folder group, not a role. A DevOps engineer working in a vault uses `ops` folders most, but anyone can read or contribute. This avoids role-as-permission framing, which the wiki layer doesn't enforce.
- **Per-component sub-vaults**. Backstage scales by giving each component its own doc site. claude-mem currently has one vault per project; deeper sub-vault hierarchy is a Phase-N+1 question if needed.
- **Bidirectional links between concerns**. An incident postmortem (`ops`) often references an ADR (`B`) and a bug report (`qa`). The wiki layer's wikilinks already do this naturally — no special concern-aware machinery needed.
