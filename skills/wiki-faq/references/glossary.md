# Glossary

claude-mem terminology. Use this when the user asks "what is X?" and X is a project term.

## Wiki and vault

**Wiki**
The agent-owned knowledge base in `wiki/`. Markdown files with YAML frontmatter, organized into subfolders by content type (concepts, decisions, sources, modules, etc., depending on mode). Cross-referenced by `[[wikilink]]` syntax.

**Vault**
The directory that contains both `wiki/` and `.raw/`. Usually the same as the project root (so the same folder serves as plugin source + vault + git repo simultaneously).

**`.raw/`**
Immutable source documents. PDFs, articles, transcripts, exports, etc. Agents never modify files in `.raw/` — they read and produce `wiki/` content based on them. New sources are added by dropping files in `.raw/` and running `wiki-ingest`.

**Hot cache**
`wiki/hot.md`. A ~500-word recent-context summary, loaded into the agent's context at every session start. It tells the next session what was happening recently without crawling the full wiki. Updated at the end of every session that touched `wiki/`. The `Stop` hook prompts for the update.

## Modes and concerns

**Base mode**
The vault's primary scaffold shape. One of:
- **B (Repository)** — code-focused: `modules/`, `components/`, `decisions/`, `dependencies/`, `flows/`. For developers.
- **C (Business / Project)** — product/business: `stakeholders/`, `decisions/`, `deliverables/`, `intel/`, `comms/`. For BAs / PMs.
- **B+C** — both, in one vault. Mixed teams.
- **ADLC (Agentic Development Life Cycle)** — additive mode for agent-operated delivery: `requirements/`, `features/`, `user-stories/`, `gaps/`, `sprints/`, `planning/` plus the Mode C folders. Agents cover BA / QA / PM (via `ba-suite-subagent` + `architecture-subagent`); humans operate and gate. Wiki is canonical; per-service specs live in code wikis under `services/`. Pairs with the `qa` concern. See `skills/wiki/references/modes.md` § Mode ADLC.

The `wiki` skill asks for the mode at scaffold time. Once chosen, mode-specific folders should always exist on disk for the labeled vault.

**Concerns**
Opt-in folder kits added on top of the base mode for specific SDLC roles. Five available:
- `ops` — DevOps / SRE
- `qa` — QA / Test
- `sec` — Security
- `design` — UX
- `writing` — Technical writers

Each adds 2–4 folders with their own frontmatter shapes. See [[SDLC Wiki Concerns]] for design rationale and `skills/wiki/references/concerns/<name>.md` for per-concern detail.

## Graph layer

**graphify**
The Python library (`graphifyy` on PyPI) that builds a structural code graph from a source tree. AST extraction (free) plus optional LLM-driven semantic extraction (parallel subagents). claude-mem wraps it via `/graphify-ingest`, `/graphify-update`, and three query skills.

**AST**
Abstract Syntax Tree. Deterministic representation of code structure produced by tree-sitter parsers. Captures imports, function definitions, calls, class hierarchies. Free to compute; no LLM involved.

**Semantic extraction**
LLM-driven graph fragment that captures relationships AST can't see: shared data assumptions, indirect dependencies, conceptual similarity, doc-to-code links. Each chunk runs in a `graphify-extract-subagent` for parallelism.

**Community**
A cluster of related nodes detected by Louvain or Leiden algorithm. Numeric ID assigned at clustering time. claude-mem labels meaningful communities (≥3 members) with human-readable names.

**Label**
2–5 word human-readable name for a community. Stored in `graphify-out/labels.json`. Preserved across `/graphify-update` runs via Jaccard similarity matching against the previous run's communities (threshold 0.6).

**Edge confidence**
Every edge in the graph carries a confidence tag and numeric score:
- `EXTRACTED` (1.0) — explicit in source: a literal call, citation, or import
- `INFERRED` (0.4–0.9) — reasonable inference from context
- `AMBIGUOUS` (0.1–0.3) — uncertain; marked rather than omitted

Lets you trace the audit: "what was actually in the source vs. what the model inferred?"

**God node**
A high-degree node — many incoming and outgoing edges. Often a core abstraction (`AppDelegate`, `getOAuthConfig`). The graph report surfaces the top god nodes.

## Architecture pieces

**Skill**
A reusable workflow defined in `skills/<name>/SKILL.md` with YAML frontmatter (`name`, `description`). Loaded automatically by Claude Code, Cursor, Codex, OpenCode, Copilot when their respective host registers it. Triggered by description-matching against user input or by an explicit slash command.

**Subagent**
A worker definition in `agents/<name>-subagent.md` dispatched by skills via the Agent tool with `subagent_type: "<name>-subagent"`. Runs in its own isolated context and returns a single message — used for parallel batch work and context isolation. Four exist: `wiki-ingest-subagent`, `wiki-lint-subagent`, `graphify-extract-subagent`, `mechanical-scanner-subagent`.

**Hook**
A lifecycle event handler. claude-mem ships hooks for `SessionStart` (load hot cache) and `Stop` (prompt to refresh hot cache when wiki changed) across three host formats: `hooks/hooks.json` (Claude Code), `.cursor/hooks.json` (Cursor), `.github/hooks/hooks.json` (Copilot). See [[Claude-mem Hooks]].

**Manifest**
`.raw/.manifest.json` (wiki layer) or `graphify-out/manifest.json` (graph layer). Tracks what's been ingested / processed so subsequent runs can skip unchanged inputs. Hash-based change detection.

## Operations

**Scaffold**
First-time vault setup. Run `/wiki`. Creates folder structure, `index.md`, `log.md`, `hot.md`, vault `AGENTS.md`.

**Ingest**
Process a source document into the wiki. Run `wiki-ingest <file>` for a single source, or `wiki-ingest` with multiple files for batch mode (3+ sources auto-dispatch parallel subagents).

**Lint**
Health check the wiki: orphan pages, dead links, frontmatter gaps, graph-layer drift. Run `wiki-lint`. Dispatches the `wiki-lint-subagent` for vaults ≥20 pages.

**Update (graphify)**
Incremental rebuild after code changes. Run `/graphify-update`. Detects changed files, re-extracts only those, merges into existing graph, preserves community labels via Jaccard matching.

## See also

- [[SDLC Wiki Concerns]] — full design rationale for modes + concerns
- [[graphify-integration]] — structural-layer architecture
- [[Claude-mem Hooks]] — hook design across hosts
- [[LLM Wiki Pattern]] — Karpathy's original pattern (foundation)
