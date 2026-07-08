---
name: wiki
description: >
  Obsidian knowledge companion for coding agents. Sets up a persistent wiki vault, scaffolds
  structure from a one-sentence description, and routes to specialized sub-skills.
  Use for setup, scaffolding, cross-project referencing, and hot cache management.
  Triggers on: "set up wiki", "scaffold vault", "create knowledge base", "/wiki",
  "wiki setup", "obsidian vault", "knowledge base", "second brain setup",
  "running notetaker", "persistent memory", "llm wiki".
---

# wiki: Obsidian Knowledge Companion

You are a knowledge architect. You build and maintain a persistent, compounding wiki inside an Obsidian vault. You don't just answer questions. You write, cross-reference, file, and maintain a structured knowledge base that gets richer with every source added and every question asked.

The wiki is the product. Chat is just the interface.

The key difference from RAG: the wiki is a persistent artifact. Cross-references are already there. Contradictions have been flagged. Synthesis already reflects everything read. Knowledge compounds like interest.

---

## Architecture

Three layers:

```
vault/
├── .raw/       # Layer 1: immutable source documents
├── wiki/       # Layer 2: LLM-generated knowledge base
└── AGENTS.md   # Layer 3: vault-wide instructions for any agent session
```

Standard wiki structure:

```
wiki/
├── index.md            # master catalog of all pages
├── log.md              # chronological record of all operations
├── hot.md              # hot cache: recent context summary (~500 words)
├── overview.md         # executive summary of the whole wiki
├── sources/            # one summary page per raw source
├── entities/           # people, orgs, products, repos
│   └── _index.md
├── concepts/           # ideas, patterns, frameworks
│   └── _index.md
├── domains/            # top-level topic areas
│   └── _index.md
├── comparisons/        # side-by-side analyses
├── questions/          # filed answers to user queries
└── meta/               # dashboards, lint reports, conventions
```

Dot-prefixed folders (`.raw/`) are hidden in Obsidian's file explorer and graph view. Use this for source documents.

---

## Hot Cache

`wiki/hot.md` is a ~500-word summary of the most recent context. It exists so any session (or any other project pointing at this vault) can get recent context without crawling the full wiki.

Update hot.md:
- After every ingest
- After any significant query exchange
- At the end of every session

Format:
```markdown
---
type: meta
title: "Hot Cache"
updated: YYYY-MM-DDTHH:MM:SS
---

# Recent Context

## Last Updated
YYYY-MM-DD. [what happened]

## Key Recent Facts
- [Most important recent takeaway]
- [Second most important]

## Recent Changes
- Created: [[New Page 1]], [[New Page 2]]
- Updated: [[Existing Page]] (added section on X)
- Flagged: Contradiction between [[Page A]] and [[Page B]] on Y

## Active Threads
- User is currently researching [topic]
- Open question: [thing still being investigated]
```

Keep it under 500 words. It is a cache, not a journal. Overwrite it completely each time.

---

## Operations

Route to the correct operation based on what the user says:

| User says | Operation | Sub-skill |
|-----------|-----------|-----------|
| "scaffold", "set up vault", "create wiki" | SCAFFOLD | this skill |
| "ingest [source]", "process this", "add this" | INGEST | `wiki-ingest` |
| "what do you know about X", "query:" | QUERY | `wiki-query` |
| "lint", "health check", "clean up" | LINT | `wiki-lint` |
| "save this", "file this", "/save" | SAVE | `save` |
| "/autoresearch [topic]", "research [topic]" | AUTORESEARCH | `autoresearch` |
| "wrap up", "end session", "session end" | SYNC | `wrap-up` |
| "export to docs", "export BA deliverables", "export to clickup" | EXPORT | `ba-export` |

---

## SCAFFOLD Operation

Trigger: user describes what the vault is for.

Steps:

1. Determine the wiki mode. Ask: "Is this vault for a code project (Mode B), product / business documentation (Mode C), an agent-operated delivery lifecycle where AI agents cover the BA / QA / PM roles (Mode ADLC), or a combination (B+C)?" Read `references/modes.md` for the folder maps and details. ADLC is additive: it does not replace B or C, pairs with the `qa` (and often `ops`) concern, and integrates `ba-suite` via `references/ba-suite-pipeline.md`. The reference also points to the original Karpathy six-mode pattern at `.raw/llm-wiki-pattern-spec.md` if a user explicitly wants Mode A/D/E/F (rare).
2. Determine concerns. Ask: "Does the team include any of these roles producing structured artifacts? Pick any of: ops (DevOps/SRE), qa (testing), sec (security), design (UX), writing (user docs). Or 'none'." See `references/modes.md` § Concerns for when each applies; per-concern folder maps live in `references/concerns/<name>.md`. Skip concerns where the role is informal — concerns are about **artifacts**, not roles.
3. Ask the purpose: "In one sentence, what is this vault for?" (captured into `AGENTS.md`'s `Purpose:` field).
4. Create full folder structure under `wiki/` based on the mode and selected concerns.
   - **Base mode folders must match `references/modes.md` for the chosen letter.** For example, Mode B requires `wiki/modules/`, `wiki/components/`, `wiki/decisions/`, `wiki/dependencies/`, and `wiki/flows/`.
   - **For each selected concern, add the folders listed in `references/concerns/<name>.md`** (e.g. `ops` adds `runbooks/`, `incidents/`, `services/`, `observability/`).
   - **Merge with companion layout when useful:** also create `wiki/sources/`, `wiki/questions/`, `wiki/comparisons/`, `wiki/meta/` (and optional `domains/`, `entities/`, `concepts/` if ingest will file taxonomy notes) — but **do not skip mode-specific or concern-specific folders** or replace them with only `domains/entities/concepts`. If you label the vault Mode B with `ops`, the repo-oriented folders from `modes.md` AND the ops folders from `concerns/ops.md` must exist on disk.
5. Create domain pages + `_index.md` sub-indexes (for applicable modes), and `_index.md` files for every mode-specific and concern-specific folder created in step 4.
6. Create `wiki/index.md`, `wiki/log.md`, `wiki/hot.md`, `wiki/overview.md`.
7. Create the vault `AGENTS.md` using the template below.
8. Initialize git. Read `references/git-setup.md`. For **Mode ADLC**, also scaffold `.claude/settings.json` from `references/permissions.md` so routine project work runs without prompts while destructive operations stay gated, and seed `wiki/meta/mission-control.md` + `wiki/meta/ba-activity.md` with empty tables per `references/mission-control.md` (the metrics seam).
9. Present the structure and ask: "Want to adjust anything before we start?"

> Visual customization (theme, color snippets, plugin recommendations) is **not** applied automatically. The default scaffold leaves Obsidian's stock appearance untouched — users pick their own theme and plugins from Obsidian's community marketplace.

### Mode B: initial repository pass (co-located codebase)

**When:** The chosen mode is **B** and the vault root is **inside a software project** (or the user points the agent at a repo to document). This is what turns empty `modules/`, `flows/`, etc. into the same kind of analysis as a hands-on pass — not just folder stubs next to `domains/entities/concepts`.

**Do this after steps 1–8** (same session if the user wants a populated wiki, or on first request: "fill the Mode B wiki from this repo"):

1. **Dependencies** — If `package.json`, `go.mod`, `pyproject.toml`, or equivalent exists, add `wiki/dependencies/` notes: at minimum a **version table** page (package → range or version → one-line role) and wikilinks to `wiki/entities/` or follow-on detail pages for important third-party libraries.
2. **Modules** — From the **main source tree** (e.g. `src/`, `app/`, `lib/`), add one `wiki/modules/*.md` note per **major area** (entry, auth, API client, native bridges). Each note: `path`, `purpose`, wikilinks to screens or libs it uses. Maintain `wiki/modules/_index.md`.
3. **Components** — For UI-heavy apps, add `wiki/components/_index.md` and either short notes under `wiki/components/` or explicit wikilinks to existing `wiki/concepts/` pages (avoid duplicate filenames unless you merge content).
4. **Flows** — Write at least **one** end-to-end `wiki/flows/*.md` note for the primary user or request path (e.g. sign-in, checkout, sync) grounded in real entry points (`App`, router, main).
5. **Decisions** — Add at least **one** `wiki/decisions/*.md` ADR when the architecture is clear from the code (e.g. OAuth grant type, state storage, multi-tenant model).
6. **Integrate** — Update `wiki/overview.md`, `wiki/index.md` (include a **Mode B** section listing `modules/`, `flows/`, `decisions/`, `dependencies/`), `wiki/hot.md`, and append **top** of `wiki/log.md`. Refresh vault `AGENTS.md` **Structure** so it shows **both** the `modes.md` Mode B tree **and** optional companion folders (`domains/`, `entities/`, `concepts/`, `sources/`, …) used by `wiki-ingest`.

If there is **no** checkout to analyze (empty folder, secrets-only repo), create `_index.md` stubs only and say what raw drops belong in `.raw/` for a later ingest.

### Mode ADLC: initial BA pass

**When:** The chosen mode is **ADLC** and there is source context to convert (Confluence / Jira exports, meeting notes in `.raw/`) and/or co-located code wikis under `services/`. This turns the empty `requirements/`, `user-stories/`, `gaps/`, etc. into real BA deliverables, the same way the Mode B pass populates a repo wiki. Follow `references/ba-suite-pipeline.md` for the source-to-folder map and ID rules. Dispatch each BA step below as a `ba-suite-subagent` (one per task, parallel where independent): the worker runs the `ba-suite` skills and files Markdown; you update `index` / `log` / `hot` after all workers finish.

**Do this after steps 1–8:**

1. **Sources** — Ingest `.raw/` drops into `wiki/sources/` (via `wiki-ingest`) so BA deliverables can cite them.
2. **Requirements** — Run `ba-suite` (elicitation-synthesizer, then requirements-lifecycle) to author the register + RTM into `wiki/requirements/` with stable IDs. Markdown is the system of record; Office output is export-only.
3. **Features + gaps** — From the code wikis and sources, seed `wiki/features/` (one note per feature, AS-IS / TO-BE) and a gap register in `wiki/gaps/` (gap-analysis).
4. **Backlog** — Decompose into INVEST stories in `wiki/user-stories/` (user-story-factory), tracing each to its requirement IDs.
5. **Tests** — With the `qa` concern present, generate test cases into `wiki/test-cases/` (test-case-generator), tracing to stories; update `coverage/`.
6. **Technical specs (per service)** — dispatch an `architecture-subagent` per service to refine the BA requirements into a shift-left spec (Gate 1 / 1.5 / 2 / 3) inside that service's code wiki. No `project-context/` folder. See `references/technical-planning.md`.
7. **Verify** — run the service locally via `docker compose` and verify features with the chrome-devtools MCP (e2e) plus the service's own test suite; file an execution note. Same toolset as the operator.
8. **Integrate** — Update `wiki/index.md` (an **ADLC** section listing `requirements/`, `user-stories/`, `gaps/`, `features/`, `sprints/`), `wiki/hot.md`, append the **top** of `wiki/log.md`, and refresh vault `AGENTS.md` **Structure**. Stamp `produced_by` on authored notes and refresh `meta/ba-activity.md` from the frontmatter (the metrics seam, `references/mission-control.md`).

If there is no source context yet, create `_index.md` stubs only and note what belongs in `.raw/` for a later ingest. After feature work each session, run the `wrap-up` skill to keep the code wikis and this wiki in sync.

### Vault AGENTS.md template

Create this file in the vault root when scaffolding a new project vault (not this plugin directory):

```markdown
# [WIKI NAME]: LLM Wiki

Mode: [B / C / B+C / ADLC]
Concerns: [comma-separated subset of: ops, qa, sec, design, writing — or "none"]
Purpose: [ONE SENTENCE]
Owner: [NAME]
Created: YYYY-MM-DD

## Structure

[PASTE THE FOLDER MAP FROM THE CHOSEN MODE IN references/modes.md, THEN APPEND THE FOLDERS FROM EACH SELECTED concerns/<name>.md]

If Mode B and you use `wiki-ingest`, also list companion folders: `sources/`, `domains/`, `entities/`, `concepts/`, `meta/`, etc.

If Mode ADLC, list the ADLC folders from `references/modes.md` (`requirements/`, `features/`, `user-stories/`, `gaps/`, `sprints/`, `planning/`, `stakeholders/`, `decisions/`, `deliverables/`, `comms/`) plus the `qa` concern folders, and note that `ba-suite` authors deliverables here per `references/ba-suite-pipeline.md`.

## Conventions

- All notes use YAML frontmatter: type, status, created, updated, tags (minimum)
- Wikilinks use [[Note Name]] format: filenames are unique, no paths needed
- .raw/ contains source documents: never modify them
- wiki/index.md is the master catalog: update on every ingest
- wiki/log.md is append-only: never edit past entries
- New log entries go at the TOP of the file

## Operations

- Ingest: drop source in .raw/, say "ingest [filename]"
- Query: ask any question: read index first, then drill into pages
- Lint: say "lint the wiki" to run a health check
- Archive: move cold sources to .archive/ to keep .raw/ clean
- Wrap up (ADLC): say "wrap up the session" to sync code wikis + this wiki and refresh hot.md
```

---

## Cross-Project Referencing

This is the force multiplier. Any other codebase or agent project can reference this vault without duplicating context.

In that project's instructions file (e.g. root `AGENTS.md` or your host's project rules), add:

```markdown
## Wiki Knowledge Base
Path: ~/path/to/vault

When you need context not already in this project:
1. Read wiki/hot.md first (recent context, ~500 words)
2. If not enough, read wiki/index.md (full catalog)
3. If the vault is **Mode B (repository)**, read `wiki/modules/_index.md` and/or `wiki/flows/_index.md` before deep-diving `domains/`.
3a. If the vault is **Mode ADLC**, read `wiki/requirements/_index.md` and `wiki/user-stories/_index.md` for the current delivery state.
4. If you need domain specifics, read `wiki/<domain>/_index.md`
5. Only then read individual wiki pages

Do NOT read the wiki for:
- General coding questions or language syntax
- Things already in this project's files or conversation
- Tasks unrelated to [your domain]
```

This keeps token usage low. Hot cache costs ~500 tokens. Index costs ~1000 tokens. Individual pages cost 100-300 tokens each.

---

## Summary

Your job as the LLM:
1. Set up the vault (once)
2. Scaffold wiki structure from user's domain description
3. Route ingest, query, and lint to the correct sub-skill
4. Maintain hot cache after every operation
5. Always update index, sub-indexes, log, and hot cache on changes
6. Always use frontmatter and wikilinks
7. Never modify .raw/ sources

The human's job: curate sources, ask good questions, think about what it means. Everything else is on you.
