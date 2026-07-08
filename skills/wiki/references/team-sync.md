# Team state sharing across wikis (multi-role, multi-wiki)

How a team — developers, architects, BA / QA, tech writers — keeps state coherent when several people (and their agents) work against the same ADLC wiki set: one product wiki plus N service code wikis. Complements [`modes.md`](modes.md) (folder maps) and the [[Wiki Sharing Patterns]] concept page (tooling / topology options for access). This doc is the operating protocol.

## Principles

1. **Git is the state bus.** Every wiki lives in a git repo; sharing state = commit + push + pull. No live-sync layer is required for agent-operated work — agents write in sessions, and sessions sync at boundaries. (Real-time co-editing tools like Relay / Obsidian Sync remain an option for human editors; see [[Wiki Sharing Patterns]].)
2. **IDs are the foreign keys.** State crosses wikis by stable ID (`FR-*`, `ADR-{SVC}-*`, `TC-*`, story IDs) and wikilink pointers — never by copying content. Every fact has exactly ONE home wiki; everything else points at it.
3. **One fact, one home.** Business view (requirements, features, gaps, decisions) lives in the product wiki. Technical truth (specs, ADRs, module notes, verification records) lives in the owning service's code wiki. The product `features/` page links down; the service spec traces up via `traces_to:`. Duplication is drift waiting to happen.
4. **Singletons are the merge hotspots.** `log.md`, `hot.md`, `index.md`, and `_index.md` files are per-wiki singletons that every session touches. The conventions below exist to make them merge-safe; everything else (one page per record / requirement / spec) merges trivially because concurrent sessions touch different files.

## Role → concern ownership

Ownership means "arbiter of conflicts and approver of changes in that area", not exclusive write access — any role's agent may propose edits anywhere, but the owner resolves disagreement.

| Role | Owns (product wiki) | Owns (service code wikis) |
|---|---|---|
| BA / PM | `requirements/`, `user-stories/`, `stakeholders/`, `gaps/`, `deliverables/`, `planning/` | — |
| Architect | `decisions/` (business-facing) | `specs/` (gates), `decisions/` (ADRs), `flows/` |
| Developer | — | `modules/`, `components/`, `plans/`, implementation notes |
| QA | `test-plans/`, `test-cases/`, `coverage/`, `bugs/` | verification records, e2e coverage notes |
| Tech writer | `user-docs/`, `tutorials/`, `api-docs/` | — |
| Operator (any) | `hot.md`, `log.md`, `index.md` via wrap-up | same, per service wiki |

Record the mapping in the vault `AGENTS.md` (a `Roles:` block under `Mode:` / `Concerns:`) so every agent session knows whose area it is editing and who gates what.

## Session protocol

1. **Pull first.** At session start, `git pull` the vault and each `services/<svc>` checkout you will touch. Then read `hot.md`. A stale wiki is worse than no wiki: you inherit contradictions someone else already resolved.
2. **Work in your concern.** Agents write into the folders their role owns; edits to another role's area are proposals — flag them in the session report rather than silently rewriting.
3. **Wrap up before you leave.** The `wrap-up` skill is the sync point: down-propagate to code wikis, up-propagate to the product wiki, archive delivered plans, reconcile rollups, refresh `hot.md`, append `log.md`.
4. **Commit and push the wikis** (when the operator approves). Un-pushed wiki state doesn't exist for the rest of the team.

One writer per wiki area at a time is advisory, not enforced — concurrent sessions on *different* concerns merge cleanly by construction. Two sessions in the same folder should coordinate (or accept that the second `Edit` fails on the modified file — the built-in backstop that has worked in production).

## Merge-hotspot conventions

- **`log.md` — union merge.** Append-only, newest at top, one dated `## [...]` block per entry. Add a `.gitattributes` line to each wiki repo so concurrent appends merge automatically instead of conflicting:

  ```gitattributes
  wiki/log.md merge=union
  **/wiki/log.md merge=union
  ```

  Union merge keeps both sides' lines; because entries are self-contained dated blocks, order glitches are cosmetic and the next wrap-up can reorder. Keep entries one-line-per-fact pointers (full records are their own pages) — this is also what keeps the log greppable.
- **`hot.md` — regenerate, never merge.** It is a cache of "what's hot now", scoped to the last session. On conflict, take either side and let the next wrap-up regenerate it from `log.md` + the session. Never hand-merge two hot caches.
- **`meta/mission-control.md` / `meta/ba-activity.md` — derived, regenerate from records.** Like `hot.md`, never hand-merge: on conflict take either side, then reconcile the board against the verification / review records and the ledger against `produced_by` frontmatter (see [`mission-control.md`](mission-control.md)). The records are the truth; the pages are views.
- **`index.md` / `_index.md` — derived counts, sorted entries.** Keep catalog lines one-per-page and alphabetically / chronologically sorted so concurrent additions land in different diff hunks. Counts are derived — when in doubt, `wiki-lint` reconciles them; don't fight over them in a merge.
- **Records are pages.** Verification records, review records, retros, decision records: one file each, named with feature + date. Two sessions never conflict on a file only one of them creates.

## Cross-machine invariants

- **`services/` symlinks are machine-local.** Gitignore them; each teammate recreates their own (a `bin/` setup script or a documented one-liner per service). Committed wiki content must never embed a teammate's absolute checkout path — wikilinks and `traces_to:` IDs are location-independent, and graphify already stores project-root-relative paths.
- **Same wiki, any host.** Nothing in the vault may assume a particular editor (Obsidian vs IDE), OS, or clone location. The wiki is plain Markdown + git; that is the portability contract.

## Status fields are the shared state machine

Cross-role coordination runs on frontmatter status, not on chat: `specified → implemented → partial/contradicted → verified → delivered` (requirements/specs), `proposed → shipped` (features), `draft → published` (docs), `manual → e2e` (coverage tags). A role's agent advances only the statuses its role owns (QA flips verification states, BA flips requirement states, wrap-up flips features). Downstream roles trust the status field instead of re-deriving it — which is why the honesty rules in the worker agents (evidence with exit codes, no tag without a green test, no PASS on the wrong target) are load-bearing for the whole team.

## Non-git participants

A stakeholder who reads but doesn't run agents gets a derived view — Obsidian Publish, a static-site export of the product wiki, or the `.raw/exports/` Office bundle from `ba-export`. Editors without code access are the one case where the wiki may live in a sibling repo instead of co-located; the trade-offs live in [[Wiki Sharing Patterns]].
