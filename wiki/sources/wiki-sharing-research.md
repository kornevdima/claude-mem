---
type: source
title: "Wiki Sharing Patterns Research (web synthesis)"
created: 2026-05-10
updated: 2026-05-10
source_type: web-research-synthesis
confidence: medium
tags:
  - wiki-sharing
  - team-collaboration
  - multi-role
  - microservices
  - docs-as-code
status: mature
related:
  - "[[Wiki Sharing Patterns]]"
key_claims:
  - "Obsidian Sync's team mode caps at 20 collaborators with no fine-grained permissions and no live cursors."
  - "Relay plugin offers real-time CRDT-based collaboration with folder-level RBAC; free up to 3 users."
  - "Docs-as-code has four canonical topologies: sidecar (co-located), orthogonal (separate), federated, specialized."
  - "Backstage TechDocs uses federated topology: per-service docs co-located + central index in cloud storage."
  - "GitHub blog acknowledges that 'managing lots of Markdown files can get overwhelming' for cross-team scaling."
  - "BAs without code-repo access need wiki sharing decoupled from code access — a real constraint not addressed by sidecar topology alone."
---

# Wiki Sharing Patterns Research

Consolidated source page for the wiki-sharing investigation that shaped [[Wiki Sharing Patterns]] (May 2026). Four parallel WebSearches plus four targeted WebFetches.

## Sources cited

### Multi-role access (Obsidian collaboration)

- **[Obsidian Help: Collaborate on a shared vault](https://help.obsidian.md/Collaborate+on+a+shared+vault)** — Official guide. Obsidian Sync supports shared vaults, but only with active Sync subscriptions for all collaborators.
- **[Obsidian Help: Syncing for teams](https://help.obsidian.md/teams/sync)** — Team-mode specifics. Max 20 collaborators per shared vault. **No fine-grained permissions** — all collaborators get vault-wide access except for the user-management capability (owner only). **No live cursors** — edits appear post-sync; conflict-merging on simultaneous writes.
- **[Relay — team collaboration in Obsidian](https://relay.md/)** — Third-party plugin. Real-time CRDT-based collaboration with live cursors. Folder-level RBAC at Starter tier ($6/user/mo) and above. Free for up to 3 users; $5/mo for up to 6 users. Premium tier ($18/mo) adds git-sync option. SSO at Starter+.
- **[Sync Obsidian Vault with Git for AI Collaboration — BSWEN](https://docs.bswen.com/blog/2026-03-23-sync-obsidian-vault-git-ai-collaboration/)** — Practitioner write-up of git-based vault sharing for AI-assisted teams. Dual-vault strategy: shared git vault for team work, private local vault for personal notes.
- **[Peerdraft Obsidian plugin](https://github.com/peerdraft/obsidian-plugin)** — Alternative to Relay. Folder-level sync with collaborators' vaults.
- **[Obsidian Forum: Shared vault with multiple users in GitHub](https://forum.obsidian.md/t/experiment-shared-vault-with-multiple-users-in-github/53726)** — Community experiment with git-based shared vault patterns.

### Docs-as-code topologies (the canonical taxonomy)

- **[Docs-as-code topologies — Fabrizio Ferri Benedetti (Passo)](https://passo.uno/docs-as-code-topologies/)** — Definitive write-up of the four patterns:
  - **Sidecar (co-located)** — docs with code; what claude-mem currently defaults to.
  - **Orthogonal (separate)** — central docs repo, code repos keep their own dev docs. *"Few advantages, many drawbacks."*
  - **Federated** — per-component docs in code repos + central aggregating repo. Used by Backstage, OpenTelemetry.
  - **Specialized** — central docs for guides + code-generated reference per component. Author's personal favorite; pragmatic balance.

### Microservices documentation strategy

- **[Backstage TechDocs Architecture](https://backstage.io/docs/features/techdocs/architecture)** — Confirms federated approach: per-service `mkdocs.yml` + markdown lives next to code; CI/CD generates static docs into central cloud storage; Backstage frontend stitches them.
- **[Thoughtworks: Monorepo vs. Multi-repo](https://www.thoughtworks.com/en-us/insights/blog/agile-engineering-practices/monorepo-vs-multirepo)** — Engineering trade-offs framing.
- **[CircleCI: Monorepo development practices](https://circleci.com/blog/monorepo-dev-practices/)** — Visibility, collaboration, shared tooling arguments for monorepo + co-located docs.
- **[Aviator: Monorepo Guide for Microservices](https://www.aviator.co/blog/monorepo-a-hands-on-guide-for-managing-repositories-and-microservices/)** — Practical guidance for managing microservices in a monorepo.
- **[Kinsta: Monorepo vs. Multi-Repo strategies](https://kinsta.com/blog/monorepo-vs-multi-repo/)** — Pros/cons summary.
- **[Spectro Cloud: AI and the year of the monorepo (2026)](https://www.spectrocloud.com/blog/will-ai-turn-2026-into-the-year-of-the-monorepo)** — Argues that AI agentic workflows favor monorepo structure with one canonical set of agent instructions at the top level.

### Cross-functional knowledge bases

- **[Slite: 12 Best Knowledge Base Software for 2026](https://slite.com/learn/knowledge-base-softwares)** — Industry survey. Confluence is positioned as the standard with Jira integration; Bloomfire as cross-functional silo-eliminator.
- **[Glean: Company knowledge base](https://www.glean.com/blog/company-knowledge-base)** — Argues cross-functional unified hub raises productivity ~50%.
- **[NIX United: Cross-functional teams](https://nix-united.com/blog/cross-functional-teams-in-software-development-principles-and-examples/)** — Defines the cross-functional collaboration model — engineers, QA, designers, DevOps, BAs, product all working in one unit.

## Method

Conducted 2026-05-10:

1. Four parallel WebSearches:
   - obsidian vault sharing team collaboration git multi-user access control 2026
   - engineering wiki microservices monorepo documentation strategy one vs multiple 2026
   - documentation co-located code repository vs separate docs repo trade-offs 2026
   - cross-functional team knowledge base business analyst QA access engineering documentation 2026
2. Four targeted WebFetches:
   - passo.uno docs-as-code topologies (full taxonomy)
   - help.obsidian.md teams/sync (Obsidian Sync team mode specifics)
   - relay.md (Relay plugin features and pricing)
   - backstage.io techdocs architecture (cross-team / multi-service pattern)

Confidence rated **medium** — doc-level analysis with strong source diversity, but no hands-on test of any sharing tool. For an actual rollout decision, run a small pilot with the chosen sharing approach before committing the team.

## Key extracted claims (with source pointer)

| Claim | Source |
|---|---|
| Obsidian Sync team-mode caps at 20 collaborators, has no fine-grained per-folder permissions, no live cursors | [Obsidian Help](https://help.obsidian.md/teams/sync) |
| Relay supports real-time CRDT-based collaboration with folder-level RBAC | [Relay homepage](https://relay.md/) |
| Four canonical docs-as-code topologies: sidecar, orthogonal, federated, specialized | [Passo: Docs-as-code topologies](https://passo.uno/docs-as-code-topologies/) |
| Backstage TechDocs uses federated topology — per-service docs co-located, central frontend aggregates from cloud storage | [Backstage TechDocs Architecture](https://backstage.io/docs/features/techdocs/architecture) |
| Orthogonal (separate docs repo) topology has "few advantages, many drawbacks" — creates duplication, weakens dev relationship | [Passo](https://passo.uno/docs-as-code-topologies/) |
| Specialized topology (central guides + per-component reference) is the author's personal favorite for cross-functional projects | [Passo](https://passo.uno/docs-as-code-topologies/) |
| Monorepo + co-located docs is increasingly favored by AI agentic workflows because of single canonical instruction set at root | [Spectro Cloud (2026)](https://www.spectrocloud.com/blog/will-ai-turn-2026-into-the-year-of-the-monorepo) |
| BAs without code-repo access cannot use sidecar topology directly — they need wiki access decoupled from code access | Synthesis (not in any single source; deduced from cross-cutting constraints) |

## Synthesis output

See [[Wiki Sharing Patterns]] for the design synthesis: three sub-problems (multi-role access, multi-service structure, wiki location), options for each with trade-off matrices, and recommendations awaiting field feedback before claude-mem changes any defaults.
