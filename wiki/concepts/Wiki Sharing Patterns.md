---
type: concept
title: "Wiki Sharing Patterns"
created: 2026-05-10
updated: 2026-05-10
tags:
  - architecture
  - sharing
  - team-collaboration
  - microservices
  - design-decision
status: developing
related:
  - "[[SDLC Wiki Concerns]]"
  - "[[Spec-Kit and claude-mem]]"
sources:
  - "[[wiki-sharing-research]]"
---

# Wiki Sharing Patterns

How a claude-mem wiki gets shared across roles and across services. **This is a research-and-options page** — claude-mem keeps its current default (one wiki per project, co-located with code) until field feedback motivates a change.

> [!note] Operational protocol shipped (2026-07-03)
> The multi-role / multi-wiki **state-sharing protocol** — role → concern ownership, pull-first / wrap-up-last sessions, merge conventions for `log.md` / `hot.md` / indexes, machine-local symlinks, status fields as the cross-role state machine — now lives in `skills/wiki/references/team-sync.md`. This page remains the tooling / topology comparison behind it.

## Three orthogonal sub-problems

When a team starts using claude-mem beyond a solo developer, three questions emerge:

1. **Multi-role access** — devs, BAs, QA, security all want the wiki, but they have different access rights, tools, and editing patterns.
2. **Multi-service structure** — monorepo with N services, or N repos, all under one team. Where do their wikis live?
3. **Wiki location** — co-located with code (current default) versus a sibling directory or a separate repo. The choice affects every other decision.

Each is independent of the others. The same team may pick "co-located + git-based sharing + one wiki per repo" or "separate repo + Relay + federated services" — every combination has trade-offs.

## Sub-problem 1: Multi-role access

Six approaches, each viable for a different team shape:

| Approach | Cost | Real-time? | Permissions | Non-tech friendly |
|---|---|---|---|---|
| **Git repo, everyone clones** | Free | No (commit-based) | Repo-level only | No (needs git literacy) |
| **Obsidian Sync — Teams** | ~$8/user/mo | Merge on sync, no live cursors | Vault-wide only | **Yes** |
| **Relay plugin** | Free up to 3; $5–18/user/mo above | **Yes (CRDT, live cursors)** | Folder-level RBAC at $6/mo+ | **Yes** |
| **Cloud folder** (Dropbox / Nextcloud / iCloud) | Free–cheap | No | Folder via cloud provider | **Yes** |
| **Obsidian Publish** (read-only web) | $10/mo per site | N/A | Public or password | **Yes (read-only)** |
| **Static site export** (MkDocs / Docusaurus / Mintlify) | Free–cheap | N/A | Hosting-dependent | Yes (web UI) |

### How to pick

- **All-developer team** → git-based. Free, fits the workflow, no setup. Limitation: no live cursors, occasional merge conflicts on `wiki/index.md` and `wiki/log.md`.
- **Mixed team where BAs / QA edit too** → Relay (folder-level RBAC, real-time, free trial up to 3 users) or Obsidian Sync (paid, simpler but no per-folder ACL).
- **BAs / QA only need to read** → Obsidian Publish or a static-site export (MkDocs / Docusaurus). Decouples reading from the git layer entirely.
- **Strict access control between sub-teams** → Relay's folder-level RBAC is the only off-the-shelf option; otherwise build your own with multiple cloud-folder shares or static-site silos.

### The "BA without code access" wedge

A BA whose role doesn't include code-repo access cannot use sidecar topology (wiki co-located with code) directly. They have three options:

1. The team decides BA gets code-repo read access (administrative change, often not on the table)
2. The team migrates the wiki to a separate repo (sub-problem 3, option B or C below)
3. The team gives BA read-only access via Obsidian Publish or a static-site export (cheap if BA only consumes; harder if BA edits)

## Sub-problem 2: Multi-service structure

From [[wiki-sharing-research]], four canonical docs-as-code topologies:

| Topology | Where docs live | Pros | Cons |
|---|---|---|---|
| **Sidecar (co-located)** | With each service's code | Updates with code; CI lock-step; simple | Less flexible; weak cross-service overview |
| **Orthogonal (separate)** | Single docs repo, technical writers own | Editorial autonomy | "Few advantages, many drawbacks" — drift, duplication |
| **Federated** | Per-service docs co-located + central index aggregating them | Team autonomy + cross-service overview; matches Backstage TechDocs | Submodule / CI complexity; needs discipline |
| **Specialized** | Central docs for guides + code-generated reference per service | Pragmatic; eliminates duplication | Needs strong automation; most engineering |

### How claude-mem fits today

Today claude-mem is **sidecar**. One wiki per project. Works perfectly for:

- Solo dev / small team / single repo
- Monorepo with multiple services (each service = `wiki/modules/<service>/`)
- Mode B+C combination where a BA shares the same repo as the dev

It does **not** support:

- Federated cross-repo aggregation (multi-repo microservices org with one shared catalog)
- Specialized topology (auto-generated reference per service stitched into central guides)

Both would require a new skill (something like `wiki-federate`) that we explicitly chose to defer until a real user needs it.

### Recommendation per scenario

- **Monorepo + microservices in one repo** → keep claude-mem's default. Use Mode B+C with concerns matching team roles. Each service gets a `wiki/modules/<service>/` sub-tree.
- **Multi-repo + microservices, ≤5 services** → one claude-mem wiki per repo. Cross-link via wikilinks pointing at sibling project paths (the wiki layer doesn't enforce location). Relay or git-based sharing makes them co-discoverable.
- **Multi-repo + microservices, large org** → none of claude-mem's current skills handle this gracefully. Defer to Backstage / TechDocs-style infra alongside per-repo claude-mem instances.

## Sub-problem 3: Wiki location at init time

Maps onto the topology choice plus access constraints:

| Choice | What it means | Best for | Worst for |
|---|---|---|---|
| **Co-located with code** (current default) | `wiki/` next to `src/`, same repo, same access boundary | Devs working with AI coding agents; tight code-graph integration; simple setup | BAs without code-repo access; orgs with strict access tiers |
| **Sibling directory** | `wiki/` next to the code repo, but its own git repo | BAs need wiki access without code | Slight setup complexity; graphify needs cross-repo path resolution |
| **Separate repo entirely** | Standalone wiki repo (referenced from code via README pointer) | Strict access control; wiki needs its own deployment / publish pipeline | Drift risk; harder to keep in sync with code; harder to graphify-correlate |
| **Federated central wiki** | Each repo has its `wiki/`; a central wiki repo aggregates via submodules or CI | Microservices orgs at scale | Submodule pain; high discipline cost |

### Why claude-mem keeps co-located as the default

The `/wiki` skill currently scaffolds `wiki/` inside the project root. We're keeping this default for now because:

- It's the simplest path for solo devs and small teams (the majority of current usage).
- Graphify integration depends on the wiki being accessible to the same skill that's reading code.
- Hot cache + git auto-tracking + the SessionStart hook all assume the wiki is reachable from the cwd.
- Changing the default before we have field feedback risks breaking the simple case to support a hypothetical complex case.

### What would change the default

Add the location choice to `/wiki` SCAFFOLD if real users report:

- "I work with a BA who can't access the code repo" (the wedge above)
- "We have an access-tier policy that forbids wiki + code in the same repo"
- "We want to publish the wiki externally without exposing the code"

Until then, the location stays a **manual override** — a user who needs separate-repo can scaffold the wiki manually in a sibling directory and update their project's `AGENTS.md` to point there. claude-mem's skills handle absolute paths fine.

## Decision points awaiting field feedback

| Decision | Default today | What we're watching for |
|---|---|---|
| Wiki location at init | Co-located with code | Reports of BAs blocked by code-repo access policy |
| Multi-role sharing tool recommendation | None (user picks) | Common patterns from real teams (which tool wins for which team shape) |
| Multi-service / federated support | Sidecar only | Multi-repo orgs hitting cross-service navigation friction |
| Per-folder permissions / RBAC | Inherited from filesystem | Concrete request for sub-team access boundaries within one wiki |

Each row is a candidate for a future skill, scaffold-flow change, or new mode/concern. None ships preemptively.

## Quick guidance for users today

If you're trying to set up wiki sharing right now, here's the decision tree:

```
Are all wiki users developers with code-repo access?
├── Yes → git-based sharing (free, simple, fits the workflow)
│         keep co-located. claude-mem's default works.
└── No (BA / QA / non-dev users involved)
    ├── Do non-devs need to edit?
    │   ├── No (read-only is fine) → Obsidian Publish OR static site
    │   │                              keep co-located; publish a derived view
    │   └── Yes → Relay or Obsidian Sync
    │             still works co-located if non-devs have code access
    │             else → manually scaffold wiki in a sibling repo
    └── Strict access tiers (BA must NOT see code)
        → manually scaffold wiki in a separate repo
        → use Relay (folder RBAC) or git-based with branch perms
        → claude-mem's skills handle absolute wiki paths fine
```

## See also

- [[wiki-sharing-research]] — consolidated source citations
- [[SDLC Wiki Concerns]] — claude-mem's role-based folder model (Mode B + concerns)
- [[Spec-Kit and claude-mem]] — adjacent decision: per-feature spec workflow vs. persistent wiki
- `wiki-faq` skill — in-session help that can route users to this comparison
