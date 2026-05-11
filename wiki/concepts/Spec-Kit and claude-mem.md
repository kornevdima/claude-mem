---
type: concept
title: "Spec-Kit and claude-mem"
created: 2026-05-10
updated: 2026-05-10
tags:
  - architecture
  - sdd
  - spec-driven
  - tooling-comparison
  - design-decision
status: evergreen
related:
  - "[[SDLC Wiki Concerns]]"
  - "[[Project Profile]]"
sources:
  - "[[spec-kit-research]]"
---

# Spec-Kit and claude-mem

How GitHub's [spec-kit](https://github.com/github/spec-kit) toolkit relates to claude-mem, why we recommend coexistence over integration, and where each tool wins.

## TL;DR

**Spec-kit and claude-mem solve different problems and should be used together, not merged.**

- **spec-kit** owns the **pre-implementation feature workflow**: turning a fuzzy idea into an executable spec → plan → tasks → code, one feature at a time.
- **claude-mem** owns the **long-term project knowledge layer**: persistent wiki, sources, decisions, code graph, history, BA-driven product documentation that doesn't always lead to code.

Recommend both. Integrate neither — at least not now. (See "Future option" at the end.)

## What spec-kit is

CLI toolkit installed via `uvx`. Scaffolds a five-phase per-feature workflow:

1. `/speckit.constitution` — project-wide principles (`.specify/memory/constitution.md`)
2. `/speckit.specify` — user stories + acceptance criteria, tech-agnostic
3. `/speckit.plan` — technical translation, including `data-model.md`, `contracts/`, `research.md`
4. `/speckit.tasks` — dependency-ordered task list
5. `/speckit.implement` — executes tasks via the AI agent

Each feature lives in its own `.specify/specs/<feature>/` tree. Ships integrations for 30+ AI agents (Claude Code, Cursor, Copilot, Gemini CLI, Codex, etc.).

Core thesis: *"Specifications don't serve code — code serves specifications."* Spec is the source of truth; code regenerates from it.

## How they compare

| Dimension | spec-kit | claude-mem |
|---|---|---|
| **Granularity** | Per-feature spec tree | Project-wide, compounding wiki |
| **Lifecycle** | Pre-implementation; archive after | Persistent; accumulates across years |
| **Scope** | "What to build" (intent → tasks → code) | "What we know" (sources, decisions, history, code graph) |
| **Cross-feature memory** | Constitution provides principles only | Hot cache + index + graph layer + full search |
| **Author model** | Human + AI dialogue, human drives | Human ingests / saves; AI synthesizes |
| **Output of the tool** | Code (eventually) | Knowledge (persistent) |
| **Storage** | `.specify/specs/<feature>/` | `wiki/` (Mode B/C + concerns) |
| **Replaces what?** | Per the GitHub blog: *"wikis nobody reads"* — the pre-spec feature-requirements slice | The wiki itself, but as a different abstraction |
| **Code-graph awareness** | None | graphify layer (`graphify-out/`) |

## Where they overlap (real tension)

| Concept | spec-kit name | claude-mem name |
|---|---|---|
| Project rules / agent context | `.specify/memory/constitution.md` | `AGENTS.md` |
| Research notes per feature/topic | `research.md` (per feature) | `wiki/sources/` (project-wide) + `autoresearch` skill |
| Architecture / decision rationale | `plan.md` | `wiki/decisions/` (Mode B ADRs) |
| Feature-level workflow / task tracking | `tasks.md` | None natively; spec-kit fills this gap |

If a team uses both, the constitution-vs-AGENTS.md duplication is the most likely source of confusion. Recommend keeping `AGENTS.md` canonical for general project-wide agent rules, and limiting `constitution.md` to the spec-driven principles unique to that workflow.

## Where they're complementary

| Layer | Owner |
|---|---|
| Pre-implementation feature workflow (intent → spec → plan → tasks → code) | **spec-kit** |
| Long-term knowledge (sources, decisions log, research, code graph, history) | **claude-mem** |
| BA-driven product documentation that doesn't lead to code (stakeholder maps, intel, deliverables, comms) | **claude-mem Mode C** — spec-kit doesn't address this |
| Code graph / structural retrieval | **claude-mem** graphify layer |
| Feature spec history searchable across past features | Neither natively. Future option: ingest completed `.specify/specs/<feature>/spec.md` into `wiki/sources/`. |

## The BA angle (the critical fork)

Spec-kit's methodology doc names BAs/PMs as spec drivers. The GitHub blog targets developers exclusively. The methodology assumes: **BA writes spec → developer implements**.

This works for BAs whose job is **defining features that will become code**. It doesn't work for:

- **BAs without code-repo access**, who maintain product documentation as their primary deliverable.
- **BAs working on non-code initiatives** (process redesign, vendor evaluations, market intel, stakeholder management).
- **Mixed roles** where the BA never participates in the implementation phase and doesn't need spec.md → code traceability.

**claude-mem Mode C** (Business / Project) is built for those BA workflows. Folders like `stakeholders/`, `decisions/`, `deliverables/`, `intel/`, `comms/` reflect ongoing product-management work that has no implementation handoff at all.

So:

- BA writes feature specs that lead to code → **spec-kit**
- BA maintains product/business documentation, owns deliverables and decisions, no code handoff → **claude-mem Mode C**
- BA does both → **both, layered**

## Concerns we explicitly considered (and ruled against integration)

1. **Per-feature granularity loses cross-feature memory.** Spec-kit doesn't index past specs against current ones. claude-mem's hot cache, `wiki/index.md`, and graph layer do.
2. **Constitution overlaps with `AGENTS.md`.** Two sources of "project principles" creates ambiguity.
3. **Workflow lock-in.** Spec-kit's 5-phase flow is opinionated. Not every team works that way.
4. **No bridge to historical knowledge.** Spec-kit's `research.md` is per-feature; doesn't see past wiki content.
5. **Reinvention cost.** Spec-kit is mature, well-documented, has 30+ integrations. Building our own version (option D in the original analysis) is high cost, low leverage.

## Decision: option B (recommend, don't integrate)

Five options were considered (full table in the [research source](spec-kit-research)):

- A. Ignore spec-kit, document the choice
- **B. Recommend coexistence with documented boundaries** ← chosen
- C. Add a `speckit` concern that scaffolds spec-kit-style folders inside `wiki/`
- D. Adopt spec-kit's methodology natively (build our own)
- E. Light integration: post-implementation hook archives spec.md into `wiki/sources/`

We chose **B** because:

- Spec-kit and claude-mem solve different problems; merging them creates a worse version of both.
- Spec-kit is mature; reinventing it (option D) wastes effort.
- Adding a `speckit` concern (option C) duplicates spec-kit's templates inside our wiki paradigm and creates a maintenance lag — every spec-kit upstream change needs mirroring.
- Option E is appealing as a future enhancement but optional; it doesn't block coexistence today.

## Practical guidance for users

If you adopt both:

- **Keep both directories.** `.specify/` for spec-kit's per-feature trees. `wiki/` for claude-mem's project-wide knowledge.
- **Pick one canonical place for project rules.** Recommend `AGENTS.md` for cross-tool / general rules. `constitution.md` only if you've adopted spec-driven development as your primary methodology.
- **After a feature implements**, optionally drop the completed `spec.md` into `.raw/` and run `wiki-ingest` so the intent becomes searchable through `wiki-query` and visible to the graph layer when it's regenerated.
- **Don't have spec-kit edit `wiki/`.** Their templates assume their `.specify/` layout; mixing them risks corruption of either side.
- **claude-mem's `wiki-faq` skill** documents this comparison; troubleshooting routes for "where does X go" can point users at this page.

## Future option E (deferred)

If users start asking for tighter integration, the lowest-cost addition would be:

- A small skill (`wiki-archive-spec` or similar, ~50 lines) that:
  1. Detects `.specify/specs/<feature>/spec.md` files marked complete
  2. Copies the spec into `wiki/sources/specs/<feature>-<date>.md` with appropriate frontmatter
  3. Triggers `wiki-ingest` on the new file so entities and concepts cross-link into the existing wiki

This makes past intent searchable through the wiki layer without forcing users to manage the same data twice. Filed as a roadmap candidate, not in scope for the current phase work.

## See also

- [[spec-kit-research]] — consolidated source citations
- [[SDLC Wiki Concerns]] — claude-mem's role-based folder model (Mode B + concerns)
- [[Project Profile]] — adjacent concept of pre-implementation context for AI agents (different abstraction)
- `wiki-faq` skill — in-session help that can route users to this comparison
