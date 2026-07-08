# Workflow

How the 14 skills compose into real work. Read this when the user asks "what's the workflow?", "which skill when?", or "how does this fit together?"

## Two layers

claude-mem has **two parallel layers** in every project:

| Layer | What it captures | Lives in | Owned by |
|---|---|---|---|
| **Narrative** | Decisions, rationale, sources, concepts, meeting notes — the "why" | `wiki/` | Humans + skills (`wiki-ingest`, `save`, `wiki-lint`) |
| **Structural** (optional) | Code structure, calls, imports, communities — the "what" | `graphify-out/` | The `graphify-*` skills |

Use the narrative layer for any project (code, product docs, BA workflows). Add the structural layer only for code projects that benefit from a graph.

## The skills, grouped by purpose

### Setup / scaffolding

- **`/wiki`** — first-time scaffold. Asks the base mode (B / C / B+C / ADLC) and which concerns apply (`ops`, `qa`, `sec`, `design`, `writing`). Creates folder structure + vault `AGENTS.md`. Run once per project. See [[SDLC Wiki Concerns]] for the mode/concern model, and `skills/wiki/references/modes.md` § Mode ADLC for the agentic-delivery mode.
- **`/graphify-ingest`** — first-time code-graph build. AST + parallel semantic extraction via subagents. ~$1–3 in Sonnet tokens. Writes `graphify-out/` and `wiki/code/`.
- **`/graphify-update`** — incremental graph rebuild after a feature lands. Pennies (often $0 if changes are code-only). Preserves community labels via Jaccard matching.

### Knowledge management

- **`wiki-ingest`** — process a source (file, URL, image) into the wiki. Single-source mode is interactive; batch mode (3+ sources) dispatches parallel `wiki-ingest-subagent` workers. In an ADLC vault it routes BA deliverables to `ba-suite-subagent` and per-service specs to `architecture-subagent` instead of generic extraction.
- **`save`** — file the current chat conversation as a structured wiki note. Use after a useful exchange you don't want to lose.
- **`autoresearch`** — autonomous research loop on a topic. Searches the web, synthesizes, files into the wiki. Use for deep-dives.

### Export

- **`ba-export`** — export wiki BA deliverables to Office docs (`.docx` / `.xlsx`, PlantUML diagrams) in `.raw/exports/`, reusing the `ba-suite` skills via `ba-export-subagent`; optional ClickUp / Jira push. One-way (wiki to docs); the wiki stays canonical.

### Querying

- **`wiki-query`** — general "answer questions from the wiki." Reads hot cache → index → relevant pages. Routes code-structural questions to graphify when a graph exists. Auto-scales on large / ADLC vaults to grep-first + bounded recursion.
- **`/graphify-explain "X"`** — single-node lookup with full edge list. Cheapest first-step query when graph exists.
- **`/graphify-path "A" "B"`** — shortest path between two nodes.
- **`/graphify-query "..."`** — open-ended BFS/DFS traversal anchored at term-matched nodes.

### Maintenance

- **`wiki-lint`** — health check: orphan pages, dead links, frontmatter gaps, graph-layer drift (label mismatches, stale labels.json, missing community pages), and ADLC traceability / cross-wiki drift. Dispatches `wiki-lint-subagent` for vaults ≥20 pages.

### Session

- **`wrap-up`** — session-end sync (ADLC). On "wrap up" / "end session": checks git across `services/`, injects updates into the code wikis, reflects shipped features / gaps / requirements into the product wiki, refreshes `hot.md` + `log.md`. The `Stop` hook nudges it when `services/` changed.

### Service build (ADLC, internal sub-agents)

Not skills — the ADLC agent dispatches these at the service level during the per-service build pipeline:

- **`feature-builder`** — implements code + unit tests from the spec (reads the service's own AGENTS.md for commands).
- **`feature-tester`** — authors e2e specs from the feature's verification contract.
- **`feature-reviewer`** — reviews the diff (correctness, reuse, efficiency, test coverage); registers a review record in the wiki; returns APPROVED or CHANGES_REQUESTED.
- **`feature-verifier`** — runs the contract via `docker compose` + chrome-devtools MCP; logs pass/fail; never fixes bugs.
- **`doc-writer`** — writes user docs for built + verified features.

Sequenced build -> test -> review -> verify -> document; the agent commits. On CHANGES_REQUESTED the review loops back to builder + tester, then re-reviews (capped rounds). Stack-neutral (no hardcoded framework).

### Project context

- **`/project-profile`** — generate `AGENTS.md` for a brownfield project. Mechanical scan of build/test/lint configs (via `mechanical-scanner-subagent`) plus a short tribal-knowledge interview. Cross-tool format.

### Reference / authoring helpers

- **`obsidian-markdown`** — Obsidian Flavored Markdown reference (wikilinks, callouts, embeds, properties).
- **`obsidian-bases`** — `.base` files (Obsidian's database layer). For dynamic tables / dashboards.
- **`wiki-faq`** — this skill.

## End-to-end example: new code project

```
1. /wiki
   → ask "code project (B), product docs (C), or both? → B"
   → ask "concerns? → ops, qa"
   → scaffolds wiki/ with modules/, flows/, decisions/, dependencies/,
     runbooks/, incidents/, services/, observability/,
     test-plans/, test-cases/, bugs/, coverage/

2. bash bin/setup-graphify.sh /path/to/project
   → installs graphifyy, pins Python interpreter

3. /graphify-ingest
   → builds graph.json + wiki/code/ summaries (~$1-3)

4. (work happens — code changes, decisions made)

5. /save when something worth keeping comes out of chat
   wiki-ingest <file> when you drop a doc into .raw/

6. /graphify-update before commit (after substantial code change)
   → incremental rebuild, preserves cluster labels

7. wiki-lint every 10–15 ingests
   → health check, fix orphans / dead links / drift
```

## End-to-end example: ongoing maintenance

```
- New article in .raw/?       → wiki-ingest <file>
- New 3+ articles in .raw/?    → wiki-ingest (batch mode auto-dispatches subagents)
- Useful chat outcome?         → /save
- Deep dive needed?            → /autoresearch <topic>
- Code question (graph exists)? → wiki-query (routes to graphify) or /graphify-explain "X" directly
- Code question (no graph)?    → wiki-query (reads narrative layer)
- Feature done?                → /graphify-update before commit
- "Where are the orphans?"     → wiki-lint
- "Refresh the project profile?" → /project-profile (TBD, currently first-run only)
```

## When NOT to invoke a skill

- **Don't** run `/wiki` if `wiki/` already exists and is healthy. Use `wiki-lint` instead for a check-up.
- **Don't** run `/graphify-ingest` if `graphify-out/` exists and code changes are minor. Use `/graphify-update`.
- **Don't** run `wiki-ingest` for chat content. Use `save`.
- **Don't** run `autoresearch` for a single source you already have. Use `wiki-ingest`.

## Modes and concerns: which to pick?

Base mode:

- **B (Repository)** — code-focused: modules, flows, ADRs, dependencies. Devs.
- **C (Business / Project)** — product/business: stakeholders, decisions, deliverables, intel. BAs / PMs.
- **B+C** — both layers in one vault. Mixed teams.
- **ADLC** — agent-operated delivery lifecycle: agents cover BA/QA/PM, humans operate and gate; wiki is canonical, per-service specs in code wikis. Additive; pairs with `qa`.

Concerns (opt-in, additive):

- **ops** — DevOps / SRE: runbooks, incidents, services, observability
- **qa** — QA / Test: test-plans, test-cases, bugs, coverage
- **sec** — Security: threat-models, compliance, security-decisions
- **design** — UX: designs, user-research
- **writing** — Tech writers: user-docs, api-docs, tutorials

A small dev team picks `B`. A platform team picks `B + ops + qa`. A regulated SaaS picks `B+C + ops + qa + sec`. A 2-person agent-operated team picks `ADLC + qa`. See [[SDLC Wiki Concerns]] for design rationale.

## See also

- [[Claude-mem Hooks]] — what the SessionStart and Stop hooks do, cross-tool
- [[graphify-integration]] — the structural-layer architecture
- [[Project Profile Skill Suite]] — `/project-profile` design
- `README.md` — install and quickstart
